#!/usr/bin/env bash
HERE=$(dirname "$0")
REPO=${2:-"https://github.com/tdhooghe/auto-sklearn.git"}
PKG=${3:-"auto-sklearn"}

# creating local venv
. ${HERE}/../shared/setup.sh ${HERE} true

PIP install --no-cache-dir -r $HERE/requirements.txt

TARGET_DIR="${HERE}/venv/lib/python3.9/site-packages/${PKG}"
rm -Rf ${TARGET_DIR}

git clone --single-branch --branch hyperboost ${REPO} ${TARGET_DIR}
cd ${TARGET_DIR}
PIP install -U -e ${TARGET_DIR}

installed="${HERE}/.setup/installed"
PY -c "from autosklearn import __version__; print(__version__)" >> "$installed"
