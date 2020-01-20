#!/usr/bin/env python

# iptables -I FORWARD -j NFQUEUE --queue-num 0
# iptables -I OUTPUT -j NFQUEUE --queue-num 0
# Must do when done:  iptables fllush

import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 10000:  # leaving
            print('HTTP Request')
            print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 10000:  # lcomeing from
            print('HTTP Response')
            print(scapy_packet.show())

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
