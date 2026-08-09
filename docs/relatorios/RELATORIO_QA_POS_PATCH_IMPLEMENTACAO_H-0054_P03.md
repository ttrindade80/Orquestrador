cadeia:
  raiz: docs/relatorios/IMP-0054-selecao-multinivel.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0054_P03.md

decisao_retestada:
  - D-MULTI-06-P03

escopo:
  diff_focal: conforme ao conjunto reportado no P03; não foi identificada alteração da fixture H-0053.
  observacao_worktree: havia mudanças pré-existentes fora do escopo focal; esta QA não as alterou.

resultado:
  estado_por_selecionabilidade: conforme. Raízes, pais intermediários e folhas selecionáveis possuem estado binário e tg; itens não selecionáveis permanecem sem estado/tg. A profundidade não é usada como critério.
  coerencia_pai_filhos: conforme para pais selecionáveis com filhos selecionáveis imediatos. A reconciliação em pós-ordem materializa os dois sentidos da unanimidade, sem estado parcial.
  propagacao_descendente: conforme para pai selecionável; Espaço inclui/remover a subárvore selecionável.
  reconciliação_ascendente: conforme. Construção manual marca pai intermediário e raiz; desseleção remove ancestrais afetados e preserva o ramo irmão.
  nao_selecionaveis: conforme no conjunto de seleção, na renderização e no cálculo de unanimidade; não são propagados.

achados:
  - id: QA-H0054-P03-001
    natureza: regressão material
    evidencia: |
      No cenário equivalente a “P selecionavel=false, com A e B selecionáveis”,
      P não recebe tg nem entra na seleção, mas o chip de Espaço ficou inativo
      e o acionamento produziu seleção vazia, em vez de selecionar A e B.
      O segundo acionamento também não remove descendentes. A mesma restrição
      aparece em tela/navegacao.py:no_tem_alcance_selecao(), que exige
      no_multinivel_selecionavel(no), e em tela/selecao.py:_alvos_multinivel(),
      que retorna vazio antes de alcançar descendentes quando o corrente não é
      selecionável. Não havia teste existente para esse cenário; a evidência
      foi obtida por probe em memória, sem editar testes.
    impacto: viola a semântica vigente de Espaço recursivo em pai não selecionável com descendentes selecionáveis.

fixture:
  resultado: conforme.
  evidencia: três pais de nível 1; primeiro ramo com dois pais de nível 2 e folhas; item não selecionável no segundo ramo; terceiro ramo volumoso; profundidade material de três níveis; 33 nós e paginação nominal em três páginas.

regressoes:
  h0054: conforme nos testes focais para múltiplos itens por página, PageUp/PageDown, seleção entre páginas, [✥] Navegar, cursor independente, paginação antes de Selecionar, [PgUp][PgDn] Páginas, [Esc] Limpar, [?] Ajuda por último, ausência de estado parcial e Enter sem semântica nova.
  h0053: conforme pelo caminho integrado: foco inicial, cursor, navegação, setas, Espaço abre/fecha, filhos desaparecem/reaparecem, Expandir/Recolher contextual, folha sem ação, sem seleção e sem tg. Fixtures H-0053 preservadas.

testes:
  focais: 84 passed.
  completos: 1087 passed.
  demos: h0054 código 0; h0053 código 0.

validacao_manual: pendente; a execução automatizada não substitui a sessão TTY do usuário.

status: I2_IMPLEMENTATION_PATCH_REQUIRED
