#!/usr/bin/env python3

ignore = ['duplex', 'alias', 'Current configuration']

with open('config_sw1.txt', 'r') as f:
	for line in f:
		if not line.startswith('!'):
			if not line.startswith(ignore[0], 1) and not line.startswith(ignore[1]) and not line.startswith(ignore[2]):
				print(line.rstrip())