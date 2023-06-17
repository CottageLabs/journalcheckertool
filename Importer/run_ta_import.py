from datetime import datetime
import requests
import json
from jctdata import settings
from jctdata.lib.send_mail import send_mail


messages = []
messages.append("{x}: Starting TA importer run.".format(x=datetime.utcnow()))

# Start jct TA import
request = requests.get(settings.JCT_TA_IMPORT_URL)
if request.status_code == 200:
    messages.append("{x}: Started JCT TA import.".format(x=datetime.utcnow()))
    status = 'started'
else:
    messages.append("{x}: ERROR starting JCT TA import.".format(x=datetime.utcnow()))
    status = 'ERROR starting'

messages.append("{x}: Finished TA importer run.".format(x=datetime.utcnow()))

subject = "TA Importer run : {a}".format(a=status)
send_mail(subject, json.dumps(messages, indent=4), None)

