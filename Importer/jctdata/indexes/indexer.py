import os, shutil

from jctdata import settings

class Indexer(object):
    ID = "override"
    SOURCES = []

    def __init__(self):
        self.dir = settings.INDEX_PATH[self.ID]
        self.keep_historic = settings.INDEX_HISTORY.get(self.ID, 5)

    def current_dir(self):
        dirs = []
        for entry in os.listdir(self.dir):
            if os.path.isdir(os.path.join(self.dir, entry)):
                dirs.append(entry)

        if len(dirs) == 0:
            return None

        dirs.sort(reverse=True)
        return dirs[0]

    def gather(self):
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
            print("INDEXER: cleaning up old directory {x}".format(x=removing))
            shutil.rmtree(removing)