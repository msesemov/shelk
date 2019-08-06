#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Задание 19.2a

Скопировать функцию send_config_commands из задания 19.2 и добавить параметр verbose,
который контролирует будет ли выводится на стандартный поток вывода
информация о том к какому устройству выполняется подключение.

verbose - это параметр функции send_config_commands, не параметр ConnectHandler!

По умолчанию, результат должен выводиться.

Пример работы функции:

In [13]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...

In [14]: result = send_config_commands(r1, commands, verbose=False)

In [15]:

Скрипт должен отправлять список команд commands на все устройства из файла devices.yaml с помощью функции send_config_commands.
'''

import netmiko
import paramiko


def devices(src_yaml):
    import yaml
    with open(src_yaml, 'r') as f:
        devs = yaml.load(f)
        return devs


def send_config_commands(device, config_commands, verbose=False):
    print('Connection to device {}'.format(device['ip']))
    try:
        if not verbose:
            with netmiko.ConnectHandler(**device) as ssh:
                ssh.enable()

                result = ssh.send_config_set(config_commands)
                return result
        else:
            device.update({'verbose': True})
            with netmiko.ConnectHandler(**device, ) as ssh:

                ssh.enable()

                result = ssh.send_config_set(config_commands)
                return result
    except paramiko.ssh_exception.AuthenticationException as e:
        return e
    except netmiko.ssh_exception.NetMikoTimeoutException as e:
        return e


if __name__ == '__main__':
    commands = [
        'logging 10.255.255.1', 'logging buffered 20010', 'no logging console'
    ]
    for DEVICE_PARAMS in devices('devices.yaml'):
        print(send_config_commands(DEVICE_PARAMS, commands, True))
