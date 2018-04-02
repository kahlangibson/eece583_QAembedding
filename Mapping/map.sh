#!/bin/bash
for filename in ../benchmarks/*.blif; do
	echo $(basename $filename)
    ../abc -c "read_blif $filename" -F ./SCRIPT -o ./output/$(basename $filename)
done
