import yaml
import json
import os
import shutil
from copy import deepcopy


def compile_language(path, out_dir):
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)

    default = os.path.join(path, "default", "lang")
    default_lang = _compile_dir(default)

    # build the json for dynamic load
    bases = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x)) and x != "default"]
    for base in bases:
        funder_lang = _compile_dir(os.path.join(path, base, "lang"))
        funder_lang = _merge(default_lang, funder_lang)
        with open(os.path.join(out_dir, base + ".json"), "w") as o:
            o.write(json.dumps(funder_lang, indent=2))

    # build a default language pack as js that can be imported in a script tag
    with open(os.path.join(out_dir, "default_lang.js"), "w") as o:
        o.write("var JCT_LANG=" + json.dumps(default_lang))


def _compile_dir(path):
    compiled = {}
    if not os.path.exists(path):
        return compiled
    for entry in os.listdir(path):
        if not os.path.isdir(os.path.join(path, entry)):
            print(os.path.join(path, entry))
            with open(os.path.join(path, entry)) as y:
                data = yaml.load(y.read(), Loader=yaml.BaseLoader)
            key = entry.split(".")[0]
            compiled[key] = data

        else:
            compiled[entry] = _compile_dir(os.path.join(path, entry))
    return compiled


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
    compile_language("funders", "language")