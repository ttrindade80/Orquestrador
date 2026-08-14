# Relatório de Validação Manual — H-0063

```yaml
rastreabilidade:
  etapa: VALIDACAO_MANUAL
  objeto: H-0063
  item: ITEM-0010
  adr: ADR-0046
  handoff: docs/handoff/H-0063-tela-estilo-estrutura-navegacao-dois-niveis.md
  predecessor:
    docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0063.md
  predecessor_status: I5_MANUAL_VALIDATION_REQUIRED

resultado:
  status: VALIDACAO_MANUAL_EXECUTADA
  gates_manuais_h0063:
    aprovados:
      - VM-H0063-001
      - VM-H0063-002
      - VM-H0063-003
    reprovados: []
  gates_aprovados:
    - VM-H0063-001
    - VM-H0063-002
    - VM-H0063-003
  gates_reprovados: []
  classificacao_final_handoff: PENDENTE_DE_ENQUADRAMENTO_DAS_OBSERVACOES

gates:
  - id: VM-H0063-001
    resultado_observado: APROVADO
    fato: F4 físico abriu a funcionalidade; a tela foi observada como tela
      normal completa, não como popup (reprovação anterior de H-0062).

  - id: VM-H0063-002
    resultado_observado: APROVADO
    fato: Navegação física em dois níveis funciona; funcionalidade
      navegacional suficiente para não repetir a reprovação de H-0062.

  - id: VM-H0063-003
    resultado_observado: APROVADO
    fato: Redimensionamento físico funciona; paginação também funciona no
      uso real em TTY.

observacoes_adicionais:
  - id: O-H0063-MANUAL-001
    fato_observado: >
      Ao paginar, a implementação não tenta manter um pai junto com todos os
      seus filhos quando o conjunto pai + filhos caberia integralmente em uma
      única página. O usuário não recorda se existe regra vigente equivalente
      a: se pai + todos os filhos cabem em uma página, não iniciar esse
      conjunto no final de uma página quando ele não couber inteiro no espaço
      restante.
    classificacao: PENDENTE
    nota: >
      Sem enquadramento nesta etapa — não afirmado como defeito, violação de
      H-0063, violação de paginação, necessidade de patch ou melhoria futura.

  - id: O-H0063-MANUAL-002
    fato_observado: >
      A organização/exibição da Barra de Menus não está conforme a expectativa
      visual do usuário. O usuário recorda que pode já existir um ITEM de
      backlog destinado a criar ou uniformizar regra de exibição/organização
      da Barra de Menus; a existência e o escopo desse item não foram
      verificados nesta etapa.
    classificacao: PENDENTE
    nota: >
      Sem enquadramento nesta etapa — não afirmado que H-0063 viola a Barra de
      Menus, que seja defeito implementacional, que seja automaticamente fora
      de escopo, nem que o item de backlog exista de fato.

observacoes_adicionais_pendentes_de_classificacao:
  - O-H0063-MANUAL-001
  - O-H0063-MANUAL-002

proxima_acao_gerencial:
  - verificar regra vigente de paginação para pai + filhos
  - verificar existência/escopo de item de backlog sobre organização da Barra de Menus

bloqueios: []
```

Registro documental da validação manual já executada pelo usuário em TTY real.
Os três gates de `RELATORIO_QA_IMPLEMENTACAO_H-0063.md` (VM-H0063-001,
VM-H0063-002, VM-H0063-003) foram observados como aprovados. A classificação
final do handoff permanece pendente até o enquadramento normativo das
observações adicionais O-H0063-MANUAL-001 e O-H0063-MANUAL-002. Não se usa
nesta etapa `VALIDACAO_MANUAL_APROVADA_FINAL` nem `VALIDACAO_MANUAL_REPROVADA`.
