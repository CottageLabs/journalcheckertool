from jctdata.datasources import crossref
from jctdata.datasources import doaj
from jctdata.datasources import tj

SOURCES = {
    "crossref" : crossref.Crossref(),
    "doaj" : doaj.DOAJ(),
    "tj" : tj.TJ()
}


def gather_data(datasources, reanalyse=False):
    pathset = {}
    for source in datasources:
        handler = SOURCES[source]
        ru = handler.requires_update()
        if ru:
            handler.gather()
        if ru or reanalyse:
            handler.analyse()
        pathset[source] = handler.current_paths()
    return pathset


if __name__ == "__main__":
    gather_data(["doaj"], True)