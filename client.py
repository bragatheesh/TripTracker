import socket

HOST = socket.gethostname()    #server name goes in here
PORT = 6000             
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST,PORT))
with open('TODO.txt', 'rb') as file_to_send:
    for data in file_to_send:
        socket.sendall(data)
print 'end'
socket.close()
