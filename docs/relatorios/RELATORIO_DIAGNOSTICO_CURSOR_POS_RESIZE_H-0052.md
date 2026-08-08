status: DIAGNOSTICO_CONCLUIDO
handoff: H-0052
achado: cursor_pos_resize
classificacao: DEFEITO_PREEXISTENTE
validacao_manual_1_de_3:
  compatibilidade_h0052: APROVADA
  achado_independente: sim
proxima_acao: CONTINUAR_VALIDACAO_MANUAL

## Reprodução conceitual

Na fixture `config/telas/demo/h0045_validacao_nova_pagina.json`, em uma
geometria pequena o `item_nova_4` ocupa as páginas 5 e 6. A página 6 contém
somente continuação (`primeira_linha_do_item: false`). Ao navegar para ela,
`tela/paginacao.py::ir_para_pagina` não encontra primeiro item lógico e remove
o cursor de `estado["cursores"]`. Ao maximizar, o resize chama
`demo/demo.py::_reconciliar_paginacao_apos_resize`, mas
`reconciliar_pagina_com_cursor` retorna sem ação quando não existe cursor.
Assim, a página antiga é apenas limitada pelo renderer; `_item_corrente_de_contexto`
não materializa cursor algum.

## Delta H-0052 × baseline

O delta em `tela/navegacao.py` acrescenta o fallback/guarda de
`politica_navegacao.tipo` e bloqueia setas para tipos não `nivel_unico`. O
delta em `envelope_pre_adr_0028.py` apenas valida o novo campo. A fixture não
declara `tipo`, portanto resolve para `nivel_unico`, como no comportamento
legado. O caminho de PageUp/PageDown, resize, reconciliação de página e
renderização está em `tela/paginacao.py`, `demo/demo.py` e
`tela/renderizacao/**`, sem alteração no delta. A versão `HEAD` dos dois
proprietários alterados confirma que a lógica nova não existia, mas também que
nenhuma lógica responsável por este defeito foi modificada. O caminho causador
já era o mesmo no baseline; a guarda de tipo não participa dele.

## Proprietário e testes

O proprietário causal é `tela/paginacao.py`, principalmente
`ir_para_pagina` e a guarda inicial de `reconciliar_pagina_com_cursor`; o
resize em `demo/demo.py` é somente o chamador. Há cobertura parcial: P03 testa
resize com item iniciado na página, P11 testa continuação sem cursor, e P12
testa continuação mais resize, mas não afirma a reaparição do cursor após o
retorno a uma página única na fixture observada. Não existe teste focal que
combine os quatro passos do achado.

## Classificação e impacto

Classificação: `DEFEITO_PREEXISTENTE`. H-0052 preservou a compatibilidade
principal e não introduziu o desaparecimento. O achado deve ser registrado
como item separado, sem correção neste diagnóstico. A validação manual 1/3
mantém `compatibilidade_h0052: APROVADA`; o achado independente não reclassifica
essa compatibilidade como falha.
