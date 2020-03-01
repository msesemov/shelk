# -*- coding: utf-8 -*-
'''
Задание 4.1a

Скопировать класс CiscoTelnet из задания 4.1 и добавить проверку на ошибки.

Добавить метод _check_error_in_command, который выполняет проверку на такие ошибки:
* Invalid input detected, Incomplete command, Ambiguous command

Создать исключение ErrorInCommand, которое будет генерироваться при возникновении
ошибки на оборудовании.

Метод ожидает как аргумент команду и вывод команды. Если в выводе не обнаружена ошибка,
метод ничего не возвращает. Если в выводе найдена ошибка, метод генерирует исключение
ErrorInCommand с сообщением о том какая ошибка была обнаружена, на каком устройстве и в какой команде.

Добавить проверку на ошибки в методы send_show_command и send_config_commands.

Пример работы класса с ошибками:
In [1]: r1 = CiscoTelnet('192.168.100.1', 'cisco', 'cisco', 'cisco')

In [2]: r1.send_show_command('sh clck')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-e26d712f3ad3> in <module>
----> 1 r1.send_show_command('sh clck')
...
ErrorInCommand: При выполнении команды "sh clck" на устройстве 192.168.100.1 возникла ошибка "Invalid input detected at '^' marker.

In [3]: r1.send_config_commands('loggg 7.7.7.7')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-3-ab4a1ce52554> in <module>
----> 1 r1.send_config_commands('loggg 7.7.7.7')
...
ErrorInCommand: При выполнении команды "loggg 7.7.7.7" на устройстве 192.168.100.1 возникла ошибка "Invalid input detected at '^' marker.

Без ошибок:
In [4]: r1.send_show_command('sh clock')
Out[4]: 'sh clock\r\n*09:39:38.633 UTC Thu Oct 10 2019\r\nR1#'

In [5]: r1.send_config_commands('logging 7.7.7.7')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 7.7.7.7\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop77', 'ip address 107.7.7.7 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop77\r\nR1(config-if)#ip address 107.7.7.7 255.255.255.255\r\nR1(config-if)#end\r\nR1#'



Примеры команд с ошибками:
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.
R1(config)#logging
% Incomplete command.

R1(config)#sh i
% Ambiguous command:  "sh i"
'''

# списки команд с ошибками и без:

from base_telnet_class import TelnetBase
import time


class CiscoTelnet(TelnetBase):
    def __init__(self, ip, username, password, enable, disable_paging=True):
        self.ip = ip
        super().__init__(ip, username, password)
        super()._write_line('enable')
        super()._read_until_regex('Password:')
        super()._write_line(enable)

        if disable_paging:
            self.prompt = '#'
            super()._write_line('terminal length 0')
            if self.prompt:
                time.sleep(1)
                self._telnet.read_very_eager()
            else:
                self._read_until_regex(self.prompt)

    def send_show_command(self, command):
        super()._write_line(command)
        output = super()._read_until_regex(self.prompt)
        self._check_error_in_command(command, output)
        return output

    def send_config_commands(self, command):
        super()._write_line('conf t')
        output = super()._read_until_regex(self.prompt)

        if isinstance(command, str):
            command = [command, 'end']
        for cmd in command:
            super()._write_line(cmd)
            output += super()._read_until_regex(self.prompt)
            self._check_error_in_command(cmd, output)
        return output

    def _check_error_in_command(self, command, output):
        exceptions = ['Invalid input detected',
                    'Incomplete command',
                    'Ambiguous command']
        for exception in exceptions:
            if exception in output:
                e = f'При выполнении команды \"{command}\" на устройстве {self.ip} возникла ошибка {exception}'
                raise ErrorInCommand(e)

class ErrorInCommand(Exception):
    pass


if __name__ == '__main__':
    config_commands_errors = ['logging 0255.255.1', 'logging', 'sh i']
    correct_config_commands = ['logging buffered 20010', 'ip http server']
    r1 = CiscoTelnet('192.168.100.1', 'cisco', 'cisco', 'cisco')
    print(r1.send_show_command('sh clck'))
#    print(r1.send_config_commands('logging 7.7.7.7'))
    #print(r1.send_config_commands(['interface loop77', 'ip address 107.7.7.7 255.255.255.255']))