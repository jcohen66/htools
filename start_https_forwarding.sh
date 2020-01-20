iptables --flush
echo 1 > /proc/sys/net/ipv4/ip_forward

iptables -I OUTPUT -j NFQUEUE --queue-num 0
iptables -I INPUT -j NFQUEUE --queue-num 0
#iptables -I FORWARD -j NFQUEUE --queue-num 0
iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000
iptables -t nat -A PREROUTING -p tcp --destination-port 443 -j REDIRECT --to-port 10000

