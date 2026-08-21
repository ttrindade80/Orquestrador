---
name: ADR-0049-composicao-justificacao-global-texto-tui
description: "Institui autoridade canônica única de composição de parágrafo, wrap e justificação textual da TUI, substituindo as autoridades locais equivalentes"
metadata:
  type: adr
  status: aceita_e_aplicada
  id: ADR-0049
  data: 2026-08-19
  substitui: null
rastreabilidade:
  decisao_usuario: "Decisões fechadas D-0027-01 a D-0027-10, com D-0027-10 registrada nesta reabertura após a validação manual do ITEM-0027"
  rfc_origem: null
  issues_relacionadas:
    - ITEM-0027
  contratos_afetados:
    - docs/contratos/contrato_composicao_textual.md
  handoffs_bloqueados: []
---

# ADR-0049 — Composição e justificação global de texto da TUI

## 1. Status

`aceita e aplicada`

## 2. Contexto

O levantamento focal do `ITEM-0027`
(`docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_JUSTIFICACAO_GLOBAL_ITEM-0027.md`)
confirmou que a TUI mantém hoje duas autoridades locais independentes de
quebra de texto (`tela/renderizacao/popup.py::_quebrar_texto` e
`tela/renderizacao/conteudo_externo.py::_quebrar_texto`), uma variante ANSI
compartilhada apenas pelo segundo caminho
(`tela/renderizacao/texto_ansi.py::_quebrar_sem_ansi`) e um único algoritmo
de justificação de parágrafo por distribuição de espaços
(`tela/renderizacao/popup.py::_justificar_linha`), sem equivalente em
conteúdo externo, tabela, conjuntos de campos, barra de menus ou lançador.

O caminho de conteúdo externo é consumido, com a mesma decisão de composição,
por
hierarquia, tabela, conjuntos de campos, matriz de participantes, cálculo de
altura, mapa físico e paginação interna. Essa duplicação de autoridade para a
mesma responsabilidade semântica — compor parágrafo, derivar linhas de
palavras inteiras na largura útil e, quando solicitado, justificar — é o
problema que este item resolve. Não é
tratado aqui, por não constituírem a mesma responsabilidade semântica,
padding/alinhamento de coluna, preenchimento de célula, distribuição
geométrica de chips, distribuição de grade do lançador, moldura/preenchimento
de caixa ou composição declarativa do corpo — o levantamento os registrou
como superfície física relacionada, não como autoridades concorrentes de
justificação de parágrafo.

## 3. Decisão explícita do usuário

O usuário fechou as decisões D-0027-01 a D-0027-10, sintetizadas em §4.
Nenhuma alternativa arquitetural nova é escolhida por esta ADR: as decisões
abaixo registram as fronteiras comportamentais fechadas para o `ITEM-0027`,
incluindo a decisão de composição de parágrafo decorrente da validação manual.

## 4. Decisão

### D-0027-01 — Autoridade global

A TUI passa a ter um mecanismo canônico e global de composição de parágrafo
e justificação textual. Autoridades locais independentes para essa mesma
responsabilidade semântica não permanecem. A finalidade do `ITEM-0027` é
substituir as autoridades locais equivalentes por uma autoridade
compartilhada — não introduzir uma fachada sobre implementações divergentes
que continuem a existir por baixo.

### D-0027-02 — Contrato canônico explícito

O mecanismo global tem contrato canônico novo e explícito, a ser
materializado durante a aplicação (`APLICAR_ADR`) em
`docs/contratos/contrato_composicao_textual.md`. Esta ADR define o papel
desse contrato como autoridade comportamental completa do mecanismo; não o
cria nem antecipa seu schema.

### D-0027-03 — Política para diferenças históricas

As peculiaridades dos helpers locais atuais não são preservadas
automaticamente na migração. Regras de conduta:

- preservar diferença de comportamento somente quando representar semântica
  necessária de algum consumidor;
- não perpetuar peculiaridade histórica apenas para reproduzir a
  implementação antiga;
- diferenças que não correspondam a requisito real convergem para o
  comportamento canônico único.

### D-0027-04 — Escopo do mecanismo comum

O núcleo comum cobre a responsabilidade de composição textual de parágrafo,
incluindo o necessário para: recomposição do parágrafo lógico completo em
linhas de palavras inteiras conforme D-0027-10; justificação de parágrafo
quando esse modo for solicitado; cálculo coerente por largura visual; e a
segurança necessária para o conteúdo ANSI já suportado pela TUI. A existência
do mecanismo global não torna todo texto da TUI justificado — ele fornece a
implementação canônica quando composição, wrap ou justificação de parágrafo
forem necessários.

### D-0027-05 — Fronteira com regras locais dos consumidores

Continuam pertencendo aos consumidores suas regras semânticas próprias:
prefixos; designadores; indicadores; indentação de continuação; definição da
largura útil entregue ao mecanismo; estrutura de colunas; escolha de quais
campos podem quebrar; comportamento verboso/não verboso; e truncamento
específico quando a apresentação deliberadamente exige uma única linha. O
mecanismo global não assume essas decisões.

### D-0027-06 — O que não é justificação de parágrafo

Não são tratados como duplicação do algoritmo de justificação de parágrafo:
`ljust`, `rjust` e `center` usados apenas para padding/alinhamento;
alinhamento de colunas; preenchimento de células; distribuição geométrica de
chips; distribuição de grade do lançador; moldura ou preenchimento de caixa;
e composição declarativa de `corpo`. Essas operações só entram no escopo do
`ITEM-0027` mediante evidência objetiva de que implementam composição
textual de parágrafo equivalente ao núcleo canônico.

### D-0027-07 — Compatibilidade estrutural

O `ITEM-0027` não altera `corpo.arranjo`, `tiling`, política de paginação,
topologia `PageUp`/`PageDown`, schema de conteúdo, semântica dos dados,
taxonomia dos elementos funcionais nem a composição declarativa da tela. A
largura continua dinâmica, calculada a partir da geometria efetiva do
terminal/consumidor.

### D-0027-08 — Consistência entre renderização e medição

Quando um consumidor usa a composição textual para calcular linhas físicas,
altura ou paginação, medição e renderização consomem comportamento
compatível da mesma autoridade canônica. Não é admitida uma regra de quebra
para renderizar e outra materialmente divergente para contar as linhas
resultantes.

### D-0027-09 — Truncamento permanece distinguível

Wrap/composição de parágrafo e truncamento deliberado de linha única
continuam responsabilidades distinguíveis. A criação do mecanismo canônico
não transforma automaticamente operações atuais de truncamento em wrap.

### D-0027-10 — Composição de parágrafo por palavras indivisíveis

A unidade lógica de composição multilinear é o parágrafo completo. A cada
composição ou recomposição, inclusive após resize, as linhas físicas devem
ser derivadas novamente do texto lógico completo do parágrafo.

A sequência conceitual é: parágrafo lógico → identificação das palavras →
distribuição de palavras inteiras em linhas → justificação das linhas
aplicáveis → representação física.

As linhas são formadas por palavras inteiras que caibam na largura útil. O
mecanismo comum não pode partir palavras para fazê-las caber e não realiza
hifenização automática, separação silábica nem divisão arbitrária por número
de células. Uma palavra individual maior que a largura útil permanece
semanticamente indivisível para o compositor; o compositor não pode alterá-la
para fazê-la caber. O tratamento físico dessa condição pertence à
representação física ou ao consumidor quando necessário e não deve ser
confundido com composição de parágrafo nem convertido silenciosamente em
quebra silábica.

A justificação ocorre somente depois de determinadas as palavras pertencentes
a cada linha. Sua expansão distribui espaço nos vãos entre palavras da mesma
linha. Em particular, resize recompõe o parágrafo original a partir do texto
lógico, em vez de justificar ou repartir novamente linhas físicas anteriormente
produzidas.

Esta decisão autoriza a afirmação específica de que a justificação distribui
espaço entre palavras pertencentes à mesma linha. Ela não estabelece política
global genérica para whitespace ou separadores arbitrários, nem se generaliza
para tabs, separadores estruturais, conteúdo não textual ou qualquer política
literal de preservação ou normalização.

## 5. Consequências

### Positivas

- Elimina a duplicação confirmada de autoridade de wrap entre
  `popup.py` e `conteudo_externo.py`.
- Estabelece um único algoritmo de justificação de parágrafo como
  referência canônica, hoje existente apenas em `popup.py`.
- Reduz o risco de divergência futura entre a regra usada para renderizar e
  a regra usada para medir/paginar, ao fixar a exigência de consistência
  (D-0027-08).
- Cria autoridade documental própria (o contrato canônico) para uma
  responsabilidade que hoje não possui contrato dedicado.

### Custos e restrições

- A aplicação exige revisar consumidores em múltiplas famílias (popup,
  conteúdo externo, matriz de participantes, paginação interna) sem alterar
  sua semântica local própria.
- Peculiaridades históricas que não correspondam a requisito real de
  consumidor são descontinuadas, o que pode alterar detalhes de saída até
  então incidentais.
- A convergência de comportamento exige validação cuidadosa dos testes
  hoje ligados a cada helper local, listados no levantamento.

### Artefatos afetados

| Artefato / família funcional afetada | Aplicação necessária |
|---|---|
| `docs/contratos/contrato_composicao_textual.md` | Criar como autoridade comportamental completa do mecanismo canônico (não criado nesta ADR). |
| Popup (autoridade local de wrap e de justificação de parágrafo) | Reconciliar essa autoridade local, semanticamente equivalente, com o mecanismo canônico (D-0027-01). |
| Conteúdo externo e seus consumidores (hierarquia, tabela, conjuntos de campos) | Migrar para comportamento de composição/wrap compatível com o mecanismo canônico; peculiaridades locais só são preservadas quando constituírem semântica necessária do consumidor (D-0027-03). Onde a apresentação deliberadamente exigir uma única linha, o truncamento correspondente permanece distinto de wrap/composição de parágrafo (D-0027-09). |
| Composição textual com conteúdo ANSI | Reconciliar com o mecanismo canônico, preservando a segurança ANSI já suportada (D-0027-04). |
| Matriz de participantes (console matricial verboso) | Migrar o consumo de wrap para o mecanismo canônico, preservando a fronteira local de indicadores/margens/`content_w` (D-0027-05). |
| Paginação interna e cálculo de mapa físico | Consumir a mesma autoridade canônica usada para renderizar, mantendo medição e renderização consistentes (D-0027-08). |
| Consumidores existentes que hoje acessam capacidades de renderização compartilhadas | Migrar para o mecanismo canônico, garantindo que esses consumidores continuem recebendo, após a reconciliação, as capacidades de renderização de que dependem. |
| `docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md`, `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` | Não alterados por esta ADR; eventual termo novo do mecanismo canônico é registrado como candidato ao módulo proprietário adequado somente durante a aplicação. |

A definição de qual módulo Python, API, assinatura, helper ou mecanismo de
reexportação implementará cada reconciliação acima pertence à aplicação
(`APLICAR_ADR`) e a eventual handoff futuro, não a esta ADR (ver §8).

## 6. Compatibilidade e transição

A aplicação é incremental e não é especificada executivamente por esta ADR.
O dimensionamento gerencial já calibrado pelo levantamento prevê dois
handoffs coesos — o mecanismo canônico com integração inicial do popup e
testes unitários fortes do núcleo, seguido da migração do caminho
compartilhado de conteúdo externo e dos consumidores correlatos com
regressão transversal —, mas nenhum handoff é criado nesta etapa. A
compatibilidade comportamental observável dos consumidores é preservada
exceto onde D-0027-03 determina convergência para o comportamento canônico.

## 7. Alternativas consideradas

| Alternativa | Motivo para rejeitar ou adiar |
|---|---|
| Introduzir uma fachada pública única sobre as implementações locais divergentes existentes, sem unificá-las | Rejeitada por D-0027-01: a finalidade do item é substituir as autoridades locais equivalentes, não apenas ocultá-las atrás de uma fachada. |
| Preservar automaticamente todas as peculiaridades de comportamento dos helpers locais atuais | Rejeitada por D-0027-03: peculiaridade histórica só é preservada quando representa semântica necessária de um consumidor real. |
| Estender o escopo do mecanismo canônico a padding/alinhamento de coluna, grade do lançador, chips e moldura de caixa | Rejeitada por D-0027-06: essas operações não são justificação de parágrafo e só entram no escopo mediante evidência objetiva de equivalência. |
| Aproveitar a criação do mecanismo canônico para alterar `corpo.arranjo`, `tiling`, paginação ou taxonomia de elementos funcionais | Rejeitada por D-0027-07: o item preserva integralmente a compatibilidade estrutural vigente. |

## 8. Itens fora de escopo

- Definição de nome de módulo Python, API pública, assinatura de função,
  classe, parâmetro ou algoritmo matemático específico do mecanismo
  canônico — pertence a handoff futuro de aplicação, salvo o já fechado
  pelas decisões D-0027-01 a D-0027-10.
- Criação do arquivo `docs/contratos/contrato_composicao_textual.md` —
  materializado durante `APLICAR_ADR` (D-0027-02).
- Alteração de `corpo.arranjo`, `tiling`, política de paginação, topologia
  `PageUp`/`PageDown`, schema de conteúdo, semântica dos dados, taxonomia
  dos elementos funcionais ou composição declarativa da tela (D-0027-07).
- Unificação de padding/alinhamento de coluna, preenchimento de célula,
  distribuição geométrica de chips, distribuição de grade do lançador ou
  moldura/preenchimento de caixa com o núcleo canônico (D-0027-06).
- Criação de handoffs, numeração de handoff ou especificação executiva de
  implementação — o dimensionamento gerencial em dois handoffs é
  informação de planejamento registrada em §6, não execução desta etapa.
- Alteração da nomenclatura vigente dos módulos `20` e `21` ou de qualquer
  outro módulo terminológico.
- Alteração de `docs/backlog.md`.

## 9. Critérios para aplicação

- [ ] A decisão foi propagada somente aos documentos afetados listados em
      §5.
- [ ] Não restaram duas autoridades locais independentes de wrap para a
      mesma responsabilidade semântica (D-0027-01).
- [ ] `docs/contratos/contrato_composicao_textual.md` foi criado como
      autoridade comportamental completa do mecanismo canônico
      (D-0027-02).
- [ ] Diferenças de comportamento preservadas correspondem a semântica
      necessária de consumidor real, com justificativa registrada
      (D-0027-03).
- [ ] Medição (altura, mapa físico, paginação) e renderização consomem
      comportamento compatível da mesma autoridade canônica (D-0027-08).
- [ ] Truncamento de linha única permanece distinguível de wrap/composição
      de parágrafo (D-0027-09).
- [ ] A composição recompõe o parágrafo lógico completo, distribui palavras
      inteiras em linhas e só depois justifica as linhas aplicáveis, sem
      hifenização, separação silábica ou divisão de palavras (D-0027-10).
- [ ] Resize recompõe a partir do texto lógico original, e uma palavra maior
      que a largura útil não é partida pelo compositor; seu tratamento físico
      permanece na representação ou no consumidor (D-0027-10).
- [ ] Nenhuma implementação de código foi feita durante esta etapa de
      criação documental.
- [ ] Caminhos permanecem relativos à raiz do Orquestrador.
- [ ] A execução de aplicação produziu relatório próprio em
      `docs/relatorios/`.
- [ ] A aplicação foi submetida a QA independente.

## 10. Bloqueios

Nenhum.
