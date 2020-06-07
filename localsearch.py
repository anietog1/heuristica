import util, copy, random

def vnd3levels(n, m, L, p, t, iters=10, swapratio=0.1):
    bestt = t
    beststart, bestfinish = util.schedule_from_t(n, m, L, p, bestt)
    bestz = util.get_z(n, m, bestt, bestfinish)

    swaps = int(n * m * swapratio) + 1

    level = 0
    for _ in range(iters):
        t, start, finish = copy.deepcopy((bestt, beststart, bestfinish))

        if level == 0:
            t, _, _ = util.fake_move_right(n, m, L, p, t)
        elif level == 1:
            for _ in range(swaps):
                machine = random.randint(0, m - 1)
                job = random.randint(0, n - 2)

                if finish[job + 1][machine] - start[job][machine] > p[job + 1][machine] + p[job][machine]:
                    t[machine][job + 1], t[machine][job] = t[machine][job], t[machine][job + 1]
        elif level == 2:
            for _ in range(swaps):
                machine = random.randint(0, m - 1)
                job1 = job2 = random.randint(0, n - 1)
                while job1 == job2: job2 = random.randint(0, n - 1)
                t[machine][job1], t[machine][job2] = t[machine][job2], t[machine][job1]

        t, _, finish = util.optimal_schedule_from_t(n, m, L, p, t)
        z = util.get_z(n, m, t, finish)

        if z <= bestz:
            bestt, beststart, bestfinish, bestz = t, start, finish, z

        if z >= bestz:
            level = (level + 1) % 3

    return bestt, beststart, bestfinish
