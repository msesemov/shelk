#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Задание 21.1

Создать функцию generate_config.


Проверить работу функции на шаблоне templates/for.txt и данных из файла data_files/for.yml.

'''
from jinja2 import Environment, FileSystemLoader


def generate_config(template, data_dict):
    '''
    Параметры функции:
    * template - путь к файлу с шаблоном (например, "templates/for.txt")
    * data_dict - словарь со значениями, которые надо подставить в шаблон

    Функция должна возвращать строку с конфигурацией, которая была сгенерирована.
    '''
    env = Environment(loader=FileSystemLoader('templates'),
                        trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(template)
    return template.render(data_dict)

if __name__ == '__main__':
    data_d = {'id': 1,
            'name': 'R1',
            'vlans': ({10: 'data',
                        20: 'mgmt',
                        30: 'voice'}),
            'ospf': ({'network': '10.1.1.0 0.0.0.255',
                        'area': 0},
                    {'network': '10.1.2.0 0.0.0.255',
                        'area': 2})}
    print(generate_config('for.txt', data_d))