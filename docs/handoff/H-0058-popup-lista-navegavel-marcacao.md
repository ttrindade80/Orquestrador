# H-0058 — Pop-up: lista navegável e marcação exclusiva/múltipla

## Identificação e fronteira

- Item: `ITEM-0017`.
- ADR: `ADR-0044-popup-modal-generico-de-decisao`.
- Handoff anterior fechado: `H-0057`.
- Baseline transportada: branch `master`, `HEAD f8064df`.
- Capacidade: terceira capacidade incremental da ADR-0044.

Este handoff materializa, em uma unidade executável, a extensão do pop-up
modal genérico para conteúdo de tipo `marcacao`: apresentação de lista plana,
cursor navegável, marcação `exclusiva` e marcação `multipla`. A configuração,
o envelope de conteúdo e o estado vivo continuam separados. O conteúdo chega
pronto; o pop-up não resolve produtor, origem, loader ou associação externa.

Não implementar neste handoff confirmação por `Enter`, `status: CONFIRMADO`,
payload confirmado, binding do resultado, interpretação pelo chamador ou ação
de negócio. O estado de cursor e marcações entregue aqui é provisório e
interno à instância; será somente consumido pela capacidade posterior H-0059.

A solução global de justificação continua deferida. Não criar justificação
local, não reabrir decisões da ADR-0044 e não registrar novo item de backlog.

## Autoridades aplicadas

Usar como fonte normativa fechada:

- `docs/adr/ADR-0044-popup-modal-generico-de-decisao.md`;
- `docs/contratos/contrato_popup.md`;
- `docs/nomenclatura/35_POPUP.md`;
- `tela/renderizacao/popup.py`;
- `tela/teste_popup.py`;
- `demo/teste_demo_popup.py`;
- `demo/fixtures/h0057_popup_texto_dinamico.py`;
- trechos materiais de `demo/demo.py` somente para o acionamento modal, o
  despacho de teclas, a renderização, o resize e o quadro de terminal pequeno;
- declarações existentes de pop-up e acionamentos em
  `config/telas/demo/demo.json`.

Não usar outros documentos para criar semântica. O caminho já existente de
`sobrepor_no_corpo` em `tela/renderizacao/tela.py` é o ponto de integração
da mesma instância com o corpo; só deve ser alterado se a extensão de
`PopupInstancia` exigir adaptação diretamente necessária à renderização.

## Semântica obrigatória

### Entrada e validação

Uma declaração de conteúdo de marcação usa `tipo: marcacao` e a política
declarada literalmente como `marcacao: exclusiva` ou `marcacao: multipla`.
Essa política pertence à declaração/configuração, não ao envelope runtime.
O envelope de entrada de marcação contém somente:

```yaml
tipo: marcacao
instrucao: "Escolha uma opção:"
itens:
  - id: opcao_1
    texto: "Opção 1"
  - id: opcao_2
    texto: "Opção 2"
marcados:
  - opcao_2
```

`instrucao` é obrigatória e não selecionável. `itens` é uma lista plana de
um único nível, com pelo menos um item. Cada item real tem ID estável e único;
o texto de cada item ocupa uma única linha física, sem wrapping, truncamento,
reticências ou paginação. O envelope aceita somente `tipo`, `instrucao`,
`itens` e `marcados`; campos desconhecidos, IDs ausentes/duplicados,
marcações inexistentes e cardinalidade inicial incompatível falham fechados
antes de materializar a instância. Marcações referenciam IDs, nunca índices
físicos.

Aplicar à instrução as regras de alinhamento e wrapping textual já vigentes;
ela permanece não selecionável. O espaçamento vertical normativo entre
instrução e itens, quando declarado para marcação, permanece no domínio
`0|1`, sem default arbitrário ou novo campo local.

Para `marcacao: exclusiva`, a entrada contém exatamente um ID em `marcados`.
Para `marcacao: multipla`, `marcados` admite zero a N IDs, inclusive lista
vazia. A configuração continua responsável por título, alinhamento,
espaçamentos, chips, modalidade e contrato; não copiar configuração para o
envelope.

### Formação visual e estado vivo

O conteúdo de marcação é composto depois do título e antes da área própria de
chips, coexistindo com moldura, texto da instrução e o chip `[Esc] Voltar` já
entregue. A instrução não participa do cursor. A apresentação tenta exatamente
nesta ordem: coluna, matriz, linha.

Na matriz, usar o menor número de colunas capaz de acomodar todos os itens,
preenchendo verticalmente por colunas e avançando da esquerda para a direita.
Não criar placeholders, itens em branco ou células vazias navegáveis. A
mudança de formação é somente física: ordem lógica, IDs, cursor e marcações
permanecem os mesmos.

O cursor inicial é o primeiro item real da ordem declarada. O cursor é
independente das marcações. O estado vivo deve preservar o item corrente e as
marcações por ID sem alterar declaração, envelope recebido ou tela
subjacente. O item corrente deve ter representação visual inequívoca, e a
marcação deve ter representação distinta, ambas compatíveis com o estilo
universal vigente; não hardcodar nova aparência, símbolo ou cor específica do
pop-up.

### Teclas e navegação

No runtime demonstrativo vigente, as teclas físicas chegam como `\x1b[A`
(`↑`), `\x1b[B` (`↓`), `\x1b[C` (`→`), `\x1b[D` (`←`), espaço
(` `) e `\x1b` (`Esc`). Manter essa entrada e a captura modal antes da
tela subjacente.

A navegação é toroidal por eixo, sem compensação entre eixos, salto diagonal
ou busca pelo item mais próximo:

- coluna: `↑/↓` percorrem o toroide; `←/→` resultam em `SEM_MOVIMENTO`;
- linha: `←/→` percorrem o toroide; `↑/↓` resultam em `SEM_MOVIMENTO`;
- matriz: os eixos horizontal e vertical são toroides independentes;
- eixo sem outro item ocupado resulta em `SEM_MOVIMENTO`;
- células vazias não recebem cursor nem participam do toroide.

### Marcação

Em `marcacao: exclusiva`, mantém-se exatamente uma marcação válida. Espaço
sobre item diferente transfere a marcação; espaço sobre o item já marcado
resulta em `SEM_MUDANCA`; mover o cursor não muda a marcação.

Em `marcacao: multipla`, espaço alterna a marcação do item corrente. Zero a N
itens podem permanecer marcados; desmarcar o item corrente é permitido. A
ordem lógica declarada, e não a ordem temporal das teclas, governa as
marcações mantidas no estado.

### Resize, modalidade e saída

Reutilizar a geometria dinâmica, wrapping de texto, distribuição de chips,
centralização no corpo, restauração e política de terminal pequeno vigentes
em H-0057. Resize e recomposição preservam ou reconciliam para estado válido
o cursor e as marcações pelos IDs. A mesma instância permanece aberta; não
reabrir, fechar, trocar modalidade, alterar configuração ou perder marcações.

Toda tecla continua capturada enquanto o pop-up existir. `Esc` continua
fechando a mesma modalidade e produzindo exatamente `{"status": "ABORTADO"}`
sem `valor` ou outro payload. Uma tecla `Enter` (`\r` ou `\n`) não
confirma, não fecha, não produz resultado externo e não executa ação nesta
etapa.

## Arquivos e superfícies autorizados

### Alteráveis

- `tela/renderizacao/popup.py`: validação do tipo `marcacao`, estado vivo da
  instância, composição da lista, navegação, marcações e renderização; manter
  integralmente o caminho textual já entregue.
- `tela/renderizacao/tela.py`: somente adaptação diretamente necessária para
  sobrepor a instância expandida; preservar composição, cálculo da área do
  corpo, centralização e restauração.
- `tela/teste_popup.py`: testes focais estruturais do renderer, validação,
  estado, navegação, marcação, resize e regressão textual.
- `demo/demo.py`: somente importação/uso da fixture H-0058, resolução dos
  novos IDs demonstrativos e encaminhamento modal; preservar a captura
  modal, a tela subjacente, o resize e o caminho de `Esc`.
- `demo/teste_demo_popup.py`: testes estruturais do acionamento, instância,
  renderização, resize, marcação interna, `Esc` e ausência de confirmação.
- `config/telas/demo/demo.json`: somente declarações e acionamentos
  demonstrativos estritamente necessários para uma configuração exclusiva e
  uma múltipla; preservar `popup_basico`, `popup_texto_dinamico`, seus
  chips, seus textos e seus acionamentos.

### Fixture, configuração e runtime

- Criar `demo/fixtures/h0058_popup_lista_marcacao.py` como fixture
  determinista de conteúdo pronto. Ela deve fornecer, em cada envelope, os
  seis itens de uma lista plana com IDs `opcao_1` a `opcao_6`, textos
  distintos em uma linha e a instrução correspondente. O envelope exclusivo
  deve iniciar com `marcados: [opcao_2]`; o múltiplo deve iniciar com
  `marcados: [opcao_2, opcao_4]`. Usar funções de fixture separadas para os
  dois envelopes, sem confirmação ou execução de negócio.
- Na configuração demonstrativa, adicionar duas declarações de pop-up usando
  as políticas literais `marcacao: exclusiva` e `marcacao: multipla`, cada
  uma com o chip de `Esc` já normatizado. Adicionar dois acionamentos simples
  de demonstração, `e` para a declaração exclusiva e `m` para a múltipla,
  usando o formato existente `tipo: popup`, `tecla`, `popup`. Essas teclas
  só abrem a demonstração; não redefinem as teclas de navegação ou marcação.
- O runtime de abertura deve selecionar a fixture pelo ID resolvido, manter o
  envelope imutável e preservar na instância o cursor e as marcações
  provisórias por ID. Não persistir esse estado no JSON.
- Saída observável: lista, instrução, item corrente, marcas, moldura, chips,
  resize e retorno `ABORTADO` sem payload. Não há temporário de repositório
  previsto ou autorizado para esta capacidade.

### Preservados e fora da autorização

Preservar os arquivos e comportamentos não listados como alteráveis, em
especial o fixture `demo/fixtures/h0057_popup_texto_dinamico.py`, o pop-up
textual básico, a geometria/wrapping/resize de H-0057, a tela subjacente, a
modalidade, o quadro de terminal pequeno e a justificação deferida. Não criar
ou alterar ADR, contrato, nomenclatura, backlog, produtor de conteúdo,
integração de negócio, binding, payload confirmado, ação, outro fixture ou
outro módulo por conveniência.

## Testes focais reproduzíveis

Executar a partir da raiz do projeto:

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_popup.py demo/teste_demo_popup.py
PYTHONDONTWRITEBYTECODE=1 python -m pytest
```

O executor deve acrescentar testes determinísticos, sem TTY real, que
comprovem:

1. envelope `marcacao` válido com lista simples renderiza instrução, itens,
   foco, marcações, moldura e chips, sem truncar itens;
2. foco inicial é o primeiro item real da ordem declarada;
3. coluna, matriz e linha obedecem os limites toroidais e `SEM_MOVIMENTO` nos
   eixos inativos, sem cursor em célula vazia;
4. espaço em modo exclusivo mantém uma marcação, transfere para item
   diferente e retorna `SEM_MUDANCA` no item já marcado;
5. espaço em modo múltiplo marca, desmarca quando previsto e mantém a ordem
   declarada dos IDs;
6. mover cursor não altera marcação e marcação não altera foco;
7. recomposição/resize estreito e retorno a dimensões suficientes preservam a
   mesma instância e reconciliam foco/marcações válidos por ID;
8. terminal pequeno usa o quadro geral vigente e, ao recuperar dimensões,
   restaura o pop-up sem reabrir e sem perder estado;
9. `Esc` continua produzindo somente `{"status": "ABORTADO"}` e nenhum
   `valor`;
10. o pop-up somente textual de H-0056 e o cenário dinâmico de H-0057
    continuam aprovados;
11. `\r` e `\n` enquanto a lista está aberta não confirmam, não fecham,
    não produzem `CONFIRMADO`/payload e não executam ação.

Não declarar como teste automático uma verificação que exija TTY real. A
observação interativa fica na demonstração abaixo.

## Demonstração em TTY real

Usar a execução vigente da demo, sem modo de confirmação de negócio, com a
fixture `demo/fixtures/h0058_popup_lista_marcacao.py` e os dois acionamentos
adicionados em `config/telas/demo/demo.json`. O cenário deve permitir ao
usuário:

- abrir uma lista com quantidade suficiente de opções para ver o foco mudar;
- percorrer os limites conforme coluna, matriz ou linha determinada pela
  largura corrente;
- observar a transferência exclusiva e a alternância múltipla com espaço;
- observar simultaneamente instrução, itens, moldura e `[Esc] Voltar`;
- redimensionar, ver a recomposição e recuperar a mesma instância e estado;
- pressionar `Esc` e retornar à tela subjacente com `ABORTADO` sem payload.

O roteiro não deve usar `Enter` para confirmar, não deve criar resultado
confirmado e não deve executar ação de negócio. A fixture é conteúdo pronto,
não produtor.

## Critérios de aceite

1. Dado uma declaração `tipo: marcacao` e envelope com `instrucao`, pelo
   menos um item real e campos permitidos, ao abrir o pop-up a instância é
   criada com lista plana renderizável; o título, texto, moldura e chips
   continuam presentes.
2. Dada uma lista válida, antes de qualquer tecla o item corrente é o
   primeiro ID da ordem declarada e sua representação visual é inequívoca.
3. Dada a formação coluna, ao pressionar `↑` ou `↓` o cursor percorre os
   itens de modo toroidal; ao pressionar `←` ou `→` o cursor não muda e o
   movimento interno é `SEM_MOVIMENTO`.
4. Dada a formação linha, ao pressionar `←` ou `→` o cursor percorre os
   itens de modo toroidal; ao pressionar `↑` ou `↓` o cursor não muda e o
   movimento interno é `SEM_MOVIMENTO`.
5. Dada a formação matriz, ao pressionar setas o eixo correspondente percorre
   seu toroide independente, sem entrar em célula vazia ou compensar o outro
   eixo.
6. Dada a política `marcacao: exclusiva` com uma marcação inicial válida,
   ao mover o cursor a marcação permanece; ao pressionar espaço sobre item
   diferente, exatamente esse item passa a ser o marcado.
7. Dada a política `marcacao: exclusiva` com o cursor sobre o item já
   marcado, ao pressionar espaço o estado permanece sem mudança
   (`SEM_MUDANCA`).
8. Dada a política `marcacao: multipla`, ao pressionar espaço sobre item não
   marcado ele passa a marcado; ao pressionar espaço novamente no mesmo item
   ele é desmarcado; a lista interna permanece na ordem declarada.
9. Dada uma recomposição por resize, o envelope não muda, a mesma instância
   permanece aberta e cursor/marcações continuam IDs válidos, inclusive após
   retorno à dimensão anterior.
10. Dado um terminal pequeno, o quadro mínimo vigente é usado sem paginação,
    truncamento, remoção de chips ou perda de estado; com espaço suficiente,
    a mesma instância volta a ser representada.
11. Dado o pop-up aberto, ao pressionar `Esc` ele fecha e o único resultado
    é `{"status": "ABORTADO"}`, sem chave `valor`; a tela subjacente volta
    a receber interação.
12. Dado o pop-up textual de H-0056 ou o dinâmico de H-0057, as operações de
    abertura, renderização, wrapping, resize, instância, `Esc` e
    `ABORTADO` mantêm os resultados já entregues.
13. Dado o pop-up de marcação aberto, ao pressionar `\r` ou `\n` a
    instância permanece aberta, sem `CONFIRMADO`, payload, binding ou ação
    de negócio.
14. Dada configuração/envelope inválidos — campo desconhecido, lista vazia,
    ID ausente/duplicado/inexistente ou cardinalidade incompatível — a
    abertura falha fechada antes da interação e não cria estado parcial.

## Entrega e relatório da implementação futura

Além dos arquivos autorizados acima, o executor futuro deve criar somente o
relatório:

`docs/relatorios/IMP-0058-popup-lista-navegavel-marcacao.md`

Com teto normal de 900 palavras, esse relatório deve registrar somente:
arquivos criados/alterados, comportamento entregue, testes executados,
demonstração, desvios, exceções e bloqueios. Não registrar nele confirmação,
payload ou ação como entregues se permanecerem na fronteira H-0059.
