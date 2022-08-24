from jctdata.indexes.jac import JAC
from jctdata.indexes.iac import IAC

INDEXERS = {
    JAC.ID: JAC,
    IAC.ID: IAC
}


def get_indexer(name):
    return INDEXERS.get(name)()


def get_all_indexers():
    return [v() for v in INDEXERS.values()]


def get_all_index_names():
    return INDEXERS.keys()