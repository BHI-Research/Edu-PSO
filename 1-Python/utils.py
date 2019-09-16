import argparse


def read_args():

    parser = argparse.ArgumentParser(description='Simple PSO Benchmark.')

    # w
    parser.add_argument('-w',  type=float, default=0.5,
                        help="Constant inertia weight")
    # c1
    parser.add_argument('-c1',  type=float, default=1.5,
                        help="Cognitive term weight")
    # c2
    parser.add_argument('-c2',  type=float, default=2.5,
                        help="Group term weight")
    # n
    parser.add_argument('-n',  type=int, default=50, help="Swarm size")
    # d
    parser.add_argument('-d',  type=int, default=10, help="Dimensions")
    # i
    parser.add_argument('-i',  type=int, default=50, help="Iterations")
    # box
    parser.add_argument('-box',  type=float, default=10.0, help="Box limit")
    # x0
    parser.add_argument('-x0',  type=float, default=5.0,
                        help="Swarm initial position")
    # fn
    parser.add_argument('-fn',  type=int, default=1, help="Cost function id")
    # loops
    parser.add_argument('-loops',  type=int, default=5,
                        help="Loops (Benchmark)")
    # Verbose
    parser.add_argument('--verbose',  action='store_true',
                        help="Enable partial prints")
    # File
    parser.add_argument('--file',  action='store_true',
                        help="Enable file output prints")
    # Benchmark
    # bench_flag
    parser.add_argument('-bench_flag',  type=int,
                        default=1, help="Value to test")
    # bench_step
    parser.add_argument('-bench_step',  type=float,
                        default=20, help="Benchmark step")
    # bench_start
    parser.add_argument('-bench_start',  type=float,
                        default=10.0, help="Benchmark start value")
    # bench_end
    parser.add_argument('-bench_end',  type=float, default=105.0,
                        help="Benchmark last value")
    # bench_name
    parser.add_argument('-bench_name',  type=str,
                        help="Benchmark name")

    
    return parser.parse_args()



def file_output(args, t, solution):

    f = open("output.txt", "a")
    settings = (vars(args))
    for a in settings:
        if (a != 'verbose' and a != 'file'):
            f.write(str(settings[a]))
            f.write("\t")
    f.write(str(t))
    f.write("\t")
    f.write(str(solution))
    f.write("\n")


def update_bench(args, u):

    value = args.bench_start + u * args.bench_step
    if args.bench_flag == 1:
        args.n = int(value)
        args.bench_name = "Particles"
    elif args.bench_flag == 2:
        args.d = int(value)
        args.bench_name = "Dimensions"
    elif args.bench_flag == 3:
        args.i = int(value)
        args.bench_name = "Iterations"
    elif args.bench_flag == 4:
        args.w = value
        args.bench_name = "W"
    elif args.bench_flag == 5:
        args.c1 = value
        args.bench_name = "C1"
    elif args.bench_flag == 6:
        args.c2 = value
        args.bench_name = "C2"
    elif args.bench_flag == 7:
        args.box = value
        args.bench_name = "Box"
    elif args.bench_flag == 8:
        args.loops = int(value)
        args.bench_name = "Loops"

    return args,value