import hashlib, json
senha = "7070"
hash = hashlib.sha256(senha.encode()).hexdigest()
print(hash)


       
