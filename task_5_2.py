#!/usr/bin/env python3

prefix = input('Enter ip-prefix: ')
network = prefix.split('/')
octet = network[0].split('.')
x_len = int(network[1])
b_len = x_len * '1' + (32 - x_len) * '0'

ip_template = '''
    Network:
    {0:<8d} {1:<8d} {2:<8d} {3:<8d}
    {0:08b} {1:08b} {2:08b} {3:08b}

    Mask:
    /{4}
    {5:<8} {6:<8} {7:<8} {8:<8}
    {5:08b} {6:08b} {7:08b} {8:08b}
    '''

print(ip_template.format(int(octet[0]), int(octet[1]), int(octet[2]), int(octet[3]), x_len, int(b_len[0:8], 2), int(b_len[8:16], 2), int(b_len[16:24], 2), int(b_len[24:], 2)))
