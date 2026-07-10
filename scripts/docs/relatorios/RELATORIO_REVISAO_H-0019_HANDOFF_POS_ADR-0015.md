---
name: relatorio-revisao-h-0019-handoff-pos-adr-0015
description: Revisão documental do handoff H-0019 após formalização e commit da ADR-0015 — registra mudanças conceituais, compatibilidade e decisões normativas
metadata:
  type: relatorio
  scope: scripts
  status: REVISAO_CONCLUIDA
  data: "2026-07-10"
---

# RELATORIO_REVISAO_H-0019_HANDOFF_POS_ADR-0015

## Status

```
REVISAO_CONCLUIDA
handoff_status: HANDOFF_REVISED_READY
```

---

## Base verificada

| Item | Valor |
|---|---|
| Commit HEAD no início da revisão | `9d4c74d  docs: formaliza composicao hierarquica do corpo` |
| Workspace no início | Limpo (`git status --short`: sem saída) |
| Commit esperado | `9d4c74d  docs: formaliza composicao hierarquica do corpo` |
| Workspace esperado | Limpo |
| Coincidência de base | SIM |

### git log --oneline -6 (início)

```
9d4c74d docs: formaliza composicao hierarquica do corpo
3b98856 docs: registra levantamento pos H-0018
46e0cb9 feat: cobre distribuicao da barra de menus
c8a20fa test: adiciona explorador da barra de menus
ab5ad68 feat: renderiza barra de menus horizontal responsiva
b2eb458 feat: ocupa altura do terminal pelo corpo
```

---

## Arquivos alterados

| Arquivo | Ação |
|---|---|
| `docs/handoff/H-0019-layout-horizontal-plano-corpo.md` | Modificado (revisão pós-ADR-0015) |
| `docs/relatorios/RELATORIO_REVISAO_H-0019_HANDOFF_POS_ADR-0015.md` | Criado (este relatório) |

Nenhum outro arquivo foi alterado.

---

## Motivo da revisão

O handoff H-0019 foi criado em 2026-07-09 com base no levantamento pós-H-0018
(commit `3b98856`). Foi auditado (`HANDOFF_APPROVED_WITH_NOTES`,
`RELATORIO_AUDITORIA_H-0019_HANDOFF.md`) e então bloqueado pela ADR-0015
antes de qualquer implementação.

A ADR-0015 (`docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`,
commit `9d4c74d`) formalizou novas regras normativas que contradiziam partes
da versão anterior do H-0019:

1. **Composição hierárquica como árvore**: `grupo` é nó estrutural que recebe
   área e redistribui internamente — não é transparente.
2. **Distribuição pertence ao container**: `distribuicao` é atributo do container,
   não do filho.
3. **Particionamento contíguo**: regra de "3 vãos iguais" e "N+1 vãos" estão
   supersedidas.
4. **Terminologia**: "lado a lado" não é termo normativo final.

Status do H-0019 antes desta revisão: `BLOCKED_BY_ADR_0015_PENDING_REVISION`

---

## Leituras realizadas

Todos os seguintes arquivos foram lidos integralmente antes de qualquer alteração:

```
docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
docs/handoff/H-0019-layout-horizontal-plano-corpo.md
docs/relatorios/RELATORIO_AUDITORIA_H-0019_HANDOFF.md
docs/relatorios/RELATORIO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO.md
docs/relatorios/RELATORIO_VERIFICACAO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO.md
docs/relatorios/RELATORIO_VERIFICACAO_DOCUMENTAL_ADR-0015_POS_CORRECAO.md
docs/NOMENCLATURA.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_json_tela_minima.md
```

Lidos para contexto técnico (sem alteração):

```
tela/loader.py (linhas 340–360)
tela/renderizador.py (referência de contexto)
config/telas/ (referência de contexto)
```

---

## Mudanças realizadas no handoff

### 1. Status atualizado

**Antes**: `BLOCKED_BY_ADR_0015_PENDING_REVISION`

**Depois**: `HANDOFF_REVISED_READY`

Registrado no metadata do handoff e na seção `## Status`.

### 2. Commit base atualizado

**Antes**: `3b98856  docs: registra levantamento pos H-0018`

**Depois**: `9d4c74d  docs: formaliza composicao hierarquica do corpo`

A implementação deve partir do estado do repositório no commit `9d4c74d`.

### 3. Nova seção "Revisão pós-ADR-0015" adicionada

Substituiu as seções antigas "Bloqueio por ADR-0015" e "Revisão
pós-auditoria". Documenta:

- Histórico do bloqueio
- Autoridade da revisão (ADR-0015 como superior)
- Cinco mudanças conceituais aplicadas
- Proteção contra implementações baseadas na versão anterior

### 4. Algoritmo de Passo 1 revisado — grupo NÃO é expandido

**Versão anterior (Passo 1 antigo — REJEITADO)**:

```python
for elemento in elementos:
    if elemento.tipo == "grupo":
        for interno in elemento.elementos:
            funcionais.append(interno)  # EXPANSÃO REJEITADA
    else:
        funcionais.append(elemento)
```

**Versão revisada (Passo 1 novo)**:

O algoritmo itera diretamente sobre os filhos diretos de `corpo.elementos[]`
sem expansão de grupos. `grupo` conta como um slot que recebe área alocada,
mas não tem renderização visual própria no H-0019 (ADR-0015 Decisão 2).
`_caixa_de_elemento` retorna `None` para `grupo`; a área alocada fica
visualmente vazia. Suporte à redistribuição interna de grupo vai para H-0020.

**Motivação**: ADR-0015 Decisão 2 estabelece que `grupo` é nó estrutural que
recebe área do container pai e redistribui internamente — não é transparente.
Expandir grupo no Passo 1 antecipa comportamento de H-0020 e contradiz o
modelo de árvore formalizado pela ADR-0015.

### 5. "lado a lado" removido como termo normativo

**Ocorrências normativas na versão anterior removidas ou substituídas**:

| Linha (aprox.) | Contexto original | Substituição |
|---|---|---|
| Seção Contexto | "composição lado a lado dos elementos" | "particionamento contíguo da largura" |
| Escopo positivo item 2 | "renderizar elementos diretos lado a lado" | "aplicar particionamento contíguo da largura disponível" |
| Algoritmo Passo 2 mensagem de erro | "elementos lado a lado (minimo 10 chars)" | "no particionamento horizontal (minimo 10 chars por area)" |
| Critério de aceite 4 | "renderiza dois ou mais elementos diretos lado a lado" | "renderiza com particionamento contíguo da largura" |
| Testes (dois nomes) | "dois_elementos_lado_a_lado", "aparecem lado a lado" | "dois_elementos", "aparecem na mesma faixa de linhas" |

**Usos mantidos como registros históricos/literais** (sem função normativa):

- Seção "Revisão pós-ADR-0015": "A expressão 'lado a lado' não deve
  aparecer como termo normativo..." — documenta a remoção.
- Risk R-4: "N+1 vãos iguais (INTERPRETAÇÃO REJEITADA)" — histórico rejeitado.
- Seção "Exigência de nova auditoria": "Confirmar que 'lado a lado' não
  aparece como termo normativo." — critério de auditoria futura.

### 6. Nome do algoritmo atualizado

**Antes**: `## Algoritmo de layout horizontal plano`

**Depois**: `## Algoritmo de particionamento horizontal do corpo`

Alinhado com a terminologia ADR-0015 (particionamento contíguo).

### 7. Nova seção "Política para distribuição neste ciclo" adicionada

**Decisão**: Opção A — Sem `distribuicao` explícita neste ciclo.

H-0019 implementa `corpo.arranjo = "horizontal"` com distribuição uniforme
implícita (`modo = igual`) entre filhos diretos, sem exigir declaração de
`distribuicao` no JSON. Compatível com:

- `contrato_json_tela_minima.md` (v0.1, ADR-0015): `distribuicao` definida
  como opcional no container.
- ADR-0015 Decisão 6: modo `igual` é válido.
- JSONs existentes não declaram `distribuicao` no `corpo`.

`distribuicao` percentual/fração fica explicitamente fora de escopo (H-0020
ou posterior).

### 8. Nova seção "Política para largura insuficiente" adicionada

Confirma que terminal pequeno com reticências (`...`) está **fora de escopo**
do H-0019 (ADR-0015 Decisão 13 registra como conceito futuro). Somente
`RenderizadorErro` determinístico é permitido.

### 9. Nova seção "Exigência de nova auditoria" adicionada

H-0019 revisado deve ser auditado antes de qualquer implementação. Novo
relatório de auditoria deve ser criado em:

```
docs/relatorios/RELATORIO_AUDITORIA_H-0019_POS_REVISAO_ADR-0015.md
```

### 10. Testes atualizados

**Removido do escopo H-0019**:

```
test_arranjo_horizontal_grupo_estrutural
```

Este teste verificava expansão de grupo — comportamento rejeitado pela
ADR-0015. Movido para "Fora de escopo futuro" (H-0020).

**Renomeado**:

```
test_arranjo_horizontal_dois_elementos_lado_a_lado
  → test_arranjo_horizontal_dois_elementos

test_arranjo_horizontal_caixas_coladas
  → test_arranjo_horizontal_areas_contiguas
```

**Adicionado**:

```
test_arranjo_horizontal_resto_deterministico
```

Verifica que o resto da divisão inteira é distribuído deterministicamente
pelas primeiras áreas (maiores restos, ADR-0015 Decisão 8).

### 11. Seções obrigatórias adicionadas

Adicionadas as seções requeridas que estavam ausentes:

- `## Revisão pós-ADR-0015`
- `## Política para distribuição neste ciclo`
- `## Política para largura insuficiente`
- `## Exigência de nova auditoria`

### 12. Ordem de autoridade atualizada

ADR-0015 explicitamente posicionada como autoridade superior aos contratos
de módulo na hierarquia:

```
contrato_processo_desenvolvimento.md
  > ADR-0015 (autoridade superior)
    > ADR-0008, ADR-0010, ADR-0011, ADR-0013, ADR-0014
      > contratos de módulo
        > H-0019 revisado
```

### 13. Leitura obrigatória atualizada

ADR-0015 e todos os relatórios de verificação documental da ADR-0015
adicionados à lista de leitura obrigatória (itens 1 a 4).

---

## Compatibilidade com ADR-0015

| Decisão ADR-0015 | Compatibilidade no H-0019 revisado |
|---|---|
| Decisão 1 — Corpo como árvore | H-0019 trata `corpo.elementos[]` como nível 1 da árvore, sem expansão de nós estruturais |
| Decisão 2 — Grupo como nó estrutural | `grupo` não é expandido; conta como slot com área vazia no H-0019 |
| Decisão 3 — Nível | H-0019 trabalha somente com nível 1 (filhos diretos de `corpo`) |
| Decisão 4 — Arranjo por container | `corpo.arranjo = "horizontal"` é declarado no container raiz |
| Decisão 5 — Distribuição por container | `distribuicao` pertence ao `corpo`; H-0019 usa modo `igual` implícito |
| Decisão 6 — Modos de distribuição | Modo `igual` adotado (Opção A); percentual/fração fora de escopo |
| Decisão 7 — Quantidade de valores | N/A neste ciclo (sem `distribuicao.valores[]` explícita) |
| Decisão 8 — Arredondamento determinístico | Passo 2 usa maiores restos: `base_w + (1 if i < resto else 0)` |
| Decisão 9 — Contato entre molduras | Concatenação direta sem separador; bordas adjacentes coladas |
| Decisão 10 — Preenchimento de área alocada | Passo 4 preenche áreas menores com linhas de espaços |
| Decisão 11 — Regras dinâmicas de dimensão | Fora de escopo H-0019 |
| Decisão 12 — Paginação dentro da área | Fora de escopo H-0019 |
| Decisão 13 — Terminal muito pequeno | `RenderizadorErro` determinístico; `...` fora de escopo H-0019 |
| Decisão 14 — Sincronização de cortes | Fora de escopo H-0019 |
| Decisão 16 — Bloqueio do H-0019 | Cumprido; revisão realizada; nenhuma implementação anterior |
| Decisão 17 — Ciclos futuros | H-0020 para grupos; H-0019 permanece plano |

**Compatibilidade**: INTEGRAL

---

## Compatibilidade com contrato_composicao_corpo.md v0.3

| Regra do contrato v0.3 | Tratamento no H-0019 revisado |
|---|---|
| R-20: sem vão externo, particionamento contíguo | Passo 5 concatena sem separador |
| R-15: `grupo` é nó estrutural, não funcional | Grupo não é expandido; não gera visual no H-0019 |
| R-18: distribuição aloca área, não apenas conteúdo | Passo 4 preserva área com preenchimento |
| R-19: arredondamento por maiores restos | Passo 2 aplica fórmula determinística |
| R-22: sem fallback silencioso | Passo 2 lança `RenderizadorErro` para largura insuficiente |
| Seção 4.9: distribuição opcional por container | Opção A (distribuição uniforme implícita) compatível |
| Seção 4.2: aliases transicionais aceitos | Loader e renderer normalizam `sobreposto`/`lado_a_lado` |

**Compatibilidade**: INTEGRAL

---

## Termos removidos ou reclassificados

| Termo | Status no H-0019 revisado | Substituição |
|---|---|---|
| `lado a lado` (normativo) | REMOVIDO como termo normativo | `arranjo horizontal`, `particionamento contíguo`, `áreas adjacentes coladas` |
| `3 vãos iguais` | APENAS como referência histórica rejeitada em R-4 | `particionamento contíguo` |
| `N+1 vãos` | APENAS como interpretação rejeitada em R-4 e seção Revisão | `particionamento contíguo` |
| `borda↔coluna_1↔coluna_2↔borda` | APENAS em contexto de rejeição histórica (R-4 e Revisão) | N/A |
| `vãos externos` / `vão lateral` | APENAS em R-4 (o que NÃO implementar) | N/A |
| `lado_a_lado` (literal, como alias) | MANTIDO como alias transitional literal aceito pelo loader | — |
| `sobreposto` (literal, como alias) | MANTIDO como alias transitional literal aceito pelo loader | — |

---

## Escopo final do H-0019 revisado

H-0019 implementa **apenas**:

1. `corpo.arranjo = "horizontal"` como arranjo do container raiz `corpo`.
2. Aplicação somente aos filhos diretos de `corpo.elementos[]`.
3. Particionamento contíguo da largura total disponível entre filhos diretos.
4. Cada filho recebe uma área/faixa de largura alocada (modo `igual` implícito).
5. A distribuição aloca área, não apenas conteúdo.
6. Cada elemento funcional é renderizado dentro da sua área alocada.
7. Áreas adjacentes ficam contíguas, sem separador/vão externo.
8. Bordas adjacentes ficam coladas: `││`, `╮╭`, `╯╰`.
9. A primeira área começa no primeiro caractere útil.
10. A última área termina no último caractere útil.
11. Resto da divisão distribuído deterministicamente (maiores restos).
12. Alturas diferentes normalizadas por preenchimento dentro da área alocada.
13. Largura insuficiente gera `RenderizadorErro` determinístico.

---

## Itens mantidos fora de escopo

Os seguintes itens foram explicitamente confirmados como fora do escopo do
H-0019 revisado, conforme seção "Fora de escopo futuro" do handoff:

- Grupos hierárquicos com redistribuição interna (H-0020)
- Distribuição percentual/fração
- `distribuicao` como campo JSON explícito no corpo
- Regras dinâmicas de mínimo/preferido/máximo
- Sincronização de cortes entre grupos
- Paginação real, terminal com `...`, console real
- Navegação por `[✥]`, foco, seleção, filtros, ações
- Alterações em contratos, ADRs ou NOMENCLATURA
- `test_arranjo_horizontal_grupo_estrutural` (H-0020)

---

## Proteção da barra_de_menus

As seguintes proteções estão explicitamente registradas nas seções
"Escopo negativo" e "Preservações obrigatórias" do H-0019 revisado:

| Artefato | Proteção |
|---|---|
| `barra_de_menus.distribuicao` | NÃO alterar |
| `_normaliza_distribuicao` | NÃO alterar |
| `_validar_distribuicao` | NÃO alterar |
| `_linhas_barra` | NÃO alterar |
| `tela/explorar_barra_de_menus.py` | NÃO alterar |
| `tela/teste_explorar_barra_de_menus.py` | NÃO alterar |
| `contrato_barra_de_menus.md` | NÃO alterar |
| `contrato_chip.md` | NÃO alterar |

Qualquer necessidade de alterar qualquer um desses artefatos durante a
implementação do H-0019 deve parar com `ARCHITECTURE_REVIEW_REQUIRED`.

---

## Necessidade de nova auditoria

O H-0019 revisado **deve ser auditado** antes de qualquer implementação.

A seção "Exigência de nova auditoria" do handoff revisado lista os critérios
que a nova auditoria deve verificar:

1. Nenhuma regra ativa contradiz a ADR-0015.
2. "lado a lado" não aparece como termo normativo.
3. Grupo não é expandido no algoritmo.
4. Opção A (distribuição uniforme implícita) está compatível com contratos.
5. Todos os testes obrigatórios cobrem os cenários listados.
6. Proteção da barra_de_menus está explícita.

Relatório de auditoria a criar:

```
docs/relatorios/RELATORIO_AUDITORIA_H-0019_POS_REVISAO_ADR-0015.md
```

---

## Conclusão

A revisão do H-0019 foi realizada com sucesso. O handoff foi atualizado de
`BLOCKED_BY_ADR_0015_PENDING_REVISION` para `HANDOFF_REVISED_READY`.

Mudanças principais:

- Algoritmo Passo 1 revisado: grupo não é expandido (ADR-0015 Decisão 2).
- "lado a lado" removido de todas as posições normativas.
- Opção A adotada para distribuição (modo `igual` implícito).
- ADR-0015 registrada como autoridade superior na ordem de autoridade.
- Commit base atualizado para `9d4c74d`.
- Seções obrigatórias adicionadas (`Revisão pós-ADR-0015`,
  `Política para distribuição neste ciclo`, `Política para largura
  insuficiente`, `Exigência de nova auditoria`).
- `test_arranjo_horizontal_grupo_estrutural` movido para fora de escopo.

A versão revisada está coerente com ADR-0015 e contratos atualizados (v0.3
de `contrato_composicao_corpo.md`). Uma nova auditoria é obrigatória antes
da implementação.

---

## Verificações executadas

### git diff --stat

```
 scripts/docs/handoff/H-0019-layout-horizontal-plano-corpo.md | 1018 ++++++++++++--------
 1 file changed, 617 insertions(+), 401 deletions(-)
```

### git diff --name-only

```
scripts/docs/handoff/H-0019-layout-horizontal-plano-corpo.md
```

### git status --short

```
 M docs/handoff/H-0019-layout-horizontal-plano-corpo.md
?? docs/relatorios/RELATORIO_REVISAO_H-0019_HANDOFF_POS_ADR-0015.md
```

### grep de termos proibidos como regras ativas

```bash
grep -n "3 vãos\|N+1\|borda↔coluna\|coluna_1↔coluna_2\|vãos iguais\|lado a lado" \
  docs/handoff/H-0019-layout-horizontal-plano-corpo.md || true
```

**Saída** (todas ocorrências são contextuais — não regras ativas):

```
82:  **2. "lado a lado" removido como termo normativo**
84:  A expressão "lado a lado" não deve aparecer como termo normativo...
96:  **3. N+1 vãos e 3 vãos: interpretações rejeitadas**
98:  A regra de "N+1 vãos iguais" (borda↔coluna_1, ...) — seção Revisão
178: A regra anterior de "3 vãos iguais" está explicitamente supersedida.
1023: ... "N+1 vãos iguais" (INTERPRETAÇÃO REJEITADA), "3 vãos" (INTERPRETAÇÃO REJEITADA)
1024: ... vão lateral, padding entre colunas ...
1032: N+1 vãos iguais (borda↔coluna_1, ...) foi adotada ... — Interpretação rejeitada historicamente
1133: 2. Confirmar que "lado a lado" não aparece como termo normativo.
```

**Classificação de cada ocorrência**:

| Linha | Classificação |
|---|---|
| 82, 84 | Seção de revisão — documenta a remoção; não é regra ativa |
| 96, 98 | Seção de revisão — documenta interpretação rejeitada; não é regra ativa |
| 178 | Seção Contexto — referência histórica explicitamente supersedida |
| 1023-1024 | Risk R-4 — marcado como INTERPRETAÇÃO REJEITADA; não é regra ativa |
| 1032 | Risk R-4 — "Interpretação rejeitada historicamente"; não é regra ativa |
| 1133 | Seção Exigência de nova auditoria — critério de verificação futura |

**Resultado**: NENHUM termo proibido aparece como regra ativa no handoff revisado.

### Verificação de escopo negativo

Arquivos não alterados (somente lidos):

```
docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md    → NÃO alterado
docs/contratos/contrato_composicao_corpo.md                        → NÃO alterado
docs/contratos/contrato_tela_json.md                               → NÃO alterado
docs/contratos/contrato_json_tela_minima.md                        → NÃO alterado
docs/NOMENCLATURA.md                                               → NÃO alterado
tela/ (todos os arquivos)                                          → NÃO alterado
config/ (todos os arquivos)                                        → NÃO alterado
docs/relatorios/RELATORIO_AUDITORIA_H-0019_HANDOFF.md             → NÃO alterado
docs/relatorios/RELATORIO_DOCUMENTAL_ADR-0015_*.md                → NÃO alterado
docs/relatorios/RELATORIO_VERIFICACAO_DOCUMENTAL_ADR-0015_*.md    → NÃO alterado
```
