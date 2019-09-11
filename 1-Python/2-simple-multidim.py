from __future__ import print_function
import random
import time
from functions import * 


w = 0.5
c1 = 1.5
c2 = 2.5

verbose=False


                
################################################################
class Particle:
    def __init__(self, bounds, x0=False):
        self.pos = []
        self.vel = []
        self.err_best = 100.0  # max
        self.err = -1
        self.bounds = bounds

        if x0:
            self.dimensions = len(x0)
            for i in range(0, self.dimensions):
                self.pos.append(x0[i])
        else:
            self.dimensions = len(bounds)
            for i in range(0, self.dimensions):
                self.pos.append(random.uniform(bounds[i][0], bounds[i][1]))
                
        for i in range(0, self.dimensions):
            self.vel.append(random.uniform(-1, 1))
            

        self.pos_best = self.pos
       

    def evaluate(self,fn):

        self.err = fn(self.pos)
        if self.err < self.err_best:
            self.pos_best = self.pos.copy()
            self.err_best = self.err

    def update(self, bounds, pos_best_g):
        for i in range(self.dimensions):

            # Update Vel
            r1 = random.random()
            r2 = random.random()
            
            vel_cognitive = c1*r1*(self.pos_best[i]-self.pos[i])
            vel_social = c2*r2*(pos_best_g[i]-self.pos[i])
            self.vel[i] = w*self.vel[i]+vel_cognitive+vel_social
            
            # Update Pos
            self.pos[i] = self.pos[i]+self.vel[i]

            if self.pos[i] > bounds[i][1]:
                self.pos[i] = bounds[i][1]

            if self.pos[i] < bounds[i][0]:
                self.pos[i] = bounds[i][0]

################################################################


class PSO:
    def __init__(self,  n_particles, bounds,x0=False):

        if x0:
            self.dimensions = len(x0)    
        else:
            self.dimensions = len(bounds)
        
        self.err_best_g = -1
        self.pos_best_g = []
        self.swarm = []
        self.bounds = bounds
        self.n_particles = n_particles

        for i in range(0, n_particles):
            self.swarm.append(Particle(bounds,x0))

    def run(self, fn, max_iters):
        i = 0
        while i < max_iters:

            for j in range( self.n_particles):
                self.swarm[j].evaluate(fn)

                if self.swarm[j].err < self.err_best_g or self.err_best_g == -1:
                    self.pos_best_g = self.swarm[j].pos
                    self.err_best_g = self.swarm[j].err

            for j in range(self.n_particles):
                self.swarm[j].update(self.bounds, self.pos_best_g)

            
            if verbose:
                print ("#",i+1,"\tBest Solution:\t ",self.err_best_g)

            i += 1

        return self.err_best_g
    


if __name__ == "__main__":


    dimensions = 2
    box_limit= [-10.0, 10.0]
    x0 = 5.0
    initial=[]               
    bounds=[]  
    
    for i in range(dimensions):
        initial.append(x0)
        bounds.append(box_limit)
        
    n_particles=5
    pso = PSO( n_particles, bounds )
    
    start = time.time()
    solution=pso.run(fn1,20)
    
    print('\npso.run time: ' , (time.time() - start)*1000,'ms')       
    print('*'*30)
    print('SOLUTION:\t',solution)       
    print('*'*30)
    
