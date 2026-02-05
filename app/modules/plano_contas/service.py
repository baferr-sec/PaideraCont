from typing import List, Optional
from .model import Conta
from .schema import ContaCreate, natureza_por_tipo

_CONTAS: List[Conta] = []
_NEXT_ID = 1

def listar_contas() -> List[Conta]:
    return sorted(_CONTAS, key=lambda c: c.codigo)

def obter_por_codigo(codigo: str) -> Optional[Conta]:
    for c in _CONTAS:
        if c.codigo == codigo:
            return c
    return None

def criar_conta(data: ContaCreate) -> Conta:
    global _NEXT_ID

    if obter_por_codigo(data.codigo):
        raise ValueError("Já existe uma conta com esse código.")

    # Se tiver pai, precisa existir
    if data.conta_pai_codigo:
        pai = obter_por_codigo(data.conta_pai_codigo)
        if not pai:
            raise ValueError("Conta pai não encontrada (conta_pai_codigo inválido).")
        # Boa prática: pai normalmente não deveria aceitar lançamento
        if pai.aceita_lancamento:
            raise ValueError("Conta pai não pode aceitar lançamento (marque aceita_lancamento=false no pai).")

    # Natureza: se não vier, define pelo tipo
    natureza = data.natureza or natureza_por_tipo(data.tipo)

    # Regra: GRUPO não aceita lançamento
    if data.tipo == "GRUPO" and data.aceita_lancamento:
        raise ValueError("Conta do tipo GRUPO não pode aceitar lançamento.")

    conta = Conta(
        id=_NEXT_ID,
        codigo=data.codigo,
        nome=data.nome,
        tipo=data.tipo,
        aceita_lancamento=data.aceita_lancamento,
        conta_pai_codigo=data.conta_pai_codigo,
        natureza=natureza,
        ativa=True,
    )
    _CONTAS.append(conta)
    _NEXT_ID += 1
    return conta
