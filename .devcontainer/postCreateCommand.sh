#!/bin/sh

if [ -f "../base/pyproject.toml" ]; then
    CWD=$(pwd)
    cd ../base
    python -m pip install -e .
    cd "$CWD"
else
    python -m pip --disable-pip-version-check --no-cache-dir install git+https://github.com/xannor/py_reolinkapi.git#main    
fi
python -m pip --disable-pip-version-check --no-cache-dir install -r requirements_dev.txt
