#!/bin/sh

timefile='./data/time_dims.txt'
scale_values='1 2 5 10'

# aum dim esterne
# aum dim interne
# entrambe
# entrambe con block_size

echo "row A - col B" >> $timefile
for scale in $scale_values; do
    gtime -f "%e" -o $timefile -a python matrix_multiplication.py plain \
    $((20 * scale)) 20 20 $((20 * scale)) 4
done


echo "col A - row B" >> $timefile
for scale in $scale_values; do
    gtime -f "%e" -o $timefile -a python matrix_multiplication.py plain \
    20 $((20 * scale)) $((20 * scale)) 20 4
done


echo "row col A - row col B" >> $timefile
for scale in $scale_values; do
    gtime -f "%e" -o $timefile -a python matrix_multiplication.py plain \
    $((20 * scale)) $((20 * scale)) $((20 * scale)) $((20 * scale)) 4
done


echo "block size" >> $timefile
for scale in $scale_values; do
    gtime -f "%e" -o $timefile -a python matrix_multiplication.py plain \
    100 100 100 100 $((2 * scale))
done
