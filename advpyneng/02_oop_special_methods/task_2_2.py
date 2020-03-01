# -*- coding: utf-8 -*-
'''
Задание 2.2

Скопировать класс PingNetwork из задания 1.2 и изменить его таким образом,
чтобы адреса пинговались не при вызове метода scan, а при вызове экземпляра.

Вся функциональность метода scan должна быть перенесена в метод, который отвечает
за вызов экземпляра.

Пример работы с классом PingNetwork. Сначала создаем сеть:
In [2]: net1 = IPv4Network('8.8.4.0/29')

И выделяем несколько адресов:
In [3]: net1.allocate('8.8.4.2')
   ...: net1.allocate('8.8.4.4')
   ...: net1.allocate('8.8.4.6')
   ...:

Затем создается экземпляр класса PingNetwork, сеть передается как аргумент:
In [6]: ping_net = PingNetwork(net1)

После этого экземпляр должен быть вызываемым объектом (callable):

In [7]: ping_net()
Out[7]: (['8.8.4.4'], ['8.8.4.2', '8.8.4.6'])

In [8]: ping_net(include_unassigned=True)
Out[8]: (['8.8.4.4'], ['8.8.4.2', '8.8.4.6', '8.8.4.1', '8.8.4.3', '8.8.4.5'])


'''
from task_2_1 import IPv4Network
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

    def __call__(self, workers=5, include_unassigned=False):
        reachable = []
        unreachable = []
        if include_unassigned is False:
            devices = self.ip_obj.allocated
        else:
            devices = self.ip_obj.unassigned() + self.ip_obj.allocated

        with ThreadPoolExecutor(max_workers=workers) as executor:
            result = executor.map(self._ping, devices)
            for device, output in zip(devices, result):
                if output is True:
                    reachable.append(device)
                else:
                    unreachable.append(device)
        return (reachable, unreachable)


if __name__ == '__main__':
    net1 = IPv4Network('8.8.4.0/29')
    net1.allocate('8.8.4.2')
    net1.allocate('8.8.4.4')
    net1.allocate('8.8.4.6')
    ping_net = PingNetwork(net1)
    print(ping_net())
    print(ping_net(include_unassigned=True))