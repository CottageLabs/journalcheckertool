import esprit
import json
import uuid
import os
from datetime import datetime

from jctdata import settings

MAPPING = {
    "jac" : {
        "dynamic_templates": [
            {
                "default": {
                    "match": "*",
                    "match_mapping_type": "string",
                    "mapping": {
                        "type": "multi_field",
                        "fields": {
                            "{name}": {"type": "{dynamic_type}", "index": "analyzed", "store": "no"},
                            "exact": {"type": "{dynamic_type}", "index": "not_analyzed", "store": "yes"}
                        }
                    }
                }
            }
        ]
    }
}


def index(infile, bulkfile, conn, index_type, mapping):
    with open(infile, "r") as f, open(bulkfile, "w") as o:
        line = f.readline()
        while line:
            d = json.loads(line)
            d["id"] = uuid.uuid4().hex
            bulklines = esprit.raw.to_bulk_single_rec(d)
            o.write(bulklines)
            line = f.readline()

    if not esprit.raw.type_exists(conn, index_type, es_version="1.7.5"):
        r = esprit.raw.put_mapping(conn, index_type, mapping, es_version="1.7.5")
        print("Creating ES Type + Mapping in index {0}; status: {1}".format(index_type, r.status_code))
    else:
        print("ES Type + Mapping already exists in index {0}".format(index_type))

    esprit.tasks.bulk_load(conn, index_type, bulkfile)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Load data into the index')
    parser.add_argument('target')

    args = parser.parse_args()

    target_dir = os.path.join(settings.DATABASES, "jct", args.target)

    dirs = []
    for entry in os.listdir(target_dir):
        if os.path.isdir(os.path.join(target_dir, entry)):
            dirs.append(entry)

    if len(dirs) == 0:
        print("target has not got a build to load into the index")
        exit(0)

    dirs.sort()
    latest = dirs[0]

    IN = os.path.join(target_dir, latest, args.target + ".json")

    # IN = "databases/jct/journals-2022-05-06.json"
    CONN = esprit.raw.Connection(settings.ES_HOST, settings.INDEX)
    INDEX_TYPE = args.target + "-" + datetime.strftime(datetime.utcnow(), settings.INDEX_SUFFIX_DATE_FORMAT)
    # BULK_FILE = "../databases/jct/jac-2022-05-06.bulk"
    BULK_FILE = os.path.join(target_dir, latest, args.target + ".bulk")

    MAPPING = {INDEX_TYPE : settings.DEFAULT_MAPPING}
    index(IN, BULK_FILE, CONN, INDEX_TYPE, MAPPING)