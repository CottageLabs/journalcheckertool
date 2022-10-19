import json

from jctdata.datasources import crossref
from jctdata.datasources import doaj
from jctdata.datasources import doaj_inprogress
from jctdata.datasources import tj
from jctdata.datasources import ta
from jctdata.datasources import ror
from jctdata.datasources import sa_negative
from jctdata.datasources import sa_positive
from jctdata.datasources import funderdb
from jctdata.datasources import oa_exceptions
from jctdata.datasources import jcs

from jctdata.lib import logger


SOURCES = {
    "crossref" : crossref.Crossref(),
    "doaj" : doaj.DOAJ(),
    "doaj_inprogress" : doaj_inprogress.DOAJInProgress(),
    "tj" : tj.TJ(),
    "ta" : ta.TA(),
    "ror": ror.ROR(),
    "sa_negative" : sa_negative.SANegative(),
    "sa_positive" : sa_positive.SAPositive(),
    "funderdb": funderdb.FunderDB(),
    "oa_exceptions": oa_exceptions.OAExceptions(),
    "jcs": jcs.JCS()
}

LOG_ID = "RESOLVER"


def gather_data(datasources, reanalyse=False):
    pathset = {}
    for source in datasources:
        handler = SOURCES[source]
        ru = handler.requires_update()

        if ru or not handler.paths_exists():
            logger.log("{x} requires update".format(x=source), LOG_ID)
            handler.gather()
        else:
            logger.log("{x} does not require update".format(x=source), LOG_ID)

        if ru or reanalyse:
            logger.log("analysing {x}".format(x=source), LOG_ID)
            handler.analyse()

        pathset[source] = handler.current_paths()
        logger.log("{y} analysed files: {x}".format(y=source, x=json.dumps(pathset[source])), LOG_ID)

        handler.cleanup()

    return pathset
