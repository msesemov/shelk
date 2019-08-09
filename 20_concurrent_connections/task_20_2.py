#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Задание 20.2

Создать функцию send_show_command_to_devices, которая отправляет
одну и ту же команду show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.2   YES NVRAM  up                    up
Ethernet0/1                10.1.1.1        YES NVRAM  administratively down down
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml
'''

from concurrent.futures import ThreadPoolExecutor, as_completed


def devices(src_yaml):
    import yaml
    with open(src_yaml, 'r') as f:
        devs = yaml.safe_load(f)
    return devs


def send_show_command_to_devices(device, COMMAND):
    try:
        with netmiko.ConnectHandler(**device) as ssh:
            ssh.enable()

            result = ssh.send_command(COMMAND)
            return result
    except paramiko.ssh_exception.AuthenticationException as e:
        return e
    except netmiko.ssh_exception.NetMikoTimeoutException as e:
        return e




def threads_conn(function, devices, limit=3):
    reachable = []
    unreachable = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future = [executor.submit(function, device)
                for device in devices]
        for f in as_completed(future):
            print(f.result())



if __name__ == '__main__':
    ip_list = []
    for DEVICE_PARAMS in devices('devices.yaml'):
        ip_list.append(DEVICE_PARAMS['ip'])
    print(threads_conn(send_show_command_to_devices, ip_list))
