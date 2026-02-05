from typing import Dict, Any, List

from app.modules.relatorios.razao import gerar_razao
from app.modules.plano_contas import service as contas_service


def gerar_balanco_patrimonial() -> Dict[str, Any]:
    """
    Balanço Patrimonial automático (CPC 26)
    """

    razao = gerar_razao()
    contas = {c.codigo: c for c in contas_service.listar_contas()}

    ativo: List[Dict[str, Any]] = []
    passivo: List[Dict[str, Any]] = []
    patrimonio_liquido: List[Dict[str, Any]] = []

    total_ativo = 0.0
    total_passivo = 0.0
    total_pl = 0.0

    for item in razao:
        codigo = item["conta"]
        saldo = float(item["saldo"])

        if codigo not in contas:
            continue

        tipo = contas[codigo].tipo

        linha = {
            "codigo": codigo,
            "nome": contas[codigo].nome,
            "saldo": round(saldo, 2),
        }

        if tipo == "ATIVO":
            ativo.append(linha)
            total_ativo += saldo

        elif tipo == "PASSIVO":
            passivo.append(linha)
            total_passivo += saldo

        elif tipo == "PL":
            patrimonio_liquido.append(linha)
            total_pl += saldo

    return {
        "demonstracao": "Balanço Patrimonial (CPC 26)",
        "ativo": {
            "contas": ativo,
            "total": round(total_ativo, 2),
        },
        "passivo": {
            "contas": passivo,
            "total": round(total_passivo, 2),
        },
        "patrimonio_liquido": {
            "contas": patrimonio_liquido,
            "total": round(total_pl, 2),
        },
        "equilibrio": round(total_ativo - (total_passivo + total_pl), 2),
    }
