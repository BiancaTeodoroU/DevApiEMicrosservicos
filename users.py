import json 

with open("users.json") as file:
    usuarios = json.load(file)

print(usuarios)