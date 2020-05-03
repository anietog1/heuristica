#! /usr/bin/python3
import util
import random

def fsolve(n, m, L, p):
    rcl = [(job, 0) for job in range(n)] # (job, machine)
    t = [[] for _ in range(m)]
    finish = [[None] * m for _ in range(n)]

    while len(rcl) > 0:
        idx = random.randint(0, len(rcl) - 1)
        job, machine = rcl.pop(idx)
        if machine < m - 1:
            rcl.append((job, machine + 1))

        start = 0
        if len(t[machine]) > 0:
            prev_job, _ = t[machine][-1]
            start = max(start, finish[prev_job][machine])

        if machine > 0:
            start = max(start, finish[job][machine - 1])

        if start // L < (start + p[job][machine] - 1) // L:
            start = (start // L + 1) * L

        finish[job][machine] = start + p[job][machine]
        t[machine].append((job, start))
        print('trabajo %d en maquina %d inicia en %d y termina en %d' % (job + 1, machine + 1, start, finish[job][machine]))

    return t

if __name__ == '__main__':
    util.execute(fsolve)
