import csv, json, itertools, os, re
from datetime import datetime

from jctdata import settings
from jctdata import resolver
from lib.title_variants import title_variants

ISSN_RX = "\d{4}-\d{3}[\dxX]"


def jac_index_data():
    print('JAC: Data for journal autocomplete start')
    paths = resolver.gather_data(["crossref", "doaj", "tj", "ta"])
    ISSNS = [
        ("crossref", paths["crossref"].get("coincident_issns")),
        ("doaj", paths["doaj"].get("coincident_issns")),
        ("tj", paths["tj"].get("coincident_issns")),
        ("ta", paths["ta"].get("coincident_issns"))
    ]
    TITLE = [
        ("crossref", paths["crossref"].get("titles")),
        ("doaj", paths["doaj"].get("titles")),
        ("tj", paths["tj"].get("titles")),
        ("ta", paths["ta"].get("titles"))
    ]
    PUB = [
        ("crossref", paths["crossref"].get("publishers")),
        ("doaj", paths["doaj"].get("publishers")),
        ("tj", paths["tj"].get("publishers"))
    ]
    journals(ISSNS, TITLE, PUB)
    print('JAC: Data for journal autocomplete end')


def journals(coincident_issn_files, title_files, publisher_files):
    print("JAC: Preparing journal autocomplete data")
    dir = datetime.strftime(datetime.utcnow(), settings.DIR_DATE_FORMAT)
    jacdir = os.path.join(settings.DATABASES, "jct", "jac", dir)
    os.makedirs(jacdir, exist_ok=True)
    issn_clusters_file = os.path.join(jacdir, "issn_clusters.csv")

    preference_order = settings.JAC_PREF_ORDER

    outfile = os.path.join(jacdir, "jac.json")

    issn_clusters(coincident_issn_files, issn_clusters_file)
    titlerows = _cat_and_dedupe(title_files)
    titles = _cluster_to_dict(titlerows, 3)
    pubrows = _cat_and_dedupe(publisher_files)
    publishers = _cluster_to_dict(pubrows, 2)

    with open(issn_clusters_file, "r") as f, open(outfile, "w") as o:
        reader = csv.reader(f)
        for row in reader:
            vissns = valid_issns(row)
            if len(vissns) == 0:
                continue

            record = {"issns": vissns}
            main, alts = _get_titles(vissns, titles, preference_order)
            if main is None:
                continue
            record["title"] = main
            if len(alts) > 0:
                record["alts"] = alts

            publisher = _get_publisher(vissns, publishers, preference_order)
            if publisher is not None:
                record["publisher"] = publisher

            _index(record)

            o.write(json.dumps(record) + "\n")


def valid_issns(issns):
    return [issn.upper() for issn in issns if re.match(ISSN_RX, issn)]


def issn_clusters(coincident_issn_files, clusters_file):
    issn_clusters = []

    inputs = _cat_and_dedupe(coincident_issn_files)
    inputs.sort(key=lambda x: x[0])

    current_issn_root = None
    current_cluster = []
    for row in inputs:
        if not current_issn_root:
            current_issn_root = row[0]
            current_cluster.append(row[0])
        if current_issn_root != row[0]:
            # the issn has changed, so we can write the current cluster
            current_cluster = list(set(current_cluster))
            current_cluster.sort()
            issn_clusters.append(current_cluster)

            current_cluster = [row[0]]
            current_issn_root = row[0]

        if row[1]:
            current_cluster.append(row[1])

    issn_clusters.sort()
    issn_clusters = list(k for k,_ in itertools.groupby(issn_clusters))

    with open(clusters_file, "w") as f:
        writer = csv.writer(f)
        writer.writerows(issn_clusters)


def _cat_and_dedupe(files):
    inputs = []
    for source, cif in files:
        with open(cif, "r") as f:
            reader = csv.reader(f)
            inputs += [row + [source] for row in reader]

    inputs.sort()
    inputs = list(k for k, _ in itertools.groupby(inputs))
    return inputs


def _cluster_to_dict(rows, n):
    d = {}
    for row in rows:
        if row[0] not in d:
            d[row[0]] = []
        d[row[0]].append([row[x+1] for x in range(n)])
    return d


def _extract_preferred(title_source_pairs, preference_order):
    selected = None
    idx = -1
    for pref in preference_order:
        for i, tup in enumerate(title_source_pairs):
            source, title = tup
            if pref == source:
                selected = title
                idx = i
                break

    if selected is None:
        selected = title_source_pairs[0][0]
        idx = 0

    del title_source_pairs[idx]
    return selected


def _get_titles(issns, titles, preference_order):
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
        main = _extract_preferred(alts, preference_order)
        return main, [x for x in list(set([a[0] for a in alts])) if x != main]

    if len(mains) == 1:
        return mains[0][0], [x for x in list(set([a[0] for a in alts])) if x != mains[0][0]]

    main = _extract_preferred(mains, preference_order)
    return main, [x for x in list(set([m[0] for m in mains] + [a[0] for a in alts])) if x != main]


def _get_publisher(issns, publishers, preference_order):
    pubs = []

    for issn in issns:
        candidates = publishers.get(issn, [])
        for c in candidates:
            pubs.append((c[0].strip(), c[1].strip()))

    if len(pubs) == 0:
        return None

    pub = _extract_preferred(pubs, preference_order)
    return pub


def _index(record):
    idx = {}

    idx["issns"] = [issn.lower() for issn in record["issns"]]
    idx["issns"] += [issn.replace("-", "") for issn in idx["issns"]]

    idx["title"] = title_variants(record["title"])

    if "alts" in record:
        idx["alts"] = []
        for alt in record["alts"]:
            idx["alts"] += title_variants(alt)
        idx["alts"] = list(set(idx["alts"]))

    record["index"] = idx


if __name__ == "__main__":
    print(datetime.utcnow())
    jac_index_data()
    print(datetime.utcnow())