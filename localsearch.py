import sys
import copy
import util

# mueve los trabajos a la derecha llenando huequitos
def move_right(n, m, L, p, t, start, finish):
    for machine in reversed(range(m)):
        for job_idx in reversed(range(n)):
            if machine == m - 1 and job_idx == n - 1:
                # ultimo trabajo se deja quieto
                continue

            job, _ = t[machine][job_idx]
            duration = p[job][machine]

            max_finish = util.INF

            if machine < m - 1:
                max_finish = start[job][machine + 1]

            if job_idx == n - 1:
                # al ultimo trabajo de cada maquina
                # se le aplica solamente con el max_finish
                # solo debe garantizar que termina antes de que empieza en la sig
                _finish = util.finish_if(max_finish, duration, L)
                start[job][machine] = _finish - duration
                finish[job][machine] = _finish
                t[machine][job_idx] = (job, start)
            else:
                # cuadro con el siguiente en la posicion actual
                next_job, _ = t[machine][job_idx + 1]
                _finish = util.finish_if(start[next_job][machine], duration, L)
                _start = _finish - duration
                start[job][machine] = _start
                finish[job][machine] = _finish
                t[machine][job_idx] = _start

                # busco una mejor posicion
                for right_idx in reversed(range(job_idx + 2, n)):
                    left_job, _ = t[machine][right_idx - 1]
                    left_finish = finish[left_job][machine]

                    right_job, _ = t[machine][right_idx]
                    right_start = start[right_job][machine]

                    possible_finish = util.finish_if(right_start, duration, L)
                    possible_start = possible_finish - duration

                    if possible_finish <= max_finish and possible_start >= left_finish:
                        start[job][machine] = possible_start
                        finish[job][machine] = possible_finish
                        t[machine].insert(right_idx, (job, possible_start))
                        t[machine].pop(job_idx)
                        break

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
