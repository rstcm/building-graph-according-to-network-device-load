import sys

def ip_addr_valid(ip_list):
    for ip in ip_list:
        ip = ip.rstrip('\n')
        ip_octets = ip.split('.')
        if (len(ip_octets ) == 4) and (int(ip_octets[0]) != 127) and (1 <= int(ip_octets[0]) <= 223) and (int(ip_octets[0]) != 169 or int(ip_octets[0]) != 254) and (0 <= int(ip_octets[1]) <= 255 and 0 <= int(ip_octets[2]) <= 255 and 0 <= int(ip_octets[3]) <= 255):
            continue
        else:
            print('There was an invalid IP address in file: {}'.format(ip))
            sys.exit()
#ip_addr_valid(['192.168.10.100'])
