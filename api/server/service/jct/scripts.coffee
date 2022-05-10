
'''

API.add 'service/jct/scripts/institutions', 
  get: () ->
    size = 500
    q = {query: {filtered: {query: {}, filter: {bool: {should: [
      {term: {'snaks.property.exact':'P6782'}} # ROR ID
    ]}}}}, size: size, _source: {includes: ['id','label','description','snaks.property','snaks.value','snaks.qid','sitelinks.enwiki.title']}}
    q.query.filtered.query.match_all = {}
    counter = 0
    from = 0
    total = false
    batch = []
    jct_institution.remove '*'
    while total is false or from < total
      q.from = from
      res = wikidata_record.search q # convert this to a direct search of wikidata API, unless changing to maintain wikidata index or switching to ROR
      if total is false
        total = res?.hits?.total ? 0
        console.log total
      for r in res?.hits?.hits ? []
        rec = title: r._source.label, values: [], wid: r._source.id
        rec.alternate = r._source.sitelinks.enwiki.title if r._source.sitelinks?.enwiki?.title and r._source.sitelinks.enwiki.title isnt rec.title
        rec.description = r._source.description if r._source.description and r._source.description isnt rec.title
        for s in r._source.snaks
          isno = false
          try isno = s.value and not isNaN parseInt s.value
          if typeof s.value is 'string' and s.value and s.value.substring(0,1) not in ["0","1","2","3","4","5","6","7","8","9"] and not s.value.startsWith('/') and not s.value.startsWith('grid.') and not s.value.startsWith('http') and not isno and s.value not in rec.values
            # collect useful values to string match against for suggestions
            rec.values.push s.value
          rec.id ?= s.value if s.property is 'P6782'
          if not rec.country and s.property is 'P17' and cwd = wikidata_record.get s.qid
            rec.country = cwd.label
        rec._id = rec.id
        delete rec.values if not rec.values.length
        console.log(rec) if rec._id is '01js4x705'
        batch.push rec
        counter += 1
      if batch.length > 2000
        jct_institution.insert batch
        batch = []
      from += size
      console.log from, counter, total
    if batch.length
      jct_institution.insert batch
    return counter



import Future from 'fibers/future'

# ones that really do not seem to exist in crossref with an issn
# archive of formal proofs is not a journal and does not appear in crossref, although does have issn 2150-914x
# achemenet
# plenum - looks like only books
# duodecim - Finnish medical guides publisher (not journals)
# ferrata storti foundation (not in italian either)
# gordon and breach science publishers are part of taylor & francis (as are a few others, but they are found anyway)
# carfax publishing (old one owned by T&F)
# birkhauser (part of de gruyter) (which is part of springer?)
# reidel part of springer
# dietrich steinkopff springer
# EMBO part of nature
# Gates Foundation could be Gates Open Research which is actaully F1000 Research
# TU Braunschweig - not clear that it actually publishes any journals itself
# discrete mathematics and theoretical computer science exists and has issn 1462-7264 but is not in crossref
# EUROPEAN GEOSCIENCES UNION part of copernicus
# european language resources association is part of springer
# frank cass part of T&F
# IFAC secretariat does not appear to have journals with ISSNs and is not in crossref
# Masson is part of elsevier (published as elsevier masson and just masson?)
# society for leukocyte biology is part of wiley
# the lancet is part of elsevier
# lawrence erlbaum is part of informa / t&f
# osa publishing is also optical society of america
# AIDIC has issn 2283-9216 as chemical engineering transactions but does not appear to be in crossref
# public knowledge project may publish something but can't find publisher name and they are open anyway (makes OJS)
# Society of Photo-Optical Instrumentation Engineers same as SPIE
# US Department of Health and Human Services does not publish journals
# dagstuhl publishing is a journal publisher but all OA


_jct_review_result = false
API.add 'service/jct/scripts/review', 
  get: () -> 
    if _jct_review_result and not this.queryParams.refresh
      return _jct_review_result

    _clean = (publisher) ->
      publisher = publisher.toLowerCase()
      publisher = 'spie' if publisher.indexOf('s p i e') isnt -1
      publisher = 'mdpi' if publisher.indexOf('mdpi') isnt -1 # catch this in the brackets before splitting at brackets
      publisher = 'inter-research' if publisher.indexOf('inter-research') isnt -1
      publisher = 'schweizerbart' if publisher.indexOf('schweizerbart') isnt -1
      publisher = 'universität graz' if publisher.indexOf('universität graz') isnt -1 or publisher.indexOf('universitat graz') isnt -1
      publisher = 'microbiology society' if publisher.indexOf('society') isnt -1 and publisher.indexOf('microbiology') isnt -1
      publisher = 'society of petroleum engineers' if publisher.indexOf('SPE') isnt -1
      publisher = 'italian physical society' if publisher.indexOf('Società Italiana di Fisica') isnt -1
      if publisher.indexOf('(') isnt -1
        pts = publisher.split '('
        publisher = if pts[1].trim().indexOf(' ') isnt -1 and pts[0].indexOf('palgrave') is -1 then pts[1].trim() else pts[0].trim()
      if publisher.indexOf('[') isnt -1
        publisher = publisher.split('[')[0].trim()
      publisher = publisher.replace('kexue chubaneshe','')
      publisher = publisher.replace(/[\-\/]/g,' ').replace(/[^a-z0-9 ]/g,'').replace(/  +/g,' ').trim()
      publisher = publisher.replace('optical society of america','optical society')
      if publisher is 'who'
        pc = 'world health organization'
      else if publisher.indexOf('akademie') isnt -1 and publisher.indexOf('wissenschaften')
        pc = 'akademie wissenschaften'
      else if publisher.indexOf('jagiellonian') isnt -1
        pc = 'jagiellonian'
      else if publisher.indexOf('international water association') isnt -1
        pc = 'iwa publishing'
      else if publisher.indexOf('american heart') isnt -1
        pc = 'american heart' # appears to come out as part of wolters kluwer, but does still state american heart association in publisher name
      else if publisher.indexOf('american phytopathological society') isnt -1
        pc = 'scientific societies'
      else if publisher.indexOf('american society') isnt -1 and publisher.indexOf('nutrition') isnt -1
        pc = 'american society nutrition' # publisher name appears to be american society for nutrition, and may be part of OUP 
      else if publisher.indexOf('planck') isnt -1
        pc = 'planck demographic' # so far only the demographic research one is in the list
      else if publisher.indexOf('beilstein') isnt -1
        pc = 'beilstein'
      else if publisher.indexOf('bmj') is 0
        pc = 'bmj'
      else if publisher.indexOf('brill') is 0
        pc = 'brill'
      else if publisher.indexOf('ceur') is 0
        pc = 'samara national research university' # has issn 1613-0073
      else if publisher.indexOf('csic') isnt -1
        pc = 'csic'
      else if publisher.indexOf('institute of physics') isnt -1
        pc = 'iop publishing'
      else if publisher.indexOf('oldenbourg') isnt -1
        pc = 'oldenbourg' # part of de gruyter too
      else if publisher.indexOf('masson') isnt -1
        pc = 'masson' # is part of elsevier too
      else if publisher.indexOf('gruyter') isnt -1
        pc = 'gruyter' # part of de gruyter too
      else if publisher.indexOf('nauka') isnt -1
        pc = 'nauka'
      else if publisher.indexOf('sissa') isnt -1
        pc = 'sissa'
      else if publisher.indexOf('lippencott') isnt -1 or publisher.indexOf('lippincott') isnt -1
        pc = 'lippincott'
      else if publisher.indexOf('south african') isnt -1 and publisher.indexOf('medical') isnt -1
        pc = 'health medical publishing'
      else if publisher.indexOf('international society') isnt -1 and publisher.indexOf('global health') isnt -1
        pc = 'edinburgh university global health society'
      else if publisher.indexOf('springer nature') isnt -1
        pc = 'springer nature'
      else if publisher.indexOf('springer') isnt -1
        pc = 'springer'
      else
        pc = ''
        for pr in publisher.split ' '
          if pr.length > 1 and pr not in ['proceedings', 'corporation', 'publishers', 'limited', 'verlag', 'group', 'gmbh', 'for', 'and', 'doo', 'ltd', 'pub', 'inc', 'zrt', 'the', 'of', 'bv', 'ag', 'co', 'kg']
            pc += ' ' if pc isnt ''
            pc += pr
      return pc

    pubs = API.service.jct._publishers
    res = {total: 0, dois: 0, publishers: 0, journals: 0, open: 0, missing: [], results: [], q: []}
    for pub in pubs
      res.total += 1
      #break if res.total > 5
      q = _clean pub
      res.q.push q
      qr = 'src:crossref AND issn:*'
      for word in q.split ' '
        qr += ' AND publisher:' + word + '*'
      console.log res.total #+ ', ' + qr
      r = academic_journal.search qr, 10000
      rs = {pub: pub, q: q, name: undefined, dois: 0, journals: 0, journal: [], hits: r.hits.total}
      for j in r?.hits?.hits ? []
        pb = _clean j._source.publisher
        #console.log q, pb
        # wiley blackwell can show up as wiley, wiley-blackwell, blackwell publishing, etc
        if (q.indexOf(pb) isnt -1 and q.length <= (pb.length*1.1)) or pb.indexOf('polska akademia') isnt -1 or (q.indexOf('wiley') isnt -1 and (pb.indexOf('wiley') isnt -1 or pb.indexOf('blackwell') isnt -1))
          rs.name ?= j._source.publisher
          rs.dois += j._source.counts['total-dois'] if j._source.counts?
          rs.journals += 1
          rs.journal.push j._source.title
          rs.open = true if 'doaj' in j._source.src
      if rs.name?
        res.results.push rs
        res.dois += rs.dois
        res.journals += rs.journals
        res.publishers += 1
        res.open += 1 if rs.open
      else
        res.missing.push pub
    delete res.q #res.results
    delete res.missing
    _jct_review_result = res
    return res



API.add 'service/jct/scripts/trial', 
  get:
    roleRequired: if API.settings.dev then undefined else 'root'
    action: () -> 
      q = this.queryParams.q ? 'publisher:"wiley"'
      delay = this.queryParams.delay ? 20
      size = this.queryParams.size ? 500
      from = this.queryParams.from ? 0
      cf = this.queryParams.cf ? true
      verbose = this.queryParams.verbose ? false
      refresh = this.queryParams.refresh

      target = false
      results = []
      compliant = 0
      fails = 0

      _get = (issn) ->
        _dget = (issn) ->
          try
            cr = HTTP.call 'GET', 'https://' + (if cf then 'api.journalcheckertool.org' else 'api.cottagelabs.com/service/jct') + '/calculate?issn=' + issn + (if refresh then '&refresh=true' else '')
            cm = if typeof cr.content is 'string' then JSON.parse(cr.content) else cr.content
            results.push if verbose then cr else cm.compliant
            compliant += 1 if cm.compliant is true
          catch
            fails += 1
          console.log results.length, fails
        if typeof issn is 'string' and issn
          Meteor.setTimeout (() -> _dget issn), 1
        else
          fails += 1

      _trial = () ->
        started = Date.now()
        pbs = academic_journal.search q, {size: size, from: from}
        if target is false
          target = pbs?.hits?.total ? 0
          target = size if size < target
        for h in pbs?.hits?.hits ? []
          future = new Future()
          Meteor.setTimeout (() -> future.return()), delay
          future.wait()
          try
            rec = h._source
            if rec.issn? and rec.issn.length
              anissn = if typeof rec.issn is 'string' then rec.issn else rec.issn[0]
              _get anissn
            else
              fails += 1
          catch
            fails += 1

        while target is false or target > (results.length + fails)
          future = new Future()
          Meteor.setTimeout (() -> future.return()), 500
          future.wait()

        ended = Date.now()
        console.log 'JCT trial done'
        
        API.mail.send
          from: 'alert@cottagelabs.com'
          to: 'alert@cottagelabs.com'
          subject: 'JCT trial complete'
          text: 'Got ' + results.length + ' results (' + compliant + ' compliant) out of ' + target + ' with ' + delay + 'ms delay, in ' + (ended-started) + 'ms. \n\n' + JSON.stringify results
        
      Meteor.setTimeout _trial, 1
      return true

'''