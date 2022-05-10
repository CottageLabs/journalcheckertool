# This builds in the list of funders, to save querying the API

FUNDERDB=../funderdb
FDB2HERE=../ui

(cd $FUNDERDB || exit; python3 funders.py)
(cd $FUNDERDB || exit; git log --pretty=format:'%h' -n 1 > $FDB2HERE/funderdb.git)

cp $FUNDERDB/autocomplete/funders.js static/js
