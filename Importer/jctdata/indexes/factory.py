from jctdata.indexes.jac import JAC
from jctdata.indexes.iac import IAC
from jctdata.indexes.funder_language import FunderLanguage
from jctdata.indexes.funder_config import FunderConfig
from jctdata.indexes.journal import Journal
from jctdata.indexes.jcs import JCS_CSV
from jctdata.indexes.ta import TA
from jctdata.indexes.institution import Institution
from jctdata.indexes.bad_ta_issns import BadTAIssns

INDEXERS = {
    JAC.ID: JAC,
    IAC.ID: IAC,
    FunderLanguage.ID: FunderLanguage,
    FunderConfig.ID: FunderConfig,
    Journal.ID: Journal,
    JCS_CSV.ID: JCS_CSV,
    TA.ID: TA,
    Institution.ID: Institution,
    BadTAIssns.ID: BadTAIssns
}


def get_indexer(name):
    return INDEXERS.get(name)()


def get_all_indexers():
    return [v() for v in INDEXERS.values()]


def get_all_index_names():
    return list(INDEXERS.keys())