import csv, time, requests
import json
import os
from datetime import datetime

OAW = "https://api.oa.works/permissions?issn="

def read_issn(issn, out_dir):
    oaw_url = OAW + issn
    print(issn, oaw_url)

    try:
        resp = requests.get(oaw_url, timeout=10)
    except:
        print("TIMEOUT?")

    parts = issn.split("-")
    out = os.path.join(out_dir, parts[0], parts[1])
    os.makedirs(out, exist_ok=True)

    return

def all_from_oaworks(journals_base, out_base, batch=10000, limit=200000, offset=0):

    jdirs = os.listdir(journals_base)
    if len(jdirs) == 0:
        print("no journals found")
        return

    jdirs.sort()
    jlatest = jdirs[0]

    out_dir = os.path.join(out_base, datetime.utcnow().strftime("%Y-%m-%d_%H%M"))

    with open(os.path.join(jlatest, "journal.json"), "r") as f:
        for line in f:
            journal = json.loads(line)
            issns = journal.get("issn", [])
            for issn in issns:
                read_issn(issn, out_dir)


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
    JOURNALS = "databases/jct/journal"
    OUT = "databases/oaworks"
    all_from_oaworks(JOURNALS, OUT)