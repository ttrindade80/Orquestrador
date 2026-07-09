# RELATORIO_QA_H-0016_MIGRACAO_JSON_BARRA_DE_MENUS_HORIZONTAL_RESPONSIVA

```text
auditor:        Claude Code (papel QA final)
data:           2026-07-09
ciclo:          H-0016
titulo:         Migração canônica do JSON da barra_de_menus e renderização horizontal responsiva
commit-base:    b2eb458  feat: ocupa altura do terminal pelo corpo
executor:       OpenCode / GLM
```

---

## Status final

```text
QA_APPROVED
```

Nenhum achado bloqueante. Nenhum achado de alta severidade. Implementação
completa e alinhada ao handoff revisado (AUDIT_APPROVED_WITH_NOTES), ao
ADR-0014 e aos contratos. Todas as 451 verificações passam em 5 suítes.

---

## Arquivos analisados

### Referência (lidos integralmente)

```text
docs/handoff/H-0016-migracao-json-barra-de-menus-horizontal-responsiva.md
docs/relatorios/RELATORIO_AUDITORIA_H-0016_HANDOFF.md
docs/relatorios/RELATORIO_AUDITORIA_H-0016_HANDOFF_POS_REVISAO.md
docs/relatorios/IMP-0016-migracao-json-barra-de-menus-horizontal-responsiva.md
docs/adr/ADR-0014-barra-horizontal-termos-especificos.md
docs/contratos/contrato_processo_desenvolvimento.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_json_barra_de_menus.md
docs/contratos/contrato_chip.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_json_lancador.md
docs/NOMENCLATURA.md
```

### Implementação (lidos integralmente)

```text
config/telas/orquestrador.json
config/telas/grupo_minimo.json
config/telas/destino_minimo.json
config/telas/stub_b.json
tela/renderizador.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
tela/teste_demo.py
tela/teste_diagnostico.py
```

### Preservação verificada (git diff)

```text
tela/loader.py
tela/modelo.py
tela/demo.py
tela/diagnostico.py
docs/contratos/ (todos)
docs/adr/ (todos)
docs/NOMENCLATURA.md
config/estilo.json
config/lancador.json
config/layout_console.json
```

---

## Comandos executados

```bash
# Estado do repositório
git log --oneline -6
git status --short
git diff --stat
git diff --name-only

# Diff pontual para verificar escopo dos JSONs
git diff -- config/telas/orquestrador.json
git diff -- tela/loader.py tela/modelo.py tela/demo.py tela/diagnostico.py
git diff -- docs/contratos/ docs/adr/ docs/NOMENCLATURA.md \
            config/estilo.json config/lancador.json config/layout_console.json

# Testes obrigatórios (a partir de scripts/)
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_demo.py
python tela/teste_diagnostico.py

# Limpeza de cache
find . -name '__pycache__' -type d -prune -print
find . -name '*.pyc' -print
```

---

## Resumo executivo

A implementação do H-0016 está **completa, correta e dentro do escopo
declarado**. Os quatro pontos obrigatórios do ciclo foram entregues:

1. **Migração dos 4 JSONs** — `barra_de_menus.distribuicao` migrado de
   string `"horizontal"` para objeto canônico com `modo =
   "horizontal_responsiva"`, `ordem.politica = "declaracao"` e âncoras
   usando os IDs reais (`chip_esc` primeiro, `chip_ajuda` último). Chips
   preservados byte-a-byte. Diffs confirmados por inspeção direta.

2. **Renderização horizontal responsiva** — `_linhas_barra` substituído por
   `_linhas_barra(barra_de_menus, content_w)` com algoritmo normativo
   completo: normalização → validação defensiva → validação de âncoras →
   linha única → multilinha (`coluna_a_coluna`/`linha_a_linha`) →
   `RenderizadorErro` com `"erro_layout"`.

3. **Compatibilidade transitória** — alias string `"horizontal"` e
   `distribuicao` ausente/`None` continuam aceitos (defaults normativos
   sem âncoras).

4. **H-0015 preservado** — `l_barra = len(linhas_barra) + 2` permanece
   correto; com barra horizontal em 1 linha, `L_barra = 3` (antes 4) e
   `n_minimo = 15` (antes 16) em largura 42.

Todas as validações defensivas dos achados médios PR-M-01 a PR-M-04 foram
implementadas deterministicamente. Testes/snapshots foram atualizados para
refletir a barra horizontal. Arquivos proibidos e imutáveis intocados.

---

## Verificação de escopo

### Estado do repositório (verificado em execução real)

```text
git log --oneline -6:
  b2eb458 feat: ocupa altura do terminal pelo corpo
  4762583 docs: registra ocupacao vertical e barra responsiva
  8a6403a feat: migra arranjo vertical e barra declarativa
  ceaf0be docs: registra ADRs de arranjo e barra declarativa
  ab48702 feat: adiciona acesso demonstravel ao grupo minimo
  0bcb477 feat: implementa grupo estrutural minimo em tela isolada

git status --short:
   M config/telas/destino_minimo.json
   M config/telas/grupo_minimo.json
   M config/telas/orquestrador.json
   M config/telas/stub_b.json
   M tela/renderizador.py
   M tela/teste_demo.py
   M tela/teste_diagnostico.py
   M tela/teste_loader.py
   M tela/teste_modelo.py
   M tela/teste_renderizador.py
  ?? docs/handoff/H-0016-migracao-json-barra-de-menus-horizontal-responsiva.md
  ?? docs/relatorios/IMP-0016-migracao-json-barra-de-menus-horizontal-responsiva.md
  ?? docs/relatorios/RELATORIO_AUDITORIA_H-0016_HANDOFF.md
  ?? docs/relatorios/RELATORIO_AUDITORIA_H-0016_HANDOFF_POS_REVISAO.md

git diff --stat:
 config/telas/destino_minimo.json |  41 ++-
 config/telas/grupo_minimo.json   |  41 ++-
 config/telas/orquestrador.json   |  41 ++-
 config/telas/stub_b.json         |  41 ++-
 tela/renderizador.py             | 348 +++++++++++++++++--
 tela/teste_demo.py               |  34 +-
 tela/teste_diagnostico.py        |   3 +-
 tela/teste_loader.py             |  55 +++
 tela/teste_modelo.py             |  18 +
 tela/teste_renderizador.py       | 553 +++++++++++++++++++++++++++++--
 10 files changed, 1096 insertions(+), 79 deletions(-)
```

Arquivos alterados correspondem exatamente ao declarado no IMP-0016 e ao
escopo autorizado pelo handoff. **Nenhum arquivo fora do escopo foi
modificado.**

---

## Verificação da migração JSON

### Ponto 1 — Os 4 JSONs ativos foram migrados

| Arquivo | modo | politica | ancora primeiro | ancora ultimo |
|---------|------|----------|----------------|---------------|
| `orquestrador.json` | `horizontal_responsiva` | `declaracao` | `["chip_esc"]` | `["chip_ajuda"]` |
| `grupo_minimo.json` | `horizontal_responsiva` | `declaracao` | `["chip_esc"]` | `["chip_ajuda"]` |
| `destino_minimo.json` | `horizontal_responsiva` | `declaracao` | `["chip_esc"]` | `["chip_ajuda"]` |
| `stub_b.json` | `horizontal_responsiva` | `declaracao` | `["chip_esc"]` | `["chip_ajuda"]` |

Verificado por leitura direta dos 4 arquivos. **OK.**

### Ponto 3 — `ordem.politica = "declaracao"` (não "declaracao_validada")

Confirmado em todos os 4 JSONs. Achado B-002 da auditoria anterior
(uso de `"declaracao_validada"` fora da ADR-0014) foi integralmente
corrigido no handoff revisado e respeitado na implementação. **OK.**

### Ponto 4 — Âncoras usam IDs reais dos chips

`chip_esc` (primeiro) e `chip_ajuda` (último) correspondem exatamente
aos IDs declarados em `barra_de_menus.chips[]` nos 4 JSONs. **OK.**

### Diffs dos JSONs — escopo limitado a `distribuicao`

Inspeção do `git diff` de `orquestrador.json` confirma que **apenas o
campo `barra_de_menus.distribuicao`** foi alterado: de `"horizontal"`
(string) para o objeto canônico. Nenhuma outra linha do arquivo foi
tocada. O mesmo padrão de diff (+41 linhas, estrutura idêntica) se aplica
aos outros 3 JSONs. **OK.**

---

## Verificação da preservação dos chips

### Ponto 2 — chips[] preservado exatamente em cada JSON

Verificado por leitura direta dos 4 arquivos e por inspeção do diff (só
`distribuicao` mudou):

| JSON | chip_esc | chip_ajuda | ordem |
|------|----------|------------|-------|
| `orquestrador.json` | Esc/Sair/acao_contextual_esc/sempre/sempre/rotulo_dinamico | ?/Ajuda/abrir_ajuda/sempre/sempre/visivel_ativo | chip_esc primeiro, chip_ajuda último |
| `grupo_minimo.json` | Esc/Voltar/acao_contextual_esc/sempre/sempre/rotulo_dinamico | ?/Ajuda/abrir_ajuda/sempre/sempre/visivel_ativo | idem |
| `destino_minimo.json` | Esc/Voltar/acao_contextual_esc/sempre/sempre/rotulo_dinamico | ?/Ajuda/abrir_ajuda/sempre/sempre/visivel_ativo | idem |
| `stub_b.json` | Esc/Voltar/acao_contextual_esc/sempre/sempre/rotulo_dinamico | ?/Ajuda/abrir_ajuda/sempre/sempre/visivel_ativo | idem |

Campos `id`, `tecla`, `texto`, `acao`, `regra_existencia`, `regra_ativo`
e `forma_exibicao` preservados exatamente. Nenhum chip adicionado,
removido, reordenado ou alterado. **OK.**

---

## Verificação de loader/modelo

### Ponto 29 — loader.py, modelo.py, demo.py e diagnostico.py não foram alterados

```
git diff -- tela/loader.py tela/modelo.py tela/demo.py tela/diagnostico.py
(saída vazia — nenhum diff)
```

Confirmado. O dict bruto de `barra_de_menus` é preservado pelo loader
sem transformação de `distribuicao`; a validação é responsabilidade
exclusiva do renderer. Alinhado ao escopo negativo do handoff e à nota
PR-N-02. **OK.**

---

## Verificação da renderização horizontal responsiva

### Ponto 6 — Renderer usa `barra_de_menus.distribuicao` declarado no JSON

`_linhas_barra` lê `barra_de_menus.get("distribuicao")` e o normaliza;
objeto canônico declarado no JSON é usado diretamente (via
`_normalizar_distribuicao`). **OK.**

### Ponto 7 — Renderer não inventa distribuição fora do JSON

`_DISTRIBUICAO_HORIZONTAL_RESPONSIVA_DEFAULT` é usado apenas quando
`distribuicao` é `None`/ausente ou o alias `"horizontal"`. Para objeto
canônico, o JSON declarado é usado sem substituição. **OK.**

### Ponto 8 — Compatibilidade transitória com `"horizontal"` como alias legado

`_normalizar_distribuicao`: string `"horizontal"` → default sem âncoras.
Qualquer string diferente → `RenderizadorErro`. Alias não substitui o
caminho canônico; objeto declarado tem prioridade. Coberto por
`test_alias_string_horizontal_aceito`. **OK.**

### Ponto 9 — `_linhas_barra(barra_de_menus, content_w)` substitui o empilhamento vertical

Assinatura nova com `content_w: int` confirmada em `renderizador.py:445`.
Chamada em `renderizar_tela:669` atualizada para
`_linhas_barra(modelo.barra_de_menus, content_w)`. Empilhamento vertical
(um chip por linha) removido. **OK.**

### Ponto 10 — Linha única quando chips cabem

`renderizador.py:492-495`: calcula `sep_chips.join(texto_chips)`, verifica
`len(linha_unica) <= content_w`, retorna `[linha_unica]` se couber.
Coberto por `test_linha_unica_cabe`. **OK.**

### Ponto 11 — Multilinha quando linha única não cabe e linhas.maximo permite

`renderizador.py:501-511`: itera de 2 até `maximo`, aplica
`preenchimento_multilinha`, retorna na primeira configuração que encaixar.
Coberto por `test_linha_unica_nao_cabe_vai_para_multilinha`. **OK.**

### Ponto 12 — `coluna_a_coluna` determinístico

`_montar_coluna_a_coluna` (`renderizador.py:403-424`): preenche coluna por
coluna (`ceil(N/K)` usando `(n + n_linhas - 1) // n_linhas`), largura de
cada coluna = maior chip da coluna, colunas separadas por
`vao_entre_colunas.minimo`. Coberto por `test_coluna_a_coluna_layout`.
Verificado com exemplos do handoff: `[A,B,C,D,E]` e `K=2` →
`linha1="A  C  E"`, `linha2="B  D"`. **OK.**

### Ponto 13 — `linha_a_linha` implementado deterministicamente

`_montar_linha_a_linha` (`renderizador.py:427-442`): preenche linha por
linha, `ceil(N/K)` chips por linha, chips separados por
`vao_entre_chips.minimo`. Coberto por `test_linha_a_linha_implementado`.
**OK.**

### Ponto 14 — `RenderizadorErro` com `"erro_layout"` quando não couber

`renderizador.py:513-520`: levanta `RenderizadorErro` com mensagem
contendo `"erro_layout"` quando nenhuma configuração cabe. Coberto por
`test_multilinha_nao_cabe_erro_layout`. **OK.**

### Pontos 15–18 — Nenhum chip omitido/inventado/truncado/reordenado

A lista `texto_chips` é construída diretamente de `chips` (ordem
declarada, sem filtro). Nenhum chip é removido para caber (→
`RenderizadorErro`). Nenhum texto é cortado (`_texto_chip_barra` usa
os campos brutos do JSON). Coberto por
`test_chips_declarados_aparecem_exatamente_uma_vez` e
`test_ordem_preservada`. **OK.**

---

## Verificação de ordem e âncoras

### Pontos 4 e 5 — Âncoras como validação, não reordenação

`_validar_ancoras` (`renderizador.py:353-400`): verifica posições
iniciais/finais de `chips[]`; violação → `RenderizadorErro`; renderer
não move chips para satisfazer âncoras. Coberto por
`test_ancora_primeiro_violada`, `test_ancora_ultimo_violada`,
`test_ancora_id_inexistente`. **OK.**

### Âncora com id inexistente em chips[]

Verificado: id ausente em `chips[]` → `RenderizadorErro` na verificação
de existência antes da verificação de posição. **OK.**

### Âncora em posição errada

Verificado: id presente mas em posição errada → `RenderizadorErro` com
mensagem descritiva (posição esperada vs. encontrada). **OK.**

---

## Verificação de validações defensivas

Todas as notas médias PR-M-01 a PR-M-04 foram tratadas com erro
determinístico em `_validar_distribuicao` (`renderizador.py:282-350`):

| Validação | Campo | Comportamento | Teste |
|-----------|-------|---------------|-------|
| PR-M-01 | `ordem.politica` diferente de `"declaracao"` | `RenderizadorErro` | `test_politica_desconhecida_erro` |
| PR-M-02 | `preenchimento_multilinha` fora de `_PREENCHIMENTOS_MULTILINHA_VALIDOS` ou fora de `preenchimentos_multilinha_suportados` | `RenderizadorErro` | `test_preenchimento_multilinha_desconhecido_erro` |
| PR-M-03 | `linhas.minimo`/`maximo` não-int, `< 1` ou `maximo < minimo` | `RenderizadorErro` | `test_linhas_minimo_invalido_erro`, `test_linhas_maximo_menor_que_minimo_erro` |
| PR-M-04 | `overflow.quando_nao_couber` diferente de `"erro_layout"` ou flags não booleanas | `RenderizadorErro` | `test_overflow_desconhecido_erro`, `test_overflow_flag_nao_booleana_erro` |
| modo desconhecido | `distribuicao.modo` | `RenderizadorErro` | `test_modo_desconhecido_erro` |

Observação técnica: `_eh_int_nao_bool` exclui corretamente `bool` de
`isinstance(valor, int)` para tratar `true`/`false` JSON (que Python lê
como `bool`) como tipo inválido para `linhas.minimo`/`maximo`. **OK.**

---

## Verificação de preservação do H-0015

### Ponto 22 — Nova contabilidade `L_barra = 2 + N_linhas_barra`

`renderizador.py:681`: `l_barra = len(linhas_barra) + 2`. Com 2 chips
em `content_w=39`: `[Esc] Sair` (10) + 2 espaços + `[?] Ajuda` (9) =
21 ≤ 39 → 1 linha → `L_barra = 3`. Verificado em
`test_altura_minima_com_barra_horizontal` (`n_minimo=15`). **OK.**

### Ponto 23 — Altura explícita continua funcionando

`test_renderizar_tela_preserva_altura_h0015`: `renderizar_tela(altura=24)`
produz saída com exatamente 24 linhas. Lógica de preenchimento vertical
de `renderizador.py:679-710` preservada integralmente. **OK.**

### Ponto 24 — Barra continua no rodapé

`renderizador.py:712-715`: caixa da barra é sempre o último elemento
montado em `partes`. Linhas de fill são inseridas **antes** da barra.
**OK.**

### Ponto 25 — Erro determinístico de altura insuficiente preservado

`renderizador.py:684-700`: `RenderizadorErro` quando `l_cab + l_barra >
altura` ou `l_corpo_conteudo > l_corpo_disponivel`. Verificado por
execução dos testes. **OK.**

---

## Verificação de preservação dos fluxos g/d/b/Esc

### Ponto 26 — Fluxo g/d/b/Esc preservado

`test_fluxo_g_d_b_esc_preservado`: verifica que a saída do renderer
contém `[d]`, `[g]` (lancador) e `[Esc]`, `[?]` (barra). Nenhuma
alteração de semântica de teclas. `demo.py` e `diagnostico.py` não foram
alterados. **OK.**

---

## Verificação dos testes

### Ponto 27 — Diagnóstico determinístico e expectativa atualizada

`teste_diagnostico.py:28/28`: snapshot de `_EXPECTED_ORQUESTRADOR`
atualizado para refletir barra horizontal (`│ [Esc] Sair  [?] Ajuda`
em linha única). Diagnóstico permanece determinístico. **OK.**

### Ponto 28 — Snapshots/expectativas literais atualizados

Confirmado pelo IMP-0016 e pela inspeção dos testes:

- `teste_renderizador.py`: `_EXPECTED_ORQUESTRADOR` e
  `_EXPECTED_ORQUESTRADOR_RETA` refletem barra em 1 linha horizontal.
  `teste_altura_explicita`: `l_barra=3`, `n_minimo=15`. Linha 20 do
  layout a `altura=24` é fill (antes era `╭ Menus`); linha 21 é `╭ Menus`.
- `teste_demo.py`: snapshots de 42/80 cols com barra horizontal;
  `altura_minima=15`.
- `teste_diagnostico.py`: snapshot com linha horizontal.

Intenção de cada teste preservada; apenas o valor esperado espelhado à
saída horizontal correta. **OK.**

### Cobertura da classe `TestLinhasBarra`

Todos os casos obrigatórios definidos no handoff foram implementados:

| Caso | Método | Status |
|------|--------|--------|
| Linha única cabe | `test_linha_unica_cabe` | PASSOU |
| Multilinha quando linha única não cabe | `test_linha_unica_nao_cabe_vai_para_multilinha` | PASSOU |
| erro_layout quando não cabe | `test_multilinha_nao_cabe_erro_layout` | PASSOU |
| Alias string `"horizontal"` aceito | `test_alias_string_horizontal_aceito` | PASSOU |
| distribuicao ausente aceito | `test_distribuicao_ausente_aceito` | PASSOU |
| chips vazia retorna lista vazia | `test_chips_vazia_retorna_lista_vazia` | PASSOU |
| Âncora primeiro válida | `test_ancora_primeiro_valida` | PASSOU |
| Âncora primeiro violada | `test_ancora_primeiro_violada` | PASSOU |
| Âncora último válida | `test_ancora_ultimo_valida` | PASSOU |
| Âncora último violada | `test_ancora_ultimo_violada` | PASSOU |
| Âncora id inexistente | `test_ancora_id_inexistente` | PASSOU |
| Ordem preservada | `test_ordem_preservada` | PASSOU |
| Chips declarados aparecem exatamente uma vez | `test_chips_declarados_aparecem_exatamente_uma_vez` | PASSOU |
| Chips do lancador não entram na barra | `test_chips_do_lancador_nao_entram_na_barra` | PASSOU |
| `coluna_a_coluna` layout | `test_coluna_a_coluna_layout` | PASSOU |
| `linha_a_linha` implementado | `test_linha_a_linha_implementado` | PASSOU |
| Modo desconhecido erro | `test_modo_desconhecido_erro` | PASSOU |
| Política desconhecida erro (PR-M-01) | `test_politica_desconhecida_erro` | PASSOU |
| Preenchimento desconhecido erro (PR-M-02) | `test_preenchimento_multilinha_desconhecido_erro` | PASSOU |
| Linhas mínimo inválido erro (PR-M-03) | `test_linhas_minimo_invalido_erro` | PASSOU |
| Linhas máximo < mínimo erro (PR-M-03) | `test_linhas_maximo_menor_que_minimo_erro` | PASSOU |
| Overflow desconhecido erro (PR-M-04) | `test_overflow_desconhecido_erro` | PASSOU |
| Overflow flag não booleana erro (PR-M-04) | `test_overflow_flag_nao_booleana_erro` | PASSOU |
| renderizar_tela com canônico | `test_renderizar_tela_com_distribuicao_canonica` | PASSOU |
| Preserva altura H-0015 | `test_renderizar_tela_preserva_altura_h0015` | PASSOU |
| Altura mínima com barra horizontal | `test_altura_minima_com_barra_horizontal` | PASSOU |
| Fluxo g/d/b/Esc preservado | `test_fluxo_g_d_b_esc_preservado` | PASSOU |

Cobertura cruzada em `teste_loader.py` (12 novas asserções H-0016: os 4
JSONs carregam com `distribuicao` como objeto com `modo`/`politica`/âncoras
corretas) e `teste_modelo.py` (3 novas asserções H-0016: modelo expõe
`distribuicao` como objeto). **OK.**

### Ponto 31 — IMP-0016 existe e trata PR-M-01 a PR-M-04 e PR-N-01/PR-N-02

Arquivo `docs/relatorios/IMP-0016-migracao-json-barra-de-menus-horizontal-responsiva.md`
existe (arquivo não rastreado `??`). Contém seção "Tratamento das notas da
auditoria pós-revisão" com subseções para PR-M-01, PR-M-02, PR-M-03,
PR-M-04, PR-N-01 e PR-N-02, cada uma com evidência de tratamento e teste
cobrindo o caso. **OK.**

---

## Verificação de arquivos alterados

### Ponto 29 — Arquivos imutáveis não foram alterados

```
git diff -- tela/loader.py tela/modelo.py tela/demo.py tela/diagnostico.py
(saída vazia)
```

Confirmado: nenhum arquivo de fonte não autorizado foi modificado. **OK.**

### Ponto 30 — Arquivos proibidos não foram alterados

```
git diff -- docs/contratos/ docs/adr/ docs/NOMENCLATURA.md \
            config/estilo.json config/lancador.json config/layout_console.json
(saída vazia)
```

Confirmado: nenhum arquivo proibido foi tocado. **OK.**

---

## Verificação de limpeza do workspace

### Ponto 32 — Nenhum `__pycache__` ou `.pyc`

```bash
find . -name '__pycache__' -type d -prune -print
(sem saída)

find . -name '*.pyc' -print
(sem saída)
```

Workspace limpo. O uso de `sys.dont_write_bytecode = True` nos arquivos
de teste impede a geração de bytecode. **OK.**

---

## Verificação de escopo negativo

Itens do escopo negativo verificados por inspeção do `git diff` e leitura
do código:

| Item proibido | Status |
|---------------|--------|
| composição horizontal do corpo | NÃO implementado |
| `corpo.arranjo = "horizontal"` | NÃO implementado |
| distribuição de altura entre elementos do corpo | NÃO implementado |
| correção do preenchimento vertical do H-0015 | NÃO implementado |
| grupo com 2 elementos | NÃO implementado |
| aninhamento | NÃO implementado |
| percentual/fração | NÃO implementado |
| console real | NÃO implementado |
| foco entre elementos / navegação por `[✥]` | NÃO implementado |
| paginação / filtros / modo verboso / seleção | NÃO implementado |
| registry novo de ações/telas | NÃO implementado |
| mudança semântica de Esc, g, d, b ou Enter | NÃO implementado |
| hardcoding de lista canônica global de chips | NÃO implementado |
| truncamento de texto de chip | NÃO implementado |
| omissão de chip quando não couber | NÃO implementado |
| reordenação heurística de chips | NÃO implementado |
| fallback vertical um-chip-por-linha | NÃO implementado |
| uso de regras do lancador como regras da barra | NÃO implementado |
| inclusão de chips do lancador na barra | NÃO implementado |

Todos os itens do escopo negativo confirmados como não implementados. **OK.**

---

## Achados

Nenhum achado bloqueante, alto ou médio. As notas abaixo são observações
técnicas de baixa severidade que não comprometem a implementação.

### QA-N-01 — Dupla validação de `preenchimento_multilinha`

- **Severidade**: nota
- **Evidência**: `_validar_distribuicao` (`renderizador.py:308-317`)
  valida `preenchimento_multilinha` contra `_PREENCHIMENTOS_MULTILINHA_VALIDOS`
  (tupla hardcoded) E contra `preenchimentos_multilinha_suportados` do JSON.
  Com a estrutura canônica atual (ambas as listas idênticas), a dupla
  verificação é redundante.
- **Impacto**: Nenhum no ciclo atual. Em cenário futuro onde
  `preenchimentos_multilinha_suportados` no JSON declare um subconjunto de
  `_PREENCHIMENTOS_MULTILINHA_VALIDOS`, o comportamento poderia ser
  assimétrico.
- **Recomendação**: Registrar para revisão futura. Não bloqueia este ciclo.

### QA-N-02 — `preenchimentos_multilinha_suportados` (herança de PR-N-01)

- **Severidade**: nota
- **Evidência**: Campo `preenchimentos_multilinha_suportados` está presente
  nos 4 JSONs migrados conforme especificado no handoff, mas não faz parte
  da estrutura canônica de referência da ADR-0014.
- **Impacto**: Baixo. Campo não contradiz semântica da ADR; serve como
  metadado declarativo consumido pelo renderer.
- **Recomendação**: Registrado no IMP-0016 para revisão futura de
  ADR/contrato. Não bloqueia este ciclo. (Herda de PR-N-01.)

---

## Resultado dos testes

```
python tela/teste_loader.py     → exit 0  (79/79)   [12 novas H-0016]
python tela/teste_modelo.py     → exit 0  (56/56)   [3 novas H-0016]
python tela/teste_renderizador.py → exit 0 (171/171) [38 novas H-0016 em TestLinhasBarra + snapshots]
python tela/teste_demo.py       → exit 0  (117/117) [snapshots atualizados]
python tela/teste_diagnostico.py → exit 0  (28/28)  [snapshot atualizado]

Total: 451/451 verificações passando
```

---

## Conclusão

A implementação do H-0016 está **correta, completa e dentro do escopo
declarado**. Todos os 32 pontos obrigatórios de QA foram verificados e
confirmados. Nenhum achado bloqueante, alto ou médio foi identificado.
Dois achados de nota referentes a (a) dupla validação de
`preenchimento_multilinha` e (b) extensão do campo
`preenchimentos_multilinha_suportados` na ADR-0014, ambos herdados das
auditorias anteriores e sem impacto no ciclo atual.

A dívida técnica do ADR-0014 identificada no H-0015 foi integralmente
quitada: os 4 JSONs ativos estão no formato canônico declarativo; o
renderer implementa o algoritmo normativo mínimo (linha única →
multilinha → `erro_layout`); âncoras funcionam como validação
declarativa (não reordenação). O H-0015 é preservado com a nova
contabilidade `L_barra = 2 + N_linhas_barra = 3`.

---

## Próxima ação recomendada

```text
1. Aprovar o ciclo H-0016: QA_APPROVED, sem pendências bloqueantes.
2. Fazer commit da implementação (todos os 10 arquivos modificados +
   4 arquivos não rastreados de documentação).
3. Registrar QA-N-01 e QA-N-02 como itens de backlog para revisão
   futura da ADR-0014 e do contrato_json_barra_de_menus.md.
4. Iniciar planejamento do próximo ciclo.
```
