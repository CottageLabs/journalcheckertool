import os, json

def make_lang_pack(id, out):
    with open(os.path.join("language", id + ".json"), "r") as i:
        data = json.loads(i.read())

    with open(out, "w") as o:
        o.write("var JCT_LANG=" + json.dumps(data))


if __name__ == "__main__":
    make_lang_pack("europeancommissionhorizoneuropeframeworkprogramme", "horizon_lang.js")