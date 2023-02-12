from src.predict import part_sentence_output, one_sentence2Entity
from src.paragraph2out import para2out

if __name__ == '__main__':
    eid = 0
    sentence = "13.1.1出具经法定代表人签字、公司盖章的“法定代表人授权委托书”，并附法定代表人或授权人身份证复印件；"

    # index, tag = part_sentence_output(sentence)
    # entity_list,eid = one_sentence2Entity(index, tag, eid, sentence)
    # for i in entity_list:
    #     print(i.show_entity())

    para2out(sentence)
