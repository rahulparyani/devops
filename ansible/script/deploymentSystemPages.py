# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 14:08:47 2020

@author: parthjadav

Edited on : 24-12-2021

@author: Kunal Parekh

Removed deployments folder from src variable in CopyStatic Method.

Edited on : 27-04-2022

@author: Kunal Parekh

Added deployments folder in src variable in CopyStatic Method.


"""
import os
import sys
import time
import subprocess
import fnmatch
from datetime import datetime

server=str(sys.argv[3])
server1=(server.upper())
app=str(sys.argv[4])
app1=(app.upper())
env=str(sys.argv[5])
serviceName=str(sys.argv[6])
dc=str(sys.argv[7])
staticFolder=str(sys.argv[8])
rtdFolder=str(sys.argv[9])
rtdPath=str(sys.argv[10])
earName=str(sys.argv[11])
willWaitBServer=str(sys.argv[12])
prvfle=str(sys.argv[13])

willRestart=str(sys.argv[1])
willDeployStatic=str(sys.argv[2])

if (willDeployStatic=="true"):
    willRestart="true"

FCOLOR1="#E85F47"
FCOLOR2="#F5DDC5"
SCOLOR1="#70AD47"
SCOLOR2="#E2EFD9"

willOffline="true"
willOnline="true"
willWait="true"
willServiceStop="true"
willServiceStart="true"

appPath="/data/asitemicroapps/"+app+"/"
static=appPath
    
f1=None
nothing=None
proceed=None
deployed=None
failed=None
unDeployed=None
status=None
onLine=None
earOrWar=None
timeTaken=None
continueToNext=None

emailBody="<html><body><table style='border:1px solid' align='center' bgcolor='{}' style='width:50%'><tr><font size='3' color='white' face='calibri'><th colspan='2' align='center'>{}<BR>{}<BR>{}</th></font></tr>".format(SCOLOR1,app1,env,server1)

if (willDeployStatic=="true"):
   
    def copyStatic():
        global f1
        sys.stdout.write ('In copyStatic method\n')
        now = datetime.now()
        print("now =", now)
        src=rtdPath+rtdFolder+"/deployments/*"
        try:
            p=subprocess.run(["scp","-i","/etc/ansible/"+prvfle+"","-r","-q",src,static], stderr=subprocess.PIPE, universal_newlines=True)
            if p.returncode == 0:
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>STATIC FILES</td><td width=50%>&#9989;</td></font></tr>".format(SCOLOR2)
                print("Static files are copied")
            else:
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>STATIC FOLDER IS EMPTY OR NOT EXISTS</td><td width=50%>&#9888;</td></font></tr>".format(SCOLOR2)
                print("Static folder is empty or not exists", p.stderr)
        except OSError as e:
            emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROBLEM OCCURED WHILE COPYING STATIC FILES</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
            print("Problem occured while copying static files", p.stderr)
            f1="true"
            print(sys.stderr, "Execution failed:", e)
        return emailBody1        
        sys.stdout.write ('Exit from copyStatic method\n')

                        
    def main():
        global f1
        if (willDeployStatic=="true"):
                if os.path.exists(appPath):
                    if ((willDeployStatic=="true") and (f1 != "true")):
                        emailBody1=emailBody+copyStatic()
                else:
                    sys.stdout.write(app+' NOT FOUND IN '+server+'\n')
                    emailBody1=emailBody+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>{} NOT FOUND IN {}</td><td width=50%>&#10060;</td></font></tr></table></body></html><br><br>".format(FCOLOR2,app1,server1)
                    f1="true"
        return emailBody1
    emailBody=main()
    if f1 != "true":
        emailSubject="{}-{}-{} DEPLOYMENT PROCESS SUCCESSFUL".format(app1,env,dc)
        sys.stdout.write('Go for next instance\n')
    elif continueToNext=="true":
        emailSubject="{}-{}-{} DEPLOYMENT PROCESS FAILED".format(app1,env,dc)
        sys.stdout.write('Go for next instance\n')
    else:
        emailSubject="{}-{}-{} DEPLOYMENT PROCESS FAILED".format(app1,env,dc)
else:
    emailSubject="{}-{}-{} DEPLOYMENT PROCESS FAILED".format(app1,env,dc)
    emailBody="Please select atleast one option"
    



sys.stdout.write("Email Subject ")
sys.stdout.write(emailSubject)
sys.stdout.write("For Email ")
sys.stdout.write(emailBody)
