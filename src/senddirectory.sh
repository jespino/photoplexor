#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

if [ -d "$1" ]; then
    for x in $1/*; do
        echo Sending $x
        echo Id returned: `curl --form photo=@"$x" http://localhost:8080 2> /dev/null`
    done
else
    echo "ERROR: $1 is not a valid directory"
fi
