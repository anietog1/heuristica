import util

def neh(n, m, L, p):
    chosen = []
    available = [job for job in range(n)]

    duration = [calc_z(n, m, L, p, [job] * m) for job in range(n)]
    available.sort(key=lambda job: duration[job])

    while available:
        j = available.pop(0)

        minz = util.INF
        mini = len(chosen)

        for i in range(len(chosen) + 1):
            chosen.insert(i, j)
            tempz = calc_z(n, m, L, p, chosen)

            if tempz < minz:
                minz = tempz
                mini = i

            chosen.pop(i)
        chosen.insert(mini, j)

    rcl = [chosen[i] for _ in range(m) for i in range(n)]
    return rcl

def calc_z(n, m, L, p, chosen):
    t = [[] for _ in range(m)]
    start = [[None] * m for _ in range(n)]
    finish = [[None] * m for _ in range(n)]
    z = 0

    for job in chosen:
        for machine in range(m):
            _start = 0
            duration = p[job][machine]

            if len(t[machine]) > 0:
                prev_job = t[machine][-1]
                _start = max(_start, finish[prev_job][machine])

            if machine > 0:
                _start = max(_start, finish[job][machine - 1])

            _start = util.start_with_shift(_start, duration, L)

            t[machine].append(job)
            start[job][machine] = _start
            finish[job][machine] = _start + duration
            z = max(z, finish[job][machine])

    return z
