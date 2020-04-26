from Crypto.Cipher import AES
import random
import string
import base64

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

def xor(s1,s2):
    out =''
    for i in range(0,len(s1)):
        out=out+str(1-abs(int(s1[i])-int(s2[i])))
    return out

def ecb_encrypt(message, key):
    aes = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    return base64.b64encode(aes.encrypt(message.encode('utf-8'))).decode()


def ecb_decrypt(encrypted, key):
    aes = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    return aes.decrypt(base64.b64decode(encrypted.encode('utf-8')))


def enc_ofb(in1,key, iv, enc):
    length=128
    key2=key[:32]
    tmp = text_to_bits(iv)[:length]
    leng = len(in1)
    out=""
    i=0
    while(i+length<=leng):
        tmp = text_to_bits(enc(tmp,key2))
        tmp=tmp[12:length+12]
        tt=xor(tmp,in1[i:i+length])
        out = out + tt
        i=i+length

    if(i!=leng):
        tmp = text_to_bits(enc(tmp,key2))
        tmp=tmp[12:length+12]
        tt=xor(tmp,in1[i:i+length].ljust(length,'0'))
        out = out + tt


    return out

def enc_cbc(in1,key, iv, enc):
    length=128
    key2=key[:32]
    tmp = text_to_bits(iv)[:length]
    leng = len(in1)
    out=""
    i=0
    while(i+length<=leng):
        tmp=xor(tmp,in1[i:i+length])
        tt=enc(tmp,key2)
        tt = text_to_bits(tt)
        out = out + tt
        tmp=tt[12:length+12]
        i=i+length
    if(i!=leng):
        tmp=xor(tmp,in1[i:i+length].ljust(length,'0'))
        tt=enc(tmp,key2)
        tt = text_to_bits(tt)
        out = out + tt

    return out

def dec_cbc(in1,key, iv, enc):
    length=128
    length2=172*8
    key2=key[:32]
    tmp = text_to_bits(iv)[:length]
    leng = len(in1)
    out=""
    i=0
    while(i+length2<=leng):
        tmp2=in1[i+12:i+length+12]
        tt=enc(text_from_bits(in1[i:i+length2]),key2)
        tt =xor(tt.decode("utf-8"),tmp)
        tmp=tmp2
        out = out + tt
        i=i+length2
    return out

def enc_ctr(in1,key, iv, enc):
    length=128
    key2=key[:32]
    tmp = iv
    counter=1
    leng = len(in1)
    out=""
    i=0
    while(i+length<=leng):
        tt=enc(tmp+str(counter).rjust(16,'0'),key2)
        tt = text_to_bits(tt)
        tt=tt[12:length+12]
        tt =xor(tt,in1[i:i+length])
        out = out + tt
        counter+=1
        i=i+length
    if(i!=leng):
        tt=enc(tmp+str(counter).rjust(16,'0'),key2)
        tt = text_to_bits(tt)
        tt=tt[12:length+12]
        tt =xor(tt,in1[i:i+length].ljust(length,'0'))
        out = out + tt

    return out
