---
name: RELATORIO_AUDITORIA_H-0012_HANDOFF
description: Auditoria/QA do handoff H-0012 antes de implementacao
metadata:
  type: relatorio_auditoria_handoff
  status: ARCHITECTURE_REVIEW_REQUIRED
  handoff_auditado: docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md
  data: 2026-07-08
---

# Relatorio de Auditoria — H-0012

## Status

`ARCHITECTURE_REVIEW_REQUIRED`

O handoff H-0012 esta bem delimitado quanto ao objetivo gerencial
("grupo estrutural minimo em tela isolada") e respeita a decisao de nao
reabrir H-0011 nem recriar H-0011A. Entretanto, ha um achado bloqueante nos
comandos/criterios obrigatorios de verificacao: a exigencia literal sobre a
saida dos testes nao e compativel com os testes existentes.

## Comandos iniciais executados

```bash
git status --short
```

Saida:

```text
?? docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md
```

```bash
git log --oneline -5
```

Saida:

```text
6c91279 docs: cancela H-0011 e remove H-0011A
a940fbc docs: fecha base documental de composicao hierarquica
f41bd2f docs: registra validacao declarativa com stub b
36c55d2 feat: implementa fluxo minimo do lancador com tela destino
ec0a59e docs: fecha contratos incrementais de tela json
```

```bash
test -f docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md && echo HANDOFF_EXISTE
```

Saida:

```text
HANDOFF_EXISTE
```

## Leitura realizada

Foram lidos os documentos, codigos, testes e JSONs solicitados na auditoria,
incluindo o handoff H-0012, indice documental, nomenclatura, indice de ADRs,
ADR-0010, contratos de processo/tela/composicao/JSONs incrementais, H-0010A,
H-0011 cancelado, modulos `tela/`, testes existentes e os JSONs
`orquestrador`, `destino_minimo` e `stub_b`.

## Achados bloqueantes

1. **A verificacao obrigatoria dos testes exige uma forma de saida que os
   testes atuais nao produzem.**

   O handoff determina, na secao de comandos obrigatorios de verificacao:

   ```text
   Todos devem encerrar com codigo de saida 0 e imprimir apenas linhas [PASSOU].
   ```

   Essa condicao e mais forte do que "todos os testes passaram". Os testes
   existentes imprimem cabecalhos de secao, resumos e detalhes alem das linhas
   `[PASSOU]`. Exemplos encontrados:

   - `tela/teste_loader.py`: imprime `== Carregamento... ==`,
     `-- Declaracao inerte... --`, `== Resumo ==`.
   - `tela/teste_modelo.py`: imprime `== Construcao... ==`,
     `-- Declaracao inerte... --`, `== Resumo ==`.
   - `tela/teste_renderizador.py`: imprime multiplas secoes como
     `== Renderer sobre modelo... ==`, `== Casos de erro... ==`,
     `== Inercia... ==`, `== Resumo ==`.
   - `tela/teste_diagnostico.py` e `tela/teste_demo.py` seguem o mesmo
     padrao.

   Portanto, uma implementacao correta pode encerrar todos os testes com
   codigo 0 e ainda falhar seguindo o handoff literalmente, porque a saida
   nao contem "apenas linhas `[PASSOU]`". Para tornar o handoff executavel, a
   regra precisa ser ajustada para exigir codigo de saida 0 e ausencia de
   linhas `[FALHOU]`, ou entao autorizar explicitamente a alteracao dos
   harnesses de teste para remover cabecalhos e resumos.

## Achados nao bloqueantes

1. **Ha tensao documental residual sobre `grupo` em `corpo.elementos[]`.**

   O H-0012 introduz `tipo = "grupo"` como container estrutural em
   `corpo.elementos[]`, enquanto `contrato_json_tela_minima.md` ainda lista
   apenas `console`, `dashboard` e `lancador` como tipos validos. A tensao e
   mitigada pela ADR-0010 e por `contrato_tela_json.md`, que autorizam a
   evolucao para grupos hierarquicos. Alem disso, o proprio H-0012 define
   `grupo` como estrutural, nao funcional. Ainda assim, a limpeza documental
   futura deve remover a dependencia textual da sequencia H-0011A-D e refletir
   a decisao gerencial de seguir com H-0012 sem letras.

2. **O exemplo de `grupo_minimo.json` usa o formato operacional atual de
   dashboard (`campos[]`), enquanto `contrato_json_dashboard.md` descreve um
   envelope minimo com `conteudo` e `regras_exibicao`.**

   Essa diferenca ja existe nos JSONs reais (`orquestrador.json`,
   `destino_minimo.json`, `stub_b.json`) e no renderer atual, que le
   `dashboard._campos_inertes["campos"]` com `fonte = "literal"`. Nao bloqueia
   o H-0012 porque o ciclo depende do comportamento implementado em H-0010A,
   mas merece harmonizacao documental posterior.

3. **A permissao em torno de `tela/diagnostico.py` poderia ser mais
   consistente.**

   A especificacao funcional F-4 diz que, se o output do Orquestrador mudar, o
   executor deve parar com `ARCHITECTURE_REVIEW_REQUIRED`. A lista de arquivos
   proibidos menciona `tela/diagnostico.py` com excecao "se o output mudar".
   Como a regra mais especifica manda parar antes de alterar, a intencao e
   compreensivel, mas o texto pode induzir leitura permissiva.

4. **O working tree nao estava limpo no inicio da auditoria.**

   Havia o handoff H-0012 como arquivo nao rastreado. Isso e coerente com a
   etapa documental em andamento e nao bloqueia a implementacao, mas deve ser
   conhecido pelo executor antes de usar `git diff --name-only` e
   `git status --short` como evidencia final.

## Pontos positivos

- O H-0012 preserva explicitamente H-0011 como `CANCELADO_NAO_IMPLEMENTAR`.
- O handoff respeita a decisao gerencial de nao criar H-0012A/H-0012B.
- O escopo positivo e pequeno: uma tela isolada, um grupo estrutural, um
  elemento funcional interno.
- O Orquestrador e seus JSONs principais estao protegidos por escopo negativo.
- A orientacao de parar se `demo.py` precisar mudar e adequada para evitar
  expansao indevida do ciclo.
- Os criterios CA-08 a CA-24 sao, em geral, verificaveis por testes focados.

## Conclusao

O handoff H-0012 **nao deve ser entregue para implementacao ainda** enquanto a
regra "imprimir apenas linhas `[PASSOU]`" permanecer literal. O ajuste
recomendado e documental e pequeno: alinhar a verificacao obrigatoria ao
comportamento real dos testes existentes, por exemplo exigindo codigo de saida
0 e nenhuma linha `[FALHOU]`.

Depois desse ajuste, o H-0012 fica apto a seguir com ressalvas documentais
nao bloqueantes sobre a nomenclatura H-0011A-D e sobre o envelope incremental
de `dashboard`.
