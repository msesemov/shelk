#!/usr/bin/env python3

ip = input('Enter IP-address: ')
octets = ip.split('.')
d_oct = []
for octet in octets:
	d_oct.append(int(octet))

if ip.count('.') == 3 and d_oct[0] >=0 and d_oct[0] <= 255 and d_oct[1] >=0 and d_oct[1] <= 255 and d_oct[2] >=0 and d_oct[2] <= 255 and d_oct[3] >=0 and d_oct[3] <= 255:
	if d_oct[0] >= 1 and d_oct[0] <= 223:
		print('unicast')
	elif d_oct[0] >= 224 and d_oct[0] <= 239:
		print('multicast')
	elif d_oct[0] == 255 and d_oct[1] == 255 and d_oct[2] == 255 and d_oct[3] == 255:
		print('local broadcast')
	elif d_oct[0] == 0 and d_oct[1] == 0 and d_oct[2] == 0 and d_oct[3] == 0:
		print('unassigned')
	else:
		print('unused')
else:
	print('incorrect IP-address')
