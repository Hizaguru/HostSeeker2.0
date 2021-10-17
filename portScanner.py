#!/usr/bin/env python
# ping a list of host with threads for increase speed
# use standard linux /bin/ping utility
import random
from threading import Thread
import subprocess
try:
    import queue
except ImportError:
    import Queue as queue
import re


tgtPorts = ["22", "101", "33"]

def connScan(tgtHost, tgtPort):
  try:
    connSkt = socket(AF_INET, SOCK_STREAM)
    connSkt.connect((tgtHost, tgtPort))
    connSkt.send('Scanning ports...\r\r\r')
    results = connSkt.recv(100)
    screenLock.acquire()
    print('[+] %d/tcp open' % tgtPort)
    print('[+] ' + str(results))
  except:
    screenLock.acquire()
    print('[-] %d/tcp closed' % tgtPort)
  finally:
    screenLock.release()
    connSkt.close()


def portScan(tgtHost, tgtPorts):
  try:
    tgtIP = gethostbyname(tgtHost)
  except:
    print("[-] Cannot resolve '%s': Unknown host" % tgtHost)
    return

  try:
    tgtName = gethostbyaddr(tgtIP)
    print('\n[+] Scan Results for: ' + tgtName[0])
  except:
    print('\n[+] Scan Results for: ' + tgtIP)

  setdefaulttimeout(1)
  for tgtPort in tgtPorts:
    t = Thread(target=connScan, args=(tgtHost, int(tgtPort)))
    t.start()


# some global vars
num_threads = 32
ips_q = queue.Queue()
out_q = queue.Queue()

# build IP array

ips = []
for i in range(1,102):
  ips.append("192.168.0."+str(i))

# build IP array
#ips = []
#for i in range(1000):
#    num1 = random.randint(1, 191)
#    num2 = random.randint(0, 255)
#    num3 = random.randint(0, 255)
#    num4 = random.randint(0, 255)
#    ipAddr = str(num1) + "." + str(num2) + "." + str(num3) + "." + str(num4)
#    ips.append(ipAddr)
hosts_up = []
# thread code : wraps system ping command
def thread_pinger(i, q):
  """Pings hosts in queue"""
  while True:
    # get an IP item form queue
    ip_address = q.get()
    # ping it
    args=['/bin/ping', '-c', '1', '-W', '1', str(ip_address)]
    print(args)
    p_ping = subprocess.Popen(args,
                              shell=False,
                              stdout=subprocess.PIPE)
    # save ping stdout
    p_ping_out = str(p_ping.communicate()[0])

    if (p_ping.wait() == 0):

      # rtt min/avg/max/mdev = 22.293/22.293/22.293/0.000 ms
      search = re.search(r'rtt min/avg/max/mdev = (.*)/(.*)/(.*)/(.*) ms',
                         p_ping_out, re.M|re.I)
      ping_rtt = search.group(2)
      out_q.put("OK " + str(ip_address) + " rtt= "+ ping_rtt)
      #adds responding hosts to array.
      hosts_up.append(str(ip_address))

        #build  the method here that will portscan the hosts.

    # update queue : this ip is processed
    q.task_done()

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

# print result

while True:
  try:
    msg = out_q.get_nowait()
  except queue.Empty:
    break
  print(msg)

def main():
  for x in range(len(hosts_up)):
    portScan(hosts_up[x][1:-1], tgtPorts)

if __name__ == '__main__':
  main()