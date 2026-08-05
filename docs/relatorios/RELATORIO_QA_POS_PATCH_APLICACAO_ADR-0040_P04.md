---
name: relatorio-qa-pos-patch-aplicacao-adr-0040-p04
description: QA independente da aplicação documental P04 da ADR-0040
metadata:
  type: relatorio
  escopo: qa_pos_patch_aplicacao_adr
---

# QA pós-patch da aplicação documental — ADR-0040 P04

## Cadeia e achados retestados

```yaml
cadeia:
  raiz: docs/relatorios/RELATORIO_APLICACAO_ADR-0040.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0040_P04.md
achados_retestados:
  - QA-APL-0040-P03-01
  - QA-APL-0040-P03-02
```

## Resultado dos achados

- `QA-APL-0040-P03-01`: **resolvido**. O contrato da tela materializa
  explicitamente a inicialização por `controle_execucao.modo_inicial`, a
  preservação durante suspensão e retorno à mesma instância, a
  reinicialização em nova abertura ou recarga — inclusive quando o valor
  coincide — e o descarte sem persistência no encerramento. Os contratos da
  barra e do chip atribuem o ciclo de vida à tela/runtime; o módulo 32 mantém
  o modo apenas como dado transportado na requisição, sem apropriação pelo
  console. Os módulos 02 e 31 reiteram a separação configuração/runtime e a
  representação do modo corrente.

- `QA-APL-0040-P03-02`: **pendente**. O P04 apresenta os campos obrigatórios
  de `delta_terminologico` e um bloco consolidado com proveniência P03/P04.
  Contudo, o bloco principal lista `02`, `31` e `32` em
  `modulos_alterados`, enquanto `arquivos_alterados` do P04 lista somente
  `02` e `31` entre as nomenclaturas e o próprio relatório declara que o
  módulo 32 não foi alterado nesta execução. A frase “delta acima” identifica
  implicitamente o primeiro bloco como P03, mas não corrige a divergência de
  escopo nem fornece correspondência unívoca entre delta, arquivos e diff.
  O módulo 32 comprova o delta precedente e os módulos 02/31 comprovam o
  delta adicional; a inconsistência permanece no relatório P04.

## Verificações focais e preservações

Foram lidos integralmente os nove artefatos do manifesto. O diff focal contém
as cinco alterações documentais declaradas para o P04; o módulo 32 aparece no
estado acumulado por alteração precedente e não no conjunto declarado pelo
P04. `git diff --check` não reportou erro.

Foram confirmados: enumeração fechada `executar`/`dry_run`; ausência de default;
modo vivo em runtime sem escrita no `tela.json`; distinção de `dry_run_ativo`
como especialização focal da ADR-0037; preservação da autoridade de origem;
ausência de novo campo ou migração da especialização focal; e ausência de
alteração nos documentos fora do diff focal. Não há evidência de alteração
em código, configuração concreta, testes, handoff, índice, backlog ou
histórico no escopo auditado.

## Novos achados materiais

Nenhum além da inconsistência de proveniência e escopo que mantém
`QA-APL-0040-P03-02` pendente.

## Status

```yaml
status: ADR_APPLICATION_REJECTED
proxima_acao: PATCH_APLICACAO_ADR
```
