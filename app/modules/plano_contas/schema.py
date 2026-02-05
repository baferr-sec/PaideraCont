from pydantic import BaseModel, Field
from typing import Optional, Literal

TipoConta = Literal["GRUPO", "ATIVO", "PASSIVO", "PL", "RECEITA", "CUSTO", "DESPESA", "RESULTADO"]
Natureza = Literal["D", "C"]  # D=devedora | C=credora

def natureza_por_tipo(tipo: str) -> str:
    # Regra contábil padrão:
    # Ativo/Despesa/Custo -> natureza D
    # Passivo/PL/Receita/Resultado -> natureza C
    return "D" if tipo in {"ATIVO", "DESPESA", "CUSTO"} else "C"

class ContaCreate(BaseModel):
    codigo: str = Field(..., examples=["1.1.1"])
    nome: str = Field(..., examples=["Caixa"])
    tipo: TipoConta = Field(..., examples=["ATIVO"])
    aceita_lancamento: bool = Field(..., examples=[True])
    conta_pai_codigo: Optional[str] = Field(None, examples=["1.1"])
    natureza: Optional[Natureza] = Field(
        None,
        description="Se não informar, o sistema define pela regra padrão (tipo)."
    )

class ContaOut(BaseModel):
    id: int
    codigo: str
    nome: str
    tipo: str
    aceita_lancamento: bool
    conta_pai_codigo: Optional[str] = None
    natureza: str
    ativa: bool = True
