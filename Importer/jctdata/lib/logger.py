from datetime import datetime


def log(message, source=None):
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    if source is None:
        source = ""
    else:
        source += ":"

    print("[" + timestamp + "] " + source + " " + message)