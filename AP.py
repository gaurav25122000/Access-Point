import os
import re
import subprocess

from utils import dnsmasq, get_args, hostapd

if __name__ == "__main__":
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
