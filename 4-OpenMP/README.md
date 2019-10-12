# Edu-PSO OpenMP
A simple parallel OpenMP implementation of PSO written in C++.

# How to run
By just running the run.sh script you will compile and execute this PSO implementation. Make sure to have cmake installed first. The generated binary files will be located at /build.

```
$ sh run.sh
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
CMake Warning (dev) at /usr/share/cmake-3.10/Modules/FindOpenMP.cmake:310 (if):
  if given arguments:
    
    "TRUE"
    
  An argument named "TRUE" appears in a conditional statement.  Policy
  CMP0012 is not set: if() recognizes numbers and boolean constants.  Run
  "cmake --help-policy CMP0012" for policy details.  Use the cmake_policy
  command to set the policy and suppress this warning.
Call Stack (most recent call first):
  /usr/share/cmake-3.10/Modules/FindOpenMP.cmake:425 (_OPENMP_GET_SPEC_DATE)
  CMakeLists.txt:4 (FIND_PACKAGE)
This warning is for project developers.  Use -Wno-dev to suppress it.

-- Found OpenMP_C: -fopenmp  
CMake Warning (dev) at /usr/share/cmake-3.10/Modules/FindOpenMP.cmake:310 (if):
  if given arguments:

    "TRUE"

  An argument named "TRUE" appears in a conditional statement.  Policy
  CMP0012 is not set: if() recognizes numbers and boolean constants.  Run
  "cmake --help-policy CMP0012" for policy details.  Use the cmake_policy
  command to set the policy and suppress this warning.
Call Stack (most recent call first):                                                    
  /usr/share/cmake-3.10/Modules/FindOpenMP.cmake:425 (_OPENMP_GET_SPEC_DATE)            
  CMakeLists.txt:4 (FIND_PACKAGE)                                                       
This warning is for project developers.  Use -Wno-dev to suppress it.

-- Found OpenMP_CXX: -fopenmp  
-- Found OpenMP: TRUE   
OPENMP FOUND
-- Configuring done
-- Generating done
-- Build files have been written to: /home/nahuel/Escritorio/PSO_entrega/PSO_OMP/build
Scanning dependencies of target application
[ 33%] Building CXX object CMakeFiles/application.dir/main.cpp.o
[ 66%] Building CXX object CMakeFiles/application.dir/pso.cpp.o
[100%] Linking CXX executable application
[100%] Built target application

How many times you want to execute PSO? 1

Execution N° 1: 


How many dimensinos? 2
How many particles? 10
How many steps? 50


Best position: [ 0.000067, -0.000079,]

Best global fit 0.000000

Execution time: 0.002407 segundos


Done.
```

[![BHI|Research Group](https://github.com/BHI-Research/Edu-PSO/blob/master/DEMO/logoBHI.png?raw=true)](https://bhi-research.github.io/)
