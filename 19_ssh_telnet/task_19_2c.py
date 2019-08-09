#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Задание 19.2c

Скопировать функцию send_config_commands из задания 19.2b и переделать ее таким образом:

Если при выполнении команды возникла ошибка,
спросить пользователя надо ли выполнять остальные команды.

Варианты ответа [y]/n:
* y - выполнять остальные команды. Это значение по умолчанию, поэтому нажатие любой комбинации воспринимается как y
* n или no - не выполнять остальные команды

Функция send_config_commands по-прежнему должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками

Оба словаря в формате
* ключ - команда
* значение - вывод с выполнением команд

Проверить работу функции можно на одном устройстве.

Пример работы функции:

In [11]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...
Команда "logging 0255.255.1" выполнилась с ошибкой "Invalid input detected at '^' marker." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: y
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: n

In [12]: pprint(result)
({},
 {'logging': 'config term\n'
             'Enter configuration commands, one per line.  End with CNTL/Z.\n'
             'R1(config)#logging\n'
             '% Incomplete command.\n'
             '\n'
             'R1(config)#',
  'logging 0255.255.1': 'config term\n'
                        'Enter configuration commands, one per line.  End with '
                        'CNTL/Z.\n'
                        'R1(config)#logging 0255.255.1\n'
                        '                   ^\n'
                        "% Invalid input detected at '^' marker.\n"
                        '\n'
                        'R1(config)#'})

'''

import netmiko
import paramiko
import re


def devices(src_yaml):
    import yaml
    with open(src_yaml, 'r') as f:
        devs = yaml.safe_load(f)
        return devs


def send_config_commands(device, config_commands, verbose=False):
    template = '''Команда "{}" выполнилась с ошибкой "{}" на устройстве {}'''
    try:
        rex_err = r'#(.+)\n\s*\^?\n?%\s(\w+\s\w+\s?\w+)'
        rex_ok = r'#(.+)\n\w'

        if verbose:
            print('Connection to device {}'.format(device['ip']))

        with netmiko.ConnectHandler(**device) as ssh:
            ssh.enable()
            result = ssh.send_config_set(config_commands)
            match = re.finditer(rex_err, result)
            bad = {}
            good = {}
            if match:
                for m in match:
                    print(template.format(*m.groups(), device['ip']))
                    if_in = input('Продолжать выполнять команды? [y]/n:')
                    if if_in == 'n':
                        bad.update({m.groups()[0]: m.groups()[1]})
                        break
                    elif if_in == 'y' or not if_in:
                        bad.update({m.groups()[0]: m.groups()[1]})
            match = re.finditer(rex_ok, result)
            if match:
                for m in match:
                    if m.groups()[0] != 'end':
                        good.update({m.groups()[0]: None})
            return (good, bad)
    except paramiko.ssh_exception.AuthenticationException as e:
        return e
    except netmiko.ssh_exception.NetMikoTimeoutException as e:
        return e


if __name__ == '__main__':
    commands_with_errors = ['logging 0255.255.1', 'logging', 'i']
    correct_commands = ['logging buffered 20010', 'ip http server']
    commands = commands_with_errors + correct_commands
    for DEVICE_PARAMS in devices('devices.yaml'):
        print(send_config_commands(DEVICE_PARAMS, commands, True))
