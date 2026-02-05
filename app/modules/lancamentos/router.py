from fastapi import APIRouter, HTTPException
from typing import List
from datetime import date

from .schema import LancamentoCreate, LancamentoOut
from . import service
from app.modules.lancamentos.encerramento import gerar_lancamentos_encerramento


router = APIRouter()

# =========================================================
# LANÇAMENTOS CONTÁBEIS (DIÁRIO)
# =========================================================

@router.get("/", response_model=List[LancamentoOut])
def listar():
    """
    Lista todos os lançamentos contábeis (Diário).
    """
    return [LancamentoOut(**l.__dict__) for l in service.listar_lancamentos()]


@router.post("/", response_model=LancamentoOut, status_code=201)
def criar(lanc: LancamentoCreate):
    """
    Cria um lançamento contábil.
    """
    try:
        l = service.criar_lancamento(lanc)
        return LancamentoOut(**l.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# =========================================================
# ENCERRAMENTO DO RESULTADO
# =========================================================

@router.get("/encerramento/preview")
def preview_encerramento(data: date):
    """
    Simula os lançamentos de encerramento do resultado.
    NÃO grava nada.
    """
    try:
        lancamentos = gerar_lancamentos_encerramento(data)
        return {
            "modo": "preview",
            "data_encerramento": data,
            "quantidade_lancamentos": len(lancamentos),
            "lancamentos": lancamentos,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/encerramento/confirmar")
def confirmar_encerramento(data: date):
    """
    Executa os lançamentos de encerramento do resultado.
    """
    try:
        lancamentos = gerar_lancamentos_encerramento(data)

        executados = []
        for lanc in lancamentos:
            executados.append(service.criar_lancamento(lanc))

        return {
            "modo": "confirmado",
            "data_encerramento": data,
            "quantidade_lancamentos": len(executados),
            "lancamentos": executados,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
