# RELATORIO_APLICACAO_ADR-0020

## 1. Identificação

- ADR aplicada: `scripts/docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md`
- Etapa: `APLICAR_ADR`
- Papel: autor documental responsável pela aplicação de ADR aprovada
- Raiz Git: `/home/tiago/Dropbox/UFRGS/Survey/versao_0_1`
- Branch: `master`
- Commit-base: `f00b0bb` (confirmado)
- QA de entrada: `RELATORIO_QA_POS_PATCH_ADR-0020.md` — `ADR_APPROVED_WITH_NOTES`
- Status da ADR antes: `proposta`
- Status da ADR depois: `aceita`

---

## 2. Objetivo

Propagar fielmente as decisões D1–D16 da ADR-0020 aprovada (incluindo o patch
da D6 aprovado em QA pós-patch) aos documentos normativos afetados: índice de
ADRs, nomenclatura, contrato de composição do corpo, contrato da tela JSON e
contrato JSON de tela mínima.

---

## 3. Estado Git inicial

- Branch: `master`
- HEAD: `f00b0bb` (igual ao commit-base esperado)
- Arquivos modificados/em stage: nenhum
- Arquivos não rastreados relevantes: `ADR-0020`, relatórios de QA e levantamento
- `git diff --check`: limpo
- `git diff --cached --check`: limpo

Nenhum bloqueio de repositório identificado (sem merge, rebase, cherry-pick ou
revert em andamento; sem stage previamente preenchido).

---

## 4. Autoridades consultadas

| Documento | Papel |
|---|---|
| `ADR-0020-matriz-de-grupos-coordenadas-explicitas.md` | Autoridade da nova decisão (D1–D16) |
| `RELATORIO_QA_ADR-0020.md` | Histórico da rejeição inicial e achado ACH-001 |
| `RELATORIO_QA_POS_PATCH_ADR-0020.md` | Autoridade processual para avançar à aplicação |
| `ADR-0015-composicao-hierarquica-distribuicao-corpo.md` | Vigente no que não especializado |
| `ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md` | Vigente no que não especializado |
| `ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md` | Vigente no que não especializado |
| `NOMENCLATURA.md` | Documento de destino |
| `INDICE_ADR.md` | Documento de destino |
| `contrato_composicao_corpo.md` | Documento de destino |
| `contrato_tela_json.md` | Documento de destino |
| `contrato_json_tela_minima.md` | Documento de destino |

---

## 5. Decisões aplicadas

| Decisão | Conteúdo aplicado | Documentos de destino |
|---|---|---|
| D1 — Dois comportamentos estruturais | `livre` (hierárquico existente) e `matriz` (bidimensional) | ADR-0020, NOMENCLATURA §15, contrato_composicao §3.3, contrato_tela §8, contrato_minima §6.2 |
| D2 — Seletor `estrutura` | Seletor canônico `estrutura: "livre"` ou `estrutura: "matriz"`; proibição de `tipo`, `arranjo`, `modo` | ADR-0020, NOMENCLATURA §15.1, contrato_composicao §3.3, contrato_tela §8 |
| D3 — Compatibilidade por ausência | Ausência de `estrutura` = `livre`; nunca ativa `matriz` | ADR-0020, NOMENCLATURA §15.1-15.2, contrato_composicao §3.3/§5.13, contrato_tela §8, contrato_minima §6.2/§6.4 |
| D4 — Comportamento livre | `arranjo` válido; `distribuicao` opcional; ausência segue ADR-0018; sem grade compartilhada | NOMENCLATURA §15.2, contrato_composicao §3.3/§5.13, contrato_tela §8, contrato_minima §6.2 |
| D5 — Dimensões | linhas 2–4, colunas 2–4; rejeição determinística fora dos limites | NOMENCLATURA §15.3, contrato_composicao §5.14, contrato_tela §8, contrato_minima §6.4 |
| D6 — Distribuições obrigatórias (patch) | `matriz.linhas.distribuicao` e `matriz.colunas.distribuicao` obrigatórios; sem default `igual`; maiores restos por eixo; preserva ADR-0018 para `livre` | NOMENCLATURA §15.4, contrato_composicao §5.15 + INV-MAT-DIST-01-06, contrato_tela §8, contrato_minima §6.4 |
| D7 — Grade comum | Uma única grade compartilhada; bordas alinhadas; não calculada por célula | NOMENCLATURA §15.4, contrato_composicao §5.16, contrato_tela §8 |
| D8 — Coordenadas explícitas | Índices 1-based; posição por coordenadas; proibição de duplicidade; referência a `elementos[]` | NOMENCLATURA §15.4, contrato_composicao §5.17, contrato_tela §8, contrato_minima §6.4 |
| D9 — Conteúdo das células | console, lancador, dashboard, grupo; profundidade ADR-0019 preservada | contrato_composicao §5.19, contrato_tela §8 |
| D10 — Cobertura completa | Células vazias proibidas; quantidade = linhas×colunas; sem placeholder | NOMENCLATURA §15.5, contrato_composicao §5.18, contrato_tela §8, contrato_minima §6.4 |
| D11 — Sem mesclagem | rowspan/colspan/mesclagem fora de escopo | NOMENCLATURA §15.5, contrato_composicao §5.18 |
| D12 — Rejeição determinística | Sem fallback, sem correção automática, sem conversão para `livre` | NOMENCLATURA §15.5, contrato_composicao §5.20/R-31, contrato_tela §8, contrato_minima §6.4 |
| D13 — Proibição de `arranjo` | `arranjo` proibido em `estrutura: matriz`; válido em `livre` | NOMENCLATURA §15.5, contrato_composicao §3.3/R-30, contrato_tela §8, contrato_minima §6.4 |
| D14 — Terminal e área insuficiente | Preserva ADR-0017; política específica de matriz permanece pendente | contrato_composicao §5.21 |
| D15 — Compatibilidade retroativa | JSONs sem `estrutura` preservados; `livre` intacto; todas as decisões anteriores preservadas | Propagado em todos os documentos |
| D16 — Matriz especializa grupo | Não substitui árvore, `elementos[]`, profundidade, tipos; apenas organiza filhos diretos | contrato_composicao §5.19/R-32, contrato_tela §8 |

---

## 6. Arquivos autorizados

| Arquivo | Tipo | Ação |
|---|---|---|
| `scripts/docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md` | existente | alterado — status `proposta` → `aceita` (frontmatter e corpo) |
| `scripts/docs/adr/INDICE_ADR.md` | existente | alterado — adicionada linha ADR-0020 |
| `scripts/docs/NOMENCLATURA.md` | existente | alterado — adicionada seção 15 |
| `scripts/docs/contratos/contrato_composicao_corpo.md` | existente | alterado — seções 3.3, 5.13–5.24, R-25–R-32, critérios de validação |
| `scripts/docs/contratos/contrato_tela_json.md` | existente | alterado — novo bloco sobre `estrutura` na seção 8 |
| `scripts/docs/contratos/contrato_json_tela_minima.md` | existente | alterado — seção 6.2 expandida, seção 6.4 criada, V-9–V-12, critérios de aceite |
| `scripts/docs/relatorios/RELATORIO_APLICACAO_ADR-0020.md` | novo | criado — este relatório |

Total: 6 arquivos existentes alterados + 1 arquivo novo criado = 7. Dentro do limite autorizado.

---

## 7. Aplicação na ADR-0020

Alterações realizadas:

- `metadata.status`: `proposta` → `aceita`
- Seção `## Status`: `proposta` → `aceita`

Não alterados: D1–D16, schema, exemplos válidos, exemplos inválidos, invariantes,
consequências documentais, consequências futuras de implementação, testes futuros,
limitações, fora de escopo, critérios para handoff, pendências não resolvidas,
relações normativas, documentos consultados.

A ADR não declara que a aplicação documental foi aprovada por QA, pois o QA da
aplicação ainda não ocorreu.

---

## 8. Aplicação no índice

Adicionada a seguinte linha ao `INDICE_ADR.md` após ADR-0019:

```
| ADR-0020 | Especialização bidimensional do nó `grupo` — formaliza os comportamentos
`livre` (hierárquico existente) e `matriz` (grade comum com coordenadas explícitas);
seletor declarativo `estrutura`; ausência de `estrutura` equivale a `livre`;
distribuições obrigatórias e independentes por eixo (`matriz.linhas.distribuicao`,
`matriz.colunas.distribuicao`); dimensões 2–4 por eixo; cobertura completa de
células; rejeição determinística sem fallback; compatibilidade retroativa integral
(especializa ADR-0015, ADR-0018 e ADR-0019) | aceita | 2026-07-12 |
```

Status da ADR-0018 no índice: não alterado (permanece `aceita` — divergência
histórica preservada conforme instrução).

---

## 9. Aplicação na nomenclatura

Adicionada seção 15 `Comportamento estrutural do grupo — livre e matriz (ADR-0020)`
com:

- §15.1 — Seletor declarativo `estrutura` (tabela de valores, proibições)
- §15.2 — Comportamento `livre` (preservação integral)
- §15.3 — Comportamento `matriz` e distinção obrigatória com outros domínios
- §15.4 — Termos da matriz de grupos (8 termos definidos)
- §15.5 — Termos desaconselhados ou inválidos em `estrutura: matriz` (6 entradas)

Terminologia anterior preservada. Sem conflito com seções pré-existentes 1–14.

---

## 10. Aplicação no contrato de composição do corpo

Adições ao `contrato_composicao_corpo.md`:

**Frontmatter**: adicionados `ADR-0019` e `ADR-0020` à lista `adrs_aplicadas`.

**Seção 3.3** — Comportamentos estruturais do `grupo`: seletor `estrutura`,
`livre`, `matriz`, compatibilidade por ausência, proibição de `arranjo` em matriz.

**Seção 5.13** — Distinção normativa `livre` × `matriz` com preservação da ADR-0018.

**Seção 5.14** — Dimensões da matriz (D5): limites 2–4, tabela de combinações, inválidos.

**Seção 5.15** — Distribuições obrigatórias por eixo (D6 pós-patch): regras, modos,
maiores restos por eixo, invariantes INV-MAT-DIST-01 a 06.

**Seção 5.16** — Grade comum de coordenadas (D7): única grade, bordas alinhadas.

**Seção 5.17** — Células com coordenadas explícitas (D8): regras de indexação.

**Seção 5.18** — Cobertura completa (D10): proibição de célula vazia.

**Seção 5.19** — Conteúdo das células e profundidade (D9, ADR-0019).

**Seção 5.20** — Rejeição determinística (D12): sem fallback.

**Seção 5.21** — Terminal e área insuficiente (D14).

**Seção 5.22** — Schema normativo da matriz (estrutura JSON completa 2×2).

**Seção 5.23** — Exemplos válidos (EX-MAT-V1 a EX-MAT-V5):
- EX-MAT-V1: matriz 2×2 com `igual` explícito nos dois eixos
- EX-MAT-V2: matriz 2×4 com frações diferentes
- EX-MAT-V3: matriz com modos diferentes entre linhas e colunas
- EX-MAT-V4: grupo `livre` sem `estrutura`
- EX-MAT-V5: grupo `livre` com `estrutura: livre`

**Seção 5.24** — Exemplos inválidos (EX-MAT-I1 a EX-MAT-I9):
- EX-MAT-I1: ausência de distribuição de linhas
- EX-MAT-I2: ausência de distribuição de colunas
- EX-MAT-I3: somente um eixo com distribuição
- EX-MAT-I4: coordenada duplicada
- EX-MAT-I5: elemento duplicado
- EX-MAT-I6: célula faltante
- EX-MAT-I7: `arranjo` em `estrutura: matriz`
- EX-MAT-I8: quarto nível de grupo em célula
- EX-MAT-I9: matriz inválida sem fallback

**Seção 7** — Regras R-25 a R-32 adicionadas.

**Seção 8** — Critérios de validação de matriz adicionados (12 itens).

---

## 11. Aplicação no contrato da tela JSON

Adicionado bloco normativo na seção 8 (`corpo`) do `contrato_tela_json.md`:

- Tabela de comportamento por valor de `estrutura` (ausente/`livre`/`matriz`)
- Schema do objeto `matriz` com campos obrigatórios
- Tabela de campos obrigatórios por modo de distribuição de eixo
- Lista completa de validações a propagar para o loader

Distinção claramente expressa:

| Estado | Objeto `matriz` | `arranjo` |
|---|---|---|
| `estrutura` ausente | não aplicável | válido |
| `estrutura: "livre"` | não aplicável | válido |
| `estrutura: "matriz"` | obrigatório | proibido |

Sem declaração de implementação existente. Usadas formulações como "o loader
deverá futuramente validar".

---

## 12. Aplicação no contrato JSON de tela mínima

Alterações no `contrato_json_tela_minima.md`:

**Frontmatter**: adicionados `ADR-0019` e `ADR-0020` à lista `adrs_aplicadas`.

**Seção 6.2** (Nó estrutural `grupo`): expandida para incluir `estrutura` como
campo opcional; tabela de valores de `estrutura`; compatibilidade de grupos sem
`estrutura`; `distribuicao` rotulada como opcional em `estrutura: "livre"`.

**Seção 6.4** (nova — Campos mínimos de `grupo` com `estrutura: "matriz"`):
- Envelope mínimo válido de matriz 2×2 com `igual` explícito nos dois eixos
- Tabela de campos obrigatórios em `estrutura: "matriz"`
- Declaração de obrigatoriedade explícita do modo `igual`
- Listagem de proibições
- Declaração de rejeição determinística
- Declaração de que matriz não é obrigatória para toda tela

**Seção 8** (Regras de validação): adicionados V-9 a V-12 para matriz.

**Segunda seção 8** (Critérios de aceite): adicionados 5 critérios de matriz.

Exemplos mínimos existentes preservados. Tipos funcionais não ampliados.

---

## 13. Relação com ADR-0015

A ADR-0015 é preservada e complementada. Todos os pontos vigentes mantidos:

- composição hierárquica como árvore;
- nó estrutural `grupo`;
- `arranjo` e `distribuicao` por container (válidos em `livre`);
- modos `igual`, `percentual`, `fracao`;
- maiores restos (aplicado por eixo na matriz);
- preenchimento de área alocada;
- sincronização de cortes para `livre`.

A ADR-0020 **adiciona** a especialização bidimensional `matriz` sem cancelar
nem reescrever a ADR-0015.

---

## 14. Relação com ADR-0018

**Em `estrutura: livre`**: a ausência de `distribuicao` continua seguindo a
ADR-0018 — não equivale a `igual`, preserva construção orientada pelo conteúdo.
Nenhuma regra do comportamento `livre` foi modificada.

**Em `estrutura: matriz`**: a obrigatoriedade de distribuição explícita nos
dois eixos é especialização nova. Não redefine nem cancela a ADR-0018. A
distinção foi propagada explicitamente em todos os documentos alterados.

A divergência textual de status da ADR-0018 (arquivo: `proposta`; índice:
`aceita`) é pendência histórica separada. Não foi corrigida, não foi alterada,
não foi mencionada como resolvida.

O arquivo `ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md` não
foi alterado. O status da ADR-0018 no índice não foi alterado.

---

## 15. Relação com ADR-0019

A ADR-0019 é preservada integralmente:

- limite máximo de três níveis de grupos: mantido;
- contagem exclusiva por nós estruturais `grupo`: mantida;
- linhas, colunas e células não contam como níveis: declarado;
- `grupo` em célula conta como nível normalmente: declarado;
- quarto nível de grupo em célula é inválido: exemplificado em EX-MAT-I8.

O arquivo `ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md`
não foi alterado.

---

## 16. Exemplos e validações propagados

### Exemplos válidos (5)
1. Matriz 2×2 com `igual` explícito nos dois eixos (EX-MAT-V1)
2. Matriz 2×4 com frações diferentes (EX-MAT-V2)
3. Matriz com modos diferentes entre linhas e colunas (EX-MAT-V3)
4. Grupo `livre` sem `estrutura` (EX-MAT-V4)
5. Grupo `livre` com `estrutura: "livre"` (EX-MAT-V5)

### Exemplos inválidos (9)
1. Ausência de distribuição de linhas (EX-MAT-I1)
2. Ausência de distribuição de colunas (EX-MAT-I2)
3. Somente um eixo com distribuição (EX-MAT-I3)
4. Coordenada duplicada (EX-MAT-I4)
5. Elemento duplicado (EX-MAT-I5)
6. Célula faltante (EX-MAT-I6)
7. `arranjo` em `estrutura: matriz` (EX-MAT-I7)
8. Quarto nível de grupo em célula (EX-MAT-I8)
9. Matriz inválida sem fallback (EX-MAT-I9)

### Validações inválidas propagadas
Todos os itens listados na seção "Regras de validação a propagar" do prompt foram
propagados para `contrato_tela_json.md` seção 8, `contrato_composicao_corpo.md`
seção 8 e `contrato_json_tela_minima.md` seção 8 (V-9–V-12).

---

## 17. Preservações

- Todos os JSONs ativos sem `estrutura` continuam válidos (D3, D15)
- Comportamento `livre` preservado integralmente (D4, D15)
- Modos `igual`, `percentual`, `fracao` em `livre` preservados
- Ausência de `distribuicao` em `livre` segue ADR-0018 (não equivale a `igual`)
- Composição plana preservada
- Composição hierárquica (até 3 níveis de grupos) preservada (ADR-0019)
- Navegação, passividade de `dashboard`, console, lancador preservados
- Redimensionamento reativo (ADR-0017) preservado
- Quadro de terminal pequeno (ADR-0017) preservado
- Maiores restos (ADR-0015) preservado — aplicado por eixo na matriz
- Taxonomia fechada de tipos funcionais preservada

---

## 18. Pendências não aplicadas

As seguintes pendências da ADR-0020 permanecem abertas e não foram abordadas
nesta aplicação documental (como exigido):

1. Política específica de área insuficiente para matriz (D14)
2. Suporte futuro a células vazias
3. Suporte futuro a mesclagem (`rowspan`/`colspan`)
4. Suporte futuro a dimensões acima de 4 × 4
5. Implementação de código (loader, modelo, renderizador)
6. Testes
7. Criação de handoff
8. QA da aplicação documental (próxima categoria)

---

## 19. Busca de resíduos e contradições

### Busca obrigatória inicial
Executada antes das alterações. Confirmados os pontos de impacto nos documentos
de destino.

### Busca de resíduos pós-aplicação
Executada com padrão:
```
matriz.*opcional|distribui[cç][aã]o.*opcional|igual.*impl[ií]cit|
conteúdo natural.*matriz|arranjo.*matriz|fallback.*livre|célula vazia|
rowspan|colspan|mais de 4|nível 4|nivel 4
```

Todas as ocorrências analisadas individualmente:

| Ocorrência | Documento | Avaliação |
|---|---|---|
| "célula vazia" em §4.1, §8.2, §8.4 (NOMENCLATURA) | Seções pré-existentes de `lancador`/`console` | Domínio diferente — correto |
| "nível 4" em §14 (NOMENCLATURA) e contratos | Pre-existing ADR-0019 content | Correto — proibição |
| "`distribuicao`...opcional" em §15.2 (NOMENCLATURA) | Nova seção 15.2 sobre `livre` | Correto — em `livre` é opcional |
| "`distribuicao`...opcional" em `contrato_json_tela_minima.md` §6.2-6.3 | Contexto de `livre` e geral | Correto |
| "fallback.*livre" em `contrato_tela_json.md` §8 | Lista de proibições | Correto |
| "arranjo.*matriz" em múltiplos arquivos | Proibições e exemplos inválidos | Correto |
| rowspan/colspan na ADR-0020 | Seções "fora de escopo" e "pendências" | Correto — histórico/pendência |
| rowspan/colspan em NOMENCLATURA §15.5 | Tabela de termos desaconselhados | Correto |
| rowspan/colspan em `contrato_json_tela_minima.md` §6.4 | Lista de proibições | Correto |

Nenhum resíduo incompatível identificado.

---

## 20. Escopo físico

### Antes das alterações
| Arquivo | Estado |
|---|---|
| `ADR-0020` | não rastreado (untracked) |
| `INDICE_ADR.md` | rastreado, sem modificação |
| `NOMENCLATURA.md` | rastreado, sem modificação |
| `contrato_composicao_corpo.md` | rastreado, sem modificação |
| `contrato_tela_json.md` | rastreado, sem modificação |
| `contrato_json_tela_minima.md` | rastreado, sem modificação |

### Após as alterações
| Arquivo | Estado | Operação |
|---|---|---|
| `ADR-0020` | não rastreado | editado (status proposta→aceita) |
| `INDICE_ADR.md` | modificado | adicionada 1 linha |
| `NOMENCLATURA.md` | modificado | adicionadas 77 linhas (seção 15) |
| `contrato_composicao_corpo.md` | modificado | adicionadas 642 linhas |
| `contrato_tela_json.md` | modificado | adicionadas 66 linhas |
| `contrato_json_tela_minima.md` | modificado | adicionadas 126 linhas |
| `RELATORIO_APLICACAO_ADR-0020.md` | criado | novo arquivo |

Stage: vazio. Nenhum arquivo de código, teste, config ou JSON ativo alterado.

---

## 21. Estado Git final

```
M scripts/docs/NOMENCLATURA.md
M scripts/docs/adr/INDICE_ADR.md
M scripts/docs/contratos/contrato_composicao_corpo.md
M scripts/docs/contratos/contrato_json_tela_minima.md
M scripts/docs/contratos/contrato_tela_json.md
?? scripts/docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md
?? scripts/docs/relatorios/RELATORIO_APLICACAO_ADR-0020.md
?? scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md
?? scripts/docs/relatorios/RELATORIO_QA_ADR-0020.md
?? scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0020.md
?? scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md
```

Stage vazio. `git diff --check` limpo. `git diff --cached --check` limpo.

---

## 22. Status final

```yaml
status_final: ADR_APPLICATION_COMPLETED
bloqueantes: 0
altos: 0
medios: 0
baixos: 0
observacoes: 1
```

Observação preservada (OBS-001 do QA pós-patch): divergência documental
histórica da ADR-0018 (arquivo: `proposta`; índice: `aceita`) — pendência
externa ao escopo desta aplicação, não corrigida, não afirmada como resolvida.

---

## 23. Próxima categoria processual

`QA_APLICACAO_ADR`
