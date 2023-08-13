from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch
import os
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

rewrite_path = "./rewrite_llama2_explicit"

# assign directory
directory = './testing-PHI-Gold-fixed'

if not os.path.exists(rewrite_path):
    os.makedirs(rewrite_path)

# Load falcon-7b model
model = "tiiuae/falcon-7b"

tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto",
)




list_of_text_contents = []
list_of_files = []

# iterate over files in
# that directory
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
    prompt = "Please anonymize the following clinical note. Specifically, replace all the following information with the term “[redacted]”: redact any strings that might be a name or acronym or initial, redact any strings separated by the \/ symbol, redact patients' names, doctors' names and the strings in front of M.D. or after Dr., redact pager names and medical staff names, redact any strings that look like something years old or age 37, redact any dates and IDs and numbers and record dates, redact locations and addresses and clinic names, redact professions and ages and contacts, redact any acronyms and initials.: \n" + list_of_text_contents[i]

    # inputs = tokenizer.encode(prompt, return_tensors='pt', truncation=True, max_length=2048)

    # Run the model

    sequences = pipeline(
        # inputs,
        prompt,
        max_length=4096,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id,
    )
    # for seq in sequences:
    #     print(f"Result: {seq['generated_text']}")

    # rewrite_finding = tokenizer.decode(seq[0], skip_special_tokens=True)
    rewrite_finding = sequences[0]['generated_text']

    rewrite_file = os.path.join(rewrite_path, list_of_files[i] + "_anonymized.txt")

    with open(rewrite_file, "w") as f:
        f.write(rewrite_finding)

    # print("-----------第" + str(i + 1) + "个\n-----------")
    # # print("-----------My prompt " + "\n-----------")
    # # print(prompt)
    # print("-----------Anonymized " + "\n-----------")
    # print(rewrite_finding)

