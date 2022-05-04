import csv


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


def simple_property_extract(source, outfile, property=0, identifiers=None, skip_title_row=False, info=None):
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
                            newrow = [row[i], row[property]]
                            if info:
                                newrow.append(info)
                            writer.writerow(newrow)