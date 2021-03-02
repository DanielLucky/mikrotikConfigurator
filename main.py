import paramiko
from socket import gethostbyname


def import_file():
    listMT = {}
    with open('Addresses.cdb', 'r', encoding="cp866") as fileAddress:
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
                        break

            listMT[note] = {note: all_info_mt_ip_clear}  # Заполнение словаря

            all_info_mt_ip_clear = ''
    return listMT


def host_availability(dict_filter):
    pass


def check_settings(host, command):
    port = 22
    user = 'admin'
    password = ''

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=password, port=port)
    stdin, stdout, stderr = client.exec_command(command)
    data = stdout.read() + stderr.read()
    client.close()

    return data


def sort_import_file(import_dict, key):
    if key != '*':
        for date_key in import_dict:
            if date_key == key:
                dict_fit = {date_key: import_dict[date_key]}
            else:
                dict_no_fit = {date_key: import_dict[date_key]}  # словарь не подходящих по фильтру
        return dict_fit
    else:
        return import_dict




print(import_file(), '\n ---------------')  # Импорт и парсинг файла
import_f = import_file()

print(sort_import_file(import_f, '*'), '\n ---------------')  # сортировка по ключу
sort_import_f = sort_import_file(import_f, '*')

print(host_availability(sort_import_f))  # доступность хоста
