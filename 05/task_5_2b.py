#!/usr/bin/env python3

from sys import argv

prefix, mask_len = argv[1:]

octet = prefix.split('.')
x_len = int(mask_len)
b_len = x_len * '1' + (32 - x_len) * '0'
b_net = '{:08b}'.format(int(octet[0])) + '{:08b}'.format(int(octet[1])) + '{:08b}'.format(int(octet[2])) + '{:08b}'.format(int(octet[3]))
b_net = b_net[:x_len] + (32 - x_len) * '0'

net_template = '''
    Network:
    {0:<8d} {1:<8d} {2:<8d} {3:<8d}
    {0:08b} {1:08b} {2:08b} {3:08b}
	'''

mask_template = '''
    Mask:
    /{0}
    {1:<8} {2:<8} {3:<8} {4:<8}
    {1:08b} {2:08b} {3:08b} {4:08b}
    '''

print(net_template.format(int(b_net[0:8], 2), int(b_net[8:16], 2), int(b_net[16:24], 2), int(b_net[24:], 2)))
print(mask_template.format(x_len, int(b_len[0:8], 2), int(b_len[8:16], 2), int(b_len[16:24], 2), int(b_len[24:], 2)))
