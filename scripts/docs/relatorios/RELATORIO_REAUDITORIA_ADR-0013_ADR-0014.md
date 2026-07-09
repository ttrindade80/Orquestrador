# Relatório de Reauditoria — ADR-0013 e ADR-0014

## Status

QA_APPROVED

## Contexto

A reauditoria documental foi realizada após correção do achado bloqueante
registrado na auditoria anterior de ADR-0013/ADR-0014.

A auditoria anterior havia retornado `QA_REJECTED` porque a ADR-0014 ainda
permitia interpretação simplificada de
`barra_de_menus.distribuicao = "horizontal"` como linha única fixa.

Esta reauditoria verificou que a documentação corrigida agora normatiza a
distribuição da `barra_de_menus` como distribuição horizontal responsiva,
preserva a distinção entre termos específicos e mantém o escopo documental
sem alteração de código, JSONs ou handoffs.

## Arquivos lidos

- `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md`
- `docs/adr/ADR-0014-barra-horizontal-termos-especificos.md`
- `docs/relatorios/RELATORIO_DOCUMENTAL_ADR-0013_ADR-0014.md`
- `docs/relatorios/RELATORIO_AUDITORIA_ADR-0013_ADR-0014.md`
- `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md`
- `docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md`
- `docs/adr/INDICE_ADR.md`
- `docs/NOMENCLATURA.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`

## Verificações executadas

```text
git status --short
git diff --stat
git diff --name-only
rg -n "horizontal_responsiva|distribuicao|linha única|linha unica|multilinha|overflow|filtro parcial|termo específico|termo especifico" docs/adr/ADR-0014-barra-horizontal-termos-especificos.md docs/contratos/contrato_barra_de_menus.md docs/contratos/contrato_tela_json.md docs/NOMENCLATURA.md docs/contratos/contrato_processo_desenvolvimento.md
```

## Reavaliação do bloqueio — distribuição responsiva da barra_de_menus

O bloqueio anterior foi resolvido.

A ADR-0014 agora registra explicitamente que
`barra_de_menus.distribuicao = "horizontal"` não significa linha única fixa.
O valor passa a significar distribuição horizontal responsiva dos chips da
barra.

A ADR-0014 também proíbe reduzir `horizontal_responsiva` a linha única simples
e proíbe empilhamento vertical como fallback genérico. A documentação agora
impede omissão, truncamento e reordenação automática para fazer a barra caber.

## Verificação da ADR-0013

ADR-0013 continua correta.

A ADR preserva a distinção entre ocupação vertical da janela do terminal e
`corpo.arranjo = "vertical"`. Ela registra que a tela textual deve ocupar
largura e altura disponíveis, que o corpo ocupa a altura disponível entre
`cabecalho` e `barra_de_menus`, e que o preenchimento com linhas em branco é
responsabilidade do renderer.

A decisão não altera `corpo.arranjo`, não implementa código neste ciclo e
deixa a representação exata das linhas em branco para handoff futuro.

## Verificação da ADR-0014

ADR-0014 está adequada após a correção.

A ADR agora normatiza `barra_de_menus.distribuicao = "horizontal"` como
distribuição horizontal responsiva, registra a string `"horizontal"` como
alias transitório de
`barra_de_menus.distribuicao.modo = "horizontal_responsiva"` e define o
formato canônico futuro como objeto declarativo.

A ADR preserva a política declarativa por tela da ADR-0012, impede uso de
lista canônica global, impede invenção de chips ausentes, distingue chips do
`lancador` de chips da `barra_de_menus` e mantém a distribuição da barra
independente de `corpo.arranjo = "horizontal"`.

## Verificação da estrutura canônica futura

A estrutura canônica futura foi registrada de forma suficiente.

Foram verificados os elementos normativos esperados:

- `modo = "horizontal_responsiva"`;
- `tentativa_inicial = "linha_unica"`;
- `quebra = "multilinha_quando_nao_couber"`;
- `preenchimento_multilinha = "coluna_a_coluna"` ou `"linha_a_linha"`;
- `ordem.politica = "declaracao"` ou `"grupos_declarados"`;
- `ancoras.primeiro` e `ancoras.ultimo`;
- `linhas.minimo`, `linhas.maximo` e `linhas.preferir_menor_numero`;
- `alinhamento_linhas`;
- `espacamentos`;
- `colunas.largura = "por_maior_item_da_coluna"`;
- `colunas.subcolunas.chip.alinhamento`;
- `colunas.subcolunas.texto.alinhamento`;
- `overflow.quando_nao_couber = "erro_layout"`;
- `overflow.nao_omitir_chips = true`;
- `overflow.nao_truncar_texto = true`;
- `overflow.nao_reordenar = true`.

Os parâmetros quantitativos permanecem como defaults de referência refináveis
em handoff futuro, sem comprometer a norma responsiva.

## Verificação do algoritmo normativo mínimo

O algoritmo normativo mínimo foi registrado.

A ADR-0014 determina leitura de `barra_de_menus.chips[]`, definição da
sequência base por declaração ou grupos declarados, validação de âncoras,
cálculo da largura dos itens, tentativa inicial em linha única, quebra para
multilinha até `linhas.maximo`, uso do preenchimento multilinha declarado,
cálculo de colunas e subcolunas, e erro determinístico de layout quando
nenhum arranjo couber.

Esse algoritmo fecha a lacuna anterior e impede a leitura simplificada
`horizontal = linha única simples`.

## Verificação da regra contra filtro parcial

A regra contra filtro parcial continua preservada.

ADR-0014 e `contrato_processo_desenvolvimento.md` registram que filtros
parciais podem ser usados para busca, auditoria e localização, mas não podem
guiar alteração normativa automática.

Alterações normativas e de implementação devem atingir termos específicos
completos, como `corpo.arranjo = "vertical"`,
`corpo.arranjo = "horizontal"`,
`barra_de_menus.distribuicao = "horizontal"`,
`barra_de_menus.distribuicao.modo = "horizontal_responsiva"`,
`ocupacao_vertical_terminal`, `preenchimento_altura_corpo`,
`chip canônico` e `chip declarado por tela`.

## Verificação de contratos e NOMENCLATURA

Os contratos e a NOMENCLATURA estão coerentes com a correção.

`contrato_barra_de_menus.md` registra a regra normativa completa da
distribuição horizontal responsiva, incluindo alias transitório, objeto
canônico futuro, tentativa de linha única, quebra multilinha, preenchimento
declarado, ordem, âncoras, overflow determinístico e proibições.

`contrato_tela_json.md` reconhece as duas formas de
`barra_de_menus.distribuicao`: string transitória `"horizontal"` e objeto
canônico futuro com `modo = "horizontal_responsiva"`.

`NOMENCLATURA.md` distingue `corpo.arranjo = "horizontal"`,
`barra_de_menus.distribuicao = "horizontal"` e
`barra_de_menus.distribuicao.modo = "horizontal_responsiva"` como termos
específicos independentes.

`contrato_composicao_corpo.md` preserva a distinção entre
`corpo.arranjo = "vertical"` e `ocupacao_vertical_terminal`.

## Verificação de escopo

O escopo documental foi preservado.

`git diff --name-only` indicou apenas alterações em documentos sob `docs/`.
Não foram identificadas alterações em:

- `config/`;
- `tela/`;
- `docs/handoff/`.

Este relatório registra a reauditoria concluída com `QA_APPROVED` e não altera
ADRs, contratos, NOMENCLATURA, código, JSONs ou handoffs.

## Achados bloqueantes

0

## Achados não bloqueantes

0

## Conclusão

Pode seguir para commit documental.
