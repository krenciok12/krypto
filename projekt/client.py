import os
import socket, ssl
from random import randrange
from func import gcdExtended

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ssl_sock = ssl.wrap_socket(s,
                           ca_certs="certificate_c.pem",
                           cert_reqs=ssl.CERT_REQUIRED,
                           ssl_version=ssl.PROTOCOL_TLSv1_2)
ssl_sock.connect(('127.0.0.1',5151))

numberOfPeople = int(ssl_sock.recv(4096))
id = int(ssl_sock.recv(4096))
g = int(ssl_sock.recv(4096))
p = int(ssl_sock.recv(4096))
q = int(ssl_sock.recv(4096))


while True:

    x = randrange(1,q)
    gx = pow(g,x,p)
    ssl_sock.send(str.encode(str(gx),'utf-8'))

    for i in range(10):
        r = randrange(1,q)
        ssl_sock.send(str.encode(str(pow(g,r,p)),'utf-8'))
        t = int(ssl_sock.recv(4096))
        if t == 0:
            ssl_sock.send(str.encode(str(r),'utf-8'))
        if t == 1:
            xr = (x+r)%q
            ssl_sock.send(str.encode(str(xr),'utf-8'))

    gy = 1
    for i in range(id):
        y = int(ssl_sock.recv(4096))
        gy=(gy*y) % p
    for i in range(id+1,numberOfPeople):
        y = int(ssl_sock.recv(4096))
        gy = (gcdExtended(y,p)[1]*gy) % p

    questioner = int(ssl_sock.recv(4096))

    if questioner==id:
        question = input("Wprowadź pytanie: ")
        ssl_sock.send(str.encode(str(question),'utf-8'))
    else:
        print("Czekaj na pytanie")
        question = (ssl_sock.recv(4096))
        print("Pytanie: ",question.decode('utf-8'))


    an = str(input("Wprowadz odpowiedz: "))
    while an not in ["tak","nie"]:
        an = str(input("Wprowadz jeszcze raz: "))

    c = 0
    if an == "nie":
        c = x
    else:
        c = randrange(1,q)

    ssl_sock.send(str.encode(str(gy),'utf-8'))
    ssl_sock.send(str.encode(str(pow(gy,c,p)),'utf-8'))
    for i in range(10):
        r = randrange(1,q)
        ssl_sock.send(str.encode(str(pow(gy,r,p)),'utf-8'))
        t = int(ssl_sock.recv(4096))
        if t == 0:
            ssl_sock.send(str.encode(str(r),'utf-8'))
        if t == 1:
            xr = (c+r)%q
            ssl_sock.send(str.encode(str(xr),'utf-8'))

    res=1
    for i in range(numberOfPeople):
        res=(res*int(ssl_sock.recv(4096))) % p



    if res==1:
        print("Nikt nie odpowiedział twierdząco na pytanie")
    else:
        print("Ktoś odpowiedział twierdząco na pytanie")



ssl_sock.close()
