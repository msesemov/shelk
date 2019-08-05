#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Задание 19.1

Создать функцию send_show_command.

Функция подключается по SSH (с помощью netmiko) к одному устройству
 и выполняет указанную команду.

Параметры функции:
* device - словарь с параметрами подключения к устройству
* command - команда, которую надо выполнить

Функция возвращает строку с выводом команды.

Скрипт должен отправлять команду command на все устройства из файла
devices.yaml с помощью функции send_show_command.

'''

from netmiko import ConnectHandler


def devices(src_yaml):
    import yaml
    with open(src_yaml, 'r') as f:
        devs = yaml.load(f)
        return devs


def send_show_command(DEVICE_PARAMS, COMMAND):

    print('Connection to device {}'.format(DEVICE_PARAMS['ip']))

    with ConnectHandler(**DEVICE_PARAMS) as ssh:
        ssh.enable()

        result = ssh.send_command(COMMAND)
        print(result)


if __name__ == '__main__':
    command = 'sh ip int br'
    for DEVICE_PARAMS in devices('devices.yaml'):
        send_show_command(DEVICE_PARAMS, command)
