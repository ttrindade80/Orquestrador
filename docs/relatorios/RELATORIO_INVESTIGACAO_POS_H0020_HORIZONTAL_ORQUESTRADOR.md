# RELATORIO_INVESTIGACAO_POS_H0020_HORIZONTAL_ORQUESTRADOR

## Status

```
INVESTIGACAO_CONCLUIDA
```

---

## Base verificada

| Item | Valor |
|---|---|
| HEAD observado | `79063ba  fix: preenche areas horizontais do corpo` |
| Workspace | limpo (sem modificações) |
| Testes antes da investigação | 621/621 (todas as 6 suítes) |

---

## Situação do workspace

```
git status --short
(sem saída — workspace limpo)
```

Situação A confirmada. Nenhum arquivo foi alterado pelo usuário antes da investigação.

---

## Objetivo

Determinar por que o teste manual do `orquestrador.json` com
`corpo.arranjo = "horizontal"` ou `"lado_a_lado"` não apresenta
o preenchimento vertical interno esperado após o H-0020.

---

## Contexto do teste manual

O usuário alterou temporariamente `config/telas/orquestrador.json`
(campo `corpo.arranjo`) de `"vertical"` para `"horizontal"` e também
testou com o alias `"lado_a_lado"`. Em ambos os casos, o resultado
exibido continuou com espaços verticais que visualmente aparecem fora
das caixas horizontais — o preenchimento vertical interno do arranjo
horizontal não foi percebido como diferente do comportamento pré-H-0020.

---

## Arquivos analisados

```
docs/handoff/H-0020-preenchimento-vertical-areas-corpo-horizontal.md
docs/relatorios/IMP-0020-preenchimento-vertical-areas-corpo-horizontal.md
docs/relatorios/RELATORIO_QA_H-0020_PREENCHIMENTO_VERTICAL_AREAS_CORPO_HORIZONTAL.md
docs/handoff/H-0019-layout-horizontal-plano-corpo.md
docs/relatorios/IMP-0019-layout-horizontal-plano-corpo.md
tela/renderizador.py  (integralmente — 981 linhas)
tela/demo.py          (integralmente — 250 linhas)
tela/teste_renderizador.py  (seleção de linhas relevantes)
config/telas/orquestrador.json
```

---

## Comandos executados

### Trava obrigatória

```
git log --oneline -10
→ 79063ba fix: preenche areas horizontais do corpo  (HEAD)
  624e0a5 docs: registra levantamento pos H-0019
  29a8a79 feat: implementa layout horizontal plano do corpo
  ...

git status --short
→ (sem saída)

git diff --stat
→ (sem saída)

git diff --name-only
→ (sem saída)
```

### Grep obrigatório de funções-chave

```bash
grep -RIn "def renderizar_tela|_montar_corpo_horizontal|l_corpo_disponivel|
           altura_disponivel|l_corpo_fill|arranjo_corpo" \
    tela/renderizador.py tela/demo.py tela/teste_renderizador.py
```

Resultados relevantes:

| Arquivo | Linha | Ocorrência |
|---|---|---|
| `renderizador.py` | 686 | `def _montar_corpo_horizontal(elementos, borda, total_w, altura_disponivel=None)` |
| `renderizador.py` | 750 | `altura_alvo = altura_disponivel if altura_disponivel is not None else altura_max` |
| `renderizador.py` | 866 | `arranjo_corpo = modelo.corpo.arranjo` |
| `renderizador.py` | 876 | `if arranjo_corpo == "horizontal":` |
| `renderizador.py` | 892 | `_l_corpo_disponivel = altura - l_cab - l_barra` |
| `renderizador.py` | 896–899 | `_montar_corpo_horizontal(..., altura_disponivel=_l_corpo_disponivel)` |
| `renderizador.py` | 961–972 | fill H-0015 com guarda `arranjo_corpo != "horizontal"` |
| `demo.py` | 217–219 | `shutil.get_terminal_size()` → `largura`, `altura` |
| `demo.py` | 221 | `renderizar_estado(estado, modelo, largura, altura=altura)` |

### Grep do orquestrador.json

```bash
grep -n '"arranjo"|"elementos"|"tipo"|"grupo"|"console"|"dashboard"|"lancador"' \
    config/telas/orquestrador.json
```

Resultado (linhas relevantes):
```
24:    "arranjo": "vertical",
25:    "elementos": [
28:        "tipo": "console",
65:        "tipo": "dashboard",
102:       "tipo": "lancador",
```

### Execução dos testes mínimos

```
PYTHONDONTWRITEBYTECODE=1 python tela/teste_renderizador.py
→ Total de verificacoes: 293 / Passaram: 293 / Falharam: 0

PYTHONDONTWRITEBYTECODE=1 python tela/teste_demo.py
→ Total de verificacoes: 117 / Passaram: 117 / Falharam: 0
```

---

## Reprodução controlada

Snippet Python em memória (sem alterar arquivos persistentes):

```python
tela_raw = carregar_tela(None, 'orquestrador')
tela_raw['corpo']['arranjo'] = 'horizontal'  # ajuste em memória
modelo = construir_modelo(tela_raw)
saida = renderizar_tela(modelo, tipo_borda='curva', largura=80, altura=30)
```

### Parâmetros usados

| Parâmetro | Valor |
|---|---|
| `largura` | 80 |
| `altura` | 30 |
| `arranjo` | `"horizontal"` (ajustado em memória) |
| filhos diretos | 3 (`console`, `dashboard`, `lancador`) |
| tipos dos filhos | `console_principal`, `dashboard_info`, `lancador_principal` |
| `l_cab` | 3 |
| `l_barra` | 3 |
| `l_corpo_disponivel` | 24 (= 30 − 3 − 3) |
| linhas do bloco retornado | 24 ✓ (correto) |

### Saída observada (linhas do corpo, 3 a 26)

```
  3: ╭ ITENS ──────────────────╮╭ INFO ───────────────────╮╭ NAVEGAR ───────────────╮
  4: │ (console)               │╰─────────────────────────╯│ [d] Destino            │
  5: ╰─────────────────────────╯                           │ [g] Grupo Min.         │
  6:                                                       ╰────────────────────────╯
  7:                                                                                 
  8:                                                                                 
  9:                                                                                 
 ... (linhas 7 a 26 são espaços — 20 linhas de 80 espaços)
```

### Estado das linhas de fill (7 a 26)

- `len(linha)` = 80 ✓ (correto por coluna: 27+27+26 = 80)
- `linha.strip() == ""` = True para todas
- Visualmente: **indistinguíveis do fill externo H-0015** (`" " * total_w`)

### Verificação lado_a_lado

```python
tela_raw['corpo']['arranjo'] = 'lado_a_lado'
saida_lado == saida_horizontal  # True
```

O alias produz saída **idêntica**.

### Preenchimento visual esperado vs. obtido

**Obtido (com H-0020):**
```
╭ ITENS ─────────────╮╭ INFO ──────────────╮╭ NAVEGAR ────────────╮
│ (console)           │╰────────────────────╯│ [d] Destino         │
╰─────────────────────╯                      │ [g] Grupo Min.      │
                                             ╰─────────────────────╯
          (20 linhas de espaços em branco — " " * 80)
```

**Esperado pela "Regra visual esperada" do H-0020:**
```
╭ ITENS ─────────────╮╭ INFO ──────────────╮╭ NAVEGAR ────────────╮
│ (console)           ││                    ││ [d] Destino         │
│                     ││                    ││ [g] Grupo Min.      │
│                     ││                    ││                     │
│                     ││                    ││                     │
...
╰─────────────────────╯╰────────────────────╯╰─────────────────────╯
```

---

## Hipótese H1 — Demo não passa altura disponível

**Status: DESCARTADA**

`demo.py` linhas 217–221:

```python
tamanho_terminal = shutil.get_terminal_size(fallback=(80, 24))
largura = tamanho_terminal.columns
altura = tamanho_terminal.lines
modelo = _carregar_modelo_por_id(estado["tela_atual"])
print(renderizar_estado(estado, modelo, largura, altura=altura), end="")
```

`renderizar_estado` (linhas 166–178):
```python
def renderizar_estado(estado, modelo, largura=None, altura=None):
    return renderizar_tela(
        modelo, tipo_borda=estado["tipo_borda"], largura=largura, altura=altura
    )
```

A altura real do terminal chega corretamente ao renderizador. A reprodução
confirma: com `largura=80, altura=30`, `_l_corpo_disponivel=24` é computado
e o bloco tem exatamente 24 linhas.

---

## Hipótese H2 — Altura não chega ao branch horizontal

**Status: DESCARTADA**

Em `renderizador.py` linhas 876–901:

```python
if arranjo_corpo == "horizontal":
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

O branch horizontal calcula `_l_corpo_disponivel` corretamente e o passa
para `_montar_corpo_horizontal`. A guarda `if l_corpo_fill > 0 and arranjo_corpo != "horizontal":` (linha 962) bloqueia o fill externo H-0015.

O fluxo real com `orquestrador.json` em horizontal chega ao branch correto
e `_montar_corpo_horizontal` é chamada com `altura_disponivel=24`. O bloco
retornado tem 24 linhas. **O código segue o caminho correto.**

---

## Hipótese H3 — Estrutura do orquestrador não coberta

**Status: PARCIALMENTE CONFIRMADA (causa secundária)**

`orquestrador.json` tem **3 filhos diretos** em `corpo.elementos[]`:

| Índice | id | tipo | linhas geradas por `_caixa` |
|---|---|---|---|
| 0 | `console_principal` | `console` | 3 (topo + `"(console)"` + base) |
| 1 | `dashboard_info` | `dashboard` | 2 (topo + base; todos os campos têm `fonte: "pendente"`, sem literal) |
| 2 | `lancador_principal` | `lancador` | 4 (topo + `"[d] Destino"` + `"[g] Grupo Min."` + base) |

Com `total_w=80`: `larguras=[27, 27, 26]`. `altura_max=4`.

Nenhum filho é do tipo `grupo`. A estrutura é processada corretamente pelo
algoritmo — o problema não é de estrutura incompatível, mas de cobertura de
teste (H4) e de implementação incompleta do visual (H6).

A fixture típica dos testes H-0020 usa 2 elementos `console`+`console`,
ambos com mesma altura (3 linhas). O caso real com 3 elementos de alturas
diferentes (3, 2, 4) e `dashboard` sem conteúdo literal não é coberto.

---

## Hipótese H4 — Lacuna de cobertura nos testes

**Status: CONFIRMADA (causa secundária)**

A classe `TestPreenchimentoVerticalH0020` usa exclusivamente `_modelo_horizontal()`
(fixture sintética, linha 2254). Os modelos criados:
- Têm 1 chip simples (`[k] Ok`)
- Usam apenas tipos `console` e `console` (ou `console`+`dashboard`) com títulos simples
- Não carregam `orquestrador.json` do disco

Nenhum teste exercita o pipeline de integração:

```
carregar_tela(None, 'orquestrador')
  → construir_modelo(tela_raw com arranjo='horizontal')
    → renderizar_tela(modelo, largura=W, altura=H)
```

Os testes verificam:
- `len(corpo) == l_corpo_disponivel` ✓
- `len(bloco) == l_corpo_disponivel` ✓
- Ausência de fill externo após o bloco ✓

Mas **não verificam** que as linhas de fill possuem bordas laterais
(`│` e `│`). Esta verificação exporia a diferença entre o visual implementado
e o visual esperado pela spec.

---

## Hipótese H5 — Alias lado_a_lado segue o mesmo caminho

**Status: CONFIRMADA**

`renderizador.py` linhas 869–870:
```python
if arranjo_corpo == "lado_a_lado":
    arranjo_corpo = "horizontal"
```

A reprodução confirma `saida_lado_a_lado == saida_horizontal` (True).
O problema observado pelo usuário é idêntico para ambos os valores.
Não há falha específica do alias — ele segue exatamente o mesmo caminho
do `"horizontal"`.

---

## Hipótese H6 — Elementos funcionais não preenchem moldura até a altura

**Status: CONFIRMADA (causa principal)**

Esta é a causa raiz da falha visual observada.

### O que o H-0020 implementou

O fill é `" " * larguras[i]` por coluna (especificado no handoff H-0020,
passo 4). Ao concatenar colunas linha a linha:

```
" " * larguras[0] + " " * larguras[1] + " " * larguras[2]
= " " * 27       + " " * 27           + " " * 26
= " " * 80  (= " " * total_w)
```

As linhas de fill são **visualmente idênticas ao fill externo H-0015**
que o H-0020 pretendia corrigir.

### Por que o visual esperado não é atingido

A `_caixa()` (linha 172) gera caixas **completas**: topo + conteúdo + base.
A base (`╰╯`) é gerada imediatamente após o último item de conteúdo.
O fill adicionado em `_montar_corpo_horizontal` vai **após** a base:

```
[topo    ]  line 0
[content ]  line 1
[base ╰╯ ]  line 2  ← base aqui, não na última linha
[" " * w ]  line 3  ← fill SEM borda
[" " * w ]  line 4
...
```

Resultado visual:
```
╭────╮  (linha 0: topo)
│ X  │  (linha 1: conteúdo)
╰────╯  (linha 2: base — box FECHA AQUI)
        (linhas 3+: espaços sem bordas)
```

### O que seria necessário para o visual esperado

A "Regra visual esperada" do H-0020 mostra:
```
╭────────╮╭────────╮
│ item A ││ item B │
│        ││        │  ← fill COM bordas laterais
│        ││        │
╰────────╯╰────────╯  ← base na ÚLTIMA linha
```

Para isso, `_montar_corpo_horizontal` precisaria:
1. Gerar **topo + conteúdo** (sem base) para cada coluna.
2. Preencher com `borda["v"] + " " * (w − 2) + borda["v"]` até `altura_alvo − 1`.
3. Append de `_linha_base(borda, w − 2)` como linha `altura_alvo − 1` de cada coluna.

Isso exige decompor `_caixa()` em duas partes — não foi implementado em H-0020.

### Evidência quantitativa da reprodução

Com `orquestrador.json`, `largura=80`, `altura=30`:

| Propriedade | Valor | Correto? |
|---|---|---|
| `l_corpo_disponivel` | 24 | ✓ |
| linhas no bloco | 24 | ✓ (dimensionalmente) |
| linhas 7–26 são `" " * 80` | True | ✓ por coluna, mas visualmente idêntico ao fill externo |
| linhas 7–26 têm bordas `│` | False | ✗ (problema visual) |
| boxes fecham na linha 6 (última caixa) | True | ✗ (esperado: base na linha 26) |

---

## Causa principal

```
BUG_H0020_RENDERIZADOR_HORIZONTAL_INCOMPLETO
```

O H-0020 moveu o fill de externo (H-0015) para interno (por coluna),
satisfazendo os critérios de aceite dimensionais dos testes (bloco tem
`l_corpo_disponivel` linhas, sem fill externo). Porém o fill interno
`" " * larguras[i]` é **visualmente idêntico** ao fill externo H-0015:
`" " * total_w`. O visual esperado (`│        │` com base na última linha)
requer decomposição de `_caixa()` em partes — não implementada em H-0020.

A inconsistência entre a "Regra visual esperada" (com bordas estendidas)
e o algoritmo especificado (`" " * larguras[i]`) não foi detectada durante
o QA automatizado, pois os testes verificam apenas dimensões (número de
linhas, largura) e não a presença de bordas nas linhas de fill.

---

## Causas secundárias

1. **LACUNA_TESTE_INTEGRACAO_ORQUESTRADOR**: Nenhum teste exercita o
   pipeline `carregar_tela("orquestrador")` → `renderizar_tela` com
   `arranjo="horizontal"`. Os testes H-0020 usam exclusivamente fixtures
   sintéticas via `_modelo_horizontal()`.

2. **Inconsistência spec-algoritmo não detectada no QA**: A "Regra visual
   esperada" do H-0020 mostra caixas com bordas estendidas, mas o algoritmo
   do handoff especifica `linhas.append(" " * larguras[i])` — sem bordas.
   Esta inconsistência deveria ter sido identificada na auditoria.

---

## Próximo ciclo recomendado

```
H-0021 — Correção pós-QA manual do preenchimento horizontal no orquestrador
```

O H-0021 deve corrigir `_montar_corpo_horizontal` para produzir o visual
esperado:

1. Para cada elemento, separar a geração em **topo+conteúdo** e **base**.
2. Normalizar cada coluna até `altura_alvo − 1` com linhas bordeadas:
   `borda["v"] + " " * (larguras[i] − 2) + borda["v"]`
3. Acrescentar `_linha_base(borda, larguras[i] − 2)` como a linha
   `altura_alvo − 1` de cada coluna.
4. Adicionar teste de integração com `orquestrador.json` em modo horizontal
   que verifique a presença de `│` nas linhas de preenchimento.

Esta mudança requer cuidado especial para:
- Elementos do tipo `grupo` (sem visual — área vazia mas ainda bordeada?)
- Consistência dos testes existentes de H-0019 e H-0020
- Manutenção do invariante `len(linha) == total_w` após a mudança de fill

---

## Impacto no H-0022

```
parar
```

O visual de colunas horizontais não está conforme a especificação. O H-0022
deve aguardar a correção do H-0021 antes de prosseguir. Iniciar H-0022
sobre uma base visual incorreta do arranjo horizontal consolidaria um
comportamento incorreto nos ciclos seguintes.

---

## Conclusão

O H-0020 foi implementado e aprovado em QA automatizado (621/621). A
falha observada no teste manual não é bug de fluxo (altura é propagada
corretamente, branch horizontal é acionado, guarda H-0015 funciona) mas
sim uma **incompletude visual**: o fill interno `" " * larguras[i]`
produz espaços sem bordas, visualmente idênticos ao fill externo H-0015.

A "Regra visual esperada" do H-0020 (caixas com bordas estendidas e base
na última linha) requer uma implementação diferente de `_montar_corpo_horizontal`
que decomponha `_caixa()` em partes — isso não foi entregue em H-0020.

O diagnóstico é confirmado por reprodução controlada: com `orquestrador.json`
ajustado em memória para `arranjo="horizontal"`, largura=80, altura=30, as
linhas 7–26 do corpo são `" " * 80` sem qualquer borda lateral, enquanto o
esperado seria linhas com `│ ... │` por coluna até a linha 26, com base na
linha 26.
