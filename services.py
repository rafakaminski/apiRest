from model import Cliente, Transacao, AtualizarTransacao
from fastapi import HTTPException

clientes = [
    Cliente(id=1, 
            nome="Silvio Santos",
            valor_na_conta=10000, 
            transacoes=[Transacao(id=1,
                                  valor=1500, 
                                  tipo="d", 
                                  descricao="Uma transacao")]),
    Cliente(id=2, 
            nome="Fausto Silva", 
            valor_na_conta=10, 
            transacoes=[Transacao(id=1,
                                  valor=1500, 
                                  tipo="c", 
                                  descricao="Uma transacao"), 
                        Transacao(id=2,
                                  valor=32, 
                                  tipo="d", 
                                  descricao="Uma transacao")]),
    Cliente(id=3, 
            nome="Gugu Liberato", 
            valor_na_conta=0, 
            transacoes=[])
]

transaction_id_counter = 0

def criar_transacao_func(id_cliente: int, transacao: Transacao):
    global transaction_id_counter  # Indica que vamos acessar o contador global

    for cliente in clientes:
        if cliente.id == id_cliente:
            # Incrementa o contador de ID de transação e atribui ao atributo id da transação
            transaction_id_counter += 1
            transacao.id = transaction_id_counter
            cliente.transacoes.append(transacao)
            return transacao

    raise HTTPException(status_code=404, detail="Cliente não encontrado")

def listar_transacoes_func(id_cliente: int):
    for cliente in clientes:
        if cliente.id == id_cliente:
            return cliente.transacoes
    raise HTTPException(status_code=404, detail="Cliente não encontrado")

def obter_transacao_func(id_cliente: int, transacao_id: int): 
    for cliente in clientes:
        if cliente.id == id_cliente: 
            for transacao in cliente.transacoes:
                if transacao.id == transacao_id:
                    return transacao
    raise HTTPException(status_code=404, detail="Transação não encontrada")

def atualizar_transacao_func(id_cliente: int, transacao_id: int, transacao_atualizada: AtualizarTransacao):
    for cliente in clientes:
        if cliente.id == id_cliente:
            for transacao in cliente.transacoes:
                if transacao.id == transacao_id:
                    transacao.valor = transacao_atualizada.valor
                    transacao.tipo = transacao_atualizada.tipo
                    transacao.descricao = transacao_atualizada.descricao
                    return transacao
    raise HTTPException(status_code=404, detail="Transação não encontrada")

    
def deletar_transacao_func(id_cliente: int, transacao_id: int):
    for cliente in clientes:
        if cliente.id == id_cliente:
            for index, transacao in enumerate(cliente.transacoes):
                if transacao.id == transacao_id:
                    del cliente.transacoes[index]
                    return {"msg": "Transação excluida com sucesso"}
    raise HTTPException(status_code=404, detail="Transação não encontrada")

def obter_cliente_func(id_cliente: int):
    for cliente in clientes:
        if cliente.id == id_cliente:
            return cliente
    raise HTTPException(status_code=404, detail="Cliente não encontrado")