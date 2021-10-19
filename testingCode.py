import nmap
from termcolor import colored


def detectOS(host):
    nm = nmap.PortScanner()
    machine = nm.scan(host, arguments='-O')
    try:
        print(colored(f"The Host(s): '{host}' os system: " + machine['scan'][host]['osmatch'][0]['osclass'][0]['osfamily'],
                      'green'))
    except:
        print(colored(f"Couldn't detect host's '{host}' OS", 'red'))
        pass


    print("It continues.")

detectOS('192.168.0.105')