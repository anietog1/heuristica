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

            max_finish = util.get_z(n, m, L, p, t, start, finish)
            if machine < m - 1:
                max_finish = util.finish_if(start[job][machine + 1], duration, L)
            max_start = max_finish - duration

            last_job, _ = t[machine][-1]

            if job_idx == n - 1:
                # al ultimo trabajo de cada maquina
                # se le aplica solamente con el max_finish
                # solo debe garantizar que termina antes de que empieza en la sig
                start[job][machine] = max_start
                finish[job][machine] = max_finish
                t[machine][job_idx] = (job, max_start)
            elif finish[last_job][machine] <= max_start:
                # reviso si hay espacio entre el ultimo en esta maquina y el siguiente mio
                t[machine].append((job, max_start))
                t[machine].pop(job_idx)
            else:
                # cuadro con el siguiente en la posicion actual
                next_job, _ = t[machine][job_idx + 1]
                _finish = util.finish_if(start[next_job][machine], duration, L)
                _start = _finish - duration

                if _finish <= max_finish:
                    start[job][machine] = _start
                    finish[job][machine] = _finish
                    t[machine][job_idx] = (job, _start)
                elif max_finish <= start[next_job][machine]:
                    start[job][machine] = max_start
                    finish[job][machine] = max_finish
                    t[machine][job_idx] = (job, max_start)
                else:
                    # si no puedo ni pegarme al siguiente, no puedo hacer nada
                    continue

                # busco una mejor posicion
                for right_idx in reversed(range(job_idx + 2, n)):
                    left_job, _ = t[machine][right_idx - 1]
                    left_finish = finish[left_job][machine]

                    right_job, _ = t[machine][right_idx]
                    right_start = start[right_job][machine]

                    possible_finish = util.finish_if(right_start, duration, L)
                    possible_start = possible_finish - duration

                    if left_finish <= possible_start and possible_finish <= max_finish:
                        # encajo al final del huequito
                        start[job][machine] = possible_start
                        finish[job][machine] = possible_finish
                        t[machine].insert(right_idx, (job, possible_start))
                        t[machine].pop(job_idx)
                        break
                    elif left_finish <= max_start and max_finish <= right_start:
                        # no encajo justo al final, pero puedo acomodarme
                        start[job][machine] = max_start
                        finish[job][machine] = max_finish
                        t[machine].insert(right_idx, (job, max_start))
                        t[machine].pop(job_idx)
                        break

# mueve los trabajos a la izquierda llenando huequitos
def move_left(n, m, L, p, t, start, finish):
    for machine in range(m):
        for job_idx in range(n):
            job, _ = t[machine][job_idx]
            duration = p[job][machine]

            if machine == 0 and job_idx == 0:
                start[job][machine] = 0
                finish[job][machine] = duration
                t[machine][job_idx] = (job, 0)
                continue

            min_start = 0
            if machine > 0:
                min_start = util.start_if(finish[job][machine - 1], duration, L)
            min_finish = min_start + duration

            first_job, _ = t[machine][0]

            if job_idx == 0:
                start[job][machine] = min_start
                finish[job][machine] = min_finish
                t[machine][job_idx] = (job, min_start)
            elif start[first_job][machine] >= min_finish:
                start[job][machine] = min_start
                finish[job][machine] = min_finish
                t[machine].pop(job_idx)
                t[machine].insert(0, (job, min_start))
            else:
                prev_job, _ = t[machine][job_idx - 1]
                _start = util.start_if(finish[prev_job][machine], duration, L)
                _finish = _start + duration

                if min_start <= _start:
                    start[job][machine] = _start
                    finish[job][machine] = _finish
                    t[machine][job_idx] = (job, _start)
                elif finish[prev_job][machine] <= min_start:
                    start[job][machine] = min_start
                    finish[job][machine] = min_finish
                    t[machine][job_idx] = (job, min_start)
                else:
                    continue

                for left_idx in range(0, job_idx - 2):
                    left_job, _ = t[machine][left_idx]
                    left_finish = finish[left_job][machine]

                    right_job, _ = t[machine][left_idx + 1]
                    right_start = start[right_job][machine]

                    possible_start = util.start_if(left_finish, duration, L)
                    possible_finish = possible_start + duration

                    if possible_finish <= right_start and min_start <= possible_start:
                        start[job][machine] = possible_start
                        finish[job][machine] = possible_finish
                        t[machine].insert(left_idx + 1, (job, possible_start))
                        t[machine].pop(job_idx)
                        break
                    elif left_finish <= min_start and min_finish <= right_start:
                        start[job][machine] = min_start
                        finish[job][machine] = min_finish
                        t[machine].insert(left_idx + 1, (job, min_start))
                        t[machine].pop(job_idx)
                        break

# intercambia los trabajos con index job1, job2 en una maquina o en todas
def swap_in_machine(machine, job1, job2, n, m, L, p, t, start, finish):
    if machine == None or machine == -1:
        for k in range(m):
            t[k][job1], t[k][job2] = t[k][job2], t[k][job1]
    else:
        t[machine][job1], t[machine][job2] = t[machine][job2], t[machine][job1]

    util.update_for(n, m, L, p, t, start, finish)

# intercambia los trabajos j1, j2 en todas las máquinas
def swap_jobs(j1, j2, n, m, L, p, t, start, finish):
    for machine in t:
        j1_idx, j2_idx = None, None

        for j in range(n):
            job, _ = machine[j]

            if job == j1:
                j1_idx = j

            if job == j2:
                j2_idx = j

        machine[j1_idx], machine[j2_idx] = machine[j2_idx], machine[j1_idx]
    
    util.update_for(n, m, L, p, t, start, finish)
