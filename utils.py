import optparse


def get_args():
    parser = optparse.OptionParser()

    parser.add_option(
        "-i", "--interface", dest="interface", help="Interface to scan the networks"
    )
    parser.add_option(
        "-s",
        "--ssid",
        dest="ssid",
        help="The Name of the Access Point that will appear on devices",
    )
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please Specify an interface, use --help for more info")
    elif not options.ssid:
        parser.error("[-] Please Specify an interface, use --help for more info")
    else:
        return options


def hostapd(interface, ssid):
    f1 = open("hostapd.conf", "w")
    f1.write("interface=" + interface + "\n")
    f1.write("ssid=" + ssid + "\n")
    f1.write("channel=1" + "\n")
    f1.write("driver=nl80211" + "\n")
    f1.close()


def dnsmasq(interface):
    f2 = open("dnsmasq.conf", "w")
    f2.write("interface=" + interface + "\n")
    f2.write("dhcp-range=10.0.0.10,10.0.0.100,8h" + "\n")
    f2.write("dhcp-option=3,10.0.0.1" + "\n")
    f2.write("dhcp-option=6,10.0.0.1" + "\n")
    f2.write("address=/#/10.0.0.1" + "\n")
