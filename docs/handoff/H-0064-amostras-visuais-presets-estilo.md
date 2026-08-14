# H-0064 — Amostras visuais dos presets na tela de Estilo

## 1. Metadata e rastreabilidade

```yaml
projeto: Orquestrador
item: ITEM-0010
adr: ADR-0046
handoff: H-0064
data_criacao: 2026-08-12
status: READY_FOR_IMPLEMENTATION
predecessor: H-0063
relacao: continuacao_funcional
historico:
  H-0061:
    estado: aprovado
    capacidade: infraestrutura_de_estilo_runtime
  H-0062:
    estado: substituido
  H-0063:
    estado: tecnicamente_aprovado
dependencias:
  - H-0061 (infraestrutura de estilo — candidato, materialização, baseline)
  - H-0063 (tela normal, quatro pais, dois_niveis_por_foco, filho corrente/escolhido)
```

H-0064 é continuação funcional de H-0063, não substituição. A tela normal, os
quatro pais, a navegação `dois_niveis_por_foco`, a Barra de Menus e a
fronteira de estado navegacional/mutação de H-0063 permanecem integralmente
vigentes. H-0062 permanece histórico/substituído e não é reaberto.

## 2. Objetivo exclusivo

Acrescentar à tela normal de Estilo entregue por H-0063 **amostras visuais
dos presets** em cada filho do segundo nível, para as quatro categorias já
expostas:

- `borda`
- `chip`
- `indicadores.selecionado`
- `indicadores.incluido`

Amostra é apresentação: permite reconhecer e comparar presets visualmente.
Amostra não é escolha, não é candidato e não é demonstração integrada. A
escolha exclusiva de filho, o filho corrente, o filho escolhido, `Espaço`,
`Esc`, resize e paginação continuam funcionando exatamente como em H-0063,
sem nova política.

## 3. Autoridade principal

- `docs/adr/ADR-0046-alteracao-aplicacao-estilo-global-runtime.md` — seção 2
  ("Origem das opções e materialização das amostras") é a autoridade
  normativa direta desta etapa; demais seções regem candidato, demonstração e
  pop-up, que ficam fora deste handoff.
- `docs/handoff/H-0063-tela-estilo-estrutura-navegacao-dois-niveis.md` —
  estrutura, navegação, fronteira de estado, arquivos autorizados e testes
  que H-0064 preserva e estende.
- `docs/contratos/contrato_estilo.md` §§3.1, 3.2, 3.3, 4 (R-2, R-6, R-7) —
  campos concretos de borda (sete), chip (cinco), `indicadores.selecionado`
  (símbolo + off) e `indicadores.incluido` (par on/off); proibição de
  hardcode; responsabilidade exclusiva do renderer na tradução de cor.
- `docs/nomenclatura/10_ESTILO.md` §§4.2–4.4 — vocabulário de presets,
  catálogo, `preset_default` e campos de runtime das mesmas categorias.
- `config/estilo.json` — lido somente como catálogo concreto atual, nunca
  alterado por este handoff.

## 4. Categorias (preservadas, sem expansão)

Mantidas exatamente as quatro categorias de H-0063:

- `borda`
- `chip`
- `indicadores.selecionado`
- `indicadores.incluido`

Continuam fora de escopo, sem tela, fluxo ou amostra: `tiling`,
`cor_inativo`, `cor_alerta`, `indicadores.concluido`.

## 5. Origem das opções e proibição de hardcode

Os filhos continuam vindo dinamicamente dos mesmos mapas `presets` já
projetados por `tela/estilo.py` (H-0063). A amostra de cada filho é derivada
dos campos do próprio preset já disponível na projeção (`PresetEstilo.dados`)
— não é buscada por um caminho novo nem duplicada em estrutura paralela.

Proibido:

- nomes de presets, símbolos, caracteres, delimitadores ou cores concretas
  hardcoded no controlador ou no renderer de Estilo;
- lista paralela de presets, mapa de amostras por nome ou switch/case sobre o
  nome do preset;
- catálogo especial de amostras fora de `config/estilo.json`.

Um preset sintético válido inserido no catálogo (via cópia temporária de
`config/estilo.json` em teste, como já praticado em H-0063) deve aparecer
como filho com amostra correspondente sem alteração enumerativa no código.

## 6. Amostra de borda (correção H0064-QA-003)

Cada preset de `borda.presets` apresenta uma **amostra compacta de borda em
uma linha**, cabendo na linha física do filho. Esta correção remove a
exigência anterior de miniatura de três linhas — incompatível com o modo não
verboso vigente na fixture de H-0063 (`politica_exibicao.verboso: false`,
item lógico igual a uma linha física, `contrato_console.md` §§5–6) — e a
substitui pela representação de uma linha abaixo.

A amostra usa exclusivamente os sete campos do próprio preset, concatenados
nesta ordem:

```text
canto_superior_esquerdo + traco_superior + canto_superior_direito
+ lateral + lateral
+ canto_inferior_esquerdo + traco_inferior + canto_inferior_direito
```

Ou representação documentalmente equivalente que preserve, em uma única
linha, os sete campos concretos, sem omitir nem duplicar a função de nenhum
campo. O objetivo é demonstrar o conjunto de glifos do preset — não
reproduzir geometricamente uma caixa real de três linhas.

Regras:

- os sete campos aparecem de forma reconhecível dentro da linha única:
  `canto_superior_esquerdo`, `canto_superior_direito`,
  `canto_inferior_esquerdo`, `canto_inferior_direito`, `traco_superior`,
  `traco_inferior`, `lateral`;
- nenhum caractere é escolhido por nome do preset — somente pelos campos
  lidos de `PresetEstilo.dados`;
- a amostra não introduz quebra de linha, moldura própria ou área adicional.

## 7. Amostra de chip (correção H0064-QA-002)

Cada preset de `chip.presets` apresenta uma amostra compacta composta por
três partes conceituais, nesta ordem:

```text
caractere_esquerdo + payload_canônico + caractere_direito
```

`caractere_esquerdo` e `caractere_direito` vêm do próprio preset
(`contrato_estilo.md` §3.2; `docs/nomenclatura/10_ESTILO.md` §4.3). O
`payload_canônico` é conteúdo demonstrativo fixo da categoria chip — não é
dado de preset e não é identificador de preset. Este handoff define
literalmente:

```text
payload_canônico: "Ab"
```

`Ab` é o mesmo literal para todos os presets de chip: não é lido de
`config/estilo.json`, não existe em mapa especial por preset e não depende
do nome do preset. Não é permitido `if preset == ...` nem switch/case sobre
o nome do preset para produzir ou variar o payload — `Ab` é conteúdo
canônico da amostra da categoria, escrito uma única vez na implementação.

Exemplo conceitual:

```text
<preset.caractere_esquerdo>Ab<preset.caractere_direito>
```

`caixa_alta` do preset controla a capitalização do payload exibido, não sua
existência:

| `caixa_alta` | payload exibido |
|---|---|
| `false` | `Ab` |
| `true` | `AB` |

`Ab` contém ao menos uma letra minúscula (`b`), de modo que a transformação
de `caixa_alta` seja observável (`Ab` → `AB`) e presets com `caixa_alta`
diferente produzam amostras textualmente distintas mesmo com os mesmos
delimitadores.

A amostra deve permitir distinguir presets cuja diferença é somente cor —
"Destaque Texto" e "Destaque Fundo" compartilham delimitadores e só se
distinguem por `cor_texto`/`cor_fundo` (contrato_estilo.md §3.2). Não
reproduzir o defeito histórico em que `cor_texto`/`cor_fundo` eram ignorados
na amostra.

### 7.1 Aplicação de `cor_texto`, `cor_fundo` e reset ANSI

- `cor_texto` aplica-se ao payload (`Ab`/`AB`) da amostra de chip — o
  trecho de conteúdo visual afetado pela cor de texto do preset — de modo
  que dois presets com os mesmos delimitadores e o mesmo `caixa_alta`, mas
  `cor_texto` diferente, produzam saída ANSI distinta;
- `cor_fundo` é visível no mesmo payload (`Ab`/`AB`), pela mesma razão;
- após a amostra (delimitadores + payload), ocorre reset ANSI adequado
  antes de qualquer conteúdo subsequente da linha do filho (nome, separador
  ou outra amostra), impedindo vazamento de foreground/background.

A tradução de nome semântico de cor (`"azul"`, `"padrão"` etc.) para valor de
terminal permanece responsabilidade exclusiva do renderer (R-7,
`contrato_barra_de_menus.md` §18; `contrato_estilo.md` §3.2); o controlador
não resolve cor. Não usar catálogo paralelo de nomes especiais nem mapa fixo
preset→amostra. Este handoff não inventa novo protocolo ANSI: a amostra
reutiliza os helpers normais já existentes de estilo/texto ANSI (por
exemplo, `tela/renderizacao/texto_ansi.py`) para aplicar cor, capitalização
e reset — sem duplicar lógica de tradução de cor ou de sequência de escape.

## 8. Amostra de `indicadores.selecionado`

Cada filho mostra o símbolo derivado do próprio preset:
`indicadores.selecionado.presets[*].simbolo`. Não usar símbolo fixo por nome
de preset.

## 9. Amostra de `indicadores.incluido`

Cada filho mostra o par `on`/`off` derivado do próprio preset em
`indicadores.incluido.presets[*]`. A apresentação deve permitir reconhecer
ambos os estados simultaneamente (não alternar um único glifo).

## 10. Relação nome + amostra

Cada filho é composto visualmente em uma única linha lógica, seguindo a
composição:

```text
<nome do preset> + separador canônico + <amostra>
```

O nome real do preset continua vindo de `campos["titulo"]`, já produzido por
H-0063 (via `PresetEstilo.dados`). O separador é um elemento estrutural
estável da apresentação — fixado por este handoff, não dependente do preset
nem do nome do preset; é o mesmo separador para todo filho de toda
categoria. A escolha do glifo concreto do separador é decisão de
implementação dentro desse papel estrutural fixo (por exemplo, dois espaços
ou um caractere simples de separação), sem variar por preset.

A amostra não substitui o nome, e nenhuma formatação pode esconder corrente,
escolhido, nome ou amostra. O estado navegacional corrente/escolhido
(cursor, filho corrente, filho escolhido) continua visível exatamente como em
H-0063 — a amostra não pode ocultá-lo nem competir visualmente com ele a
ponto de tornar o estado ilegível.

## 11. Integração com `dois_niveis_por_foco`

H-0064 preserva integralmente a política canônica reutilizada por H-0063:
pai corrente, filho corrente, filho escolhido, movimento por setas, `Espaço`
transferindo a escolha exclusiva do pai, `Esc` retornando aos pais e
preservando escolhas, foco/cursor reconciliados. As amostras não criam nova
política de navegação, não criam terceiro nível, não mudam a topologia dos
toroides e não alteram a semântica de `Esc` ou `Espaço` já fechada por H-0055
e H-0063.

Renderizar a amostra é estritamente apresentacional: **não é permitido**
acoplar a renderização da amostra a qualquer mutação de candidato, baseline,
`preset_default` persistido ou estilo global. A amostra é derivada da mesma
leitura observacional que já produz o nome do filho.

## 12. Estratégia de composição, resize e paginação (correção H0064-QA-003)

H-0064 não autoriza extensão estrutural do Console para multiline, não cria
renderer paralelo e não introduz um novo modo de item lógico. A decisão para
H-0064 é:

**CADA FILHO CONTINUA REPRESENTADO POR UM ÚNICO NÓ LÓGICO E UMA ÚNICA LINHA
FÍSICA.**

Todas as amostras (borda, chip, selecionado, incluído) devem caber nesse
modelo. A composição `<nome do preset> + separador canônico + <amostra>`
(§10) resulta em um único texto — com ANSI quando aplicável a chip — atribuído
ao mesmo nó lógico que já representa o filho em H-0063, dentro do modo não
verboso vigente na fixture (`politica_exibicao.verboso: false`,
`contrato_console.md` §§5–6). Este handoff não altera
`politica_exibicao.verboso` nem aciona expansão vertical de item.

As amostras devem funcionar com a infraestrutura normal já vigente:

- truncamento/wrap ocorre apenas conforme a infraestrutura vigente de
  largura e overflow do Console — não introduzir geometria fixa nem limiar
  específico de amostra;
- nenhuma linha física extra é criada por amostra;
- paginação mantém um item lógico por filho — cada filho, com sua amostra,
  ocupa exatamente uma posição paginável, como já ocorre em H-0063;
- resize (`SIGWINCH`, conforme H-0063 §8) recompõe a linha normalmente, sem
  resíduo, preservando pai corrente, filho corrente e filho escolhido;
- sequências ANSI da amostra de chip não alteram a contagem de largura
  visual usada por truncamento/paginação — o cálculo de largura usa o
  mecanismo de largura visual já existente
  (`tela/renderizacao/texto_ansi.py`) quando há ANSI; nenhuma sequência ANSI
  é cortada de forma inválida; o reset ANSI (§7.1) ocorre antes do restante
  da linha.

Este handoff não implementa a futura política do `ITEM-0024` de manter
grupos pai+filhos juntos entre páginas. Se um grupo for dividido por
paginação, o comportamento observado é o já vigente em H-0063/console.

## 13. Barra de Menus (correção H0064-QA-001)

H-0064 não altera a Barra de Menus; apenas preserva exatamente a política
vigente da tela H-0063, incluindo os chips de paginação quando
`politica_paginacao: com`. Não introduz chip novo, reordenação nova nem
política global nova.

A Barra vigente, herdada literalmente de
`config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json`,
declara `politica_paginacao: com` e o chip `chip_paginas`
(`[PgUp][PgDn] Páginas`), junto de `chip_sair` (`[Esc]`), `chip_navegar`
(`[✥] Navegar`), `chip_selecionar` (`[␣] Selecionar`) e `chip_ajuda`
(`[?] Ajuda`). Os chips presentes respeitam a ordem relativa canônica
(`contrato_barra_de_menus.md` §7: `[Esc] → [PgUp][PgDn] → ... → [✥] → [␣]
→ ... → [?]`):

```text
[Esc] ... → [PgUp][PgDn] Páginas → [✥] Navegar → [␣] Selecionar → [?] Ajuda
```

Quando a tela estiver paginada, a Barra preserva `[PgUp][PgDn] Páginas`
nessa posição — H-0064 não remove, reordena nem substitui esse chip
herdado, e não introduz outro chip, rótulo ou tecla. `ITEM-0032` (política
global da Barra de Menus) permanece fora de escopo; H-0064 não o antecipa.

## 14. Fronteira rigorosa — fora de escopo

H-0064 **não** implementa:

- configuração candidata;
- atualização do candidato por `Espaço`;
- divergência candidato × baseline;
- `Enter`/`Aplicar` contextual;
- descarte de candidato;
- preview ou demonstração integrada (Cabeçalho + Console + Dashboard + Barra
  sob override, prevista para handoff futuro da ADR-0046 §5);
- override local de demonstração;
- Dashboard de demonstração;
- popup de confirmação;
- `ABORTADO`, `CONFIRMADO`;
- persistência ou publicação;
- alteração de `config/estilo.json`.

A escolha observacional de filho já existente em H-0063 permanece
observacional; H-0064 não a transforma em alteração de candidato.

## 15. Arquivos autorizados para implementação (correção H0064-QA-003)

Lista mínima e justificada, decorrente da decisão de §12: um único nó
lógico por filho, uma única linha física, renderer normal já vigente — sem
estender o Console para multiline e sem renderer paralelo.

### Tela/controlador e renderização (evolução de H-0063)

- `tela/estilo.py` — evoluir a projeção existente para carregar/expor, junto
  de cada filho já construído, os campos concretos do preset necessários à
  amostra (os mesmos já retidos em `PresetEstilo.dados`); não recriar a
  estrutura de pais/filhos nem a fronteira de estado navegacional já fechada
  por H-0063.
- `tela/renderizacao/estilo.py` — evoluir a adaptação/projeção de conteúdo
  para compor, em uma única linha lógica por filho, `<nome do preset> +
  separador canônico + <amostra>` (§10): amostra compacta de borda em uma
  linha (§6), amostra de chip com payload `Ab`/`AB`, tradução de cor e
  reset ANSI (§7, §7.1), símbolo de `selecionado` (§8) e par de `incluido`
  (§9); reutiliza os helpers normais existentes de estilo/texto ANSI (por
  exemplo, `tela/renderizacao/texto_ansi.py`) para cor, capitalização e
  largura visual; continua sem compor popup, moldura, Cabeçalho próprio ou
  geometria multilinha.
- `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json` —
  somente ajuste mínimo, se necessário para acomodar a apresentação da
  amostra em uma linha (por exemplo, largura/gabarito do bloco), preservando
  Cabeçalho, Console, Barra de Menus e `politica_paginacao: com`; não listar
  presets nem criar um novo shell.

Como a decisão desta correção mantém uma única linha por filho dentro do
renderer normal já usado por H-0063, `tela/renderizador.py` e
`tela/renderizacao/contexto_execucao.py` não têm necessidade material
identificada para este handoff e saem da lista de autorização. Permanecem,
como já valia, fontes/infraestrutura canônicas a consumir sem alteração:
`config/estilo.json`, `tela/loader.py`, `tela/navegacao.py`,
`tela/selecao.py`, `tela/renderizacao/tela.py`,
`tela/renderizacao/console.py`, `tela/renderizacao/conteudo_externo.py`,
`tela/renderizador.py`, `tela/renderizacao/contexto_execucao.py` e os
contratos vigentes. Se, durante a implementação, o ponto exato de emprego de
um helper existente (por exemplo, de largura visual ANSI) precisar ser
localizado com mais precisão, essa localização ocorre dentro dos módulos já
autorizados acima — sem criar protocolo novo nem ampliar autorização a outro
arquivo sem nova correção documental.

### Fixture/demo e testes (dedicados a H-0064 — opção B)

Preferida a criação de evidência própria de H-0064, mantendo o runtime
compartilhado com H-0063 e evitando duplicação desnecessária de infraestrutura
já testada. Os testes de H-0063 (`tela/teste_estilo_h0063.py`,
`demo/teste_demo_estilo_h0063.py`) continuam vigentes e não são alterados
por este handoff — devem continuar passando integralmente após a evolução
da fixture/tela compartilhada (mesmo arquivo JSON, ajuste mínimo acima).
H-0064 pode adicionar testes próprios sem apagar evidência estrutural de
H-0063; não é necessário criar fixture nova apenas por formalidade.

- `tela/teste_estilo_h0064.py` — testes dedicados de derivação e composição
  de amostra a partir dos campos concretos do preset (borda em uma linha,
  chip incluindo payload `Ab`/`AB` e cores, selecionado, incluido), preset
  sintético, ausência de mutação de candidato/config e os critérios
  ANSI/largura visual de §17; não duplica os testes estruturais e de
  navegação já cobertos por `tela/teste_estilo_h0063.py`.
- `demo/teste_demo_estilo_h0064.py` — demonstração reproduzível com amostras
  visíveis, resize e paginação; reutiliza o mesmo F4/pilha de telas/decoder
  de `demo/demo.py` sem criar caminho paralelo; não duplica o ciclo de
  navegação já demonstrado em `demo/teste_demo_estilo_h0063.py`.
- `docs/relatorios/IMP-0064-amostras-visuais-presets-estilo.md` — relatório
  futuro da implementação, com arquivos efetivamente alterados, testes e
  validação TTY, se realizada.

Não criar fixture persistente paralela de presets: testes que precisarem de
um preset sintético devem copiar `config/estilo.json` para diretório
temporário, como já praticado em H-0063.

## 16. Critérios de aceite (revisados — correção H0064-QA-001, 002, 003)

H-0064 está concluído quando prova automatizada demonstrar que:

1. os quatro pais continuam existindo, na mesma ordem de H-0063;
2. todos os filhos continuam derivados dinamicamente de `presets`, sem
   enumeração hardcoded;
3. todo filho possui nome e amostra correspondente compostos em uma única
   linha lógica por filho (`<nome do preset> + separador canônico +
   <amostra>`, §10);
4. a amostra de borda consome os sete campos concretos do preset
   (`canto_superior_esquerdo`, `canto_superior_direito`,
   `canto_inferior_esquerdo`, `canto_inferior_direito`, `traco_superior`,
   `traco_inferior`, `lateral`) em uma amostra compacta de uma linha (§6);
5. a amostra de chip consome `caractere_esquerdo`, `caractere_direito`, o
   payload canônico `Ab`/`AB`, `cor_texto`, `cor_fundo` e `caixa_alta` do
   preset (§7, §7.1);
6. dois presets de chip com os mesmos delimitadores e mesmo `caixa_alta`,
   mas `cor_texto` diferente, produzem saída ANSI diferente (reset ANSI
   comprovado — vazamento algum para conteúdo subsequente);
7. dois presets de chip com os mesmos delimitadores e mesmo `caixa_alta`,
   mas `cor_fundo` diferente, produzem saída ANSI diferente; e a largura
   visual (contagem de colunas, ignorando códigos ANSI) permanece coerente
   entre presets comparados, independentemente da cor aplicada;
8. a amostra de `selecionado` usa o símbolo concreto
   (`indicadores.selecionado.presets[*].simbolo`) do preset;
9. a amostra de `incluido` usa os valores concretos `on` e `off` do preset,
   ambos reconhecíveis simultaneamente em uma única linha compacta;
10. um preset sintético inserido em cópia temporária do catálogo aparece
    como filho com amostra correspondente, sem alteração enumerativa no
    código;
11. os testes de H-0063 (`tela/teste_estilo_h0063.py`,
    `demo/teste_demo_estilo_h0063.py`) continuam passando integralmente
    após a evolução da fixture/tela compartilhada;
12. paginação continua funcional com as amostras presentes, mantendo um
    item lógico por filho (§12);
13. resize continua funcional, sem resíduo, preservando pai corrente, filho
    corrente e filho escolhido (§12);
14. `[PgUp][PgDn] Páginas` permanece na Barra de Menus, na posição canônica,
    quando a instância declara `politica_paginacao: com` e há mais de uma
    página (§13);
15. navegar (setas, `Espaço`, `Esc`) não altera candidato, baseline,
    `preset_default` persistido, estilo global ou `config/estilo.json` —
    nenhuma mutação real de estilo;
16. não existe popup no fluxo;
17. não existe `Aplicar`, `CONFIRMADO` ou `ABORTADO` no fluxo;
18. nenhuma expansão estrutural do Console (sem multiline por item, sem
    renderer paralelo, sem novo modo de item lógico — §12).

## 17. Testes automatizados mínimos

### Amostra e dados

- Cada filho de `borda` expõe os sete campos concretos do preset associado
  e a amostra compacta de uma linha os incorpora (§6).
- Cada filho de `chip` expõe `caractere_esquerdo`, `caractere_direito`,
  `caixa_alta`, `cor_texto` e `cor_fundo` do preset associado; o payload
  canônico `Ab`/`AB` (§7) é o mesmo texto para todos os presets de chip.
- Cada filho de `indicadores.selecionado` expõe o `simbolo` concreto do
  preset associado.
- Cada filho de `indicadores.incluido` expõe `on` e `off` concretos do preset
  associado.
- Um preset sintético em fixture temporária aparece com amostra sem
  enumeração no código.

### Comparação visual/ANSI da amostra de chip (correção H0064-QA-002)

Testes que comparem conteúdo renderizado ou representação intermediária
suficiente para comprovar, todos com o mesmo delimitador e o mesmo payload
canônico `Ab`/`AB`:

1. mesmo delimitador + payload, mas `cor_texto` diferente: saída ANSI
   diferente entre os dois presets;
2. mesmo delimitador + payload, mas `cor_fundo` diferente: saída ANSI
   diferente entre os dois presets;
3. `caixa_alta: false`: payload exibido é `Ab`;
4. `caixa_alta: true`: payload exibido é `AB`;
5. reset ANSI: o estilo (cor de texto/fundo) da amostra de chip não vaza
   para o conteúdo que segue na mesma linha (nome de outro filho, separador
   ou outra amostra);
6. largura visual: a contagem de colunas da amostra de chip é igual entre
   presets que diferem apenas em `cor_texto`/`cor_fundo` — códigos ANSI não
   contam como largura física, verificada com o mecanismo de largura visual
   já existente (`tela/renderizacao/texto_ansi.py`), não por comparação
   arbitrária de strings.

### Fronteira de estado (regressão de H-0063)

- Navegar entre filhos, transferir escolha por `Espaço` e retornar por `Esc`
  não alteram candidato, `config/estilo.json`, `preset_default` persistido
  ou estilo global — reafirmação da fronteira já validada por H-0063, agora
  também na presença das amostras.

### Resize e paginação

- Renderizar em dimensões larga, média, estreita suportada e após
  crescimento, com amostras presentes, sem exceção, sem resíduo, conteúdo
  dentro da largura e altura, foco/cursor reconciliados, um item lógico por
  filho (sem linhas físicas extras).
- Paginação com amostras presentes preserva navegação e não introduz erro de
  composição; `[PgUp][PgDn] Páginas` continua ativo/inativo conforme o
  número de páginas.

## 18. Validação manual prevista

Prever validação TTY manual apenas se o QA considerar necessário para
confirmar:

- legibilidade das amostras compactas de borda em uma linha e das amostras
  de chip (delimitadores, payload `Ab`/`AB`, cores);
- distinção visual entre presets, inclusive os que diferem somente por cor;
- comportamento das amostras após resize;
- ausência de resíduos.

Não exigir novamente validação de `F4` ou da topologia de navegação em dois
níveis, já validada por H-0063, salvo regressão detectada.

## 19. Fora de escopo (trabalhos futuros)

- candidato, `Enter`/`Aplicar`, demonstração integrada, override local,
  Dashboard de demonstração, popup, `CONFIRMADO`/`ABORTADO`, persistência e
  publicação — permanecem para handoffs futuros da ADR-0046;
- `ITEM-0024` (agrupar pai+filhos entre páginas);
- `ITEM-0032` (política global da Barra de Menus);
- `tiling`, `cor_inativo`, `cor_alerta`, `indicadores.concluido`;
- F1, F11, F2, F3, F5.

## 20. Fronteira posterior

Após a aprovação de H-0064, a próxima partição do `ITEM-0010` (candidato e
`Espaço` alterando escolha, ou demonstração integrada) será decidida pelo
gerente, observando o resultado real desta amostra visual. Este documento não
numera nem especifica handoffs posteriores.
