import random
import math

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

def gcd(a, b):
    if a == 0 :
        return b

    return gcd(b%a, a)

def gcdExtended(a, b):

    if a == 0 :
        return b, 0, 1

    gcd, x1, y1 = gcdExtended(b%a, a)

    x = y1 - (b//a) * x1
    y = x1

    return gcd, x, y

def gen(n):
    private = []
    k=0
    for i in range(n):
        r = random.randint(k+1,k+10)
        k += r
        private.append(r)

    M = sum(private) + random.randint(1,private[n-1])

    w = random.randint(math.floor(M/2),M)
    g, W, _ = gcdExtended(w,M)
    while g!=1:
        w = random.randint(math.floor(M/2),M)
        g, W, _ = gcdExtended(w,M)

    W = W % M

    public = [it*w % M for it in private]


    return public, private, M, W

def enc(public, m):
    n = len(public)
    bm = text_to_bits(m)
    ciphertext = []
    for i in range(0,len(bm),n):
        ciphertext.append(sum(public[j]*int(bm[i+j]) for j in range(0,n)))

    return ciphertext

def dec(private, M, W, m):
    n = len(private)
    plaintext = ""
    for it in m[::-1]:
        k = it*W % M
        for it2 in private[::-1]:
            if (k>=it2):
                k=k-it2
                plaintext = "1" + plaintext
            else:
                plaintext = "0" + plaintext

    return text_from_bits(plaintext)


n = int(input("Wprowadz n: "))

public, private, M, W = gen(n)

print("private key: \n",private)
print("M: \n",M)
print("W: \n",W)
print("public key: \n",public)


plaintext = "tajemnicza wiadomosc nr1"
print("tekst: \n", plaintext)

ciphertext = enc(public,plaintext)

print("zaszyfrowane: \n",ciphertext)
decrypted = dec(private, M, W, ciphertext)

print("odszyfrowane: \n",decrypted)
