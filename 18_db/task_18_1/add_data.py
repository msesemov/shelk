#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import yaml
import glob
import re
import os

dhcp_files = glob.glob('*_dhcp_snooping.txt')
db_filename = 'dhcp_snooping.db'

try:
    db_exists = os.path.exists(db_filename)
except NameError:
    print('База данных не существует. Перед добавлением данных, ее надо создать')

conn = sqlite3.connect(db_filename)

print('Добавляю данные в таблицу switches...')

with open('switches.yml', 'r') as f:
    switches = yaml.load(f)
    for switch, location in switches['switches'].items():
        try:
            with conn:
                query = '''insert into switches (hostname, location)
                           values (?, ?)'''
                conn.execute(query, [switch, location])
        except sqlite3.IntegrityError as e:
            print('При добавлении данных:', (switch, location), 'Возникла ошибка:', e)

regex_s = re.compile('(\S+\d+)_\S+\.txt')
regex_d = re.compile('(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)')

print('Добавляю данные в таблицу dhcp...')

result = []
for file in dhcp_files:
    sw = re.search(regex_s, file)
    with open(file) as data:
        for row in data:
            match = regex_d.search(row)
            if match:
                res = (*match.groups(), sw.group(1))
                result.append(res)
                try:
                    with conn:
                        query1 = '''insert into dhcp (mac, ip, vlan, interface, switch)
                                values (?, ?, ?, ?, ?)'''
                        conn.execute(query1, res)
                except sqlite3.IntegrityError as e:
                    print('При добавлении данных:', res, 'Возникла ошибка:', e)


conn.close()
