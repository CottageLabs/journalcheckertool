import argparse
import os
import shutil
import yaml
import json


def rel2abs(file, *args):
    file = os.path.realpath(file)
    if os.path.isfile(file):
        file = os.path.dirname(file)
    return os.path.abspath(os.path.join(file, *args))


def append_test_funders_to_list(funders):
    """
    Reads a test JSON file and append contents to the funders.

    Args:
    funders: funders list.
    """

    funder_config_file = rel2abs(__file__, "..", "Importer", "test_database", "funder_config.json")

    print(f"Test config file : {funder_config_file}")

    # Check if the file exists
    if not os.path.exists(funder_config_file):
        print(f"Error: File '{funder_config_file}' does not exist.")
        return

    with open(funder_config_file, 'r') as f:
        for line in f:
            funder_cfg = json.loads(line.strip())

            if funder_cfg:
                funders.append({
                    "id": funder_cfg.get("id"),
                    "name": funder_cfg.get("name"),
                    "abbr": funder_cfg.get("abbr"),
                    "country": funder_cfg.get("country"),
                    "primary": True
                })

                for aka in funder_cfg.get("aka", []):
                    funders.append({
                        "id": funder_cfg.get("id"),
                        "name": aka.get("name"),
                        "abbr": aka.get("abbr"),
                        "country": funder_cfg.get("country"),
                        "primary": False
                    })


def list_funders(path, out_dir, append_test_data:bool):
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
        if append_test_data:
            append_test_funders_to_list(funders)
        o.write("jct.funderlist=" + json.dumps(funders))

    # write a markdown fragment which can be used in the API documentation
    with open(os.path.join(out_dir, "funder-ids.md"), "w") as o:
        funders.sort(key=lambda x: x["name"])
        for funder in funders:
            o.write("**{x}**\n: `{y}`\n\n".format(x=funder["name"], y=funder["id"]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate funders data.")
    parser.add_argument("-t", "--test_data", action="store_true", default=False, help="Appends test data")
    args = parser.parse_args()

    if args.test_data:
        print("Test mode - Appends test data")

    list_funders("funders", "autocomplete", args.test_data)