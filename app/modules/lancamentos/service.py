from typing import List
from .model import Lancamento
from .schema import LancamentoCreate
from app.modules.plano_contas import service as contas_service

_LANCAMENTOS: List[Lancamento] = []
_NEXT_ID = 1

def listar_lancamentos() -> List[Lancamento]:
    return _LANCAMENTOS

def criar_lancamento(data: LancamentoCreate) -> Lancamento:
    global _NEXT_ID

    conta_d = contas_service.obter_por_codigo(data.conta_debito)
    conta_c = contas_service.obter_por_codigo(data.conta_credito)

    if not conta_d or not conta_c:
        raise ValueError("Conta débito ou crédito não encontrada.")

    if not conta_d.aceita_lancamento:
        raise ValueError("Conta de débito não aceita lançamento.")

    if not conta_c.aceita_lancamento:
        raise ValueError("Conta de crédito não aceita lançamento.")

    # Natureza: débito precisa ser D e crédito precisa ser C
    if conta_d.natureza != "D":
        raise ValueError("Conta de débito não é de natureza devedora (D).")

    if conta_c.natureza != "C":
        raise ValueError("Conta de crédito não é de natureza credora (C).")

    lanc = Lancamento(
        id=_NEXT_ID,
        data=data.data,
        conta_debito=data.conta_debito,
        conta_credito=data.conta_credito,
        valor=data.valor,
        historico=data.historico,
    )

    _LANCAMENTOS.append(lanc)
    _NEXT_ID += 1
    return lanc
