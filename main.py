import os
import pprint
import paramiko
import subprocess
from socket import gethostbyname

DEVNULL = subprocess.DEVNULL


def decorator(import_list_mt):
    print(f'Выберите действие:\n'
          f'Сортировка - [1] ::: '
          f'Доступность хостов - [2] ::: '
          f'Проверка настроек - [3] ::: '
          f'Применение настроек - [4] ::: '
          f'Импорт файла - [5]')
    select = input()
    if select == '1':
        print('Sort key:', end='')
        sort_import_f = sort_import_file(import_list_mt, input())
        pprint.pprint(sort_import_f)
        print('Выбрано:', len(sort_import_f), end='\n\n')
        return sort_import_f

    elif select == '2':
        host_av = host_availability(import_list_mt)
        print('Доступные хосты:')
        pprint.pprint(host_av)
        print('Недоступные хосты:', len(import_list_mt.keys() - host_av.keys()))
        if len(import_list_mt.keys() - host_av.keys()) != 0:
            pprint.pprint(import_list_mt.keys() - host_av.keys())
        print('Выбрано:', len(host_av), end='\n\n')
        return host_av

    elif select == '3':
        print('Введите команду:', end='')
        set_check = check_settings(import_list_mt, input())  # 'put [queue type get [find name=pcq-download-default] pcq-limit]' pcq_download
        pprint.pprint(set_check)
        print('Выбрано:', len(set_check), end='\n\n')
        return set_check

    elif select == '4':
        pass

    elif select == '5':
        import_list_default = import_file()  # Импорт и парсинг файла
        pprint.pprint(import_list_default)
        print('Выбрано:', len(import_list_default))
        return import_list_default


def import_file():
    listMT = {}
    print('Импортирование файла Addresses.CDB')
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
                        all_info_mt_ip_clear = 0  # Исключение PoE MT
            if all_info_mt_ip_clear != 0:
                listMT[note] = {'ip': all_info_mt_ip_clear}  # Заполнение словаря

            all_info_mt_ip_clear = ''
    return listMT


def host_availability(dict_filter):
    availability_dict = {}
    for data in dict_filter:
        # print(data)
        for data_ip in dict_filter[data].values():
            # print(data_ip)
            requesrt = subprocess.call(["ping", "-c", "1", data_ip], stdout=DEVNULL)
            if requesrt == 0:
                availability_dict[data] = {'ip': data_ip}
            # print(availability_dict)
    return availability_dict


def check_settings(host_dict, command):
    port = 22
    user = 'support'
    password = 'Zaq12wsx'
    data_out_dict = {}
    host_dict = host_availability(host_dict) # Проверка на доступность

    for data in host_dict:

        for data_ip in host_dict[data]:

            print(data_ip)
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print('mt', data, host_dict[data]['ip'], 'chenge')
            try:
                client.connect(hostname=host_dict[data]['ip'], username=user, password=password, port=port, banner_timeout=200, look_for_keys=False)
            except:
                print('Недоступен хост:', host_dict[data]['ip'],)
            stdin, stdout, stderr = client.exec_command(command)
            data_out = stdout.read() + stderr.read()
            client.close()


            data_out_dict[data] = {'ip': host_dict[data]['ip'], command: data_out.decode('utf-8')}

    return data_out_dict


def sort_import_file(import_dict, key):
    sort_dict = {}
    if key == '*':
        return import_dict

    key = key.split('*')

    if key[-1] == '':  # поиск при 'xxx*'
        for data in import_dict:
            if data[:len(key[0])] == key[0]:
                sort_dict[data] = import_dict[data]
    else:
        for data in import_dict:  # поиск при точном значении
            if data == key[0]:
                sort_dict[data] = import_dict[data]
    return sort_dict


print('Импортирование файла Addresses.CDB')
import_f = import_file()  # Импорт и парсинг файла
pprint.pprint(import_f)
print('Выбрано:', len(import_f))

while True:
    import_f = decorator(import_f)

