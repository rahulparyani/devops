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
indexPath=appPath+"/"
log=appPath+"logs/"
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

if ((willRestart=="true") or (willDeployStatic=="true")):
    def serverOffline():
        global f1
        sys.stdout.write('In serverOffline method\n')
        now = datetime.now()
        print("now =", now)
        dest=indexPath+"/index1.html"
        indexCount=len(fnmatch.filter(os.listdir(indexPath), 'index*.html'))
        print("files found",indexCount)
        if (indexCount==1):
            indexFileName=fnmatch.filter(os.listdir(indexPath), 'index*.html')
            indexPath1=indexPath+indexFileName[0]
            print(indexFileName[0])
            if (indexFileName[0]=="index1.html") :
                sys.stdout.write("Already Offline\n")
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>ALREADY OFFLINE</td><td width=50%>&#9888;</td></font></tr>".format(SCOLOR2)
            elif (indexFileName[0]=="index.html"):
                sys.stdout.write("index.html found\n")
                os.rename(indexPath1, dest)
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>OFFLINE</td><td width=50%>&#9989;</td></font></tr>".format(SCOLOR2)
            else:
                sys.stdout.write(indexPath1+" found\n")
                os.rename(indexPath1, dest)
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>OFFLINE</td><td width=50%>&#9989;</td></font></tr>".format(SCOLOR2)
    
        elif(indexCount > 1):
            emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>MULTIPLE INDEX FOUND</td><td width=50%>&#9888;</td></font></tr>".format(SCOLOR2)
            dest1=indexPath+"/index1_old.html"
            x="index1.html"
            indexPath1=indexPath+x
            x="index.html"
            indexPath2=indexPath+x
            if (os.path.exists(indexPath1)) and (os.path.exists(indexPath2)):
                os.rename(indexPath1, dest1)
                sys.stdout.write("Index1 to indexOld\n")
                os.rename(indexPath2, dest)
                sys.stdout.write("Index to index1")
            elif (not os.path.exists(indexPath1)) and (os.path.exists(indexPath2)):
                os.rename(indexPath2, dest)
                sys.stdout.write("Index to index1\n")
            elif (os.path.exists(indexPath1)) and (not os.path.exists(indexPath2)):
                sys.stdout.write("Already Offline\n")
            else:
                sys.stdout.write("Index not found\n")
        else:
            sys.stdout.write("Index not found\n")
            f1="true"
            emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>INDEX NOT FOUND</td><td width=50%>&#9888;</td></font></tr>".format(SCOLOR2)
        return emailBody1
        sys.stdout.write ('Exit from serverOffline method\n')
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
    
    def copyStatic():
        global f1
        sys.stdout.write ('In copyStatic method\n')
        now = datetime.now()
        print("now =", now)
        src=rtdPath+rtdFolder+"deployments/*"
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

    def serverOnline():
        global f1
        global proceed
        global onLine
        sys.stdout.write('In serverOnline method\n')
        now = datetime.now()
        print("now =", now)
        dest=indexPath+"/index.html"
        indexCount=len(fnmatch.filter(os.listdir(indexPath), '*index*.*html*'))
        print("files found",indexCount)
        if (indexCount==1):
            indexFileName=fnmatch.filter(os.listdir(indexPath), '*index*.*html*')
            indexPath1=indexPath+indexFileName[0]
            print(indexFileName[0])
            if (indexFileName[0]=="index.html") :
                sys.stdout.write("Already Online\n")
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>ALREADY ONLINE</td><td width=50%>&#9888;</td></font></tr>".format(SCOLOR2)
                proceed="true"
                onLine="true"
            else:
                sys.stdout.write(indexPath1+" found\n")
                os.rename(indexPath1, dest)
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>ONLINE</td><td width=50%>&#9989;</td></font></tr>".format(SCOLOR2)
                proceed="true"
                onLine="true"
        
        elif(indexCount > 1):
            indexPath1=indexPath+"index1.html"
            indexPath2=indexPath+"index.html"
            if os.path.exists(indexPath1):
                os.rename(indexPath1, dest)
                sys.stdout.write("Index1 to index\n")
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>ONLINE</td><td width=50%>&#9989;</td></font></tr>".format(SCOLOR2)
                proceed="true"
                onLine="true"
            elif os.path.exists(indexPath2):
                sys.stdout.write("Already Online\n")
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>ALREADY ONLINE</td><td width=50%>&#9888;</td></font></tr>".format(SCOLOR2)
                proceed="true"
                onLine="true"
            else:
                sys.stdout.write("Index1 not found\n")
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>Index1 NOT FOUND</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
                f1="true"
        else:
            sys.stdout.write("Index1 not found\n")
            emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>Index1 NOT FOUND</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
            f1="true"
        return emailBody1
        sys.stdout.write ('Exit from serverOnline method\n')        
        
    def main():
        global f1
        if len(serviceName) > 1:
            if willRestart=="true":
                if os.path.exists(appPath):
                    if willOffline=="true":
                        emailBody1=emailBody+serverOffline()
                        if willWait=="true":
                            time.sleep(20)
                        if ((willServiceStop=="true") and (f1 != "true")):
                            serviceStatus=queryServiceStatus()
                            if serviceStatus=='unknown':
                                sys.stdout.write(serviceName+' service is '+serviceStatus+'\n')
                                emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>{}</td><td width=50%>PROBLEM IN SERVICE NAME</td></font></tr></table></body></html><br><br>".format(FCOLOR2,server1)
                                f1="true"
                            else:
                                sys.stdout.write(serviceName+' is found and in '+serviceStatus+' mode\n')
                                isServiceStopped=serviceStop()
                                if isServiceStopped=="true":
                                    sys.stdout.write('service stopped successfully\n')
                                    emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>SERVICE STOPPED</td><td width=50%> &#9989;</td></font></tr>".format(SCOLOR2)
                                    if ((willDeployStatic=="true") and (f1 != "true")):
                                        emailBody1=emailBody1+copyStatic()
                                        
                                    if ((willServiceStart=="true") and (f1 != "true")):
                                        isServiceStarted=serviceStart()
                                        if isServiceStarted=="true":
                                            sys.stdout.write('service started successfully\n')
                                            emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>SERVICE STARTED</td><td width=50%> &#9989;</td></font></tr>".format(SCOLOR2)
                                            if willOnline=="true":
                                                emailBody1=emailBody1+serverOnline()
                                            if onLine=="true":
                                                emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>DEPLOYMENT STATUS</td><td width=50%>SUCCESSFUL<BR> &#9989;</td></font></tr></table></body></html><br><br>".format(SCOLOR2)
                                            else:
                                                emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>DEPLOYMENT STATUS</td><td width=50%>FAILED<BR>&#10060;</td></font></tr></table></body></html><br><br>".format(FCOLOR2)
                                                f1="true"                                            
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
                         sys.stdout.write('willOffline is '+willOffline+'\n')
                         emailBody1=emailBody+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>willOffline is {}</td><td width=50%>&#10060;</td></font></tr></table></body></html><br><br>".format(FCOLOR2,willOffline)
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