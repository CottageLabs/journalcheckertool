import csv, os
import itertools


def analyse(issns, out, batch, oaworks_dir, doaj_file, tj_file, ta_dir, limit):
    LIMIT = limit

    oaworks_data = oaworks_load(oaworks_dir)
    doaj_data = doaj_load(doaj_file)
    tj_data = tj_load(tj_file)
    ta_data = ta_load(ta_dir)

    issn_registry = []

    with open(issns, "r") as f1:

        batch_num = 1
        f2 = open(out + "." + str(batch_num) + ".csv", "w")

        issnreader = csv.reader(f1)
        writer = csv.writer(f2)

        for j, row in enumerate(issnreader):
            if j > LIMIT:
                break

            if j > batch * batch_num:
                batch_num += 1
                f2.close()
                f2 = open(OUT + "." + str(batch_num) + ".csv", "w")
                writer = csv.writer(f2)
                print("starting batch", batch_num)

            issn_list = []
            if row[0]:
                issn_list.append(row[0])
            if row[1]:
                issn_list.append(row[1])
            print("{x}: {y}".format(x=j, y=",".join(issn_list)))

            for issn in issn_list:
                if issn in issn_registry:
                    continue
                issn_registry.append(issn)

                row_set = assemble_on_issn(issn, oaworks_data, doaj_data, tj_data, ta_data)
                for i, r in enumerate(row_set):
                    finalrow = [
                        r[0],   # the issn
                        row[2], # the title
                        str(i + 1) + "/" + str(len(row_set)),   # batch information
                    ] + r[1:]
                    writer.writerow(finalrow)

        f2.close()

def assemble_on_issn(issn, oaworks_data, doaj_data, tj_data, ta_data):
    # row_set = [[issn]]
    # row_set = oaworks(issn, row_set, oaworks_dir)
    # row_set = doaj(issn, row_set, doaj_file)
    # row_set = tj(issn, row_set, tj_file)
    # row_set = ta(issn, row_set, ta_dir)
    # return row_set
    row_set = [[issn]]
    row_set = oaworks_extract(issn, row_set, oaworks_data)
    row_set = doaj_extract(issn, row_set, doaj_data)
    row_set = tj_extract(issn, row_set, tj_data)
    row_set = ta_extract(issn, row_set, ta_data)
    return row_set


def ta_load(ta_dir):
    data = {}
    for file in os.listdir(ta_dir):
        if file == "taindex.csv":
            continue

        path = os.path.join(ta_dir, file)
        with open(path, "r") as f:
            reader = csv.reader(f)
            reader.__next__()

            taname = file.rsplit(".", 1)[0]
            data[taname] = [row for row in reader]

    return data


def ta_extract(issn, row_set, ta_data):
    tas = []
    for ta_name, data in ta_data.items():
        for row in data:
            if issn == row[1] or issn == row[2]:
                tas.append(ta_name)

    data = []
    if len(tas) == 0:
        data.append(["", ""])
    else:
        data.append(["TA", ",".join(tas)])

    return _combine(row_set, data)


def ta(issn, row_set, ta_dir):
    tas = []
    for file in os.listdir(ta_dir):
        if file == "taindex.csv":
            continue

        path = os.path.join(ta_dir, file)
        with open(path, "r") as f:
            reader = csv.reader(f)
            first = True
            for row in reader:
                if first:
                    first = False
                    continue

                if issn == row[1] or issn == row[2]:
                    tas.append(file.rsplit(".", 1)[0])

    data = []
    if len(tas) == 0:
        data.append(["", ""])
    else:
        data.append(["TA", ",".join(tas)])

    return _combine(row_set, data)


def tj_load(tj_file):
    data = []
    with open(tj_file, "r") as f:
        reader = csv.reader(f)
        reader.__next__()
        data = [row for row in reader]
    return data


def tj_extract(issn, row_set, tj_data):
    data = []
    for row in tj_data:
        if issn == row[1] or issn == row[1]:
            data.append(["TJ"])
            break

    if len(data) == 0:
        data.append([""])

    return _combine(row_set, data)


def tj(issn, row_set, tj_file):
    data = []
    with open(tj_file, "r") as f:
        reader = csv.reader(f)
        first = True
        for row in reader:
            if first:
                first = False
                continue

            if issn == row[1] or issn == row[1]:
                data.append(["TJ"])

    if len(data) == 0:
        data.append([""])

    return _combine(row_set, data)


def doaj_load(doaj_file):
    data = []
    with open(doaj_file, "r") as f:
        reader = csv.reader(f)
        data = [row for row in reader]
    return data


def doaj_extract(issn, row_set, doaj_data):
    data = []
    for row in doaj_data:
        if (issn == row[0] or issn == row[1]) and len(row) >= 5:
            data.append([row[4]])

    if len(data) == 0:
        data.append([""])

    return _combine(row_set, data)


def doaj(issn, row_set, doaj_file):
    data = []
    with open(doaj_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if (issn == row[0] or issn == row[1]) and len(row) >= 5:
                data.append([row[4]])

    if len(data) == 0:
        data.append([""])

    return _combine(row_set, data)


def oaworks_load(oaworks_dir):
    data = []
    for file in os.listdir(oaworks_dir):
        path = os.path.join(oaworks_dir, file)
        with open(path, "r") as f:
            reader = csv.reader(f)
            data += [row for row in reader]

    # data.sort(key=lambda x: x[0] + x[1])

    return data


def oaworks_extract(issn, row_set, oaworks_data):
    data = []
    for row in oaworks_data:
        if (issn == row[0] or issn == row[1]) and len(row) >= 10:
            data.append([row[6], row[7], row[8], row[9], row[10]])
    if len(data) == 0:
        data.append(["", "", "", "", ""])
    return _combine(row_set, data)


def oaworks(issn, row_set, oaworks_dir):
    data = []
    for file in os.listdir(oaworks_dir):
        path = os.path.join(oaworks_dir, file)
        with open(path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if (issn == row[0] or issn == row[1]) and len(row) >= 10:
                    data.append([row[6], row[7], row[8], row[9], row[10]])
            if len(data) > 0:
                break

    if len(data) == 0:
        data.append(["", "", "", "", ""])
    return _combine(row_set, data)


def _combine(source, additional):
    if len(additional) == 0:
        return source

    # deduplicate the additionals
    additional.sort()
    additional = list(k for k,_ in itertools.groupby(additional))

    new_data = []
    for s in source:
        for a in additional:
            new_data.append(s + a)
    return new_data


if __name__ == "__main__":
    ISSNS = "databases/crossref/crossref.csv"
    OUT = "databases/jct/assembled-2022-03-28"
    OAW = "databases/oaworks"
    DOAJ = "databases/doaj/doaj.csv"
    TJ = "databases/tj/tj.csv"
    TA = "databases/ta"
    BATCH = 20000
    LIMIT = 200000

    analyse(ISSNS, OUT, BATCH, OAW, DOAJ, TJ, TA, LIMIT)