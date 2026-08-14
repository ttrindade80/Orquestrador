# H-0071 — Correção de composição multitecla de chips e aplicação à Barra de Menus real

## 1. Metadata e rastreabilidade

```yaml
projeto: Orquestrador
item: ITEM-0010
adr: ADR-0046
handoff: H-0071
patch: P06
data_criacao: 2026-08-13
data_patch: 2026-08-14
status: H1_HANDOFF_APPROVED
predecessor_funcional: H-0070
relacao: correcao_pos_validacao_manual_e_pos_patch_normativo
estado_documental_transportado:
  ADR-0046:
    status_qa: ADR_APPROVED
    origem: patch_normativo_pos_P03
  aplicacao_documental_contratos_e_nomenclatura:
    status_qa: ADR_APPLICATION_APPROVED_WITH_NOTES
    origem: aplicacao_documental_pos_P03_P01
    nota: proveniencia_do_WIP_acumulado
    achado_material_pendente: nenhum
  bloqueios_documentais_vigentes: nenhum
achados_manuais_a_resolver:
  - MF-ITEM0010-001
  - MF-ITEM0010-002
  - MF-ITEM0010-003
achados_deste_patch:
  - ACH-H0071-P05-01
  - ACH-H0071-P05-02
```

Este patch reconcilia o handoff com a ADR-0046 pós-P03 e com a aplicação
documental pós-P03/P01. A nota de QA da aplicação é somente de proveniência
do WIP acumulado; não há achado material pendente nessa camada. Ele não
reabre H-0070 como um todo e não altera ADR, contratos, nomenclatura, código,
testes ou configuração nesta etapa.

Afirmações do relatório histórico
`docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0071_P04.md` — inclusive
as de que a Barra real já produz `[PgUp/PgDn]` e já preserva `cor_inativo` —
não são evidência vigente. Esse P04 é histórico e não deve ser sobrescrito;
não define o relatório da próxima execução. A correção factual/histórica
desse relatório fica para etapa posterior, depois de o comportamento final
estar novamente demonstrado.

## 2. Objetivo exclusivo

Autorizar uma implementação que entregue, em uma única fatia coesa:

1. `Destaque Texto` com somente o foreground do conteúdo em destaque, fundo
   normal em toda a unidade e um espaço normal em cada lateral;
2. a composição de qualquer ação multitecla como uma única unidade visual,
   com `/` entre teclas, tanto na amostra de Estilo quanto na Barra real;
3. a preservação dos estados funcionais ativo/inativo dos chips, inclusive
   quando os dois controles de Páginas tiverem estados diferentes;
4. a estrutura física vigente do console `ec → tg → tx`, com cursor, toggle e
   texto em posições distintas e estáveis.

Não há mudança de navegação, hierarquia, semântica de paginação ou política
de seleção. A correção vigente é de representação/entrada declarativa e de
configuração concreta dos delimitadores, não de novo compositor nem de nova
arquitetura de paginação.

## 3. Autoridade vigente e reconciliação pós-P03

Prevalecem `ADR-0046`, especialmente `DEC-ITEM0010-CHIP-01` a
`DEC-ITEM0010-CHIP-07`, e as seções aplicadas de:

- `docs/contratos/contrato_chip.md` §§10.1–10.5 e 12–14;
- `docs/contratos/contrato_estilo.md` §3.2 e regras R-14/R-15;
- `docs/contratos/contrato_barra_de_menus.md` §18.1 e regra R-14;
- `docs/nomenclatura/10_ESTILO.md`, `31_BARRA_DE_MENUS_E_CHIPS.md` e
  `32_CONSOLE.md`.

H-0070 é referência operacional. Sua antiga distinção entre presets que
concatenavam cada tecla individualmente e presets que formavam unidade única
está superada. A composição vigente é uniforme para todos os presets.

Curva e Ornamental são presets distintos. Não há equivalência gráfica entre
eles. Delimitadores vigentes:

- Curva: esquerda `╭`, direita `╮`;
- Ornamental: esquerda `❲`, direita `❳`.

## 4. Correções obrigatórias

### 4.1 Destaque Texto

`Destaque Texto` deve produzir conceitualmente ` PgUp/PgDn `.

Somente `PgUp/PgDn` recebe o foreground de destaque. O espaço esquerdo, o
conteúdo e o espaço direito conservam o fundo normal do terminal. Não existe
fundo destacado lateral, campo lateral opcional ou assimetria de fundo nessa
semântica. Nenhuma configuração adicional deve ser materializada para isso.

### 4.2 Unidade multitecla na amostra e na Barra real

Uma ação representada por duas ou mais teclas ocupa uma única unidade visual;
as teclas são separadas por `/` e os delimitadores do preset aparecem somente
nas extremidades externas. `[PgUp][PgDn]` não é forma física válida.

Exemplos vigentes:

```text
[PgUp/PgDn]
╭PgUp/PgDn╮
❲PgUp/PgDn❳
-PgUp/PgDn-
 PgUp/PgDn.
```

Destaque Texto: ` PgUp/PgDn `.

Correspondência normativa dos delimitadores:

- Colchete: `[PgUp/PgDn]`;
- Curva: `╭PgUp/PgDn╮`;
- Ornamental: `❲PgUp/PgDn❳`.

Assim, a Barra real no preset Colchete deve renderizar:

```text
[PgUp/PgDn] Páginas
```

É proibida a forma física `[PgUp][PgDn] Páginas`. Essa notação pode existir
somente como identificador documental das duas teclas, nunca como saída
renderizada. Chips de uma tecla mantêm o comportamento vigente.

A amostra da tela de Estilo e a Barra real devem consumir a mesma regra de
composição, com a mesma contenção de estilo e a mesma largura visual efetiva.
Sequências ANSI não contam como células.

O compositor canônico já produz essa unidade quando recebe entrada bem
formada. O defeito vigente não é o delimitador emitido pelo compositor.

### 4.3 Ativo e inativo

O compositor não pode neutralizar estado funcional já existente:

- chip ativo conserva aparência ativa;
- chip inativo usa `cor_inativo`;
- `Enter/Aplicar` inativo aparece em `cor_inativo`;
- Páginas totalmente inativo aparece em `cor_inativo`;
- se PgUp e PgDn tiverem estados funcionais diferentes, essa diferença é
  preservada na unidade única, sem separar a ação em dois chips visuais;
- mudança de preset, foreground ou fundo não neutraliza `cor_inativo`.

Cor, fundo e reset ficam contidos na unidade visual do chip e não vazam para
o texto descritivo, o chip seguinte ou outra região da Barra.

Assim, `cor_inativo` não é perdido posteriormente pelo compositor: o estado
inativo nunca chega ao compositor. Em página 1/1, `total_paginas = 1`:
semanticamente PgUp e PgDn devem estar inativos. A correção deve ocorrer na
representação/entrada adequada, de modo que o estado funcional real de PgUp
e de PgDn seja calculado e transportado até o compositor.

### 4.4 Estrutura `ec → tg → tx`

`MF-ITEM0010-003` permanece requisito vigente. A implementação deve
preservar a estrutura vigente, sem redesenhar navegação ou hierarquia:

```text
>   [ ] Texto
    [ ] Texto
    [x] Texto
```

`ec`, `tg` e `tx` ocupam colunas físicas distintas; o toggle não fica colado
ao cursor. A linha focalizada e a não focalizada mantêm as mesmas colunas de
toggle e texto. Este handoff não autoriza alterar
`tela/renderizacao/conteudo_externo.py` para os defeitos atuais. Se a
implementação futura encontrar evidência positiva de que esse arquivo precisa
mudar, deve parar e solicitar exceção operacional antes da alteração.

### 4.5 Causa executável confirmada da paginação (ACH-H0071-P05-02)

A tela real usa entrada declarativa legada. Cadeia confirmada para H-0063:

`config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json`

contém um único chip de Páginas com:

- `tecla`: `"PgUp][PgDn"`;
- `regra_ativo`: `"quando_paginacao"`.

Essa entrada segue até a Barra real. Como o modelo possui um único
`chip_paginas`, ele não satisfaz o agrupamento que trabalha com os dois IDs
canônicos `chip_pagina_anterior` e `chip_pagina_proxima`. A string inteira
`"PgUp][PgDn"` é então entregue como payload de uma única tecla ao
compositor. O compositor envolve corretamente esse payload e o resultado
físico acaba `[PgUp][PgDn]`.

A regra `"quando_paginacao"` não é reconhecida pelo avaliador vigente e
termina tratada como ativa. Por isso, em 1/1, o estado inativo nunca chega ao
compositor.

A implementação deve reconciliar essa representação legada com a entrada já
consumida pelo agrupamento/compositor vigentes, sem criar schema, formato
visual ou semântica de paginação novos. A mesma declaração legada confirmada
também existe em:

- `config/telas/demo/h0054_selecao_multinivel.json`;
- `config/telas/demo/h0055_dois_niveis_por_foco.json`.

Essas duas telas entram no escopo somente para impedir que o mesmo defeito
permaneça. Não se inventa comportamento específico novo para H-0054 ou
H-0055.

### 4.6 Presets Curva e Ornamental em `config/estilo.json` (ACH-H0071-P05-01)

O WIP acumulado ainda materializa Ornamental com os delimitadores de Curva.
A implementação futura deve restaurar na configuração concreta:

- Curva = `╭` / `╮`;
- Ornamental = `❲` / `❳`.

Não tratar os dois presets como equivalentes.

## 5. Preservações

Devem permanecer sem regressão: preset `Ponto`; `Destaque Fundo`; Curva
`╭`/`╮` distinta de Ornamental `❲`/`❳`; largura visual sem contar ANSI;
contenção de estilo; navegação existente; semântica funcional de paginação;
estados de uma tecla; fluxo de candidato, demonstração, confirmação,
persistência e publicação do ITEM-0010; Console `ec → tg → tx`; e os demais
comportamentos aprovados.

Ficam fora deste handoff: nova categoria ou preset; nova arquitetura,
schema ou semântica de paginação; alteração de ADR, contratos ou
nomenclatura; redesign da navegação ou da hierarquia; tiling;
F1/F2/F3/F5/F11; fullscreen; popup novo; e qualquer alteração não necessária
aos pontos deste patch.

## 6. Escopo de implementação — arquivos nominalmente autorizados

Nenhum diretório inteiro é autorizado. O conjunto abaixo substitui a
obrigação antiga de alterar renderers e carregamento para os defeitos
atuais. Não há defeito confirmado que exija correção em
`tela/renderizacao/estilo.py`, `tela/renderizacao/barra_menus.py`,
`tela/carregamento/estilo.py`, `docs/contratos/contrato_barra_de_menus.md`,
`docs/nomenclatura/10_ESTILO.md`,
`docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`,
`docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` ou
`tela/testes_renderizador/fundamentos.py`.

### 6.1 Produção

- **`config/estilo.json`** — restaurar Ornamental `❲`/`❳` e preservar Curva
  `╭`/`╮`.
- **`config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json`** —
  reconciliar a entrada declarativa legada de Páginas.
- **`config/telas/demo/h0054_selecao_multinivel.json`** — a mesma reconciliação
  da representação legada confirmada, sem comportamento novo.
- **`config/telas/demo/h0055_dois_niveis_por_foco.json`** — a mesma
  reconciliação da representação legada confirmada, sem comportamento novo.

O relatório futuro da implementação permanece autorizado e separado. A
próxima execução de PATCH_IMPLEMENTACAO deverá criar
`docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0071_P05.md`. Esse caminho
é o artefato obrigatório da próxima implementação e pertence à etapa futura
de PATCH_IMPLEMENTACAO; não sobrescrever o P04 histórico.

Arquivos que este handoff **não exige alterar** para os defeitos atuais:

- `tela/renderizacao/barra_menus.py`;
- `tela/renderizacao/estilo.py`;
- `tela/carregamento/estilo.py`;
- `tela/renderizacao/conteudo_externo.py`;
- `tela/testes_renderizador/fundamentos.py`.

A obrigação antiga de modificar esses arquivos, herdada de P01–P04, fica
revogada. Se durante a implementação futura surgir evidência positiva de que
algum deles precisa mudar, a implementação deve parar e solicitar exceção
operacional antes da alteração.

### 6.2 Testes a atualizar ou criar durante a implementação

Obrigação confirmada de correção ou acréscimo:

- **`tela/teste_estilo_h0071.py`** — a expectativa de presets não pode ser
  reconstruída a partir da própria configuração. Exigir expectativa
  independente/canônica da distinção Curva × Ornamental.
- **`demo/teste_demo_estilo_h0063.py`** — regressão que exercite a própria
  configuração real
  `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json` pelo
  caminho de carregamento/renderização da demonstração H-0063. Verificar
  semanticamente: ausência física de `[PgUp][PgDn]`; presença da composição
  canônica de Páginas; estado inativo em página 1/1. Não basta fabricar dois
  chips corretos dentro de fixture de teste.
- **`demo/teste_demo_console.py`** — atualizar a expectativa legada que ainda
  aceita/asserta `[PgUp][PgDn]` para a forma física vigente.

Outros testes já exigidos por este handoff permanecem úteis como regressão,
sem obrigação de alterar o conteúdo quando não houver defeito confirmado:

- `tela/testes_renderizador/barra_menus.py`;
- `demo/teste_demo_estilo_h0071.py`;
- `demo/teste_demo_paginacao.py`;
- `tela/teste_popup.py`;
- `tela/teste_renderizador.py`;
- `demo/teste_demo.py`;
- `demo/teste_demo_estilo_h0069.py`;
- `demo/teste_demo_estilo_h0070.py`.

Classificação de cobertura: testes diretos de `_texto_chip_multitecla` são
`UNITARIO_HELPER`; `demo/teste_demo_estilo_h0071.py` é `INTEGRACAO_PARCIAL`;
fixtures H-0045 são regressões sobre entradas já bem formadas; inspeções em
`fundamentos.py` são regressões/inspeção de fonte. Esses testes podem
permanecer úteis, mas não podem ser usados sozinhos como prova de que a tela
H-0063 real foi corrigida.

As expectativas devem verificar a saída final observável — texto, estados,
ANSI contido e colunas visuais — sem reproduzir internamente a implementação
para construir a expectativa.

## 7. Critérios de aceite mínimos

Os testes devem comprovar diretamente:

1. `Destaque Texto` sem qualquer alteração de fundo;
2. um espaço normal em cada lado de `Destaque Texto`;
3. `[PgUp/PgDn] Páginas` na Barra real da configuração H-0063, sem fabricar
   a entrada no teste;
4. ausência de `[PgUp][PgDn]` na renderização dessa mesma configuração;
5. `Aplicar` inativo usando `cor_inativo`;
6. Páginas inativo usando `cor_inativo` em página 1/1 da configuração H-0063;
7. estado funcional de PgUp/PgDn preservado quando diferente;
8. cursor, toggle e texto em colunas distintas;
9. mesma coluna de toggle e texto com e sem cursor;
10. Ponto e Destaque Fundo sem regressão;
11. amostra de Estilo e Barra real usando a mesma regra de composição;
12. Curva `╭`/`╮` distinta de Ornamental `❲`/`❳`, com expectativa canônica
    independente da configuração sob teste.

Também devem ser cobertos os presets delimitados vigentes, uma tecla sem
regressão, contenção/reset ANSI e largura visual sem ANSI contado. Cada
assert deve observar o resultado renderizado, não a existência de uma função
ou campo interno específico.

## 8. Validação manual posterior

Depois da aprovação técnica, o H-0071 exige validação em TTY real pelo
usuário. A verificação visual da tela H-0063 deve incluir:

1. `Páginas` não pode aparecer fisicamente como `[PgUp][PgDn]`;
2. em página 1/1, a ação deve apresentar estado inativo;
3. Curva deve aparecer como `╭A╮`;
4. Ornamental deve aparecer como `❲A❳`;
5. Destaque Texto deve continuar foreground-only;
6. Destaque Fundo e Ponto devem permanecer distintos;
7. Console `ec → tg → tx` deve ser preservado.

Também permanecem: `[PgUp/PgDn] Páginas` na forma canônica da Barra real;
`Aplicar` ativo/inativo; preservação de diferença funcional entre PgUp e
PgDn quando aplicável; posição de cursor, toggle e texto.

Esta validação manual não é executada no PATCH_HANDOFF.

## 9. Relatórios e bloqueios

O relatório desta etapa documental (PATCH_HANDOFF P06) é
`docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0071_P06.md`.
`docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0071_P05.md` pertence ao patch
anterior do próprio handoff e não é relatório de implementação. O relatório
futuro obrigatório da próxima PATCH_IMPLEMENTACAO é
`docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0071_P05.md`; só deve ser
produzido após a implementação e não substitui o P04 histórico.

Não há bloqueio documental para encaminhamento ao gerente. Nenhuma
implementação, alteração de teste, execução de QA ou commit faz parte desta
etapa.
