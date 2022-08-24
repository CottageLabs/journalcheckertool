# Import all data to JCT

To build and import all (new style) indexes, use the following command.

```
python cli.py load _all
```

Note that this does not trigger the remote JCT imports, they must be triggered separately.

# Using the Import CLI

The Import CLI gives you control over exactly what import steps are run.  The general form of the interface is

```
python cli.py [mode] [target] [-s [stage]] [-o or -a]
```

**mode** tells the importer which part of its lifecycle it should be running, and the options are:
* resolve - run resolution on the target.  Note that this bypasses the indexers limits on how often targets are resolved, this will always directly resolve the target every time it is run.
* index - construct the index data for the target.  Note that this will resolve the sources via the usual index resolver, so will only resolve sources if they are older than their maximum age.
* load - load the index data into elasticsearch

**target** tells the importer what to act on in the given mode.  Depending on the **mode** the options of targets are
different:
* resolve mode - the target can be any of the datasources (e.g. `crossref`, `doaj`, `ror`, etc)
* index mode - the target can be any of the output index types (e.g. `jac` or `iac`), or the special keyword `_all` to index all targets
* load mode - as index mode

**stage** tells the importer which stage in the mode to process.  Each mode has different stages in its processing pipeline:
* resolve
  1. gather - pull the data from the datasource
  2. analyse - analyse the pulled data, ready for use in indexing
* index
  1. gather - gather and analyse all the data in the `resolve` pipeline
  2. analyse - analyse the data from each datasource to build the data for this index
  3. assemble - assemble the analysed data into indexable documents
  4. load - load the data into the elasticsearch index
* load - has no stages, this argument will have no effect in this mode

**stage pipeline execution (-o or -a)** tells the importer whether to run only the given **stage** or to run all the
stages before it, up-to and including the supplied stage.

Here are a set of example commands:

1. Gather all of the data from crossref, and analyse it:

```
python cli.py resolve crossref
```

You can also set the stage and pipeline execution explicitly.  Here we specify a **stage** of `analyse` which is the
last stage of `resolve` and we specify `-a` to indicate to run all prior stages, so `gather` and `analyse` will both
be run.

```
python cli.py resolve crossref -s analyse -a
```

If we had already retrieved the data from crossref, and we just wanted to re-run the analysis stage, we could run
only the analyse stage, and omit the `gather` stage, by specifying `-o` meaning "only run the specified stage and not
the prior stages".  Note that in this case you must ensure that the previous stages have been run, or you will receive
errors.

```
python cli.py resolve crossref -s analyse -o
```

2. Prep the JAC index

```
python cli.py index jac
```

This is equivalent to the more explicit command

```
python cli.py index jac -s assemble -a
```

As with the Crossref example, you can run only a single stage.  For example if we wanted to just analyse the data for the
JAC index, we could do

```
python cli.py index jac -s analyse -o
```

3. Load JAC Index into Elasticsearch

```
python cli.py load jac
```

---

(previous instructions, still to review)


# Import data to JCT

To import data into jct, run

```
python jct.py
```

This runs the following imports

* Journal autocomplete data import
* Institution autocomplete data import
* JCT import, which in turn imports from
  * Journals form Crossref and DOAJ
  * TJ
  * SA Prohibited data
  * Rights retention data
  * Funder config
  * Funder language
  * TA

This will send an email, when the importer has finished running the commands needed to invoke an import. The import task itself runs in the background and could take a couple of hours to complete.

To import just the TA data, run

```
python jct_ta.py
```

This will send an email, when the importer has finished running the commands needed to invoke a TA import. The import task itself runs in the background and could take a couple of hours to complete.

## Check the import has run fine

To check the import, run

```
python check_index.py
```

This will send an email when the import check is completed. It checks for count and date created (if it exists).

## Building the JCT autocomplete

The JCT autocomplete has two autocomplete sources - [journal](#building-the-journal-autocomplete) and [institution](#building-the-institution-autocomplete). 

To build the autocomplete, run

```
python jctdata/jct.py
```

To index the journal autocomplete data, run

```
python jctdata/index.py jac -s dev
```

To index the institution autocomplete data, run

```
python jctdata/index.py iac -s dev
```

### Building the Journal Autocomplete

Run

```
python jctdata/jac.py
```

This will gather data from Crossref and DOAJ (more sources need to be added to make this complete), and produce 
an output file in `databases/jct/jac/[current timestamp]/jac.json`

You can then import this into ES (dev) with:

```
python jctdata/index.py jac -s dev
```

This will create a new index type with the name `jac` in an index called `jct_jac_dev[timestamp]`

It will then create (or repoint) the alias `jct_jac_dev` to this new index.

If you want to create the index for production, omit the `-s dev` argument.

This operation will also remove any old indices for the same type, leaving behind 2 old ones for reference (or however many are specified in `settings.py`).

### Building the Institution Autocomplete

Run

```
python jctdata/iac.py
```

This will gather data from ROR and produce an output file in `databases/jct/iac/[current timestamp]/jac.json`

You can then import this into ES (dev) with:

```
python jctdata/index.py iac -s dev
```

This will create a new index type with the name `iac` in an index called `jct_iac_dev[timestamp]`

It will then create (or repoint) the alias `jct_iac_dev` to this new index.

If you want to create the index for production, omit the `-s dev` argument.

This operation will also remove any old indices for the same type, leaving behind 2 old ones for reference (or however many are specified in `settings.py`).


### Gathering data

Look in `jctdata/resolver.py`.  In the `__name__ == "__main__"` section at the bottom, list the
datasources (using the names used in `settings.py`) you want to gather like:

```
gather_data(["doaj", "crossref", "tj", "ror"], True)
```

This will download and analyse all the data from those datasources, if your current copies of that data are older than the configured maximum (in `settings.py`).

Data will be placed in `databases/[source]/[timestamp]/origin.csv` or `databases/[source]/[timestamp]/origin.json`.  For example, the DOAJ data will be in `databases/doaj/2022-04-07_2150/origin.csv` and the ror data will be in `databases/ror/2021-09-23/origin.json`. The ROR data will look for the latest copy of the data made available. The timestamp of the directory will reflect that date.

To force a re-download of the data, just delete the timestamp directory and re-run.


## Config

Look in `settings.py`.  There is no clever local settings override of the default settings, just modify this file
locally for now, we'll put something better in later.
