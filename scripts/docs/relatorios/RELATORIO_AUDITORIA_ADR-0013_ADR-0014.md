# Relatório de Auditoria — ADR-0013 e ADR-0014

## Status

QA_REJECTED

## Contexto

Auditoria documental das ADRs ADR-0013 e ADR-0014 e dos contratos atualizados no projeto `orquestrador_novo`, após a migração de arranjo vertical e `barra_de_menus` declarativa.

A auditoria foi executada sem alteração de código, JSONs, testes ou handoffs. O único arquivo criado por esta tarefa é este relatório.

## Arquivos lidos

- `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md`
- `docs/adr/ADR-0014-barra-horizontal-termos-especificos.md`
- `docs/relatorios/RELATORIO_DOCUMENTAL_ADR-0013_ADR-0014.md`
- `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md`
- `docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md`
- `docs/adr/INDICE_ADR.md`
- `docs/NOMENCLATURA.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `config/telas/orquestrador.json`
- `config/telas/grupo_minimo.json`
- `config/telas/destino_minimo.json`
- `tela/renderizador.py`
- `tela/demo.py`
- `tela/teste_renderizador.py`
- `tela/teste_demo.py`

## Verificações executadas

```text
git status --short
git diff --stat
git diff --name-only
rg --files docs config/telas tela
rg -n "distribuicao|barra_de_menus|arranjo" config/telas/orquestrador.json config/telas/grupo_minimo.json config/telas/destino_minimo.json
rg -n "get_terminal_size|renderizar_tela|_linhas_barra|largura|lines|altura|barra_de_menus|arranjo|distribuicao" tela/renderizador.py tela/demo.py tela/teste_renderizador.py tela/teste_demo.py
```

## Verificação da ADR-0013

ADR-0013 está adequada.

Ela registra que a tela textual deve ocupar largura e altura disponíveis, que a largura já é dinâmica e que a altura deve virar dimensão explícita do render (`ADR-0013`, linhas 66-79). Também define que o corpo ocupa a altura entre `cabecalho` e `barra_de_menus` e que o espaço restante deve ser preenchido por linhas em branco pelo renderer, não pelo JSON (`ADR-0013`, linhas 81-100).

A ADR separa corretamente `corpo.arranjo = "vertical"` de ocupação vertical do terminal (`ADR-0013`, linhas 102-125 e 148-164), deixa a representação final das linhas em branco para handoff futuro (`ADR-0013`, linhas 127-139) e explicita que não implementa código nem altera testes agora (`ADR-0013`, linhas 141-146).

Não foram encontrados bloqueios na ADR-0013.

## Verificação da ADR-0014

ADR-0014 está parcialmente adequada, mas não pronta para commit documental por causa da lacuna de distribuição responsiva.

Pontos conformes:

- preserva a política declarativa por tela da ADR-0012 (`ADR-0014`, linhas 73-77);
- define `barra_de_menus.distribuicao` como termo específico completo (`ADR-0014`, linhas 79-84);
- distingue `barra_de_menus.distribuicao = "horizontal"` de `corpo.arranjo = "horizontal"` (`ADR-0014`, linhas 106-115);
- exige que o renderer respeite a distribuição declarada e não empilhe um chip por linha quando a distribuição for horizontal (`ADR-0014`, linhas 92-104);
- registra que `g` e `d` são chips do `lancador`/corpo, não da `barra_de_menus` (`ADR-0014`, linhas 117-124);
- declara que a implementação da barra horizontal fica para handoff futuro (`ADR-0014`, linhas 126-129).

Lacuna bloqueante: a ADR não registra explicitamente a distribuição horizontal como distribuição responsiva e deixa a regra de quebra de linha para decisão futura (`ADR-0014`, linhas 249-250 e 258-261), sem impedir a interpretação simplificada de "todos os chips em uma linha".

## Verificação da distribuição responsiva da barra_de_menus

Resultado: bloqueante.

ADR-0014 e os contratos atualizados impedem o empilhamento simples de um chip por linha (`ADR-0014`, linhas 92-98; `contrato_barra_de_menus.md`, linhas 504-515; `contrato_tela_json.md`, linhas 510-516; `NOMENCLATURA.md`, linhas 503-512). Isso é positivo, mas insuficiente para os critérios desta auditoria.

Não há registro normativo suficiente de que:

- a primeira tentativa deve distribuir os chips horizontalmente em uma linha;
- a distribuição deve considerar espaçamento mínimo entre chips;
- a distribuição deve considerar espaçamento máximo entre chips;
- se os chips não couberem adequadamente, a barra pode ocupar múltiplas linhas;
- a quebra multilinha não é empilhamento simples de um chip por linha;
- a distribuição multilinha deve seguir preenchimento por colunas/grade conforme especificação legada.

A documentação atual menciona apenas que a regra de quebra quando chips excederem a largura disponível é pendência de handoff futuro (`ADR-0014`, linhas 249-250 e 260-261). Isso não fecha parâmetros quantitativos e também não registra claramente a necessidade de distribuição responsiva.

Classificação deste item: QA_REJECTED.

## Verificação da regra contra filtro parcial

A regra contra filtro parcial está adequada.

ADR-0014 permite filtros parciais apenas para busca, auditoria e localização (`ADR-0014`, linhas 133-137), proíbe uso como critério de alteração normativa automática (`ADR-0014`, linhas 139-164), exige identificação do termo específico completo antes de alterar ADRs, contratos, JSONs, código e testes (`ADR-0014`, linhas 146-152) e lista exemplos adequados (`ADR-0014`, linhas 173-185).

O contrato de processo reforça a mesma regra: filtros parciais só para busca, alterações apenas sobre termos específicos completos, substituição global proibida, ADRs/handoffs devem nomear campo/conceito afetado e auditorias devem bloquear ambiguidade (`contrato_processo_desenvolvimento.md`, linhas 141-167).

Não há autorização para substituições globais por `vertical`, `horizontal`, `barra`, `chip` ou `arranjo`.

## Verificação de contratos e NOMENCLATURA

As alterações em contratos e NOMENCLATURA são, no geral, mínimas e coerentes.

`NOMENCLATURA.md` distingue `corpo.arranjo = "vertical"` de ocupação da altura do terminal (`NOMENCLATURA.md`, linhas 157-166), distingue `barra_de_menus.distribuicao = "horizontal"` de `corpo.arranjo = "horizontal"` (`NOMENCLATURA.md`, linhas 503-512) e registra a regra contra filtro parcial (`NOMENCLATURA.md`, linhas 514-520).

`contrato_tela_json.md` registra a ocupação vertical futura como responsabilidade do renderer e diferencia `ocupacao_vertical_terminal` de `corpo.arranjo` (`contrato_tela_json.md`, linhas 240-248). Também registra que `barra_de_menus.distribuicao = "horizontal"` deve ser respeitada pelo renderer e não é `corpo.arranjo = "horizontal"` (`contrato_tela_json.md`, linhas 510-521).

`contrato_composicao_corpo.md` registra adequadamente a distinção entre arranjo vertical e preenchimento de altura, inclusive responsabilidade do renderer e não do JSON (`contrato_composicao_corpo.md`, linhas 198-222).

`contrato_barra_de_menus.md` registra a distinção entre `barra_de_menus` e `lancador`, a política declarativa por tela e a incompatibilidade de empilhar chips quando a distribuição declarada é horizontal (`contrato_barra_de_menus.md`, linhas 47-67, 111-121 e 504-515).

Ressalva: os contratos da barra também não fecham a distribuição responsiva. Eles impedem empilhamento simples, mas não registram mínimo/máximo de espaçamento, multilinha por grade/colunas, ou regra explícita contra a solução "todos os chips em uma linha".

## Verificação de escopo

`git diff --name-only` retornou somente:

```text
scripts/docs/NOMENCLATURA.md
scripts/docs/adr/INDICE_ADR.md
scripts/docs/contratos/contrato_barra_de_menus.md
scripts/docs/contratos/contrato_composicao_corpo.md
scripts/docs/contratos/contrato_processo_desenvolvimento.md
scripts/docs/contratos/contrato_tela_json.md
```

Não há alterações rastreadas em:

- `scripts/config/`
- `scripts/tela/`
- `scripts/docs/handoff/`

`git status --short` também indicava como não rastreados apenas os novos documentos de ADR/relatório antes desta auditoria:

```text
?? docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md
?? docs/adr/ADR-0014-barra-horizontal-termos-especificos.md
?? docs/relatorios/RELATORIO_DOCUMENTAL_ADR-0013_ADR-0014.md
```

Após esta auditoria, este relatório passa a constar como novo arquivo não rastreado.

## Achados bloqueantes

1. ADR-0014 não registra a distribuição horizontal da `barra_de_menus` como distribuição responsiva. A documentação impede o empilhamento simples de um chip por linha, mas não impede suficientemente a interpretação simplificada de "todos os chips em uma linha", nem registra mínimo/máximo de espaçamento, multilinha por grade/colunas ou preenchimento por colunas conforme especificação legada.

## Achados não bloqueantes

1. ADR-0014 deixa parâmetros quantitativos e regra de quebra de linha para handoff futuro. Isso seria aceitável se a necessidade de distribuição responsiva estivesse registrada de forma normativa, mas hoje a ressalva contribui para o bloqueio acima.
2. Há pequeno erro textual em `ADR-0014`, linha 136: `levanta mentos`. Não altera semântica.

## Pontos positivos

- ADR-0013 está clara, específica e protegida contra confusão com `corpo.arranjo = "vertical"`.
- ADR-0014 separa corretamente `barra_de_menus.distribuicao = "horizontal"` de `corpo.arranjo = "horizontal"`.
- A regra contra alteração por filtro parcial está bem registrada na ADR-0014 e no contrato de processo.
- O escopo documental foi preservado: sem alterações em `config/`, `tela/` ou `docs/handoff/`.
- Os contratos atualizados são coerentes com ADR-0011 e ADR-0012 e não reescrevem ADRs anteriores.

## Conclusão

Não pode seguir para commit documental ainda.

É necessária correção documental em ADR-0014 e/ou nos contratos afetados para registrar explicitamente que `barra_de_menus.distribuicao = "horizontal"` deve ser implementada como distribuição responsiva: tentativa inicial em linha, espaçamento mínimo/máximo, possibilidade de múltiplas linhas quando não couber, sem empilhamento simples, e com regra multilinha por colunas/grade conforme especificação legada. Parâmetros quantitativos exatos podem permanecer para handoff futuro, desde que a interpretação simplificada fique bloqueada.
