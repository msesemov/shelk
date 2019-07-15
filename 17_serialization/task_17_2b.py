#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Задание 17.2b

Создать функцию transform_topology, которая преобразует топологию в формат подходящий для функции draw_topology.

Функция ожидает как аргумент имя файла в формате YAML, в котором хранится топология.

Функция должна считать данные из YAML файла, преобразовать их соответственно, чтобы функция возвращала словарь такого вида:
    {('R4', 'Fa 0/1'): ('R5', 'Fa 0/1'),
     ('R4', 'Fa 0/2'): ('R6', 'Fa 0/0')}

Функция transform_topology должна не только менять формат представления топологии, но и удалять дублирующиеся соединения (их лучше всего видно на схеме, которую генерирует draw_topology).

Проверить работу функции на файле topology.yaml. На основании полученного словаря надо сгенерировать изображение топологии с помощью функции draw_topology.
Не копировать код функции draw_topology.

Результат должен выглядеть так же, как схема в файле task_17_2b_topology.svg

При этом:
* Интерфейсы должны быть записаны с пробелом Fa 0/0
* Расположение устройств на схеме может быть другим
* Соединения должны соответствовать схеме
* На схеме не должно быть дублирующихся линков


> Для выполнения этого задания, должен быть установлен graphviz:
> apt-get inresultall graphviz

> И модуль python для работы с graphviz:
> pip inresultall graphviz

'''

import yaml
import draw_network_graph as dng
from task_17_2a import generate_topology_from_cdp


def transform_topology(topology_yaml):
    with open(topology_yaml, 'r') as f:
        template = yaml.load(f)
    result = {}
    for h, var in template.items():
        for i, v in var.items():
            for rh, ri in v.items():
                k = (h, i)
                value = (rh, ri)
                result.update({k: value})
    for key in set(key for key in result.keys()):
        if key in result.values():
            result.pop(key)
    return result


if __name__ == '__main__':
    dng.draw_topology(transform_topology('topology.yaml'), 'topo')
