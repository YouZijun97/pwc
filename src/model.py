import torch
from transformers import AutoModel

# 加载预训练模型
pretrained = AutoModel.from_pretrained("hfl/rbt6")
device = "cuda:0" if torch.cuda.is_available() else "cpu"  # 有没有GPU
pretrained = pretrained.to(device)

# 定义下游模型
class Model(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.tuneing = False
        self.pretrained = pretrained

        self.rnn = torch.nn.GRU(768, 768, batch_first=True)
        self.fc = torch.nn.Linear(768, 8)

    def forward(self, inputs):
        if self.tuneing:
            out = self.pretrained(**inputs).last_hidden_state
        else:
            with torch.no_grad():
                out = pretrained(**inputs).last_hidden_state

        out, _ = self.rnn(out)
        out = self.fc(out).softmax(dim=2)

        return out

    def fine_tuneing(self, tuneing):
        self.tuneing = tuneing
        if tuneing:
            for i in pretrained.parameters():
                i.requires_grad = True

            pretrained.train()
            self.pretrained = pretrained
        else:
            for i in pretrained.parameters():
                i.requires_grad_(False)

            pretrained.eval()
            self.pretrained = None


# 对计算结果和label变形,并且移除pad
def reshape_and_remove_pad(outs, labels, attention_mask):
    # 变形,便于计算loss
    # [b, lens, 8] -> [b*lens, 8]
    outs = outs.reshape(-1, 8)
    # [b, lens] -> [b*lens]
    labels = labels.reshape(-1)

    # 忽略对pad的计算结果
    # [b, lens] -> [b*lens - pad]
    select = attention_mask.reshape(-1) == 1
    outs = outs[select]
    labels = labels[select]

    return outs, labels


# 获取正确数量和总数
def get_correct_and_total_count(labels, outs):
    # [b*lens, 8] -> [b*lens]
    outs = outs.argmax(dim=1)
    correct = (outs == labels).sum().item()
    total = len(labels)

    # 计算除了0以外元素的正确率,因为0太多了,包括的话,正确率很容易虚高
    select = labels != 0
    outs = outs[select]
    labels = labels[select]
    correct_content = (outs == labels).sum().item()
    total_content = len(labels)

    return correct, total, correct_content, total_content
