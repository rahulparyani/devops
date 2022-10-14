"""
Created on 10-04-2020

@author: Kunal Parekh
"""
import subprocess

def wildflyStructure():
    """
    Copy wildfly structure on a fresh server
    """

    command = ('yum install java-1.8.0-openjdk-devel -y &&'
              'wget -O /tmp/wildfly-9.0.1.Final.zip http://download.jboss.org/wildfly/9.0.1.Final/wildfly-9.0.1.Final.zip &&'
              'unzip /tmp/wildfly-9.0.1.Final.zip -d /data/ &&'
              'rm -f /tmp/wildfly-9.0.1.Final.zip ')

    ssh=subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    result = ssh.stdout.readlines()
    if result == []:
     error = ssh.stderr.readlines()
     print >>sys.stderr, "ERROR: %s" % error
    else:
     print (b''.join(result).decode('utf-8'))

wildflyStructure()

