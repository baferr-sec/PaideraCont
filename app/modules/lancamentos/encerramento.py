from typing import List
from datetime import date

from app.modules.relatorios.dre import gerar_dre_completa
from app.modules.relatorios.razao import gerar_razao
from app.modules.plano_contas import service as contas_service
from app.modules.lancamentos.schema import LancamentoCreate


def gerar_lancamentos_encerramento(data: date) -> List[LancamentoCreate]:
    """
    Gera (prévia) dos lançamentos de encerramento do resultado.
    Não executa automaticamente — apenas prepara.
    """

    razao = gerar_razao()
    contas = {c.codigo: c for c in contas_service.listar_contas()}

    lancamentos: List[LancamentoCreate] = []

    conta_resultado = "7"
    conta_pl = "3.5"

    # Encerrar contas de resultado (RECEITA/CUSTO/DESPESA)
    for item in razao:
        codigo = item["conta"]
        saldo = float(item["saldo"])

        if codigo not in contas:
            continue

        tipo = contas[codigo].tipo

        if tipo in {"RECEITA", "CUSTO", "DESPESA"} and saldo != 0:
            # Se saldo > 0: (dependendo da natureza) geramos o lançamento para zerar
            # Aqui usamos uma regra prática: zerar a conta contra "7"
            if saldo > 0:
                lancamentos.append(
                    LancamentoCreate(
                        data=data,
                        conta_debito=conta_resultado,
                        conta_credito=codigo,
                        valor=abs(saldo),
                        historico=f"Encerramento da conta {codigo}",
                    )
                )
            else:
                lancamentos.append(
                    LancamentoCreate(
                        data=data,
                        conta_debito=codigo,
                        conta_credito=conta_resultado,
                        valor=abs(saldo),
                        historico=f"Encerramento da conta {codigo}",
                    )
                )

    # Transferir Resultado Líquido para PL (3.5)
    dre = gerar_dre_completa()
    resultado = float(dre["totais"]["resultado_liquido"])

    if resultado != 0:
        if resultado > 0:
            # Lucro
            lancamentos.append(
                LancamentoCreate(
                    data=data,
                    conta_debito=conta_resultado,
                    conta_credito=conta_pl,
                    valor=resultado,
                    historico="Transferência do lucro para o PL (Lucros/Prejuízos Acumulados)",
                )
            )
        else:
            # Prejuízo
            lancamentos.append(
                LancamentoCreate(
                    data=data,
                    conta_debito=conta_pl,
                    conta_credito=conta_resultado,
                    valor=abs(resultado),
                    historico="Transferência do prejuízo para o PL (Lucros/Prejuízos Acumulados)",
                )
            )

    return lancamentos
