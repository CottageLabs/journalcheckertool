
import moment from 'moment'
import { Random } from 'meteor/random'

# there are a few direct debug console.log calls in here, depending on whether or not the collection is
# one with _log in the name or not, just to avoid endless log loops but still have useful output in debug mode for dev

API.collection = (opts, dev=API.settings.dev) ->
  opts = { type: opts } if typeof opts is 'string'
  if opts.devislive is true
    this._devislive = true
    dev = true
  opts.index ?= API.settings.es.index
  this._index = opts.index
  this._type = opts.type
  this._route = '/' + this._index
  this._route += '/' + this._type if this._type
  this._mapping = opts.mapping
  API.es.map this._index, this._type, this._mapping, undefined, dev # only has effect if no mapping already

API.collection.prototype.map = (mapping, dev=API.settings.dev) ->
  dev = true if this._devislive is true
  this._mapping = mapping
  return API.es.map this._index, this._type, mapping, true, dev # would overwrite any existing mapping
API.collection.prototype.mapping = (original, dev=API.settings.dev) -> 
  dev = true if this._devislive is true
  return if original then this._mapping else API.es.mapping this._index, this._type, dev

API.collection.prototype.get = (rid, versioned, dev=API.settings.dev) ->
  dev = true if this._devislive is true
  # TODO is there any case for recording who has accessed certain documents?
  # NOTE this only works case-sensitively so record IDs have to be in the correct case
  if typeof rid is 'number' or (typeof rid is 'string' and rid.indexOf(' ') is -1 and rid.indexOf(':') is -1 and rid.indexOf('/') is -1 and rid.indexOf('*') is -1)
    check = API.es.call 'GET', this._route + '/' + rid, undefined, undefined, undefined, undefined, undefined, undefined, dev
    return (if versioned then check else check._source) if check?.found isnt false and check?.status isnt 'error' and check?.statusCode isnt 404 and check?._source?
  return undefined

API.collection.prototype.insert = (q, obj, uid, refresh, dev=API.settings.dev) ->
  dev = true if this._devislive is true
  if typeof q is 'string' and typeof obj is 'object'
    obj._id = q
  else if typeof q is 'object' and not obj?
    obj = q
  if Array.isArray obj
    ups = []
    for o of obj
      obj[o].createdAt = Date.now()
      obj[o].created_date = moment(obj[o].createdAt, "x").format "YYYY-MM-DD HHmm.ss"
      obj[o]._id ?= Random.id()
      ups.push obj[o]
    return this.bulk ups, 'index', uid, undefined, dev
  else
    obj.createdAt = Date.now()
    obj.created_date = moment(obj.createdAt, "x").format "YYYY-MM-DD HHmm.ss"
    obj._id ?= Random.id()
    return API.es.call('POST', this._route + '/' + obj._id, obj, refresh, undefined, undefined, undefined, undefined, dev)?._id

API.collection.prototype.update = (q, obj, uid, refresh, versioned, partial, dev=API.settings.dev) ->
  dev = true if this._devislive is true
  # versioned here can be a version number, in which case the update will only work if it can update onto that version, otherwise returns 409
  # if no version number provided, versioning of the update will still be used for internal clash avoidance
  # and will not necessarily be versioned to the version the user last saw - just to the last version this update method retrieved immediately before the action.
  return undefined if obj?.script? and partial isnt true
  if typeof q is 'object' and q._id? and obj is undefined
    obj = q
    q = obj._id
  q ?= obj._id
  return false if not q?
  res = this.get q, true, dev
  if res
    rec = res._source
    if _.keys(obj).length is 1 and typeof _.values(obj)[0] is 'string' and  (_.values(obj)[0].indexOf('+') is 0 or _.values(obj)[0].indexOf('-') is 0)
      if rec[_.keys(obj)[0]]? and typeof rec[_.keys(obj)[0]] is 'number'
        partial = true
        obj = {script: "ctx._source." + _.keys(obj)[0] + _.values(obj)[0].replace('+=','+').replace('-=','-').replace('+','+=').replace('-','-=')}
      else
        obj[_.keys(obj)[0]] = 1
    if not partial
      for k of obj
        API.collection.dot(rec,k,obj[k]) if k isnt '_id'
      rec.updatedAt = Date.now()
      rec.updated_date = moment(rec.updatedAt, "x").format "YYYY-MM-DD HHmm.ss"
    rs = API.es.call 'POST', this._route + '/' + rec._id, (if partial then obj else rec), refresh, versioned, undefined, undefined, partial, dev
    if rs is 409
      # TODO think about whether using versioned updates is useful all the time or not. For now, it will only be used if version is set by whatever 
      return 409
    else
      return if rs?._version? then rs._version else rs
  else
    # TODO alter this to return something and set action to 'update' to get a bulk each instead of individual record updates
    return this.each q, undefined, ((res) -> this.update res._id, obj, uid, refresh, versioned, partial, dev), undefined, uid, undefined, dev

API.collection.prototype.remove = (q, uid, dev=API.settings.dev) ->
  dev = true if this._devislive is true
  if (typeof q is 'string' or typeof q is 'number') and this.get q
    API.es.call 'DELETE', this._route + '/' + q, undefined, undefined, undefined, undefined, undefined, undefined, dev
    return true
  else if q is '*'
    # TODO who should be allowed to do this?
    omp = this.mapping true, dev
    API.es.call 'DELETE', this._route, undefined, undefined, undefined, undefined, undefined, undefined, dev
    API.es.map this._index, this._type, omp, undefined, dev
    return true
  else
    # TODO alter this to return the record ID and set action to 'remove' to get a bulk each instead of individual record removes
    return this.each q, undefined, ((res) -> this.remove res._id, uid, dev), undefined, uid, undefined, dev

API.collection.prototype.search = (q, opts, versioned, dev=API.settings.dev) ->
  dev = true if this._devislive is true
  # NOTE is there any case for recording who has done searches? - a write for every search could be a heavy load...
  # or should it be possible to apply certain restrictions on what the search returns?
  # Perhaps - but then this coud/should be applied by the service providing access to the collection
  _es_meta = false
  if typeof q is 'object' and q._es_meta?
    _es_meta = q._es_meta
    delete q._es_meta
  if typeof opts is 'object' and opts._es_meta?
    _es_meta = opts._es_meta
    delete opts._es_meta
  try
    versioned = opts.versioned
    delete opts.versioned
  if opts is 'versioned'
    versioned = true
    opts = undefined
  dbq = false
  if typeof q is 'object' and q.queryParams?.dbq?
    dbq = true
    delete q.queryParams.dbq
  q = API.collection._translate q, opts
  res = {}
  if not q?
    res = undefined
  else if typeof q is 'string'
    res = API.es.call 'GET', this._route + '/_search?' + (if versioned then 'version=true&' else '') + (if q.indexOf('?') is 0 then q.replace('?', '') else q), undefined, undefined, undefined, undefined, undefined, undefined, dev
  else
    res = API.es.call 'POST', this._route + '/_search' + (if versioned then '?version=true' else ''), q, undefined, undefined, undefined, undefined, undefined, dev
  if API.settings.dev
    res ?= {}
    res.q = q
  if dbq and q? and res?.hits?.total? and res.hits.total > 0 and dev # simple way to get rid of records in test indexes
    res.deleted = this.remove q
  if res? and _es_meta is false
    delete res.timed_out
    delete res._shards
  return res

API.collection.prototype.find = (q, opts, versioned, dev=API.settings.dev) ->
  dev = true if this._devislive is true
  try versioned = opts.versioned
  if opts is 'versioned'
    versioned = true
    opts = undefined
  opts ?= true
  got = this.get q, versioned, dev
  if got?
    return got
  else
    try
      return undefined if not q? or JSON.stringify(q).length < 3
      hits = this.search(q, opts, versioned, dev).hits.hits
      return if hits.length isnt 0 then (if versioned then hits[0] else hits[0]._source ? hits[0].fields ? {_id: hits[0]._id}) else undefined
    catch err
      return undefined

API.collection.prototype.bulk = (recs, action, uid, bulk, dev=API.settings.dev) ->
  dev = true if this._devislive is true
  # ES uses index/update/delete whereas I've used insert/update/remove in collections, so accept either of them
  # ES accepts create too, which will only create if not already existing whereas index overwrites - but difference not needed yet
  return false if not action? or not recs? or recs.length < 1 or typeof recs isnt 'object' or ['insert','index','update','remove','delete'].indexOf(action) is -1
  # recs must be a list of records, or change docs, or ID strings
  # NOTE what about versioning and version clashes
  # is it worth the bulk process "locking" other collection writes while it runs? How would that work across a cluster? Would need a lock index...
  # it may be better for update and remove to just behave in this way anyway, depends what actions have to occur on those records
  # NOTE that for bulk update this so far only works with docs. Also, docs don't work on dot notation - to replace a value in an object, whole object must be specified
  ret = API.es.bulk this._index, this._type, recs, (if action is 'insert' then 'index' else if action is 'remove' then 'delete' else action), bulk, dev
  if ret? # what is the best check here?
    return ret
  else
    return false

API.collection.prototype.each = (q, opts, fn, action, uid, scroll='20m', dev=API.settings.dev) ->
  dev = true if this._devislive is true
  # each executes the function for each record. If the function makes changes to a record and saves those changes, 
  # this can cause many writes to the collection. So, instead, that sort of function could return something
  # and if the action has also been specified then all the returned values will be used to do a bulk write to the collection index.
  # suitable returns would be entire records for insert, record update objects for update, or record IDs for remove
  # this does not allow different actions for different records that are operated on - so has to be bulks of the same action
  started = Date.now()
  if fn is undefined and opts is undefined and typeof q is 'function'
    fn = q
    q = '*'
  if fn is undefined and typeof opts is 'function'
    fn = opts
    opts = undefined
  opts ?= {}
  qy = API.collection._translate q, opts
  qy.from ?= 0
  sz = qy.size ? 800
  qy.size = 1
  chk = API.es.call 'POST', this._route + '/_search', qy, undefined, undefined, undefined, undefined, undefined, dev
  if chk?.hits?.total? and chk.hits.total isnt 0
    # make sure that query result size does not take up more than about 1gb
    # NOTE also that in a scroll-scan size is per shard, not per result set
    max_size = Math.floor(1000000000 / (Buffer.byteLength(JSON.stringify(chk.hits.hits[0])) * chk._shards.total))
    sz = max_size if max_size < sz
  qy.size = sz
  res = API.es.call 'POST', this._route + '/_search', qy, undefined, undefined, true, undefined, undefined, dev
  if res?.hits?.total? and res.hits.total isnt 0 and res.hits.total isnt res.hits.hits.length and res._scroll_id?
    res = API.es.call 'GET', '/_search/scroll', undefined, undefined, undefined, res._scroll_id, scroll, undefined, dev
  return 0 if not res?.hits?.hits? or res.hits.hits.length is 0
  total = res.hits.total
  processed = 0
  updates = []
  breaker = false
  while res?.hits?.hits? and res.hits.hits.length and not breaker
    for h in res.hits.hits
      fn = fn.bind this
      fr = fn h._source ? h.fields ? {_id: h._id}
      processed += 1
      updates.push(fr) if fr? and (typeof fr is 'object' or typeof fr is 'string')
      if fr is 'break'
        breaker = true
        console.log('break triggered in collection each') if API.settings.dev
        break
    if res._scroll_id?
      rss = API.es.call 'GET', '/_search/scroll', undefined, undefined, undefined, res._scroll_id, scroll, undefined, dev
      if not rss?
        res = undefined
      else
        res = rss
    else
      res.hits.hits = []
  if action? and updates.length
    bulked = this.bulk updates, action, uid, undefined, dev
  return if action then {total: total, updated:updates.length, processed:processed, bulk: bulked} else processed

API.collection.prototype.fetch = (q, opts={}, dev=API.settings.dev) ->
  dev = true if this._devislive is true
  qy = API.collection._translate q, opts
  qy.from ?= 0
  qy.size ?= 3000
  results = [] # NOTE if results is bigger than what node can hold, which by default is 1.7G, this will fail. Also the below scrolls would fail if any one of them brings back too much data
  res = API.es.call 'POST', this._route + '/_search', qy, undefined, undefined, true, undefined, undefined, dev
  if res.hits.hits.length
    for h in res.hits.hits
      results.push h._source ? h.fields ? {_id: h._id}
    # scroll queries that are not of scan type will have results in the first request, whereas scan queries will not
  return results if not res?._scroll_id?
  res = API.es.call 'GET', '/_search/scroll', undefined, undefined, undefined, res._scroll_id, undefined, undefined, dev
  return results if not res?._scroll_id? or not res.hits?.hits? or res.hits.hits.length is 0
  while (res.hits.hits.length)
    for h in res.hits.hits
      results.push h._source ? h.fields ? {_id: h._id}
    res = API.es.call 'GET', '/_search/scroll', undefined, undefined, undefined, res._scroll_id, undefined, undefined, dev
  return results

API.collection.prototype.count = (key, q, dev=API.settings.dev) ->
  dev = true if this._devislive is true
  if not q?
    kq = typeof key is 'object'
    if not kq and typeof key is 'string'
      kq = key.indexOf('*') isnt -1
      if not kq
        mp = JSON.stringify this.mapping()
        kq = mp.indexOf(key.replace('.exact','')) is -1
    if kq
      return API.es.count this._index, this._type, undefined, API.collection._translate(key), dev
  return API.es.count this._index, this._type, key, API.collection._translate(q), dev


### query formats that can be accepted:
    'A simple string to match on'
    'statement:"A more complex" AND difficult string' - which will be used as is to ES as a query string
    '?q=query params directly as string'
    {"q":"object of query params"} - must contain at least q or source as keys to be identified as such
    {"must": []} - a list of must queries, in full ES syntax, which will be dropped into the query filter (works for "should" as well)
    {"object":"of key/value pairs, all of which must match"} - so this is an AND terms match (.exact will be added where not present on keys) - if keys do not point to strings, they will be assumed to be named ES queries that can drop into the bool
    ["list","of strings to OR match on"] - this is an OR query strings match UNLESS strings contain : then mapped to terms matches
    [{"list":"of objects to OR match"}] - so a set of OR terms matches (.exact will be added if objects) - if objects are not key: string they are assumed to be full ES queries that can drop into the bool

    Keys can use dot notation, and can use .exact so that terms match on full terms e.g. "Mark MacGillivray" rather than partials

    Options that can be included:
    If options is true, the query will be adjusted to sort by createdAt descending, so returning the newest first (it sets newest:true, see below)
    If options is string 'random' it will convert the query to be a random order
    If options is a number it will be assumed to be the size parameter
    Otherwise options should be an object (and the above can be provided as keys, "newest", "random")
    If newest is true the query will have a sort desc on createdAt. If false, sort will be asc
    If "random" key is provided, "seed" can be provided too if desired, for seeded random queries
    If "restrict" is provided, should point to list of ES queries to add to the and part of the query filter
    Any other keys in the options object should be directly attributable to an ES query object
    TODO can add more conveniences for passing options in here, such as simplified terms, etc.

    Default query looks like:
    {query: {filtered: {query: {match_all: {}}, filter: {bool: {must: []}}}}, size: 10}
###
API.collection._translate = (q, opts) ->
  console.log('Translating query',q,opts) if API.settings.log?.level is 'all'
  opts = {random:true} if opts is 'random'
  opts = {size:opts} if typeof opts is 'number'
  opts = {newest: true} if opts is true
  opts = {newest: false} if opts is false
  qry = opts?.query ? {}
  qry.query ?= {}
  _structure = (sq) ->
    if not sq.query? or not sq.query.filtered?
      sq.query = filtered: {query: sq.query, filter: {}}
    sq.query.filtered.filter ?= {}
    sq.query.filtered.filter.bool ?= {}
    sq.query.filtered.filter.bool.must ?= []
    if not sq.query.filtered.query.bool?
      ms = []
      ms.push(sq.query.filtered.query) if not _.isEmpty sq.query.filtered.query
      sq.query.filtered.query = bool: must: ms
    sq.query.filtered.query.bool.must ?= []
    return sq
  qry = _structure qry
  if typeof q is 'object'
    # if a search endpoint passes its "this" contenxt then expand out the query or body params
    if q.queryParams? or q.bodyParams?
      qp = q.queryParams ? {}
      if q.bodyParams?
        for b of q.bodyParams
          qp[b] = q.bodyParams[b]
      q = qp
    delete q.apikey if q.apikey?
    delete q._ if q._?
    delete q.callback if q.callback?
    # some URL params that may be commonly used in this API along with valid ES URL query params will be removed here by default too
    # this makes it easy to handle them in routes whilst also just passing the whole queryParams object into this translation method and still get back a valid ES query
    delete q.key if q.key?
    delete q.counts if q.counts?
    if JSON.stringify(q).indexOf('[') is 0
      qry.query.filtered.filter.bool.should = []
      for m in q
        if typeof m is 'object' and m?
          for k of m
            if typeof m[k] is 'string'
              tobj = term:{}
              tobj.term[k.replace('.exact','')+'.exact'] = m[k] # TODO is it worth checking mapping to see if .exact is used by it...
              qry.query.filtered.filter.bool.should.push tobj
            else if typeof m[k] in ['number','boolean']
              qry.query.filtered.query.bool.should.push {query_string:{query:k + ':' + m[k]}}
            else if m[k]?
              qry.query.filtered.filter.bool.should.push m[k]
        else if typeof m is 'string'
          qry.query.filtered.query.bool.should ?= []
          qry.query.filtered.query.bool.should.push query_string: query: m
    else if q.query?
      qry = q # assume already a query
    else if q.source?
      qry = JSON.parse(q.source) if typeof q.source is 'string'
      qry = q.source if typeof q.source is 'object'
      opts ?= {}
      for o of q
        opts[o] ?= q[o] if o not in ['source']
    else if q.q?
      if q.prefix? and q.q.indexOf(':') isnt -1
        delete q.prefix
        pfx = {}
        qpts = q.q.split ':'
        pfx[qpts[0]] = qpts[1]
        qry.query.filtered.query.bool.must.push prefix: pfx
      else
        qry.query.filtered.query.bool.must.push query_string: query: q.q
      opts ?= {}
      for o of q
        opts[o] ?= q[o] if o not in ['q']
    else
      if q.must?
        qry.query.filtered.filter.bool.must = q.must
      if q.should?
        qry.query.filtered.filter.bool.should = q.should
      if q.must_not?
        qry.query.filtered.filter.bool.must_not = q.must_not
      for y of q # an object where every key is assumed to be an AND term search if string, or a named search object to go in to ES
        if (y in ['fields','terms']) or (y is 'sort' and typeof q[y] is 'string' and q[y].indexOf(':') isnt -1) or (y in ['from','size'] and (typeof q[y]is 'number' or not isNaN parseInt q[y]))
          opts ?= {}
          opts[y] = q[y]
        else if y not in ['must','must_not','should']
          if typeof q[y] is 'string'
            tobj = term:{}
            tobj.term[y.replace('.exact','')+'.exact'] = q[y] # TODO is it worth checking mapping to see if .exact is used by it...
            qry.query.filtered.filter.bool.must.push tobj
          else if typeof q[y] in ['number','boolean']
            qry.query.filtered.query.bool.must.push {query_string:{query:y + ':' + q[y]}}
          else if typeof q[y] is 'object'
            qobj = {}
            qobj[y] = q[y]
            qry.query.filtered.filter.bool.must.push qobj
          else if q[y]?
            qry.query.filtered.filter.bool.must.push q[y]
  else if typeof q is 'string'
    if q.indexOf('?') is 0
      qry = q # assume URL query params and just use them as such?
    else if q?
      q = '*' if q is ''
      qry.query.filtered.query.bool.must.push query_string: query: q
  qry = _structure qry # do this again to make sure valid structure is present after above changes, and before going through opts which require expected structure
  if opts?
    if opts.newest is true
      delete opts.newest
      opts.sort = {createdAt:{order:'desc'}}
    else if opts.newest is false
      delete opts.newest
      opts.sort = {createdAt:{order:'asc'}}
    delete opts._ # delete anything that may have come from query params but are not handled by ES
    delete opts.apikey
    if opts.fields and typeof opts.fields is 'string' and opts.fields.indexOf(',') isnt -1
      opts.fields = opts.fields.split(',')
    if opts.random
      if typeof qry is 'string'
        qry += '&random=true' # the ES module knows how to convert this to a random query
        qry += '&seed=' + opts.seed if opts.seed?
      else
        fq = {function_score: {random_score: {}}}
        fq.function_score.random_score.seed = seed if opts.seed?
        if qry.query.filtered
          fq.function_score.query = qry.query.filtered.query
          qry.query.filtered.query = fq
        else
          fq.function_score.query = qry.query
          qry.query = fq
      delete opts.random
      delete opts.seed
    if opts._include? or opts.include? or opts._includes? or opts.includes? or opts._exclude? or opts.exclude? or opts._excludes? or opts.excludes?
      qry._source ?= {}
      inc = if opts._include? then '_include' else if opts.include? then 'include' else if opts._includes? then '_includes' else 'includes'
      includes = opts[inc]
      if includes?
        includes = includes.split(',') if typeof includes is 'string'
        qry._source.includes = includes
        delete opts[inc]
      exc = if opts._exclude? then '_exclude' else if opts.exclude? then 'exclude' else if opts._excludes? then '_excludes' else 'excludes'
      excludes = opts[exc]
      if excludes?
        excludes = excludes.split(',') if typeof excludes is 'string'
        for i in includes ? []
          excludes = _.without(excludes, i) if i in excludes
        qry._source.excludes = excludes
        delete opts[exc]
    if opts.and?
      qry.query.filtered.filter.bool.must.push a for a in opts.and
      delete opts.and
    if opts.sort?
      if typeof opts.sort is 'string' and opts.sort.indexOf(',') isnt -1
        if opts.sort.indexOf(':') isnt -1
          os = []
          for ps in opts.sort.split ','
            nos = {}
            nos[ps.split(':')[0]] = {order:ps.split(':')[1]}
            os.push nos
          opts.sort = os
        else
          opts.sort = opts.sort.split ','
      if typeof opts.sort is 'string' and opts.sort.indexOf(':') isnt -1
        os = {}
        os[opts.sort.split(':')[0]] = {order:opts.sort.split(':')[1]}
        opts.sort = os
    if opts.restrict?
      qry.query.filtered.filter.bool.must.push(rs) for rs in opts.restrict
      delete opts.restrict
    if opts.not? or opts.must_not?
      tgt = if opts.not? then 'not' else 'must_not'
      if _.isArray opts[tgt]
        qry.query.filtered.filter.bool.must_not = opts[tgt]
      else
        qry.query.filtered.filter.bool.must_not ?= []
        qry.query.filtered.filter.bool.must_not.push(nr) for nr in opts[tgt]
      delete opts[tgt]
    if opts.should?
      if _.isArray opts.should
        qry.query.filtered.filter.bool.should = opts.should
      else
        qry.query.filtered.filter.bool.should ?= []
        qry.query.filtered.filter.bool.should.push(sr) for sr in opts.should
      delete opts.should
    if opts.all?
      qry.size = 1000000 # just a simple way to try to get "all" records - although passing size would be a better solution, and works anyway
      delete opts.all
    if opts.terms?
      try opts.terms = opts.terms.split(',')
      qry.facets ?= {}
      for tm in opts.terms
        qry.facets[tm] = { terms: { field: tm, size: 1000 } }
      delete opts.terms
    for af in ['facets','aggs','aggregations']
      if opts[af]?
        qry[af] ?= {}
        qry[af][f] = opts[af][f] for f of opts[af]
        delete opts[af]
    qry[k] = v for k, v of opts
  # no filter query or no main query can cause issues on some queries especially if certain aggs/terms are present, so insert some default searches if necessary
  qry.query.filtered.query = { match_all: {} } if typeof qry is 'object' and qry.query?.filtered?.query? and _.isEmpty(qry.query.filtered.query)
  #qry.query.filtered.query.bool.must = [{"match_all":{}}] if typeof qry is 'object' and qry.query?.filtered?.query?.bool?.must? and qry.query.filtered.query.bool.must.length is 0 and not qry.query.filtered.query.bool.must_not? and not qry.query.filtered.query.bool.should and (qry.aggregations? or qry.aggs? or qry.facets?)
  console.log('Returning translated query',JSON.stringify(qry)) if API.settings.log?.level is 'all'
  # clean slashes out of query strings
  if qry.query?.filtered?.query?.bool?
    for bm of qry.query.filtered.query.bool
      for b of qry.query.filtered.query.bool[bm]
        if typeof qry.query.filtered.query.bool[bm][b].query_string?.query is 'string' and qry.query.filtered.query.bool[bm][b].query_string.query.indexOf('/') isnt -1
          qry.query.filtered.query.bool[bm][b].query_string.query = qry.query.filtered.query.bool[bm][b].query_string.query.replace(/\//g,'\\/')
  if qry.query?.filtered?.filter?.bool?
    for fm of qry.query.filtered.filter.bool
      for f of qry.query.filtered.filter.bool[fm]
        if qry.query.filtered.filter.bool[fm][f].query_string?.query? and qry.query.filtered.filter.bool[fm][f].query_string.query.indexOf('/') isnt -1
          qry.query.filtered.filter.bool[fm][f].query_string.query = qry.query.filtered.filter.bool[fm][f].query_string.query.replace(/\//g,'\\/')
  delete qry._source if qry._source? and qry.fields?
  return qry

API.collection.dot = (obj, key, value, del) ->
  if typeof key is 'string'
    return API.collection.dot obj, key.split('.'), value, del
  else if key.length is 1 and (value? or del?)
    if del is true or value is '$DELETE'
      if obj instanceof Array
        obj.splice key[0], 1
      else
        delete obj[key[0]]
      return true
    else
      obj[key[0]] = value # TODO see below re. should this allow writing into multiple sub-objects of a list?
      return true
  else if key.length is 0
    return obj
  else
    if not obj[key[0]]?
      if false
        # check in case obj is a list of objects, and key[0] exists in those objects
        # if so, return a list of those values.
        # Keep order of the list? e.g for objects not containing the key, output undefined in the list space where value would have gone?
        # and can this recurse further? If the recovered items are lists or objecst themselves, go further into them?
        # if so, how would that be represented?
        # and is it possible for this to work at all with value assignment?
      else if value?
        obj[key[0]] = if isNaN(parseInt(key[0])) then {} else []
        return API.collection.dot obj[key[0]], key.slice(1), value, del
      else
        return undefined
    else
      return API.collection.dot obj[key[0]], key.slice(1), value, del

