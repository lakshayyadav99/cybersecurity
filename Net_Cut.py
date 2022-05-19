import netfilterqueue
import subprocess

subprocess.call(["iptables","-I","FORWARD","-j","NFQUEUE","--queue-num","0"])

def process_packet(packet):
    print(packet)
    packet.drop()
try:
    while True:
        queue = netfilterqueue.NetfilterQueue()
        queue.bind(0,process_packet)
        queue.run()

except KeyboardInterrupt:
    print("Flushing Iptable")
    subprocess.call(["iptables","--flush"])

