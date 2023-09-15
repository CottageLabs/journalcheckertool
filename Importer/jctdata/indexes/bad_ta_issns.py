import csv, json, os, shutil
from jctdata import resolver, settings
from jctdata.indexes.indexer import Indexer
from datetime import datetime


class BadTAIssns(Indexer):
    ID = "bad_ta_issns"
    SOURCES = ["ta"]

    def gather(self):
        self.log('Gathering data for TA database from sources: {x}'.format(x=",".join(self.SOURCES)))
        paths = resolver.gather_data(self.SOURCES, True)

    def analyse(self):
        self.log("No analysis required")

    def assemble(self):
        self.log("Preparing TA data")

        dir = datetime.strftime(datetime.utcnow(), settings.DIR_DATE_FORMAT)
        tadir = os.path.join(self.dir, dir)
        os.makedirs(tadir, exist_ok=True)

        outfile = os.path.join(tadir, "bad_ta_issns.csv")

        pathset = resolver.SOURCES["ta"].current_paths()
        bad_issns = pathset.get("bad_issns")

        if not os.path.exists(bad_issns):
            self.log("No bad issns in TAs found")

        shutil.copy(bad_issns, outfile)
        self.log("Copied bad issns in TAs to {x}".format(x=outfile))

        self._cleanup()