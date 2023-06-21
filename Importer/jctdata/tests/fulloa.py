from jctdata import settings
from jctdata.indexes.journal import Journal
import os, csv, json
from datetime import datetime

JOURNAL = Journal()
if JOURNAL.current_dir() is None:
    JOURNAL.gather()
    JOURNAL.analyse()
    JOURNAL.assemble()

JOURNAL_DATA = {}
JOURNALS_FILE = os.path.join(JOURNAL.dir, JOURNAL.current_dir(), JOURNAL.ID + ".json")
with open(JOURNALS_FILE, "r") as f:
    for data in f:
        record = json.loads(data)
        for issn in record.get("issn", []):
            JOURNAL_DATA[issn] = record


def decision_exception_noexception(data):
    if data.get("oa_exception") is True:
        return "FullOA.Exception", "*", "*"
    else:
        return "FullOA.NoException", "*", "*"


def decision_indoaj_notindoaj(data):
    if data.get("indoaj") is True:
        return "FullOA.InDOAJ", "*", "*"
    else:
        return "FullOA.NotInDOAJ", "*", "*"


def decision_inprogress_notinprogress(data):
    if data.get("doajinprogress") is True:
        return "FullOA.InProgressDOAJ", "*", "*"
    else:
        return "FullOA.NotInProgressDOAJ", "*", "*"


def decision_properties_meet_requirements(data):
    # FIXME: according to the algorithm this should check the publishing_licence, but the live
    # algorithm does not do that, so not doing it here either
    if data.get("doajinprogress") is True and not data.get("indoaj"):
        return "FullOA.Compliant", "*", "*"

    licences = [l.get("type").lower().replace("-", "").replace(" ", "") for l in data.get("doaj", {}).get("bibjson", {}).get("license", []) if "type" in l]
    if len(licences) == 0:
        return "FullOA.Unknown", "*", "*"

    if "ccby" in licences or "cc0" in licences or "ccbysa" in licences:
        return "FullOA.Compliant", "*", "*"

    return "FullOA.NonCompliant", "*", "*"


def generate():
    tests = []
    for n, cfg in PATHS.items():
        gen = generator(cfg.get("edges", []), ALGORITHM)
        print("generating for {x}, path {y}".format(x=n, y=cfg.get("edges", [])))
        try:
            for i in range(2):
                issn, funder, inst = next(gen)
                newtest = [n, issn, funder, inst, cfg.get("edges", [])]
                tests.append(newtest)
                print(newtest)
        except StopIteration:
            pass

    with open("/home/richard/tmp/jct/fulloatest.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(tests)


ALGORITHM = {
    "START": {
        "fn": decision_exception_noexception,
        "edges": {
            "FullOA.Exception": False,
            "FullOA.NoException": "in_doaj"
        }
    },
    "in_doaj": {
        "fn": decision_indoaj_notindoaj,
        "edges": {
            "FullOA.InDOAJ": "funder_requirements",
            "FullOA.NotInDOAJ": "in_progress"
        }
    },
    "in_progress": {
        "fn": decision_inprogress_notinprogress,
        "edges": {
            "FullOA.InProgressDOAJ": "funder_requirements",
            "fULLoa.NotInProgressDOAJ": False
        }
    },
    "funder_requirements": {
        "fn": decision_properties_meet_requirements,
        "edges": {
            "FullOA.Compliant": False,
            "FullOA.Unknown": False,
            "FullOA.NonCompliant": False
        }
    }
}


def generator(path, algorithm):
    for issn, data in JOURNAL_DATA.items():
        log = []

        onward = "START"
        while onward:
            node = algorithm.get(onward)

            edge, funder, inst = node["fn"](data)
            log.append(edge)
            onward = node.get("edges", {}).get(edge, False)

            pm = _path_match(path, log)
            if pm == 1:
                # print("yield {x}".format(x=[issn, funder, inst]))
                yield issn, funder, inst
            elif pm == -1:
                break

    return


def _path_match(path, log):
    for i in range(len(path)):
        if len(log) <= i:
            return 0

        if path[i] != log[i]:
            return -1

    return 1


PATHS = {
    "oa_exception": {"edges" : ["FullOA.Exception"]},
    "in_doaj_compliant": {"edges" : ["FullOA.NoException", "FullOA.InDOAJ", "FullOA.Compliant"]},
    "in_doaj_unknown": {"edges": ["FullOA.NoException", "FullOA.InDOAJ", "FullOA.Unknown"]},
    "in_doaj_noncompliant": {"edges": ["FullOA.NoException", "FullOA.InDOAJ", "FullOA.NonCompliant"]},
    "in_progress_compliant": {"edges" : ["FullOA.NoException", "FullOA.NotInDOAJ", "FullOA.InProgressDOAJ", "FullOA.Compliant"]},
    "in_progress_unknown": {"edges" : ["FullOA.NoException", "FullOA.NotInDOAJ", "FullOA.InProgressDOAJ", "FullOA.Unknown"]},
    "in_progress_noncompliant": {"edges" : ["FullOA.NoException", "FullOA.NotInDOAJ", "FullOA.InProgressDOAJ", "FullOA.NonCompliant"]},
    "not_in_doaj": {"edges": ["FullOA.NoException", "FullOA.NotInDOAJ", "FullOA.NotInProgressDOAJ"]}
}

if __name__ == "__main__":
    # tests = TJTests()
    # tests.generate()
    generate()