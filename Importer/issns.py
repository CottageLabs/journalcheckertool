import csv, esprit

def issns_from_index(out, es_conn, limit=200000):
    OUT = out
    LIMIT = limit
    CONN = es_conn

    with open(OUT, "w") as f:
        writer = csv.writer(f)

        for journal in esprit.tasks.scroll(CONN, "journal", limit=LIMIT):
            issns = journal.get("issn")
            title = journal.get("title")

            if len(issns) == 0:
                continue
            if len(issns) == 1:
                issns.append("")

            writer.writerow(issns + [title])


if __name__ == "__main__":
    OUT = "/home/richard/tmp/jct_tests/allissns.csv"
    LIMIT = 200000
    CONN = esprit.raw.Connection("http://localhost:9200", "jct_dev")
    issns_from_index(OUT, CONN, LIMIT)