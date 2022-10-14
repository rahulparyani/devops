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

FCOLOR1="#E85F47"
FCOLOR2="#F5DDC5"
SCOLOR1="#70AD47"
SCOLOR2="#E2EFD9"

willWait="true"
willServiceStop="true"
willServiceStart="true"

appPath="/etc/httpd/"
static=appPath
    
f1=None
status=None
continueToNext=None

emailBody="<html><body><table style='border:1px solid' align='center' bgcolor='{}' style='width:50%'><tr><font size='3' color='white' face='calibri'><th colspan='2' align='center'>{}<BR>{}<BR>{}</th></font></tr>".format(SCOLOR1,app1,env,server1)

if ((willRestart=="true") or (willDeployStatic=="true")):
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
        while count < 30:
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
    
    def copyStatic():
        global f1
        sys.stdout.write ('In copyStatic method\n')
        now = datetime.now()
        print("now =", now)
        src=rtdPath+rtdFolder+"/*"
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
        if len(serviceName) > 1:
            if willRestart=="true":
                if os.path.exists(appPath):
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
                                if ((willDeployStatic=="true") and (f1 != "true")):
                                    emailBody1=emailBody1+copyStatic()
                                        
                                if ((willServiceStart=="true") and (f1 != "true")):
                                    isServiceStarted=serviceStart()
                                    if isServiceStarted=="true":
                                        sys.stdout.write('service started successfully\n')
                                        emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>SERVICE STARTED</td><td width=50%> &#9989;</td></font></tr>".format(SCOLOR2)
                                        emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>DEPLOYMENT STATUS</td><td width=50%>SUCCESSFUL<BR> &#9989;</td></font></tr></table></body></html><br><br>".format(SCOLOR2)
                                    else:
                                        sys.stdout.write('service could not started due to some reasons\n')
                                        emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>SERVICE STARTED</td><td width=50%>&#10060;</td></font></tr></table></body></html><br><br>".format(FCOLOR2)
                                        emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>DEPLOYMENT STATUS</td><td width=50%>FAILED<BR>&#10060;</td></font></tr></table></body></html><br><br>".format(FCOLOR2)
                                        f1="true"
                            else:
                                sys.stdout.write('service could not stopped due to some reasons\n')
                                emailBody1=emailBody+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>SERVICE STOPPED</td><td width=50%>&#10060;</td></font></tr></table></body></html><br><br>".format(FCOLOR2)
                                f1="true"
                    else:
                        sys.stdout.write('willServiceStop is '+willServiceStop+' and f1 is '+f1+'\n')
                        emailBody1=emailBody+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>INDEX FILE NOT FOUND </td><td width=50%>&#10060;</td></font></tr></table></body></html><br><br>".format(FCOLOR2,willServiceStop)
                        f1="true"
                else:
                    sys.stdout.write(app+' NOT FOUND IN '+server+'\n')
                    emailBody1=emailBody+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>{} NOT FOUND IN {}</td><td width=50%>&#10060;</td></font></tr></table></body></html><br><br>".format(FCOLOR2,app1,server1)
                    f1="true"
            else:
                emailBody1=emailBody
                if (willDeployStatic=="true"):
                    emailBody1=emailBody1+copyStatic()
                if (f1 != "true"):
                    emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>DEPLOYMENT STATUS</td><td width=50%>SUCCESSFUL<BR> &#9989;</td></font></tr></table></body></html><br><br>".format(SCOLOR2)
                else:
                    emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>DEPLOYMENT STATUS</td><td width=50%>FAILED<BR>&#10060;</td></font></tr></table></body></html><br><br>".format(FCOLOR2)
        else:
            emailBody1=emailBody+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>{}</td><td width=50%>PROBLEM IN SERVICE NAME</td></font></tr>".format(FCOLOR2,server1)
            emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>{}</td><td width=50%>PLEASE GIVE CORRECT NAME OF SERVICE IN VARIABLE</td></font></tr></table></body></html><br><br>".format(FCOLOR2,server1)
            print ('PROBLEM IN SERVICE NAME \nPLEASE GIVE CORRECT NAME OF SERVICE IN VARIABLE')
            f1="true"
    
        return emailBody1

    if ((willWaitBServer=="true") and (willRestart=="true")):
        if app=="Servicemix":
            sys.stdout.write('WAITING FOR 60 SECONDS BEFORE TAKING NEXT INSTANCE OFFLINE :::\n')
            time.sleep(60)
        else:
            sys.stdout.write('WAITING FOR 30 SECONDS BEFORE TAKING NEXT INSTANCE OFFLINE :::\n')
            time.sleep(30)
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