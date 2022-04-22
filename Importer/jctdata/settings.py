import os

def rel2abs(file, *args):
    file = os.path.realpath(file)
    if os.path.isfile(file):
        file = os.path.dirname(file)
    return os.path.abspath(os.path.join(file, *args))


DATABASES = rel2abs(__file__, "..", "databases")
RESOURCES = rel2abs(__file__, "..", "resources")

DIR_DATE_FORMAT = "%Y-%m-%d_%H%M"
ROR_DIR_DATE_FORMAT = "%Y-%m-%d"
ROR_DOWNLOAD_PATH = "https://github.com/ror-community/ror-api/raw/master/rorapi/data/"
# Using github api to get the list of files in dir
#         To get the tree sha,
#         git clone https://github.com/ror-community/ror-api.git
#         cd ror-api/rorapi/
#         git ls-tree HEAD | grep data
#         > 040000 tree 8ec3e0e5bce8a33c644f1544b877d756eca1a2f6    data
ROR_TREE_SHA = "8ec3e0e5bce8a33c644f1544b877d756eca1a2f6"

ROR_DATA_FILE = os.path.join(RESOURCES, "ror", "v1.0-2022-03-17-ror-data.json.zip")

MAX_DATASOURCE_AGE = {
    "crossref" : 60 * 60 * 24 * 7,
    "doaj" : 60 * 60 * 24 * 7,
    "tj" : 60 * 60 * 24 * 7,
    "ror": 60 * 60 * 24 * 7
}

DATASOURCE_PATH = {
    "crossref" : os.path.join(DATABASES, "crossref"),
    "doaj" : os.path.join(DATABASES, "doaj"),
    "tj" : os.path.join(DATABASES, "tj"),
    "ror": os.path.join(DATABASES, "ror")
}

CROSSREF_OLDEST_DOI = 2019

JAC_PREF_ORDER = [
    "doaj",
    "crossref"
]

DEFAULT_MAPPING = {
    "dynamic_templates": [
        {
            "default": {
                "match": "*",
                "match_mapping_type": "string",
                "mapping": {
                    "type": "multi_field",
                    "fields": {
                        "{name}": {"type": "{dynamic_type}", "index": "analyzed", "store": "no"},
                        "exact": {"type": "{dynamic_type}", "index": "not_analyzed", "store": "yes"}
                    }
                }
            }
        }
    ]
}

ES_HOST = "http://localhost:9200"
INDEX_SUFFIX_DATE_FORMAT = "%Y%m%d%H%M%S"
INDEX_KEEP_OLD_INDICES = 2