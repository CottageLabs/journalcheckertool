from jctdata import datasource
from jctdata import settings
from datetime import datetime

import os
import requests
import csv
from io import StringIO

class TJ(datasource.Datasource):
    ID = "tj"

    def current_paths(self):
        dir = self.current_dir()
        coincident_issn_file = os.path.join(self.dir, dir, "coincident_issns.csv")
        title_file = os.path.join(self.dir, dir, "titles.csv")
        publisher_file = os.path.join(self.dir, dir, "publishers.csv")
        return {
            "coincident_issns" : coincident_issn_file,
            "titles" : title_file,
            "publishers": publisher_file
        }

    def gather(self):
        dir = datetime.strftime(datetime.utcnow(), settings.DIR_DATE_FORMAT)
        os.makedirs(os.path.join(self.dir, dir))
        out = os.path.join(self.dir, dir, "origin.csv")

        resp = requests.get(settings.TJ_SHEET)
        with open(out, "w") as f:
            f.write(resp.text)

    def analyse(self):
        dir = self.current_dir()
        infile = os.path.join(self.dir, dir, "origin.csv")
        coincident_issn_file = os.path.join(self.dir, dir, "coincident_issns.csv")
        title_file = os.path.join(self.dir, dir, "titles.csv")
        publisher_file = os.path.join(self.dir, dir, "publishers.csv")
        print("TJ: analysing csv {x}".format(x=infile))

        reader = csv.reader(stream)

        reader.__next__()
        for row in reader:
