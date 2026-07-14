# RELATORIO_QA_H-0015_OCUPACAO_VERTICAL_JANELA_TERMINAL_CORPO

Auditor: Claude Code (QA final — modo somente leitura; nenhum arquivo de
implementação, contrato, ADR, configuração ou teste foi alterado; nenhum
commit realizado).

Data: 2026-07-09

---

## Status final

```
QA_APPROVED
```

Implementação completa, correta e alinhada ao handoff H-0015 e à ADR-0013.
Todos os 25 pontos de QA obrigatórios verificados. Todos os 5 suítes de teste
passam com exit 0 sem nenhum `[FALHOU]`. Um achado de nível nota (constantes
mortas em `teste_demo.py`) sem impacto funcional.

---

## Arquivos analisados

Handoff e relatórios:
- `docs/handoff/H-0015-ocupacao-vertical-janela-terminal-corpo.md`
- `docs/relatorios/RELATORIO_AUDITORIA_H-0015_HANDOFF.md`
- `docs/relatorios/IMP-0015-ocupacao-vertical-janela-terminal-corpo.md`

ADRs:
- `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md`
- `docs/adr/ADR-0014-barra-horizontal-termos-especificos.md`

Contratos (verificação de não alteração):
- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_barra_de_menus.md`

Código alterado (diff verificado):
- `tela/renderizador.py`
- `tela/demo.py`
- `tela/teste_renderizador.py`
- `tela/teste_demo.py`

Código não alterado (diff vazio confirmado):
- `tela/loader.py`
- `tela/modelo.py`
- `tela/diagnostico.py`
- `tela/teste_loader.py`
- `tela/teste_modelo.py`
- `tela/teste_diagnostico.py`
- `config/telas/orquestrador.json`
- `config/telas/grupo_minimo.json`
- `config/telas/destino_minimo.json`
- `config/telas/stub_b.json`

---

## Comandos executados

```bash
git log --oneline -6
git status --short
git diff --stat
git diff --name-only
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_demo.py
python tela/teste_diagnostico.py
python -c "... renderizar_tela(modelo, largura=42, altura=24) ..."
python -c "... renderizar_tela(modelo, largura=42, altura=6) -> RenderizadorErro ..."
python -c "... altura=None preserva comportamento ..."
python -c "... subprocess g/Esc/Esc -> exit 0, GRUPO MINIMO no stdout ..."
grep -rn "ADR-0015" tela/ docs/relatorios/IMP-0015-...
grep -n "horizontal_responsiva|coluna_a_coluna|linha_a_linha|ancoras|overflow" tela/
find . -name '__pycache__' -type d -prune -print
find . -name '*.pyc' -print
git diff tela/loader.py tela/modelo.py tela/diagnostico.py
git diff config/ docs/contratos/ docs/adr/ docs/NOMENCLATURA.md
```

---

## Resumo executivo

O H-0015 implementou a ADR-0013 (ocupação vertical da janela do terminal pelo
corpo) de forma correta e mínima. O renderer aceita o novo parâmetro opcional
`altura: int | None = None`; quando fornecido e suficiente, insere linhas
físicas de `total_w` espaços entre o último box do corpo e o box da
`barra_de_menus`, totalizando exatamente `altura` linhas. Quando `altura is
None`, o comportamento anterior é preservado integralmente. A demo lê largura
e altura em uma única chamada `shutil.get_terminal_size(fallback=(80, 24))` e
propaga ambas ao renderer. O terminal pequeno gera `RenderizadorErro`
determinístico em dois casos: `L_cab + L_barra > altura` e
`L_corpo_conteudo > L_corpo_disponivel`. Nenhuma funcionalidade da ADR-0014 foi
implementada. O fluxo g/d/b/Esc foi preservado. Os achados ACH-H15-01,
ACH-H15-02, ACH-H15-03, ACH-H15-04 foram tratados corretamente.

---

## Verificação de escopo

Confirmado que apenas os arquivos da lista "alterar obrigatório" do handoff
foram modificados:

| Arquivo | Status |
|---|---|
| `tela/renderizador.py` | Alterado (diff confirmado) |
| `tela/demo.py` | Alterado (diff confirmado) |
| `tela/teste_renderizador.py` | Alterado (diff confirmado) |
| `tela/teste_demo.py` | Alterado (diff confirmado) |
| `docs/relatorios/IMP-0015-*` | Criado (untracked, confirmado) |

Nenhum arquivo fora desta lista foi alterado. `git diff --name-only` retorna
exatamente os quatro arquivos acima.

---

## Verificação de aderência à ADR-0013

| Item ADR-0013 | Status |
|---|---|
| 1. Tela ocupa largura e altura disponíveis | Conforme: renderer aceita `altura`; demo propaga `.lines` |
| 2. Altura como dimensão explícita do render | Conforme: `altura: int | None = None` em `renderizar_tela` |
| 3. Corpo ocupa área entre cabeçalho e barra_de_menus | Conforme: `L_corpo_disponivel = altura - L_cab - L_barra` |
| 4. Preencher com linhas em branco quando conteúdo < disponível | Conforme: `L_corpo_fill = L_corpo_disponivel - L_corpo_conteudo`; linhas de `" " * total_w` inseridas |
| 5. Preenchimento é do renderer, não do JSON | Conforme: JSON não alterado; preenchimento calculado em `renderizar_tela` |
| 6. Não altera semântica de `corpo.arranjo` | Conforme: `corpo.arranjo = "vertical"` mantido como composição |
| 7. `corpo.arranjo = "vertical"` ≠ ocupação de terminal | Conforme: distinção explícita em docstring e comentários |
| 8. Uso de termos específicos | Conforme: usa `altura`, `L_corpo_disponivel`, `L_corpo_fill` |
| 9. Representação exata das linhas de preenchimento (fechada pelo handoff) | Conforme: `" " * total_w` — linhas físicas fora de qualquer caixa |

---

## Verificação de não implementação da ADR-0014

Grep sobre `tela/renderizador.py` e `tela/demo.py` para:
`horizontal_responsiva`, `coluna_a_coluna`, `linha_a_linha`, `ancoras`,
`overflow` → **nenhuma ocorrência**.

Barra de menus: continua com um chip por linha, comportamento idêntico ao
anterior ao H-0015. Nenhum campo de distribuição horizontal foi introduzido.

---

## Verificação da implementação

### `tela/renderizador.py`

**Ponto 1**: `renderizar_tela` aceita `altura: int | None = None`.
- Verificado: assinatura em `renderizador.py:248–253` confirma o novo parâmetro.

**Ponto 2**: Quando `altura is None`, caminho anterior preservado.
- Verificado por teste: `renderizar_tela(modelo, largura=42) == renderizar_tela(modelo, largura=42, altura=None)` → PASSOU.

**Ponto 3**: Quando `altura` explícita e suficiente, saída tem exatamente `altura` linhas.
- Verificado: `renderizar_tela(modelo, largura=42, altura=24)` → `count("\n") == 24` ✓
- Verificado via linha de comando: `linhas: 24`, `OK — 24 linhas confirmadas` ✓

**Ponto 4**: Linhas de preenchimento pertencem ao corpo e são criadas pelo renderer.
- Verificado: lógica em `renderizador.py:394–401`; JSON não foi alterado.
- Preenchimento inserido com `"\n".join(" " * total_w for _ in range(l_corpo_fill))`.

**Ponto 5**: Cada linha de preenchimento tem exatamente `largura` espaços.
- Verificado: teste `altura=24 gera exatamente 8 linhas de preenchimento` e
  `linhas de preenchimento tem exatamente 42 espacos (CA-05)` → PASSOU.

**Ponto 6**: Testes não usam `strip()` para destruir evidência das linhas de preenchimento.
- Verificado: `teste_altura_explicita` em `teste_renderizador.py:1021–1022`:
  `fills = [ln for ln in linhas_24 if ln == fill_esperado]` onde
  `fill_esperado = " " * 42` — comparação integral sem `strip()`. ✓

**Ponto 7**: `barra_de_menus` fica no rodapé quando altura explícita é usada.
- Verificado: teste CA-07 `barra_de_menus no rodape: ultima linha nao-vazia termina com '╯'` → PASSOU.

**Ponto 8**: Cabeçalho permanece no topo.
- Verificado: teste CA-06 `cabecalho no topo: primeira linha comeca com '╭ ORQUESTRADOR'` → PASSOU.

**Ponto 9**: Corpo ocupa espaço vertical entre cabeçalho e barra_de_menus.
- Verificado: teste CA-08 `preenchimento entre corpo e Menus: linha 12 = fill, linha 20 = '╭ Menus'` → PASSOU.
  Estrutura: `linhas_24[12] == fill_esperado` e `linhas_24[20].startswith("╭ Menus")`.

**Ponto 10**: Terminal pequeno gera `RenderizadorErro` determinístico.
- Verificado: dois caminhos de erro confirmados:
  - `altura=6`: `RenderizadorErro: altura insuficiente: terminal com 6 linhas nao comporta cabecalho (3) + barra_de_menus (4)` ✓
  - `altura=15`: `RenderizadorErro: altura insuficiente: corpo requer 9 linhas mas area disponivel e 8 linhas (altura=15, cabecalho=3, barra=4)` ✓

### `tela/demo.py`

**Ponto 11**: `demo.py` captura largura e altura com `shutil.get_terminal_size(fallback=(80, 24))`.
- Verificado: `demo.py:217–219`:
  ```python
  tamanho_terminal = shutil.get_terminal_size(fallback=(80, 24))
  largura = tamanho_terminal.columns
  altura = tamanho_terminal.lines
  ```

**Ponto 12**: `demo.py` propaga largura e altura ao renderer.
- Verificado: `renderizar_estado` em `demo.py:166–178` aceita `largura=None, altura=None` e repassa ao renderer.
- Todas as 3 chamadas a `renderizar_estado` em `main()` passam `altura=altura`: linhas 221, 233, 244. ✓

**Ponto 13**: Fluxo g/d/b/Esc preservado.
- Verificado via subprocess: `g\n\x1b\n\x1b\n` → exit 0, `GRUPO MINIMO` no stdout, stderr vazio ✓
- Verificado em testes: 117/117 PASSOU, incluindo `demo 'g\n\x1b\n\x1b\n' propaga altura=24: stdout tem 72 newlines (3 renders × 24)`.

**Ponto 14**: Diagnóstico permanece determinístico e não interativo.
- Verificado: `gerar_diagnostico_tela()` chama `renderizar_tela(modelo)` sem largura nem altura (caminho `None`).
  Teste `gerar_diagnostico_tela() bate com _EXPECTED_DIAGNOSTICO_CURVA_42 (default curva, 42)` → PASSOU.
  `diagnostico.py nao contem 'sys.stdin'` e `diagnostico.py nao contem 'input('` → PASSOU.

---

## Verificação dos testes

### `tela/teste_renderizador.py`

Nova função `teste_altura_explicita()` cobrindo:
- CA-01/CA-03: `altura=16` sem fill, idêntico a `altura=None`
- CA-02: `altura=24` → 24 linhas, barra preservada
- CA-04: largura uniforme de todas as linhas não-vazias
- CA-05: linhas de preenchimento com exatamente 42 espaços (sem `strip()`)
- CA-06/CA-07: cabeçalho no topo, barra no rodapé
- CA-08: preenchimento entre último box do corpo e box Menus
- CA-09/CA-10: `altura=None` preserva comportamento
- CA-11/CA-12/CA-13/CA-14: `RenderizadorErro` descritivo em dois cenários de altura insuficiente
- Invariante `"\n\n" not in saida` preservado
- Determinismo de duas chamadas idênticas
- Borda reta com altura explícita

Total: 133/133 verificações. Exit 0.

### `tela/teste_demo.py`

- `_ALTURA_SUBPROCESS = 24` e `_LARGURA_SUBPROCESS = 80` garantem determinismo.
- `env_sem_dimensoes` remove `COLUMNS` **e** `LINES` do ambiente do subprocess.
- Saídas esperadas de subprocess computadas dinamicamente com `renderizar_tela(..., largura=80, altura=24)`.
- Nova função `teste_renderizar_estado_altura()` cobrindo CA-02, CA-03, CA-09, consistência com renderer, barra no rodapé, largura, imutabilidade de estado/modelo.
- Verificação de determinismo de altura: stdout de `g\n\x1b\n\x1b\n` tem exatamente 72 newlines (3 × 24).

Total: 117/117 verificações. Exit 0.

### ACH-H15-01 (alta severidade na auditoria): Tratado corretamente.
As igualdades estritas dos testes de subprocess foram atualizadas para
considerar `altura=24` (fallback). Constatado em execução real: testes passam.

### ACH-H15-02 (baixa): Tratado corretamente.
Identificação de linhas de preenchimento via `ln == fill_esperado` sem `strip()`.

### ACH-H15-03 (baixa-média): Tratado corretamente.
`env_sem_dimensoes` remove `COLUMNS` e `LINES`; verificação explícita de 72 newlines.

### ACH-H15-04 (nota): Tratado corretamente.
`teste_diagnostico.py` lido como referência; não necessitou alteração.

---

## Verificação de preservação de fluxos anteriores

| Fluxo | Status |
|---|---|
| `[g]` abrindo grupo_minimo | PRESERVADO (117/117) |
| `[d]` abrindo destino_minimo | PRESERVADO (117/117) |
| `[b]` alternando borda | PRESERVADO (117/117) |
| Esc em tela interna voltando | PRESERVADO (117/117) |
| Esc na raiz saindo | PRESERVADO (117/117) |
| barra_de_menus declarativa | PRESERVADO (133/133) |
| `corpo.arranjo = "vertical"` como composição | PRESERVADO (sem reinterpretação) |
| diagnóstico determinístico não-interativo | PRESERVADO (28/28) |
| `renderizar_tela(modelo)` sem altura idêntico ao anterior | PRESERVADO (133/133) |

---

## Verificação de arquivos alterados

Estado git verificado:

```
git status --short:
 M tela/demo.py
 M tela/renderizador.py
 M tela/teste_demo.py
 M tela/teste_renderizador.py
?? docs/handoff/H-0015-ocupacao-vertical-janela-terminal-corpo.md
?? docs/relatorios/IMP-0015-ocupacao-vertical-janela-terminal-corpo.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0015_HANDOFF.md

git diff --name-only:
scripts/tela/demo.py
scripts/tela/renderizador.py
scripts/tela/teste_demo.py
scripts/tela/teste_renderizador.py
```

Todos os arquivos alterados estão na lista de "alterar obrigatório" do handoff.
Arquivos proibidos sem diff: `loader.py`, `modelo.py`, `diagnostico.py`,
`config/`, `docs/contratos/`, `docs/adr/`, `docs/NOMENCLATURA.md` — confirmado
por `git diff` individual sobre cada grupo.

Nenhum commit foi realizado.

---

## Verificação de limpeza do workspace

```bash
find . -name '__pycache__' -type d -prune -print  → (nenhuma saída)
find . -name '*.pyc' -print                        → (nenhuma saída)
```

Nenhum `__pycache__` nem arquivo `.pyc` gerado durante a execução dos testes.
Os arquivos de teste usam `sys.dont_write_bytecode = True`.

---

## Achados

### QA-ACH-01

- **ID**: QA-ACH-01
- **Severidade**: nota
- **Evidência**: Em `tela/teste_demo.py`, as constantes
  `_EXPECTED_DESTINO_MINIMO_CURVA_80` (linha 169), `_EXPECTED_DESTINO_MINIMO_RETA_80`
  (linha 183), `_EXPECTED_GRUPO_MINIMO_CURVA_80` (linha 197) e
  `_EXPECTED_GRUPO_MINIMO_RETA_80` (linha 211) são definidas no módulo mas não
  referenciadas em nenhuma das funções de teste. Os testes de subprocess que
  existem (`teste_navegacao_subprocess`) computam o esperado dinamicamente via
  `renderizar_tela(..., largura=_LARGURA_SUBPROCESS, altura=_ALTURA_SUBPROCESS)`.
  Essas constantes provavelmente existiam antes do H-0015 (quando o esperado era
  uma string de 10 linhas sem fill) e tornaram-se código morto após a migração
  das igualdades estritas de subprocess para cálculo dinâmico (tratamento do
  ACH-H15-01).
- **Impacto**: Nulo — nenhum teste usa essas constantes; todos os 117 testes
  passam. Apenas ruído no módulo.
- **Recomendação**: Remover as quatro constantes em ciclo futuro de limpeza,
  ou mantê-las como documentação de referência. Não bloqueia este ciclo.

---

## Resultado dos testes

| Suíte | Verificações | Falhas | Exit |
|---|---|---|---|
| `python tela/teste_loader.py` | 67/67 | 0 | 0 |
| `python tela/teste_modelo.py` | 53/53 | 0 | 0 |
| `python tela/teste_renderizador.py` | 133/133 | 0 | 0 |
| `python tela/teste_demo.py` | 117/117 | 0 | 0 |
| `python tela/teste_diagnostico.py` | 28/28 | 0 | 0 |

**Total: 398/398 verificações, 0 falhas, 5/5 exit 0.**

Verificações determinísticas adicionais via linha de comando:
- `renderizar_tela(modelo, largura=42, altura=24)` → `linhas: 24` ✓
- `renderizar_tela(modelo, largura=42, altura=6)` → `RenderizadorErro` ✓
- `altura=None` preserva comportamento ✓
- Subprocess `g\n\x1b\n\x1b\n` → exit 0, `GRUPO MINIMO` no stdout, stderr vazio ✓

---

## Rastreabilidade ADR

Verificação de menção incorreta a `ADR-0015`:

```bash
grep -rn "ADR-0015" tela/ docs/relatorios/IMP-0015-* docs/handoff/H-0015-* → nenhuma ocorrência
```

A rastreabilidade está correta: **H-0015 implementa ADR-0013**. O código,
testes, docstrings e relatório IMP-0015 referenciam consistentemente `H-0015 /
ADR-0013`. Nenhuma menção espúria a `ADR-0015` encontrada.

---

## Conclusão

A implementação do H-0015 está correta, completa e alinhada a todos os
critérios de aceite do handoff (CA-01 a CA-38) e aos itens da ADR-0013. O
único achado é de nível nota (constantes mortas em `teste_demo.py`) sem
impacto funcional. Todos os 25 pontos de QA obrigatórios foram verificados e
confirmados. Os achados da auditoria do handoff (ACH-H15-01 a ACH-H15-04)
foram tratados adequadamente pelo implementador.

---

## Próxima ação recomendada

1. Commitar os 4 arquivos alterados (`demo.py`, `renderizador.py`,
   `teste_renderizador.py`, `teste_demo.py`) e o relatório `IMP-0015`.
2. Opcionalmente remover as constantes mortas `_EXPECTED_DESTINO_MINIMO_*` e
   `_EXPECTED_GRUPO_MINIMO_*` de `teste_demo.py` em ciclo futuro de limpeza.
3. Iniciar H-0016 (distribuição horizontal responsiva da barra_de_menus —
   ADR-0014) quando agendado.
