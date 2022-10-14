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
from pathlib import Path

server=str(sys.argv[9])
server1=(server.upper())
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
willDeployStatic=str(sys.argv[7])
willDeployDynamicJars=str(sys.argv[8])

if ((willDeployConf=="true") or (willDeployConfiguration=="true") or (willDeployLib=="true") or (willDeployProperties=="true") or (willDeployExecutable=="true")):
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
willDeletExecutableStatusFiles="true"

appPath="/data/wildfly-9.0.1.Final/"+app+"/"
wildFlyVersion="wildfly-9.0.1.Final"
deployments=appPath+"deployments/"
indexPath=deployments+"asitemonitor.ear/monitor.war/"
conf=appPath+"conf/"
configuration=appPath+"configuration/"
lib=appPath+"lib/"
properties=appPath+"properties/"
static="/data/staticsite/"+staticFolder+"/"
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

if ((willDeployExecutable=="true") or (willDeployProperties=="true") or (willRestart=="true") or (willDeployStatic=="true") or (willDeployConf=="true") or (willDeployConfiguration=="true") or (willDeployLib=="true") or (willDeployDynamicJars=="true")):
    def serverOffline():
        global f1
        sys.stdout.write('In serverOffline method\n')
        now = datetime.now()
        print("now =", now)
        dest=indexPath+"/index1.jsp"
        indexCount=len(fnmatch.filter(os.listdir(indexPath), 'index*.jsp'))
        print("files found",indexCount)
        if (indexCount==1):
            indexFileName=fnmatch.filter(os.listdir(indexPath), 'index*.jsp')
            indexPath1=indexPath+indexFileName[0]
            print(indexFileName[0])
            if (indexFileName[0]=="index1.jsp") :
                sys.stdout.write("Already Offline\n")
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>ALREADY OFFLINE</td><td width=50%>&#9888;</td></font></tr>".format(SCOLOR2)
            elif (indexFileName[0]=="index.jsp"):
                sys.stdout.write("index.jsp found\n")
                os.rename(indexPath1, dest)
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>OFFLINE</td><td width=50%>&#9989;</td></font></tr>".format(SCOLOR2)
            else:
                sys.stdout.write(indexPath1+" found\n")
                os.rename(indexPath1, dest)
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>OFFLINE</td><td width=50%>&#9989;</td></font></tr>".format(SCOLOR2)
    
        elif(indexCount > 1):
            emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>MULTIPLE INDEX FOUND</td><td width=50%>&#9888;</td></font></tr>".format(SCOLOR2)
            dest1=indexPath+"/index1_old.jsp"
            x="index1.jsp"
            indexPath1=indexPath+x
            x="index.jsp"
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

    def killByPID():
        sys.stdout.write('In killByPID method\n')
        command="ps aux | grep service_"+app+"/ | awk -F ' ' '{print $2}'"
        process=subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
        proc_stdout=process.communicate()[0].strip()
        print(proc_stdout)
        proc_stdout=str(proc_stdout)
        PIDTemp= proc_stdout.split('\'')
        print(PIDTemp[1])
        PIDTemp=PIDTemp[1].split('\\n')
        print(PIDTemp)
        
        for i, arg in enumerate(PIDTemp):
            print(i)
            print(len(arg))
            if ((arg != "") and (len(arg) > 1)):
                command="ps -Flww -p "+arg
                process=subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
                proc_stdout=process.communicate()[0].strip()
                print(proc_stdout)
            
                command="sudo kill "+arg
                process=subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
                proc_stdout=process.communicate()[0].strip()
                print(proc_stdout)
        sys.stdout.write ('Exit from killByPID method\n')
        
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

        if ((app=="adoddle") or (app=="collab") or (app=="workflow")):
            maxcount=15
        else:
            maxcount=90

        print("Will wait for seconds =", maxcount)
        while count < maxcount:
            serviceStatus=queryServiceStatus()
            sys.stdout.write('serviceStop -> while loop\n')
            count1=str(count)
            if ((serviceStatus == 'inactive') or (serviceStatus == 'failed')):
                sys.stdout.write ('Count is '+count1+' and serviceStatus is '+serviceStatus+'\n')
                isServiceStopped="true"
                break
            time.sleep(2)
            count=count + 1
        
        if ((app=="adoddle") or (app=="collab") or (app=="workflow")):
            killByPID()
            isServiceStopped="true"
        sys.stdout.write ('Exit from serviceStop method\n')
        print("took time to stop service =", count)
        return isServiceStopped
    
    def copyStatic():
        global f1
        sys.stdout.write ('In copyStatic method\n')
        now = datetime.now()
        print("now =", now)
        src=rtdPath+rtdFolder+"static/"+staticFolder+"/*"
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
    def copyConf():
        global f1
        sys.stdout.write ('In copyConf method\n')
        now = datetime.now()
        print("now =", now)
        src=rtdPath+rtdFolder+"conf/"+server+"/*"
        if((rtdFolder=="PWS/") or (rtdFolder=="viewer/")):
            src=rtdPath+rtdFolder+"conf/"+app+"/"+server+"/*"
        try:
            p=subprocess.run(["scp","-i","/etc/ansible/"+prvfle+"","-r",src,conf], stderr=subprocess.PIPE, universal_newlines=True)
            if p.returncode==0:
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>CONF FILES</td><td width=50%>&#9989;</td></font></tr>".format(SCOLOR2)
                print("Conf files are copied")
            else:
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>CONF FOLDER IS EMPTY OR NOT EXISTS</td><td width=50%>&#9888;</td></font></tr>".format(SCOLOR2)
                print("Conf folder is empty or not exists", p.stderr)
        except OSError as e:
            emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROBLEM OCCURED WHILE COPYING CONF FILES</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
            print("Problem occured while copying Conf files", p.stderr)
            f1="true"
            print(sys.stderr, "Execution failed:", e)
        return emailBody1
        sys.stdout.write ('Exit from copyConf method\n')
    def copyConfiguration():
        global f1
        sys.stdout.write ('In copyConfiguration method\n')
        now = datetime.now()
        print("now =", now)
        src=rtdPath+rtdFolder+"configuration/"+server+"/*"
        if((rtdFolder=="PWS/") or (rtdFolder=="viewer/")):
            src=rtdPath+rtdFolder+"configuration/"+app+"/"+server+"/*"
        try:
            p=subprocess.run(["scp","-i","/etc/ansible/"+prvfle+"","-r",src,configuration], stderr=subprocess.PIPE, universal_newlines=True)
            if p.returncode==0:
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>CONFIGURATION FILES</td><td width=50%>&#9989;</td></font></tr>".format(SCOLOR2)
                print("configuration files are copied")
            else:
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>CONFIGURATION FOLDER IS EMPTY OR NOT EXISTS</td><td width=50%>&#9888;</td></font></tr>".format(SCOLOR2)
                print("configuration folder is empty or not exists", p.stderr)
        except OSError as e:
            emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROBLEM OCCURED WHILE COPYING CONFIGURATION FILES</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
            print("Problem occured while copying configuration files", p.stderr)
            f1="true"
            print(sys.stderr, "Execution failed:", e)
        return emailBody1        
        sys.stdout.write ('Exit from copyConfiguration method\n')    
    def copyLib():
        global f1
        sys.stdout.write ('In copyLib method\n')
        now = datetime.now()
        print("now =", now)
        src=rtdPath+rtdFolder+"lib/*"
        try:
            p=subprocess.run(["scp","-i","/etc/ansible/"+prvfle+"","-r",src,lib], stderr=subprocess.PIPE, universal_newlines=True)
            if p.returncode == 0:
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>LIB FILES</td><td width=50%>&#9989;</td></font></tr>".format(SCOLOR2)
                print("Lib files are copied")
            else:
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>LIB FOLDER IS EMPTY OR NOT EXISTS</td><td width=50%>&#9888;</td></font></tr>".format(SCOLOR2)
                print("Lib folder is empty or not exists", p.stderr)
        except OSError as e:
            emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROBLEM OCCURED WHILE COPYING LIB FILES</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
            print("Problem occured while copying lib files", p.stderr)
            f1="true"
            print(sys.stderr, "Execution failed:", e)
        return emailBody1
        sys.stdout.write ('Exit from copyLib method\n')    
    def copyDynamicJars():
        global f1
        sys.stdout.write ('In copyDynamicJars method\n')
        now = datetime.now()
        print("now =", now)
        src=rtdPath+rtdFolder+"DynamicJars/*"
        try:
            p=subprocess.run(["scp","-i","/etc/ansible/"+prvfle+"","-r",src,DynamicJars], stderr=subprocess.PIPE, universal_newlines=True)
            if p.returncode == 0:
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>DynamicJars </td><td width=50%>&#9989;</td></font></tr>".format(SCOLOR2)
                print("DynamicJars are copied")
            else:
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>DynamicJars FOLDER IS EMPTY OR NOT EXISTS</td><td width=50%>&#9888;</td></font></tr>".format(SCOLOR2)
                print("DynamicJars folder is empty or not exists", p.stderr)
        except OSError as e:
            emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROBLEM OCCURED WHILE COPYING DynamicJars</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
            print("Problem occured while copying DynamicJars", p.stderr)
            f1="true"
            print(sys.stderr, "Execution failed:", e)
        return emailBody1        
        sys.stdout.write ('Exit from copyDynamicJars method\n')    
    def copyProperties():
        global f1
        sys.stdout.write ('In copyProperties method\n')
        now = datetime.now()
        print("now =", now)
        src=rtdPath+rtdFolder+"properties/"+server+"/*"
        if((rtdFolder=="PWS/") or (rtdFolder=="viewer/")):
            src=rtdPath+rtdFolder+"properties/"+app+"/"+server+"/*"
        try:
            p=subprocess.run(["scp","-i","/etc/ansible/"+prvfle+"","-r",src,properties], stderr=subprocess.PIPE, universal_newlines=True)
            if p.returncode==0:
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROPERTIES FILES</td><td width=50%>&#9989;</td></font></tr>".format(SCOLOR2)
                print("properties files are copied")
            else:
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROPERTIES FOLDER IS EMPTY OR NOT EXISTS</td><td width=50%>&#9888;</td></font></tr>".format(SCOLOR2)
                print("properties folder is empty or not exists", p.stderr)
        except OSError as e:
            emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROBLEM OCCURED WHILE COPYING PROPERTIES FILES</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
            print("Problem occured while copying properties files", p.stderr)
            f1="true"
            print(sys.stderr, "Execution failed:", e)
        return emailBody1        
        sys.stdout.write ('Exit from copyProperties method\n')    
    def copyExecutable():
        global f1
        sys.stdout.write ('In copyExecutable method\n')
        now = datetime.now()
        print("now =", now)
        src=rtdPath+rtdFolder+"deployments/*"
        try:
            p=subprocess.run(["scp","-i","/etc/ansible/"+prvfle+"","-r",src,deployments], stderr=subprocess.PIPE, universal_newlines=True)
            if p.returncode == 0:
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>EAR/WAR</td><td width=50%>&#9989;</td></font></tr>".format(SCOLOR2)
                print("Ear/War is copied")
            else:
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>DEPLOYMENTS FOLDER IS EMPTY OR NOT EXISTS</td><td width=50%>&#9888;</td></font></tr>".format(SCOLOR2)
                print("deployments folder is empty or not exists", p.stderr)
        except OSError as e:
            emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROBLEM OCCURED WHILE COPYING EAR/WAR</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
            print("Problem occured while copying ear/war", p.stderr)
            f1="true"
            print(sys.stderr, "Execution failed:", e)
        return emailBody1        
        sys.stdout.write ('Exit from copyExecutable method\n')    

    def removeEarWarFiles(filesName):
        for x in filesName:
            filesName1=deployments+x
            if os.path.exists(filesName1):
                os.remove(filesName1)
                sys.stdout.write (filesName1+' is removed\n')
            else:
                sys.stdout.write (filesName1+' not found\n')    
    def deletExecutableStatusFiles():
        sys.stdout.write ('In deletExecutableStatusFiles method\n')
        now = datetime.now()
        print("now =", now)
        global earOrWar
        earOrWar=(Path(earName).suffix)
        print(earOrWar)
        if earOrWar==".war":
            print("its war deployment")
            filesName=fnmatch.filter(os.listdir(deployments), '*.war.*')
            removeEarWarFiles(filesName)
            filesName=fnmatch.filter(os.listdir(deployments), '*.ear.*')
            removeEarWarFiles(filesName)
        else:
            print("its ear deployment")
            filesName=fnmatch.filter(os.listdir(deployments), '*.ear.*')
            removeEarWarFiles(filesName)
        sys.stdout.write ('Exit from deletExecutableStatusFiles method\n')
    
    def deploymentStatus():
        sys.stdout.write ('In deploymentStatus method\n')
        now = datetime.now()
        print("now =", now)
        global status
        global f1
        global timeTaken
        f1="true"
        waitCount=0
        while True:
            sys.stdout.write('deploymentStatus -> while loop\n')
            deployed=earName+'.deployed'
            failed=earName+'.failed'
            unDeployed=earName+'.undeployed'

            if ((len(fnmatch.filter(os.listdir(deployments), failed)))==1):
                status="DEPLOYMENT FAILED"
                sys.stdout.write (failed+ 'found \n')
                break
            elif ((len(fnmatch.filter(os.listdir(deployments), unDeployed)))==1):
                status="DEPLOYMENT UNDEPLOYED"
                sys.stdout.write (unDeployed+ 'found \n')
                break
            else:
                if (((len(fnmatch.filter(os.listdir(deployments), deployed)))==1) and (os.path.exists(deployments+'asitemonitor.ear.deployed'))):
                    status="DEPLOYMENT SUCCESSFULL"
                    f1="false"
                    break
                elif (((len(fnmatch.filter(os.listdir(deployments), deployed)))==1) and (os.path.exists(deployments+'asitemonitor.ear.undeployed'))):
                    status="DEPLOYMENT SUCCESSFULL BUT asitemonitor.ear is undeployed"
                    break            
                elif (((len(fnmatch.filter(os.listdir(deployments), deployed)))==1) and (os.path.exists(deployments+'asitemonitor.ear.failed'))):
                    status="DEPLOYMENT SUCCESSFULL BUT asitemonitor.ear is failed"
                    break                    
                else:    
                    time.sleep(5)
                    if waitCount==132:
                        status="DEPLOYMENT UNDEPLOYED1"
                        sys.stdout.write ('DEPLOYMENT UNDEPLOYED1 found \n')
                        break
                    waitCount=waitCount + 1
        timeTaken=(waitCount)*5
        emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>TIME TAKEN TO DEPLOY/FAIL/UNDEPLOY</td><td width=50%>{} Seconds</td></font></tr>".format(SCOLOR2,timeTaken)
        sys.stdout.write ('Exit from deploymentStatus method\n')
        return emailBody1

    def serverOnline():
        global f1
        global proceed
        global onLine
        sys.stdout.write('In serverOnline method\n')
        now = datetime.now()
        print("now =", now)
        dest=indexPath+"/index.jsp"
        indexCount=len(fnmatch.filter(os.listdir(indexPath), '*index*.*jsp*'))
        print("files found",indexCount)
        if (indexCount==1):
            indexFileName=fnmatch.filter(os.listdir(indexPath), '*index*.*jsp*')
            indexPath1=indexPath+indexFileName[0]
            print(indexFileName[0])
            if (indexFileName[0]=="index.jsp") :
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
            indexPath1=indexPath+"index1.jsp"
            indexPath2=indexPath+"index.jsp"
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
                            if ((app=="collab") and (dc == "AUS")):
                                time.sleep(180)
                            else:
                                time.sleep(30)
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
                                        
                                    if ((willDeployConf=="true") and (f1 != "true")):
                                        emailBody1=emailBody1+copyConf()
                
                                    if ((willDeployConfiguration=="true") and (f1 != "true")):
                                        emailBody1=emailBody1+copyConfiguration()
                
                                    if ((willDeployLib=="true") and (f1 != "true")):
                                        emailBody1=emailBody1+copyLib()
                
                                    if ((willDeployDynamicJars=="true") and (f1 != "true")):
                                        emailBody1=emailBody1+copyDynamicJars()
                
                                    if ((willDeployProperties=="true") and (f1 != "true")):
                                        emailBody1=emailBody1+copyProperties()
                
                                    if ((willDeployExecutable=="true") and (f1 != "true")):
                                        emailBody1=emailBody1+copyExecutable()
                
                                    if f1 != "true":
                                        deletExecutableStatusFiles()
                
                                    if ((willServiceStart=="true") and (f1 != "true")):
                                        isServiceStarted=serviceStart()
                                        if isServiceStarted=="true":
                                            sys.stdout.write('service started successfully\n')
                                            emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>SERVICE STARTED</td><td width=50%> &#9989;</td></font></tr>".format(SCOLOR2)
                                            emailBody1=emailBody1+deploymentStatus()
                                            if status=="DEPLOYMENT SUCCESSFULL":
                                                if willOnline=="true":
                                                    emailBody1=emailBody1+serverOnline()
                                                if onLine=="true":
                                                    emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>DEPLOYMENT STATUS</td><td width=50%>SUCCESSFUL<BR> &#9989;</td></font></tr></table></body></html><br><br>".format(SCOLOR2)
                                                else:
                                                    emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>DEPLOYMENT STATUS</td><td width=50%>FAILED<BR>&#10060;</td></font></tr></table></body></html><br><br>".format(FCOLOR2)
                                                    f1="true"
                                            elif status=="DEPLOYMENT SUCCESSFULL BUT asitemonitor.ear is undeployed":
                                                emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>DEPLOYMENT STATUS</td><td width=50%>SUCCESSFUL<BR> &#9989;</td></font></tr>".format(SCOLOR2)
                                                emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>asitemonitor.ear</td><td width=50%>UNDEPLOYED<BR>&#10060;</td></font></tr></table></body></html><br><br>".format(FCOLOR2)
                                                f1="true"
                                            elif status=="DEPLOYMENT SUCCESSFULL BUT asitemonitor.ear is failed":
                                                emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>DEPLOYMENT STATUS</td><td width=50%>SUCCESSFUL<BR> &#9989;</td></font></tr>".format(SCOLOR2)
                                                emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>asitemonitor.ear</td><td width=50%>FAILED<BR>&#10060;</td></font></tr></table></body></html><br><br>".format(FCOLOR2)
                                                f1="true"
                                            elif status=="DEPLOYMENT UNDEPLOYED1":
                                                emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>TOOK MORE THAN {} SECONDS</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2,timeTaken)
                                                emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>DEPLOYMENT STATUS</td><td width=50%>UNDEPLOYED<BR>&#10060;</td></font></tr></table></body></html><br><br>".format(FCOLOR2)
                                                f1="true"
                                            elif status=="DEPLOYMENT UNDEPLOYED":
                                                emailBody1=emailBody1+"<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>DEPLOYMENT STATUS</td><td width=50%>UNDEPLOYED<BR>&#10060;</td></font></tr></table></body></html><br><br>".format(FCOLOR2)
                                                f1="true"
                                            elif status=="DEPLOYMENT FAILED":
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
                if (willDeployDynamicJars=="true"):
                    emailBody1=emailBody1+copyDynamicJars()
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
            time.sleep(120)
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