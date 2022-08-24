import os, shutil

from jctdata import datasource
from datetime import datetime
from jctdata import settings


class FunderDB(datasource.Datasource):
    ID = "funderdb"

    def current_paths(self):
        dir = self.current_dir()
        origindir = os.path.join(self.dir, dir, "origin")
        return {
            "origin" : origindir,
        }

    def gather(self):
        print("FUNDERDB: gathering funderdb from {x}".format(x=settings.FUNDER_DB_DIR))

        dir = datetime.strftime(datetime.utcnow(), settings.DIR_DATE_FORMAT)
        outdir = os.path.join(self.dir, dir, "origin")
        os.makedirs(outdir)

        default_in = os.path.join(settings.FUNDER_DB_DIR, "default")
        funders_in = os.path.join(settings.FUNDER_DB_DIR, "funders")

        default_out = os.path.join(outdir, "default")
        funders_out = os.path.join(outdir, "funders")

        shutil.copytree(default_in, default_out)
        shutil.copytree(funders_in, funders_out)

        print("FUNDERDB: funderdb copied to {x}".format(x=outdir))

    def analyse(self):
        print("FUNDERDB: no analyis required")