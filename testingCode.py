import socket

import nmap
from termcolor import colored


def detectOS(host):
    nm = nmap.PortScanner()
    machine = nm.scan(host, arguments='-O')
    try:
        hostname = socket.gethostbyaddr(host)[0]
        hostDict = {hostname: host}
        print(colored(f"The Host(s): '{hostDict}' os system: " + machine['scan'][host]['osmatch'][0]['osclass'][0][
                    'osfamily'],'green'))
    except socket.error:
        print(colored(f"Couldn't detect host's '{host}' hostname.", 'red'), colored(
            f"The Host(s): '{host}' os system: " + machine['scan'][host]['osmatch'][0]['osclass'][0]['osfamily'],'green'))
        # print(colored(
        #     f"The Host(s): '{host}' os system: " + machine['scan'][host]['osmatch'][0]['osclass'][0]['osfamily'],'green'))
        pass
detectOS('192.168.0.104')