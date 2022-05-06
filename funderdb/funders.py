import os
import shutil
import yaml
import json


def list_funders(path, out_dir):
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)

    bases = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x)) and x != "default"]
    bases.sort()

    funders = []
    for base in bases:
        print(os.path.join(path, base))
        with open(os.path.join(path, base, "config.yml")) as y:
            funder_cfg = yaml.load(y.read(), Loader=yaml.BaseLoader)

        funders.append({
            "id" : funder_cfg.get("id"),
            "name" : funder_cfg.get("name"),
            "abbr" : funder_cfg.get("abbr"),
            "country" : funder_cfg.get("country"),
            "primary": True
        })

        for aka in funder_cfg.get("aka", []):
            funders.append({
                "id" : funder_cfg.get("id"),
                "name" : aka.get("name"),
                "abbr" : aka.get("abbr"),
                "country" : funder_cfg.get("country"),
                "primary" : False
            })

    # write a plain json version
    with open(os.path.join(out_dir, "funders.json"), "w") as o:
        o.write(json.dumps(funders, indent=2))

    # write a js version which can be imported in a script tag
    with open(os.path.join(out_dir, "funders.js"), "w") as o:
        o.write("jct.funderlist=" + json.dumps(funders))


if __name__ == "__main__":
    list_funders("funders", "autocomplete")