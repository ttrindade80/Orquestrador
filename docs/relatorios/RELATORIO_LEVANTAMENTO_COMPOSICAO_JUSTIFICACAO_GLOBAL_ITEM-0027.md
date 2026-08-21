# Levantamento focal — ITEM-0027

## Escopo

Levantamento factual da implementação atualmente usada pela TUI para composição de linhas, quebra, preenchimento, truncamento e justificação de texto. Não foram propostas mudanças, arquitetura ou handoffs; não houve alteração de código.

Não foram lidos documentos normativos. As ocorrências de `wrap` relativas à navegação toroidal, autowrap do terminal e comentários sem operação textual foram separadas do mapa de composição.

## Buscas executadas

Foram executadas, nesta ordem, as duas buscas autorizadas:

1. `rg -n -i --glob '*.py' 'justify|justific|textwrap|wrap|par[aá]grafo|quebra.{0,20}(linha|texto)|distribu.{0,20}espa[cç]|espa[cç].{0,20}distribu|ljust|rjust|center' tela demo tests orquestrador.py`
2. `rg -n --glob '*.py' '\.(ljust|rjust|center)\(|textwrap\.(wrap|fill|shorten)\(|\bwrap\(' tela demo tests orquestrador.py`

Os dois comandos registraram os caminhos `tests` e `orquestrador.py` como inexistentes. Não foram substituídos por busca recursiva ampla.

## Mapa das implementações

### Núcleos de quebra, composição e justificação

| Caminho | Responsável | Operação | Reutilização / comportamento |
|---|---|---|---|
| `tela/renderizacao/popup.py:681-730` | `_quebrar_texto` | wrap de texto de popup | Lógica local independente. Valida largura inteira positiva, conserva separadores e espaços de extremidade, divide palavra longa quando inevitável e não trunca. Usada pelo popup textual e pela instrução do popup de marcação. |
| `tela/renderizacao/popup.py:733-767` | `_justificar_linha` e `_formatar_linha` | justificação por distribuição de espaços; alinhamento esquerdo/centralizado | Único algoritmo encontrado que distribui o excesso entre vãos internos de um parágrafo. A distribuição usa `divmod`, prioriza os primeiros vãos no resto e só ocorre em linhas não finais com `alinhamento == "justificado"`; a última linha fica à esquerda. |
| `tela/renderizacao/conteudo_externo.py:60-82` | `_quebrar_texto` | wrap de conteúdo externo | Segunda lógica local independente. No caminho sem ANSI procura o último espaço antes da largura, faz corte duro se necessário e remove espaços à esquerda da continuação. Para texto ANSI delega a `_quebrar_sem_ansi`. Largura nula/negativa devolve o texto em uma linha, em vez de lançar erro. |
| `tela/renderizacao/texto_ansi.py:103-210` | `_largura_sem_ansi`, `_cortar_sem_ansi`, `_ljust_sem_ansi`, `_quebrar_sem_ansi` | largura visual, truncamento físico, padding e wrap ANSI | Helpers reutilizáveis. `_quebrar_sem_ansi` é uma variante material do wrap: não parte CSI, prefere espaço dentro da janela e fecha/reabre SGR entre linhas. É chamada pelo `_quebrar_texto` de conteúdo externo; não é uma terceira autoridade pública independente de conteúdo. |
| `tela/renderizacao/conteudo_externo.py:85-110` | `_truncar_com_marcador` | truncamento com `...` | Helper reutilizado pelas três apresentações de conteúdo externo e por consumidores do renderizador. Não é wrap nem justificação; produz uma linha física limitada. |

### Composição de conteúdo que consome os núcleos

| Caminho | Responsável / consumidor | Operação e largura |
|---|---|---|
| `tela/renderizacao/conteudo_externo.py:113-262` e `330-525` | `_linhas_apresentacao_hierarquia_com_mapa` | Compõe prefixos, designadores, indicadores e linhas de continuação. Em modo verboso chama `_quebrar_texto` com `content_w - len(prefixo)` (mínimo local de 10); em modo não verboso chama `_truncar_com_marcador`. A variante de dois níveis calcula larguras globais de designadores e dos filhos. |
| `tela/renderizacao/conteudo_externo.py:560-671` | `_linhas_apresentacao_tabela` | Compõe colunas com `ljust`; em verboso quebra somente a última coluna dos dados pela largura restante; cabeçalho não é quebrado. Em não verboso trunca a linha inteira ou a régua. |
| `tela/renderizacao/conteudo_externo.py:701-775` | `_linhas_apresentacao_conjuntos` | Compõe `nome + separador + valor`; `nome.ljust(largura_local)` alinha nomes por conjunto quando configurado. Em verboso quebra apenas o valor e indenta continuações; em não verboso trunca o valor. Esse `justificar_nomes` é padding de coluna, não justificação de parágrafo. |
| `tela/renderizacao/matriz_participantes.py:306-395` | `_renderizar_participante_com_indicador`, `_altura_quebra_item` | No console matricial verboso, chama o wrap de conteúdo externo na largura útil da célula após indicadores. No não verboso mantém o texto inteiro e a escrita na célula limita o excesso pela fronteira física. A altura é derivada da quantidade de fragmentos. |
| `tela/renderizacao/paginacao_interna.py:18-28,87-96` e `tela/renderizacao/console.py:200-212,307-335` | paginação/mapa físico | Reutiliza o mesmo wrap de conteúdo externo para produzir linhas esperadas e para contar linhas físicas por item. A paginação depende dessa contagem e recorta fragmentos, mas não possui algoritmo de justificação próprio. |
| `tela/renderizador.py:19-23,34-39` | fachada pública | Reexporta `_quebrar_texto`, `_truncar_com_marcador`, `_largura_sem_ansi` e `_ljust_sem_ansi`; não contém a implementação. |

### Composição física relacionada, mas não equivalente à justificação

Estas ocorrências foram encontradas pelas buscas e são relevantes para representação física, mas não foram contadas como algoritmos de justificação de parágrafo:

- `tela/renderizacao/barra_menus.py:470-509,922-963`: `_montar_coluna_a_coluna` e `_montar_linha_a_linha` distribuem chips inteiros em linhas; usam padding de colunas e falham com `erro_layout` se a grade não couber. Não quebram palavras.
- `tela/renderizacao/estilo.py:123-175`: compõe chips multitecla e título de amostra; `compor_titulo_com_amostra` usa `_ljust_sem_ansi` para a coluna do nome. A composição de chip é compartilhada pela amostra de Estilo e pela barra real.
- `tela/renderizacao/lancador.py:282-308`: distribui excesso entre margens/vãos e usa `celula.ljust(col_w)` para colunas. É alinhamento de grade do lançador.
- `tela/renderizacao/geometria_caixa.py:145-185`: `_linha_conteudo` corta e preenche o envelope da caixa; os alinhamentos de cabeçalho são simples esquerda/centro/direita.
- `tela/renderizacao/tela.py:23-47` e `demo/demo.py:2430-2445,2499-2533`: quadros de insuficiência/terminal pequeno cortam a mensagem e fazem `ljust` até a largura física. São variantes de moldura/aviso, não composição de parágrafo.
- `demo/casos_validacao_paginacao.py:408-435`: `ljust` com `-` em gerador de tokens de validação; é helper de caso de demonstração, não implementação da TUI.

## Quantidades factuais

O resultado depende do nível de contagem, que fica explicitado para não misturar algoritmo com consumidor:

- **2 autoridades locais independentes de wrap genérico:** `popup._quebrar_texto` e `conteudo_externo._quebrar_texto`.
- **1 variante material de wrap:** `texto_ansi._quebrar_sem_ansi`, acionada como ramo ANSI do segundo helper.
- **1 algoritmo de justificação de parágrafo:** `popup._justificar_linha`, chamado por `popup._formatar_linha`.
- **5 caminhos de composição textual com regras locais de prefixo/coluna/célula:** popup, hierarquia, tabela, conjuntos de campos e matriz de participantes. A paginação é consumidora da quebra/contagem, não uma sexta implementação de quebra.
- **4 famílias de consumidores por fluxo amplo:** popup; conteúdo externo; console matricial; paginação interna. Se conteúdo externo for separado pelas três apresentações, são **6 subfamílias comportamentais**: popup, hierarquia, tabela, conjuntos de campos, matriz e paginação.

## Arquivos de produção envolvidos

Núcleo direto: `tela/renderizacao/popup.py`, `tela/renderizacao/conteudo_externo.py`, `tela/renderizacao/texto_ansi.py`, `tela/renderizacao/matriz_participantes.py`, `tela/renderizacao/paginacao_interna.py`, `tela/renderizacao/console.py` e `tela/renderizador.py`.

Superfície física relacionada: `tela/renderizacao/geometria_caixa.py`, `tela/renderizacao/barra_menus.py`, `tela/renderizacao/lancador.py`, `tela/renderizacao/estilo.py`, `tela/renderizacao/tela.py` e `demo/demo.py`.

## Arquivos de testes diretamente envolvidos

- `tela/teste_popup.py:220-328,447-475,746-825`: testes diretos de wrap, preservação de separadores, palavras longas, alinhamentos, distribuição de espaços da justificação, última linha, largura e overlay ANSI; também testes integrados do popup de marcação.
- `tela/teste_estilo_h0073_h0063.py:328-348`: exercita o caminho ANSI de `_quebrar_texto`, incluindo CSI, resets, largura visual e continuação.
- `tela/testes_renderizador/conteudo_externo.py:185-320,529-690`: testa diretamente `_truncar_com_marcador` e integra hierarquia/tabela em modos verboso e não verboso, preservação de tokens, indentação, largura e alternância.
- `tela/teste_formato_filho_dois_niveis_por_foco.py:329-350`: cobre quebra multilinha de coluna/filho e continuidade sem duplicar identidade ou indicadores.
- `demo/teste_demo_popup.py:110-127`: cobre recomposição do popup ao variar largura e restauração da largura original mantendo a instância.
- `demo/teste_demo_paginacao.py:1658-1681,1715-1734,1845-1896,1942-1955`: compara as linhas renderizadas com as linhas produzidas pelo mesmo `_quebrar_texto` e verifica paginação, largura, ordem, ausência de perda e ausência de duplicação.

Superfícies adjacentes, não focais para o algoritmo de parágrafo: `tela/teste_estilo_h0064.py:75-98` testa padding de nomes/amostras; `tela/teste_loader.py:3102-3105` valida rejeição de configuração `justificado` sem escopo, sem exercitar a distribuição de espaços.

Os testes não foram executados neste levantamento; a lista acima é a superfície existente identificada por busca e abertura focal.

## Duplicações e variações confirmadas

- Há duplicação confirmada de autoridade de wrap entre popup e conteúdo externo: ambas implementam `_quebrar_texto` localmente, com regras diferentes para largura inválida, separadores e preservação de espaços.
- Há uma variante ANSI confirmada dentro do caminho de conteúdo externo, com contagem visual e preservação de SGR; o popup usa sua própria quebra baseada em `len` e mantém rotinas ANSI separadas para alinhamento/overlay.
- A justificação por distribuição de espaços aparece somente no popup. Não foi encontrada implementação equivalente em conteúdo externo, barra, lançador, tabela ou conjuntos de campos.
- `justificar_nomes` em conjuntos de campos e os `ljust` de tabela/barra/lançador/estilo são alinhamentos de coluna ou padding; não são duplicações do algoritmo de `_justificar_linha`.
- Há duas variantes locais de quadro de aviso com `ljust` (`tela/renderizacao/tela.py` e `demo/demo.py`), mas seu comportamento é de envelope de insuficiência, não de composição de parágrafo.

## Acoplamentos relevantes

- A mudança de uma autoridade de wrap do conteúdo externo alcançaria hierarquia, tabela, conjuntos de campos, matriz de participantes, cálculo de altura, mapa físico, paginação e a fachada `tela.renderizador`.
- No console matricial, a largura efetiva depende de indicadores, margens, formação/colunas e `content_w`; a mesma decisão de quebra alimenta renderização, altura mínima e paginação.
- Na hierarquia de dois níveis, prefixos, designadores, indicadores e largura global de colunas alteram a largura restante antes do wrap; a continuação também tem indentação derivada do prefixo.
- No popup, a largura do corpo, a margem horizontal, a altura derivada, instrução, itens, chips e overlay no corpo são calculados juntos; a justificação é aplicada após o wrap e somente a linhas não finais.
- A barra de menus depende de composição de chips e de uma política própria de preenchimento (`coluna_a_coluna`/`linha_a_linha`), mas não depende dos helpers de wrap de parágrafo.

## Fatos úteis ao dimensionamento posterior

- O maior compartilhamento existente está no caminho de conteúdo externo: um helper de wrap é usado por três apresentações e também por consumidores de console/paginação.
- O popup é um núcleo local separado e é o único produtor de justificação de parágrafo; seus testes unitários são mais específicos para distribuição de espaços do que os testes do conteúdo externo.
- O mesmo nome `_quebrar_texto` existe em dois módulos com contratos observáveis diferentes; a fachada reexporta apenas o do conteúdo externo.
- A largura útil não é uma constante única: aparece como `content_w`, largura restante após prefixos, largura útil após margem/indicadores e largura de corpo limitada pelo console.
- O truncamento é separado do wrap no conteúdo externo (`_truncar_com_marcador`) e é aplicado de modo diferente nos modos verboso e não verboso.
- O levantamento encontrou cobertura integrada ampla para conteúdo externo, matriz e paginação, e casos unitários explícitos para popup/justificação; não encontrou teste unitário focal do ramo simples de `_quebrar_texto` de conteúdo externo nem teste focal do algoritmo de justificação com ANSI.

## Pontos NAO_CONFIRMADOS

- Não foi confirmado, pelas buscas autorizadas, outro algoritmo de justificação de parágrafo fora de `tela/renderizacao/popup.py`.
- Não foi confirmado teste unitário dedicado ao caminho sem ANSI de `tela/renderizacao/conteudo_externo._quebrar_texto`; os efeitos desse caminho aparecem cobertos por integrações de conteúdo, console e paginação.
- Não foi confirmado teste unitário dedicado a todos os limites de largura inválida de cada helper; os contratos observáveis foram inferidos do código aberto e dos casos focais existentes.
- Não foi confirmado se existem consumidores fora dos caminhos apontados pelas duas buscas autorizadas, pois não foi feita pesquisa recursiva adicional nem leitura de arquivos não apontados.

## Estado Git observado

Coletado antes da materialização deste relatório:

- `git status --short`: saída vazia.
- `git branch --show-current`: `master`.
- `git rev-parse HEAD`: `bd6fb46d8b841b38f3098f7187d3b71bee3c2ad7`.
