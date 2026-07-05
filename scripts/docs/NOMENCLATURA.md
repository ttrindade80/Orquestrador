---
name: nomenclatura-sistema-novo
description: Glossario consolidado de termos do sistema novo, base para os contratos de estilo, composicao de corpo e barra_de_menus
metadata:
  type: nomenclatura
  scope: sistema_novo
  status: parcial
  origem_especificacao: usuario_sessao_2026-07-05
  reaproveitado_de_legado: false
---

# Nomenclatura — Sistema Novo

## Regra

Este documento e a unica fonte de nomes validos para os contratos que serao
escritos a partir dele. Nenhum contrato pode introduzir sinonimo ou renomear
termo aqui definido sem atualizar este glossario primeiro.

Nenhum termo aqui foi herdado do sistema antigo por leitura direta de codigo
ou documentacao antiga; toda definicao veio de decisao explicita do usuario
nesta sessao de trabalho.

---

## 1. Estilo (universal)

Aparencia. Nunca varia por tela ou classe. Nenhuma classe ou renderer pode
hardcodar simbolo, cor ou caractere que pertenca a esta secao — tudo vem do
schema de estilo.

### 1.1 Borda

| Campo | Funcao |
|---|---|
| `traco_superior` | caractere da linha superior |
| `traco_inferior` | caractere da linha inferior |
| `canto_superior_esquerdo` | canto superior esquerdo |
| `canto_superior_direito` | canto superior direito |
| `canto_inferior_esquerdo` | canto inferior esquerdo |
| `canto_inferior_direito` | canto inferior direito |
| `lateral` | caractere da coluna esquerda/direita |

O espaco da moldura sempre existe estruturalmente; o que muda entre estilos
de borda e so o caractere de preenchimento.

### 1.2 Chip

| Campo | Funcao |
|---|---|
| `caractere_esquerdo` | caractere de abertura do chip |
| `caractere_direito` | caractere de fechamento do chip |
| `cor_texto` | cor do texto/tecla do chip |
| `caixa_alta` | booleano — texto em maiuscula ou nao |
| `cor_fundo` | cor de fundo do chip |

### 1.3 Indicadores

| Indicador | Natureza | Simbolos |
|---|---|---|
| `concluido` | par on/off | on: `✓`, off: configuravel (default espaco) |
| `selecionado` | simbolo unico, so aparece quando aplicavel | `→` |
| `incluido` | par on/off | on: `●`, off: `○` |

Todos os simbolos acima sao default configuravel via schema, nunca fixos em
codigo.

---

## 2. Tela (estrutura base)

Toda tela do sistema tem exatamente estas tres regioes:

1. **Cabecalho**: titulo + descricao.
2. **Corpo**: estrutura variavel — pode ter mais de um objeto, sobrepostos
   ou lado a lado, dependendo do tamanho da tela e do tipo dos objetos.
   Cada objeto do corpo tem titulo e conteudo.
3. **barra_de_menus**: titulo fixo "Menu", contem os chips de acao (ver
   secao 5). Antes chamada de "menu" nesta conversa — esse nome esta
   descontinuado, o termo correto e `barra_de_menus`.

### 2.1 Tipos de objeto do corpo

- **dado**: dados propriamente ditos, incluindo saida de script/log.
- **menu**: um objeto do corpo que e, ele proprio, uma composicao de
  navegacao (nao confundir com `barra_de_menus`, que e a regiao fixa da
  tela).
- **Info**: objeto opcional do corpo — resumo/legenda dos dados exibidos.

Extensibilidade: um terceiro tipo de conteudo pode ser adicionado no futuro
seguindo o mesmo principio do estilo — schema aberto, sem exigir reescrita
do renderer, desde que a amarracao declarativa (classe declara, renderer so
executa) seja respeitada.

---

## 3. Composicao de corpo (por classe de tela)

Declarada pela classe de tela, nunca decidida pelo renderer ou pela
barra_de_menus.

| Eixo | Valores |
|---|---|
| Tipo de conteudo | `menu`, `dado` |
| Tipo de exibicao | `normal` (lista simples) / `verboso` (detalhes) — depende dos dados |
| Info | presente / ausente |
| Organizacao de multiplos corpos | 1 corpo / sobrepostos / lado a lado |
| Paginacao | com / sem |
| Colunas ajustavel | com / sem — eixo proprio, distinto de paginacao |
| Espacamento interno | universal (renderer): linha em branco entre borda e conteudo, sempre |
| Organizacao horizontal | regra minima por tipo de conteudo (menu vs dado) — ver secao 6 |

---

## 4. Mecanismos de selecao (corpo tipo `dado`)

Quatro conceitos distintos, em camadas:

| Conceito | O que e | Como se forma |
|---|---|---|
| **Cursor / selecionado** | aponta um item; `[⏎]` executa acao sobre ele | setas de navegacao, indicador `→` |
| **Grupo** | origem/categoria do dado (ex.: grupo 1, 2, 3) — atributo do proprio dado | ja existe nos dados, filtra **exibicao** via `[#]` |
| **Selecao** | conjunto **nomeado** de elementos (ex.: selecao `a`, `b`) — **cruza grupos livremente**, sem limite. Mecanismo geral: serve tanto para selecionar itens de dado quanto, futuramente, para selecionar ferramentas em um processo — o mecanismo e o mesmo, o contexto de uso e que muda | toggle (cursor + barra de espaco marca/desmarca), indicador `●`/`○`, persiste com nome |
| **Lote** | unidade de **execucao** — calculado a partir de uma selecao no momento de rodar um processo especifico, tipicamente `selecao − o que ja foi processado por aquele processo`. A mesma selecao pode gerar lotes diferentes dependendo do processo | derivado, nao e marcado manualmente |

Termo descontinuado: **"lote" nao e sinonimo de "grupo"** nem de "selecao".
Grupo e origem/escopo de exibicao. Selecao e um conjunto nomeado que cruza
grupos. Lote e o resultado, calculado por processo, a partir de uma selecao.

**Em aberto por decisao do usuario (nao e pendencia, e escolha consciente)**:
a relacao exata entre `[#]` (filtro de grupo exibido) e o toggle de selecao
— incluindo a possibilidade futura de "marcar todos os itens do grupo
filtrado" como atalho — fica para ser definida quando o caso de uso
aparecer. Nao ha decisao de coexistencia/exclusividade travada agora.

---

## 5. barra_de_menus

### 5.1 Chips canonicos e ordem fixa

```
[Esc] → [<][>] → [-][+]|n| → [⏎] → [#] → toggle_selecao → especificos → [V] → [?]
```

| Chip | Presenca | Condicao |
|---|---|---|
| `[Esc]` Sair/Voltar | sempre, primeiro | Sair só na tela raiz, Voltar nas demais |
| `[<][>]` | condicional | classe declara paginação |
| `[-][+]\|n\|` | condicional | classe declara colunas ajustável |
| `[⏎]` | sempre | executa ação sobre o item com cursor (`→`) |
| `[#]` | condicional | classe declara filtro por grupo |
| toggle_selecao | condicional | classe declara formação de seleção (ver seção 4) — símbolo vem do estilo |
| específicos | condicional | chips próprios da classe — ver seção 5.2 |
| `[V]` Verboso | condicional | classe/dados aceitam modo verboso |
| `[?]` Ajuda | sempre, último | — |

Regra estrutural: **nenhum chip canônico decide sua própria exibição** —
presença é sempre derivada de uma propriedade de composição já declarada
pela classe de tela (seção 3). A barra_de_menus é só um espelho, nunca uma
fonte de decisão.

---

### 5.2 Chips específicos — categoria formal

Três tipos possíveis, não texto livre:

| Tipo | Estrutura | Natureza |
|---|---|---|
| **Toggle** | texto, tecla, `ativo` (booleano), papel | filtro de exibição, liga/desliga |
| **Múltiplo** | texto, teclas (plural), cores (por tecla), papel | filtro de exibição, conjunto de opções (`set`), tipicamente mutuamente exclusivas entre si |
| **Aciona processo** | *(estrutura a definir)* | executa lógica sobre seleção/lote — sem precedente formal em `teste_classe_c.py`. Lógica real de execução existe em `orquestrador.py` (não `teste_orquestrador_v2.py`), mas está misturada com `print()` direto no meio do código — na extração, separar o que é *processo* (mantém) do que é *exibição* (descarta, substituído pelo renderer novo) |

---

## 6. Layout e largura

- **Largura de tela**: sempre dinâmica, calculada a partir da largura real
  do terminal — sem perfis fixos pré-definidos. Sustentável porque nenhuma
  regra de composição (colunas, quebra de texto, padding, paginação)
  depende de largura fixa.
- **Redimensionamento reativo**: o sistema reage a mudança de tamanho do
  terminal em tempo real — não lê a largura uma vez na inicialização e
  guarda; a tela se ajusta enquanto está aberta, sem precisar reiniciar.
- **Organização horizontal por tipo de conteúdo do corpo**:
  - `menu`: lista vertical numerada, sem colunas, sem paginação.
  - `dado`: colunar (modo normal, `n_col` ajustável) ou tabular (modo
    verboso, largura de coluna calculada por conteúdo, texto longo quebra
    dentro da coluna).
- **Overflow**: nunca existe scroll. Conteúdo que excede o espaço
  disponível sempre pagina. Espaço sobrando é preenchido (padding),
  nunca deixado vazio de forma desorganizada.

---

## 7. Pendências em aberto

Nenhuma pendência de design em aberto no momento.

Itens adiados intencionalmente (não são lacuna, são decisão de adiar):

- Relação entre `[#]` (filtro de grupo) e o toggle de seleção — ver
  seção 4.
- Estrutura do chip "aciona processo" — ver seção 5.2, será extraída de
  `orquestrador.py` quando o primeiro caso concreto for definido,
  separando lógica de processo de código de exibição (`print`) misturado.
