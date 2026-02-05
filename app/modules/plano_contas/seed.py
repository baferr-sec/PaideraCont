from .schema import ContaCreate
from . import service

PLANO_PADRAO = [
    # ===== ATIVO =====
    ContaCreate(codigo="1", nome="ATIVO", tipo="GRUPO", natureza="D", aceita_lancamento=False, conta_pai_codigo=None),

    ContaCreate(codigo="1.1", nome="Ativo Circulante", tipo="GRUPO", natureza="D", aceita_lancamento=False, conta_pai_codigo="1"),
    ContaCreate(codigo="1.1.1", nome="Caixa", tipo="ATIVO", natureza="D", aceita_lancamento=True, conta_pai_codigo="1.1"),
    ContaCreate(codigo="1.1.2", nome="Bancos Conta Movimento", tipo="ATIVO", natureza="D", aceita_lancamento=True, conta_pai_codigo="1.1"),
    ContaCreate(codigo="1.1.3", nome="Aplicações Financeiras", tipo="ATIVO", natureza="D", aceita_lancamento=True, conta_pai_codigo="1.1"),
    ContaCreate(codigo="1.1.4", nome="Clientes", tipo="ATIVO", natureza="D", aceita_lancamento=True, conta_pai_codigo="1.1"),
    ContaCreate(codigo="1.1.5", nome="(-) PCLD", tipo="ATIVO", natureza="C", aceita_lancamento=True, conta_pai_codigo="1.1"),
    ContaCreate(codigo="1.1.6", nome="Estoques", tipo="ATIVO", natureza="D", aceita_lancamento=True, conta_pai_codigo="1.1"),

    ContaCreate(codigo="1.2", nome="Ativo Não Circulante", tipo="GRUPO", natureza="D", aceita_lancamento=False, conta_pai_codigo="1"),
    ContaCreate(codigo="1.2.2", nome="Imobilizado", tipo="GRUPO", natureza="D", aceita_lancamento=False, conta_pai_codigo="1.2"),
    ContaCreate(codigo="1.2.2.1", nome="Máquinas e Equipamentos", tipo="ATIVO", natureza="D", aceita_lancamento=True, conta_pai_codigo="1.2.2"),
    ContaCreate(codigo="1.2.2.7", nome="(-) Depreciação Acumulada", tipo="ATIVO", natureza="C", aceita_lancamento=True, conta_pai_codigo="1.2.2"),

    # ===== PASSIVO =====
    ContaCreate(codigo="2", nome="PASSIVO", tipo="GRUPO", natureza="C", aceita_lancamento=False, conta_pai_codigo=None),

    ContaCreate(codigo="2.1", nome="Passivo Circulante", tipo="GRUPO", natureza="C", aceita_lancamento=False, conta_pai_codigo="2"),
    ContaCreate(codigo="2.1.1", nome="Fornecedores", tipo="PASSIVO", natureza="C", aceita_lancamento=True, conta_pai_codigo="2.1"),
    ContaCreate(codigo="2.1.2", nome="Tributos a Recolher", tipo="PASSIVO", natureza="C", aceita_lancamento=True, conta_pai_codigo="2.1"),
    ContaCreate(codigo="2.1.3", nome="Pró-labore a Pagar", tipo="PASSIVO", natureza="C", aceita_lancamento=True, conta_pai_codigo="2.1"),

    ContaCreate(codigo="2.2", nome="Passivo Não Circulante", tipo="GRUPO", natureza="C", aceita_lancamento=False, conta_pai_codigo="2"),

    # ===== PATRIMÔNIO LÍQUIDO =====
    ContaCreate(codigo="3", nome="Patrimônio Líquido", tipo="PL", natureza="C", aceita_lancamento=False, conta_pai_codigo=None),
    ContaCreate(codigo="3.1", nome="Capital Social", tipo="PL", natureza="C", aceita_lancamento=True, conta_pai_codigo="3"),
    ContaCreate(codigo="3.5", nome="Lucros ou Prejuízos Acumulados", tipo="PL", natureza="C", aceita_lancamento=True, conta_pai_codigo="3"),

    # ===== RESULTADO =====
    ContaCreate(codigo="4", nome="Receitas", tipo="GRUPO", natureza="C", aceita_lancamento=False, conta_pai_codigo=None),
    ContaCreate(codigo="4.1", nome="Receita Bruta de Vendas", tipo="RECEITA", natureza="C", aceita_lancamento=True, conta_pai_codigo="4"),
    ContaCreate(codigo="4.2", nome="(-) Simples Nacional", tipo="RECEITA", natureza="D", aceita_lancamento=True, conta_pai_codigo="4"),

    ContaCreate(codigo="5", nome="Custos", tipo="GRUPO", natureza="D", aceita_lancamento=False, conta_pai_codigo=None),
    ContaCreate(codigo="5.1", nome="CMV / CSP", tipo="CUSTO", natureza="D", aceita_lancamento=True, conta_pai_codigo="5"),

    ContaCreate(codigo="6", nome="Despesas", tipo="GRUPO", natureza="D", aceita_lancamento=False, conta_pai_codigo=None),
    ContaCreate(codigo="6.1", nome="Despesas Administrativas", tipo="DESPESA", natureza="D", aceita_lancamento=True, conta_pai_codigo="6"),

    ContaCreate(codigo="7", nome="Resultado do Exercício", tipo="RESULTADO", natureza="C", aceita_lancamento=True, conta_pai_codigo=None),
]

def criar_plano_padrao():
    criadas = []
    for conta in PLANO_PADRAO:
        try:
            criadas.append(service.criar_conta(conta))
        except ValueError:
            pass
    return criadas
