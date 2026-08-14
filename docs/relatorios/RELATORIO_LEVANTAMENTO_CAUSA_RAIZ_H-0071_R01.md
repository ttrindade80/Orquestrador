# Levantamento de causa raiz — H-0071 / ADR-0046

## Q1 — autoridade e Curva × Ornamental

`contrato_estilo.md` é `AUTORIDADE_DE_SCHEMA`: define os sete nomes e os
campos, mas não associa símbolos aos nomes. `10_ESTILO.md` é
`AUTORIDADE_TERMINOLOGICA` e também só lista os nomes. A autoridade concreta
é `CONFIGURACAO_CONCRETA`, `config/estilo.json`: no WIP, Curva e Ornamental
estão ambas em `╭`/`╮` (linhas 54–66). O `HEAD` permitido confirma o estado
anterior: Curva `╭`/`╮` e Ornamental `❲`/`❳`. A mudança ocorreu durante H-0071,
conforme FATO-02; o WIP não fornece um commit que permita data mais precisa.

As únicas associações normativas encontradas são incorretas: ADR-0046
`DEC-ITEM0010-CHIP-01` (linhas 217–228) e sua aplicação em
`contrato_chip.md` §10.1 (`DECISAO_NORMATIVA`) dizem Curva `(…)` e Ornamental
`╭…╮`. Isso conflita com o catálogo concreto existente; a ADR pretendia
fechar composição multitecla e explicitamente diz que não escolhe schema nem
renderer. Portanto não autorizava trocar valores de Ornamental. H-0071
(`HANDOFF`, §5) e P04 (relato factual, não autoridade) transportam a afirmação
errada de Ornamental `╭`/`╮`. `contrato_barra_de_menus.md` e as nomenclaturas
21/31 tratam `[PgUp][PgDn]` como identificador documental e `[PgUp/PgDn]`
como forma física; não definem Curva/Ornamental. O primeiro artefato
normativo foi a ADR; o primeiro handoff que tornou a associação requisito de
implementação foi H-0071; a primeira materialização executável foi a mutação
de `config/estilo.json`.

## Q2/Q3 — caminho real e estado

A cadeia real da tela reproduzida é:

`config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json`
(`chip_paginas`, `tecla: "PgUp][PgDn"`, `regra_ativo: "quando_paginacao"`)
→ `_carregar_modelo_por_id`/`construir_modelo` em `demo/demo.py`
→ `_estabelecer_foco_paginacao_inicial` fixa foco e página 1
→ `renderizar_estado` → `renderizar_tela`
→ `_preparar_contexto_navegacao` → `_linhas_barra`.

O agrupamento H-0071 só entra quando há dois chips contíguos com IDs exatos
`chip_pagina_anterior` e `chip_pagina_proxima` (`barra_menus.py`, linhas
875–913). H-0063 não satisfaz essa condição: cai em `_texto_chip_barra`, que
passa a string inteira como uma única tecla a `compor_chip_multitecla`.
O compositor está correto para entrada bem formada, mas embrulha
`"PgUp][PgDn"` como payload único e produz `[PgUp][PgDn]`. H-0054 e H-0055
contêm a mesma declaração legada; `demo/teste_demo_console.py` inclusive
asserta essa forma.

Em 1/1, `total_paginas` calcula 1, logo o estado canônico esperado seria
PgUp=False e PgDn=False. Porém H-0063 só possui `chip_paginas`; seu estado
agregado é `True`, pois `quando_paginacao` é regra desconhecida para
`_avaliar_regra_ativo` e cai no retorno ativo. Não há estados por componente,
nem `inativo=True` entregue ao compositor. Assim `cor_inativo` não é perdido
por `_conteudo_chip`: ele nunca é solicitado. A composição correta preserva
estados quando recebe a tupla `(True, True)`, como demonstram os testes
unitários. O texto literal `Páginas` também é anexado fora da unidade
estilizada por `_texto_chip_multitecla`; se a exigência for colorir esse
texto, há conflito adicional com a regra documental que o mantém externo.

A execução TTY real, com `stty rows 60 cols 200`, reproduziu
`página 1/1`, `[PgUp][PgDn] Páginas` e ambas as amostras `╭A╮`.

## Q4 — validade dos testes e do P04

`tela/teste_estilo_h0071.py` é `UNITARIO_HELPER` e
`ASSERT_RECONSTRUIDO_DA_PROPRIA_CONFIGURACAO`: deriva a expectativa dos
próprios dados do preset, logo igualdade Curva/Ornamental passa. Seus testes
de Páginas chamam `_texto_chip_multitecla` diretamente. `demo/teste_demo_estilo_h0071.py`
é `INTEGRACAO_PARCIAL`, mas fabrica a barra correta com dois chips. As
regressões de `demo/teste_demo_paginacao.py` e
`tela/testes_renderizador/barra_menus.py` usam fixtures H-0045 também corretas;
são `INTEGRACAO_PARCIAL`/`REGRESSAO`, não o modelo H-0063. `fundamentos.py`
é inspeção de fonte (`UNITARIO_HELPER`/`REGRESSAO`). O teste adicional
H-0063 passa 14/14, mas só verifica presença genérica de barra. Nenhum focal
é `PONTO_DE_ENTRADA_REAL` TTY. Os focais H-0071 passaram 45/45; a suíte
combinada deu 276 pass e a falha conhecida de H-0070. P04, portanto, validou
helpers/fixtures e confundiu “mesmo compositor” com “mesma entrada declarativa”;
ademais declarou manual TTY fora do patch.

## Q5 — matriz mínima

| CAMADA | ARQUIVO | DEFEITO CONFIRMADO | TIPO FUTURO |
|---|---|---|---|
| Norma | `docs/adr/ADR-0046-alteracao-aplicacao-estilo-global-runtime.md` | exemplo Curva/Ornamental incompatível | PATCH_ADR |
| Aplicação | `docs/contratos/contrato_chip.md` | repete associação incompatível | PATCH_APLICACAO_ADR |
| Concreto | `config/estilo.json` | Ornamental alterado para Curva | PATCH_IMPLEMENTACAO |
| Entrada real | `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json` | chip legado único; estado agregado | PATCH_IMPLEMENTACAO |
| Entradas legadas | `config/telas/demo/h0054_selecao_multinivel.json`; `config/telas/demo/h0055_dois_niveis_por_foco.json` | mesma forma executável | PATCH_IMPLEMENTACAO |
| Handoff/relato | `docs/handoff/H-0071-correcao-chips-multitecla-barra-menus-estilo.md`; `docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0071_P04.md` | preservação/resultado factual errados | PATCH_HANDOFF; CORRECAO_FACTUAL_RELATORIO |
| Testes | `tela/teste_estilo_h0071.py`; `demo/teste_demo_estilo_h0063.py`; `demo/teste_demo_console.py` | oracle dinâmico, ausência do ponto real, expectativa legada | TESTE |

Ordem mínima: corrigir ADR e contrato; corrigir configuração concreta e as
declarações legadas; ajustar handoff; acrescentar regressão do ponto real e
atualizar expectativas legadas; corrigir P04 por último. Não há defeito
confirmado que exija mudança em `tela/renderizacao/estilo.py`,
`barra_menus.py`, `tela/carregamento/estilo.py`, contratos de barra,
nomenclaturas 10/21/31, paginação ou fundamentos: o caminho canônico desses
arquivos funciona.

`NAO_CONFIRMADO`: se o rótulo literal `Páginas` deve receber ANSI além das
teclas; o escopo formal de H-0054/H-0055; e a data exata da mutação WIP de
Ornamental. Arquivos adicionais de código/configuração abertos: `demo/demo.py`,
`tela/renderizador.py`, `tela/renderizacao/tela.py`,
`tela/renderizacao/contexto_execucao.py`, `tela/estilo.py`,
`tela/paginacao.py`, `tela/renderizacao/console.py`, as três configurações
H-0054/H-0055/H-0063, `demo/teste_demo_estilo_h0063.py`,
`demo/teste_demo_console.py` e `tela/testes_renderizador/integracao.py`.
