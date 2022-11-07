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


class TJTests(object):
    ID = "tj"

    STEPS = {
        "no_tj": {
            "log": "TJ.NoTJ",
            "filter": no_tj
        },
        "exists": {"log": "TJ.Exists"},
        "funder_non_compliant": {"log": "TJ.FunderNonCompliant"},
        "compliant": {"log": "TJ.Compliant"}
    }

    PATHS = {
        "no_tj": {"steps" : ["no_tj"]},
        # "funder_non_compliant": {"steps" : ["exists", "funder_non_compliant"]},
        # "compliant": {"steps": ["exists", "compliant"]}
    }

    def __init__(self):
        dirname = datetime.strftime(datetime.utcnow(), settings.DIR_DATE_FORMAT)
        self.dir = os.path.join(settings.TEST_PATH[self.ID], dirname)
        os.makedirs(self.dir, exist_ok=True)

    def generate(self):
        for p, c in self.PATHS.items():
            inputset = self._initial_input_set()
            for s in c.get("steps", []):
                fn = self.STEPS[s]["filter"]
                inputset = fn(inputset)

                stepfile = os.path.join(self.dir, "step_" + s + ".csv")
                with open(stepfile, "w") as f:
                    writer = csv.writer(f)
                    writer.writerows(inputset)

            pathfile = os.path.join(self.dir, "path_" + p + ".csv")
            with open(pathfile, "w") as f:
                writer = csv.writer(f)
                writer.writerows(inputset)

    def _initial_input_set(self):
        return [["", "", ""]]


if __name__ == "__main__":
    tests = TJTests()
    tests.generate()