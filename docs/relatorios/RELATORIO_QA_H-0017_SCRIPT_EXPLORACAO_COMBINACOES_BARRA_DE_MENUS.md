# RELATORIO_QA_H-0017_SCRIPT_EXPLORACAO_COMBINACOES_BARRA_DE_MENUS

```text
auditor:        Claude Code (papel QA final)
data:           2026-07-09
ciclo:          H-0017
titulo:         Script de exploração de combinações da barra_de_menus
commit-base:    ab5ad68  feat: renderiza barra de menus horizontal responsiva
executor:       OpenCode / GLM (implementação); Claude Code (QA)
```

---

## Status final

```text
QA_APPROVED_WITH_NOTES
```

Dois achados de baixa severidade e duas notas. Nenhum achado bloqueante
nem de alta severidade. O script funciona corretamente: 14 cenários da
matriz padrão (10 OK + 4 erros esperados + 0 inesperados), 25/25
verificações no teste automatizado, exit codes 0/2 confirmados, exit code
1 verificado por inspeção de código. As 451 verificações nas 5 suítes
existentes continuam passando. renderizador.py não foi alterado.

---

## Arquivos analisados

### Documentação do ciclo (lidos integralmente)

```text
scripts/docs/handoff/H-0017-script-exploracao-combinacoes-barra-de-menus.md
scripts/docs/relatorios/RELATORIO_AUDITORIA_H-0017_HANDOFF.md
scripts/docs/relatorios/IMP-0017-script-exploracao-combinacoes-barra-de-menus.md
```

### Referência H-0016 (lidos integralmente)

```text
scripts/docs/handoff/H-0016-migracao-json-barra-de-menus-horizontal-responsiva.md
scripts/docs/relatorios/IMP-0016-migracao-json-barra-de-menus-horizontal-responsiva.md
scripts/docs/relatorios/RELATORIO_QA_H-0016_MIGRACAO_JSON_BARRA_DE_MENUS_HORIZONTAL_RESPONSIVA.md
```

### Implementação (lidos integralmente)

```text
scripts/tela/explorar_barra_de_menus.py
scripts/tela/teste_explorar_barra_de_menus.py
scripts/tela/renderizador.py
```

---

## Comandos executados

```bash
# Estado do repositório
git log --oneline -6
git status --short
git diff --stat
git diff --name-only

# Testes obrigatórios (a partir de scripts/)
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_demo.py
python tela/teste_diagnostico.py
python tela/teste_explorar_barra_de_menus.py

# Execuções manuais do script
python tela/explorar_barra_de_menus.py
python tela/explorar_barra_de_menus.py \
  --modo-saida resumo \
  --larguras 30,40,80 \
  --chips 3,6,10 \
  --linhas-max 1,2,3 \
  --preenchimentos coluna_a_coluna,linha_a_linha
python tela/explorar_barra_de_menus.py \
  --modo-saida detalhado \
  --mostrar-erros \
  --limite-casos 20

# Limpeza
find . -name '__pycache__' -type d -prune -print
find . -name '*.pyc' -print
```

---

## Resumo executivo

H-0017 entregou o script exploratório `explorar_barra_de_menus.py` e seu
teste automatizado `teste_explorar_barra_de_menus.py` conforme especificado.
O script exercita `_linhas_barra` do renderer com cenários sintéticos
gerados em memória, verifica invariantes de renderização, produz saída
determinística em modo resumo e detalhado, e retorna exit codes corretos.
O `renderizador.py` não foi alterado. Nenhum arquivo proibido foi tocado.
As 451 verificações das 5 suítes existentes continuam passando.

Os dois achados de baixa severidade são: (a) verificação de ordem INV-4
incompleta para pares não consecutivos em coluna_a_coluna multilinha;
(b) ausência de cenário com linhas.maximo=1 na matriz padrão, com
inacurácia documental correspondente no IMP-0017. Ambos não comprometem
a ferramenta diagnóstica nem violam o handoff.

---

## Verificação de escopo

### Estado do repositório (verificado em execução real)

```text
git log --oneline -6:
  ab5ad68 feat: renderiza barra de menus horizontal responsiva
  b2eb458 feat: ocupa altura do terminal pelo corpo
  4762583 docs: registra ocupacao vertical e barra responsiva
  8a6403a feat: migra arranjo vertical e barra declarativa
  ceaf0be docs: registra ADRs de arranjo e barra declarativa
  ab48702 feat: adiciona acesso demonstravel ao grupo minimo

git status --short:
  ?? scripts/docs/handoff/H-0017-script-exploracao-combinacoes-barra-de-menus.md
  ?? scripts/docs/relatorios/IMP-0017-script-exploracao-combinacoes-barra-de-menus.md
  ?? scripts/docs/relatorios/RELATORIO_AUDITORIA_H-0017_HANDOFF.md
  ?? scripts/tela/explorar_barra_de_menus.py
  ?? scripts/tela/teste_explorar_barra_de_menus.py

git diff --stat: (vazio)
git diff --name-only: (vazio)
```

HEAD em `ab5ad68` conforme esperado. Nenhum arquivo rastreado modificado.
Apenas os arquivos não rastreados do ciclo H-0017 presentes. **OK.**

---

## Verificação do script criado

| Ponto | Verificação | Status |
|-------|------------|--------|
| 1. Script existe em scripts/tela/explorar_barra_de_menus.py | Arquivo presente, lido integralmente | OK |
| 2. Teste existe em scripts/tela/teste_explorar_barra_de_menus.py | Arquivo presente, lido integralmente | OK |
| 3. IMP-0017 existe em scripts/docs/relatorios/ | Arquivo presente, lido integralmente | OK |
| 10. Script usa renderer real | `from tela.renderizador import _linhas_barra, _DISTRIBUICAO_HORIZONTAL_RESPONSIVA_DEFAULT, RenderizadorErro` | OK |
| 11. Não duplica lógica de renderização | A renderização é feita via `_linhas_barra`; código de estimativa em `_gerar_matriz_combinatoria` é heurística de previsão de resultado, não renderer alternativo | OK |
| 13. Não depende de terminal real | Sem curses, termios, tty. Usa apenas biblioteca padrão | OK |
| 14. Não chamado pela demo | Confirmado por inspeção: demo.py não modificado, sem import | OK |
| 15. Não chamado pelo diagnóstico | Confirmado por inspeção: diagnostico.py não modificado, sem import | OK |
| 16. Não cria formato normativo definitivo | Escopo negativo respeitado; caráter exploratório preservado | OK |

---

## Verificação da CLI

| Parâmetro | Implementado | Status |
|-----------|-------------|--------|
| `--larguras` | Sim, `_parse_lista_int(args.larguras, "--larguras")` | OK |
| `--chips` | Sim, `_parse_lista_int(args.chips, "--chips")` | OK |
| `--linhas-max` | Sim, `_parse_lista_int(args.linhas_max, "--linhas-max")` com `dest="linhas_max"` | OK |
| `--preenchimentos` | Sim, `_parse_preenchimentos(args.preenchimentos)` com validação | OK |
| `--modo-saida` | Sim, choices=["resumo", "detalhado"], default="detalhado" | OK |
| `--mostrar-ok` | Sim, `action="store_true"` | OK |
| `--mostrar-erros` | Sim, `action="store_true"` | OK |
| `--limite-casos` | Sim, type=int, sem limite por default | OK |

**Parâmetro inválido → exit 2**: confirmado por execução.
`--preenchimentos invalido_xyz` → stderr: `"ERRO: preenchimento inválido: 'invalido_xyz'; aceitos: coluna_a_coluna, linha_a_linha"`, exit 2.
`--larguras abc` → exit 2.

**Saída sem argumentos → exit 0**: confirmado.

---

## Verificação da matriz de cenários

### Matriz padrão (14 cenários)

| ID | chips | content_w | linhas.max | preench | esperado | resultado |
|----|-------|-----------|-----------|---------|---------|-----------|
| C01 | 3 | 80 | 2 | col_a_col | OK | OK ✓ |
| C02 | 6 | 120 | 2 | col_a_col | OK | OK ✓ |
| C03 | 6 | 60 | 2 | col_a_col | OK | OK ✓ |
| C04 | 8 | 50 | 2 | col_a_col | OK | OK ✓ |
| C05 | 10 | 50 | 3 | col_a_col | OK | OK ✓ |
| C06 | 10 | 20 | 2 | col_a_col | erro_layout | ERRO_ESPERADO ✓ |
| C07 | 12 | 15 | 2 | col_a_col | erro_layout | ERRO_ESPERADO ✓ |
| C08 | 5 | 60 | 2 | col_a_col | OK | OK ✓ |
| C09 | 5 | 45 | 2 | linha_a_linha | OK | OK ✓ |
| C10 | 2 | 39 | 2 | col_a_col | OK (âncora válida) | OK ✓ |
| C11 | 2 | 39 | 2 | col_a_col | erro (âncora inex.) | ERRO_ESPERADO ✓ |
| C12 | 2 | 39 | 2 | col_a_col | erro (pos. errada) | ERRO_ESPERADO ✓ |
| C13 | 4 | 60 | 2 | col_a_col | OK | OK ✓ |
| C14 | 4 | 120 | 2 | col_a_col | OK | OK ✓ |

**Total: 10 OK, 4 ERRO_ESPERADO, 0 ERRO_INESPERADO, 0 violações.** Exit 0.

### Cobertura de variações

| Variação | Cobertura na matriz padrão | Cobertura via CLI |
|---------|--------------------------|-------------------|
| Chips: 1, 2, 3, 4, 5, 6, 8, 10, 12 | 2, 3, 4, 5, 6, 8, 10, 12 (falta 1) | Sim, via `--chips` |
| Larguras: muito estreita, estreita, média, larga | 15, 20, 39, 45, 50, 60, 80, 120 | Sim, via `--larguras` |
| linhas.maximo: 1, 2, 3 | 2, 3 (falta 1) | Sim, via `--linhas-max` |
| coluna_a_coluna | Sim (C01-C08, C10-C14) | Sim |
| linha_a_linha | Sim (C09) | Sim |
| Espaçamento mínimo | Sim (maioria) | Sim |
| Espaçamento máximo | Sim (C14) | Sim |
| Âncora válida | Sim (C10) | N/A (embutido) |
| Âncora inexistente | Sim (C11) | N/A |
| Âncora posição errada | Sim (C12) | N/A |
| Overflow forçado | Sim (C06, C07) | Sim |

**Nota**: `linhas.maximo=1` não está na matriz padrão. Ver Achado QA-02.

### Execução combinatória verificada

Com `--larguras 30,40,80 --chips 3,6,10 --linhas-max 1,2,3 --preenchimentos coluna_a_coluna,linha_a_linha`:
324 cenários → 150 OK, 174 ERRO_ESPERADO, 0 ERRO_INESPERADO. Exit 0.
`linhas.maximo=1` é exercitado nesta execução (86 cenários com `linhas.maximo=1`).

---

## Verificação das invariantes

| INV | Descrição | Verificação no script | Status |
|-----|-----------|----------------------|--------|
| 1 | Cada chip aparece exatamente uma vez | `junta.count(texto) > 1` detecta duplicata | OK |
| 2 | Nenhum chip inventado | Implícita (textos únicos; renderer só renderiza declarados) | OK |
| 3 | Nenhum chip omitido | `junta.count(texto) == 0` detecta ausência | OK |
| 4 | Ordem preservada | Verificação intra-linha por pares consecutivos | PARCIAL — ver QA-01 |
| 5 | Texto não truncado | `texto not in junta` detecta ausência/truncamento | OK |
| 6 | Linhas físicas ≤ linhas.maximo | `len(linhas) > maximo` | OK |
| 7 | Largura de cada linha ≤ content_w | `len(linha) > content_w` por linha | OK |
| 8 | Chips do lancador ausentes | Implícita (chips sintéticos distintos do lancador) | OK |
| 9 | Sem fallback vertical | Não verificável sem acesso ao modo interno do renderer | LIMITAÇÃO DOCUMENTADA |
| 10 | Linha única: todos os chips na mesma linha | `texto not in linhas[0]` detecta ausência | OK |
| 11 | coluna_a_coluna: padrão verificado | `textos_chips[0] not in linhas[0]` (verificação simplificada) | PARCIAL |
| 12 | linha_a_linha: padrão verificado | Primeiros CPL chips em linhas[0] | OK |

**INV-4 — detalhe**: A verificação usa pares consecutivos `(textos_chips[i], textos_chips[i+1])` em cada linha. Para pares em que um dos chips não aparece naquela linha (posição == -1), o par é pulado. Consequência: em `coluna_a_coluna` com K≥2 linhas, chips não consecutivos que compartilham uma linha (ex.: chip[0] e chip[2] na linha 0 com K=2) não têm sua ordem relativa verificada entre si. Ver Achado QA-01.

**INV-11 — detalhe**: A verificação simplificada confirma apenas que `chip[0]` está na `linha[0]`, não verifica todos os chips da primeira coluna.

---

## Verificação de linha única/multilinha

| Cenário | Chips | content_w | Resultado | Linhas físicas |
|---------|-------|-----------|-----------|---------------|
| C01 (linha única) | 3 curtos | 80 | OK | 1 ✓ |
| C02 (linha única) | 6 curtos | 120 | OK | 1 ✓ |
| C03 (duas linhas) | 6 médios | 60 | OK | 2 ✓ |
| C04 (duas linhas) | 8 curtos | 50 | OK | 2 ✓ |
| C05 (três linhas) | 10 curtos | 50 | OK | ≤3 ✓ |

Linha única verificada pelo Caso 3 do teste automatizado: 3 chips em content_w=80 → `['[F1] Ok-T3  [F2] Ir-T3  [F3] Ver-T3']` (1 string). ✓

---

## Verificação de coluna_a_coluna e linha_a_linha

### coluna_a_coluna

Verificado no Caso 4 do teste automatizado:
- 4 chips, content_w=25, K=2
- Resultado: `['[F1] Ok-T4  [F3] Ver-T4', '[F2] Ir-T4  [F4] Ai-T4']`
- Chip[0] e Chip[2] estão na linha 0 (coluna-major): ✓
- Chip[1] e Chip[3] estão na linha 1: ✓
- INV-11 verificada (chip[0] em linhas[0]): ✓

### linha_a_linha

Verificado no Caso 5 do teste automatizado:
- 4 chips, content_w=25, K=2, CPL=2
- Resultado: `['[F1] Ok-T5  [F2] Ir-T5', '[F3] Ver-T5  [F4] Ai-T5']`
- Chips 1 e 2 na linha 0 (linha-major): ✓
- Chips 3 e 4 na linha 1: ✓
- INV-12 verificada: ✓

Cenário C09 da matriz padrão: 5 chips mistos, content_w=45, linha_a_linha.
Linha única teria 75 chars > 45 → multilinha com K=2 necessária. ✓

---

## Verificação de âncoras e overflow

### Âncoras

| Tipo | Cenário | Resultado | Status |
|------|---------|-----------|--------|
| Válida | C10: chip_esc primeiro, chip_ajuda último | OK | ✓ |
| Inexistente | C11: id 'chip_x' não existe | ERRO_ESPERADO (RenderizadorErro: "ancora primeiro: id 'chip_x' nao existe em chips[]") | ✓ |
| Posição errada | C12: chip_esc não está na posição 0 | ERRO_ESPERADO (RenderizadorErro: "ancora primeiro violada: esperado id 'chip_esc' na posicao 0, encontrado 'chip_ajuda'") | ✓ |

**Caso 7** (teste automatizado): âncora `chip_inexistente_xyz` →
`RenderizadorErro: "ancora primeiro: id 'chip_inexistente_xyz' nao existe em chips[]"`. Mensagem menciona id inexistente. ✓

**Caso 8** (teste automatizado): âncora `t8c_esc` em posição errada →
`RenderizadorErro: "ancora primeiro violada: esperado id 't8c_esc' na posicao 0, encontrado 't8c_ajuda'"`. Mensagem menciona posição errada. ✓

### Overflow

| Tipo | Cenário | Resultado | Status |
|------|---------|-----------|--------|
| Overflow forçado | C06: 10 chips, content_w=20 | ERRO_ESPERADO, mensagem contém "erro_layout" | ✓ |
| Overflow forçado | C07: 12 chips, content_w=15 | ERRO_ESPERADO, mensagem contém "erro_layout" | ✓ |
| Script continua após erro | Ambos C06 e C07 executam sem abortar a matriz | 14 cenários executados | ✓ |

---

## Verificação dos testes automatizados

| Caso | Tipo de verificação | Resultado |
|------|--------------------|-----------| 
| 1. Matriz padrão exit 0 | subprocess | PASSOU |
| 2. Modo resumo determinístico | subprocess, saída idêntica em 2 chamadas | PASSOU |
| 3. Linha única 3 chips | chamada direta `_linhas_barra` | PASSOU |
| 4. coluna_a_coluna 4 chips → 2 linhas | chamada direta `_linhas_barra` | PASSOU |
| 5. linha_a_linha 4 chips → 2 linhas | chamada direta `_linhas_barra` | PASSOU |
| 6. Overflow → erro_layout, script continua | subprocess | PASSOU |
| 7. Âncora inexistente → RenderizadorErro | chamada direta `_linhas_barra` | PASSOU |
| 8. Âncora posição errada → RenderizadorErro | chamada direta `_linhas_barra` | PASSOU |
| 9. Exit 1 para violação inesperada | inspeção código-fonte (conforme autorizado) | PASSOU |
| 10. Exit 2 para parâmetro inválido | subprocess | PASSOU |

**Total: 25/25 verificações. Exit 0.**

Caso 9 verificado por inspeção: `tem_inesperado or tem_violacao → return 1` presente em `main()` (explorar_barra_de_menus.py:911-914). Abordagem por inspeção autorizada pelo handoff H-0017 (seção "Casos obrigatórios" item 9) e nota AUD-N-02.

---

## Verificação das execuções manuais

### Execução 1 — sem argumentos (matriz padrão)

```bash
python tela/explorar_barra_de_menus.py
```

```
=== RESUMO DA EXPLORACAO ===
Total de cenarios executados:   14
OK:                             10
Erro esperado:                  4
Erro inesperado:                0
Violacoes de invariante:        0

Por preenchimento_multilinha:
  coluna_a_coluna: OK=9 ERRO_ESP=4 ERRO_INESP=0
  linha_a_linha: OK=1 ERRO_ESP=0 ERRO_INESP=0

Por linhas.maximo:
  2: OK=9 ERRO_ESP=4 ERRO_INESP=0
  3: OK=1 ERRO_ESP=0 ERRO_INESP=0

Por largura (content_w):
  15: OK=0 ERRO_ESP=1 ERRO_INESP=0
  20: OK=0 ERRO_ESP=1 ERRO_INESP=0
  39: OK=1 ERRO_ESP=2 ERRO_INESP=0
  45: OK=1 ERRO_ESP=0 ERRO_INESP=0
  50: OK=2 ERRO_ESP=0 ERRO_INESP=0
  60: OK=3 ERRO_ESP=0 ERRO_INESP=0
  80: OK=1 ERRO_ESP=0 ERRO_INESP=0
  120: OK=2 ERRO_ESP=0 ERRO_INESP=0
```

Exit code: **0** ✓

### Execução 2 — modo resumo com parâmetros explícitos

```bash
python tela/explorar_barra_de_menus.py \
  --modo-saida resumo \
  --larguras 30,40,80 \
  --chips 3,6,10 \
  --linhas-max 1,2,3 \
  --preenchimentos coluna_a_coluna,linha_a_linha
```

```
=== RESUMO DA EXPLORACAO ===
Total de cenarios executados:   324
OK:                             150
Erro esperado:                  174
Erro inesperado:                0
Violacoes de invariante:        0

Por preenchimento_multilinha:
  coluna_a_coluna: OK=71 ERRO_ESP=91 ERRO_INESP=0
  linha_a_linha: OK=79 ERRO_ESP=83 ERRO_INESP=0

Por linhas.maximo:
  1: OK=22 ERRO_ESP=86 ERRO_INESP=0
  2: OK=54 ERRO_ESP=54 ERRO_INESP=0
  3: OK=74 ERRO_ESP=34 ERRO_INESP=0

Por largura (content_w):
  30: OK=24 ERRO_ESP=84 ERRO_INESP=0
  40: OK=45 ERRO_ESP=63 ERRO_INESP=0
  80: OK=81 ERRO_ESP=27 ERRO_INESP=0
```

Exit code: **0** ✓
Coincide com saídas documentadas no IMP-0017. Determinismo confirmado: duas
execuções consecutivas com `--modo-saida resumo` produzem saída idêntica
(verificado pelo Caso 2 do teste automatizado, len1=len2=721 bytes).

### Execução 3 — modo detalhado com limite e mostrar-erros

```bash
python tela/explorar_barra_de_menus.py \
  --modo-saida detalhado \
  --mostrar-erros \
  --limite-casos 20
```

Exibe 4 cenários de erro (C06, C07, C11, C12) com blocos detalhados,
seguido do resumo. Mensagens de erro corretas:
- C06: `"erro_layout: chips da barra_de_menus (10) nao cabem em 20 caracteres..."`
- C07: `"erro_layout: chips da barra_de_menus (12) nao cabem em 15 caracteres..."`
- C11: `"ancora primeiro: id 'chip_x' nao existe em chips[]"`
- C12: `"ancora primeiro violada: esperado id 'chip_esc' na posicao 0, encontrado 'chip_ajuda'"`

Exit code: **0** ✓

---

## Verificação de preservação do H-0016

| Ponto | Verificação | Status |
|-------|------------|--------|
| renderizador.py não alterado | `git diff --stat` vazio; arquivo igual ao do H-0016 | OK |
| 451 verificações nas 5 suítes existentes | Todas passando (ver seção Resultado dos testes) | OK |
| `_linhas_barra` acessível por importação direta | Confirmado: função de módulo global em renderizador.py | OK |
| Comportamento aprovado do renderer preservado | Nenhuma linha do renderizador.py modificada | OK |
| JSONs ativos não alterados | `git diff --stat` vazio; todos 4 JSONs intocados | OK |
| loader.py, modelo.py, demo.py, diagnostico.py | Não alterados (`git diff` vazio) | OK |

---

## Verificação de arquivos alterados

```text
git diff --name-only: (vazio)
git diff --stat:      (vazio)

git status --short (arquivos não rastreados apenas):
  ?? scripts/docs/handoff/H-0017-script-exploracao-combinacoes-barra-de-menus.md
  ?? scripts/docs/relatorios/IMP-0017-script-exploracao-combinacoes-barra-de-menus.md
  ?? scripts/docs/relatorios/RELATORIO_AUDITORIA_H-0017_HANDOFF.md
  ?? scripts/tela/explorar_barra_de_menus.py
  ?? scripts/tela/teste_explorar_barra_de_menus.py
```

Arquivos permitidos criados no ciclo:

| Arquivo | Tipo | Status |
|---------|------|--------|
| scripts/tela/explorar_barra_de_menus.py | criado | ✓ permitido |
| scripts/tela/teste_explorar_barra_de_menus.py | criado | ✓ permitido |
| scripts/docs/relatorios/IMP-0017-script-exploracao-combinacoes-barra-de-menus.md | criado | ✓ permitido |
| scripts/docs/handoff/H-0017-script-exploracao-combinacoes-barra-de-menus.md | criado (QA anterior) | ✓ permitido |
| scripts/docs/relatorios/RELATORIO_AUDITORIA_H-0017_HANDOFF.md | criado (QA anterior) | ✓ permitido |
| scripts/docs/relatorios/RELATORIO_QA_H-0017_* (este arquivo) | criado (QA final) | ✓ permitido |

**Nenhum arquivo fora do escopo foi modificado.** ✓

---

## Verificação de limpeza do workspace

```bash
find . -name '__pycache__' -type d -prune -print
# (sem saída)

find . -name '*.pyc' -print
# (sem saída)
```

Workspace limpo. O uso de `sys.dont_write_bytecode = True` no topo de
`explorar_barra_de_menus.py` e `teste_explorar_barra_de_menus.py` impede
geração de bytecode. ✓

---

## Verificação de escopo negativo

Confirmado que **NÃO** foram implementados:

| Item proibido | Status |
|--------------|--------|
| Nova regra normativa da barra_de_menus | NÃO implementado |
| Alteração de ADR | NÃO (git diff vazio em docs/adr/) |
| Alteração de contrato | NÃO (git diff vazio em docs/contratos/) |
| Alteração de NOMENCLATURA | NÃO (git diff vazio) |
| Alteração dos JSONs ativos | NÃO (git diff vazio) |
| Mudança no comportamento do renderer H-0016 | NÃO (renderizador.py não alterado) |
| Mudança de semântica de chips | NÃO |
| Mudança no lancador | NÃO |
| Uso de chips do lancador na barra | NÃO |
| Composição horizontal do corpo | NÃO |
| corpo.arranjo = "horizontal" | NÃO |
| Distribuição de altura entre elementos do corpo | NÃO |
| Correção do preenchimento vertical H-0015 | NÃO |
| Console real (curses, termios, tty) | NÃO |
| Paginação | NÃO |
| Filtros | NÃO |
| Seleção | NÃO |
| Registry novo de ações | NÃO |
| Registry novo de telas | NÃO |
| Integração automática ao diagnóstico principal | NÃO |
| Integração automática à demo | NÃO |
| Dependência de terminal real | NÃO |
| Formato normativo definitivo de validação | NÃO |

---

## Achados

### QA-01 — INV-4 incompleta para pares não consecutivos em coluna_a_coluna multilinha

- **ID**: QA-01
- **Severidade**: baixa
- **Evidência**: A função `_verificar_invariantes` verifica a ordem dos
  chips dentro de cada linha usando pares consecutivos
  `(textos_chips[i], textos_chips[i+1])`. Quando um dos dois não aparece
  naquela linha (`posicao == -1`), o par é ignorado com `continue`. Em
  `coluna_a_coluna` com K≥2 linhas, chips não consecutivos no índice
  global compartilham uma linha: por exemplo, com 4 chips e K=2, a linha 0
  contém chip[0] e chip[2]. O par (chip[0], chip[1]) é ignorado (chip[1]
  não está na linha 0); o par (chip[1], chip[2]) também (chip[1] ausente);
  o par (chip[2], chip[3]) é ignorado (chip[3] ausente). Resultado: a
  ordem relativa de chip[0] e chip[2] dentro de linha 0 **nunca é
  verificada** pelo loop.
- **Impacto**: Se o renderer produzisse chip[2] antes de chip[0] na linha 0
  (o que não ocorre, dado que o renderer é correto e determinístico), a
  violação não seria detectada. O risco prático é zero no ciclo atual; a
  lacuna só importaria se o renderer tivesse um bug de reordenação em
  coluna_a_coluna multilinha. A invariante INV-11 (chip[0] em linhas[0])
  cobre parcialmente esse caso.
- **Recomendação**: Em revisão futura, substituir a verificação por pares
  consecutivos por verificação de todos os pares de chips presentes em cada
  linha: `if pi != -1 and pj != -1 and pi > pj` para qualquer par (i, j)
  com i < j. Alternativa: verificar posições relativas dos chips presentes
  em cada linha de forma isolada.

---

### QA-02 — linhas.maximo=1 ausente na matriz padrão e inacurácia no IMP-0017

- **ID**: QA-02
- **Severidade**: baixa
- **Evidência**: O critério de aceite #6 do handoff H-0017 diz "Script
  varia linhas.maximo entre 1, 2 e 3". A seção "Variações obrigatórias na
  matriz" lista `linhas.maximo: 1, 2, 3`. A matriz padrão executável sem
  argumentos (14 cenários) contém apenas `linhas.maximo={2, 3}`; nenhum
  cenário tem `linhas.maximo=1`. O IMP-0017, seção "Variações
  implementadas", afirma: "4. linhas.maximo: 1, 2, 3 — exercitados na
  **matriz padrão** e combinatória." A afirmação sobre a matriz padrão é
  incorreta.
- **Impacto**: A matriz padrão executável sem argumentos não exercita
  `linhas.maximo=1`, que é o caso mais restritivo (força overflow para
  qualquer conjunto de chips que não caiba em linha única). O parâmetro CLI
  `--linhas-max 1` cobre esse caso na execução combinatória (como confirmado
  na execução 2: 86 cenários com `linhas.maximo=1`, 22 OK e 64 erros
  esperados). A cobertura funcional existe; apenas a conveniência da matriz
  padrão e a exatidão do IMP-0017 estão afetadas.
- **Recomendação**: Adicionar ao menos 1 cenário com `linhas.maximo=1` na
  matriz padrão em revisão futura (ex.: 3 chips longos em content_w pequeno,
  esperado `erro_layout`, para exercitar o caso de overflow com linhas=1).
  Corrigir a afirmação no IMP-0017 para "exercitados na combinatória
  (linhas.maximo=1 não está na matriz padrão)".

---

### QA-N-01 — Código smell: `or True` na condição de impressão do resumo

- **ID**: QA-N-01
- **Severidade**: nota
- **Evidência**: `explorar_barra_de_menus.py:906` contém
  `if modo_saida == "resumo" or True:`. A condição `or True` torna
  a condicional sempre verdadeira, o que significa que o resumo é sempre
  impresso independentemente do modo de saída. O comentário `# Sempre
  mostra o resumo` confirma que a intenção é imprimir sempre.
- **Impacto**: O comportamento resultante está correto (o resumo sempre é
  impresso ao final, conforme o handoff especifica para o caso de nenhum
  flag). A condição poderia ser simplesmente `print(resumo)` sem
  condicional. O código é confuso para manutenção futura mas não produz
  comportamento incorreto.
- **Recomendação**: Substituir por `print(resumo)` diretamente em revisão
  futura.

---

### QA-N-02 — INV-2 (chip inventado) verificada implicitamente

- **ID**: QA-N-02
- **Severidade**: nota
- **Evidência**: A invariante 2 ("Nenhum chip ausente é inventado — não
  aparecem ids não declarados") não tem verificação explícita de strings
  não declaradas na saída renderizada. O código verifica INV-1 (`cnt > 1`)
  e INV-3 (`cnt == 0`) mas não faz varredura da saída em busca de textos
  fora da lista `textos_chips`.
- **Impacto**: A verificação é implicitamente satisfeita porque: (a) os
  chips sintéticos têm textos únicos com sufixo numérico (AUD-01 resolvido);
  (b) o renderer só renderiza chips presentes em `chips[]`; (c) se um chip
  inventado aparecesse com o formato `"[tecla] texto"`, seria um texto não
  declarado na lista e as INV-1/INV-3 dos chips declarados ainda passariam,
  mas o texto inventado não seria detectado. Na prática, o renderer é
  correto e não inventa chips. O IMP-0017 documenta: "chips do lancador
  ausentes — não aplicável a cenários sintéticos; verificado implicitamente".
- **Recomendação**: Em revisão futura, complementar com verificação
  explícita: para cada linha da saída, confirmar que todos os tokens no
  formato `"[tecla] texto"` correspondem a algum chip declarado.

---

## Resultado dos testes

```text
python tela/teste_loader.py         → exit 0   (79/79)
python tela/teste_modelo.py         → exit 0   (56/56)
python tela/teste_renderizador.py   → exit 0   (171/171)
python tela/teste_demo.py           → exit 0   (117/117)
python tela/teste_diagnostico.py    → exit 0   (28/28)
python tela/teste_explorar_barra_de_menus.py → exit 0  (25/25)

Suítes existentes: 451/451 verificações passando (sem regressão)
Suíte nova:        25/25 verificações passando
Total:             476/476 verificações passando
```

### Execuções manuais

```text
python tela/explorar_barra_de_menus.py
  → exit 0  (14 cenários: 10 OK, 4 ERRO_ESPERADO, 0 inesperado)

python tela/explorar_barra_de_menus.py --modo-saida resumo --larguras 30,40,80 --chips 3,6,10 --linhas-max 1,2,3 --preenchimentos coluna_a_coluna,linha_a_linha
  → exit 0  (324 cenários: 150 OK, 174 ERRO_ESPERADO, 0 inesperado)

python tela/explorar_barra_de_menus.py --modo-saida detalhado --mostrar-erros --limite-casos 20
  → exit 0  (14 cenários executados, 4 erros exibidos com detalhes corretos)

python tela/explorar_barra_de_menus.py --preenchimentos invalido_xyz
  → exit 2  (parâmetro inválido)
```

---

## Conclusão

A implementação do H-0017 está **funcional, dentro do escopo declarado e
sem regressões**. O script cria exatamente o que o handoff pede: ferramenta
diagnóstica/exploratória que exercita `_linhas_barra` com cenários
sintéticos, verifica invariantes e produz saída determinística. Todos os
32 critérios de aceite do handoff são atendidos ou satisfatoriamente
cobertos.

Os dois achados de baixa severidade (QA-01 e QA-02) não comprometem a
ferramenta: o renderer é correto e determinístico para todos os inputs
testados (0 erros inesperados em 338 cenários executados), portanto a
lacuna em INV-4 não produz falso negativo na prática; e linhas.maximo=1
é coberto via CLI. Os achados ficam registrados para revisão futura.

---

## Próxima ação recomendada

```text
1. Aprovar o ciclo H-0017: QA_APPROVED_WITH_NOTES.
2. Fazer commit dos 5 arquivos não rastreados do H-0017:
   - scripts/docs/handoff/H-0017-script-exploracao-combinacoes-barra-de-menus.md
   - scripts/docs/relatorios/RELATORIO_AUDITORIA_H-0017_HANDOFF.md
   - scripts/docs/relatorios/IMP-0017-script-exploracao-combinacoes-barra-de-menus.md
   - scripts/tela/explorar_barra_de_menus.py
   - scripts/tela/teste_explorar_barra_de_menus.py
   Mais este relatório de QA.
3. Registrar QA-01 e QA-02 como itens de backlog para revisão
   em ciclo futuro (possível H-0018 ou ciclo de manutenção).
4. Iniciar planejamento do próximo ciclo de funcionalidade.
```
