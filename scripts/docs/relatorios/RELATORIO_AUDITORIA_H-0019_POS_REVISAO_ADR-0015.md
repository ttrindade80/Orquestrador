---
name: relatorio-auditoria-h-0019-pos-revisao-adr-0015
description: Auditoria do handoff H-0019 revisado após ADR-0015 — verifica compatibilidade normativa, escopo, algoritmo, testes e proteção de artefatos antes de liberar implementação
metadata:
  type: relatorio
  scope: scripts
  status: AUDITORIA_CONCLUIDA
  data: "2026-07-10"
---

# RELATORIO_AUDITORIA_H-0019_POS_REVISAO_ADR-0015

## Status

```
HANDOFF_REVISED_APPROVED_WITH_NOTES
```

---

## Resumo executivo

O handoff H-0019 revisado pós-ADR-0015 está apto para implementação. A versão
revisada está integralmente compatível com a ADR-0015 e com os contratos
atualizados (v0.3 de `contrato_composicao_corpo.md`). Nenhum termo proibido
aparece como regra ativa. A Opção A (distribuição uniforme implícita) é
compatível com os contratos vigentes. O algoritmo de particionamento horizontal
está completamente especificado e testável. A proteção da `barra_de_menus` está
explícita. O escopo está corretamente limitado ao corpo raiz e filhos diretos,
sem grupos hierárquicos, sem percentual/fração e sem distribuição explícita.

Há dois achados: um de severidade NOTA (comportamento pré-existente de expansão
de `grupo` no modo vertical no código atual — fora do escopo H-0019 e não
agravado pelo handoff) e um de severidade BAIXO (caso N=1 sem teste formal —
consistente com achado A-003 da auditoria anterior). Nenhum achado exige
correção do handoff antes da implementação.

A implementação pode avançar com autorização explícita do usuário após ciência
destas notas.

---

## Base verificada

| Item | Valor |
|---|---|
| HEAD no momento da auditoria | `9d4c74d  docs: formaliza composicao hierarquica do corpo` |
| Commit base declarado no handoff | `9d4c74d  docs: formaliza composicao hierarquica do corpo` |
| Coincidência de base | SIM |
| Workspace | ` M docs/handoff/H-0019-layout-horizontal-plano-corpo.md` + `?? docs/relatorios/RELATORIO_REVISAO_H-0019_HANDOFF_POS_ADR-0015.md` |
| Workspace esperado | Coincide exatamente |

### git log --oneline -6 (momento da auditoria)

```
9d4c74d docs: formaliza composicao hierarquica do corpo
3b98856 docs: registra levantamento pos H-0018
46e0cb9 feat: cobre distribuicao da barra de menus
c8a20fa test: adiciona explorador da barra de menus
ab5ad68 feat: renderiza barra de menus horizontal responsiva
b2eb458 feat: ocupa altura do terminal pelo corpo
```

---

## Arquivos analisados

### Handoff e relatórios

```
docs/handoff/H-0019-layout-horizontal-plano-corpo.md           (lido na íntegra)
docs/relatorios/RELATORIO_REVISAO_H-0019_HANDOFF_POS_ADR-0015.md  (lido na íntegra)
docs/relatorios/RELATORIO_AUDITORIA_H-0019_HANDOFF.md          (lido na íntegra — referência histórica)
```

### ADR e documentos normativos

```
docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md  (lido na íntegra)
docs/NOMENCLATURA.md                                             (lido na íntegra)
```

### Contratos

```
docs/contratos/contrato_composicao_corpo.md   (v0.3, lido na íntegra)
docs/contratos/contrato_tela_json.md          (parcial — seções 1–5)
docs/contratos/contrato_json_tela_minima.md   (lido na íntegra)
```

### Relatórios documentais da ADR-0015

```
docs/relatorios/RELATORIO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO.md
docs/relatorios/RELATORIO_VERIFICACAO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO.md
docs/relatorios/RELATORIO_VERIFICACAO_DOCUMENTAL_ADR-0015_POS_CORRECAO.md
```
(referenciados indiretamente via RELATORIO_REVISAO — confirmada existência)

### Código inspecionado

```
tela/loader.py        (linhas 340–360 — arranjo e retorno do loader)
tela/modelo.py        (linhas 1–55 — dataclasses, Corpo.arranjo)
tela/renderizador.py  (linhas 656–684, 770–848 — _caixa_de_elemento, renderizar_tela)
```

### JSONs de configuração

```
config/telas/orquestrador.json   (referenciado — não alterado)
config/telas/grupo_minimo.json   (referenciado — não alterado)
config/telas/destino_minimo.json (arranjo "sobreposto" confirmado)
config/telas/stub_b.json         (arranjo "sobreposto" confirmado)
```

---

## Comandos executados

### Verificação de estado do repositório

```bash
git log --oneline -6
git status --short
git diff --stat
git diff --name-only
```

**Resultado**: base `9d4c74d` confirmada; apenas os dois arquivos esperados alterados.

### Grep de termos proibidos

```bash
grep -n "3 vãos\|N+1\|borda↔coluna\|coluna_1↔coluna_2\|vãos iguais\|lado a lado" \
  docs/handoff/H-0019-layout-horizontal-plano-corpo.md || true
```

**Saída**:

```
82:**2. "lado a lado" removido como termo normativo**
84:A expressão "lado a lado" não deve aparecer como termo normativo em texto
96:**3. N+1 vãos e 3 vãos: interpretações rejeitadas**
98:A regra de "N+1 vãos iguais" (borda↔coluna_1, coluna_1↔coluna_2,
178:disponível entre filhos diretos. A regra anterior de "3 vãos iguais" está
1023:particionamento horizontal — seja "N+1 vãos iguais" (INTERPRETAÇÃO
1024:REJEITADA), "3 vãos" (INTERPRETAÇÃO REJEITADA), vão lateral, padding entre
1032:N+1 vãos iguais (borda↔coluna_1, coluna_1↔coluna_2, coluna_2↔borda) foi
1133:2. Confirmar que "lado a lado" não aparece como termo normativo.
```

### Inspeção de _caixa_de_elemento

```bash
grep -n "_caixa_de_elemento\|def _caixa_de_elemento\|grupo" tela/renderizador.py | head -10
```

**Resultado**: confirmado que `_caixa_de_elemento` retorna `None` para qualquer
tipo que não seja `console`, `dashboard` ou `lancador` (linha 683: `return None`).
`grupo` retorna `None` → área alocada ficará visualmente vazia no H-0019.

### Comandos finais

```bash
git diff --stat
```

```
 .../H-0019-layout-horizontal-plano-corpo.md   | 1018 ++++++++++++--------
 1 file changed, 617 insertions(+), 401 deletions(-)
```

```bash
git diff --name-only
```

```
scripts/docs/handoff/H-0019-layout-horizontal-plano-corpo.md
```

```bash
git status --short
```

```
 M docs/handoff/H-0019-layout-horizontal-plano-corpo.md
?? docs/relatorios/RELATORIO_REVISAO_H-0019_HANDOFF_POS_ADR-0015.md
```

---

## Verificação de rastreabilidade

| Item | Esperado | Encontrado | Status |
|---|---|---|---|
| ID do handoff | H-0019 | H-0019 (linha 1 do metadata) | OK |
| Status do handoff revisado | `HANDOFF_REVISED_READY` | `HANDOFF_REVISED_READY` (linha 4 e seção Status) | OK |
| Revisão pós-ADR-0015 registrada | Sim | Seção "Revisão pós-ADR-0015" presente (linha 36) | OK |
| ADR-0015 como autoridade superior | Sim | Seção "Ordem de autoridade" confirma ADR-0015 acima dos contratos | OK |
| Base observada | `9d4c74d` | `9d4c74d` no metadata e na seção "Contexto" | OK |
| Auditoria anterior como histórica | Sim | Seção "Histórico do bloqueio" trata RELATORIO_AUDITORIA_H-0019_HANDOFF.md como referência histórica (status `HANDOFF_APPROVED_WITH_NOTES`, base `3b98856`) | OK |
| Relatório de revisão pós-ADR-0015 | Existe e é coerente | RELATORIO_REVISAO_H-0019_HANDOFF_POS_ADR-0015.md lido na íntegra — coerente com o handoff revisado | OK |

---

## Verificação de compatibilidade com ADR-0015

| Decisão ADR-0015 | Verificação no H-0019 revisado | Status |
|---|---|---|
| D1 — Corpo como árvore | Algoritmo itera sobre `corpo.elementos[]` como nível 1; nenhuma expansão de nó estrutural | OK |
| D2 — Grupo como nó estrutural | Seção "Sobre grupo neste algoritmo": `grupo` não é expandido; `_caixa_de_elemento` retorna `None` para grupo; área vazia no H-0019 | OK |
| D3 — Nível | H-0019 trabalha somente no nível 1 (filhos diretos de `corpo`) | OK |
| D4 — Arranjo por container | `corpo.arranjo = "horizontal"` é o arranjo do container raiz | OK |
| D5 — Distribuição por container | Seção "Política para distribuição": `distribuicao` pertence ao `corpo`; modo `igual` implícito | OK |
| D6 — Modos de distribuição | Modo `igual` adotado (Opção A); percentual/fração explicitamente fora de escopo | OK |
| D7 — Quantidade de valores | N/A neste ciclo — sem `distribuicao.valores[]` explícita | OK (N/A) |
| D8 — Arredondamento determinístico | Passo 2: `base_w + (1 if i < resto else 0)` — maiores restos; `sum(larguras) == total_w` invariante | OK |
| D9 — Contato entre molduras | Passo 5: concatenação direta sem separador; bordas adjacentes `││`, `╮╭`, `╯╰` como consequência natural | OK |
| D10 — Preenchimento de área alocada | Passo 4: normalização de altura com `" " * larguras[i]` para áreas menores | OK |
| D11 — Regras dinâmicas de dimensão | Explicitamente fora de escopo H-0019 | OK (fora de escopo) |
| D12 — Paginação dentro da área | Explicitamente fora de escopo H-0019 | OK (fora de escopo) |
| D13 — Terminal muito pequeno | `RenderizadorErro` determinístico; `...` explicitamente fora de escopo | OK |
| D14 — Sincronização de cortes | Explicitamente fora de escopo H-0019 | OK (fora de escopo) |
| D16 — Bloqueio do H-0019 | Cumprido: revisão realizada; nenhuma implementação anterior; novo status `HANDOFF_REVISED_READY` | OK |
| D17 — Ciclos futuros | H-0020 para grupos com redistribuição interna; H-0019 permanece plano | OK |

**Compatibilidade com ADR-0015**: INTEGRAL

---

## Verificação de compatibilidade com contratos atualizados

### contrato_composicao_corpo.md v0.3

| Regra | Tratamento no H-0019 revisado | Status |
|---|---|---|
| R-15: grupo é nó estrutural, não funcional | Grupo não é expandido no algoritmo horizontal | OK |
| R-16: profundidade máxima 3 | H-0019 não altera profundidade; scope é nível 1 | OK |
| R-18: distribuição aloca área | Passo 4 preserva área com preenchimento | OK |
| R-19: arredondamento por maiores restos | Passo 2 aplica fórmula determinística explícita | OK |
| R-20: sem vão externo, contato contíguo | Passo 5 concatena sem separador | OK |
| R-22: sem fallback silencioso | Passo 2 lança `RenderizadorErro` para largura insuficiente; Risk R-7 | OK |
| Seção 4.9: distribuição opcional | Opção A compatível; ausência de `distribuicao` equivale ao modo `igual` | OK |
| Seção 4.2: aliases transicionais | Loader e renderer normalizam `sobreposto`/`lado_a_lado` | OK |

### contrato_json_tela_minima.md

| Regra | Tratamento no H-0019 revisado | Status |
|---|---|---|
| Seção 5.1: `corpo.arranjo` é opcional | H-0019 adiciona validação mas não torna o campo obrigatório | OK |
| Seção 6.3: `distribuicao` é opcional, ausência = modo `igual` | Opção A é diretamente compatível com esta regra | OK |

**Compatibilidade com contratos**: INTEGRAL

---

## Verificação de remoção de regras antigas

### Classificação de ocorrências do grep

| Linha | Ocorrência | Classificação |
|---|---|---|
| 82 | `**2. "lado a lado" removido como termo normativo**` | Seção de revisão — documenta a remoção; NÃO é regra ativa |
| 84 | `A expressão "lado a lado" não deve aparecer como termo normativo...` | Seção de revisão — declaração da regra de remoção; NÃO é regra ativa |
| 96 | `**3. N+1 vãos e 3 vãos: interpretações rejeitadas**` | Seção de revisão — documenta rejeição; NÃO é regra ativa |
| 98 | `A regra de "N+1 vãos iguais" (borda↔coluna_1,...)` | Seção de revisão — documenta interpretação rejeitada; NÃO é regra ativa |
| 178 | `A regra anterior de "3 vãos iguais" está explicitamente supersedida.` | Seção "Contexto" — referência histórica supersedida; NÃO é regra ativa |
| 1023 | `"N+1 vãos iguais" (INTERPRETAÇÃO REJEITADA)` | Risk R-4 — marcado explicitamente como rejeitado; NÃO é regra ativa |
| 1024 | `"3 vãos" (INTERPRETAÇÃO REJEITADA)` | Risk R-4 — marcado explicitamente como rejeitado; NÃO é regra ativa |
| 1032 | `N+1 vãos iguais... foi adotada... — Interpretação rejeitada historicamente` | Risk R-4 — "rejeitada historicamente"; NÃO é regra ativa |
| 1133 | `2. Confirmar que "lado a lado" não aparece como termo normativo.` | Seção "Exigência de nova auditoria" — critério de verificação; NÃO é regra ativa |

**Resultado**: NENHUM termo proibido aparece como regra ativa no handoff revisado.
Todas as ocorrências estão em contexto de rejeição histórica, documentação de
remoção ou critério de auditoria. Plenamente aceitável.

---

## Verificação do escopo revisado

| Item | Esperado | No handoff | Status |
|---|---|---|---|
| Apenas `corpo.arranjo = "horizontal"` no container raiz `corpo` | Sim | Seção "Objetivo": "Implementar suporte mínimo [...] a `corpo.arranjo = "horizontal"`" | OK |
| Apenas filhos diretos de `corpo.elementos[]` | Sim | Passo 1: itera sobre `modelo.corpo.elementos` sem expansão | OK |
| Sem implementação completa de grupos hierárquicos | Sim | Escopo negativo: "NÃO implementar redistribuição interna de grupo (H-0020)" | OK |
| Sem arranjo dentro de grupo | Sim | Escopo negativo: "NÃO implementar arranjo horizontal dentro de grupo aninhado" | OK |
| Sem distribuicao percentual | Sim | Escopo negativo e "Política para distribuição": percentual fora de escopo | OK |
| Sem distribuicao por fração/pesos | Sim | Escopo negativo: "NÃO implementar distribuição por fração/pesos" | OK |
| Sem sincronização de cortes | Sim | Escopo negativo e "Fora de escopo futuro" | OK |
| Sem paginação real | Sim | Escopo negativo | OK |
| Sem terminal pequeno com "..." | Sim | "Política para largura insuficiente": `...` fora de escopo H-0019 | OK |
| Sem mudanças em barra_de_menus | Sim | Escopo negativo e "Preservações obrigatórias" | OK |

O handoff NÃO exige grupos hierárquicos para implementar H-0019.
`grupo` em `corpo.elementos[]` conta como slot com área visualmente vazia.
Não há motivo para `ARCHITECTURE_REVIEW_REQUIRED` por escopo de grupos.

---

## Verificação da decisão de distribuição

**Decisão registrada no handoff**: Opção A — Sem `distribuicao` explícita neste
ciclo. Distribuição uniforme implícita entre filhos diretos de `corpo.elementos[]`.

| Verificação | Resultado |
|---|---|
| Compatível com ADR-0015 Decisão 6 (modo `igual` é válido) | SIM |
| Compatível com contrato_composicao_corpo.md v0.3 seção 4.9 (`distribuicao` opcional) | SIM |
| Compatível com contrato_json_tela_minima.md seção 6.3 (`distribuicao` ausente = modo `igual`) | SIM |
| Compatível com escopo mínimo do H-0019 | SIM |
| JSONs existentes não declaram `distribuicao` no `corpo` | CONFIRMADO |

A distribuição uniforme implícita NÃO conflita com os contratos atualizados.
Opção A é **aprovada para este ciclo**.

---

## Verificação do algoritmo de particionamento horizontal

| Exigência | Especificação no handoff | Status |
|---|---|---|
| Entrada como lista de elementos diretos do corpo | `elementos = modelo.corpo.elementos` — Passo 1 | OK |
| Cálculo da largura total disponível | `base_w = total_w // N` — Passo 2 | OK |
| Divisão da largura entre filhos diretos | `larguras = [base_w + (1 if i < resto else 0)...]` — Passo 2 | OK |
| Distribuição de resto deterministicamente (maiores restos) | Fórmula explícita com invariante `sum(larguras) == total_w` — Passo 2 | OK |
| Renderização de cada filho dentro da área alocada | `_caixa_de_elemento(..., inner_w_i, content_w_i, label_max_i)` — Passo 3 | OK |
| Concatenação direta sem separador externo | Passo 5: `linha += linhas[r]` — sem separador | OK |
| Bordas adjacentes coladas (`││`, `╮╭`, `╯╰`) | Passo 5: "Concatenação direta produz bordas adjacentes coladas" | OK |
| Primeira área começa no primeiro caractere útil | Consequência natural do particionamento contíguo | OK |
| Última área termina no último caractere útil | Consequência natural do particionamento contíguo | OK |
| Cada linha final preserva largura total | Invariante: `len(linha) == total_w` — Passo 5 | OK |
| Alturas diferentes preenchidas dentro da área alocada | Passo 4: `linhas.append(" " * larguras[i])` | OK |
| Largura insuficiente gera erro determinístico | Passo 2: `if w < 10: raise RenderizadorErro(...)` com mensagem descritiva | OK |
| Sem truncamento silencioso | "Política para largura insuficiente" + Risk R-7 | OK |
| Sem omissão de elemento | Iteração sobre todos os N filhos diretos | OK |
| Sem reordenação | Iteração na ordem de `elementos[]` | OK |
| Sem fallback silencioso para vertical | Risk R-7 + critério de aceite 8 | OK |

**Confirmação adicional**: `_caixa_de_elemento` (linha 656–683 do renderizador.py)
retorna `None` para qualquer tipo que não seja `console`, `dashboard` ou `lancador`.
Portanto `grupo` retorna `None` e a área alocada fica visualmente vazia — conforme
descrito no handoff e na ADR-0015.

---

## Verificação de aliases transicionais

| Valor JSON | Comportamento loader | Comportamento renderer | Status |
|---|---|---|---|
| `"vertical"` | Aceito (`ARRANJOS_CORPO_VALIDOS`) | Particionamento vertical (atual) | OK |
| `"horizontal"` | Aceito | Particionamento horizontal plano | OK |
| `"sobreposto"` | Aceito | Vertical (alias: normalizado para vertical) | OK |
| `"lado_a_lado"` | Aceito | Horizontal (alias: normalizado para horizontal) | OK |
| `None` / ausente | Aceito | Vertical (default atual) | OK |
| Qualquer outro valor | `TelaEstruturaInvalida` | — | OK |

Normalização de aliases ocorre no **renderer**, não no loader.
O loader apenas aceita o conjunto de valores válidos.
O modelo armazena o valor como declarado (sem normalização).

`lado_a_lado` (literal) aparece apenas como alias transicional — não como
termo normativo em texto livre. "lado a lado" (texto livre) foi removido de
todas as posições normativas. CONFORME.

---

## Verificação de proteção da barra_de_menus

| Artefato | Escopo negativo | Preservações obrigatórias | Proteção explícita | Status |
|---|---|---|---|---|
| `barra_de_menus.distribuicao` | NÃO alterar ✓ (linha 310) | — | — | OK |
| `_normaliza_distribuicao` | NÃO alterar ✓ (linha 311) | Listada ✓ | — | OK |
| `_validar_distribuicao` | NÃO alterar ✓ (linha 312) | Listada ✓ | — | OK |
| `_linhas_barra` | NÃO alterar ✓ (linha 313) | Listada ✓ | — | OK |
| `tela/explorar_barra_de_menus.py` | NÃO refatorar ✓ (linha 314) | Listada ✓ (linha 359) | — | OK |
| `tela/teste_explorar_barra_de_menus.py` | NÃO alterar ✓ (linha 315) | Listada ✓ (linha 360) | — | OK |
| `contrato_barra_de_menus.md` | NÃO alterar ✓ (linha 316) | Listada ✓ (linha 362) | — | OK |
| `contrato_chip.md` | NÃO alterar ✓ (linha 317) | Listada ✓ (linha 363) | — | OK |

**Regra de parada**: "Qualquer necessidade de alterar `_linhas_barra`,
`_normaliza_distribuicao`, `_validar_distribuicao` ou qualquer arquivo da
`barra_de_menus` deve parar com `ARCHITECTURE_REVIEW_REQUIRED`." (linha 368–369)

Proteção explícita e completa. Risco R-1 (confundir `corpo.arranjo = "horizontal"`
com `barra_de_menus.distribuicao`) está documentado com sintoma e mitigação.

---

## Verificação de testes exigidos

| Cenário exigido | Teste listado no handoff | Status |
|---|---|---|
| Loader aceita `horizontal` no corpo raiz | `test_loader_arranjo_horizontal_aceito` | OK |
| Loader aceita `vertical` no corpo raiz | `test_loader_arranjo_vertical_aceito` | OK |
| Loader aceita aliases transicionais literais | `test_loader_arranjo_sobreposto_aceito`, `test_loader_arranjo_lado_a_lado_aceito` | OK |
| Loader rejeita arranjo inválido | `test_loader_arranjo_invalido_diagonal`, `test_loader_arranjo_invalido_string_vazia`, `test_loader_arranjo_invalido_tipo_inteiro` | OK |
| `None` preserva comportamento atual | `test_loader_arranjo_none_aceito` + `test_arranjo_none_preserva_vertical` | OK |
| `vertical` preserva comportamento atual | `test_arranjo_vertical_preserva_comportamento` | OK |
| `sobreposto` preserva comportamento atual | `test_arranjo_sobreposto_preserva_vertical` | OK |
| `horizontal` reparte largura entre filhos diretos | `test_arranjo_horizontal_dois_elementos` | OK |
| `horizontal` gera áreas contíguas sem separador externo | `test_arranjo_horizontal_areas_contiguas` | OK |
| Bordas adjacentes aparecem coladas | `test_arranjo_horizontal_areas_contiguas` (verifica `││`, `╮╭`, `╯╰`) | OK |
| Primeira área começa no primeiro caractere útil | `test_arranjo_horizontal_areas_contiguas` (posição 0) | OK |
| Última área termina no último caractere útil | `test_arranjo_horizontal_areas_contiguas` (posição -1) | OK |
| Linhas renderizadas preservam largura total | `test_arranjo_horizontal_areas_contiguas` (42 chars) | OK |
| Resto de divisão distribuído deterministicamente | `test_arranjo_horizontal_resto_deterministico` (100 // 3 = [34, 33, 33]) | OK |
| Altura desigual recebe preenchimento | `test_arranjo_horizontal_padding_inferior` | OK |
| Largura insuficiente gera erro determinístico | `test_arranjo_horizontal_largura_insuficiente` | OK |
| `barra_de_menus` permanece preservada | `test_arranjo_horizontal_barra_preservada` | OK |
| Baseline completo continua passando | Critério de aceite 12 (544 + novos = zero regressões) | OK |

**Nota**: Caso N=1 (`arranjo = "horizontal"` com um único filho direto) está
especificado no Passo 1 do algoritmo ("renderizar na largura total") mas sem
teste formal correspondente. Ver achado A-002.

---

## Achados

| ID | Severidade | Descrição | Evidência | Impacto | Correção recomendada |
|---|---|---|---|---|---|
| A-001 | NOTA | Comportamento pré-existente de expansão de `grupo` no modo vertical do `renderizador.py` (linhas 779–795 do commit `9d4c74d`) contradiz ADR-0015 Decisão 2. O handoff H-0019 instrui corretamente "preservar comportamento atual" para o modo vertical sem piorar a situação. O algoritmo horizontal introduzido pelo H-0019 NÃO expande grupo. | `renderizador.py` linhas 780–789: `if elemento.tipo == "grupo": for interno in elemento.elementos: ...`; ADR-0015 D2: "grupo recebe área do container pai e redistribui internamente — não é transparente" | Pré-existente; fora do escopo H-0019; H-0019 não agrava a situação. O modo horizontal é correto segundo ADR-0015 | Não corrigir no H-0019. Registrar no IMP-0019 como comportamento pré-existente do modo vertical a ser corrigido em H-0020 ou ciclo específico. |
| A-002 | BAIXO | Caso N=1 com `corpo.arranjo = "horizontal"` está especificado no Passo 1 ("Se N == 1, renderizar na largura total (sem particionamento)") mas não tem teste formal correspondente. O princípio de "sem fallback silencioso" exige que comportamento documentado seja verificável. | Passo 1 do algoritmo define N=1; seção de testes obrigatórios não lista `test_arranjo_horizontal_um_elemento`. Consistente com achado A-003 da auditoria anterior (`RELATORIO_AUDITORIA_H-0019_HANDOFF.md`) | Caso borda sem cobertura de teste formal neste ciclo. N=1 é matematicamente trivial (área total = largura total) mas sem verificação automática | O executor pode adicionar opcionalmente `test_arranjo_horizontal_um_elemento` ao IMP-0019. Se não adicionado, registrar no IMP-0019 que N=1 é caso borda sem teste formal neste ciclo. Não exige correção do handoff. |

**Resumo de achados por severidade:**

| Severidade | Quantidade | Exige correção do handoff |
|---|---|---|
| BLOQUEANTE | 0 | — |
| ALTO | 0 | — |
| MÉDIO | 0 | — |
| BAIXO | 1 (A-002) | Não |
| NOTA | 1 (A-001) | Não |

---

## Decisão

```
APROVADO_COM_NOTAS
```

**Justificativa**:

- Nenhum achado BLOQUEANTE, ALTO ou MÉDIO.
- Achado NOTA A-001 é comportamento pré-existente fora do escopo H-0019;
  H-0019 não piora a situação — o algoritmo horizontal está correto segundo ADR-0015.
- Achado BAIXO A-002 (N=1 sem teste) não compromete a implementação; é
  caso borda com comportamento trivial e documentado.
- Todos os critérios de aprovação estão satisfeitos.

**Critérios de aprovação verificados**:

- [x] Status do handoff revisado é `HANDOFF_REVISED_READY`
- [x] Não há regra ativa de "3 vãos iguais"
- [x] Não há regra ativa de "N+1 vãos"
- [x] "lado a lado" não é termo normativo
- [x] ADR-0015 é autoridade superior
- [x] Distribuição uniforme implícita é compatível com contratos atualizados
- [x] Escopo está limitado ao corpo raiz e filhos diretos
- [x] Grupos hierárquicos estão fora de escopo
- [x] Percentual/fração estão fora de escopo
- [x] Algoritmo de particionamento contíguo está testável
- [x] `barra_de_menus` está protegida
- [x] Não há achado bloqueante, alto ou médio que exija correção

---

## Conclusão

O handoff H-0019 revisado pós-ADR-0015 está apto para implementação com
status `HANDOFF_REVISED_APPROVED_WITH_NOTES`.

A revisão resolveu integralmente os pontos de conflito com a ADR-0015:
grupo não é expandido no algoritmo horizontal, "lado a lado" foi removido
como termo normativo, "3 vãos iguais" e "N+1 vãos" foram rebaixados para
histórico rejeitado, a Opção A de distribuição é compatível com os contratos
vigentes e a proteção da `barra_de_menus` está explícita e completa.

**Condições para implementação**:

1. Esta auditoria deve ser registrada (relatório criado em
   `docs/relatorios/RELATORIO_AUDITORIA_H-0019_POS_REVISAO_ADR-0015.md`).
2. O usuário deve autorizar explicitamente a implementação.
3. O executor deve registrar no IMP-0019 o achado A-001 (comportamento
   pré-existente do modo vertical) e o achado A-002 (N=1 sem teste formal),
   com decisão explícita sobre cada um.
4. A implementação deve partir do estado do repositório em `9d4c74d`.
5. A implementação NÃO deve iniciar antes de receber autorização explícita
   do usuário, conforme este relatório e o handoff revisado.
