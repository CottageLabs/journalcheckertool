import csv, json, os
from datetime import datetime

from jctdata import settings
from jctdata import resolver
from jctdata.lib.analysis import issn_clusters, cluster_to_dict
from jctdata.indexes.indexer import Indexer


class Journal(Indexer):
    ID = "journal"
    SOURCES = ["crossref", "doaj", "tj", "ta", "doaj_inprogress", "sa_negative", "sa_positive", "oa_exceptions", "jcs"]

    def __init__(self):
        super(Journal, self).__init__()
        self._doaj_data = False
        self._tj_data = False
        self._tj_excludes = False
        self._dip_data = False
        self._san_data = False
        self._sap_data = False
        self._oae_data = False
        self._jcs_data = False

    def gather(self):
        self.log('Gathering data for journal compliance from sources: {x}'.format(x=",".join(self.SOURCES)))
        paths = resolver.gather_data(self.SOURCES, True)

        issns = self._get_paths(paths)

        self.log("ISSN sources: " + ", ".join([x[0] for x in issns]))

    def analyse(self):
        self.log("Analysing data for journal compliance")
        dir = datetime.strftime(datetime.utcnow(), settings.DIR_DATE_FORMAT)
        journalsdir = os.path.join(self.dir, dir)
        os.makedirs(journalsdir, exist_ok=True)

        issn_clusters_file = os.path.join(journalsdir, "issn_clusters.csv")

        pathset = {}
        for s in self.SOURCES:
            pathset[s] = resolver.SOURCES[s].current_paths()
        issns = self._get_paths(pathset)

        issn_clusters(issns, issn_clusters_file)

        self.log("analysed data written to directory {x}".format(x=journalsdir))

    def assemble(self):
        self.log("Preparing journal compliance")

        journalsdir = os.path.join(self.dir, self.current_dir())
        outfile = os.path.join(journalsdir, self.ID + ".json")

        issn_clusters_file = os.path.join(journalsdir, "issn_clusters.csv")

        with open(issn_clusters_file, "r") as f, open(outfile, "w") as o:
            reader = csv.reader(f)
            for vissns in reader:
                record = {"issn": vissns, "createdAt": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}

                self._doaj(record)
                self._tj(record)
                self._doaj_in_progress(record)
                self._sa_negative(record)
                self._sa_positive(record)
                self._oa_exceptions(record)
                self._jcs(record)

                o.write(json.dumps(record) + "\n")

        self.log("Journal compliance assembled")

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

        for issn in record.get("issn", []):
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

        if self._tj_excludes is False:
            paths = resolver.SOURCES["tj"].current_paths()
            tj_csv = paths["funder_excludes"]
            self._tj_excludes = {}

            with open(tj_csv, "r") as f:
                reader = csv.reader(f)
                data = []
                for row in reader:
                    self._tj_excludes[row[0]] = row[1]

        for issn in record.get("issn", []):
            if issn in self._tj_data:
                record["tj"] = True
            if issn in self._tj_excludes:
                if "tj_excluded_by" not in record:
                    record["tj_excluded_by"] = []
                excluder = self._tj_excludes[issn]
                if excluder not in record["tj_excluded_by"]:
                    record["tj_excluded_by"].append(excluder)


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

        for issn in record.get("issn", []):
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

        for issn in record.get("issn", []):
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

        for issn in record.get("issn", []):
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

            caveats_csv = paths["caveats"]
            with open(caveats_csv, "r") as f:
                reader = csv.reader(f)
                data = {}
                for row in reader:
                    data[row[0]] = row[1]
                self._oae_caveats = data

        for issn in record.get("issn", []):
            if issn in self._oae_data:
                record["oa_exception"] = True
                record["oa_exception_caveat"] = self._oae_caveats.get(issn, "")
                break

    def _jcs(self, record):
        if self._jcs_data is False:
            paths = resolver.SOURCES["jcs"].current_paths()
            jcs_csv = paths["origin"]
            self._jcs_data = {}

            with open(jcs_csv, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] not in self._jcs_data:
                        self._jcs_data[row[0]] = []
                    self._jcs_data[row[0]].append(int(row[3]))

        for issn in record.get("issn", []):
            if issn in self._jcs_data:
                record["jcs_years"] = self._jcs_data[issn]
                break
