import json

class Clonable(object):
    def clone(self):
        return None

class Serializable(Clonable):
    KEYS = []
    def __dict__(self):
        return None

    def save(self, filename):
        obj = self.__dict__()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(obj, f, indent=4)

    def dict(self):
        """Permet de créer des dictionnaires à partir des classes filles"""
        return None

    @staticmethod
    def hook(dct):
        return None

    @staticmethod
    def load(filename):
        return None

    def clone(self):
        return json.loads(json.dumps(self.__dict__()), object_hook=self.__class__.hook, encoding='utf-8')



