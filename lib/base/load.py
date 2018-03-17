import json

def load(cfg):
    with open(cfg) as f:
        file = json.load(f)
    return file
