import os
import subprocess
from PassCrack import isEncrypted
def Scan(devl):
    l = []
    os.system("sudo mount -L"+devl+" /home/jfrans/Mount")
    os.system("sudo find /home/jfrans/Mount/ -name \"*.pdf\" >> /tmp/FPaths.txt")
    with open("/tmp/FPaths.txt","r") as file:
        for i in file:
            l.append(i.strip())
    os.system("rm /tmp/FPaths.txt")
    os.system("sudo find /home/jfrans/Mount/ -name \"*.docx\" >> /tmp/FPaths.txt")
    with open("/tmp/FPaths.txt","r") as file:
        for i in file:
            l.append(i.strip())
    os.system("rm /tmp/FPaths.txt")
    os.system("sudo find /home/jfrans/Mount/ -name \"*.xlsx\" >> /tmp/FPaths.txt")
    with open("/tmp/FPaths.txt","r") as file:
        for i in file:
            l.append(i.strip())
    os.system("rm /tmp/FPaths.txt")
    os.system("sudo find /home/jfrans/Mount/ -name \"*.txt\" >> /tmp/FPaths.txt")
    with open("/tmp/FPaths.txt","r") as file:
        for i in file:
            l.append(i.strip())
    os.system("rm /tmp/FPaths.txt")
    os.system("sudo find /home/jfrans/Mount/ -name \"*.pptx\" >> /tmp/FPaths.txt")
    with open("/tmp/FPaths.txt","r") as file:
        for i in file:
            l.append(i.strip())
    os.system("rm /tmp/FPaths.txt")
    os.system("sudo find /home/jfrans/Mount/ -name \"*.csv\" >> /tmp/FPaths.txt")
    with open("/tmp/FPaths.txt","r") as file:
        for i in file:
            l.append(i.strip())
    os.system("rm /tmp/FPaths.txt")
    #os.system("sudo umount "+path)
    return l

def FindDevices():
        syscmd = subprocess.run(["sudo","lsblk","-o","NAME,LABEL"],stdout=subprocess.PIPE,text=True)
        ls = [x[x.rfind(" ")+1:] for x in syscmd.stdout.split("\n") if len(x.strip().split(" "))>1]
        ls.pop(0)
        return ls

def FindEncryptedFiles(x):  #Pass Scan(devlabel) if you don't have a list already'
    encrlist = []
    for i in x:
        if isEncrypted(i,i.strip()[i.strip().rfind('.')+1:]):
            encrlist.append(i)
    return encrlist

def ScanSAM():
	Lsblk = subprocess.run(["lsblk","-o","FSTYPE,MOUNTPOINT,PATH"],stdout=subprocess.PIPE,text=True)
	for i in Lsblk.stdout.split("\n"):
        #print(i)
		if 'ntfs' in i.split():
			Path = i.split()[1]
			Path1 = Path
			if "/dev/" in Path:
				if not os.path.exists("/tmp/tmpmount"):
					os.mkdir("/tmp/tmpmount")
				Path1 = Path
				os.system("sudo mount "+Path+" /tmp/tmpmount")
			if os.path.exists("/tmp/tmpmount/Windows/System32/config/SAM"):
				print("I AM HERE")
				os.system("sudo cp /tmp/tmpmount/Windows/System32/config/SAM .")
				os.system("sudo cp /tmp/tmpmount/Windows/System32/config/SYSTEM .")
			print("Progress")
			os.system("sudo umount "+Path1)

ScanSAM()
#p = "/dev/nvme1n1p4"
#print(Scan("PureArch"))
#x = Scan("PureArch")
#encrlist = []
#for i in x:
#   if isEncrypted(i,i.strip()[i.strip().rfind('.')+1:]):
#        encrlist.append(i)
#print(encrlist)
#print(FindDevices())
