import os
#os.environ["CUDA_VISIBLE_DEVICES"] = "3,4,7"
# os.environ["CUDA_VISIBLE_DEVICES"] = "3"

from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from tqdm  import tqdm

from transformers import AutoTokenizer, AutoModelForCausalLM

# inputs = tokenizer("A step by step recipe to make bolognese pasta:", return_tensors="pt")
# outputs = model.generate(**inputs)
# print(tokenizer.batch_decode(outputs, skip_special_tokens=True))

class QAMT0:
    # MODEL_CHECKPOINT = "google/flan-t5"
    MODEL_CHECKPOINT = "tiiuae/falcon-7b"


    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL_CHECKPOINT)
        self.model = AutoModelForCausalLM.from_pretrained(self.MODEL_CHECKPOINT,trust_remote_code=True).to("cuda")


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

# assign directories
# source_dir = '/content/drive/MyDrive/CAID/Data/DeID/testing-PHI-Gold-fixed'
# target_dir = '/content/drive/MyDrive/CAID/Data/DeID/rewrite_bloom'


source_dir = './testfolder'

# source_dir = './testing-PHI-Gold-fixed'
target_dir = './rewrite_falcon_general_batch'

# source_dir = './testfolder'
# target_dir = './testoutput'

# create target directory if not exist
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# if os.path.isfile(target_dir):# 如果原先有生成的文本就先删除
#     os.remove(target_dir)



# 从给定的文本中提取批次
def create_batches(text, batch_size):
    # 这里你可以选择合适的方式来分割文本，例如按句子或段落
    # 下面是一个简单的按固定字符数分割的示例
    return [text[i:i+batch_size] for i in range(0, len(text), batch_size)]

# 批次大小（你可以根据需求调整此值）
batch_size = 1

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

            # 创建批次
            batches = create_batches(text, batch_size)

            # 逐个处理批次
            anonymized_text = ""
            for batch in batches:
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
                            batch = batch.replace(r, '[redacted]')
                        else:
                            pattern = r'\b{}\b'.format(r)
                            batch  = re.sub(pattern, '[redacted]', batch)
                
                anonymized_text += batch  

            # save the anonymized text to a new file
            with open(os.path.join(target_dir, filename[:-4] + "_anonymized.txt"), 'w') as f:
                f.write(anonymized_text)