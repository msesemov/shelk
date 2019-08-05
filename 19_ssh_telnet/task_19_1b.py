#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Задание 19.1b

Скопировать функцию send_show_command из задания 19.1a и переделать ее таким образом,
чтобы обрабатывалось не только исключение, которое генерируется
при ошибке аутентификации на устройстве, но и исключение,
которое генерируется, когда IP-адрес устройства недоступен.

При возникновении ошибки, на стандартный поток вывода должно выводиться сообщение исключения.

Для проверки измените IP-адрес на устройстве или в файле devices.yaml.
'''
import netmiko
import paramiko


def devices(src_yaml):
    import yaml
    with open(src_yaml, 'r') as f:
        devs = yaml.load(f)
        return devs


def send_show_command(DEVICE_PARAMS, COMMAND):

    print('Connection to device {}'.format(DEVICE_PARAMS['ip']))

    try:
        with netmiko.ConnectHandler(**DEVICE_PARAMS) as ssh:
            ssh.enable()

            result = ssh.send_command(COMMAND)
            print(result)
    except paramiko.ssh_exception.AuthenticationException as a:
        print(a)
    except netmiko.ssh_exception.NetMikoTimeoutException as t:
        print(t)


if __name__ == '__main__':
    command = 'sh ip int br'
    for DEVICE_PARAMS in devices('devices.yaml'):
        send_show_command(DEVICE_PARAMS, command)
