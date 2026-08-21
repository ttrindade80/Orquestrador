---
name: H-0077-composicao-textual-conteudo-externo-consumidores
description: Migração do caminho compartilhado de conteúdo externo e consumidores correlatos para o núcleo canônico de composição textual
metadata:
  type: handoff
  id: H-0077
  item: ITEM-0027
  adr: ADR-0049
  qa_adr: ADR_APPROVED
  qa_aplicacao: ADR_APPLICATION_APPROVED
  estado: CONCLUIDO
  patch_handoff: P02
  qa_handoff: H1_HANDOFF_APPROVED
  implementacao_patch: P02
  qa_implementacao: I1_IMPLEMENTATION_APPROVED
  decisao_aplicada: D-0027-10
  validacao_manual: MANUAL_VALIDATION_APPROVED
  residuo_independente: QA-IMPL-H0077-03
  handoffs_planejados_total: 2
  handoff_predecessor: H-0076
---

# H-0077 — Composição textual: conteúdo externo e consumidores

## 1. Objetivo e unidade de trabalho

Migrar o caminho compartilhado de conteúdo externo
(`tela/renderizacao/conteudo_externo.py`) e os consumidores correlatos —
hierarquia, tabela, conjuntos de campos, matriz de participantes, cálculo de
altura, mapa físico e paginação interna — para o núcleo canônico de
composição textual entregue e aprovado por H-0076
(`tela/renderizacao/composicao_textual.py`), garantindo coerência entre
renderização, medição, altura e paginação interna.

Após a reabertura, a base normativa é o núcleo corrigido de H-0076: cada
consumidor deve fornecer o parágrafo lógico completo; o núcleo identifica e
distribui palavras inteiras em linhas físicas e só depois justifica as linhas
aplicáveis. Não há divisão por largura/células, hifenização automática ou
separação silábica. Resize e recomposição partem novamente do texto lógico
completo, nunca de linhas físicas anteriores.

Este handoff não reimplementa nem redefine o núcleo canônico. Ele reconcilia
a segunda autoridade de wrap ainda existente (`_quebrar_texto` local de
`conteudo_externo.py`, apoiada em `_quebrar_sem_ansi` de `texto_ansi.py` para
conteúdo ANSI) com a autoridade única já aceita.

## 2. Autoridades e fronteiras de decisão

Ordem de autoridade:

1. `docs/adr/ADR-0049-composicao-justificacao-global-texto-tui.md`;
2. `docs/contratos/contrato_composicao_textual.md`;
3. `docs/handoff/H-0076-composicao-textual-canonica-popup.md`, como fronteira
   já fechada do que pertence ao núcleo e do que foi propositalmente deixado
   fora dele;
4. `docs/nomenclatura/01_NUCLEO_COMUM.md` e
   `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`;
5. `docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_JUSTIFICACAO_GLOBAL_ITEM-0027.md`,
   somente como evidência factual da implementação atual.

O núcleo canônico corrigido (`tela/renderizacao/composicao_textual.py`) e sua
suíte (`tela/teste_composicao_textual.py`) são tratados como aprovados e
estáveis para esta reconciliação. Não redefinir `compor_texto`, `_quebrar_texto`
ou `_justificar_linha` desse módulo. Não criar fachada, registry, adapter ou
segunda camada estrutural sobre ele. Não criar política global de
whitespace/separadores — decisão já fechada por D-0027-03/D-0027-06 e pelo §6
do contrato: peculiaridade histórica só permanece quando for requisito
semântico real e local de um consumidor identificado abaixo.

Todo consumidor migrado deve herdar a semântica de D-0027-10: palavras são
indivisíveis, a formação das linhas precede a justificação e a recomposição
usa o parágrafo lógico completo. Um alias de compatibilidade, se necessário,
não pode manter regra própria de wrap nem constituir autoridade concorrente.

## 3. Cadeia concreta de consumidores localizada

Investigação focal em `tela/` (restrita à cadeia funcional; não é
descoberta documental) confirmou a seguinte cadeia de dependência da
autoridade local hoje em `conteudo_externo.py`:

- `tela/renderizacao/conteudo_externo.py` define `_quebrar_texto` (delega a
  `_quebrar_sem_ansi` de `texto_ansi.py` quando há ANSI) e `_truncar_com_marcador`.
  `_quebrar_texto` é usado internamente por
  `_linhas_apresentacao_hierarquia_com_mapa` (hierarquia, um e dois níveis),
  `_linhas_dois_niveis_formatado_com_mapa` (dois níveis por foco, H-0072),
  `_linhas_apresentacao_tabela` e `_linhas_apresentacao_conjuntos`
  (conjuntos de campos).
- `tela/renderizacao/matriz_participantes.py` importa `_quebrar_texto` e
  `_participantes_de_conteudo_externo` diretamente de `conteudo_externo`.
  `_altura_quebra_item` (medição de altura) chama `_quebrar_texto` e é
  consumida por `_larguras_mapa_fisico_matricial` (cálculo de mapa físico
  matricial); `_renderizar_participante_com_indicador` chama `_quebrar_texto`
  para a renderização efetiva.
- `tela/renderizacao/console.py` importa `_linhas_conteudo_externo` de
  `conteudo_externo` e `_altura_quebra_item`/`_larguras_mapa_fisico_matricial`
  de `matriz_participantes`. `_linhas_console` despacha para
  `_linhas_conteudo_externo`; `mapa_fisico_de_itens` deriva
  `linhas_fisicas = len(entrada["linhas"])` diretamente do resultado dessas
  funções — a coerência entre medição e renderização depende de que ambas
  usem a mesma fonte.
- `tela/renderizacao/paginacao_interna.py` importa `_quebrar_texto`
  diretamente de `conteudo_externo` e usa em `_linhas_texto_item_para_pagina`;
  consome `mapa_fisico_de_itens` (de `console.py`) em
  `_recortar_linhas_paginadas` e `_elemento_fragmentado_para_pagina` para
  recortar linhas por página.
- `tela/renderizador.py` importa `_quebrar_texto`, `_texto_valor_campo` e
  `_truncar_com_marcador` de `conteudo_externo`; `_quebrar_texto` não é
  chamada dentro do próprio arquivo (import hoje não consumido localmente),
  mas a linha de import quebra se a assinatura/local mudar sem reconciliação.

Nenhum outro arquivo de `tela/` importa `_quebrar_texto` ou
`_quebrar_sem_ansi` fora dessa cadeia.

### 3.1 Contrato de fornecimento dos consumidores

Os caminhos de hierarquia (um e dois níveis), dois níveis por foco, tabela e
conjuntos de campos devem selecionar localmente o conteúdo que constitui cada
parágrafo e fornecê-lo ao núcleo como texto lógico completo. Não podem
pré-fragmentar o parágrafo em linhas, células, segmentos ou pedaços físicos
para depois delegar esses pedaços ao núcleo. Prefixos, designadores,
indicadores, indentação, largura útil, estrutura de coluna, seleção de campos,
modo verboso/não verboso e truncamento deliberado continuam decisões locais;
não são convertidos em uma política global de composição.

Se um consumidor mantiver uma representação física local para uma
responsabilidade própria, ela não pode ser reutilizada como entrada lógica de
uma nova composição. Toda recomposição, inclusive após resize, deve voltar ao
parágrafo completo correspondente.

## 4. Escopo autorizado

### Alterar — código-fonte da migração

O P02 documental preserva o escopo funcional principal de H-0077:
`conteudo_externo.py`, `matriz_participantes.py` e
`paginacao_interna.py`, com `renderizador.py` limitado à reconciliação de
import/alias quando necessária. Condicionais já existentes permanecem
condicionais; não há autorização para ampliar a migração.

- `tela/renderizacao/conteudo_externo.py`: substituir a implementação local
  de `_quebrar_texto` (e o desvio para `_quebrar_sem_ansi` em texto com ANSI)
  pelo consumo do núcleo canônico. Cada dispatcher deve encaminhar o
  parágrafo lógico completo, sem pré-fragmentação física. `_truncar_com_marcador`,
  `_texto_valor_campo`, os dispatchers de apresentação, prefixos,
  designadores, indicadores, indentação de continuação, estrutura de coluna e
  a escolha de campos quebráveis permanecem locais e intocados em sua
  semântica.
- `tela/renderizacao/matriz_participantes.py`: ajustar o ponto de consumo de
  `_quebrar_texto` (import e uso em `_altura_quebra_item`,
  `_renderizar_participante_na_celula`/`_renderizar_participante_com_indicador`
  e `_larguras_mapa_fisico_matricial`) para a mesma composição canônica.
  Medição, renderização e mapa devem operar sobre palavras inteiras e linhas
  físicas efetivamente formadas, preservando indicadores, margens e
  `content_w` como responsabilidades locais.
- `tela/renderizacao/paginacao_interna.py`: ajustar o ponto de consumo de
  `_quebrar_texto` em `_linhas_texto_item_para_pagina` para a mesma fonte e
  para as linhas físicas reais que serão paginadas; não contar ou recortar
  fragmentos produzidos por uma quebra anterior.
- `tela/renderizador.py`: ajustar apenas o bloco de import de
  `conteudo_externo` (linhas do import de `_quebrar_texto`,
  `_texto_valor_campo`, `_truncar_com_marcador`) se o local/nome da função
  mudar; não é autorização para alterar lógica de renderização do arquivo.

### Alteração condicional — somente se estritamente necessário

- `tela/renderizacao/console.py`: só se a coerência entre
  `_linhas_conteudo_externo`/`_linhas_dois_niveis_formatado_com_mapa` e
  `mapa_fisico_de_itens` exigir ajuste pontual para permanecer consistente
  (D-0027-08). O mapa deve refletir as linhas físicas efetivamente formadas;
  não é autorização para introduzir uma nova política de composição. Se
  `_linhas_console`/`mapa_fisico_de_itens` já ficarem coerentes sem alteração,
  o arquivo permanece intacto.
- `tela/renderizacao/texto_ansi.py`: só se for estritamente necessário para
  reutilizar ou tornar coerentes primitivas ANSI existentes, no mesmo padrão
  de restrição já aplicado por H-0076. Se o núcleo canônico já cobrir o
  necessário, o arquivo permanece intacto.
- `tela/teste_estilo_h0070.py`, `tela/teste_estilo_h0071.py`,
  `tela/teste_estilo_h0073_h0063.py`, `tela/teste_navegacao.py`: consomem
  `_linhas_apresentacao_hierarquia_com_mapa` e/ou
  `_linhas_dois_niveis_formatado_com_mapa` e/ou `_quebrar_texto` de
  `conteudo_externo`. Só podem ser alterados se a convergência de
  comportamento (D-0027-03) mudar uma saída hoje coberta por esses testes;
  nesse caso, a mudança deve ser justificada como convergência para o
  comportamento canônico, não como reescrita de expectativa. Se a divergência
  observada for maior do que um ajuste pontual de fixture/expectativa, parar
  e emitir o pedido de `AUTORIZACAO_DE_ESCOPO_NECESSARIA`.

### Alterações adicionais autorizadas pelo patch P01

- `tela/teste_paginacao.py`: alteração de teste focal exclusivamente nos três
  testes P16 identificados por QA:
  `test_p16_fluxo_continuo_comeca_na_proxima_linha_disponivel`,
  `test_p16_condicional_move_inteiro_quando_nao_cabe_no_residuo` e
  `test_p16_item_maior_que_pagina_nas_tres_politicas`. A finalidade única é
  fazer nova regressão semântica após D-0027-10, reconciliando fixtures e
  expectativas com as linhas físicas efetivamente produzidas pela composição
  canônica. Se um fixture deixar de exercer a política desejada, reconstruí-lo
  preservando a política; não restaurar a quebra antiga nem alterar a
  paginação funcional para satisfazer expectativa obsoleta. Não enfraquecer
  políticas P16, remover cenários, trocar valores esperados sem reconstruir
  semanticamente o cenário ou mascarar regressões; os testes devem continuar
  comprovando as mesmas políticas de paginação.
- `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json`:
  alteração excepcional e mecânica para remover somente o literal residual
  `\n` preexistente que invalida o JSON. Não alterar estrutura JSON, conteúdo
  semântico, valores, estilos, configuração de tela ou indentação além do
  estritamente decorrente da remoção do resíduo.

QA-IMPL-H0077-03 permanece fora do escopo: o resíduo independente de H-0070
não autoriza arquivo adicional nem correção como condição deste handoff.

### Criar

- `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0077.md`.

Qualquer arquivo estritamente necessário fora desta lista exige parada antes
da alteração e o pedido de `AUTORIZACAO_DE_ESCOPO_NECESSARIA` definido em
§9.

### Preservar integralmente (não alterar)

- `tela/renderizacao/composicao_textual.py`;
- `tela/teste_composicao_textual.py`;
- `tela/renderizacao/popup.py`;
- `tela/teste_popup.py`;
- `demo/teste_demo_popup.py` (salvo regressão transversal estritamente
  necessária, o que não é esperado nesta migração);
- ADRs, contratos, nomenclatura, `docs/backlog.md`.

H-0076 está aprovado e não deve ser refeito nem ter seu resultado alterado.

## 5. Fronteira com H-0076

H-0076 entregou o núcleo (`compor_texto`, parágrafo lógico completo,
distribuição por palavras inteiras, justificação sob solicitação, segurança
ANSI, CSI indivisível, fechamento/restabelecimento de SGR) e sua integração
exclusiva com o popup. Uma palavra individual maior que a largura permanece
íntegra para o compositor; o núcleo não escolhe clipping, overflow, scroll,
erro, fallback, truncamento ou expansão de container. H-0077 não toca
`popup.py` nem redefine essas capacidades: apenas estende o mesmo núcleo já
aprovado ao caminho de conteúdo externo e aos consumidores listados em §3.
Se um consumidor ou renderer já tiver tratamento físico local para uma
palavra maior que a largura, ele só pode ser preservado como responsabilidade
própria e sem modificar semanticamente a palavra dentro do compositor.

## 6. Objetivo estrutural

Ao final desta implementação:

1. `conteudo_externo.py` não mantém implementação independente equivalente
   de composição/wrap já coberta pelo núcleo canônico;
2. hierarquia, dois níveis por foco, tabela e conjuntos de campos fornecem
   parágrafos lógicos completos, sem pré-fragmentação física, através do
   caminho compartilhado reconciliado;
3. todos os consumidores migrados formam linhas com palavras inteiras,
   sem hifenização, separação silábica ou divisão por largura/células;
4. resize e recomposição voltam ao texto lógico completo, sem usar linhas
   físicas anteriores como entrada;
5. cálculo de linhas/altura, mapa físico, paginação e renderização usam a
   mesma composição efetivamente formada (D-0027-08);
6. não existe terceira autoridade genérica concorrente de composição
   textual;
7. regras específicas dos consumidores (prefixos, designadores,
   indicadores, indentação de continuação, largura útil, estrutura de
   coluna, campos quebráveis, verboso/não verboso, truncamento de linha
   única) continuam locais.

## 7. Fronteira crítica — medição e renderização

Quando um consumidor usa composição textual para determinar altura, calcular
quantidade de linhas, construir mapa físico ou decidir divisão/paginação,
esses cálculos devem permanecer coerentes com a renderização efetiva. É
defeito se medição usar regra antiga enquanto renderização usa o núcleo
novo, se altura e saída física divergirem, ou se a paginação calcular linhas
por mecanismo diferente do efetivamente renderizado. Isso se aplica
concretamente a `_altura_quebra_item` (medição) versus
`_renderizar_participante_com_indicador` (renderização) em
`matriz_participantes.py`; ambos devem usar a mesma semântica de palavras
inteiras, largura útil, modo e tratamento ANSI. Aplica-se também a
`_larguras_mapa_fisico_matricial`: suas larguras e alturas devem derivar das
linhas físicas reais, não de uma contagem baseada na antiga fragmentação de
palavras. Por fim, `mapa_fisico_de_itens` deve refletir as linhas de
`_linhas_console` que serão renderizadas, e a paginação deve recortar essa
mesma sequência. Qualquer divergência entre esses caminhos é defeito.

## 8. Truncamento e ANSI

`_truncar_com_marcador` (truncamento deliberado de linha única) não é
absorvido pelo núcleo de composição, não é transformado em wrap, e wrap não
é transformado em truncamento — a distinção funcional entre os dois
permanece intacta em `conteudo_externo.py`.

`_truncar_com_marcador` não pode simular o tratamento de uma palavra maior
que a largura dentro do compositor. A decisão já aprovada para whitespace e
separadores também permanece aberta em termos concretos: vãos entre palavras
podem participar da justificação, mas não se cria contrato global de
preservação literal, normalização, condensação ou trimming.

Reutilizar o núcleo H-0076 e as primitivas já existentes de `texto_ansi.py`.
Não criar parser ANSI paralelo, segunda implementação de largura visual ou
segunda implementação genérica de quebra ANSI. A largura deve ser visual,
CSI deve permanecer íntegro e uma palavra estilizada deve continuar
indivisível, sem vazamento de SGR entre linhas ou regiões.

## 9. Exceção operacional

Se a implementação descobrir arquivo adicional estritamente necessário além
da lista fixada em §4, parar antes da alteração e retornar:

```yaml
status: AUTORIZACAO_DE_ESCOPO_NECESSARIA
caminho:
motivo:
mudanca_esperada:
impacto_sem_autorizacao:
```

Não ampliar autonomamente.

## 10. Testes obrigatórios

Cobrir, no mínimo:

### Caminho compartilhado

- `conteudo_externo.py` consumindo o núcleo canônico para wrap;
- palavras inteiras em hierarquia, dois níveis por foco, tabela e conjuntos
  de campos, com cada caminho fornecendo o parágrafo lógico completo;
- ausência de implementação genérica de wrap concorrente remanescente em
  `conteudo_externo.py` (nem local, nem via `_quebrar_sem_ansi` para o papel
  de wrap genérico).

### Consumidores

- hierarquia (um e dois níveis, incluindo `dois_niveis_por_foco`);
- tabela;
- conjuntos de campos;
- matriz de participantes (`_altura_quebra_item`,
  `_renderizar_participante_com_indicador`, distribuição matricial).

### Medição

- altura/quantidade de linhas coerente com a composição efetivamente
  renderizada, para hierarquia, matriz de participantes e mapa físico
  (`mapa_fisico_de_itens`).
- palavra maior que a largura não contada como múltiplas linhas por
  fragmentação antiga; a quantidade medida deve ser a quantidade realmente
  renderizada.
- `_altura_quebra_item`, `_renderizar_participante_com_indicador` e
  `_larguras_mapa_fisico_matricial` usando a mesma semântica de palavras
  inteiras e a mesma composição efetiva.

### Paginação

- divisão interna (`paginacao_interna.py`) coerente com as linhas físicas
  realmente produzidas, sem perda nem duplicação.
- nova regressão semântica dos três P16 após D-0027-10; fixtures que deixem
  de exercer as políticas devem ser reconstruídos, sem restaurar quebra de
  palavra nem ajustar paginação para expectativas obsoletas.

### ANSI

- largura visual;
- CSI indivisível;
- palavra estilizada indivisível;
- ausência de vazamento de SGR entre linhas/regiões dos consumidores
  migrados.

### Composição e justificação

- linhas formadas antes da justificação, com expansão posterior somente nos
  vãos entre palavras das linhas aplicáveis;
- nenhuma política global nova para última linha, distribuição matemática,
  resto, linha de uma palavra ou whitespace/separadores arbitrários;
- ausência de hifenização automática, separação silábica, divisão por células
  e qualquer pré-fragmentação de parágrafo pelos consumidores;
- palavra maior que a largura mantida íntegra pelo compositor, sem escolher
  globalmente clipping, overflow, scroll, erro, fallback, truncamento ou
  expansão de container;
- resize recompondo o texto lógico completo, sem usar linhas físicas
  anteriores como entrada.

### Regressão transversal

- comportamento observável dos consumidores preservado onde for semântico
  (prefixos, designadores, indicadores, indentação, truncamento de linha
  única, verboso/não verboso);
- largura dinâmica: mudança de largura sem inconsistência entre altura e
  paginação.

Incluir na regressão os testes de demonstração já existentes para essa
superfície, quando fizerem parte da cadeia real: `teste_conteudo_externo_h0036_render`,
`teste_h0037_manual_001_marcador_truncamento`,
`teste_h0037_manual_002_esc_primeiro`,
`teste_h0037_qapp7_verb_sem_corte_silencioso` (em
`tela/testes_renderizador/conteudo_externo.py`);
`TestDistribuicaoMatricialH0035` (em
`tela/testes_renderizador/matriz_participantes.py`);
`test_h0045_p10_mapa_fisico_usa_largura_da_celula_e_preserva_fragmentos`
(revalidado sem exigir fragmentação de palavras),
`test_h0045_ph07_coerencia_renderer_mapa_fisico`,
`test_h0045_p12_quebra_textual_por_largura_marcadores_unicos` (em
`tela/testes_renderizador/integracao.py`).

### Requisitos pós-implementação do patch P01

Após o futuro patch de implementação, devem ser demonstrados:

- nova regressão semântica, com aprovação dos três testes P16 autorizados
  acima, provando as mesmas políticas sob as linhas reais do núcleo;
- coleta e execução dos sete testes H-0073/H-0063 em
  `tela/teste_estilo_h0073_h0063.py`, após a correção do fixture;
- repetição da suíte focal integral do H-0077;
- aprovação contínua dos testes de H-0076 (`tela/teste_composicao_textual.py`
  e `tela/teste_popup.py`);
- `git diff --check` limpo.

A regressão obrigatória de H-0076 deve permanecer exatamente:

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q \
  tela/teste_composicao_textual.py \
  tela/teste_popup.py \
  demo/teste_demo_popup.py
```

QA-IMPL-H0077-03 não precisa ser corrigido como condição de H-0077 enquanto
permanecer objetivamente independente.

## 11. Suíte — comando focal reproduzível

Não impor a suíte global. Executar obrigatoriamente o comando focal
reproduzível associado aos arquivos consumidores identificados em §3-§4, mais
o núcleo e o popup para prova de não regressão de H-0076:

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q \
  tela/teste_renderizador.py \
  tela/teste_formato_filho_dois_niveis_por_foco.py \
  tela/teste_paginacao.py \
  tela/teste_navegacao.py \
  tela/teste_estilo_h0070.py \
  tela/teste_estilo_h0071.py \
  tela/teste_estilo_h0073_h0063.py \
  tela/teste_composicao_textual.py \
  tela/teste_popup.py
```

`tela/teste_renderizador.py` é a fachada que agrega
`tela/testes_renderizador/conteudo_externo.py`,
`tela/testes_renderizador/matriz_participantes.py` e
`tela/testes_renderizador/integracao.py`, entre outros módulos da mesma
suíte. Teste focal adicional só é permitido se decorrer diretamente dos
arquivos autorizados em §4.

## 12. Critérios de aceite da implementação futura

A implementação deve demonstrar, reprodutivelmente:

1. `conteudo_externo.py` consome a autoridade canônica de
   `composicao_textual.py` para wrap;
2. não existe wrap genérico concorrente remanescente nesse caminho (nem
   local, nem redirecionado para `_quebrar_sem_ansi` fora do papel que já
   lhe cabia antes desta migração);
3. hierarquia, dois níveis por foco, tabela, conjuntos de campos e matriz de
   participantes fornecem parágrafos completos, sem pré-fragmentação, e
   continuam funcionais com comportamento observável preservado onde
   semântico;
4. `_altura_quebra_item`,
   `_renderizar_participante_com_indicador` e
   `_larguras_mapa_fisico_matricial` concordam com a mesma composição de
   palavras inteiras;
5. altura, mapa físico, paginação interna e renderização concordam com as
   linhas físicas realmente produzidas;
6. resize recompõe o texto lógico completo e uma palavra maior que a largura
   não é partida nem transformada em política física global;
7. justificação ocorre somente depois da formação das linhas, sem política
   global para última linha, resto, linha de uma palavra ou separadores;
8. ANSI permanece correto (largura visual, CSI indivisível, palavra estilizada
   indivisível e sem vazamento de SGR);
9. truncamento de linha única (`_truncar_com_marcador`) permanece separado
   de wrap/composição;
10. H-0076 (núcleo e popup) não sofre regressão;
11. nenhuma política global de whitespace/separadores é criada.

Não exigir TTY manual como substituto da regressão técnica. A validação
visual posterior continua obrigatória para o popup longo justificado.

## 13. Validação manual posterior

Depois da regressão técnica de H-0077, repetir:

```zsh
python demo/demo.py h0077_texto_amplo_justificado
```

A inspeção principal permanece no popup longo justificado, verificando
palavras inteiras, recomposição após resize e justificação posterior à
formação das linhas. H-0077 não deve modificar essa demo neste patch
documental.

## 14. Relatório de implementação futuro

Criar `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0077.md`, registrando
somente: arquivos criados/alterados; consumidores migrados;
remoção/reconciliação das autoridades locais; coerência de
medição/renderização/paginação; testes; demonstração; desvios; bloqueios.
Máximo normal: 900 palavras.

## 15. Itens fora de escopo

- Redefinir ou reimplementar `tela/renderizacao/composicao_textual.py`;
- alterar `popup.py` ou reabrir a migração já aprovada de H-0076;
- criar política global de preservação, normalização, condensação ou
  trimming de whitespace/separadores;
- alterar `corpo.arranjo`, `tiling`, política de paginação, topologia
  `PageUp`/`PageDown`, schema de conteúdo, semântica dos dados ou taxonomia
  dos elementos funcionais;
- alterar padding/alinhamento de coluna, célula, chip, grade do lançador ou
  moldura de caixa;
- unificar padding/alinhamento estrutural com o núcleo de justificação de
  parágrafo;
- alterar ADRs, contratos, nomenclatura ou `docs/backlog.md`.

## 16. Bloqueios

QA-IMPL-H0077-03 permanece transportado como resíduo independente de H-0070,
fora do ITEM-0027. Não ampliar o escopo para corrigi-lo automaticamente.
Nenhum bloqueio documental adicional.
