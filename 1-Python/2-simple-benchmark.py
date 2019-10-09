from __future__ import print_function
import random
import time
from utils import *
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

    def evaluate(self,fn):

        for i in range(self.n):

            self.err[i] = fn(self.pos[i])

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

    def run(self,fn, args):
        i = 0
        while i < args.i:

            self.evaluate(fn)

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
    args = read_args()

    print("Tunning:\t", args.bench_name, "\nSteps:\t",
          args.bench_step, "\t(from,to)\t", args.bench_start, args.bench_end)
    initial = []
    bounds = []

    
    if args.fn == 1:
        fn = fn1
    else:
        print("ERROR : FUNCTION NOT FOUND")

    box_limit = [-args.box, args.box]

    for i in range(args.d):
        initial.append(args.x0)
        bounds.append(box_limit)
        
    benchmark_t = []
    benchmark_t_min = []
    benchmark_t_max = []

    benchmark_s = []
    benchmark_s_min = []
    benchmark_s_max = []
    
    axis_x = []
    
    tune =  args.bench_start
    update = 0

    while tune <=  args.bench_end:
        
        args,tune=update_bench(args,update)
        update +=1
        axis_x.append(tune)

        total_t = []
        max_t = float('-inf')
        min_t = float('inf')

        total_s = []
        max_s = float('-inf')
        min_s = float('inf')
        for i in range(args.loops):
            pso = Swarm(args, bounds)
            start = time.time()
            solution = pso.run(fn,args)
            t = (time.time() - start)
            if t < min_t:
                min_t = t
            if t > max_t:
                max_t = t
            if solution < min_s:
                min_s = solution
            if solution > max_s:
                max_s = solution
            total_t.append(t)
            total_s.append(solution)

        benchmark_t.append(sum(total_t)/len(total_t))
        benchmark_t_min.append(min_t)
        benchmark_t_max.append(max_t)
        
        benchmark_s.append(sum(total_s)/len(total_s))
        benchmark_s_min.append(min_s)
        benchmark_s_max.append(max_s)

        file_output(args, t, solution)
        """
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
        """
       
        
    #Matlib Plot
    plt.subplot(2, 1, 1)
    plt.plot(axis_x,benchmark_t_min)
    plt.plot(axis_x,benchmark_t)
    plt.plot(axis_x,benchmark_t_max)
    plt.title('PSO ' + args.bench_name + ' vs Time')
    plt.ylabel('Time (ms)')
        
    plt.subplot(2, 1, 2)
    plt.plot(axis_x,benchmark_s_min)
    plt.plot(axis_x,benchmark_s)
    plt.plot(axis_x,benchmark_s_max)
    plt.ylabel('Error')
    plt.xlabel(args.bench_name)
           
    plt.show()