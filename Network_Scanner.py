#!/usr/bin/env python
import scapy.all as scapy
def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered = scapy.srp(arp_request_broadcast, timeout = 1, verbose = False)[0]
    client_list = []
    for element in answered:
        client_dict = {"ip":element[1].psrc, "mac":element[1].hwsrc}
        client_list.append(client_dict)
    return client_list

def print_result(result_list):
    print("IP\t\t\t MAC ADD\n_______________")
    for client in result_list:
        print(client["ip"]+"\t\t"+client["mac"])

scan_result = scan("192.168.0.1/24")
print_result(scan_result)