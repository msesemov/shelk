#!/usr/bin/env python3

ignore = ['duplex', 'alias', 'Current configuration']

with open('config_sw1.txt', 'r') as f, open('config_sw1_cleared.txt', 'w') as dest:
	for line in f:
		if not line.startswith(ignore[0], 1) and not line.startswith(ignore[1]) and not line.startswith(ignore[2]):
			dest.write(line)