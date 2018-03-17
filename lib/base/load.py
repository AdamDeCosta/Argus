import json

_cfg_dir = 'config/'

def load(cfg):
    with open(cfg) as f:
        file = json.load(f)
    return file