import json

class Clonable(object):
    def clone(self):
        return None

class Serializable(Clonable):
    def __dict__(self):
        return None

    def save(self, filename):
        obj = self.__dict__()
        f = open(filename, 'w', encoding='utf-8')
        json.dump(obj, f, indent=4)
        f.close()

    def dict(self):
        """Permet de créer des dictionnaires à partir des classes filles"""
        return None

    @staticmethod
    def hook(dct):
        return None

    @staticmethod
    def load(filename):
        return None
