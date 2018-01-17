from Crypto.Cipher import ChaCha20
class Encryption:
    def __init__(self, name, product, noofusers, noofdaystrial):
        self.name = name
        self.product = product
        self.noofusers = noofusers
        self.noofdaystrial = noofdaystrial

    def license_details(self):
        #license_details_list = self.name + " " 
        #license_details_list += self.product + " " 
        #license_details_list += str(self.noofusers) + " "
        #license_details_list += str(self.noofdaystrial)
        license_details_list = [self.name,self.product,self.noofusers,self.noofdaystrial]
        return " ".join(str(e) for e in license_details_list) 

    def encrypt(self):
        plaintext = str.encode(self.license_details())
        secret = b'*Thirty-two byte (256 bits) key*'
        cipher = ChaCha20.new(key=secret)
        msg = cipher.nonce +  (cipher.encrypt(plaintext))
        return msg

    def decrypt(self,bytetext):
        self.bytetext = bytetext
        secret = b'*Thirty-two byte (256 bits) key*'
        msg_nonce = self.bytetext[:8]
        ciphertext = self.bytetext[8:]
        cipher = ChaCha20.new(key=secret, nonce=msg_nonce)
        plaintext = cipher.decrypt(ciphertext )
        return plaintext.decode("utf-8").split(' ')

#sampletext = b'\x04\x1f<\x9d\x89\xfb\xf4_F\x9e)\x07XP\xa9\xa7\xaf)@\xa7\x9f\xa40|\xe3N\xabC\x86\xec\x0b\xfezv'
#resultlist = Encryption.decrypt(EOBJ,sampletext)
#print(resultlist)