# Relatório — Patch do handoff H-0054 P04

status: HANDOFF_PATCH_APPLIED

```yaml
rastreabilidade:
  etapa: PATCH_HANDOFF
  objeto: H-0054
  patch: P04
  cadeia_raiz: docs/handoff/H-0054-selecao-multinivel.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_POS_PATCH_HANDOFF_H-0054_P03.md
  origem_documental:
    adr: ADR-0042 P04
    aplicacao: ADR_APPLICATION_APPROVED
  decisao_tratada:
    - D-MULTI-07-P04
```

## Resultado

O handoff passou a transportar a coerência estrutural de selecionabilidade:
descendente selecionável implica nó e todos os ancestrais estruturais
selecionáveis até a raiz, em profundidade arbitrária. Toda raiz e todo pai
intermediário com seleção abaixo possuem estado binário e `tg`.

Foi removido o cenário `pai não selecionável + descendente selecionável` como
requisito funcional. Ele está registrado como configuração inválida e
incoerente, sem suporte funcional, teste, chip ou propagação exigidos. O
handoff define o domínio válido sem exigir novo validador, mecanismo de
rejeição, exceção ou schema.

A fixture correta preserva pelo menos três pais de nível 1. O primeiro ramo
mantém `1.`/`1.1`/`1.2` e suas folhas selecionáveis. O segundo ramo usa `2.`
como pai selecionável com `tg`, contendo filho selecionável e item interno não
selecionável, sem `tg`, sem descendentes selecionáveis e fora da unanimidade.
O caso negativo e os cenários descendente, ascendente e de desseleção foram
atualizados.

## Critérios e preservações

Os testes e critérios de aceite exigem a invariável estrutural, `tg` em raiz,
pais intermediários e folhas selecionáveis, subárvore integralmente não
selecionável, unanimidade ignorando o item não selecionável, propagação
bidirecional e profundidade arbitrária. Permanecem preservados D-MULTI-06-P03,
estado binário, IDs estáveis, foco/cursor independentes, paginação com múltiplos
itens, PageUp/PageDown, `[PgUp][PgDn] Páginas`, `[✥] Navegar`, `[Esc] Limpar`,
`[?] Ajuda` por último, Enter sem nova semântica e H-0053 sem seleção.

Continuam deferidos barra global, posição global de `[✥]`, ordenação futura,
chips separados de PageUp/PageDown, paginação futura de `arvore_colapsavel`,
H-0055, ITEM-0025 e backlog.

O patch seguinte da implementação deve reconciliar ou remover o suporte
transitório ao cenário inválido sem alterar configurações válidas e sem
prescrever arquitetura.

bloqueios: nenhum no patch documental.
