import os
import re
import xml.etree.ElementTree as ET
import csv

# 指定XML文件所在的目录
directory = './testing-PHI-Gold-fixed'

# 创建CSV文件，并写入表头
with open('sentences_he_she.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['sentences'])

    # 遍历文件夹中的每个文件
    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            filepath = os.path.join(directory, filename)

            # 解析XML文件
            tree = ET.parse(filepath)
            root = tree.getroot()

            # 遍历XML文件的每个元素，并检查其文本内容
            for elem in root.iter():
                if elem.text:
                    # 分割文本为句子
                    sentences = re.split(r'[.!?]', elem.text)
                    for sentence in sentences:
                        # 使用正则表达式检查句子是否包含“he”或“she”作为独立的单词
                        if re.search(r'\b(he|she|He|She|SHE|SHe|HE|him|HIM})\b', sentence, re.IGNORECASE):
                            writer.writerow([sentence.strip()])
