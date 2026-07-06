---
name: REL-DOC-DOC-0007-CABECALHO
description: Auditoria documental do item DOC-0007 — formalização do cabecalho como domínio próprio
metadata:
  type: relatorio_qa
  status: APROVADO
  data: 2026-07-05
rastreabilidade:
  auditoria: "DOC-0007"
  contratos_alvo:
    - docs/contratos/contrato_cabecalho.md
  adr_relacionadas: []
  bugs_abertos: []
---

# REL-DOC — Auditoria DOC-0007 — contrato_cabecalho

## Revisão executada

Auditoria documental do item DOC-0007: criação de `config/cabecalho.json`,
criação de `docs/contratos/contrato_cabecalho.md`, atualização de
`docs/NOMENCLATURA.md` (seção 0 e nova seção 7), atualização de
`docs/INDICE.md` e atualização de `docs/build_docs/to_do.md`.

## Status final

`APROVADO`

## Arquivos esperados alterados/criados

| Arquivo | Status |
|---|---|
| `config/cabecalho.json` | Criado |
| `docs/contratos/contrato_cabecalho.md` | Criado |
| `docs/NOMENCLATURA.md` | Atualizado (seção 0 e seção 7 nova) |
| `docs/INDICE.md` | Atualizado |
| `docs/build_docs/to_do.md` | Atualizado |
| `docs/relatorios/RELATORIO_QA_DOC-0007_CABECALHO.md` | Criado |

## Achados bloqueantes

Nenhum.

## Evidências verificadas

### E-001 — Formulação "avaliar se compensa" removida de `NOMENCLATURA.md`

Verificação:

- A entrada da tabela de status de migração por domínio (seção 0) para
  Cabeçalho foi alterada de `*(avaliar se compensa)*` para
  `config/cabecalho.json` com status `feito (seção 7)`.
- A menção "e possivelmente `cabecalho`" foi substituída por `cabecalho`
  sem o qualificador de incerteza.
- A nota de rodapé da linha antiga ("cabeçalho é simples... pode não
  justificar arquivo próprio") foi removida.

Resultado: OK.

### E-002 — Seção 7 criada em `NOMENCLATURA.md` com schema completo

Verificação:

- Seção 7 "Cabeçalho" inserida entre seção 6 e seção 8.
- Seção 7.1: dois campos textuais declarados (`titulo` e `descricao`), com
  restrição de `max_caracteres = 200` para `descricao`.
- Seção 7.2: schema de `titulo` com todos os campos decididos:
  `posicao`, `recuo_lateral`, `capitalizacao`, `formato_na_borda`.
  Valores permitidos listados. Semântica de `formato_na_borda` e
  `posicao` documentada.
- Seção 7.3: schema de `descricao` com todos os campos decididos:
  `max_caracteres`, `alinhamento`, `recuo`, `capitalizacao`.
  Valores permitidos listados. Semântica de `alinhamento` documentada.
- Seção 7.4: referência a `config/cabecalho.json` como única fonte de
  valores concretos de apresentação; confirmação de que textos concretos
  de telas não constam no JSON.

Resultado: OK.

### E-003 — `config/cabecalho.json` criado com os valores exatos decididos

Verificação:

- Arquivo criado em `config/cabecalho.json`.
- Campo `titulo.posicao = "esquerda"`.
- Campo `titulo.recuo_lateral = 3`.
- Campo `titulo.capitalizacao = "maiusculas"`.
- Campo `titulo.formato_na_borda = "com_espacos_laterais"`.
- Campo `descricao.max_caracteres = 200`.
- Campo `descricao.alinhamento = "esquerda"`.
- Campo `descricao.recuo = 10`.
- Campo `descricao.capitalizacao = "inicio_de_frase"`.
- Nenhum campo `_meta`, nenhum texto concreto de tela presente.
- JSON válido (estrutura verificada).

Resultado: OK.

### E-004 — `contrato_cabecalho.md` criado com `status: ativo` e cobertura completa

Verificação:

- Frontmatter declara `status: ativo`, `versao: "0.1"`,
  `origem_especificacao: "docs/NOMENCLATURA.md#7-cabecalho"`.
- Seção 2: distinção `cabecalho` vs corpo, `barra_de_menus` declarada com
  tabela comparativa.
- Contrato declara explicitamente que o `cabecalho` não herda regras de
  layout de corpo, `Info`, `menu` nem `barra_de_menus`.
- Seção 3: presença obrigatória declarada; dois campos exatos declarados.
- Seção 4: `config/cabecalho.json` como única fonte de valores concretos.
- Seção 5: schema de `titulo` com semântica completa de `posicao`,
  `recuo_lateral`, `capitalizacao`, `formato_na_borda`.
- Seção 6: schema de `descricao` com semântica completa de `alinhamento`,
  `recuo`, `max_caracteres`, `capitalizacao`.
- Seção 7: 8 regras de uso (R-1 a R-8) cobrindo presença obrigatória,
  dois campos sem extensão, textos na classe, proibição de hardcoding,
  independência de layout, e comportamento dos campos ignorados em modo
  centralizado.
- Seção 8: 14 critérios de validação verificáveis.
- Seção 9: nenhuma pendência em aberto registrada.

Resultado: OK.

### E-005 — Valores concretos não duplicados no contrato

Verificação:

- O contrato não reproduz os valores numéricos de `recuo_lateral`,
  `recuo`, `max_caracteres` nem o preset de `posicao` ou `alinhamento`
  que constam em `config/cabecalho.json`.
- A seção 4 aponta `config/cabecalho.json` como única fonte de valores
  concretos.
- As tabelas do contrato declaram semântica e valores permitidos — não os
  valores de produção selecionados.

Resultado: OK.

### E-006 — `INDICE.md` atualizado consistentemente

Verificação:

- Ordem de leitura (item 5) lista `contrato_cabecalho.md` entre os
  contratos ativos.
- Estrutura esperada de `config/` lista `cabecalho.json`.
- Estrutura esperada de `contratos/` lista `contrato_cabecalho.md`.

Resultado: OK.

### E-007 — DOC-0007 registrado em `to_do.md` como concluído na seção correta

Verificação:

- Entrada `DOC-0007 — Formalizar cabecalho` adicionada na seção
  "Itens prontos para execução", antes da seção de itens bloqueados.
- Campo `Status: concluido`.
- Campo `Concluido_em: 2026-07-05`.
- Todos os arquivos envolvidos listados.

Resultado: OK.

### E-008 — Escopo restrito: nenhum arquivo proibido alterado

Verificação:

- `contrato_estilo.md` — não alterado.
- `contrato_composicao_corpo.md` — não alterado.
- `contrato_barra_de_menus.md` — não alterado.
- ADRs existentes — não alteradas.
- Nenhum arquivo de código alterado.
- Nenhum arquivo fora de `docs/` e `config/` alterado.

Resultado: OK.

### E-009 — Decisões fechadas respeitadas integralmente

Verificação cruzada das 7 decisões fechadas declaradas no escopo:

| Decisão | Verificação |
|---|---|
| 1. `cabecalho` é região fixa superior | Seção 2 do contrato, seção 7 de `NOMENCLATURA.md` |
| 2. `cabecalho` sempre existe | R-1 do contrato, seção 3 |
| 3. Dois campos textuais: `titulo` e `descricao` | R-2, seção 3, seção 7.1 de `NOMENCLATURA.md` |
| 4. Textos pertencem à classe/tela | R-3, seção 3, seção 7.1 de `NOMENCLATURA.md` |
| 5. JSON guarda somente valores de apresentação | R-3, seção 4, cabecalho.json sem textos concretos |
| 6. Não é corpo, Info, menu, barra_de_menus | Seção 2 do contrato, seção 7 de `NOMENCLATURA.md` |
| 7. Não herda regras dessas regiões | R-5 do contrato, seção 2 |

Resultado: OK.

## Verificações sem achados

- `contrato_cabecalho.md` declara `status: ativo` no frontmatter.
- Os valores permitidos listados no contrato (seções 5 e 6) são consistentes
  com os declarados no escopo do DOC-0007.
- A semântica de `formato_na_borda = com_espacos_laterais` está consistente
  entre `NOMENCLATURA.md` seção 7.2, contrato seção 5 e escopo do DOC-0007.
- A semântica de `posicao` e `alinhamento` (esquerda/centro/direita) está
  consistente entre `NOMENCLATURA.md` seção 7, contrato seções 5-6 e escopo.
- Nenhuma ADR foi necessária: o DOC-0007 não altera nenhum contrato já `ativo`.
- A seção 0 de `NOMENCLATURA.md` não contém mais linguagem de incerteza
  sobre o `cabecalho`.

## Verificação de escopo

| Item | Resultado |
|---|---|
| Relatório QA formal criado | OK |
| `config/cabecalho.json` criado sem `_meta` e sem textos concretos | OK |
| `contrato_cabecalho.md` criado e `status: ativo` | OK |
| `NOMENCLATURA.md` seção 0 atualizada (formulação "avaliar" removida) | OK |
| `NOMENCLATURA.md` seção 7 criada com schema completo | OK |
| `INDICE.md` atualizado | OK |
| `to_do.md` atualizado com DOC-0007 concluído, fora de bloqueados | OK |
| Contratos existentes preservados sem alteração | OK |
| ADRs preservadas sem alteração | OK |
| Nenhum código alterado | OK |
| Nenhum arquivo fora de `docs/` e `config/` alterado | OK |

## Conclusão

A auditoria DOC-0007 foi registrada com status `APROVADO`. Zero achados
bloqueantes. Zero achados remanescentes. Nenhuma pendência em aberto.
