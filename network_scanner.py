#!/usr/bin/env ython3

import scapy.all as scapy


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    print(arp_request.summary())
#    scapy.ls(scapy.ARP())


scan('10.0.2.1')
