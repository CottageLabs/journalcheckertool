import os, shutil

from jctdata import settings
from jctdata.lib import logger

class Indexer(object):
    ID = "indexer"
    SOURCES = []

    def __init__(self):
        self.dir = settings.INDEX_PATH[self.ID]
        self.keep_historic = settings.INDEX_HISTORY.get(self.ID, 5)

    def log(self, msg):
        logger.log(msg, self.ID.upper())

    def current_dir(self):
        dirs = []
        for entry in os.listdir(self.dir):
            if os.path.isdir(os.path.join(self.dir, entry)):
                dirs.append(entry)

        if len(dirs) == 0:
            return None

        dirs.sort(reverse=True)
        return dirs[0]

    def gather(self, force=False):
        raise NotImplementedError()

    def analyse(self):
        raise NotImplementedError()

    def assemble(self):
        raise NotImplementedError()

    def _cleanup(self):
        dir = self.dir
        dirs = []
        for entry in os.listdir(dir):
            if os.path.isdir(os.path.join(dir, entry)):
                dirs.append(entry)

        if len(dirs) <= self.keep_historic:
            return

        dirs.sort(reverse=True)
        for remove in dirs[self.keep_historic:]:
            removing = os.path.join(dir, remove)
            self.log("cleaning up old directory {x}".format(x=removing))
            shutil.rmtree(removing)