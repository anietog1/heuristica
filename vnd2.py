#! /usr/bin/python3

import util, random, copy, constructivos, rw

def fsolve(n, m, L, p, iters=1000, swapratio=0.1, popratio=0.1, wastelimit=10):
    rcl = constructivos.neh(n, m, L, p)

    bestt = util.t_from(n, m, rcl)
    beststart, bestfinish = util.schedule_from_t(n, m, L, p, bestt)
    bestz = util.get_z(n, m, bestt, bestfinish)

    pops = int(n * m * popratio) + 1
    swaps = int(n * m * swapratio) + 1

    for _ in range(iters):
        t, start, finish = copy.deepcopy((bestt, beststart, bestfinish))

        for _ in range(swaps):
            machine = random.randint(0, m - 1)
            job = random.randint(0, n - 2)

            if finish[job + 1][machine] - start[job][machine] > p[job + 1][machine] + p[job][machine]:
                t[machine][job + 1], t[machine][job] = t[machine][job], t[machine][job + 1]

        start, finish = util.schedule_from_t(n, m, L, p, t)
        z = util.get_z(n, m, t, finish)

        if z < bestz:
            bestt, beststart, bestfinish, bestz = t, start, finish, z
        else:
            t, start, finish = copy.deepcopy((bestt, beststart, bestfinish))

            for _ in range(pops):
                machine = random.randint(0, m - 1)
                job_idx = random.randint(0, n - 2)
                job = t[machine].pop(job_idx)
                t[machine].append(job)

            start, finish = util.schedule_from_t(n, m, L, p, t)
            z = util.get_z(n, m, t, finish)

            if z < bestz:
                bestt, beststart, bestfinish, bestz = t, start, finish, z
            else:
                t, start, finish = copy.deepcopy((bestt, beststart, bestfinish))

                job1 = random.randint(0, n - 1)
                job2 = random.randint(0, n - 1)

                for machine in range(m):
                    for j in range(n):
                        if t[machine][j] == job1:
                            job1_idx = j
                        if t[machine][j] == job2:
                            job2_idx = j
                    t[machine][job1_idx], t[machine][job2_idx] = t[machine][job2_idx], t[machine][job1_idx]

                start, finish = util.schedule_from_t(n, m, L, p, t)
                z = util.get_z(n, m, t, finish)

                if z < bestz:
                    bestt, beststart, bestfinish, bestz = t, start, finish, z

    return bestt, beststart, bestfinish

if __name__ == '__main__':
    rw.execute(fsolve)
