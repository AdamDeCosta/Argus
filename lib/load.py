import json

_cfg_dir = 'config/'

def load(cfg):
    with open(cfg) as f:
        file = json.load(f)
    return file


def load_plugin_cfg(plugin: object):
    plugin_name = plugin.__class__.__name__
    cfg_file = _cfg_dir + plugin_name + '.json'
    with open(cfg_file) as f:
        cfg = json.load(f)
    return cfg
