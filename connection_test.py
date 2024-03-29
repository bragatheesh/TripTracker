import sys
import telnetlib
import time
import datetime
import os
import socket

SERVER = socket.gethostname() #this is the ip of the server, using gethostname right now for local testing
SERVER_PORT = 6000 #port the server will be listening on

HOST = "192.168.0.10" #define the IP address for the WiFi OBD dongle
PORT = 35000 #port which the wifi obd dongle is listening for telnet connections

global ENG_ON #engine on flag init to false (engine is off)
global INIT_FUEL_LEVEL #fuel level when car was turned on
global FIN_FUEL_LEVEL#fuel when car was turned off
global FUEL_NA #flag to alert if ECU does not support fuel data
global START_TIME
global STOP_TIME
global RUN_TIME

print "Current working directory: " + os.getcwd() + "\n" #debug for dir

filename = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.txt' #create .txt file with today's date and time of creation
f = open(filename, 'w') #open file for writing


def wait_car_on(): #used to wait until car is on
    rpm = "00 00" #init rpm to "00 00"
    
    while rpm == "00 00":

        tn.write("010C\r\n") #sends a request for RPM 
        rpm = tn.read_until("UNABLE TO CONNECT", 5) #reads for up to 5 seconds or until the word "UNABLE TO CONNECT" appears

        rpm = rpm.split(" 41 0C ", 1) #splits the resulting response by 0C, the string after 0C contains RPM data

        if len(rpm) == 2: 
            #print "data size is 2"
            rpm = rpm[1] #sets data as the RPM data string

            if len(rpm) > 5: #this is to strip off all except for the first 5 characters
                length = len(rpm)
                length = length - 5
                length = -1 * length
                rpm = rpm[:length]
        else:
            rpm = "00 00" #added to cover case when ECU does not respond to RPM request and sends unexpected data 

        time.sleep(1) #to prevent overflowing OBD buffer

    f.write("Car turned on at " + time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime()) + "\n\n\n")
    
    print "CAR IS ON!"
    return 1

def check_car_off(): #used to check if car is off

    tn.write("010C\r\n") 
    rpm = tn.read_until("UNABLE TO CONNECT", 2) 

    rpm = rpm.split(" 41 0C ", 1)

    if len(rpm) != 2: #covers the case when ECU does not return anything because car is off
        print "CAR IS OFF"
        return 0

    rpm = rpm[1]

    if len(rpm) > 5: #this is to strip off all except for the first 5 characters
        length = len(rpm)
        length = length - 5
        length = -1 * length
        rpm = rpm[:length]

    if rpm == "00 00":
        print "CAR IS OFF"
        return 0

    return 1 #if none of the cases are true, we fall through and return that car is on

try:

    ENG_ON = 0 #engine on flag init to false (engine is off)
    INIT_FUEL_LEVEL = 0 #fuel level when car was turned on
    FIN_FUEL_LEVEL = 0 #fuel when car was turned off
    FUEL_NA = 0 #flag to alert if ECU does not support fuel data
    START_TIME = 0
    STOP_TIME = 0
    RUN_TIME = 0
    
    print "Attempting to connect to obd" #debug

    tn = telnetlib.Telnet(HOST, PORT) #connect to obd dongle at port 35000 with IP defined above using telnet

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

    
    print "Waiting for car to turn on"
    ENG_ON = wait_car_on() #wait till car is on
    START_TIME = time.time()
    print "Getting initial fuel level"
    if ENG_ON == 1: #grabbing initial fuel level
        tn.write("012F\r\n") #sends a request for fuel level 
        iFuel = tn.read_until("UNABLE TO CONNECT", 10)

        iFuel = iFuel.split(" 2F ", 1) 

        if len(iFuel) == 2:
            iFuel = iFuel[1]

            if len(iFuel) > 2: #this is to strip off all except for the first 2 characters
                length = len(iFuel)
                length = length - 2
                length = -1 * length
                iFuel = iFuel[:length]

            INIT_FUEL_LEVEL = int(iFuel, 0)
            f.write("Initial Fuel Level: " + iFuel + "\n\n\n") #write initial fuel level as the first thing on the file
            print "Initial Fuel Level: " + iFuel

        else:
            f.write("Initial Fuel Level: N/A\n\n\n") #if ECU does not support fuel level input or unexpected output was returned
            print "Failed to get initial fuel level"
            FUEL_NA = 1

    print "Driving"        
    while ENG_ON == 1: #this is where we spin gathering speed data and checking to see if the trip has ended

        tn.write("010D\r\n") #sends a request for vehicle speed
        speed = tn.read_until("NO DATA", 5)
        print "speed: " + speed
        
        tn.write("0110\r\n") #requests Mass Air Flow rate which is used for calculating MPG
        maf = tn.read_until("NO DATA", 5)
        print "maf: " + maf
        
        speed = speed.split(" 41 0D ", 1)
        
        if len(speed) == 2:
            speed = speed[1]
            if len(speed) > 2: #this is to strip off all except for the first 2 characters
                length = len(speed)
                length = length - 2
                length = -1 * length
                speed = speed[:length]

        else:
            speed = "NA"
            

        maf = maf.split(" 10 ", 1)
        if len(maf) == 2:
            maf = maf[1]
            

        else:
            maf = "NA"
        

        f.write(time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime()) + " speed: " + speed + " maf: " + maf + "\n") #formula for calculating MPG is VSS * 7.718 / MAF
        print time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime()) + " speed: " + speed + " maf: " + maf 

        ENG_ON = check_car_off() #check to see if car has been turned off
        if ENG_ON == 0:
            STOP_TIME = time.time()
        time.sleep(5) #wait five seconds before polling speed and MAF again

    #if we break out, it's because engine is off or something went wrong. Try to grab final fuel level and exit

    if FUEL_NA == 0:
        tn.write("012F\r\n") #sends a request for fuel level 
        fFuel = tn.read_until("UNABLE TO CONNECT", 10)

        fFuel = fFuel.split(" 2F ", 1) 

        if len(fFuel) == 2:
            fFuel = fFuel[1]
            FIN_FUEL_LEVEL = int(fFuel, 0)
            f.write("Final Fuel Level: " + fFuel + "\n\n\n")
            if FIN_FUEL_LEVEL > INIT_FUEL_LEVEL: #we check here whether the car has been refilled with gas, this would trigger an entire tank fuel economy calculation
                f.write("Car has been filled up with gas on this trip\n\n\n")

    else:
        f.write("\n\n\nFinal Fuel Level: N/A\n\n\n")

    RUN_TIME = STOP_TIME - START_TIME
    f.write("Car turned off at " + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + "\n\n\n")
    f.write("Trip duration: " + str(RUN_TIME))
    print "Trip duration: " + str(RUN_TIME)
        
    
    tn.close() #close telnet connection
    f.close() #close file

    #now we want to connect to the server to transfer our log file
    #TODO: INSERT CODE TO SWITCH WIFI CONNECTION
        #as a place holder, we will just wait for 10 seconds to have the user manually switch the wifi connection
    time.sleep(10)

    #TODO: If wifi connection fails, we should store the names of the files to be transferred in a file called queue.txt
    #which will be cleared after every successful transmit
    
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating a TCP socket
    socket.connect((SERVER, SERVER_PORT)) #connecting to the server

    with open(f, 'rb') as send_file: #open the log file for reading
        for data in send_file:
            socket.sendall(data) #send file over TCP to server

    #TODO: we should wait for an ACK from the server containing the size of the file

    socket.close() #close the socket 
    print "Done"

except KeyboardInterrupt: #catches CTRL-C and exits gracefully
    print "Exiting"
    tn.close()
    f.close()

except:
    print "Unexpected Error, closing files and exiting"
    f.close()
    tn.close()
