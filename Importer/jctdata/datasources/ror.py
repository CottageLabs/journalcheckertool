import json, csv
from copy import deepcopy
import requests, os
from jctdata import datasource
from jctdata import settings
from datetime import datetime, timedelta
from zipfile import ZipFile

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
        return {
            "origin": origin_file
        }

    def requires_update(self):
        print("ROR: Checking for latest file")
        dirs = []
        os.makedirs(self.dir, exist_ok=True)
        for entry in os.listdir(self.dir):
            if os.path.isdir(os.path.join(self.dir, entry)):
                dirs.append(entry)

        if len(dirs) == 0:
            return True

        dirs.sort(reverse=True)
        created = datetime.strptime(dirs[0], settings.ROR_DIR_DATE_FORMAT)
        latest_dt, url = self._get_latest_file()
        if latest_dt:
            return created < latest_dt
        return created + timedelta(seconds=self.max_age) < datetime.utcnow()

    def gather(self):
        latest_dt, url = self._get_latest_file()
        dir = datetime.strftime(latest_dt, settings.ROR_DIR_DATE_FORMAT)
        os.makedirs(os.path.join(self.dir, dir), exist_ok=True)
        out = os.path.join(self.dir, dir, "origin.json")

        zip_file = os.path.join(self.dir, dir, "origin.zip")

        if not os.path.exists(zip_file):
            print("ROR: downloading data dump")
            resp = requests.get(url)
            with open(zip_file, "wb") as f:
                f.write(resp.content)
        self._extract_ror_data(zip_file, out)

    def analyse(self):
        dir = self.current_dir()
        infile = os.path.join(self.dir, dir, "origin.json")
        ror_file = os.path.join(self.dir, dir, "rors.csv")
        title_file = os.path.join(self.dir, dir, "titles.csv")
        print("ROR: analysing extracted data dump {x}".format(x=infile))
        self._ror_map(infile, ror_file)
        self._title_map(infile, title_file)

    def _get_latest_file(self):
        """
        To get the tree sha,
        git clone https://github.com/ror-community/ror-api.git
        cd ror-api/rorapi/
        git ls-tree HEAD | grep data
        > 040000 tree 8ec3e0e5bce8a33c644f1544b877d756eca1a2f6    data

        Using github api to get the list of files in dir
        https://api.github.com/repos/ror-community/ror-api/git/trees/8ec3e0e5bce8a33c644f1544b877d756eca1a2f6?recursive=false

        If we wanted to get list commits in the directory
        https://api.github.com/repos/ror-community/ror-api/commits?path=rorapi/data

        ROR data file url
        https://github.com/ror-community/ror-api/raw/master/rorapi/data/ror-2021-09-23/ror.zip
        """
        url = "https://api.github.com/repos/ror-community/ror-api/git/trees/{a}?recursive=false".format(
            a=settings.ROR_TREE_SHA)
        resp = requests.get(url)
        if resp.ok:
            data_files = {}
            for fp in resp.json().get('tree', []):
                if fp.get('path', '').startswith('ror') and fp.get('type', None) == 'blob':
                    dt = fp['path'].strip('/ror.zip').strip('ror-')
                    data_files[dt] = fp['path']
            dates = list(data_files.keys())
            dates.sort(reverse=True)
            latest_dt = datetime.strptime(dates[0], settings.ROR_DIR_DATE_FORMAT)
            url = settings.ROR_DOWNLOAD_PATH + data_files[dates[0]]
            return latest_dt, url
        return None, None

    def _extract_ror_data(self, zip_file, out):
        print("ROR: extracting data dump {x}".format(x=zip_file))

        with ZipFile(zip_file, mode="r") as archive, open(out, "w") as o:
            data = archive.read("ror.json").decode(encoding="utf-8")
            j = json.loads(data)
            for ror_rec in j:
                rec = {
                    'id': ror_rec.get('id', '').replace("https://ror.org/", ''),
                    'ror': ror_rec.get('id', ''),
                    'title': ror_rec.get('name', ''),
                    'aliases': ror_rec.get('aliases', []),
                    'acronyms': ror_rec.get('acronyms', []),
                    'country': ror_rec.get('country', {}).get('country_name', '')
                }
                o.write(json.dumps(rec) + "\n")

    def _ror_map(self, infile, outfile):
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

    def _title_map(self, infile, outfile):
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


if __name__ == "__main__":
    print(datetime.utcnow())
    ror = ROR()
    if ror.requires_update():
        ror.gather()
    # ror.analyse()
    print(datetime.utcnow())
