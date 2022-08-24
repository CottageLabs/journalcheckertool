import os


def rel2abs(file, *args):
    file = os.path.realpath(file)
    if os.path.isfile(file):
        file = os.path.dirname(file)
    return os.path.abspath(os.path.join(file, *args))


DATABASES = rel2abs(__file__, "..", "databases")
RESOURCES = rel2abs(__file__, "..", "resources")

DIR_DATE_FORMAT = "%Y-%m-%d_%H%M"

# # === DEPRECATED: ROR switched to Zenodo to serve these data dumps, we can no longer use this GitHub repo
# ROR_DIR_DATE_FORMAT = "%Y-%m-%d"
# ROR_DOWNLOAD_PATH = "https://github.com/ror-community/ror-api/raw/master/rorapi/data/"
# # Using github api to get the list of files in dir
# #         To get the tree sha,
# #         git clone https://github.com/ror-community/ror-api.git
# #         cd ror-api/rorapi/
# #         git ls-tree HEAD | grep data
# #         > 040000 tree 8ec3e0e5bce8a33c644f1544b877d756eca1a2f6    data
# ROR_TREE_SHA = "8ec3e0e5bce8a33c644f1544b877d756eca1a2f6"

# Found at https://zenodo.org/record/6657125 - manually download and add to this repo when updated
ROR_DATA_FILE = os.path.join(RESOURCES, "ror", "v1.1-2022-06-16-ror-data.zip")

MAX_DATASOURCE_AGE = {
    "crossref": 60 * 60 * 24 * 7,
    "doaj": 60 * 60 * 24 * 7,
    "doaj_inprogress": 60 * 60 * 24 * 7,
    "tj": 60 * 60 * 24 * 7,
    "ta": 60 * 60 * 24 * 7,
    "ror": 60 * 60 * 24 * 7,
    "sa_negative": 60 * 60 * 24 * 7,
    "sa_positive": 60 * 60 * 24 * 7
}

DATASOURCE_PATH = {
    "crossref": os.path.join(DATABASES, "crossref"),
    "doaj": os.path.join(DATABASES, "doaj"),
    "doaj_inprogress": os.path.join(DATABASES, "doaj_inprogress"),
    "tj": os.path.join(DATABASES, "tj"),
    "ta": os.path.join(DATABASES, "ta"),
    "ror": os.path.join(DATABASES, "ror"),
    "sa_negative": os.path.join(DATABASES, "sa_negative"),
    "sa_positive": os.path.join(DATABASES, "sa_positive")
}

DATASOURCE_HISTORY = {
    "crossref": 3,
    "doaj": 3,
    "doaj_inprogress": 3,
    "tj": 3,
    "ta": 3,
    "ror": 3,
    "sa_negative": 3,
    "sa_positive": 3
}

INDEX_PATH = {
    "jac": os.path.join(DATABASES, "jct", "jac"),
    "iac": os.path.join(DATABASES, "jct", "iac")
}

INDEX_HISTORY = {
    "jac": 5,
    "iac": 5
}

CROSSREF_OLDEST_DOI = 2019

TJ_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT2SPOjVU4CKhP7FHOgaf0aRsjSOt-ApwLOy44swojTDFsWlZAIZViC0gdbmxJaEWxdJSnUmNoAnoo9/pub?gid=0&single=true&output=csv"

TA_INDEX_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vStezELi7qnKcyE8OiO2OYx2kqQDOnNsDX1JfAsK487n2uB_Dve5iDTwhUFfJ7eFPDhEjkfhXhqVTGw/pub?gid=1130349201&single=true&output=csv"

DOAJ_IN_PROGRESS_URL = "https://doaj.org/jct/inprogress"

DOAJ_IN_PROGRESS_KEYFILE = "../keyfiles/doaj_inprogress.txt"

SA_NEGATIVE_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ0EEMZTikcQZV28BiCL4huv-r0RnHiDrU08j3W1fyERNasoJYuAZek5G3oQH1TUKmf_X-yC5SiHaBM/pub?gid=0&single=true&output=csv"

SA_POSITIVE_SHEET ="https://docs.google.com/spreadsheets/d/e/2PACX-1vTm6sDI16Kin3baNWaAiMUfGdMEUEGXy0LRvSDnvAQTWDN_exlYGyv4gnstGKdv3rXshjSa7AUWtAc5/pub?gid=0&single=true&output=csv"

JAC_PREF_ORDER = ["doaj", "crossref", "tj", "sa_negative", "sa_positive", "ta"]

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
ES_INDEX_PREFIX = 'jct'
ES_INDEX_SUFFIX = 'dev'

JCT_BASE_URL = 'http://localhost:3002/api/service/jct/' # end in slash
JCT_IMPORT_URL = JCT_BASE_URL + 'import?refresh=true'
JCT_TA_IMPORT_URL = JCT_BASE_URL + 'ta/import'
JCT_TEST_URL = JCT_BASE_URL + 'test'
JCT_TEST_TIMEOUT = 120  # 2 minutes

MAILGUN_KEY = ""
MAILGUN_DOMAIN = ""
STATUS_EMAIL_RECEIVER = ''
STATUS_EMAIL_SENDER = ''
MAILGUN_SUBJECT_PREFIX = 'jct dev'
