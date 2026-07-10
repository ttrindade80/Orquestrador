---
name: contrato-tela-json
description: Schema e regras gerais do tela.json — declaracao configuravel de uma tela
metadata:
  type: contrato
  scope: scripts
  versao: "0.1"
  status: ativo
  rastreabilidade:
    origem_especificacao: "docs/adr/ADR-0008-modelo-configuracao-por-tela.md"
    reaproveitado_de_legado: false
---

# Contrato — `tela.json`

## 1. Objetivo

Definir o schema conceitual e as regras gerais de `tela.json`, a declaração
configurável de uma tela do novo Orquestrador.

Este contrato fecha a estrutura macro, os campos obrigatórios, a separação
entre configuração e estado de runtime, a modelagem inicial de corpo,
`console`, `dashboard`, `lancador`, `barra_de_menus`, chips, filtros,
bindings, ações, validação e pipeline de renderização.

Este contrato não implementa código, não cria JSON real de tela e não fecha
todos os contratos internos futuros, como a classe `chip` ou todos os tipos
de item de `console`.

---

## 2. Natureza do `tela.json`

`tela.json` é a declaração configurável de uma tela. Ele descreve a
configuração concreta que o renderer deve validar, resolver e renderizar.

O JSON da tela pode declarar:

- estrutura textual do `cabecalho`;
- composição do `corpo`;
- elementos do corpo;
- tiling e arranjo visual da tela;
- instâncias de `console`, `dashboard` e `lancador`;
- instância de `barra_de_menus`;
- lista de chips;
- filtros;
- bindings;
- ações registradas;
- regras de alinhamento, espaçamento, overflow, paginação e modo verboso.

`tela.json` é declarativo. Ele não é código executável e não pode carregar
lógica procedural arbitrária.

---

## 3. Estrutura macro obrigatória

Toda tela declarada por JSON deve conter obrigatoriamente:

```text
schema
id
cabecalho
corpo
barra_de_menus
```

A estrutura macro da tela permanece fixa:

```text
tela
├── cabecalho
├── corpo
└── barra_de_menus
```

O JSON configura essas regiões e suas instâncias; ele não redefine a existência
da estrutura macro.

---

## 4. `schema` e versionamento

Toda tela deve declarar a versão do schema:

```json
"schema": "tela.v1"
```

A versão serve para validação, diagnóstico e migração futura. Um renderer só
pode renderizar uma tela quando a versão declarada for conhecida e suportada.

---

## 5. Identificadores estáveis

Todo elemento referenciável deve possuir `id` estável no escopo adequado.

Exemplos de entidades que precisam de `id` quando existirem:

- tela;
- elemento de corpo;
- item de `lancador`;
- item de `console`;
- campo de `dashboard`;
- chip;
- filtro;
- origem de dados;
- ação registrada.

IDs são usados para validação, binding, testes, diagnóstico e manutenção.

---

## 6. Configuração vs estado de runtime

`tela.json` declara configuração, não estado transitório da execução.

Não devem ser armazenados no JSON como estado vivo:

- cursor atual;
- página atual;
- filtro ativo atual;
- modo verboso ligado/desligado no momento;
- seleção atual;
- item atualmente focado.

O JSON pode declarar defaults:

- filtro inicial;
- modo verboso inicial;
- página inicial;
- foco inicial.

O estado de runtime pertence à execução e é recalculado ou atualizado enquanto
a tela está aberta.

---

## 7. `cabecalho`

A seção `cabecalho` é obrigatória.

Campos mínimos:

```text
titulo
descricao
```

Os textos concretos do cabeçalho pertencem à tela declarada no JSON.
Parâmetros universais de apresentação continuam regidos pelo contrato do
`cabecalho` e/ou por configuração de tela quando a ADR-0008 for aplicada aos
contratos afetados.

---

## 8. `corpo`

A seção `corpo` é obrigatória.

Campos mínimos:

```text
tiling ou arranjo equivalente
elementos[]
```

`elementos[]` é uma lista de elementos de corpo. Cada elemento deve declarar,
no mínimo:

```text
id
tipo
```

Tipos funcionais válidos de elemento:

```text
console
dashboard
lancador
```

A taxonomia de tipos funcionais é **fechada** — extensões exigem ADR.

**Nó estrutural `grupo` (ADR-0015, 2026-07-10)**: `elementos[]` pode
conter, além de tipos funcionais, o nó estrutural `grupo`. `grupo` não é
tipo funcional — não tem borda, moldura, título, conteúdo, ação, chip,
origem de dados nem `tela_destino`. Recebe área do container pai e
redistribui entre seus filhos diretos. Declara seu próprio `arranjo` e sua
própria `distribuicao`.

**Composição hierárquica como árvore (ADR-0015)**: o corpo é modelado como
árvore de composição. `corpo.elementos[]` é o nível 1. `grupo.elementos[]`
cria o próximo nível. Profundidade máxima: 3 níveis. Estruturas com nível 4
ou superior geram erro estrutural determinístico. A forma plana de elementos
continua válida e equivale a nível 1.

**Distribuição pertence a containers (ADR-0015)**: tanto `corpo` quanto
`grupo` podem declarar `distribuicao`. A distribuição do container determina
como a área disponível é repartida entre seus filhos diretos. Containers
distintos podem ter distribuições distintas. Os modos formalizados são `igual`,
`percentual` e `fracao`; conceitos dinâmicos (mínimo, preferido, máximo)
estão registrados para ciclos futuros. Ver `contrato_composicao_corpo.md`
seções 5.7 a 5.12.

A sequência histórica registrada pela ADR-0010 foi cancelada como roteiro
ativo. A partir de H-0014, a numeração de handoffs **não usa letras**
(H-0014, H-0015, …), conforme estabelecido por H-0012/H-0013 e reafirmado
pela ADR-0011.

`console`, `lancador` e `dashboard` continuam sendo os tipos funcionais do
corpo. O posicionamento de qualquer elemento é controlado pela estrutura
declarada no `corpo` do `tela.json`, não por campo de posicionamento especial
por tipo (ADR-0010). O compositor não conhece os campos internos de cada
elemento — esses permanecem responsabilidade da instância declarada.

---

## 9. Tiling e posicionamento

`tela.json` deve poder declarar regras de tiling, arranjo e posicionamento da
tela.

A decisão de tiling e posicionamento da instância pertence ao JSON da tela,
não ao código.

Regras:

- `estilo.json` não decide composição de tela;
- `barra_de_menus` não decide composição de corpo;
- o renderer apenas aplica a declaração validada.

`estilo.json` permanece biblioteca global de aparência. `tela.json` declara a
instância de tela.

**Terminologia de arranjo (ADR-0011, 2026-07-08)**: os valores finais de
`corpo.arranjo` são `vertical` e `horizontal`. Os termos `sobreposto` e
`lado_a_lado` são aliases transicionais (`sobreposto → vertical`,
`lado_a_lado → horizontal`), aceitos para compatibilidade até migração
específica; não são terminologia final. Novos JSONs de tela devem usar
`vertical`/`horizontal`, salvo compatibilidade transicional explicitada.

**Ocupação vertical da janela (ADR-0013, 2026-07-09)**: a tela deve ocupar a
largura **e** a altura disponíveis da janela do terminal. A largura já é
tratada dinamicamente; a `altura_disponivel` passa a ser **dimensão futura**
da renderização da tela — o corpo deve preencher a área vertical disponível
entre `cabecalho` e `barra_de_menus`, com preenchimento de linhas em branco
pelo renderer quando o conteúdo declarado for menor. Esta ocupação **não**
altera a semântica de `corpo.arranjo`: `corpo.arranjo = "vertical"` é
composição, `ocupacao_vertical_terminal` é preenchimento da altura — termos
específicos distintos que não colapsam.

---

## 10. `lancador` como instância

Um elemento de corpo do tipo `lancador` é uma instância configurável por tela.

Campos mínimos sugeridos:

```text
id
tipo = lancador
titulo
itens[]
layout/regras_exibicao
```

Cada item de `lancador` deve ter no mínimo:

```text
id
chip ou tecla
texto
tela_destino
```

Regras obrigatórias:

- item de `lancador` chama uma tela destino;
- adicionar item ao `lancador` deve ser alteração declarativa no JSON;
- o código apenas percorre a lista de itens;
- `lancador` não é navegável por `[✥]`.

---

## 11. `dashboard` como instância

Um elemento de corpo do tipo `dashboard` é uma instância passiva configurável
por tela.

Definição mínima universal:

- não é navegável por `[✥]`;
- não é obrigatório;
- possui moldura própria;
- aceita posicionamento dentro do corpo conforme configuração da tela;
- não possui conteúdo universal fixo.

Campos mínimos sugeridos:

```text
id
tipo = dashboard
titulo
origem_dados
campos[]
layout/regras_exibicao
```

Cada campo de `dashboard` deve casar exibição com dados:

```text
id
rotulo
fonte
formato opcional
```

A estrutura antiga do `Info` com 8 campos, Total e 8 marcadores é apenas draft
da instância de `dashboard` da tela raiz do Orquestrador. Ela não é regra
universal da classe `dashboard`.

---

## 12. `console` como container genérico

Um elemento de corpo do tipo `console` é um container interativo e navegável
genérico.

O `console` define política geral de composição e navegação. Os itens internos
definem sua renderização específica.

Campos mínimos sugeridos:

```text
id
tipo = console
titulo
origem_dados
politica_composicao
politica_navegacao
politica_selecao
itens[] ou item_binding
layout/regras_exibicao
```

Regras:

- um `console` pode conter itens heterogêneos;
- o cursor navega por itens, não por linhas físicas;
- cada item declara se é navegável;
- cada item declara se é selecionável;
- cada item pode ou não ter ação de Enter;
- itens diferentes na mesma tela podem ter ações diferentes;
- se o item em foco não tiver ação de Enter, o chip/ação Enter fica inativo;
- se o item em foco tiver ação válida, Enter fica ativo.

---

## 13. Política geral de composição do `console`

A instância de `console` deve poder declarar uma política geral comum aos
itens.

Exemplos de campos:

```text
alinhamento_origem
fluxo
espacamento_entre_itens
overflow_normal
modo_verboso
```

Exemplo conceitual:

```text
     KEY
     NOME: valor longo do segundo item que estoura linha...
```

Cada item pode ter regra interna própria, mas o resultado renderizado deve
ser encaixado na política geral do `console`.

---

## 14. Modo verboso

Modo verboso é estado de exibição reutilizável, não variação específica de
cada tela.

Regras:

- modo normal: itens renderizam de forma compacta e seguem a política de
  overflow normal;
- modo verboso: itens podem expandir verticalmente e usar novas linhas para
  mostrar o conteúdo integral;
- o chip/tecla `[V]` alterna modo verboso quando a instância permite;
- a tela não redefine a lógica interna do modo verboso de cada tipo de item;
- cada tipo de item pode declarar como se comporta em modo normal e verboso.

---

## 15. Paginação

Paginação é consequência automática do conteúdo renderizado que não cabe na
área disponível.

Regras:

- filtro é aplicado antes da paginação;
- modo normal ou verboso afeta o tamanho dos itens renderizados;
- se o conjunto renderizado não couber, o `console` cria páginas;
- cada item pode declarar política de quebra de página.

Políticas de quebra de página previstas:

```text
evitar_quebra
permitir_quebra
permitir_quebra_somente_se_maior_que_pagina
```

Regras de quebra:

- item que evita quebra deve ser movido inteiro para a página seguinte quando
  possível;
- se o item não couber inteiro nem em página vazia, a quebra passa a ser
  permitida;
- item com quebra permitida pode atravessar páginas.

---

## 16. Navegação e seleção

A navegação deve ser permitida por item.

Campos conceituais por item:

```text
navegavel: true | false
selecionavel: true | false
acao_enter: ...
```

A política de seleção é declarada pela instância de `console`:

```text
nenhuma
unica
multipla
```

Regras:

- seleção múltipla usa toggle `[␣]`;
- seleção única não precisa toggle: o cursor define o alvo;
- Enter executa a ação do item em foco;
- item sem ação torna Enter inativo;
- item com ação torna Enter ativo;
- seleção por toggle representa seleção múltipla.

---

## 17. Filtros

Filtros são regras declarativas de redução do conjunto renderizável.

Regras:

- filtros atuam no render;
- filtros operam sobre campos existentes nos dados vinculados;
- filtros são aplicados antes da paginação;
- adicionar filtro sobre atributo já existente nos dados deve exigir alteração
  apenas no JSON da tela;
- não deve ser necessário alterar código de impressão ou renderização.

Estrutura conceitual:

```text
filtros[]
  id
  campo
  tipo
  valores/opcoes
```

Chip de filtro:

```text
chip
  acao: alternar_filtro
  filtro: <id_do_filtro>
```

---

## 18. `barra_de_menus`

A seção `barra_de_menus` é obrigatória.

Campos mínimos:

```text
chips[]
distribuicao
```

A `barra_de_menus` é uma instância declarada pela tela. Ela não decide
composição; ela apenas expõe chips declarados.

**Distribuição visual (ADR-0014, 2026-07-09)**: `barra_de_menus.distribuicao`
admite duas formas aceitas:

- **forma transitória** — string `"horizontal"`, presente nos JSONs ativos;
- **forma canônica futura** — objeto declarativo, com
  `barra_de_menus.distribuicao.modo = "horizontal_responsiva"`.

A string `"horizontal"` é **alias transitório** de
`distribuicao.modo = "horizontal_responsiva"` e significa **distribuição
horizontal responsiva** dos chips — **não** linha única fixa. O renderer deve
respeitar a distribuição declarada, dispondo os chips horizontalmente e
quebrando em multilinha de forma determinística quando não couberem em uma
linha, sem omitir, truncar ou reordenar chips para "fazer caber". A migração
dos JSONs para o formato canônico objeto é pendência de handoff futuro;
`tela.json` deve poder declarar ambas as formas.

`barra_de_menus.distribuicao` é termo específico completo, distinto de
`corpo.arranjo = "horizontal"` (arranjo do corpo, ADR-0011): são campos em
regiões distintas com semântica própria. Detalhes normativos completos
(alias transitório, estrutura canônica futura, algoritmo, ordem, âncoras,
overflow e proibições) em `contrato_barra_de_menus.md` seção 17 e na ADR-0014.

**Alteração por termo específico (ADR-0014, Parte B)**: termos ambíguos
(`vertical`, `horizontal`, `barra`, `chip`, `arranjo`) não devem ser
alterados por filtro parcial automatizado; alterações normativas e de
implementação devem atingir apenas termos específicos completos.

---

## 19. Chip como entidade declarativa

`tela.json` prepara a modelagem futura de `chip` como classe própria.

Cada chip deve poder declarar, no mínimo:

```text
id
tipo
tecla
texto
acao
regra_existencia
regra_ativo
forma_exibicao
```

Tipos conceituais de chip:

```text
canonico
especifico
filtro
alternancia
acao
```

Este contrato não fecha o contrato completo de `chip`, mas exige que chips em
`tela.json` sejam entidades declaradas, não hardcoded.

---

## 20. Ações

Ações declaradas no JSON devem ser whitelisted ou registradas. O JSON nunca
pode declarar comando arbitrário.

Proibido conceitualmente:

```json
"acao": "python script_x.py --alguma-coisa"
```

Permitido conceitualmente:

```json
"acao": {
  "tipo": "abrir_tela",
  "alvo": "selecao"
}
```

ou:

```json
"acao": {
  "tipo": "executar_acao_registrada",
  "id": "atualizar_status"
}
```

`tela.json` é declarativo, não procedural.

---

## 21. Bindings

Binding é o casamento entre declaração visual, dados e ações.

Separação conceitual:

```text
binding_dados
binding_renderizacao
binding_navegacao
binding_acao
```

Regras:

- `binding_dados` conecta origem de dados e campos;
- `binding_renderizacao` transforma dados em itens ou campos exibíveis;
- `binding_navegacao` define navegabilidade e selecionabilidade;
- `binding_acao` define o que ações como Enter ou chips fazem.

---

## 22. Pipeline de renderização

Ordem conceitual obrigatória:

```text
carregar tela.json
validar schema
resolver referências
carregar dados
aplicar bindings
aplicar filtros ativos
renderizar itens em modo normal/verboso
paginar
calcular navegação/cursor
calcular estado ativo/inativo dos chips
renderizar tela
```

Filtro vem antes da paginação.

---

## 23. Validação obrigatória

Toda tela deve ser validada antes de renderizar.

Critérios mínimos de validação:

- `schema` existe e é suportado;
- `id` da tela existe;
- `cabecalho`, `corpo` e `barra_de_menus` existem;
- todos os elementos têm `id` único no escopo adequado;
- tipos de corpo são conhecidos;
- tipos de item são conhecidos ou registrados;
- telas destino existem;
- chips não duplicam tecla na mesma barra;
- filtros referenciam campos existentes;
- ações referenciam tipos ou IDs permitidos;
- bindings referenciam origens e campos existentes;
- item navegável possui estrutura suficiente para navegação;
- item selecionável só aparece em `console` com política compatível;
- modo verboso só é ativável quando a instância permite;
- não há comandos arbitrários no JSON.

---

## 24. Erro, vazio e ausência de dados

Cada elemento deve ter política para:

- origem de dados vazia;
- origem de dados com erro;
- filtro sem resultado;
- ação indisponível;
- tela destino ausente;
- item que não cabe.

As decisões detalhadas podem ficar pendentes, mas esses estados precisam ser
declarados ou receber default contratual.

---

## 25. Hierarquia de defaults e sobrescritas

Hierarquia inicial:

```text
estilo.json global
→ defaults do tipo de componente
→ configuração da tela
→ configuração do elemento
→ configuração do item
```

`estilo.json` trata aparência global. `tela.json` trata instância de tela.

---

## 26. Limite declarativo do JSON

`tela.json` pode declarar:

- campos;
- bindings;
- filtros;
- ações registradas;
- destinos;
- layout;
- composição;
- regras de exibição.

`tela.json` não pode declarar lógica procedural arbitrária, loops, comandos
livres ou scripts não registrados.

---

## 27. Pendências derivadas

Pendências obrigatórias derivadas deste contrato:

- aplicar o contrato de `tela.json` em `docs/NOMENCLATURA.md`, quando a
  revisão ampla da ADR-0008 for executada;
- revisar `contrato_lancador.md` para instância em `tela.json`;
- revisar `dashboard` e composição para instância em `tela.json`;
- revisar `contrato_barra_de_menus.md` para lista de chips declarados;
- criar contrato próprio da classe `chip`;
- revisar `console` como container genérico;
- criar contratos/classes de itens internos de `console` conforme necessidade;
- definir registry de tipos válidos;
- definir formato real dos JSONs de tela;
- criar draft do JSON da tela raiz do Orquestrador;
- arquivar artefatos históricos/transicionais ao fechamento da Fase 0.
