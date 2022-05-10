# JCT Funder Database

This repository contains all the funder configuration for JCT.  This covers:

* Runtime configuration for the back-end algorithms
* Front-end configuration for advice display cards
* Language files for the UI

In order to use the data in this repository in the JCT front and back end applications it must be compiled to JSON files.  There are two JSON files per funder:

1. A language pack for the UI
2. A configuration file to be used by both back-end and front-end

These compiled JSON files are NOT included in this repository, you will need to compile them using the Python scripts provided, as described in the following sections

## Language Pack

```
pip install pyyaml
python lang.py
```

This will create a directory `lang` which contains one language file per funder


## Configuration

```
pip install pyyaml
python config.py
```

This will create a directory `config` which contains one config file per funder


## Funder Autocomplete List

```
pip install pyyaml
python funders.py
```

This will create a directory `autocomplete` which contains a file `funders.json` which is a list of all the funder ids, names and abbreviations.  This can be used to build the autocomplete funder entry box.