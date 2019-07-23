#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import sys


def get_all_from_db(db_filename):
    conn = sqlite3.connect(db_filename)
    print('В таблице dhcp такие записи:')
    print('-'*17, '', '-'*14,  '  --', '',  '-'*16,  '', '-'*3)
    for row in conn.execute('select * from dhcp'):
        print('{:<17}  {:<15}  {:>2}  {:<16}  {}'.format(*row))
    print('-'*17, '', '-'*14,  '  --', '',  '-'*16,  '', '-'*3)


def get_key_val_db(key, value, db_filename):
    query_dict = {'vlan': 'select * from dhcp where vlan = ?',
              'mac': 'select * from dhcp where mac = ?',
              'ip': 'select * from dhcp where ip = ?',
              'interface': 'select * from dhcp where interface = ?',
              'switch': 'select * from dhcp where switch = ?'}
    keys = query_dict.keys()
    if not key in keys:
        print('Enter key from {}'.format(', '.join(keys)))
    else:
        conn = sqlite3.connect(db_filename)
        conn.row_factory = sqlite3.Row

        print('\nИнформация об устройствах с такими параметрами:', key, value)

        query = query_dict[key]
        result = conn.execute(query, (value,))
        print('-'*17, '', '-'*14,  '  --', '',  '-'*16,  '', '-'*3)

        for row in result:
            print('{:<17}  {:<15}  {:>2}  {:<16}  {}'.format(*row))
                #print('{:12}: {}'.format(row_name, row[row_name]))
        print('-'*17, '', '-'*14,  '  --', '',  '-'*16,  '', '-'*3)


if __name__ == '__main__':
    args = sys.argv[1:]
    db_filename = 'dhcp_snooping.db'
    if len(args) == 0:
        get_all_from_db(db_filename)
    elif len(args) == 2:
        get_key_val_db(*args, db_filename)
    else:
        print('Пожалуйста, введите два или ноль аргументов')
