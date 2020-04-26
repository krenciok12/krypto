import sys
import chilkat
import fun

glob = chilkat.CkGlobal()
success = glob.UnlockBundle("Anything")

#"keystore.jks"
keystore=input("Keystore: ")

#"password"
password=input("Haslo: ")

jks = chilkat.CkJavaKeyStore()
success = jks.LoadFile(password,keystore)
if (success != True):
    print(jks.lastErrorText())
    sys.exit()

#"0"
index=int(input("Indeks: "))
secretKey = jks.getSecretKey("password", index, "base64");

#ccNumber = fun.text_to_bits(open('text1.txt','r+').read())

rodzaj=input("Rodzaj: ")
q= int(input("Ilosc: "))
M=[input("Wiadaomosć {}: ".format(i+1)) for i in range(q)]



if (rodzaj=="cbc"):
    for m in M:
        iv = fun.randomString(16)
        encryptedStr = fun.enc_cbc(fun.text_to_bits(m),secretKey,iv, fun.ecb_encrypt)
        print("m: ",m)
        print("iv: ",iv)
        print("Encrypted: ",encryptedStr)
        print("\n")

        #decryptedStr = fun.dec_cbc(encryptedStr,secretKey,iv,fun.ecb_decrypt)
        #print("Decrypted:")
        #print(fun.text_from_bits(decryptedStr))

if (rodzaj=="ofb"):
    for m in M:
        iv = fun.randomString(16)
        encryptedStr = fun.enc_ofb(fun.text_to_bits(m),secretKey,iv, fun.ecb_encrypt)
        print("m: ",m)
        print("iv: ",iv)
        print("Encrypted: ",encryptedStr)
        print("\n")

        #decryptedStr = fun.enc_ofb(encryptedStr,secretKey,iv,fun.ecb_encrypt)
        #print("Decrypted:")
        #print(fun.text_from_bits(decryptedStr))

if (rodzaj=="ctr"):
    for m in M:
        iv = fun.randomString(16)
        encryptedStr = fun.enc_ctr(fun.text_to_bits(m),secretKey,iv, fun.ecb_encrypt)
        print("m: ",m)
        print("iv: ",iv)
        print("Encrypted: ",encryptedStr)
        print("\n")

        #decryptedStr = fun.enc_ctr(encryptedStr,secretKey,iv,fun.ecb_encrypt)
        #print("Decrypted:")
        #print(fun.text_from_bits(decryptedStr))
