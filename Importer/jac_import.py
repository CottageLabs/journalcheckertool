from jctdata.jct import gather_index_data
from jctdata.index import index_latest_with_alias
from jctdata import settings

gather_index_data()
index_latest_with_alias('jac', settings.ES_INDEX_SUFFIX)
