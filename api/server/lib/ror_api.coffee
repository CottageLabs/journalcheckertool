jct_institution = new API.collection {index:"jct", type:"institution"}

_ror_api_import = () ->
# Import institution from API
# This is limited to getting just the first 10,000
# So using the bulk data dump

# get everything from RoR
  removed = false
  total = 0
  total_number_of_pages = 0
  counter = 1
  size_per_page = 20

  batch = []
  while total_number_of_pages is 0 or counter < total_number_of_pages
    if batch.length >= 10000 or (removed and batch.length >= 5000)
      if not removed
# makes a shorter period of lack of records to query
# there will still be a period of 5 to 10 minutes where not all institutions will be present
# but, since imports only occur once week depending on settings, and
# responses should be cached at cloudflare anyway, this should not affect anyone as long as
# imports are not often run during UK/US business hours
        jct_institution.remove '*'
        console.log 'Removing old institution records'
        future = new Future()
        Meteor.setTimeout (() -> future.return()), 10000
        future.wait()
        removed = true
      console.log 'Importing RoR page ' + counter
      jct_institution.insert batch
      batch = []
    try
      url = 'https://api.ror.org/organizations?page=' + counter
      console.log 'getting from ror ' + url
      res = HTTP.call 'GET', url, {headers: {'User-Agent': 'Journal Checker Tool; mailto: jct@cottagelabs.zendesk.com'}}
      # console.log(JSON.stringify(res.data))
      if total is 0
        total = res.data['number_of_results']
        mod = total % size_per_page
        q =  (total - mod) / size_per_page
        if mod > 0
          q = q + 1
        total_number_of_pages = q
      if res.data.items? and res.data.items.length > 0
        for rec in res.data.items
          ror = rec.id
          id = ror.replace("https://ror.org/", '')
          rec.id = id
          rec.ror = id
          rec.ror_id = ror
          batch.push rec
      counter += 1
    catch err
      future = new Future()
      Meteor.setTimeout (() -> future.return()), 2000 # wait 2s on probable crossref downtime
      future.wait()

  if batch.length
    jct_institution.insert batch
    batch = []