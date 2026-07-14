# RELATORIO_QA_H-0021_CORRECAO_PREENCHIMENTO_HORIZONTAL_ORQUESTRADOR

## Status

```
QA_APPROVED
```

---

## Resumo executivo

O QA do ciclo H-0021 ("Correção pós-QA manual do preenchimento horizontal no
orquestrador") foi conduzido com leitura integral de todos os artefatos
obrigatórios, verificação do diff real no workspace, execução das 6 suítes
de teste e inspeção do código implementado.

Nenhum achado bloqueante, alto ou médio foi identificado. A implementação
segue rigorosamente o handoff aprovado (opção B — parâmetro `altura_alvo=None`
em `_caixa()` e padrão pop+fill+append em `_montar_corpo_horizontal`), cobre
todos os 14 testes exigidos, preserva zero regressões nas 621 verificações
anteriores e atinge o total de 659/659.

---

## Base verificada

| Item | Valor |
|------|-------|
| HEAD observado | `3132d4c  docs: registra investigacao pos H-0020` |
| Workspace antes do QA | ` M tela/renderizador.py` / ` M tela/teste_renderizador.py` / `?? docs/handoff/H-0021-...` / `?? docs/relatorios/IMP-0021-...` / `?? docs/relatorios/RELATORIO_AUDITORIA_H-0021_HANDOFF.md` |
| Workspace conforme esperado | sim |

---

## Arquivos analisados

```
docs/handoff/H-0021-correcao-preenchimento-horizontal-orquestrador.md
docs/relatorios/RELATORIO_AUDITORIA_H-0021_HANDOFF.md
docs/relatorios/IMP-0021-correcao-preenchimento-horizontal-orquestrador.md
docs/relatorios/RELATORIO_INVESTIGACAO_POS_H0020_HORIZONTAL_ORQUESTRADOR.md
docs/handoff/H-0020-preenchimento-vertical-areas-corpo-horizontal.md
docs/relatorios/IMP-0020-preenchimento-vertical-areas-corpo-horizontal.md
docs/relatorios/RELATORIO_QA_H-0020_PREENCHIMENTO_VERTICAL_AREAS_CORPO_HORIZONTAL.md
docs/handoff/H-0019-layout-horizontal-plano-corpo.md
docs/relatorios/IMP-0019-layout-horizontal-plano-corpo.md
docs/relatorios/RELATORIO_QA_H-0019_LAYOUT_HORIZONTAL_PLANO_CORPO.md
docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
docs/NOMENCLATURA.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_json_tela_minima.md
tela/renderizador.py   (integralmente — linhas 1..1006)
tela/teste_renderizador.py   (integralmente — linhas 1..3345)
tela/demo.py, tela/loader.py, tela/modelo.py   (referência)
config/telas/orquestrador.json   (referência)
```

---

## Comandos executados

### Primeira trava obrigatória

```
git log --oneline -10
→ 3132d4c docs: registra investigacao pos H-0020 (HEAD)  ✓

git status --short
→  M tela/renderizador.py
   M tela/teste_renderizador.py
   ?? docs/handoff/H-0021-correcao-preenchimento-horizontal-orquestrador.md
   ?? docs/relatorios/IMP-0021-correcao-preenchimento-horizontal-orquestrador.md
   ?? docs/relatorios/RELATORIO_AUDITORIA_H-0021_HANDOFF.md

git diff --stat
→ scripts/tela/renderizador.py       |  33 +++-
  scripts/tela/teste_renderizador.py | 383 +++++++++++++++++++++++++++++++++++++
  2 files changed, 412 insertions(+), 4 deletions(-)

git diff --name-only
→ scripts/tela/renderizador.py
  scripts/tela/teste_renderizador.py
```

### Verificação de regra de numeração

```bash
grep -RIn "H-0020A\|H-0019A\|H-0011B" \
  docs/handoff/H-0021-correcao-preenchimento-horizontal-orquestrador.md \
  docs/relatorios/RELATORIO_AUDITORIA_H-0021_HANDOFF.md \
  docs/relatorios/IMP-0021-correcao-preenchimento-horizontal-orquestrador.md \
  tela/renderizador.py \
  tela/teste_renderizador.py || true
```

Resultado: ocorrências encontradas apenas em `RELATORIO_AUDITORIA_H-0021_HANDOFF.md`
(3 ocorrências) e em `IMP-0021` (1 ocorrência) — todas dentro de comandos
`grep` citados como exemplos de verificação, não como referências ativas a
handoff com letra. Uso aceitável.

### Proteção da barra_de_menus

```bash
git diff -- tela/renderizador.py | grep -n "_normalizar_distribuicao\|_validar_distribuicao\|_linhas_barra" || true
```

Resultado: sem saída — funções não alteradas no diff. ✓

### Caches Python

```bash
find . -name '__pycache__' -type d -print
find . -name '*.pyc' -print
```

Resultado: ambos sem saída — nenhum cache criado. ✓

---

## Verificação de escopo de arquivos

**Arquivos modificados no diff:**

| Arquivo | Status | Permitido |
|---------|--------|-----------|
| `tela/renderizador.py` | modificado | ✓ |
| `tela/teste_renderizador.py` | modificado | ✓ |

**Artefatos documentais do ciclo (untracked — criados, não modificados):**

| Arquivo | Status |
|---------|--------|
| `docs/handoff/H-0021-correcao-preenchimento-horizontal-orquestrador.md` | novo untracked ✓ |
| `docs/relatorios/IMP-0021-correcao-preenchimento-horizontal-orquestrador.md` | novo untracked ✓ |
| `docs/relatorios/RELATORIO_AUDITORIA_H-0021_HANDOFF.md` | novo untracked ✓ |

Nenhum arquivo proibido foi alterado.

**Resultado: CONFORME ✓**

---

## Verificação da regra de numeração

As ocorrências de "H-0020A", "H-0019A" e "H-0011B" encontradas nos artefatos
documentais (auditoria e IMP-0021) aparecem exclusivamente dentro de comandos
bash `grep` citados como exemplos de verificação e de proibição histórica —
não como referências ativas a handoffs com letra. Aceito.

Nos arquivos de código `tela/renderizador.py` e `tela/teste_renderizador.py`:
nenhuma ocorrência. ✓

**Resultado: CONFORME ✓**

---

## Verificação da adaptação de `_caixa`

**Código verificado em `tela/renderizador.py`, linhas 172–188:**

```python
def _caixa(label, linhas_conteudo, borda, inner_w, content_w, label_max, altura_alvo=None):
    partes = [_linha_topo(label, borda, label_max)]
    for texto in linhas_conteudo:
        partes.append(_linha_conteudo(texto, borda, content_w))
    if altura_alvo is not None:
        linha_fill = borda["v"] + " " * inner_w + borda["v"]
        while len(partes) < altura_alvo - 1:
            partes.append(linha_fill)
    partes.append(_linha_base(borda, inner_w))
    return "\n".join(partes)
```

| Critério | Status | Evidência |
|----------|--------|-----------|
| `altura_alvo=None` é parâmetro nomeado ao final da assinatura | ✓ | linha 172 |
| Sem `altura_alvo`: comportamento anterior preservado (topo + conteúdo + base) | ✓ | bloco `if altura_alvo is not None:` não executado |
| Com `altura_alvo`: fill bordeado inserido antes da base | ✓ | linhas 184–186 |
| Fill bordeado: `borda["v"] + " " * inner_w + borda["v"]` | ✓ | linha 184 |
| Comprimento do fill: `1 + inner_w + 1 = inner_w + 2 = total_w` | ✓ | invariante verificado nos testes 3 e 6 |
| Topo na linha 0 | ✓ | `partes[0] = _linha_topo(...)` |
| Conteúdo nas linhas 1..k | ✓ | loop `for texto in linhas_conteudo:` |
| Fill interno bordeado nas linhas k+1..h-2 | ✓ | `while len(partes) < altura_alvo - 1:` |
| Base na última linha (h-1) | ✓ | `partes.append(_linha_base(borda, inner_w))` após o while |
| Sem truncamento silencioso | ✓ | nenhuma condição de truncamento presente |
| Sem omissão de conteúdo | ✓ | todo `linhas_conteudo` é processado antes do fill |
| Usos existentes de `_caixa()` sem `altura_alvo` inalterados | ✓ | 4 chamadas existentes sem o argumento (linhas 884–886, 677–679, 683–685, 689–691, 1000–1003) |

**Nota QA-001**: a função `_caixa()` com `altura_alvo` não é chamada diretamente
por `_montar_corpo_horizontal` — o algoritmo real usa pop+fill+append sobre a
saída de `_caixa_de_elemento()`. O parâmetro `altura_alvo` foi implementado em
`_caixa()` como artefato formal da opção B, mas o caminho de execução do
preenchimento horizontal passa pelo loop em `_montar_corpo_horizontal`.
Comportamento correto e conforme o handoff ("o executor pode adotar variante
equivalente").

**Resultado: CONFORME ✓**

---

## Verificação de `_montar_corpo_horizontal`

**Código verificado em `tela/renderizador.py`, linhas 764–781:**

```python
for i, linhas in enumerate(todas_as_linhas_por_area):
    w = larguras[i]
    if altura_disponivel is not None:
        if linhas:
            base_linha = linhas.pop()
        else:
            base_linha = _linha_base(borda, w - 2)
        linha_fill = borda["v"] + " " * (w - 2) + borda["v"]
        while len(linhas) < altura_alvo - 1:
            linhas.append(linha_fill)
        linhas.append(base_linha)
    else:
        while len(linhas) < altura_alvo:
            linhas.append(" " * w)
```

| Critério | Status | Evidência |
|----------|--------|-----------|
| Usa `altura_disponivel` para ativar fill bordeado | ✓ | `if altura_disponivel is not None:` |
| Fill bordeado: `borda["v"] + " " * (w - 2) + borda["v"]` | ✓ | linha 774 |
| Comprimento do fill: `1 + (w - 2) + 1 = w` | ✓ | invariante de largura — mitiga R-4 |
| Base existente extraída antes do fill | ✓ | `linhas.pop()` (linha 771) |
| Guard `if linhas:` evita IndexError em lista vazia | ✓ | linha 770 — mitiga R-1 |
| Base nova gerada para área vazia | ✓ | `_linha_base(borda, w - 2)` (linha 773) |
| Fill até `altura_alvo - 1` | ✓ | `while len(linhas) < altura_alvo - 1:` |
| Base reposicionada em `altura_alvo - 1` (última linha) | ✓ | `linhas.append(base_linha)` após o while |
| Caminho `altura_disponivel is None` preservado | ✓ | `else: while ... linhas.append(" " * w)` |
| Bordas adjacentes coladas (`││` no fill, `╯╰` na base) | ✓ | decorrente da concatenação de bordas direita/esquerda adjacentes |
| Largura total de cada linha = `total_w` | ✓ | `sum(larguras) == total_w` e cada linha tem `larguras[i]` chars |
| Ordem declarativa dos filhos preservada | ✓ | `for i, elemento in enumerate(elementos):` |
| Sem filho omitido ou reordenado | ✓ | loop preserva índices da lista original |
| Sem fallback silencioso para vertical | ✓ | nenhum `except`/`if` que desvie para vertical |

**Resultado: CONFORME ✓**

---

## Verificação do caso `orquestrador.json`

**Snippet em memória (teste 1):**

```python
tela_raw = carregar_tela(_BASE_PADRAO, "orquestrador")
tela_raw["corpo"]["arranjo"] = "horizontal"
modelo = construir_modelo(tela_raw)
saida = renderizar_tela(modelo, tipo_borda="curva", largura=80, altura=30)
```

| Verificação | Status | Evidência |
|-------------|--------|-----------|
| Sem alteração persistente de `orquestrador.json` | ✓ | `tela_raw["corpo"]["arranjo"]` modifica apenas o dict em memória |
| Bloco horizontal tem 24 linhas (`l_corpo_disponivel = 30 − 3 − 3`) | ✓ | `bloco = linhas[3:27]`; `len(bloco) == 24` — teste 1 |
| Linhas internas contêm `│` por coluna | ✓ | `all("│" in ln for ln in inner)` — teste 1 |
| Sem linhas `" " * 80` no bloco | ✓ | `not any(ln == " " * 80 for ln in bloco)` — teste 1 |
| Cada linha do bloco tem 80 chars | ✓ | `all(len(ln) == 80 for ln in bloco)` — teste 1 |
| Filhos `console_principal`, `dashboard_info`, `lancador_principal` presentes | ✓ | `╭ ITENS`, `╭ INFO`, `╭ NAVEGAR` presentes — teste 8 |
| Filhos na ordem declarada (esq → dir) | ✓ | `linha_topos.index("╭ ITENS") < index("╭ INFO") < index("╭ NAVEGAR")` — teste 8 |
| `dashboard_info` sem conteúdo literal: bordas presentes | ✓ | `chars_esq_dash` todos `│`; `char_base == "╰"` — teste 7 |
| Base das caixas na última linha | ✓ | `última[27] == "╰"` — teste 7 |
| Alias `lado_a_lado` produz resultado idêntico | ✓ | `saida_h == saida_l` — teste 2 |

**Resultado: CONFORME ✓**

---

## Verificação de aliases transicionais

| Alias | Normalização | Status |
|-------|-------------|--------|
| `lado_a_lado` → `horizontal` | `renderizador.py` linhas 894–895 (inalteradas) | ✓ |
| `sobreposto` → `vertical` | `renderizador.py` linha 892–893 (inalteradas) | ✓ |

Testes 2 (`lado_a_lado`) e 11 (`sobreposto`) confirmam o comportamento.

**Resultado: CONFORME ✓**

---

## Verificação de preservações

| Comportamento | Status | Verificação |
|--------------|--------|-------------|
| `vertical` — fill externo H-0015 intacto | ✓ | testes 7 (H0020), 10 (H0021): `[ln for ln in linhas if ln == " " * 42]` > 0 |
| `sobreposto` — alias de vertical, saída idêntica | ✓ | testes 8 (H0020), 11 (H0021): `saida_v == saida_s` |
| `None` — equivale a vertical | ✓ | testes 9 (H0020), 12 (H0021): `saida_n == saida_v` |
| `horizontal` sem altura — fill `" " * w` (H-0019/H-0020) | ✓ | testes 11 (H0020), 9 (H0021): `dash_fill == " " * 21` |
| `lado_a_lado` como alias de `horizontal` | ✓ | testes 10 (H0020), 2 (H0021): `saida_h == saida_l` |
| `barra_de_menus` com chips corretos | ✓ | testes 12 (H0020), 13 (H0021): `[Esc] Sair`, `[?] Ajuda` presentes |
| snapshot `_EXPECTED_ORQUESTRADOR` preservado (vertical, 42) | ✓ | teste 10 H0021: `saida == _EXPECTED_ORQUESTRADOR` |

**Resultado: CONFORME ✓**

---

## Verificação de proteção da barra_de_menus

```bash
git diff -- tela/renderizador.py | grep -n "_normalizar_distribuicao\|_validar_distribuicao\|_linhas_barra" || true
```

Saída: (sem saída — nenhuma dessas funções foi alterada no diff) ✓

| Artefato | Status |
|----------|--------|
| `_normalizar_distribuicao` (com `r`) | ✓ intocada — linha 259 do renderizador |
| `_validar_distribuicao` | ✓ intocada — linha 292 do renderizador |
| `_linhas_barra` | ✓ intocada — linha 582 do renderizador |
| `_validar_ancoras` | ✓ intocada — linha 490 do renderizador |
| `tela/explorar_barra_de_menus.py` | ✓ não aparece no diff |
| `tela/teste_explorar_barra_de_menus.py` | ✓ não aparece no diff; 38/38 confirmado |
| `docs/contratos/contrato_barra_de_menus.md` | ✓ não aparece no diff |
| `docs/contratos/contrato_chip.md` | ✓ não aparece no diff |

A grafia `_normalizar_distribuicao` (com `r`) é usada corretamente em todo o
código e nos documentos do ciclo. A grafia sem `r` aparece apenas como nota
histórica em contextos de proibição (R-6 do handoff), conforme previsto.

**Resultado: CONFORME ✓**

---

## Verificação dos testes

### Classe `TestPreenchimentoBordeadoH0021`

14 testes implementados, mapeados contra os 14 testes obrigatórios do handoff:

| # | Nome do teste | Cobertura verificada |
|---|---------------|---------------------|
| 1 | `test_horizontal_fill_bordeado_orquestrador_json` | `orquestrador.json` em memória, 24 linhas, `│` nas internas, sem `" "*80`, len=80 |
| 2 | `test_horizontal_fill_bordeado_lado_a_lado_alias` | `lado_a_lado` idêntico ao `horizontal`; bordas nas internas |
| 3 | `test_horizontal_fill_linhas_internas_com_bordas_laterais` | `ln[0] == "│"`, `ln[-1] == "│"`, `len(ln) == 42` |
| 4 | `test_horizontal_base_na_ultima_linha_da_area` | `ultima.startswith("╰")`, `ultima.endswith("╯")`, sem `╰` prematuro |
| 5 | `test_horizontal_bordas_adjacentes_em_fill_e_base` | `"││" in fill_lines`, `"╯╰" in linhas_bloco[-1]` |
| 6 | `test_horizontal_largura_total_em_todas_linhas_apos_h0021` | `len(linhas_bloco) == 20`, `all(len(ln) == 42)` |
| 7 | `test_horizontal_dashboard_sem_literal_tem_bordas` | `chars_esq_dash` todos `│`; `char_base == "╰"` |
| 8 | `test_horizontal_filhos_preservados_em_ordem` | `╭ ITENS`, `╭ INFO`, `╭ NAVEGAR` presentes; ordem esq→dir |
| 9 | `test_horizontal_sem_altura_preserva_h0019_h0020` | `len == 3` (altura_max); `dash_fill == " " * 21` |
| 10 | `test_vertical_nao_regride_apos_h0021` | `saida == _EXPECTED_ORQUESTRADOR`; fill externo de espaços |
| 11 | `test_sobreposto_nao_regride_apos_h0021` | `saida_v == saida_s`; 20 linhas |
| 12 | `test_none_nao_regride_apos_h0021` | `saida_n == saida_v`; 20 linhas |
| 13 | `test_barra_de_menus_preservada_apos_h0021` | `╭ Menus`, `[Esc] Sair`, `[?] Ajuda`; `callable(_normalizar_distribuicao)` |
| 14 | `test_baseline_completo_continua_passando` | registro explícito; 659/659 confirmado externamente |

**Observação sobre o teste 4**: a verificação de ausência de base prematura
usa `linhas_bloco[:-1]` (todos exceto o último) buscando `╰`. A linha de
topo contém `╭` e `╮` mas não `╰`; as linhas de fill têm `│` mas não `╰`.
Portanto, a verificação está correta. ✓

**Observação sobre o teste 9**: supõe larguras `[21, 21]` para 2 elementos
em largura 42. `42 // 2 = 21, resto 0`. Dashboard (coluna 1) tem `w = 21`.
`" " * 21` é o fill esperado. ✓

**Resultado: CONFORME ✓** — todos os 14 testes exigidos presentes e corretos.

---

## Verificação do IMP-0021

| Seção exigida | Status | Observação |
|---------------|--------|------------|
| Status `IMPLEMENTATION_COMPLETE` | ✓ | presente |
| Base verificada | ✓ | HEAD `3132d4c` registrado |
| Arquivos alterados | ✓ | lista completa presente |
| Resumo da implementação | ✓ | dois pontos de alteração cirúrgica descritos |
| Adaptação de `_caixa` | ✓ | opção B descrita com snippet de código |
| Preenchimento bordeado | ✓ | pop+fill+append descrito com snippet |
| Integração com `orquestrador.json` em memória | ✓ | snippet e tabela de verificações |
| Tratamento do alias `lado_a_lado` | ✓ | seção presente |
| Testes executados | ✓ | tabela completa 621→659 |
| Verificação de proteção da `barra_de_menus` | ✓ | `_normalizar_distribuicao` (com `r`) confirmada |
| NOTA-1 registrada | ✓ | seção "Tratamento das notas da auditoria" / NOTA-1 |
| NOTA-2 registrada | ✓ | seção "Tratamento das notas da auditoria" / NOTA-2 |
| Opção B adotada explicitamente | ✓ | seção "Decisão de implementação": "Foi adotada a opção B" |
| Justificativa da opção B | ✓ | "por menor impacto" e "evita o problema de dois passes" |
| Opção B não exigiu alteração fora do escopo | ✓ | confirmado — apenas `renderizador.py` e `teste_renderizador.py` alterados |

**Resultado: CONFORME ✓**

---

## Verificação de proibições de escopo

Verificado via diff real e inspeção do código que **nenhum** dos itens
proibidos foi implementado:

| Item proibido | Status |
|---------------|--------|
| Distribuição vertical do corpo | ✓ não presente |
| `corpo.distribuicao` percentual/fracao | ✓ não presente |
| Grupos hierárquicos | ✓ não presente |
| Arranjo/distribuicao dentro de grupo | ✓ não presente |
| Profundidade de 3 níveis | ✓ não presente |
| Sincronização de cortes | ✓ não presente |
| Paginação real | ✓ não presente |
| Terminal pequeno com reticências | ✓ não presente |
| Configuração declarativa de largura | ✓ não presente |
| Campo largura/dimensao no JSON | ✓ não presente |
| Console real | ✓ não presente |
| Navegação por [✥] | ✓ não presente |
| Foco, seleção, filtros, ações | ✓ não presente |
| Registry novo | ✓ não presente |
| Alterações em barra_de_menus | ✓ não alterada |
| Alterações em contratos, ADRs, NOMENCLATURA | ✓ não alterados |
| Mudanças em `orquestrador.json` | ✓ não alterado |
| Commit | ✓ não realizado |

**Resultado: CONFORME ✓**

---

## Achados

| ID | Severidade | Descrição | Evidência | Impacto | Correção recomendada |
|----|-----------|-----------|-----------|---------|----------------------|
| QA-001 | NOTA | A Opção B foi implementada em `_caixa()` (parâmetro `altura_alvo=None`) mas o caminho de execução real do preenchimento horizontal não passa por `_caixa()` com `altura_alvo` — usa pop+fill+append sobre a saída de `_caixa_de_elemento()` em `_montar_corpo_horizontal`. O parâmetro em `_caixa()` existe formalmente mas não é chamado com `altura_alvo` por nenhum caminho ativo. | `renderizador.py` linhas 172–188: `_caixa()` com `altura_alvo`; linhas 739–741: `_caixa_de_elemento()` sem `altura_alvo`; linhas 764–781: pop+fill+append no loop | Comportamento correto e conforme o handoff ("o executor pode adotar variante equivalente"). Sem impacto na correção ou cobertura. | Nenhuma correção necessária. O handoff permite variante equivalente e o IMP-0021 registra explicitamente a abordagem adotada. |

**Total de achados:** 1 NOTA, 0 BAIXO, 0 MÉDIO, 0 ALTO, 0 BLOQUEANTE.

---

## Resultado dos testes

| Suíte | Resultado | Exit code |
|-------|-----------|-----------|
| `teste_loader.py` | 89/89 | 0 |
| `teste_modelo.py` | 56/56 | 0 |
| `teste_renderizador.py` | 331/331 | 0 |
| `teste_demo.py` | 117/117 | 0 |
| `teste_diagnostico.py` | 28/28 | 0 |
| `teste_explorar_barra_de_menus.py` | 38/38 | 0 |
| **TOTAL** | **659/659** | **0** |

Regressões: 0.
Novos testes adicionados: 38 (`TestPreenchimentoBordeadoH0021`).

---

## Decisão

```
APROVADO
```

Todos os critérios de aprovação são satisfeitos:

- [x] Nenhum arquivo proibido foi alterado
- [x] Não há referência ativa a handoff com letra
- [x] `barra_de_menus` permanece protegida (`_normalizar_distribuicao`, `_validar_distribuicao`, `_linhas_barra` intocadas; 38/38)
- [x] Todos os testes obrigatórios passam (659/659)
- [x] Baseline ampliado passa sem regressão (0 regressões em 621 verificações anteriores)
- [x] H-0021 implementa apenas o escopo aprovado
- [x] Preenchimento horizontal bordeado funciona no `orquestrador.json` em memória (testes 1, 7, 8)
- [x] Base das caixas está na última linha da área horizontal (teste 4)
- [x] Não há achado bloqueante, alto ou médio

---

## Conclusão

A implementação do H-0021 corrigiu com precisão cirúrgica o preenchimento
visual do modo horizontal: as caixas agora se estendem até a altura alocada,
com bordas laterais (`│ ... │`) nas linhas de fill e base (`╰ ... ╯`)
posicionada na última linha da área. A correção adota o padrão pop+fill+append
descrito explicitamente no handoff como "implementação segura", sem criar novos
fluxos ou impactar qualquer componente além de `_montar_corpo_horizontal`. O
parâmetro `altura_alvo=None` em `_caixa()` foi adicionado conforme a Opção B,
preservando todos os usos existentes. Zero regressões. 659/659 verificações.

O único achado (QA-001, severidade NOTA) documenta que o parâmetro `altura_alvo`
de `_caixa()` não é chamado ativamente no fluxo horizontal — a lógica real
vive no loop de `_montar_corpo_horizontal`. Isso é correto, conforme o handoff,
e devidamente registrado no IMP-0021.

---

## Metadados do QA

| Item | Valor |
|------|-------|
| Auditor | Claude Sonnet 4.6 (claude-sonnet-4-6) |
| Data do QA | 2026-07-10 |
| Commit HEAD no momento do QA | `3132d4c` |
| Workspace após QA | ` M tela/renderizador.py` / ` M tela/teste_renderizador.py` / `?? docs/handoff/H-0021-...` / `?? docs/relatorios/IMP-0021-...` / `?? docs/relatorios/RELATORIO_AUDITORIA_H-0021_HANDOFF.md` / `?? docs/relatorios/RELATORIO_QA_H-0021_CORRECAO_PREENCHIMENTO_HORIZONTAL_ORQUESTRADOR.md` |
| Relatório criado | `docs/relatorios/RELATORIO_QA_H-0021_CORRECAO_PREENCHIMENTO_HORIZONTAL_ORQUESTRADOR.md` |
