#!/bin/bash
export PATH=/Library/Frameworks/Python.framework/Versions/2.7/bin:$PATH
SOURCE="${BASH_SOURCE[0]}"
CUPATH=$(dirname $(dirname "$0"))
cd "$CUPATH"