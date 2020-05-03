#! /usr/bin/python3
import util
import random

# método:
# agregar elementos disponibles aleatoriamente
def fsolve(n, m, L, p, tries = 500):
    bestz = 9999999999999999
    bestt = None

    for _ in range(tries):
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
        
        last_job, last_start = t[-1][-1]
        z = last_start + p[last_job][m - 1]

        if z < bestz:
            bestz = z
            bestt = t

    return bestt

if __name__ == '__main__':
    util.execute(fsolve)
