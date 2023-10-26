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
# output_path = "./rewrite_{}_implicit2".format(model_name_part)

input_directory = './Understand_Test'
# model = "LLaMA1_7B"
model = "Llama-2-7b-chat-hf"
model_name_part = model
output_path = "./rewrite_{}_implicit_understand".format(model_name_part)

Implicit_prompt = "Please anonymize the following text: \n"



rewrite_path = output_path
directory = input_directory

if not os.path.exists(rewrite_path):
    os.makedirs(rewrite_path)



tokenizer = AutoTokenizer.from_pretrained(model)
model = AutoModelForCausalLM.from_pretrained(model,trust_remote_code=True).to("cuda")




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
    prompt = Implicit_prompt + list_of_text_contents[i]  
    inputs = tokenizer.encode(prompt, return_tensors='pt', truncation=True, max_length=2048)

    # Run the model
    output = model.generate(inputs)
    rewrite_finding = tokenizer.decode(output[0], skip_special_tokens=True)
    rewrite_file = os.path.join(rewrite_path, list_of_files[i] + "_anonymized.txt")

    with open(rewrite_file, "w") as f:
        f.write(rewrite_finding)

    # print("-----------第" + str(i + 1) + "个\n-----------")
    # # print("-----------My prompt " + "\n-----------")
    # # print(prompt)
    # print("-----------Anonymized " + "\n-----------")
    # print(rewrite_finding)

