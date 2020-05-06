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

# debugging. hay que ponerlo más bonito
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

# agenda en el orden indicado por rcl y retorna t, start, finish
# bien estándar
def schedule_in_order(rcl, n, m, L, p):
    t = [[] for _ in range(m)]
    start = [[None] * m for _ in range(n)]
    finish = [[None] * m for _ in range(n)]

    for job, machine in rcl:
        _start = 0

        if len(t[machine]) > 0:
            prev_job, _ = t[machine][-1]
            _start = max(_start, finish[prev_job][machine])

        if machine > 0:
            _start = max(_start, finish[job][machine - 1])

        _start = start_if(_start, p[job][machine], L)

        start[job][machine] = _start
        finish[job][machine] = _start + p[job][machine]
        t[machine].append((job, _start))

    return t, _start, finish

# calcula todos los datos dado el ordenamiento ya en t
# se ignora por completo el tiempo de inicio en t
def update_for(n, m, L, p, t, start, finish):
    for machine in range(m):
        for job_idx in range(n):
            job, _ = t[machine][job_idx]

            _start = 0

            if job_idx > 0:
                prev_job, _ = t[machine][job_idx - 1]
                _start = max(_start, finish[prev_job][machine])

            if machine > 0:
                _start = max(_start, finish[job][machine - 1])

            _start = start_if(_start, p[job][machine], L)

            start[job][machine] = _start
            finish[job][machine] = _start + p[job][machine]
            t[machine][job_idx] = (job, _start)

# calcula start y finish dadas las condiciones
def start_finish_for(n, m, L, p, t):
    start = [[None] * m for _ in range(n)]
    finish = [[None] * m for _ in range(n)]

    for machine_idx in range(m):
        for job_idx in range(n):
            job, st = t[machine_idx][job_idx]
            start[job][machine_idx] = st
            finish[job][machine_idx] = start[job][machine_idx] + p[job][machine_idx]

    return start, finish

# se asume todo ok
# se calcula el z dados los datos actuales
def get_z(n, m, L, p, t, start = None, finish = None):
    if start == None or finish == None:
        start, finish = start_finish_for(n, m, L, p, t)

    last_machine = m - 1
    last_job, _ = t[last_machine][-1]

    return finish[last_job][last_machine]
