# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 12:51:02 2020

@author: parthjadav
"""

import subprocess
import sys
import os

src="centos@ldnqaweb01:/home/centos/mytest.txt"
deployments="/home/centos/"
prvfle="ldnqa.pem"

sys.stdout.write ('In copyStatic method\n')

try:
    p=subprocess.run(["scp","-i","/etc/ansible/"+prvfle+"","-r",src,deployments], stderr=subprocess.PIPE, universal_newlines=True)

    if p.returncode == 0:
        print("Static files are copied")
    else:
        print("Static folder is empty or not exists", p.stderr)
except OSError as e:
    print("Problem occured while copying static files", p.stderr)
    print(sys.stderr, "Execution failed:", e)