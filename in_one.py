import sys
import os.path
import time
import datetime
import subprocess
import paramiko
import re
import threading

import matplotlib.pyplot as pyp
import matplotlib.animation as animation

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
    
#############################################################

def ip_addr_valid(ip_list):
    for ip in ip_list:
        ip = ip.rstrip('\n')
        ip_octets = ip.split('.')
        if (len(ip_octets ) == 4) and (int(ip_octets[0]) != 127) and (1 <= int(ip_octets[0]) <= 223) and (int(ip_octets[0]) != 169 or int(ip_octets[0]) != 254) and (0 <= int(ip_octets[1]) <= 255 and 0 <= int(ip_octets[2]) <= 255 and 0 <= int(ip_octets[3]) <= 255):
            continue
        else:
            print('There was an invalid IP address in file: {}'.format(ip))
            sys.exit()

###################################################################

def ip_reach(iplist):
    for ip in iplist:
        ip = ip.rstrip('\n')

        ping_reply = subprocess.call('ping %s /n 2' %(ip), stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
        if ping_reply == 0:
            print('\n *{} is reachable \n'.format(ip))

        else:
            print('\n Sorry, {} is not reachable :( Check connectivity and try again \n'.format(ip))
            sys.exit()

########################################################################

while True:

    userfile = input('\nEnter full path for a user file: ')
    if os.path.isfile(userfile) == True:
        print("\n{} file exists".format(userfile))
        break

    else:
        print("\n{} file does not exist. Please check full path and try again.\n".format(userfile))


        
while True:

    cmdfile = input('\nEnter full path for a cmd file: ')
    if os.path.isfile(cmdfile) == True:
        print("\n{} file exists".format(cmdfile))
        break

    else:
        print("\n{} file does not exist. Please check full path and try again.\n".format(cmdfile))
        
def ssh_connection(ip):
    try:
     
        global cmdfile
        global userfile
        
        user_file = open(userfile, 'r')
        user_file.seek(0)
        username = user_file.readlines()[0].split(',')[0].rstrip('\n')
        user_file.seek(0)
        password = user_file.readlines()[0].split(',')[1].rstrip('\n')
        user_file.close()
         
        session = paramiko.SSHClient()
         
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy)
         
        session.connect(ip.rstrip('\n'), username = username, password = password)
         
        connection = session.invoke_shell()
         
         
        connection.send('enable\n')
        connection.send('terminal length 0\n')
        time.sleep(1)
        
        cmd_file = open(cmdfile, 'r')
        cmd_file.seek(0)
         
        for command in cmd_file.readlines():
            connection.send(command.rstrip('\n') + '\n')
            time.sleep(2)
            
        cmd_file.close()
        
        output = connection.recv(65535)
        
        if re.search(b'% Invalid input', output):
            print('\nThere was at least one IOS syntax error on device {}'.format(ip))
        
        else: 
            print("Done for a device {}\nData sent to file at {}\n\n".format(ip, str(datetime.datetime.now())))
            
        cpu = re.search(b"%Cpu\(s\):(\s)+(.+?)(\s)* us,", output)
        utilization = cpu.group(2).decode('utf-8')
        
        with open("D:\\netapp\\3_build_graph\\cpu.txt", 'a') as f:
            f.write(utilization + '\n')
         
            
    except paramiko.AuthenticationException:
        print('* Invalid username or password \n Please check username/password file and device configuration.\n')
        print('* Closing program... Bye!')

######################################################################################

def create_threads(iplist, function):
    threads = []
    for ip in iplist:
        th = threading.Thread(target = function, args = (ip,))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()
        
#################################################################################

ip_list = ip_file_valid()

try:
    ip_addr_valid(ip_list)
except KeyboardInterrupt:
    print("Program was aborted by user!")
    sys.exit()

try:
    ip_reach(ip_list)
except KeyboardInterrupt:
    print("Program was aborted by user!")
    sys.exit()

while True:
    create_threads(ip_list, ssh_connection)
    time.sleep(10)
    
    #Creating new figure
    figure = pyp.figure()
    figure.clear()

    #Creating subplot with 1 row, 1 column, and index 1 meaning single subplot
    subplot = figure.add_subplot(1, 1, 1)
    subplot.clear()

    def animation_function(i):

        cpu_data = open("D:\\netapp\\3_build_graph\\cpu.txt").readlines()

        x = []

        for each_value in cpu_data:
            if len(each_value) > 1:
                x.append(float(each_value))

        #Clearing/Refreshing the figure to avoid overwriting for each new poll (every 10 seconds)
        subplot.clear()

        #Plotting the values in the list
        subplot.plot(x)

    #Using the figure, the function and polling interval of 10000ms (10 seconds) to build the graph
    graph_animation = animation.FuncAnimation(figure, animation_function, interval = 10000)

    #Displaying the grapgh to the screen
    pyp.show()

     