from fastapi import FastAPI, Request
import datetime
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

#foi criada uma lista ( array ) vazio para manter as pessoas.

lista = []

# foi criada uma classe Item para representar uma pessoa e 
# para validar os dados dela. 

class Item(BaseModel):
    nome: str
    data: datetime.datetime
    posicao: int = 0
    tipo: str
    atendido: bool

    # na construção da pessoa, coloquei um valor default 
    # da proxima posição na lista que se não tiver ninguem 
    # na fila ele vai pegar o valor definir como 0,
    # caso exista alguem na fila ele já vai definir um novo valor.  
    def __init__(self, **args):
        super().__init__(posicao = 0 if len(lista) == 0 else lista[len(lista) - 1].posicao + 1, **args )

#parte1
# criação das pessoas e adicionando elas na lista ao mesmo tempo.

pessoa1 = Item(
    nome = 'adolfo',
    atendido = False,
    data = datetime.datetime.now(),
    tipo = 'N'
)

lista.append(pessoa1)

pessoa2 = Item(
    nome = 'godofredo',
    atendido = False,
    data = datetime.datetime.now(),
    tipo = 'P'
)

lista.append(pessoa2)

pessoa3 = Item(
    nome = 'seila',
    atendido = False,
    data = datetime.datetime.now(),
    tipo = 'N'
)

lista.append(pessoa3)

# No getPessoa ele encontra a pessoa baseada pela posição 
# e devolve a pessoa, caso ela esteja na fila, se não retorna None.

def getPessoa(posicao):
    pessoa = None
    for i in lista:
        if i.posicao == posicao:
            pessoa = i 
    return pessoa

# ele percorre toda a lista de pessoas, 
# atualizando a posição delas a partir do inicio informado.

def updateListaAtendimento(inicio):
    for i in range(inicio,len(lista)):
        lista[i].posicao = lista[i].posicao -1
        if lista[i].posicao == 0: 
            lista[i].atendido == True

#parte1
# aqui ele exibe as informações da pessoa na lista.

@app.get('/fila')
def get_lista():
    return [{'nome': x.nome, 'data': x.data, 'posicao': x.posicao} for x in lista]

# getP manda uma mensagem de erro caso a pessoa não exista na posição 
# informada na fila determinada. caso a pessoa é encontrada ele retorna,
# os dados da pessoa.
#parte2
@app.get('/fila/{id}')
def getP(id):
    pessoa = getPessoa(int(id))
    if pessoa == None:
        raise HTTPException(
            status_code=404,
            detail="Pessoa não encontrada",
            headers={"X-Error": "There goes my error"},
        )
    pessoa2 = {'nome': pessoa.nome, 'data': pessoa.data, 'posicao': pessoa.posicao}
    return pessoa2

# getAD valida os dados e caso esteja correto os dados, ele cadastra
# a pessoa na fila, caso não estejam certos ele retorna mensagens 
# informando oque está errado.

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

#parte4

#atualiza a posição de todas as posições das pessoas na fila.

@app.put('/fila')
def updatePosicao():
    updateListaAtendimento(0)
    return('Atualizado')

#parte5

# ele remove a pessoa informada da lista e atualiza todas
# as posições das pessoas na fila, após a pessoa deletada.
# e caso a pessoa da posição na fila não exista, informa um erro 404 
# em formato json.

@app.delete('/fila/{id}')
def deletePessoa(id):
    pessoa = getPessoa(int(id))
    print(pessoa)
    if pessoa == None:
        raise HTTPException(status_code=404, detail='Item not found')
    index = lista.index(pessoa) 
    lista.remove(pessoa)
    updateListaAtendimento(index)
    return('Tudo certo')

