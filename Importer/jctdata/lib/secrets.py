import os


def get_secret(file_path):
    if not os.path.exists(file_path):
        raise Exception("Secrets file {x} does not exist".format(x=file_path))

    with open(file_path) as f:
        contents = f.read().strip()

    if not contents:
        raise Exception("Secrets file {x} was empty".format(x=file_path))
    return contents