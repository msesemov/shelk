#!/usr/bin/env python3


vlan_set = []
c=[]
mac_template = ' {}\t{}\t{}'

with open('CAM_table.txt', 'r') as f:
	for line in f:
		if line[0:5].strip().isdigit():
			a = line.rstrip().split()[0:5]
			a.remove(a[2])
			print(a)
			vlan_set.append(a)
			#vlan_set.append(line.strip().split())
print(sorted(vlan_set))
