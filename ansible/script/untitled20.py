import subprocess
import sys

app="adoddle/"

def killByPID():
    sys.stdout.write('In killByPID method\n')
    command="ps aux | grep service_"+app+" | awk -F ' ' '{print $2}'"
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
        if ((arg != "") and (len(arg) < 1)):
            command="ps -Flww -p "+arg
            process=subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
            proc_stdout=process.communicate()[0].strip()
            print(proc_stdout)
        
#            command="sudo kill "+arg
#            process=subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
#            proc_stdout=process.communicate()[0].strip()
#            print(proc_stdout)
    sys.stdout.write ('Exit from killByPID method\n')
    
killByPID()