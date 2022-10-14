# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 14:08:47 2020

@author: parthjadav
"""
import os
import sys
import time
import subprocess
import fnmatch
from datetime import datetime

server=str(sys.argv[2])
server1=(server.upper())
app=str(sys.argv[3])
app1=(app.upper())
env=str(sys.argv[4])
serviceName=str(sys.argv[5])
dc=str(sys.argv[6])
willWaitBServer=str(sys.argv[7])
prvfle=str(sys.argv[8])

willRestart=str(sys.argv[1])

FCOLOR1="#E85F47"
FCOLOR2="#F5DDC5"
SCOLOR1="#70AD47"
SCOLOR2="#E2EFD9"

willWait="true"
willServiceStop="true"
willServiceStart="true"

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

if (willRestart=="true"):
    def queryServiceStatus():
        sys.stdout.write('In queryServiceStatus method\n')
        serviceStatus=os.popen('systemctl is-active '+serviceName)
        serviceStatus=serviceStatus.read()
        serviceStatus=serviceStatus.strip()
        return serviceStatus
        
    def serviceStart():
        sys.stdout.write ('In serviceStart method\n')
        now = datetime.now()
        print("now =", now)        
        os.popen('systemctl start '+serviceName)
        isServiceStarted="false"
        count=0
        while count < 90:
            serviceStatus=queryServiceStatus()
            sys.stdout.write('serviceStart -> while loop\n')
            count1=str(count)
            if serviceStatus=='active':
                sys.stdout.write('Count is '+count1+' and serviceStatus is '+serviceStatus+'\n')
                isServiceStarted="true"
                break
            time.sleep(2)
            count=count + 1
        sys.stdout.write ('Exit from serviceStart method\n')
        return isServiceStarted
            
    def serviceStop():
        sys.stdout.write ('In serviceStop method\n')
        now = datetime.now()
        print("now =", now)
        os.popen('systemctl stop '+serviceName)
        isServiceStopped="false"
        count=0
        while count < 90:
            serviceStatus=queryServiceStatus()
            sys.stdout.write('serviceStop -> while loop\n')
            count1=str(count)
            if ((serviceStatus == 'inactive') or (serviceStatus == 'failed')):
                sys.stdout.write ('Count is '+count1+' and serviceStatus is '+serviceStatus+'\n')
                isServiceStopped="true"
                break
            time.sleep(2)
            count=count + 1
        sys.stdout.write ('Exit from serviceStop method\n')
        return isServiceStopped
    
    def main():
        global f1
        if len(serviceName) > 1:
            if willRestart=="true":
                if willWait=="true":
                    time.sleep(20)
                if ((willServiceStop=="true") and (f1 != "true")):
                    serviceStatus=queryServiceStatus()
                    if serviceStatus=='unknown':
                        sys.stdout.write(serviceName+' service is '+serviceStatus+'\n')
                        emailBody1=emailBody+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>{}</td><td width=50%>PROBLEM IN SERVICE NAME</td></font></tr></table></body></html><br><br>".format(FCOLOR2,server1)
                        f1="true"
                    else:
                        sys.stdout.write(serviceName+' is found and in '+serviceStatus+' mode\n')
                        isServiceStopped=serviceStop()
                        if isServiceStopped=="true":
                            sys.stdout.write('service stopped successfully\n')
                            emailBody1=emailBody+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>SERVICE STOPPED</td><td width=50%> &#9989;</td></font></tr>".format(SCOLOR2)
                                        
                            if ((willServiceStart=="true") and (f1 != "true")):
                                isServiceStarted=serviceStart()
                                if isServiceStarted=="true":
                                    sys.stdout.write('service started successfully\n')
                                    emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>SERVICE STARTED</td><td width=50%> &#9989;</td></font></tr>".format(SCOLOR2)
                                else:
                                    sys.stdout.write('service could not started due to some reasons\n')
                                    emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>SERVICE STARTED</td><td width=50%>&#10060;</td></font></tr></table></body></html><br><br>".format(FCOLOR2)
                                    f1="true"
                        else:
                            sys.stdout.write('service could not stopped due to some reasons\n')
                            emailBody1=emailBody+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>SERVICE STOPPED</td><td width=50%>&#10060;</td></font></tr></table></body></html><br><br>".format(FCOLOR2)
                            f1="true"
                else:
                    sys.stdout.write('willServiceStop is '+willServiceStop+' and f1 is '+f1+'\n')
                    emailBody1=emailBody+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>INDEX FILE NOT FOUND</td><td width=50%>&#10060;</td></font></tr></table></body></html><br><br>".format(FCOLOR2,willServiceStop)
                    f1="true"
        else:
            emailBody1=emailBody+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>{}</td><td width=50%>PROBLEM IN SERVICE NAME</td></font></tr>".format(FCOLOR2,server1)
            emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>{}</td><td width=50%>PLEASE GIVE CORRECT NAME OF SERVICE IN VARIABLE</td></font></tr></table></body></html><br><br>".format(FCOLOR2,server1)
            print ('PROBLEM IN SERVICE NAME \nPLEASE GIVE CORRECT NAME OF SERVICE IN VARIABLE')
            f1="true"
    
        return emailBody1

    if ((willWaitBServer=="true") and (willRestart=="true")):
            time.sleep(30)

    emailBody=main()
    if f1 != "true":
        emailSubject="{}-{}-{} RESTART PROCESS SUCCESSFUL".format(app1,env,dc)
        sys.stdout.write('Go for next instance\n')
    elif continueToNext=="true":
        emailSubject="{}-{}-{} RESTART PROCESS FAILED".format(app1,env,dc)
        sys.stdout.write('Go for next instance\n')
    else:
        emailSubject="{}-{}-{} RESTART PROCESS FAILED".format(app1,env,dc)
else:
    emailSubject="{}-{}-{} RESTART PROCESS FAILED".format(app1,env,dc)
    emailBody="Please select atleast one option"
    



sys.stdout.write("Email Subject ")
sys.stdout.write(emailSubject)
sys.stdout.write("For Email ")
sys.stdout.write(emailBody)