---
title: "How It Works"
date: 2021-02-13T23:42:57Z
description: "A description of how the Journal Checker Tool works."
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

# How the Journal Checker Tool works

The Journal Checker Tool (JCT) is provided by cOAlition S to authors to support them in finding Plan S compliant 
"routes" through which to publish their articles. The tool allows an author to enter the name of a funder, an 
institution and the journal to which they plan to submit an article, and checks if this combination of funder, 
institution and journal offers any route to compliance with Plan S.

## <a name="architecture"></a>Architecture

The JCT is divided into two components - a *backend* and a *frontend*.

**Back-end:** the back-end component harvests and [caches](#caches) data from a number of significant 
[data sources](#data_sources), handles search requests via an API, and executes several [algorithms](#algorithms) used 
to determine compliance with the Plan S policies. The back-end is designed in such a way that it may be used in other, 
third-party webservices via its API.

**Front-end:** the front-end component is the part that most users see, providing the search form and results screen, 
as well as documents such as FAQs etc.

**Codebase:** [https://github.com/CottageLabs/jct](https://github.com/CottageLabs/jct)

## <a name="data_sources"></a>Data Sources

A number of data sources are used by the JCT to inform its calculation of *Plan S* compliance. These are documented in [Data Sources Used By JCT](/data-sources).



## <a name="caches"></a>Caches

The data used in the JCT calculation is both very large (millions of records) and distributed across the global 
network. This means that, in order to maintain a good level of performance, the JCT operates a set of local caches of 
some of this data. These caches are "refreshed" regularly. Refreshing the caches picks up new records as well as 
updates to existing records.



## <a name="api"></a>API

The API to the the back-end component of the JCT is used by the front-end component. This API is also made openly 
available so that others may use it directly. 
The API is [documented here](/apidocs).



## <a name="algorithms"></a>Algorithms

The JCT makes its calculations according to a defined algorithm.

<img src="/img/algorithm_main.svg">

### Inputs

A request against the compliance algorithm (such as via the Web API) can provide the following constraining parameters:

| **Parameter** | Cardinality | **Data type** |
| ------------- | ----------- | ------------- |
| Journal       | 1           | ISSN          |
| Funder        | 0..*        | CrossRef ID   |
| Institution   | 0..*        | ROR ID        |

Note that both Funder and Institution are not strictly required for the algorithm to execute. This is because there are 
compliance routes documented here which do not *require* either Funder or Institution. Nonetheless, Funder and 
Institution data is essential to give the user a complete picture of the compliance space for their context.

The ISSN is required. This constraint means that we can calculate compliance for journals **only if they are identified 
with an ISSN**.

### Outputs

The output of the algorithm consists of a set of 4 or more compliance analyses for the various input combinations. 
Each of these analyses contains:

* The ISSN of the Journal the analysis refers to
* The Funders the analysis refers to
* The ROR IDs of the Institutions the analysis refers to
* The compliance route for which this answer is relevant
* Whether this analysis determines the set of Funder, Institution and Journal here to be compliant. One of 3 possible outcomes is available:
    * *Compliant* - the algorithm has determined that the input would comply with Plan S at the time the query was executed
    * *Non-Compliant* - the algorithm has determined that the input does not comply with Plan S at the time the query was executed
    * *Unknown* - there was insufficient information in the data source(s) to determine whether the input complies with Plan S or not at the time the query was executed
* Qualifications for compliance - any guidance that the user needs to understand their compliance result in the context of the query.
* An audit trail for the decision - a record of the checks that took place in order to come to this conclusion

The best route to compliance may be different for each user.

### Full OA Check

When JCT checks for compliance with the Full OA route, this is the algorithm which is followed.

Note that transitions are annotated with the codes you will see in the API logs for your request.

<img src="/img/algorithm_fulloa.svg">


### Self Archiving Check

When JCT checks for compliance with the Self Archiving route, this is the algorithm which is followed.

Note that transitions are annotated with the codes you will see in the API logs for your request.

<img src="/img/algorithm_sa.svg">


### TA Check

When JCT checks for compliance with the Transformative Agreements route, this is the algorithm which is followed.

Note that transitions are annotated with the codes you will see in the API logs for your request.

<img src="/img/algorithm_ta.svg">


### TJ Check

When JCT checks for compliance with the Transformative Journals route, this is the algorithm which is followed.

Note that transitions are annotated with the codes you will see in the API logs for your request.

<img src="/img/algorithm_tj.svg">

