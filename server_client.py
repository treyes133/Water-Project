import socket
import sys, time
import  binascii, threading, struct, traceback



if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    address = "localhost"

    port = 324

    server_address = (address, port)
    print("connecting to ",address," on port ",port)
    sock.connect(server_address)

    print("Connected")

    message = "receiver1+data+1010;"
    message = bytes(message.encode('utf-8'))
    msg = struct.pack('>I', len(message)) + message 
    sock.sendall(msg)


    sock.sendall(message)

    time.sleep(5)
    sock.close()

    
