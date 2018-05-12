# Script Name		: remote_user
# Author                : m47ik
# Created		: 12 May 2018
# Version		 : 1.0
# Get the list of servers by pinging the range and store in arry
#
# Modifications		: 

# Description		: This goes through the server list and pings the machine, if it's up it will load the putty session, if its not it will notify you.

import os				
import subprocess			 
from time import strftime		# Load just the strftime Module from Time

# This is the function to run if it detects the OS is windows.

def windows():																							
		f = open('server_startup_'+strftime("%Y-%m-%d")+'.log', 'a')	# Open the logfile
	for server in open('startup_list.txt','r'):														# Read the list of servers from the list
		ret = subprocess.call("ping -n 3 %s" % server, shell=True,stdout=open('NUL', 'w'),stderr=subprocess.STDOUT)	# Ping the servers in turn
		if ret == 0:             																			# If you get a response.
			f.write ("%s: is alive, loading PuTTY session" % server.strip() + "\n")		# Write out to the logfile
			subprocess.Popen(('putty -load '+server))											# Load the putty session
		else: 
			f.write ("%s : did not respond" % server.strip() + "\n")	# Write to the logfile if the server is down

def linux():
	f = open('server_startup_'+strftime("%Y-%m-%d")+'.log', 'a')	# Open the logfile
	for server in open('startup_list.txt'):															# Read the list of servers from the list
		ret = subprocess.call("ping -c 3 %s" % server, shell=True,stdout=open('/dev/null', 'w'),stderr=subprocess.STDOUT)	# Ping the servers in turn
		if ret == 0:																							# If you get a response.
			f.write ("%s: is alive" % server.strip() + "\n")										# Print a message
			subprocess.Popen(['ssh', server.strip()])
		else:             
			f.write ("%s: did not respond" % server.strip() + "\n")

# End of the functions			

# Start of the Main Program

if os.name == "posix":	                # If the OS is linux...
	linux()			# Call the linux function
elif os.name in ("nt", "dos", "ce"):	# If the OS is Windows...
	windows()		# Call the windows function
else:
	print("Not supported")
