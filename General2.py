import os
import torch

from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from tqdm  import tqdm

from transformers import AutoTokenizer, AutoModelForCausalLM


#
input_directory = './testing-PHI-Gold-fixed'
model = "tiiuae/falcon-7b"
model_name_part = model.split("/")[-1]
output_path = "./rewrite_{}_general2".format(model_name_part)




# input_directory = './testing-PHI-Gold-fixed'
# model = "LLaMA1_7B"
# # model = "LLaMA2_7B"
# model_name_part = model
# output_path = "./rewrite_{}_genral2".format(model_name_part)




class QAMT0:
    model_path = model

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_path,trust_remote_code=True).to("cuda")
        # self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_path,trust_remote_code=True).to("cuda")

    def extract(self, text:str, question:str, iterate:bool=False) -> []:
        try:
            inputs  = self.tokenizer.encode("Answer this question – {} – Q : {} ".format(text, question), return_tensors="pt").to("cuda")
            outputs = self.model.generate(inputs)
            result = self.tokenizer.decode(outputs[0])
            result = result.replace("<pad>", "").replace("</s>", "").strip()
            values = result.split(', ')

            results  = []
            new_text = text
            for value in values:
                value = value.strip()
                if len(value) > 0:
                    if value not in new_text:
                        # Found a hallucination
                        iterate = False
                        break
                    results.append(value)
                    new_text = new_text.replace(value, "").replace("  ", " ").replace(" ,", ",").replace(" .", ".").replace("() ", "").replace(" ()", "").replace('(', '').replace(')', '')

            if iterate:
                results += self.extract(new_text, question, iterate)
            return results
        except TypeError as e:
            print('TypeError', filename)
            return ['TypeError']

qamt0 = QAMT0()

source_dir = input_directory
target_dir = output_path

# create target directory if not exist
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

if os.path.isfile(target_dir):# 如果原先有生成的文本就先删除
    os.remove(target_dir)

# iterate over files in the source directory
for filename in tqdm(sorted(os.listdir(source_dir))):
    # checking if it is a file
    if os.path.isfile(os.path.join(source_dir, filename)):
        print("Processing file:", filename)
        # load the XML file
        with open(os.path.join(source_dir, filename), 'r') as f:
            soup = BeautifulSoup(f, features="xml")
            # extract the text content
            text = soup.find('TEXT').text
            # extract the answers to the 7 questions
            result1 = qamt0.extract(text, "What are the names?", iterate=True)
            result2 = qamt0.extract(text, "Who are the professions?", iterate=True)
            result3 = qamt0.extract(text, "What are the locations?", iterate=True)
            result4 = qamt0.extract(text, "What are ages?", iterate=True)
            result5 = qamt0.extract(text, "What are dates?", iterate=True)
            result6 = qamt0.extract(text, "What are contacts?", iterate=True)
            result7 = qamt0.extract(text, "What are IDs?", iterate=True)
            result8 = qamt0.extract(text, "What are the phone numbers?", iterate=True)
            # replace the matching characters with [redacted]
            for result in [result1, result2, result3, result4, result5, result6, result7, result8]:
                for r in result:
                    # print(r)
                    if '(' or ')' in r:
                      text = text.replace(r, '[redacted]')
                    else:
                      pattern = r'\b{}\b'.format(r)
                      text = re.sub(pattern, '[redacted]', text)
            # save the anonymized text to a new file
            with open(os.path.join(target_dir, filename[:-4] + "_anonymized.txt"), 'w') as f:
                f.write(text)