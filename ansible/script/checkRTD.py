# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 20:00:28 2020

@author: parthjadav
"""

import os
import sys
import smtplib
from datetime import datetime

server=str(sys.argv[9])
server1=(server.upper())
app=str(sys.argv[10])
app1=(app.upper())
env=str(sys.argv[11])
dc=str(sys.argv[12])
staticFolder=str(sys.argv[13])
rtdFolder=str(sys.argv[14])
rtdPath=str(sys.argv[15])
rtdPathFolder=str(sys.argv[16])
appType=str(sys.argv[17])

willRestart=str(sys.argv[1])
willDeployConf=str(sys.argv[2])
willDeployConfiguration=str(sys.argv[3])
willDeployLib=str(sys.argv[4])
willDeployProperties=str(sys.argv[5])
willDeployExecutable=str(sys.argv[6])
willDeployStatic=str(sys.argv[7])
willDeployDynamicJars=str(sys.argv[8])

FCOLOR1="#E85F47"
FCOLOR2="#F5DDC5"
isEmaiBodyUsed=None
willEmail=None

print(FCOLOR1)
print(app1)
print(env)
emailSubject=""
emailBody1=""

emailBody="<html><body><table style='border:1px solid' align='center' bgcolor='{}' style='width:50%'><tr><font size='3' color='white' face='calibri'><th colspan='2' align='center'>{}<BR>{}<BR>{}</th></font></tr>".format(FCOLOR1,app1,env,server1)

def notificationEmail(message):
    sys.stdout.write("in NotificationEmail method\n")
    sender = 'parthjadav@asite.com'
    receivers = ['parthjadav@asite.com']
    smtpObj = smtplib.SMTP('192.168.100.9')
    smtpObj.sendmail(sender, receivers, message)
    sys.stdout.write("exit from NotificationEmail method\n")

def checkRTD():
    sys.stdout.write('Checking RTD folder status\n')
    global emailSubject
    global emailBody1
    global isEmaiBodyUsed
    global willEmail
    onDeployExecutable=None
    onDeployConf=None
    onDeployConfiguration=None
    onDeployLib=None
    onDeployDynamicJars=None
    onDeployProperties=None
    onDeployStatic=None

    if ((willDeployConf == "true") or (willDeployConfiguration == "true") or (willDeployLib == "true") or (willDeployProperties == "true") or (willDeployExecutable == "true") or (willDeployStatic == "true") or (willDeployDynamicJars == "true")):
        now = datetime.now()
        print("now =", now)
        src=rtdPathFolder+rtdFolder+"/deployments/"
        if willDeployExecutable == "true":
            if sum([len(files) for r, d, files in os.walk(src)]) < 1:
                print("EAR/WAR NOT FOUND IN READYDEPLOY FOLDER")
                print(src)
                onDeployExecutable="false"
                emailBody1=emailBody+"<tr align='center' bgcolor={}><font size='3' color='black' face='calibri'><td width=50%>EAR/WAR NOT FOUND IN READYDEPLOY FOLDER</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
                isEmaiBodyUsed="true"
        now = datetime.now()
        print("now =", now)
        src=rtdPathFolder+rtdFolder+"conf/"+server+"/"
        if((rtdFolder=="PWS/") or (rtdFolder=="viewer/")):
            src=rtdPathFolder+rtdFolder+"conf/"+app+"/"+server+"/"
        if willDeployConf == "true":
            if sum([len(files) for r, d, files in os.walk(src)]) < 1:
                print("CONF FOLDER IS EMPTY")
                print(src)                
                onDeployConf="false"
                if isEmaiBodyUsed != "true":
                    emailBody1=emailBody+"<tr align='center' bgcolor={}><font size='3' color='black' face='calibri'><td width=50%>CONF FOLDER IS EMPTY</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
                    isEmaiBodyUsed="true"
                else:
                    emailBody1=emailBody1+"<tr align='center' bgcolor={}><font size='3' color='black' face='calibri'><td width=50%>CONF FOLDER IS EMPTY</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
    
        now = datetime.now()
        print("now =", now)
        src=rtdPathFolder+rtdFolder+"configuration/"+server+"/"
        if((rtdFolder=="PWS/") or (rtdFolder=="viewer/")):
            src=rtdPathFolder+rtdFolder+"/configuration/"+app+"/"+server+"/"
        if willDeployConfiguration == "true":
            if sum([len(files) for r, d, files in os.walk(src)]) < 1:
                print("CONFIGURATION FOLDER IS EMPTY")
                print(src)                
                onDeployConfiguration="false"
                if isEmaiBodyUsed != "true":
                    emailBody1=emailBody+"<tr align='center' bgcolor={}><font size='3' color='black' face='calibri'><td width=50%>CONFIGURATION FOLDER IS EMPTY</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
                    isEmaiBodyUsed="true"
                else:
                    emailBody1=emailBody1+"<tr align='center' bgcolor={}><font size='3' color='black' face='calibri'><td width=50%>CONFIGURATION FOLDER IS EMPTY</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
    
        now = datetime.now()
        print("now =", now)
        src=rtdPathFolder+rtdFolder+"/lib/"
        if willDeployLib == "true":
            if sum([len(files) for r, d, files in os.walk(src)]) < 1:
                print("LIB DIR IS EMPTY")
                print(src)                
                onDeployLib="false"
                if isEmaiBodyUsed != "true":
                    emailBody1=emailBody+"<tr align='center' bgcolor={}><font size='3' color='black' face='calibri'><td width=50%>LIB DIR IS EMPTY</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
                    isEmaiBodyUsed="true"
                else:
                    emailBody1=emailBody1+"<tr align='center' bgcolor={}><font size='3' color='black' face='calibri'><td width=50%>LIB DIR IS EMPTY</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
    
        now = datetime.now()
        print("now =", now)
        src=rtdPathFolder+rtdFolder+"/DynamicJars/"
        if willDeployDynamicJars == "true":
            if sum([len(files) for r, d, files in os.walk(src)]) < 1:
                print("DynamicJars FOLDER IS EMPTY")
                print(src)                
                onDeployDynamicJars="false"
                if isEmaiBodyUsed != "true":
                    emailBody1=emailBody+"<tr align='center' bgcolor={}><font size='3' color='black' face='calibri'><td width=50%>DynamicJars FOLDER IS EMPTY</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
                    isEmaiBodyUsed="true"
                else:
                    emailBody1=emailBody1+"<tr align='center' bgcolor={}><font size='3' color='black' face='calibri'><td width=50%>DynamicJars FOLDER IS EMPTY</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
        
        now = datetime.now()
        print("now =", now)
        src=rtdPathFolder+rtdFolder+"properties/"+server+"/"
        if((rtdFolder=="PWS/") or (rtdFolder=="viewer/")):
            src=rtdPathFolder+rtdFolder+"properties/"+app+"/"+server+"/"
            print("in if")
        if willDeployProperties == "true":
            if sum([len(files) for r, d, files in os.walk(src)]) < 1:
                print("PROPERTIES FOLDER IS EMPTY")
                print(src)                
                onDeployProperties="false"
                if isEmaiBodyUsed != "true":
                    print("in prop if")
                    emailBody1=emailBody+"<tr align='center' bgcolor={}><font size='3' color='black' face='calibri'><td width=50%>PROPERTIES FOLDER IS EMPTY</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
                    isEmaiBodyUsed="true"
                else:
                    print("in prop else")
                    emailBody1=emailBody1+"<tr align='center' bgcolor={}><font size='3' color='black' face='calibri'><td width=50%>PROPERTIES FOLDER IS EMPTY</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
    
        now = datetime.now()
        print("now =", now)
        src=rtdPathFolder+rtdFolder+"/static/"+staticFolder+"/"
        if willDeployStatic == "true":
            if sum([len(files) for r, d, files in os.walk(src)]) < 1:
                print("STATIC FOLDER IS EMPTY")
                print(src)                
                onDeployStatic="false"
                if isEmaiBodyUsed != "true":
                    emailBody1=emailBody+"<tr align='center' bgcolor={}><font size='3' color='black' face='calibri'><td width=50%>STATIC FOLDER IS EMPTY</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
                    isEmaiBodyUsed="true"
                else:
                    emailBody1=emailBody1+"<tr align='center' bgcolor={}><font size='3' color='black' face='calibri'><td width=50%>STATIC FOLDER IS EMPTY</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
    
        now = datetime.now()
        print("now =", now)
        
        if((onDeployExecutable != "false") and (onDeployConf != "false") and (onDeployConfiguration != "false") and (onDeployLib != "false") and (onDeployDynamicJars != "false") and (onDeployProperties != "false")  and (onDeployStatic != "false")):
            print("Go for Deployments")
        else:
            emailSubject="{}-{}-{} DEPLOYMENT PROCESS FAILED".format(app1,env,dc)
            emailBody1=emailBody1+"</table></body></html><br><br>"
            willEmail="true"
    else:
        if willRestart == "true":
            print("Go for Deployments")
        else:
            emailSubject="{}-{}-{} DEPLOYMENT PROCESS FAILED".format(app1,env,dc)
            emailBody1="Please select atleast one option"
            willEmail="true"
    sys.stdout.write('Checked RTD folder status\n')
    

checkRTD()

if willEmail == "true":
    print(emailSubject)
    print(emailBody1)
    message = """Subject: {}
    MIME-Version: 1.0
    Content-type: text/html
    {}
    """.format(emailSubject,emailBody1)
    #notificationEmail(message)