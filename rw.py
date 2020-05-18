import sys

def read_input(filename=None):
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

def write_output(n, m, t, start, filename=None):
    if filename:
        f = open(filename, 'w')
    else:
        f = sys.stdout

    for machine_idx in range(m):
        for job_idx in range(n):
            job = t[machine_idx][job_idx]
            f.write('%d\t%d\t' % (job, start[job][machine_idx]))
        f.write('\n')

    if f is not sys.stdout:
        f.close()

# ejecuta el método y hace las operaciones de entrada y salida
def execute(fsolve, input_filename=None, output_filename=None):
    n, m, L, p = read_input(input_filename)
    t, start, _ = fsolve(n, m, L, p)
    write_output(n, m, t, start, output_filename)
