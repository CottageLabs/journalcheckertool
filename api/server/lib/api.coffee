
@API = new Restivus
  defaultHeaders: { 'Content-Type': 'application/json; charset=utf-8' },
  prettyJson: true

API.settings = Meteor.settings

API.add '/',
  get: () ->
    return
      time: Date.now()
      name: 'JCT API'





