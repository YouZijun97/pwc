def sentence_preprocess(sentence):

    new_sentence = remove_signal(sentence)
    new_sentence = remove_xuhao(new_sentence)

    return new_sentence

def remove_signal(sentence):
    new_sentence = sentence.replace(" ", "").replace("“", "").replace("”", "")\
        .replace("\t", "").replace("（", "(").replace("）", ")")
    signal_list = ["·","★","…","—","●"]
    for ch in signal_list:
        new_sentence = new_sentence.replace(ch, "")

    return new_sentence


def remove_xuhao(sentence):
    index = 0
    signal_list = ["、", ".", ")", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

    for signal in signal_list:
        if sentence.find(signal) < 6:
            index = max(sentence.find(signal),index)
    if index != 0:
        index += 1
    new_sentence = sentence[index:]

    return new_sentence

if __name__ == '__main__':
    sentence = "（1） 、商务文件应包括如下内容（格式见第四章） ："
    x = sentence_preprocess(sentence)
    print(x, "\t句子长度是:",len(x))
