import copy

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

def optimal_schedule_from_rcl(n, m, L, p, rcl):
    t = [[] for _ in range(m)]
    start = [[None] * m for _ in range(n)]
    finish = [[None] * m for _ in range(n)]

    machines = [0] * n
    for job in rcl:
        machine = machines[job]

        min_start = 0
        duration = p[job][machine]

        if machine > 0:
            min_start = max(min_start, start_with_shift(finish[job][machine - 1], duration, L))

        n_jobs = len(t[machine])
        for job_idx in range(0, n_jobs + 1):
            max_finish = None

            if job_idx > 0:
                left_job = t[machine][job_idx - 1]
                left_finish = finish[left_job][machine]

                if min_start < left_finish:
                    min_start = start_with_shift(left_finish, duration, L)

            if job_idx < n_jobs:
                right_job = t[machine][job_idx]
                right_start = start[right_job][machine]
                max_finish = right_start
            else:
                max_finish = INF

            if min_start + duration < max_finish:
                t[machine].insert(job_idx, job)
                start[job][machine] = min_start
                finish[job][machine] = min_start + duration
                machines[job] += 1
                break

    return t, start, finish

def optimal_schedule_from_t(n, m, L, p, t):
    rcl = rcl_from(n, m, t)
    return optimal_schedule_from_rcl(n, m, L, p, rcl)    

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

def fake_move_left(n, m, L, p, t):
    return optimal_schedule_from_t(n, m, L, p, t)

def fake_move_right(n, m, L, p, t):
    pp, tt = copy.deepcopy((p, t))

    for job in range(n):
        pp[job].reverse()

    for machine in range(m):
        tt[machine].reverse()
    tt.reverse()

    tt, _, _ = optimal_schedule_from_t(n, m, L, pp, tt)

    for machine in range(m):
        tt[machine].reverse()
    tt.reverse()

    start, finish = schedule_from_t(n, m, L, p, tt)
    return tt, start, finish

def stupid_rcl(n, m):
    rcl = []
    for _ in range(m):
        for j in range(n):
            rcl.append(j)
    return rcl

def normalized_rcl(n, m, rcl):
    t = t_from(n, m, rcl)
    return rcl_from(n, m, t)
