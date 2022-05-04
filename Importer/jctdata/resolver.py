import json

from jctdata.datasources import crossref
from jctdata.datasources import doaj
from jctdata.datasources import doaj_inprogress
from jctdata.datasources import tj
from jctdata.datasources import ta
from jctdata.datasources import ror
from jctdata.datasources import sa_negative

SOURCES = {
    "crossref" : crossref.Crossref(),
    "doaj" : doaj.DOAJ(),
    "doaj_inprogress" : doaj_inprogress.DOAJInProgress(),
    "tj" : tj.TJ(),
    "ta" : ta.TA(),
    "ror": ror.ROR(),
    "sa_negative" : sa_negative.SANegative()
}


def gather_data(datasources, reanalyse=False):
    pathset = {}
    for source in datasources:
        handler = SOURCES[source]
        ru = handler.requires_update()

        if ru or not handler.paths_exists():
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
    gather_data(["sa_negative"], True)