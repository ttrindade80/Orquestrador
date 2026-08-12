---
name: nomenclatura-popup
description: Terminologia proprietária do pop-up modal genérico de decisão
metadata:
  type: nomenclatura
  scope: popup
  fase_de_aplicacao: VIGENTE
  fonte_normativa: docs/adr/ADR-0044-popup-modal-generico-de-decisao.md
  contrato_relacionado: docs/contratos/contrato_popup.md
---

# Pop-up modal

## 1. Responsabilidade

Este módulo é proprietário da terminologia da capacidade de apresentação
modal sobreposta para decisões pequenas e focais. O comportamento completo
está em `docs/contratos/contrato_popup.md`; este módulo não redefine o estilo,
a tela, o corpo, o console, a barra de menus, o carregamento de dados ou a
ação de negócio.

## 2. Termos proprietários

- `pop-up`
- pop-up modal
- declaração de pop-up
- ID de declaração de pop-up
- mapa `popups`
- resolução da declaração
- instância de pop-up
- conteúdo do pop-up
- envelope de entrada do pop-up
- resultado do pop-up
- área de chips do pop-up
- marcação exclusiva do pop-up
- marcação múltipla do pop-up
- estado provisório
- compatibilidade chamador × pop-up

## 3. Definições

| Termo | Definição |
|---|---|
| `pop-up` | Apresentação modal sobreposta à tela ativa para uma decisão pequena e focal; não é uma região permanente nem um elemento da composição do corpo. |
| pop-up modal | `pop-up` enquanto a tela subjacente permanece materializada e suspensa para interação. |
| declaração de pop-up | Configuração estrutural/interativa estável registrada como uma entrada do mapa `popups`; não contém o conteúdo concreto nem o estado vivo de uma abertura. |
| ID de declaração de pop-up | Chave estável da entrada de `popups` que identifica a declaração; não é posição física e não precisa ser repetida em um campo interno `id`. |
| mapa `popups` | Campo geral do JSON estrutural da tela que reúne zero ou mais declarações por ID; é um mapa/objeto, não uma lista, e não é uma instância aberta. A propriedade do JSON estrutural permanece no módulo 02 e no contrato `tela.json`. |
| resolução da declaração | Operação runtime que localiza a declaração em `popups[ID]` antes de combinar o envelope pronto e materializar a instância; ID inexistente falha sem fallback. |
| instância de pop-up | Objeto de runtime criado para uma abertura concreta, com a declaração resolvida, envelope daquela abertura e estado vivo próprios; não modifica a declaração. |
| conteúdo do pop-up | Conteúdo pronto entregue pelo chamador para uma abertura, de tipo `texto` ou `marcacao`. |
| envelope de entrada do pop-up | Envelope discriminado por `tipo` que transporta o conteúdo pronto da abertura e rejeita campos desconhecidos. |
| resultado do pop-up | Envelope lógico devolvido ao chamador com `status: CONFIRMADO` ou `status: ABORTADO` e, somente quando aplicável, `valor`. |
| área de chips do pop-up | Área própria posterior ao conteúdo, com ordem declarada no pop-up e aparência derivada do estilo universal. |
| marcação exclusiva do pop-up | Política declarada literalmente como `marcacao: exclusiva`, com exatamente uma marcação válida e transferência por Espaço. |
| marcação múltipla do pop-up | Política declarada literalmente como `marcacao: multipla`, com zero a N marcações e alternância do item corrente por Espaço. |
| estado provisório | Cursor, marcações e demais condições vivas da interação antes da confirmação; não é configuração nem conteúdo persistido. |
| compatibilidade chamador × pop-up | Validade conjunta entre configuração, envelope recebido e contrato de resultado aceito pelo chamador antes da materialização. |

## 4. Fronteiras obrigatórias

As seguintes distinções são normativas:

| Par | Distinção |
|---|---|
| `pop-up` × `tela` | O pop-up é apresentação sobreposta e não substitui a tela ativa. |
| `pop-up` × `console` | O pop-up não é container de console, mesmo quando apresenta lista navegável. |
| `pop-up` × elemento funcional | O pop-up não integra a taxonomia de elementos funcionais do corpo. |
| `pop-up` × região permanente | O pop-up é transitório e sobreposto; não cria uma quarta região permanente. |
| mapa `popups` × instância aberta | O mapa é configuração estrutural estável; a instância é um objeto runtime de uma abertura concreta. |
| chave de `popups` × conteúdo | A chave é o ID estável da declaração; o conteúdo chega no envelope externo da abertura. |
| declaração de pop-up × envelope de entrada | A declaração contém configuração estrutural/interativa; o envelope contém conteúdo pronto de uma abertura. |
| declaração de pop-up × estado vivo | A declaração permanece no JSON; cursor, marcações provisórias e demais condições vivas pertencem à instância runtime. |
| declaração de pop-up × instância de pop-up | A primeira é configuração reutilizável; a segunda é materialização concreta e não altera a primeira. |
| ID estrutural × posição física | O ID identifica a declaração independentemente de posição, ordem ou recomposição geométrica. |
| área de chips do pop-up × `barra_de_menus` | São áreas distintas; a primeira usa a ordem declarada no próprio pop-up e a segunda conserva a ordem canônica da tela. |
| `marcacao: exclusiva` × `seleção única` do console | A primeira mantém marcação independente do cursor; a segunda é o item sob cursor e muda quando o cursor se move. |
| envelope de entrada do pop-up × JSON estrutural da tela | O envelope é conteúdo runtime de uma abertura; o JSON estrutural declara configuração e não incorpora esse conteúdo. |
| conteúdo recebido × estado vivo da instância | Conteúdo recebido é imutável durante a abertura; estado vivo inclui cursor e marcações provisórias. |
| `ABORTADO` × seleção/lista vazia | `ABORTADO` é status de saída sem payload; lista vazia pode ser valor confirmado de `marcacao: multipla`. |

## 5. Conteúdo e geometria

O conteúdo do pop-up pode ser textual ou uma marcação navegável plana. O tipo
`texto` é uma string semântica com alinhamento `esquerda`, `centralizado` ou
`justificado` e wrapping. O tipo `marcacao` possui instrução obrigatória,
itens reais com IDs estáveis e uma linha física por item.

As formações físicas da marcação seguem `coluna → matriz → linha`. `coluna` é
preferida enquanto todos os itens couberem em uma única coluna. Se ela não
couber e houver pelo menos duas linhas físicas disponíveis, `matriz` usa o
maior número de colunas fisicamente ocupadas que caiba integralmente e
conserve pelo menos duas linhas. O preenchimento é vertical, da esquerda para
a direita, sem placeholders ou células artificiais. `linha` somente é usada
quando houver espaço para apenas uma linha física e todos os itens couberem
nela; uma linha não é matriz. Cada item permanece em uma linha física, e o vão
entre colunas da matriz e entre itens da linha é exatamente `2` espaços, tanto
no encaixe quanto na representação. Sem formação válida, usa-se o `quadro
mínimo de terminal pequeno`.

Para cada novo par de dimensões válido, a formação é recomposta de modo
reversível, preservando na mesma instância IDs, ordem lógica, cursor e
marcações provisórias. A navegação toroidal por eixo permanece a mesma; essa
topologia não transforma o pop-up em `console`.

O pop-up é centralizado na área física do corpo e usa tamanho intrínseco,
limitado por essa área. Espaçamentos verticais aceitam `0|1` e o espaçamento
horizontal aceita `1..5`. O conteúdo não recebe truncamento, reticências ou
paginação.

## 6. Entrada, retorno e produtor

O chamador entrega o conteúdo pronto e consome o resultado. O pop-up não
resolve origem de dados, produtor, loader ou carregamento, e o envelope de
entrada não pertence ao envelope multinível do console. A política de
marcação pertence à configuração e não ao envelope.

`Esc` produz `status: ABORTADO`, sem payload. Confirmação, quando declarada,
produz `status: CONFIRMADO` e valor conforme o tipo. O rótulo do chip não é
ação de negócio.

## 7. Relação com outros módulos

- `02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md`: distingue configuração, conteúdo
  recebido e runtime sem assumir a propriedade do vocabulário deste módulo.
- `10_ESTILO.md`: fornece a aparência universal reutilizada por moldura e
  chips.
- `20_TELA_CORPO_E_COMPOSICAO.md`: define a fronteira negativa entre o pop-up
  e a árvore do corpo.
- `21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`: fornece a autoridade geral de
  resize e do quadro mínimo de terminal pequeno.
- `31_BARRA_DE_MENUS_E_CHIPS.md`: distingue a área própria de chips da barra.
- `32_CONSOLE.md`: conserva `seleção única` como termo próprio do console.
- `42_DADOS_EXTERNOS_MULTINIVEL.md` e `43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md`:
  não recebem o envelope do pop-up nem sua relação com o chamador.

## 8. Relação com ADR

- ADR-0044: fecha a capacidade, suas fronteiras, os tipos de conteúdo, as
  políticas de marcação, o retorno e a separação entre configuração,
  conteúdo e runtime.
- ADR-0045: especializa o resize responsivo das formações físicas do conteúdo
  `tipo: marcacao`, sem alterar a propriedade deste módulo sobre a
  terminologia do pop-up.
