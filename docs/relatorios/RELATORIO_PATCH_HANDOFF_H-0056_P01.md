# Relatório — patch do handoff H-0056 P01

## Resultado

O bloqueio decisório original foi resolvido pela autoridade da
ADR-0044 P01 / D-POP-25, com aplicação documental aprovada em QA. O H-0056 foi
atualizado para o estado documental `QA_HANDOFF` e permanece não implementado
e não concluído.

## Alterações efetuadas

- incorporado o campo geral opcional `popups`, como mapa `0..N`, fora de
  `cabecalho`, `corpo` e `barra_de_menus`;
- fechado o ID estrutural `popup_basico` como chave do mapa, sem `id` interno;
- fechada a configuração demonstrativa com `tipo`, `titulo`, `alinhamento`, os
  espaçamentos normativos e o chip `[Esc] Voltar`;
- mantida a separação entre declaração estrutural e envelope runtime textual,
  com resolução por `popups["popup_basico"]`;
- acrescentados testes estruturais de leitura, resolução, ID inexistente,
  ausência de `id` redundante, separação do conteúdo e reuso da declaração.

Os caminhos de implementação, testes, stub demonstrativo e o relatório futuro
`docs/relatorios/IMP-0056-popup-basico-exibicao-voltar.md` foram preservados.
O escopo funcional do pop-up básico foi preservado; H-0057, H-0058 e H-0059
permanecem fora.

## Verificações

Foi verificado no diff que o bloqueio foi removido, a declaração está no nível
geral, a chave funciona como identidade, não há `id` redundante, o conteúdo
runtime permanece externo e a abertura resolve `popups["popup_basico"]`.
Também foram preservados os caminhos e o relatório futuro exigido. `git diff
--check` passou. Nenhuma implementação, QA, stage ou commit foi realizado; o
patch alterou somente os dois arquivos autorizados.

## Bloqueios restantes

Nenhum bloqueio normativo material restante para encaminhar o H-0056 a
`QA_HANDOFF`.
