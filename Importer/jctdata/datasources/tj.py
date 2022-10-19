from jctdata import datasource
from jctdata import settings
from datetime import datetime

import os
import requests
import csv

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
        self.log("gathering TJ data from {x}".format(x=settings.TJ_SHEET))
        dir = datetime.strftime(datetime.utcnow(), settings.DIR_DATE_FORMAT)
        os.makedirs(os.path.join(self.dir, dir))
        out = os.path.join(self.dir, dir, "origin.csv")

        resp = requests.get(settings.TJ_SHEET)
        resp.encoding = "utf-8"
        with open(out, "w") as f:
            f.write(resp.text)
        print("TJ: data written to {x}".format(x=out))

    def analyse(self):
        dir = self.current_dir()
        infile = os.path.join(self.dir, dir, "origin.csv")
        coincident_issn_file = os.path.join(self.dir, dir, "coincident_issns.csv")
        title_file = os.path.join(self.dir, dir, "titles.csv")
        publisher_file = os.path.join(self.dir, dir, "publishers.csv")
        self.log("analysing csv {x}".format(x=infile))

        self._coincident_issns(infile, coincident_issn_file)
        self._title_map(infile, title_file)
        self._publisher_map(infile, publisher_file)

    def _coincident_issns(self, tj_file, outfile):
        issn_pairs = []

        with open(tj_file, "r") as f:
            reader = csv.reader(f)
            reader.__next__()
            for row in reader:
                if row[1] and row[2]:
                    issn_pairs.append([row[1], row[2]])
                    issn_pairs.append([row[2], row[1]])
                elif row[1] and not row[2]:
                    issn_pairs.append([row[1], ""])
                elif not row[1] and row[2]:
                    issn_pairs.append([row[2], ""])

        issn_pairs.sort(key=lambda x: x[0])

        with open(outfile, "w") as o:
            writer = csv.writer(o)
            writer.writerows(issn_pairs)

    def _title_map(self, tj_file, outfile):
        with open(outfile, "w") as o:
            writer = csv.writer(o)

            with open(tj_file, "r") as f:
                reader = csv.reader(f)
                reader.__next__()
                for row in reader:
                    if row[1]:
                        if row[0]:
                            writer.writerow([row[1], row[0], "main"])
                    if row[2]:
                        if row[0]:
                            writer.writerow([row[2], row[0], "main"])

    def _publisher_map(self, tj_file, outfile):
        with open(outfile, "w") as o:
            writer = csv.writer(o)

            with open(tj_file, "r") as f:
                reader = csv.reader(f)
                reader.__next__()
                for row in reader:
                    if row[1]:
                        if row[3]:
                            writer.writerow([row[1], row[3]])
                    if row[2]:
                        if row[3]:
                            writer.writerow([row[2], row[3]])

