import sys
import torch
from transformers import AutoTokenizer
from .config import DIR
from .cos_simi import entity_find
from .entity import Entity

# 加载分词器
tokenizer = AutoTokenizer.from_pretrained("hfl/rbt6", model_max_length=512)
device = "cuda:0" if torch.cuda.is_available() else "cpu"  # 有没有GPU

sys.path.insert(0, str(DIR))
model_path = DIR / "model" / "命名实体识别train9_中文106.model"
model_load = torch.load(model_path, map_location="cpu")

model_load.eval()

def part_sentence_output(part_sentence):
    input_id = tokenizer.encode_plus(part_sentence)
    for key, value in input_id.items():
        x = torch.tensor(value)
        x = torch.reshape(x, (1, -1))
        input_id.update({key: x})
    out = model_load(input_id).argmax(dim=2)
    out = out[0]
    select = input_id["attention_mask"][0] == 1
    input_id2 = input_id["input_ids"][0, select]
    # x = tokenizer.decode(input_id2).replace(' ', '')
    # x = x[5:-5]
    # print("原句", x)

    for tag in [out]:
        if tag[-1] != 7:
            tag = tag[2:]
        else:
            tag = tag[1:-1]
        input_id2 = input_id2[1:-1]
        tag = tag.numpy().tolist()

    return input_id2, tag

def one_sentence2Entity(input_id2,tag,eid,original_line):
    entity_list = []
    description_list = []
    person_list = []
    length = len(tag)
    end = 0

    for index, num in enumerate(tag):
        temp = ""
        if index < end:
            continue
        flag = 1
        if num == 2 or num == 1:
            for j in range(index, length):
                temp += tokenizer.decode(input_id2[j])
                if tag[j] != 2 and tag[j] != 1:
                    temp = temp[:-1]
                    entity_list.append(temp)
                    end = j
                    flag = 0
                    break

            if flag == 1:
                entity_list.append(temp)
                break

        if num == 3 or num == 4:
            for j in range(index, length):
                temp += tokenizer.decode(input_id2[j])
                if tag[j] != 3 and tag[j] != 4:
                    temp = temp[:-1]
                    person_list.append(temp)
                    end = j
                    flag = 0
                    break

            if flag == 1:
                person_list.append(temp)
                break

        if num == 5 or num == 6:
            for j in range(index, length):
                temp += tokenizer.decode(input_id2[j])
                if tag[j] != 5 and tag[j] != 6:
                    temp = temp[:-1]
                    description_list.append(temp)
                    end = j
                    flag = 0
                    break

            if flag == 1:
                description_list.append(temp)
                break

        # 粗略处理部分实体描述重复出现的情况

    description_list2 = []
    description_list += person_list
    [description_list2.append(i) for i in description_list if not i in description_list2 and len(i) > 1]
    # for ch in description_list2:
    #     if len(ch) < 2:
    #         description_list2.remove(ch)
    count = 0
    Entity_list = []
    for entity in entity_list:

        if len(entity) < 3:
            continue
        x = entity_find(entity)  # 查找归一化名称
        if x != {}:
            y = max(x, key=x.get)
        else:
            continue

        peers = []
        count += 1
        de = []
        for description in description_list2:
            if near_part(entity, description, original_line):
                de.append(description)
        for i in range(count):
            peers.append(eid - count + 1 + i)
        x = Entity(eid, y, entity[:-1], original_line, de, peers=peers)
        x.show_entity()
        Entity_list.append(x)
        eid += 1
    return Entity_list, eid

def outp2(sentence,eid):
    """
    输入一个句子，返回实体，描述，限定词的位置的列表

    :param sentence: "1. 法定代表人 授权委托书"
    :return: [0,0, 3,4,4,4,4, 1,2,2,2,2]
    """

    sentence_list = sentence.split("。")
    answer = []
    for one_sentence in sentence_list:
        one_sentence = one_sentence.strip()
        if one_sentence == "":
            continue

        input_id1, part_tag = part_sentence_output(one_sentence)
        entity_list, eid = one_sentence2Entity(input_id1, part_tag, eid, sentence)
        answer += entity_list

    return answer, eid




def outp(sentence):
    """

    :param sentence:
    :return: entity_list, person_list, description_list
    """

    sentence_list = sentence.split("。")

    tag = []
    input_id2 = []
    for one_sentence in sentence_list:
        one_sentence = one_sentence.strip()
        if one_sentence == "":
            continue

        input_id1, part_tag = part_sentence_output(one_sentence)
        input_id2 += input_id1
        tag += part_tag

    entity_list = []
    description_list = []
    person_list = []
    length = len(tag)
    end = 0

    for index, num in enumerate(tag):
        temp = ""
        if index < end:
            continue
        flag = 1
        if num == 2 or num == 1:
            for j in range(index, length):
                temp += tokenizer.decode(input_id2[j])
                if tag[j] != 2 and tag[j] != 1:
                    temp = temp[:-1]
                    entity_list.append(temp)
                    end = j
                    flag = 0
                    break

            if flag == 1:
                entity_list.append(temp)
                break

        if num == 3 or num == 4:
            for j in range(index, length):
                temp += tokenizer.decode(input_id2[j])
                if tag[j] != 3 and tag[j] != 4:
                    temp = temp[:-1]
                    person_list.append(temp)
                    end = j
                    flag = 0
                    break

            if flag == 1:
                person_list.append(temp)
                break

        if num == 5 or num == 6:
            for j in range(index, length):
                temp += tokenizer.decode(input_id2[j])
                if tag[j] != 5 and tag[j] != 6:
                    temp = temp[:-1]
                    description_list.append(temp)
                    end = j
                    flag = 0
                    break

            if flag == 1:
                description_list.append(temp)
                break

    # 粗略处理部分实体描述重复出现的情况

    # description_list2 = []
    # [description_list2.append(i) for i in description_list if not i in description_list2 and len(i) > 1]
    # # for ch in description_list2:
    # #     if len(ch) < 2:
    # #         description_list2.remove(ch)
    return entity_list, person_list, description_list


def entity_find2(sentence):
    """
    :param sentence:
    :return:
    """
    entity_list, person_list, description_list2 = outp(sentence)
    description_list2 += person_list
    answer = dict()
    i = 1
    description_list2 = list(set(description_list2))
    # print(entity_list)
    for entity in entity_list:
        if len(entity_list) == 1:
            answer[entity + str(i)] = description_list2
            return answer
        de = []
        for description in description_list2:
            if near_part(entity, description, sentence, 10):
                de.append(description)
        if entity + str(i) in answer.keys():
            i += 1
            answer[entity + str(i)] = de

        else:
            answer[entity + str(i)] = de
        index = sentence.find(entity)
        sentence = sentence[index + len(entity) :]
    return answer

def near_part(str1, str2, sentence, distance=2):
    """
    判断str1，str2是否邻近
    :param str1:
    :param str2:
    :param sentence:
    :return:
    """
    index1 = sentence.find(str1)
    index2 = sentence.find(str2)
    if index2 == -1:
        return False
    if index1 > index2:
        l1 = len(str2)
        if index1 - index2 - l1 < distance:
            return True
    else:
        l1 = len(str1)
        if index2 - index1 - l1 < distance:
            return True
    return False


if __name__ == "__main__":
    eid = 0
    sentence = "3、提供投标人的《中小企业声明函》、《残疾人福利性单位声明函》（格式后附，不可修改），未提供、未盖章或填写内容与相关材料不符的不予价格扣除。"
    y = entity_find2(sentence)
    print(y)

    index, tag = part_sentence_output(sentence)
    entity_list = one_sentence2Entity(index, tag, eid, sentence)
    print(entity_list)
