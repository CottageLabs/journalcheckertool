# Building the Journal Autocomplete

Run

```
python jctdata/jac.py
```

This will gather data from Crossref and DOAJ (more sources need to be added to make this complete), and produce 
an output file in `databases/jct/jac/[current timestamp]/jac.json`

You can then import this into ES with:

```
python jctdata/index.py jct_dev jac
```

This will create a new index type with the name `jac` in an index called `jct_dev_jac[timestamp]`

It will then create (or repoint) the alias `jct_dev_jac` to this new index.

It does not currently remove the old index.


# Gathering data

Look in `jctdata/resolver.py`.  In the `__name__ == "__main__"` section at the bottom, list the
datasources (using the names used in `settings.py`) you want to gather like:

```
gather_data(["doaj", "crossref"], True)
```

This will download and analyse all the data from those datasources, if your current copies of that data are older than the configured maximum (in `settings.py`).

Data will be placed in `databases/[source]/[timestamp]/origin.csv`.  For example, the DOAJ data will be in `databases/doaj/2022-04-07_2150/origin.csv`

To force a re-download of the data, just delete the timestamp directory and re-run.


# Config

Look in `settings.py`.  There is no clever local settings override of the default settings, just modify this file
locally for now, we'll put something better in later.
