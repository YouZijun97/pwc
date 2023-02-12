import json

class Entity:
    def __init__(self, eid, entity_name, entity_original, original_text, entity_description, children=None, peers=None):
        self.eid = eid
        self.entity_name = entity_name
        self.entity_original = entity_original
        self.original_text = original_text
        self.entity_description = entity_description
        self.children = children
        self.peers = peers

    def get_entity(self):
        out = dict()
        out["eid"] = self.eid
        out["entity_name"] = self.entity_name
        out["entity_original"] = self.entity_original
        out["original_text"] = self.original_text
        out["entity_description"] = self.entity_description
        return out

    def get_relation(self):
        out = dict()
        if self.children:
            out["type"] = 1
            out["parent"] = self.eid
            out["children"] = self.children
            return out

        if self.peers:
            out["type"] = 2
            out["peers"] = self.peers
            return out

    def show_entity(self):
        print(self.eid, self.entity_name, self.entity_original, self.original_text,self.entity_description, self.peers)


class Json_output:
    """
    存储输出的类
    json_output.entities 返回Entity类的列表
    json_outpyt.relations 返回Entity关系的列表
    """

    def __init__(self):
        self.entities = []
        self.relations = []

    def set_entity(self, entity0):
        self.entities.append(entity0)

    def set_relation(self, relation):
        self.relations.append(relation)


