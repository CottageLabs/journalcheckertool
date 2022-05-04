---
title: "Public API docs"
date: 2021-01-03T15:39:00Z
description: "Documentation of the public API for the Journal Checker Tool: Plan S Compliance Validator."
---

<style type="text/css">
table {
    border: 1px solid #cccccc;
}

thead {
    font-weight: bold;
}

td, th {
    border: 1px solid #cccccc;
    padding: 5px;
}
</style>

# JCT Public API

The api is available at [{{< param apidocs.ApiURL >}}]({{< param apidocs.ApiURL >}}).

## Request a compliance calculation

To carry out a compliance calculation, you can make an HTTP GET request, as detailed below.

```bash
GET /calculate?issn=[issn]&funder=[funder]&ror=[ror]
```

The server will execute the algorithm, and gather responses for all routes 
before responding to the request.

The parameters you can pass to the `/calculate` endpoint are as follows:

* **issn** - either the print or online ISSN of the journal you wish to check. *required*
* **funder** - the JCT ID for the funder that you wish to check.  Allowable Funder IDs are listed [here](/funder-ids). *required*
* **ror** - the ROR ID of the organisation that you wish to check.  See [https://ror.org](https://ror.org/) for more information. *optional*

The `issn` field is the only *required* field, though without the `ror` and `funder` fields your results will
be partial, and may not give you complete and accurate information.  

If you enter an invalid `funder`, the API will respond with a `400 (Bad Request)`

The `ror` field is optional, and is equivalent to selecting "Not affiliated" via the User Interface.

Examples:
* PLoS One, Wellcome Trust, University of Oxford: [{{< param apidocs.ApiURL >}}calculate?issn=1932-6203&funder=wellcome&ror=052gg0110]({{< param apidocs.ApiURL >}}calculate?issn=1932-6203&funder=wellcome&ror=052gg0110).
* Nature Medicine, Academy of Finland, no institution: [{{< param apidocs.ApiURL >}}calculate?issn=1078-8956&funder=academyoffinlandaka&not_he=true]({{< param apidocs.ApiURL >}}calculate?issn=1078-8956&funder=academyoffinlandaka&not_he=true)

### Overall response format

```json
{
  "request" : {
    "started" : "<(int) start timestamp of the request>",
    "ended" : "<(int) end timestamp of the request>",
    "took" : "<(int) the time in ms between request start and end (on the server, not including travel time)>",
    "journal" : [
      {
        "id": "<journal issn>", 
        "title": "<journal title>", 
        "issn" : ["<all of the matching ISSNs for this journal>"],
        "publisher" : "<journal publisher>"
      }
    ],
    "funder" : [
      {"id": "<funder ID>", "title": "<funder title>"}
    ],
    "institution" : [
      {"id": "<institution ROR>", "title": "<institution name>"}
    ],
    "checks": ["<list of routes calculated, (see Route IDs below)>"]
  },
  "compliant" : "<(bool) true|false if there is at least one compliant card in the list of cards to show the user>",
  "results" : [
    {"<route response objects as per the below>": ""}
  ],
  "cards" : [
    {"<cards to be displayed as per the below>" :  ""}
  ]
}
```

### Per-Route response data

For each route, there is a general response format:

```json
{
  "route" : "<the ID of the route (see Route IDs below)>",
  "compliant" : "<the Compliance ID for this route result (see below)",
  "qualifications" : [
    {"<qualification id> (see below)" : { "<qualification specific data (if needed)>" : "" }}
  ],
  "issn" : ["<the ISSN checked for this result, if there is one>"],
  "funder" : "<the funder checked on this result, if there is one>",
  "ror" : "the ROR relevant to this result, if there is one>",
  "log" : [
    {
      "code" : "<algorithm transition code (see below)>",
      "parameters" : {
        "<parameter name>" : ["<parameter value>"]
      }
    }
  ]
}
```

#### Route IDs

* `fully_oa` - Fully OA route
* `self_archiving` - Self Archiving route
* `ta` - Transformative Agreement route
* `tj` - Transformative Journal route
* `hybrid` - Hybrid Journal route

#### Compliance IDs

* `yes` - Route offers compliance
* `no` - Route does not offer compliance
* `unknown` - Not known if route offers compliance

#### Qualification IDs

* `doaj_under_review` - the journal is in the DOAJ's "in progress" or "under review" list, not the public DOAJ
    * no qualification specific data required
* `rights_retention_author_advice` - the journal does not have a self-archiving (SA) policy and does not appear in the rights retention data source
    * no qualification specific data required
* `corresponding_authors` - the transformative agreement (TA) is only open to corresponding authors
    * no qualification specific data required
  
#### Log

The log provides a list of decisions made by the algorithm, in order of traversal.  This allows you to 
see the path through the algorithm that was taken to reach each decision, along with any relevant parameters.

See the table below for a full list of decisions, their meanings, and the parameters that may be associated.

For example, items such as this may be present:

```json
{
  "log" : [
    { "code" : "FullOA.InDOAJ" },
    { 
      "code" : "FullOA.Compliant",
      "parameters" : {
        "licence" : ["CC BY", "CC-BY-SA"]
      }
    } 
  ]
}
```

##### Full OA Route Codes

| Code | Meaning | Property | Property Value |
| ---- | ------- | -------- | -------------- |
| FullOA.NotInDOAJ | Journal not found in DOAJ | | |
| FullOA.InProgressDOAJ | Journal application found in DOAJ | | |
| FullOA.NotInProgressDOAJ | No application found in DOAJ | | |
| FullOA.InDOAJ | Journal found in DOAJ | | |
| FullOA.Compliant | Journal properties are compliant | licence | List of Journal licences |
| FullOA.Unknown | Journal properties are unclear | missing | List of missing properties |
| FullOA.NonCompliant | Journal properties are non-compliant | license | List of Journal licences |

##### Self-Archiving Route Codes

| Code | Meaning | Property | Property Value |
| ---- | ------- | -------- | -------------- |
| SA.RRException | Journal was found in JCT's list of journals which explicitly do not permit the Rights Retention strategy | | |
| SA.RRNoException | The Journal was *not* found in JCT's list of journals which explicitly do not permit the Rights Retention strategy | | |
| SA.InOAB | Journal was found in Open Access Button (OAB) | | |
| SA.NotInOAB | Journal was not found in OAB | | |
| SA.OABNonCompliant | The record in OAB did not comply with the funder's requirements | licence | List of allowed SA licenses |
| | | embargo | Embargo length (list of length 1) |
| | | version | List of allowed SA versions |
| SA.OABIncomplete | Some data was missing from the OAB record, no determination could be made | missing | List of missing properties |
| SA.OABCompliant | The record in OAB complied with the funder's requirements | licence | List of allowed SA licences |
| | | embargo | Embargo length (list of length 1) |
| | | version | List of allowed SA versions |
| SA.FunderRRNotActive | Funder has not adopted the Rights Retention strategy | | |
| SA.FunderRRActive | Funder has adopted the Rights Retention strategy | | |
| SA.Unknown | Self-Archiving status could not be determined | | |
| SA.NonCompliant | Self-Archiving is not possible under current circumstances | | |
| SA.Compliant | Self-Archiving is permitted via Rights Retention | | |

##### Transformative Agreement Route Codes

| Code | Meaning | Property | Property Value |
| ---- | ------- | -------- | -------------- |
| TA.NoTA | No TA was found that matched the query parameters | | |
| TA.Exists | A TA was found that matched the query parameters | | |
| TA.NotActive | The TA that was found is not currently applicable | | |
| TA.Active | The TA that was found is currently applicable | | |
| TA.Unknown | It was not clear if the parameters of the TA meet the funder's criteria | | |
| TA.NonCompliant | The parameters of the TA do not meet the funder's criteria | | |
| TA.Compliant | The TA is compliant with the funder's requirements | | |

##### Transformative Journals Route Codes

| Code | Meaning | Property | Property Value |
| ---- | ------- | -------- | -------------- |
| TJ.NoTJ | The Journal was not registered as a TJ | | |
| TJ.Exists | The Journal is registered as a TJ | | |
| TJ.NonCompliant | The parameters of the TJ do not meet the funder's criteria | | |
| TJ.Compliant | The TJ is compliant with the funder's requirements | | |


##### Hybrid Journals Route Codes

| Code | Meaning | Property | Property Value |
| ---- | ------- | -------- | -------------- |
| Hybrid.NotInOAW | The Journal was not registered in OA.Works | | |
| Hybrid.InOAW | The Journal was registered in OA.Works | | |
| Hybrid.NonCompliant | The properites of the hybrid journal do not meet the funder's requirements | licence | List of allowed hybrid licences |
| Hybrid.Unknown | There was not sufficient information to determine if the hybrid journal meets the funder's requirements | missing | List of properties missing |
| Hybrid.Compliant | The properties of the hybrid journal are compliant with the funder's requirements | licence | List of allowed publishing licences |


### Cards to show the user

The list of cards in the `cards` section of the response defines those particular routes to compliance
which the funder wants the user to be made aware of.  Cards are shown based on the compliance routes
in the `results` section of the API response, and only cards which should be shown to the user will
be listed.  The content of the `cards` section of the response
contains the full definitions of each card, which you can display to the user using the language
files provided for that funder (see below).

```json
{
  "id": "[card_id]",
  "match_routes": {
    "must": [
      "[route_id]"
    ],
    "or": [
      "[route_id]",
      "[route_id]"
    ],
    "not": [
      "[route_id]"
    ]
  },
  "match_qualifications": {
    "must": [
      "[route_id].[qualification_id]"
    ],
    "or": [
      "[route_id].[qualification_id]",
      "[route_id].[qualification_id]"
    ],
    "not": [
      "[route_id].[qualification_id]"
    ]
  },
  "preferred": "true|false",
  "compliant": "true|false",
  "display_if_compliant": [
    "[route_id]",
    "[route_id]"
  ],
  "modal": "[modal_id]"
}
```

* `cards[].id` - a unique id for the card, an arbitrary string, but which will be used to identify the
  card throughout the language files
* `cards[].match_routes` - match rules for compliant routes to determine whether or not to show this card
  * `must` - all routes listed must be compliant
  * `or` - at least one of the routes listed must be compliant
  * `not` - none of the routes listed may be compliant
* `cards[].match_qualifications` - match rules for qualifications present in calculated routes
  * `must` - all qualifications listed must be present
  * `or` - at least one of the qualifications listed must be present
  * `not` - none of the qualifications listed may be present
* `cards[].preferred` - the card represents a preferred route to compliance by the funder
* `cards[].compliant` - the card represents a route to compliance, and the presence of at least one in the results will trigger
  the compliant style in the front end.
* `cards[].display_if_compliant` - the list of routes, in order, to display information about whether or not they are compliant.  If you leave
  this blank then no route-specific guidance will be displayed, but the `default` text for the card will be displayed anyway, so
  you only need to use this option if the card could display information about multiple routes, and you wish to control which
  information is displayed depending on which routes are compliant
* `cards[].modal` - the modal to bind to the card's overall modal (other modals can be specified inline in the card text as normal)


## Funder Specific Configurations and Language

Each funder in JCT may specify custom language for how the compliance information should be
interpreted and displayed to end users.  This information is optimised for use in the JCT user interface.
Nonetheless it is also available via the API for use by any downstream systems.  

```bash
GET /funder_language/<funder id>
```

The response is a JSON document which contains all of the language used by the JCT front end, which covers:
* General site text specific to the funder
* Text for all API log codes
* Content for all compliance cards
* Any modals attached to any part of the information

Examples:
* Wellcome Trust: [{{< param apidocs.ApiURL >}}funder_language/wellcome]({{< param apidocs.ApiURL >}}funder_language/wellcome)
* UKRI: [{{< param apidocs.ApiURL >}}funder_language/unitedkingdomresearchinnovationukri]({{< param apidocs.ApiURL >}}funder_language/unitedkingdomresearchinnovationukri)

## Transformative Journals

Determine if a journal is a transformative journal, using the issn:

```bash
GET /tj/{issn}
```

Response format:

```json
{
  "issn" : "<issn requested>",
  "transformative_journal" : true
}
```

OR `404` if record not found

Examples:
* PLoS One (not a Transformative Journal): [{{< param apidocs.ApiURL >}}tj/1932-6203]({{< param apidocs.ApiURL >}}tj/1932-6203)
* Journal of Cell Science (a Transformative Journal): [{{< param apidocs.ApiURL >}}tj/0021-9533]({{< param apidocs.ApiURL >}}tj/0021-9533)

## Transformative Agreements

```bash
GET /ta?issn={issn}&ror={ror}
```

Response format:

```json
{
  "issn" : ["<issn in the TA>"],
  "ror" : "<ror in the TA>",
  "result" : {
    "compliant": "<yes|no|unknown>",
    "qualifications": [
      {
        "<qualification id>": {
          "<qualification specific data (if needed)>": ""
        }
      }
    ],
    "log": [
      {
        "action": "<description of the action (see above for details.)>",
        "result": "<the outcome of the action (optional, depending on circumstance)>"
      }
    ]
  }
}
```

OR `404` if no TA exists for that combination.

Examples:
* PLoS One, Oxford (No such TA exists): [{{< param apidocs.ApiURL >}}ta?issn=1932-6203&ror=052gg0110]({{< param apidocs.ApiURL >}}ta?issn=1932-6203&ror=052gg0110)
* Acta Zoologica, University of Maribor (TA exists): [{{< param apidocs.ApiURL >}}ta?issn=1463-6395&ror=01d5jce07]({{< param apidocs.ApiURL >}}ta?issn=1463-6395&ror=01d5jce07)