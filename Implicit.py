from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch
import os
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

# # Load falcon-7b model
# #
# input_directory = './testing-PHI-Gold-fixed'
# # model = "tiiuae/falcon-7b"
# model = "google/flan-t5-base"
# model_name_part = model.split("/")[-1]
# output_path = "./rewrite_{}_implicit".format(model_name_part)
# # 修改以上model和input_directory


# Load Local model
#
input_directory = './testing-PHI-Gold-fixed'
model = "LLaMA1_7B"
# model = "LLaMA2_7B"
model_name_part = model
output_path = "./rewrite_{}_implicit".format(model_name_part)

# 修改以上model和input_directory




rewrite_path = output_path
directory = input_directory

if not os.path.exists(rewrite_path):
    os.makedirs(rewrite_path)



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
    prompt = "Please anonymize the following text: \n" + list_of_text_contents[i]  
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

