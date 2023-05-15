import csv, json, os
from jctdata import resolver, settings
from jctdata.indexes.indexer import Indexer
from datetime import datetime



class TA(Indexer):
    ID = "ta"
    SOURCES = ["ta"]

    def gather(self):
        self.log('Gathering data for TA database from sources: {x}'.format(x=",".join(self.SOURCES)))
        paths = resolver.gather_data(self.SOURCES, True)

    def analyse(self):
        self.log("No analysis required")

    def assemble(self):
        self.log("Preparing TA data")

        dir = datetime.strftime(datetime.utcnow(), settings.DIR_DATE_FORMAT)
        tadir = os.path.join(self.dir, dir)
        os.makedirs(tadir, exist_ok=True)

        outfile = os.path.join(tadir, "ta.json")

        pathset = resolver.SOURCES["ta"].current_paths()
        taindex = pathset.get("origin")

        with open(taindex, "r") as f, open(outfile, "w") as o:
            reader = csv.reader(f)
            reader.__next__()   # skip the header row
            for row in reader:
                taobj = {
                    "jct_id": row[0],
                    "esac_id": row[0],
                    "end_date": row[2],
                    "data_url": row[4]
                }
                if row[1]:
                    taobj["relationship"] = row[1]
                    taobj["jct_id"] = taobj["jct_id"] + "." + taobj["relationship"]

                o.write(json.dumps(taobj) + "\n")

        self.log("TA data assembled")

        self._cleanup()