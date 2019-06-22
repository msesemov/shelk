#!/usr/bin/env python3

ip = input('Enter IP-address: ')
octets = ip.split('.')

if ip.count('.') == 3:
	for octet in octets:
		if octet >=0 and octet <= 255:



			if int(octets[0]) >= 1 and int(octets[0]) <= 223:
				print('unicast')
			elif int(octets[0]) >= 224 and int(octets[0]) <= 239:
				print('multicast')
			elif int(octets[0]) == 255 and int(octets[1]) == 255 and int(octets[2]) == 255 and int(octets[3]) == 255:
				print('local broadcast')
			elif int(octets[0]) == 0 and int(octets[1]) == 0 and int(octets[2]) == 0 and int(octets[3]) == 0:
				print('unassigned')
			else:
				print('unused')
else:
	print('incorrect IP-address')
