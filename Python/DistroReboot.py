#!/usr/bin/env python
# DistroReboot.py
"""
This function unzips the newest version of CoCoDist zip file that is in the current folder. 
It can store specific files by adding file names as arguments following calling the function
    python DistroReboot file1.xml file2.xml file3.py ... filen.http 
It then moves the current CoCoDist_Linux folder into the OlderDistos folder and assigns a new number
which is the current highest number in the folder + 1. 
Next it unzips the highest value of CoCoDist_Linux_v{}.tar.gz . If there were any folders specifically
added it will then move the files from the temporary holding folder "StoredXML" into the new distribution

Author : David Orn
         david@iiim.is

"""

import os, numpy as np, sys



def comm(inpArg):
    print "Running command {}".format(inpArg)
    os.system()

def makeSimilarFileStructure():
    folder_prefix = "OlderDistros/CoCoDist_Linux_old"
    os.system("rm -r OlderDistros/*")

    for fileno in range(1,8,1):
        folderName = folder_prefix+str(fileno)
        os.system("mkdir "+ folderName)

    os.system("mkdir CoCoDist_Linux")
    os.system("touch CoCoDist_Linux/t1.xml CoCoDist_Linux/t2.xml")

def saveFiles(args):
    # Move currently used files into a storing folder.
    for files in args:
        os.system("cp CoCoDist_Linux/" + files + " StoredXML/")

def move_back(args):
    # Move currently used files into a storing folder.
    for files in args:
        os.system("cp StoredXML/"+files+" CoCoDist_Linux/")

#:makeSimilarFileStructure()
# Move files to old directory
old = "OlderDistros/" # Testing
folder_name = old+"CoCoDist_Linux_old"


num = [] 
#old = "OlderDistors"
for files in os.listdir(old):
    num.append(int(files.split("old")[1]))

max_num = np.amax(num)
next_num = max_num+1
next_folder = folder_name + str(next_num)
        
print "Will move current distro to {}".format(next_folder)
# Make new directory
os.system("mkdir "+ next_folder)

# Saving input files, if any
if len(sys.argv) > 1:
    saveFiles(sys.argv[1:])

# Move current files into directory
print("Moving files to older distribution")
os.system("mv CoCoDist_Linux "+next_folder)

# Find the newest distro
distro_zip_name = "CoCoDist_Linux_v"
file_name = []
for files in os.listdir("."):
    if distro_zip_name in files:
        file_name.append(files)
file_name.sort(reverse=True)
print "Will tar and unzip {}".format(file_name[0])
os.system("tar -xzvf "+ file_name[0])

if len(sys.argv) > 1:
    print "Moving files into new directory"
    move_back(sys.argv[1:])


print "Finished running script successfully"

