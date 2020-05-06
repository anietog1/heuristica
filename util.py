import sys

INF = 999999999

# lb = max(suma de todos los trabajos en 1 máquina)
def lower_bound(n, m, L, p):
    lb = 0
    for k in range(m):
        cur = 0
        for j in range(n):
            cur += p[j][k]
        lb = max(lb, cur)
    return lb

# chequea cuando iniciar según la longitud del turno y el t inicial
# duration <= L
def start_if(start, duration, L):
    if start // L < (start + duration - 1) // L:
        return (start // L + 1) * L
    else:
        return start

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

# t : [[(int, int)]] machines => jobs => (job, start)
# filename = None => stdout
def write_output(t, filename = None):
    if filename:
        f = open(filename, 'w')
    else:
        f = sys.stdout

    for machine in t:
        for job, start in machine:
            f.write('%d\t%d\t' % (job + 1, start))
        f.write('\n')

    if f is not sys.stdout:
        f.close()

# ejecuta el método y hace las operaciones de entrada y salida
def execute(fsolve, input_filename = None, output_filename = None):
    n, m, L, p = read_input(input_filename)
    t = fsolve(n, m, L, p)
    write_output(t, output_filename)

def debug(n, m, L, p, t, start, finish):
    print('[DEBUG]')
    print('n: %d m: %d L: %d' % (n, m, L))
    print('p:')
    print(p)
    print('t:')
    print(t)
    print('start:')
    print(start)
    print('finish:')
    print(finish)
