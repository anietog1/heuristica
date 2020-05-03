#! /usr/bin/python3
import util

# debe regresar t[k] = [(job, start)]
# trabajo j [job] es procesado en el tiempo start en la maquina k
def fsolve(n, m, L, p):
    t = [None] * m
    for k in range(m):
        t[k] = []
    finish = [[None] * m] * n

    for j in range(n):
        for k in range(m):
            start = None

            if k > 0 and j > 0:
                start = max(finish[j][k - 1], finish[j - 1][k])
            elif k > 0 and j == 0:
                start = finish[j][k - 1]
            elif k == 0 and j > 0:
                start = finish[j - 1][k]
            elif k == 0 and j == 0:
                start = 0

            if start // L < (start + p[j][k]) // L:
                start = (start // L + 1) * L

            finish[j][k] = start + p[j][k]
            t[k].append((j, start))

    return t

if __name__ == '__main__':
    util.execute(fsolve)
