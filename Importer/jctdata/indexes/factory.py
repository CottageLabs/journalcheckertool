from jctdata.indexes.jac import JAC
from jctdata.indexes.iac import IAC
from jctdata.indexes.funder_language import FunderLanguage
from jctdata.indexes.funder_config import FunderConfig
from jctdata.indexes.journal import Journal

INDEXERS = {
    JAC.ID: JAC,
    IAC.ID: IAC,
    FunderLanguage.ID: FunderLanguage,
    FunderConfig.ID: FunderConfig,
    Journal.ID: Journal
}


def get_indexer(name):
    return INDEXERS.get(name)()


def get_all_indexers():
    return [v() for v in INDEXERS.values()]


def get_all_index_names():
    return list(INDEXERS.keys())