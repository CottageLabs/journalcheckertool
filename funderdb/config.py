import yaml
import json
import os
import shutil
from copy import deepcopy


def compile_config(path, out_dir):
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)

    with open(os.path.join(path, "default", "config.yml")) as y:
        default_cfg = yaml.load(y.read(), Loader=yaml.BaseLoader)

    bases = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x)) and x != "default"]
    for base in bases:
        with open(os.path.join(path, base, "config.yml")) as y:
            funder_cfg = yaml.load(y.read(), Loader=yaml.BaseLoader)
        funder_cfg = _merge(default_cfg, funder_cfg)
        with open(os.path.join(out_dir, base + ".json"), "w") as o:
            o.write(json.dumps(funder_cfg, indent=2))

    # generate a default configuration that can be loaded with a script tag
    with open(os.path.join(out_dir, "default_config.js"), "w") as o:
        o.write("jct.config=" + json.dumps(default_cfg))


def _merge(default, funder):
    result = deepcopy(default)
    for k, v in funder.items():
        if isinstance(v, dict):
            if k in default:
                result[k] = _merge(default[k], funder[k])
            else:
                result[k] = funder[k]
        else:
            result[k] = funder[k]
    return result


if __name__ == "__main__":
    compile_config("funders", "config")