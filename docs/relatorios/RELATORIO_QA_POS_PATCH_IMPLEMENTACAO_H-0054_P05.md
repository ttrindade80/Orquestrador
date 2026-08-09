# Relatório QA pós-patch de implementação — H-0054 P05

```yaml
cadeia:
  raiz: docs/relatorios/IMP-0054-selecao-multinivel.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0054_P05.md

decisao_retestada:
  - D-MULTI-07-P04
```

## Resultado

O suporte transitório ao cenário inválido “pai não selecionável com descendente selecionável” foi removido/reconciliado: `no_tem_alcance_selecao()` exige o nó corrente selecionável e `_alvos_multinivel()` não cria alcance através de nó não selecionável. Não há teste funcional, segundo toggle, travessia especial ou mecanismo novo de rejeição para esse cenário.

A fixture H-0054 é coerente em profundidade arbitrária: possui três raízes de nível 1, os ramos `1.1`/`1.2` com múltiplas folhas, o terceiro ramo e volume para três páginas. Todo ancestral de seleção é selecionável e possui `tg`. No ramo `2.`, o pai e seus ramos selecionáveis possuem `tg`; o item negativo não possui `tg`, não entra no conjunto, não tem descendentes selecionáveis e é ignorado na unanimidade.

D-MULTI-06-P03 permanece íntegra: conjunto de IDs como fonte única, estado binário, seleção descendente, reconciliação ascendente e desseleção preservando o ramo irmão. Paginação, PageUp/PageDown, `[✥] Navegar`, cursor independente, `[Esc] Limpar`, `[?] Ajuda` por último e Enter foram preservados. H-0053 permanece sem seleção/`tg`, com foco, cursor, navegação, Expandir/Recolher e Espaço preservados.

Verificações: focal `87 passed`; suíte completa `1090 passed`; demos H-0054 e H-0053 com código `0`. O diff focal não indica alteração P05 fora dos arquivos reportados; fixtures H-0053 não foram alteradas.

Validação manual: aprovada antes da mudança estrutural, conforme o contexto recebido; não foi repetida neste QA. Resta somente a confirmação visual/interativa final do ramo `2.`.

Achados: nenhum achado automatizado ou de escopo P05. A redução de testes é conforme a remoção dos quatro casos transitórios obsoletos.

**status: `I5_MANUAL_VALIDATION_REQUIRED`**
