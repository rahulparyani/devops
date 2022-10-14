# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 16:08:55 2021

@author: parthjadav
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 20:00:28 2020

@author: parthjadav
"""

import sys

FCOLOR1="#E85F47"
FCOLOR2="#F5DDC5"
SCOLOR1="#70AD47"
SCOLOR2="#E2EFD9"

isEmaiBodyUsed=None
willEmail="true"


server=str(sys.argv[1])
server1=(server.upper())

emailSubject=""
emailBody1=""

app1="TestApplication"
env="Sandbox"
dc="UK"

sys.stdout.write('Go for next instance\n')

emailSubject="{}-{}-{} DEPLOYMENT PROCESS SUCCESSFUL".format(app1,env,dc)
emailBody="<html><body><table style='border:1px solid' align='center' bgcolor='{}' style='width:50%'><tr><font size='3' color='white' face='calibri'><th colspan='2' align='center'>{}<BR>{}<BR>{}</th></font></tr>".format(FCOLOR1,app1,env,server1)
emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>ALREADY OFFLINE</td><td width=50%>&#9888;</td></font></tr>".format(SCOLOR2)
emailBody=emailBody+emailBody1
emailBody1="<tr align='center' bgcolor='{}'><font size='3' color='black' face='calibri'><td width=50%>STATIC FILES</td><td width=50%>&#9989;</td></font></tr></table></body></html>".format(SCOLOR2)
emailBody=emailBody+emailBody1

sys.stdout.write("Email Subject ")
sys.stdout.write(emailSubject)
sys.stdout.write("For Email ")
sys.stdout.write(emailBody)