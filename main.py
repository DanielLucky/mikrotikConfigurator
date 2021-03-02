import os
import pprint
import paramiko
import subprocess
from socket import gethostbyname


DEVNULL = subprocess.DEVNULL

def import_file():
    listMT = {}
    with open('Addresses.CDB', 'r', encoding="cp866") as fileAddress:
        # print(fileAddress.read())
        all_info_mt_ip_clear = ''
        file = fileAddress.read().split('M2')
        print(len(file))

        for all_info_mt in file[1:]:
            all_info_mt_note = all_info_mt.split('!')[2]
            note = all_info_mt_note[1:-3].encode('cp866').decode('windows-1251')

            for all_info_mt_ip in tuple(all_info_mt.split('!')[7]):  # parse ip
                try:
                    if type(int(all_info_mt_ip)) == type(int()):
                        all_info_mt_ip_clear = all_info_mt_ip_clear + all_info_mt_ip
                except:
                    if all_info_mt_ip == '.':
                        all_info_mt_ip_clear = all_info_mt_ip_clear + all_info_mt_ip
                    elif all_info_mt_ip == ':':
                        all_info_mt_ip_clear = 0 # Исключение PoE MT
            if all_info_mt_ip_clear != 0:
                listMT[note] = {note: all_info_mt_ip_clear}  # Заполнение словаря

            all_info_mt_ip_clear = ''
    return listMT


def host_availability(dict_filter):
    availability_dict = {}
    for data in dict_filter:
        #print(data)
        for data_ip in dict_filter[data].values():
            #print(data_ip)
            requesrt = subprocess.call(["ping", "-c", "1", data_ip], stdout=DEVNULL)
            if requesrt == 0:
                availability_dict[data] = {data: data_ip}
            #print(availability_dict)
    return availability_dict


def check_settings(host_dict, command):
    port = 22
    user = 'support'
    password = 'Zaq12wsx'
    data_out_dict = {}
    for data in host_dict:
        for data_ip in host_dict[data].values():
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=data_ip, username=user, password=password, port=port)
            stdin, stdout, stderr = client.exec_command(command)
            data_out = stdout.read() + stderr.read()
            client.close()

            data_out_dict[data] = {data: host_dict[data], 'answer': data_out.decode('utf-8')[:-2]}
    return data_out_dict


def sort_import_file(import_dict, key):
    sort_dict = {}
    if key == '*':
        return import_dict

    key = key.split('*')

    if key[-1] == '': # поиск при 'xxx*'
        for data in import_dict:
            if data[:len(key[0])] == key[0]:
                sort_dict[data] = import_dict[data]
    else:
        for data in import_dict: # поиск при точном значении
            if data == key[0]:
                sort_dict[data] = import_dict[data]
    return sort_dict


print('Импортирование файла Addresses.CDB')
import_f = import_file() # Импорт и парсинг файла
pprint.pprint(import_f)
print(f'Выбрано: {len(import_f)} MT\n '
      f'Выберите действие\n'
      f'Сортировка - "1" ::: Доступность хостов - "2" ')
select = input()
if select == '1':
    pass



#print(sort_import_file(import_f, '*'))  # сортировка по ключу
# print('Sort key:')
# sort_import_f = sort_import_file(import_f, input())
# pprint.pprint(sort_import_f)
#
# # print(host_availability(sort_import_f), '\n ---------------')  # доступность хоста
# host_av = host_availability(sort_import_f)
# print('Доступные хосты:')
# pprint.pprint(host_av)
# print('Недоступные хосты:')
# pprint.pprint(sort_import_f.keys() - host_av.keys())

#print(check_settings(host_av, 'put [queue type get [find name=pcq-download-default] pcq-limit]'))
#check_set = check_settings(host_av, 'put [queue type get [find name=pcq-download-default] pcq-limit]')

# pprint.pprint(check_set, width=1)