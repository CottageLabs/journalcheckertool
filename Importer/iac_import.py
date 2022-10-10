from jctdata.iac import iac_index_data
from jctdata.index import index_latest_with_alias
from jctdata import settings

iac_index_data()
index_latest_with_alias('iac', settings.ES_INDEX_SUFFIX)
