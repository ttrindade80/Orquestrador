cadeia:
  raiz: docs/relatorios/IMP-0054-selecao-multinivel.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0054_P04.md

achados_retestados:
  - QA-H0054-P03-001

resultado:
  QA-H0054-P03-001: resolvido
  conclusao: >-
    A implementação distingue selecionabilidade própria de alcance de seleção.
    Um pai não selecionável permanece sem tg e fora do conjunto, mas Espaço
    permanece ativo quando há descendentes selecionáveis; o primeiro acionamento
    seleciona somente esses descendentes e o segundo os remove.

casos_auditados:
  pai_nao_selecionavel: >-
    P=false com A=true e B=true: sem tg, fora do conjunto, chip ativo,
    seleção de A/B e desseleção posterior de A/B, sem alteração de P.
  sem_alcance: >-
    P=false com A=false: sem alcance, chip inativo e Espaço sem alteração.
  profundidade: >-
    P=false, Q=false, R=true: P tem alcance, Espaço alcança R e P/Q não
    recebem tg nem entram no conjunto; não há lógica por nível.

reconciliacao: >-
  D-MULTI-06-P03 permanece pela unanimidade dos filhos selecionáveis imediatos.
  Nós não selecionáveis são excluídos; não há promoção transitiva através de
  intermediário não selecionável, exceção ad hoc ou hack por ancestral.

regressoes:
  H0054: >-
    Testes confirmam múltiplos itens por página, PageUp/PageDown, seleção entre
    páginas, [✥] Navegar, cursor independente, ordem Paginação antes de
    Selecionar, [PgUp][PgDn] Páginas, [Esc] Limpar, [?] Ajuda por último e
    Enter sem semântica nova.
  H0053: >-
    Caminho integrado permanece sem seleção/tg, com foco inicial, cursor,
    [✥] Navegar, setas, Expandir/Recolher e Espaço em ramo; folha sem ação.

testes:
  focais: "88 passed"
  completos: "1091 passed"

demonstracoes:
  h0054_selecao_multinivel: codigo_0
  h0053_arvore_colapsavel: codigo_0

diff_focal:
  P04: >-
    Revisado em tela/navegacao.py, tela/selecao.py e tela/teste_navegacao.py,
    com o relatório P04 como artefato documental; nenhuma alteração foi feita
    em outro arquivo durante este QA. Alterações preexistentes fora do escopo
    foram preservadas.

validacao_manual: pendente_confirmacao_interativa_TTY
status: I5_MANUAL_VALIDATION_REQUIRED
