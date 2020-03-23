import os
import subprocess
import optparse
import re


def get_args():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="Interface to scan the networks")
    parser.add_option("-s", "--ssid", dest="ssid", help="The Name of the Access Point that will appear on devices")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please Specify an interface, use --help for more info")
    elif not options.ssid:
        parser.error("[-] Please Specify an interface, use --help for more info")
    else:
        return options


def hostapd(interface, ssid):
    f1 = open("hostapd.conf", 'w')
    f1.write("interface=" + interface+"\n")
    f1.write("ssid=" + ssid+"\n")
    f1.write("channel=1"+"\n")
    f1.write("driver=nl80211"+"\n")
    f1.close()


def dnsmasq(interface):
    f2 = open("dnsmasq.conf", 'w')
    f2.write("interface=" + interface+"\n")
    f2.write("dhcp-range=10.0.0.10,10.0.0.100,8h"+"\n")
    f2.write("dhcp-option=3,10.0.0.1"+"\n")
    f2.write("dhcp-option=6,10.0.0.1"+"\n")
    f2.write("address=/#/10.0.0.1"+"\n")


option = get_args()
try:
    hostapd(option.interface, option.ssid)
    dnsmasq(option.interface)
    os.system("service network-manager stop")
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    os.system("iptables --flush")
    os.system("iptables --table nat --flush")
    os.system("iptables --delete-chain")
    os.system("iptables --table nat --delete-chain")
    os.system("iptables -P FORWARD ACCEPT")
    os.system("dnsmasq -C dnsmasq.conf")
    os.system("hostapd hostapd.conf -B")
    os.system("ifconfig " + option.interface + " 10.0.0.1 netmask 255.255.255.0")
    while True:
        continue
except KeyboardInterrupt:
    print("\n\nRestoring Initial Configuration.....")
    os.system("rm -rf hostapd.conf")
    os.system("rm -rf dnsmasq.conf")
    findpid = subprocess.getoutput("ps -ae| grep dnsmasq")
    pid1 = re.findall("\d\d\d\d\d", findpid)
    if not pid1:
        pid1 = re.findall("\d\d\d\d", findpid)
    findpid = subprocess.getoutput("ps -ae| grep hostapd")
    pid2 = re.findall("\d\d\d\d\d", findpid)
    if not pid2:
        pid2 = re.findall("\d\d\d\d", findpid)
    subprocess.call(["kill", pid1[0]])
    subprocess.call(["kill", pid2[0]])
    print("Starting Network Service ")
    os.system("service network-manager start")
