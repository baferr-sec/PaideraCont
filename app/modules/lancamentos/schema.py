from pydantic import BaseModel, Field
from typing import Literal
from datetime import date

TipoDC = Literal["D", "C"]

class LancamentoCreate(BaseModel):
    data: date = Field(..., examples=["2026-02-01"])
    conta_debito: str = Field(..., examples=["1.1.1"])
    conta_credito: str = Field(..., examples=["3.1"])
    valor: float = Field(..., gt=0, examples=[1000.00])
    historico: str = Field(..., examples=["Integralização de capital"])

class LancamentoOut(BaseModel):
    id: int
    data: date
    conta_debito: str
    conta_credito: str
    valor: float
    historico: str
