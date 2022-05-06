
# elasticsearch API (simplified from original Noddy API, and TODO converted to newer ES with no types)
# NOTE it's worth looking at the old code if more complex queries, terms, etc are needed, as they are present there
# because the logger uses ES to log logs, ES uses console.log at some points where other things should use API.log

import Future from 'fibers/future'

API.es = {}

if not API.settings.es?
  console.log 'ES WARNING - ELASTICSEARCH SEEMS TO BE REQUIRED BUT SETTINGS HAVE NOT BEEN PROVIDED.'
else
  try
    API.settings.es.url = [API.settings.es.url] if typeof API.settings.es.url is 'string'
    for url in API.settings.es.url
      s = HTTP.call 'GET', url
    if API.settings.log?.level is 'debug'
      console.log 'ES confirmed ' + API.settings.es.url + ' is reachable'
  catch err
    console.log 'ES FAILURE - INSTANCE AT ' + API.settings.es.url + ' APPEARS TO BE UNREACHABLE.'
    console.log err
API.settings.es.index ?= API.settings.name ? 'noddy'

# track if we are waiting on retry to connect http to ES (when it is busy it takes a while to respond)
API.es._waiting = false
API.es._retries = {
  baseTimeout: 100,
  maxTimeout: 5000,
  times: 8,
  shouldRetry: (err,res,cb) ->
    rt = false
    try
      serr = err.toString()
      rt = serr.indexOf('ECONNREFUSED') isnt -1 or serr.indexOf('ECONNRESET') isnt -1 or serr.indexOf('socket hang up') isnt -1 or (typeof err?.response?.statusCode is 'number' and err.response.statusCode > 500)
    catch
      rt = true
    if rt and API.settings.dev # cannot API.log because will already be hitting ES access problems
      console.log 'Waiting for Retry on ES connection'
      try console.log serr
      try console.log err?.response?.statusCode
    API.es._waiting = rt
    cb null, rt
}

API.es.map = (index, type, mapping, overwrite, dev=API.settings.dev, url=API.settings.es.url) ->
  url = url[Math.floor(Math.random()*url.length)] if Array.isArray url
  console.log('ES checking mapping for ' + index + (if dev and index.indexOf('_dev') is -1 then '_dev' else '') + ' ' + type) if API.settings.log?.level is 'debug'
  try
    try RetryHttp.call 'PUT', url + '/' + index + (if dev and index.indexOf('_dev') is -1 then '_dev' else ''), {retry:API.es._retries}
    maproute = index + (if dev and index.indexOf('_dev') is -1 then '_dev' else '') + '/_mapping/' + type
    try
      m = RetryHttp.call 'GET', url + '/' + maproute, {retry:API.es._retries}
      overwrite = true if _.isEmpty(m.data)
    catch
      overwrite = true
    if overwrite
      try mapping ?= API.es._mapping
      if mapping?
        RetryHttp.call 'PUT', url + '/' + maproute, {data: mapping, retry:API.es._retries}

API.es.mapping = (index='', type='', dev=API.settings.dev, url=API.settings.es.url) ->
  index += '_dev' if index.length and dev and index.indexOf('_dev') is -1
  try
    mp = API.es.call 'GET', index + '/_mapping/' + type, undefined, undefined, undefined, undefined, undefined, undefined, dev, url
    return if index.length then (if type.length then mp[index].mappings[type] else mp[index].mappings) else mp
  catch
    return {}

API.es.call = (action, route, data, refresh, version, scan, scroll='10m', partial=false, dev=API.settings.dev, url=API.settings.es.url) ->
  return undefined if data? and typeof data is 'object' and data.script? and partial is false
  scroll = '120m' if scroll is true
  url = url[Math.floor(Math.random()*url.length)] if Array.isArray url
  route = '/' + route if route.indexOf('/') isnt 0
  return false if action is 'DELETE' and route.indexOf('/_all') is 0 # disallow delete all
  if dev and route.indexOf('_dev') is -1 and route.indexOf('/_') isnt 0
    rpd = route.split '/'
    rpd[1] += '_dev'
    rpd[1] = rpd[1].replace(',','_dev,')
    route = rpd.join '/'
  routeparts = route.substring(1, route.length).split '/'

  if API.es._waiting
    future = new Future()
    Meteor.setTimeout (() -> future.return()), Math.floor(Math.random()*601+300)
    future.wait()
  API.es._waiting = false

  opts = data:data
  if partial isnt false and route.indexOf('_update') is -1
    partial = 3 if partial is true
    route += '/_update'
    route += '?retry_on_conflict=' + partial if typeof partial is 'number'
  route += (if route.indexOf('?') is -1 then '?' else '&') + 'version=' + version if version?
  if scan is true
    route += (if route.indexOf('?') is -1 then '?' else '&')
    if not data? or (typeof data is 'object' and not data.sort?) or (typeof data is 'string' and data.indexOf('sort=') is -1)
      route += 'search_type=scan&'
    route += 'scroll=' + scroll
  else if scan?
    route = '/_search/scroll?scroll_id=' + scan + (if action isnt 'DELETE' then '&scroll=' + scroll else '')
  try
    try
      if action is 'POST' and data?.query? and data.sort? and routeparts.length > 1
        skey = _.keys(data.sort)[0].replace('.exact','')
        delete opts.data.sort if JSON.stringify(API.es.mapping(routeparts[0],(if routeparts.length > 1 and routeparts[1] isnt '_search' then routeparts[1] else '')),dev,url).indexOf(skey) is -1
    opts.retry = API.es._retries
    #console.log action, url, route, opts
    ret = RetryHttp.call action, url + route, opts
    if API.settings.log?.level in ['all','debug']
      ld = JSON.parse(JSON.stringify(ret.data))
      ld.hits.hits = ld.hits.hits.length if ld.hits?.hits?
      if '_search' in route and not ret.data?.hits?.hits?
        console.log JSON.stringify opts
        console.log JSON.stringify ld
    return ret.data
  catch err
    # if version and versions don't match, there will be a 409 thrown here - pass it back so collection can handle it
    # https://www.elastic.co/blog/elasticsearch-versioning-support
    lg = level: 'debug', msg: 'ES error, but may be OK, 404 for empty lookup, for example', action: action, url: url, route: route, opts: opts, error: err.toString()
    if err.response?.statusCode isnt 404 and route.indexOf('_log') is -1
      console.log(lg) if API.settings.log?.level? is 'debug'
    if API.settings.log?.level is 'all'
      console.log lg
      console.log JSON.stringify opts
      console.log JSON.stringify err
      try console.log err.toString()
    if API.settings.log?.level is 'debug' and err.response?.statusCode not in [404,409]
      console.log JSON.stringify opts
      console.log JSON.stringify err
      try console.log err.toString()
    # is it worth returning false for 404 and undefined otherwise? If so would need to check if undefined is expected anywhere, and how the API would return a false as 404, at the moment it only assumes that undefined is a 404 because false could be a valid response
    return if err.response?.statusCode is 409 then 409 else undefined

API.es.count = (index, type, key, query, dev=API.settings.dev, url=API.settings.es.url) ->
  query ?= { query: {"filtered":{"filter":{"bool":{"must":[]}}}}}
  if key?
    query.size = 0
    query.aggs = {
      "keycard" : {
        "cardinality" : {
          "field" : key,
          "precision_threshold": 40000 # this is high precision and will be very memory-expensive in high cardinality keys, with lots of different values going in to memory
        }
      }
    }
    return API.es.call('POST', '/' + index + (if type then '/' + type else '') + '/_search', query, undefined, undefined, undefined, undefined, undefined, dev, url)?.aggregations?.keycard?.value
  else
    return API.es.call('POST', '/' + index + (if type then '/' + type else '') + '/_search', query, undefined, undefined, undefined, undefined, undefined, dev, url)?.hits?.total

API.es.bulk = (index, type, data, action='index', bulk=50000, dev=API.settings.dev, url=API.settings.es.url) ->
  # https://www.elastic.co/guide/en/elasticsearch/reference/1.4/docs-bulk.html
  # https://www.elastic.co/guide/en/elasticsearch/reference/1.4/docs-update.html
  url = url[Math.floor(Math.random()*url.length)] if Array.isArray url
  index += '_dev' if dev and index.indexOf('_dev') is -1
  rows = if typeof data is 'object' and not Array.isArray(data) and data?.hits?.hits? then data.hits.hits else data
  rows = [rows] if not Array.isArray rows
  if index.indexOf('_log') is -1
    console.log 'Doing bulk ' + action + ' of ' + rows.length + ' rows for ' + index + ' ' + type
  else if API.settings.log?.level in ['all','debug']
    console.log 'Doing bulk ' + action + ' of ' + rows.length + ' rows for ' + index + ' ' + type
  loaded = 0
  counter = 0
  pkg = ''
  #responses = []
  for r of rows
    counter += 1
    row = rows[r]
    row._index += '_dev' if typeof row isnt 'string' and row._index? and row._index.indexOf('_dev') is -1 and dev
    meta = {}
    meta[action] = {"_index": (if typeof row isnt 'string' and row._index? then row._index else index), "_type": (if typeof row isnt 'string' and row._type? then row._type else type) }
    meta[action]._id = if action is 'delete' and typeof row is 'string' then row else (row._id if row._id?) # what if action is delete but can't set an ID?
    pkg += JSON.stringify(meta) + '\n'
    if action is 'create' or action is 'index'
      pkg += JSON.stringify(if row._source then row._source else row) + '\n'
    else if action is 'update'
      delete row._id if row._id?
      pkg += JSON.stringify({doc: row}) + '\n' # is it worth expecting other kinds of update in bulk import?
    # don't need a second row for deletes
    if counter is bulk or parseInt(r) is (rows.length - 1) or pkg.length > 70000000
      if API.settings.dev
        console.log 'ES bulk loading package of length ' + pkg.length + (if counter isnt bulk and pkg.length > 70000000 then ' triggered by length' else '')
      try
        #hp = 
        HTTP.call 'POST', url + '/_bulk', {content:pkg, headers:{'Content-Type':'text/plain'}} #,retry:API.es._retries}
        #responses.push hp
        loaded += counter
      catch err
        console.log err
      pkg = ''
      counter = 0
  return {records:loaded} #, responses:responses}



API.es._mapping = {
  "properties": {
    "location": {
      "properties": {
        "geo": {
          "type": "geo_point",
          "lat_lon": true
        }
      }
    },
    "created_date": {
      "type": "date",
      "format" : "yyyy-MM-dd HHmm||yyyy-MM-dd HHmm.ss||date_optional_time"
    },
    "updated_date": {
      "type": "date",
      "format" : "yyyy-MM-dd HHmm||yyyy-MM-dd HHmm.ss||date_optional_time"
    },
    "createdAt": {
      "type": "date",
      "format" : "yyyy-MM-dd HHmm||yyyy-MM-dd HHmm.ss||date_optional_time"
    },
    "updatedAt": {
      "type": "date",
      "format" : "yyyy-MM-dd HHmm||yyyy-MM-dd HHmm.ss||date_optional_time"
    },
    "attachment": {
      "type": "attachment",
      "index": "not_analyzed",
      "store": "no"
    }
  },
  "date_detection": false,
  "dynamic_templates" : [
    {
      "default" : {
        "match" : "*",
        "unmatch": "_raw_result",
        "match_mapping_type": "string",
        "mapping" : {
          "type" : "string",
          "fields" : {
            "exact" : {"type" : "{dynamic_type}", "index" : "not_analyzed", "store" : "no", "ignore_above": 1024} # ignore_above may not work in older ES...
          }
        }
      }
    }
  ]
}
