# Relatório de QA da aplicação documental — ADR-0049

## Verificações focais

- A ADR-0049 está registrada como `aceita`; a aplicação documental é indicada como realizada e o QA da aplicação permanece pendente.
- O `ITEM-0027` permanece `em_andamento`. A próxima ação submete a base documental a `QA_APLICACAO_ADR` e condiciona os handoffs à aprovação; não há antecipação semântica dessa aprovação.
- O relatório de aplicação corresponde aos artefatos documentais declarados: contrato, ADR, índice, backlog e módulo `21`; registra que não houve alteração de código, testes ou handoff e que o QA ainda não ocorreu.
- O módulo `21` recebeu somente os termos de composição textual, wrap, justificação de parágrafo e largura visual, com distinções coerentes com a ADR. Não redefine `renderizador` do módulo `01` nem a composição declarativa de `20`.
- O diff focal e o estado Git não mostram código, testes ou handoffs alterados. `git diff --check` terminou limpo.

## Achados materiais

### QA-APP-0049-01 — Algoritmo de distribuição canonizado sem autoridade

O contrato fixa, em sua seção de justificação, distribuição “tão uniforme quanto possível”, resto determinístico começando pelo primeiro vão, ausência de expansão na última linha e comportamento específico quando não há vãos. A ADR exige justificação quando solicitada, mas não escolhe algoritmo matemático nem essas regras de borda. O detalhe foi elevado a requisito comportamental novo.

### QA-APP-0049-02 — Política de espaços e separadores canonizada sem autoridade

A regra de wrap do contrato determina que espaços e separadores não sejam condensados, removidos, reordenados ou acrescentados. A ADR determina convergência das peculiaridades históricas apenas quando semanticamente necessárias, mas não fecha uma política histórica específica de tratamento de espaços. Essa regra não pode ser canonizada somente na aplicação.

### QA-APP-0049-03 — Política nova de entradas inválidas e falhas

As seções de entrada e erros determinam rejeição para largura ausente, não inteira ou não positiva, texto incompatível, modo ou alinhamento não reconhecido, ANSI malformado/não suportado e limites técnicos, além de definir linha para texto vazio. A ADR não decide assinatura, validação, comportamento de largura inválida de helpers nem política geral de erro. Trata-se de decisão operacional material além da autoridade concedida.

## Delta terminológico confirmado

O delta do módulo `21` está confirmado: os quatro termos novos e as distinções entre composição textual e composição declarativa, wrap e truncamento, justificação e alinhamento estrutural, e largura visual e comprimento físico são compatíveis com a ADR. Nenhuma correção terminológica é necessária.

## Status final

`ADR_APPLICATION_REJECTED`

A aplicação documental não pode ser aprovada enquanto os achados QA-APP-0049-01 a QA-APP-0049-03 permanecerem no contrato.
