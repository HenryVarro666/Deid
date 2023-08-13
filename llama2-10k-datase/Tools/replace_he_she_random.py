import re
from names_dataset import NameDataset
import random
import pandas as pd

def replace_pronoun_with_random_name(sentence, all_names):
    # 使用一个替换函数为"she"和"She"进行替换
    random_name = random.choice(all_names)
    # sentence = re.sub(r'(\W?)(she|She|SHE)(\W?)', lambda match: match.group(1) + random_name + match.group(3), sentence)
    sentence = re.sub(r'(\b|^)(she|She|SHE|SHe|sHe|shE)(\b|$)', lambda match: match.group(1) + random_name + match.group(3), sentence)


    # 使用一个替换函数为"he"和"He"进行替换
    random_name = random.choice(all_names)
    sentence = re.sub(r'(\b|^)(he|He|HE|hE|Him|him|HIM)(\b|$)', lambda match: match.group(1) + random_name + match.group(3), sentence)
    


    return sentence



# # 实例化NameDataset对象
# nd = NameDataset()

# # 获取所有名字
# all_names = list(nd.first_names)

# # 仅保留由英文字母组成的名字
# all_names = [name for name in all_names if re.match(r'^[a-zA-Z\s-]+$', name)]

# # 读取CSV文件
# file_path = 'sentences_he_she.csv'
# df = pd.read_csv(file_path)

# # 对 "sentences" 列进行处理
# df['sentences'] = df['sentences'].apply(lambda x: replace_pronoun_with_random_name(x, all_names))

# # 如果需要，保存更改后的DataFrame到新的CSV文件
# df.to_csv('sentences_replaced.csv', index=False)



# 实例化NameDataset对象
nd = NameDataset()

# 获取所有名字
all_names = list(nd.first_names)

# 仅保留由英文字母组成的名字
all_names = [name for name in all_names if re.match(r'^[a-zA-Z\s-]+$', name)]

# 读取CSV文件
file_path = 'sentences_he_she.csv'
df = pd.read_csv(file_path)

# 创建一个新的列"replaced"，其中包含替换后的句子
df['replaced'] = df['sentences'].apply(lambda x: replace_pronoun_with_random_name(x, all_names))

# 保存更改后的DataFrame到一个新的CSV文件
new_file_path = 'sentences_random.csv'
df.to_csv(new_file_path, index=False)