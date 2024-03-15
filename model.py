from pydantic import BaseModel
from typing import Optional, List

class Transacao(BaseModel):
    id: int
    valor: float
    tipo: str
    descricao: Optional[str] = None

class Cliente(BaseModel):
    id: int
    nome: str
    valor_na_conta: float
    transacoes: List[Transacao] = []

class AtualizarTransacao(BaseModel):
    valor: float
    tipo: str
    descricao: Optional[str] = None