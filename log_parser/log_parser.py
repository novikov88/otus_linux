import json
import os
import argparse
import re

parser = argparse.ArgumentParser(description="путь для директории")
parser.add_argument("-f", dest="path", default=os.path.expanduser("~/logs"), action='store', help="Path to logfile")
args = parser.parse_args()


def requests_count(agr_path, log_file):
    count_request = 0
    with open(agr_path + '/' + log_file) as log:
        for line in log:
            ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            if ip_match is not None:
                count_request += 1
        print("Общее количество запросов: ", count_request)
        return count_request


def count_number_of_methods(agr_path, log_file):
    dict_requests = {'GET': 0, 'POST': 0, 'PUT': 0, 'PATCH': 0, 'DELETE': 0, 'HEAD': 0, 'CONNECT': 0, 'OPTIONS': 0,
                     'TRACE': 0}
    with open(agr_path + '/' + log_file) as log:
        for line in log:
            ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            if ip_match is not None:
                method = re.search(r'\] \"(POST|GET|PUT|PATCH|DELETE|HEAD|CONNECT|OPTIONS|TRACE)', line)
                if method is not None:
                    method = method.groups()[0]
                    dict_requests[method] += 1
        print("Количество запросов по типам:", dict_requests)
        return dict_requests


def get_top_3_ip_addresses(agr_path, log_file):
    cont_requests = {}
    top_ip = {"1": {'ip': '', 'count': 0},
              "2": {'ip': '', 'count': 0},
              "3": {'ip': '', 'count': 0}}
    with open(agr_path + '/' + log_file) as log:
        for line in log:
            ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            if ip_match is not None:
                ip_match = ip_match.group()
                try:
                    cont_requests[ip_match] += 1
                except KeyError:
                    cont_requests[ip_match] = 1
        for i in range(3):
            ip = max(cont_requests, key=cont_requests.get)
            count = cont_requests.pop(ip)
            top_ip[f'{i + 1}']['ip'] = ip
            top_ip[f'{i + 1}']['count'] = count
        print("Топ 3 IP адресов, с которых были сделаны запросы:", top_ip)
        return top_ip


def top_3_longest_requests(agr_path, file_of_log):
    top_requests = {'1': {'request': '', 'url': '', 'ip': '', 'time': 0, 'date': []},
                    '2': {'request': '', 'url': '', 'ip': '', 'time': 0, 'date': []},
                    '3': {'request': '', 'url': '', 'ip': '', 'time': 0, 'date': []}}
    with open(agr_path + '/' + file_of_log) as log:
        for line in log:
            ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            time_r = re.search(r'\d+$', line)
            if ip_match is not None:
                ip_match = ip_match.group()
                if time_r is not None:
                    time_r = int(time_r.group())
                    url = line.split()[6]
                    request = line.split()[5]
                    date = line.split()[3] + line.split()[4]
                    for i in range(1, 4):
                        if time_r > top_requests[f'{i}']['time']:
                            if top_requests[f'{i}']['time'] != ip_match:
                                top_requests[f'{i}']['request'] = request[1:]
                                top_requests[f'{i}']['time'] = time_r
                                top_requests[f'{i}']['ip'] = ip_match
                                top_requests[f'{i}']['url'] = url
                                top_requests[f'{i}']['date'] = date
                                break
        print("Топ 3 самых долгих запроса:", top_requests)
        return top_requests


try:
    os.mkdir("results")
except FileExistsError:
    pass

if os.path.isfile(args.path):
    file = ""
    name = args.path.split("/")[:0:-1]
    with open(f"results/log_parser-{name[0]}.json", 'w') as result_file:
        json.dump(requests_count(args.path, file), result_file, indent=4)
        result_file.write(",\r\n")
        json.dump(count_number_of_methods(args.path, file), result_file, indent=2)
        result_file.write(",\r\n")
        json.dump(get_top_3_ip_addresses(args.path, file), result_file, indent=4)
        result_file.write(",\r\n")
        json.dump(top_3_longest_requests(args.path, file), result_file, indent=4)
else:
    for file in os.listdir(args.path):
        with open(f"results/log_parser-{file}.json", 'w') as result_file:
            json.dump(requests_count(args.path, file), result_file, indent=4)
            result_file.write(",\r\n")
            json.dump(count_number_of_methods(args.path, file), result_file, indent=2)
            result_file.write(",\r\n")
            json.dump(get_top_3_ip_addresses(args.path, file), result_file, indent=4)
            result_file.write(",\r\n")
            json.dump(top_3_longest_requests(args.path, file), result_file, indent=4)
