---
name: REL-DOC-DOC-0011-ADR-0006-APLICACAO
description: Auditoria documental da aplicação da ADR-0006 — taxonomia console, lancador e dashboard
metadata:
  type: relatorio_qa
  status: APROVADO
  data: 2026-07-06
rastreabilidade:
  auditoria: "DOC-0011 / ADR-0006 aplicação"
  adr_relacionadas:
    - docs/adr/ADR-0006-renomeacao-console-dashboard.md
    - docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md
  contratos_alvo:
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_lancador.md
    - docs/contratos/contrato_cabecalho.md
    - docs/contratos/contrato_estilo.md
  configs_alvo:
    - config/barra_de_menus.json
    - config/layout_console.json
    - config/layout_dado.json
---

# REL-DOC — QA DOC-0011 / Aplicação ADR-0006

## Revisão executada

Foi verificada a aplicação documental da ADR-0006 nos arquivos de nomenclatura, índice, contratos e configs declarados como alvo. A revisão conferiu a taxonomia ativa `console`, `lancador` e `dashboard`, as restrições da `barra_de_menus`, a transição `layout_dado` -> `layout_console` e a preservação do escopo sem alterações de código.

## Status final

APROVADO

## Arquivos verificados

- docs/NOMENCLATURA.md
- docs/INDICE.md
- docs/contratos/contrato_composicao_corpo.md
- docs/contratos/contrato_barra_de_menus.md
- docs/contratos/contrato_lancador.md
- docs/contratos/contrato_cabecalho.md
- docs/contratos/contrato_estilo.md
- config/barra_de_menus.json
- config/layout_console.json
- config/layout_dado.json
- docs/build_docs/to_do.md
- docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md
- docs/adr/ADR-0006-renomeacao-console-dashboard.md
- docs/adr/INDICE_ADR.md
- docs/relatorios/RELATORIO_QA_DOC-0010_ADR-0005_APLICACAO.md
- docs/relatorios/RELATORIO_QA_DOC-0010_ADR-0005_POS_AJUSTE.md

## Evidências

### E-001 — JSONs válidos

- `python -m json.tool config/barra_de_menus.json >/dev/null && echo "barra_de_menus.json OK"`: `barra_de_menus.json OK`
- `python -m json.tool config/layout_console.json >/dev/null && echo "layout_console.json OK"`: `layout_console.json OK`
- `python -m json.tool config/layout_dado.json >/dev/null && echo "layout_dado.json OK"`: `layout_dado.json OK`

### E-002 — Taxonomia ativa atualizada

- `docs/NOMENCLATURA.md:176-181`: define `console`, `lancador` e `dashboard`; `console` preserva regras do antigo `dado`, e `dashboard` é antigo `Info`.
- `docs/NOMENCLATURA.md:197-204`: eixos ativos usam `console`, `lancador`, `dashboard`, `posicao_dashboard` e `colunas_ajustavel` restrita a `console`.
- `docs/contratos/contrato_composicao_corpo.md:57-59`: tabela de tipos reconhece `console`, `lancador` e `dashboard`.
- `docs/contratos/contrato_composicao_corpo.md:77-82`: eixos ativos usam `tipo_conteudo = console | lancador`, `dashboard` e `posicao_dashboard`.

### E-003 — `dado` e `Info` preservados somente como histórico/transicional

- `docs/NOMENCLATURA.md:59`: antigo corpo tipo `dado` aponta para `config/layout_dado.json` como obsoleto/transicional.
- `docs/NOMENCLATURA.md:177`: `dado` aparece apenas como nome antigo cujas regras são preservadas por `console`.
- `docs/contratos/contrato_composicao_corpo.md:57`: `dado` aparece como nome antigo de `console`.
- `docs/build_docs/to_do.md:147`: ocorrência de `dado` está em item DOC-0010 concluído, anterior à ADR-0006; classificada como histórico, não regra ativa.
- Não foram encontradas ocorrências ativas de `tipo Info`, `objeto Info` ou `posicao_info` nos alvos verificados.

### E-004 — `[✥]` restrito a `console`

- `docs/NOMENCLATURA.md:283-286`: `[✥]` e setas da `barra_de_menus` controlam somente cursor de corpo tipo `console`.
- `docs/NOMENCLATURA.md:388`: chip `[✥]` existe quando há corpo tipo `console` navegável e fica ativo quando o foco é `console`.
- `docs/contratos/contrato_barra_de_menus.md:144`: `[✥]` depende de ao menos um corpo tipo `console` navegável.
- `config/barra_de_menus.json:87-89`: existência e estado dinâmico referem corpo tipo `console` navegável.

### E-005 — `lancador` e `dashboard` não navegáveis por `[✥]`

- `docs/NOMENCLATURA.md:284-286`: `lancador` não é corpo navegável por `[✥]`; `dashboard` também não é corpo navegável por `[✥]`.
- `docs/NOMENCLATURA.md:699-700`: `dashboard` é saída passiva; usuário lê, não interage, sem cursor navegável por `[✥]`.
- `docs/contratos/contrato_composicao_corpo.md:128-129`: `lancador` não é corpo navegável por `[✥]` nem pelas setas da `barra_de_menus`.
- `docs/contratos/contrato_composicao_corpo.md:352-353`: critério de validação reforça que `lancador` não é tratado como navegável por `[✥]`.

### E-006 — `[V]` e `[-][+]` restritos a `console`

- `docs/NOMENCLATURA.md:204`: `colunas_ajustavel` aplica-se apenas a corpos tipo `console`.
- `docs/NOMENCLATURA.md:385`: `[-][+]` depende de `colunas_ajustavel: com` para tipo `console`.
- `docs/NOMENCLATURA.md:392`: `[V]` existe para `tipo_exibicao: verboso`, apenas em `console`.
- `docs/contratos/contrato_barra_de_menus.md:141` e `146`: `[-][+]` e `[V]` são condicionados a tipo `console`.
- `config/barra_de_menus.json:55-57` e `138-140`: `restricao_tipo_conteudo` está como `console` para `colunas` e `verboso`.

### E-007 — `layout_console` canônico e `layout_dado` obsoleto/transicional

- `docs/NOMENCLATURA.md:350-357`: seção canônica passou para `config/layout_console.json`; `config/layout_dado.json` permanece apenas para rastreabilidade.
- `docs/INDICE.md:51-52`: lista `layout_console.json` e marca `layout_dado.json` como obsoleto/transicional, não canônico.
- `docs/contratos/contrato_composicao_corpo.md:114-117`: regras de layout de `console` são lidas de `config/layout_console.json`; `layout_dado` fica transicional.
- `config/layout_console.json:3-9`: `layout_console`, `arquivo_canonico: true`, substitui `config/layout_dado.json`.
- `config/layout_dado.json:3-8`: `layout_dado`, `status: obsoleto_transicional`, `arquivo_canonico: false`, `substituido_por: config/layout_console.json`.

### E-008 — Estrutura antiga de `Info` não universalizada como `dashboard`

- `docs/NOMENCLATURA.md:702-704`: estrutura de 8 campos + Total + 8 marcadores é exemplo e instância conhecida, não regra universal de `dashboard`.
- `docs/contratos/contrato_composicao_corpo.md:150-160`: estrutura é declarada como caso específico legado do sistema de survey, não regra universal obrigatória.

### E-009 — Escopo preservado

- `git status --short` antes deste relatório mostrou apenas alterações documentais/config esperadas e os ADRs/relatórios prévios de DOC-0010/DOC-0011.
- `find . -path './.git' -prune -o -type f | grep -E '\.(py|sh|js|ts|tsx|jsx|rs|go|java|c|cpp|h|hpp)$' | sort | xargs -r git diff --name-only --` retornou vazio.
- Não houve alteração de arquivos de código ou templates na aplicação auditada.

## Ocorrências remanescentes classificadas

| Arquivo:linha | Trecho | Classificação | Justificativa |
|---|---|---|---|
| docs/NOMENCLATURA.md:59 | Antigo corpo tipo `dado` / `layout_dado.json` obsoleto/transicional | OK — transicional | Mantém rastreabilidade e declara substituição por `console`. |
| docs/NOMENCLATURA.md:177 | antigo tipo `dado` | OK — histórico | Explica herança terminológica de `console`; não define `dado` como tipo ativo. |
| docs/contratos/contrato_composicao_corpo.md:57 | antigo tipo `dado` | OK — histórico | `console` é o tipo ativo; `dado` aparece como nome anterior. |
| docs/build_docs/to_do.md:147 | `[✥]` restrito a corpo tipo `dado` | OK — histórico | Linha pertence ao item DOC-0010 concluído, anterior à ADR-0006; DOC-0012 registra a aplicação correta para `console`. |
| docs/NOMENCLATURA.md:356 | `layout_dado.json` obsoleto/transicional | OK — transicional | Declara explicitamente que não é fonte canônica nova. |
| docs/INDICE.md:52 | `layout_dado.json  # obsoleto/transicional; nao canonico` | OK — transicional | Preserva arquivo legado sem canonicidade. |
| config/layout_dado.json:6-8 | `obsoleto_transicional`, `arquivo_canonico: false`, `substituido_por` | OK — transicional | Config legado está marcado como não canônico. |
| docs/NOMENCLATURA.md:286 | `lancador`/`dashboard` não navegáveis por `[✥]` | OK — regra correta ativa | Reforça a restrição esperada pela ADR-0006. |
| docs/contratos/contrato_barra_de_menus.md:144 | `[✥]` exige corpo tipo `console` navegável | OK — regra correta ativa | Restrição ativa está alinhada à ADR-0006. |

## Achados

Nenhum achado bloqueante. Nenhum ajuste obrigatório.

## Conclusão

A aplicação da ADR-0006 está aprovada. Os arquivos ativos usam a taxonomia `console`, `lancador` e `dashboard`; `[✥]`, `[-][+]` e `[V]` foram restringidos a `console`; `dashboard` permanece saída passiva não navegável; `layout_console.json` é canônico; `layout_dado.json` está preservado apenas como obsoleto/transicional; e não há alteração de código.
