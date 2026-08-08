---
status: BLOCKED_USER_DECISION
adr: ADR-0042
bloqueio: schema_de_declaracao_da_politica_nao_determinado_pela_autoridade
---

# Relatório de aplicação da ADR-0042

## Estado da aplicação

A aplicação parou antes de qualquer propagação documental, no momento de
materializar no `contrato_json_console.md` a declaração explícita de uma das
cinco políticas de navegação. Nenhum arquivo normativo foi alterado antes do
bloqueio; portanto, não há aplicação parcial concluída.

## Evidência do bloqueio

Em `docs/contratos/contrato_json_console.md`, a seção 4 usa a estrutura:

```json
"politica_navegacao": { "navegavel": false }
```

A seção 5 define `politica_navegacao` como objeto e estabelece `navegavel`
como campo mínimo booleano. A seção 2 usa esse booleano para determinar a
focalizabilidade. As validações da seção 7 não acrescentam um discriminador
de política nem uma lista de valores comportamentais.

`docs/contratos/contrato_console.md` exige o campo `politica_navegacao` na
seção 3 e, na seção 22.1, reafirma `politica_navegacao.navegavel` como
mecanismo declarativo. Também não define campo ou valor que distinga
`nivel_unico`, `tabela`, `arvore_colapsavel`, `selecao_multinivel` e
`dois_niveis_por_foco`.

Assim, o schema vigente permite declarar navegabilidade booleana, mas não
permite declarar explicitamente qualquer uma das cinco políticas. A ADR-0042
já decidiu a semântica dessas políticas e que a escolha deve ser explícita;
ela não decidiu o nome de um novo campo nem a mudança do tipo/formato vigente.

## Decisão necessária

Qual forma deve declarar a política dentro de `politica_navegacao`?

1. Extender o objeto vigente com um campo discriminador escolhido pelo
   usuário, por exemplo `{"navegavel": true, "<campo>": "<politica>"}`.
   Afeta os dois contratos; pode preservar a compatibilidade do objeto atual,
   mas exige definir o nome do campo e sua regra de compatibilidade.
2. Tornar `politica_navegacao` o valor textual de uma das cinco políticas,
   por exemplo `"politica_navegacao": "<politica>"`. Afeta os dois contratos
   e é incompatível com a forma de objeto vigente sem regra explícita de
   transição.

## Estado dos arquivos

```yaml
arquivos_alterados_antes_do_bloqueio: []
arquivos_criados:
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0042.md
arquivos_preservados:
  - docs/adr/ADR-0042-navegacao-multinivel-do-console.md
  - docs/contratos/contrato_console.md
  - docs/contratos/contrato_json_console.md
  - docs/contratos/contrato_barra_de_menus.md
  - docs/contratos/contrato_chip.md
  - docs/nomenclatura/32_CONSOLE.md
  - docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
  - docs/adr/INDICE_ADR.md
  - docs/backlog.md
```

Não há alteração parcial a preservar ou revisar.

## Delta terminológico

```yaml
delta_terminologico:
  modulos_alterados: []
  termos_adicionados: []
  termos_alterados: []
  distincoes_adicionadas: []
  fronteiras_alteradas: []
  dependencias_condicionais_adicionadas: []
```
