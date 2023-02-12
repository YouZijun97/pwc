# coding=utf-8
import os
from src.entry import run
import json
from src.preprocess import sentence_preprocess
from src.paragraph2out import para2out
path = "./devset_txt"
csv_path = "./devset_csv/"
files = os.listdir(path)

for file in files:
    if not os.path.isdir(file):
        f = open(path + "/" + file, 'r', encoding="UTF-8", errors='ignore')
        fw = open(csv_path+file[:-3] + "csv", 'w', encoding='utf-8')
        fw.write("original_text, entity_list\n")
        iter_f = iter(f)
        paragraph = ""
        for line in iter_f:  # 每个line是文件中的每一行；可能包括多个句子，有可能就是一个名词短语 #暂时保留这个结构，对每个句子进行spacy分析；后面提高效率可以改成pipe
            line = sentence_preprocess(line)
            jsonout = para2out(line)
            entity_list = jsonout.entities
            temp = ""
            for entity in entity_list:
                temp += entity["entity_original"]
                temp += "、"
            fw.write(line + "," + temp[:-1] + "\n")


