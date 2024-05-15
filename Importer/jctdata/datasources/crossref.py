import requests, csv, os
from jctdata import settings, datasource
from datetime import datetime


class Crossref(datasource.Datasource):
    ID = "crossref"
    ROW_PER_PAGE = 1000
    LIMIT = 200000

    def current_paths(self):
        dir = self.current_dir()
        coincident_issn_file = os.path.join(self.dir, dir, "coincident_issns.csv")
        title_file = os.path.join(self.dir, dir, "titles.csv")
        publisher_file = os.path.join(self.dir, dir, "publishers.csv")
        return {
            "coincident_issns" : coincident_issn_file,
            "titles" : title_file,
            "publishers" : publisher_file
        }

    def gather(self):
        dir = datetime.strftime(datetime.utcnow(), settings.DIR_DATE_FORMAT)
        os.makedirs(os.path.join(self.dir, dir))
        outfile = os.path.join(self.dir, dir, "origin.csv")

        with open(outfile, "w") as f:
            writer = csv.writer(f)
            counter = 0
            cursor = "*"
            while True:
                if counter >= self.LIMIT:
                    self.log("configured import limit reached {x}".format(x=self.LIMIT))
                    break

                url = 'https://api.crossref.org/journals?cursor=' + cursor + '&rows=' + str(self.ROW_PER_PAGE) + "&mailto=" + settings.CROSSREF_MAILTO
                self.log("retrieve from {x}".format(x=url))
                resp = requests.get(url)
                if resp.status_code != 200:
                    self.log("error status code {x}".format(x=resp.status_code))
                    break

                data = resp.json()
                if data.get("status") != "ok":
                    self.log("document status not ok: {x}".format(x=data.get("status")))
                    break

                cursor = data.get("message", {}).get("next-cursor")
                self.log("next cursor {x}".format(x=cursor))

                items = data.get("message", {}).get("items", [])
                if len(items) == 0:
                    self.log("zero length results list, terminating")
                    break

                self.log("processing {x} items from this page".format(x=len(items)))

                for entry in items:
                    publisher = entry.get("publisher")
                    title = entry.get("title")
                    issns = entry.get("ISSN")
                    issns = list(set(issns))    # because sometimes the issns are duplicated
                    doi_years = [pair[0] for pair in entry.get("breakdowns", {}).get("dois-by-issued-year", [])]
                    last_doi = max(doi_years) if len(doi_years) > 0 else 0
                    discontinued = entry.get("discontinued", False)
                    if len(issns) > 2:
                        self.log("more than 2 ISSNs found: " + ",".join(issns))
                        issns = issns[:2]
                    issns += [""]*(2-len(issns))
                    writer.writerow(issns + [title, publisher, last_doi, str(discontinued)])

                counter += len(items)
                self.log("Import total so far: {x}".format(x=counter))

    def analyse(self):
        dir = self.current_dir()
        infile = os.path.join(self.dir, dir, "origin.csv")
        coincident_issn_file = os.path.join(self.dir, dir, "coincident_issns.csv")
        title_file = os.path.join(self.dir, dir, "titles.csv")
        publisher_file = os.path.join(self.dir, dir, "publishers.csv")
        oldest_doi = settings.CROSSREF_OLDEST_DOI

        self._coincident_issns(infile, coincident_issn_file, oldest_doi)
        self._title_map(infile, title_file)
        self._publisher_map(infile, publisher_file)

    def _coincident_issns(self, crossref_file, outfile, oldest_doi):
        issn_pairs = []

        with open(crossref_file) as f:
            reader = csv.reader(f)

            for row in reader:
                if int(row[4]) != 0 and int(row[4]) < oldest_doi:
                    continue

                if row[0] and row[1]:
                    issn_pairs.append([row[0], row[1]])
                    issn_pairs.append([row[1], row[0]])
                elif row[0] and not row[1]:
                    issn_pairs.append([row[0], ""])
                elif not row[0] and row[1]:
                    issn_pairs.append([row[1], ""])

        issn_pairs.sort(key=lambda x: x[0])

        with open(outfile, "w") as o:
            writer = csv.writer(o)
            writer.writerows(issn_pairs)

    def _title_map(self, crossref_file, outfile):
        with open(outfile, "w") as o:
            writer = csv.writer(o)

            with open(crossref_file) as f:
                reader = csv.reader(f)

                for row in reader:
                    if row[0]:
                        if row[2]:
                            writer.writerow([row[0], row[2], "main"])
                    if row[1]:
                        if row[2]:
                            writer.writerow([row[1], row[2], "main"])

    def _publisher_map(self, crossref_file, outfile):
        with open(outfile, "w") as o:
            writer = csv.writer(o)

            with open(crossref_file) as f:
                reader = csv.reader(f)

                for row in reader:
                    if row[0]:
                        if row[3]:
                            writer.writerow([row[0], row[3]])
                    if row[1]:
                        if row[3]:
                            writer.writerow([row[1], row[3]])
