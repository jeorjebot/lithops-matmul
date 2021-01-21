#!/bin/sh
timefile='../data/time_local_cloud.txt'

scale_values='1 2 5 10'

echo "\nStart computation"

echo "plain cloud" >> $timefile
for scale in $scale_values; do
    #plain
    gtime -f "%e" -o $timefile -a python matrix_multiplication.py plain \
    $((10 * scale)) $((10 * scale)) $((10 * scale)) $((10 * scale)) 2
done

echo "encrypted cloud" >> $timefile
for scale in $scale_values; do
    # encrypted
    gtime -f "%e" -o $timefile -a python matrix_multiplication.py encrypted \
    $((10 * scale)) $((10 * scale)) $((10 * scale)) $((10 * scale)) 2
done

echo "scale plain cloud" >> $timefile
for scale in $scale_values; do
    #plain
    gtime -f "%e" -o $timefile -a python matrix_multiplication.py plain \
    $((10 * scale)) $((10 * scale)) $((10 * scale)) $((10 * scale)) $((2 * scale))
done

echo "scale encrypted cloud" >> $timefile
for scale in $scale_values; do
    # encrypted
    gtime -f "%e" -o $timefile -a python matrix_multiplication.py encrypted \
    $((10 * scale)) $((10 * scale)) $((10 * scale)) $((10 * scale)) $((2 * scale))
done

echo "plain local" >> $timefile
for scale in $scale_values; do
    #plain
    gtime -f "%e" -o $timefile -a python matrix_multiplication_local.py plain \
    $((10 * scale)) $((10 * scale)) $((10 * scale)) $((10 * scale)) 2
done

echo "scale plain local" >> $timefile
for scale in $scale_values; do
    #plain
    gtime -f "%e" -o $timefile -a python matrix_multiplication_local.py plain \
    $((10 * scale)) $((10 * scale)) $((10 * scale)) $((10 * scale)) $((2 * scale))
done

echo "\nDone!"
