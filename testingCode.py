import socket
import sys

import nmap
from termcolor import colored

scanner = nmap.PortScanner()

# ip_addr = '192.168.0.101'
#
# print(scanner.scan(ip_addr, arguments="-O")['scan'][ip_addr]['osmatch'][1]['name'][0:])

# def detectOS(host):
#     nm = nmap.PortScanner()
#     machine = nm.scan(host, arguments='-O')
#     try:
#         hostname = socket.gethostbyaddr(host)[0]
#         hostDict = {hostname: host}
#         print(colored(f"The Host(s): '{hostDict}' os system is " + machine['scan'][host]['osmatch'][1]['name'][0:][
#                     'osfamily'],'green'))
#     except socket.error:
#         print(colored(f"Unable to detect host's '{host}' hostname.", 'red'), colored(
#             f"The Host(s): '{host}' os system: " + machine['scan'][host]['osmatch'][1]['name'][0:],
#             'green'))
#     except KeyboardInterrupt:
#         print("\n Exitting Program !!!!")
#         sys.exit()
#
#     except IndexError:
#         print(colored(f"Unable to detect host's {host} Operating system... ",'red'), colored("But my lucky guess: Some Windows Based server OS", 'green'))
#         print(colored(f"Unable to detect host's '{host}' hostname.", 'red'), colored(
#             f"The Host(s): '{host}' os system: " + machine['scan'][host]['osmatch'][0]['osclass'][0]['osfamily'],
#             'green'))
#         pass
#detectOS("192.168.0.104")

import nmap
nm = nmap.PortScanner()
ip = '192.168.0.102'
machine = nm.scan(ip, arguments='-O')
print(machine['scan'][ip]['osmatch'][0]['osclass'][0]['osfamily'])
