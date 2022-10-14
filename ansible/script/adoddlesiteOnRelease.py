# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 14:08:47 2020

@author: parthjadav
"""
import smtplib
import os
import sys
import subprocess
import shutil
from datetime import datetime
import socket

server=str(sys.argv[9])
print("server =", server)
server1=(server.upper())
print("server1 =", server1)


print(socket.gethostname())
server=socket.gethostname()
print("server =", server)
server1=(server.upper())
print("server1 =", server1)

app=str(sys.argv[10])
app1=(app.upper())
env=str(sys.argv[11])
serviceName=str(sys.argv[12])
dc=str(sys.argv[13])
staticFolder=str(sys.argv[14])
rtdFolder=str(sys.argv[15])
rtdPath=str(sys.argv[16])
earName=str(sys.argv[17])
willWaitBServer=str(sys.argv[18])
prvfle=str(sys.argv[19])

willRestart=str(sys.argv[1])
willDeployConf=str(sys.argv[2])
willDeployConfiguration=str(sys.argv[3])
willDeployLib=str(sys.argv[4])
willDeployProperties=str(sys.argv[5])
willDeployExecutable=str(sys.argv[6])
willDeployStatic="true"
willDeployDynamicJars=str(sys.argv[8])

FCOLOR1="#E85F47"
FCOLOR2="#F5DDC5"
SCOLOR1="#70AD47"
SCOLOR2="#E2EFD9"

willOffline="true"
willOnline="true"
willWait="true"
willServiceStop="true"
willServiceStart="true"
willDeletExecutableStatusFiles="true"

appPath="/data/wildfly-9.0.1.Final/"+app+"/"
wildFlyVersion="wildfly-9.0.1.Final"
deployments=appPath+"deployments/"
indexPath=deployments+"asitemonitor.ear/monitor.war/"
conf=appPath+"conf/"
configuration=appPath+"configuration/"
lib=appPath+"lib/"
properties=appPath+"properties/"
DynamicJars=appPath+"DynamicJars/"
tmp=appPath+"tmp/"
log=appPath+"log/"

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

    def renameStatic():
        global f1
        sys.stdout.write ('In renameStatic method\n')
        now = datetime.now()
        print("now =", now)
        static1="/data/staticsite/"+staticFolder+"Temp1/"
        static="/data/staticsite/"+staticFolder+"/"
        print("static1 =", static1)
        print("static =", static)
        if not os.path.exists(static1):
            print("STATICTEMP1 FOLDER NOT EXISTS ", static1)
            emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>STATICTEMP1 FOLDER NOT EXISTS</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
        else:
            print("STATICTEMP1 FOLDER FOUND ", static1)

            if not os.path.exists(static):
                print("STATIC FOLDER NOT EXISTS ", static)
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>STATIC FOLDER NOT EXISTS</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
            else:
                print("STATIC FOLDER FOUND ", static)
                try:
                    static2="/data/staticsite/"+staticFolder+"Temp2/"
                    p=subprocess.run(["sudo","mv",static,static2], stderr=subprocess.PIPE, universal_newlines=True)
                    if p.returncode == 0:
                        emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>adoddlesite renamed to adoddlesiteTemp2 </td><td width=50%>&#9989;</td></font></tr>".format(SCOLOR2)
                        print("adoddlesite renamed to adoddlesiteTemp2")
                        try:
                            p=subprocess.run(["sudo","mv",static1,static], stderr=subprocess.PIPE, universal_newlines=True)
                            if p.returncode == 0:
                                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>adoddlesiteTemp1 renamed to adoddlesite </td><td width=50%>&#9989;</td></font></tr>".format(SCOLOR2)
                                print("adoddlesiteTemp1 renamed to adoddlesite")
                                try:
                                    p=subprocess.run(["sudo","mv",static2,static1], stderr=subprocess.PIPE, universal_newlines=True)
                                    if p.returncode == 0:
                                        emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>adoddlesiteTemp2 renamed to adoddlesiteTemp1 </td><td width=50%>&#9989;</td></font></tr>".format(SCOLOR2)
                                        print("adoddlesiteTemp2 renamed to adoddlesiteTemp1")
                                    else:
                                        emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROBLEM OCCURED WHILE RENAMING adoddlesiteTemp2 to adoddlesiteTemp1 </td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
                                        f1="true"
                                        print("Problem occured while renaming adoddlesiteTemp2 to adoddlesiteTemp1", p.stderr)
                                except OSError as e:
                                    emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROBLEM OCCURED WHILE 2 RENAMING adoddlesiteTemp2 to adoddlesiteTemp1</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
                                    print("Problem occured while 2 renaming adoddlesiteTemp2 to adoddlesiteTemp1", p.stderr)
                                    f1="true"
                                    print(sys.stderr, "Execution failed:", e)
                            else:
                                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROBLEM OCCURED WHILE RENAMING adoddlesiteTemp1 to adoddlesite</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
                                f1="true"
                                print("Problem occured while renaming adoddlesiteTemp1 to adoddlesite", p.stderr)
                        except OSError as e:
                            emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROBLEM OCCURED WHILE 2 RENAMING adoddlesiteTemp1 to adoddlesite</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
                            print("Problem occured while 2 renaming adoddlesiteTemp1 to adoddlesite", p.stderr)
                            f1="true"
                            print(sys.stderr, "Execution failed:", e)
                    else:
                        emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROBLEM OCCURED WHILE RENAMING adoddlesite to adoddlesiteTemp2</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
                        f1="true"
                        print("Problem occured while renaming adoddlesite to adoddlesiteTemp2", p.stderr)
                except OSError as e:
                    emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROBLEM OCCURED WHILE 2 RENAMING adoddlesite to adoddlesiteTemp2</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
                    print("Problem occured while 2 renaming adoddlesite to adoddlesiteTemp2", p.stderr)
                    f1="true"
                    print(sys.stderr, "Execution failed:", e)
        sys.stdout.write ('Exit from renameStatic method\n')
        now = datetime.now()
        print("now =", now)        
        return emailBody1        
    
    def main():
        global f1
        emailBody1=emailBody

        if ((willDeployStatic=="true") and (f1 != "true")):
            emailBody1=emailBody1+renameStatic()
            
        if f1 != "true":
            emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>DEPLOYMENT STATUS</td><td width=50%>SUCCESSFUL<BR> &#9989;</td></font></tr></table></body></html><br><br>".format(SCOLOR2)
        else:
            emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>DEPLOYMENT STATUS</td><td width=50%>FAILED<BR>&#10060;</td></font></tr></table></body></html><br><br>".format(FCOLOR2)
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

def notificationEmail(message):
    sys.stdout.write("in NotificationEmail method\n")
    smtpObj = smtplib.SMTP(smtpserver1)
    smtpObj.sendmail(sender, receivers, message)
    sys.stdout.write("exit from NotificationEmail method\n")

sender = 'serena@asite.com'
receivers1=str(sys.argv[20])
receivers = list(receivers1.split(","))
smtpserver1=str(sys.argv[21])

message = """From: {}
To: {}
Subject: {}
MIME-Version: 1.0
Content-type: text/html

{}
""".format(sender,",".join(receivers),emailSubject,emailBody)
notificationEmail(message)