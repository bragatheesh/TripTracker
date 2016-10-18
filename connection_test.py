import sys
import telnetlib
import time
import datetime
import os

HOST = "192.168.0.10" #define the IP address for the WiFi OBD dongle

print "Current working directory: " + os.getcwd() + "\n" #debug for dir

#filename = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime()) + '.txt' #create .txt file with today's date and time of creation
#f = open(filename, 'w') #open file for writing

try:
    print "Attempting to connect to obd" #debug

    tn = telnetlib.Telnet(HOST, 35000) #connect to obd dongle at port 35000 with IP defined above using telnet

    print "Connected!" #alert user that we have succesfully connected to obd dongle

    tn.write("atz\r\n") #send reset to OBD to reinit; good practice
    time.sleep(2) #delay 2 seconds to allow successfull reset

    tn.write("atal\r\n") #what does this do again???
    time.sleep(1) #delay 1 second

    tn.write("ath1\r\n") #enable headers on diagnostic packets
    time.sleep(1)
    
    tn.write("ats1\r\n") #what does this do again???
    time.sleep(1)
    
    tn.write("atl1\r\n") #enables one data packet per line
    time.sleep(1)
    
    tn.write("atsp0\r\n") #enables automatic vehicle protocol detection
    time.sleep(1)

    
    tn.close() #close telnet connection
    #f.close()
    print "Done"

except KeyboardInterrupt: #catches CTRL-C and exits gracefully
    print "Exiting"
    tn.close()
    #f.close()
