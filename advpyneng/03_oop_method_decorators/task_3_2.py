# -*- coding: utf-8 -*-
'''
Задание 3.2

Скопировать класс PingNetwork из задания 1.2.
Один из методов класса зависит только от значения аргумента и не зависит
от значений переменных экземпляра или другого состояния объекта.

Сделать этот метод статическим и проверить работу метода.

'''


import task_3_1
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess


class PingNetwork:
    def __init__(self, ip_obj):
        self.ip_obj = ip_obj

    @staticmethod
    def _ping(ip):
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
            devices = self.ip_obj.unassigned + self.ip_obj.allocated

        with ThreadPoolExecutor(max_workers=3) as executor:
            result = executor.map(self._ping, devices)
            for device, output in zip(devices, result):
                if output is True:
                    reachable.append(device)
                else:
                    unreachable.append(device)
        return (reachable, unreachable)

if __name__ == '__main__':
    net1 = task_3_1.IPv4Network('8.8.4.0/29')
    net1.allocate('8.8.4.2')
    net1.allocate('8.8.4.4')
    net1.allocate('8.8.4.6')
    print(net1.allocated)
    print(net1.unassigned)
    ping_net = PingNetwork(net1)
    print(ping_net.scan())
    print(ping_net.scan(include_unassigned=True))