#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import glob


def check_if_db(db_name):
    import os
    try:
        db_exists = os.path.exists(db_name)
    except NameError:
        print('База данных не существует. Перед добавлением данных, ее надо создать')
    return db_exists


def create_connection(db_name):
    '''
    Функция создает соединение с БД db_name
    и возвращает его
    '''
    connection = sqlite3.connect(db_name)
    return connection


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


def get_all_from_db(connection, query):
    '''
    Функция ожидает аргументы:
     * connection - соединение с БД
     * query - запрос, который нужно выполнить

    Функция возвращает данные полученные из БД.
    '''
    result = [row for row in connection.execute(query)]
    return result


def write_db_switches_from_yaml(src_yaml, db_name):
    import yaml
    conn = create_connection(db_name)
    print('Добавляю данные в таблицу switches...')
    with open(src_yaml, 'r') as f:
        switches = yaml.load(f)
        for switch, location in switches['switches'].items():
            query = '''insert into switches (hostname, location)
                       values (?, ?)'''
            values = (switch, location)
            write_data_to_db(conn, query, values)
    conn.close()


def write_db_from_sh_dhcp(dhcp_files, db_name):
    import re
    regex_s = re.compile('(\w+\d+)_\S+\.txt')
    regex_d = re.compile('(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)')
    conn = create_connection(db_name)
    print('Добавляю данные в таблицу dhcp...')
    result = []

    for file in dhcp_files:
        sw = re.search(regex_s, file)
        switch = sw.group(1)
        query_ac = '''update dhcp set active = ? where switch = ?'''
        write_data_to_db(conn, query_ac, [0, switch])

        with open(file) as data:
            for row in data:
                match = regex_d.search(row)
                if match:
                    res = (*match.groups(), switch, 1)
                    query = '''insert or replace into dhcp (mac, ip, vlan, interface, switch, active)
                            values (?, ?, ?, ?, ?, ?)'''
                    write_data_to_db(conn, query, res)
    conn.close()


if __name__ == '__main__':
    dhcp_files = glob.glob('new_data/*_dhcp_snooping.txt')
    db_name = 'dhcp_snooping.db'
    if check_if_db(db_name):
        write_db_switches_from_yaml('switches.yml', db_name)
        write_db_from_sh_dhcp(dhcp_files, db_name)
    else:
        print('База данных не существует. Перед добавлением данных, ее надо создать')
