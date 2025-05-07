from jct.lib import dates
from jct.models import Journal, Funder, Institution
from jct.dao import DAO

import json

class Compliance:
    def __init__(self):
        self._data = {
            "request": {
                "started": int(dates.now().timestamp()),
                "ended": None,
                "took": None,
                "journal": [],
                "funder": [],
                "institution": [],
                "checks": []
            },
            "results": [],
            "cards": []
        }

    @property
    def journal(self):
        return self._data["request"]["journal"]

    @journal.setter
    def journal(self, journal: Journal):
        if journal:
            self._data["request"]["journal"] = [journal]

    @property
    def funder(self):
        return self._data["request"]["funder"]

    @funder.setter
    def funder(self, funder: Funder):
        if funder:
            self._data["request"]["funder"] = [funder]

    @property
    def institution(self):
        return self._data["request"]["institution"]

    @institution.setter
    def institution(self, institution: Institution):
        if institution:
            self._data["request"]["institution"] = [institution]

    def add_check(self, check):
        self._data["results"].append(check)

    def end_check(self):
        self._data["request"]["ended"] = int(dates.now().timestamp())
        self._data["request"]["took"] = self._data["request"]["ended"] - self._data["request"]["started"]

    def to_result_dict(self):
        d = {
            "request": {
                "started": self._data["request"]["started"],
                "ended": self._data["request"]["ended"],
                "took": self._data["request"]["took"],
                "journal": [j.to_info_dict() for j in self.journal],
                "funder": [f.to_info_dict() for f in self.funder],
                "institution": [i.to_info_dict() for i in self.institution],
                "checks": list(set([c.route for c in self._data["results"]]))
            },
            "results": [c.to_result_dict() for c in self._data["results"]],
            "cards": self._data["cards"]
        }
        return d

    def to_json(self):
        d = self.to_result_dict()
        return json.dumps(d)

class Check:
    def __init__(self, route, issn=None, funder=None, ror=None):
        self._data = {
            "route": route,
            "compliant": False,
            "unknown": False,
            "qualifications": None,
            "log": []
        }

        if issn is not None:
            self._data["issn"] = [issn]

        if funder is not None:
            self._data["funder"] = funder

        if ror is not None:
            self._data["ror"] = ror

    def log(self, code, parameters=None):
        entry = {"code": code}
        if parameters is not None:
            entry["paramaters"] = parameters
        self._data["log"].append(entry)

    @property
    def logs(self):
        return self._data.get("log", [])

    @property
    def route(self):
        return self._data["route"]

    @property
    def qualifications(self):
        return self._data.get("qualifications", [])

    @qualifications.setter
    def qualifications(self, quals):
        self._data["qualifications"] = quals

    @property
    def unknown(self):
        return self._data["unknown"]

    @unknown.setter
    def unknown(self, val):
        self._data["unknown"] = val

    @property
    def compliant(self):
        return self._data["compliant"]

    @compliant.setter
    def compliant(self, val):
        self._data["compliant"] = val

    def to_result_dict(self):
        d = {
            "route": self.route,
            "compliant": "yes" if self.compliant else "no" if not self.unknown else "unknown",
            "log": self.logs,
            "qualifications": self.qualifications
        }

        if "issn" in self._data:
            d["issn"] = self._data["issn"]
        if "funder" in self._data:
            d["ror"] = self._data["funder"].id
        if "institution" in self._data:
            d["ror"] = self._data["institution"].ror

        return d


class ComplianceDAO(DAO):
    TYPE = "compliance"

    @classmethod
    def save(cls, compliance):
        pass