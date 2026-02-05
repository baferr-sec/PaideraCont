from dataclasses import dataclass
from typing import Optional

@dataclass
class Conta:
    id: int
    codigo: str
    nome: str
    tipo: str
    aceita_lancamento: bool
    conta_pai_codigo: Optional[str] = None
    natureza: str = "D"
    ativa: bool = True
