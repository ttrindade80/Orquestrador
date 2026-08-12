# Relatório de Validação Manual H-0060

## Identificação

- Item: ITEM-0028
- ADR: ADR-0045
- Handoff: H-0060
- PATCH_HANDOFF: P01
- Implementação final: R02 — `docs/relatorios/IMP-0060-resize-responsivo-formacoes-popup-marcacao-R02.md`
- QA final: `IMPLEMENTATION_APPROVED` — `docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0060_R02.md`

## Registro da validação

A validação foi realizada pelo usuário em TTY real, com natureza visual e interativa. O agente documental não executou comandos, não observou o terminal e não produziu evidência automatizada substitutiva.

A primeira validação manual foi reprovada: enquanto a formação coluna cabia integralmente, o pop-up era exibido; ao reduzir o terminal abaixo da altura necessária para a coluna completa, o runtime passava diretamente para Terminal pequeno demais, sem apresentar matriz e linha. Esse fato foi registrado como `MV-H0060-001`, mantido aqui somente como histórico resolvido.

Após o diagnóstico da integração de `renderizar_tela` com a altura física do corpo, o PATCH_HANDOFF P01 permitiu a correção focal em `tela/renderizacao/tela.py`. A implementação R02 recebeu `IMPLEMENTATION_APPROVED` em QA independente, e então foi solicitada nova validação manual completa.

## Roteiro final submetido

A aprovação global fornecida pelo usuário cobre os seis grupos do roteiro final:

- `VM-H0060-001`: sequência física de resize coluna → matriz → linha → Terminal pequeno demais, com matriz antes da linha e máximo de colunas comportado.
- `VM-H0060-002`: reversibilidade linha → matriz → coluna ao ampliar o terminal, sem fechar o pop-up.
- `VM-H0060-003`: navegação toroidal nas três formações, sem foco em célula vazia ou salto diagonal indevido.
- `VM-H0060-004`: preservação do cursor e da marcação exclusiva no mesmo item lógico durante o resize.
- `VM-H0060-005`: preservação do cursor e do conjunto de marcações na modalidade múltipla durante o resize.
- `VM-H0060-006`: redução a Terminal pequeno demais e recuperação automática do pop-up, mantendo instância lógica, cursor, marcações e formação adequada.

O retorno final declarado pelo usuário, após a revalidação posterior à correção e ao novo QA, foi: `aprovado`. Esse retorno é registrado como aprovação global do roteiro final, não como seis respostas literais individuais.

## Autoria e resultado formal

- `EXECUTOR_DA_VALIDACAO`: usuário
- `AMBIENTE`: TTY real
- `REGISTRADOR_DO_RELATORIO`: agente documental
- `RESULTADO_DECLARADO_PELO_USUARIO`: aprovado
- `STATUS_FORMAL`: `MANUAL_VALIDATION_APPROVED`

Não há bloqueio manual remanescente.
