# -*- coding: utf-8 -*-
'''
Задание 4.1

Создать класс CiscoTelnet, который наследует класс TelnetBase из файла base_telnet_class.py.

Переписать метод __init__ в классе CiscoTelnet таким образом:

* добавить параметры:
 * enable - пароль на режим enable
 * disable_paging - отключает постраничный вывод команд, по умолчанию равен True
* после подключения по Telnet должен выполняться переход в режим enable:
  для этого в методе __init__ должен сначала вызываться метод __init__ класса
   TelnetBase, а затем выполняться переход в режим enable.

Добавить в класс CiscoTelnet метод send_show_command, который отправляет команду
show и возвращает ее вывод в виде строки. Метод ожидает как аргумент одну команду.

Добавить в класс CiscoTelnet метод send_config_commands, который отправляет одну
или несколько команд на оборудование в конфигурационном режиме и возвращает ее
вывод в виде строки. Метод ожидает как аргумент одну команду (строку) или
несколько команд (список).

Пример работы класса:
In [1]: r1 = CiscoTelnet('192.168.100.1', 'cisco', 'cisco', 'cisco')

Метод send_show_command:
In [2]: r1.send_show_command('sh clock')
Out[2]: 'sh clock\r\n*09:39:38.633 UTC Thu Oct 10 2019\r\nR1#'

Метод send_config_commands:
In [3]: r1.send_config_commands('logging 7.7.7.7')
Out[3]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\n
R1(config)#logging 7.7.7.7\r\nR1(config)#end\r\nR1#'

In [4]: r1.send_config_commands(['interface loop77', 'ip address 107.7.7.7 255.255.255.255'])
Out[4]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\n
R1(config)#interface loop77\r\nR1(config-if)#ip address 107.7.7.7 255.255.255.255\r\n
R1(config-if)#end\r\nR1#'


Тест берет значения из файла devices.yaml, поэтому если
для заданий используются другие адреса/логины, надо заменить их там.
'''
from base_telnet_class import TelnetBase
import time

class CiscoTelnet(TelnetBase):
    def __init__(self, ip, username, password, enable, disable_paging=True):
        super().__init__(ip, username, password)
        super()._write_line('enable')
        super()._read_until_regex('Password:')
        super()._write_line(enable)

        if disable_paging:
            self.prompt = None
            super()._write_line('terminal length 0')
            super()._read_until_regex('#')
            if not self.prompt:
                time.sleep(1)
                self._telnet.read_very_eager()
            else:
                self._read_until_regex(self.prompt)

    def send_show_command(self, command):
        super()._write_line(command)
        return super()._read_until_regex('#')

    def send_config_commands(self, command):
        super()._write_line('conf t')
        output = super()._read_until_regex('#')

        if isinstance(command, str):
            command = [command, ]
        for cmd in command:
            super()._write_line(cmd)
            output += super()._read_until_regex('#')
        super()._write_line('end')
        output += super()._read_until_regex('#')
        return output


if __name__ == '__main__':
    r1 = CiscoTelnet('192.168.100.1', 'cisco', 'cisco', 'cisco')
#    print(r1.send_show_command('sh clock'))
#    print(r1.send_config_commands('logging 7.7.7.7'))
    #print(r1.send_config_commands(['interface loop77', 'ip address 107.7.7.7 255.255.255.255']))