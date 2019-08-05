#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Задание 19.1a

Скопировать функцию send_show_command из задания 19.1
 и переделать ее таким образом,
чтобы обрабатывалось исключение, которое генерируется
при ошибке аутентификации на устройстве.

При возникновении ошибки, на стандартный поток вывода
 должно выводиться сообщение исключения.

Для проверки измените пароль на устройстве или в файле devices.yaml.
'''

from netmiko import ConnectHandler
import paramiko


def devices(src_yaml):
    import yaml
    with open(src_yaml, 'r') as f:
        devs = yaml.load(f)
        return devs


def send_show_command(DEVICE_PARAMS, COMMAND):

    print('Connection to device {}'.format(DEVICE_PARAMS['ip']))

    try:
        with ConnectHandler(**DEVICE_PARAMS) as ssh:
            ssh.enable()

            result = ssh.send_command(COMMAND)
            print(result)
    except paramiko.ssh_exception.AuthenticationException as e:
        print(e)


if __name__ == '__main__':
    command = 'sh ip int br'
    for DEVICE_PARAMS in devices('devices.yaml'):
        send_show_command(DEVICE_PARAMS, command)
