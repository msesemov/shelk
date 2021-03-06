#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3


def create_connection(db_name):
    '''
    Функция создает соединение с БД db_name
    и возвращает его
    '''
    try:
        connection = sqlite3.connect(db_name)
        return connection
    except Error as e:
        print(e)
    return None


def create_db(db_name, db_schema):
    db_exists = os.path.exists(db_name)

    conn = sqlite3.connect(db_name)

    if not db_exists:
        print('Создаю базу данных...')
        with open(db_schema, 'r') as f:
            schema = f.read()
        conn.executescript(schema)
        print('Done')
    else:
        print('База данных существует')


def write_data_to_db(connection, query, data):
    '''
    Функция ожидает аргументы:
     * connection - соединение с БД
     * query - запрос, который нужно выполнить
     * data - данные, которые надо передать в виде списка кортежей

    Функция пытается записать все данные из списка data.
    Если данные удалось записать успешно, изменения сохраняются в БД
    и функция возвращает True.
    Если в процессе записи возникла ошибка, транзакция откатывается
    и функция возвращает False.
    '''
    try:
        with connection:
            connection.execute(query, data)
    except sqlite3.IntegrityError as e:
        print('При добавлении данных:', data, 'Возникла ошибка:', e)
        return False
    else:
        print('Запись данных прошла успешно')
        return True


def add_data_switches(db_name, src_yaml):
    import yaml
    conn = create_connection(db_name)
    print('Добавляю данные в таблицу switches...')
    with open(src_yaml[0], 'r') as f:
        switches = yaml.load(f)
        for switch, location in switches['switches'].items():
            query = '''insert into switches (hostname, location)
                       values (?, ?)'''
            values = (switch, location)
            write_data_to_db(conn, query, values)


def add_data(db_name, dhcp_files):
    import re
    regex_s = re.compile('(\w+\d+)_\S+\.txt')
    regex_d = re.compile('(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)')
    conn = create_connection(db_name)

    for file in dhcp_files:
        sw = re.search(regex_s, file)
        switch = sw.group(1)
        query_ac = '''UPDATE dhcp SET active = '0' WHERE switch = ?'''
        write_data_to_db(conn, query_ac, [switch])
        query_ac = '''UPDATE dhcp SET last_active = datetime('now') WHERE switch = ?'''
        write_data_to_db(conn, query_ac, [switch])

        with open(file) as data:
            for row in data:
                match = regex_d.search(row)
                if match:
                    res = (*match.groups(), switch, '1')
                    query = '''INSERT OR REPLACE INTO dhcp (mac, ip, vlan, interface, switch, active, last_active)
                            VALUES (?, ?, ?, ?, ?, ?, datetime('now'))'''
                    write_data_to_db(conn, query, res)


def get_all_data(db_name):
    conn = create_connection(db_name)
    query = 'SELECT * FROM dhcp'
    print('-'*17, '', '-'*14,  '  --', '',  '-'*16,  '', '-'*3, '-', '-'*19)

    for row in conn.execute(query):
        print('\nАктивные записи:\n')

        print('{:<17}  {:<15}  {:>2}  {:<16}  {} {} {}'.format(*row))
    print('-'*17, '', '-'*14,  '  --', '',  '-'*16,  '', '-'*3, '-', '-'*19)


def get_data(db_name, key, value):
    conn = create_connection(db_name)
    query_dict = {'vlan': 'select * from dhcp where vlan = ?',
              'mac': 'select * from dhcp where mac = ?',
              'ip': 'select * from dhcp where ip = ?',
              'interface': 'select * from dhcp where interface = ?',
              'switch': 'select * from dhcp where switch = ?',
              'active': 'select * from dhcp where active = ?'}
    keys = query_dict.keys()
    if not key in keys:
        print('Enter key from {}'.format(', '.join(keys)))
    else:
        conn.row_factory = sqlite3.Row

        print('\nИнформация об устройствах с такими параметрами:', key, value)

        query = query_dict[key]
        print('-'*17, '', '-'*14,  '  --', '',  '-'*16,  '', '-'*3, '-', '-'*19)
        for row in conn.execute(query, (value,)):
            print('{:<17}  {:<15}  {:>2}  {:<16}  {} {} {}'.format(*row))
        print('-'*17, '', '-'*14,  '  --', '',  '-'*16,  '', '-'*3, '-', '-'*19)
