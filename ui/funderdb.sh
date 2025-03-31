# This builds in the list of funders, to save querying the API

FUNDERDB=../funderdb
FDB2HERE=../ui

# This script takes and argument '-t'. When argument '-t' specified, funders data will be appended with test data
# sh funders.sh -t  to append test funders data (usually for development and testing)
# sh funders.sh without testdata (for production)

(cd $FUNDERDB || exit; python3 funders.py $1)
(cd $FUNDERDB || exit; git log --pretty=format:'%h' -n 1 > $FDB2HERE/funderdb.git)

cp $FUNDERDB/autocomplete/funders.js static/js
