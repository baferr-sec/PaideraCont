from typing import Dict, Any, List, Optional, Tuple

from app.modules.plano_contas import service as contas_service
from app.modules.relatorios.razao import gerar_razao


def _fmt_ref(refs: List[str]) -> str:
    """Formata referências como (4.1) ou (4.1, 4.2)."""
    if not refs:
        return ""
    return f"({', '.join(refs)})"


def _sum_por_prefixos(
    saldos_por_conta: Dict[str, float],
    prefixos: List[str]
) -> Tuple[float, List[str]]:
    """
    Soma saldos das contas cujos códigos começam com qualquer prefixo.
    Retorna (valor, lista de referências efetivamente encontradas).
    """
    total = 0.0
    refs_encontradas: List[str] = []

    for pref in prefixos:
        # soma todas as contas que começam com pref (ex: 4.1, 4.1.1, 4.1.2...)
        found = False
        for codigo, saldo in saldos_por_conta.items():
            if codigo.startswith(pref):
                total += float(saldo)
                found = True
        if found:
            refs_encontradas.append(pref)

    return total, refs_encontradas


def _line(descricao: str, valor: float, refs: List[str], estilo: str = "normal") -> Dict[str, Any]:
    """
    estilo: normal | subtotal | total
    """
    return {
        "descricao": descricao,
        "referencia": _fmt_ref(refs),
        "valor": round(float(valor), 2),
        "estilo": estilo,
    }


def gerar_dre_completa() -> Dict[str, Any]:
    """
    DRE detalhada (CPC 26) baseada no plano de contas + razão:
    - Receita Bruta
    - (-) Deduções/Impostos sobre vendas
    - (=) Receita Líquida
    - (-) CMV/CSP (Custos)
    - (=) Lucro Bruto
    - (-) Despesas Operacionais (adm/vendas/outras, conforme existirem)
    - (=) Resultado Operacional
    - (+/-) Resultado Financeiro (se houver contas)
    - (=) Resultado Antes dos Tributos
    - (-) IR/CSLL (se houver contas)
    - (=) Resultado Líquido do Exercício
    """

    # 1) Pegar saldos pelo razão (saldo já respeita natureza)
    razao = gerar_razao()
    saldos_por_conta = {item["conta"]: float(item["saldo"]) for item in razao}

    # 2) Carregar plano de contas (pra saber o que existe e permitir evoluir)
    contas = {c.codigo: c for c in contas_service.listar_contas()}

    # 3) Mapear grupos (prefixos/padrões)
    # Baseado no que você já definiu no seed:
    # 4.1 Receita Bruta de Vendas
    # 4.2 (-) Simples Nacional (dedução)
    # 5.1 CMV/CSP (custos)
    # 6.1 Despesas Administrativas
    #
    # E deixamos ganchos para crescer:
    # 4.3 Receitas financeiras (se você criar)
    # 6.2 Despesas com vendas (se você criar)
    # 6.3 Despesas financeiras (se você criar)
    # 6.9 Outras (se você criar)
    # 8.x IR/CSLL (se você criar um grupo futuro)
    receita_bruta, ref_rb = _sum_por_prefixos(saldos_por_conta, ["4.1"])
    deducoes, ref_ded = _sum_por_prefixos(saldos_por_conta, ["4.2"])

    custos, ref_cmv = _sum_por_prefixos(saldos_por_conta, ["5.1"])

    # Despesas operacionais (começa no 6.1, mas já abre portas)
    desp_adm, ref_adm = _sum_por_prefixos(saldos_por_conta, ["6.1"])
    desp_vendas, ref_vendas = _sum_por_prefixos(saldos_por_conta, ["6.2"])
    outras_desp_op, ref_outras_op = _sum_por_prefixos(saldos_por_conta, ["6.9"])

    # Resultado financeiro (opcional, se existir no seu plano)
    rec_fin, ref_rec_fin = _sum_por_prefixos(saldos_por_conta, ["4.3"])
    desp_fin, ref_desp_fin = _sum_por_prefixos(saldos_por_conta, ["6.3"])

    # Tributos sobre lucro (opcional — para Simples geralmente não se aplica assim, mas deixamos pronto)
    ir_csll, ref_ir = _sum_por_prefixos(saldos_por_conta, ["8.1", "8.2"])

    # 4) Montar subtotais (CPC 26)
    receita_liquida = receita_bruta - deducoes
    lucro_bruto = receita_liquida - custos

    despesas_operacionais = desp_adm + desp_vendas + outras_desp_op
    resultado_operacional = lucro_bruto - despesas_operacionais

    resultado_financeiro = rec_fin - desp_fin
    resultado_antes_tributos = resultado_operacional + resultado_financeiro

    resultado_liquido = resultado_antes_tributos - ir_csll

    # 5) Linhas detalhadas com referências (parênteses)
    linhas: List[Dict[str, Any]] = []

    linhas.append(_line("Receita Bruta de Vendas e/ou Serviços", receita_bruta, ref_rb))
    linhas.append(_line("(-) Deduções da Receita / Tributos sobre Vendas", deducoes, ref_ded))
    linhas.append(_line("Receita Líquida", receita_liquida, ref_rb + ref_ded, estilo="subtotal"))

    linhas.append(_line("(-) Custos dos Produtos/Serviços (CMV/CSP)", custos, ref_cmv))
    linhas.append(_line("Lucro Bruto", lucro_bruto, ref_rb + ref_ded + ref_cmv, estilo="subtotal"))

    # Detalhe de despesas operacionais (só inclui se existir algo > 0 ou se a conta existir no plano)
    def _existe_prefixo(prefixo: str) -> bool:
        return any(cod.startswith(prefixo) for cod in contas.keys())

    if _existe_prefixo("6.1") or desp_adm != 0:
        linhas.append(_line("(-) Despesas Administrativas", desp_adm, ref_adm))
    if _existe_prefixo("6.2") or desp_vendas != 0:
        linhas.append(_line("(-) Despesas com Vendas", desp_vendas, ref_vendas))
    if _existe_prefixo("6.9") or outras_desp_op != 0:
        linhas.append(_line("(-) Outras Despesas Operacionais", outras_desp_op, ref_outras_op))

    linhas.append(_line("Resultado Operacional", resultado_operacional, [], estilo="subtotal"))

    # Resultado financeiro (se houver contas criadas)
    if _existe_prefixo("4.3") or rec_fin != 0:
        linhas.append(_line("(+) Receitas Financeiras", rec_fin, ref_rec_fin))
    if _existe_prefixo("6.3") or desp_fin != 0:
        linhas.append(_line("(-) Despesas Financeiras", desp_fin, ref_desp_fin))

    if (_existe_prefixo("4.3") or _existe_prefixo("6.3")) or resultado_financeiro != 0:
        linhas.append(_line("Resultado Financeiro", resultado_financeiro, [], estilo="subtotal"))

    linhas.append(_line("Resultado Antes dos Tributos sobre o Lucro", resultado_antes_tributos, [], estilo="subtotal"))

    # Tributos sobre lucro (opcional)
    if _existe_prefixo("8.1") or _existe_prefixo("8.2") or ir_csll != 0:
        linhas.append(_line("(-) IRPJ e CSLL", ir_csll, ref_ir))

    linhas.append(_line("Resultado Líquido do Exercício", resultado_liquido, ["7"], estilo="total"))

    return {
        "demonstracao": "DRE (CPC 26) - detalhada",
        "linhas": linhas,
        "totais": {
            "receita_bruta": round(receita_bruta, 2),
            "deducoes": round(deducoes, 2),
            "receita_liquida": round(receita_liquida, 2),
            "custos": round(custos, 2),
            "lucro_bruto": round(lucro_bruto, 2),
            "despesas_operacionais": round(despesas_operacionais, 2),
            "resultado_operacional": round(resultado_operacional, 2),
            "resultado_financeiro": round(resultado_financeiro, 2),
            "resultado_antes_tributos": round(resultado_antes_tributos, 2),
            "ir_csll": round(ir_csll, 2),
            "resultado_liquido": round(resultado_liquido, 2),
        },
    }
