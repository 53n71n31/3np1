import sys, getopt, bisect

helpstr = """3NP1 (2019)
NAME
    Recursively applies f(n) starting from given value n until specified
    value s is reached (or forever)

            / n/2   if n even
    f(n) = <
            \ g(n)  otherwise

    where 
        g(n) = 3*n+1    unless specified otherwise
        s = 1           unless 

USAGE
    python 3np1.py -n <value> [OPTIONS]

OPTIONS
    -h,     (this) help notes
    -n,     starting value    
    -i,     max. iteration number
    -p,     output iterated values, otherwise only stopping iteration
            count (i.e. upon reaching s or max iteration) is output
    -s,     specify stopping value, the recursion ends when this result
            is reached
    -e,     <string> specify g(n) in string form, e.g. "3*n+1". Use
            'n' for the iteration variable
    -m,     keep track of previously computed vaues, stop when cycle detected

EXAMPLES

    python 3np1.py -n 3
            Calculate Collatz sequence count for number 3

    python 3np1.py -n 3 -p
            Same as above, but prints the sequence

    python 3np1.py -n 7 -e "5*n+1" -s 5 -i 999
            Calculate and print 5*n+1 sequence for n = 7, iterating 
            max of 999 times and stopping when s = 5 is reached.
"""
def compute(n, dump, st, eq, dokeep=False, maxiter=None):
    i = 0
    vis = []
    while True:
        cycle = False
        if dokeep:
            l = len(vis)
            if l != 0:
                idx =  bisect.bisect_left(vis, n)
                if idx != l and vis[idx] == n:
                    cycle = True
            bisect.insort(vis, n)
        if (st and n == st) or cycle or (maxiter and i >= maxiter):
            sys.stdout.write("1\n" if (n == 1 and dump) else "\n")
            sys.stdout.flush()
            sys.stderr.write("%d iterations\n" % i)
            return
        if dump:
           sys.stdout.write("%d " % n) 
        n = n/2 if (n%2 == 0) else eval(eq)
        i += 1

def main():
    opts, args = getopt.getopt(sys.argv[1:], "pn:i:e:s:mh")
    dump = False
    n = None
    i = None
    e = "3*n+1"
    s = None
    keep = False
    for o, a in opts:
        if o == '-p':
            dump = True
        elif o == '-n':
            n = int(a)
        elif o == '-i':
            i = int(a)
        elif o == '-e':
            e = a
        elif o == '-s':
            s = int(a)
        elif o == '-m':
            keep = True
        elif o == '-h':
            sys.stderr.write(helpstr)
            exit(0)
        else:
            sys.stderr.write("unknown option: %s\n" % o)    
            sys.exit(2)
    if n:
        compute(n, dump, s, e, keep, i)
    else:
        sys.stderr.write("missing input value!\n")

if __name__ == "__main__":
    main()
