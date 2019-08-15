#!/usr/bin/python3
import nmap
import sys
import pprint

nm = nmap.PortScanner()

# nm.scan(hosts='192.168.86.0/24', arguments='-n -sP -PE -PA21,23,80,3389')
nm.scan(hosts='192.168.86.0/24', arguments='-sP')
for x in nm.all_hosts():
    print(nm[x]['addresses']['ipv4'],nm[x]['hostnames'][0]['name'],nm[x]['status']['reason'])
