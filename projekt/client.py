import os
import socket, ssl
from random import randrange
from func import gcdExtended

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ssl_sock = ssl.wrap_socket(s,
                           ca_certs="cert.pem",
                           cert_reqs=ssl.CERT_REQUIRED,
                           ssl_version=ssl.PROTOCOL_TLSv1)
ssl_sock.connect(('127.0.0.1',5151))
numberOfPeople = int(ssl_sock.recv(4096))
id = int(ssl_sock.recv(4096))
g = int(ssl_sock.recv(4096))
p = int(ssl_sock.recv(4096))
q = int(ssl_sock.recv(4096))

print("Ilość: ", numberOfPeople)
print("n: ", id)
print("g: ", g)
print("p: ", p)
print("q: ", q)

while True:
    x = randrange(1,q)
    gx = pow(g,x,p)
    ssl_sock.send(str.encode(str(gx),'utf-8'))

    gy = 1
    for i in range(id):
        y = int(ssl_sock.recv(4096))
        gy=(gy*y) % p
    for i in range(id+1,numberOfPeople):
        y = int(ssl_sock.recv(4096))
        gy = (gcdExtended(y,p)[1]*gy) % p


    an = int(input("Wprowadz odpoewiedz: "))
    if an == 0:
        ssl_sock.send(str.encode(str(pow(gy,x,p)),'utf-8'))
    else:
        rand = randrange(1,q)
        ssl_sock.send(str.encode(str(pow(gy,rand,p)),'utf-8'))

    res = int(ssl_sock.recv(4096))
    print("Wynik: ", res)



ssl_sock.close()
