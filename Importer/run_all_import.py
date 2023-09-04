from datetime import datetime
import json
from jctdata.lib.send_mail import send_mail
from jctdata import cli


messages = []
messages.append("{x}: Starting importer run.".format(x=datetime.utcnow()))

cli.run("load", ("_all",))
messages.append("{x}: Ran all local importer processes".format(x=datetime.utcnow()))
messages.append("{x}: Finished importer run.".format(x=datetime.utcnow()))

subject = "Importer run"
send_mail(subject, json.dumps(messages, indent=4), None)
