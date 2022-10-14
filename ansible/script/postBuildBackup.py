# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 11:00:55 2022

@author: kparekh
"""
import subprocess
import sys
from datetime import datetime

server=str(sys.argv[1])
server1=(server.upper())
app=str(sys.argv[2])
app1=(app.upper())
env=str(sys.argv[3])
dc=str(sys.argv[4])
prvfle=str(sys.argv[5])
rtdBackupPath=str(sys.argv[6])
folderOnLinux=str(sys.argv[7])
rtdBackupBase=rtdBackupPath.rsplit("/", 2)[0]

FCOLOR1="#E85F47"
FCOLOR2="#F5DDC5"
SCOLOR1="#70AD47"
SCOLOR2="#E2EFD9"

emailBody="<html><body><table style='border:1px solid' align='center' bgcolor='{}' style='width:50%'><tr><font size='3' color='white' face='calibri'><th colspan='2' align='center'>{}<BR>{}<BR>{}</th></font></tr>".format(SCOLOR1,app1,env,server1)
f1=None
now = datetime.now()
print("now =", now)

def postBuildBackupFodlerCreate():
    """
    Post Build Backup Folder Stucture Creation Function
    """
    global f1
    sys.stdout.write ('In postBuildBackupFodlerCreate method\n')
    now = datetime.now()
    print("rtd backup path= ", rtdBackupPath)
    print("now =", now)

    try:
        p=subprocess.run(["find","./","-type","d","-exec","mkdir","-p",rtdBackupPath+"/{}",";"], stderr=subprocess.PIPE, universal_newlines=True, cwd=folderOnLinux)
        if p.returncode == 0:
            emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>RTD BACKUP FOLDER CREATION</td><td width=50%>&#9989;</td></font></tr>".format(SCOLOR2)
            print("RTD BACKUP FOLDER CREATED")
        else:
            f1="true"
            emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>RTD BACKUP FOLDER CREATION PROBLEM</td><td width=50%>&#9888;</td></font></tr>".format(FCOLOR2)
            print("RTD BACKUP FOLDER CREATION PROBLEM", p.stderr)
    except OSError as e:
        emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROBLEM OCCURED WHILE CREATING RTD BACKUP FOLDER</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
        print("RTD BACKUP FOLDER CREATION PROBLEM", p.stderr)
        f1="true"
        print(sys.stderr, "Execution failed:", e)
    return emailBody1
    sys.stdout.write ('Exit from postBuildBackupFodlerCreate method\n')

def postBuildBackup():
    """
    Post Build Backup
    """
    global f1
    sys.stdout.write ('In postBuildBackup method\n')
    now = datetime.now()
    print("now =", now)
    print("rtd backup path= ", rtdBackupPath)
    try:
        p=subprocess.run(["find","./","-type","f","-exec","mv","-f","{}",rtdBackupPath+"/{}",";"], stderr=subprocess.PIPE, universal_newlines=True, cwd=folderOnLinux)
        if p.returncode == 0:
            emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>RTD BACKUP </td><td width=50%>&#9989;</td></font></tr>".format(SCOLOR2)
            print("RTD FILES COPIED")
        else:
            f1="true"
            emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>RTD BACKUP COPY PROBLEM</td><td width=50%>&#9888;</td></font></tr>".format(FCOLOR2)
            print("RTD FILES COPY PROBLEM", p.stderr)
    except OSError as e:
        emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROBLEM OCCURED WHILE COPYING RTD FOLDER</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
        print("RTD FILES COPY PROBLEM", p.stderr)
        f1="true"
        print(sys.stderr, "Execution failed:", e)
    return emailBody1
    sys.stdout.write ('Exit from postBuildBackup method\n')

def deleteOldBackup():
    """
    Delete Old Backups
    """
    global f1
    sys.stdout.write ('In deleteOldBackup method\n')
    now = datetime.now()
    print("now =", now)
    print("rtd backup path= ", rtdBackupPath)
    print("rtd base backup path= ", rtdBackupBase)
    try:
        p=subprocess.run(["find",rtdBackupBase,"-maxdepth","1","-mtime","+8","-exec","sudo","rm","-rf","{}","&&","echo","{} Deleted",";"], stderr=subprocess.PIPE, universal_newlines=True)
        if p.returncode == 0:
            emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>OLD BACKUP DELETE </td><td width=50%>&#9989;</td></font></tr>".format(SCOLOR2)
            print("OLD BACKUP DELETED")
        else:
            f1="true"
            emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROBLEM OCCURED WHILE DELETING OLD BACKUP</td><td width=50%>&#9888;</td></font></tr>".format(FCOLOR2)
            print("OLD BACKUP DELETED PROBLEM", p.stderr)
    except OSError as e:
        emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROBLEM OCCURED WHILE DELETING OLD BACKUP</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
        print("OLD BACKUP DELETED PROBLEM", p.stderr)
        f1="true"
        print(sys.stderr, "Execution failed:", e)
    return emailBody1
    sys.stdout.write ('Exit from deleteOldBackup method\n')


def main():
    global f1
    emailBody1=emailBody+postBuildBackupFodlerCreate()
    emailBody1=emailBody1+postBuildBackup()
    emailBody1=emailBody1+deleteOldBackup()
    return emailBody1

emailBody=main()
if f1 != "true":
    emailSubject="{}-{}-{} PROCESS SUCCESSFUL".format(app1,env,dc)
else:
    emailSubject="{}-{}-{} PROCESS FAILED".format(app1,env,dc)

sys.stdout.write("Email Subject ")
sys.stdout.write(emailSubject)
sys.stdout.write("For Email ")
sys.stdout.write(emailBody)