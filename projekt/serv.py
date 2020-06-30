from socketserver import TCPServer, ThreadingMixIn, StreamRequestHandler
import ssl
import func
from random import randint

numberOfPeople = int(input("Ilosc osób: "))
counter = 0
questioner = 0
question = ""
asked = True
g,p,q = func.schnoor_group(512)
Gx = [0] * numberOfPeople
Res = [0] * numberOfPeople


class MySSL_TCPServer(TCPServer):
    def __init__(self,
                 server_address,
                 RequestHandlerClass,
                 certfile,
                 keyfile,
                 ssl_version=ssl.PROTOCOL_TLSv1_2,
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
        return connstream, fromaddr

class MySSL_ThreadingTCPServer(ThreadingMixIn, MySSL_TCPServer): pass

class testHandler(StreamRequestHandler):
    def handle(self):
        global counter, numberOfPeople, questioner, asked, question

        id = counter

        if counter>=numberOfPeople:
            return

        self.wfile.write(str.encode(str(numberOfPeople),'utf-8'))
        self.wfile.write(str.encode(str(id),'utf-8'))
        self.wfile.write(str.encode(str(g),'utf-8'))
        self.wfile.write(str.encode(str(p),'utf-8'))
        self.wfile.write(str.encode(str(q),'utf-8'))

        while True:

            Gx[id] = int(self.connection.recv(4096))

            #zero knowledge proof
            for i in range (10):
                gr = int(self.connection.recv(4096))
                t = randint(0,1)
                self.wfile.write(str.encode(str(t),'utf-8'))
                if t == 0:
                    r = int(self.connection.recv(4096))
                    if gr!=pow(g,r,p):
                        print("BŁĄD")
                if t == 1:
                    xr = int(self.connection.recv(4096))
                    if (Gx[id]*gr) % p !=pow(g,xr,p):
                        print("BŁĄD")

            counter+=1
            while counter % numberOfPeople !=0:
                pass

            for i in range(numberOfPeople):
                if i!=id:
                    self.wfile.write(str.encode(str(Gx[i]),'utf-8'))

            self.wfile.write(str.encode(str(questioner),'utf-8'))
            if id==questioner:
                question = str(self.connection.recv(4096))
                asked = False
                questioner=(questioner+1) % numberOfPeople
            else:
                while asked:
                    pass
                self.wfile.write(str.encode(str(question),'utf-8'))
                asked = True

            gy = int(self.connection.recv(4096))
            Res[id] = int(self.connection.recv(4096))

            for i in range (10):
                gr = int(self.connection.recv(4096))
                t = randint(0,1)
                self.wfile.write(str.encode(str(t),'utf-8'))
                if t == 0:
                    r = int(self.connection.recv(4096))
                    if gr!=pow(gy,r,p):
                        print("BŁĄD")
                if t == 1:
                    xr = int(self.connection.recv(4096))
                    if (Res[id]*gr) % p !=pow(gy,xr,p):
                        print("BŁĄD")

            counter+=1
            while counter % numberOfPeople !=0:
                pass

            for it in Res:
                self.wfile.write(str.encode(str(it),'utf-8'))



        #self.wfile.write(b'data')




MySSL_ThreadingTCPServer(('127.0.0.1',5151),testHandler,"certificate.pem","Key.pem").serve_forever()
