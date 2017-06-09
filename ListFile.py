import glob, os
os.chdir("/var/www/")
a = open("files", "w")
for file in glob.glob("*.log"):
    a.write(str(file) + os.linesep)
for file in glob.glob("*.db"):
    a.write(str(file) + os.linesep)
