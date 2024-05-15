import os


def rel2abs(file, *args):
    file = os.path.realpath(file)
    if os.path.isfile(file):
        file = os.path.dirname(file)
    return os.path.abspath(os.path.join(file, *args))


DATABASES = rel2abs(__file__, "..", "databases")
RESOURCES = rel2abs(__file__, "..", "resources")
TEST_DATABASE = rel2abs(__file__, "..", "test_database")
TEMP_DIR = rel2abs(__file__, "..", "temp")

DIR_DATE_FORMAT = "%Y-%m-%d_%H%M"

# ROR Zenodo configuration settings
# Doc URL - https://ror.readme.io/docs/data-dump#download-ror-data-dumps-programmatically-with-the-zenodo-api
ZENODO_ROR_DOWNLOAD_PATH = "https://zenodo.org/api/records/?communities=ror-data&sort=mostrecent"
ROR_DIR_DATE_FORMAT = "%Y-%m-%d"

# Found at https://zenodo.org/record/6657125 - manually download and add to this repo when updated
# ROR_DATA_FILE = os.path.join(RESOURCES, "ror", "v1.32-2023-09-14-ror-data.zip")
ROR_DATA_FILE = None

MAX_DATASOURCE_AGE = {
    "crossref": 60 * 60 * 24 * 7,
    "doaj": 60 * 60 * 24 * 7,
    "doaj_inprogress": 60 * 60 * 24 * 7,
    "tj": 60 * 60 * 24 * 7,
    "ta": 60 * 60 * 24 * 7,
    "ror": 60 * 60 * 24 * 7,
    "sa_negative": 60 * 60 * 24 * 7,
    "sa_positive": 60 * 60 * 24 * 7,
    "funderdb": 60,   # funderdb is always updated, only a short delay to avoid importing multiple times in a concurrent run
    "oa_exceptions": 60 * 60 * 24 * 7,
    "jcs": 60 * 60 * 24 * 7
}

DATASOURCE_PATH = {
    "crossref": os.path.join(DATABASES, "crossref"),
    "doaj": os.path.join(DATABASES, "doaj"),
    "doaj_inprogress": os.path.join(DATABASES, "doaj_inprogress"),
    "tj": os.path.join(DATABASES, "tj"),
    "ta": os.path.join(DATABASES, "ta"),
    "ror": os.path.join(DATABASES, "ror"),
    "sa_negative": os.path.join(DATABASES, "sa_negative"),
    "sa_positive": os.path.join(DATABASES, "sa_positive"),
    "funderdb": os.path.join(DATABASES, "funderdb"),
    "oa_exceptions": os.path.join(DATABASES, "oa_exceptions"),
    "jcs": os.path.join(DATABASES, "jcs")
}

DATASOURCE_HISTORY = {
    "crossref": 3,
    "doaj": 3,
    "doaj_inprogress": 3,
    "tj": 3,
    "ta": 3,
    "ror": 3,
    "sa_negative": 3,
    "sa_positive": 3,
    "funderdb": 2,
    "oa_exceptions": 3,
    "jcs": 3
}

INDEX_PATH = {
    "jac": os.path.join(DATABASES, "jct", "jac"),
    "iac": os.path.join(DATABASES, "jct", "iac"),
    "funder_language": os.path.join(DATABASES, "jct", "funder_language"),
    "funder_config": os.path.join(DATABASES, "jct", "funder_config"),
    "journal": os.path.join(DATABASES, "jct", "journal"),
    "jcs_csv": os.path.join(DATABASES, "jct", "jcs_csv"),
    "ta": os.path.join(DATABASES, "jct", "ta"),
    "institution": os.path.join(DATABASES, "jct", "institution"),
    "bad_ta_issns": os.path.join(DATABASES, "jct", "bad_ta_issns")
}

INDEX_HISTORY = {
    "jac": 5,
    "iac": 5,
    "funder_language": 5,
    "funder_config": 5,
    "journal": 5,
    "jcs_csv": 2,
    "ta": 5,
    "institution": 5,
    "bad_ta_issns": 2
}

INDEX_LOADERS = {
    "jac": "es",
    "iac": "es",
    "funder_language": "es",
    "funder_config": "es",
    "journal": "es",
    "jcs_csv": "file",
    "ta": "es",
    "institution": "es",
    "bad_ta_issns": "helpdesk"
}

FILE_LOADER_PATHS = {
    "jcs_csv": rel2abs(__file__, "..", "..", "ui", "static", "data", "jcs_price_data.csv")
}

TEST_PATH = {
    "tj": os.path.join(DATABASES, "tests", "tj")
}

HELPDESK_LOADER_PATHS = {
    "bad_ta_issns": {
        "subject": "Bad TA ISSNs (testing, Laura you can ignore this)",
        "message": "The following ISSNs were found to be invalid in the TA dataset"
    }
}

CROSSREF_OLDEST_DOI = 2019
CROSSREF_MAILTO="us+jct@cottagelabs.com"

TJ_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT2SPOjVU4CKhP7FHOgaf0aRsjSOt-ApwLOy44swojTDFsWlZAIZViC0gdbmxJaEWxdJSnUmNoAnoo9/pub?gid=0&single=true&output=csv"

TA_INDEX_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vStezELi7qnKcyE8OiO2OYx2kqQDOnNsDX1JfAsK487n2uB_Dve5iDTwhUFfJ7eFPDhEjkfhXhqVTGw/pub?gid=1130349201&single=true&output=csv"

DOAJ_PUBLIC_DATA_DUMP = "https://doaj.org/public-data-dump/journal"

DOAJ_PUBLIC_DATA_DUMP_KEYFILE = rel2abs(__file__, "../keyfiles/doaj_public_data_dump.txt")

DOAJ_IN_PROGRESS_URL = "https://doaj.org/jct/inprogress"

DOAJ_IN_PROGRESS_KEYFILE = rel2abs(__file__, "../keyfiles/doaj_inprogress.txt")

SA_NEGATIVE_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ0EEMZTikcQZV28BiCL4huv-r0RnHiDrU08j3W1fyERNasoJYuAZek5G3oQH1TUKmf_X-yC5SiHaBM/pub?gid=0&single=true&output=csv"

SA_POSITIVE_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQXYjTvrKA3zTXPJDtO3MMj8zGISaQ-0p6d-CDSxJM0iv5DQ1BQ1S7JNy7BAiUw3K4MUE-zG8MbiL4R/pub?gid=0&single=true&output=csv"

# This is the data transfer sheet, but it appears to have updates that are not in the master sheet
# SA_POSITIVE_SHEET ="https://docs.google.com/spreadsheets/d/e/2PACX-1vTm6sDI16Kin3baNWaAiMUfGdMEUEGXy0LRvSDnvAQTWDN_exlYGyv4gnstGKdv3rXshjSa7AUWtAc5/pub?gid=0&single=true&output=csv"

OA_EXCEPTIONS_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSexj1DPUkhIDZvVX-CkGTkR_zwduUVlZ4DKVNnS1g0w1AlGKDUSx2t7HAawCcSAR6qqsJAQ7dPHWIa/pub?gid=404801205&single=true&output=csv"

FUNDER_DB_DIR = rel2abs(__file__, "..", "..", "funderdb")

JCS_API = "https://journalcomparisonservice.org/issns/{year}"

JCS_FIRST_YEAR = 2021

JAC_PREF_ORDER = ["doaj", "crossref", "jcs", "tj", "sa_negative", "sa_positive", "oa_exceptions", "ta"]

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
