from jct.dao import DAO
from jct.core import app

class Institution:
    def __init__(self, compliance=None, info=None):
        self._compliance = compliance if compliance is not None else {}
        self._info = info if info is not None else {}

    @property
    def ror(self):
        return self._compliance.get("ror")

    @property
    def name(self):
        return self._info.get("name")

    def to_info_dict(self):
        return {
            "id": self.ror,
            "title": self.name
        }


class InstitutionDAO(DAO):
    @classmethod
    def get(cls, ror):
        """
        Get the institution information for the given ROR
        :param ror: the ROR of the institution
        :return: an Insititution object
        """
        compliance_source = InstitutionComplianceDAO.get(ror)
        info_source = InstitutionInfoDAO.get(ror)
        return Institution(compliance=compliance_source, info=info_source)

    @classmethod
    def save(self, obj):
        raise NotImplementedError()

class InstitutionComplianceDAO(DAO):
    TYPE = "institution"

    @classmethod
    def get(cls, ror):
        """
        Get the institution information for the given ROR
        :param ror: the ROR of the institution
        :return: an Insititution object
        """
        return cls.pull_by_key("ror", ror)


class InstitutionInfoDAO(DAO):
    TYPE = "iac"

    @classmethod
    def get(cls, ror):
        """
        Get the institution information for the given ROR
        :param ror: the ROR of the institution
        :return: an Insititution object
        """
        return cls.pull_by_key("ror", ror)
