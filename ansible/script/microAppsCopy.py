# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 14:34:21 2022

@author: kparekh
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

def copyMicroApps(appName, apachePath, microPath):
    """
    Copy the structure and related files
    """
    if (microPath):
        if (microPath.lower() != "none"):
            copyMicroFolder(appName, microPath)
            copyConsulClient(appName)
        else:
            print ("MicroApp Path set to None so skipping MicroApp Folder Deployment")
    else:
        print("MicroApp Path did not pass to function")
    if (apachePath):
        if (apachePath.lower() != "none"):
            copyApacheConfFiles(appName, apachePath)
        else:
            print("Apache Path is None so skipping Conf File Deoployment")
    else:
        print("Apache Path did not pass to function")
    
def copyMicroFolder(appName, microPath):
    if appName :
        command = ('cp -rf techops_appconfig/{}/{} {} && echo \'MicroApp Folder Deployment Complete\''.format(appName, appName, microPath))
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
        print ("Consul not present for {}".format(appName))

         
n = len(sys.argv)
print("Total Apps passed:", n-1)
if(n>1):
    if (n>3):
        if((re.match('^.+conf[.]d.?\\/$',sys.argv[1])) or (sys.agrv[1].lower() == "none")):
            if(re.match('^.+asitemicroapps\\/$',sys.argv[2]) or (sys.agrv[2].lower() == "none")):
                cloneGitRepo()
                for i in range(3,n):
                    print("Apache Path:", sys.argv[1])
                    print("MicroApp Path:", sys.argv[2])
                    if ("," not in sys.argv[i]):
                         print("Application Name:", sys.argv[i])
                         print(" Lower case :", sys.argv[i].lower())
                         copyMicroApps(sys.argv[i].lower(), sys.argv[1].lower(), sys.argv[2].lower())
                    else:
                        print("Please pass Application name as command line Argument (space seprated)")
            else:
                print("Please pass the MicroApp Path till asitemicroapps/ folder make sure that last '/' is present (Path is case sensitive)")
        else:
            print("Please pass the Apache Path till conf.d/ folder make sure that last '/' is present (Path is case sensitive)")
    else:
        print("Please pass Application name as command line Argument (space seprated)")
else:
    print ("Please give arguments in this manner: ApachePath MicroPath ApplicationName1 ApplicationName2 ...")
    print('Note:')
    print("Please pass the MicroApp Path till asitemicroapps/ folder make sure that last '/' is present (Path is case sensitive)")
    print("Please pass the Apache Path till conf.d/ folder make sure that last '/' is present (Path is case sensitive)")