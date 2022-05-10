# Cards display logic

## When to display a card

A card is displayable if both:

1. It's `match_routes` statement is true (or is missing)
2. It's `match_qualifications` statement is true (or is missing)

### Match routes

`match_routes` supports 3 logical operators:

* `must` - the routes listed within must be compliant
* `or` - at least one route listed within must be compliant
* `not` - none of the routes listed within may be compliant

Routes are identified by their route id, as used as a key in the `routes` section
of `config.yml`.

For example, the following configuration would cause a card to be displayed if:

* SA is compliant
* TJ or Hybrid is compliant
* TA is non-compliant

```yaml
match_routes:
  must:
    - sa
  or:
    - tj
    - hybrid
  not:
    - ta
```

### Match Qualifications

`match_qualifications` supports 3 logical operators:

* `must` - the qualifications listed within must be compliant
* `or` - at least one qualification listed within must be compliant
* `not` - none of the qualifications listed within may be compliant

Qualifications are identified by a string of the form:

```
[route id].[qualification code]
```

For example, the `rights_retention_author_advice` qualification in the self-archiving route
would be identified as:

```
sa.rights_retention_author_advice
```

For example, the following configuration woudl cause the card to be displayed if the
`rights_retention_author_advice` qualification is missing from the self-archiving route.

```yaml
match_qualifications:
  not:
    - sa.rights_retention_author_advice
```

## Displaying a card

A card has two configuration properties that tell you how to display it:

* `preferred` - whether to label the card as a preferred route
* `display_if_compliant` - a list of routes to display information about if those routes are compliant

A card is of the general form:

```
[icon]
[preferred status]
[title]

[general information about the way to comply]
[specific information about each relevant route to display]
```

To construct this from the language files, this can be done using the following language codes:

```
img: cards.[card_id].icon
site.preferred
cards.[card_id].title

cards.[card_id].body.default
cards.[card_id].body.[compliant route id]
```

