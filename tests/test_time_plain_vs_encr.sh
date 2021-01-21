#!/bin/sh
timefile='../data/time_plain_encr.txt'

scale_values='1 2 5 10'

echo "\nStart computation"


echo "plain" >> $timefile
for scale in $scale_values; do
    # plain
    gtime -f "%e" -o $timefile -a python matrix_multiplication_local.py plain \
    $((10 * scale)) $((10 * scale)) $((10 * scale)) $((10 * scale)) $((2 * scale))
done

echo "encr" >> $timefile
for scale in $scale_values; do
    # encrypted
    gtime -f "%e" -o $timefile -a python matrix_multiplication_local.py encrypted \
    $((10 * scale)) $((10 * scale)) $((10 * scale)) $((10 * scale)) $((2 * scale))
done

echo "encr2" >> $timefile
for scale in $scale_values; do
    # encrypted 2
    gtime -f "%e" -o $timefile -a python matrix_multiplication_local.py encrypted \
    $((10 * scale)) $((10 * scale)) $((10 * scale)) $((10 * scale)) $((2 * scale))
done

echo "\nDone!"
