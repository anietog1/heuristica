#! /usr/bin/python3
import util
import random
import stupid
import math
import random
import localsearch
import copy

# método:
# hacer left -> right, si mejora, melo
# si no hacer swaps, por ahí 3, si mejora, melo
# si tampoco mejora hacer un gran swap de trabajos en todas las máquinas
def fsolve(n, m, L, p, iters = 10000, swaps = 2):
    bestt = stupid.fsolve(n, m, L, p)
    beststart, bestfinish = util.start_finish_for(n, m, L, p, bestt)
    bestz = util.get_z(n, m, L, p, bestt, beststart, bestfinish)

    for _ in range(iters):
        t, start, finish = copy.deepcopy((bestt, beststart, bestfinish))

        localsearch.move_right(n, m, L, p, t, start, finish)
        localsearch.move_left(n, m, L, p, t, start, finish)

        z = util.get_z(n, m, L, p, t, start, finish)

        if z < bestz:
            bestt, beststart, bestfinish = t, start, finish
            bestz = z
            continue

        for _ in range(swaps):
            machine = random.randint(0, m - 1)
            job1 = random.randint(0, n - 1)
            job2 = random.randint(0, n - 1)
            localsearch.swap_in_machine(machine, job1, job2, n, m, L, p, t, start, finish)

        z = util.get_z(n, m, L, p, t, start, finish)

        if z < bestz:
            bestt, beststart, bestfinish = t, start, finish
            bestz = z
            continue

        job1 = random.randint(0, n - 1)
        job2 = random.randint(0, n - 1)
        localsearch.swap_jobs(job1, job2, n, m, L, p, t, start, finish)

        z = util.get_z(n, m, L, p, t, start, finish)

        if z < bestz:
            bestt, beststart, bestfinish = t, start, finish
            bestz = z
            continue

    return t

if __name__ == '__main__':
    util.execute(fsolve)
