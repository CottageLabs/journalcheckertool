# Funder Configuration

## Funder Identification

```yaml
id: academyoffinlandaka
alternate_ids:
  - altid1
  - altid2
name: Academy of Finland
abbr: AKA
country: Finland
plan_s: 2021-01-01
aka:
  - name: Alternative Name
    abbr: ALT ABBR
```

* `id` - the unique identifier for the funder.  Can be any string unique within the funder database
* `name` - the preferred full name of the funder
* `abbr` - the preferred abbreviation of the funder
* `country` - the country of the funder.  Only provide this information if the country of the funder **is not** in the name of the funder
    **and** you wish the country to be displayed in the JCT UI, otherwise it can be omitted
* `plan_s` - ISO datestamp for the date that the funder began implementation of Plan S principles
* `aka` - alternative names for the funder.  These wil be presented in the JCT pull-down, but only the base funder 
  name/abbr will be selected if the page is loaded using the funder id in the URL query
  



## APC Payments

```yaml
apc:
  tj: true|false
```

* `apc.tj` - will the funder pay an APC for a TJ.  Boolean.

## Route configuration

This configuration is used by the back-end to configure the algorithm run for a given
query.

Overall structure for this configuration section is

```
routes:
    sa: [self-archiving configuration]
    full_oa: [Full OA configuration]
    hybrid: [Hybrid configuration]
    ta: [TA configuration]
    tj: [TJ configuration]
```

Each route is keyed by its standard `route_id`.

### SA Configuration Options

```
sa:
  calculate: true
  rights_retention: 2100-01-01
  license:
    - cc-by
    - cc-by-sa
    - cc0
  embargo: 0
```

* `routes.sa.calculate` - should the route be calculated
* `routes.sa.rights_retention` - the date that rights retention comes into effect for this publisher (use a date in the far future for "adoption to follow")
* `routes.sa.license` - licences acceptable for this funder for this route
* `embargo` - embargo length (in months) that is acceptable for this funder

### Full OA Configuration Options

```
full_oa:
  calculate: true
  license:
    - cc-by
    - cc-by-sa
    - cc0
```

* `routes.full_oa.calculate` - should the route be calculated
* `routes.full_oa.license` - licences acceptable for this funder for this route


### Hybrid Configuration Options

```
hybrid:
  calculate: false
  license:
    - cc-by
    - cc-by-sa
    - cc0
```

* `routes.hybrid.calculate` - should the route be calculated (note that by default this is turned off, as most funders do not support hybrid routes explicitly)
* `routes.hybrid.license` - licences acceptable for this funder for this route

### TA Configuration Options

```
ta:
  calculate: true
  license:
    - cc-by
    - cc-by-sa
    - cc0
```

* `routes.ta.calculate` - should the route be calculated
* `routes.ta.license` - licences acceptable for this funder for this route

### TJ Configuration Options

```
tj:
  calculate: true
```

* `routes.tj.calculate` - should the route be calculated


## Card Configuration

Card configurations are provided as a list:

```yaml
cards:
  - [card config]
  - [card config]
  - ...etc
```

All card configurations follow the same general form.

```yaml
id: [card_id]
match_routes:
  must:
    - [route_id]
  or:
    - [route_id]
    - [route_id]
  not:
    - [route_id]
match_qualifications:
  must:
    - [route_id].[qualification_id]
  or:
    - [route_id].[qualification_id]
    - [route_id].[qualification_id]
  not:
    - [route_id].[qualification_id]
preferred: true|false
compliant: true|false
display_if_compliant:
  - [route_id]
  - [route_id]
modal: [modal_id]
```

* `cards[].id` - a unique id for the card, an arbitrary string, but which will be used to identify the
card throughout the language files
* `cards[].match_routes` - match rules for compliant routes to determine if to show this card
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
* `cards[].display_if_compliant` - the list of routes, in order, to display information about if they are compliant.  If you leave
    this blank then no route-specific guidance will be displayed, but the `default` text for the card will be displayed anyway, so
    you only need to use this option if the card could display information about multiple routes, and you wish to control which
    information is displayed depending on which routes are compliant
* `cards[].modal` - the modal to bind to the card's overall modal (other modals can be specified inline in the card text as normal)

