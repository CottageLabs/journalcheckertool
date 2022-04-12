import os

def rel2abs(file, *args):
    file = os.path.realpath(file)
    if os.path.isfile(file):
        file = os.path.dirname(file)
    return os.path.abspath(os.path.join(file, *args))


DATABASES = rel2abs(__file__, "..", "databases")

DIR_DATE_FORMAT = "%Y-%m-%d_%H%M"

MAX_DATASOURCE_AGE = {
    "crossref" : 60 * 60 * 24 * 7,
    "doaj" : 60 * 60 * 24 * 7,
    "tj" : 60 * 60 * 24 * 7
}

DATASOURCE_PATH = {
    "crossref" : os.path.join(DATABASES, "crossref"),
    "doaj" : os.path.join(DATABASES, "doaj"),
    "tj" : os.path.join(DATABASES, "tj")
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
INDEX = "jct_dev"
INDEX_SUFFIX_DATE_FORMAT = "%Y%m%d%H%M"