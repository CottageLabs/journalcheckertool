import json, os, re
from datetime import datetime
from jctdata import settings
from jctdata import resolver
from lib.title_variants import title_variants

ROR_RX = "\d{2}[a-z0-9]{5}\d{2}"


def iac_index_data():
    print('IAC: Data for institution autocomplete start')
    paths = resolver.gather_data(["ror"])
    ROR = paths["ror"].get("origin")
    institutions(ROR)
    print('IAC: data for Institution autocomplete end')


def institutions(ror_file):
    if not os.path.isfile(ror_file):
        print("IAC: {f} does not exist. Gather data maybe. Bye!".format(f=ror_file))
        return
    print("IAC: Preparing institution autocomplete data")
    dir = datetime.strftime(datetime.utcnow(), settings.DIR_DATE_FORMAT)
    iacdir = os.path.join(settings.DATABASES, "jct", "iac", dir)
    os.makedirs(iacdir, exist_ok=True)
    outfile = os.path.join(iacdir, "iac.json")

    with open(ror_file, "r") as f, open(outfile, "w") as o:
        while True:
            line = f.readline()
            if not line:
                break
            rec = json.loads(line)
            vror = _valid_ror(rec.get('id', ''))
            if not vror:
                continue
            record = {"ror": vror}
            if rec.get('country', None):
                record['country'] = rec['country']
            main = rec.get('title', None)
            if main is None:
                continue
            record["title"] = main
            if rec.get('aliases', []):
                record["aliases"] = rec['aliases']
            if rec.get('acronyms', []):
                record["acronyms"] = rec['acronyms']
            _index(record)
            o.write(json.dumps(record) + "\n")


def _valid_ror(ror):
    if re.match(ROR_RX, ror):
        return ror
    return None


def _index(record):
    idx = {}
    idx["ror"] = record['ror']
    idx["title"] = title_variants(record["title"])

    if len(record.get('aliases', [])) > 0:
        idx["aliases"] = []
        for alt in record["aliases"]:
            idx["aliases"].extend(title_variants(alt))
        idx["aliases"] = list(set(idx["aliases"]))
    if len(record.get('acronyms', [])) > 0:
        idx["acronyms"] = list(set(record['acronyms']))
    record["index"] = idx


if __name__ == "__main__":
    print(datetime.utcnow())
    iac_index_data()
    print(datetime.utcnow())

