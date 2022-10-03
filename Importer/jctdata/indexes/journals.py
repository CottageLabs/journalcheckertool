import csv, json, itertools, os, re, shutil
from datetime import datetime

from jctdata import settings
from jctdata import resolver
from jctdata.lib.title_variants import title_variants
from jctdata.lib.analysis import cat_and_dedupe, issn_clusters, cluster_to_dict, extract_preferred
from jctdata.indexes.indexer import Indexer


class Journals(Indexer):
    ID = "journals"
    SOURCES = ["crossref", "doaj", "tj", "ta", "doaj_inprogress", "sa_negative", "sa_positive", "oa_exceptions"]

    def __init__(self):
        super(Journals, self).__init__()
        self._doaj_data = False
        self._tj_data = False
        self._dip_data = False
        self._san_data = False
        self._sap_data = False
        self._oae_data = False

    def gather(self):
        print('JOURNALS: Gathering data for journal compliance from sources: {x}'.format(x=",".join(self.SOURCES)))
        paths = resolver.gather_data(self.SOURCES, True)

        issns = self._get_paths(paths)

        print("JOURNALS: ISSN sources: " + ", ".join([x[0] for x in issns]))

    def analyse(self):
        print("JOURNALS: Analysing data for journal compliance")
        dir = datetime.strftime(datetime.utcnow(), settings.DIR_DATE_FORMAT)
        journalsdir = os.path.join(self.dir, dir)
        os.makedirs(journalsdir, exist_ok=True)

        issn_clusters_file = os.path.join(journalsdir, "issn_clusters.csv")

        pathset = {}
        for s in self.SOURCES:
            pathset[s] = resolver.SOURCES[s].current_paths()
        issns = self._get_paths(pathset)

        issn_clusters(issns, issn_clusters_file)

        print("JOURNALS: analysed data written to directory {x}".format(x=journalsdir))

    def assemble(self):
        print("JOURNALS: Preparing journal compliance")

        journalsdir = os.path.join(self.dir, self.current_dir())
        outfile = os.path.join(journalsdir, "journals.json")

        issn_clusters_file = os.path.join(journalsdir, "issn_clusters.csv")

        with open(issn_clusters_file, "r") as f, open(outfile, "w") as o:
            reader = csv.reader(f)
            for vissns in reader:
                record = {"issns": vissns}

                self._doaj(record)
                self._tj(record)
                self._doaj_in_progress(record)
                self._sa_negative(record)
                self._sa_positive(record)
                self._oa_exceptions(record)

                o.write(json.dumps(record) + "\n")

        print("JOURNALS: Journal compliance assembled")

        self._cleanup()

    def _get_paths(self, paths):
        issns = []
        for source, files in paths.items():
            if "coincident_issns" in files:
                issns.append((source, files["coincident_issns"]))
        return issns

    def _doaj(self, record):
        if self._doaj_data is False:
            paths = resolver.SOURCES["doaj"].current_paths()
            doaj_csv = paths["licences"]

            with open(doaj_csv, "r") as f:
                reader = csv.reader(f)
                data = [row for row in reader]
                self._doaj_data = cluster_to_dict(data, 1)

        for issn in record.get("issns", []):
            if issn in self._doaj_data:
                record["indoaj"] = True
                license = json.loads(self._doaj_data[issn][0][0])
                record["doaj"] = {"bibjson": {"license" : license}}
                break

    def _tj(self, record):
        if self._tj_data is False:
            paths = resolver.SOURCES["tj"].current_paths()
            tj_csv = paths["coincident_issns"]

            with open(tj_csv, "r") as f:
                reader = csv.reader(f)
                data = []
                for row in reader:
                    for c in row:
                        if c != "":
                            data.append(c)
                self._tj_data = data

        for issn in record.get("issns", []):
            if issn in self._tj_data:
                record["tj"] = True
                break

    def _doaj_in_progress(self, record):
        if self._dip_data is False:
            paths = resolver.SOURCES["doaj_inprogress"].current_paths()
            dip_csv = paths["coincident_issns"]

            with open(dip_csv, "r") as f:
                reader = csv.reader(f)
                data = []
                for row in reader:
                    for c in row:
                        if c != "":
                            data.append(c)
                self._dip_data = data

        for issn in record.get("issns", []):
            if issn in self._dip_data:
                record["doajinprogress"] = True
                break

    def _sa_negative(self, record):
        if self._san_data is False:
            paths = resolver.SOURCES["sa_negative"].current_paths()
            san_csv = paths["coincident_issns"]

            with open(san_csv, "r") as f:
                reader = csv.reader(f)
                data = []
                for row in reader:
                    for c in row:
                        if c != "":
                            data.append(c)
                self._san_data = data

        for issn in record.get("issns", []):
            if issn in self._san_data:
                record["sa_prohibited"] = True
                break

    def _sa_positive(self, record):
        if self._sap_data is False:
            paths = resolver.SOURCES["sa_positive"].current_paths()
            sap_csv = paths["coincident_issns"]

            with open(sap_csv, "r") as f:
                reader = csv.reader(f)
                data = []
                for row in reader:
                    for c in row:
                        if c != "":
                            data.append(c)
                self._sap_data = data

        for issn in record.get("issns", []):
            if issn in self._sap_data:
                record["retained"] = True
                break

    def _oa_exceptions(self, record):
        if self._oae_data is False:
            paths = resolver.SOURCES["oa_exceptions"].current_paths()
            oae_csv = paths["coincident_issns"]

            with open(oae_csv, "r") as f:
                reader = csv.reader(f)
                data = []
                for row in reader:
                    for c in row:
                        if c != "":
                            data.append(c)
                self._oae_data = data

        for issn in record.get("issns", []):
            if issn in self._oae_data:
                record["oa_exception"] = True
                break