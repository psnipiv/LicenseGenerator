from cryptography.fernet import Fernet

class Encryption:
    def __init__(self, name, product, noofusers, noofdaystrial):
        self.name = name
        self.product = product
        self.noofusers = noofusers
        self.noofdaystrial = noofdaystrial

    def license_details(self):
        license_details_list = [self.name, self.product, self.noofusers, self.noofdaystrial]
        str1 = ','.join(str(element) for element in license_details_list)
        return str1

    def encrypt(self):
        key = Fernet.generate_key()
        f_key = Fernet(key)
        token = f_key.encrypt(self.license_details())
        return token
        #return f_key.decrypt(token)

EOBJ = Encryption(name='Microsoft', product="Azure", noofusers=15, noofdaystrial=365)
print(Encryption.encrypt(EOBJ))
