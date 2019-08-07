#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Задание 19.2b

Скопировать функцию send_config_commands из задания 19.2a и добавить проверку на ошибки.

При выполнении каждой команды, скрипт должен проверять результат на такие ошибки:
 * Invalid input detected, Incomplete command, Ambiguous command

Если при выполнении какой-то из команд возникла ошибка,
функция должна выводить сообщение на стандартный поток вывода с информацией
о том, какая ошибка возникла, при выполнении какой команды и на каком устройстве, например:
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1

Ошибки должны выводиться всегда, независимо от значения параметра verbose.
При этом, verbose по-прежнему должен контролировать будет ли выводиться сообщение:
Подключаюсь к 192.168.100.1...


Функция send_config_commands теперь должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками

Оба словаря в формате:
* ключ - команда
* значение - вывод с выполнением команд

Проверить работу функции можно на одном устройстве.


Пример работы функции send_config_commands:

In [16]: commands
Out[16]:
['logging 0255.255.1',
 'logging',
 'i',
 'logging buffered 20010',
 'ip http server']

In [19]: good, bad = result

In [20]: good.keys()
Out[20]: dict_keys(['logging buffered 20010', 'ip http server'])

In [21]: bad.keys()
Out[21]: dict_keys(['logging 0255.255.1', 'logging', 'i'])


Примеры команд с ошибками:
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#i
% Ambiguous command:  "i"
'''

# списки команд с ошибками и без:

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
        if not verbose:
            with netmiko.ConnectHandler(**device) as ssh:
                ssh.enable()
                result = ssh.send_config_set(config_commands)
                match = re.finditer(rex_err, result)
                bad = {}
                good = {}
                if match:
                    for m in match:
                        print(template.format(*m.groups(), device['ip']))
                        bad.update({m.groups()[0]: m.groups()[1]})
                match = re.finditer(rex_ok, result)
                if match:
                    for m in match:
                        if m.groups()[0] != 'end':
                            good.update({m.groups()[0]: None})
                return (good, bad)
        else:
            print('Connection to device {}'.format(device['ip']))
            device.update({'verbose': True})
            with netmiko.ConnectHandler(**device) as ssh:
                ssh.enable()
                result = ssh.send_config_set(config_commands)
                match = re.finditer(rex_err, result)
                bad = {}
                good = {}
                if match:
                    for m in match:
                        print(template.format(*m.groups(), device['ip']))
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
