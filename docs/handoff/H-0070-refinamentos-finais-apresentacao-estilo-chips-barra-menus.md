# H-0070 — Refinamentos finais de apresentação do Estilo e aplicação dos estilos de chip na Barra de Menus

## 1. Metadata e rastreabilidade

```yaml
projeto: Orquestrador
item: ITEM-0010
adr: ADR-0046
handoff: H-0070
data_criacao: 2026-08-13
status: READY_FOR_IMPLEMENTATION
predecessor_funcional: H-0069
relacao: refinamento_visual_pos_funcional
historico_predecessor:
  H-0069:
    estado: TECNICAMENTE_E_MANUALMENTE_APROVADO
    aprovado_manualmente:
      - caminho_confirmado
      - caminho_abortado
      - demonstracao_integrada
      - retorno_normal_a_tela_estilo
      - ausencia_do_crash_anteriormente_encontrado
    pendencia: validacao_manual_final_do_ITEM-0010_aguardando_refinamentos_visuais
item_0010:
  estado: em_andamento
capacidade_pretendida: refinamentos_finais_apresentacao_estilo_e_chips_multitecla
```

Os refinamentos cobertos por este handoff **não** são regressão de H-0069/P02.
H-0069 permanece `TECNICAMENTE_E_MANUALMENTE_APROVADO` nos itens já validados
(§2 acima). A validação manual final do `ITEM-0010` (H-0069 §19) permanece
pendente e será retomada ao final deste handoff (§13).

## 2. Objetivo exclusivo

Entregar, em uma única fatia coesa, os refinamentos visuais finais
identificados na validação manual pós-P02 de H-0069:

1. remover os ordinais alfabéticos (`A)`, `B)`, `C)`) da apresentação dos
   filhos da tela Estilo, preservando hierarquia, indentação e indicador de
   preset vigente;
2. alinhar verticalmente as amostras visuais dos filhos de uma mesma
   categoria em uma coluna comum;
3. corrigir a composição de chips multitecla para os presets `Ponto`,
   `Destaque Texto` e `Destaque Fundo` (hoje incorretos/incompletos);
4. aplicar essa composição correta aos chips **reais** da Barra de Menus, não
   apenas às amostras da tela Estilo;
5. preservar a geometria da Barra de Menus (sem sobreposição, truncamento
   indevido ou perda de espaçamento) sob troca de estilo em runtime e resize.

Este handoff **não** introduz funcionalidade nova fora desse conjunto, não
reabre semântica de confirmação/candidato/persistência, e não altera a ordem
lógica da Barra de Menus.

## 3. Autoridade e capacidade predecessora

- `ADR-0046` continua a autoridade normativa vigente para presets de estilo,
  candidato, aplicação e persistência; este handoff não cria segunda noção de
  override, segundo mecanismo de persistência/publicação, nem novo preset.
- H-0069 encerrou a capacidade funcional do fluxo de demonstração integrada
  (§20 daquele handoff). H-0070 não reabre esse fluxo — apenas ajusta
  apresentação de tela Estilo e materialização de chips já existentes.
- H-0069 §19 previu explicitamente que a validação manual final do
  `ITEM-0010` poderia identificar "pequenos refinamentos de apresentação de
  chips" sem que isso reabrisse a arquitetura. Este handoff é esse
  refinamento, formalizado como fatia própria por decisão do gerente.

## 4. Evidência técnica levantada nesta etapa documental

Achados obtidos por leitura de código (escopo §16) que fundamentam as
decisões de §5–§11 e comprovam que nenhuma delas exige mudança arquitetural
além do já autorizado por ADR-0046:

### 4.1 Defeito reproduzível hoje na Barra de Menus real

`config/estilo.json` tem `chip.preset_default = "Ponto"` (estado atual do
arquivo de configuração de produção, já presente no worktree — este handoff
não o altera). Executando a tela `h0045_paginacao_console_unico` com
`carregar_estilo()` (sem override), a Barra de Menus real produz hoje:

```text
Esc. SAIR  PgUp. PgDn. PÁGINAS   ✥. NAVEGAR
```

(com o chip `PgUp.` em `cor_inativo` quando a página 1 é a primeira). Este é
exatamente o padrão proibido por §8: dois chips `Ponto` separados
(`PgUp. PgDn.`) em vez de um único chip `PgUp/PgDn.`. A causa é estrutural:
`tela/renderizacao/barra_menus.py` já possui um agrupamento exclusivo para o
par `chip_pagina_anterior`/`chip_pagina_proxima` (H-0051 / D-PGU-01 a
D-PGU-03, linhas ~864-897), mas esse agrupamento apenas concatena o texto de
cada chip renderizado individualmente — correto para presets delimitados
(`Colchete` → `[PgUp][PgDn]`), incorreto para `Ponto`/`Destaque Texto`/
`Destaque Fundo`, que exigem um único chip composto.

### 4.2 `cor_texto`/`cor_fundo` do chip nunca chegam à Barra de Menus real

Em `tela/renderizacao/barra_menus.py:122` (`_texto_chip_barra`), os campos
`cor_texto`/`cor_fundo` do `EstiloResolvido` são lidos mas explicitamente
descartados (`_ = (cor_texto, cor_fundo)`, comentário "H-0039: sem efeito
enquanto o valor semântico for 'padrão'"). Somente `cor_inativo` e
`cor_alerta` são de fato aplicados (envelope `codigo + base + reset`, linhas
165-174). Ou seja: hoje os presets `Destaque Texto`/`Destaque Fundo` não têm
nenhum efeito visual na Barra de Menus real — apenas nas amostras da tela
Estilo (`tela/renderizacao/estilo.py::amostra_chip`, que já aplica cor
corretamente). §11 exige fechar exatamente essa lacuna.

### 4.3 `EstiloResolvido` do chip não carrega o nome do preset

`tela/carregamento/estilo.py::EstiloResolvido` expõe apenas os 5 campos
concretos do chip (`caractere_esquerdo`, `caractere_direito`, `cor_texto`,
`cor_fundo`, `caixa_alta|), sem o nome do preset (`"Ponto"`, `"Destaque
Texto"` etc.). A implementação **não pode** decidir a composição multitecla
por nome de preset — deve discriminar estruturalmente pelos campos já
carregados, por exemplo:

- `caractere_esquerdo == " " and caractere_direito == "."` → família `Ponto`;
- `caractere_esquerdo == " " and caractere_direito == " " and cor_texto !=
  "padrão"` → família `Destaque Texto`;
- `caractere_esquerdo == " " and caractere_direito == " " and cor_fundo !=
  "padrão"` → família `Destaque Fundo`;
- caso contrário (delimitadores não-espaço, como `[`/`]`, `╭`/`╮`, `❲`/`❳`,
  `-`/`-`) → comportamento vigente preservado (§7).

Essa é uma leitura estrutural dos mesmos 5 campos já resolvidos por
`config/estilo.json` — não inventa preset novo nem novo campo de
configuração.

### 4.4 Ordinal alfabético dos filhos e composição do prefixo de linha

`tela/estilo.py` declara, em `_NIVEIS_FORMATO` (linha ~75), o nível `filho`
com `designador={"tipo": "alfabetico_maiusculo", "sufixo": ")"}`. O texto
concreto (`"A)"`, `"B)"`, ...) é calculado por
`tela/renderizacao/designadores.py::_texto_designador` e montado, junto com o
cursor de navegação e o indicador de inclusão (vigente/não vigente), em
`tela/renderizacao/conteudo_externo.py::_linhas_apresentacao_hierarquia_com_mapa`
(modo não verboso, linhas ~195-211). A ordem atual de montagem do prefixo de
cada linha é:

```text
prefixo_indicador (cursor →/espaço) + prefixo_inclusao (● / ○ vigente) +
recuo ("  " × profundidade) + marcador ("A)" + espaço) + texto
```

`prefixo_inclusao`/`incluido_on`/`incluido_off` chegam a essa função a partir
de `tela/renderizacao/console.py::_linhas_console` (ramo
`_selecao_multinivel`, que cobre `dois_niveis_por_foco` — política usada pela
tela Estilo), com `incluir_selecao=True`. Esse é o indicador visual de preset
vigente/não vigente citado em §5/§14 — mecanismo distinto do cursor e do
ordinal, que já deve ser preservado tal como está.

Simplesmente remover o `designador` do nível `filho` faz o ramo `else` (sem
marcador) omitir também o espaço que hoje separa o marcador do texto (linha
201-202 de `conteudo_externo.py`), quebrando o alinhamento do texto. Cumprir
literalmente a decisão de §5 (cursor ocupando a região hoje ocupada pelo
ordinal) exige portanto tocar
`tela/renderizacao/conteudo_externo.py::_linhas_apresentacao_hierarquia_com_mapa`
— função genérica também usada por outras apresentações multinível. Este
handoff autoriza essa alteração pontual (§9), com a condição de não alterar o
comportamento para nenhum nível/tela cujo `designador` não seja vazio (todos
os consumidores atuais, exceto o nível `filho` da tela Estilo, continuam com
designador não vazio).

Único consumidor de produção do designador `alfabetico_maiusculo` combinado
com `dois_niveis_por_foco`/cursor/inclusão: `tela/estilo.py`. Fixtures de
teste que também exercitam designadores alfabéticos e merecem checagem de
não regressão: `config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json`,
`config/telas/demo/h0036_hierarquia_conteudo.json`.

### 4.5 Composição das amostras — ausência de alinhamento entre irmãos

`tela/renderizacao/estilo.py::compor_titulo_com_amostra` monta, por filho
isoladamente, `nome + SEPARADOR_NOME_AMOSTRA (2 espaços fixos) + amostra` —
sem qualquer conhecimento dos nomes dos demais filhos da mesma categoria.
Não há hoje nenhum alinhamento de coluna entre amostras de irmãos. O módulo
já expõe, e este handoff deve reutilizar, os utilitários de largura visual
existentes em `tela/renderizacao/texto_ansi.py`: `_largura_sem_ansi`
(largura visível ignorando sequências ANSI/CSI) e `_ljust_sem_ansi`
(padding à direita respeitando essa largura) — ambos já usados por
`tela/renderizacao/barra_menus.py` e por
`demo/teste_demo_estilo_h0064.py::test_largura_visual_amostra_chip_no_quadro_coerente`.
Nenhuma função nova de largura visual precisa ser criada.

O cálculo do maior nome por categoria precisa ocorrer em
`tela/estilo.py::ControladorTelaEstilo._construir_conteudo` (que já itera
`secao["presets"].items()` por categoria antes de criar cada `no_filho`),
não dentro de `compor_titulo_com_amostra` (que só vê um preset por vez).

## 5. Decisões visuais fechadas — filhos da tela Estilo

- Remover completamente os ordinais alfabéticos (`A)`, `B)`, `C)` ou
  equivalentes) da apresentação dos filhos.
- Preservar a hierarquia visual e a indentação atual dos filhos (mesma
  quantidade de recuo por profundidade que hoje).
- O cursor de navegação deve ocupar a região horizontal hoje utilizada pelo
  ordinal alfabético (a coluna liberada pela remoção de `"A) "` não deve
  simplesmente colapsar).
- Preservar o indicador visual de preset vigente/não vigente (o par
  `incluido_on`/`incluido_off`, §4.4) exatamente como hoje se comporta.
- Preservar o alinhamento do texto dos presets (nome do preset inicia em
  coluna consistente entre linha focalizada e não focalizada).
- O cursor não pode provocar deslocamento diferente entre linha focalizada e
  não focalizada — a largura do prefixo deve ser idêntica em ambos os casos
  (já é o caso hoje para `indicador`/`indicador_off`, que têm a mesma
  formatação; a implementação deve preservar essa igualdade também na nova
  composição).

Exemplo de aceite (`→` cursor focado, espaço = não focado; `●`/`○` = vigente/
não vigente; a posição exata do cursor dentro da região liberada — colado ao
recuo ou colado ao texto — é decisão de implementação, desde que a largura
seja idêntica entre focado/não focado):

```text
antes (hoje):     →  ●   A) Borda Curva  ╭─╮
depois (H-0070):  ●    →  Borda Curva  ╭─╮
                  ○       Borda Reta   ┌─┐
```

## 6. Decisões visuais fechadas — alinhamento das amostras

- As amostras visuais dos filhos de uma mesma categoria devem começar
  exatamente na mesma coluna visual.
- Determinar a maior largura visual entre os nomes dos filhos da categoria
  (usando `_largura_sem_ansi`, mesmo os nomes sendo texto plano hoje — não
  usar `len()` bruto).
- Completar os nomes menores com espaços até essa largura (usar
  `_ljust_sem_ansi`, não `str.ljust`).
- Iniciar todas as amostras da categoria na mesma coluna.
- ANSI/CSI tem largura visual zero — a amostra em si pode conter códigos de
  cor (categoria `chip`); isso não pode influenciar a coluna de início
  calculada a partir dos *nomes* (que são texto plano) nem ser contado como
  largura ao validar o alinhamento resultante.
- Regra vale para as quatro categorias (`borda`, `chip`,
  `indicadores.selecionado`, `indicadores.incluido`), inclusive quando a
  amostra contém cor ANSI (categoria `chip`, presets `Destaque Texto`/
  `Destaque Fundo`).

Exemplo conceitual (categoria `borda`):

```text
Borda Curva  ╭─╮
Borda Reta   ┌─┐
Linha        ──
```

## 7. Preservação obrigatória — chips de uma tecla

Chips que representam uma única tecla **não mudam**. Comportamento e
representação atuais preservados para todos os presets, em todas as telas.
Este handoff não autoriza redesenhar chips de uma tecla para harmonizá-los
com os casos multitecla.

## 8. Preservação obrigatória — presets com delimitadores próprios

Presets cujos campos `caractere_esquerdo`/`caractere_direito` não são espaço
(hoje: `Colchete`, `Curva`, `Ornamental`, `Traço`) mantêm a composição
multitecla vigente: cada tecla materializada individualmente, concatenação
direta sem separador, sem "/" introduzido. Exemplo canônico preservado:
`[PgUp][PgDn] Páginas`. Não inserir política universal de separador que
afete esses presets.

## 9. Chip multitecla — preset `Ponto`

Discriminador estrutural: `caractere_esquerdo == " " and caractere_direito
== "."` (§4.3).

- Uma tecla: comportamento vigente preservado, sem alteração.
- Duas ou mais teclas da mesma ação: formam um único chip textual, teclas
  separadas por `"/"`, um único ponto final.

```text
 PgUp/PgDn. Páginas
```

Composição: um espaço inicial pertencente ao chip, conteúdo `PgUp/PgDn`, um
único ponto final, seguido do espaçamento normal chip→texto (mesmo
`vao_chip_texto` hoje usado entre chip e rótulo). Não produzir
`PgUp. PgDn.`, `PgUp./PgDn.`, `PgUp/PgDn` (sem ponto) nem `[PgUp][PgDn]`
quando o preset vigente for `Ponto`.

## 10. Chip multitecla — preset `Destaque Texto`

Discriminador estrutural: `caractere_esquerdo == " " and caractere_direito
== " " and cor_texto != "padrão"` (§4.3).

- Uma tecla: comportamento vigente preservado.
- Multitecla: teclas da mesma ação formam um único chip, separadas por
  `"/"`; representação visual ` PgUp/PgDn ` (espaço lateral antes e depois).
- A cor de texto aplica-se ao conteúdo `PgUp/PgDn` (mesmo mecanismo de
  `_codigo_ansi_de_cor` + `_ANSI_RESET_FG` já usado por `cor_inativo`/
  `cor_alerta` em `_texto_chip_barra`); os espaços laterais não precisam
  receber o efeito de cor, mas pertencem à largura visual do chip.
- O texto da ação (`Páginas`) permanece semanticamente fora do chip,
  separado pelo espaçamento normal do renderizador (`vao_chip_texto`), sem
  duplicação acidental de espaços entre o fim do chip e o rótulo.

## 11. Chip multitecla — preset `Destaque Fundo`

Discriminador estrutural: `caractere_esquerdo == " " and caractere_direito
== " " and cor_fundo != "padrão"` (§4.3).

- Uma tecla: comportamento vigente preservado.
- Multitecla: teclas da mesma ação formam um único chip, separadas por
  `"/"`; representação visual ` PgUp/PgDn `.
- O fundo cobre toda a unidade visual, incluindo os dois espaços laterais —
  `PgUp/PgDn` e os espaços formam um único retângulo destacado (envelope de
  cor de fundo abrindo antes do primeiro espaço e fechando depois do
  último, via `_codigo_ansi_de_fundo`-equivalente para a Barra de Menus —
  reaproveitar a derivação FG→BG já usada por
  `tela/renderizacao/estilo.py::_codigo_ansi_de_fundo` para as amostras, sem
  criar segunda tabela de tradução de cor).
- A largura visual do chip inclui os dois espaços. O texto da ação permanece
  fora da área de fundo.

## 12. Aplicação real na Barra de Menus

Os comportamentos de §9-§11 devem funcionar nos chips **reais** da Barra de
Menus (`tela/renderizacao/barra_menus.py`), não apenas nas amostras da tela
Estilo (`tela/renderizacao/estilo.py::amostra_chip`, que já está correto e
não precisa mudar). Ponto de extensão nominal: o bloco de agrupamento
exclusivo do par `chip_pagina_anterior`/`chip_pagina_proxima`
(`tela/renderizacao/barra_menus.py`, linhas ~864-897, H-0051/D-PGU-01 a
D-PGU-03) precisa se tornar dependente da família estrutural do preset de
chip vigente (§4.3): preservar a concatenação por tecla individual para
presets delimitados (§8); produzir um único chip composto para `Ponto`/
`Destaque Texto`/`Destaque Fundo` (§9-§11). `_texto_chip_barra`
(`tela/renderizacao/barra_menus.py:122`) precisa deixar de descartar
`cor_texto`/`cor_fundo` (§4.2) e passar a aplicá-los quando != `"padrão"`,
com o mesmo padrão de envelope (`codigo + conteúdo + reset`) já usado para
`cor_inativo`/`cor_alerta`, respeitando a extensão do envelope aos espaços
laterais quando for `cor_fundo` (§11).

Nenhum outro par de chips além de `chip_pagina_anterior`/
`chip_pagina_proxima` é afetado por este handoff — a extensão para "ação com
mais de uma tecla" fica restrita ao mecanismo de agrupamento já existente
(H-0051), sem generalizar para pares declarados por outras telas/JSONs. O
texto descritivo da ação (`Páginas`) continua semanticamente separado do
chip.

## 13. Geometria da Barra de Menus

- Cálculo por largura visual efetiva: a montagem de linha única/multilinha
  já usa `_largura_sem_ansi` (`tela/renderizacao/barra_menus.py`, linhas
  ~919 e ~936) — preservar esse ponto único de cálculo; qualquer chip novo
  produzido por §9-§11 deve continuar sendo medido por essa mesma função,
  nunca por `len()` do texto ANSI bruto.
- Códigos ANSI de cor/fundo têm largura zero; espaços visíveis (inclusive os
  espaços laterais de `Destaque Texto`/`Destaque Fundo`) contam normalmente
  na largura.
- Alinhamento coerente dos itens independentemente do preset vigente; sem
  sobreposição; sem truncamento indevido causado apenas pela troca de
  preset; sem perda do espaçamento chip→descrição (`vao_chip_texto`).
- Recomposição correta quando o estilo muda em runtime (candidato aplicado)
  e após resize — reaproveitar os mecanismos de recomposição já cobertos
  pelas suítes H-0045/H-0069 (nenhum mecanismo novo de recomposição).
- Se, durante a implementação, for identificado outro ponto de cálculo de
  colunas/posições da Barra baseado em largura pré-renderização além dos já
  citados nesta seção, a implementação deve apontá-lo explicitamente no
  relatório de implementação (§18) antes de alterá-lo.

## 14. Fora de escopo explícito

Este handoff **não** altera:

- ordem lógica das ações da Barra de Menus, nem posição global dos itens;
- regra futura de ordenação do chip Navegar;
- organização geral da Barra além do agrupamento já existente (H-0051);
- troca de `? Ajuda` para `F1`; `F2`, `F3`, `F5`, `F11`; tiling por tela;
- nova política de paginação;
- semântica de confirmação, candidato, persistência ou publicação
  (H-0065–H-0068 permanecem exatamente como entregues);
- novo popup ou novo tipo de popup;
- nova categoria de estilo ou novo preset em `config/estilo.json`;
- redesign geral da tela Estilo além do especificado em §5-§6;
- modificação da ordem dos quatro grupos de categoria;
- alteração da sessão de demonstração local H-0069.

## 15. Preservações do ITEM-0010

Preservar integralmente, sem exceção: F4 abre Estilo; quatro categorias
vigentes; navegação em dois níveis; `Esc` em filhos = Voltar; `Esc` na raiz =
Sair; seleção de candidato; `Aplicar` somente com candidato divergente;
demonstração integrada H-0069; popup de confirmação; `ABORTADO` preservando
candidato; `CONFIRMADO` persistindo/publicando; limpeza da sessão H-0069;
comportamento de resize já aprovado; chips de uma tecla (§7); persistência
fail-closed; `config/estilo.json` sem escrita antes da confirmação.

## 16. Arquivos autorizados para implementação

- `tela/estilo.py` — remover o designador `alfabetico_maiusculo` do nível
  `filho` em `_NIVEIS_FORMATO`; em `_construir_conteudo`, pré-calcular a
  maior largura visual dos nomes por categoria (via `_largura_sem_ansi`) e
  passá-la para a composição do título do filho.
- `tela/renderizacao/estilo.py` — `compor_titulo_com_amostra` (e/ou nova
  função irmã) passa a aceitar a largura de padding do nome e usar
  `_ljust_sem_ansi` antes de concatenar `SEPARADOR_NOME_AMOSTRA` + amostra.
  Reexportar em `__all__` o que for necessário.
- `tela/renderizacao/conteudo_externo.py` —
  `_linhas_apresentacao_hierarquia_com_mapa`: alteração pontual e
  condicionada (nível focalizável com indicador presente e designador
  vazio) para reposicionar o cursor na região antes ocupada pelo marcador,
  sem alterar o comportamento de nenhum outro nível/tela com designador não
  vazio. Qualquer alteração aqui exige a bateria de regressão completa de
  §19-I, incluindo as fixtures citadas em §4.4.
- `tela/renderizacao/barra_menus.py` — `_texto_chip_barra` (aplicar
  `cor_texto`/`cor_fundo`, §4.2/§10/§11) e o bloco de agrupamento
  `chip_pagina_anterior`/`chip_pagina_proxima` (§12), tornando-o dependente
  da família estrutural do preset de chip (§4.3).
- `tela/teste_estilo_h0070.py` — testes novos dedicados (unidade/estrutura)
  cobrindo §5-§6 (categorias A e B de §19).
- `demo/teste_demo_estilo_h0070.py` — testes novos de integração/E2E
  cobrindo §9-§13 na Barra de Menus real, incluindo runtime style change e
  resize (categorias E a H de §19).
- Extensões (sem reescrita) nos arquivos de teste já existentes listados em
  §19 como "testes existentes a ampliar".
- `docs/relatorios/IMP-0070-refinamentos-finais-apresentacao-estilo-chips-barra-menus.md`
  — relatório futuro da implementação (§18).

Nenhuma fixture nova é autorizada: §17 já identifica fixtures existentes
suficientes para reprodução e demonstração. Não alterar `config/estilo.json`,
ADR, contratos, nomenclatura ou backlog.

## 17. Arquivos preservados (não alterar sem necessidade técnica comprovada)

- `tela/renderizacao/estilo.py::amostra_chip`/`amostra_borda`/
  `amostra_selecionado`/`amostra_incluido` — já corretos, não precisam
  mudar de comportamento (apenas a composição do título ganha padding).
- `tela/renderizacao/designadores.py` — a lógica de cálculo de designadores
  em si não muda; apenas deixa de ser invocada com designador não vazio
  para o nível `filho` da tela Estilo.
- `tela/renderizacao/console.py`, `tela/renderizacao/popup.py`,
  `tela/renderizacao/tela.py`, `tela/renderizador.py`,
  `tela/renderizacao/contexto_execucao.py` — sem necessidade técnica
  identificada nesta etapa; se a implementação encontrar necessidade real,
  deve justificá-la explicitamente no relatório de implementação (§18).
- `tela/carregamento/estilo.py`, `tela/estilo.py` (fora das mudanças de
  §16) — mecanismo de candidato/aplicação/persistência inalterado.
- Sessão de demonstração local H-0069 (`demo/demo.py`, ramo `Enter/Aplicar`
  → demonstração → popup) — reutilizada sem alteração de mecanismo; a
  demonstração deve automaticamente herdar a correção de §9-§13 por
  consumir os mesmos renderers genéricos, sem necessidade de tocar o
  próprio fluxo de demonstração.

## 18. Critérios de aceite

1. Nenhum filho da tela Estilo exibe `A)`, `B)`, `C)` ou designador
   alfabético equivalente.
2. O cursor de navegação ocupa a região horizontal antes ocupada pelo
   ordinal; largura de prefixo idêntica entre linha focalizada e não
   focalizada.
3. Indicador de preset vigente/não vigente (`●`/`○`) preservado.
4. Indentação e alinhamento do texto dos presets preservados.
5. Amostras de uma mesma categoria começam todas na mesma coluna visual,
   inclusive quando contêm ANSI (categoria `chip`).
6. Chips de uma tecla idênticos ao comportamento vigente, para todos os
   presets, em todas as telas.
7. Presets delimitados (`Colchete` e demais) preservam `[PgUp][PgDn]` sem
   `/` introduzido.
8. Preset `Ponto` com ação multitecla produz exatamente `PgUp/PgDn.` como
   chip único (espaço inicial + conteúdo + ponto final), nunca
   `PgUp. PgDn.`.
9. Preset `Destaque Texto` com ação multitecla produz um único chip
   ` PgUp/PgDn ` com cor aplicada ao conteúdo.
10. Preset `Destaque Fundo` com ação multitecla produz um único chip
    ` PgUp/PgDn ` com fundo cobrindo inclusive os espaços laterais.
11. Os três comportamentos acima valem na Barra de Menus real (não somente
    na amostra da tela Estilo), inclusive após troca de estilo em runtime e
    após resize.
12. Nenhuma sobreposição, truncamento indevido ou perda de espaçamento
    chip→texto causada pela troca de preset.
13. Toda a suíte de regressão listada em §19-I permanece verde (ou as
    divergências são causalmente explicadas no relatório de implementação).

## 19. Testes obrigatórios

### A. Filhos (novo — `tela/teste_estilo_h0070.py`)
- ordinal `A)`/`B)`/`C)` ausente do texto renderizado dos filhos;
- cursor ocupa a coluna liberada (largura de prefixo focalizado ==
  não focalizado; conteúdo visível na posição correspondente muda entre os
  dois estados);
- texto do preset permanece alinhado (mesma coluna de início entre irmãos
  do mesmo nível);
- indicador `●`/`○` de vigente/não vigente preservado e correto.

### B. Amostras (novo — `tela/teste_estilo_h0070.py`)
- início de todas as amostras de uma categoria na mesma coluna visual
  (usar `_largura_sem_ansi` para medir, nunca `len()`);
- nomes de comprimentos diferentes recebem padding adequado
  (`_ljust_sem_ansi`);
- ANSI presente na amostra (categoria `chip`) não altera a coluna física
  calculada a partir dos nomes.

### C. Chips de uma tecla (extensão de `tela/testes_renderizador/barra_menus.py`)
- comportamento atual preservado para todos os presets, uma tecla.

### D. Multitecla delimitada (extensão de `tela/testes_renderizador/barra_menus.py` e regressão de `demo/teste_demo_paginacao.py`)
- comportamento existente preservado: preset `Colchete` continua produzindo
  `[PgUp][PgDn]`.

### E. `Ponto` (novo — `demo/teste_demo_estilo_h0070.py`)
- `PgUp`/`PgDn` gera um único chip `PgUp/PgDn.` com espaço inicial e ponto
  final único.

### F. `Destaque Texto` (novo — `demo/teste_demo_estilo_h0070.py`)
- `PgUp`/`PgDn` forma um único chip; conteúdo recebe a cor; largura visual
  inclui os espaços laterais.

### G. `Destaque Fundo` (novo — `demo/teste_demo_estilo_h0070.py`)
- `PgUp`/`PgDn` forma um único chip; fundo cobre inclusive os espaços
  laterais; largura visual correta.

### H. Barra de Menus real (novo — `demo/teste_demo_estilo_h0070.py`)
- aplicação real dos três presets multitecla na Barra (não só na amostra);
- texto da ação separado do chip;
- alinhamento correto;
- recomposição correta sob troca de estilo em runtime;
- recomposição correta após resize;
- ANSI sem impacto indevido na largura calculada.

### I. Regressão (executar a suíte completa; corrigir causas em vez de conveniência)
- `tela/teste_estilo_h0063.py` a `tela/teste_estilo_h0069.py`;
- `demo/teste_demo_estilo_h0063.py` a `demo/teste_demo_estilo_h0069.py`;
- `tela/teste_popup.py`;
- `tela/testes_renderizador/barra_menus.py`;
- `tela/testes_renderizador/integracao.py` (em particular
  `test_h0045_p11_conjunto_vazio_chips_pagina_visiveis_e_inativos` e
  `test_h0045_p12_vazio_chips_visiveis_inativos_e_autoridade_geometrica`,
  que consultam `estado_ativo_chips["chip_pagina_anterior"/"chip_pagina_proxima"]`
  — devem continuar corretas; a *lógica* de ativo/inativo não muda, apenas
  a composição textual);
- `demo/teste_demo_paginacao.py` — **atenção**: as asserções literais
  `"[PgUp][PgDn] Páginas"` em
  `test_demo_h0045_p01_cadeia_tty_quatro_caracteres_e_chips_pagina_1`,
  `test_demo_h0045_p01_chips_visiveis_sem_foco_ambos_inativos` e
  `test_demo_h0045_p02_sequencia_resize_barra_sem_residuo` já falham hoje,
  antes de qualquer mudança de código deste handoff — porque
  `config/estilo.json` tem `chip.preset_default = "Ponto"` (não
  `"Colchete"`) no worktree atual (§4.1). Isso não é uma falha externa
  desconectada para classificar e deixar de lado: é a manifestação direta
  do defeito que este handoff corrige. A implementação deve atualizar essas
  asserções para a composição correta do preset `Ponto`
  (`" PgUp/PgDn. Páginas"`, ajustada à captura real de `_sem_ansi`), como
  parte da entrega, e não como conveniência à parte;
- fixtures `config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json` e
  `config/telas/demo/h0036_hierarquia_conteudo.json` (via seus testes
  associados) — checar que a alteração de §16 em
  `_linhas_apresentacao_hierarquia_com_mapa` não as afeta;
- suíte completa do projeto.

Falhas externas realmente desconectadas deste escopo (se houver, fora do
padrão descrito acima) devem ser classificadas causalmente no relatório de
implementação, não corrigidas por conveniência dentro do H-0070.

## 20. Demonstração reproduzível

Sem modificar `config/estilo.json` de produção:

1. **Reprodução do defeito atual (`Ponto`)**: carregar a tela
   `h0045_paginacao_console_unico` com `carregar_estilo()` padrão (lê
   `config/estilo.json`, hoje com `preset_default = "Ponto"`) e renderizar —
   reproduz `PgUp. PgDn.` na Barra de Menus real, conforme §4.1. Após a
   correção, a mesma chamada deve produzir `PgUp/PgDn.`.
2. **`Destaque Texto`/`Destaque Fundo`**: usar o mecanismo de candidato já
   existente (`estilo_runtime.definir_preset_candidato`, mesma técnica de
   H-0065, sobre raiz de teste isolada como em H-0061/H-0068/H-0069) para
   selecionar esses presets de `chip` antes de renderizar a mesma tela
   `h0045_paginacao_console_unico` (que já possui o par
   `chip_pagina_anterior`/`chip_pagina_proxima`), sem tocar
   `config/estilo.json` de produção.
3. **Amostras/filhos da tela Estilo**: reutilizar `h0063_estilo_estrutura_
   navegacao_dois_niveis` (tela Estilo) já coberta por H-0063–H-0069.
4. **Demonstração integrada real (Barra + demais elementos, runtime style
   change, resize, `CONFIRMADO`/`ABORTADO`)**: reutilizar a fixture
   `config/telas/demo/h0069_estilo_demonstracao_integrada.json` e o fluxo
   `Enter/Aplicar` → demonstração → popup já entregue por H-0069.

Nenhuma fixture nova é necessária para nenhum dos quatro pontos acima.

## 21. Validação manual posterior

Este handoff exige validação manual TTY pelo usuário **depois** do QA
técnico, cobrindo no mínimo:

- ausência dos ordinais dos filhos da tela Estilo;
- posição do cursor e indentação dos filhos;
- alinhamento das amostras entre irmãos de uma mesma categoria;
- todos os presets de chip (uma tecla, delimitados, `Ponto`, `Destaque
  Texto`, `Destaque Fundo`);
- `Ponto` com ação multitecla (`PgUp/PgDn.`) na Barra de Menus real;
- `Destaque Texto` multitecla na Barra de Menus real;
- `Destaque Fundo` multitecla na Barra de Menus real;
- resize da Barra de Menus com cada um desses presets;
- troca de estilo em runtime (demonstração integrada H-0069);
- `Aplicar`, `ABORTADO`, `CONFIRMADO`, retorno à tela Estilo.

Esta rodada deve ser considerada também a validação manual final do
`ITEM-0010` (H-0069 §19), desde que nenhum novo defeito material seja
encontrado. Esta validação **não** é executada durante `CRIAR_HANDOFF` —
fica para a etapa de QA/validação posterior à implementação.

## 22. Relatório de implementação esperado

`docs/relatorios/IMP-0070-refinamentos-finais-apresentacao-estilo-chips-barra-menus.md`
deve registrar: arquivos efetivamente alterados (contra a lista de §16);
decisão final de posicionamento do cursor na região do ordinal (§5); prova
de que nenhum outro consumidor de
`_linhas_apresentacao_hierarquia_com_mapa` regrediu; resultado da suíte de
regressão de §19-I, incluindo a correção das asserções de
`demo/teste_demo_paginacao.py`; e o resultado da demonstração TTY de §20.

## 23. Bloqueios

Nenhum bloqueio identificado nesta etapa documental. As buscas focais de
código (§16 do prompt de autoria) confirmaram que todas as decisões fechadas
em §5-§13 são executáveis dentro dos mecanismos já existentes (`EstiloResolvido`,
utilitários de largura visual em `texto_ansi.py`, agrupamento H-0051 de
`chip_pagina_anterior`/`chip_pagina_proxima`, mecanismo de inclusão/cursor de
`conteudo_externo.py`), sem exigir novo preset, novo campo de configuração,
segunda noção de override ou alteração normativa de ADR-0046.

## 24. Fora de escopo (consolidado)

Ver §14. Adicionalmente, fora de escopo: qualquer alteração em
`config/estilo.json`, ADR-0046, contratos ou nomenclatura como parte desta
etapa documental — este handoff descreve como a implementação futura deve
consumir a configuração vigente, sem propor alteração ao schema.
