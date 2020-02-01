#!/usr/bin/env python

import subprocess
import netfilterqueue

#subprocess.call(["iptables", "-I", "FORWARD", "-j", "NFQUEUE", "--queue-num", "0"])

def process_packet(packet):
    print(packet)
    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0,process_packet)
queue.run

#    subprocess.call(["iptables", "--flush"])