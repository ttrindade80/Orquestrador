# Relatório — Criação do handoff H-0077

## Capacidade

Migrar o caminho compartilhado de conteúdo externo
(`tela/renderizacao/conteudo_externo.py`) e seus consumidores correlatos para
o núcleo canônico de composição textual entregue e aprovado por H-0076
(`tela/renderizacao/composicao_textual.py`), garantindo coerência entre
renderização, medição, altura e paginação interna. É o segundo e último
handoff do `ITEM-0027`, conforme o dimensionamento gerencial em dois
handoffs já registrado em `ADR-0049` §6.

## Cadeia concreta de consumidores localizada

Investigação focal com `rg` restrita a `tela/` (não houve descoberta
documental ampla) confirmou a seguinte cadeia de dependência da autoridade
local `_quebrar_texto` hoje definida em `conteudo_externo.py`:

- `conteudo_externo.py` define `_quebrar_texto` (delegando a
  `_quebrar_sem_ansi` de `texto_ansi.py` quando há ANSI) e usa-a
  internamente em `_linhas_apresentacao_hierarquia_com_mapa`,
  `_linhas_dois_niveis_formatado_com_mapa`, `_linhas_apresentacao_tabela` e
  `_linhas_apresentacao_conjuntos`. `_truncar_com_marcador` é mecanismo
  distinto, preservado.
- `matriz_participantes.py` importa `_quebrar_texto` e
  `_participantes_de_conteudo_externo` diretamente; usa em
  `_altura_quebra_item` (medição de altura, consumida por
  `_larguras_mapa_fisico_matricial`) e em
  `_renderizar_participante_com_indicador` (renderização efetiva).
- `console.py` importa `_linhas_conteudo_externo` de `conteudo_externo` e
  `_altura_quebra_item`/`_larguras_mapa_fisico_matricial` de
  `matriz_participantes`; `mapa_fisico_de_itens` deriva `linhas_fisicas`
  diretamente do resultado dessas funções.
- `paginacao_interna.py` importa `_quebrar_texto` diretamente para
  `_linhas_texto_item_para_pagina` e consome `mapa_fisico_de_itens` para
  recorte de páginas.
- `tela/renderizador.py` importa `_quebrar_texto`, `_texto_valor_campo` e
  `_truncar_com_marcador` de `conteudo_externo` (o primeiro hoje sem uso
  local, mas a linha de import quebra se o nome/local mudar).

Nenhum outro arquivo de `tela/` importa `_quebrar_texto` ou
`_quebrar_sem_ansi` fora dessa cadeia.

## Arquivos futuros autorizados

Alterar (migração): `tela/renderizacao/conteudo_externo.py`,
`tela/renderizacao/matriz_participantes.py`,
`tela/renderizacao/paginacao_interna.py`, `tela/renderizador.py` (só o bloco
de import). Alteração condicional, apenas se estritamente necessário:
`tela/renderizacao/console.py`, `tela/renderizacao/texto_ansi.py`,
`tela/teste_estilo_h0070.py`, `tela/teste_estilo_h0071.py`,
`tela/teste_estilo_h0073_h0063.py`, `tela/teste_navegacao.py`. Criar:
`docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0077.md`.

## Arquivos preservados

`tela/renderizacao/composicao_textual.py` e
`tela/teste_composicao_textual.py` (núcleo de H-0076, aprovado, não
redefinido); `tela/renderizacao/popup.py`, `tela/teste_popup.py`,
`demo/teste_demo_popup.py`; ADRs, contratos, nomenclatura,
`docs/backlog.md`.

## Testes previstos

Caminho compartilhado (conteúdo externo consumindo o núcleo; ausência de
wrap concorrente), consumidores (hierarquia, tabela, conjuntos de campos,
matriz de participantes), medição (altura/linhas coerente com a composição
renderizada), paginação (divisão interna coerente com linhas físicas), ANSI
(largura visual, CSI indivisível, sem vazamento de SGR) e regressão
transversal (comportamento observável preservado onde semântico, largura
dinâmica). O handoff nomeia os testes de demonstração já existentes que
fazem parte da superfície real (`teste_conteudo_externo_h0036_render`,
`teste_h0037_manual_001_marcador_truncamento`,
`TestDistribuicaoMatricialH0035`,
`test_h0045_ph07_coerencia_renderer_mapa_fisico`, entre outros) e fixa um
comando `pytest` focal reproduzível cobrindo
`tela/teste_renderizador.py` (fachada de `testes_renderizador/*`),
`tela/teste_formato_filho_dois_niveis_por_foco.py`, `tela/teste_paginacao.py`,
`tela/teste_navegacao.py`, os três `teste_estilo_h00{70,71}*`,
`tela/teste_composicao_textual.py` e `tela/teste_popup.py` — os dois últimos
como prova de não regressão de H-0076.

## Fronteira com H-0076

O handoff reafirma que o núcleo e a integração do popup entregues por
H-0076 estão aprovados e não são redefinidos nem retocados. H-0077 apenas
estende o consumo do mesmo núcleo ao caminho de conteúdo externo. A decisão
de não política global de whitespace/separadores (D-0027-03, D-0027-06,
contrato §6) é reiterada explicitamente como restrição, com a orientação de
que diferenças de comportamento só permanecem quando forem requisito
semântico real de um consumidor concreto listado em §3 do handoff — nunca
como convergência global.

## Verificações

Os dois artefatos foram criados nos caminhos exatos exigidos. Nenhum código
nem outro documento foi alterado nesta etapa. `git status --short` e
`git diff --check` sobre os dois arquivos devem ser executados pelo operador
como confirmação final, conforme instruído.

## Bloqueios

Nenhum. A superfície foi delimitável com a investigação focal realizada, sem
necessidade de decisão normativa nova ou decisão do usuário.
