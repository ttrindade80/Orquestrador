# RELATORIO_QA_H-0020_PREENCHIMENTO_VERTICAL_AREAS_CORPO_HORIZONTAL

## Status

```
QA_APPROVED
```

---

## Resumo executivo

A implementação do H-0020 está correta, completa e dentro do escopo aprovado. O
preenchimento vertical das áreas alocadas no corpo horizontal foi implementado
internamente em `_montar_corpo_horizontal` via parâmetro `altura_disponivel`. O fill
externo H-0015 foi neutralizado no modo horizontal com guarda explícita. O
comportamento H-0019 (sem `altura`) e H-0015 (modos vertical/None/sobreposto) foram
integralmente preservados. As funções protegidas da barra_de_menus permanecem
intocadas. Todos os 621/621 testes passam. Nenhum arquivo proibido foi alterado.
Nenhum achado bloqueante, alto ou médio.

---

## Base verificada

| Item | Valor |
|---|---|
| HEAD observado | `624e0a5  docs: registra levantamento pos H-0019` |
| Base declarada no handoff | `624e0a5  docs: registra levantamento pos H-0019` |
| Coincidência | SIM |
| Workspace no início do QA | `M tela/renderizador.py`, `M tela/teste_renderizador.py`, `?? docs/handoff/H-0020-...`, `?? docs/relatorios/IMP-0020-...`, `?? docs/relatorios/RELATORIO_AUDITORIA_H-0020_HANDOFF.md` |
| Workspace esperado declarado | Coincide exatamente |

---

## Arquivos analisados

### Handoff, auditoria e IMP

```
docs/handoff/H-0020-preenchimento-vertical-areas-corpo-horizontal.md
docs/relatorios/RELATORIO_AUDITORIA_H-0020_HANDOFF.md
docs/relatorios/IMP-0020-preenchimento-vertical-areas-corpo-horizontal.md
```

### Documentação normativa

```
docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
docs/NOMENCLATURA.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_json_tela_minima.md
```

### Artefatos do H-0019

```
docs/handoff/H-0019-layout-horizontal-plano-corpo.md
docs/relatorios/IMP-0019-layout-horizontal-plano-corpo.md
docs/relatorios/RELATORIO_QA_H-0019_LAYOUT_HORIZONTAL_PLANO_CORPO.md
docs/relatorios/RELATORIO_LEVANTAMENTO_POS_H0019_AJUSTES_LAYOUT_E_DIMENSAO.md
```

### Código — leitura integral

```
tela/renderizador.py  (linhas 1–981 lidas na íntegra)
tela/teste_renderizador.py  (linhas 1–2962 lidas na íntegra)
```

### Lidos para proteção de escopo (não alterar)

```
tela/loader.py
tela/modelo.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_demo.py
tela/teste_diagnostico.py
tela/teste_explorar_barra_de_menus.py
tela/explorar_barra_de_menus.py
```

---

## Comandos executados

### Primeira trava obrigatória

```bash
git log --oneline -8
git status --short
git diff --stat
git diff --name-only
```

**Resultado:**

```
624e0a5 docs: registra levantamento pos H-0019
29a8a79 feat: implementa layout horizontal plano do corpo
9d4c74d docs: formaliza composicao hierarquica do corpo
3b98856 docs: registra levantamento pos H-0018
46e0cb9 feat: cobre distribuicao da barra de menus
c8a20fa test: adiciona explorador da barra de menus
ab5ad68 feat: renderiza barra de menus horizontal responsiva
b2eb458 feat: ocupa altura do terminal pelo corpo
---
 M tela/renderizador.py
 M tela/teste_renderizador.py
?? docs/handoff/H-0020-preenchimento-vertical-areas-corpo-horizontal.md
?? docs/relatorios/IMP-0020-preenchimento-vertical-areas-corpo-horizontal.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0020_HANDOFF.md
---
 scripts/tela/renderizador.py       |  75 ++++++---
 scripts/tela/teste_renderizador.py | 314 +++++++++++++++++++++++++++++++++++++
 2 files changed, 369 insertions(+), 20 deletions(-)
---
scripts/tela/renderizador.py
scripts/tela/teste_renderizador.py
```

Workspace conforme o esperado. QA prosseguido.

### Grep de funções protegidas da barra_de_menus

```bash
git diff -- tela/renderizador.py | grep -n "_normalizar_distribuicao\|_validar_distribuicao\|_linhas_barra\|^+def\|^-def"
```

**Resultado:**

```
9:-def _montar_corpo_horizontal(elementos, borda, total_w):
11:+def _montar_corpo_horizontal(elementos, borda, total_w, altura_disponivel=None):
96:+            linhas_barra = _linhas_barra(modelo.barra_de_menus, content_w)
121:-    linhas_barra = _linhas_barra(modelo.barra_de_menus, content_w)
124:+        linhas_barra = _linhas_barra(modelo.barra_de_menus, content_w)
```

Somente `_montar_corpo_horizontal` teve assinatura estendida (única linha `-def` e `+def`).
`_linhas_barra` aparece como chamada movida/adicionada, mas sua definição não foi
alterada. `_normalizar_distribuicao` e `_validar_distribuicao` não aparecem no diff —
confirmadamente intocadas.

### Caches

```bash
find . -name '__pycache__' -type d -print
find . -name '*.pyc' -print
```

**Resultado:** sem saída — nenhum cache criado (`PYTHONDONTWRITEBYTECODE=1` usado em todas as execuções).

### Estado final do workspace

```bash
git diff --stat
git diff --name-only
git status --short
```

**Resultado:**

```
 scripts/tela/renderizador.py       |  75 ++++++---
 scripts/tela/teste_renderizador.py | 314 +++++++++++++++++++++++++++++++++++++
 2 files changed, 369 insertions(+), 20 deletions(-)
---
scripts/tela/renderizador.py
scripts/tela/teste_renderizador.py
---
 M tela/renderizador.py
 M tela/teste_renderizador.py
?? docs/handoff/H-0020-preenchimento-vertical-areas-corpo-horizontal.md
?? docs/relatorios/IMP-0020-preenchimento-vertical-areas-corpo-horizontal.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0020_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_H-0020_PREENCHIMENTO_VERTICAL_AREAS_CORPO_HORIZONTAL.md
```

---

## Verificação de escopo de arquivos

| Arquivo modificado | Status esperado | Conforme |
|---|---|---|
| `tela/renderizador.py` | M — permitido | ✓ |
| `tela/teste_renderizador.py` | M — permitido | ✓ |
| `docs/relatorios/IMP-0020-preenchimento-vertical-areas-corpo-horizontal.md` | ?? — permitido | ✓ |
| `docs/handoff/H-0020-preenchimento-vertical-areas-corpo-horizontal.md` | ?? — documentação do ciclo | ✓ |
| `docs/relatorios/RELATORIO_AUDITORIA_H-0020_HANDOFF.md` | ?? — documentação do ciclo | ✓ |

Nenhum arquivo proibido alterado. `loader.py`, `modelo.py`, `demo.py`, `diagnostico.py`,
todos os testes protegidos, contratos, ADRs, NOMENCLATURA.md e config/ permanecem
intactos — confirmado pelo diff e pelo git status.

---

## Verificação do renderizador

### Assinatura de `_montar_corpo_horizontal`

Linha 686 do `renderizador.py`:

```python
def _montar_corpo_horizontal(elementos, borda, total_w, altura_disponivel=None):
```

Conforme com a especificação do handoff: parâmetro `altura_disponivel: int | None = None`
adicionado como quarto argumento com default `None`. ✓

### Remoção do caminho especial N=1

O caminho especial para N=1 foi removido. N=1 agora cai no caminho geral com
`larguras=[total_w]`, produzindo resultado idêntico ao anterior e agora suportando
`altura_disponivel`. Verificado via `test_arranjo_horizontal_n1` (passa em 293/293). ✓

### Lógica de `altura_alvo` (linhas 750–756)

```python
altura_alvo = altura_disponivel if altura_disponivel is not None else altura_max
if altura_alvo < altura_max:
    altura_alvo = altura_max

for i, linhas in enumerate(todas_as_linhas_por_area):
    while len(linhas) < altura_alvo:
        linhas.append(" " * larguras[i])
```

- `None` → `altura_alvo = altura_max` — comportamento H-0019 preservado. ✓
- Fornecido → `altura_alvo = altura_disponivel` (ou `altura_max` se conteúdo exceder). ✓
- Sem truncamento silencioso. ✓

### Loop de concatenação (linhas 762–766)

```python
linhas_resultado = []
for r in range(altura_alvo):
    linha = ""
    for linhas in todas_as_linhas_por_area:
        linha += linhas[r]
    linhas_resultado.append(linha)
```

Usa `altura_alvo` — conforme. ✓

### Inicialização de `linhas_barra` (linha 874)

```python
linhas_barra = None
```

Inicializada antes do bloco de corpo — permite pré-computação no modo horizontal com
`altura` fornecida e guarda `if linhas_barra is None:` funcionar corretamente. ✓

### Branch horizontal com `altura` fornecida (linhas 881–900)

```python
if altura is not None:
    linhas_barra = _linhas_barra(modelo.barra_de_menus, content_w)
    l_cab = _contar_linhas(partes[0])
    l_barra = len(linhas_barra) + 2
    if l_cab + l_barra > altura:
        raise RenderizadorErro(...)
    _l_corpo_disponivel = altura - l_cab - l_barra
else:
    _l_corpo_disponivel = None

bloco_horizontal = _montar_corpo_horizontal(
    modelo.corpo.elementos, borda, total_w,
    altura_disponivel=_l_corpo_disponivel,
)
```

Fluxo completo conforme o handoff:
1. Pré-computa `linhas_barra` antecipadamente. ✓
2. Deriva `l_barra`. ✓
3. Verifica `l_cab + l_barra <= altura`. ✓
4. Computa `_l_corpo_disponivel = altura - l_cab - l_barra`. ✓
5. Passa para `_montar_corpo_horizontal`. ✓

### Guarda `if linhas_barra is None:` (linhas 928–929)

```python
if linhas_barra is None:
    linhas_barra = _linhas_barra(modelo.barra_de_menus, content_w)
```

Evita dupla chamada (R-4) quando já pré-computada no modo horizontal com `altura`. ✓

---

## Verificação do preenchimento vertical interno

### Funcionamento geral

Cada coluna em `todas_as_linhas_por_area` é preenchida com `" " * larguras[i]` até
`altura_alvo`. As linhas de preenchimento têm exatamente `larguras[i]` caracteres,
e a concatenação linha a linha preserva `len(linha) == total_w`. ✓

### Verificação de cobertura de casos

| Caso | Comportamento | Confirmado por |
|---|---|---|
| `horizontal` + `altura` fornecida | Cada coluna preenchida até `l_corpo_disponivel` | testes H0020-1, H0020-2, H0020-3, H0020-5, H0020-6 |
| `horizontal` + `altura is None` | Normaliza até `altura_max` (H-0019) | teste H0020-11 |
| `vertical` + `altura` fornecida | Fill externo H-0015 intacto | teste H0020-7 |
| `sobreposto` + `altura` fornecida | Idêntico a `vertical` | teste H0020-8 |
| `None` + `altura` fornecida | Idêntico a `vertical` | teste H0020-9 |
| `lado_a_lado` + `altura` fornecida | Idêntico a `horizontal` (alias) | teste H0020-10 |
| Conteúdo acima de `altura_disponivel` | `altura_alvo = altura_max` (sem truncar) | lógica `if altura_alvo < altura_max:` |

---

## Verificação da neutralização do fill externo H-0015

### Guarda explícita (linhas 962–973)

```python
l_corpo_fill = l_corpo_disponivel - l_corpo_conteudo
if l_corpo_fill > 0 and arranjo_corpo != "horizontal":
    partes.append(
        "\n".join(" " * total_w for _ in range(l_corpo_fill))
    )
```

- Condição `arranjo_corpo != "horizontal"` impede fill externo no modo horizontal. ✓
- Modos `vertical`, `None`, `sobreposto` (normalizados) não são `"horizontal"` — fill
  externo H-0015 preservado. ✓
- Nota: `arranjo_corpo` é a variável normalizada pós-alias (linha 866–870), portanto
  `lado_a_lado` → `"horizontal"` → guarda se aplica. ✓

### Efeito prático com `altura` fornecida no modo horizontal

No fluxo com `altura` fornecida e `arranjo_corpo == "horizontal"`:
- `l_corpo_conteudo` = linhas do bloco = `_l_corpo_disponivel` (absorvido internamente)
- `l_corpo_fill = _l_corpo_disponivel - _l_corpo_disponivel = 0`
- Guarda adicional `and arranjo_corpo != "horizontal"` bloqueia mesmo se `l_corpo_fill > 0`
  por alguma diferença de contagem.

A guarda é determinística e explícita, conforme A-003 da auditoria. ✓

---

## Verificação de aliases transicionais

| Alias | Normalizado para | Linha no código | Conforme |
|---|---|---|---|
| `"sobreposto"` | `"vertical"` | 867–868: `if arranjo_corpo == "sobreposto": arranjo_corpo = "vertical"` | ✓ |
| `"lado_a_lado"` | `"horizontal"` | 869–870: `if arranjo_corpo == "lado_a_lado": arranjo_corpo = "horizontal"` | ✓ |

Normalização local ao renderer — modelo e loader não foram alterados. ✓

---

## Verificação de proteção da barra_de_menus

### Funções protegidas verificadas via diff

```bash
git diff -- tela/renderizador.py | grep -n "_normalizar_distribuicao\|_validar_distribuicao\|_linhas_barra\|^+def\|^-def"
```

| Função | Aparece como `-def` (removida/alterada) | Aparece como `+def` (adicionada/alterada) | Conforme |
|---|---|---|---|
| `_normalizar_distribuicao` | NÃO | NÃO | ✓ NÃO ALTERADA |
| `_validar_distribuicao` | NÃO | NÃO | ✓ NÃO ALTERADA |
| `_linhas_barra` | NÃO | NÃO | ✓ NÃO ALTERADA |
| `_validar_ancoras` | NÃO | NÃO | ✓ NÃO ALTERADA |
| `_montar_corpo_horizontal` | SIM (assinatura estendida) | SIM (assinatura estendida) | ✓ permitido |

`_linhas_barra` aparece como chamada (não como definição) no diff — uso intacto,
nunca modificada. ✓

### Grafia `_normalizar_distribuicao` (com `r`)

O código usa `_normalizar_distribuicao` (com `r`) na linha 249 do `renderizador.py` e
em nenhum lugar do IMP-0020 aparece a grafia incorreta `_normaliza_distribuicao`
(sem `r`) como norma — apenas como nota histórica da inconsistência do IMP-0019. ✓

### Artefatos da barra_de_menus

| Arquivo | Alterado | Conforme |
|---|---|---|
| `tela/explorar_barra_de_menus.py` | Não | ✓ |
| `tela/teste_explorar_barra_de_menus.py` | Não | ✓ |
| `docs/contratos/contrato_barra_de_menus.md` | Não | ✓ |
| `docs/contratos/contrato_chip.md` | Não | ✓ |

---

## Verificação dos testes

### Cobertura dos testes novos (`TestPreenchimentoVerticalH0020`)

12 métodos, 32 verificações. Correspondência com os 13 testes exigidos:

| # handoff | Teste exigido | Método implementado | Conforme |
|---|---|---|---|
| 1 | `test_horizontal_alto_mantém_bordas_ate_altura_disponivel` | `test_horizontal_alto_mantem_bordas_ate_altura_disponivel` | ✓ |
| 2 | `test_horizontal_preenchimento_dentro_das_colunas` | `test_horizontal_preenchimento_dentro_das_colunas` | ✓ |
| 3 | `test_horizontal_sem_linhas_total_w_apos_bloco` | `test_horizontal_sem_linhas_externas_apos_bloco` | ✓ (propósito idêntico) |
| 4 | `test_horizontal_bordas_adjacentes_em_linhas_preenchidas` | `test_horizontal_bordas_adjacentes_em_linhas_preenchidas` | ✓ |
| 5 | `test_horizontal_largura_total_em_todas_linhas_preenchidas` | `test_horizontal_largura_total_em_todas_linhas_preenchidas` | ✓ |
| 6 | `test_horizontal_colunas_diferentes_preenchidas_mesma_altura` | `test_horizontal_colunas_diferentes_preenchidas_mesma_altura` | ✓ |
| 7 | `test_vertical_preserva_comportamento_atual` | `test_vertical_preserva_comportamento_atual` | ✓ |
| 8 | `test_sobreposto_preserva_comportamento_atual` | `test_sobreposto_preserva_comportamento_atual` | ✓ |
| 9 | `test_none_preserva_comportamento_atual` | `test_none_preserva_comportamento_atual` | ✓ |
| 10 | `test_lado_a_lado_preserva_comportamento_horizontal` | `test_lado_a_lado_preserva_comportamento_horizontal` | ✓ |
| 11 | `test_horizontal_sem_altura_preserva_h0019` | `test_horizontal_sem_altura_preserva_h0019` | ✓ |
| 12 | `test_barra_de_menus_preservada_apos_h0020` | `test_barra_de_menus_preservada_apos_h0020` | ✓ |
| 13 | `test_baseline_completo_continua_passando` (verificação de regressão, não teste novo) | Verificado pela execução das 6 suítes: 621/621 | ✓ |

**Nota sobre o teste #3**: O nome implementado é `test_horizontal_sem_linhas_externas_apos_bloco`
em vez de `test_horizontal_sem_linhas_total_w_apos_bloco`. Propósito idêntico: confirmar
que nenhuma linha `" " * total_w` é inserida após o bloco horizontal antes da barra.
Não é achado — o handoff especificou o cenário, não o nome exato.

### Verificação da `TestArranjoH0019` (preservação H-0019)

A classe `TestArranjoH0019` contém 13 métodos invocados em `run_all()`. Em especial:
- `test_arranjo_horizontal_padding_inferior`: confirma normalização até `altura_max` sem
  `altura` fornecida. Continua passando sem alteração. ✓
- `test_arranjo_horizontal_n1`: confirma N=1 na largura total. Continua passando após
  remoção do caminho especial (N=1 cai no geral com `larguras=[total_w]`). ✓
- `test_arranjo_horizontal_com_altura_preserva_h0015`: confirma `altura=40 → 40 linhas`. ✓

---

## Verificação do IMP-0020

| Seção exigida | Presente | Conforme |
|---|---|---|
| Status | `IMPLEMENTATION_COMPLETE` | ✓ |
| Base verificada | Coincidência com `624e0a5` | ✓ |
| Arquivos alterados | `renderizador.py`, `teste_renderizador.py`, `IMP-0020` | ✓ |
| Resumo da implementação | Presente | ✓ |
| Como l_corpo_disponivel foi propagado | Fluxo detalhado presente | ✓ |
| Como o fill H-0015 externo foi neutralizado | Guarda explícita descrita | ✓ |
| Interação com `altura is None` (H-0019) | `altura_alvo = altura_max` quando `None` | ✓ |
| Testes executados (tabela) | 589→621, delta +32, exit 0 | ✓ |
| Resultado dos testes | `621/621` | ✓ |
| Proteção da barra_de_menus | `_normalizar_distribuicao`, `_validar_distribuicao`, `_linhas_barra` não alteradas | ✓ |
| Pendências | Nenhuma | ✓ |
| Conclusão | Presente | ✓ |

### Tratamento das notas da auditoria

| Nota | Tratamento no IMP-0020 | Conforme com handoff |
|---|---|---|
| A-001 | Registrada como nota histórica sobre H-0020 para grupos — tensão documental não afeta implementação | ✓ |
| A-002 | Registrada como inconsistência documental pré-existente do IMP-0019; IMP-0020 usa grafia correta `_normalizar_distribuicao` (com `r`) | ✓ |
| A-003 | Guarda explícita `if l_corpo_fill > 0 and arranjo_corpo != "horizontal":` descrita na seção "Neutralização do preenchimento externo H-0015" | ✓ |

---

## Achados

| ID | Severidade | Descrição | Evidência | Impacto | Correção recomendada |
|---|---|---|---|---|---|
| QA-001 | NOTA | O nome do teste #3 implementado (`test_horizontal_sem_linhas_externas_apos_bloco`) difere do nome especificado no handoff (`test_horizontal_sem_linhas_total_w_apos_bloco`). O propósito e a cobertura são idênticos: verifica que nenhuma linha `" " * total_w` (fill externo) aparece após o bloco horizontal. | Handoff linha 517; `teste_renderizador.py` linha 2687: `def test_horizontal_sem_linhas_externas_apos_bloco(self):` | Nenhum — cenário coberto, comportamento verificado, nomes de testes não são normativos. | Nenhuma ação necessária. |

**Resumo por severidade:**

| Severidade | Quantidade | Bloqueia aprovação |
|---|---|---|
| BLOQUEANTE | 0 | — |
| ALTO | 0 | — |
| MÉDIO | 0 | — |
| BAIXO | 0 | — |
| NOTA | 1 | Não |

---

## Resultado dos testes

| Suíte | Verificações | Exit code |
|---|---|---|
| `teste_loader.py` | 89/89 | 0 |
| `teste_modelo.py` | 56/56 | 0 |
| `teste_renderizador.py` | 293/293 | 0 |
| `teste_demo.py` | 117/117 | 0 |
| `teste_diagnostico.py` | 28/28 | 0 |
| `teste_explorar_barra_de_menus.py` | 38/38 | 0 |
| **TOTAL** | **621/621** | **0** |

**Total informado pelo implementador:** 621/621 — coincide. ✓

**Novos testes em `teste_renderizador.py`:** 293 − 261 = 32 (classe `TestPreenchimentoVerticalH0020`, 12 métodos). ✓

Caches: nenhum `__pycache__` ou `.pyc` encontrado após execução. ✓

---

## Decisão

```
APROVADO
```

**Justificativa:**

- Nenhum arquivo proibido alterado — escopo restrito a `renderizador.py` e
  `teste_renderizador.py`.
- `barra_de_menus` protegida: `_normalizar_distribuicao`, `_validar_distribuicao`,
  `_linhas_barra`, `_validar_ancoras` — definitivamente intocadas.
- Todos os 621/621 testes passam — zero regressões.
- Baseline ampliado (589→621) com zero falhas.
- H-0020 implementa apenas o escopo aprovado: preenchimento vertical interno no modo
  horizontal.
- Fill externo H-0015 preservado para modos vertical/None/sobreposto.
- `_montar_corpo_horizontal` com `altura_disponivel=None` preserva comportamento H-0019.
- Guarda `if l_corpo_fill > 0 and arranjo_corpo != "horizontal":` determinística e
  explícita.
- Aliases `sobreposto` e `lado_a_lado` preservados.
- `TestArranjoH0019` continua passando sem alteração.
- IMP-0020 correto, completo e com tratamento adequado de A-001, A-002, A-003.
- Nenhum achado BLOQUEANTE, ALTO ou MÉDIO.
- Único achado: QA-001 (NOTA) — nome de teste difere do especificado no handoff,
  mas propósito e cobertura são idênticos.

**Critérios de aprovação verificados:**

- [x] Nenhum arquivo proibido alterado
- [x] `barra_de_menus` permanece protegida
- [x] Todos os testes obrigatórios passam (621/621)
- [x] Baseline ampliado sem regressão
- [x] H-0020 implementa apenas o escopo aprovado
- [x] Preenchimento vertical interno funciona no modo horizontal
- [x] Fill externo H-0015 preservado no modo vertical/default
- [x] Nenhum achado bloqueante, alto ou médio

---

## Conclusão

O H-0020 está aprovado. A implementação corrige o preenchimento vertical das áreas
alocadas no corpo horizontal conforme especificado no handoff e aprovado na auditoria.
O preenchimento agora ocorre **dentro** de cada coluna via `_montar_corpo_horizontal`
com `altura_disponivel`, e o fill externo H-0015 foi neutralizado no modo horizontal
com guarda explícita. O comportamento de todos os modos anteriores (H-0019 sem
`altura`, H-0015 em vertical/None/sobreposto) foi integralmente preservado.

O ciclo H-0020 pode ser commitado.
