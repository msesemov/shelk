#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Задание 21.5a

Создать функцию configure_vpn, которая использует шаблоны из задания 21.5 для настройки VPN на маршрутизаторах на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству
* dst_device_params - словарь с параметрами подключения к устройству
* src_template - имя файла с шаблоном, который создает конфигурацию для одной строны туннеля
* dst_template - имя файла с шаблоном, который создает конфигурацию для второй строны туннеля
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов и данных на каждом устройстве.
Функция возвращает вывод с набором команд с двух марушртизаторов (вывод, которые возвращает send_config_set).

При этом, в словаре data не указан номер интерфейса Tunnel, который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel, взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 9.
И надо будет настроить интерфейс Tunnel 9.

Для этого задания нет теста!
'''

from jinja2 import Environment, FileSystemLoader
import netmiko
import paramiko
import re


def send_show_command(device, command):
    try:
        with netmiko.ConnectHandler(**device) as ssh:
            ssh.enable()

            result = ssh.send_command(command)
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


def configure_vpn(src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict):
    intf1 = send_show_command(src_device_params, 'show ip int brief')
    intf2 = send_show_command(dst_device_params, 'show ip int brief')
    env = Environment(loader=FileSystemLoader('templates'),
                        trim_blocks=True, lstrip_blocks=True)
    src_template = env.get_template(src_template)
    dst_template = env.get_template(dst_template)
    regex = r'[Tt]unnel(\d+)\s'
    match1 = re.finditer(regex, intf1)
    match2 = re.finditer(regex, intf2)
    tunnels_set = set()
    for m in match1:
        num = int(m.group(1))
        tunnels_set.add(num)
    for m in match2:
        num = int(m.group(1))
        tunnels_set.add(num)
    if len(tunnels_set) == 0:
        vpn_data_dict['tun_num'] = 0
    else:
        tunnels_list = list(tunnels_set)
        next_tunn = tunnels_list[-1] + 1
        vpn_data_dict['tun_num'] = next_tunn
    src = send_config_commands(src_device_params, src_template.render(vpn_data_dict))
    dst = send_config_commands(dst_device_params, dst_template.render(vpn_data_dict))
    return [src, dst]

if __name__ == '__main__':

    data = {
        'tun_num': None,
        'wan_ip_1': '192.168.100.1',
        'wan_ip_2': '192.168.100.2',
        'tun_ip_1': '10.0.1.1 255.255.255.252',
        'tun_ip_2': '10.0.1.2 255.255.255.252'
    }
    src_dev = {'device_type': 'cisco_ios',
                'ip': '192.168.100.1',
                'username': 'cisco',
                'password': 'cisco',
                'secret': 'cisco'}
    dst_dev = {'device_type': 'cisco_ios',
                'ip': '192.168.100.2',
                'username': 'cisco',
                'password': 'cisco',
                'secret': 'cisco'}

    print(configure_vpn(src_dev, dst_dev, 'gre_ipsec_vpn_1.txt' , 'gre_ipsec_vpn_2.txt', data))
