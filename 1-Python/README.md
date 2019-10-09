# Edu-PSO Python

## 1 - Simple Swarm
A simple serial implementation of PSO written in Python.

### How to run
```
$ python 1-simple.py

pso.run time:  17.65608787536621 ms
******************************
SOLUTION:	 [3.457934971437845, 3.9188672846589276, -1.1475257953475577, -4.291704605524991, 4.599855481976059]
ERROR:	 5.593228909729295
******************************
```

## 2 - Simple Benchmark
This implementation allows you to compare multiple executions of PSO, while one of its params changes from a min value to a max value in a given step.

### How to run
Use the `benchmark.sh` file to run this implementation changing multiple params: Swarm size (from 5 to 100), iterations (from 5 to 250), W (from 0.1 to 5), C1 (from 0.1 to 5), C2 (from 0.1 to 5)

```sh
sh benchmark.sh
```

You'll see the following plots:
![Bechmark Graph](https://raw.githubusercontent.com/BHI-Research/Edu-PSO/master/1-Python/Figures/fig1.PNG)
![Bechmark Graph](https://raw.githubusercontent.com/BHI-Research/Edu-PSO/master/1-Python/Figures/fig2.PNG)
![Bechmark Graph](https://raw.githubusercontent.com/BHI-Research/Edu-PSO/master/1-Python/Figures/fig3.PNG)
![Bechmark Graph](https://raw.githubusercontent.com/BHI-Research/Edu-PSO/master/1-Python/Figures/fig4.PNG)
![Bechmark Graph](https://raw.githubusercontent.com/BHI-Research/Edu-PSO/master/1-Python/Figures/fig5.PNG)

[![BHI|Research Group](https://github.com/BHI-Research/Edu-PSO/blob/master/DEMO/logoBHI.png?raw=true)](https://bhi-research.github.io/)

