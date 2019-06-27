#!/usr/bin/env python3

from sys import argv

vlan_num = argv[1]

vlan_set = []
mac_template = '{}\t{}\t{}'

with open('CAM_table.txt', 'r') as f:
	for line in f:
		if line[0:5].strip().isdigit():
			a = line.rstrip().split()[0:5]
			c = [int(a[0]), a[1], a[3]]
			vlan_set.append(c)
vlan_set.sort()
for vlan in vlan_set:
	if vlan[0] == int(vlan_num):
		print(mac_template.format(vlan[0], vlan[1], vlan[2]))