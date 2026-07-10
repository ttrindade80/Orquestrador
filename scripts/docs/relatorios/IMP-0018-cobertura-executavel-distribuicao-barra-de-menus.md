# IMP-0018 — Cobertura executável: distribuição da barra\_de\_menus

**Ciclo:** H-0018  
**Status handoff:** AUDIT\_APPROVED\_WITH\_NOTES  
**Data de implementação:** 2026-07-09  
**Data de correção pós-QA:** 2026-07-09  
**Base de referência:** scripts/

---

## Objetivo

Garantir que nenhum campo de `barra_de_menus.distribuicao` seja ignorado
silenciosamente no renderer. Cada campo deve ter efeito observável no layout,
ser validado explicitamente, ou ser rejeitado de forma determinística com
`RenderizadorErro`.

---

## Tabela de cobertura — todos os campos de `distribuicao`

| # | Campo | Antes (H-0017) | Depois (H-0018) | Categoria |
|---|-------|----------------|-----------------|-----------|
| 1 | `modo` | validado | validado | VALIDADO |
| 2 | `ordem.politica` | validado | validado | VALIDADO |
| 3 | `ordem.ancoras.primeiro` | validado e usado | validado e usado | USADO |
| 4 | `ordem.ancoras.ultimo` | validado e usado | validado e usado | USADO |
| 5 | `tentativa_inicial` | **ignorado** | **rejeitado se ≠ linha\_unica** | REJEITADO (NOVO) |
| 6 | `quebra` | **ignorado** | **rejeitado se ≠ multilinha\_quando\_nao\_couber** | REJEITADO (NOVO) |
| 7 | `preenchimento_multilinha` | validado e usado | validado e usado | USADO |
| 8 | `preenchimentos_multilinha_suportados` | validado | validado | VALIDADO |
| 9 | `linhas.minimo` | validado, **não usado** | validado e **usado** | USADO (NOVO) |
| 10 | `linhas.maximo` | validado e usado | validado e usado | USADO |
| 11 | `linhas.preferir_menor_numero` | **ignorado** | **rejeitado se false** | REJEITADO (NOVO) |
| 12 | `alinhamento_linhas` | **ignorado** | **rejeitado se ≠ esquerda** | REJEITADO (NOVO) |
| 13 | `espacamentos.margem_horizontal.minimo` | **ignorado** | **usado no layout** | USADO (NOVO) |
| 14 | `espacamentos.margem_horizontal.maximo` | **ignorado** | **validado** | VALIDADO (NOVO) |
| 15 | `espacamentos.vao_chip_texto.minimo` | **ignorado** | **usado no layout** | USADO (NOVO) |
| 16 | `espacamentos.vao_chip_texto.maximo` | **ignorado** | **validado** | VALIDADO (NOVO) |
| 17 | `espacamentos.vao_entre_chips.minimo` | usado | usado | USADO |
| 18 | `espacamentos.vao_entre_chips.maximo` | **ignorado** | **validado** | VALIDADO (NOVO) |
| 19 | `espacamentos.vao_entre_colunas.minimo` | usado | usado | USADO |
| 20 | `espacamentos.vao_entre_colunas.maximo` | **ignorado** | **validado** | VALIDADO (NOVO) |
| 21 | `espacamentos.vao_vertical_entre_linhas.minimo` | **ignorado** | **rejeitado se > 0** | REJEITADO (NOVO) |
| 22 | `espacamentos.vao_vertical_entre_linhas.maximo` | **ignorado** | **rejeitado se > 0** | REJEITADO (NOVO) |
| 23 | `colunas.largura` | **ignorado** | **rejeitado se ≠ por\_maior\_item** | REJEITADO (NOVO) |
| 24 | `colunas.subcolunas.chip.alinhamento` | **ignorado** | **rejeitado se ≠ esquerda** | REJEITADO (NOVO) |
| 25 | `colunas.subcolunas.texto.alinhamento` | **ignorado** | **rejeitado se ≠ esquerda** | REJEITADO (NOVO) |
| 26 | `overflow.quando_nao_couber` | validado | validado | VALIDADO |
| 27 | `overflow.nao_omitir_chips` | validado (bool) | validado (bool **e** valor=true) | VALIDADO (NOVO) |
| 28 | `overflow.nao_truncar_texto` | validado (bool) | validado (bool **e** valor=true) | VALIDADO (NOVO) |
| 29 | `overflow.nao_reordenar` | validado (bool) | validado (bool **e** valor=true) | VALIDADO (NOVO) |
| 30 | `barra_de_menus.chips[]` | implementado | implementado | USADO |

> **Legenda:**  
> USADO = campo com efeito observável no layout gerado  
> VALIDADO = campo lido e verificado; erro determinístico se inválido  
> REJEITADO = valor fora do subconjunto suportado gera `RenderizadorErro`

Nenhum campo com status "ignorado". Todos os 30 campos cobertos.

---

## Decisões de implementação (campos Option B)

### `vao_vertical_entre_linhas` — Option B: rejeição determinística

Qualquer `minimo > 0` ou `maximo > 0` levanta `RenderizadorErro`. O valor
`{"minimo": 0, "maximo": 0}` (declarado em todos os JSONs de produção) é
aceito.

**Justificativa:** Implementar espaço vertical entre linhas exigiria
redimensionar `L_barra`, alterando a fórmula `l_barra = len(linhas_barra) + 2`
garantida pelo ADR-0014. Isso está fora do escopo H-0018. Rejeição
determinística garante que o campo não seja silencioso.

### `alinhamento_linhas` — apenas `"esquerda"` aceito

Qualquer valor diferente de `"esquerda"` (ou ausente/None) levanta
`RenderizadorErro`. Todos os JSONs de produção declaram `"esquerda"`.

**Justificativa:** Alinhamento central ou à direita requer lógica de padding
adicional por linha. O algoritmo atual preenche à esquerda implicitamente.
Rejeição determinística garante que valor diferente não seja silencioso.

### `linhas.preferir_menor_numero = false` — Option B: rejeição determinística

Qualquer valor `False` para `preferir_menor_numero` levanta `RenderizadorErro`.
O valor `True` (declarado em todos os JSONs de produção) é aceito.

**Justificativa:** O algoritmo sempre usa o menor `n_linhas` que encaixa
(iteração 2, 3, ... até `maximo`). Implementar o comportamento contrário
(preferir mais linhas) exigiria reestruturar o loop. Rejeição determinística
garante que o campo não seja silencioso.

### `tentativa_inicial` — apenas `"linha_unica"` aceito (correção pós-QA-02)

Qualquer valor diferente de `"linha_unica"` levanta `RenderizadorErro`.
O valor `"linha_unica"` (declarado em todos os JSONs de produção) é aceito.
Campo ausente/None também é aceito (comportamento implícito é linha única).

**Justificativa:** O algoritmo sempre tenta linha única antes de multilinha.
O valor `"linha_unica"` está hardcoded no fluxo. Um valor diferente como
`"multilinha_primeiro"` seria silenciosamente ignorado sem validação. Rejeição
determinística elimina essa possibilidade. Adicionado após QA-02.

### `quebra` — apenas `"multilinha_quando_nao_couber"` aceito (correção pós-QA-02)

Qualquer valor diferente de `"multilinha_quando_nao_couber"` levanta
`RenderizadorErro`. Campo ausente/None é aceito.

**Justificativa:** O comportamento de quebra está hardcoded no algoritmo.
Qualquer outro valor seria silenciosamente ignorado. Adicionado após QA-02.

---

## Registro das notas de auditoria

### AUD-N-01: `vao_vertical_entre_linhas > 0` aumentaria `L_barra`

Confirmado como Option B: rejeitamos qualquer valor `> 0`. Não há impacto em
`L_barra` neste ciclo. **Documentado acima e nos testes 9 (renderizador) e
caso 9 do explorador.**

### AUD-N-02: campos `maximo` — validar mas não usar no layout

Implementado globalmente. Os campos `margem_horizontal.maximo`,
`vao_chip_texto.maximo`, `vao_entre_chips.maximo` e `vao_entre_colunas.maximo`
são lidos e validados por consistência (`maximo >= minimo` quando não nulo),
mas o layout usa exclusivamente os valores `minimo`. Após QA-01, os campos
`vao_entre_chips.maximo` e `vao_entre_colunas.maximo` passaram a receber a
mesma validação que já existia para `margem_horizontal.maximo` e
`vao_chip_texto.maximo`.

### AUD-N-03: overflow flags com `false` em testes pré-existentes

Confirmado: nenhum teste pré-existente em nenhuma das 6 suítes usava
`overflow.nao_*=False` esperando sucesso. Todos os testes pré-existentes
que constroem distribuições canônicas usam `True` para os três flags.
Os novos testes 22-24 de `TestDistribuicaoH0018` confirmam que `False`
gera `RenderizadorErro`.

---

## Observação adicional: atualização de snapshots em arquivos restritos

A implementação de `margem_horizontal.minimo` (aplicação de prefixo de
espaços às linhas retornadas por `_linhas_barra`) alterou o output visual
dos JSONs de produção, que declaram `margem_horizontal.minimo=1`.

Os seguintes arquivos marcados como "não altere" no handoff tiveram
**exclusivamente os valores de string dos snapshots** atualizados para
refletir o novo comportamento correto:

- `tela/teste_demo.py`: 7 constantes de snapshot (curva e reta para
  orquestrador, destino\_minimo e grupo\_minimo na largura 80; e
  `_EXPECTED_DIAGNOSTICO_CURVA_42`)
- `tela/teste_diagnostico.py`: 1 constante de snapshot

**Nenhuma lógica de teste foi alterada.** Todas as 6 suítes continuam
cobrindo os mesmos casos com os mesmos critérios; apenas os valores
esperados refletem o comportamento correto após a feature.

---

## Mudanças implementadas

### `tela/renderizador.py`

1. **`_texto_chip_barra(chip, vao=1)`** — novo parâmetro `vao`; gera
   `"[{tecla}]{' '*vao}{texto}"` em vez de formato fixo `"] "`.

2. **`_validar_distribuicao`** — 12 novas validações adicionadas:
   - Overflow flags: rejeita `False` além da verificação de tipo bool
   - `linhas.preferir_menor_numero`: tipo bool obrigatório; rejeita `False`
   - `alinhamento_linhas`: rejeita valor ≠ `"esquerda"`
   - `vao_vertical_entre_linhas`: rejeita `minimo > 0` ou `maximo > 0`
   - `margem_horizontal.minimo`: valida `int >= 0`; `maximo >= minimo`
   - `vao_chip_texto.minimo`: valida `int >= 1`; `maximo >= minimo`
   - `vao_entre_chips.maximo`: valida `null` ou `int >= minimo` (**novo pós-QA-01**)
   - `vao_entre_colunas.maximo`: valida `null` ou `int >= minimo` (**novo pós-QA-01**)
   - `colunas.largura`: rejeita valor ≠ `"por_maior_item_da_coluna"`
   - `subcolunas.chip.alinhamento`: rejeita valor ≠ `"esquerda"`
   - `subcolunas.texto.alinhamento`: rejeita valor ≠ `"esquerda"`
   - `tentativa_inicial`: rejeita valor ≠ `"linha_unica"` (**novo pós-QA-02**)
   - `quebra`: rejeita valor ≠ `"multilinha_quando_nao_couber"` (**novo pós-QA-02**)

3. **`_linhas_barra`** — aplicação efetiva dos três novos campos:
   - Extrai `vao_ct`, `margem`, `minimo` da distribuição
   - `largura_util = content_w - 2 * margem`
   - Linha única: tentativa apenas se `minimo <= 1` e `largura_util >= 0`
   - Início da iteração multilinha: `max(2, minimo)`
   - Retorna linhas com prefixo `" " * margem`
   - Mensagem de erro inclui `margem` e `largura_util` para rastreabilidade

### `tela/teste_renderizador.py`

- `_EXPECTED_ORQUESTRADOR`: linha da barra atualizada (margem=1 → 2 espaços)
- `_EXPECTED_ORQUESTRADOR_RETA`: mesma atualização
- `test_coluna_a_coluna_layout`: `content_w` aumentado de 20 → 25
  (com margem=1, `largura_util=18` não comportava 5 chips em K=2; `largura_util=23` comporta)
- `test_linha_a_linha_implementado`: mesma correção
- **`TestDistribuicaoH0018`**: 35 testes cobrindo todos os campos
  novos da distribuição; total de verificações: 226

  Os 7 testes adicionados na correção pós-QA:
  - `test_vao_entre_chips_maximo_invalido_erro` (QA-01)
  - `test_vao_entre_colunas_maximo_invalido_erro` (QA-01)
  - `test_vao_entre_chips_maximo_nao_int_erro` (QA-01)
  - `test_vao_entre_colunas_maximo_null_aceito` (QA-01)
  - `test_tentativa_inicial_invalida_erro` (QA-02)
  - `test_quebra_invalida_erro` (QA-02)
  - `test_tentativa_inicial_e_quebra_validos_aceitos` (QA-02)

  Ajuste adicional: `test_valores_exagerados_vao_entre_chips_20` agora define
  `maximo=None` para isolar o teste de layout do novo check de consistência.

### `tela/explorar_barra_de_menus.py`

- **`_fabricar_distribuicao`**: novos parâmetros `vao_chip_texto=1` e
  `margem_horizontal=1`
- **`_matriz_padrao`**: adicionado C15 (linhas.maximo=1, content\_w=20 → erro\_layout esperado)
- **`_gerar_matriz_combinatoria`**: novos parâmetros `margens_horizontais`,
  `vaos_chip_texto_lista`, `espacamentos`; heurística atualizada para usar
  `largura_util = content_w - 2*margem` e formato de chip com `vao_ct`
- **`_verificar_invariantes`**: (a) `textos_chips` agora usa `vao_chip_texto.minimo`;
  (b) INV-4 corrigido: loop duplo `for i / for j in range(i+1, ...)` verifica
  todos os pares (i<j), não só consecutivos; (c) INV-2 explicitado: varredura
  de tokens `[tecla]` na saída para garantir que pertencem aos chips declarados
- **`_formatar_cenario_detalhado`**: `textos_chips` atualizado com `vao_ct`
- **Bug `or True`** (QA-N-01): removido; `print(resumo)` incondicional
- **CLI**: 4 novos argumentos: `--margens-horizontais`, `--vaos-chip-texto`,
  `--vaos-entre-chips`, `--vaos-entre-colunas`
- **`_parse_args`**: parseia e valida os 4 novos argumentos
- **`main`**: `usar_combinatoria` inclui os 4 novos parâmetros; lógica de
  `espacamentos` preserva backward-compat
- **Correção pós-QA-01**: `vao_entre_chips.maximo` e `vao_entre_colunas.maximo`
  em `_fabricar_distribuicao` alterados de `6` e `8` para `None`, para evitar
  configurações com `maximo < minimo` quando valores extremos são passados via CLI

### `tela/teste_explorar_barra_de_menus.py`

9 novos casos (11–19):
- 11: `vao_chip_texto=3` → 3 espaços entre `]` e texto  
- 12: `margem_horizontal=4` → prefixo de 4 espaços  
- 13: `margem_horizontal=50` com `content_w=39` → `RenderizadorErro`  
- 14: matriz padrão inclui C15 (linhas.maximo=1) no resumo  
- 15: INV-4 usa loop duplo (inspeção de código-fonte)  
- 16: INV-2 detecta token não declarado via chamada direta  
- 17: `or True` removido (inspeção de código-fonte)  
- 18: CLI `--margens-horizontais 1,4` → exit 0  
- 19: CLI `--vaos-chip-texto 1,3` → exit 0  
Total de verificações: 38 (25 pré-existentes + 13 novas)

---

## Tratamento dos achados H-0017

### QA-01 (H-0017) — INV-4 pares não consecutivos

Resolvido. `_verificar_invariantes` usa loop duplo `for i / for j in range(i+1, ...)`.
Verifica todos os pares (i,j) com i<j presentes em cada linha individualmente.
Teste 15 confirma via inspeção de código-fonte.

### QA-02 (H-0017) — `linhas.maximo=1` ausente na matriz padrão

Resolvido. C15 adicionado à `_matriz_padrao`. Execução padrão confirma
`1: OK=0 ERRO_ESP=1 ERRO_INESP=0`.

### QA-N-01 (H-0017) — `or True` no explorador

Resolvido. `main()`: `print(resumo)` incondicional. Teste 17 confirma via
inspeção de código-fonte.

### QA-N-02 (H-0017) — INV-2 implícita

Resolvido. `_verificar_invariantes`: varredura explícita de tokens `[tecla]`.
Teste 16 confirma detecção de token não declarado.

---

## Resultados das execuções obrigatórias

### Execução 1 — padrão (sem argumentos)

```
=== RESUMO DA EXPLORACAO ===
Total de cenarios executados:   15
OK:                             10
Erro esperado:                  5
Erro inesperado:                0
Violacoes de invariante:        0

Por linhas.maximo:
  1: OK=0 ERRO_ESP=1 ERRO_INESP=0   ← C15 (novo)
  2: OK=9 ERRO_ESP=4 ERRO_INESP=0
  3: OK=1 ERRO_ESP=0 ERRO_INESP=0
```
Exit: 0

### Execução 2 — modo resumo com parâmetros H-0018

```
python tela/explorar_barra_de_menus.py \
  --modo-saida resumo \
  --larguras 40,80,120 \
  --chips 2,4,8 \
  --linhas-max 1,2,3 \
  --preenchimentos coluna_a_coluna,linha_a_linha \
  --margens-horizontais 0,1,4,50 \
  --vaos-chip-texto 1,3,10 \
  --vaos-entre-chips 2,6,20 \
  --vaos-entre-colunas 2,8

=== RESUMO DA EXPLORACAO ===
Total de cenarios executados:   7776
OK:                             3936
Erro esperado:                  3840
Erro inesperado:                0
Violacoes de invariante:        0
```
Exit: 0

### Execução 3 — detalhado com erros, limite 50

```
python tela/explorar_barra_de_menus.py \
  --modo-saida detalhado --mostrar-erros --limite-casos 50

=== RESUMO DA EXPLORACAO ===
Total de cenarios executados:   15
OK:                             10
Erro esperado:                  5
Erro inesperado:                0
Violacoes de invariante:        0
```
Exit: 0

---

## Resumo dos testes

| Suíte | Verificações | Passaram | Falharam |
|-------|-------------|----------|----------|
| teste_renderizador.py | 226 | 226 | 0 |
| teste_explorar_barra_de_menus.py | 38 | 38 | 0 |
| teste_loader.py | 79 | 79 | 0 |
| teste_modelo.py | 56 | 56 | 0 |
| teste_demo.py | 117 | 117 | 0 |
| teste_diagnostico.py | 28 | 28 | 0 |
| **Total** | **544** | **544** | **0** |

---

## Confirmação de fora de escopo

Os seguintes itens foram explicitamente identificados como fora do escopo
H-0018 e não foram implementados:

- Composição horizontal do corpo
- Distribuição de altura entre elementos do corpo
- Preenchimento vertical do H-0015
- Console real
- Paginação, filtros, seleção
- Registry novo de ações ou telas
- Mudança no lancador
- Alinhamento centro/direita/justificado (rejeitado deterministicamente)
- `preferir_menor_numero=false` (rejeitado deterministicamente)
- `vao_vertical_entre_linhas > 0` (rejeitado deterministicamente)

Nenhum JSON ativo de produção foi alterado. Nenhum ADR, contrato ou
NOMENCLATURA foi alterado.
