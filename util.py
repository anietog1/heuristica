import sys

# lb = max sum of all jobs on machines
def lower_bound(n, m, L, p):
    lb = 0
    for k in range(m):
        cur = 0
        for j in range(n):
            cur += p[j][k]
        lb = max(lb, cur)
    return lb

# returns n, m, L, p. input filename = None
def read_input(filename = None):
    if filename:
        f = open(filename)
    else:
        f = sys.stdin

    n, m, L = [int(x) for x in f.readline().split('\t')]

    p = [None] * n
    for j in range(n):
        p[j] = [int(x) for x in f.readline().split('\t')[:-1]]

    if f is not sys.stdin:
        f.close()

    return n, m, L, p
