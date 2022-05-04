from jctdata import datasource
from jctdata import settings
from datetime import datetime

import os
import requests
import csv


def pair_manager(source, outfile, first=0, second=1, skip_title_row=False):
    pairs = []

    with open(source) as f:
        reader = csv.reader(f)
        if skip_title_row:
            reader.__next__()

        for row in reader:
            if row[first] and row[second]:
                pairs.append([row[first], row[second]])
                pairs.append([row[second], row[first]])
            elif row[first] and not row[second]:
                pairs.append([row[first], ""])
            elif not row[first] and row[second]:
                pairs.append([row[second], ""])

    pairs.sort(key=lambda x: x[0])

    with open(outfile, "w") as o:
        writer = csv.writer(o)
        writer.writerows(pairs)


def simple_property_extract(source, outfile, property=0, identifiers=None, skip_title_row=False, info=None):
    if identifiers is None:
        identifiers = [1, 2]

    with open(outfile, "w") as o:
        writer = csv.writer(o)

        with open(source, "r") as f:
            reader = csv.reader(f)
            if skip_title_row:
                reader.__next__()
            for row in reader:
                for i in identifiers:
                    if row[i]:
                        if row[property]:
                            newrow = [row[i], row[property]]
                            if info:
                                newrow.append(info)
                            writer.writerow(newrow)


class SANegative(datasource.Datasource):
    ID = "sa_negative"

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

        resp = requests.get(settings.SA_NEGATIVE_SHEET)
        with open(out, "w") as f:
            f.write(resp.text)

    def analyse(self):
        dir = self.current_dir()
        infile = os.path.join(self.dir, dir, "origin.csv")
        coincident_issn_file = os.path.join(self.dir, dir, "coincident_issns.csv")
        title_file = os.path.join(self.dir, dir, "titles.csv")
        publisher_file = os.path.join(self.dir, dir, "publishers.csv")
        print("SA NEGATIVE: analysing csv {x}".format(x=infile))

        self._coincident_issns(infile, coincident_issn_file)
        self._title_map(infile, title_file)
        self._publisher_map(infile, publisher_file)


    def _coincident_issns(self, sa_file, outfile):
        pair_manager(sa_file, outfile, first=1, second=2, skip_title_row=True)

    def _title_map(self, sa_file, outfile):
        simple_property_extract(sa_file, outfile, property=0, identifiers=[1,2], info="main", skip_title_row=True)

    def _publisher_map(self, sa_file, outfile):
        simple_property_extract(sa_file, outfile, property=3, identifiers=[1, 2], skip_title_row=True)
