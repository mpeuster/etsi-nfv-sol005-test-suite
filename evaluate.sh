#!/bin/bash
rm -f durations.result

for i in `seq 1 10`;
do
    echo "Running test run" $i
    pytest --durations=0 -q >> durations.result
    sleep 5
done    


