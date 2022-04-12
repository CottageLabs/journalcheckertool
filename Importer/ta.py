import csv, requests, os


def retrieve_ta_data(index, outdir):
    with open(index, "r") as f:
        reader = csv.reader(f)
        first = True
        for i, row in enumerate(reader):
            if first:
                first = False
                continue
            data_url = row[4]
            print("{y} retrieving from {x}".format(x=data_url, y=i))
            try:
                resp = requests.get(data_url, timeout=10)
            except requests.Timeout:
                print("{y} TIMEOUT: {x}".format(x=data_url, y=i))
            if resp.status_code != 200:
                print("{y} ERROR: Failed to retrieve {x}".format(x=data_url, y=i))
            else:
                print("{y} Retrieved {x} [{z}]".format(x=row[0], y=i, z=row[1]))

            fn = row[0]
            if row[1]:
                fn += "." + row[1]
            fn = "".join([c for c in fn if c.isalpha() or c.isdigit() or c in ' .']).rstrip()
            fn += ".csv"

            outfile = os.path.join(outdir, fn)
            with open(outfile, "w") as o:
                o.write(resp.text)
            print("{y} saved to {x}".format(y=i, x=fn))


if __name__ == "__main__":
    INDEX = "databases/ta/taindex.csv"
    OUTDIR = "databases/ta"
    retrieve_ta_data(INDEX, OUTDIR)