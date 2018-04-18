import json


class Serializable(object):
    def serialize(self):
        return

    def deserialize(self, filename):
        return

def save(serializable:Serializable, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(serializable.serialize(), f, indent=4)

def load(serializable:Serializable, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        return json.load(f, object_hook=serializable.deserialize)

