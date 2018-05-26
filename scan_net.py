#!/usr/bin/env python
# Version 1.0
import subprocess
from os import devnull, name
import argparse
import time
import re

start_time = time.time()

parser = argparse.ArgumentParser(
    description='You can Scan your wifi, LAN or a custom ip range for alive hosts')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-l', '--lan', action='store_true',
                   help='Scan connected LAN')
group.add_argument('-w', '--wifi', action='store_true',
                   help='Scan connected Wifi')
group.add_argument('-i', '--ip', type=str,
                   help='Specify an IP range with the flag -i i.e scan_net.py -c 1.1.1.1')
args = parser.parse_args()

print "\033[H\033[J"

line = '------------------------------------------------------'
ls = []
active = 0
dead = 0
devnull = open(devnull, 'wb')

if args.ip:
    for ix in range(1, 255):
        ip = args.ip.split('.')
        if len(ip) < 4:
            print "Error: Please input complete IP Address"
            exit()
        else:
            ip.pop()
            iprange = '.'.join(ip) + '.{0}'.format(ix)
            if not re.match("^[0-9.]*$", iprange):
                print "Error! Only numbers 0-9 and . seperators allowed! Input -h for help"
                exit()
            ls.append((iprange, subprocess.Popen(
                ['ping', '-c', '2', iprange], stdout=devnull)))
    while ls:
        for i, (iprange, proc) in enumerate(ls[:]):
            if proc.poll() is not None:
                ls.remove((iprange, proc))
                if proc.returncode == 0:
                    print('%s \033[32m Active\033[0m' % iprange)
                    active = active + 1
                else:
                    dead = dead + 1
        time.sleep(.04)
    devnull.close()
elif args.lan:
    for ix in range(1, 255):
        wip = subprocess.check_output(['hostname -i'], shell=True)
        ip = str(wip).split('.')
        ip.pop()
        iprange = '.'.join(ip) + '.{0}'.format(ix)
        ls.append((iprange, subprocess.Popen(
            ['ping', '-c', '2', iprange], stdout=devnull)))
    while ls:
        for i, (iprange, proc) in enumerate(ls[:]):
            if proc.poll() is not None:
                ls.remove((iprange, proc))
                if proc.returncode == 0:
                    print('%s \033[32m Active\033[0m' % iprange)
                    active = active + 1
                else:
                    dead = dead + 1
        time.sleep(.04)
    devnull.close()
elif args.wifi:
    for ix in range(1, 255):
        wip = subprocess.check_output(['hostname -I'], shell=True)
        wip.split()
        if len(wip) > 4:
            ip = wip[:9]
            iprange = ''.join(ip) + '.{0}'.format(ix)
        else:
            ip = str(wip).split('.')
            ip.pop()
            iprange = '.'.join(ip) + '.{0}'.format(ix)
        ls.append((iprange, subprocess.Popen(
            ['ping', '-c', '2', iprange], stdout=devnull)))
    while ls:
        for i, (iprange, proc) in enumerate(ls[:]):
            if proc.poll() is not None:
                ls.remove((iprange, proc))
                if proc.returncode == 0:
                    print('%s \033[32m Active\033[0m' % iprange)
                    active = active + 1
                else:
                    dead = dead + 1
        time.sleep(.04)
    devnull.close()

print line
print " Current Operating System \033[35m", name, "\033[0m"
print line
print " Active Hosts \033[32m [ ", active, " ]\033[0m"
print ''
print " Unreachable Hosts \033[31m [ ", dead, " ] \033[0m"
total_time = time.time() - start_time
print ''
print ' Time Elapsed : \033[34m% .3f Seconds\033[0m' % total_time
print line
