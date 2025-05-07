from jct.dao import DAO
from jct.core import app

class Funder:
    def __init__(self, raw=None):
        self._data = raw

    @property
    def id(self):
        return self._data.get("id")

    @property
    def name(self):
        return self._data.get("name")

    @property
    def active_routes(self):
        return [r for r in self._data.get("routes", []) if r.get("calculate", False)]

    def to_info_dict(self):
        return {
            "id": self.id,
            "title": self.name,
        }


class FunderDAO(DAO):
    TYPE = "funder_config"

    @classmethod
    def get(cls, funder_id):
        """
        Get the funder information for the given funder ID
        :param funder_id: the ID of the funder
        :return: a Funder object with the funder information
        """
        source = cls.pull(funder_id)
        return Funder(raw=source)

    @classmethod
    def save(self, obj):
        raise NotImplementedError()
