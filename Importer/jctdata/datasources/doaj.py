import tarfile, json, csv
from copy import deepcopy
import requests, os
from jctdata import datasource
from jctdata import settings
from datetime import datetime


class DOAJ(datasource.Datasource):
    ID = "doaj"

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
        out = os.path.join(self.dir, dir, "origin.csv")

        tarball = os.path.join(self.dir, dir, "origin.tar.gz")

        if not os.path.exists(tarball):
            print("DOAJ: downloading latest data dump")
            resp = requests.get("https://doaj.org/public-data-dump/journal")
            with open(tarball, "wb") as f:
                f.write(resp.content)
        self._extract_doaj_data(tarball, out)

    def _extract_doaj_data(self, tarball, out):
        print("DOAJ: extracting data dump {x}".format(x=tarball))
        tf = tarfile.open(tarball, "r:gz")
        with open(out, "w") as o:
            writer = csv.writer(o)
            while True:
                entry = tf.next()
                if entry is None:
                    break
                f = tf.extractfile(entry)
                j = json.loads(f.read())

                for journal in j:
                    eissn = journal.get("bibjson", {}).get("eissn", "")
                    pissn = journal.get("bibjson", {}).get("pissn", "")
                    title = journal.get("bibjson", {}).get("title", "")
                    alt = journal.get("bibjson", {}).get("alternative_title", "")
                    publisher = journal.get("bibjson", {}).get("publisher", {}).get("name", "")
                    row = [eissn, pissn, title, alt, publisher]

                    licences = journal.get("bibjson", {}).get("license", [])
                    if len(licences) == 0:
                        writer.writerow(row)

                    for i, l in enumerate(licences):
                        lrow = deepcopy(row)
                        lrow += [
                            str(i + 1) + "/" + str(len(licences)),
                            l.get("type")
                        ]
                        writer.writerow(lrow)

    def analyse(self):
        dir = self.current_dir()
        infile = os.path.join(self.dir, dir, "origin.csv")
        coincident_issn_file = os.path.join(self.dir, dir, "coincident_issns.csv")
        title_file = os.path.join(self.dir, dir, "titles.csv")
        publisher_file = os.path.join(self.dir, dir, "publishers.csv")
        print("DOAJ: analysing extracted data dump {x}".format(x=infile))

        self._coincident_issns(infile, coincident_issn_file)
        self._title_map(infile, title_file)
        self._publisher_map(infile, publisher_file)

    def _coincident_issns(self, doaj_file, outfile):
        issn_pairs = []

        with open(doaj_file, "r") as f:
            reader = csv.reader(f)

            for row in reader:
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

    def _title_map(self, doaj_file, outfile):
        with open(outfile, "w") as o:
            writer = csv.writer(o)

            with open(doaj_file, "r") as f:
                reader = csv.reader(f)

                for row in reader:
                    if row[0]:
                        if row[2]:
                            writer.writerow([row[0], row[2], "main"])
                        if row[3]:
                            writer.writerow([row[0], row[3], "alt"])
                    if row[1]:
                        if row[2]:
                            writer.writerow([row[1], row[2], "main"])
                        if row[3]:
                            writer.writerow([row[1], row[3], "alt"])

    def _publisher_map(self, doaj_file, outfile):
        with open(outfile, "w") as o:
            writer = csv.writer(o)

            with open(doaj_file, "r") as f:
                reader = csv.reader(f)

                for row in reader:
                    if row[0]:
                        if row[4]:
                            writer.writerow([row[0], row[4]])
                    if row[1]:
                        if row[4]:
                            writer.writerow([row[1], row[4]])

if __name__ == "__main__":
    TARBALL = "databases/doaj/doaj_journal_data_2022-04-05.tar.gz"
    OUT = "databases/doaj/doaj-2022-04-05.csv"
    ISSN = "databases/doaj/coincident_issns-2022-04-05.csv"
    TITLE = "databases/doaj/titles-2022-04-05.csv"
    PUB = "databases/doaj/pubs-2022-04-05.csv"

    doaj = DOAJ()
    doaj.gather(OUT, TARBALL)
    doaj.analyse(OUT, ISSN, TITLE, PUB)

"""
{"last_updated": "2021-04-29T13:15:45Z", "bibjson": {"editorial": {"review_process": ["Peer review"],
                                                                   "review_url": "http://revues.imist.ma/?journal=JMSR&page=about&op=editorialPolicies#openAccessPolicy",
                                                                   "board_url": "http://journal-jmsr.net/editorial_board.php"},
                                                     "pid_scheme": {"has_pid_scheme": false},
                                                     "copyright": {"author_retains": true,
                                                                   "url": "http://journal-jmsr.net/aboutthejournal.php"},
                                                     "keywords": ["medical", "surgical", "clinical", "nursing",
                                                                  "pathology"], "plagiarism": {"detection": false},
                                                     "subject": [{"code": "R", "scheme": "LCC", "term": "Medicine"}],
                                                     "eissn": "2351-8200", "language": ["EN"],
                                                     "title": "Journal of Medical and Surgical Research", "article": {
        "license_display_example_url": "http://journal-jmsr.net/aboutthejournal.php", "license_display": ["Embed"]},
                                                     "preservation": {"has_preservation": true, "service": [
                                                         "Institut Marocain de l'Information Scientifique et Technique (IMIST)"],
                                                                      "url": "http://journal-jmsr.net/aboutthejournal.php"},
                                                     "license": [
                                                         {"NC": true, "ND": true, "BY": true, "type": "CC BY-NC-ND",
                                                          "SA": false}], "ref": {
        "aims_scope": "http://revues.imist.ma/?journal=JMSR&page=about&op=editorialPolicies#focusAndScope",
        "journal": "http://journal-jmsr.net/", "oa_statement": "http://journal-jmsr.net/aboutthejournal.php",
        "author_instructions": "http://revues.imist.ma/?journal=JMSR&page=about&op=submissions#authorGuidelines",
        "license_terms": "http://journal-jmsr.net/aboutthejournal.php"}, "oa_start": 2014, "alternative_title": "JMSR",
                                                     "apc": {"has_apc": false,
                                                             "url": "http://journal-jmsr.net/aboutthejournal.php"},
                                                     "other_charges": {"has_other_charges": false,
                                                                       "url": "http://journal-jmsr.net/aboutthejournal.php"},
                                                     "publication_time_weeks": 12,
                                                     "deposit_policy": {"has_policy": false},
                                                     "publisher": {"country": "MA",
                                                                   "name": "Medical and Surgical Research Journals Group"},
                                                     "boai": true, "waiver": {"has_waiver": false}},
 "admin": {"ticked": true, "seal": false}, "id": "b537a8e783d54a74b979219eae032445",
 "created_date": "2016-08-03T13:36:31Z"}
"""