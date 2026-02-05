from collections import defaultdict
from typing import Dict, Any, DefaultDict, List

from app.modules.lancamentos import service as lanc_service
from app.modules.plano_contas import service as contas_service


def gerar_razao() -> List[Dict[str, Any]]:
    # Cada item do razão terá sempre número em debito/credito/saldo
    def novo_item():
        return {
            "conta": "",
            "nome": "",
            "natureza": "",
            "debito": 0.0,
            "credito": 0.0,
            "saldo": 0.0,
        }

    razao: DefaultDict[str, Dict[str, Any]] = defaultdict(novo_item)

    contas = {c.codigo: c for c in contas_service.listar_contas()}

    for lanc in lanc_service.listar_lancamentos():
        # Débito
        item_d = razao[lanc.conta_debito]
        item_d["conta"] = lanc.conta_debito
        item_d["nome"] = contas[lanc.conta_debito].nome
        item_d["natureza"] = contas[lanc.conta_debito].natureza
        item_d["debito"] = float(item_d["debito"]) + float(lanc.valor)

        # Crédito
        item_c = razao[lanc.conta_credito]
        item_c["conta"] = lanc.conta_credito
        item_c["nome"] = contas[lanc.conta_credito].nome
        item_c["natureza"] = contas[lanc.conta_credito].natureza
        item_c["credito"] = float(item_c["credito"]) + float(lanc.valor)

    # Calcular saldo conforme natureza
    for item in razao.values():
        deb = float(item["debito"])
        cred = float(item["credito"])

        if item["natureza"] == "D":
            item["saldo"] = deb - cred
        else:
            item["saldo"] = cred - deb

    return list(razao.values())
