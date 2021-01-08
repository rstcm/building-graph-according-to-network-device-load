import paramiko
import os.path
import sys
import time
import re
import datetime

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
        


        
    