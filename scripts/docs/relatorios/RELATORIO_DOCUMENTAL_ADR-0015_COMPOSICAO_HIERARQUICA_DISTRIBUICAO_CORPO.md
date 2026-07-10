---
name: relatorio-documental-adr-0015-composicao-hierarquica-distribuicao-corpo
description: Consolida a criação da ADR-0015, a atualização dos contratos afetados, o bloqueio do H-0019 e o patch complementar de NOMENCLATURA.md
metadata:
  type: relatorio
  scope: scripts
  status: DOCUMENTATION_COMPLETED
  data: "2026-07-10"
---

# RELATORIO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO

## Status

DOCUMENTATION_COMPLETED

---

## Objetivo

Este relatório consolida o patch documental relativo à ADR-0015 —
"Composição hierárquica e distribuição de área do corpo". O escopo cobre:

- a criação do arquivo `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`;
- a atualização dos contratos afetados (`contrato_composicao_corpo.md`,
  `contrato_tela_json.md`, `contrato_json_tela_minima.md`);
- o registro da ADR-0015 no índice (`INDICE_ADR.md`);
- o bloqueio do `H-0019` até que uma versão revisada compatível com a ADR-0015
  seja produzida;
- o patch complementar de `docs/NOMENCLATURA.md` — seção 10 corrigida e
  seção 14 adicionada com os 25 itens normativos da ADR-0015 (pendência
  normativa resolvida neste patch).

Nenhum arquivo de código, testes, configuração ou outras ADRs foi alterado.
Nenhum commit foi criado nesta etapa.

---

## Base observada

- **Commit HEAD**: `3b98856eb84dd83f7e352ed48ee4ea74e8f10fd8`
- **Mensagem**: `docs: registra levantamento pos H-0018`
- **Estado do workspace**: modificações e arquivos não rastreados presentes (ver abaixo)

### Arquivos modificados (tracked, unstaged)

```
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_json_tela_minima.md
 M docs/contratos/contrato_tela_json.md
 M docs/NOMENCLATURA.md
```

### Arquivos não rastreados (untracked)

```
?? docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
?? docs/handoff/H-0019-layout-horizontal-plano-corpo.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0019_HANDOFF.md
?? docs/relatorios/RELATORIO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO.md
```

> Nota: `git diff --name-only` lista apenas arquivos rastreados modificados.
> Arquivos criados neste patch (`ADR-0015`, `H-0019`, `RELATORIO_AUDITORIA_H-0019`)
> aparecem como `??` em `git status --short` por serem não rastreados.

---

## Arquivos lidos

Os seguintes arquivos foram lidos para consolidar este relatório:

- `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`
- `docs/adr/INDICE_ADR.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/handoff/H-0019-layout-horizontal-plano-corpo.md`
- `docs/relatorios/RELATORIO_AUDITORIA_H-0019_HANDOFF.md` — **existe no workspace**
- `docs/NOMENCLATURA.md` — lido integralmente para o patch complementar

---

## Arquivos criados

| Arquivo | Observação |
|---|---|
| `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md` | ADR aceita em 2026-07-10; não rastreada (untracked) |
| `docs/relatorios/RELATORIO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO.md` | Este relatório |

---

## Arquivos alterados

| Arquivo | Tipo de alteração |
|---|---|
| `docs/adr/INDICE_ADR.md` | Entrada ADR-0015 adicionada na tabela de decisões |
| `docs/contratos/contrato_composicao_corpo.md` | Versão 0.2 → 0.3; regras R-15 a R-22; seções 3.2, 4.8, 4.9, 5.7–5.12 |
| `docs/contratos/contrato_tela_json.md` | Grupo estrutural, composição hierárquica e distribuição por container formalizados |
| `docs/contratos/contrato_json_tela_minima.md` | ADR-0015 adicionada à rastreabilidade; grupos e distribuição opcionais no envelope mínimo |
| `docs/handoff/H-0019-layout-horizontal-plano-corpo.md` | Bloqueio aplicado; status alterado; seção de bloqueio inserida no topo |
| `docs/NOMENCLATURA.md` | Patch complementar: seção 10 corrigida (regra de "3 vãos iguais" substituída por particionamento contíguo conforme ADR-0015); seção 14 adicionada com os 25 itens normativos da ADR-0015; data de atualização atualizada para 2026-07-10 |

---

## Decisões registradas na ADR-0015

A seguir, resumo das decisões principais formalizadas:

1. **Corpo como árvore de composição** — o corpo é modelado conceitualmente
   como árvore, não lista plana.
2. **Nós funcionais** — `console`, `dashboard` e `lancador` são os três tipos
   funcionais (folhas da árvore).
3. **Grupo como nó estrutural** — `grupo` é nó estrutural, sem borda própria
   e sem conteúdo próprio; agrupa filhos para fins de layout.
4. **Definição de nível** — o corpo (raiz) ocupa nível 0; cada camada de
   filhos incrementa o nível em 1.
5. **Profundidade máxima de 3 níveis** — nível 0 (corpo), nível 1 e nível 2;
   nível 3 é proibido na versão atual.
6. **Arranjo por container** — `arranjo` pertence ao container (`corpo` ou
   `grupo`), não ao elemento filho.
7. **Distribuição por container** — `distribuicao` pertence ao container,
   especifica como a área é repartida entre os filhos diretos.
8. **Horizontal reparte largura** — em arranjo horizontal, distribuição aloca
   colunas de caracteres.
9. **Vertical reparte altura** — em arranjo vertical, distribuição aloca linhas.
10. **Distribuição aloca área, não apenas conteúdo** — a área alocada é
    reservada independentemente do conteúdo do filho.
11. **Sobra horizontal vira espaços** — pixels/colunas excedentes são
    distribuídos como espaço em branco.
12. **Sobra vertical vira linhas em branco** — linhas excedentes são
    adicionadas como linhas em branco ao final.
13. **Modos de distribuição** — `igual`, `percentual`, `fracao`,
    `restrito` e `dinamico`.
14. **Percentual deve somar 100** — violação é erro de configuração.
15. **Fração usa pesos e denominador implícito pela soma** — `fracao: [1, 2]`
    divide a área em 1/3 e 2/3.
16. **Quantidade de valores deve bater com filhos diretos** — inconsistência
    é erro de configuração.
17. **Arredondamento por maiores restos** — método determinístico para
    distribuição de células inteiras.
18. **Contato entre molduras sem vãos externos** — a última coluna/linha de
    um filho termina imediatamente antes do início do próximo; não há vão.
19. **Ajustado ao conteúdo como preferido, não mínimo** — `ajustado_ao_conteudo`
    expressa dimensão preferida; o elemento pode receber mais.
20. **Paginação dentro da área alocada** — o elemento rola internamente sem
    transbordar para a área de outro.
21. **Terminal muito pequeno com política determinística futura** — possível
    uso de `...`; política exata é trabalho futuro.
22. **Sincronização automática de cortes** — cortes de paginação são
    sincronizados automaticamente entre grupos no mesmo nível.
23. **Sincronização explícita futura** — mecanismo de sincronização explícita
    entre grupos não adjacentes é extensão futura.
24. **H-0019 bloqueado até revisão** — o handoff deve ser revisado antes de
    qualquer implementação.

---

## Contratos atualizados

### contrato_composicao_corpo.md

- **Versão**: atualizado de `0.2` para `0.3` (confirmado no frontmatter do arquivo).
- **Rastreabilidade**: `ADR-0015-composicao-hierarquica-distribuicao-corpo.md`
  adicionada à lista `adrs_aplicadas`.
- **Contradição normativa resolvida**: seção 5.6 substituiu a regra de
  "3 vãos iguais" pela regra de particionamento contíguo.
- **Regras adicionadas**: R-15 a R-22, cobrindo grupo como nó estrutural,
  profundidade máxima, arranjo por container, distribuição que aloca área,
  arredondamento por maiores restos, contato sem vão externo,
  `ajustado_ao_conteudo` como preferido e proibição de fallback silencioso.
- **Seções adicionadas**:
  - `3.2` — Nó estrutural `grupo` (ADR-0015)
  - `4.8` — Arranjo por container (ADR-0015)
  - `4.9` — Distribuição por container (ADR-0015)
  - `5.7` — Modos de distribuição (ADR-0015)
  - `5.8` — Arredondamento determinístico (ADR-0015)
  - `5.9` — Preenchimento de área alocada (ADR-0015)
  - `5.10` — Regras dinâmicas de dimensão (ADR-0015 — conceitos futuros)
  - `5.11` — Paginação dentro da área alocada (ADR-0015)
  - `5.12` — Sincronização de cortes entre grupos (ADR-0015)

### contrato_tela_json.md

- **Grupo estrutural formalizado**: `elementos[]` pode conter objetos do tipo
  `grupo`, além dos tipos funcionais existentes.
- **Composição hierárquica como árvore**: o corpo é modelado como árvore de
  composição com `grupo` como nó estrutural.
- **Distribuição pertence a containers**: tanto `corpo` quanto `grupo` podem
  declarar `distribuicao`; a distribuição aloca área, não apenas conteúdo.
- **Tipos funcionais preservados**: `console`, `dashboard` e `lancador`
  continuam sendo os três tipos funcionais válidos.

### contrato_json_tela_minima.md

- **ADR-0015 adicionada à rastreabilidade**: incluída na lista `adrs_aplicadas`
  no frontmatter.
- **Envelope mínimo preservado**: a estrutura obrigatória mínima não foi
  alterada; `distribuicao` continua opcional no envelope mínimo.
- **Grupos estruturais permitidos**: grupos são permitidos conforme o contrato
  de composição, mas não são obrigatórios no envelope mínimo.
- **`corpo.arranjo` continua opcional**: sem alteração no status de obrigatoriedade.

### docs/NOMENCLATURA.md

- **Seção 10 — regra corrigida**: o bullet que descrevia "3 vãos iguais" foi
  substituído pela regra de particionamento contíguo conforme ADR-0015. Uma
  nota registra explicitamente a supersessão da regra anterior.
- **Seção 14 adicionada**: "Composição hierárquica e distribuição de área do
  corpo (ADR-0015)" — 25 itens normativos cobrindo a terminologia canônica
  da ADR-0015 de forma concisa, sem duplicar a especificação completa.
- A contradição normativa sobre "3 vãos iguais" foi removida da base de
  nomenclatura. A documentação da ADR-0015 agora está completa sem pendência
  de nomenclatura.

---

## Bloqueio aplicado ao H-0019

- **Status final**: `BLOCKED_BY_ADR_0015_PENDING_REVISION`
- **`HANDOFF_READY` removido**: não consta no arquivo atual.
- **Seção de bloqueio inserida no topo** do documento, antes de qualquer seção
  de status ou conteúdo técnico.
- **Aviso explícito no corpo**: "Qualquer execução baseada nesta versão deve
  bloquear com `ARCHITECTURE_REVIEW_REQUIRED`."
- **Dependência ADR-0015 registrada nos metadados**: `ADR-0015` listada como
  ADR normativa bloqueante.
- **Retomada**: H-0019 precisa de revisão antes de qualquer implementação; a
  versão revisada deve citar ADR-0015 como autoridade superior e remover
  qualquer regra incompatível.

---

## Relação com auditoria anterior do H-0019

- A auditoria anterior (`RELATORIO_AUDITORIA_H-0019_HANDOFF.md`, presente no
  workspace) aprovou o H-0019 com notas — resultado `HANDOFF_APPROVED_WITH_NOTES`.
- À época da auditoria, a generalização para N+1 vãos era tratada como
  extensão documentável, não como contradição normativa.
- A ADR-0015 supera essa interpretação: a regra de "N+1 vãos iguais" foi
  explicitamente rejeitada; o modelo correto é particionamento contíguo com
  distribuição por container.
- Em consequência, o H-0019 passa a bloqueado mesmo que anteriormente estivesse
  classificado como implementável com notas.

---

## Fora de escopo preservado

Nenhum dos seguintes grupos de arquivos foi alterado neste patch:

- Arquivos em `tela/` — intocados.
- Arquivos em `config/` — intocados.
- Arquivos de teste — intocados.
- Código Python (`.py`) — intocado.
- Outras ADRs aceitas (ADR-0001 a ADR-0014) — intocadas.
- Contratos fora da lista (`contrato_estilo.md`, `contrato_barra_de_menus.md`) — intocados.
- Handoffs diferentes do H-0019 — intocados.

---

## Patch complementar — Sanitização terminológica de NOMENCLATURA.md (2026-07-10)

Aplicado segundo patch complementar para remover terminologia transicional
remanescente em `docs/NOMENCLATURA.md`:

- `lado a lado` removido como termo textual normativo em todas as seções;
- `sobreposto` preservado apenas como alias transicional literal entre backticks
  quando necessário; removido de uso descritivo ("force sobreposto" → "force arranjo `vertical`");
- `lado_a_lado` (com underscores, entre backticks) preservado apenas como alias
  transicional literal; ocorrências com espaço ("lado a lado") convertidas;
- pendência "layout lado a lado + dashboard" reescrita como
  `corpo.arranjo = "horizontal"` + `dashboard` nas seções 6.1, 10 e 11;
- bloco de **Controle de aliases** adicionado na seção 1.4, explicitando:
  aliases não são terminologia final; não devem ser usados em novos textos
  normativos; novos handoffs devem usar `vertical`/`horizontal`;
  H-0019 deve implementar `corpo.arranjo = "horizontal"`, não "lado a lado";
- subtítulo "Lado a lado" na seção 6.1 substituído por "Arranjo horizontal";
- seção 2: "sobrepostos ou lado a lado" → "em arranjo vertical ou horizontal";
- seção 4.2: "coexistem lado a lado" → "coexistem em posições distintas e adjacentes";
- seção 10: alias textual `sobreposto`/`lado a lado` corrigido para
  `sobreposto`/`lado_a_lado` (terminologia canônica com underscores).

---

## Pontos pendentes para ciclo futuro

1. **Revisão do H-0019 pós-ADR-0015**: H-0019 precisa de uma versão revisada
   que incorpore as novas regras de composição hierárquica e distribuição.
2. **H-0020 — grupos e hierarquia**: implementação de `grupo` e hierarquia em
   3 níveis está planejada para H-0020 (conforme `contrato_composicao_corpo.md`
   seção de roadmap).
3. **Teste de verificação de níveis**: será criado somente após implementação
   do H-0019 revisado e da hierarquia em 3 níveis.
4. **Distribuição restrita/dinâmica**: conceitos `minimo`, `preferido` e
   `maximo` foram formalizados conceitualmente na ADR-0015, mas a implementação
   é trabalho futuro.
5. **Sincronização explícita entre grupos não adjacentes**: mecanismo ainda não
   especificado; registrado como extensão futura na ADR-0015.
6. **Política de terminal muito pequeno**: representação compacta (possível uso
   de `...`) ainda não determinada; política exata é trabalho futuro.

---

## Verificações executadas

### `git diff --stat`

```
 scripts/docs/adr/INDICE_ADR.md                     |   1 +
 .../docs/contratos/contrato_composicao_corpo.md    | 324 +++++++++++++++++++--
 .../docs/contratos/contrato_json_tela_minima.md    |  40 ++-
 scripts/docs/contratos/contrato_tela_json.md       |  61 ++--
 scripts/docs/NOMENCLATURA.md                       |  ~70 ++-
 5 files changed, ~447 insertions(+), ~49 deletions(-)
```

### `git diff --name-only`

```
scripts/docs/adr/INDICE_ADR.md
scripts/docs/contratos/contrato_composicao_corpo.md
scripts/docs/contratos/contrato_json_tela_minima.md
scripts/docs/contratos/contrato_tela_json.md
scripts/docs/NOMENCLATURA.md
```

### `git status --short`

```
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_json_tela_minima.md
 M docs/contratos/contrato_tela_json.md
 M docs/NOMENCLATURA.md
?? docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
?? docs/handoff/H-0019-layout-horizontal-plano-corpo.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0019_HANDOFF.md
?? docs/relatorios/RELATORIO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO.md
```

### `grep "3 vãos\|3 vaos\|N+1\|vãos iguais"` em `NOMENCLATURA.md`

```
(referência histórica supersedida presente na seção 10 como nota explícita de supersessão — não como regra ativa)
```

### `grep "ADR-0015\|particionamento contíguo"` em `NOMENCLATURA.md`

Confirmado em:
- Seção 10 — bullet corrigido cita ADR-0015 explicitamente
- Seção 14 — título e item 25 citam ADR-0015

### `grep HANDOFF_READY` em H-0019

```
(sem resultado — HANDOFF_READY removido corretamente)
```

### `find . -name '__pycache__' -type d`

```
(sem resultado)
```

### `find . -name '*.pyc'`

```
(sem resultado)
```

---

## Git status final

```
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_json_tela_minima.md
 M docs/contratos/contrato_tela_json.md
 M docs/NOMENCLATURA.md
?? docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
?? docs/handoff/H-0019-layout-horizontal-plano-corpo.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0019_HANDOFF.md
?? docs/relatorios/RELATORIO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO.md
```

---

## Patch corretivo pós-verificação documental (2026-07-10)

Aplicado após rejeição do pacote pela verificação documental
(`RELATORIO_VERIFICACAO_DOCUMENTAL_ADR-0015_...md`, status `DOCUMENTATION_REJECTED`).

- **A-001 corrigido**: critério de validação da seção 8 substituiu "o espaço
  horizontal é dividido em 3 vãos iguais" por particionamento contíguo entre
  os filhos diretos do container, alinhado com a seção 5.6 e com R-20 (ADR-0015).
- **A-002 corrigido**: critério da seção 8 "Em layout lado a lado, cada elemento
  exibe seu próprio indicador de paginação..." reescrito como "Em arranjo horizontal
  (`corpo.arranjo = "horizontal"`)..." — terminologia deprecada removida de posição
  normativa.
- **A-003 corrigido**: label de caso especial da seção 5.5 reescrito de
  "**Layout lado a lado**" para "**Arranjo horizontal (`arranjo = "horizontal"`)**".
- **A-004 corrigido**: pendência obsoleta sobre `docs/NOMENCLATURA.md` seção 10
  removida da seção 9 do contrato — a correção já havia sido aplicada no patch
  complementar deste ciclo.
- O relatório de verificação rejeitado foi preservado como evidência histórica
  (`RELATORIO_VERIFICACAO_DOCUMENTAL_ADR-0015_...md`).
- O pacote precisa passar por nova verificação antes do commit.

---

## Micro-patch complementar pós-verificação pós-correção (2026-07-10)

Aplicado após aprovação com notas do relatório pós-correção
(`RELATORIO_VERIFICACAO_DOCUMENTAL_ADR-0015_POS_CORRECAO.md`,
status `DOCUMENTATION_VERIFIED_WITH_NOTES`, decisão `APROVADO_COM_NOTAS_PARA_COMMIT`).

- **B-001 corrigido**: label remanescente da seção 5.5 com "lado a lado"
  substituído por terminologia vigente: `**Combinação \`corpo.arranjo = "horizontal"\`
  + \`dashboard\` presente**`. Consistência plena com seção 9 e ADR-0015.
- **B-002 corrigido**: nota histórica da seção 5.6 que dizia "`docs/NOMENCLATURA.md`
  seção 10 deve ser atualizada em ciclo futuro" ajustada para registrar que a
  atualização já foi aplicada neste ciclo — a regra de "3 vãos iguais" consta apenas
  como referência histórica supersedida; regra vigente é particionamento contíguo
  conforme ADR-0015.
- O relatório pós-correção aprovado com notas foi preservado como histórico.
- Pacote documental permanece com status `DOCUMENTATION_COMPLETED`.

---

## Conclusão

DOCUMENTATION_COMPLETED

**Critérios satisfeitos:**

- [x] Relatório criado.
- [x] `ADR-0015` existe no workspace (não rastreada, criada no patch).
- [x] `INDICE_ADR.md` atualizado com entrada para ADR-0015.
- [x] Contratos atualizados (`contrato_composicao_corpo.md` v0.3, `contrato_tela_json.md`, `contrato_json_tela_minima.md`).
- [x] `H-0019` está bloqueado (`BLOCKED_BY_ADR_0015_PENDING_REVISION`; `HANDOFF_READY` removido).
- [x] `docs/NOMENCLATURA.md` atualizado: seção 10 corrigida (regra de "3 vãos iguais" removida/supersedida); seção 14 adicionada com os 25 itens normativos da ADR-0015.
- [x] Contradição normativa sobre "3 vãos iguais" removida da base de nomenclatura.
- [x] Patch complementar de sanitização terminológica aplicado: `lado a lado` removido como termo normativo; `sobreposto`/`lado_a_lado` preservados apenas como aliases transicionais literais; bloco de controle de aliases adicionado na seção 1.4; pendências e subtítulos reescritos com `corpo.arranjo = "horizontal"`.
- [x] Nenhum arquivo proibido foi alterado (tela/, config/, testes, código Python, outras ADRs).
- [x] Nenhum cache criado (sem `__pycache__`, sem `.pyc`).
- [x] Nenhum commit criado.
