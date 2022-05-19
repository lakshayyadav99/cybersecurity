#!/usr/bin/env python
import subprocess
import re

subprocess.call("ifconfig")
interface = raw_input("interface>")
new_mac = raw_input("new mac>")

ifconfig_result = subprocess.check_output(["ifconfig", interface])
mac_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

def mac_changer(interface, new_mac):
    print("[+] Changing Mac Address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])



mac_changer(interface, new_mac)

ifconfig_result = subprocess.check_output(["ifconfig", interface])
new_mac_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
if mac_result.group(0) == new_mac_result.group(0):
    print("[-]Mac Address not changed")
else:
    print("[+] Mac Address changed")
