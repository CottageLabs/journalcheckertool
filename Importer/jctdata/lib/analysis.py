import csv
import itertools
import re

ISSN_RX = "^\d{4}-\d{3}[\dxX]$"


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


def simple_property_extract(source, outfile, property=0, identifiers=None, skip_title_row=False, info=None, property_function=None):
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
                            prop = row[property]
                            if property_function:
                                prop = property_function(prop)
                            newrow = [row[i], prop]
                            if info:
                                newrow.append(info)
                            writer.writerow(newrow)


def cat_and_dedupe(files):
    inputs = []
    for source, cif in files:
        with open(cif, "r") as f:
            reader = csv.reader(f)
            inputs += [row + [source] for row in reader]

    inputs.sort()
    inputs = list(k for k, _ in itertools.groupby(inputs))
    return inputs


def issn_clusters(coincident_issn_files, clusters_file):
    issn_clusters = []

    inputs = cat_and_dedupe(coincident_issn_files)
    inputs = remove_invalid_issns(inputs)
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

        if len(row) > 1 and row[1]:
            current_cluster.append(row[1])

    issn_clusters.sort()
    issn_clusters = list(k for k,_ in itertools.groupby(issn_clusters))

    d = {}
    for row in issn_clusters:
        if row[0] not in d:
            d[row[0]] = []
        d[row[0]] += [row[x + 1] for x in range(len(row) - 1)]

    # go through every key, and for each value in the array associated with it, look
    # for the key of that value.  This will lead to another set of values.  For each
    # of those transitive values that are not the original key and are not in the
    # original list of values, add it to a list of additional values to add.  Then remove
    # the key of the value, so we don't count it again.
    #
    # In this way, we "consume" all the values into their unique super-clusters by
    # expanding the first list of values with values from all transitive lists.
    # In theory we end up with a unique list of coincident identifiers, with all
    # smaller subsets of the larger cluster subsumed into one.
    keys = list(d.keys())
    for k in keys:
        if k not in d:
            continue
        additions = []
        for e in d[k]:
            if e in d:
                additions += [x for x in d[e] if x != k and x not in d[k]]
                del d[e]
        d[k] = list(set(d[k] + additions))

    rows = []
    for k, v in d.items():
        rows.append([k] + v)

    with open(clusters_file, "w") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def cluster_to_dict(rows, n):
    d = {}
    for row in rows:
        if row[0] not in d:
            d[row[0]] = []
        d[row[0]].append([row[x+1] for x in range(n)])
    return d


def remove_invalid_issns(input):
    valid = []
    for row in input:
        newrow = valid_issns(row)
        if len(newrow) > 0:
            valid.append(newrow)
    return valid


def valid_issns(issns):
    return [issn.upper() for issn in issns if re.match(ISSN_RX, issn)]


def extract_preferred(source_pairs, preference_order):
    selected = None
    idx = -1
    for pref in preference_order:
        opts = []
        for i, tup in enumerate(source_pairs):
            title, source = tup
            if pref == source:
                opts.append((i, title))

        if len(opts) == 0:
            continue

        countopts = {}
        for opt in opts:
            if opt[1] not in countopts:
                countopts[opt[1]] = {"count": 1, "idx": [opt[0]]}
            else:
                countopts[opt[1]]["count"] += 1
                countopts[opt[1]]["idx"].append(opt[0])

        selected_count = 0
        for k, v in countopts.items():
            if v["count"] > selected_count:
                selected = k
                selected_count = v["count"]
                idx = v["idx"][0]

        break

    if selected is None:
        selected = source_pairs[0][0]
        idx = 0

    del source_pairs[idx]
    return selected
