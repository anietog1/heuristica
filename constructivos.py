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

            rcl = [[chosen[i]] * m for i in range(len(chosen))]
            t, start, finish = util.schedule_from_rcl(len(chosen), m, L, p, rcl)
            tempz = util.get_z(len(chosen), m, t, finish)

            if tempz < minz:
                minz = tempz
                mini = i

            chosen.pop(i)

        chosen.insert(mini, j)

    rcl = [[chosen[i]] * m for i in range(n)]
    return rcl
