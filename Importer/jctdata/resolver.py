import json

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
            print("RESOLVER: {x} requires update".format(x=source))
            handler.gather()
        else:
            print("RESOLVER: {x} does not require update".format(x=source))

        if ru or reanalyse:
            print("RESOLVER: analysing {x}".format(x=source))
            handler.analyse()

        pathset[source] = handler.current_paths()
        print("RESOLVER : {y} analysed files: {x}".format(y=source, x=json.dumps(pathset[source])))

    return pathset


if __name__ == "__main__":
    gather_data(["doaj"], True)