import csv, time, requests

def all_from_oaworks(issns, out_base, batch=10000, limit=200000, offset=0):
    ISSNS = issns
    OAW = "https://api.openaccessbutton.org/permissions?issn="
    OUT = out_base
    BATCH = batch
    LIMIT = limit
    OFFSET = offset

    with open(ISSNS, "r") as f:
        reader = csv.reader(f)

        batch_num = 1
        g = open(OUT + "." + str(batch_num) + ".csv", "w")
        writer = csv.writer(g)

        i = 0
        for row in reader:
            i += 1

            if i > LIMIT:
                break

            if i < OFFSET:
                continue

            if i > BATCH * batch_num:
                batch_num += 1
                g.close()
                g = open(OUT + "." + str(batch_num) + ".csv", "w")
                writer = csv.writer(g)
                print("starting batch", batch_num)

            ident = [row[0], row[1], row[2]]

            issn_no = 0
            while True:
                if issn_no > 1:
                    writer.writerow(ident)
                    break

                issn = row[issn_no]
                if not issn:
                    issn_no += 1
                    continue

                oaw_url = OAW + issn
                print(i, issn, oaw_url)

                time.sleep(0.3)
                try:
                    resp = requests.get(oaw_url, timeout=10)
                except:
                    writer.writerow(ident + ["TIMEOUT"])
                    time.sleep(5)
                    issn_no += 1
                    continue

                if resp.status_code != 200:
                    issn_no += 1
                    continue

                d = resp.json()
                if len(d.get("all_permissions", [])) == 0:
                    issn_no += 1
                    continue

                total = str(len(d["all_permissions"]))
                for j, perm in enumerate(d["all_permissions"]):
                    out = ident + [
                        issn,
                        str(j+1) + "/" + total,
                        perm.get("score", 0),
                        perm.get("issuer", {}).get("journal_oa_type", ""),
                        perm.get("licence"),
                        ", ".join(l["type"] for l in perm.get("licences", [])),
                        perm.get("version"),
                        ", ".join(perm.get("versions", [])),
                        ", ".join(perm.get("requirements", {}).get("funder", []))
                    ]
                    writer.writerow(out)
                break

        g.close()

if __name__ == "__main__":
    ISSNS = "databases/crossref/crossref.csv"
    OUT = "databases/oaworks/oaworks_3"
    OFFSET = 63327
    BATCH = 10000
    LIMIT = 110000
    all_from_oaworks(ISSNS, OUT, BATCH, LIMIT, OFFSET)