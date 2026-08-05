# Relatório de aplicação remanescente — ADR-0008 / ITEM-0015

## Etapa e objeto

Aplicação documental direta do delta remanescente da ADR-0008 relativo ao
ITEM-0015. O objeto foi a fronteira normativa entre configuração por tela,
biblioteca global de estilo e estado de runtime no cabeçalho.

## Arquivos alterados

- `docs/contratos/contrato_cabecalho.md`
- `docs/contratos/contrato_estilo.md`
- `docs/nomenclatura/30_CABECALHO.md`
- `docs/relatorios/RELATORIO_APLICACAO_REMANESCENTE_ADR-0008_ITEM-0015.md`

## Delta material

O contrato do cabeçalho passou a declarar o JSON estrutural da respectiva tela
como fonte dos textos concretos de `titulo` e `descricao` e dos parâmetros
locais de apresentação. O contrato mantém a região macro fixa, os dois campos,
o schema, a semântica, os invariantes e as validações, e explicita que os
parâmetros locais não pertencem ao estilo global.

O contrato de estilo passou a caracterizar `config/estilo.json` como biblioteca
global de aparência compartilhada e a listar seus limites em relação à tela.
Seu schema vigente e as decisões posteriores de presets, materialização,
carregamento único, cores e `tiling` foram preservados.

A nomenclatura do cabeçalho passou a registrar a ADR-0008 e a proveniência
correspondente, removendo o caminho legado como termo proprietário ou fonte
vigente.

## Verificações executadas

- Busca de ocorrências do caminho obsoleto nos três documentos afetados: nenhuma ocorrência.
- Busca de `ADR-0008` nos três documentos afetados: ocorrência registrada nos três.
- `git diff --check` nos três documentos e neste relatório.
- `git diff` restrito aos três documentos e a este relatório.

## Ocorrências obsoletas eliminadas

Foram eliminadas as referências que atribuíam textos ou parâmetros locais do
cabeçalho a um arquivo global próprio, inclusive sua caracterização como
futuro, exclusivo, obrigatório ou fonte de leitura em runtime.

## Fronteira final

- JSON da tela: textos concretos de `titulo` e `descricao` e parâmetros locais de apresentação do cabeçalho.
- `config/estilo.json`: aparência global compartilhada, incluindo bordas, forma visual de chips, indicadores, cores globais e demais campos universais vigentes; não contém composição, conteúdo, instâncias ou regras locais de tela.
- Runtime: estado vivo produzido e mantido pela execução; não é armazenado como estado vivo nos JSONs.

## `delta_terminologico`

`config/elementos/cabecalho.json` deixou de ser termo proprietário e fonte
vigente. O cabeçalho passa a usar `JSON estrutural da tela` para os valores
concretos locais, preservando `config/estilo.json` como artefato de aparência
global e mantendo a autoridade comportamental em `contrato_cabecalho.md`.

## Bloqueios

Nenhum.
