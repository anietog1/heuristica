#! /usr/bin/python3

import util

def neh(n, m, L, p):
    chosen = []
    available = [job for job in range(n)]

    duration = [sum(p[job]) for job in range(n)]
    available.sort(key=lambda job: duration[job])

    while available:
        j = available.pop(0)

        minz = util.INF
        mini = len(chosen)

        for i in range(len(chosen) + 1):
            chosen.insert(i, j)

            rcl = [chosen[i] for _ in range(m) for i in range(len(chosen))]

            t = [[] * n for _ in range(m)]
            start = [[None] * m for _ in range(n)]
            finish = [[None] * m for _ in range(n)]

            machines = [0] * n
            tempz = 0

            for job in rcl:
                machine = machines[job]
                machines[job] += 1

                _start = 0

                if len(t[machine]) > 0:
                    prev_job = t[machine][-1]
                    _start = max(_start, finish[prev_job][machine])

                if machine > 0:
                    _start = max(_start, finish[job][machine - 1])

                _start = util.start_with_shift(_start, p[job][machine], L)

                start[job][machine] = _start
                finish[job][machine] = _start + p[job][machine]
                tempz = max(tempz, finish[job][machine])

            if tempz < minz:
                minz = tempz
                mini = i

            chosen.pop(i)

        chosen.insert(mini, j)

    rcl = [chosen[i] for _ in range(m) for i in range(len(chosen))]
    return rcl
