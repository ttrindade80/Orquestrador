cadeia:
  raiz: docs/relatorios/IMP-0054-selecao-multinivel.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_POS_PATCH_IMPLEMENTACAO_H-0054_P03.md

achados_tratados:
  - QA-H0054-P03-001

causa_confirmada: >-
  no_tem_alcance_selecao() confundia selecionabilidade própria com alcance
  recursivo, e _alvos_multinivel() abortava antes de percorrer descendentes
  quando o nó corrente não era selecionável.

correcao:
  - >-
    no_tem_alcance_selecao() agora considera acionável o nó selecionável ou
    qualquer nó com descendente selecionável.
  - >-
    _alvos_multinivel() continua a travessia para nós não selecionáveis,
    exclui o próprio nó e coleta somente descendentes selecionáveis.
  - >-
    A fonte de verdade, a reconciliação pós-ordem e a unanimidade vigente de
    D-MULTI-06-P03 foram preservadas.

provas:
  - >-
    Pai não selecionável com dois descendentes selecionáveis tem chip ativo;
    Espaço seleciona e depois desseleciona somente os descendentes; o pai não
    recebe tg nem entra no conjunto.
  - >-
    Pai sem alvo permanece inativo e a seleção não muda.
  - >-
    A mesma regra funciona em profundidade arbitrária.
  - >-
    Ancestral selecionável não é promovido através de pai não selecionável;
    filhos selecionáveis seguem a reconciliação vigente.

testes:
  novos: 4 testes unitários explícitos em tela/teste_navegacao.py.
  regressao_d_multi_06_p03: aprovado na suíte focal e completa.
  focais: 88 passed.
  completos: 1091 passed.

demonstracoes:
  h0054_selecao_multinivel: codigo 0.
  h0053_arvore_colapsavel: codigo 0.

arquivos_alterados_nesta_etapa:
  - tela/navegacao.py
  - tela/selecao.py
  - tela/teste_navegacao.py
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0054_P04.md

fixture_p03: preservada.
bloqueios: nenhum.
status: IMPLEMENTATION_PATCH_APPLIED
