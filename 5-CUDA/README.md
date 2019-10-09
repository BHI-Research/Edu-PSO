# Edu-PSO CUDA
A simple parallel implementation of PSO optimized with CUDA written in C++

### How to run
By just running the `run.sh` script you will compile and execute this PSO implementation. Make sure to have `cmake` installed first.
The generated binary files will be located at `/build`.

```
$ sh serie.sh
-- The C compiler identification is GNU 7.4.0
-- The CXX compiler identification is GNU 7.4.0
-- Check for working C compiler: /usr/bin/cc
-- Check for working C compiler: /usr/bin/cc -- works
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Detecting C compile features
-- Detecting C compile features - done
-- Check for working CXX compiler: /usr/bin/c++
-- Check for working CXX compiler: /usr/bin/c++ -- works
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Looking for pthread.h
-- Looking for pthread.h - found
-- Looking for pthread_create in pthread
-- Looking for pthread_create in pthread - found
-- Found Threads: TRUE  
-- Found CUDA: /usr/local/cuda (found version "10.0") 
-- Configuring done
-- Generating done
-- Build files have been written to: /home/alumno1/PSO_C/PruebasCUDA/PSO_CUDA5/build
[ 33%] Building NVCC (Device) object CMakeFiles/CUDAproject.dir/CUDAproject_generated_pso.cu.o
[ 66%] Building NVCC (Device) object CMakeFiles/CUDAproject.dir/CUDAproject_generated_main.cu.o
Scanning dependencies of target CUDAproject
[100%] Linking CXX executable CUDAproject
[100%] Built target CUDAproject
How many times you want to execute PSO?  1

Execution N° 1: 
enter dimensions
2
enter number of particles
10
enter number of steps
50
Goal achieved @ step 0 (error=1.600e-13) :-)
Best known position: [  0.00  0.00]
Dimensions = 2
Particles = 10
Steps = 50
Simulation time = 0.098124 seconds
Done.
```
[![BHI|Research Group](https://github.com/BHI-Research/Edu-PSO/blob/master/DEMO/logoBHI.png?raw=true)](https://bhi-research.github.io/)
