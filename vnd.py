#! /usr/bin/python3

import util, random, copy, constructivos, rw

def fsolve(n, m, L, p, iters=300, swapratio=0.1):
    rcl = constructivos.neh(n, m, L, p)

    bestt = util.t_from(n, m, rcl)
    beststart, bestfinish = util.schedule_from_t(n, m, L, p, bestt)
    bestz = util.get_z(n, m, bestt, bestfinish)

    swaps = int(n * m * swapratio) + 1

    level = 0
    for _ in range(iters):
        t, start, finish = copy.deepcopy((bestt, beststart, bestfinish))

        if level == 0:
            t, _, _ = util.fake_move_right(n, m, L, p, t)
            t, start, finish = util.fake_move_left(n, m, L, p, t)
            z = util.get_z(n, m, t, finish)
        elif level == 1:
            for _ in range(swaps):
                machine = random.randint(0, m - 1)
                job = random.randint(0, n - 2)

                if finish[job + 1][machine] - start[job][machine] > p[job + 1][machine] + p[job][machine]:
                    t[machine][job + 1], t[machine][job] = t[machine][job], t[machine][job + 1]

            t, start, finish = util.optimal_schedule_from_t(n, m, L, p, t)
            z = util.get_z(n, m, t, finish)
        elif level == 2:
            for _ in range(swaps):
                machine = random.randint(0, m - 1)
                job1 = random.randint(0, n - 2)
                job2 = random.randint(0, n - 2)
                t[machine][job1], t[machine][job2] = t[machine][job2], t[machine][job1]

            t, start, finish = util.optimal_schedule_from_t(n, m, L, p, t)
            z = util.get_z(n, m, t, finish)

        if z <= bestz:
            bestt, beststart, bestfinish, bestz = t, start, finish, z
        else:
            level = (level + 1) % 3

    return bestt, beststart, bestfinish

if __name__ == '__main__':
    rw.execute(fsolve)
