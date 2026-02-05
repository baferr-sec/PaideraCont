from fastapi import FastAPI

# Módulo: Plano de Contas
from app.modules.plano_contas.router import router as plano_contas_router

# Módulo: Lançamentos Contábeis
from app.modules.lancamentos.router import router as lancamentos_router

# Módulo: Relatórios (Razão e Balancete)
from app.modules.relatorios.router import router as relatorios_router


app = FastAPI(
    title="PaideraCont",
    description="Sistema contábil e financeiro alinhado aos CPCs",
    version="0.1.0",
)

# -------------------------
# Rota raiz (status do sistema)
# -------------------------
@app.get("/")
def root():
    return {
        "sistema": "PaideraCont",
        "status": "Sistema em manutenção 🚧",
        "modulos": [
            "Plano de Contas",
            "Lançamentos Contábeis",
            "Razão",
            "Balancete",
        ],
    }

# -------------------------
# Registro das rotas
# -------------------------
app.include_router(
    plano_contas_router,
    prefix="/plano-contas",
    tags=["Plano de Contas"],
)

app.include_router(
    lancamentos_router,
    prefix="/lancamentos",
    tags=["Lançamentos"],
)

app.include_router(
    relatorios_router,
    prefix="/relatorios",
    tags=["Relatórios"],
)
