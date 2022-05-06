# This is a temporary fix to build in the funder database data into the UI before
# it is available formally via the API/standard build

FUNDERDB=../jct-funderdb
FDB2HERE=../jct

#(cd $FUNDERDB || exit; python config.py)
(cd $FUNDERDB || exit; python funders.py)
#(cd $FUNDERDB || exit; python lang.py)
(cd $FUNDERDB || exit; git log --pretty=format:'%h' -n 1 > $FDB2HERE/funderdb.git)

#cp $FUNDERDB/config/default_config.js static/js
#cp $FUNDERDB/language/default_lang.js static/js
cp $FUNDERDB/autocomplete/funders.js static/js
