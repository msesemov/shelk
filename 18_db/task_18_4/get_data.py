#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import sys


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


def get_key_val_db(connection, key, value):
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
        connection.row_factory = sqlite3.Row

        print('\nИнформация об устройствах с такими параметрами:', key, value)

        query = query_dict[key]
        return connection.execute(query, (value,))


if __name__ == '__main__':
    args = sys.argv[1:]
    db_name = 'dhcp_snooping.db'
    conn = create_connection(db_name)
    if len(args) == 0:
        query = 'select * from dhcp where active = 1'
        active_db = get_all_from_db (conn, query)
        print('\nАктивные записи:\n')
        print('-'*17, '', '-'*14,  '  --', '',  '-'*16,  '', '-'*3, ' -')
        for row in active_db:
            print('{:<17}  {:<15}  {:>2}  {:<16}  {}  {}'.format(*row))
        print('-'*17, '', '-'*14,  '  --', '',  '-'*16,  '', '-'*3, ' -\n')
        query = 'select * from dhcp where active = 0'
        inactive_db = get_all_from_db(conn, query)
        if len(inactive_db) != 0:
            print('Неактивные записи:\n')
            print('-'*17, '', '-'*14,  '  --', '',  '-'*16,  '', '-'*3, ' -')
            for row in inactive_db:
                print('{:<17}  {:<15}  {:>2}  {:<16}  {}  {}'.format(*row))
            print('-'*17, '', '-'*14,  '  --', '',  '-'*16,  '', '-'*3, ' -\n')
    elif len(args) == 2:
        key_val = get_key_val_db(conn, *args,)
        inact = []
        act = []
        for row in key_val:
            if row[5] == 0:
                inact.append(row)
            else:
                act.append(row)
        print('\nАктивные записи:\n')
        print('-'*17, '', '-'*14,  '  --', '',  '-'*16,  '', '-'*3, '-')
        for a in act:
            print('{:<17}  {:<15}  {:>2}  {:<16}  {} {}'.format(*a))
        print('-'*17, '', '-'*14,  '  --', '',  '-'*16,  '', '-'*3, '-\n')
        if len(inact) != 0:
            for i in inact:
                print('Неактивные записи:\n')
                print('-'*17, '', '-'*14,  '  --', '',  '-'*16,  '', '-'*3, '-')
                print('{:<17}  {:<15}  {:>2}  {:<16}  {} {}'.format(*i))
            print('-'*17, '', '-'*14,  '  --', '',  '-'*16,  '', '-'*3, '-\n')
    else:
        print('Пожалуйста, введите два или ноль аргументов')
