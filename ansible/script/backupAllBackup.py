# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 23:03:59 2020

@author: parthjadav
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 14:08:47 2020

@author: parthjadav
"""
import os
import sys
import subprocess
from datetime import datetime

server=str(sys.argv[9])
server1=(server.upper())
env=str(sys.argv[10])
dc=str(sys.argv[11])
rtdPath=str(sys.argv[12])
prvfle=str(sys.argv[13])
AnsibleServer=str(sys.argv[14])

willAll=str(sys.argv[1])
willDeployConf=str(sys.argv[2])
willDeployConfiguration=str(sys.argv[3])
willDeployLib=str(sys.argv[4])
willDeployProperties=str(sys.argv[5])
willDeployExecutable=str(sys.argv[6])
willDeployStatic=str(sys.argv[7])
willDeployDynamicJars=str(sys.argv[8])

FCOLOR1="#E85F47"
FCOLOR2="#F5DDC5"
SCOLOR1="#70AD47"
SCOLOR2="#E2EFD9"

emailBody1=""
if ((willDeployExecutable=="true") or (willDeployProperties=="true") or (willAll=="true") or (willDeployStatic=="true") or (willDeployConf=="true") or (willDeployConfiguration=="true") or (willDeployLib=="true") or (willDeployDynamicJars=="true")):
    def copyStatic():
        sys.stdout.write ('In copyStatic method\n')
#        now = datetime.now()
#        print("now =", now)
#        src=rtdPathFinal+"static/"
#        print("static path is =", src)
#        print("staticOnRTD path is =", static)
#        if not os.path.exists(src):
#            os.makedirs(src)
#
#        try:
#            p=subprocess.run(["scp","-i","/etc/ansible/"+prvfle+"","-r",static,src], stderr=subprocess.PIPE, universal_newlines=True)
#            if p.returncode == 0:
#                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>STATIC FILES</td><td width=50%>&#9989;</td></font></tr>".format(SCOLOR2)
#                print("Static files are copied")
#            else:
#                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>STATIC FOLDER IS EMPTY OR NOT EXISTS</td><td width=50%>&#9888;</td></font></tr>".format(SCOLOR2)
#                print("Static folder is empty or not exists", p.stderr)
#        except OSError as e:
#            emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROBLEM OCCURED WHILE COPYING STATIC FILES</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
#            print("Problem occured while copying static files", p.stderr)
#            print(sys.stderr, "Execution failed:", e)
#        return emailBody1        
        sys.stdout.write ('Exit from copyStatic method\n')
    def copyConf():
        sys.stdout.write ('In copyConf method\n')
        now = datetime.now()
        print("now =", now)
        src=rtdPathFinal+"conf/"+server+"/"
        print("conf path is =", conf)
        print("confOnRTD path is =", src)
        if not os.path.exists(src):
            os.makedirs(src)

        try:
            p=subprocess.run(["scp","-i","/etc/ansible/"+prvfle+"","-r",conf,src], stderr=subprocess.PIPE, universal_newlines=True)
            if p.returncode==0:
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>CONF FILES</td><td width=50%>&#9989;</td></font></tr>".format(SCOLOR2)
                print("Conf files are copied")
            else:
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>CONF FOLDER IS EMPTY OR NOT EXISTS</td><td width=50%>&#9888;</td></font></tr>".format(SCOLOR2)
                print("Conf folder is empty or not exists", p.stderr)
        except OSError as e:
            emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROBLEM OCCURED WHILE COPYING CONF FILES</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
            print("Problem occured while copying Conf files", p.stderr)
            print(sys.stderr, "Execution failed:", e)
        return emailBody1
        sys.stdout.write ('Exit from copyConf method\n')
    def copyConfiguration():
        sys.stdout.write ('In copyConfiguration method\n')
        now = datetime.now()
        print("now =", now)
        src=rtdPathFinal+"configuration/"+server+"/"
        print("configuration path is =", configuration)
        print("configurationOnRTD path is =", src)
        if not os.path.exists(src):
            os.makedirs(src)
            
        try:
            p=subprocess.run(["scp","-i","/etc/ansible/"+prvfle+"","-r",configuration,src], stderr=subprocess.PIPE, universal_newlines=True)
            if p.returncode==0:
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>CONFIGURATION FILES</td><td width=50%>&#9989;</td></font></tr>".format(SCOLOR2)
                print("configuration files are copied")
            else:
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>CONFIGURATION FOLDER IS EMPTY OR NOT EXISTS</td><td width=50%>&#9888;</td></font></tr>".format(SCOLOR2)
                print("configuration folder is empty or not exists", p.stderr)
        except OSError as e:
            emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROBLEM OCCURED WHILE COPYING CONFIGURATION FILES</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
            print("Problem occured while copying configuration files", p.stderr)
            print(sys.stderr, "Execution failed:", e)
        return emailBody1        
        sys.stdout.write ('Exit from copyConfiguration method\n')    
    def copyLib():
        sys.stdout.write ('In copyLib method\n')
        now = datetime.now()
        print("now =", now)
        src=rtdPathFinal+"lib/"
        
        print("lib path is =", lib)
        print("libOnRTD path is =", src)
        if not os.path.exists(src):
            os.makedirs(src)
        
        try:
            p=subprocess.run(["scp","-i","/etc/ansible/"+prvfle+"","-r",lib,src], stderr=subprocess.PIPE, universal_newlines=True)
            if p.returncode == 0:
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>LIB FILES</td><td width=50%>&#9989;</td></font></tr>".format(SCOLOR2)
                print("Lib files are copied")
            else:
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>LIB FOLDER IS EMPTY OR NOT EXISTS</td><td width=50%>&#9888;</td></font></tr>".format(SCOLOR2)
                print("Lib folder is empty or not exists", p.stderr)
        except OSError as e:
            emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROBLEM OCCURED WHILE COPYING LIB FILES</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
            print("Problem occured while copying lib files", p.stderr)
            print(sys.stderr, "Execution failed:", e)
        return emailBody1
        sys.stdout.write ('Exit from copyLib method\n')    
    def copyDynamicJars():
        sys.stdout.write ('In copyDynamicJars method\n')
        now = datetime.now()
        print("now =", now)
        src=rtdPathFinal+"DynamicJars/"

        print("DynamicJars path is =", DynamicJars)
        print("DynamicJarsOnRTD path is =", src)
        if not os.path.exists(src):
            os.makedirs(src)

        try:
            p=subprocess.run(["scp","-i","/etc/ansible/"+prvfle+"","-r",DynamicJars,src], stderr=subprocess.PIPE, universal_newlines=True)
            if p.returncode == 0:
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>DynamicJars </td><td width=50%>&#9989;</td></font></tr>".format(SCOLOR2)
                print("DynamicJars are copied")
            else:
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>DynamicJars FOLDER IS EMPTY OR NOT EXISTS</td><td width=50%>&#9888;</td></font></tr>".format(SCOLOR2)
                print("DynamicJars folder is empty or not exists", p.stderr)
        except OSError as e:
            emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROBLEM OCCURED WHILE COPYING DynamicJars</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
            print("Problem occured while copying DynamicJars", p.stderr)
            print(sys.stderr, "Execution failed:", e)
        return emailBody1        
        sys.stdout.write ('Exit from copyDynamicJars method\n')    

    def exists_remote(host, path):
        status = subprocess.call(
            ['ssh', host, 'test -f {}'.format((path))])
        if status == 0:
            return True
        if status == 1:
            return False
        raise Exception('SSH failed')

    def copyProperties():
        global emailBody1
        sys.stdout.write ('In copyProperties method\n')
        now = datetime.now()
        print("now =", now)

        src=rtdPathFinal+"/properties/"+server+"/"
        print("properties path is =", properties)
        print("propertiesOnRTD path is =", src)

        
        if exists_remote(server,properties):
            print ("found", properties)
        else:
            print ("not found", properties)
        if os.path.exists(properties):
            if not os.path.exists(src):
                os.makedirs(src)
               
            try:
                p=subprocess.run(["sudo","scp","-i","/etc/ansible/"+prvfle+"","-r",properties,src], stderr=subprocess.PIPE, universal_newlines=True)
                if p.returncode==0:
                    emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROPERTIES FILES</td><td width=50%>&#9989;</td></font></tr>".format(SCOLOR2)
                    print("properties files are copied")
                else:
                    emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>FOLDER OF PROPERTIES IS EMPTY OR NOT EXISTS</td><td width=50%>&#9888;</td></font></tr>".format(FCOLOR2)
                    print("properties folder is empty or not exists", p.stderr)
            except OSError as e:
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROBLEM OCCURED WHILE COPYING PROPERTIES FILES</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
                print("Problem occured while copying properties files", p.stderr)
                print(sys.stderr, "Execution failed:", e)
            return emailBody1
        else:
            emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROPERTIES FOLDER IS EMPTY OR NOT EXISTS</td><td width=50%>&#9888;</td></font></tr>".format(FCOLOR2)
            print("properties folder is empty or not exists")
            return emailBody1
        sys.stdout.write ('Exit from copyProperties method\n')    
    def copyExecutable():
        sys.stdout.write ('In copyExecutable method\n')
        now = datetime.now()
        print("now =", now)
        src=rtdPathFinal+"deployments/"
        print("deployments path is =", deployments)
        print("deploymentsOnRTD path is =", src)
        if not os.path.exists(src):
            os.makedirs(src)
            
        try:
            p=subprocess.run(["scp","-i","/etc/ansible/"+prvfle+"","-r",deployments,src], stderr=subprocess.PIPE, universal_newlines=True)
            if p.returncode == 0:
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>EAR/WAR</td><td width=50%>&#9989;</td></font></tr>".format(SCOLOR2)
                print("Ear/War is copied")
            else:
                emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>DEPLOYMENTS FOLDER IS EMPTY OR NOT EXISTS</td><td width=50%>&#9888;</td></font></tr>".format(SCOLOR2)
                print("deployments folder is empty or not exists", p.stderr)
        except OSError as e:
            emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>PROBLEM OCCURED WHILE COPYING EAR/WAR</td><td width=50%>&#10060;</td></font></tr>".format(FCOLOR2)
            print("Problem occured while copying ear/war", p.stderr)
            print(sys.stderr, "Execution failed:", e)
        return emailBody1        
        sys.stdout.write ('Exit from copyExecutable method\n')    


    def wildFly():
        global emailBody1
        emailBody1=""
#        if ((willDeployConf=="true") or (willAll=="true")):
#            emailBody1=emailBody1+copyConf()
#
#        if ((willDeployConfiguration=="true") or (willAll=="true")):
#            emailBody1=emailBody1+copyConfiguration()
#
#        if ((willDeployLib=="true") or (willAll=="true")):
#            emailBody1=emailBody1+copyLib()
#
#        if ((willDeployDynamicJars=="true") or (willAll=="true")):
#            emailBody1=emailBody1+copyDynamicJars()

        if ((willDeployProperties=="true") or (willAll=="true")):
            emailBody1=emailBody1+copyProperties()

#        if ((willDeployExecutable=="true") or (willAll=="true")):
#            emailBody1=emailBody1+copyExecutable()
#
#        if ((willDeployStatic=="true") or (willAll=="true")):
#            emailBody1=emailBody1+copyStatic()
            
        return emailBody1

#    static="/data/staticsite/"
    emailBody="<html><body><table style='border:1px solid' align='center' bgcolor='{}' style='width:50%'><tr><font size='3' color='white' face='calibri'><th colspan='2' align='center'>{}<BR>{}</th></font></tr><tr></tr>".format(SCOLOR1,env,server1)    
    folder="/data/wildfly-9.0.1.Final/"
    for f in os.scandir(folder):
        if f.is_dir():
            print(f.name)
            app=f.name
            print(app)
            app1=(app.upper())
            print(app1)

            if ((app != "modules_old") and (app != "modules") and (app != "bin") and (app != "appclient") and (app != "welcome-content") and (app != "domain") and (app != "standalone") and (app != ".installation") and (app != "docs")):
                appPath="centos@"+server+":"+folder+app+"/"
                if (server == AnsibleServer):
                    appPath=folder+app+"/"
                wildFlyVersion="wildfly-9.0.1.Final"
                deployments=appPath+"deployments/"
                conf=appPath+"conf/"
                configuration=appPath+"configuration/"
                lib=appPath+"lib/"
                properties=appPath+"properties/"
                DynamicJars=appPath+"DynamicJars/"
                rtdPathFinal=rtdPath+"backupcode/"+app
    
                emailBody2="<tr><font size='3' color='white' face='calibri'><th colspan='2' align='center'>{}<BR></th></font></tr>".format(app1)
                emailBody3=wildFly()
                emailBody=emailBody+emailBody2+emailBody3

    folder="/data/asitemicroapps/"
    for f in os.scandir(folder):
        if f.is_dir():
            print(f.name)
            app=f.name
            print(app)
            app1=(app.upper())
            print(app1)

            if ((app != "modules_old") and (app != "modules") and (app != "bin") and (app != "appclient") and (app != "welcome-content") and (app != "domain") and (app != "standalone") and (app != ".installation") and (app != "docs")):
                appPath="centos@"+server+":"+folder+app+"/war/"
                if (server == AnsibleServer):
                    appPath=folder+app+"/war/"

                deployments=appPath+"deployments/"
                conf=appPath+"conf/"
                configuration=appPath+"configuration/"
                lib=appPath+"lib/"
                properties=appPath+"properties/"
                DynamicJars=appPath+"DynamicJars/"
                rtdPathFinal=rtdPath+"backupcode/"+app
    
                emailBody2="<tr><font size='3' color='white' face='calibri'><th colspan='2' align='center'>{}<BR></th></font></tr>".format(app1)
                emailBody3=wildFly()
                emailBody=emailBody+emailBody2+emailBody3
    
    emailBody=emailBody+"</table></body></html><br><br>"
    emailSubject="{}-{}-{} BACKUP PROCESS SUCCESSFUL".format(server1,env,dc)
else:
    emailSubject="{}-{}-{} BACKUP PROCESS FAILED".format(server1,env,dc)
    emailBody="Please select atleast one option"

sys.stdout.write("Email Subject ")
sys.stdout.write(emailSubject)
sys.stdout.write("For Email ")
sys.stdout.write(emailBody)