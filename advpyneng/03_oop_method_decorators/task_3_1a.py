# -*- coding: utf-8 -*-
'''
Задание 3.1a

Скопировать класс IPv4Network из задания 3.1.
Добавить метод from_tuple, который позволяет создать экземпляр класса IPv4Network
из кортежа вида ('10.1.1.0', 29).

Пример создания экземпляра класса:

In [3]: net2 = IPv4Network.from_tuple(('10.1.1.0', 29))

In [4]: net2
Out[4]: IPv4Network(10.1.1.0/29)

'''
import ipaddress


class IPv4Network:
    def __init__(self, addr):
        subnet = ipaddress.ip_network(addr)
        self.subnet = subnet
        self.address = addr.split('/')[0]
        self.mask = subnet.prefixlen
        self.broadcast = str(subnet.broadcast_address)
        self.allocated = ()

    @property
    def hosts(self):
        result = ()
        for ip in self.subnet.hosts():
            result += (str(ip),)
        return result

    def allocate(self, address):
        self.allocated += (address,)

    @property
    def unassigned(self):
        result = list(self.hosts)
        for used in self.allocated:
            result.remove(used)
        return tuple(result)

    @classmethod
    def from_tuple(cls, net_tuple):
        return cls(net_tuple[0] + '/' + str(net_tuple[1]))


if __name__ == '__main__':
    net2 = IPv4Network.from_tuple(('10.1.1.0', 29))
    print(str(net2))