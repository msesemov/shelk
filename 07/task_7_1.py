#!/usr/bin/env python3

ospf_route = 'O        10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0'

route_template = '''
Protocol:              {}
Prefix:                {}
AD/Metric:             {}
Next-Hop:              {}
Last update:           {}
Outbound Interface     {}
'''
route_s = ospf_route.split()

file = open('task7.1.txt', 'w')
file.write(route_template.format(route_s[0].replace('O', 'OSPF'), route_s[1], route_s[2].strip('[]'), route_s[4].strip(','), route_s[5].strip(','), route_s[6]))
file.close()