import json

_cfg_dir = 'config/'


class Config:
    def __init__(self):
        self.name = self.__class__.__name__
        self.settings = self.load_cfg()

    def load_cfg(self):
        cfg_file = _cfg_dir + self.name + '.json'
        with open(cfg_file) as f:
            cfg = json.load(f)
        return cfg
