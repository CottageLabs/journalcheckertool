---
title: "Data Sources Used By JCT"
date: 2021-02-13T23:42:57Z
description: "A description of the data sources used by Journal Checker Tool."
---

# Data Sources Used By JCT

A number of data sources are used by the JCT, primarily for two purposes.

## 1. For the search interface

Firstly, remote datasources are used to populate the "autocomplete" feature in the search boxes for journal titles and for institutions. This feature provides a convenience to the user, allowing them to begin typing a  journal title or institution name and have the system supply matches, allowing the user to rapidly select the one they want. The fact that a journal title - or an institution name - appears in such a list does **not** imply any kind of endorsement of them by the Journal Checker Tool or by cOAlition S. These lists are offered simply as a convenience to the user in the search interface.
For journal titles, the datasource used by the JCT is  [Crossref](https://www.crossref.org/).
For institutions, the datasource used by the JCT is [ROR](https://ror.org).

## 2. For the Plan S compliance checks

In addition to CrossRef and ROR, JCT uses the following datasources to inform its calculation of Plan S compliance.

### DOAJ (Directory of Open Access Journals)

[DOAJ](https://doaj.org/) provides a high quality, manually curated list of fully OA journals, and is therefore perfectly suited to the *full OA* compliance check for Plan S. DOAJ provides a curated data feed to JCT.

### Open Access Button

Open Access Button Permission System provides clear information on how 85% of papers can be self-archived. Information provided includes which versions can be shared, licenses allowed, computed deposit statements and embargoes. [Open Access Button](https://openaccessbutton.org) provides a curated data feed to JCT.

### ESAC Agreement Registry

[The ESAC Agreement Registry](https://esac-initiative.org/about/transformative-agreements/agreement-registry/) is a community-curated registry of *[Transformative Agreements](https://esac-initiative.org/about/transformative-agreements/)* (TAs) between publishers on the one hand and academic institutions (mainly represented in consortia) on the other. The Plan S policy for recognising a TA requires that it be registered in ESAC and offer authors the option to publisher under a CC-BY licence. Therefore, the JCT derives its list of recognised TAs from the ESAC website.

