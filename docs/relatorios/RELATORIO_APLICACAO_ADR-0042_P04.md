# Relatório de aplicação — ADR-0042 P04

## Arquivos alterados

- `docs/adr/ADR-0042-navegacao-multinivel-do-console.md` — atualização do
  apontamento do relatório de aplicação para P04.
- `docs/contratos/contrato_console.md` — atualização exclusiva da seção
  vigente de `selecao_multinivel` (§22.15).
- `docs/nomenclatura/32_CONSOLE.md` — atualização compacta do termo
  `selecao_multinivel` (§4.10).
- `docs/relatorios/RELATORIO_APLICACAO_ADR-0042_P04.md` — este relatório.

## Delta material

O contrato passa a estabelecer, em profundidade arbitrária, que descendente
selecionável implica o nó e todos os ancestrais estruturais selecionáveis.
Todo pai com conteúdo selecionável possui estado binário, `tg` e participa da
seleção. Item não selecionável permanece sem estado e sem `tg`, fora do
conjunto selecionado e da unanimidade, e implica subárvore integralmente não
selecionável. `pai não selecionável + descendente selecionável` é configuração
inválida/incoerente, sem comportamento funcional de Espaço documentado.

O caso H-0054 foi preservado como pai de nível 1 `2.` selecionável, com `tg`,
um filho selecionável e um item não selecionável sem `tg`; este último não é
marcado por propagação, não possui descendentes selecionáveis e não interfere
na unanimidade.

## Remoção/reconciliação de suporte obsoleto

Não havia, nos trechos vigentes aplicados, comportamento funcional explícito
para pai não selecionável com descendente selecionável. A seção foi
reconciliada para declarar essa configuração inválida e para não definir
Espaço para ela.

## Delta terminológico

```yaml
delta_terminologico:
  modulos_alterados:
    - docs/nomenclatura/32_CONSOLE.md
  termos_adicionados: []
  termos_alterados:
    - selecao_multinivel
  distincoes_adicionadas:
    - descendente selecionável implica ancestrais estruturais selecionáveis
    - item não selecionável implica subárvore integralmente não selecionável
    - pai não selecionável com descendente selecionável é configuração inválida
  fronteiras_alteradas:
    - configuracao_valida_de_selecao_multinivel
  dependencias_condicionais_adicionadas: []
```

## Preservações e verificações

Foram preservados integralmente D-MULTI-06-P03, estado binário, `tg`,
unanimidade dos filhos selecionáveis imediatos, reconciliação ascendente,
propagação descendente por Espaço, ausência de estado parcial, profundidade
arbitrária e o caso negativo correto do H-0054. Não foram alterados árvore,
paginação, PageUp/PageDown, cursor, foco, Enter, execução, confirmação,
persistência, barra, símbolos ou geometria.

A conferência textual confirma: (1) descendente implica ancestrais; (2) pai
com seleção abaixo possui `tg`; (3) pai não selecionável com descendente é
inválido; (4) não há Espaço funcional para o cenário inválido; (5) item não
selecionável não possui descendentes selecionáveis; (6) permanece fora da
seleção; (7) permanece fora da unanimidade; (8) P03 permanece íntegra; (9) a
unanimidade usa filhos selecionáveis imediatos; (10) paginação, árvore e barra
permanecem inalteradas.

## Bloqueios

Nenhum. QA da aplicação permanece fora desta etapa.
