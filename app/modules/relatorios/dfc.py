from typing import Dict, Any, List

from app.modules.relatorios.dre import gerar_dre_completa
from app.modules.relatorios.razao import gerar_razao
from app.modules.plano_contas import service as contas_service


def _saldo_por_prefixo(razao: List[Dict[str, Any]], prefixo: str) -> float:
    total = 0.0
    for item in razao:
        if item["conta"].startswith(prefixo):
            total += float(item["saldo"])
    return total


def gerar_dfc_indireta() -> Dict[str, Any]:
    """
    DFC – Método Indireto (CPC 03 / IAS 7)
    Parte do Resultado do Exercício (DRE) e ajusta:
    - itens sem efeito caixa
    - variações do capital de giro
    """

    # 1) Resultado do exercício (DRE)
    dre = gerar_dre_completa()
    resultado = float(dre["totais"]["resultado_liquido"])

    # 2) Razão (saldos por conta)
    razao = gerar_razao()
    contas = {c.codigo: c for c in contas_service.listar_contas()}

    # 3) Ajustes sem efeito caixa
    # Depreciação acumulada (ex.: 1.2.2.7)
    depreciacao = _saldo_por_prefixo(razao, "1.2.2.7")

    # Provisões (ex.: PCLD 1.1.5)
    provisoes = _saldo_por_prefixo(razao, "1.1.5")

    ajustes_sem_caixa = depreciacao + provisoes

    # 4) Variação do capital de giro
    # Convenção:
    # - Aumento de ativo operacional = (-) caixa
    # - Aumento de passivo operacional = (+) caixa

    clientes = _saldo_por_prefixo(razao, "1.1.4")        # Clientes
    estoques = _saldo_por_prefixo(razao, "1.1.6")        # Estoques
    fornecedores = _saldo_por_prefixo(razao, "2.1.1")    # Fornecedores
    tributos = _saldo_por_prefixo(razao, "2.1.2")        # Tributos a recolher

    variacao_cg = (
        - clientes
        - estoques
        + fornecedores
        + tributos
    )

    # 5) Caixa das atividades operacionais
    caixa_operacional = resultado + ajustes_sem_caixa + variacao_cg

    return {
        "demonstracao": "DFC – Método Indireto (CPC 03)",
        "resultado_exercicio": round(resultado, 2),

        "ajustes_sem_efeito_caixa": {
            "depreciacao": round(depreciacao, 2),
            "provisoes": round(provisoes, 2),
            "total": round(ajustes_sem_caixa, 2),
        },

        "variacao_capital_giro": {
            "clientes": round(-clientes, 2),
            "estoques": round(-estoques, 2),
            "fornecedores": round(fornecedores, 2),
            "tributos": round(tributos, 2),
            "total": round(variacao_cg, 2),
        },

        "caixa_atividades_operacionais": round(caixa_operacional, 2),

        # ganchos para evoluir depois
        "caixa_atividades_investimento": 0.0,
        "caixa_atividades_financiamento": 0.0,

        "variacao_liquida_caixa": round(caixa_operacional, 2),
    }