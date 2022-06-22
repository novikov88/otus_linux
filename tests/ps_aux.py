from subprocess import run
from datetime import datetime


def get_information():
    list_parsed = []
    stdout = run_console('ps', 'aux').decode()
    command_string = stdout.split('\n')
    for string in command_string:
        string = string.split()
        while len(string) > 11:
            string[10] = string[10] + " " + string.pop()
        list_parsed.append(string)
    list_parsed.pop(0)
    list_parsed.pop(-1)

    users_list = get_users(list_parsed)
    count_processes = get_number_of_processes(list_parsed)
    user_processes = get_user_processes(list_parsed)
    total_memory_used = get_memory(list_parsed)
    total_cpu = get_total_cpu(list_parsed)
    max_memory_process = get_max_memory_process(list_parsed)
    max_cpu_process = get_max_cpu_process(list_parsed)

    show_report(users_list, count_processes, user_processes, total_memory_used, total_cpu, max_memory_process,
                max_cpu_process)

    save_report(users_list, count_processes, user_processes, total_memory_used, total_cpu, max_memory_process,
                max_cpu_process)


def run_console(command, key):
    return run([command, key], capture_output=True).stdout


def get_users(list_parsed):
    users_list = []
    for user in list_parsed:
        if user[0] not in users_list:
            users_list.append(user[0])
    return users_list


def get_number_of_processes(list_parsed):
    count_processes = len(list_parsed)
    return count_processes


def get_user_processes(list_parsed):
    user_processes = {}
    for user in list_parsed:
        if user[0] not in user_processes:
            user_processes[user[0]] = 1
        else:
            user_processes[user[0]] += 1
    return user_processes


def get_memory(list_parsed):
    total_memory_used = 0
    for value in list_parsed:
        total_memory_used += float(value[5])
    return format((total_memory_used / 1024), '.2f')


def get_total_cpu(list_parsed):
    total_cpu = 0.0
    for value in list_parsed:
        total_cpu += float(value[2])
    return format(total_cpu, '.2f')


def get_max_memory_process(list_parsed):
    memory_list = [0]
    for value in list_parsed:
        if float(value[5]) > float(memory_list[0]):
            memory_list.clear()
            memory_list.append(value[5])
            memory_list.append(value[10])
    return memory_list[1]


def get_max_cpu_process(list_parsed):
    cpu_list = [0]
    for value in list_parsed:
        if float(value[2]) > float(cpu_list[0]):
            cpu_list.clear()
            cpu_list.append(value[2])
            cpu_list.append(value[10])
    return cpu_list[1]


def show_report(users_list, count_processes, user_processes, total_memory_used, total_cpu, max_memory_process,
                max_cpu_process):
    print('Отчёт о состоянии системы:')
    print('Пользователи системы: ', end='')
    for user in range(len(users_list) - 1):
        print(users_list[user], end=', ')
    print(users_list[-1])
    print('Процессов запущено:', count_processes)
    print('Пользовательских процессов:')
    for v, k in user_processes.items():
        print(v + ':', k)
    print('Всего памяти используется:', total_memory_used, 'mb')
    print('Всего CPU используется:', total_cpu, '%')
    print('Больше всего памяти использует:', max_memory_process[:20])
    print('Больше всего CPU использует:', max_cpu_process[:20])


def save_report(users_list, count_processes, user_processes, total_memory_used, total_cpu, max_memory_process,
                max_cpu_process):
    filename = datetime.now().strftime("%d-%m-%Y-%H:%M:%S-scan.txt")
    print('Отчет сохранен в файл', filename)
    with open(filename, 'w') as filename:
        filename.write('Отчёт о состоянии системы:\n')
        filename.write('Пользователи системы: ')
        for user in range(len(users_list) - 1):
            filename.write(str(users_list[user]) + ', ')
        filename.write(str(users_list[-1]) + '\n')
        filename.write('Процессов запущено: ' + str(count_processes) + '\n')
        filename.write('Пользовательских процессов:' + '\n')
        for v, k in user_processes.items():
            filename.write(str(v) + ': ' + str(k) + '\n')
        filename.write('Всего памяти используется: ' + str(total_memory_used) + ' mb' + '\n')
        filename.write('Всего CPU используется: ' + str(total_cpu) + ' %' + '\n')
        filename.write('Больше всего памяти использует: ' + str(max_memory_process) + '\n')
        filename.write('Больше всего CPU использует: ' + str(max_cpu_process) + '\n')


get_information()
