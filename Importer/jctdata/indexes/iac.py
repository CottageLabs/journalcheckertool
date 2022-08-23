import json, os, re
from datetime import datetime

from jctdata import settings
from jctdata import resolver
from jctdata.lib.title_variants import title_variants
from jctdata.indexes.indexer import Indexer

ROR_RX = "\d{2}[a-z0-9]{5}\d{2}"


class IAC(Indexer):
    ID = "iac"
    SOURCES = ["ror"]

    def gather(self):
        print('IAC: Gathering data for institutional autocomplete from sources: {x}'.format(x=",".join(self.SOURCES)))
        paths = resolver.gather_data(self.SOURCES, True)
        print("IAC: ROR source: " + paths.get("ror", {}).get("origin", "no ror source"))

    def analyse(self):
        print("IAC: No analysis stage required")

    def assemble(self):
        print("IAC: Preparing institution autocomplete data")

        dir = datetime.strftime(datetime.utcnow(), settings.DIR_DATE_FORMAT)
        iacdir = os.path.join(self.dir, dir)
        os.makedirs(iacdir, exist_ok=True)
        outfile = os.path.join(iacdir, "iac.json")

        ror_path = resolver.SOURCES[self.SOURCES[0]].current_paths()
        ror_file = ror_path.get("origin")

        if not os.path.isfile(ror_file):
            print("IAC: {f} does not exist. Gather data maybe. Bye!".format(f=ror_file))
            return

        with open(ror_file, "r") as f, open(outfile, "w") as o:
            while True:
                line = f.readline()
                if not line:
                    break
                rec = json.loads(line)
                vror = self._valid_ror(rec.get('id', ''))
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
                self._index(record)
                o.write(json.dumps(record) + "\n")

        print("IAC: Institutional Autocomplete data assembled")

        self._cleanup()

    def _valid_ror(self, ror):
        if re.match(ROR_RX, ror):
            return ror
        return None

    def _index(self, record):
        idx = {}
        idx["ror"] = record['ror']
        idx["title"] = title_variants(record["title"])

        if len(record.get('aliases', [])) > 0 or len(record.get("acronyms", [])) > 0:
            idx["aliases"] = []
            for alt in record.get("aliases", []):
                idx["aliases"].extend(title_variants(alt))

            for ac in record.get('acronyms', []):
                idx["aliases"].extend(title_variants(ac))

            idx["aliases"] = list(set(idx["aliases"]))

        record["index"] = idx