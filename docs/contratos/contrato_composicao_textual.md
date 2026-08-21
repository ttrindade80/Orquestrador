---
name: contrato-composicao-textual
description: Contrato comportamental da composição textual canônica da TUI
metadata:
  type: contrato
  scope: tui_composicao_textual
---

# Contrato especializado — composição textual canônica da TUI

## 1. Finalidade e autoridade

Este contrato define o comportamento observável da composição textual canônica
da TUI: a transformação de texto dependente de largura em uma sequência
ordenada de linhas físicas. Ele é a autoridade comportamental única para wrap,
composição de linhas e justificação de parágrafo quando essa capacidade for
necessária.

Autoridades locais semanticamente equivalentes devem convergir para este
comportamento. Peculiaridade histórica só pode permanecer quando for semântica
necessária do consumidor; a reprodução incidental de um helper antigo não é
requisito.

Este contrato não escolhe módulo Python, helper, função, classe, assinatura,
API, fachada, reexportação, localização da implementação ou organização
interna.

## 2. Dependências terminológicas

Este contrato usa as autoridades terminológicas de:

- `docs/nomenclatura/01_NUCLEO_COMUM.md`;
- `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`.

`renderizador` conserva a autoridade transversal já definida no núcleo comum.
A composição declarativa do corpo, incluindo `corpo.arranjo` e `tiling`, não é
redefinida nem incorporada por este contrato.

## 3. Conceitos comportamentais

- **Texto lógico:** parágrafo completo recebido para composição multilinear,
  podendo conter conteúdo ANSI já suportado pela TUI. Ele é a entrada lógica
  de toda composição ou recomposição e não é substituído por linhas físicas já
  produzidas.
- **Palavra:** unidade lógica textual que o compositor mantém inteira. Ela não
  é partida, hifenizada ou separada silabicamente pelo compositor.
- **Largura útil efetiva:** quantidade positiva de células visuais que o
  consumidor entrega para a composição, depois de descontar suas próprias
  margens, prefixos, indicadores e demais estruturas.
- **Largura visual:** quantidade de células ocupadas pela representação visível
  do texto; sequências de controle ANSI suportadas não ocupam células.
- **Linha física:** cada unidade ordenada produzida para renderização a partir
  do texto lógico. Para palavras que cabem na largura útil efetiva, sua largura
  visual não excede essa largura; o tratamento físico de uma palavra individual
  que a exceda não é definido por este contrato.
- **Vão interno:** vão entre palavras da mesma linha, elegível para receber
  expansão na justificação de parágrafo. Espaços de borda, padding e
  alinhamento estrutural não são vãos internos de parágrafo.

Wrap/composição de parágrafo é distinto de truncamento deliberado de linha
única. Padding ou alinhamento de coluna, célula, chip, grade e moldura também
é distinto de justificação de parágrafo.

## 4. Entrada semântica mínima

A operação recebe, em termos comportamentais:

1. o texto lógico completo do parágrafo a ser composto;
2. a largura útil efetiva, expressa em células visuais e maior que zero;
3. o modo solicitado pelo consumidor, distinguindo composição/wrap de
   justificação de parágrafo; qualquer alinhamento textual aplicável deve ser
   explicitamente solicitado;
4. a informação necessária para reconhecer e tratar corretamente as
   sequências ANSI pertencentes ao conjunto já suportado pela TUI, separando
   controle visual de conteúdo que ocupa células.

O contrato não cria modo implícito de justificação: na ausência de solicitação
explícita, a composição não expande vãos para preencher a largura.

## 5. Resultado

O resultado é uma sequência ordenada de linhas físicas derivadas do texto
lógico completo do parágrafo. A operação deve:

- preservar a ordem e o conteúdo textual, sem perda, duplicação ou inserção
  de conteúdo, salvo as transformações expressamente admitidas neste
  contrato;
- introduzir somente as fronteiras de linha necessárias ao wrap e, quando
  solicitado, as células adicionais de espaço da justificação;
- respeitar a largura visual efetiva de cada linha nos casos em que as palavras
  nela contidas cabem nessa largura;
- preservar a informação ANSI necessária para que a representação resultante
  mantenha o estado visual correto.
- recompor, inclusive após resize, a partir do texto lógico completo, sem usar
  linhas físicas produzidas anteriormente como entrada lógica.

## 6. Regra de wrap em largura útil

A unidade lógica da composição multilinear é o parágrafo completo. O parágrafo
é recomposto como um todo a cada composição ou recomposição, inclusive após
resize. A entrada lógica é sempre o texto lógico completo; linhas físicas
produzidas anteriormente não são reutilizadas como entrada de uma nova
composição.

As linhas físicas são formadas com palavras inteiras, preservando a ordem do
texto e sem inserir hífen ou outro marcador de quebra. Para palavras que cabem
na largura útil efetiva, a composição forma linhas que não excedem essa
largura. O compositor não parte palavras para fazê-las caber e não realiza
hifenização automática, separação silábica ou divisão arbitrária por número de
células.

O comportamento específico de espaços e separadores herdado das
implementações locais atuais não é preservado automaticamente pelo mecanismo
canônico. Uma diferença de comportamento correspondente só permanece quando
constituir requisito semântico real de um consumidor, ou vier a ser decidida
posteriormente; o mecanismo canônico não infere essa política a partir da
implementação histórica.

Quando uma palavra individual exceder a largura útil, ela permanece
semanticamente indivisível para o compositor e não pode ser alterada para
caber. O contrato comum define somente essa indivisibilidade; não define o
tratamento físico dessa condição nem escolhe uma política adicional para ela.

## 7. Justificação de parágrafo

A justificação de parágrafo só é aplicada quando o consumidor a solicita
explicitamente. Quando solicitada, o mecanismo canônico produz essa
apresentação distribuindo o excesso de células — a diferença entre a largura
visual de uma linha elegível e a largura útil efetiva — entre os vãos
existentes entre palavras das linhas às quais a justificação se aplica. A
formação das linhas, com suas palavras inteiras, ocorre antes dessa expansão.

A forma algorítmica concreta dessa distribuição, incluindo qualquer regra de
uniformidade, distribuição de resto, tratamento de linha sem vãos internos
suficientes, não é definida por este contrato enquanto não existir decisão
própria. A última linha permanece neutra: este contrato não determina se ela
deve ou não ser justificada, expandida ou submetida a qualquer distribuição
especial.

Justificação permanece distinta de padding ou alinhamento estrutural: não
altera prefixos, indicadores, margens, colunas ou qualquer padding estrutural
do consumidor.

## 8. Segurança ANSI e largura visual

Para conteúdo ANSI já suportado pela TUI:

- a largura é calculada pelas células visuais, sem contar sequências de
  controle como caracteres visíveis;
- nenhuma sequência CSI pode ser cortada parcialmente por uma fronteira de
  linha ou de segmento;
- fronteiras de linha são materializadas de modo que o estado visual de uma
  linha ou região não vaze indevidamente para a seguinte;
- controles necessários para fechar, preservar ou restabelecer estado visual
  não são tratados como conteúdo textual nem aumentam a largura visual;
- a composição não cria uma política de cores, estilo ou interpretação ANSI
  além da segurança necessária para o conteúdo já suportado.

## 9. Consistência entre renderização e medição

Renderização e medição devem consumir comportamento compatível desta mesma
autoridade, com o mesmo texto, largura útil efetiva, modo e tratamento ANSI.
Quantidade de linhas físicas, altura derivada e mapa físico devem ser obtidos
da mesma composição que será renderizada; não é válida uma regra de quebra
separada para contar linhas ou paginar.

Quando a largura mudar, a composição física é recalculada com a nova largura
útil efetiva a partir do texto lógico completo do parágrafo; linhas físicas
anteriores não são entrada lógica da recomposição. Isso não altera o conteúdo
semântico, `corpo.arranjo`, `tiling`, topologia de paginação, comandos
`PageUp`/`PageDown` ou schema de conteúdo.

## 10. Responsabilidades dos consumidores

Continuam fora do núcleo canônico:

- criação e posicionamento de prefixos, designadores e indicadores;
- indentação de continuação;
- definição da largura útil efetiva;
- estrutura de colunas e escolha dos campos que podem quebrar;
- seleção de modo verboso ou não verboso;
- decisões semânticas sobre quais textos constituem parágrafos;
- truncamento deliberado quando a apresentação exigir uma única linha;
- padding e alinhamento de colunas ou células, chips, grades e molduras;
- composição declarativa do corpo, distribuição de área, paginação e schema.

Truncamento deliberado de linha única não é convertido automaticamente em
wrap. Um consumidor só usa a composição textual quando a sua semântica exige
compor um parágrafo ou quebrar texto em linhas.

## 11. Erros e limites de entrada

A implementação futura deve ter comportamento determinístico para o seu
domínio de entrada válido. A definição concreta de validação, rejeição,
exceção, fallback ou qualquer outro tratamento de entrada inválida —
incluindo largura, texto, modo, alinhamento, conteúdo ANSI, texto vazio fora
do domínio válido e limite técnico de implementação — pertence à definição
executiva posterior, quando depender da API concreta do mecanismo canônico.

Este contrato não impõe limite visual fixo além da exigência de largura útil
efetiva positiva já registrada em §3 e §4. O consumidor é responsável por
fornecer uma largura compatível com sua geometria efetiva.

## 12. Critérios de aceite para handoffs futuros

Um handoff que implemente ou migre consumidores deve demonstrar, no mínimo:

- uma única autoridade comportamental para composição, wrap e justificação;
- linhas em largura curta, exata e ampla, com preservação de ordem e conteúdo;
- parágrafo completo recomposto no resize, sem reutilização de linhas físicas
  anteriores como entrada lógica;
- nenhuma palavra dividida pelo compositor, sem hifenização automática,
  separação silábica ou divisão arbitrária;
- palavra maior que a largura preservada semanticamente, sem política física
  adicional escolhida por este contrato;
- formação das linhas antes da justificação, com expansão somente nos vãos
  entre palavras das linhas aplicáveis;
- neutralidade quanto à última linha, sem política específica de justificar,
  expandir ou distribuir;
- justificação somente sob solicitação, com distribuição do excesso entre
  vãos internos elegíveis e sem alterar padding estrutural do consumidor;
- largura visual ANSI correta, CSI indivisível e ausência de vazamento de estado;
- igualdade comportamental entre linhas renderizadas e linhas medidas para
  altura, mapa físico e paginação;
- truncamento de linha única comprovadamente separado de wrap;
- preservação das responsabilidades locais do consumidor e das fronteiras de
  `corpo.arranjo`, `tiling`, paginação, schema e composição declarativa;
- ausência de dependência do resultado em nome de módulo, helper, assinatura,
  fachada ou outra decisão arquitetural não definida pela ADR.
