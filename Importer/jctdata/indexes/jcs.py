import csv, json, itertools, os, re, shutil
from datetime import datetime

from jctdata import settings
from jctdata import resolver
from jctdata.lib.title_variants import title_variants
from jctdata.lib.analysis import cat_and_dedupe, issn_clusters, cluster_to_dict, extract_preferred
from jctdata.indexes.indexer import Indexer


class JCS_CSV(Indexer):
    ID = "jcs_csv"
    SOURCES = ["jcs"]

    def gather(self):
        self.log('Gathering data for jcs csv from sources: {x}'.format(x=",".join(self.SOURCES)))
        paths = resolver.gather_data(self.SOURCES, True)
        self.log("ORIGIN source: " + paths["jcs"]["origin"])

    def analyse(self):
        self.log("Analysing data for jcs csv")
        dir = datetime.strftime(datetime.utcnow(), settings.DIR_DATE_FORMAT)
        jcsdir = os.path.join(self.dir, dir)
        os.makedirs(jcsdir, exist_ok=True)

        pathset = resolver.SOURCES["jcs"].current_paths()
        origin_file = pathset.get("origin")

        data = {}
        with open(origin_file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] not in data:
                    data[row[0]] = {
                        "title": row[1],
                        "publisher": row[2],
                        "years": []
                    }
                year = int(row[3])
                if year not in data[row[0]]["years"]:
                    data[row[0]]["years"].append(year)

        current_data_year = self._current_data_year()
        filtered_data = {k: v for k, v in data.items() if max([int(y) for y in v["years"]]) >= current_data_year}

        filtered_file = os.path.join(jcsdir, "filtered.csv")
        with open(filtered_file, "w") as f:
            writer = csv.writer(f)
            keys = sorted(list(filtered_data.keys()))
            for k in keys:
                v = filtered_data[k]
                years = sorted(v["years"])
                writer.writerow([k, v["title"], v["publisher"], ", ".join([str(y) for y in years])])

        self.log("analysed data written to directory {x}".format(x=jcsdir))

    def assemble(self):
        self.log("Preparing jcs csv")
        dir = self.current_dir()
        filter_file = os.path.join(self.dir, dir, "filtered.csv")
        publish_file = os.path.join(self.dir, dir, self.ID + ".csv")
        with open(publish_file, "w") as f, open(filter_file, "r") as g:
            f.write("ISSN, Journal Title, Publisher, Years available\n")
            f.write(g.read())

        self.log("jcs csv data assembled")
        self._cleanup()


    def _current_data_year(self):
        current_date = datetime.utcnow()
        year_current = current_date.year
        rollover_date = datetime.strptime(str(year_current) + "-11-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
        cutoff_year = year_current - 1
        if current_date < rollover_date:
            cutoff_year = year_current - 2
        return cutoff_year

