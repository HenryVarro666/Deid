import pandas as pd
import re

# 定义文件名
# input_file = 'sentences_normal.csv'

input_file = 'sentences_random.csv'


columns = ['sentences', 'replaced']

# 读取CSV文件
data = pd.read_csv(input_file)

# 定义一个函数来检查字符串中单词 'he / she' 出现的次数

def count_and_locate_he(text):
    return re.findall(r'\b(he|He|HE|Him|him)\b', str(text), flags=re.IGNORECASE)

def count_and_locate_she(text):
    return re.findall(r'\b(she|She|SHE)\b', str(text), flags=re.IGNORECASE)

for col in columns:
    occurrences_he = data[col].apply(count_and_locate_he)
    occurrences_she = data[col].apply(count_and_locate_she)

    total_count_he = sum(map(len, occurrences_he))
    total_count_she = sum(map(len, occurrences_she))

    print(f"Total number of occurrences of the word 'he' in {col}: {total_count_he}")
    print(f"Total number of occurrences of the word 'she' in {col}: {total_count_she}")

    if col == 'replaced':
        print("Occurrences of 'he':")
        for index, occurrences in occurrences_he.iteritems():
            if occurrences:
                print(f"Index {index}: {data.loc[index, col]}")

        print("Occurrences of 'she':")
        for index, occurrences in occurrences_she.iteritems():
            if occurrences:
                print(f"Index {index}: {data.loc[index, col]}")
