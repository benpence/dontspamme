#!/bin/bash

cd dontspamme
grep -R -n TODO ./ | sed    \
    -e 's/^\.\///'          \
    -e "s/ \#*\/* *TODO:/\\`echo -e '\n\r'`   /g"
