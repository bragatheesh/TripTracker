# TripTracker
Python program for RPi to communicate with OBD to aggregate car data per trip

Readme is still WIP like the rest of the project:

Introduction: 
TripTracker is an IOT device which will enable you to track your trips with almost any automobile. The device will be prototyped with a Raspberry Pi 3 combined with a GPS shield along with a OBD dongle. The Raspberry Pi will be able to combine data taken from the car and the GPS shield opening up an unlimited range of applications. In its early development, TripTracker will do the following things: collect vehicle speed, collect position data, log both data points, transmit log back to home server where an application will aggregate and analyze the data and return a trip summary. TripTracker will be programmed in Python and will feature both client and server components: client is the data acquiring tool (Pi3); server stores and analyzes all data and will display in a polished way. 

Tools Required:
Raspberry Pi3 (because of inbuilt wifi and bluetooth)
GPS Shield or some other way of accessing and logging location data
Interface to the car’s OBD port (WiFi or Bluetooth)
Computer running the server

Client Process:
Interface Pi3 with OBD dongle through either wifi or bluetooth
Use Pi to request vehicle speed data
Log requested data
Interface Pi3 with GPS device
Log position
Send data to server

Server Process:
Receive data from Pi
Analyze and plot data
Display data

