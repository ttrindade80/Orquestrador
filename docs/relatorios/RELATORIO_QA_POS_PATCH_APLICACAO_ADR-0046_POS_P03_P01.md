# RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0046_POS_P03_P01

cadeia:
  raiz: ADR-0046
  predecessor_imediato: RELATORIO_PATCH_APLICACAO_ADR-0046_POS_P03_P01.md

## ACH-APLICACAO-ADR0046-P03-01

**PENDENTE.** A associação final está correta: Curva usa `╭` / `╮` e
Ornamental usa `❲` / `❳`, apresentados como presets distintos. A composição
multitecla mantém uma única unidade com `/`, e `[PgUp][PgDn]` permanece apenas
como identificação documental, não como forma física.

## Achado novo material

- **Divergência entre escopo declarado e diff real:** o diff de
  `docs/contratos/contrato_chip.md` não se restringe aos exemplos normativos da
  seção 10.1. Ele também altera o metadado de rastreabilidade, a seção 7, a
  seção 9, a nota de paginação, e acrescenta regras materiais nas seções
  10.1–10.5 e 12. Isso contraria a afirmação de que somente a passagem de
  exemplos da seção 10.1 foi alterada e de que o restante do contrato ficou
  intacto.

## Verificações focais

- A busca autorizada confirma em 10.1: `Colchete [PgUp/PgDn]`, `Curva
  ╭PgUp/PgDn╮` e `Ornamental ❲PgUp/PgDn❳`.
- A mesma seção explicita unidade visual única, separador `/` e a exclusão de
  `[PgUp][PgDn]` como forma física.
- O diff autorizado confirma alterações materiais fora da propagação
  documental do achado e torna incorreta a representação do diff no relatório
  do patch.

## Status atual

ADR_APPLICATION_REJECTED
