#!/usr/bin/python3
import os
import subprocess
import functools
""""
def JohnTR(LC,UC,NUM,SC,minlen,maxlen,filetype):
    
    if not SC=='n':
        imode = "ASCII"
    elif UC+LC+NUM=='nny':
        imode = "Digits"
    elif UC+LC+NUM=='yyy':
        imode = "Alnum"
    elif UC+LC+NUM=='yyn':
        imode = "Alpha"
    elif UC+LC+NUM=='ynn':
        imode = "Upper"
    elif UC+LC+NUM=='nyn':
        imode = "Lower"
    elif UC+LC+NUM=='nyy':
        imode = "LowerNum"
    elif UC+LC+NUM=='yny':
        imode = "UpperNum"
    else:
        imode = "ASCII"

    os.system("john --format="+filetype+" --single -min-len="+minlen+" -max-len="+maxlen+" /tmp/PassHash.txt > /home/jfrans/Desktop/Password.txt")
    os.system("john --format="+filetype+" --show /tmp/PassHash.txt > /home/jfrans/Desktop/Password.txt")
    with open("/home/jfrans/Desktop/Password.txt",'r') as result:
        if "0 left" not in functools.reduce(lambda a,b : a+b, [c for c in result.readlines()]):
            result.seek(0)
            if imode == "Digits":
                #os.system("john --format="+filetype+" --wordlist=/usr/share/john/NumericList.txt /tmp/PassHash.txt > ~/Desktop/Password.txt")
                os.system("john --format="+filetype+" --show /tmp/PassHash.txt > /home/jfrans/Desktop/Password.txt")
                if "0 left" not in functools.reduce(lambda a,b : a+b, [c for c in result.readlines()]):
                    os.system("john --format="+filetype+" --incremental="+imode+" -min-len="+minlen+" -max-len="+maxlen+" /tmp/PassHash.txt > /home/jfrans/Desktop/Password.txt")
                    os.system("john --format="+filetype+" --show /tmp/PassHash.txt > /home/jfrans/Desktop/Password.txt")
            else:
                os.system("john --format="+filetype+" --wordlist=CustomPasswordList.txt -min-len="+minlen+" -max-len="+maxlen+" /tmp/PassHash.txt > /home/jfrans/Desktop/Password.txt")
                os.system("john --format="+filetype+" --show /tmp/PassHash.txt > /home/jfrans/Desktop/Password.txt")
                if "0 left" not in functools.reduce(lambda a,b : a+b, [c for c in result.readlines()]):
                    input("Wordlist Failed! Performing Brute Force")
                    os.system("john --format="+filetype+" --incremental="+imode+" -min-len="+minlen+" -max-len="+maxlen+" /tmp/PassHash.txt > /home/jfrans/Desktop/Password.txt")
                    os.system("john --format="+filetype+" --show /tmp/PassHash.txt > /home/jfrans/Desktop/Password.txt")
"""
def JohnTR(LC,UC,NUM,SC,minlen,maxlen,filetype,jhash,dictionary=False):

    if filetype in "docx pptx xlsx":
        filetype = "office"
    #os.system("echo "+jhash.stdout.replace("$","\$")+" 1> /tmp/PassHash.txt")
    if not SC=='n':
        imode = "ASCII"
    elif UC+LC+NUM=='nny':
        imode = "Digits"
    elif UC+LC+NUM=='yyy':
        imode = "Alnum"
    elif UC+LC+NUM=='yyn':
        imode = "Alpha"
    elif UC+LC+NUM=='ynn':
        imode = "Upper"
    elif UC+LC+NUM=='nyn':
        imode = "Lower"
    elif UC+LC+NUM=='nyy':
        imode = "LowerNum"
    elif UC+LC+NUM=='yny':
        imode = "UpperNum"
    else:
        imode = "ASCII"

    if dictionary:
        os.system("john --format="+filetype+" --wordlist=password.lst -min-len="+minlen+" -max-len="+maxlen+" "+jhash+" > /tmp/ShrLck_Password.txt")

    os.system("john --format="+filetype+" --incremental="+imode+" -min-len="+minlen+" -max-len="+maxlen+" "+jhash+" > /tmp/ShrLck_Password.txt")
    os.system("john --format="+filetype+" --show "+jhash+" > /tmp/ShrLck_Password.txt")


def HashCat(LC,UC,NUM,SC,minlen,maxlen,jhash):
    charset = ''
    if not LC.lower() == 'n':
        charset += '?l'
    if not UC.lower() == 'n':
        charset += '?u'
    if not NUM.lower() == 'n':
        charset += '?d'
    if not SC.lower() == 'n':
        charset += '?s'

    with open("/home/jfrans/Desktop/Password.txt",'w+') as result:
        txt = jhash.stdout
        hsh = txt[txt.find('$'):].strip()
        syscmd = subprocess.run(["hashid","-m",hsh],stdout=subprocess.PIPE,text=True)
        m = syscmd.stdout.strip()
        m = m[m.rfind(":")+2:-1]
        hsh = hsh.replace('$','\$')
        if charset == '?d':
            os.system("hashcat -a 3 -m "+m+" -w 3 -i --increment-min "+minlen+" -o /home/jfrans/Desktop/Password.txt "+hsh+" "+(charset*int(maxlen)))

            os.system("hashcat -m "+m+" --show "+hsh+" > /home/jfrans/Desktop/Password.txt")
        else:
            os.system("hashcat -a 0 -m "+m+" -w 3 -o /home/jfrans/Desktop/Password.txt "+hsh+" /home/jfrans/Hackathon/Forensics/CustomPasswordList.txt")
            os.system("hashcat -m "+m+" --show "+hsh+" > /home/jfrans/Desktop/Password.txt")
            #if input("Wordlist Failed. Would you like to try Brute Force? (y/N): ").lower()=='y':
                #os.system("hashcat -a 3 -m "+m+" -1 "+charset+" -w 3 -i --increment-min "+minlen+" -o ~/Desktop/Password.txt "+hsh+" "+('?1'*int(maxlen)))

def GetHash(path,filetype):
    if filetype in "docx pptx xlsx":
        filetype = "office"
    os.system(filetype+"2john "+path+" > /tmp/PassHash.txt")
    syscmd = subprocess.run([filetype+"2john",path],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    return syscmd

def isEncrypted(path,filetype):
    temp = ""
    if filetype in "txt csv":
        return False
    if filetype in "docx pptx xlsx":
        filetype = "office"
    cmd = GetHash(path,filetype)
    if "not encrypted" in cmd.stdout or "unencrypted" in cmd.stderr:
            return False
    return True

def CrackNTLM(LC,UC,NUM,SC,minlen,maxlen,hsh,gpu,dictionary=False):
    if gpu == "n":
        JohnTR(LC,UC,NUM,SC,minlen,maxlen,"NT",hsh,dictionary)
        return

    charset = ''
    if not LC.lower() == 'n':
        charset += '?l'
    if not UC.lower() == 'n':
        charset += '?u'
    if not NUM.lower() == 'n':
        charset += '?d'
    if not SC.lower() == 'n':
        charset += '?s'

    if dictionary:
        os.system("hashcat -a 0 -m 1000 -w 3 -o /tmp/ShrLck_Password.txt "+hsh+" password.lst")

    if charset == '?d':
        os.system("hashcat -a 3 -m 1000 -w 3 -i --increment-min "+minlen+" -o /tmp/ShrLck_Password.txt "+hsh+" "+(charset*int(maxlen)))
        os.system("hashcat -m 1000 --show "+hsh+" > /tmp/ShrLck_Password.txt")
    else:
        os.system("hashcat -m 1000 --show "+hsh+" > /tmp/ShrLck_Password.txt")
    #if input("Wordlist Failed. Would you like to try Brute Force? (y/N): ").lower()=='y':
        os.system("hashcat -a 3 -m 1000 -1 "+charset+" -w 3 -i --increment-min "+minlen+" -o /tmp/ShrLck_Password.txt "+hsh+" "+('?1'*int(maxlen)))
        os.system("hashcat -m 1000 --show "+hsh+" > /tmp/ShrLck_Password.txt")

syscmd = subprocess.run(["whoami"],stdout=subprocess.PIPE,text=True)
#user = syscmd.stdout.strip()
user = "jfrans"
""""
while(True):
    syscmd = subprocess.run(["whoami"],stdout=subprocess.PIPE,text=True)
    user = syscmd.stdout.strip()
    file = input("Enter name of File:")
    syscmd = subprocess.run(["find","/home/jfrans/","-name",file],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    path = syscmd.stdout.strip()
    if not os.path.exists(path):
        print("File not found")
        exit()
    filetype = file[file.rfind('.')+1:]
    print(isEncrypted(path,filetype))

gpu = input("Use GPU? (y/N): ")
LC = input("Use Lower Case? (Y/n): ")
UC = input("Use Upper Case? (Y/n): ")
NUM = input("Use Numbers? (Y/n): ")
SC = input("Use Special Characters? (Y/n): ")
minlen = input("Minimum Password Length: ")
maxlen = input("Maximum Password Length: ")

GetHash(path,filetype)
if gpu.lower() == 'y':
    HashCat(LC,UC,NUM,SC,minlen,maxlen)
else:
    JohnTR(LC,UC,NUM,SC,minlen,maxlen)
"""
