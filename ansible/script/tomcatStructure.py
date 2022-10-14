"""
Created on 13-04-2020

@author: Kunal Parekh
"""
import subprocess

def tomcatStructure():
    """
    Copy structure of tomcat v8.0.29 on a fresh server
    """

    command = ('yum install java-1.8.0-openjdk-devel -y &&'
              'wget -O /tmp/apache-tomcat-8.0.29.tar.gz https://archive.apache.org/dist/tomcat/tomcat-8/v8.0.29/bin/apache-tomcat-8.0.29.tar.gz &&'
              'tar zxvf  /tmp/apache-tomcat-8.0.29.tar.gz -C /opt/ &&'
              'rm -f  /tmp/apache-tomcat-8.0.29.tar.gz &&'
              'mv /opt/apache-tomcat-8.0.29 /data/tomcat ')
    ssh=subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    result = ssh.stdout.readlines()
    if result == []:
     error = ssh.stderr.readlines()
     print >>sys.stderr, "ERROR: %s" % error
    else:
     print (b''.join(result).decode('utf-8'))

tomcatStructure()
