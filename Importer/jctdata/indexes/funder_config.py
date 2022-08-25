import os, yaml, json

from jctdata.indexes.indexer import Indexer
from jctdata import resolver
from jctdata import settings

from datetime import datetime
from copy import deepcopy


class FunderConfig(Indexer):
    ID = "funder_config"
    SOURCES = ["funderdb"]

    def gather(self):
        print('FUNDER_CONFIG: Gathering data for funder config from sources: {x}'.format(
            x=",".join(self.SOURCES)))
        paths = resolver.gather_data(self.SOURCES, True)
        print("FUNDER_CONFIG: funderdb source: " + paths.get("funderdb", {}).get("origin", "no funderdb source"))

    def analyse(self):
        print("FUNDER_CONFIG: Preparing funder configuration")

        dir = datetime.strftime(datetime.utcnow(), settings.DIR_DATE_FORMAT)
        fcdir = os.path.join(self.dir, dir)
        analyse_dir = os.path.join(fcdir, "analyse")
        os.makedirs(analyse_dir, exist_ok=True)

        funderdb_paths = resolver.SOURCES[self.SOURCES[0]].current_paths()
        funderdb_dir = funderdb_paths.get("origin")
        default_cfg_path = os.path.join(funderdb_dir, "default", "config.yml")

        with open(default_cfg_path) as y:
            default_cfg = yaml.load(y.read(), Loader=yaml.BaseLoader)

        funders_dir = os.path.join(funderdb_dir, "funders")
        for funder in os.listdir(funders_dir):
            funder_cfg = os.path.join(funders_dir, funder, "config.yml")
            with open(funder_cfg) as y:
                funder_cfg = yaml.load(y.read(), Loader=yaml.BaseLoader)
            funder_cfg = self._merge(default_cfg, funder_cfg)
            with open(os.path.join(analyse_dir, funder + ".json"), "w") as o:
                o.write(json.dumps(funder_cfg, indent=2))

        print("FUNDER_CONFIG: Funder configurations built")

    def assemble(self):
        print("FUNDER_CONFIG: Assembling funder configuration index")

        fcdir = os.path.join(self.dir, self.current_dir())
        outfile = os.path.join(fcdir, "funder_config.json")
        analyse_dir = os.path.join(fcdir, "analyse")

        with open(outfile, "w") as o:
            for config_file in os.listdir(analyse_dir):
                cfgfile_path = os.path.join(analyse_dir, config_file)
                with open(cfgfile_path, "r") as f:
                    data = json.loads(f.read())
                o.write(json.dumps(data) + "\n")

        print("FUNDER_CONFIG: Funder config index data prepared")

        self._cleanup()

    def _merge(self, default, funder):
        result = deepcopy(default)
        for k, v in funder.items():
            if isinstance(v, dict):
                if k in default:
                    result[k] = self._merge(default[k], funder[k])
                else:
                    result[k] = funder[k]
            else:
                result[k] = funder[k]
        return result
