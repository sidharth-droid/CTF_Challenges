from scapy.all import rdpcap, ICMP

packets = rdpcap("breach.pcapng")
data = []
for pkt in packets:
    if pkt.haslayer(ICMP):
        icmp_layer = pkt[ICMP]
        # Collect type if not noise (Type != 8) and not end (Type != 255)
        if icmp_layer.type != 8 and icmp_layer.type != 255:
            data.append(icmp_layer.type)
flag = "".join(chr(x) for x in data)
print(f"Flag: {flag}")


# icmp and icmp.type != 8 and icmp.type != 255

# FLAG{1cmp_3xfil_hiDd3n_1n_typ3}