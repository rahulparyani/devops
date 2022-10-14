"""
Created on 24-09-2020

@author: Kunal Parekh

"""
import subprocess

 

def installApache():
    """
    Install Apache application on a fresh server
    """

 

    command=('yum install httpd -y &&'
             'yum install mod_ssl -y &&'
             'yum install mod_security -y &&'
             'yum install mod_security_crs -y &&'
             'wget -O /opt/mod_evasive24.so https://pranav-test-files.s3.eu-west-2.amazonaws.com/mod_evasive24.so &&'
             'wget -O /opt/mod_jk.so https://pranav-test-files.s3.eu-west-2.amazonaws.com/mod_jk.so &&'
             'yum install epel-release -y &&'
             'dnf install https://pkgs.dyn.su/el8/base/x86_64/raven-release-1.0-1.el8.noarch.rpm -y &&'
             'dnf --enablerepo=raven-extras install mod_evasive -y')
    ssh=subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    result = ssh.stdout.readlines()
    if result == []:
     error = ssh.stderr.readlines()
     print >>sys.stderr, "ERROR: %s" % error
    else:
     print (b''.join(result).decode('utf-8'))

 

installApache()
 