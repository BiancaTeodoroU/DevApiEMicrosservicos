import requests

response = requests.get("https://toledoprudente.edu.br/")
usuario = response.json()
print(f'Nome de usuario: {usuario["name"]}')