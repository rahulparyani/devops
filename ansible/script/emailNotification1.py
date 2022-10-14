# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 14:08:47 2020

@author: parthjadav
"""

import sys
import smtplib

def notificationEmail(message):
    sys.stdout.write("in NotificationEmail method\n")
    smtpObj = smtplib.SMTP(smtpserver1)
    smtpObj.sendmail(sender, receivers, message)
    sys.stdout.write("exit from NotificationEmail method\n")

sender = 'serena@asite.com'
receivers1=str(sys.argv[1])
receivers = list(receivers1.split(","))
smtpserver1=str(sys.argv[2])

emailBody = ""
for i, arg in enumerate(sys.argv):        
    if i >= 3:
        temp = {arg}
        ServerOp = """
        {}
        """.format(temp)
        
        ServerOp1 = ServerOp
        ServerOp1 = ServerOp1.split("Email Subject ")
        ServerOp1 = ServerOp1[1].split("For Email ")
        emailSubject = ServerOp1[0]
        ServerOp = ServerOp.split("For Email ")
        emailBody = emailBody+ServerOp[1]
        emailBody = emailBody.replace('\"}','')

message = """From: {}
To: {}
Subject: {}
MIME-Version: 1.0
Content-type: text/html

{}
""".format(sender,",".join(receivers),emailSubject,emailBody)
notificationEmail(message)

sys.stdout.write("Final mail is ")
sys.stdout.write(message)