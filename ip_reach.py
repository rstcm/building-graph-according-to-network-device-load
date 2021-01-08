import sys
import subprocess

def ip_reach(iplist):
        for ip in iplist:
            ip = ip.rstrip('\n')

            ping_reply = subprocess.call('ping {} /n 2'.format(ip), stdout =subprocess.DEVNULL, stderr = subprocess.DEVNULL)
            if ping_reply == 0:
                print("\n{} is reachable".format(ip))
            else:
                print("\n{} is not reachable".format(ip))
                sys.exit()

