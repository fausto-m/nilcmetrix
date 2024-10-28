#!/bin/bash
docker run --rm --link pgs_cohmetrix:pgs_cohmetrix -v /Users/fausto.ms/Documents/GitHub/simple-text-br/nilcmetrix:/opt/text_metrics cohmetrix:focal bash -c "python3 run_min.py \"$1\""
