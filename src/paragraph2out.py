from .cos_simi import entity_find
from .entity import Entity, Json_output
from .predict import outp,near_part
from .preprocess import sentence_preprocess

def para2out(paragraph):
    id = 0
    json_out1 = Json_output()
    for original_line in paragraph.splitlines():

        # 1.句子预处理
        preprocess_sentence = sentence_preprocess(original_line)
        if preprocess_sentence == "":  # 输入数据为空
            continue

        # 2.查找实体、实体描述
        entity_list,  person_list, description_list = outp(preprocess_sentence)

        # 3.实体筛选并赋予归一化名称，实体描述筛选
        text_and_name = []
        for entity in entity_list:
            if len(entity) < 3:
                continue
            name_dict = entity_find(entity)  # 查找归一化名称
            if name_dict != {}:
                name = max(name_dict, key=name_dict.get)
            else:
                continue
            text_and_name.append(entity)
            text_and_name.append(name)

        # 4. 实体描述筛选
        # person_list = list(set(person_list))
        # description_list = list(set(description_list))
        person_list = [i for i in person_list if len(i) > 2]
        description_list = [i for i in description_list if len(i) > 1]

        # 5.实体描述与实体相匹配
        l1 = len(text_and_name)//2
        if l1 == 0:
            continue
        peers = []
        for i in range(l1):
            entity_text = text_and_name[2*i]
            de = []
            for description in description_list:
                if near_part(entity_text, description, original_line):
                    de.append(description)

            sentence = preprocess_sentence
            for person in person_list:
                if near_part(entity_text, person, sentence, 1):
                    entity_text = person+entity_text
                    break
                index = min(sentence.find(entity_text)+len(entity_text), sentence.find(person)+len(person))
                sentence = sentence[index:]

            # 5.赋予实体
            peers +=[id]
            entity = Entity(id, text_and_name[2*i+1], entity_text, original_line, de, peers=peers)
            entity.show_entity()
            json_out1.set_entity(entity.get_entity())
            id += 1
            if i == l1-1 and len(entity.peers) > 1:
                json_out1.set_relation(entity.get_relation())

    return json_out1