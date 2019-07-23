#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import glob

dhcp_files = glob.glob('*_dhcp_snooping.txt')
db_filename = 'dhcp_snooping.db'


def check_if_db(db_filename):
    import os
    try:
        db_exists = os.path.exists(db_filename)
    except NameError:
        print('База данных не существует. Перед добавлением данных, ее надо создать')
    return db_exists


def write_db_switches_from_yaml(src_yaml, db_filename):
    import yaml
    conn = sqlite3.connect(db_filename)
    print('Добавляю данные в таблицу switches...')
    with open(src_yaml, 'r') as f:
        switches = yaml.load(f)
        for switch, location in switches['switches'].items():
            try:
                with conn:
                    query = '''insert into switches (hostname, location)
                               values (?, ?)'''
                    values = [switch, location]
                    conn.execute(query, values)
            except sqlite3.IntegrityError as e:
                print('При добавлении данных:', values, 'Возникла ошибка:', e)
    conn.close()


def write_db_from_sh_dhcp(dhcp_files, db_filename):
    import re
    regex_s = re.compile('(\S+\d+)_\S+\.txt')
    regex_d = re.compile('(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)')
    conn = sqlite3.connect(db_filename)
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


if __name__ == '__main__':
    dhcp_files = glob.glob('*_dhcp_snooping.txt')
    db_filename = 'dhcp_snooping.db'
    if check_if_db(db_filename):
        write_db_switches_from_yaml('switches.yml', db_filename)
        write_db_from_sh_dhcp(dhcp_files, db_filename)
    else:
        print('База данных не существует. Перед добавлением данных, ее надо создать')
