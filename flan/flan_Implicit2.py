from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import T5Tokenizer, T5ForConditionalGeneration
import transformers
import torch
import os
from bs4 import BeautifulSoup
import time
from tqdm import tqdm


input_directory = './testing-PHI-Gold-fixed'
# model = "tiiuae/falcon-7b"
model = "google/flan-t5-base"
model_name_part = model.split("/")[-1]
output_path = "./rewrite_{}_implicit2".format(model_name_part)


Implicit_prompt = "Please anonymize the following text: \n"



rewrite_path = output_path
directory = input_directory

if not os.path.exists(rewrite_path):
    os.makedirs(rewrite_path)

tokenizer = T5Tokenizer.from_pretrained(model)
model = T5ForConditionalGeneration.from_pretrained(model, device_map="auto")

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
    prompt = Implicit_prompt + list_of_text_contents[i]
    inputs = tokenizer(prompt, return_tensors="pt").input_ids.to("cuda")
    output = model.generate(inputs)
    rewrite_finding = tokenizer.decode(output[0], skip_special_tokens=True)
    rewrite_file = os.path.join(rewrite_path, list_of_files[i] + "_anonymized.txt")

    with open(rewrite_file, "w") as f:
        f.write(rewrite_finding)

    print("-----------Anonymized " + "\n-----------")
    print(output)
