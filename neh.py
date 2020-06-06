#! /usr/bin/python3

import util, random, copy, constructivos, rw

def fsolve(n, m, L, p):
    rcl = constructivos.neh(n, m, L, p)
    t, start, finish = util.schedule_from_rcl(n, m, L, p, rcl)
    return t, start, finish

if __name__ == '__main__':
    rw.execute(fsolve)
