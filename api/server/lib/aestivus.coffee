
import connect from 'connect'
import connectRoute from 'connect-route'
import bodyParser from 'body-parser'
import Fiber from 'fibers'

@JsonRoutes = {}

#WebApp.connectHandlers.use connect.urlencoded({limit: '1024mb'})
#WebApp.connectHandlers.use connect.query()
WebApp.connectHandlers.use bodyParser.json({limit: '4mb', type: ['application/json', 'text/plain', 'application/*+json']})

JsonRoutes.Middleware = JsonRoutes.middleWare = connect()
WebApp.connectHandlers.use JsonRoutes.Middleware

JsonRoutes.routes = []
@connectRouter
connectRouter = @connectRouter

WebApp.connectHandlers.use Meteor.bindEnvironment(connectRoute(( (router) -> connectRouter = router )))

# Error middleware must be added last, to catch errors from prior middleware.
# That's why we cache them and then add after startup.
errorMiddlewares = []
JsonRoutes.ErrorMiddleware =
  use: () ->
    errorMiddlewares.push arguments

Meteor.startup () ->
  _.each errorMiddlewares, ((errorMiddleware) ->
    errorMiddleware = _.map errorMiddleware, ((maybeFn) ->
      if _.isFunction maybeFn
        return (a, b, c, d) ->
          Meteor.bindEnvironment(maybeFn)(a, b, c, d);
      return maybeFn;
    )
    WebApp.connectHandlers.use.apply(WebApp.connectHandlers, errorMiddleware);
  )
  errorMiddlewares = []

JsonRoutes.add = (method, path, handler) ->
  path = '/' + path if path[0] isnt '/'
  JsonRoutes.routes.push {method: method, path: path}

  connectRouter[method.toLowerCase()] path, ((req, res, next) ->
    setHeaders res, responseHeaders
    Fiber(() ->
      try
        handler req, res, next
      catch error
        next error
    ).run()
  )

responseHeaders = {} #'Cache-Control': 'no-store', Pragma: 'no-cache'

JsonRoutes.setResponseHeaders = (headers) ->
  responseHeaders = headers

setHeaders = (res, headers) ->
  _.each headers, ((value, key) -> res.setHeader key, value )

ironRouterSendErrorToResponse = (err, req, res) ->
  res.statusCode = 500 if res.statusCode < 400
  res.statusCode = err.status if err.status
  msg = if (process.env.NODE_ENV ?= 'development') is 'development' then (err.stack || err.toString()) + '\n' else 'Server error.'
  console.error err.stack or err.toString()

  return req.socket.destroy() if res.headersSent

  res.setHeader 'Content-Type', 'text/html'
  res.setHeader 'Content-Length', Buffer.byteLength(msg)
  return res.end() if req.method is 'HEAD'

  res.end msg
  return




class share.Route

  constructor: (@api, @path, @options, @endpoints) ->
    # Check if options were provided
    if not @endpoints
      @endpoints = @options
      @options = {}

  addToApi: do ->
    availableMethods = ['head', 'get', 'post', 'put', 'patch', 'delete', 'options']

    return ->
      self = this

      # Throw an error if a route has already been added at this path
      # TODO: Check for collisions with paths that follow same pattern with different parameter names
      if _.contains @api._config.paths, @path
        throw new Error "Cannot add a route at an existing path: #{@path}"

      # Override the default OPTIONS endpoint with our own
      @endpoints = _.extend options: @api._config.defaultOptionsEndpoint, @endpoints
      @endpoints = _.extend head: @api._config.defaultHeadEndpoint, @endpoints

      @_resolveEndpoints()

      # Add to our list of existing paths
      @api._config.paths.push @path

      allowedMethods = _.filter availableMethods, (method) ->
        _.contains(_.keys(self.endpoints), method)
      rejectedMethods = _.reject availableMethods, (method) ->
        _.contains(_.keys(self.endpoints), method)

      # Setup endpoints on route
      fullPath = @api._config.apiPath + @path
      _.each allowedMethods, (method) ->
        self.endpoints[method] = self.endpoints[self.endpoints[method]] if typeof self.endpoints[method] is 'string'
        endpoint = self.endpoints[method]
        @JsonRoutes.add method, fullPath, (req, res) ->
          try
            rq = _.clone req.query
            try
              for q of rq
                try
                  if rq[q] is 'undefined'
                    rq[q] = undefined
                  else if rq[q] is 'true'
                    rq[q] = true
                  else if rq[q] is 'false'
                    rq[q] = false
                  else if typeof rq[q] is 'string' and rq[q].replace(/[0-9]/g,'').length is 0 and (rq[q] is '0' or not rq[q].startsWith('0'))
                    try
                      pn = parseInt rq[q]
                      rq[q] = pn if not isNaN pn
          catch
            rq = req.query
            
          endpointContext =
            urlParams: req.params
            queryParams: rq
            bodyParams: req.body
            request: req
            response: res
          # Add endpoint config options to context
          _.extend endpointContext, endpoint

          # Run the requested endpoint
          responseData = null
          try
            responseData = endpoint.action.call endpointContext
            if (responseData is null or responseData is undefined)
              responseData = 404
          catch error
            # Do exactly what Iron Router would have done, to avoid changing the API
            ironRouterSendErrorToResponse(error, req, res);
            return

          # Generate and return the http response, handling the different endpoint response types
          if responseData.body? and (responseData.statusCode or typeof responseData.status is 'number' or responseData.headers)
            self._respond res, responseData.body, (responseData.statusCode ? responseData.status), responseData.headers
          else if not res.headersSent
            self._respond res, responseData
      _.each rejectedMethods, (method) ->
        @JsonRoutes.add method, fullPath, (req, res) ->
          responseData = status: 'error', message: 'API endpoint does not exist'
          headers = 'Allow': allowedMethods.join(', ').toUpperCase()
          self._respond res, responseData, 405, headers


  ###
    Convert all endpoints on the given route into our expected endpoint object if it is a bare
    function

    @param {Route} route The route the endpoints belong to
  ###
  _resolveEndpoints: ->
    _.each @endpoints, (endpoint, method, endpoints) ->
      if _.isFunction(endpoint)
        endpoints[method] = {action: endpoint}
    return


  ###
    Respond to an HTTP request
  ###
  _respond: (response, body, statusCode=200, headers={}) ->
    # Override any default headers that have been provided (keys are normalized to be case insensitive)
    # TODO: Consider only lowercasing the header keys we need normalized, like Content-Type
    defaultHeaders = @_lowerCaseKeys @api._config.defaultHeaders
    headers = @_lowerCaseKeys headers
    headers = _.extend defaultHeaders, headers

    # Prepare JSON body for response when Content-Type indicates JSON type
    if headers['content-type'].match(/json|javascript/) isnt null
      if @api._config.prettyJson
        body = JSON.stringify body, undefined, 2
      else
        body = JSON.stringify body

    # Send response
    sendResponse = ->
      response.writeHead statusCode, headers
      response.end body
    sendResponse()

  ###
    Return the object with all of the keys converted to lowercase
  ###
  _lowerCaseKeys: (object) ->
    _.chain object
    .pairs()
    .map (attr) ->
      [attr[0].toLowerCase(), attr[1]]
    .object()
    .value()



class @Restivus

  constructor: (options) ->
    @_routes = []
    @_config =
      paths: []
      apiPath: 'api/'
      prettyJson: false
      defaultHeaders:
        'Content-Type': 'application/json'
      enableCors: true

    # Configure API with the given options
    _.extend @_config, options

    if @_config.enableCors
      corsHeaders =
        'Access-Control-Allow-Methods': 'HEAD, GET, PUT, POST, DELETE, OPTIONS'
        'Access-Control-Allow-Origin': '*'
        'Access-Control-Allow-Headers': 'X-apikey, X-id, Origin, X-Requested-With, Content-Type, Content-Disposition, Accept, DNT, Keep-Alive, User-Agent, If-Modified-Since, Cache-Control'

      # Set default header to enable CORS if configured
      _.extend @_config.defaultHeaders, corsHeaders

      if not @_config.defaultOptionsEndpoint
        @_config.defaultOptionsEndpoint = ->
          @response.writeHead 200, corsHeaders
          @response.end()

    if not @_config.defaultHeadEndpoint
      hdrs = @_config.defaultHeaders
      @_config.defaultHeadEndpoint = ->
        @response.writeHead 200, hdrs
        @response.end()

    # Normalize the API path
    if @_config.apiPath[0] is '/'
      @_config.apiPath = @_config.apiPath.slice 1
    if _.last(@_config.apiPath) isnt '/'
      @_config.apiPath = @_config.apiPath + '/'

    return this


  add: (path, options, endpoints) ->
    if typeof options is 'function'
      f = action: options
      options = get: f, post: f

    route = new share.Route(this, path, options, endpoints)
    @_routes.push(route)
    route.addToApi()

    return this


