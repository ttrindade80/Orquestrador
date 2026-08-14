# ADR-0046 — Alteração e aplicação do estilo global em runtime

```yaml
id: ADR-0046
titulo: Alteração e aplicação do estilo global em runtime
status: ADR_APPROVED
item: ITEM-0010
item_titulo: Tela de escolha do estilo global
data: 2026-08-12
```

## Contexto

O `ITEM-0010` requer uma funcionalidade global aberta por `F4` para escolher
presets de aparência, demonstrar o resultado e aplicá-lo durante a execução.
O modelo vigente materializa `config/estilo.json` uma única vez e trata o
objeto de estilo resolvido como imutável durante toda a sessão. Esse modelo
impede a aplicação controlada de uma configuração persistida sem reiniciar a
execução.

O estilo continua sendo universal: não há escolha persistente por tela e
nenhuma classe ou renderer pode possuir símbolos, caracteres ou cores
hardcoded. A mudança desta ADR é de ciclo de vida e de interação, não de
propriedade da aparência. A distinção entre configuração concreta, estado de
runtime, candidato de edição e override temporário precisa permanecer
explícita.

## Decisão

Será criada uma funcionalidade global de escolha e aplicação de estilo, aberta
por `F4`, com quatro categorias expostas, edição acumulável, demonstração
integrada e confirmação pelo pop-up modal genérico vigente.

### 1. Entrada e limites da funcionalidade

1. `F4` abre a funcionalidade global de escolha de estilo.
2. F1/Ajuda e F11/tela cheia permanecem trabalhos futuros e não são alterados
   por esta ADR.
3. A primeira versão expõe somente estas categorias estruturais:
   `borda`, `chip`, `indicadores.selecionado` e `indicadores.incluido`.
4. `tiling`, `cor_inativo`, `cor_alerta` e `indicadores.concluido` ficam fora
   da primeira versão. Não se cria, por consequência, tela ou fluxo de
   edição para esses campos.

As quatro categorias são conhecimento estrutural da funcionalidade. Esse
conhecimento não se estende aos nomes ou valores dos presets concretos.

### 2. Origem das opções e materialização das amostras

1. Para cada categoria exposta, as opções são obtidas dinamicamente do mapa
   `presets` correspondente em `config/estilo.json`.
2. A escolha inicial de cada categoria é a opção indicada por seu
   `preset_default`, depois de a configuração ser validada e materializada.
3. Nomes de presets, símbolos, caracteres, delimitadores e valores de
   aparência não são duplicados hardcoded na tela nem no renderer da tela de
   estilos.
4. Cada filho da navegação apresenta seu nome e uma amostra derivada do
   próprio preset:
   - `borda`: miniatura de três linhas, suficiente para evidenciar cantos,
     linhas horizontais e laterais;
   - `chip`: amostra compacta que consome o próprio preset;
   - `indicadores.selecionado`: símbolo materializado do preset;
   - `indicadores.incluido`: par `on`/`off` materializado.
5. A amostra serve para comparação rápida e não substitui a demonstração
   integrada do candidato.

Uma opção inexistente, um catálogo inválido ou uma materialização incompleta
continua sendo falha fechada segundo o contrato de estilo; esta ADR não cria
fallback para preset ou valor concreto.

### 3. Navegação e escolha

A tela usa a política vigente `dois_niveis_por_foco`, sem redesenhá-la:

- pais são as quatro categorias expostas;
- filhos são as entradas dos respectivos mapas `presets`;
- cada pai mantém exatamente um filho escolhido;
- as setas movem o cursor de acordo com o contrato vigente;
- `Espaço` transfere a escolha exclusiva para o filho corrente;
- mover o cursor, por si só, não altera a escolha mantida pelo pai.

A escolha exclusiva por pai é distinta da seleção única do console. A tela não
cria uma política de navegação concorrente, não acrescenta nível de
hierarquia, não muda a topologia dos toróides e não altera a semântica
vigente de `Esc` dentro dessa política.

### 4. Camadas de estado

O fluxo deve conservar quatro conceitos separados:

| Camada | Conteúdo e responsabilidade | Pode alterar o estilo global vigente? |
|---|---|---:|
| Configuração persistida | `config/estilo.json`, incluindo catálogos e `preset_default`; é a última configuração persistida conhecida pelo fluxo | Não, por si só |
| Materialização de runtime | Objeto resolvido consumido pela execução corrente | É o estilo global vigente quando publicado pelo fluxo de aplicação |
| Candidato de edição | Estado separado, derivado da configuração persistida, com alterações acumuladas nas categorias expostas | Não |
| Override de demonstração | Visão local derivada do candidato, aplicada à demonstração e ao pop-up daquela tentativa | Não |

No início da visita à tela, o candidato é formado a partir da última
configuração persistida e suas escolhas correntes vêm dos `preset_default`.
Enquanto a tela está em edição, alterações de várias categorias acumulam-se
somente no candidato. O estilo global vigente e a configuração persistida não
são modificados por cursor, `Espaço` ou qualquer outra operação de edição.

O candidato é comparado com a última configuração persistida, e não somente
com o objeto de runtime ou com uma escolha visual intermediária. A ação
`Enter/Aplicar` fica ativa apenas quando essa comparação encontra diferença.
Quando não há diferença, a ação permanece inativa e não abre a demonstração.

### 5. Demonstração integrada

Quando `Enter/Aplicar` estiver ativo, ele abre uma tela de demonstração que
usa o candidato como override local. A demonstração deve incluir uma
composição representativa com:

- Cabeçalho;
- Console;
- Dashboard;
- Barra de Menus com variedade suficiente de chips e estados para tornar
  visíveis os efeitos das categorias expostas.

O override local deve alcançar os consumidores visuais dessa demonstração,
mas não é publicado como estilo global. O estilo global vigente da execução
permanece inalterado enquanto a demonstração estiver aberta. A demonstração
deve evidenciar o efeito integrado do candidato; não basta listar as opções
ou exibir somente as miniaturas da tela de seleção.

### 6. Confirmação pelo pop-up

Sobre a demonstração abre-se um pop-up pequeno de confirmação, preservando o
máximo possível da tela subjacente visível. O pop-up:

1. reutiliza o sistema genérico de pop-up vigente;
2. apresenta conteúdo textual que pergunta se o estilo demonstrado deve ser
   aplicado;
3. também é renderizado sob o override local do candidato;
4. devolve somente `CONFIRMADO` ou `ABORTADO`, conforme o contrato do pop-up;
5. não executa persistência nem troca o estilo global;
6. entrega a decisão ao chamador, a quem pertence a lógica de negócio.

Esta ADR não fixa literal específico para a pergunta nem para os rótulos dos
chips quando o contrato aplicável não exigir literalidade. Não se cria um
mecanismo modal novo, uma quarta região da tela ou uma semântica de negócio
embutida no pop-up.

### 7. Transições do fluxo

As transições normativas são:

| Estado | Evento | Próximo estado | Efeito obrigatório |
|---|---|---|---|
| Seleção/edição | `F4` | Seleção/edição | Abre a funcionalidade com candidato derivado da última configuração persistida |
| Seleção/edição | setas | Seleção/edição | Move somente o cursor conforme `dois_niveis_por_foco` |
| Seleção/edição | `Espaço` | Seleção/edição | Transfere a escolha exclusiva do pai para o filho corrente e atualiza o candidato |
| Seleção/edição | `Enter/Aplicar` inativo | Seleção/edição | Nenhum efeito de persistência, demonstração ou runtime |
| Seleção/edição | `Enter/Aplicar` ativo | Demonstração + confirmação | Abre a demonstração com override local e apresenta o pop-up sobre ela |
| Demonstração + confirmação | `ABORTADO` | Seleção/edição | Encerra a demonstração, retorna à seleção, preserva integralmente o candidato e não altera persistência nem estilo global |
| Demonstração + confirmação | `CONFIRMADO` e persistência bem-sucedida | Seleção/edição | Publica a nova materialização, retorna à seleção e equaliza candidato e baseline persistida |
| Demonstração + confirmação | falha de persistência | Seleção/edição não confirmada | Não publica o candidato; conserva-o disponível para nova tentativa ou edição e mantém a configuração persistida e o estilo global anteriores |
| Seleção/edição | saída sem aplicação | Saída | Descarta somente diferenças ainda não confirmadas e restaura logicamente a última configuração persistida |

Uma confirmação abortada não é uma restauração de configuração: ela apenas
encerra a demonstração e mantém o candidato editado. Se o usuário sair depois,
as diferenças ainda não confirmadas serão então descartadas. Qualquer
aplicação confirmada anteriormente na mesma visita já atualizou a baseline e
permanece aplicada.

### 8. Aplicação confirmada e falha de persistência

No caminho `CONFIRMADO`, o chamador deve:

1. persistir em `config/estilo.json` os `preset_default` correspondentes ao
   candidato nas quatro categorias expostas, preservando os demais valores
   fora do escopo;
2. considerar a operação de persistência bem-sucedida somente depois de a
   nova configuração estar gravada de forma completa e válida;
3. somente após esse sucesso substituir controladamente o objeto de estilo
   global materializado da execução pela materialização do candidato;
4. fazer a sessão usar imediatamente o novo estilo, sem reinício;
5. retornar à tela de seleção;
6. tornar a configuração recém-aplicada a nova baseline persistida;
7. deixar candidato e baseline equivalentes, tornando `Enter/Aplicar` inativo.

A ordem persistência → troca do estilo global é obrigatória. A operação é
fail-closed: qualquer falha de persistência impede a troca do estilo global,
não confirma a aplicação, não descarta o candidato e o mantém disponível para
nova tentativa ou edição. Não se aceita estilo parcialmente persistido ou
materialização parcialmente resolvida como sucesso.

O objeto global vigente continua sendo único em cada instante. A substituição
é controlada e atômica do ponto de vista dos consumidores: os renderers não
observam um objeto global parcialmente alterado. Candidato e override não
contam como estilos globais vigentes e não podem vazar para outras telas ou
para a execução fora da demonstração.

### 9. Saída e ausência de restauração de fábrica

Sair da tela sem uma nova aplicação confirmada descarta somente as diferenças
posteriores à última aplicação confirmada. O fluxo restaura logicamente a
última configuração persistida conhecida, que é também a baseline do fluxo.
Não há restauração de padrão de fábrica neste ciclo.

Se uma aplicação foi confirmada durante a visita, ela continua sendo a
baseline e o estilo global vigente ao sair. O cancelamento posterior de outra
tentativa não desfaz essa aplicação.

### 10. Patch normativo — composição de chips multitecla e semântica de destaque (ITEM-0010)

A validação manual final do `ITEM-0010` revelou que parte da composição
visual de chips multitecla e parte da semântica visual do preset de destaque
ainda não estavam normativamente fechadas de forma suficiente. Consulta focal
a `docs/contratos/contrato_chip.md` confirmou que esse contrato não decide
composição multitecla, separador `/`, delimitadores externos vs. por tecla,
nem coloração assimétrica lateral. Não existindo autoridade inferior que
substitua a necessidade de fechamento normativo, esta ADR fecha as decisões
abaixo.

**DEC-ITEM0010-CHIP-01 — composição multitecla uniforme.** Para qualquer ação
representada por duas ou mais teclas: a ação é uma única unidade visual de
chip; as teclas são separadas pelo caractere `/`; os delimitadores visuais do
preset aparecem somente nas extremidades externas da unidade; não há
delimitador completo independente por tecla. Esta decisão não redefine os
símbolos concretos dos presets vigentes nem escolhe novo schema ou renderer;
os exemplos abaixo usam o catálogo já existente. Delimitadores preservados
explicitamente: Curva, `╭` à esquerda e `╮` à direita; Ornamental, `❲` à
esquerda e `❳` à direita. Curva e Ornamental permanecem presets distintos;
não há equivalência gráfica entre eles. Exemplos normativos de forma:
Colchete `[PgUp/PgDn]`, Curva `╭PgUp/PgDn╮`, Ornamental `❲PgUp/PgDn❳`, Traço
`-PgUp/PgDn-`. Chips de uma única tecla permanecem com o comportamento
vigente. A descrição textual da ação permanece fora da unidade visual do
chip. Esta decisão substitui, para composição multitecla, o fechamento
anterior de `H-0070` que preservava concatenação individual por tecla (por
exemplo, `[PgUp][PgDn]` ou equivalente); a partir desta ADR, a forma
normativa é a unidade única aqui descrita.

**Esclarecimento documental sobre a composição multitecla.** Notações
históricas ou documentais como `[PgUp][PgDn]` podem continuar aparecendo
somente como identificador das teclas/controles quando necessário. A
representação física renderizada de uma única ação multitecla é obrigatoriamente
uma única unidade visual com `/`, portanto `[PgUp/PgDn]` para o preset de
colchetes. Documentos posteriores não devem tratar `[PgUp][PgDn] Páginas`
como forma visual canônica vigente.

**DEC-ITEM0010-CHIP-02 — preset Ponto.** No preset Ponto, o delimitador
visual esquerdo é um espaço e o delimitador visual direito é um ponto; em
ação multitecla aplica-se a mesma unidade única com `/`. Exemplo normativo:
` PgUp/PgDn.` — um espaço à esquerda, conteúdo `PgUp/PgDn` e um único ponto à
direita.

**DEC-ITEM0010-CHIP-03 — presets de destaque e cor.** Presets de
destaque/cor seguem a mesma regra de unidade visual multitecla: uma ação;
teclas separadas por `/`; espaçamento lateral pertencente à composição
visual do chip. O estilo deve ser aplicado à Barra de Menus real, não
somente à tela/demonstração de estilo. O estilo não pode vazar para o texto
descritivo da ação nem para o chip seguinte.

**DEC-ITEM0010-CHIP-04 — Destaque Texto.** O preset `Destaque Texto` altera
somente a cor do texto/conteúdo da unidade visual do chip. O fundo normal do
terminal é mantido em toda a unidade: há um espaço normal à esquerda, o
conteúdo com foreground na cor de destaque e um espaço normal à direita. A
representação semântica é ` PgUp/PgDn `: o espaço esquerdo, o conteúdo e o
espaço direito usam o fundo normal do terminal, e somente `PgUp/PgDn` recebe a
cor de destaque no foreground. Não existe fundo de destaque no lado direito
nem assimetria de fundo como característica desse preset.

Essa semântica não exige `cor_fundo_esquerdo` nem `cor_fundo_direito`; esses
campos, se existentes, não constituem requisito normativo para o preset
`Destaque Texto`. A aplicação documental posterior deverá reconciliar
contratos, nomenclatura, schema e configuração concreta que tenham sido
criados ou alterados exclusivamente para materializar a interpretação
anterior de fundo assimétrico. Esta ADR não decide nesta etapa quais campos
físicos serão removidos. A aplicação documental deve eliminar somente
semântica ou estrutura que não possua outra autoridade ou uso vigente.

**DEC-ITEM0010-CHIP-05 — separador `/`.** O `/` é parte normativa da
composição de ações multitecla e atua como separador canônico dessa
composição. Esta ADR não classifica o separador como novo campo de
configuração, valor de preset ou hardcoding de renderer; a localização
arquitetural/documental dessa representação será definida ao aplicar esta
ADR aos contratos/schemas afetados.

**DEC-ITEM0010-CHIP-06 — largura visual.** A composição e o alinhamento de
chips devem considerar a largura visual efetiva, desconsiderando sequências
ANSI que não ocupam células no terminal. Esta decisão é registrada apenas no
nível necessário para impedir que a aplicação do estilo altere geometria ou
alinhamento visual.

**DEC-ITEM0010-CHIP-07 — hierarquia/cursor fora deste patch.** A falha
manual referente à ordem e indentação cursor → toggle → texto não é decisão
nova deste patch: ela já decorre de autoridade vigente e deverá ser tratada
posteriormente como não conformidade de implementação. Este patch não
amplia a ADR para redesenhar navegação multinível, cursor, toggle ou
geometria hierárquica.

**Preservações obrigatórias desta correção.** As alterações de composição e
estilo do `ITEM-0010` não modificam a semântica vigente de estado
ativo/inativo. Quando um chip existente estiver funcionalmente inativo, sua
representação continua usando `cor_inativo`, inclusive nos controles Páginas
e Aplicar quando o estado funcional correspondente estiver inativo. A nova
composição visual não pode apagar, sobrepor ou neutralizar `cor_inativo`.

O `ITEM-0010` também não revoga nem substitui a estrutura vigente do console
`ec → tg → tx`; qualquer implementação afetada deve preservar essas posições
distintas. A autoridade comportamental desse tema permanece nos documentos
próprios do Console.

**Relação com achados manuais.** `MF-ITEM0010-001` é defeito de
implementação já observado; a regra futura correta de composição multitecla
passa a ser `DEC-ITEM0010-CHIP-01`. `MF-ITEM0010-002`: o núcleo de aplicação
do estilo global à Barra real já era obrigatório; `DEC-ITEM0010-CHIP-03` e
`DEC-ITEM0010-CHIP-04` fecham apenas os detalhes ainda não normativos.
`MF-ITEM0010-003` permanece defeito de implementação sob autoridade
existente e não depende deste patch normativo.

**Documentos a reconciliar na aplicação.** As decisões `DEC-ITEM0010-CHIP-01`
a `DEC-ITEM0010-CHIP-07` não escolhem desenho físico de schema ou de
renderer. A aplicação posterior desta ADR deverá reconciliar ao menos:
`docs/contratos/contrato_estilo.md`; `docs/contratos/contrato_chip.md`;
`docs/contratos/contrato_barra_de_menus.md`; e a nomenclatura de
estilo/chips, quando afetada.

## Regras anteriores substituídas

Esta ADR substitui explicitamente, para o ciclo de vida do estilo global, as
seguintes regras vigentes:

1. A regra de `docs/nomenclatura/10_ESTILO.md` §4.8 e das distinções
   correspondentes que trata o carregamento de `config/estilo.json` como
   ocorrido uma única vez e o objeto resolvido como imutável durante toda a
   sessão.
2. A regra `R-4` de `docs/contratos/contrato_estilo.md`, segundo a qual o
   schema de estilo não pode mudar enquanto uma tela está aberta e qualquer
   mudança exige reconstrução da tela.
3. A parte de `R-10` de `docs/contratos/contrato_estilo.md` que limita a
   materialização à carga inicial única por sessão.

O novo modelo é: materialização inicial a partir de `config/estilo.json`,
seguida de materializações adicionais somente em aplicações explicitamente
confirmadas e persistidas. O objeto global materializado vigente pode ser
substituído de forma controlada; candidato e override de demonstração nunca
são o estilo global vigente.

Permanecem vigentes a autoridade exclusiva de `config/estilo.json`, a
universalidade do estilo, a validação fechada, a materialização integral, a
proibição de hardcoding, a separação entre configuração e estado vivo e o
consumo de um único estilo global vigente por todos os renderers. A
demonstração é uma exceção somente como override local, explicitamente
temporário e não persistente; ela não autoriza estilos persistentes por tela.

A aplicação desta decisão em contratos e módulos de nomenclatura não faz parte
da criação desta ADR. Os handoffs futuros devem realizar essa aplicação sem
alterar a decisão aqui registrada.

## Invariantes

- `F4` é a entrada desta funcionalidade; F1 e F11 não são redefinidos.
- O conjunto de categorias expostas é exatamente o definido na seção 1.
- As opções são filhas dinâmicas dos mapas `presets`; a tela não replica
  nomes, símbolos ou delimitadores concretos.
- Cada categoria mantém exatamente uma escolha de filho.
- Movimento de cursor nunca troca uma escolha sem `Espaço`.
- Editar não persiste nem substitui o estilo global.
- O candidato é comparado à última configuração persistida.
- A demonstração e o pop-up usam override local; o estilo global permanece
  inalterado até aplicação confirmada.
- `ABORTADO` encerra a demonstração, preserva o candidato e não produz efeito
  persistente ou global.
- Persistência falha-closed: sem persistência bem-sucedida, não há troca do
  estilo global.
- Após confirmação bem-sucedida, a nova persistência, a materialização global
  e o candidato ficam logicamente alinhados.
- Sair sem aplicar descarta apenas diferenças não confirmadas; não restaura
  padrão de fábrica.

## Particionamento previsto

Esta ADR é única e governa três handoffs previstos. Eles são apenas
registrados aqui; nenhum handoff é criado por esta etapa:

- `H-0061`: carregamento, candidato, persistência e troca de estilo em
  runtime;
- `H-0062`: tela de seleção interativa dos presets;
- `H-0063`: demonstração, pop-up de confirmação e integração E2E.

## Fora de escopo

Ficam explicitamente fora desta ADR:

- tiling por tela e tecla `|`;
- F1/Ajuda e F11/tela cheia;
- mapa de F2/F3/F5;
- edição de cores configuráveis, incluindo `cor_inativo` e `cor_alerta`;
- indicador `concluido`;
- redesign de `dois_niveis_por_foco`;
- criação de sistema novo de pop-up;
- aplicação da ADR em contratos ou módulos de nomenclatura;
- criação dos handoffs previstos.

## Consequências

O estilo global pode mudar durante uma sessão sem reinício, mantendo uma
ordem de commit verificável e fail-closed. A demonstração permite avaliar a
composição real antes da persistência, e o candidato permite acumular escolhas
sem efeitos colaterais.

Em contrapartida, o runtime precisa distinguir a configuração persistida da
materialização vigente, manter um candidato separado e delimitar o override
da demonstração. A aplicação deve também assegurar que todos os consumidores
observem a substituição controlada do estilo, sem cópias locais concorrentes.

## Detalhes deliberadamente não fechados

Esta ADR não escolhe nomes de classes, funções, módulos internos, mecanismo
específico de escrita atômica, geometria exata da tela, texto literal do
pop-up, rótulos concretos dos chips, catálogo de fixtures nem nomes de presets.
Esses detalhes devem respeitar as decisões normativas acima e os contratos
vigentes aplicáveis, sem antecipar patch documental nesta etapa.

## Referências normativas

- `docs/backlog.md` — bloco `ITEM-0010`.
- `config/estilo.json`.
- `docs/nomenclatura/01_NUCLEO_COMUM.md`.
- `docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md`.
- `docs/nomenclatura/10_ESTILO.md`.
- `docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md`.
- `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`.
- `docs/nomenclatura/32_CONSOLE.md`.
- `docs/nomenclatura/35_POPUP.md`.
- `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md`.
- `docs/contratos/contrato_estilo.md`.
- `docs/contratos/contrato_barra_de_menus.md`.
- `docs/contratos/contrato_chip.md`.
- `docs/contratos/contrato_popup.md`.
- `docs/contratos/contrato_console.md`.
