import requests
import pytest
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi import HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.testclient import TestClient

app = FastAPI()

clientes = [
    {
        "id": 1,
        "nome": "Silvio Santos",
        "valor_na_conta": "10000",
        "transacoes": [
            {
                "id": 1,
                "valor": "1500",
                "tipo": "d",
                "descricao" : "Uma transacao"
            }
        ],
    },
    {
        "id": 2,
        "nome": "Fausto Silva",
        "valor_na_conta": "10",
        "transacoes": [
            {
                "id": 1,
                "valor": "1500",
                "tipo": "c",
                "descricao" : "Uma transacao"
            },
            {
                "id": 2,
                "valor": "32",
                "tipo": "d",
                "descricao" : "Uma transacao"
            }
        ],
    },
    {
        "id": 3,
        "nome": "Gugu liberato",
        "transacoes": [],
    }
]

class NovaTransacao(BaseModel):
    valor: int
    tipo: str
    descricao: str

class TransacaoAtualizada(BaseModel):
    valor: int
    tipo: str
    descricao: str



@app.post("/clientes/{cliente_id}/transacoes")
async def criar_transacao(cliente_id: int, transacao: NovaTransacao):
    cliente = clientes[cliente_id - 1]
    nova_transacao = {
        "id": len(cliente["transacoes"]) + 1,
        "valor": transacao.valor,
        "tipo": transacao.tipo,
        "descricao": transacao.descricao
    }
    cliente["transacoes"].append(nova_transacao)
    return nova_transacao

cliente = TestClient(app)

def test_criar_transacao():
    cliente_id = 1
    cliente = clientes[cliente_id - 1]
    nova_transacao = {
        "valor": 1500,
        "tipo": "c",
        "descricao": "Uma transacao"
    }
    response = cliente.post("/clientes/{cliente_id}/transacoes", json=nova_transacao)
    assert response.status_code == 200
    assert response.json() == {
        "id": len(cliente['transacoes']) + 1,  # Usando o próximo ID disponível
        "valor": 1500,
        "tipo": "c",
        "descricao": "Uma transacao"
    }

# -----------------------------------------------------------------------------------------------------------


@app.get("/cliente/{cliente_id}")
async def busca_cliente(cliente_id: int):
    return clientes[cliente_id - 1]

cliente = TestClient(app)

def test_busca_cliente():
    response = cliente.get("/cliente/1")
    expected_data = {
        "id": 1,
        "nome": "Silvio Santos",
        "valor_na_conta": "10000",
        "transacoes": [
            {
                "id": 1,
                "valor": 1500,  # Convertido para inteiro
                "tipo": "d",
                "descricao": "Uma transacao"
            }
        ]
    }
    assert response.status_code == 200
    assert response.json() == expected_data




@app.get("/cliente/{cliente_id}/transacoes")
async def busca_transacoes(cliente_id: int):
    cliente = clientes[cliente_id - 1]
    if "transacoes" in cliente:
        return cliente["transacoes"]
    else:
        return{"message": "Cliente não possui transações"}

def test_read_main():
    response = cliente.get("/clientes/1/transacoes")
    assert response.status_code == 200
    assert response.json() == {
        {
            "id": 1,
            "valor": "1500",
            "tipo": "c",
            "descricao" : "Uma transacao"
        },
        {
            "id": 2,
            "valor": "32",
            "tipo": "d",
            "descricao" : "Uma transacao"
        }
    }


@app.get("/cliente/{cliente_id}/transacao/{transacao_id}")  
async def busca_transacao(cliente_id: int, transacao_id: int):
    cliente = clientes[cliente_id - 1]
    if "transacoes" in cliente:
        for transacao in cliente["transacoes"]:
            if transacao["id"] == transacao_id:
                return transacao
        # Se o loop terminar sem retornar, significa que a transação não foi encontrada
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    else:
        raise HTTPException(status_code=404, detail="Cliente não possui transações")

def test_read_main():
    response = cliente.get("/clientes/2/transacao/1")
    assert response.status_code == 200
    assert response.json() == {
        {
            "id": 1,
            "valor": "1500",
            "tipo": "c",
            "descricao" : "Uma transacao"
        }
    }


@app.put("/clientes/{cliente_id}/transacoes/{transacao_id}")
async def atualiza_transacao(cliente_id: int, transacao_id: int, transacao_atualizada: TransacaoAtualizada):
    cliente = clientes[cliente_id - 1]
    if "transacoes" in cliente:
        for transacao in cliente["transacoes"]:
            if transacao["id"] == transacao_id:
                # Atualiza os detalhes da transação com os valores fornecidos no corpo da requisição
                transacao["valor"] = transacao_atualizada.valor
                transacao["tipo"] = transacao_atualizada.tipo
                transacao["descricao"] = transacao_atualizada.descricao
                return transacao
        # Se o loop terminar sem retornar, significa que a transação não foi encontrada
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    else:
        raise HTTPException(status_code=404, detail="Cliente não possui transações")

def test_atualiza_transacao():
    # Dados de exemplo para o teste
    cliente_id = 1
    transacao_id = 1
    transacao_atualizada = {
        "valor": 100.0,
        "tipo": "Débito",
        "descricao": "Compra de alimentos"
    }

    # Realiza a requisição PUT para atualizar a transação
    response = cliente.put(f"/clientes/{cliente_id}/transacoes/{transacao_id}", json=transacao_atualizada)

    # Verifica se a resposta foi bem-sucedida (código de status 200)
    assert response.status_code == 200

    # Verifica se a transação foi atualizada corretamente
    assert response.json() == {
        "id": transacao_id,
        "valor": 100.0,
        "tipo": "Débito",
        "descricao": "Compra de alimentos"
    }
    

@app.delete("/cliente/{cliente_id}/transacao/{transacao_id}")
async def deleta_transacao(cliente_id: int, transacao_id: int):
    cliente = clientes[cliente_id - 1]
    if "transacoes" in cliente:
        for index, transacao in enumerate(cliente["transacoes"]):
            if transacao["id"] == transacao_id:
                # Remove a transação do cliente
                del cliente["transacoes"][index]
                return status.HTTP_204_NO_CONTENT
        # Se o loop terminar sem retornar, significa que a transação não foi encontrada
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    else:
        raise HTTPException(status_code=404, detail="Cliente não possui transações")