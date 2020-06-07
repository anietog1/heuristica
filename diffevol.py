#! /usr/bin/python3

import util, random, copy, constructivos, rw, localsearch

def fsolve(n, m, L, p, NS=20, generations=100, CR=0.4, F=0.5):
    P = [None] * NS
    zs = [None] * NS

    D = n * m

    for i in range(NS):
        gene = [random.random() for _ in range(D)]
        t = decode(n, m, gene)
        t, _, finish = util.optimal_schedule_from_t(n, m, L, p, t)
        P[i] = gene
        zs[i] = util.get_z(n, m, t, finish)

    for _ in range(generations):
        for j in range(NS):
            a = b = c = -1

            while a == b or a == c or b == c:
                a = random.randint(0, NS - 1)
                b = random.randint(0, NS - 1)
                c = random.randint(0, NS - 1)

            r = random.randint(0, D - 1)

            v = [None] * D
            for k in range(D):
                if random.random() < CR or k == r:
                    v[k] = P[c][k] + F * (P[a][k] - P[b][k])
                else:
                    v[k] = P[j][k]

            t = decode(n, m, v)
            t, _, finish = util.optimal_schedule_from_t(n, m, L, p, t)
            z = util.get_z(n, m, t, finish)

            if z < zs[j]:
                P[j] = v
                zs[j] = z

    bestgene = None
    bestz = util.INF
    for i in range(NS):
        if zs[i] < bestz:
            bestgene = P[i]
            bestz = zs[i]

    t = decode(n, m, bestgene)
    t, start, finish = util.optimal_schedule_from_t(n, m, L, p, t)
    z = util.get_z(n, m, t, finish)

    return t, start, finish

def decode(n, m, rclgene):
    gene = [[] for _ in range(m)]

    idx = 0
    for machine in range(m):
        for _ in range(n):
            gene[machine].append(rclgene[idx])
            idx = idx + 1

    t = [[] for _ in range(m)]

    for machine in range(m):
        order = [j for j in range(n)]
        order.sort(key=lambda j: gene[machine][j])
        t[machine] = order

    return t

if __name__ == '__main__':
    rw.execute(fsolve)
