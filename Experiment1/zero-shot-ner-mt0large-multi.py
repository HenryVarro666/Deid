# CUDA_VISIBLE_DEVICES=3,4,7 python3 zero-shot-ner-mt0large-multi.py

# export CUDA_VISIBLE_DEVICES = '0,1,2,3,4,5,6,7'

import os
#os.environ["CUDA_VISIBLE_DEVICES"] = "3,4,7"
os.environ["CUDA_VISIBLE_DEVICES"] = "3"

from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from accelerate import Accelerator
import sys

sys.setrecursionlimit(50000)

# accelerator = Accelerator(device_placement="cuda") 
# accelerator = Accelerator(device_index=[3, 4, 7])  # use GPUs 4, 5, and 8
 
# accelerator = Accelerator(device_placement="cuda:8")  # 指定第8块显卡
# device = accelerator.device


class QAMT0:
    MODEL_CHECKPOINT = "bigscience/mt0-large"
    
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL_CHECKPOINT)
        # self.model     = AutoModelForSeq2SeqLM.from_pretrained(self.MODEL_CHECKPOINT,torch_dtype="auto", device_map="auto")
        #self.model = accelerator.prepare(AutoModelForSeq2SeqLM.from_pretrained(self.MODEL_CHECKPOINT)).to("cuda")
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.MODEL_CHECKPOINT).to("cuda")

        
    def extract(self, text:str, question:str, iterate:bool=False) -> []:
        try:
            inputs  = self.tokenizer.encode("Answer this question – {} – Q : {} ".format(text, question), return_tensors="pt").to("cuda")
            # inputs  = self.tokenizer.encode("Answer this question – {} – Q : {} ".format(text, question), return_tensors="pt").to(accelerator.device)
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
                    new_text = new_text.replace(value, "[redacted]")
                    
            if iterate:
                results += self.extract(new_text, question, iterate)
            return results
        except TypeError as e:
            print('TypeError', filename)
            return 'TypeError'

qamt0 = QAMT0()

# assign directories
source_dir = '/home/caocao/zeroshot/testing-PHI-Gold-fixed'
target_dir = '/home/caocao/zeroshot/anonymized1'
# create target directory if not exist
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

if os.path.isfile(target_dir):# 如果原先有生成的文本就先删除
    os.remove(target_dir)

# iterate over files in the source directory
for filename in os.listdir(source_dir):
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
            # replace the matching characters with [redacted]
            for result in [result1, result2, result3, result4, result5, result6, result7]:
                for r in result:
                    if r in text:
                        text = text.replace(r, "[redacted]")
            # save the anonymized text to a new file
            with open(os.path.join(target_dir, filename[:-4] + "_anonymized.txt"), 'w') as f:
                f.write(text)

