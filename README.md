# PaideraCont

Sistema contábil desenvolvido em Python com FastAPI, com foco em **correção contábil, governança e arquitetura de software**, e não apenas em interface visual.

Autor: Bruno Ferreira  
Data da última atualização: 06/02/2026

---

## 🎯 Objetivo do Projeto

Desenvolver um sistema contábil didático e tecnicamente sólido, alinhado a:

- Princípios Contábeis (CPC)
- IFRS
- Método das partidas dobradas
- Boas práticas de auditoria
- Arquitetura limpa e evolutiva

O projeto foi concebido desde o início para **não gerar retrabalho futuro**, servindo como base para evoluções como SPED, ECD e ambientes SaaS.

---

## 🧭 Visão Geral das Fases

### 🟦 FASE 0 — Decisões Estruturais (CONCLUÍDA)

Definições imutáveis do projeto:

- CPC / IFRS como base conceitual
- Ledger contábil como fonte única da verdade
- Ausência de deletes (somente estorno)
- UX subordinada à contabilidade
- Projeto versionado em GitHub

📌 **Status:** Encerrada definitivamente  
📌 **Impacto:** Evita refatorações estruturais futuras

---

### 🟩 FASE 1 — Núcleo Contábil Imutável (CONCLUÍDA)

Implementação do coração do sistema:

- Plano de Contas estruturado e hierárquico
- Contas analíticas vs. sintéticas
- Natureza D/C respeitada
- Períodos contábeis:
  - criação
  - fechamento
  - travamento total após fechamento
- Lotes:
  - numeração sequencial
  - tipos (manual, estorno, ajuste)
  - fechamento obrigatório e validado
- Lançamentos:
  - numeração sequencial imutável
  - vinculados a período e lote
  - sem delete
  - estorno como único caminho de correção

📌 **Status:** Encerrada  
📌 **Resultado:** Ledger confiável e auditável

---

### 🟨 FASE 2 — Relatórios Contábeis Governados (CONCLUÍDA ✅)

Nesta fase, o sistema passou a gerar **relatórios contábeis formais**, com regras claras de governança.

#### Relatórios implementados:
- Razão
- Balancete
- Balanço Patrimonial
- Demonstração do Resultado do Exercício (DRE)
- Demonstração do Fluxo de Caixa (DFC)
- Diário

#### Regras de governança aplicadas:
- Relatórios **OFICIAIS** só podem ser gerados para **períodos FECHADOS**
- Apenas **lotes FECHADOS** são considerados em relatórios oficiais
- Relatórios provisórios existem apenas para análise interna
- Nenhum relatório ignora regras de período, lote ou lançamento

Essas regras garantem:
- previsibilidade
- rastreabilidade
- aderência a práticas de auditoria
- coerência contábil real (não apenas técnica)

📌 **Status:** Fase oficialmente encerrada  
📌 **Observação:** A Fase 2 NÃO inclui SPED, TXT ou validação em PVA

---

### 🟥 FASE 3 — SPED / ECD (PLANEJADA)

Próxima fase prevista:

- Registro I050 / 0500 (Plano de Contas)
- Registro I200 / I250 (Lançamentos)
- Geração de TXT conforme layout oficial
- Preparação para validação em PVA

📌 **Status:** Ainda não iniciada  
📌 **Importante:** Só será iniciada após o fechamento formal da Fase 2 (concluído)

---

## 🛠️ Tecnologias Utilizadas

- Python
- FastAPI
- Estrutura modular por domínio
- Dados em memória (fase atual)
- Git / GitHub

---

## 📌 Considerações Finais

O PaideraCont não é um ERP comercial, mas um **projeto técnico sério**, voltado ao aprendizado profundo de:

- contabilidade aplicada
- governança de sistemas
- arquitetura de software contábil

Cada fase é encerrada formalmente antes da próxima, evitando atalhos e retrabalho.

---

🚀 Próximo passo: **início consciente da Fase 3 (SPED/ECD)**, quando decidido.
