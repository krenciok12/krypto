
from random import randrange, getrandbits

def gcdExtended(a, b):

    if a == 0 :
        return b, 0, 1

    gcd, x1, y1 = gcdExtended(b%a, a)

    x = y1 - (b//a) * x1
    y = x1

    return gcd, x, y

def is_prime(n, k=128):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    for i in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True
def generate_prime_candidate(length):

    p = getrandbits(length)
    p |= (1 << length - 1) | 1
    return p

def generate_prime_number(length=1024):
    p = 4
    while not is_prime(p, 128):
        p = generate_prime_candidate(length)
    return p

def schnoor_group(length=512):
    q=generate_prime_number(length)
    r=getrandbits(length)
    p=q*r+1
    while not is_prime(p, 128):
        r = getrandbits(length)
        p = r*q+1

    h=getrandbits(length)
    g = pow(h,r,p)
    while g==1:
        h = getrandbits(length)
        g = pow(h,r,p)


    return g, p, q
"""
g,p,q = schnoor_group(512)

n = 7
X = []
for i in range(n):
    X.append(randrange(1,q))

Gx = []
for i in range(n):
    Gx.append(pow(g,X[i],p))

Gy = []
for i in range(n):
    tmp = 1
    for j in range(i):
        tmp=(tmp*Gx[j]) % p
    for j in range(i+1,n):
        t = gcdExtended(Gx[j],p)[1]
        tmp *= (gcdExtended(Gx[j],p)[1]*tmp) %p
    Gy.append(tmp)

tmp=1
for i in range(n):
    tmp=(tmp*pow(Gy[i],X[i],p)) % p
    print(i,tmp)

print(tmp)
"""
