# Edu-PSO

[![BHI|Research Group](https://github.com/BHI-Research/Edu-PSO/blob/master/DEMO/logoBHI.png?raw=true)](https://bhi-research.github.io/)

### Introduction

Particle Swarm Optimization (PSO) is a metaheuristic inspired on the behavior of a group of animals in the search for food. The algorithm offers opportunities not only as a research subject, but also as a remarkable parallel and distributed computing educational tool. As a parallel processing implementation, particles offers an excellent metaphor for concurrent entities. From the educational point of view, positions, velocities and forces are simple concepts to understand. In this work we present the educational benefits of PSO and we show some challenges in the implementation of the algorithm in hardware accelerators.

[![Edu-PSO|Particle](https://github.com/BHI-Research/Edu-PSO/blob/master/img/part.png?raw=true)]

### Demo

We present a website with a [JavaScript](https://github.com/BHI-Research/Edu-PSO/tree/master/DEMO) implementation to understand the movement of the swarm of particles and how it reaches the result.

[![Edu-PSO|DEMO Animation](https://github.com/BHI-Research/Edu-PSO/blob/master/img/EduPSODEMO.gif?raw=true)](https://bhi-research.github.io/)


### PSO Formulation

A quite general formulation of an optimization problem is:

[![Edu-PSO|DEMO Ecuation 1](https://github.com/BHI-Research/Edu-PSO/blob/master/img/e1.PNG?raw=true)](https://bhi-research.github.io/)

Vectors  *x* and *y* represent continuous and binary variables respectively. Vector  *O* comprises the data (parameters) of the system under study. Function *F(.)* is the  objective function to be optimized and *h(.)* and *g(.)* are the vectors of equality and inequality constraints respectively. This is a very general and conceptual approach to address problems of practical interest. The basic PSO algorithm is described by two simple equations:

[![Edu-PSO|DEMO Ecuation 2](https://github.com/BHI-Research/Edu-PSO/blob/master/img/e2.PNG?raw=true)](https://bhi-research.github.io/)

Vector  *z* is a matrix of *Np.n*, where n is the number of optimization variables and *Np* is the number on members of the swarm. In other words *z* constitutes a pool of possible solutions which represent particles in the search space whose positions vary through adjustments in the velocity (Eq. 4). Vector *v* is the velocity, which, for each particle is calculated as a function of the best position reached by itself along its trajectory (*p*) (individual memory) and of the best position reached by the whole swarm along its evolution (*q*) (social memory) (5). The velocity also has an inertia term (*wv*) which preserves current velocity in a certain proportion. Parameters *w*, *c1*, *c2* and *Np* are user defined parameters, as well as *Kmax*, the maximum number of iterations (k) of the algorithm. The information of the objective function and constraints is provided in each iteration in matrices *p* and *q* which preserve good quality individuals (more feasible, more optimal). 



### Algorithm

Pseudocode:
```sh
1- Distribute the particles randomly in the search space with a random velocity value.
2- loop:
    1- Calculate the objective function at the position of the particle
    2- Find the particle with the best position
    3- Update the social values of the swarm
    4- Update the particle velocity vector
    5- Move the particles to a new position
3- Return the position value of the particle with the smallest error in the calculation of the objective function
```

### Implementation

- [1 - Python](https://github.com/BHI-Research/Edu-PSO/tree/master/1-Python)
- [2 - Numpy](https://github.com/BHI-Research/Edu-PSO/tree/master/2-Numpy)
- [3 - C++](https://github.com/BHI-Research/Edu-PSO/tree/master/3-C%2B%2B)
- [4 - OpenMP](https://github.com/BHI-Research/Edu-PSO/tree/master/4-OpenMP)
- [5 - CUDA](https://github.com/BHI-Research/Edu-PSO/tree/master/5-CUDA)
- [6 - JavaScript](https://github.com/BHI-Research/Edu-PSO/tree/master/6-JavaScript)



[![BHI|Research Group](https://github.com/BHI-Research/Edu-PSO/blob/master/DEMO/logoBHI.png?raw=true)](https://bhi-research.github.io/)


