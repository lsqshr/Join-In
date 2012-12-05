import os
from optparse import OptionParser
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

parser = OptionParser()
#get the port number for the database server
parser.add_option("-p", "--push", dest="remote",
                  help="push this commit and previous ones to remoting server",
                  metavar="PUSH",type="string",default="github")
parser.add_option("-b", "--branch", dest="branch",
                  help="push this branch to remoting server",
                  metavar="PUSH",type="string",default="master")

(options,args) = parser.parse_args()

if len(args)!=0:
	os.system("git push"+options.branch+options.remote)