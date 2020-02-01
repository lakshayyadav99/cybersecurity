#!/usr/bin/env python

import subprocess
import re
def change_mac(i, n):
    print("[+] Changing mac address for " + i + " to " + n)
    subprocess.call(["ifconfig", i, "down"])
    subprocess.call(["ifconfig", i, "hw", "ether", n])
    subprocess.call(["ifconfig", i, "up"])


interface = raw_input("interface >")
new_mac = raw_input("new mac >")
ifconfig_result = subprocess.check_output(["ifconfig", interface])
mac_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
change_mac(interface, new_mac)
ifconfig_result_after = subprocess.check_output(["ifconfig", interface])
mac_result_after = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result_after)
if mac_result.group(0) == mac_result_after.group(0) :
    print("[-] Mac Address Not Changes")
else:
    print("[+] Mac Address Changed")