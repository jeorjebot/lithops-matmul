import phe as paillier

pubkey, privkey = paillier.generate_paillier_keypair()

plain = 123

print(pubkey)
print(privkey)

encrypted = pubkey.encrypt(plain)
print(encrypted)

encrypted *= 234 # 123*123=15129

decrypted = privkey.decrypt(encrypted)
print(decrypted)