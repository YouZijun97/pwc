from .paragraph2out import para2out

def run(paragraph: str):
    out = dict()
    json_out1 = para2out(paragraph)
    out["entities"] = json_out1.entities
    out["relations"] = json_out1.relations
    return out