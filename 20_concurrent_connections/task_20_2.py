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
import netmiko
import paramiko
from concurrent.futures import ThreadPoolExecutor, as_completed


def devices(src_yaml):
    import yaml
    with open(src_yaml, 'r') as f:
        devs = yaml.safe_load(f)
    return devs


def send_show_command_to_devices(devices, command, filename, limit=3):
    with open(filename, 'w+') as wfile:
        with ThreadPoolExecutor(max_workers=limit) as executor:
            future = [executor.submit(send_show_command, device)
                    for device in devices]
            for f in as_completed(future):
                    wfile.write(f.result())


def send_show_command(DEVICE_PARAMS, COMMAND='sh ip int br'):
    #print('Connection to device {}'.format(DEVICE_PARAMS['ip']))
    try:
        with netmiko.ConnectHandler(**DEVICE_PARAMS) as ssh:
            ssh.enable()
            prompt = '\n' + ssh.find_prompt() + COMMAND + '\n'
            result = prompt  + ssh.send_command(COMMAND)
            return result
    except paramiko.ssh_exception.AuthenticationException as e:
        return e
    except netmiko.ssh_exception.NetMikoTimeoutException as e:
        return e


if __name__ == '__main__':
    command = 'sh ip int br'
    send_show_command_to_devices(devices('devices.yaml'), command, 'output.txt')
