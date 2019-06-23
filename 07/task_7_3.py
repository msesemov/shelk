#!/usr/bin/env python3


with open('CAM_table.txt', 'r') as f:
	for line in f:
		vlans = line[:5].rsplit()
		for vlan in vlans:
			if vlan.isdigit():
				value = (line.rsplit())
				print(' {}\t{}\t{}'.format(value[0], value[1], value[3]))
