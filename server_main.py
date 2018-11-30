import socket
import sys, time
import  binascii, threading, struct, traceback, select

class client(threading.Thread):
    status = True
    socket = None
    address = None
    connection = None
    data_header = []
    data_label = []
    data_value = []
    hold_up = None
    t = None
    death = False
    def __init__(self, sock, addr, conn):
        threading.Thread.__init__(self)
        self.socket = sock
        self.address = addr[0]
        self.connection = conn

    def run(self):
        try:
            #nonblocking socket
            self.socket.setblocking(0)

            while(self.status is True):
                try:
                                        try:
                                                ready_to_read, ready_to_write, in_error = select.select([self.connection,], [self.connection,], [], 5)
                                                #print("Not closed")
                                                
                                        except select.error:
                                                self.connection.shutdown(2)    # 0 = done receiving, 1 = done sending, 2 = both
                                                self.connection.close()
                                            # connection error event here, maybe reconnect
                                                print('connection error')
                                                self.death = True
                                        #print("receiving data")
                                        data = self.recv_msg(self.connection)
                                        if not self.death and data is not None:
                                                #print("unpacking data")
                                                temp = self.unpack(data,"+",";")
                                                #print("parsing data")
                                                recv_data_headers = temp[0]
                                                recv_data_labels = temp[1]
                                                recv_data_values = temp[2]



                                                #print("added to hold up")
                                                self.data_header.append(recv_data_headers)
                                                self.data_label.append(recv_data_labels)
                                                self.data_value.append(recv_data_values)
                                                #print(self.status)
                                    #except(socket.error):
                                    #   if e.errno is errno.ECONNRESET:
                                    #       print("Client disconnected")
                                    #       self.status = False
                                    #       while self.status is False:
                                    #           time.sleep(0.001)
                                    #       self.status = False
                except Exception as exp:
                    self.death = True
                    print("self.death",self.death)
                    pass
                if(len(self.data_label) > 0):
                    if self.hold_up is None:
                        self.hold_up = [self.data_header[0],self.data_label[0],self.data_value[0]]
                        del self.data_header[0]
                        del self.data_label[0]
                        del self.data_value[0]
                time.sleep(0.001)
        except:
            #client disconnected
            #print("client ", self.address, " disconnected :: ")
            traceback.print_exc()
            self.status = False
            while self.status is False:
                time.sleep(0.001)
        #print("Thread closing ",self.address)
        #after the above finishes, the thread will die
    def next_data(self):
        temp = self.hold_up
        self.hold_up = None
        #print("Hold up pulled")
        return temp
    def recv_msg(self, sock):
        # Read message length and unpack it into an integer
        raw_msglen = self.recvall(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(sock, msglen).decode('utf-8')

    def recvall(self, sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = b''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data
    def unpack(self,data,delimiter_sub,delimiter_break):
        data_header = []
        data_labels = []
        data_values = []
        while len(data) > 0:
            data_header.append(data[:data.index(delimiter_sub)])
            data = data[data.index(delimiter_sub)+1:]
            data_labels.append(data[:data.index(delimiter_sub)])
            data = data[data.index(delimiter_sub)+1:]
            data_values.append(data[:data.index(delimiter_break)])
            data = data[data.index(delimiter_break)+1:]
        return [data_header,data_labels,data_values]


class main_thread(threading.Thread):
    status = True
    clients = []
    def __init__(self, clients):
        threading.Thread.__init__(self)
        self.clients = clients
        #print("Switchboard active!")

    def run(self):
        try:
            while self.status is True:
                if(len(self.clients) > 0):
                    remove = []
                    for x in range(0,len(self.clients)):
                        client = self.clients[x]
                        if client.death is True:
                            #print("adding",x,"to list")
                            remove.append(x)
                        #header, label, data
                        client_data = client.next_data()
                        if(client_data is not None):
                            #print("hold up has value")
                            header = client_data[0][0]
                            label = client_data[1][0]
                            data = client_data[2][0]
                            
                            print(header)
                            print(label)
                            print(data)
                    for x in range(len(remove)-1,-1,-1):
                        #print("Deleting",x)
                        del self.clients[x]
        except:
            traceback.print_exc()
    def decompose_header(self, header):
            destination = header[:header.index(",")]
            header = header[header.index(",")+1:]

            source = header[:header.index(",")]
            header = header[header.index(",")+1:]

            label = header

            return [destination,source,label]




    def update_clients(self, new_client):
            self.clients.append(new_client)

    
port = 324
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind to port
server_address = ('', port)
sock.bind(server_address)

#start the listening process

print("test2")
#start the client acceptance system
print("accepting clients on port ",port)
clients = []

mt = main_thread(clients)
mt.start()
print("test3")
sock.setblocking(1)

if __name__ == "__main__":
        while True:
            try:
            
                sock.setblocking(1)
                sock.listen(1)
                conn,addr = sock.accept()
                #print client address info\
                print("client connected :: ",addr)
                new_client = client(sock,addr,conn)
                new_client.start()
                remove_index = mt.update_clients(new_client)

            except Exception as exc:
                print(exc)
                pass


