#!/bin/bash
for filename in ./benchmarks/*.blif; do
    ../abc -q "read_blif $filename" -f ./Mapping/SCRIPT -o ./Mapping/output/$(basename $filename)
done
python ./Mapping/rewrite.py
