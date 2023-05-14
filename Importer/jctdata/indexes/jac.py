import csv, json, itertools, os, re, shutil
from datetime import datetime

from jctdata import settings
from jctdata import resolver
from jctdata.lib.title_variants import title_variants
from jctdata.lib.analysis import cat_and_dedupe, issn_clusters, cluster_to_dict, extract_preferred
from jctdata.indexes.indexer import Indexer


class JAC(Indexer):
    ID = "jac"
    SOURCES = ["crossref", "doaj", "tj", "ta", "doaj_inprogress", "sa_negative", "sa_positive", "oa_exceptions", "jcs"]

    def gather(self):
        self.log('Gathering data for journal autocomplete from sources: {x}'.format(x=",".join(self.SOURCES)))
        paths = resolver.gather_data(self.SOURCES, True)

        issns, titles, pubs = self._get_paths(paths)

        self.log("ISSN sources: " + ", ".join([x[0] for x in issns]))
        self.log("TITLE sources: " + ", ".join([x[0] for x in titles]))
        self.log("PUB sources: " + ", ".join([x[0] for x in pubs]))

    def analyse(self):
        self.log("Analysing data for journal autocomplete")
        dir = datetime.strftime(datetime.utcnow(), settings.DIR_DATE_FORMAT)
        jacdir = os.path.join(self.dir, dir)
        os.makedirs(jacdir, exist_ok=True)

        issn_clusters_file = os.path.join(jacdir, "issn_clusters.csv")
        titles_file = os.path.join(jacdir, "titles.csv")
        pubs_file = os.path.join(jacdir, "pubs.csv")

        pathset = {}
        for s in self.SOURCES:
            pathset[s] = resolver.SOURCES[s].current_paths()
        issns, titles, pubs = self._get_paths(pathset)

        issn_clusters(issns, issn_clusters_file)
        titlerows = cat_and_dedupe(titles)
        pubrows = cat_and_dedupe(pubs)

        with open(titles_file, "w") as f:
            writer = csv.writer(f)
            writer.writerows(titlerows)

        with open(pubs_file, "w") as f:
            writer = csv.writer(f)
            writer.writerows(pubrows)

        self.log("analysed data written to directory {x}".format(x=jacdir))

    def assemble(self):
        self.log("Preparing journal autocomplete data")

        preference_order = settings.JAC_PREF_ORDER
        jacdir = os.path.join(self.dir, self.current_dir())
        outfile = os.path.join(jacdir, "jac.json")

        issn_clusters_file = os.path.join(jacdir, "issn_clusters.csv")
        titles_file = os.path.join(jacdir, "titles.csv")
        pubs_file = os.path.join(jacdir, "pubs.csv")

        with open(titles_file) as f:
            reader = csv.reader(f)
            titlerows = [row for row in reader]

        with open(pubs_file) as f:
            reader = csv.reader(f)
            pubrows = [row for row in reader]

        titles = cluster_to_dict(titlerows, 3)
        publishers = cluster_to_dict(pubrows, 2)

        with open(issn_clusters_file, "r") as f, open(outfile, "w") as o:
            reader = csv.reader(f)
            for vissns in reader:
                record = {"issns": vissns}
                main, alts = self._get_titles(vissns, titles, preference_order)
                if main is not None:
                    record["title"] = main
                else:
                    record["title"] = ""
                if len(alts) > 0:
                    record["alts"] = alts

                publisher = self._get_publisher(vissns, publishers, preference_order)
                if publisher is not None:
                    record["publisher"] = publisher

                self._index(record)

                o.write(json.dumps(record) + "\n")

        self.log("Journal Autocomplete data assembled")

        self._cleanup()

    def _get_paths(self, paths):
        issns = []
        titles = []
        pubs = []
        for source, files in paths.items():
            if "coincident_issns" in files:
                issns.append((source, files["coincident_issns"]))
            if "titles" in files:
                titles.append((source, files["titles"]))
            if "publishers" in files:
                pubs.append((source, files["publishers"]))

        return issns, titles, pubs

    def _get_titles(self, issns, titles, preference_order):
        mains = []
        alts = []

        for issn in issns:
            candidates = titles.get(issn, [])
            for c in candidates:
                if c[1] == "main":
                    mains.append((c[0].strip(), c[2].strip()))
                elif c[1] == "alt":
                    alts.append((c[0].strip(), c[2].strip()))

        if len(mains) == 0:
            # if there are no titles, return an empty state
            if len(alts) == 0:
                return None, alts
            # otherwise return the best title from the alternates
            main = extract_preferred(alts, preference_order)
            return main, [x for x in list(set([a[0] for a in alts])) if x != main]

        if len(mains) == 1:
            return mains[0][0], [x for x in list(set([a[0] for a in alts])) if x != mains[0][0]]

        main = extract_preferred(mains, preference_order)
        return main, [x for x in list(set([m[0] for m in mains] + [a[0] for a in alts])) if x != main]

    def _get_publisher(self, issns, publishers, preference_order):
        pubs = []

        for issn in issns:
            candidates = publishers.get(issn, [])
            for c in candidates:
                pubs.append((c[0].strip(), c[1].strip()))

        if len(pubs) == 0:
            return None

        pub = extract_preferred(pubs, preference_order)
        return pub

    def _index(self, record):
        idx = {}

        idx["issns"] = [issn.lower() for issn in record["issns"]]
        idx["issns"] += [issn.replace("-", "") for issn in idx["issns"]]

        idx["title"] = title_variants(record.get("title", ""))
        idx["alts"] = idx["title"]  # This helps with getting better index scores because alts also contains the main titles

        if "alts" in record:
            for alt in record["alts"]:
                idx["alts"] += title_variants(alt)
            idx["alts"] = list(set(idx["alts"]))

        record["index"] = idx

