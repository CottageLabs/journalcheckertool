import os, json

def make_config(id, out):
    with open(os.path.join("config", id + ".json"), "r") as i:
        data = json.loads(i.read())

    with open(out, "w") as o:
        o.write("jct.config=" + json.dumps(data))


if __name__ == "__main__":
    make_config("europeancommissionhorizoneuropeframeworkprogramme", "horizon_config.js")