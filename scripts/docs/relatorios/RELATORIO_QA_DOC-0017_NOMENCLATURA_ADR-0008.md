---
name: relatorio-qa-doc-0017-nomenclatura-adr-0008
description: QA documental da aplicacao da ADR-0008 em docs/NOMENCLATURA.md
metadata:
  type: relatorio_qa
  status: aprovado
  doc: DOC-0017
  adr: ADR-0008
  data: 2026-07-07
---

# Relatorio QA — DOC-0017 — NOMENCLATURA.md × ADR-0008

## Status final

**APROVADO**

## Escopo verificado

Foram verificados:

- `docs/build_docs/instruction.md`;
- `docs/build_docs/to_do.md`;
- `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`;
- `docs/contratos/contrato_tela_json.md`;
- `docs/NOMENCLATURA.md`;
- diff de `docs/NOMENCLATURA.md` e `docs/build_docs/to_do.md`.

Este QA avaliou somente a aplicacao documental da ADR-0008 em
`docs/NOMENCLATURA.md`, referente ao DOC-0017. Nenhum contrato, JSON ou codigo
foi alterado nesta tarefa de QA.

## Comandos executados

```bash
git status --short
git diff --check -- docs/NOMENCLATURA.md docs/build_docs/to_do.md
git diff -- docs/NOMENCLATURA.md docs/build_docs/to_do.md
```

Resultado:

- `git diff --check` nao reportou erros.
- O diff solicitado mostra alteracoes em `docs/NOMENCLATURA.md` e
  `docs/build_docs/to_do.md`.
- O `git status --short` mostrou tambem outros artefatos documentais ja
  presentes no workspace (`docs/INDICE.md`, `docs/adr/INDICE_ADR.md`,
  `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`,
  `docs/contratos/contrato_tela_json.md` e relatorios de QA anteriores).
  Esses arquivos nao foram alterados por esta tarefa de QA nem fazem parte do
  diff de aplicacao do DOC-0017 verificado aqui.

## Evidencias objetivas

1. A politica antiga de JSON por dominio/componente foi substituida pelo
   modelo da ADR-0008: `NOMENCLATURA.md` declara que o modelo passou para JSON
   por tela, preservando `config/estilo.json` como biblioteca global de
   aparencia e `tela.json` como declaracao concreta de tela
   (`docs/NOMENCLATURA.md`, linhas 27-72).

2. `tela.json` esta descrito como declarativo, nao procedural: a secao 2.2
   afirma que ele nao executa comandos arbitrarios, scripts livres, loops ou
   logica executavel nao registrada (`docs/NOMENCLATURA.md`, linhas 230-262).

3. Estado de runtime foi explicitamente excluido do JSON da tela: cursor,
   pagina, filtro ativo, modo verboso, selecao e item focado pertencem a
   execucao, enquanto o JSON pode declarar apenas defaults iniciais
   (`docs/NOMENCLATURA.md`, linhas 43-46 e 247-250).

4. `dashboard` esta definido como tipo minimo: nao navegavel por `[✥]`, nao
   obrigatorio, com moldura propria, posicionavel pela configuracao da tela,
   sem conteudo universal fixo e sem `config/dashboard.json`
   (`docs/NOMENCLATURA.md`, linhas 802-814).

5. A estrutura antiga do `Info` foi reclassificada como draft da instancia de
   `dashboard` da tela raiz do Orquestrador, nao como classe universal
   (`docs/NOMENCLATURA.md`, linhas 818-820).

6. `lancador` foi ajustado para instancia declarada por tela, com mudanca
   declarativa via JSON da tela; a regra de `[✥]` permanece restrita a
   `console`, e `lancador` nao e navegavel por `[✥]`
   (`docs/NOMENCLATURA.md`, linhas 378-381 e 982-1000).

7. `barra_de_menus` foi descrita como instancia declarada por tela e lista de
   chips, permanecendo espelho da declaracao e nao fonte de decisao de
   composicao (`docs/NOMENCLATURA.md`, linhas 468-478).

8. `console` foi descrito como container generico de itens heterogeneos, com
   detalhamento interno remetido a pendencia propria, sem fechar demais a
   taxonomia de tipos internos (`docs/NOMENCLATURA.md`, linhas 297-314).

9. `to_do.md` marca DOC-0017 como `concluido`, com `Concluido_em: 2026-07-07`,
   arquivo envolvido restrito a `docs/NOMENCLATURA.md` e descricao coerente
   com a aplicacao da ADR-0008 (`docs/build_docs/to_do.md`, linhas 228-235).

10. No diff verificado para DOC-0017 nao ha alteracao de contratos, JSON ou
    codigo. As alteracoes verificadas se limitam a `docs/NOMENCLATURA.md` e
    `docs/build_docs/to_do.md`.

## Problemas encontrados

Nenhum problema bloqueante encontrado.

## Recomendacoes de ajuste

- Manter como acompanhamento dos proximos DOCs a migracao/reavaliacao dos
  artefatos marcados como `ativo transicional` na secao 0, especialmente
  `config/lancador.json`, `config/layout_console.json`,
  `config/barra_de_menus.json` e `config/cabecalho.json`.
- Ao executar DOC-0018 e tarefas correlatas, revisar trechos historicos que
  ainda dizem que arquivos por componente guardam valores concretos, para que
  a documentacao ativa nao pareca reabrir o modelo anterior.

## Confirmacao final

Este QA criou apenas este relatorio. Nao houve alteracao de contrato, JSON ou
codigo nesta tarefa.
