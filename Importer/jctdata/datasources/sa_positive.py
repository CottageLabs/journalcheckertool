from jctdata import datasource
from jctdata import settings
from jctdata.lib import analysis

from datetime import datetime
import os
import requests


class SAPositive(datasource.Datasource):
    ID = "sa_positive"

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
        os.makedirs(os.path.join(self.dir, dir), exist_ok=True)
        out = os.path.join(self.dir, dir, "origin.csv")

        resp = requests.get(settings.SA_POSITIVE_SHEET)
        with open(out, "w") as f:
            f.write(resp.text)

    def analyse(self):
        dir = self.current_dir()
        infile = os.path.join(self.dir, dir, "origin.csv")
        coincident_issn_file = os.path.join(self.dir, dir, "coincident_issns.csv")
        title_file = os.path.join(self.dir, dir, "titles.csv")
        publisher_file = os.path.join(self.dir, dir, "publishers.csv")
        print("SA POSITIVE: analysing csv {x}".format(x=infile))

        self._coincident_issns(infile, coincident_issn_file)
        self._title_map(infile, title_file)
        self._publisher_map(infile, publisher_file)

    def _coincident_issns(self, sa_file, outfile):
        analysis.pair_manager(sa_file, outfile, first=1, second=2, skip_title_row=True)

    def _title_map(self, sa_file, outfile):
        analysis.simple_property_extract(sa_file, outfile, property=0, identifiers=[1,2], info="main", skip_title_row=True)

    def _publisher_map(self, sa_file, outfile):
        analysis.simple_property_extract(sa_file, outfile, property=4, identifiers=[1, 2], skip_title_row=True)
