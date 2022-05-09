import esprit


def get_docs(es_conn: esprit.raw.Connection, es_type: str, doc_field=None, limit: int = 200000):

    issns = set()
    count = 0
    for doc in esprit.tasks.scroll(es_conn, type=es_type, limit=limit):
        count += 1
        d = set()
        if isinstance(doc.get(doc_field), list):
            d.update(doc.get(doc_field))
        else:
            d.add(doc.get(doc_field))
        if not d:
            continue
        issns.update(d)

    return issns, count


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
    issns1, idxsize1 = get_docs(CONN1, args.type1, "issn", limit=args.limit)
    issns2, idxsize2 = get_docs(CONN2, args.type2, "issns", limit=args.limit)

    unique1 = issns1.difference(issns2)
    unique2 = issns2.difference(issns1)

    print(f'Index {args.index1} has a total of {idxsize1} documents of type {args.type1}')
    print(f'Index {args.index2} has a total of {idxsize2} documents of type {args.type2}')
    print(f'Intersection count: {len(issns1.intersection(issns2))}')
    print(f'Unique to {args.index1}: {len(unique1)}')
    print(f'Unique to {args.index2}: {len(unique2)}')

    with open(f'{args.index1}_only', 'w') as f:
        f.write(str(unique1))

    with open(f'{args.index2}_only', 'w') as g:
        g.write(str(unique2))

    print(f"Differences written to {f.name} and {g.name}")
