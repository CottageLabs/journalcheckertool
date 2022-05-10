import tarfile, json, csv
from copy import deepcopy
import requests, os
from jctdata import datasource
from jctdata import settings
from jctdata.lib.secrets import get_secret
from datetime import datetime


class DOAJInProgress(datasource.Datasource):
    ID = "doaj_inprogress"

    def current_paths(self):
        dir = self.current_dir()
        coincident_issn_file = os.path.join(self.dir, dir, "coincident_issns.csv")
        return {
            "coincident_issns" : coincident_issn_file
        }

    def gather(self):
        dir = datetime.strftime(datetime.utcnow(), settings.DIR_DATE_FORMAT)
        os.makedirs(os.path.join(self.dir, dir))
        out = os.path.join(self.dir, dir, "origin.json")

        url = settings.DOAJ_IN_PROGRESS_URL
        url += "?api_key=" + get_secret(settings.DOAJ_IN_PROGRESS_KEYFILE)

        print("DOAJ IN PROGRESS: downloading latest in progress list")
        resp = requests.get(url)

        with open(out, "w") as f:
            f.write(resp.content.decode("UTF-8"))

    def analyse(self):
        dir = self.current_dir()
        infile = os.path.join(self.dir, dir, "origin.json")
        coincident_issn_file = os.path.join(self.dir, dir, "coincident_issns.csv")
        print("DOAJ IN PROGRESS: analysing in progress list {x}".format(x=infile))

        self._coincident_issns(infile, coincident_issn_file)

    def _coincident_issns(self, doaj_file, outfile):
        issn_pairs = []

        with open(doaj_file, "r") as f:
            data = json.loads(f.read())

        for entry in data:
            if entry.get("pissn") and entry.get("eissn"):
                issn_pairs.append([entry["pissn"], entry["eissn"]])
                issn_pairs.append([entry["eissn"], entry["pissn"]])
            elif entry.get("pissn") and not entry.get("eissn"):
                issn_pairs.append([entry["pissn"], ""])
            elif not entry.get("pissn") and entry.get("eissn"):
                issn_pairs.append([entry["eissn"], ""])

        issn_pairs.sort(key=lambda x: x[0])

        with open(outfile, "w") as o:
            writer = csv.writer(o)
            writer.writerows(issn_pairs)

if __name__ == "__main__":
    doaj = DOAJInProgress()
    doaj.gather()
    doaj.analyse()
