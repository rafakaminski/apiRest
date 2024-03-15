from fastapi.testclient import TestClient
from endpoints import app

client = TestClient(app)

def test_criar_transacao_endpoint():
    response = client.post("/clientes/1/transacoes", json={"id": 3, "valor": 200, "tipo": "c", "descricao": "Teste de Transação"})
    assert response.status_code == 200
    assert response.json()["valor"] == 200
    assert response.json()["tipo"] == "c"
    assert response.json()["descricao"] == "Teste de Transação"

def test_listar_transacoes_endpoint():
    response = client.get("/clientes/1/transacoes")
    assert response.status_code == 200
    assert len(response.json()) > 0 

def test_atualizar_transacao_endpoint():
    response = client.put("/clientes/1/transacoes/1", json={"valor": 1500, "tipo": "d", "descricao": "Atualizada"})
    assert response.status_code == 200
    assert response.json()["descricao"] == "Atualizada"

def test_obter_transacao_endpoint():
    response = client.get("/clientes/1/transacoes/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_deletar_transacao_endpoint():
    response = client.delete("/clientes/1/transacoes/1")
    assert response.status_code == 200
    assert response.json() == {"msg": "Transação excluida com sucesso"}

def test_obter_cliente_endpoint():
    response = client.get("/clientes/1")
    assert response.status_code == 200
    assert response.json()["nome"] == "Silvio Santos"