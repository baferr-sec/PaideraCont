from fastapi import APIRouter

# Relatórios básicos
from app.modules.relatorios.razao import gerar_razao
from app.modules.relatorios.balancete import gerar_balancete

# Demonstrações financeiras
from app.modules.relatorios.dre import gerar_dre_completa
from app.modules.relatorios.dfc import gerar_dfc_indireta
from app.modules.relatorios.balanco import gerar_balanco_patrimonial


router = APIRouter()

# -------------------------
# RAZÃO CONTÁBIL
# -------------------------
@router.get("/razao")
def razao():
    return gerar_razao()

# -------------------------
# BALANCETE
# -------------------------
@router.get("/balancete")
def balancete():
    return gerar_balancete()

# -------------------------
# DRE – CPC 26 (detalhada)
# -------------------------
@router.get("/dre")
def dre():
    return gerar_dre_completa()

# -------------------------
# DFC – CPC 03 (método indireto)
# -------------------------
@router.get("/dfc")
def dfc():
    return gerar_dfc_indireta()

# -------------------------
# BALANÇO PATRIMONIAL – CPC 26
# -------------------------
@router.get("/balanco")
def balanco():
    return gerar_balanco_patrimonial()