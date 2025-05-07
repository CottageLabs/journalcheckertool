from jct.dao import DAO
from jct.core import app

class Journal:
    def __init__(self, compliance=None, info=None, requested_issn=None):
        self._compliance = compliance if compliance is not None else {}
        self._info = info if info is not None else {}
        self._requested_issn = requested_issn

    @property
    def requested_issn(self):
        return self._requested_issn

    @requested_issn.setter
    def requested_issn(self, issn):
        self._requested_issn = issn

    @property
    def oa_exception(self):
        return self._compliance.get("oa_exception", False)

    @property
    def oa_exception_caveat(self):
        return self._compliance.get("oa_exception_caveat")

    @property
    def oa_exception_funder_caveats(self):
        return self._compliance.get("oa_exception_funder_caveats", [])

    def get_oa_exception_caveat(self, funder):
        caveat = self.oa_exception_caveat
        if funder is not None and len(self.oa_exception_funder_caveats) > 0:
            for cav in self.oa_exception_funder_caveats:
                if cav["funder"] == funder.id:
                    caveat = cav.caveat
                    break
        return caveat

    @property
    def in_doaj(self):
        return self._compliance.get("indoaj", False)

    @property
    def in_progress_doaj(self):
        return self._compliance.get("doajinprogress", False)

    @property
    def has_doaj_licences(self):
        return len(self._compliance.get("doaj", {}).get("bibjson", {}).get("license", [])) > 0

    def doaj_licence_matches(self, allowed):
        present = []
        licences = [self._normalise_licence(l.get("type")) for l in self._compliance.get("doaj", {}).get("bibjson", {}).get("license", [])]
        for a in allowed:
            na = self._normalise_licence(a)
            if na in licences:
                present.append(a)
        return present

    def to_info_dict(self):
        return {
            "id": self._requested_issn,
            "issn": self._compliance.get("issn"),
            "publisher": self._info.get("publisher"),
            "title": self._info.get("title")
        }

    def _normalise_licence(self, l):
        l = l.lower().strip()
        l = l.replace(" ", "")
        l = l.replace("-", "")
        return l

class JournalDAO(DAO):

    @classmethod
    def get(cls, issn):
        """
        Get the journal information for the given ISSN
        :param issn: the ISSN of the Journal
        :return: a Journal object
        """
        compliance_source = JournalComplianceDAO.get(issn)
        info_source = JournalInfoDAO.get(issn)
        return Journal(compliance=compliance_source, info=info_source, requested_issn=issn)

class JournalComplianceDAO(DAO):
    TYPE = "journal"

    @classmethod
    def get(cls, issn):
        """
        Get the journal compliance information for the given ISSN
        :param issn: the ISSN of the Journal
        :return: a Journal object
        """
        compliance_source = cls.pull_by_key("issn", issn)
        return compliance_source

class JournalInfoDAO(DAO):
    TYPE = "jac"

    @classmethod
    def get(cls, issn):
        """
        Get the journal information for the given ISSN
        :param issn: the ISSN of the Journal
        :return: a Journal object
        """
        info_sources = cls.find_by_key("issn", issn)
        info_source = None
        if len(info_sources) > 0:
            info_source = info_sources[0]
        return info_source
