# coding=utf-8
import os
from src.entry import run
import json
import time


path = "./data"

files = os.listdir(path)
count = 0
for file in files:
    start = time.time()
    if not os.path.isdir(file):
        f = open(path + "/" + file, 'r', encoding="UTF-8", errors='ignore')
        iter_f = iter(f)
        paragraph = ""
        for line in iter_f:  # 每个line是文件中的每一行；可能包括多个句子，有可能就是一个名词短语 #暂时保留这个结构，对每个句子进行spacy分析；后面提高效率可以改成pipe
            paragraph += line
        # print(paragraph)
        x = run(paragraph)
        with open('test{}_cos.json'.format(count), 'w', encoding='utf-8') as f:
            f.write(json.dumps(x, indent=4, ensure_ascii=False))
            count += 1
    end = time.time()
    print(file[:16], "耗时：", end-start)


