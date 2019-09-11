from __future__ import print_function
import random
import time
from utils import read_args,file_output
from functions import * 


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

    def evaluate(self, fn):

        self.err = fn(self.pos)
        if self.err < self.err_best:
            self.pos_best = self.pos.copy()
            self.err_best = self.err

    def update(self, bounds, pos_best_g, args):
        for i in range(self.dimensions):

            # Update Vel
            r1 = random.random()
            r2 = random.random()

            vel_cognitive = args.c1*r1*(self.pos_best[i]-self.pos[i])
            vel_social = args.c2*r2*(pos_best_g[i]-self.pos[i])
            self.vel[i] = args.w*self.vel[i]+vel_cognitive+vel_social

            # Update Pos
            self.pos[i] = self.pos[i]+self.vel[i]

            if self.pos[i] > bounds[i][1]:
                self.pos[i] = bounds[i][1]

            if self.pos[i] < bounds[i][0]:
                self.pos[i] = bounds[i][0]

################################################################


class PSO:
    def __init__(self,  args, bounds, x0=False):

        if x0:
            self.dimensions = len(x0)
        else:
            self.dimensions = len(bounds)

        self.err_best_g = -1
        self.pos_best_g = []
        self.swarm = []
        self.bounds = bounds
        self.n_particles = args.n

        for i in range(0,  self.n_particles):
            self.swarm.append(Particle(bounds, x0))

    def run(self, fn, args):
        i = 0
        while i < args.i:

            for j in range(self.n_particles):
                self.swarm[j].evaluate(fn)

                if self.swarm[j].err < self.err_best_g or self.err_best_g == -1:
                    self.pos_best_g = self.swarm[j].pos
                    self.err_best_g = self.swarm[j].err

            for j in range(self.n_particles):
                self.swarm[j].update(self.bounds, self.pos_best_g,args)

            if args.verbose:
                print("#", i+1, "\tBest Solution:\t ", self.err_best_g)

            i += 1

        return self.err_best_g


if __name__ == "__main__":

   
    initial = []
    bounds = []

    args = read_args()

    if args.fn == 1:
        fn = fn1
    else:
        print("ERROR : FUNCTION NOT FOUND")

    box_limit = [-args.box, args.box]

    for i in range(args.d):
        initial.append(args.x0)
        bounds.append(box_limit)

    pso = PSO(args, bounds)

    start = time.time()
    solution = pso.run(fn, args)
    t = (time.time() - start)

    print('\npso.run time: ',t*1000 , 'ms')
    print('*'*30)
    print('SOLUTION:\t', solution)
    print('*'*30)
    
    file_output(args,t,solution)
