#!/bin/bash
mkdir build
cd build/
cmake ..
make
echo
echo -n "Ingrese cantidad de corridas:  "
read corridas
echo
for i in $(seq 1 $corridas); do 
            echo " corrida N° $i: "
            echo
            ./application -o resultado_serie.txt
            echo
done
echo "Fin del programa SERIE"
echo
cd ..
