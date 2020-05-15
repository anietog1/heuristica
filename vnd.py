#! /usr/bin/python3
import util
import random
import stupid
import math
import random
import localsearch
import copy

# método:
# ejecuto n swaps
# o hago pop a n tareas y luego hago append
# o intercambio completamente las posiciones de dos tareas
def fsolve(n, m, L, p, iters = 1000, swapratio = 0.07, popratio = 0.07):
    bestt = stupid.fsolve(n, m, L, p)
    beststart, bestfinish = util.start_finish_for(n, m, L, p, bestt)
    bestz = util.get_z(n, m, L, p, bestt, beststart, bestfinish)

    curt, curstart, curfinish = copy.deepcopy((bestt, beststart, bestfinish))
    curz = bestz

    pops = int(n * m * popratio) + 1
    swaps = int(n * m * swapratio) + 1

    for _ in range(iters):
        t, start, finish = copy.deepcopy((curt, curstart, curfinish))

        for _ in range(swaps):
            machine = random.randint(0, m - 1)
            job1 = random.randint(0, n - 1)
            job2 = random.randint(0, n - 1)
            localsearch.swap_in_machine(machine, job1, job2, n, m, L, p, t, start, finish)

        z = util.get_z(n, m, L, p, t, start, finish)

        if z < bestz:
            bestt, beststart, bestfinish = t, start, finish
            bestz = z

            curt, curstart, curfinish = bestt, beststart, bestfinish
            curz = bestz
            continue

        for _ in range(pops):
            machine = random.randint(0, m - 1)
            job_idx = random.randint(0, n - 1)
            job, _ = t[machine].pop(job_idx)
            t[machine].append((job, -1))

        util.update_for(n, m, L, p, t, start, finish)
        z = util.get_z(n, m, L, p, t, start, finish)

        if z < bestz:
            bestt, beststart, bestfinish = t, start, finish
            bestz = z

            curt, curstart, curfinish = bestt, beststart, bestfinish
            curz = bestz
            continue

        job1 = random.randint(0, n - 1)
        job2 = random.randint(0, n - 1)
        localsearch.swap_jobs(job1, job2, n, m, L, p, t, start, finish)

        z = util.get_z(n, m, L, p, t, start, finish)

        if z < bestz:
            bestt, beststart, bestfinish = t, start, finish
            bestz = z

            curt, curstart, curfinish = bestt, beststart, bestfinish
            curz = bestz
            continue

        curt, curstart, curfinish = t, start, finish
        curz = z

    return bestt

if __name__ == '__main__':
    util.execute(fsolve)
