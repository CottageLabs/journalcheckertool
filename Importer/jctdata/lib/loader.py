import esprit
import json
import uuid
import os
import requests
import re
import shutil
from datetime import datetime

from jctdata import settings
from jctdata.lib import send_mail


################################################
## Elasicsearch loader functions

def index(infile, bulkfile, conn, index_type, mapping, alias):
    with open(infile, "r") as f, open(bulkfile, "w") as o:
        line = f.readline()
        while line:
            if line:
                try:
                    d = json.loads(line)
                    if "id" not in d:
                        d["id"] = uuid.uuid4().hex
                    bulklines = esprit.raw.to_bulk_single_rec(d)
                    o.write(bulklines)
                except json.JSONDecodeError:
                    print(f"skipped line {line}")
            line = f.readline()

    if not esprit.raw.type_exists(conn, index_type, es_version="1.7.5"):
        r = esprit.raw.put_mapping(conn, index_type, mapping, es_version="1.7.5")
        print("LOADER: Creating ES Type + Mapping in index {0}; status: {1}".format(conn.index, r.status_code))
    else:
        print("LOADER: ES Type + Mapping already exists in index {0}".format(conn.index))

    print("LOADER: bulk loading from {x}".format(x=bulkfile))
    esprit.tasks.bulk_load(conn, index_type, bulkfile)

    old_idx = None
    resp = requests.get(conn.host + ":" + conn.port + "/_aliases")
    aliases = json.loads(resp.text)
    for idx, a in aliases.items():
        if alias in a.get("aliases", {}):
            old_idx = idx
            break

    if old_idx is None:
        print("LOADER: creating new alias {x} for {y}".format(x=alias, y=conn.index))
        esprit.tasks.create_alias(conn, alias)
    else:
        old_conn = esprit.raw.Connection(conn.host, old_idx, port=conn.port)
        print("LOADER: repointing existing alias {x} from {y} to {z}".format(x=alias, y=old_conn.index, z=conn.index))
        esprit.tasks.repoint_alias(old_conn, conn, alias)

    removal_candidates = [idx for idx in aliases.keys() if re.match(rf'^{alias}\d+$', idx)]
    if len(removal_candidates) < settings.INDEX_KEEP_OLD_INDICES:
        print("LOADER: less than {x} old indices, none removed".format(x=settings.INDEX_KEEP_OLD_INDICES))
        return

    removal_candidates.sort(reverse=True)
    removes = removal_candidates[settings.INDEX_KEEP_OLD_INDICES:]
    for r in removes:
        print("LOADER: removing old index {x}".format(x=r))
        conn = esprit.raw.Connection(conn.host, r, port=conn.port)
        esprit.raw.delete(conn)


def update_with_test_data(input_file, output_file):
    """
    Reads each line from the input file and appends it to a new line in the output file.

    Args:
      input_file: Path to the input file.
      output_file: Path to the output file.
    """
    test_data_file = os.path.join(settings.TEST_DATABASE, input_file)
    # Check if output file exists
    if os.path.exists(test_data_file) and os.path.exists(output_file):
        os.makedirs(settings.TEMP_DIR, exist_ok=True)

        # Clear existing files in temp directory (if any)
        for filename in os.listdir(settings.TEMP_DIR):
            file_path = os.path.join(settings.TEMP_DIR, filename)
            os.remove(file_path)

        # Copy existing output file to temporary directory
        output_file = shutil.copy2(output_file, settings.TEMP_DIR)

        # Open the input file in read mode and output file in append mode
        with open(test_data_file, 'r') as in_file, open(output_file, 'a') as out_file:
            # Read each line from the input file
            for line in in_file:
                # Write the line to the output file
                out_file.write('\n' + line.strip())

    return output_file


def index_latest_with_alias(target, index_suffix, test_database=False):
    target_dir = settings.INDEX_PATH[target]
    os.makedirs(target_dir, exist_ok=True)

    dirs = []
    for entry in os.listdir(target_dir):
        if os.path.isdir(os.path.join(target_dir, entry)):
            dirs.append(entry)

    if len(dirs) == 0:
        print("LOADER: target {x} has not got a build to load into the index".format(x=target))
        return

    dirs.sort(reverse=True)
    latest = dirs[0]

    if index_suffix and not index_suffix.startswith('_'):
        index_suffix = "_" + index_suffix

    index_prefix = settings.ES_INDEX_PREFIX
    if index_prefix and not index_prefix.endswith('_'):
        index_prefix = index_prefix + "_"

    ALIAS = index_prefix + target + index_suffix
    timestamped_index_name = ALIAS + datetime.strftime(datetime.utcnow(), settings.INDEX_SUFFIX_DATE_FORMAT)

    IN = os.path.join(target_dir, latest, target + ".json")
    CONN = esprit.raw.Connection(settings.ES_HOST, timestamped_index_name)
    INDEX_TYPE = target
    BULK_FILE = os.path.join(target_dir, latest, target + ".bulk")
    MAPPING = {INDEX_TYPE : settings.DEFAULT_MAPPING}

    print("LOADER: loading {x} into index".format(x=target))
    print("LOADER: IN: {x}".format(x=IN))
    print("LOADER: INDEX_TYPE: {x}".format(x=INDEX_TYPE))
    print("LOADER: ALIAS: {x}".format(x=ALIAS))
    print("LOADER: BULK: {x}".format(x=BULK_FILE))

    if test_database:
        print("Appending test data")
        # add test database records to the file
        IN = update_with_test_data(target + ".json", IN)
        print("LOADER: IN: {x}".format(x=IN))

    index(IN, BULK_FILE, CONN, INDEX_TYPE, MAPPING, ALIAS)


################################################
## File loader functions

def load_to_file(target):
    target_dir = settings.INDEX_PATH[target]
    os.makedirs(target_dir, exist_ok=True)

    dirs = []
    for entry in os.listdir(target_dir):
        if os.path.isdir(os.path.join(target_dir, entry)):
            dirs.append(entry)

    if len(dirs) == 0:
        print("LOADER: target {x} has not got a build to load to file".format(x=target))
        return

    dirs.sort(reverse=True)
    latest = dirs[0]

    IN = os.path.join(target_dir, latest, target + ".csv") # FIXME: this assumes a csv, which is fine for the moment, as the only one is
    OUT = settings.FILE_LOADER_PATHS[target]

    print("LOADER: loading {x} to file".format(x=target))
    print("LOADER: IN: {x}".format(x=IN))
    print("LOADER: OUT: {x}".format(x=OUT))

    shutil.copy(IN, OUT)


################################################
## Send to helpdesk function

def load_to_helpdesk(target):
    target_dir = settings.INDEX_PATH[target]
    os.makedirs(target_dir, exist_ok=True)

    dirs = []
    for entry in os.listdir(target_dir):
        if os.path.isdir(os.path.join(target_dir, entry)):
            dirs.append(entry)

    if len(dirs) == 0:
        print("LOADER: target {x} has not got a build to load to file".format(x=target))
        return

    dirs.sort(reverse=True)
    latest = dirs[0]

    # FIXME: this assumes a csv, which is fine for the moment, as the only one is
    attachment_name = target + ".csv"
    attachment = os.path.join(target_dir, latest, attachment_name)
    subject = settings.HELPDESK_LOADER_PATHS[target]['subject']
    message = settings.HELPDESK_LOADER_PATHS[target]['message']

    send_mail.send_mail(subject, message, attachment, attachment_name=attachment_name)

    print("LOADER: sending {x} to helpdesk for {y}".format(x=attachment, y=target))
