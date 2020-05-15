#! /usr/bin/python3
import util
import random
import stupid
import math
import random
import copy
import localsearch

# método:
# agregar elementos disponibles aleatoriamente
def fsolve(n, m, L, p, T0 = 1000, TF = 1, r = 0.95, LL = 100):
    bestt = stupid.fsolve(n, m, L, p)
    beststart, bestfinish = util.start_finish_for(n, m, L, p, bestt)
    bestz = util.get_z(n, m, L, p, bestt, beststart, bestfinish)

    curt, curstart, curfinish = copy.deepcopy((bestt, beststart, bestfinish))
    curz = bestz

    T = T0
    while T > TF:
        for _ in range(LL):
            t, start, finish = copy.deepcopy((curt, curstart, curfinish))

            machine = random.randint(0, m - 1)
            job1 = job2 = random.randint(0, n - 1)
            while job1 == job2:
                job2 = random.randint(0, n - 1)

            localsearch.swap_in_machine(machine, job1, job2, n, m, L, p, t, start, finish)

            z = util.get_z(n, m, L, p, t, start, finish)
            d = curz - z

            if d < 0 or random.random() < math.exp(- d / T):
                curt, curstart, curfinish = t, start, finish
                curz = z

                if curz < bestz:
                    bestz, beststart, bestfinish = curz, curstart, curfinish
                    bestz = curz

        T = T * r

    return bestt

if __name__ == '__main__':
    util.execute(fsolve)
