#!/usr/bin/env python3

macs = ['aabb:cc80:7000', 'aabb:dd80:7340', 'aabb:ee80:7000', 'aabb:ff80:7000']
mac_cisco = []

for mac in macs:
    mac_cisco.append(mac.replace(':', '.'))

print(mac_cisco)