# H-0054 — `selecao_multinivel`

## 1. Identificação e fronteira

```yaml
handoff: H-0054
item: ITEM-0007
capacidade: selecao_multinivel
estado: pronto_para_implementacao
ultimo_patch_handoff_aprovado: P03
patch_atual: P04
decisao_vigente:
  id: D-MULTI-07-P04
  adr: ADR-0042_P04
  qa_adr: ADR_APPROVED
  aplicacao: ADR_APPLICATION_APPROVED
estado_implementacao:
  P03: D-MULTI-06-P03 implementado
  P04: suporte_transitorio_a_pai_nao_selecionavel_com_descendente_selecionavel
  suporte_P04_anterior: agora_obsoleto_por_mudanca_de_decisao
validacao_manual:
  H0054_selecao_descendente: APROVADO
  H0054_selecao_ascendente: APROVADO
  H0054_desselecao_ascendente: APROVADO
  H0054_paginacao_navegacao: APROVADO
  H0053_regressao: APROVADO
  teste_pai_nao_selecionavel: INVALIDADO_POR_MUDANCA_DE_DECISAO
predecessores:
  - H-0052
  - H-0053
proximo_handoff: H-0055
```

H-0054 entrega exclusivamente a capacidade `selecao_multinivel`: navegação e
seleção de conteúdo hierárquico de profundidade arbitrária, com uma única
topologia de navegação e seleção recursiva por Espaço. A política declarada é
`politica_navegacao.tipo: selecao_multinivel`; a estrutura dos dados, a
apresentação e o nome da fixture não podem inferir a política.

H-0055 (`dois_niveis_por_foco`) permanece fora deste handoff. A
`arvore_colapsavel` de H-0053 permanece navegável sem seleção; seu Espaço
continua dedicado a expandir/recolher. ITEM-0025 permanece futuro.

## 2. Capacidade operacional

### 2.1 Foco, cursor e percurso

- Tab e Shift+Tab continuam trocando o foco entre consoles focalizáveis.
- No console focalizado, o cursor aponta um único item lógico corrente. O
  cursor usa a identidade do nó/item, não uma linha física do terminal.
- Todos os níveis navegáveis da hierarquia pertencem a uma única topologia.
  Setas não criam toroides independentes por pai, nível ou ramo e não saltam
  para outro mecanismo de foco.
- O percurso deve reunir os nós navegáveis em uma sequência única coerente
  com a ordem hierárquica já transportada pelo conteúdo externo. A geometria
  existente continua sendo a autoridade para a posição física quando houver
  mais de uma coluna; H-0054 não cria geometria, distribuição ou política de
  apresentação nova.
- Item visível não navegável não recebe cursor. Somente o console focalizado
  exibe o indicador de item corrente, na coluna `ec` e pelo símbolo já
  resolvido no estilo.
- A entrada em um console e as reconciliações de cursor continuam obedecendo
  às regras vigentes de foco, página, redimensionamento, mudança de modo,
  filtro e atualização de dados. Não criar memória especial de cursor.

### 2.2 Seleção e desseleção

- A seleção é um conjunto de IDs estáveis em runtime, independente do foco,
  cursor, ordem de marcação e página, com um conjunto por console.
- A selecionabilidade é estruturalmente coerente em profundidade arbitrária:
  descendente selecionável implica nó selecionável e todos os ancestrais
  estruturais até a raiz selecionáveis. Portanto, toda raiz e todo pai
  intermediário com seleção abaixo possuem estado binário e `tg`.
- Todo item selecionável possui estado binário de seleção e `tg`, sem relação
  com sua profundidade: raiz selecionável, pai intermediário selecionável e
  folha selecionável recebem os mesmos símbolos vigentes `●`/`○` (ou os
  equivalentes do estilo).
- Item não selecionável não possui estado de seleção, não recebe `tg`, não
  entra no conjunto selecionado e não participa da unanimidade. Não pode
  possuir descendente selecionável; logo, sua subárvore é integralmente não
  selecionável. Pode ser folha ou pai de conteúdo também integralmente não
  selecionável.
- Pai não selecionável com descendente selecionável é configuração inválida e
  incoerente, fora do domínio válido de `selecao_multinivel`. Não há suporte
  funcional, chip, propagação, unanimidade ou teste funcional exigido para
  esse cenário.
- A definição do domínio válido não exige novo validador estrutural, mecanismo
  de rejeição, exceção ou schema.
- Espaço sobre uma folha selecionável alterna nos dois sentidos:
  não selecionada → selecionada e selecionada → não selecionada. Depois do
  toggle, reconciliar os ancestrais selecionáveis de baixo para cima.
- O estado de um pai selecionável é derivado exclusivamente dos filhos
  selecionáveis imediatos:

  ```text
  pai selecionado ⇔ todos os filhos selecionáveis imediatos estão selecionados
  ```

  Todos esses filhos marcados marcam o pai; qualquer filho selecionável
  imediato desmarcado desmarca o pai. Filhos não selecionáveis são ignorados.
  A regra vale em qualquer profundidade e não admite estado parcial,
  indeterminado ou terceiro símbolo.
- D-MULTI-06-P03 permanece integral: estado binário derivado, toggle manual de
  folhas, reconciliação ascendente, desseleção ascendente, Espaço descendente
  em pais selecionáveis, reconciliação posterior de baixo para cima,
  profundidade arbitrária e conjunto de IDs estáveis.
- Ao selecionar manualmente todos os filhos selecionáveis imediatos, marcar o
  pai e repetir a reconciliação recursivamente nos ancestrais até a raiz. Ao
  desselecionar um filho, desmarcar o pai e todos os ancestrais afetados pela
  mesma regra, preservando ramos independentes.
- Espaço sobre um pai atua recursivamente sobre todos os descendentes
  selecionáveis, em qualquer profundidade. A ação de inclusão seleciona todos
  esses descendentes; a ação de remoção remove todos esses descendentes. Em
  seguida, reconciliar de baixo para cima todos os pais intermediários e o
  próprio pai, deixando os toggles parentais coerentes com os filhos; a
  inclusão termina com o próprio pai marcado e a remoção com o próprio pai
  desmarcado.
- Descendentes não selecionáveis permanecem sem alteração. A implementação não
  pode incluí-los por conveniência nem criar estado agregado visual novo para o
  pai.
- O cursor não se move ao pressionar Espaço. Mover o cursor não altera a
  seleção. Trocar foco ou página também não altera a seleção.
- A seleção persiste entre páginas. Reconciliação só remove IDs inexistentes
  ou que deixaram de ser selecionáveis ou navegáveis, preservando a ordem
  lógica, quando a autoridade vigente exigir reconciliação após atualização de
  dados ou antes da operação consumidora.
- Não há execução, confirmação, cancelamento, persistência, prévia ou ação
  posterior à seleção neste handoff. Enter não recebe semântica nova.

### 2.3 Espaço e chips

- Em `selecao_multinivel`, Espaço usa a semântica própria de seleção acima e
  não reutiliza a semântica de `arvore_colapsavel`.
- O chip aplicável é o chip de seleção existente `[␣] Selecionar`, com a regra
  de ativo/inativo vigente. Para um pai com descendente selecionável, o chip
  deve permanecer acionável porque Espaço possui o alcance recursivo fechado
  nesta seção; para folha não selecionável ou pai sem descendente selecionável,
  permanece visível e inativo conforme a apresentação vigente.
- Essa regra de chip vale somente para configurações válidas. Não se define
  chip ativo, Espaço recursivo ou qualquer comportamento funcional para pai não
  selecionável com descendente selecionável.
- A apresentação da seleção usa exclusivamente `tg` com os símbolos já
  existentes `●`/`○` (ou os valores equivalentes do estilo) e deixa vazio o
  espaço de itens não selecionáveis. `ec` e `tg` são estados distintos.
- O `tg` do pai usa os mesmos símbolos e representa o mesmo estado binário de
  seleção. Não é contador, estado agregado novo, estado parcial ou seleção
  independente desconectada dos filhos.
- Não exibir `[␣] Expandir` nem `[␣] Recolher` nesta política. Esses chips
  pertencem somente ao contexto de `arvore_colapsavel`.
- `[?] Ajuda` é obrigatório, sempre ativo, permanece em todos os estados,
  páginas e focos e é o último chip. A largura insuficiente continua sendo
  `erro_layout`; Ajuda não é omitida, truncada ou reordenada.
- `[✥]` continua sendo apenas o indicador de disponibilidade das setas. Sua
  existência considera os itens navegáveis da página atual quando houver
  paginação, conforme a regra vigente.
- Se a fixture declarar `politica_paginacao: com`, `[PgUp][PgDn] Páginas`
  conserva a notação e o estado vigentes. `PageUp` é exclusivamente página
  anterior, `PageDown` é exclusivamente próxima página; setas não paginam.

### 2.4 Preservações operacionais

- A paginação continua universal, limitada e acionada somente por
  `PageUp`/`PageDown`, com `[PgUp][PgDn] Páginas`; a política de paginação é
  aplicada antes de `[␣] Selecionar` e de qualquer demonstração de seleção.
- A página pode exibir múltiplos itens, a seleção permanece entre páginas e o
  estado dos controles é calculado para o console focalizado.
- `[✥] Navegar` segue a navegabilidade e a quantidade de itens navegáveis da
  página corrente; não recebe posição global nova nem ordenação global nova.
- `[?] Ajuda` permanece por último, sempre ativo e sem redesign. `[Esc]
  Limpar` preserva sua semântica vigente quando há seleção ativa.
- Enter permanece sem nova semântica neste handoff.
- H-0053 permanece sem seleção e sem `tg`: cursor, navegação, `[✥] Navegar`,
  Expandir/Recolher e Espaço para abrir/fechar continuam preservados.

## 3. Relação com hierarquia e apresentação

`selecao_multinivel` é uma política de navegação/seleção, não uma nova
apresentação. O conteúdo externo continua declarando sua semântica e a
apresentação `hierarquia` existente continua responsável por designadores,
recuos, colunas e linhas. A implementação deve reutilizar a mesma projeção
lógica para navegação, mapa físico e renderização dos estados `ec`/`tg`.

Não reconciliar `modo normal` com `modo não verboso` e não renomear ou
reconciliar `hierarquia_indentada` com `hierarquia`. Não introduzir `Pai:
filho_ativo`, promoção visual, nova quebra, nova distribuição geométrica ou
nova linguagem visual de seleção.

No corpo do console, ao mover o cursor, somente `ec` muda; ao
selecionar/desselecionar, somente os marcadores de inclusão dos IDs afetados
mudam. Essas invariantes do corpo do console não impedem a recomputação dos
chips vigentes quando o estado corrente mudar: `[␣] Selecionar` deve refletir a
selecionabilidade e a acionabilidade do item corrente. `[Esc] Limpar` permanece
disponível e conserva a semântica transversal vigente quando houver seleção
ativa. Ao redimensionar ou mudar o modo, preservar o item lógico corrente e
recalcular a geometria; não limpar a seleção. Ao trocar de página, reposicionar
o cursor conforme a autoridade de paginação e preservar a seleção. Enter
continua sem semântica nova; não há execução, confirmação ou ação consumidora.

## 4. Arquivos e diretórios autorizados para implementação futura

Somente os caminhos abaixo ficam autorizados para a implementação de H-0054,
testes e demonstração:

| Caminho | Uso autorizado |
|---|---|
| `tela/navegacao.py` | Resolver elegibilidade, sequência única multinível, cursor, setas, foco e despacho de Espaço, preservando as ramas de `nivel_unico` e `arvore_colapsavel`. |
| `tela/selecao.py` | Materializar o conjunto de IDs, toggle de folha, alcance recursivo de pai e reconciliação já contratada. |
| `tela/renderizador.py` | Integrar estado de seleção/cursor ao pipeline existente de renderização e aos chips, sem criar símbolos ou política visual. |
| `tela/renderizacao/console.py` | Produzir mapa físico e integração do console multinível com a projeção única, sem alterar o caminho sem seleção da árvore. |
| `tela/renderizacao/conteudo_externo.py` | Renderizar `ec`/`tg` na hierarquia existente e preservar a distinção entre nó lógico e linha física. |
| `demo/demo.py` | Associar o cenário H-0054 ao conteúdo externo, transportar estado runtime, despachar teclas e manter a demonstração TTY real. |
| `tela/teste_navegacao.py` | Testes unitários focais de política, cursor, percurso, Espaço, independência da seleção e regressões de H-0052/H-0053. |
| `demo/teste_demo_console.py` | Testes integrados de carregamento separado, renderização, chips, seleção recursiva, paginação e ponto de entrada real. |
| `config/telas/demo/h0054_selecao_multinivel.json` | Nova fixture estrutural própria de H-0054. |
| `config/telas/demo/h0054_selecao_multinivel_conteudo.json` | Novo documento externo próprio de H-0054. |
| `docs/relatorios/IMP-0054-selecao-multinivel.md` | Criar o relatório obrigatório da implementação futura de H-0054. |

`demo/demo.py` deve acrescentar somente a associação nominal do novo cenário
ao documento externo e o que for diretamente necessário ao ciclo de
seleção/demonstração. Não criar catálogo genérico novo.

A autorização de `docs/relatorios/IMP-0054-selecao-multinivel.md` vale somente
para a criação do novo relatório obrigatório da futura etapa `IMPLEMENTAR`.
Ela não autoriza alteração de outros arquivos em `docs/relatorios/`.

## 5. Arquivos preservados

Preservar sem alteração:

- `docs/adr/ADR-0042-navegacao-multinivel-do-console.md`;
- `docs/adr/ADR-0041-paginacao-universal-por-pageup-e-pagedown.md`;
- `docs/adr/ADR-0043-ajuda-universal-e-chip-contextual-de-expandir-recolher.md`;
- `docs/contratos/contrato_console.md`;
- `docs/contratos/contrato_barra_de_menus.md`;
- `docs/contratos/contrato_chip.md`;
- `docs/nomenclatura/32_CONSOLE.md`;
- `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md`;
- `docs/backlog.md`;
- `config/telas/demo/h0053_arvore_colapsavel.json`;
- `config/telas/demo/h0053_arvore_colapsavel_conteudo.json`.

Também preservar qualquer caminho não listado na seção 4, inclusive outros
cenários, outros módulos de `tela/`, outros testes, relatórios históricos,
handoffs, contratos, ADRs e nomenclaturas. A criação do relatório autorizado
acima não altera essa preservação.

## 6. Configuração e fixtures

Criar as duas fixtures próprias de H-0054, seguindo o envelope estrutural e o
documento externo já usados pela demonstração de H-0053, sem copiar sua
política:

- `h0054_selecao_multinivel.json`: console focalizável com
  `politica_navegacao.navegavel: true`, `politica_navegacao.tipo:
  selecao_multinivel`, `politica_selecao: multipla`, paginação declarada
  somente se a demonstração usar a autoridade existente, e barra com `[Esc]`,
  `[✥]` condicional, `[PgUp][PgDn]` quando aplicável, `[␣] Selecionar` e
  `[?] Ajuda` por último.
- `h0054_selecao_multinivel_conteudo.json`: conteúdo `multinivel` com
  apresentação `hierarquia`, profundidade de pelo menos três níveis, IDs
  estáveis, folhas selecionáveis, ao menos um descendente não selecionável e
  pais com descendentes selecionáveis suficientes para demonstrar inclusão e
  remoção recursivas. Os textos devem caber em uma linha no cenário nominal;
  multilinha dedicada permanece fora do escopo de ITEM-0025.

A estrutura demonstrativa deve conter pelo menos três pais selecionáveis de
nível 1 e, no mínimo, o seguinte ramo nominal:

```text
1. Pai nível 1 selecionável
   1.1 Pai nível 2 selecionável
       1.1.1 Folha selecionável
       1.1.2 Folha selecionável
   1.2 Pai nível 2 selecionável
       1.2.1 Folha selecionável
       1.2.2 Folha selecionável
```

`1.`, `1.1`, `1.2` e todas as folhas acima são selecionáveis e exibem `tg`.
O segundo pai de nível 1 deve ser `2.`, selecionável e com `tg`, contendo pelo
menos um filho selecionável e, no mesmo ramo, um item explicitamente não
selecionável, sem `tg`. Esse item não selecionável permanece fora da seleção,
não possui descendentes selecionáveis e não interfere na unanimidade calculada
somente entre filhos selecionáveis. O terceiro pai de nível 1 deve fornecer
ramo adicional com diversidade de níveis e conteúdo suficiente para paginação
nominal. A fixture pode conter itens além desses mínimos, mas deve manter
múltiplos itens por página, pelo menos duas páginas quando a paginação estiver
declarada e IDs estáveis entre páginas.

Os campos de selecionabilidade devem usar somente a representação de item/nó
já aceita pelo modelo existente; não criar chave, enum ou schema específico de
H-0054. A fixture deve conter itens suficientes para que, se a paginação for
declarada, existam pelo menos duas páginas em uma execução nominal e a seleção
possa ser marcada em uma página e observada em outra.

## 7. Entrada, fixtures, temporários e saídas

| Categoria | Tratamento de H-0054 |
|---|---|
| Entrada real | `python demo/demo.py h0054_selecao_multinivel` em TTY real; Tab/Shift+Tab, setas, Espaço, `?` e, quando declarado, PageUp/PageDown. |
| Fixture | Os dois arquivos `config/telas/demo/h0054_selecao_multinivel*`; não reutilizar nem alterar H-0053. |
| Temporários | `NAO_APLICAVEL`; H-0054 não cria subprocesso nem diretório temporário. |
| Saída persistente | `NAO_APLICAVEL`; seleção é runtime e é descartada ao sair/recarregar. |
| Saída de teste | `NAO_APLICAVEL`; testes não devem gravar relatório, snapshot ou quadro persistente. |

Política de limpeza: não apagar arquivos de usuário, não limpar diretórios
amplos e não remover estado fora da sessão. O runtime de seleção deve ser
descartado ao encerrar/recarregar conforme a autoridade. Fixtures H-0054 são
propriedade exclusiva deste handoff; não sobrescrever H-0053. Qualquer
sobrescrita de um arquivo H-0054 já existente deve ser explícita e limitada ao
mesmo caminho, preservando alterações não relacionadas.

## 8. Testes automatizados focais e regressivos

Adicionar testes apenas nos arquivos autorizados:

1. Todo pai com descendente selecionável é selecionável; todo ancestral
   estrutural desse descendente, até a raiz, também é selecionável.
2. A regra estrutural vale em profundidade arbitrária e não possui exceções
   por nível.
3. A raiz selecionável possui `tg` e estado binário.
4. Todo pai intermediário selecionável possui `tg` e estado binário.
5. Toda folha selecionável possui `tg` e estado binário.
6. Item não selecionável não possui estado nem `tg`, não entra no conjunto
   selecionado e não participa da unanimidade.
7. Em configuração válida, item não selecionável não possui descendente
   selecionável; sua subárvore é integralmente não selecionável.
8. Pai não selecionável com descendente selecionável é configuração inválida
   e incoerente: não é comportamento funcional suportado e não recebe teste,
   chip ou requisito de propagação.
9. Selecionar um pai válido marca todos os seus descendentes selecionáveis em
   profundidade arbitrária e reconcilia os pais derivados.
10. O item não selecionável do ramo `2.` não é marcado pela propagação
    descendente nem pela reconciliação ascendente.
11. O item não selecionável do ramo `2.` não impede a unanimidade entre os
    filhos selecionáveis.
12. A seleção manual completa dos filhos selecionáveis imediatos marca os
    pais e, quando aplicável, os ancestrais até a raiz.
13. Desselecionar um filho desmarca os ancestrais afetados e preserva os ramos
    irmãos independentes.
14. A regra mantém estado binário, ausência de estado parcial, topologia única,
    independência entre foco/cursor/seleção, toggle manual de folhas e
    reconciliação ascendente/descendente.
15. A paginação H-0054 permanece válida: múltiplos itens por página,
    PageUp/PageDown como únicas entradas, `[PgUp][PgDn] Páginas`, seleção entre
    páginas, `[✥] Navegar`, `[Esc] Limpar`, `[?] Ajuda` por último e Enter sem
    nova semântica.
16. H-0053 continua sem seleção: Espaço em sua fixture continua apenas
    expandindo/recolhendo, sem seleção e sem `tg`.

Também devem permanecer cobertos o carregamento separado das duas fixtures
H-0054, a navegação por níveis em uma única topologia, a ausência de chip
contextual de árvore e a independência do cursor ao pressionar Espaço.

Não transformar estes testes em QA geral do console, da apresentação, da
paginação ou de execução de ações.

## 9. Demonstração reproduzível e validação manual

Executar em TTY real:

```text
python demo/demo.py h0054_selecao_multinivel
```

Em uma sessão nominal, a demonstração deve cobrir os cenários abaixo.

#### Cenário A — seleção descendente

Com nada selecionado:

1. posicionar o cursor em `1.`;
2. pressionar Espaço;
3. confirmar que as folhas abaixo de `1.1` e `1.2` estão selecionadas,
   `1.1` e `1.2` estão marcados e `1.` está marcado.

#### Cenário B — construção ascendente manual

Começando sem seleção:

1. selecionar `1.1.1`;
2. confirmar que `1.1` ainda não está marcado;
3. selecionar `1.1.2`;
4. confirmar que `1.1` passa a marcado;
5. selecionar todas as folhas de `1.2`;
6. confirmar que `1.2` passa a marcado;
7. confirmar que `1.` passa a marcado automaticamente.

#### Cenário C — desseleção propagada

Partindo do ramo `1.` completamente selecionado:

1. desmarcar uma única folha de `1.1`;
2. confirmar que essa folha fica desmarcada;
3. confirmar que `1.1` fica desmarcado;
4. confirmar que `1.` fica desmarcado;
5. confirmar que `1.2` e suas folhas permanecem selecionados.

#### Cenário D — item não selecionável no ramo `2.`

No ramo `2.`, com `2.` e o filho selecionável válidos:

1. confirmar que `2.` possui `tg` e que o filho selecionável possui `tg`;
2. confirmar que o item interno explicitamente não selecionável não possui
   `tg`, não possui descendente selecionável e permanece fora da seleção;
3. pressionar Espaço em `2.` e confirmar que somente os descendentes
   selecionáveis são marcados;
4. confirmar que o item não selecionável permanece inalterado e não impede a
   unanimidade de `2.` calculada entre seus filhos selecionáveis.

Em todos os cenários, preservar console focalizado, cursor distinguível,
`[✥] Navegar` conforme a página, múltiplos itens por página, seleção entre
páginas, `[PgUp][PgDn] Páginas`, `[Esc] Limpar`, `[?] Ajuda` por último e Enter
sem nova semântica. A validação interativa em TTY é responsabilidade posterior
do responsável; este handoff não a declara aprovada.


## 10. Critérios de aceite

O handoff considera a capacidade conforme somente quando:

- todo descendente selecionável implica que o nó e todos os seus ancestrais
  estruturais até a raiz sejam selecionáveis;
- toda raiz e todo pai intermediário com seleção abaixo possuem estado binário
  e `tg`;
- pai não selecionável com descendente selecionável não aparece em fixture
  válida e não possui requisito funcional neste handoff;
- item não selecionável permanece sem estado e sem `tg`, fora do conjunto
  selecionado e da unanimidade, e sua subárvore não introduz selecionáveis;
- todo item selecionável, em qualquer nível, apresenta estado binário `tg`,
  inclusive raízes, pais intermediários e folhas;
- o estado de cada pai coincide sempre com a unanimidade dos filhos
  selecionáveis imediatos: todos marcados marcam o pai e qualquer um
  desmarcado desmarca o pai;
- não existe situação estável em que todos os filhos selecionáveis estejam
  marcados e o pai permaneça desmarcado;
- não existe situação estável em que algum filho selecionável esteja
  desmarcado e o pai permaneça marcado;
- a reconciliação vale recursivamente de baixo para cima pelos ancestrais;
- Espaço em pai continua produzindo seleção/desseleção descendente em
  profundidade arbitrária e os toggles parentais ficam coerentes após a
  propagação;
- itens não selecionáveis não possuem `tg`, permanecem sem alteração e são
  ignorados no cálculo de unanimidade;
- o segundo ramo é o caso negativo válido: `2.` é pai selecionável com `tg`,
  possui filho selecionável e item interno não selecionável sem `tg`;
- não há estado parcial, indeterminado, contador, estado agregado novo ou
  seleção independente desconectada dos filhos;
- foco, cursor e seleção continuam independentes, H-0053 permanece sem
  seleção e Enter não recebe semântica nova;
- a fixture contém três pais de nível 1, dois pais de nível 2 no primeiro
  ramo com múltiplas folhas, outro ramo com não selecionável e terceiro ramo
  suficiente para diversidade e paginação;
- a demonstração cobre os cenários descendente, ascendente, desseleção e não
  selecionável, preservando os ramos irmãos não afetados;
- múltiplos itens por página, paginação universal, `[✥] Navegar` conforme
  navegabilidade, `[PgUp][PgDn] Páginas`, seleção entre páginas, `[Esc]
  Limpar`, `[?] Ajuda` por último e demais correções H-0054 permanecem;
- nenhuma política nova é criada para ordenação global da barra, posição
  global de `[✥]`, PageUp/PageDown, Enter, H-0055 ou ITEM-0025.

### 10.1 Deferimentos

Não tratar neste patch:

- ordenação global dos itens canônicos da barra;
- posição global de `[✥]`;
- algoritmo futuro que preserve ordem canônica independentemente da declaração;
- separação de PageUp/PageDown em chips próprios;
- H-0055 (`dois_niveis_por_foco`);
- ITEM-0025;
- atualização do backlog sobre paginação em navegação colapsável multinível.

## 11. Relatório esperado, obrigação transitória e bloqueios

O caminho nominal do relatório de implementação, a ser produzido em etapa
posterior, é:

`docs/relatorios/IMP-0054-selecao-multinivel.md`

### 11.1 Obrigação executável do patch seguinte

O próximo patch da implementação deve reconciliar ou remover o suporte
transitório específico a:

```text
pai não selecionável + descendente selecionável
```

Esse suporte ficou obsoleto pela mudança de decisão. A obrigação é remover ou
reconciliar esse caminho sem alterar o comportamento das configurações válidas
e sem prescrever arquitetura ou um novo mecanismo de erro/validação.

Se a implementação exigir arquivo fora da seção 4, deve parar antes de editar,
registrar o caminho exato, a responsabilidade e o motivo técnico no retorno ao
gerente, e solicitar autorização focal. Não ampliar leitura ou criar caminho
por proximidade temática.

Bloqueios objetivos:

- configuração sem `politica_navegacao` objeto ou sem conteúdo hierárquico
  válido;
- IDs ausentes ou duplicados que impeçam cursor ou conjunto de seleção estável;
- impossibilidade de representar selecionabilidade de folhas/pais com a
  configuração já existente, sem criar schema novo;
- incapacidade de usar a mesma projeção lógica para cursor, mapa físico e
  renderização;
- tentativa de atribuir seleção a `arvore_colapsavel`, de usar Espaço para
  duas semânticas no mesmo estado, ou de transferir paginação para setas;
- necessidade de modificar autoridade documental, H-0053, H-0055, ITEM-0025
  ou qualquer caminho não autorizado.

## 12. Escopo negativo

É proibido neste handoff:

- implementar `dois_niveis_por_foco` ou qualquer parte de H-0055;
- integrar `arvore_colapsavel` com multiline e paginação de ITEM-0025;
- alterar a semântica, fixture ou chips de `arvore_colapsavel` de H-0053;
- selecionar por Espaço dentro de `arvore_colapsavel`;
- redefinir PageUp/PageDown, criar paginação nova ou permitir paginação por
  setas, `<`, `>`, `,` ou `.`;
- criar política nova de apresentação multinível, geometria, foco ou
  distribuição;
- reconciliar `modo normal`/`modo não verboso` ou
  `hierarquia_indentada`/`hierarquia`;
- criar `Pai: filho_ativo`, promoção visual, nova linguagem de seleção,
  Enter, execução, confirmação, cancelamento, persistência ou prévia;
- refatorar código sem necessidade direta para `selecao_multinivel`;
- alterar ADRs, contratos, nomenclaturas, backlog, relatórios históricos,
  outros handoffs, stage, commit ou push.
