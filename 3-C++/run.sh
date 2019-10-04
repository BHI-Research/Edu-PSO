#!/bin/bash
mkdir build
cd build/
cmake ..
make
echo -n "How many times you want to execute PSO? "
read executions
echo
for i in $(seq 1 $executions); do
    echo " Execution N° $i: "
    echo
    ./application -o output.txt
    echo
done
echo "Done."
cd ..
