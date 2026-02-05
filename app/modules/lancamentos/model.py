from dataclasses import dataclass
from datetime import date

@dataclass
class Lancamento:
    id: int
    data: date
    conta_debito: str
    conta_credito: str
    valor: float
    historico: str

