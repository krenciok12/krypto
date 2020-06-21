from socketserver import TCPServer, ThreadingMixIn, StreamRequestHandler
import ssl
import func

K=[]
numberOfPeople = int(input("Ilosc osób: "))
k = 0
g,p,q = func.schnoor_group(512)
print(g)
print(p)
print(q)
Gx = [0] * numberOfPeople
Res = [0] * numberOfPeople


class MySSL_TCPServer(TCPServer):
    def __init__(self,
                 server_address,
                 RequestHandlerClass,
                 certfile,
                 keyfile,
                 ssl_version=ssl.PROTOCOL_TLSv1,
                 bind_and_activate=True):
        TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        self.certfile = certfile
        self.keyfile = keyfile
        self.ssl_version = ssl_version

    def get_request(self):
        newsocket, fromaddr = self.socket.accept()
        connstream = ssl.wrap_socket(newsocket,
                                 server_side=True,
                                 certfile = self.certfile,
                                 keyfile = self.keyfile,
                                 ssl_version = self.ssl_version)
        K.append(newsocket)
        return connstream, fromaddr

class MySSL_ThreadingTCPServer(ThreadingMixIn, MySSL_TCPServer): pass

class testHandler(StreamRequestHandler):
    def handle(self):
        global k, numberOfPeople
        id = k

        self.wfile.write(str.encode(str(numberOfPeople),'utf-8'))
        self.wfile.write(str.encode(str(id),'utf-8'))
        self.wfile.write(str.encode(str(g),'utf-8'))
        self.wfile.write(str.encode(str(p),'utf-8'))
        self.wfile.write(str.encode(str(q),'utf-8'))

        while True:
            Gx[id] = int(self.connection.recv(4096))
            k+=1
            while k % numberOfPeople !=0:
                pass

            for i in range(numberOfPeople):
                if i!=id:
                    self.wfile.write(str.encode(str(Gx[i]),'utf-8'))


            Res[id] = int(self.connection.recv(4096))
            k+=1
            while k % numberOfPeople !=0:
                pass

            r=1
            for it in Res:
                r=(r*it) % p

            if r==1:
                self.wfile.write(str.encode(str(0),'utf-8'))
            else:
                self.wfile.write(str.encode(str(1),'utf-8'))

        #self.wfile.write(b'data')




MySSL_ThreadingTCPServer(('127.0.0.1',5151),testHandler,"cert.pem","key.pem").serve_forever()
