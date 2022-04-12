import os
from datetime import datetime, timedelta
from jctdata import settings

class Datasource:
    ID = None

    def __init__(self):
        self.max_age = settings.MAX_DATASOURCE_AGE[self.ID]
        self.dir = settings.DATASOURCE_PATH[self.ID]

    def requires_update(self):
        dirs = []
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
