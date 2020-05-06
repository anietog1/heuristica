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

def swap(job_machine1, job_machine2, n, m, L, p, t, start, finish):
    # básicamente hacer swap y calcular todo desde 0
    job1, machine1 = job_machine1
    job2, machine2 = job_machine2

    t[machine1][job1], t[machine2][job2] = t[machine2][job2], t[machine1][job1]

    for machine_idx in range(m):
        for job_idx in range(n):
            job, _ = t[machine_idx][job_idx]
            start = 0

            if job_idx > 0:
                prev_job, _ = t[machine_idx][job_idx - 1]
                start = max(start, finish[prev_job][machine_idx])

            if machine_idx > 0:
                start = max(start, finish[job][machine_idx - 1])

            start = util.start_if(start, p[job][machine_idx], L)

            start[job][machine_idx] = start
            finish[job][machine_idx] = start + p[job][machine_idx]
            t[machine_idx][job_idx] = (job, start)
