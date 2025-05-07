from jct.core import es_connection as ES, app

import json
import re
import time
import elasticsearch
from copy import deepcopy

ES_MAPPING_MISSING_REGEX = re.compile(r'.*No mapping found for \[[a-zA-Z0-9-_\.]+?\] in order to sort on.*', re.DOTALL)
CONTENT_TYPE_JSON = {'Content-Type': 'application/json'}

class BlockTimeOutException(Exception):
    pass


class DAOSaveExceptionMaxRetriesReached(Exception):
    pass


class ESResponseCannotBeInterpreted(Exception):
    pass


class ESMappingMissingError(Exception):
    pass


class ESError(Exception):
    pass

class DAO:

    TYPE = ""

    @classmethod
    def get(self, id):
        raise NotImplementedError()

    @classmethod
    def save(self, obj):
        raise NotImplementedError()

    @classmethod
    def index_name(cls):
        return app.config.get("ELASTIC_SEARCH_DB_PREFIX", "") + cls.TYPE

    @classmethod
    def doc_type(cls):
        return cls.TYPE

    @classmethod
    def pull(cls, id):
        """Retrieve object by id."""
        if id is None or id == '':
            return None

        try:
            out = ES.get(cls.index_name(), id, doc_type=cls.doc_type())
        except elasticsearch.NotFoundError:
            return None
        except elasticsearch.TransportError as e:
            raise Exception("ES returned an error: {x}".format(x=e.info))
        except Exception as e:
            return None
        if out is None:
            return None

        return out

    @classmethod
    def pull_by_key(cls, key, value):
        res = cls.query(q={"query": {"term": {key + ".exact": value}}})
        if res.get('hits', {}).get('total', {}).get('value', 0) == 1:
            return cls.pull(res['hits']['hits'][0]['_source']['id'])
        else:
            return None

    @classmethod
    def find_by_key(cls, key, value, max=10):
        return cls.object_query(q={"query": {"term": {key + ".exact": value}}, "size": max})

    @classmethod
    def object_query(cls, q=None, **kwargs):
        result = cls.query(q, **kwargs)
        return [cls(**r.get("_source")) for r in result.get("hits", {}).get("hits", [])]

    @classmethod
    def query(cls, q=None, **kwargs):
        """Perform a query on backend.

        :param q: maps to query_string parameter if string, or query dict if dict.
        :param kwargs: any keyword args as per
            http://www.elasticsearch.org/guide/reference/api/search/uri-request.html
        """
        query = cls.make_query(q, **kwargs)
        return cls.send_query(query)

    @staticmethod
    def make_query(theq=None, should_terms=None, consistent_order=True, **kwargs):
        """
        Generate a query object based on parameters but don't send to
        backend - return it instead. Must always have the same
        parameters as the query method. See query method for explanation
        of parameters.
        """
        if theq is None:
            theq = ""
        q = deepcopy(theq)
        if isinstance(q, dict):
            query = q
            if 'bool' not in query['query']:
                boolean = {'bool': {'must': []}}
                boolean['bool']['must'].append(query['query'])
                query['query'] = boolean
            if 'must' not in query['query']['bool']:
                query['query']['bool']['must'] = []
        elif q:
            query = {
                'query': {
                    'bool': {
                        'must': [
                            {'query_string': {'query': q}}
                        ]
                    }
                }
            }
        else:
            query = {
                'query': {
                    'bool': {
                        'must': [
                            {'match_all': {}}
                        ]
                    }
                }
            }

        if should_terms is not None and len(should_terms) > 0:
            for s in should_terms:
                if not isinstance(should_terms[s], list):
                    should_terms[s] = [should_terms[s]]
                query["query"]["bool"]["must"].append({"terms": {s: should_terms[s]}})

        sort_specified = False
        for k, v in kwargs.items():
            if k == '_from':
                query['from'] = v
            elif k == 'sort':
                sort_specified = True
                query['sort'] = v
            else:
                query[k] = v
        if "sort" in query:
            sort_specified = True

        if not sort_specified and consistent_order:
            # FIXME: review this - where is default sort necessary, and why do we want this in ID order?
            query['sort'] = [{"id.exact": {"order": "asc", "unmapped_type": "keyword"}}]

        return query

    @classmethod
    def send_query(cls, qobj, retry=50, **kwargs):
        """Actually send a query object to the backend.
        :param kwargs are passed directly to Elasticsearch search() function
        """

        if retry > app.config.get("ES_RETRY_HARD_LIMIT", 1000) + 1:  # an arbitrary large number
            retry = app.config.get("ES_RETRY_HARD_LIMIT", 1000) + 1

        r = None
        count = 0
        exception = None
        while count < retry:
            count += 1
            try:
                # ES 7.10 updated target to whole index, since specifying type for search is deprecated
                # r = requests.post(cls.target_whole_index() + recid + "_search", data=json.dumps(qobj),  headers=CONTENT_TYPE_JSON)
                if kwargs.get('timeout') is None:
                    kwargs['timeout'] = app.config.get('ES_READ_TIMEOUT', None)
                index = cls.index_name()
                r = ES.search(body=json.dumps(qobj), index=index, doc_type=cls.doc_type(),
                              headers=CONTENT_TYPE_JSON, **kwargs)
                break
            except Exception as e:
                try:
                    exception = ESMappingMissingError(e) if ES_MAPPING_MISSING_REGEX.match(json.dumps(e.args[2])) else e
                    if isinstance(exception, ESMappingMissingError):
                        raise exception
                except TypeError:
                    raise e

            time.sleep(0.5)

        if r is not None:
            return r
        if exception is not None:
            raise exception
        raise Exception("Couldn't get the ES query endpoint to respond.  Also, you shouldn't be seeing this.")
