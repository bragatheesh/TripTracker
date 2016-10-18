import sys
import telnetlib
import time
import datetime
import os

HOST = "192.168.0.10" #define the IP address for the WiFi OBD dongle

ENG_ON = 0 #engine on flag init to false (engine is off)

print "Current working directory: " + os.getcwd() + "\n" #debug for dir

filename = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime()) + '.txt' #create .txt file with today's date and time of creation
f = open(filename, 'w') #open file for writing

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

    now = time.time() #stores current time into "now"
    done = now + 10 #stores 10 seconds from "now" into "done"

    data = "00 00"
    
    while data == "00 00"
    #TODO: see what happens when RPM is polled with 1. Car OFF; 2. Key Pos 1; 3. Key Pos 2;
        tn.write("010C\r\n") #sends a request for RPM 
        data = tn.read_until("STOPPED", 2) #reads for up to 2 seconds or until the word "STOPPED" appears //need to find better way
        data = data.split("0C ", 1) #splits the resulting response by 0C, the string after 0C contains RPM data
        data = data[1] #sets data as the RPM data string
        f.write(data) #writes RPM to file followed by a newline
        f.write ("\n")
        time.sleep(1) #to prevent overflowing OBD buffer

    ENG_ON = 1
    print "CAR IS ON!" 
    
    tn.close() #close telnet connection
    f.close() #close file
    print "Done"

except KeyboardInterrupt: #catches CTRL-C and exits gracefully
    print "Exiting"
    tn.close()
    f.close()
