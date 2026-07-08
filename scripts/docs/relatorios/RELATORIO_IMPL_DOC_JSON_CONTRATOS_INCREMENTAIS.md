---
name: relatorio-impl-doc-json-contratos-incrementais
description: Relatorio documental da criacao dos contratos incrementais de JSON de tela — envelope minimo por regiao e elemento
metadata:
  type: relatorio
  scope: scripts
  data: 2026-07-08
  status: concluido
---

# Relatório — Implementação Documental: JSON Mínimo — Contratos Incrementais

## 1. Objetivo

Registrar as decisões, o processo e o resultado da criação dos contratos
incrementais de JSON mínimo de tela, conforme especificação da tarefa
`DOC_JSON_CONTRATOS_INCREMENTAIS`.

---

## 2. Contexto normativo consultado

Os seguintes documentos foram lidos integralmente antes de qualquer criação:

| Documento | Papel na tarefa |
|---|---|
| `docs/contratos/contrato_processo_desenvolvimento.md` | Regras de processo e governança documental |
| `docs/NOMENCLATURA.md` | Fonte de verdade de nomes e schema |
| `docs/INDICE.md` | Estrutura esperada e ordem de leitura |
| `docs/adr/ADR-0008-modelo-configuracao-por-tela.md` | Decisão: JSON por tela, não por componente |
| `docs/adr/ADR-0009-caminho-formato-jsons-tela.md` | Decisão: caminho `config/telas/<id>.json` |
| `docs/contratos/contrato_tela_json.md` | Macrocontrato do envelope da tela |
| `docs/contratos/contrato_cabecalho.md` | Schema e regras do cabecalho |
| `docs/contratos/contrato_barra_de_menus.md` | Schema e regras da barra_de_menus |
| `docs/contratos/contrato_chip.md` | Schema e regras da classe chip |
| `docs/contratos/contrato_lancador.md` | Schema e regras do lancador |
| `docs/contratos/contrato_composicao_corpo.md` | Schema e regras de composição do corpo |
| `docs/contratos/contrato_console.md` | Schema e regras do console |

---

## 3. Tese documental aplicada

A tese aplicada foi estritamente a fornecida na especificação da tarefa:

1. `contrato_tela_json.md` permanece macrocontrato do envelope da tela — não
   foi alterado.
2. Os novos contratos são incrementais e operacionais, focados em JSON mínimo
   por região/elemento.
3. `cabecalho`, `barra_de_menus` e `lancador` receberam contratos com JSON
   mínimo derivados das regras já existentes em seus contratos semânticos.
4. `dashboard` e `console` foram tratados como envelopes mínimos — sem fechar
   conteúdo universal interno.
5. `dashboard` e `console` incluem seção obrigatória de modelo para contratos
   futuros de conteúdo, com as seções obrigatórias de binding e JSON associado.
6. Não foi criado `config/dashboard.json`.
7. Não foi autorizado hardcoding de composição, itens, chips, destinos,
   bindings ou ações.
8. `tela_destino` permanece campo declarativo formal em todo item de
   `lancador` — mesmo em ciclo inerte.

---

## 4. Decisões aplicadas durante a criação

### D-1: `contrato_json_tela_minima.md` — envelope mínimo da tela

Decidiu-se especificar apenas os cinco campos obrigatórios definidos em
`contrato_tela_json.md` seção 3: `schema`, `id`, `cabecalho`, `corpo`,
`barra_de_menus`. O campo `corpo.arranjo` foi incluído como campo obrigatório
do corpo porque ADR-0009 e `contrato_composicao_corpo.md` exigem declaração
de arranjo — não pode ficar implícito. A lista de tipos válidos em
`corpo.elementos[]` foi derivada da taxonomia fechada de
`contrato_composicao_corpo.md` seção 3.

### D-2: `contrato_json_cabecalho.md` — dois campos, separação clara

Conforme `contrato_cabecalho.md` seção 3, o `cabecalho` tem exatamente
`titulo` e `descricao`. A separação entre textos concretos (JSON de tela) e
parâmetros de apresentação (`config/cabecalho.json`) foi formalizada
explicitamente, evitando que futuras implementações misturem as duas camadas.

### D-3: `contrato_json_barra_de_menus.md` — chips declarativos e distinção de `lancador`

O JSON mínimo usa o chip `sair` como exemplo ilustrativo — não como lista
obrigatória. A distinção entre chips de `barra_de_menus` e chips visuais de
itens de `lancador` foi formalizada com tabela comparativa, seguindo
`contrato_barra_de_menus.md` seção 3 e `contrato_chip.md` seção 3.

### D-4: `contrato_json_lancador.md` — `tela_destino` como campo declarativo válido

Conforme item 10 da tese documental, `tela_destino` é campo declarativo
formal em todo item de `lancador`, mesmo quando o ciclo de renderização é
inerte. A regra V-7 do contrato formaliza isso explicitamente, distinguindo
validade declarativa de acionamento em ciclo inerte.

### D-5: `contrato_json_dashboard.md` — envelope mínimo sem conteúdo universal

O valor `"placeholder"` foi adotado como `conteudo.tipo` de reserva, antes
de qualquer contrato de conteúdo específico ser aplicado. Isso evita que o
envelope fique semanticamente vazio sem indicar que o conteúdo está pendente.
A proibição de `config/dashboard.json` foi declarada com remissão explícita
à ADR-0008 decisão 7.

### D-6: `contrato_json_console.md` — envelope aberto para itens heterogêneos

O JSON mínimo usa `origem_dados: null` e `itens: []` como valores de reserva.
O envelope dos campos de item foi declarado como "envelope aberto" — listando
os campos que um item pode ter (`tipo`, `binding`, `renderizador`,
`navegavel`, etc.) sem os fechar neste contrato. Isso preserva a abertura para
contratos futuros de tipos internos (DOC-B008).

### D-7: `INDICE.md` — atualização mínima de registro

O `INDICE.md` foi atualizado apenas na seção de ordem de leitura, para
registrar os seis novos contratos incrementais sob a categoria de contratos
de módulo ativos. Nenhuma outra parte do índice foi alterada.

---

## 5. Verificação de critérios de aceite

| Critério | Status |
|---|---|
| Nenhum arquivo de código alterado | ✓ Confirmado |
| Nenhum arquivo em `config/` alterado | ✓ Confirmado |
| Nenhuma ADR criada ou alterada | ✓ Confirmado |
| Nenhum contrato novo contradiz `contrato_tela_json.md` | ✓ Verificado por leitura integral |
| Nenhum contrato novo contradiz ADR-0008 | ✓ Verificado — cada contrato aplica as duas ADRs |
| Nenhum contrato novo contradiz ADR-0009 | ✓ Verificado — caminho `config/telas/<id>.json` declarado em `contrato_json_tela_minima.md` |
| Contratos novos são incrementais, não duplicam integralmente contratos existentes | ✓ Cada contrato referencia o contrato semântico de autoridade |
| `dashboard` não fecha conteúdo universal | ✓ `contrato_json_dashboard.md` usa `"placeholder"` e remete a contratos futuros |
| `console` não fecha conteúdo universal | ✓ `contrato_json_console.md` declara envelope aberto e remete a contratos futuros |
| `dashboard` aponta para contratos futuros com seções de binding e JSON | ✓ Seção "Contratos futuros de conteúdo de `dashboard`" com modelo de 7 seções |
| `console` aponta para contratos futuros com seções de binding e JSON | ✓ Seção "Contratos futuros de conteúdo de `console`" com modelo de 8 seções |
| `lancador` declarativo por `itens[]`, `tela_destino` formal | ✓ V-7 formaliza `tela_destino` como campo obrigatório mesmo em ciclo inerte |
| `barra_de_menus` distinta de `lancador` | ✓ Formalizado com tabela em `contrato_json_barra_de_menus.md` seção 7 |
| Relatório final lista arquivos criados/alterados, decisões, status | ✓ Este relatório |

---

## 6. Arquivos criados

```text
docs/contratos/contrato_json_tela_minima.md
docs/contratos/contrato_json_cabecalho.md
docs/contratos/contrato_json_barra_de_menus.md
docs/contratos/contrato_json_lancador.md
docs/contratos/contrato_json_dashboard.md
docs/contratos/contrato_json_console.md
docs/relatorios/RELATORIO_IMPL_DOC_JSON_CONTRATOS_INCREMENTAIS.md
```

---

## 7. Arquivos alterados

```text
docs/INDICE.md  — atualização mínima: registro dos seis novos contratos na
                  seção de ordem de leitura (item 5), sem alterar regras
                  nem estrutura do índice.
```

---

## 8. Pendências derivadas

Os contratos criados apontam para pendências que permanecem fora de escopo
desta tarefa:

| Pendência | Referenciada em |
|---|---|
| Contratos de tipos internos de item de `console` (`contrato_conteudo_console_<tipo>.md`) | `contrato_json_console.md` seção "Contratos futuros" |
| Contratos de tipos de conteúdo de `dashboard` (`contrato_conteudo_dashboard_<tipo>.md`) | `contrato_json_dashboard.md` seção "Contratos futuros" |
| Registry completo de ações (DOC-B009) | `contrato_json_barra_de_menus.md`, `contrato_json_lancador.md` |
| JSON real da tela raiz do Orquestrador (DOC-B011) | `contrato_json_tela_minima.md` seção 9 |
| Posicionamento horizontal do bloco de `dashboard` (DOC-B004) | `contrato_json_dashboard.md` seção 7 |

---

## 9. Comandos executados

Nenhum comando de shell foi executado. Todos os artefatos foram criados por
operações de escrita direta de arquivo (ferramentas Write/Edit do ambiente de
desenvolvimento), sem execução de scripts Python, sem alteração de JSON de
produção e sem uso de `git`.

---

## 10. Status

`IMPLEMENTATION_COMPLETED`

Nenhuma contradição com contratos existentes, ADRs ou NOMENCLATURA.md foi
encontrada. Nenhum `ARCHITECTURE_REVIEW_REQUIRED` foi necessário.
