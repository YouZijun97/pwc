from src.predict import part_sentence_output, one_sentence2Entity
from src.paragraph2out import para2out

if __name__ == '__main__':
    eid = 0
    sentence = "项目各阶段工作成员(必须为项目常驻现场人员)简历(加盖公章)、身份证复印件、近12个月社保证明、最高学历复印件、在相关项目中承担的任务、在本项目组中的角色以及项目参与度，以及相关技术资质证书复印件等；"
    x,y = part_sentence_output(sentence)
    print(y)
    l1,eid = one_sentence2Entity(x,y,eid,sentence)

    # print()
    # para2out(sentence)
