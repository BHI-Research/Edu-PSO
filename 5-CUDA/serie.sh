#!/bin/bash
mkdir build
cd build/
cmake ..
make
for x in $(seq 1 5)
do
./CUDAproject -d 10 -p 10 -g 0.0 -o POSICIONESD.txt
./CUDAproject -d 20 -p 20 -g 0.0 -o POSICIONESD.txt
./CUDAproject -d 30 -p 30 -g 0.0 -o POSICIONESD.txt
./CUDAproject -d 40 -p 40 -g 0.0 -o POSICIONESD.txt
./CUDAproject -d 50 -p 50 -g 0.0 -o POSICIONESD.txt
./CUDAproject -d 60 -p 60 -g 0.0 -o POSICIONESD.txt
./CUDAproject -d 70 -p 70 -g 0.0 -o POSICIONESD.txt
./CUDAproject -d 80 -p 80 -g 0.0 -o POSICIONESD.txt
./CUDAproject -d 90 -p 90 -g 0.0 -o POSICIONESD.txt
./CUDAproject -d 100 -p 100 -g 0.0 -o POSICIONESD.txt
./CUDAproject -d 200 -p 200 -g 0.0 -o POSICIONESD.txt
./CUDAproject -d 300 -p 300 -g 0.0 -o POSICIONESD.txt
./CUDAproject -d 400 -p 400 -g 0.0 -o POSICIONESD.txt
done
cd ..
