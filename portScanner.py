#!/usr/bin/env python
# ping a list of host with threads for increase speed
# use standard linux /bin/ping utility


import socket
import sys
from threading import Thread
import subprocess
from termcolor import colored
import nmap

try:
    import queue
except ImportError:
    import Queue as queue
import re


# some global vars
num_threads = 32
ips_q = queue.Queue()
out_q = queue.Queue()

# build IP array
ips = []
for i in range(1, 105):
    ips.append("192.168.0." + str(i))

hosts_up = []

# thread code : wraps system ping command
def thread_pinger(i, q):
    """Pings hosts in queue"""
    while True:
        # get an IP item form queue
        ip_address = q.get()
        # ping it
        args = ['/bin/ping', '-c', '1', '-W', '1', str(ip_address)]
        print(args)
        p_ping = subprocess.Popen(args,
                                  shell=False,
                                  stdout=subprocess.PIPE)
        # save ping stdout
        p_ping_out = str(p_ping.communicate()[0])

        if (p_ping.wait() == 0):
            # rtt min/avg/max/mdev = 22.293/22.293/22.293/0.000 ms
            search = re.search(r'rtt min/avg/max/mdev = (.*)/(.*)/(.*)/(.*) ms',
                               p_ping_out, re.M | re.I)
            ping_rtt = search.group(2)
            out_q.put("OK " + str(ip_address) + " rtt= " + ping_rtt)
            # adds responding hosts to array.
            hosts_up.append(str(ip_address))

        # update queue : this ip is processed
        q.task_done()

#prevents double modification of shared variables.
#when one thread uses a variable, other can't access it.
#Once done, the thread relases it.
# lock = threading.Lock()
# def test_port(ipAddress, target, port):
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     try:
#         conn = s.connect((target, port))
#         with lock:
#             print('port',port)
#         conn.close()
#     except:
#         pass

#Detects OS System and hostname with host parameter..
def detectOS(host):
    nm = nmap.PortScanner()
    machine = nm.scan(host, arguments='-O')
    try:
        hostname = socket.gethostbyaddr(host)[0]
        hostDict = {hostname: host}
        print(colored(f"The Host(s): '{hostDict}' os system is " + machine['scan'][host]['osmatch'][0]['osclass'][0][
                    'osfamily'],'green'))
    except socket.error:
        print(colored(f"Unable to detect host's '{host}' hostname.", 'red'), colored(
            f"The Host(s): '{host}' os system: " + machine['scan'][host]['osmatch'][0]['osclass'][0]['osfamily'],
            'green'))
    except KeyboardInterrupt:
        print("\n Exitting Program !!!!")
        sys.exit()

    except IndexError:
        print(colored(f"Unable to detect host's {host} Operating system... ",'red'), colored("But my lucky guess: Some Windows Based server OS", 'green'))
        pass



def main():
    # start the thread pool
    for i in range(num_threads):
        worker = Thread(target=thread_pinger, args=(i, ips_q))
        worker.setDaemon(True)
        worker.start()

    # fill queue
    for ip in ips:
        ips_q.put(ip)

    # wait until worker threads are done to exit
    ips_q.join()

    print("Hosts up: ")
    for i in range(len(hosts_up)):
        detectOS(hosts_up[i])



if __name__ == "__main__":
    main()



