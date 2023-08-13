import re
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


# 读取CSV文件，获取名字
name_file_path = 'normal_names.csv'
names_df = pd.read_csv(name_file_path, header=None)
all_names = names_df[0].tolist()

# 读取包含句子的CSV文件
file_path = 'sentences_he_she.csv'
df = pd.read_csv(file_path)

# 创建一个新的列"replaced"，其中包含替换后的句子
df['replaced'] = df['sentences'].apply(lambda x: replace_pronoun_with_random_name(x, all_names))

# 保存更改后的DataFrame到一个新的CSV文件
new_file_path = 'sentences_normal.csv'
df.to_csv(new_file_path, index=False)