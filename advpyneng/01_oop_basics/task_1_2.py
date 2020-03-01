# -*- coding: utf-8 -*-
'''
Задание 1.2

Создать класс PingNetwork. При создании экземпляра класса PingNetwork,
 как аргумент передается экземпляр класса IPv4Network.

У класса PingNetwork должны быть методы _ping и scan

Метод _ping с параметром ip: должен пинговать один IP-адрес и возвращать
* True - если адрес пингуется
* False - если адрес не пингуется

Метод scan с таким параметрами:

* workers - значение по умолчанию 5
* include_unassigned - значение по умолчанию False

Метод scan:

* Пингует адреса из сети, которая передается как аргумент при создании экземпляра.
* Адреса должны пинговаться в разных потоках, для этого использовать concurrent.futures.
* По умолчанию, пингуются только адреса, которые находятся в атрибуте allocated.
  Если параметр include_unassigned равен True, должны пинговаться и адреса unassigned.
* Метод должен возвращать кортеж с двумя списками: список доступных IP-адресов и список
 недоступных IP-адресов



Пример работы с классом PingNetwork. Сначала создаем сеть:
In [3]: net1 = IPv4Network('8.8.4.0/29')

И выделяем несколько адресов:
In [4]: net1.allocate('8.8.4.2')
   ...: net1.allocate('8.8.4.4')
   ...: net1.allocate('8.8.4.6')
   ...:

In [5]: net1.allocated
Out[5]: ('8.8.4.2', '8.8.4.4', '8.8.4.6')

In [6]: net1.unassigned()
Out[6]: ('8.8.4.1', '8.8.4.3', '8.8.4.5')

Затем создается экземпляр класса PingNetwork, а сеть передается как аргумент:

In [8]: ping_net = PingNetwork(net1)

Пример работы метода scan:
In [9]: ping_net.scan()
Out[9]: (['8.8.4.4'], ['8.8.4.2', '8.8.4.6'])

In [10]: ping_net.scan(include_unassigned=True)
Out[10]: (['8.8.4.4'], ['8.8.4.2', '8.8.4.6', '8.8.4.1', '8.8.4.3', '8.8.4.5'])

'''
import task_1_1
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess


class PingNetwork:
    def __init__(self, ip_obj):
        self.ip_obj = ip_obj

    def _ping(self, ip):
        reply = subprocess.run(['ping', '-c', '2', '-W', '1', '-i', '0.2', '-n', ip],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    encoding='utf-8')
        if reply.returncode == 0:
            return True
        else:
            return False

    def scan(self, workers=5, include_unassigned=False):
        reachable = []
        unreachable = []
        if include_unassigned is False:
            devices = self.ip_obj.allocated
        else:
            devices = self.ip_obj.unassigned() + self.ip_obj.allocated

        with ThreadPoolExecutor(max_workers=3) as executor:
            result = executor.map(self._ping, devices)
            for device, output in zip(devices, result):
                if output is True:
                    reachable.append(device)
                else:
                    unreachable.append(device)
        return (reachable, unreachable)

if __name__ == '__main__':
    net1 = task_1_1.IPv4Network('8.8.4.0/29')
    net1.allocate('8.8.4.2')
    net1.allocate('8.8.4.4')
    net1.allocate('8.8.4.6')
    print(net1.allocated)
    print(net1.unassigned())
    ping_net = PingNetwork(net1)
    print(ping_net.scan())
    print(ping_net.scan(include_unassigned=True))