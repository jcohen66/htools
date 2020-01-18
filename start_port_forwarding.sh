echo 1 > /proc/sys/net/ipv4/ip_forward
iptables --flush
iptables -I OUTPUT -j NFQUEUE --queue-num 0
iptables -I INPUT -j NFQUEUE --queue-num 0