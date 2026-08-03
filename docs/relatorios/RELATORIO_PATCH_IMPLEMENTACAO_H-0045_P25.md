tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTATION_PATCHED
cadeia_raiz: VM-H0045-R08-001
predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_HANDOFF_H-0045_P12.md
achados_tratados:
  - QA-H0045-P23-001
  - QA-H0045-P23-002
  - QA-H0045-P23-003
  - IMP-H0045-P24-001

## Correção

A classificação anterior aceitava famílias abertas por `startswith`, incluindo
`DA-0` e qualquer `erro_layout`, e `_resolver_conteudo` convertia qualquer
`RenderizadorErro` em quadro mínimo. A classificação nova aceita somente a
mensagem completa produzida pelo overflow real da barra de menus ou pelas duas
mensagens reais de altura insuficiente do renderer. DA-01, DA-02, DA-04,
DA-099, códigos futuros, mensagens semelhantes e erros estruturais propagam a
exceção original.

O formato aceito da barra exige chips, caracteres úteis, `content_w`, margem,
limite de linhas, preenchimento (`coluna_a_coluna` ou `linha_a_linha`) e as
flags literais de `overflow.quando_nao_couber='erro_layout'` com proibição de
omitir/truncar/reordenar. Altura aceita apenas os formatos reais de
`terminal ... cabecalho ... barra_de_menus` e de `corpo requer ... area
disponivel ...`.

Todas as insuficiências geométricas aceitas usam o quadro controlado unificado:
`Terminal pequeno demais` e `Aumente a janela para continuar`. O quadro é
truncado com segurança em dimensões extremas e não contém interface parcial.
Em 80x8 as duas mensagens foram confirmadas; a recuperação e o estado lógico
do P23 foram preservados.

## Testes e arquivos

Alterados nesta etapa:

- `demo/demo.py`: classificação exata, propagação seletiva e quadro unificado;
- `demo/teste_demo.py`: expectativa estrutural do H-0023 e quadro completo do
  H-0044, preservando os cenários restantes;
- `demo/teste_demo_paginacao.py`: negativos P25, produtores geométricos,
  matriz e propagação pelos três caminhos reais.

Os testes H-0023 e H-0044 mantêm, respectivamente, a recuperação de resize e
a recuperação visual posterior. `tela/teste_renderizador.py` e
`demo/teste_demo_navegacao.py` foram executados sem alteração nesta etapa.

Resultados:

- filtro P25: 43 passed;
- relacionados P23/P24/P25 e H-0023/H-0044: 87 passed;
- quatro arquivos autorizados: 574 passed;
- suíte completa: 970 passed;
- matriz: 60/60 combinações passaram, incluindo escolha mínima de 1–5 linhas,
  estado controlado, preservação e recuperação;
- negativos: distribuição, `linhas.maximo`, preenchimento, estrutura/modelo,
  invariante, DA-02/04/01/099, `erro_layout` sintético, `r` e mensagem similar
  relançados por `_resolver_conteudo`, `_reconciliar_paginacao_apos_resize` e
  `_com_geometria_real_do_console`;
- `git diff --check` nos cinco caminhos autorizados: limpo.

Bloqueios: nenhum de implementação. Validação manual e QA permanecem
pendentes conforme o handoff.

proxima_acao: QA_POS_PATCH
