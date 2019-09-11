from __future__ import print_function
import random
import time
from utils import read_args, file_output
import matplotlib.pyplot as plt
from functions import *


################################################################


class Swarm:
    def __init__(self, args, bounds, x0=False):

        self.n = args.n
        self.pos = []
        self.vel = []

        self.err = []
        self.err_best = []

        if x0:
            self.dimensions = len(x0)
            for i in range(self.n):
                v = []
                x = []
                for j in range(self.dimensions):
                    v.append(random.uniform(-1, 1))
                    x.append(x0[j])
                self.vel.append(v)
                self.pos.append(x)
        else:
            self.dimensions = len(bounds)
            for i in range(self.n):
                v = []
                x = []
                self.err.append(float('inf'))
                self.err_best.append(float('inf'))
                for j in range(self.dimensions):
                    v.append(random.uniform(-1, 1))
                    x.append(random.uniform(bounds[j][0], bounds[j][1]))
                self.vel.append(v)
                self.pos.append(x)

        self.pos_best = self.pos
        self.bounds = bounds
        self.err_best_g = float('inf')
        self.pos_best_g = self.pos[0][0]

    def evaluate(self):

        for i in range(self.n):

            self.err[i] = fn1(self.pos[i])

    def update(self, args):

        for j in range(self.n):

            for i in range(self.dimensions):

                # Update Vel
                r1 = random.random()
                r2 = random.random()

                vel_cognitive = args.c1*r1*(self.pos_best[j][i]-self.pos[j][i])
                vel_social = args.c2*r2*(self.pos_best_g[i]-self.pos[j][i])
                self.vel[j][i] = args.w*self.vel[j][i]+vel_cognitive+vel_social

                # Update Pos
                self.pos[j][i] += self.vel[j][i]

                if self.pos[j][i] > self.bounds[i][1]:
                    self.pos[j][i] = self.bounds[i][1]

                if self.pos[j][i] < self.bounds[i][0]:
                    self.pos[j][i] = self.bounds[i][0]

    def run(self, args):
        i = 0
        while i < args.i:

            self.evaluate()

            for j in range(self.n):

                if self.err[j] < self.err_best_g:
                    self.pos_best_g = self.pos[j]
                    self.err_best_g = self.err[j]

            self.update(args)
            if args.verbose:
                print("#", i+1, "\tBest Solution:\t ", self.err_best_g)
            i += 1

        return self.err_best_g


if __name__ == "__main__":

    print("Running Benchmark... ")
    tuneSteps = 25
    tuneFrom = 25
    tuneTo = 2500
    tune = tuneFrom

    print("Tunning:\t", "Particles", "\nSteps:\t",
          tuneSteps, "\t(from,to)\t", tuneFrom, tuneTo)
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

    benchmark = []
    benchmark_min = []
    benchmark_max = []

    while tune <= tuneTo:
        args.n = tune
        total_t = []
        max_t = float('-inf')
        min_t = float('inf')
        for i in range(args.loops):
            pso = Swarm(args, bounds)
            start = time.time()
            solution = pso.run(args)
            t = (time.time() - start)
            if t < min_t:
                min_t = t
            if t > max_t:
                max_t = t
            total_t.append(t)

        benchmark.append(sum(total_t)/len(total_t))
        benchmark_min.append(min_t)
        benchmark_max.append(max_t)
        file_output(args, t, solution)

        tune += tuneSteps
        
    plt.plot(benchmark_min)
    plt.plot(benchmark)
    plt.plot(benchmark_max)
    
    plt.ylabel('Time')
    plt.show()