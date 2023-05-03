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


def no_tj(inputset):
    outputset = []
    for input in inputset:
        issns = _expand_issn_list(input[0])
        for issn in issns:
            if not JOURNAL_DATA.get(issn, {}).get("tj"):
                outputset.append([issn, input[1], input[2]])
    return outputset


def _expand_issn_list(seed):
    if seed != "":
        return [seed]
    return list(JOURNAL_DATA.keys())


def decision_exists_notj(data):
    if data.get("tj") is True:
        return "TJ.Exists", "*", "*"
    else:
        return "TJ.NoTJ", "*", "*"


def decision_compliant_noncompliant(data):
    if len(data.get("tj_excluded_by", [])) > 0:
        return "TJ.FunderNonCompliant", data.get("tj_excluded_by")[0], "*"
    return "TJ.Compliant", "*", "*"


# def generate():
#     paths = {
#         "no_tj": False,
#         "funder_non_compliant": False,
#         "compliant": False
#     }
#
#     tests = []
#     for issn, data in JOURNAL_DATA.items():
#
#         if paths["no_tj"] and paths["funder_non_compliant"] and paths["compliant"]:
#             break
#
#         log = []
#         edge, theissn, funder, inst = decision_exists_notj(data)
#         log.append(edge)
#         if edge == "TJ.NoTJ":
#             if paths["no_tj"] is False:
#                 tests.append([theissn, funder, inst, log])
#                 paths["no_tj"] = True
#             continue
#
#         edge, theissn, funder, inst = decision_compliant_noncompliant(data)
#         log.append(edge)
#         if edge == "TJ.FunderNonCompliant":
#             if paths["funder_non_compliant"] is False:
#                 tests.append([theissn, funder, inst, log])
#                 paths["funder_non_compliant"] = True
#         if edge == "TJ.Compliant":
#             if paths["compliant"] is False:
#                 tests.append([theissn, funder, inst, log])
#                 paths["compliant"] = True
#
#     with open("/home/richard/tmp/jct/tjtest.csv", "w") as f:
#         writer = csv.writer(f)
#         writer.writerows(tests)


def generate():
    tests = []
    for n, cfg in PATHS.items():
        gen = generator(cfg.get("edges", []))
        try:
            for i in range(1):
                issn, funder, inst = next(gen)
                tests.append([n, issn, funder, inst, cfg.get("edges", [])])
        except StopIteration:
            pass

    with open("/home/richard/tmp/jct/tjtest.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(tests)


def generator(path):
    for issn, data in JOURNAL_DATA.items():
        log = []

        edge, funder, inst = decision_exists_notj(data)
        log.append(edge)

        pm = _path_match(path, log)
        if pm == 1:
            yield issn, funder, inst
        elif pm == -1:
            continue

        if edge == "TJ.NoTJ":
            continue

        edge, funder, inst = decision_compliant_noncompliant(data)
        log.append(edge)

        pm = _path_match(path, log)
        if pm == 1:
            yield issn, funder, inst
        elif pm == -1:
            continue

        if edge == "TJ.FunderNonCompliant":
            continue
        if edge == "TJ.Compliant":
            continue
    return


def _path_match(path, log):
    for i in range(len(path)):
        if len(log) <= i:
            return 0

        if path[i] != log[i]:
            return -1

    return 1


PATHS = {
    "no_tj": {"edges" : ["TJ.NoTJ"]},
    "funder_non_compliant": {"edges" : ["TJ.Exists", "TJ.FunderNonCompliant"]},
    "compliant": {"edges": ["TJ.Exists", "TJ.Compliant"]}
}
# class TJTests(object):
#     ID = "tj"
#
#     STEPS = {
#         "no_tj": {
#             "log": "TJ.NoTJ",
#             "filter": no_tj
#         },
#         "exists": {"log": "TJ.Exists"},
#         "funder_non_compliant": {"log": "TJ.FunderNonCompliant"},
#         "compliant": {"log": "TJ.Compliant"}
#     }
#
#     PATHS = {
#         "no_tj": {"steps" : ["no_tj"]},
#         # "funder_non_compliant": {"steps" : ["exists", "funder_non_compliant"]},
#         # "compliant": {"steps": ["exists", "compliant"]}
#     }
#
#     def __init__(self):
#         dirname = datetime.strftime(datetime.utcnow(), settings.DIR_DATE_FORMAT)
#         self.dir = os.path.join(settings.TEST_PATH[self.ID], dirname)
#         os.makedirs(self.dir, exist_ok=True)
#
#     def generate(self):
#         for p, c in self.PATHS.items():
#             inputset = self._initial_input_set()
#             for s in c.get("steps", []):
#                 fn = self.STEPS[s]["filter"]
#                 inputset = fn(inputset)
#
#                 stepfile = os.path.join(self.dir, "step_" + s + ".csv")
#                 with open(stepfile, "w") as f:
#                     writer = csv.writer(f)
#                     writer.writerows(inputset)
#
#             pathfile = os.path.join(self.dir, "path_" + p + ".csv")
#             with open(pathfile, "w") as f:
#                 writer = csv.writer(f)
#                 writer.writerows(inputset)
#
#     def _initial_input_set(self):
#         return [["", "", ""]]


if __name__ == "__main__":
    # tests = TJTests()
    # tests.generate()
    generate()