

from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch
import os


from bs4 import BeautifulSoup
import time
from tqdm import tqdm


# input_directory = './testing-PHI-Gold-fixed'
# model = "tiiuae/falcon-7b"
# model_name_part = model.split("/")[-1]
# output_path = "./rewrite_{}_explicit2".format(model_name_part)


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

input_directory = './testing-PHI-Gold-fixed'
model = "Llama-2-7b-chat-hf"
# model = "LLaMA2_7B"
model_name_part = model
output_path = "./rewrite_{}_explicit2".format(model_name_part)

Explicit_prompt= "Please anonymize the following clinical note. Specifically, replace all the following information with the term “[redacted]”: redact any strings that might be a name or acronym or initial, redact any strings separated by the \/ symbol, redact patients' names, doctors' names and the strings in front of M.D. or after Dr., redact pager names and medical staff names, redact any strings that look like something years old or age 37, redact any dates and IDs and numbers and record dates, redact locations and addresses and clinic names, redact professions and ages and contacts, redact any acronyms and initials.: \n"

rewrite_path = output_path
directory = input_directory

if not os.path.exists(rewrite_path):
    os.makedirs(rewrite_path)

tokenizer = AutoTokenizer.from_pretrained(model)
model = AutoModelForCausalLM.from_pretrained(model,trust_remote_code=True).to(device)

list_of_text_contents = []
list_of_files = []

# iterate over files in that directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        print(os.path.basename(os.path.normpath(f))[:-4])
        list_of_files.append(os.path.basename(os.path.normpath(f))[:-4])
        with open(f) as fp:
            soup = BeautifulSoup(fp, features="xml")
            text = soup.find('TEXT')
            text_content = text.contents[0]
            list_of_text_contents.append(text_content)

for i in tqdm(range(len(list_of_text_contents)), desc="Processing files"):
    prompt = Explicit_prompt + list_of_text_contents[i]
    inputs = tokenizer.encode(prompt, return_tensors='pt', truncation=True, max_length=2048).to(device)


        # Run the model
    output = model.generate(inputs)
    rewrite_finding = tokenizer.decode(output[0], skip_special_tokens=True)
    rewrite_file = os.path.join(rewrite_path, list_of_files[i] + "_anonymized.txt")

    with open(rewrite_file, "w") as f:
        f.write(rewrite_finding)

    print("-----------Anonymized " + "\n-----------")
    print(output)

