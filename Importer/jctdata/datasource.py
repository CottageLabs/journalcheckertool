import os, shutil
from datetime import datetime, timedelta
from jctdata import settings

class Datasource:
    ID = None

    def __init__(self):
        self.max_age = settings.MAX_DATASOURCE_AGE[self.ID]
        self.dir = settings.DATASOURCE_PATH[self.ID]
        self.keep_historic = settings.DATASOURCE_HISTORY.get(self.ID, 3)

    def requires_update(self):
        dirs = []
        os.makedirs(self.dir, exist_ok=True)
        for entry in os.listdir(self.dir):
            if os.path.isdir(os.path.join(self.dir, entry)):
                dirs.append(entry)

        if len(dirs) == 0:
            return True

        dirs.sort(reverse=True)
        created = datetime.strptime(dirs[0], settings.DIR_DATE_FORMAT)
        return created + timedelta(seconds=self.max_age) < datetime.utcnow()

    def current_dir(self):
        dirs = []
        for entry in os.listdir(self.dir):
            if os.path.isdir(os.path.join(self.dir, entry)):
                dirs.append(entry)

        if len(dirs) == 0:
            return None

        dirs.sort(reverse=True)
        return dirs[0]

    def current_paths(self):
        raise NotImplementedError()

    def gather(self):
        raise NotImplementedError()

    def analyse(self):
        raise NotImplementedError()

    def cleanup(self):
        dirs = []
        for entry in os.listdir(self.dir):
            if os.path.isdir(os.path.join(self.dir, entry)):
                dirs.append(entry)

        if len(dirs) <= self.keep_historic:
            return

        dirs.sort(reverse=True)
        for remove in dirs[self.keep_historic:]:
            removing = os.path.join(self.dir, remove)
            shutil.rmtree(removing)

    def paths_exists(self):
        exists = True
        try:
            paths = self.current_paths()
        except:
            paths = {}
            exists = False
        for k, filepath in paths.items():
            if not os.path.exists(filepath):
                exists = False
        return exists