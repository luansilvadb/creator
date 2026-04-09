# DIRETRIZES DE ESPECIFICAÇÃO EXAUSTIVA (Ω)

**OBJETIVO:** Eliminar 100% da ambiguidade. O Tech Lead deve ser um tradutor de lógica para código, nunca um tomador de decisão técnica sobre o "Como" sem base na spec.

---

## NÍVEL DE DETALHAMENTO: VERBOSIDADE DE LIVRO

### 1. CONTRATOS TÉCNICOS (Obrigatório)

- Definição de Tipos Estritos (Typescript/Rust/Go).
- Esquemas de Banco de Dados com índices e justificativas.
- Contratos de API com payloads de exemplo e todos os HTTP Status Codes possíveis.

### 2. FLUXO DE EXECUÇÃO (Obrigatório)

- Diagramas de Sequência em texto detalhando a jornada do dado.
- Diagramas de Estado para entidades complexas.
- Regras de Concorrência e Isolamento (Locks, Transações).

### 3. LÓGICA DE NEGÓCIO E EDGE CASES

- Mapeamento de todos os caminhos "Não-Felizes".
- Tratamento de nulos, timeouts e falhas de rede.
- BDD Exaustivo: Mínimo de 3 cenários por funcionalidade (Sucesso, Erro de Input, Erro de Sistema).

### 4. OBSERVABILIDADE POR DESIGN

- Definição exata de mensagens de Log.
- Métricas de sucesso da funcionalidade (ex: Latência de escrita < 100ms).

---

## REGRAS DE OURO DA SPEC Ω

- **Detalhamento Infinito:** Se há dúvida na implementação, a spec falhou.
- **Tradução Direta:** O código deve ser o espelho da Spec.
- **Vedações:** Proibido o uso de "A definir" ou "TBD". Se é TBD, é um BLOCKER que gera ADR.

---

[Ω] Especificações geradas sob estas diretrizes são imutáveis após commit na sprint.
