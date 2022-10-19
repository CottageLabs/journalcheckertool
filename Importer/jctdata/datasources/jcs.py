import requests, csv, os
from jctdata import settings, datasource
from datetime import datetime
from jctdata.lib import analysis


class JCS(datasource.Datasource):
    ID = "jcs"

    def current_paths(self):
        dir = self.current_dir()
        origin_file = os.path.join(self.dir, dir, "origin.csv")
        coincident_issn_file = os.path.join(self.dir, dir, "coincident_issns.csv")
        title_file = os.path.join(self.dir, dir, "titles.csv")
        publisher_file = os.path.join(self.dir, dir, "publishers.csv")
        return {
            "origin": origin_file,
            "coincident_issns" : coincident_issn_file,
            "titles" : title_file,
            "publishers" : publisher_file
        }

    def gather(self):
        dir = datetime.strftime(datetime.utcnow(), settings.DIR_DATE_FORMAT)
        os.makedirs(os.path.join(self.dir, dir))
        outfile = os.path.join(self.dir, dir, "origin.csv")

        years = range(settings.JCS_FIRST_YEAR, datetime.utcnow().year)
        self.log("Gathering for years {x}".format(x=",".join([str(y) for y in years])))

        with open(outfile, "w") as f:
            writer = csv.writer(f)

            for year in years:
                self.log("Retrieving for year {x}".format(x=year))
                url = settings.JCS_API.replace("{year}", str(year))
                self.log("retrieve from {x}".format(x=url))
                resp = requests.get(url)
                if resp.status_code != 200:
                    self.log("error status code {x}".format(x=resp.status_code))
                    break

                data = resp.json()
                entries = data.get("issns", [])
                self.log("retrieved {x} records for {y}".format(x=len(entries), y=year))

                for entry in entries:
                    writer.writerow([entry.get("issn"), entry.get("journal_title"), entry.get("publisher"), year])

    def analyse(self):
        dir = self.current_dir()
        infile = os.path.join(self.dir, dir, "origin.csv")
        coincident_issn_file = os.path.join(self.dir, dir, "coincident_issns.csv")
        title_file = os.path.join(self.dir, dir, "titles.csv")
        publisher_file = os.path.join(self.dir, dir, "publishers.csv")

        self._coincident_issns(infile, coincident_issn_file)
        self._title_map(infile, title_file)
        self._publisher_map(infile, publisher_file)

    def _coincident_issns(self, infile, outfile):
        with open(infile) as f:
            reader = csv.reader(f)
            issns = [[row[0]] for row in reader]

        issns.sort()

        with open(outfile, "w") as o:
            writer = csv.writer(o)
            writer.writerows(issns)

    def _title_map(self, infile, outfile):
        analysis.simple_property_extract(infile, outfile, property=1, identifiers=[0], info="main",
                                         skip_title_row=False)

    def _publisher_map(self, infile, outfile):
        analysis.simple_property_extract(infile, outfile, property=2, identifiers=[0], info="main",
                                         skip_title_row=False)
