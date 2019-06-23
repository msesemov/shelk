#!/usr/bin/env python3


#with open('CAM_table.txt', 'r') as f:
f = open('CAM_table.txt', 'r')
lines = f.readlines()
vlan_set = []
mac_template = ' {}\t{}\t{}'

for line in lines:
	vlans = line[:5].rsplit()
	for vlan in vlans:
		if vlan.isdigit():
			vlan_set.append(vlan)

vlan_set.sort()

for vl in vlan_set:
	print(vl)
	for line in lines:
		if line.startswith(vl):
			value = (line.rsplit())
			print(mac_template.format(value[0], value[1], value[3]))

'''		if vlan.isdigit():
			value = (line.rsplit())
			vlan_set.append(int(value[0]))
			print(mac_template.format(value[0], value[1], value[3]))
vlan_set.sort()
'''


print(vlan_set)