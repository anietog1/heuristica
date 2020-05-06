import sys
import copy
import util

def move_right(n, m, L, p, t, start, finish):
    for k in reversed(range(m)):
        prev_machine = None if k == 0 else t[k - 1]
        machine = t[k]
        next_machine = None if k == m - 1 else t[k + 1]

        for j in reversed(range(n)):
            # si hay espacio entre este y el siguiente, moverlo hasta el final
            # sin que quede cruzando un turno

            # después, para cada dos trabajos que aparezcan siguientes, ver si
            # hay un huequito en el que quepa

            # nota: debo garantizar que los finales de turno siempre están ocupados
            # entonces yo se que el trabajo anterior finalizó al final del turno actual o justo antes de mi
            job = machine[j]
            late_end = finish[j][k]

            if j < n - 1:
                late_end = None

def move_left(n, m, L, p, t, start, finish):
    # lo mismo de arriba pero garantizando que todo trabajo inicia en un turno o inmediatamente
    # después de otro
    pass

def swap(machine, job1, job2, n, m, L, p, t, start, finish):
    if machine == None or machine == -1:
        for k in range(m):
            t[k][job1], t[k][job2] = t[k][job2], t[k][job1]
    else:
        t[machine][job1], t[machine][job2] = t[machine][job2], t[machine][job1]

    util.update_for(n, m, L, p, t, start, finish)
