#!/bin/bash
python setup.py install

dev_appserver.py \
    --datastore_path=`pwd`/scripts/datastore.rdbms \
    src/app/

python setup.py uninstall