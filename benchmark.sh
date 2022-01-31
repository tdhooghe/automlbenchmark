#!/usr/bin/env bash

python3 runbenchmark.py autosklearn2_hyperboost large 1h12c
python3 runbenchmark.py autosklearn2 large 1h12c
python3 runbenchmark.py autosklearn2_hyperboost medium_sub 1h12c
python3 runbenchmark.py autosklearn2 medium_sub 1h12c
python3 runbenchmark.py autosklearn_hyperboost large 1h12c
python3 runbenchmark.py autosklearn large 1h12c
python3 runbenchmark.py autosklearn_hyperboost medium_sub 1h12c
python3 runbenchmark.py autosklearn medium_sub 1h12c