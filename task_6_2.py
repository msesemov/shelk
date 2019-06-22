#!/usr/bin/env python3

ip = input('Enter IP-address: ')
octet = ip.split('.')

if int(octet[0]) >= 1 and int(octet[0]) <= 223:
	print('unicast')
elif int(octet[0]) >= 224 and int(octet[0]) <= 239:
	print('multicast')
elif int(octet[0]) == 255 and int(octet[1]) == 255 and int(octet[2]) == 255 and int(octet[3]) == 255:
	print('local broadcast')
elif int(octet[0]) == 0 and int(octet[1]) == 0 and int(octet[2]) == 0 and int(octet[3]) == 0:
	print('unassigned')
else:
	print('unused')
