from datetime import datetime
import requests
import json
from jctdata.jct import gather_index_data
from jctdata.index import index_latest_with_alias
from jctdata import settings
from lib.send_mail import send_mail


messages = []
messages.append("{x}: Starting importer run.".format(x=datetime.utcnow()))

# Gather data for autocomplete index
gather_index_data()
messages.append("{x}: Gathered autocomplete data.".format(x=datetime.utcnow()))

# Index journal autocomplete data
index_latest_with_alias('jac', settings.ES_INDEX_SUFFIX)
messages.append("{x}: Indexed journal autocomplete data.".format(x=datetime.utcnow()))

# Index institution autocomplete data
index_latest_with_alias('iac', settings.ES_INDEX_SUFFIX)
messages.append("{x}: Indexed institution autocomplete data.".format(x=datetime.utcnow()))

subject = "First autocomplete importer run"
send_mail(subject, json.dumps(messages, indent=4), None)

