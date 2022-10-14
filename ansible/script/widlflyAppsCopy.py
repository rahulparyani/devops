# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 13:33:04 2022

@author: Kunal Parekh
"""
import sys
import re
import subprocess
import glob


def cloneGitRepo():
    """
    Cloning the Repo
    """
    command = ('git clone https://jenkinsbuilds1:asite987@bitbucket.org/asitesol/techops_appconfig.git')
    ssh=subprocess.call(command, stdout=subprocess.PIPE, shell=True)
    if ssh == 0:
        print ('Cloned')
    else:
        print('Error in Clone')

def copyWildflyApps(appName, apachePath, wildflyPath):
    """
    Copy the structure and related files
    """
    if (wildflyPath):
        if (wildflyPath.lower() != "none"):
            copyWildflyFolder(appName, wildflyPath)
            copyWildflyServiceFolder(appName, wildflyPath)
            copyConsulClient(appName)
        else:
            print ("Wildfly Path set to None so skipping Wildfly Service and Wildfly Folder Deployment and Consul")
    else:
        print("Wildfly Path did not pass to function")
    if (apachePath):
        if (apachePath.lower() != "none"):
            copyApacheConfFiles(appName, apachePath)
        else:
            print("Apache Path is None so skipping Conf File Deoployment")
    else:
        print("Apache Path did not pass to function")
    
def copyWildflyFolder(appName, wildflyPath):
    if appName :
        command = ('cp -rf techops_appconfig/{}/{} {} && echo \'Wildfly Folder Deployment Complete\''.format(appName, appName, wildflyPath))
        ssh=subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        result = ssh.stdout.readlines()
        if result == []:
         error = ssh.stderr.readlines()
         print (sys.stderr, "ERROR: %s" % error)
        else:
         print (b''.join(result).decode('utf-8'))
    else:
        print ("appName is not passed to function")
    
def copyWildflyServiceFolder(appName, wildflyPath):
     if appName :
        command = ('cp -rf techops_appconfig/{}/service_* {}/bin && echo \'Wildfly Service Folder Deployment Complete\''.format( appName, wildflyPath))
        ssh=subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        result = ssh.stdout.readlines()
        if result == []:
         error = ssh.stderr.readlines()
         print (sys.stderr, "ERROR: %s" % error)
        else:
         print (b''.join(result).decode('utf-8'))
     else:
         print ("appName is not passed to function")
         
def copyApacheConfFiles(appName, apachePath):
     if appName :
         command = ('cp -f techops_appconfig/{}/*.conf {} && echo \'Conf File Deoployment Complete\''.format(appName, apachePath))
         ssh=subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
         result = ssh.stdout.readlines()
         if result == []:
          error = ssh.stderr.readlines()
          print (sys.stderr, "ERROR: %s" % error)
         else:
          print (b''.join(result).decode('utf-8'))
     else:
         print ("appName is not passed to function")

def copyConsulClient(appName):
    consulPath="techops_appconfig/consul/*{}client*".format(appName)
    if glob.glob(consulPath):
        command = ('mkdir -p /data/asitemicroapps/consul && cp -rf {} /data/asitemicroapps/consul && echo \'Consul Deoployment Complete\''.format(consulPath))
        ssh=subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        result = ssh.stdout.readlines()
        if result == []:
         error = ssh.stderr.readlines()
         print (sys.stderr, "ERROR: %s" % error)
        else:
         print (b''.join(result).decode('utf-8'))
    else:
        print ("Consul is not present for {}".format(appName))
         
n = len(sys.argv)
print("Total Apps passed:", n-1)
if(n>1):
    if (n>3):
        if((re.match('^.+conf[.]d.?\\/$',sys.argv[1])) or (sys.argv[1].lower() == "none")):
            if(re.match('^.+wildfly[-]9[.]0[.]1[.]Final\\/$',sys.argv[2]) or (sys.argv[2].lower() == "none")):
                cloneGitRepo()
                for i in range(3,n):
                    print("Apache Path:", sys.argv[1])
                    print("Wildfly Path:", sys.argv[2])
                    if ("," not in sys.argv[i]):
                         print("Application Name:", sys.argv[i])
                         print(" Lower case :", sys.argv[i].lower())
                         copyWildflyApps(sys.argv[i].lower(), sys.argv[1], sys.argv[2])
                    else:
                        print("Please pass Application name as command line Argument (space seprated)")
            else:
                print("Please pass the Wildfly Path till wildfly-9.0.1.Final/ folder make sure that last '/' is present (Path is case sensitive)")
        else:
            print("Please pass the Apache Path till conf.d/ folder make sure that last '/' is present (Path is case sensitive)")
    else:
        print("Please pass Application name as command line Argument (space seprated)")
else:
    print ("Please give arguments in this manner: ApachePath WildflyPath ApplicationName1 ApplicationName2 ...")
    print('Note:')
    print("Please pass the Wildfly Path till wildfly-9.0.1.Final/ folder make sure that last '/' is present (Path is case sensitive)")
    print("Please pass the Apache Path till conf.d/ folder make sure that last '/' is present (Path is case sensitive)")