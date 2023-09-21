import json, csv, requests, os, shutil
from jctdata import datasource
from jctdata import settings
from datetime import datetime, timedelta
from zipfile import ZipFile
from deprecated import deprecated


class ROR(datasource.Datasource):
    ID = "ror"

    def current_paths(self):
        dir = self.current_dir()
        # ror_file = os.path.join(self.dir, dir, "rors.csv")
        # title_file = os.path.join(self.dir, dir, "titles.csv")
        # return {
        #     "rors": ror_file,
        #     "titles": title_file
        # }
        origin_file = os.path.join(self.dir, dir, "origin.json")
        ror_file = os.path.join(self.dir, dir, "rors.csv")
        return {
            "origin": origin_file,
            "rors": ror_file
        }

    # def requires_update(self):
    #     print("ROR: Checking for latest file")
    #     dirs = []
    #     os.makedirs(self.dir, exist_ok=True)
    #     for entry in os.listdir(self.dir):
    #         if os.path.isdir(os.path.join(self.dir, entry)):
    #             dirs.append(entry)
    #
    #     if len(dirs) == 0:
    #         return True
    #
    #     dirs.sort(reverse=True)
    #     created = datetime.strptime(dirs[0], settings.ROR_DIR_DATE_FORMAT)
    #     latest_dt, url = self._get_latest_file()
    #     if latest_dt:
    #         return created < latest_dt
    #     return created + timedelta(seconds=self.max_age) < datetime.utcnow()

    def gather(self):
        dir = datetime.strftime(datetime.utcnow(), settings.DIR_DATE_FORMAT)
        zip_file = os.path.join(self.dir, dir, "origin.zip")
        os.makedirs(os.path.join(self.dir, dir), exist_ok=True)

        if settings.ROR_DATA_FILE and os.path.exists(settings.ROR_DATA_FILE):
            self.log("extracting data from locally supplied file {x}".format(x=settings.ROR_DATA_FILE))
            shutil.copy(settings.ROR_DATA_FILE, zip_file)
        else:
            latest_dt, url = self._get_latest_file()
            if not os.path.exists(zip_file):
                self.log("downloading data dump from {x}".format(x=url))
                resp = requests.get(url)
                with open(zip_file, "wb") as f:
                    f.write(resp.content)

        out = os.path.join(self.dir, dir, "origin.json")
        self._extract_ror_data(zip_file, out)

    def analyse(self):
        dir = self.current_dir()
        infile = os.path.join(self.dir, dir, "origin.json")
        ror_file = os.path.join(self.dir, dir, "rors.csv")
        title_file = os.path.join(self.dir, dir, "titles.csv")
        self.log("analysing extracted data dump {x}".format(x=infile))
        self._ror_map(infile, ror_file)
        self._title_map(infile, title_file)

    def _get_latest_file(self):
        """
        Download latest data file through zenodo
        """
        record = None
        url = settings.ZENODO_ROR_DOWNLOAD_PATH
        resp = requests.get(url)
        hits = resp.json().get('hits', {})
        # Get the first record
        if "hits" in hits:
            hits_hits = hits.get("hits", [])
            if len(hits_hits) > 0:
                record = hits["hits"][0]

        if record:
            latest_dt = datetime.fromisoformat(record["created"]).strftime(settings.ROR_DIR_DATE_FORMAT)
            files = record.get("files", [])
            files_count = len(files)
            # Get the last file which is latest
            if files_count > 0:
                file = files[files_count - 1]
                url = file["links"]["self"]
                return latest_dt, url

        return None, None

    def _extract_ror_data(self, zip_file, out):
        self.log("extracting data dump {x}".format(x=zip_file))

        with ZipFile(zip_file, mode="r") as archive, open(out, "w") as o:
            rorfile = None
            for zi in archive.infolist():
                if zi.filename.endswith(".json") and not zi.filename.startswith("."):
                    rorfile = zi
                    break

            if rorfile is None:
                raise Exception("Unable to extract ROR JSON file")

            data = archive.read(rorfile).decode(encoding="utf-8")
            j = json.loads(data)
            for ror_rec in j:
                if ror_rec["status"] != "withdrawn":
                    rec = {
                        'id': ror_rec.get('id', '').replace("https://ror.org/", ''),
                        'ror': ror_rec.get('id', ''),
                        'title': ror_rec.get('name', ''),
                        'aliases': ror_rec.get('aliases', []),
                        'acronyms': ror_rec.get('acronyms', []),
                        'country': ror_rec.get('country', {}).get('country_name', '')
                    }
                    o.write(json.dumps(rec) + "\n")

    @staticmethod
    def _ror_map(infile, outfile):
        rors = []
        # listing all rors
        with open(infile, "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                rec = json.loads(line)
                rors.append(rec.get('id', ''))
        # ROR should be unique, but just checking for duplicate entries
        # Writing to list of all RORs to csv
        list(set(rors))
        with open(outfile, "w") as o:
            writer = csv.writer(o)
            # writer.writerow(['ror'])
            for ror in rors:
                writer.writerow([ror])

    @staticmethod
    def _title_map(infile, outfile):
        with open(outfile, "w") as o:

            writer = csv.writer(o)
            # writer.writerow(['ror','title','country','type'])
            with open(infile, "r") as f:
                while True:
                    line = f.readline()
                    if not line:
                        break
                    rec = json.loads(line)
                    # row = ror,title,country,type
                    ror = rec.get('id', '')
                    title = rec.get('title', '')
                    aliases = rec.get('aliases', [])
                    acronyms = rec.get('acronyms', [])
                    country = rec.get('country', '')
                    if not ror:
                        continue
                    if title:
                        writer.writerow([ror, title, country, 'main'])
                    for a in aliases:
                        writer.writerow([ror, a, country, 'alias'])
                    for a in acronyms:
                        writer.writerow([ror, a, country, 'acronym'])

