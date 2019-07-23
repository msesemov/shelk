#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3


def create_db(db_filename):
    db_exists = os.path.exists(db_filename)

    conn = sqlite3.connect(db_filename)

    if not db_exists:
        print('Создаю базу данных...')
        with open(schema_filename, 'r') as f:
            schema = f.read()
        conn.executescript(schema)
        print('Done')
    else:
        print('База данных существует')


if __name__ == '__main__':
    data_filename = 'dhcp_snooping.txt'
    db_filename = 'dhcp_snooping.db'
    schema_filename = 'dhcp_snooping_schema.sql'
    create_db(db_filename)