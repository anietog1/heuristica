#! /usr/bin/env python

print('n,m,L,micros,ms,z,lb,percent')
for i in range(1, 120):
    txt = open('./samples/FSSPSC_{}.txt'.format(i), 'r')
    data = open('./samples/FSSPSC_{}.data'.format(i), 'r')
    n, m, L = next(txt).split()
    micros, ms = next(data).split()
    z, lb, percent = next(data).split()
    z = int(z)
    lb = int(lb)
    percent = float(percent)
    print('{},{},{},{},{},{},{},{}'.format(n, m, L, micros, ms, z, lb, percent))