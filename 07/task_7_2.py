#!/usr/bin/env python3

with open('config_sw1.txt', 'r') as f:
	for line in f:
		if not line.startswith('!'):
			print(line.rstrip())