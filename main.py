import paramiko
from socket import gethostbyname


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
                        break

            listMT[note] = {note: all_info_mt_ip_clear}  # Заполнение словаря

            all_info_mt_ip_clear = ''
    return listMT

def host_availability(host):
    try:
        if gethostbyname(host) == host:
            return '[ok]'
    except IOError:
        return '[host not available]'
    except:
        return '[host not available]'

def check_settings(host, command):
    port = 22
    user = 'support'
    password = 'support'

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=password, port=port)
    shell = client.invoke_shell()
    shell.send('queue type edit pcq-download-default pcq-rate \x01\0B 5m \x01\0f')
    #shell.send('\x01\0B 5m \x01\0f')




    client.close()
    #return data

print(check_settings('192.168.50.1', 'queue type edit pcq-download-default pcq-rate \n 25m \n'))
