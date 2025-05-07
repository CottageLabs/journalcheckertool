from jct.lib import paths

######################################
# Deployment configuration

HOST = '0.0.0.0'
DEBUG = False
PORT = 5001
SSL = True
VALID_ENVIRONMENTS = ['dev', 'test', 'staging', 'production']

####################################
# Debug Mode

# PyCharm debug settings
DEBUG_PYCHARM = False  # do not try to connect to the PyCharm debugger by default
DEBUG_PYCHARM_SERVER = 'localhost'
DEBUG_PYCHARM_PORT = 6000

#######################################
# Elasticsearch configuration

ELASTICSEARCH_HOSTS = [{'host': 'localhost', 'port': 9200}, {'host': 'localhost', 'port': 9201}]
ELASTIC_SEARCH_VERIFY_CERTS = True  # Verify the SSL certificate of the ES host.  Set to False in dev.cfg to avoid having to configure your local certificates

# # 2 sets of elasticsearch DB settings - index-per-project and index-per-type. Keep both for now so we can migrate.
# # e.g. host:port/index/type/id
# ELASTIC_SEARCH_DB = "jct"
# ELASTIC_SEARCH_TEST_DB = "jcttest"

INITIALISE_INDEX = True  # whether or not to try creating the index and required index types on startup
ELASTIC_SEARCH_VERSION = "7.10.2"

# e.g. host:port/type/doc/id
ELASTIC_SEARCH_INDEX_PER_TYPE = True
INDEX_PER_TYPE_SUBSTITUTE = '_doc'  # Migrated from esprit
ELASTIC_SEARCH_DB_PREFIX = "jct-"  # note: include the separator
ELASTIC_SEARCH_TEST_DB_PREFIX = "jcttest-"

ES_TERMS_LIMIT = 1024
ELASTICSEARCH_REQ_TIMEOUT = 20  # Seconds - used in core.py for whole ES connection request timeout
ES_READ_TIMEOUT = '2m'  # Minutes - used in DAO for searches
ES_RETRY_HARD_LIMIT = 5

READ_ONLY_MODE = False

########################################
# File Path and URL Path settings

# root of the git repo
ROOT_DIR = paths.rel2abs(__file__, "..")

# base path, to the directory where this settings file lives
BASE_FILE_PATH = paths.abs_dir_path(__file__)

BASE_URL = "https://journalcheckertool.org"
if BASE_URL.startswith('https://'):
    BASE_DOMAIN = BASE_URL[8:]
elif BASE_URL.startswith('http://'):
    BASE_DOMAIN = BASE_URL[7:]
else:
    BASE_DOMAIN = BASE_URL

BASE_API_URL = "https://api.journalcheckertool.org/"
PREFERRED_URL_SCHEME = 'https'

# Whether the app is running behind a proxy, for generating URLs based on X-Forwarded-Proto
PROXIED = False

####################################
# Email Settings
# ~~->Email:ExternalService

# Settings for Flask-Mail. Set in app.cfg
MAIL_SERVER = None          # default localhost
MAIL_PORT = 25              # default 25
#MAIL_USE_TLS               # default False
#MAIL_USE_SSL               # default False
#MAIL_DEBUG                 # default app.debug
#MAIL_USERNAME              # default None
#MAIL_PASSWORD              # default None
#MAIL_DEFAULT_SENDER        # default None
#MAIL_MAX_EMAILS            # default None
#MAIL_SUPPRESS_SEND         # default app.testing

ENABLE_EMAIL = True

ADMIN_NAME = "JCT"
ADMIN_EMAIL = "sysadmin@cottagelabs.com"
ADMINS = ["steve@cottagelabs.com", "rama@cottagelabs.com"]

CONTACT_FORM_ADDRESS = "jct@cottagelabs.zendesk.com"
CC_ALL_EMAILS_TO = None

##############################################
# Elasticsearch Mappings
# ~~->Elasticsearch:Technology~~

FACET_FIELD = ".exact"

# an array of DAO classes from which to retrieve the type-specific ES mappings
# to be loaded into the index during initialisation.
ELASTIC_SEARCH_MAPPINGS = []

DEFAULT_INDEX_SETTINGS = \
    {
        'number_of_shards': 4,
        'number_of_replicas': 1
    }

DEFAULT_DYNAMIC_MAPPING = {
    'dynamic_templates': [
        {
            "strings": {
                "match_mapping_type": "string",
                "mapping": {
                    "type": "text",
                    "fields": {
                        "exact": {
                            "type": "keyword",
                            # "normalizer": "lowercase"
                        }
                    }
                }
            }
        }
    ]
}

MAPPINGS = {
    'unknown': {
        'mappings': DEFAULT_DYNAMIC_MAPPING,
        'settings': DEFAULT_INDEX_SETTINGS
    }
}