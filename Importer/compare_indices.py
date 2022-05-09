""" Compare a number of fields (e.g. ISSN, title...) across equivalent indexes / types """

import esprit, json


def get_docs(es_conn: esprit.raw.Connection, es_type: str, doc_field: tuple, limit: int = 200000):
    docset = set()
    docs = {}
    for doc in esprit.tasks.scroll(es_conn, type=es_type, limit=limit):
        d = set()
        for f in doc_field:
            if isinstance(doc.get(f), list):
                d.add(json.dumps(sorted(doc.get(f))))
            else:
                d.add(doc.get(f))
        if not d:
            continue
        docset.add(tuple(d))
        docs[tuple(d)] = doc
    return docset, docs


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--limit', help='scroll limit (total number of results -make this big for a fair comparison!)', default=200000)
    parser.add_argument('-e', '--eshost', help='elasticsearch host (proto, host, port)', default='http://10.131.177.187:9200')
    parser.add_argument('-i1', '--index1', help='first index to compare', default='jct_dev')
    parser.add_argument('-t1', '--type1', help='first type to compare', default='journal')
    parser.add_argument('-i2', '--index2', help='second index to compare', default='jct_jac_dev')
    parser.add_argument('-t2', '--type2', help='second type to compare', default='jac')
    args = parser.parse_args()

    CONN1 = esprit.raw.Connection(args.eshost, args.index1)
    CONN2 = esprit.raw.Connection(args.eshost, args.index2)
    docset1, docs1 = get_docs(CONN1, args.type1, ('issn',), limit=args.limit)
    docset2, docs2 = get_docs(CONN2, args.type2, ('issns',), limit=args.limit)

    print(f'Index {args.index1} has a total of {len(docset1)} documents of type {args.type1}')
    print(f'Index {args.index2} has a total of {len(docset2)} documents of type {args.type2}')
    print(f'Intersection count: {len(docset1.intersection(docs2))}')
    print(f'Unique to {args.index1}: {len(docset1.difference(docs2))}')
    print(f'Unique to {args.index2}: {len(docset2.difference(docs1))}')

    with open(f'{args.index1}_only', 'w') as f:
        json.dump([v for k, v in docs1.items() if k in docset1.difference(docs2)], f, indent=2)

    with open(f'{args.index2}_only', 'w') as g:
        json.dump([v for k, v in docs2.items() if k in docset2.difference(docs1)], g, indent=2)

    print(f"Differences written to {f.name} and {g.name}")
