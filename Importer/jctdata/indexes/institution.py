import csv, json, os
from datetime import datetime

from jctdata import settings
from jctdata import resolver
from jctdata.lib.analysis import issn_clusters, cluster_to_dict
from jctdata.indexes.indexer import Indexer


class Institution(Indexer):
    ID = "institution"
    SOURCES = ["ror", "ta"]

    def __init__(self):
        super(Institution, self).__init__()
        self._ta_data = False

    def gather(self):
        self.log('Gathering data for institutions from sources: {x}'.format(x=",".join(self.SOURCES)))
        resolver.gather_data(self.SOURCES, True)

    def analyse(self):
        self.log("Analysing data for institutions")
        dir = datetime.strftime(datetime.utcnow(), settings.DIR_DATE_FORMAT)
        instsdir = os.path.join(self.dir, dir)
        os.makedirs(instsdir, exist_ok=True)

    def assemble(self):
        self.log("Preparing institution data")

        pathset = {}
        for s in self.SOURCES:
            pathset[s] = resolver.SOURCES[s].current_paths()
        rors_files = self._get_paths(pathset)

        instsdir = os.path.join(self.dir, self.current_dir())
        outfile = os.path.join(instsdir, self.ID + ".json")

        with open(outfile, "w") as o:
            for source, rors_file in rors_files:
                with open(rors_file, "r") as f:
                    reader = csv.reader(f)
                    for row in reader:
                        record = {"ror": row[0], "createdAt": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}
                        self._ta(record)
                        o.write(json.dumps(record) + "\n")

        self.log("Institutions assembled")
        self._cleanup()

    def _get_paths(self, paths):
        rors = []
        for source, files in paths.items():
            if "rors" in files:
                rors.append((source, files["rors"]))
        return rors

    def _ta(self, record):
        if self._ta_data is False:
            paths = resolver.SOURCES["ta"].current_paths()
            ror_csv = paths["rors"]
            self._ta_data = {}

            with open(ror_csv, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] not in self._ta_data:
                        self._ta_data[row[0]] = []
                    self._ta_data[row[0]].append(row[1])

        tas = self._ta_data.get(record["ror"])
        if tas is not None:
            record["tas"] = list(set(tas))
