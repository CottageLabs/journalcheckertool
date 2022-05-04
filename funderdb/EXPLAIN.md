# Explain This Result Logic

The "Explain This Result" section of the JCT website should be built as follows from the information in the
funder database and the API response.

## Overall structure

The overall structure of the "Explain This Result" section should be as follows:

```
WAYS TO COMPLY
[intro text]

* Way 1
* Way 2
* ... etc

DATA SUPPORTING YOUR WAYS TO COMPLY
[intro text]

* Full OA
* Self-Archiving
* Hybrid
* TA
* TJ
```

`WAYS TO COMPLY` are equivalent to the Cards in the funder database.

`DATA SUPPORTING YOUR WAYS TO COMPLY` are equivalent to the Routes in the funder database

### The above using keys in `explain.yml`

```
WAYS TO COMPLY (ways_to_comply.title)
[intro text] (ways_to_comply.text)

* Way 1 (cards.[card id].title)
* Way 2 (cards.[card id].title)
* ... etc

DATA SUPPORTING YOUR WAYS TO COMPLY (supporting_data.title)
[intro text] (supporting_data.text)

* Full OA (routes.full_oa.label)
* Self-Archiving (routes.sa.label)
* Hybrid (routes.hybrid.label)
* TA (routes.ta.label)
* TJ (routes.tj.label)
```

## Ways to Comply Section

For each card, in the same order as they appear in the card-based summary results, display a section that 
describes in more detail why that way to comply is available.

It should essentially summarise the `match_routes` and `match_qualifications` conditions for that
card.  It should also link to the relevant sections of `DATA SUPPORTING YOUR WAYS TO COMPLY` where relevant.

For example, for the `he_tj_hybrid` card for HE, it would be as follows

```
CONDITIONS
[intro text]
* The following routes must all be compliant:
    * Self-Archiving
* At least one of the following routes must be compliant:
    * TJ
    * Hybrid

HOW THIS WAY IS COMPLIANT
[intro text]
* This journal supports [self-archiving](link to next section)
* This journal is a [Transformative Journal](link to next section)

ADVICE
* [repeat the information provided in the card]
```

### The above using keys from `explain.yml`

```
CONDITIONS (ways_to_comply.conditions.title)
[intro text] (ways_to_comply.conditions.text)
* The following routes must all be compliant: (route_match.must)
    * Self-Archiving (routes.sa.label)
* At least one of the following routes must be compliant: (route_match.or)
    * TJ (routes.tj.label)
    * Hybrid (routes.hybrid.label)

HOW THIS WAY IS COMPLIANT (ways_to_comply.how_it_complies.title)
[intro text] (ways_to_comply.how_it_complies.text)
* This journal supports [self-archiving](link to next section) (routes.sa.compliant)
* This journal is a [Transformative Journal](link to next section) (routes.tj.compliant)

ADVICE (ways_to_comply.advice.title)
* [repeat the information provided in the card] (card.*)
```

## Data Supporting Your Ways to Comply Section

For each route, whether they are compliant or not, print the calculation made by the algorithm.

This should be essentially the same as in the current version of the system.