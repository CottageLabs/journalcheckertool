from jctdata import datasource
from jctdata import settings
from datetime import datetime

import os
import requests
import csv
import itertools

class TA(datasource.Datasource):
    ID = "ta"

    def current_paths(self):
        dir = self.current_dir()
        coincident_issn_file = os.path.join(self.dir, dir, "coincident_issns.csv")
        title_file = os.path.join(self.dir, dir, "titles.csv")
        return {
            "origin": os.path.join(self.dir, dir, "origin.csv"),
            "coincident_issns" : coincident_issn_file,
            "titles" : title_file,
            "issns": os.path.join(self.dir, dir, "issn.csv")
        }

    def gather(self):
        dir = datetime.strftime(datetime.utcnow(), settings.DIR_DATE_FORMAT)
        os.makedirs(os.path.join(self.dir, dir))
        index = os.path.join(self.dir, dir, "origin.csv")
        sheets = os.path.join(self.dir, dir, "origin")
        os.makedirs(sheets)

        resp = requests.get(settings.TA_INDEX_SHEET)
        with open(index, "w") as f:
            f.write(resp.text)

        self._retrieve_ta_data(index, sheets)

    def _retrieve_ta_data(self, index, outdir):
        with open(index, "r") as f:
            reader = csv.reader(f)
            first = True
            for i, row in enumerate(reader):
                if first:
                    first = False
                    continue
                data_url = row[4]
                self.log("{y} retrieving from {x}".format(x=data_url, y=i))
                try:
                    resp = requests.get(data_url, timeout=10)
                    resp.encoding = "utf-8"
                except requests.Timeout:
                    self.log("{y} TIMEOUT: {x}".format(x=data_url, y=i))
                if resp.status_code != 200:
                    self.log("{y} ERROR: Failed to retrieve {x}".format(x=data_url, y=i))
                else:
                    self.log("{y} Retrieved {x} [{z}]".format(x=row[0], y=i, z=row[1]))

                fn = row[0]
                if row[1]:
                    fn += "." + row[1]
                fn = "".join([c for c in fn if c.isalpha() or c.isdigit() or c in ' .']).rstrip()
                fn += ".csv"

                outfile = os.path.join(outdir, fn)
                with open(outfile, "w") as o:
                    o.write(resp.text)
                self.log("{y} saved to {x}".format(y=i, x=fn))

    def analyse(self):
        dir = self.current_dir()
        sheets = os.path.join(self.dir, dir, "origin")

        coincident_issn_file = os.path.join(self.dir, dir, "coincident_issns.csv")
        title_file = os.path.join(self.dir, dir, "titles.csv")
        issn_registry_file = os.path.join(self.dir, dir, "issn.csv")
        ror_registry_file = os.path.join(self.dir, dir, "ror.csv")

        self._coincident_issns(sheets, coincident_issn_file)
        self._title_map(sheets, title_file)
        self._issn_registry(sheets, issn_registry_file)
        self._ror_registry(sheets, ror_registry_file)

    def _coincident_issns(self, sheets_dir, outfile):
        issn_pairs = []

        sheets = os.listdir(sheets_dir)
        for sheet in sheets:
            infile = os.path.join(sheets_dir, sheet)

            with open(infile, "r") as f:
                reader = csv.reader(f)
                reader.__next__()
                for row in reader:
                    if row[1] and row[2]:
                        issn_pairs.append([row[1].strip(), row[2].strip()])
                        issn_pairs.append([row[2].strip(), row[1].strip()])
                    elif row[1] and not row[2]:
                        issn_pairs.append([row[1].strip(), ""])
                    elif not row[1] and row[2]:
                        issn_pairs.append([row[2].strip(), ""])

        issn_pairs.sort(key=lambda x: x[0] + x[1])
        issn_pairs = list(k for k, _ in itertools.groupby(issn_pairs))

        with open(outfile, "w") as o:
            writer = csv.writer(o)
            writer.writerows(issn_pairs)

    def _title_map(self, sheets_dir, outfile):
        title_map = []
        sheets = os.listdir(sheets_dir)
        for sheet in sheets:
            infile = os.path.join(sheets_dir, sheet)

            with open(infile, "r") as f:
                reader = csv.reader(f)
                reader.__next__()
                for row in reader:
                    if row[1]:
                        if row[0]:
                            title_map.append([row[1].strip(), row[0].strip(), "main"])
                    if row[2]:
                        if row[0]:
                            title_map.append([row[2].strip(), row[0].strip(), "main"])

        title_map.sort(key=lambda x: x[0] + x[1])
        title_map = list(k for k, _ in itertools.groupby(title_map))

        with open(outfile, "w") as o:
            writer = csv.writer(o)
            writer.writerows(title_map)

    def _issn_registry(self, sheets_dir, outfile):
        issn_registry = []
        sheets = os.listdir(sheets_dir)
        for sheet in sheets:
            esac_id = sheet.split(".", 1)[0]
            name_ex_suffix = sheet.rsplit(".", 1)[0]
            rel = ""
            if name_ex_suffix != esac_id:
                rel = name_ex_suffix[len(esac_id) + 1:]

            infile = os.path.join(sheets_dir, sheet)
            with open(infile, "r") as f:
                reader = csv.reader(f)
                reader.__next__()
                for row in reader:
                    if row[1]:
                        issn_registry.append([row[1].strip(), name_ex_suffix, esac_id, rel])
                    if row[2]:
                        issn_registry.append([row[2].strip(), name_ex_suffix, esac_id, rel])

        issn_registry.sort(key=lambda x: x[0] + x[1])
        issn_registry = list(k for k, _ in itertools.groupby(issn_registry))

        with open(outfile, "w") as o:
            writer = csv.writer(o)
            writer.writerows(issn_registry)

    def _ror_registry(self, sheets_dir, outfile):
        title_map = []
        sheets = os.listdir(sheets_dir)
        for sheet in sheets:
            infile = os.path.join(sheets_dir, sheet)

            with open(infile, "r") as f:
                reader = csv.reader(f)
                reader.__next__()
                for row in reader:
                    if row[1]:
                        if row[0]:
                            title_map.append([row[1].strip(), row[0].strip(), "main"])
                    if row[2]:
                        if row[0]:
                            title_map.append([row[2].strip(), row[0].strip(), "main"])

        title_map.sort(key=lambda x: x[0] + x[1])
        title_map = list(k for k, _ in itertools.groupby(title_map))

        with open(outfile, "w") as o:
            writer = csv.writer(o)
            writer.writerows(title_map)