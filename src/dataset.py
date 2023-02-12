import os

import torch
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("hfl/rbt6", model_max_length=512)
tag2id = {
    "O": 0,
    "EB": 1,
    "EI": 2,
    "PB": 3,
    "PI": 4,
    "DB": 5,
    "DI": 6,
}

class nerDataset(torch.utils.data.Dataset):
    def __init__(self, path):
        datasets_list = os.listdir(path)
        self.src = list()
        self.trg = list()
        for data in datasets_list:
            with open(path + "/" + data, encoding="utf-8") as f:
                src_temp, trg_temp = list(), list()
                # src_len = 0
                for line in f.readlines():
                    # print(line)
                    c = line.strip("")
                    # print("c = line.strip()",c)
                    if len(c) <= 1:
                        src_temp = "".join(src_temp)

                        src_temp, trg_temp = list(), list()
                        continue
                    # c = c.split('')
                    c = c[:-1]
                    c = c.split(",")

                    # print("c = c.split()",c)
                    src_temp.append(c[0])
                    trg_temp.append(tag2id[c[-1]])
                    self.trg.append(trg_temp)
                    self.src.append(src_temp)
                    # if len(self.trg)!= src_len:
                    #     src_len = len(self.trg)
                    #     print(self.trg[-1],self.src[-1])

    def __len__(self):
        return len(self.src)

    def __getitem__(self, idx):
        # 返回单条样本
        # tokens = self.src[idx]['tokens']
        # labels = self.trg[idx]['ner_tags']
        tokens = self.src[idx]
        labels = self.trg[idx]

        return tokens, labels

# 数据整理函数
def collate_fn(data):
    tokens = [i[0] for i in data]
    labels = [i[1] for i in data]

    inputs = tokenizer.batch_encode_plus(
        tokens, truncation=True, padding=True, return_tensors="pt", is_split_into_words=True
    )

    lens = inputs["input_ids"].shape[1]

    for i in range(len(labels)):
        labels[i] = [7] + labels[i]
        labels[i] += [7] * lens
        labels[i] = labels[i][:lens]

    return inputs, torch.LongTensor(labels)
