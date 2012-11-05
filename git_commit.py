import os
#clean all the pyc
os.system("find . -name \"*.pyc\" -exec rm -f {} \;")
os.system("find . -name \"*.swp\" -exec rm -f {} \;")
os.system("find . -name \"*.pyc\" -exec git rm -f {} \;")
os.system("find . -name \"*.swp\" -exec git rm -f {} \;")
print "All the *.pyc files are cleaned"
#get the commit message
message=raw_input("Say something for the input:::\n")
#add all
os.system("git add -f .;")
#git commit
os.system("git commit -m \""+message+"\";")
