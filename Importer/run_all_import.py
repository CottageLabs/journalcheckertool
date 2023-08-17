from datetime import datetime
import requests
import json
from jctdata import settings
from jctdata.lib.send_mail import send_mail
from jctdata import cli


messages = []
messages.append("{x}: Starting importer run.".format(x=datetime.utcnow()))

cli.run("load", ("_all",))
messages.append("{x}: Ran all local importer processes".format(x=datetime.utcnow()))

# Start jct import
print('Starting JCT remote import')
request = requests.get(settings.JCT_IMPORT_URL)
if request.status_code == 200:
    messages.append("{x}: Started JCT import.".format(x=datetime.utcnow()))
    status = 'started'
else:
    messages.append("{x}: ERROR starting JCT import.".format(x=datetime.utcnow()))
    status = 'ERROR starting'

messages.append("{x}: Finished importer run.".format(x=datetime.utcnow()))

subject = "Importer run : {a}".format(a=status)
send_mail(subject, json.dumps(messages, indent=4), None)

