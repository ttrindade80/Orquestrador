# IMP-0020 — Preenchimento vertical das áreas alocadas no corpo horizontal

## Status

```
IMPLEMENTATION_COMPLETE
```

---

## Base verificada

| Item | Valor |
|---|---|
| HEAD observado | `624e0a5  docs: registra levantamento pos H-0019` |
| Base declarada no handoff | `624e0a5  docs: registra levantamento pos H-0019` |
| Coincidência | SIM |
| Workspace antes da implementação | `?? docs/handoff/H-0020-preenchimento-vertical-areas-corpo-horizontal.md` + `?? docs/relatorios/RELATORIO_AUDITORIA_H-0020_HANDOFF.md` |
| Workspace esperado declarado | Coincide exatamente |

---

## Arquivos alterados

```
tela/renderizador.py
tela/teste_renderizador.py
docs/relatorios/IMP-0020-preenchimento-vertical-areas-corpo-horizontal.md
```

---

## Resumo da implementação

O H-0020 corrigiu `_montar_corpo_horizontal` em `renderizador.py` para que, em
`corpo.arranjo = "horizontal"`, cada coluna/área alocada seja preenchida
verticalmente até `l_corpo_disponivel` (altura disponível do corpo), não apenas
até `altura_max` (máximo entre colunas). O fill externo H-0015 foi neutralizado
para o modo horizontal com guarda explícita. O comportamento H-0019 (sem
`altura_disponivel`) foi integralmente preservado.

---

## Detalhes técnicos

### Mudanças em `tela/renderizador.py`

**1. `_montar_corpo_horizontal` (linha 686)**

- Assinatura estendida: `def _montar_corpo_horizontal(elementos, borda, total_w, altura_disponivel=None)`
- Parâmetro `altura_disponivel: int | None = None` adicionado.
- Caminho especial N=1 removido: N=1 cai no caminho geral com `larguras=[total_w]`,
  produzindo resultado idêntico ao caminho anterior e agora suportando `altura_disponivel`.
- Adicionada variável `altura_alvo` após `altura_max`:
  - `None` → `altura_alvo = altura_max` (H-0019 preservado)
  - Fornecido → `altura_alvo = altura_disponivel` (ou `altura_max` se conteúdo exceder)
- Loop de fill: `while len(linhas) < altura_alvo` (era `altura_max`)
- Loop de concatenação: `for r in range(altura_alvo)` (era `altura_max`)

**2. `renderizar_tela` (branch horizontal)**

- `linhas_barra = None` inicializado antes do bloco de corpo.
- No branch `if arranjo_corpo == "horizontal":`, quando `altura is not None`:
  - `linhas_barra` pré-computada para derivar `l_barra`
  - `l_cabo` e `l_barra` calculados; verificação `l_cab + l_barra > altura`
  - `_l_corpo_disponivel = altura - l_cab - l_barra` computado
  - `_montar_corpo_horizontal` chamada com `altura_disponivel=_l_corpo_disponivel`
- Quando `altura is None`: `_l_corpo_disponivel = None` → comportamento H-0019

**3. `renderizar_tela` (pós-corpo)**

- Substituição de `linhas_barra = _linhas_barra(...)` por
  `if linhas_barra is None: linhas_barra = _linhas_barra(...)`.
  Evita dupla chamada (R-4) quando já pré-computada no modo horizontal+altura.

**4. `renderizar_tela` (fill H-0015)**

- Guarda explícita adicionada:
  `if l_corpo_fill > 0 and arranjo_corpo != "horizontal":`
- Impede inserção de linhas `" " * total_w` após bloco horizontal já preenchido.

---

## Propagação de altura disponível

Fluxo com `altura` fornecida e `arranjo_corpo == "horizontal"`:

```
1. linhas_barra = _linhas_barra(...)  ← pré-computada no branch horizontal
2. l_cab = _contar_linhas(partes[0])
3. l_barra = len(linhas_barra) + 2
4. Verificação: l_cab + l_barra <= altura
5. _l_corpo_disponivel = altura - l_cab - l_barra
6. bloco = _montar_corpo_horizontal(..., altura_disponivel=_l_corpo_disponivel)
   → altura_alvo = _l_corpo_disponivel
   → cada coluna preenchida até _l_corpo_disponivel linhas
   → bloco retornado tem exatamente _l_corpo_disponivel linhas
7. partes.append(bloco)
8. if linhas_barra is None: ...  ← pula (já computada)
9. Fill H-0015: l_corpo_fill = l_corpo_disponivel - l_corpo_disponivel = 0
   guarda "and arranjo_corpo != 'horizontal'" bloqueia por segurança
10. partes.append(caixa barra)
11. Total = l_cab + _l_corpo_disponivel + l_barra = altura ✓
```

Fluxo com `altura is None` e `arranjo_corpo == "horizontal"` (H-0019 preservado):

```
1. _l_corpo_disponivel = None
2. bloco = _montar_corpo_horizontal(..., altura_disponivel=None)
   → altura_alvo = altura_max (H-0019)
3. linhas_barra = _linhas_barra(...)  ← computada após corpo
4. Fill H-0015: não executa (altura is None)
```

---

## Neutralização do preenchimento externo H-0015 no modo horizontal

Antes do H-0020, o fill H-0015 adicionava `l_corpo_fill` linhas de `" " * total_w`
após o bloco horizontal quando `altura` era fornecida. Isso resultava em linhas
planas sem estrutura de coluna entre o bloco e a barra de menus.

A guarda explícita adicionada:

```python
if l_corpo_fill > 0 and arranjo_corpo != "horizontal":
    partes.append(
        "\n".join(" " * total_w for _ in range(l_corpo_fill))
    )
```

impede a inserção desse fill externo para o modo horizontal. Na prática,
após H-0020, `l_corpo_fill = 0` para casos sem overflow (bloco absorve tudo),
mas a guarda permanece como proteção explícita conforme A-003.

---

## Compatibilidade com H-0019

- `_montar_corpo_horizontal` com `altura_disponivel=None` → `altura_alvo = altura_max`
  → comportamento H-0019 integralmente preservado.
- `test_arranjo_horizontal_padding_inferior` e todos os demais testes de
  `TestArranjoH0019` continuam passando sem alteração.
- N=1 agora cai no caminho geral com `larguras=[total_w]`. Resultado idêntico
  ao caminho especial anterior — verificado pelo teste `test_arranjo_horizontal_n1`.

---

## Compatibilidade com ADR-0015

- **D5** (área alocada preservada): fill interno garante que cada coluna ocupa
  `l_corpo_disponivel` linhas, preservando a área alocada.
- **D9** (bordas adjacentes sem vão): fill `" " * larguras[i]` concatenado
  preserva `len(linha) == total_w` e bordas coladas.
- **D10** (preenchimento vertical dentro da faixa): `altura_alvo` estende o
  fill de cada coluna dentro de sua faixa.
- **D13** (reticências fora de escopo): não implementado; `RenderizadorErro`
  para overflow permanece.

---

## Tratamento das notas da auditoria

### A-001 — NOTA

`contrato_composicao_corpo.md` seção 9 ainda menciona H-0020 para grupos;
referência histórica anterior à redefinição pós-H-0019. H-0020 atual trata
preenchimento vertical das áreas alocadas no corpo horizontal. Grupos
hierárquicos ficam fora de escopo. A tensão normativa documental não afeta
a implementação e será resolvida em ciclo documental futuro.

### A-002 — NOTA

`IMP-0019` usou grafia `_normaliza_distribuicao` sem `r` como inconsistência
documental pré-existente, já registrada no QA-001 do H-0019. H-0020 usa a
grafia correta `_normalizar_distribuicao` (com `r`) em todos os pontos
normativos e não altera a função.

### A-003 — NOTA

A implementação adicionou guarda explícita no ponto de preenchimento externo
do corpo: `if l_corpo_fill > 0 and arranjo_corpo != "horizontal":`. Isso impede
fill externo no modo horizontal já preenchido internamente, conforme mitigação
do risco R-4 documentado no handoff.

---

## Testes executados

| Suíte | Verificações antes | Verificações depois | Exit code |
|---|---|---|---|
| `teste_loader.py` | 89/89 | 89/89 | 0 |
| `teste_modelo.py` | 56/56 | 56/56 | 0 |
| `teste_renderizador.py` | 261/261 | 293/293 | 0 |
| `teste_demo.py` | 117/117 | 117/117 | 0 |
| `teste_diagnostico.py` | 28/28 | 28/28 | 0 |
| `teste_explorar_barra_de_menus.py` | 38/38 | 38/38 | 0 |
| **Total** | **589/589** | **621/621** | **0** |

Novos testes adicionados: 32 (classe `TestPreenchimentoVerticalH0020`, 12 métodos).

---

## Resultado dos testes

```
TODOS OS TESTES PASSARAM
621/621 verificações — 0 falhas
```

---

## Verificação de proteção da barra_de_menus

Funções protegidas verificadas via `git diff -- tela/renderizador.py | grep "^+def\|^-def"`:

```
-def _montar_corpo_horizontal(elementos, borda, total_w):
+def _montar_corpo_horizontal(elementos, borda, total_w, altura_disponivel=None):
```

Somente `_montar_corpo_horizontal` teve assinatura estendida. As funções:

- `_normalizar_distribuicao` — **NÃO ALTERADA** ✓
- `_validar_distribuicao` — **NÃO ALTERADA** ✓
- `_linhas_barra` — **NÃO ALTERADA** ✓ (usada como chamada, não modificada)
- `_validar_ancoras` — **NÃO ALTERADA** ✓

`teste_explorar_barra_de_menus.py`: 38/38 ✓

---

## Verificação de arquivos proibidos

```
git diff --name-only:
  tela/renderizador.py
  tela/teste_renderizador.py
```

Nenhum arquivo proibido alterado. `loader.py`, `modelo.py`, `demo.py`,
`diagnostico.py`, todos os testes protegidos, contratos, ADRs, NOMENCLATURA.md
e config/ permaneceram intactos.

---

## Verificação de caches

```
find . -name '__pycache__' -type d -print  → (sem saída)
find . -name '*.pyc' -print                → (sem saída)
```

Nenhum cache criado pela execução (uso de `PYTHONDONTWRITEBYTECODE=1`).

---

## Verificação final de estado

```
git diff --stat:
  tela/renderizador.py       | 75 ++++++---
  tela/teste_renderizador.py | 314 +++++++++++++++++++++++++++++++++++++
  2 files changed, 369 insertions(+), 20 deletions(-)

git status --short:
  M tela/renderizador.py
  M tela/teste_renderizador.py
  ?? docs/handoff/H-0020-preenchimento-vertical-areas-corpo-horizontal.md
  ?? docs/relatorios/RELATORIO_AUDITORIA_H-0020_HANDOFF.md
  ?? docs/relatorios/IMP-0020-preenchimento-vertical-areas-corpo-horizontal.md
```

---

## Pendências

Nenhuma. Todos os critérios de aceite do handoff foram satisfeitos.

---

## Conclusão

O H-0020 foi implementado conforme especificado. O preenchimento vertical das
áreas alocadas no corpo horizontal agora ocorre **dentro** de cada coluna
(via `_montar_corpo_horizontal` com `altura_disponivel`), não após o bloco como
fill externo do H-0015. O comportamento de H-0019 (sem `altura`) e de H-0015
(modos vertical/None/sobreposto com `altura`) foram integralmente preservados.
As funções protegidas da barra_de_menus permaneceram intocadas.
