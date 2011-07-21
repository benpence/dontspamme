#!/bin/bash

cd src/
grep -R -n TODO\: ./ | sed    \
    -e 's/^\.\///'          \
    -e "s/ \#*\\/* *TODO:/\\`echo -e '\n\r'`   /g"
