import sys
import chilkat
import fun
import random

glob = chilkat.CkGlobal()
success = glob.UnlockBundle("Anything")

#"keystore.jks"
#keystore=input("Keystore: ")

#"password"
#password=input("Haslo: ")

jks = chilkat.CkJavaKeyStore()
success = jks.LoadFile("password","keystore.jks")
if (success != True):
    print(jks.lastErrorText())
    sys.exit()

index=0
#index=int(input("Indeks: "))
secretKey = jks.getSecretKey("password", index, "base64");

#ccNumber = fun.text_to_bits(open('text1.txt','r+').read())

q= 2
M=[input("Wiadaomosć {}: ".format(i+1)) for i in range(q)]

m= M[random.randint(0,1)]


iv = fun.randomString(16)
encryptedStr = fun.enc_cbc(fun.text_to_bits(m),secretKey,iv, fun.ecb_encrypt)
print("m: ",m)
print("iv: ",iv)
print("Encrypted: ",encryptedStr)
print("\n")

#decryptedStr = fun.dec_cbc(encryptedStr,secretKey,iv,fun.ecb_decrypt)
#print("Decrypted:")
#print(fun.text_from_bits(decryptedStr))
