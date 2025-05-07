from jct.dao import DAO

class Unknown:
    def __init__(self, journal, funder, institution, result):
        self._journal = journal
        self._funder = funder
        self._institution = institution
        self._result = result


class UnknownDAO(DAO):
    @classmethod
    def save(cls, unknown: Unknown):
        pass