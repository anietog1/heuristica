#! /usr/bin/python3
import util

# debe regresar t[k] = [(job, start)]
# trabajo j [job] es procesado en el tiempo start en la maquina k
# método:
# solo calcular Z, practicamente
# en el orden en que los dan los trabajos
def fsolve(n, m, L, p):
    t = [[] for _ in range(m)]
    finish = [[None] * m for _ in range(n)]

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

            if start // L < (start + p[j][k] - 1) // L:
                start = (start // L + 1) * L

            finish[j][k] = start + p[j][k]
            t[k].append((j, start))

    return t

if __name__ == '__main__':
    util.execute(fsolve)
