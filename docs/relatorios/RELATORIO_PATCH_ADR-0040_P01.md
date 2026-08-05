# Relatório de patch — ADR-0040 P01

## Cadeia documental

- Cadeia raiz: `docs/relatorios/RELATORIO_QA_ADR-0040.md`
- Predecessor imediato: `docs/relatorios/RELATORIO_QA_ADR-0040.md`

## Achados tratados

- `QA-ADR-0040-01`: removida a transferência da decisão de nome de campo para
  a aplicação documental. Mantidas a declaração explícita do estado inicial,
  a ausência de default e a separação entre configuração concreta e runtime;
  incluída a parada por decisão material ausente quando não houver campo
  suficiente já explicitamente definido por autoridade vigente.
- `QA-ADR-0040-02`: removida a lista normativa de alterações da reconciliação
  futura. Registrado que esta ADR não decide escopo, arquivos, estratégia ou
  critérios de aceite, preservando a exigência de especificação e handoff
  próprios.
- `QA-ADR-0040-03`: `Alternativas consideradas` ajustada à tabela e aos
  títulos do `TEMPLATE_ADR.md`, sem reconstituir alternativas históricas como
  autoridade normativa.

## Verificações executadas

- Revisão focal do diff/conteúdo dos dois arquivos autorizados.
- Confirmada a ausência de obrigação para a aplicação escolher, definir ou
  confirmar nome de campo e de lista normativa para a reconciliação futura.
- Confirmada a preservação semântica de D-DRY-01 a D-DRY-08, da especialização
  focal da ADR-0037, da separação configuração/runtime e da ausência de
  implementação.
- Executado `git diff --check` nos dois arquivos autorizados.

## Bloqueios

nenhum.

## Status factual do patch

`ADR_PATCHED_AWAITING_QA` — correção documental concluída e aguardando QA;
este relatório não aprova a correção.
