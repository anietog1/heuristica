#! /usr/bin/python3

import util, random, copy, constructivos, rw, localsearch

def fsolve(n, m, L, p):
    rcl = util.stupid_rcl(n, m)
    t, start, finish = util.schedule_from_rcl(n, m, L, p, rcl)
    return t, start, finish

def cross(n, m, p1, p2, max_cross=3):
    pass

def improve(n, m, L, p, t, iters, swapratio, level_limit):
    bestt = localsearch.vnd3levels(n, m, L, p, t, iters, swapratio, level_limit)
    for machine in range(m):
        t[machine] = bestt[machine]

def mutate(n, m, t, mutation_factor):
    pass

if __name__ == '__main__':
    rw.execute(fsolve)
