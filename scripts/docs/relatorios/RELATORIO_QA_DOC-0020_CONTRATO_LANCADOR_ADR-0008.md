---
name: RELATORIO_QA_DOC-0020_CONTRATO_LANCADOR_ADR-0008
description: QA documental da aplicacao da ADR-0008 no contrato_lancador.md
metadata:
  type: relatorio_qa
  doc: DOC-0020
  status_final: APROVADO
  data: 2026-07-07
---

# Relatorio QA - DOC-0020 - Contrato `lancador` conforme ADR-0008

## Status final

**APROVADO**

O contrato `docs/contratos/contrato_lancador.md` aplica de forma coerente a
ADR-0008 para o `lancador`, preservando as regras anteriores ainda vigentes e
reposicionando os dados concretos da instancia no `tela.json`.

## Escopo verificado

Arquivos lidos antes da avaliacao:

- `docs/build_docs/instruction.md`
- `docs/build_docs/to_do.md`
- `docs/adr/ADR-0002-menu-sobra-direita.md`
- `docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md`
- `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_lancador.md`

Arquivos avaliados por diff:

- `docs/contratos/contrato_lancador.md`
- `docs/build_docs/to_do.md`

## Comandos executados

```bash
git status --short
git diff --check -- docs/contratos/contrato_lancador.md docs/build_docs/to_do.md
git diff -- docs/contratos/contrato_lancador.md docs/build_docs/to_do.md
```

Resultado objetivo:

- `git status --short` indicou alteracoes e arquivos novos ja presentes no
  worktree fora do escopo estrito desta QA, incluindo `docs/INDICE.md`,
  `docs/NOMENCLATURA.md`, `docs/adr/INDICE_ADR.md`,
  `docs/contratos/contrato_composicao_corpo.md`,
  `docs/contratos/contrato_lancador.md`, `docs/build_docs/to_do.md` e novos
  arquivos de ADR, contrato e relatorios.
- `git diff --check -- docs/contratos/contrato_lancador.md docs/build_docs/to_do.md`
  nao retornou problemas.
- `git diff -- docs/contratos/contrato_lancador.md docs/build_docs/to_do.md`
  mostrou alteracoes apenas nos dois arquivos solicitados para comparacao.

## Evidencias objetivas

1. Versao 0.2 confirmada em `contrato_lancador.md`: `metadata.versao` esta
   como `"0.2"` nas linhas 4-8.

2. ADR-0008 adicionada a rastreabilidade: a lista `adrs_aplicadas` inclui
   `docs/adr/ADR-0008-modelo-configuracao-por-tela.md` nas linhas 11-16.

3. Distincao entre tipo `lancador` e instancia declarada no `tela.json`:
   o objetivo distingue comportamento minimo do tipo e dados concretos da
   instancia nas linhas 24-32; a secao 2 formaliza tipo versus instancia nas
   linhas 44-56.

4. Conteudo concreto vem do `tela.json`: itens, textos, chips, destinos e
   regras visuais da instancia sao atribuídos ao `tela.json` nas linhas
   29-32 e 172-189.

5. `config/lancador.json` nao ficou como fonte universal definitiva:
   o contrato o marca como artefato ativo transicional, a reavaliar/migrar
   conforme ADR-0008, nas linhas 177-185 e 357-360.

6. Limite de texto preservado: `texto` tem maximo de 15 caracteres e excesso
   e rejeitado sem truncamento nem abreviacao nas linhas 146-152 e 289-292.

7. Campos obrigatorios de cada item preservados e ampliados: cada item exige
   `id`, `chip` ou tecla, `texto` e `tela_destino` nas linhas 113-125.

8. `tela_destino` inexistente tratado como erro de validacao: linhas 154-159
   e criterio de validacao na linha 337.

9. `lancador` permanece distinto da `barra_de_menus`: a distincao estrutural
   aparece nas linhas 60-79, e a relacao operacional e separada nas linhas
   265-273.

10. Chips do `lancador` nao foram confundidos com chips da `barra_de_menus`:
    a linha 267 declara explicitamente que nao sao os mesmos chips, e as
    linhas 294-297 vinculam a tecla do chip ao item declarado no `tela.json`.

11. `[✥]` continua inaplicavel ao `lancador`: linhas 269-271 e criterio de
    validacao na linha 351.

12. Acionamento direto pelo chip/tecla do item preservado: linhas 272-273 e
    regra R-2 nas linhas 284-287.

13. Regras antigas de centralizacao/distribuicao uniforme deixaram de ser
    universais obrigatorias: o alinhamento passa a ser regra da instancia nas
    linhas 226-240, e o calculo automatico e limitado a distribuicao visual
    dentro da regra declarada nas linhas 242-250.

14. ADR-0002 preservada sem contradizer ADR-0008: linhas 235-240 tratam a
    regra historica como default possivel/valor de alinhamento, nao como regra
    universal.

15. Renderer nao decide alinhamento sozinho: linhas 232-233, 321-324 e
    criterio de validacao na linha 338.

16. Criterios de validacao cobrem os casos solicitados: instancia sem `id`
    (linha 330), item sem `id` (linha 332), sem chip/tecla (linha 333), sem
    texto (linha 334), sem `tela_destino` (linha 335), `tela_destino`
    inexistente (linha 337), alinhamento desconhecido (linha 338), e
    hardcoding de item/texto/chip/destino pelo renderer (linhas 349-350).

17. `to_do.md` marcou DOC-0020 como concluido e atualizou DOC-0018 de forma
    coerente: DOC-0018 permanece `pronto_para_execucao` apenas para contratos
    remanescentes nas linhas 237-243; DOC-0020 esta `concluido`, com data,
    origem, descricao da aplicacao e proxima acao encerrada nas linhas 253-260.

18. A ADR-0008 exige `lancador` como instancia configuravel por tela nas
    linhas 130-138 da ADR, e o contrato de `tela.json` exige IDs estaveis para
    elementos e itens de `lancador` nas linhas 95-111 de
    `contrato_tela_json.md`; o contrato avaliado esta coerente com ambos.

## Problemas encontrados

Nenhum problema bloqueante ou ajuste obrigatorio encontrado no escopo do
DOC-0020.

## Recomendacoes de ajuste

Sem recomendacoes de ajuste para `contrato_lancador.md` ou `to_do.md` neste
DOC.

## Confirmacao de escopo de alteracao

Esta tarefa de QA alterou somente este relatorio:

- `docs/relatorios/RELATORIO_QA_DOC-0020_CONTRATO_LANCADOR_ADR-0008.md`

Nenhum outro contrato, JSON, ADR, indice ou codigo foi alterado por esta
tarefa. O worktree ja continha alteracoes e arquivos nao rastreados fora do
escopo antes da criacao deste relatorio; eles foram apenas observados pelo QA,
nao modificados.
