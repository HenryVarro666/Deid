import pandas as pd
import re

# 定义文件名
input_file1 = 'Flitered_Reddit_Data_Comments.csv'
input_file2 = 'Flitered_Twitter_Data_Comments.csv'


# 读取CSV文件
data1 = pd.read_csv(input_file1)
data2 = pd.read_csv(input_file2)

# 定义一个函数来检查字符串中单词 'he' 出现的次数
def count_he(text):
    return len(re.findall(r'\bhe\b', str(text), flags=re.IGNORECASE))

def count_she(text):
    return len(re.findall(r'\bshe\b', str(text), flags=re.IGNORECASE))

# 使用该函数计算 'clean_comment' 列中单词 'he' 出现的总次数
total_count1 = data1['clean_comment'].apply(count_he).sum()
total_count2 = data2['clean_text'].apply(count_he).sum()

total_count3 = data1['clean_comment'].apply(count_she).sum()
total_count4 = data2['clean_text'].apply(count_she).sum()



print(f"Total number of occurrences of the word 'he' in Reddit: {total_count1}")
print(f"Total number of occurrences of the word 'he' in Twitter: {total_count2}")
print(f"Total number of occurrences of the word 'she' in Reddit: {total_count3}")
print(f"Total number of occurrences of the word 'she' in Reddit: {total_count4}")

