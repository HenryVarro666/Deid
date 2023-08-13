import pandas as pd
import re

# 定义文件名

# ## Reddit_Data
# input_file = './Reddit_Data.csv'
# output_file = 'Flitered_Reddit_Data_Comments.csv'
# column = 'clean_comment'

## Twitter_Data
input_file = 'Twitter_Data.csv'
output_file = 'Flitered_Twitter_Data_Comments.csv'
column = 'clean_text'

# 读取CSV文件
data = pd.read_csv(input_file)

# 定义一个函数来检查字符串是否包含 'he' 或 'she'
def contains_he_she(text):
    return bool(re.search(r'\bhe\b|\bshe\b', str(text), flags=re.IGNORECASE))

# 从'clean_comment'列中找到精确包含'he'或'she'的行
filtered_data = data[data[column].apply(contains_he_she)]

# 只选择'clean_comment'列并保存到新的CSV文件
filtered_data[column].to_csv(output_file, index=False, header=[column])


