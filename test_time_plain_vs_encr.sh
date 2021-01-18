#!/bin/sh
timefile_plain='./data/time_plain.txt'
timefile_encr='./data/time_encr.txt'
timefile_encr2='./data/time_encr2.txt'

scale_values='1 2 5 10 20 50 100 200 500'

echo "\nStart computation"

rm -f $timefile_plain
rm -f $timefile_encr
rm -f $timefile_encr2

for scale in $scale_values; do
    # plain
    gtime -f "%e" -o $timefile_plain -a python matrix_multiplication.py plain \
    $((20 * scale)) $((20 * scale)) $((20 * scale)) $((20 * scale)) 4

    # encrypted
    gtime -f "%e" -o $timefile_encr -a python matrix_multiplication.py encrypted \
    $((20 * scale)) $((20 * scale)) $((20 * scale)) $((20 * scale)) 4

    # encrypted 2
    gtime -f "%e" -o $timefile_encr2 -a python matrix_multiplication2.py encrypted \
    $((20 * scale)) $((20 * scale)) $((20 * scale)) $((20 * scale)) 4
done

echo "\nDone!"
