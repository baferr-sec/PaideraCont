from fastapi import APIRouter, HTTPException
from typing import List

from .schema import ContaCreate, ContaOut
from . import service
from .seed import criar_plano_padrao

router = APIRouter()

# -------------------------
# Listar plano de contas
# -------------------------
@router.get("/", response_model=List[ContaOut])
def listar():
    contas = service.listar_contas()
    return [ContaOut(**c.__dict__) for c in contas]

# -------------------------
# Criar conta manual
# -------------------------
@router.post("/", response_model=ContaOut, status_code=201)
def criar(conta: ContaCreate):
    try:
        c = service.criar_conta(conta)
        return ContaOut(**c.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# -------------------------
# Criar plano padrão (SEED)
# -------------------------
@router.post("/seed")
def seed_plano_contas():
    contas = criar_plano_padrao()
    return {
        "message": "Plano de contas padrão criado",
        "quantidade_criada": len(contas)
    }

