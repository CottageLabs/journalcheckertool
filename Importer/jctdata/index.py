import esprit
import json
import uuid
import os
import requests
from datetime import datetime

from jctdata import settings


def index(infile, bulkfile, conn, index_type, mapping, alias):
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
        print("INDEX: Creating ES Type + Mapping in index {0}; status: {1}".format(conn.index, r.status_code))
    else:
        print("INDEX: ES Type + Mapping already exists in index {0}".format(conn.index))

    print("INDEX: bulk loading from {x}".format(x=bulkfile))
    esprit.tasks.bulk_load(conn, index_type, bulkfile)

    old_idx = None
    resp = requests.get(conn.host + ":" + conn.port + "/_aliases")
    aliases = json.loads(resp.text)
    for idx, a in aliases.items():
        if alias in a.get("aliases", {}):
            old_idx = idx
            break

    if old_idx is None:
        print("INDEX: creating new alias {x} for {y}".format(x=alias, y=conn.index))
        esprit.tasks.create_alias(conn, alias)
    else:
        old_conn = esprit.raw.Connection(conn.host, old_idx, port=conn.port)
        print("INDEX: repointing existing alias {x} from {y} to {z}".format(x=alias, y=old_conn.index, z=conn.index))
        esprit.tasks.repoint_alias(old_conn, conn, alias)

    removal_candidates = [idx for idx in aliases.keys() if idx.startswith(alias)]
    if len(removal_candidates) < settings.INDEX_KEEP_OLD_INDICES:
        print("INDEX: less than {x} old indices, none removed".format(x=settings.INDEX_KEEP_OLD_INDICES))
        return

    removal_candidates.sort(reverse=True)
    removes = removal_candidates[settings.INDEX_KEEP_OLD_INDICES:]
    for r in removes:
        print("INDEX: removing old index {x}".format(x=r))
        conn = esprit.raw.Connection(conn.host, r, port=conn.port)
        esprit.raw.delete(conn)


def index_latest_with_alias(target, index_suffix):
    target_dir = os.path.join(settings.DATABASES, "jct", target)

    os.makedirs(target_dir, exist_ok=True)

    dirs = []
    for entry in os.listdir(target_dir):
        if os.path.isdir(os.path.join(target_dir, entry)):
            dirs.append(entry)

    if len(dirs) == 0:
        print("target has not got a build to load into the index")
        return

    dirs.sort(reverse=True)
    latest = dirs[0]

    if index_suffix and not index_suffix.startswith('_'):
        index_suffix = "_" + index_suffix

    ALIAS = "jct_" + target + index_suffix
    timestamped_index_name = ALIAS + datetime.strftime(datetime.utcnow(), settings.INDEX_SUFFIX_DATE_FORMAT)

    IN = os.path.join(target_dir, latest, target + ".json")
    CONN = esprit.raw.Connection(settings.ES_HOST, timestamped_index_name)
    INDEX_TYPE = target
    BULK_FILE = os.path.join(target_dir, latest, target + ".bulk")
    MAPPING = {INDEX_TYPE : settings.DEFAULT_MAPPING}

    print("INDEX: loading into index")
    print("INDEX: IN: {x}".format(x=IN))
    print("INDEX: INDEX_TYPE: {x}".format(x=INDEX_TYPE))
    print("INDEX: ALIAS: {x}".format(x=ALIAS))
    print("INDEX: BULK: {x}".format(x=BULK_FILE))

    index(IN, BULK_FILE, CONN, INDEX_TYPE, MAPPING, ALIAS)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Load data into the index')
    parser.add_argument('target')
    parser.add_argument("-s", "--index_suffix")

    args = parser.parse_args()
    index_latest_with_alias(args.target, args.index_suffix)
