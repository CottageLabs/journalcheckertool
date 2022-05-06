""" Compare a number of fields (e.g. ISSN, title...) across equivalent indexes / types """

import esprit, json


def get_docs(es_conn: esprit.raw.Connection, es_type: str, doc_field: tuple, limit: int = 200000):
    docs = set()
    for doc in esprit.tasks.scroll(es_conn, type=es_type, limit=limit):
        d = set()
        for f in doc_field:
            if isinstance(doc.get(f), list):
                d.add(json.dumps(sorted(doc.get(f))))
            else:
                d.add(doc.get(f))
        if not d:
            continue
        docs.add(tuple(d))
    return docs


if __name__ == "__main__":
    LIMIT = 200000
    CONN1 = esprit.raw.Connection("http://10.131.177.187:9200", "jct_dev")
    CONN2 = esprit.raw.Connection("http://10.131.177.187:9200", "jct_jac_dev20220422180207")
    docs1 = get_docs(CONN1, 'journal', ('issn',))
    docs2 = get_docs(CONN2, 'jac', ('issns',))

    print(len(docs1.intersection(docs2)))
    print(len(docs1.difference(docs2)))
    print(len(docs2.difference(docs1)))
