---
title: "Transformative Agreements"
date: 2021-02-13T23:43:11Z
description: "Transformative agreements explained for the Journal Checker Tool: Plan S Compliance Validator."
---

# Transformative Agreements Public Data

This document describes the structure of the published data for Transformative Agreements.

<p xmlns:dct="http://purl.org/dc/terms/">
  <a rel="license"
     href="http://creativecommons.org/publicdomain/zero/1.0/"><img src="https://licensebuttons.net/p/zero/1.0/88x31.png" style="border-style: none;" alt="CC0" /></a> To the extent possible under law, <span rel="dct:publisher" resource="[_:publisher]">the person who associated CC0</span> with this work has waived all copyright and related or neighboring rights to this work.
</p>

## Transformative Agreement Index

TAs exposed by JCT are listed [in this CSV](https://docs.google.com/spreadsheets/d/e/2PACX-1vStezELi7qnKcyE8OiO2OYx2kqQDOnNsDX1JfAsK487n2uB_Dve5iDTwhUFfJ7eFPDhEjkfhXhqVTGw/pub?gid=1130349201&single=true&output=csv)

This is a CSV which has the following fields:

* ESAC ID - the ID of the TA in the ESAC Registry
* Relationship - in the case where the TA defines multiple classes of relationship between institutions and journals, we have provided a short name
for that relationship
* End Date - the date this TA is in force until
* C/A Only - is the TA relevant only to Corresponding Authors
* Data URL - a URL to a CSV of the institutions and journals involved in the TA
* Last Reviewed - the date this TA was last reviewed by the JCT team

All records that are listed in this index are:

1. Fully reviewed by the JCT Data Management team
2. Plan S compliant

If a TA is missing from this list it is because it is either still under review (or in the queue to be reviewed), or it has been reviewed and found not to
be Plan S compliant.


## Transformative Agreement Data

By following the `Data URL` from the Transformative Agreement Index, you can obtain a CSV which gives you details of the Journals and Institutions involved
in the agreement.  The CSV is structured as follows:

1. Columns 1 - 5 list all the journals and their properties
2. Columns 6 - 9 list all the institutions and their properties

To correctly read the CSV you need to "split" it between Colums 5 and 6, and the resulting two ranges contain a journal or an institution per row.

The Journal properties are:

* Journal Name - the name of the Journal, usually as provided in the original agreement.
* ISSN (Print) - the Print ISSN of the Journal where available
* ISSN (Online) - the Online ISSN of the Journal where available
* Journal First Seen - the date on which the TA Data Management team observed this journal to be part of the TA (see note below)
* Journal Last Seen - the date on which the TA Data Management team observed this journal to have left the TA (see note below)

The Institution properties are:

* Institution Name - the name of the Institution, usually as provided in the original agreement
* ROR ID - the ROR ID of the Institution, where available
* Institution First Seen - the date on which the TA Data Management team observed this institution to be part of the TA (see note below)
* Institution Last Seen - the date on which the TA Data Management team observed this institution to have left the TA (see note below)

A note on "First Seen" and "Last Seen" dates: the TA Data Management team carries out initial review and then ongoing review of TAs to determine the list
of journals and institutions that are covered.  Over time, TAs may evolve such that new institutions or journals may be added to it, or instutitions or
journals may leave it, all while the main TA agreement is in effect.  As a result, our dataset tracks those changes over time.  As we do not have access to
the details of when a journal/institution joins/leaves a TA, instead we record the dates when we first/last observed the journal/institution to be part of the
TA.  This means, for example, that if you see a "Journal First Seen" date of 2020-08-20, this does not mean that the Journal only became part of the TA on that
date, it only means that that is the first date that we reviewed the TA and observed that journal to be a member.  The journal may have been part of the TA
since the start date of the agreement, but we cannot necessarily verify that.