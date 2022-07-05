from jctdata.indexes.jac import JAC

INDEXERS = {
    "jac": JAC
}

def get_indexer(name):
    return INDEXERS.get(name)()