# Edu-PSO C++

A simple serial implementation of PSO written in C++.

### How to run
By just running the `run.sh` script you will compile and execute this PSO implementation. Make sure to have `cmake` installed first.
The generated binary files will be located at `/build`.

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
-- Configuring done
-- Generating done
-- Build files have been written to: /home/user/Edu-PSO/3-C++/build
Scanning dependencies of target application
[ 33%] Building CXX object CMakeFiles/application.dir/main.cpp.o
[ 66%] Building CXX object CMakeFiles/application.dir/pso.cpp.o
[100%] Linking CXX executable application
[100%] Built target application
How many times you want to execute PSO? 1

 Execution N° 1: 


How many dimensions? 2
How many particles? 10
How many steps? 50

Total particles number: 10

Best position: [0.000011,-0.000010,]

Best global fit: 0.000000

Execution time: 0.000309 seconds

Done.
```

[![BHI|Research Group](https://github.com/BHI-Research/Edu-PSO/blob/master/DEMO/logoBHI.png?raw=true)](https://bhi-research.github.io/)
