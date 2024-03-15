from fastapi import FastAPI, HTTPException
from model import Cliente, Transacao, AtualizarTransacao
from services import (criar_transacao_func, listar_transacoes_func, obter_transacao_func, atualizar_transacao_func, deletar_transacao_func, obter_cliente_func)
from typing import List

app = FastAPI()

@app.get("/clientes/{id_cliente}", response_model=Cliente)
async def obter_cliente_endpoint(id_cliente: int):
    return obter_cliente_func(id_cliente)

@app.post("/clientes/{id_cliente}/transacoes")
async def criar_transacao_endpoint(id_cliente: int, transacao: Transacao):
    return criar_transacao_func(id_cliente, transacao)

@app.get("/clientes/{id_cliente}/transacoes", response_model=List[Transacao])
async def listar_transacoes_endpoint(id_cliente: int):
    return listar_transacoes_func(id_cliente)
    
@app.get("/clientes/{id_cliente}/transacoes/{transacao_id}", response_model=Transacao)
async def obter_transacao_endpoint(id_cliente: int, transacao_id: int):
    return obter_transacao_func(id_cliente, transacao_id)

@app.put("/clientes/{id_cliente}/transacoes/{transacao_id}", response_model=Transacao)
async def atualizar_transacao_endpoint(id_cliente: int, transacao_id: int, transacao_atualizada: AtualizarTransacao):
    return atualizar_transacao_func(id_cliente, transacao_id, transacao_atualizada)
            
@app.delete("/clientes/{id_cliente}/transacoes/{transacao_id}")
async def deletar_transacao_endpoint(id_cliente: int, transacao_id: int):
    return deletar_transacao_func(id_cliente, transacao_id)