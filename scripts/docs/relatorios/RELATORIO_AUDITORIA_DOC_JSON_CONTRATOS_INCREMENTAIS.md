# Relatório de Auditoria — DOC JSON Contratos Incrementais

## Status final

QA_REJECTED

## Escopo auditado

Pacote documental de contratos incrementais para JSON mínimo de tela:

- `docs/contratos/contrato_json_tela_minima.md`
- `docs/contratos/contrato_json_cabecalho.md`
- `docs/contratos/contrato_json_barra_de_menus.md`
- `docs/contratos/contrato_json_lancador.md`
- `docs/contratos/contrato_json_dashboard.md`
- `docs/contratos/contrato_json_console.md`
- `docs/INDICE.md`
- `docs/relatorios/RELATORIO_IMPL_DOC_JSON_CONTRATOS_INCREMENTAIS.md`

Arquivos não relacionados encontrados no estado Git (`docs/handoff/H-0010-lancador-visual-inerte.md` e `docs/relatorios/RELATORIO_AUDITORIA_H-0010_HANDOFF.md`) não foram auditados como parte deste pacote.

## Arquivos lidos

- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/NOMENCLATURA.md`
- `docs/INDICE.md`
- `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`
- `docs/adr/ADR-0009-caminho-formato-jsons-tela.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_cabecalho.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_chip.md`
- `docs/contratos/contrato_lancador.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_console.md`
- todos os seis contratos incrementais novos do pacote
- `docs/relatorios/RELATORIO_IMPL_DOC_JSON_CONTRATOS_INCREMENTAIS.md`

## Comandos executados

```bash
git status --short
git diff --stat
git diff --name-only
git diff -- docs/INDICE.md
```

## Escopo Git

`git status --short` mostrou alteração somente em `docs/INDICE.md` entre arquivos rastreados, além dos contratos e relatórios não rastreados. Não há alteração detectada em `tela/`, `config/`, ADRs, `docs/NOMENCLATURA.md`, JSONs de produção ou código.

`git diff --stat` e `git diff --name-only` mostram apenas `docs/INDICE.md` como arquivo rastreado alterado. A alteração do índice registra os novos contratos na ordem de leitura e não altera regra superior.

## Aderência ao processo

O pacote criou contratos novos em `docs/contratos/` e relatório de implementação em `docs/relatorios/`. Não houve alteração de ADR nem de `NOMENCLATURA.md`.

Foi identificado um achado bloqueante: `contrato_json_tela_minima.md` torna `corpo.arranjo` obrigatório e remove, para o JSON mínimo, a alternativa ativa prevista em contrato superior de omitir `arranjo` e usar `tiling` do estilo como default. Isso altera regra superior sem ADR.

## Aderência à ADR-0008

Parcialmente aderente.

O pacote preserva o modelo de JSON por tela, mantém instâncias concretas no JSON da tela, não cria `config/dashboard.json` e não autoriza hardcoding de itens, destinos, chips, bindings ou ações.

A rejeição decorre da mudança indevida na hierarquia de decisão de arranjo: contratos superiores ainda permitem que `arranjo` não seja declarado no JSON da tela e que `config/estilo.json` forneça default de `tiling` quando a tela não fixa arranjo.

## Aderência à ADR-0009

Aderente.

`contrato_json_tela_minima.md` preserva o caminho canônico `config/telas/<id>.json`, exige coincidência entre `id` interno e nome base do arquivo, e não cria exigência de índice central de telas.

## Aderência ao contrato_tela_json

Parcialmente aderente.

O envelope mínimo preserva `schema`, `id`, `cabecalho`, `corpo` e `barra_de_menus`; `corpo.elementos[]` permanece lista; os tipos válidos permanecem `console`, `dashboard` e `lancador`; o JSON segue declarativo e não inclui estado de runtime.

Contudo, `contrato_tela_json.md` define para `corpo` "tiling ou arranjo equivalente", enquanto o contrato incremental exige especificamente `corpo.arranjo`. A formulação fecha uma escolha que o contrato superior ainda deixa como alternativa.

## Aderência por contrato novo

`contrato_json_tela_minima.md`: rejeitado por achado bloqueante. O contrato exige `corpo.arranjo` como campo obrigatório e descreve valores mínimos por número de elementos, contrariando a opção ativa de `arranjo` ausente com default por `tiling`.

`contrato_json_cabecalho.md`: aprovado com nota. Exige `titulo` e `descricao`, não cria terceiro campo textual e mantém textos concretos no JSON da tela. As referências a `config/cabecalho.json` refletem artefato transicional existente.

`contrato_json_barra_de_menus.md`: aprovado com nota. Mantém `barra_de_menus` como região fixa inferior, fora do corpo, com chips declarativos e separados dos chips do `lancador`. Há ambiguidade não bloqueante no exemplo de `acao` como string.

`contrato_json_lancador.md`: aprovado. Mantém `lancador` como elemento do corpo, itens em `itens[]`, `texto` máximo 15 caracteres, `tela_destino` obrigatório e ausência de navegação por `[✥]`.

`contrato_json_dashboard.md`: aprovado. Mantém `dashboard` passivo, opcional, sem conteúdo universal fixo, sem `config/dashboard.json`, e remete conteúdo real futuro a contrato próprio.

`contrato_json_console.md`: aprovado. Mantém `console` como container genérico, com itens heterogêneos, sem fechar tipos internos universais, e preserva ação de Enter no item ou binding do item.

## Achados bloqueantes

1. `contrato_json_tela_minima.md` torna `corpo.arranjo` obrigatório, contradizendo a regra ativa que permite `arranjo` não declarado e uso de `tiling` do estilo como default.

Evidência:

- `contrato_json_tela_minima.md` seção 5 lista `corpo.arranjo` como campo obrigatório.
- `contrato_composicao_corpo.md` seção 4.2 admite `arranjo` como `sobreposto | lado_a_lado | (não declarado)`.
- `contrato_composicao_corpo.md` seção 5.6 define que, quando `tela.json` não declara `arranjo`, o renderer consulta `tiling` do estilo ativo.
- `NOMENCLATURA.md` seção 1.4 também preserva `tiling` como default quando a classe não especifica arranjo fixo.

Classificação: bloqueante, por contradição com contrato ativo e alteração de regra superior sem ADR.

## Achados não bloqueantes

1. `contrato_json_barra_de_menus.md` usa no exemplo `"acao": "sair"` e permite `acao` como "objeto ou string declarativa". Isso não autoriza comando arbitrário, mas fica menos preciso que os exemplos e campos dos contratos superiores, que favorecem objeto declarativo registrado/whitelisted.

Classificação: não bloqueante, por ambiguidade de redação e exemplo JSON melhorável.

## Observações

- O pacote não altera `config/`, ADRs, `NOMENCLATURA.md`, código nem JSONs de produção.
- `docs/INDICE.md` foi alterado apenas para registrar os novos contratos na ordem de leitura.
- O relatório de implementação afirma que `contrato_composicao_corpo.md` exige declaração de arranjo, mas a leitura do contrato mostra que `arranjo` pode ser não declarado, com default vindo de `tiling`.

## Conclusão

O pacote está majoritariamente alinhado ao modelo declarativo por tela, mas não pode ser aprovado enquanto `contrato_json_tela_minima.md` alterar a regra superior de arranjo/default. O status final é `QA_REJECTED`, com 1 achado bloqueante e 1 achado não bloqueante.
