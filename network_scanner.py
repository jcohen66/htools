#!/usr/bin/env ython3

import scapy.all as scapy
import optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-t', '--target', dest='ip', help='IP or range to scan.')
    (options, arguments) = parser.parse_args()
    if not options.ip:
        parser.error('[-] Please specify an ip or range. Use --help for more info.')

    return options


def scan(ip):
    # Use ARP to ask who has target IP
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    clients_list = []
    for element in answered_list:
        client_dict = {"ip":element[1].psrc, 'mac':element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list
    

def print_result(results_list):
    print("IP\t\t\tMAC Address\n-----------------------------------------------------")
    for element in results_list:
        print(element['ip'] + '\t\t' + element['mac'])

options = get_arguments()

scan_result = scan(options.ip)
print_result(scan_result)