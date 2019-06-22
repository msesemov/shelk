#!/usr/bin/env python3

from sys import argv

src, dst = argv[1:]

ignore = ['duplex', 'alias', 'Current configuration']

with open(src, 'r') as f, open(dst, 'w') as dest:
	for line in f:
		if not line.startswith(ignore[0], 1) and not line.startswith(ignore[1]) and not line.startswith(ignore[2]):
			dest.write(line)