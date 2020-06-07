#! /usr/bin/python3

import util
import random
import copy
import constructivos
import rw, localsearch

def fsolve(n, m, L, p, population_size=10, children_size=10, generations=100,
           max_cross=2,
           mutation_prob=0.5, mutation_factor=0.2,
           improvement_prob=0.2, iters=30, swapratio=0.1, level_limit=3):
    fcompare = lambda x: (lambda t, z: z) (*x)

    P = []

    for _ in range(population_size - 1):
        rcl = util.stupid_rcl(n, m)
        random.shuffle(rcl)
        t, _, finish = util.optimal_schedule_from_rcl(n, m, L, p, rcl)
        z = util.get_z(n, m, t, finish)
        P.append((t, z))

    neh_rcl = constructivos.neh(n, m, L, p)
    t, _, finish = util.optimal_schedule_from_rcl(n, m, L, p, neh_rcl)
    z = util.get_z(n, m, t, finish)
    P.append((t, z))

    P.sort(key=fcompare)

    for _ in range(generations):
        children = []

        for _ in range(children_size):
            p1 = p2 = random.randint(0, population_size - 1)
            while p1 == p2: p2 = random.randint(0, population_size - 1)

            p3 = p4 = random.randint(0, population_size - 1)
            while p3 == p4: p4 = random.randint(0, population_size - 1)

            p1, z1 = P[p1]
            p2, z2 = P[p2]

            if z2 < z1:
                p1 = p2
                z1 = z2

            p3, z3 = P[p3]
            p4, z4 = P[p4]
            if z4 < z3:
                p3 = p4
                z3 = z4

            c1, c2 = cross(n, m, p1, p3, max_cross)
            t1, _, finish1 = util.optimal_schedule_from_t(n, m, L, p, c1)
            t2, _, finish2 = util.optimal_schedule_from_t(n, m, L, p, c2)

            z1 = util.get_z(n, m, t1, finish1)
            z2 = util.get_z(n, m, t2, finish2)

            if z1 < z2:
                kid = t1
                zkid = z1
            else:
                kid = t2
                zkid = z2

            if random.random() < mutation_prob:
                mutate(n, m, kid, mutation_factor)

            if random.random() < improvement_prob:
                improve(n, m, L, p, kid, iters, swapratio, level_limit)

            kid, start, finish = util.optimal_schedule_from_t(n, m, L, p, kid)
            zkid = util.get_z(n, m, kid, finish)
            children.append((kid, zkid))

        P.extend(children)
        P.sort(key=fcompare)
        del P[population_size:]

        _, bestz = P[0]
        thezs = {bestz}

        for i in range(1, population_size):
            curt, curz = P[i]

            while curz in thezs:
                mutate(n, m, curt, mutation_factor)
                curt, start, finish = util.optimal_schedule_from_t(n, m, L, p, curt)
                curz = util.get_z(n, m, curt, finish)

            P[i] = (curt, curz)
            thezs.update({curz})

        P.sort(key=fcompare)

    t, _ = P[0]
    start, finish = util.schedule_from_t(n, m, L, p, t)
    return t, start, finish

def cross(n, m, p1, p2, max_cross=3):
    c1 = [None] * m
    c2 = [None] * m

    machine_start = random.randint(0, m - 1)
    machine_end = random.randint(machine_start, min(machine_start + max_cross, m) - 1)

    for i in range(0, m):
        if i <= machine_start and i <= machine_end:
            c1[i] = copy.deepcopy(p2[i])
            c2[i] = copy.deepcopy(p1[i])
        else:
            c1[i] = copy.deepcopy(p1[i])
            c2[i] = copy.deepcopy(p2[i])

    return c1, c2

def improve(n, m, L, p, t, iters, swapratio, level_limit):
    bestt = localsearch.vnd3levels(n, m, L, p, t, iters, swapratio, level_limit)
    for machine in range(m):
        t[machine] = bestt[machine]

def mutate(n, m, t, mutation_factor):
    nmutations = int(mutation_factor * n * m)
    for _ in range(nmutations):
        machine = random.randint(0, m - 1)
        job1 = random.randint(0, n - 1)
        job2 = random.randint(0, n - 1)
        while job1 == job2: job2 = random.randint(0, n - 1)
        t[machine][job1], t[machine][job2] = t[machine][job2], t[machine][job1]

if __name__ == '__main__':
    rw.execute(fsolve)
