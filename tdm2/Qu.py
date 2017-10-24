import os

try:
    os.system("rm tdm.log")
except IOError:
    print("Could not find file")

print("Running script Qu.py")
os.system("python tdm.py")
print(50*'*')
print("Finished")
A = raw_input("\nPress return to continue\n")
os.system("vim tdm.log")
