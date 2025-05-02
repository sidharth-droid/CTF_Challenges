from scapy.all import IP, ICMP, Ether, wrpcap
import random

flag_hex = "464C41477B31636D705F337866696C5F68694464336E5F316E5F747970337D"
packets = []

# Noise: 100 packets, Type 8, random seq
for i in range(100):
    pkt = Ether()/IP(src="192.168.1.100", dst="10.0.0.50")/ICMP(type=8, id=1, seq=random.randint(1, 1000))
    packets.append(pkt)

# Data: 56 packets, Type from flag_hex, Seq 1-56
for i in range(0, len(flag_hex), 2):
    byte = int(flag_hex[i:i+2], 16)
    seq = (i // 2) + 1
    pkt = Ether()/IP(src="192.168.1.100", dst="10.0.0.50")/ICMP(type=byte, id=1, seq=seq)
    packets.append(pkt)

# End: Type 255, Seq 57
pkt = Ether()/IP(src="192.168.1.100", dst="10.0.0.50")/ICMP(type=255, id=1, seq=57)
packets.append(pkt)

wrpcap("breach.pcapng", packets)
print("PCAP generated with 157 packets")