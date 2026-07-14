---
name: REL-DOC-DOC-0010-ADR-0005-POS-AJUSTE
description: Auditoria pós-ajuste da aplicação da ADR-0005 — correção do ACHADO-001
metadata:
  type: relatorio_qa
  status: APROVADO
  data: 2026-07-06
rastreabilidade:
  auditoria_anterior: docs/relatorios/RELATORIO_QA_DOC-0010_ADR-0005_APLICACAO.md
  auditoria: "DOC-0010 / ADR-0005 pós-ajuste"
  adr_relacionadas:
    - docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md
  contratos_alvo:
    - docs/contratos/contrato_barra_de_menus.md
---

# REL-DOC — QA pós-ajuste DOC-0010 / ADR-0005

## Status anterior

APROVADO_COM_AJUSTES

## Status pós-ajuste

APROVADO

## Revisão executada

Foi verificado se o ACHADO-001 do relatório anterior foi resolvido em
`docs/contratos/contrato_barra_de_menus.md`, sem alterar contratos, JSON, ADRs,
nomenclatura, índice, templates ou código. A revisão focou a aplicação da
ADR-0005 sobre a existência e o estado de `[✥]`, confirmando que o chip ficou
restrito a corpo tipo `dado` navegável e que `lancador` e `Info` não voltaram a
ser tratados como corpos navegáveis por `[✥]`.

Também foram executadas verificações de escopo, ausência de migração indevida
para `console/dashboard` e validade sintática de `config/barra_de_menus.json`.
`docs/build_docs/to_do.md` não foi atualizado porque não há padrão explícito
para registrar QA pós-ajuste concluído.

## Achado anterior e estado atual

| Achado | Severidade original | Estado atual | Evidência | Observação |
|---|---|---|---|---|
| ACHADO-001 | Ajuste obrigatório local | Resolvido | E-001, E-004 | A formulação genérica "ao menos um corpo navegável" não aparece mais; `[✥]` está condicionado a corpo tipo `dado` navegável. |

## Evidências

### E-001 — Formulação genérica removida

Comando:

```sh
grep -RInE 'ao menos um corpo navegável|ao menos um corpo navegavel' docs/contratos/contrato_barra_de_menus.md
```

Resultado: sem saída. A formulação genérica não foi encontrada.

### E-002 — Sem retorno de `dado ou menu` / `dado ou lancador`

Comando:

```sh
grep -RInE 'tipo `dado` ou `lancador`|tipo `dado` ou `menu`|dado ou lancador|dado ou menu|tipo dado ou menu|tipo dado ou lancador' docs/contratos/contrato_barra_de_menus.md
```

Resultado: sem saída. Não há retorno de formulações contraditórias como
`dado ou menu` ou `dado ou lancador` no contexto de `[✥]`.

### E-003 — Menções negativas a `lancador` e `Info`

Comando obrigatório:

```sh
grep -RInE 'lancador.*corpo navegável|lancador.*corpo navegavel|Info.*corpo navegável|Info.*corpo navegavel' docs/contratos/contrato_barra_de_menus.md
```

Resultado: sem saída, porque a menção negativa está quebrada em linhas no
Markdown. A evidência complementar mostra a formulação esperada:

```text
327	- [ ] `[✥]` só existe estruturalmente quando a tela possui ao menos um corpo
328	      tipo `dado` navegável — `lancador` e `Info` não contam como corpo
329	      navegável por `[✥]`; fica ativo quando o corpo em foco é um corpo tipo
```

Classificação: OK. A menção é negativa e preserva a ADR-0005.

### E-004 — `[✥]` restrito a corpo tipo `dado`

Linhas relevantes:

```text
144:| `[✥]` | Navegar | tela possui ao menos um corpo tipo `dado` navegável | Ativo quando o corpo em foco é um corpo tipo `dado` navegável; inativo via `cor_inativo` quando há corpo tipo `dado` navegável na tela, mas o corpo em foco não é navegável por `[✥]` |
155:um corpo tipo `dado` navegável. O chip não aparece/desaparece conforme o foco
157:corpo em foco é um corpo tipo `dado` navegável, `[✥]` fica ativo; quando o
160:via `cor_inativo`. Se a tela não possui nenhum corpo tipo `dado` navegável,
328:      tipo `dado` navegável — `lancador` e `Info` não contam como corpo
```

Classificação: OK. `[✥]` está restrito a corpo tipo `dado` navegável; quando
não há corpo tipo `dado` navegável, `[✥]` não existe.

### E-005 — Sem migração indevida `console/dashboard`

Comando:

```sh
grep -RInE 'console|dashboard' docs/contratos/contrato_barra_de_menus.md
```

Resultado: sem saída. Não há migração indevida para `console` ou `dashboard`.

### E-006 — JSON ainda válido

Comando:

```sh
python -m json.tool config/barra_de_menus.json >/dev/null && echo "barra_de_menus.json OK"
```

Resultado:

```text
barra_de_menus.json OK
```

### E-007 — Escopo preservado

Comando:

```sh
git status --short
```

Resultado antes da criação deste relatório:

```text
 M config/barra_de_menus.json
 M docs/INDICE.md
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/build_docs/to_do.md
 M docs/contratos/contrato_barra_de_menus.md
 M docs/contratos/contrato_composicao_corpo.md
?? docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md
?? docs/relatorios/RELATORIO_QA_DOC-0010_ADR-0005_APLICACAO.md
```

As alterações listadas acima são pré-existentes à criação deste relatório nesta
QA pós-ajuste. A única criação esperada por esta QA é
`docs/relatorios/RELATORIO_QA_DOC-0010_ADR-0005_POS_AJUSTE.md`.

## Achados

Nenhum achado bloqueante. Nenhum ajuste obrigatório.

## Conclusão

A aplicação da ADR-0005 fica aprovada após o ajuste. O ACHADO-001 foi resolvido:
o contrato não mantém a formulação genérica anterior, não reintroduz `dado ou
menu`/`dado ou lancador`, restringe `[✥]` a corpo tipo `dado` navegável e não
aplica migração indevida para `console/dashboard`.
