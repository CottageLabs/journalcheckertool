from jctdata import datasource
from jctdata import settings
from jctdata.lib import analysis

from datetime import datetime
import os
import requests


class OAExceptions(datasource.Datasource):
    ID = "oa_exceptions"

    def current_paths(self):
        dir = self.current_dir()
        coincident_issn_file = os.path.join(self.dir, dir, "coincident_issns.csv")
        title_file = os.path.join(self.dir, dir, "titles.csv")
        publisher_file = os.path.join(self.dir, dir, "publishers.csv")
        caveats_file = os.path.join(self.dir, dir, "caveats.csv")
        return {
            "coincident_issns" : coincident_issn_file,
            "titles" : title_file,
            "publishers": publisher_file,
            "caveats": caveats_file
        }

    def gather(self):
        dir = datetime.strftime(datetime.utcnow(), settings.DIR_DATE_FORMAT)
        os.makedirs(os.path.join(self.dir, dir), exist_ok=True)
        out = os.path.join(self.dir, dir, "origin.csv")

        print("OA EXCEPTIONS: retrieving from {x}".format(x=settings.OA_EXCEPTIONS_SHEET))
        resp = requests.get(settings.OA_EXCEPTIONS_SHEET)
        resp.encoding = "utf-8"
        with open(out, "w", encoding="utf-8") as f:
            f.write(resp.text)

    def analyse(self):
        dir = self.current_dir()
        infile = os.path.join(self.dir, dir, "origin.csv")
        coincident_issn_file = os.path.join(self.dir, dir, "coincident_issns.csv")
        title_file = os.path.join(self.dir, dir, "titles.csv")
        publisher_file = os.path.join(self.dir, dir, "publishers.csv")
        caveats_file = os.path.join(self.dir, dir, "caveats.csv")
        print("OA EXCEPTIONS: analysing csv {x}".format(x=infile))

        self._coincident_issns(infile, coincident_issn_file)
        self._title_map(infile, title_file)
        self._publisher_map(infile, publisher_file)
        self._caveats_map(infile, caveats_file)


    def _coincident_issns(self, oa_file, outfile):
        analysis.pair_manager(oa_file, outfile, first=1, second=2, skip_title_row=True)

    def _title_map(self, oa_file, outfile):
        analysis.simple_property_extract(oa_file, outfile, property=0, identifiers=[1,2], info="main", skip_title_row=True)

    def _publisher_map(self, oa_file, outfile):
        analysis.simple_property_extract(oa_file, outfile, property=3, identifiers=[1, 2], skip_title_row=True)

    def _caveats_map(self, oa_file, outfile):
        analysis.simple_property_extract(oa_file, outfile, property=4, identifiers=[1, 2], skip_title_row=True)
