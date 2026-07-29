---
name: ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento
description: "Define seleção múltipla por IDs estáveis, consumo por operação focal do binding, protocolo provisório de execução com resultado estruturado e tela padrão de resultado reutilizável, organizados em quatro handoffs sequenciais"
metadata:
  type: adr
  status: aceita
  id: ADR-0034
  data: 2026-07-28
  substitui: null
rastreabilidade:
  decisao_usuario: "D-SEL-01 a D-SEL-26 — seleção múltipla por conjunto de IDs estáveis, ordem lógica e reconciliação, teclas/indicadores/chips, universo de \"Todos\" sobre o conjunto filtrado, operação consumidora do binding com fronteira ao registry genérico (ITEM-0004), protocolo provisório de entrada/execução via CLI, resultado estruturado com canais separados, classificação de sucesso/falha, envelope de erro multinível preservando texto inválido literal, tela padrão de resultado (perfil resultado_execucao), validação antecipada, fluxo focal de abertura/retorno, dry-run e execução real reversível com restauração automática, paginação da tela de resultado deferida, decomposição em quatro handoffs (H1 estado/comandos, H2 protocolo/execução, H3 tela padrão, H4 integração), fixture obrigatória de oito itens do Handoff 1 e critérios de aplicação documental"
  rfc_origem: null
  issues_relacionadas:
    - ITEM-0006
  contratos_afetados:
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_json_console.md
  handoffs_bloqueados: []
---

# ADR-0034 — Seleção múltipla e fluxo focal de processamento

## 1. Status

`aceita`

## 2. Contexto

A ADR-0030 concluiu o Bloco 1 (carregamento global e materialização do
estilo). A ADR-0031 concluiu o Bloco 2 (navegação simples e seleção única em
console de nível único), registrando explicitamente que `[␣]`, os
indicadores de inclusão (`tg` com `●`/`○`) e a execução de ação por `[⏎]`
sobre um conjunto marcado pertencem ao Bloco 3 — seleção múltipla — e ficam
fora do escopo da ADR-0031 (ADR-0031 D13, D15). O backlog registra essa
lacuna como `ITEM-0006 — Seleção múltipla no console`, com pré-requisito
"navegação simples e seleção única concluídas; ações declarativas
formalizadas quando necessárias".

Os contratos ativos já preveem a existência estrutural da política de
seleção múltipla (`contrato_console.md` §8; `contrato_json_console.md` §5;
`contrato_barra_de_menus.md` §12), mas não fecham: a identidade e a
persistência do conjunto selecionado como estado de runtime; a ordem de
execução sobre esse conjunto; a reconciliação do conjunto após atualização
dos dados; a semântica operacional de `Espaço`, `Enter` e `Esc` quando há
seleção; a fronteira entre a operação consumidora do lote e o registry
genérico de ações declarativas ainda não fechado (`ITEM-0004`, DOC-B009); um
protocolo de entrada e saída para testar essa operação de forma focal; a
classificação de sucesso e falha de um processo externo invocado a partir do
console; o formato do envelope de erro quando o processo falha ou produz
resultado inválido; e a existência de uma tela padrão reutilizável para
apresentar esse resultado.

Este documento registra as decisões fechadas fornecidas para essas lacunas.
Não introduz arquitetura, schema definitivo, política ou protocolo além do
que está explicitamente decidido, e organiza a implementação em quatro
handoffs sequenciais, cada um funcional, testável, documentado e aprovado em
QA antes do início do próximo.

---

## 3. Decisão explícita do usuário

### D-SEL-01 — Estado e identidade da seleção

A seleção múltipla:

- é estado de runtime da sessão — não é persistida no JSON estrutural da
  tela;
- é armazenada como conjunto de IDs estáveis;
- é independente por console;
- persiste entre páginas e quando um filtro apenas oculta itens;
- não persiste entre sessões;
- é descartada ao sair ou recarregar a tela, salvo as regras focais de
  retorno após operação definidas em D-SEL-19 e D-SEL-20;
- é um snapshot de IDs, não uma consulta dinâmica — não incorpora
  automaticamente itens criados depois de um acionamento de "selecionar
  todos".

### D-SEL-02 — Invariantes de seleção

- Todo item selecionável deve ser navegável; item não navegável não pode ser
  selecionável.
- A seleção ativa contém somente IDs existentes, navegáveis e selecionáveis.
- Cursor e seleção são estados distintos: `ec` indica exclusivamente o
  cursor; `tg` indica exclusivamente a inclusão ou não inclusão na seleção.
- Posição visual, página, filtro e ordem de marcação não definem identidade
  nem ordem de execução do conjunto selecionado.

### D-SEL-03 — Ordem e reconciliação da entrada da operação

A entrada da operação consumidora é uma lista sem duplicatas, ordenada pela
ordem lógica estável do console.

Antes da execução e após atualização dos dados:

- remover IDs que não existem mais;
- remover itens que deixaram de ser selecionáveis;
- executar somente os IDs válidos restantes;
- preservar a ordem lógica do console.

### D-SEL-04 — Reconciliação vazia após `Enter`

Quando havia seleção antes de `Enter`, mas a reconciliação a torna vazia:

- não executar;
- não aplicar "selecionar todos" no mesmo acionamento;
- deixar a seleção vazia;
- o próximo `Enter`, já sem seleção, assume a função `Todos` (D-SEL-06).

### D-SEL-05 — Tecla `Espaço`

`Espaço`:

- alterna a inclusão do item atual na seleção;
- não move o cursor;
- não produz efeito em item não selecionável.

### D-SEL-06 — `Enter` sem seleção (`Todos`)

`Enter` sem seleção:

- exibe chip com rótulo `Todos`;
- seleciona todos os itens selecionáveis do conjunto filtrado;
- alcança todas as páginas do conjunto filtrado;
- produz snapshot de IDs (D-SEL-01);
- quando não há item selecionável, o chip permanece visível e inativo.

### D-SEL-07 — `Enter` com seleção (`Executar`)

`Enter` com seleção:

- exibe chip com rótulo `Executar`;
- executa a operação consumidora declarada pelo binding (D-SEL-12);
- no Handoff 1 (D-SEL-22), permanece inativo porque ainda não existe
  operação externa.

### D-SEL-08 — `Esc`

`Esc`:

- com seleção ativa: o primeiro acionamento limpa a seleção e permanece na
  tela;
- sem seleção, na tela raiz: sai;
- sem seleção, nas demais telas: volta.

### D-SEL-09 — Indicadores e chip `Espaço`

Indicadores:

- `ec` aparece somente no item sob cursor;
- `tg` mostra o símbolo do estilo para selecionável incluído ou não incluído;
- `tg` fica vazio em item não selecionável.

Chip `Espaço`:

- existe quando o console suporta seleção múltipla;
- fica ativo quando o item atual é selecionável;
- fica inativo quando o item atual não é selecionável.

### D-SEL-10 — Universo de `Todos`, filtro e paginação

O universo de "Todos" é composto pelos itens selecionáveis do conjunto
filtrado, incluindo todas as páginas.

Alterar o filtro:

- altera visibilidade;
- não remove IDs já selecionados;
- não limita posteriormente a execução de uma seleção já formada.

A semântica de seleção entre páginas pertence a esta ADR, mas paginação
interativa não será implementada nem provada neste ciclo — permanece
responsabilidade do `ITEM-0003`.

### D-SEL-11 — Operação consumidora e fronteira com ações genéricas

A operação pertence ao binding ou à origem de dados consumida pelo console.
Ela não pertence ao renderer, à instância do console como regra global, nem
implicitamente à tela inteira.

Entrada da operação:

```yaml
tipo: lista_ordenada_de_ids_reconciliados
ids_duplicados: proibidos
lista_vazia: proibida
objetos_completos: não_transportados
```

O protocolo do `ITEM-0006` é mínimo, fechado e focal. Permanecem fora desta
ADR: registry genérico de ações, dispatcher genérico, catálogo genérico de
ações e comandos arbitrários declarados no JSON — essas responsabilidades
permanecem no `ITEM-0004`.

### D-SEL-12 — Protocolo provisório de entrada e execução

Para os testes focais deste ciclo:

```yaml
arquivo_de_entrada:
  meio: arquivo_JSON_temporario
  schema: selecao_execucao.v1
  campos_obrigatorios:
    - schema
    - ids

CLI:
  entrada: --entrada <arquivo-selecao.json>
  resultado: --resultado <arquivo-resultado.json>
  execucao_real:
    padrao: true
    flag_adicional: ausente
  dry_run:
    opcional: true
    flag: --dry-run
```

O protocolo é provisório. Contratos futuros de binding, script e
processamento podem redefinir seus nomes e detalhes sem reabrir o núcleo da
seleção múltipla (D-SEL-01 a D-SEL-10).

### D-SEL-13 — Resultado estruturado e canais do processo

O Orquestrador:

- cria previamente um arquivo JSON temporário de resultado;
- fornece explicitamente seu caminho ao script;
- mantém `stdout` e `stderr` como canais textuais separados;
- não interpreta `stdout` como documento JSON de resultado.

O arquivo é validado uma vez na entrada da tela de resultado e convertido
para modelo em memória. Redesenho e `SIGWINCH` não relêem o arquivo —
recalculam somente a representação física. O arquivo temporário deve ser
removido ao voltar por `Esc` e em encerramento anormal.

### D-SEL-14 — Classificação do processo

Sucesso exige simultaneamente: código de saída `0` e JSON de resultado
válido.

Conteúdo em `stderr` com código `0` não altera a classificação e não é
incorporado automaticamente ao resultado.

Código não zero é falha mesmo quando existe JSON válido; o JSON válido é
preservado no envelope de erro; não pode ser apresentado como sucesso.

Resultado ausente, malformado ou semanticamente inválido não é entregue
diretamente ao renderer — gera envelope de erro válido produzido pelo
Orquestrador e abre a mesma tela padrão de resultado.

### D-SEL-15 — Envelope de erro

O envelope é multinível, apresentado como `conjuntos_campos`, com ordem
fixa:

```yaml
campos:
  - status
  - diagnostico
  - codigo_saida
  - stdout
  - stderr
  - resultado_json
```

Quando indisponível, `resultado_json` recebe `null`, visualizado como
`indisponível`.

Quando existir texto inválido produzido pelo script, `resultado_json` deve
preservar exatamente espaços, quebras de linha, ordem de chaves e indentação
originais. É permitido somente o escape necessário para transportar esse
texto como string JSON. É proibido corrigir o JSON, normalizar ou
reserializar o texto, inferir intenção do produtor, ou reinterpretar
resultado inválido.

### D-SEL-16 — Tela padrão de resultado

A tela de resultado:

- é um `tela.json` estático e preconstruído;
- é reutilizável por múltiplas telas e scripts;
- possui ID declarado explicitamente pelo binding;
- não é criada dinamicamente em runtime.

Novo campo raiz opcional compatível com `tela.v1`:

```yaml
campo: perfil
valor: resultado_execucao
valor_desconhecido: CONFIGURACAO_INVALIDA
```

Estrutura obrigatória do perfil:

```yaml
consoles: 1
outros_elementos_funcionais: proibidos
console_navegavel: false
politica_selecao: nenhuma
politica_modo: somente_verboso
origem_do_conteudo: runtime
chips_permitidos:
  - Esc_voltar
abrir_outra_tela: proibido
iniciar_nova_execucao: proibido
```

Apresentações aceitas: `tabela`, `hierarquia`, `conjuntos_campos`.

A tela mostra integralmente o resultado, não possui chip `V`, e não possui
modo não verboso ou alternável neste ciclo.

### D-SEL-17 — Validação antecipada

No carregamento da configuração, o Orquestrador valida: existência do
`tela_resultado_id`; validade do schema; referências; presença do perfil
`resultado_execucao`; compatibilidade estrutural com o perfil.

Destino ausente ou inválido:

```yaml
classificacao: CONFIGURACAO_INVALIDA
disponibilizar_tela_de_execucao: false
iniciar_operacao: false
```

O renderer não infere o ID da tela e não cria uma tela substituta.

### D-SEL-18 — Fluxo focal de abertura e retorno

Fluxo fechado do ciclo:

```text
tela de execução
→ tela de resultado
→ retorno para a instância que abriu o resultado
```

Neste ciclo: existe somente uma origem suspensa; não há pilha genérica de
telas; o JSON compartilhado da tela de resultado não fixa a tela de retorno.

Enquanto a tela de resultado está aberta, preservar na origem: filtro,
página, cursor e foco.

Retorno por `Esc` após `dry-run`: não recarrega a origem; preserva a
seleção.

Retorno após execução real: limpa a seleção em sucesso, falha parcial, erro
ou interrupção; recarrega os dados do binding; preserva o filtro; preserva o
mesmo item sob cursor quando seu ID continuar válido; caso contrário,
posiciona o cursor no primeiro item navegável.

A pilha genérica, abertura e retorno genéricos permanecem no `ITEM-0005`.

### D-SEL-19 — Dry-run, execução real e restauração

`dry-run`: não altera dados; não limpa a seleção; preserva a seleção para
uma execução real posterior.

Execução real reversível da demonstração: altera fixture controlada;
restaura automaticamente a fixture ao encerrar; restaura também em erro ou
`KeyboardInterrupt`; nunca deixa a fixture contaminada.

A escolha entre cenários é declarativa. Não existe chip de alternância entre
execução real e `dry-run` neste ciclo.

Interrupção: produz resultado estruturado; devolve o controle ao TUI; em
execução real, limpa a seleção.

### D-SEL-20 — Paginação da tela de resultado

A arquitetura futura admite controles condicionais de página anterior e
próxima. Neste ciclo: não implementar paginação da tela de resultado; todas
as fixtures de resultado devem caber integralmente em uma página; a
dimensão lógica automatizada de referência é `80x24`; usar a área útil real
do console na tela completa; fixture que exceda a área é inválida e deve
falhar no teste; não truncar, omitir conteúdo nem criar fallback temporário.

A validação manual poderá ocorrer em terminal `1920x1200` em tela cheia, mas
o aceite automatizado continua em `80x24`.

### D-SEL-21 — Decomposição em quatro handoffs sequenciais

**Handoff 1 — estado, comandos e apresentação da seleção.** Entrega: estado
por IDs; alternância por `Espaço`; `Todos`; limpeza por `Esc`;
reconciliação; ordenação lógica; indicadores `ec` e `tg`; estados e rótulos
dos chips. Não há operação externa. `Enter` sem seleção ativa `Todos`
quando aplicável; `Enter` com seleção exibe `Executar` visível, porém
inativo. É proibido criar operação provisória para simular o Handoff 2.

**Handoff 2 — protocolo focal do binding e execução.** Entrega: entrada
focal; invocação direta do protocolo; `dry-run`; execução real reversível;
resultado estruturado; restauração protegida. O chip `Executar` continua
inativo na interface.

**Handoff 3 — tela padrão e integração da interface.** Entrega: tela JSON
estática; perfil `resultado_execucao`; carregamento do JSON externo;
envelope de erro; abertura da tela; retorno por `Esc`; ativação na
interface dos cenários `dry-run` e execução real reversível.

**Handoff 4 — integração e validação completa.** Entrega: selecionar;
executar; exibir; voltar; cenários completos de `dry-run` e execução real;
restauração automática; testes integrados.

Cada handoff deve ser funcional, testável, documentado e aprovado em QA. É
proibido iniciar o handoff seguinte com baseline quebrada, deixar regressão
conhecida para correção no Handoff 4, ou usar código provisório no Handoff 1
para simular operação externa.

### D-SEL-22 — Fixture focal obrigatória do Handoff 1

```yaml
fixture:
  exclusiva_do_ITEM_0006: true
  altera_cenarios_existentes: false
  depende_de_script_binding_filtro_ou_paginacao: false
  cursor_inicial: item_01
  selecao_inicial: vazia
```

Itens, na ordem lógica:

```yaml
- id: item_01
  texto: item_01 — Selecionável 1
  navegavel: true
  selecionavel: true

- id: item_02
  texto: item_02 — Navegável não selecionável 1
  navegavel: true
  selecionavel: false

- id: item_03
  texto: item_03 — Selecionável 2
  navegavel: true
  selecionavel: true

- id: item_04
  texto: item_04 — Não navegável 1
  navegavel: false
  selecionavel: false

- id: item_05
  texto: item_05 — Selecionável 3
  navegavel: true
  selecionavel: true

- id: item_06
  texto: item_06 — Navegável não selecionável 2
  navegavel: true
  selecionavel: false

- id: item_07
  texto: item_07 — Selecionável 4
  navegavel: true
  selecionavel: true

- id: item_08
  texto: item_08 — Não navegável 2
  navegavel: false
  selecionavel: false
```

Ordem dos alvos de navegação: `item_01 → item_02 → item_03 → item_05 →
item_06 → item_07`.

Resultado de `Todos`: `item_01, item_03, item_05, item_07`.

Itens não navegáveis permanecem visíveis, não recebem cursor e apresentam
`tg` vazio.

### D-SEL-23 — Testes previstos para o Handoff 1

Testes automatizados unitários: estado da seleção por IDs; toggle de item;
selecionar todos; limpeza por `Esc`; reconciliação; ordenação lógica;
exclusão de itens não selecionáveis.

Testes automatizados de integração: modelo com a fixture de oito itens
(D-SEL-22); estado dos chips; indicadores `ec` e `tg`; transição do rótulo
`Todos` para `Executar`.

Teste manual em TTY real: roteiro fechado e sequencial; para cada etapa,
registrar tecla acionada, item em foco, seleção esperada, indicadores
esperados, estado dos chips e resultado observado.

Ficam fora da automação do Handoff 1: quadro TTY completo; sequências ANSI;
filtro; paginação.

### D-SEL-24 — Aplicação documental futura

A aplicação documental desta ADR deve: atualizar os contratos afetados;
atualizar somente os módulos proprietários da nomenclatura; atualizar o
índice de ADRs; atualizar o backlog quando material; registrar o
`delta_terminologico`; não implementar código; não criar handoff na mesma
etapa.

Novos itens bloqueados a registrar na aplicação, sem reservar número
antecipadamente:

1. `Selecionar todos apenas na página atual` — permitir limitar a seleção em
   massa aos itens selecionáveis da página corrente.
2. `Seleção compartilhada entre consoles compatíveis` — permitir um conjunto
   de seleção comum entre consoles que exibam dados compatíveis.
3. `Chip de escolha entre execução real e dry-run` — permitir escolher na
   interface o modo da operação vinculada.
4. `Modos de visualização das telas de resultado` — permitir telas somente
   verbosas, somente não verbosas ou alternáveis.

O colapso de resultado multinível permanece absorvido pelo `ITEM-0007` e não
gera novo item.

Responsabilidades já existentes que não podem ser duplicadas:

```yaml
ITEM-0003: paginação interativa, inclusive da tela de resultado
ITEM-0004: registry, dispatcher e catálogo genérico de ações
ITEM-0005: abertura, retorno e pilha genéricos
ITEM-0007: colapso e expansão de conteúdo multinível
```

### D-SEL-25 — Compatibilidade e deltas explícitos

Esta ADR declara explicitamente:

- especialização de `Enter` sem seleção como `Todos` (D-SEL-06);
- especialização de `Enter` com seleção como execução da operação focal do
  binding (D-SEL-07, D-SEL-11);
- compatibilidade do novo campo opcional `perfil: resultado_execucao` com
  `tela.v1` (D-SEL-16);
- uso de console passivo, não navegável e somente verboso na tela padrão
  (D-SEL-16);
- preservação da distinção entre configuração concreta e estado de runtime
  (D-SEL-01);
- preservação da distinção entre JSON estrutural da tela e JSON externo de
  conteúdo (ADR-0026, ADR-0027);
- preservação da lista fechada de elementos funcionais (ADR-0010,
  ADR-0015);
- tela de processamento como composição, não como novo tipo de elemento
  (ADR-0007);
- ausência de comandos arbitrários no JSON (D-SEL-11);
- ausência de inferência de operação ou tela pelo renderer (D-SEL-17).

### D-SEL-26 — Itens fora de escopo declarados pelo usuário

Ficam nominalmente fora de escopo desta ADR: registry e dispatcher
genéricos de ações; catálogo genérico de ações; protocolo definitivo de
binding, script e processamento; pilha genérica de telas; paginação
interativa; prova de persistência entre páginas; filtro na fixture do
Handoff 1; seleção compartilhada entre consoles; chip de alternância entre
`dry-run` e execução real; modos não verboso ou alternável na tela padrão;
colapso e expansão multinível; correção automática de JSON inválido;
comandos arbitrários declarados no JSON. Hipóteses descartadas nestas
decisões não são reinterpretadas como alternativas vigentes.

---

## 4. Decisão

Fica adotado, para o `ITEM-0006`, um modelo de seleção múltipla e fluxo
focal de processamento organizado em cinco camadas:

**Estado e identidade da seleção (D-SEL-01 a D-SEL-10).** A seleção é
conjunto de IDs estáveis, estado de runtime, independente por console,
reconciliado contra os dados vigentes antes de qualquer execução. `Espaço`
alterna a inclusão do item em foco sem mover o cursor; `Enter` assume o
rótulo `Todos` quando não há seleção e `Executar` quando há; `Esc` limpa a
seleção antes de assumir o comportamento de navegação da tela. Os
indicadores `ec` (cursor) e `tg` (inclusão) permanecem semanticamente
distintos, conforme já estabelecido pela ADR-0031 para o cursor e formalizado
aqui para a inclusão.

**Operação consumidora e fronteira com ações genéricas (D-SEL-11).** A
execução sobre o conjunto selecionado é responsabilidade do binding ou da
origem de dados do console — nunca do renderer, da instância genérica do
console ou da tela como um todo. O protocolo desta ADR é mínimo e focal;
não introduz registry, dispatcher ou catálogo genérico de ações, que
permanecem no `ITEM-0004`.

**Protocolo provisório, resultado estruturado e classificação
(D-SEL-12 a D-SEL-15).** Para os testes deste ciclo, a operação é invocada
por CLI com arquivo de entrada `selecao_execucao.v1` e arquivo de resultado
fornecido pelo Orquestrador. `stdout` e `stderr` são canais textuais nunca
interpretados como o documento de resultado. A classificação de sucesso
exige simultaneamente código de saída `0` e JSON de resultado válido; texto
inválido produzido pelo processo é preservado literalmente no envelope de
erro multinível de campos fixos, sem correção nem reinterpretação.

**Tela padrão de resultado e validação antecipada (D-SEL-16 e D-SEL-17).**
A apresentação do resultado usa uma tela `tela.json` estática e reutilizável,
identificada por um novo campo opcional `perfil: resultado_execucao`
compatível com `tela.v1`, cujo perfil obrigatório restringe o corpo a um
único console passivo, não navegável, somente verboso, sem seleção e com
o único chip `Esc voltar`. A validade do destino é verificada no
carregamento da configuração, antes de qualquer operação ser iniciada;
configuração inválida bloqueia a disponibilização da tela de execução.

**Fluxo focal, dry-run, execução real e restauração (D-SEL-18 a D-SEL-20).**
O ciclo de abertura é fechado: execução → resultado → retorno à origem que
abriu, sem pilha genérica de telas. `dry-run` preserva dados e seleção;
execução real reversível altera e restaura automaticamente uma fixture
controlada, inclusive sob interrupção, e limpa a seleção ao retornar. A
paginação da tela de resultado não é implementada neste ciclo; fixtures de
resultado devem caber na dimensão lógica de referência `80x24`.

A implementação desta decisão é decomposta em quatro handoffs sequenciais
(D-SEL-21): Handoff 1 (estado, comandos e apresentação da seleção, sem
operação externa), Handoff 2 (protocolo focal e execução, chip `Executar`
ainda inativo na interface), Handoff 3 (tela padrão e integração da
interface) e Handoff 4 (integração e validação completa). O Handoff 1 é
obrigatoriamente demonstrado pela fixture fechada de oito itens de
D-SEL-22, com os testes mínimos de D-SEL-23.

Esta decisão não altera nenhuma regra de navegação, foco, cursor ou seleção
única já fechada pela ADR-0031, nem as regras de apresentação e modo
verboso/não verboso já fechadas pela ADR-0028, nem a separação entre JSON
estrutural e conteúdo externo já fechada pelas ADR-0026 e ADR-0027.

---

## 5. Consequências

### Positivas

- Fecha a lacuna operacional deixada explicitamente pela ADR-0031 (D13,
  D15) para seleção múltipla, permitindo o encerramento do `ITEM-0006`.
- Define uma fronteira clara e estável entre a operação consumidora focal
  do `ITEM-0006` e o registry genérico de ações ainda não fechado
  (`ITEM-0004`), evitando que a implementação deste ciclo antecipe decisões
  pendentes de outro item.
- Estabelece um protocolo mínimo e testável de execução externa (entrada
  JSON, resultado JSON, canais textuais separados) sem comprometer o
  protocolo definitivo de binding/script/processamento a decisões futuras.
- Introduz uma tela padrão de resultado reutilizável, reduzindo a
  necessidade de telas ad hoc por script ou cenário.
- Formaliza classificação determinística de sucesso/falha e preservação
  literal de resultado inválido, evitando heurísticas de correção
  silenciosa de JSON malformado produzido por processos externos.
- Decompõe a entrega em quatro handoffs incrementais, cada um com critério
  próprio de aprovação, reduzindo o risco de regressão acumulada.

### Custos e restrições

- Exige que a fixture de oito itens do Handoff 1 (D-SEL-22) seja criada e
  mantida como artefato exclusivo do `ITEM-0006`, sem contaminar cenários
  existentes.
- Introduz um segundo campo raiz opcional (`perfil`) no schema de
  `tela.json`, que os validadores de configuração precisarão reconhecer
  antes que a tela de resultado possa ser disponibilizada.
- Exige que o Orquestrador crie, referencie e remova de forma confiável um
  arquivo temporário de resultado por execução, incluindo em cenários de
  encerramento anormal e `KeyboardInterrupt`.
- Restringe a demonstração automatizada da tela de resultado à dimensão
  lógica `80x24`; qualquer fixture de resultado que exceda essa área é
  tratada como inválida, exigindo disciplina na criação de fixtures de
  teste.
- Adia explicitamente para aplicação documental futura quatro capacidades
  já identificadas como bloqueadas (D-SEL-24), sem reservar numeração,
  criando uma dívida documental controlada.

### Artefatos afetados

| Artefato | Aplicação necessária |
|---|---|
| `docs/contratos/contrato_console.md` | Registrar D-SEL-01 a D-SEL-10 (estado da seleção, reconciliação, teclas, indicadores, chip `Espaço`) como extensão da política de seleção múltipla já prevista em §8; propagar a fronteira operação consumidora × ações genéricas (D-SEL-11). |
| `docs/contratos/contrato_barra_de_menus.md` | Registrar os rótulos dinâmicos `Todos`/`Executar` de `[⏎]` para seleção múltipla (D-SEL-06, D-SEL-07) e o chip `[␣]` conforme D-SEL-05, D-SEL-09 e D-SEL-10, sem alterar a ordem canônica já vigente. |
| `docs/contratos/contrato_tela_json.md` | Registrar o campo raiz opcional `perfil` e o perfil `resultado_execucao` (D-SEL-16), a validação antecipada do `tela_resultado_id` (D-SEL-17) e a classificação `CONFIGURACAO_INVALIDA`. |
| `docs/contratos/contrato_composicao_corpo.md` | Registrar a tela de resultado como composição de tipos existentes (um único `console` passivo), sem criar tipo de elemento novo, coerente com a ADR-0007. |
| `docs/contratos/contrato_json_console.md` | Registrar o protocolo provisório de entrada/execução (D-SEL-12), a entrada da operação consumidora (D-SEL-11) e o envelope de erro multinível (D-SEL-15) como extensão focal do envelope do `console`. |
| `docs/nomenclatura/32_CONSOLE.md` | Avaliar necessidade de termos novos para seleção múltipla, lote de execução e reconciliação, preservando a distinção já registrada entre cursor, grupo, seleção e lote. |
| `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` | Avaliar necessidade de registrar `[␣]` e os rótulos dinâmicos `Todos`/`Executar` como termos vigentes de seleção múltipla. |
| `docs/adr/INDICE_ADR.md` | Registrar a ADR-0034 após QA favorável. |
| `docs/backlog.md` | Atualizar o estado do `ITEM-0006` quando o fluxo documental determinar mudança material; registrar os quatro itens bloqueados de D-SEL-24 sem reservar numeração de ADR. |

---

## 6. Compatibilidade e transição

Esta ADR não executa nenhuma aplicação documental, alteração de contrato,
alteração de nomenclatura, criação de handoff, implementação ou validação
manual — apenas registra a decisão fechada. Até a aplicação, os contratos e
módulos de nomenclatura listados na seção 5 permanecem no estado atual.

Console sem política de seleção múltipla declarada preserva integralmente o
comportamento histórico (`politica_selecao: "nenhuma"` ou `"unica"`,
conforme `contrato_console.md` §8); nenhuma migração automática de telas
existentes é introduzida por esta ADR.

O campo raiz opcional `perfil` é aditivo e compatível com `tela.v1`: telas
existentes sem esse campo continuam válidas sob os contratos vigentes;
somente a tela padrão de resultado, quando criada nos handoffs
subsequentes, declarará `perfil: resultado_execucao`.

O protocolo provisório de D-SEL-12 é explicitamente transitório: contratos
futuros de binding, script e processamento podem redefinir nomes de campo,
formato de CLI e mecanismo de transporte sem reabrir o núcleo de seleção
múltipla (D-SEL-01 a D-SEL-10), que é estável independentemente do
protocolo de invocação concreto.

## 7. Alternativas consideradas

Não há alternativas de desenho a registrar nesta ADR. As decisões D-SEL-01
a D-SEL-26 constituem decisão já fechada fornecida ao autor documental;
este documento não escolhe entre opções nem introduz arquitetura, schema ou
protocolo definitivo além do que foi explicitamente decidido.

## 8. Itens fora de escopo

- Registry, dispatcher e catálogo genérico de ações declarativas —
  `ITEM-0004`, DOC-B009.
- Protocolo definitivo de binding, script e processamento — D-SEL-12
  permanece provisório.
- Pilha genérica de telas, abertura e retorno genéricos entre telas —
  `ITEM-0005`.
- Paginação interativa do console e da tela de resultado — `ITEM-0003`.
- Prova de persistência de seleção entre páginas — depende de `ITEM-0003`.
- Filtro na fixture obrigatória do Handoff 1 (D-SEL-22).
- Seleção compartilhada entre consoles compatíveis — item bloqueado
  registrado em D-SEL-24, sem número reservado.
- Chip de alternância entre `dry-run` e execução real — item bloqueado
  registrado em D-SEL-24, sem número reservado.
- Modos não verboso ou alternável na tela padrão de resultado — item
  bloqueado registrado em D-SEL-24, sem número reservado.
- Colapso e expansão de conteúdo multinível — `ITEM-0007`.
- Correção automática de JSON inválido produzido pelo processo externo —
  proibida por D-SEL-15.
- Comandos arbitrários declarados no JSON — proibidos por D-SEL-11.
- QA da ADR, aplicação documental, alteração de contratos ou nomenclatura,
  criação de handoff, implementação, validação manual e commit — fora
  desta execução (ver seção 15 do prompt orquestrador desta etapa).

## 9. Critérios para aplicação

- [ ] `docs/contratos/contrato_console.md`, `docs/contratos/contrato_barra_de_menus.md`,
  `docs/contratos/contrato_tela_json.md`, `docs/contratos/contrato_composicao_corpo.md`
  e `docs/contratos/contrato_json_console.md` foram atualizados conforme a
  tabela de artefatos afetados (seção 5).
- [ ] Somente os módulos proprietários da nomenclatura efetivamente afetados
  foram atualizados.
- [ ] `docs/adr/INDICE_ADR.md` foi atualizado somente após QA favorável desta
  ADR.
- [ ] `docs/backlog.md` foi atualizado somente quando o fluxo documental
  determinar mudança material do `ITEM-0006`, incluindo o registro dos
  quatro itens bloqueados de D-SEL-24 sem numeração de ADR reservada.
- [ ] O `delta_terminologico` desta aplicação foi registrado no relatório de
  aplicação.
- [ ] Nenhuma implementação de código foi feita durante a aplicação
  documental.
- [ ] Nenhum handoff foi criado na mesma etapa da aplicação documental.
- [ ] Caminhos permanecem relativos à raiz do Orquestrador.
- [ ] A execução de aplicação produziu relatório próprio em
  `docs/relatorios/`.
- [ ] O relatório de aplicação não sobrescreveu relatório de execução
  anterior.
- [ ] A aplicação foi submetida a QA independente.

## 10. Bloqueios

nenhum
