import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

clientes = [
    {
        "id": 1,
        "nome": "Silvio Santos",
        "valor_na_conta": 10000,
        "transacoes": [
            {
                "id": 1
                "valor": "1500",
                "tipo": "d",
                "descricao" : "Uma transacao"
            }
        ],
    },
    {
        "id": 2,
        "nome": "Fausto Silva",
        "valor_na_conta": 10,
        "transacoes": [
            {
                "id": 1
                "valor": "1500",
                "tipo": "c",
                "descricao" : "Uma transacao"
            },
            {
                "id": 2
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

@app.get("/cliente/{cliente_id}")
async def busca_cliente(cliente_id: int):
    return clientes[cliente_id - 1]

@app.get("/cliente/{cliente_id}/transacao")
async def busca_transacoes(cliente_id: int):
    cliente = clientes[cliente_id - 1]
    if "transacoes" in cliente:
        return cliente["transacoes"]
    else:
        return{"message": "Cliente não possui transações"}

@app.get("/cliente/{cliente_id}/transacao/{transacao_id}")
async def busca_transacoes_por_id(cliente_id: int):
    cliente = clientes[cliente_id - 1]
    if "transacoes" in cliente:
        return cliente["transacoes"]
    else:
        return{"message": "Cliente não possui transações"}