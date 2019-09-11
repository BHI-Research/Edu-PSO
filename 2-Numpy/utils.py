import argparse

def read_args():

    parser = argparse.ArgumentParser(description='Simple PSO Benchmark.')

    parser = argparse.ArgumentParser(
        "Extract features and prediction from every images")
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
    parser.add_argument('-d',  type=int, default=2, help="Dimensions")
    # i
    parser.add_argument('-i',  type=int, default=20, help="Iterations")
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

    return parser.parse_args()


def file_output(args,t,solution):
    
    f = open("output.txt","a")
    settings =  (vars(args))
    for a in settings:
        if (a != 'verbose' and a != 'file'):
            f.write (str(settings[a]))
            f.write ("\t")
    f.write (str(t))
    f.write ("\t")
    f.write (str(solution))
    f.write ("\n")
    
    
    