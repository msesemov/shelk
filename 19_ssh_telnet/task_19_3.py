#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Задание 19.3

Создать функцию send_commands (для подключения по SSH используется netmiko).

Параметры функции:
* device - словарь с параметрами подключения к устройству, которому надо передать команды
* show - одна команда show (строка)
* config - список с командами, которые надо выполнить в конфигурационном режиме

В зависимости от того, какой аргумент был передан, функция вызывает разные функции внутри.
При вызове функции send_commands, всегда будет передаваться только один из аргументов show, config.

Далее комбинация из аргумента и соответствующей функции:
* show - функция send_show_command из задания 19.1
* config - функция send_config_commands из задания 19.2

Функция возвращает строку с результатами выполнения команд или команды.

Проверить работу функции:
* со списком команд commands
* командой command

Пример работы функции:

'''
import netmiko
import paramiko
import re


def devices(src_yaml):
    import yaml
    with open(src_yaml, 'r') as f:
        devs = yaml.safe_load(f)
    return devs


def send_show_command(device, COMMAND):

    print('Connection to device {}'.format(device['ip']))

    try:
        with netmiko.ConnectHandler(**device) as ssh:
            ssh.enable()

            result = ssh.send_command(COMMAND)
            return result
    except paramiko.ssh_exception.AuthenticationException as e:
        return e
    except netmiko.ssh_exception.NetMikoTimeoutException as e:
        return e


def send_config_commands(device, config_commands, verbose=False):
    template = '''Команда "{}" выполнилась с ошибкой "{}" на устройстве {}'''
    rex_err = r'#(.+)\n\s*\^?\n?%\s(\w+\s\w+\s?\w+)'
    rex_ok = r'#(.+)\n\w'

    if verbose:
        print('Connection to device {}'.format(device['ip']))

    try:
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


def send_commands(device, show_or_config):
    if isinstance(show_or_config, str):
        return send_show_command(device, show_or_config)
    else:
        return send_config_commands(device, show_or_config)


if __name__ == '__main__':
    commands = [
        'logging 10.255.255.1', 'logging buffered 20010', 'no logging console'
    ]
    command = 'sh clock'
    for DEVICE_PARAMS in devices('devices.yaml'):
        print(send_commands(DEVICE_PARAMS, commands))
