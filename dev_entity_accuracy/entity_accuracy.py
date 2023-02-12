# coding=utf-8
import os
from src.entry import run
import json
from src.preprocess import sentence_preprocess
from src.paragraph2out import para2out
import linecache
csv_model_path = "./devset_csv"
csv_person_path = "./devset_csv_人工"
files = os.listdir(csv_model_path)
all_file_f1 = 0
for file in files:
    if not os.path.isdir(file):
        model_file = csv_model_path + "/" + file
        person_file = csv_person_path + "/" + file
        f = open(model_file, 'r', encoding="UTF-8", errors='ignore')
        fw = open(person_file, 'r', encoding='utf-8')
        count = len(f.readline())
        sum_entity_count, sum_accuracy_count = 0, 0
        for i in range(count):
            model_line = linecache.getline(model_file, i).strip()
            person_line = linecache.getline(person_file, i).strip()
            # print(model_line, person_line)
            model_entity = model_line.split(",")[-1].split("、")
            person_entity = person_line.split(",")[-1].split("、")
            if model_entity == [""] and person_entity == [""]:
                entity_count, accuracy_count = 0, 0

            elif model_entity == [""] or person_entity == [""]:
                entity_count, accuracy_count = max(len(model_entity), len(person_entity)), 0
            else:
                entity_count = len(model_entity) + len(person_entity)
                accuracy_count = 0
                for e_m in model_entity:
                    if e_m in person_entity:
                        accuracy_count += 1
            sum_entity_count += entity_count
            sum_entity_count -= accuracy_count
            sum_accuracy_count += accuracy_count
            # print(entity_count, accuracy_count)
            # print(model_entity, person_entity)
        one_file_f1 = sum_accuracy_count/sum_entity_count
        all_file_f1 += one_file_f1
        print(file, "f1:", one_file_f1)

print("devset_txt里的文件实体级f1：",all_file_f1 / 10 )
