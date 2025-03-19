import hashlib, json
senha = "8392"
hash = hashlib.sha256(senha.encode()).hexdigest()
print(hash)


