import sys
import os.path

def ip_file_valid():

    while True:
        ip_file = input("\nEnter full path and name of IP file: ")
        if os.path.isfile(ip_file) == True:
            print('\nFile {} exists\n'.format(ip_file))
            break
        else:
            print('Invalid path or filename!\nPlease try again')
            continue

    ip = open(ip_file, 'r')
    ip.seek(0)
    ip_list = ip.readlines()
    ip.close()
    return ip_list
