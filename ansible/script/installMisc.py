"""
Created on 09-04-2020

@author: Kunal Parekh

"""
import subprocess

 

def installMisc():
    """
    Install all Misc applications on a fresh server
    """

 

    command =('yum install epel-release -y &&'
              'yum install --enablerepo=PowerTools wget unzip zip lnav htop vim lsof telnet git cifs-utils git-lfs -y')
    ssh=subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    result = ssh.stdout.readlines()
    if result == []:
     error = ssh.stderr.readlines()
     print >>sys.stderr, "ERROR: %s" % error
    else:
     print (b''.join(result).decode('utf-8'))

 

installMisc()