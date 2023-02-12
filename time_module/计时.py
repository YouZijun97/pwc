# coding=utf-8
import json
from pathlib import Path
base_dir_path = Path(__file__).parent.parent.absolute()
data_dir_path = base_dir_path / 'time_module' / 'data'
import sys
import os
import time
sys.path.insert(0, str(base_dir_path))
from src.entry import run
files = os.listdir(data_dir_path)
fw = open("result.csv", 'w', encoding='utf-8')
fw.write("file,time,file_size\n")
for file in files:
    print(file)
    start = time.time()
    file_name = str(data_dir_path)+"/"+file
    if not os.path.isdir(file):
        f = open(file_name, 'r', encoding="UTF-8", errors='ignore')
        iter_f = iter(f)
        paragraph = ""
        for line in iter_f:  # 每个line是文件中的每一行；可能包括多个句子，有可能就是一个名词短语 #暂时保留这个结构，对每个句子进行spacy分析；后面提高效率可以改成pipe
            paragraph += line

        x = run(paragraph)
        print(x)
        with open("./json_output/"+file[:-4]+'.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(x, indent=4, ensure_ascii=False))
    end = time.time()
    fw.write(file+","+str(end-start)+"s,"+str(os.path.getsize(file_name)/1024)+"KB\n")
    print(file[:16], "耗时：", end - start)
