INF = (1 << 30)

def lower_bound(n, m, L, p):
    lb = 0
    for k in range(m):
        cur = 0
        for j in range(n):
            cur += p[j][k]
        lb = max(lb, cur)
    return lb

def start_with_shift(start, duration, L):
    if start // L < (start + duration - 1) // L:
        return (start // L + 1) * L
    else:
        return start

def schedule_from_rcl(n, m, L, p, rcl):
    t = t_from(n, m, rcl)
    start, finish = schedule_from_t(n, m, L, p, t)
    return t, start, finish

def schedule_from_t(n, m, L, p, t):
    start = [[None] * m for _ in range(n)]
    finish = [[None] * m for _ in range(n)]

    for machine in range(m):
        for job_idx in range(n):
            job = t[machine][job_idx]
            duration = p[job][machine]

            _start = 0

            if job_idx > 0:
                prev_job = t[machine][job_idx - 1]
                _start = max(_start, finish[prev_job][machine])

            if machine > 0:
                _start = max(_start, finish[job][machine - 1])

            _start = start_with_shift(_start, duration, L)

            start[job][machine] = _start
            finish[job][machine] = _start + duration

    return start, finish

def rcl_from(n, m, t):
    rcl = []
    for k in range(m):
        for j in range(n):
            rcl.append(t[k][j])
    return rcl

def t_from(n, m, rcl):
    t = [[] for _ in range(m)]
    machines = [0] * n
    for job in rcl:
        t[machines[job]].append(job)
        machines[job] += 1
    return t

def get_z(n, m, t, finish):
    last_machine = m - 1
    last_job = t[last_machine][n - 1]
    return finish[last_job][last_machine]
