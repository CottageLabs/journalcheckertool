import os
import json
from datetime import datetime
import requests
import esprit
from jctdata import settings
from lib.send_mail import send_mail


def get_old_counts():
    counts_file = os.path.join(settings.DATABASES, 'counts.json')
    if os.path.exists(counts_file):
        with open(counts_file, 'r') as f:
            counts = json.load(f)
    else:
        counts = {
            "jac": 0,
            "iac": 0,
            "journal": 0,
            "funder_config": 0,
            "funder_language": 0,
            "agreement": 0,
        }
    return counts


def get_records(index, t, from_count):
    result = {}
    CONN = esprit.raw.Connection(settings.ES_HOST, index)
    q = {"query": {"match_all": {}}, "size": 1, "from": from_count}
    resp = esprit.raw.search(connection=CONN, type=t, query=q)
    data = resp.json()
    result['count'] = data["hits"]["total"]
    rec = data.get('hits', {}).get('hits', [])[0].get("_source")
    result['id'] = rec.get('id')
    result['created'] =  rec.get('created_date', None)
    return result


def do_check(result, old_count):
    # New check - check record is in the last 3 hours
    new = True
    if result['created']:
        dt_obj = datetime.strptime(result['created'], '%Y-%m-%d %H%M.%S')
        delta = datetime.utcnow() - dt_obj
        if delta.total_seconds() / 3600 > 3:
            new = False
    result['new_check'] = new
    # count check - check number of records is more than 90% of previous number
    count_check = False
    if result['count'] > old_count*0.9:
        count_check = True
    result['count_check'] = count_check
    result['outcome'] = result['new_check'] and result['count_check']


def check_index(index, t, old_count):
    # For the index with type,
    # Check first and last record for newness and number of records
    res1 = get_records(index, t, 0)
    do_check(res1, old_count)
    res2 = {}
    if res1['outcome']:
        res2 =  get_records(index, t, res1['count']-1)
        do_check(res2, old_count)
        if res2['outcome']:
            return True, res1, res2
    return False, res1, res2


def check_indices():
    print("{x}: Checking all indices for date of records and count".format(x=datetime.utcnow()))
    index_suffix = settings.ES_INDEX_SUFFIX
    if index_suffix and not index_suffix.startswith('_'):
        index_suffix = "_" + index_suffix

    types = {
        "jac":             ("jct_jac{0}".format(index_suffix), ''),
        "iac":             ("jct_iac{0}".format(index_suffix), ''),
        "journal":         ("jct{0}".format(index_suffix), 'journal'),
        "funder_config":   ("jct_funder_config{0}".format(index_suffix), ''),
        "funder_language": ("jct_funder_language{0}".format(index_suffix), ''),
        "agreement":       ("jct{0}".format(index_suffix), 'agreement')
    }

    old_counts = get_old_counts()
    new_counts = {}
    messages = []
    details = []
    status = 'passed'
    for typ in types:
        ans = check_index(types[typ][0], types[typ][1], old_counts.get(typ, 0))
        if ans[0]:
            messages.append("{x}: Index {y} passed.".format(x=datetime.utcnow(), y=typ))
        else:
            status = 'failed'
            messages.append("{x}: Index {y} failed".format(x=datetime.utcnow(), y=typ))
        details.append({
            'index': typ,
            'outcome': ans[0],
            'record1': ans[1],
            'record2': ans[2]})
        new_counts[typ] = ans[1].get('count', 0)

    counts_file = os.path.join(settings.DATABASES, 'counts.json')
    with open(counts_file, 'w') as f:
        json.dump(new_counts, f, indent=4)

    outcome_file = os.path.join(settings.DATABASES, 'outcome.json')
    with open(outcome_file, 'w') as f:
        json.dump(details, f, indent=4)

    subject = "Importer check : {a}".format(a=status)
    send_mail(subject, json.dumps(messages, indent=4), outcome_file)


def run_jct_tests():
    print("{x}: Starting JCT api test run".format(x=datetime.utcnow()))
    messages = []
    status = ''
    messages.append("{x}: Starting JCT tests.".format(x=datetime.utcnow()))
    request = requests.get(settings.JCT_TEST_URL, timeout=settings.JCT_TEST_TIMEOUT)
    if request.status_code == 200:
        messages.append("{x}: JCT tests completed.".format(x=datetime.utcnow()))
        response_data = request.json()
        outcome_file = os.path.join(settings.DATABASES, 'test_outcome.json')
        with open(outcome_file, 'w') as f:
            json.dump(response_data, f, indent=4)
        status = 'completed'
    else:
        messages.append("{x}: ERROR completing JCT tests.".format(x=datetime.utcnow()))
        status = 'ERROR'
    subject = "JCT tests after import : {a}".format(a=status)
    send_mail(subject, json.dumps(messages, indent=4), outcome_file)
    return


if __name__ == "__main__":
    check_indices()
    run_jct_tests()

