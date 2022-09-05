# Import all data to JCT

To build and import all (new style) indexes, use the following command.

```
python cli.py load _all
```

Note that this does not trigger the remote JCT imports, they must be triggered separately.

You can import both the new style and the remote imports with

```
python run_all_import.py
```

This runs the following imports

* Locally
  * Journal autocomplete data import
  * Institution autocomplete data import
  * Funder config
  * Funder language
* JCT import, which in turn imports from
  * Journals form Crossref and DOAJ
  * TJ
  * SA Prohibited data
  * Rights retention data
  * TA

This will send an email, when the importer has finished running the commands needed to invoke an import. The import task itself runs in the background and could take a couple of hours to complete.

## Config

Look in `settings.py`.  There is no clever local settings override of the default settings, just modify this file
locally for now, we'll put something better in later.

## Check the import has run fine

To check the import, run

```
python validate_all_import.py
```

This will send an email when the import check is completed. It checks for count and date created (if it exists).

# Importing only TA data

To import just the TA data, run

```
python run_ta_import.py
```

This will send an email, when the importer has finished running the commands needed to invoke a TA import. The import task itself runs in the background and could take a couple of hours to complete.

# Using the Import CLI

The Import CLI gives you control over exactly what import steps are run.  The general form of the interface is

```
python cli.py [mode] [target(s)] [-s [stage]] [-o or -a]
```

**mode** tells the importer which part of its lifecycle it should be running, and the options are:
* resolve - run resolution on the target.  Note that this bypasses the indexers limits on how often targets are resolved, this will always directly resolve the target every time it is run.
* index - construct the index data for the target.  Note that this will resolve the sources via the usual index resolver, so will only resolve sources if they are older than their maximum age.
* load - load the index data into elasticsearch

**target(s)** tells the importer what to act on in the given mode.  Depending on the **mode** the options of targets are
different:
* resolve mode - the target can be one or more of the datasources, separated by a space (e.g. `crossref`, `doaj`, `ror funderdb`, etc) or the special keyword `_all` which resolves all datasources
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
* load - has no stages, this argument will have no effect in this mode

**stage pipeline execution (-o or -a)** tells the importer whether to run only the given **stage** or to run all the
stages before it, up-to and including the supplied stage.

Here are a set of example commands:

## 1. Gather all of the data from crossref, and analyse it:

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

## 2. Prep the JAC index

```
python cli.py index jac
```

This is equivalent to the more explicit command

```
python cli.py index jac -s assemble -a
```

As with the Crossref example, you could also run only a single stage.  For example if we wanted to just analyse the data for the
JAC index, we could do

```
python cli.py index jac -s analyse -o
```

## 3. Load JAC Index into Elasticsearch

```
python cli.py load jac
```

## 4. Resolve and load everything

```
python cli.py load _all
```

# How the Local Importer works

If you run a command to import one of the datatypes to the index, for example the Journal Autocomplete, like

```
python cli.py load jac
```

The following processes happen:

1. All the datasources upon which the index is built are resolved.  For example, JAC requires Crossref, DOAJ and a variety of other smaller journal datasources.  A datasource is automatically downloaded via whatever mechanism is provided if the time elapsed since it was last downloaded is greater than the specified maximum age (e.g. a week).  If the datasource has been downloaded more recently than that, then the existing copy is used.  This speeds up repeat builds.  Data is placed in `databases/[datasource name]/[timestamp]`, usually in a file or folder called `origin`.
2. Datasources are analysed as needed.  For example, journal data sources have their ISSNs, Titles and Publishers extracted and normalised ready for any downstream indexer to use.  Again, the analysed data is placed in `databases/[datasource name]/[timestamp]`
3. The indexer assembles all the datasource information it needs into an intermediate form.  This form may be an amalgamation of the various datasources data, or a convenient output suitable for debugging/review, or both.  For example, the JAC assembles and normalises ISSNs, Titles and Publishers from all of its many datasources into a single deduplicated database, ready for assembly into the autocomplete index.
4. The indexer assembles a JSON file which comprises the indexable data.  The file consists of one JSON record per line.
5. The JSON file from the previous step is converted into the ES Bulk API format and loaded into an appropriately named index, which is of the form `jct_[index][suffix][timestamp]`.  For example, JAC loaded in a development environment will have a name like `jct_jac_dev20220828175612`
6. The ES index alias for the type is switched to point to the new index, and any old copies of the index are deleted (some number of old indices are kept for emergency roll-back, configured in `settings.py`).  The index alias will be of the form `jct_[index][suffix]`, so for JAC this would mean `jct_jac_dev` pointed to `jct_jac_dev20220828175612` after this operation.

