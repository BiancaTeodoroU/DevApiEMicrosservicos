from fastapi import FastAPI, Request
import datetime
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    nome: str
    data: datetime.datetime
    posicao: int
    tipo: str
    atendido: bool

#parte1
lista = []

def getPessoa(posicao):
    pessoa = None
    for i in lista:
        if i['posicao'] == posicao:
            pessoa = i 
    return pessoa

#parte1
@app.get('/fila')
def get_lista():
    return [{'nome': x.nome, 'data': x.data, 'posicao': x.posicao} for x in lista]

#parte2
@app.get('/fila/{id}')
def getP(id):
    print(id)
    pessoa = getPessoa(int(id))
    if pessoa == None:
        raise HTTPException(
            status_code=404,
            detail="Pessoa não encontrada",
            headers={"X-Error": "There goes my error"},
        )
    pessoa2 = {'nome': pessoa['nome'], 'data': pessoa['data'], 'posicao': pessoa['posicao']}
    return pessoa2

#parte3

@app.post('/fila')
def getAd(dados:Item):
    print(dados)
    if dados.nome != None and len(dados.nome) > 20:
        return 'O campo nome é obrigatório e deve ter no máximo 20 caracteres'
    if dados.tipo not in ['N', 'n', 'P', 'p']:
        return 'O campo tipo de atendimento só aceita 1 caractere (N ou P)'
    lista.append(dados)
    return dados
    #atendimento = input('Atendimento normal ou prioritário?: ')

