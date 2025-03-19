import hashlib, json
senha = "26"
hash = hashlib.sha256(senha.encode()).hexdigest()
print(hash)


with open('usuarios.json', 'r') as f:
    users = json.load(f)
    
print(users['admin'])
print(users['prof'])
