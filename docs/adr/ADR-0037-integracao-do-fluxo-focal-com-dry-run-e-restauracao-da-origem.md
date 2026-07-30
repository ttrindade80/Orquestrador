---
name: ADR-0037-integracao-do-fluxo-focal-com-dry-run-e-restauracao-da-origem
description: "Especializa o Handoff 4 da ADR-0034 (ITEM-0006): ativação do chip Executar, integração do executor focal do H-0042 e da tela de resultado do H-0043, toggle focal [Ins] Dry-Run com cor_alerta, origem suspensa como referência de runtime, transição atômica de acionamento e regras diferenciadas de retorno para dry-run e execução real"
metadata:
  type: adr
  status: aceita
  id: ADR-0037
  data: 2026-07-29
  substitui: null
rastreabilidade:
  decisao_usuario: "D-H4-01 a D-H4-10 — tela de origem específica do Handoff 4 reutilizando a semântica da fixture de oito itens do H-0041 sem alterar a tela histórica, com nome físico deferido ao handoff; toggle focal [Ins] Dry-Run como chip de alternância de estado vivo da instância de runtime, iniciando em execução real; cor_alerta (amarelo) aplicada ao chip em dry-run, concretizando o campo no estilo global e absorvendo a parte pendente de cor_alerta do ITEM-0011; fronteira pontual com o ITEM-0020, que permanece aberto para a padronização genérica futura do toggle, com supersessão pontual de D-SEL-19 (ADR-0034), da fronteira correspondente de contrato_barra_de_menus.md e dos fora de escopo de dry-run/cor_alerta da ADR-0036; ativação condicional do chip Executar sobre o lote reconciliado; transição atômica entre acionamento e apresentação do resultado sem tela de resultado vazia nem estado visual intermediário; origem suspensa como referência de runtime (não snapshot serializado) que não recebe entrada nem sofre mutação enquanto o resultado está aberto; retorno de dry-run sem recarregar dados e preservando seleção/filtro/página/foco/cursor/toggle; retorno de execução real com seleção sempre limpa, dados recarregados, filtro reaplicado e foco/cursor reconciliados; limpeza por propriedade entre H-0042, H-0043 e o próprio Handoff 4"
  rfc_origem: null
  issues_relacionadas:
    - ITEM-0006
    - ITEM-0011
    - ITEM-0020
  contratos_afetados:
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_estilo.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_chip.md
    - docs/contratos/contrato_json_console.md
  handoffs_bloqueados: []
---

# ADR-0037 — Integração do fluxo focal com dry-run e restauração da origem (especialização do Handoff 4 da ADR-0034)

## 1. Status

`aceita`

## 2. Contexto

A ADR-0034 decompôs o `ITEM-0006` em quatro handoffs sequenciais (D-SEL-21).
O Handoff 1 (estado, comandos e apresentação da seleção) foi entregue pelo
`H-0041`. O Handoff 2 (protocolo focal de execução sintética reversível) foi
especializado pela ADR-0035 e entregue pelo `H-0042`. O Handoff 3
(carregamento e apresentação da tela padrão de resultado) foi especializado
pela ADR-0036 e entregue pelo `H-0043`, que também promoveu, em D-H3-19, a
supersessão parcial e pontual da divisão original de D-SEL-21: a ativação do
chip `Executar`, a abertura da tela de resultado, a suspensão da tela de
origem, o retorno e a restauração passaram a pertencer exclusivamente ao
Handoff 4.

O Handoff 4 permanece aberto. As três ADRs anteriores já fecham, em nível
geral, o protocolo de execução (D-SEL-12 a D-SEL-15; H2-ESP-01 a H2-ESP-18),
o documento de resultado e o envelope de erro (`contrato_json_console.md`
§14), e a identidade, o carregamento e a regra de escolha entre documento e
envelope da tela `resultado_execucao` (D-H3-01 a D-H3-19). Esse fechamento
geral não decide, porém, o que é indispensável para integrar essas três
capacidades já entregues em um fluxo único e reversível: a existência de uma
tela de origem própria do Handoff 4; a escolha entre execução real e
`dry-run` diretamente na interface, hoje explicitamente proibida como chip de
alternância por D-SEL-19; a cor de destaque desse novo controle, que depende
da concretização de `cor_alerta` no estilo global — capacidade parcialmente
pendente do `ITEM-0011`; a fronteira exata entre essa especialização focal e
a futura padronização genérica do `ITEM-0020`; a condição precisa de ativação
do chip `Executar`; a sequência atômica entre o acionamento e a apresentação
do resultado; a natureza e as regras de preservação da origem suspensa
durante a apresentação do resultado; as regras de retorno, que diferem
conforme o cenário tenha sido `dry-run` ou execução real; e a divisão de
responsabilidade de limpeza de recursos entre as camadas já entregues e o
próprio Handoff 4.

Este documento fecha essas lacunas como especialização do Handoff 4, sem
reabrir o núcleo da seleção múltipla (D-SEL-01 a D-SEL-10), sem redefinir o
protocolo do Handoff 2 fechado pela ADR-0035 e implementado por `H-0042`, sem
redefinir a identidade, o carregamento ou a regra de escolha da tela de
resultado fechados pela ADR-0036 e implementados por `H-0043`, sem instituir
binding definitivo entre Orquestrador e Pipeline, sem antecipar o `ITEM-0004`
ou o `ITEM-0005`, e sem criar o handoff de implementação correspondente —
essa autorização permanece para um handoff futuro, criado em etapa distinta.

---

## 3. Decisão explícita do usuário

### D-H4-01 — Tela de origem específica do Handoff 4

O handoff e a implementação futuros criarão uma instância de tela/demo
específica para o fluxo integrado deste ciclo, reutilizando a semântica da
fixture de oito itens do `H-0041` (D-SEL-22) sem modificar a tela histórica
correspondente. Esta ADR não fixa o nome físico do novo JSON — essa escolha
nominal é fechada no handoff.

### D-H4-02 — Toggle focal `[Ins] Dry-Run`

A tela integrada suporta execução real e `dry-run` na mesma instância. O
estado inicial é `execução real` (`dry_run_ativo: false`). A tecla física
`Insert` alterna reversivelmente entre `execução real` e `dry-run`. O chip
`[Ins] Dry-Run`:

- é do tipo conceitual `alternância` (`contrato_chip.md` §5);
- permanece operável em ambos os estados — nunca fica inativo nem usa
  `cor_inativo`;
- não desaparece da `barra_de_menus`;
- não produz mensagem, popup, linha de status ou qualquer outro eco além da
  mudança de cor do próprio texto do chip.

O estado do toggle pertence à instância de runtime da tela — não ao estilo
global nem ao `tela.json` como estado vivo (`docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md`
§4.5).

### D-H4-03 — Cor de alerta do toggle

Com `dry_run_ativo: false`, o chip usa a cor normal de texto do preset de
chip ativo. Com `dry_run_ativo: true`, o chip usa `cor_alerta: amarelo`.
Esta decisão:

- concretiza `cor_alerta` no estilo global (`contrato_estilo.md` §3.5,
  já prevista desde a ADR-0004, ainda sem valor materializado);
- exige que o loader materialize `cor_alerta` em `EstiloResolvido`, junto do
  campo já existente `cor_inativo`;
- exige que `cor_alerta` esteja presente no objeto de estilo resolvido
  entregue ao renderer;
- permite ao renderer aplicar `cor_alerta` a um chip operável em estado de
  destaque, sem confundi-lo com o estado inativo (`cor_inativo`);
- não autoriza cor ANSI hardcoded fora da tradução canônica já existente no
  renderer (`_ANSI_POR_NOME_SEMANTICO`, que já mapeia o nome semântico
  `"amarelo"`).

Esta decisão absorve a parte ainda pendente de `cor_alerta` do `ITEM-0011`.
O item somente poderá ser encerrado no fechamento documental após a
implementação e a validação comprovarem que essa capacidade restante foi
entregue.

### D-H4-04 — Fronteira com o `ITEM-0020`

O toggle `[Ins] Dry-Run` é uma especialização focal do fluxo integrado deste
Handoff 4 — não estabelece o padrão universal para todas as telas, operações
ou ações do sistema. O `ITEM-0020` permanece ativo, com finalidade a
reconciliar futuramente para a padronização genérica da escolha entre
execução real e `dry-run`; essa padronização exige ADR própria.

Esta ADR substitui pontualmente:

- a frase de D-SEL-19 (ADR-0034) que proíbe chip de alternância entre
  execução real e `dry-run` neste ciclo;
- a fronteira correspondente registrada em `contrato_barra_de_menus.md`
  §23.3 (ausência de chip de alternância);
- os itens de fora de escopo da ADR-0036 relativos à escolha de `dry-run`
  pela interface e à definição global de `cor_alerta`.

Todas as demais decisões dessas três ADRs permanecem vigentes e não
reabertas.

### D-H4-05 — Ativação de `Executar`

Antes do acionamento, a seleção é reconciliada conforme o `H-0041`
(D-SEL-03, D-SEL-04). O chip `Executar` fica ativo somente quando,
cumulativamente: o lote reconciliado não está vazio; o executor focal
(`tela/execucao_focal.py`) está disponível; a tela de resultado já foi
pré-validada (validação antecipada de D-SEL-17). O cursor corrente não
restringe o lote — a operação consome a lista ordenada de IDs selecionados e
reconciliados.

Se a reconciliação esvaziar a seleção no próprio acionamento, a operação não
executa, `Todos` não é aplicado no mesmo acionamento, e a seleção permanece
vazia — um novo `Enter` é necessário para acionar `Todos` (D-SEL-04).

### D-H4-06 — Transição atômica

O acionamento segue a sequência obrigatória: reconciliar a seleção; capturar
o estado corrente do toggle `dry-run`/execução real; preservar a referência
da origem; executar o protocolo focal do `H-0042`; classificar o resultado;
construir em memória o modelo de resultado já entregue pelo `H-0043`;
suspender a origem; ativar `resultado_execucao`.

A tela de resultado só se torna ativa quando já existe um modelo válido para
apresentação — documento válido ou envelope de erro. É proibido: abrir uma
tela de resultado vazia; criar estado visual intermediário de processamento;
destruir ou recarregar a origem antes da apresentação; reimplementar
classificação, executor ou construção de resultado já entregues por `H-0042`
e `H-0043`. Sucesso, resultado parcial, falha semântica, falha operacional,
resultado inválido e interrupção estruturada abrem todos a mesma tela de
resultado.

### D-H4-07 — Origem suspensa

Existe zero ou uma origem suspensa por vez. A origem suspensa é uma
referência para a própria instância de runtime que abriu o resultado — não
um snapshot serializado (`docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md`
§4.6.1). Ela preserva modelo da tela, dados carregados, filtro, página,
foco, cursores, seleção múltipla e o estado do toggle `dry-run`.

Enquanto `resultado_execucao` estiver ativa, a origem não recebe entrada, não
sofre mutações, não relê arquivos e não é reconstruída. Não é criada pilha
genérica de telas (`ITEM-0005` permanece fora de escopo).

### D-H4-08 — Retorno após `dry-run`

Ao pressionar `Esc` em `resultado_execucao` com o toggle em `dry-run`: o
runtime do resultado é descartado; a mesma origem suspensa é reativada;
referências próprias do Handoff 4 são limpas; a origem é redesenhada. Não há
releitura de dados; seleção, filtro, página, foco e cursores são
preservados; o toggle `dry-run` permanece ligado no retorno — o usuário
precisa pressionar `Insert` para voltar ao modo real.

Se o terminal tiver sido redimensionado enquanto o resultado estava aberto,
o estado semântico da origem é preservado e apenas a geometria física é
recalculada para o terminal vigente, sem releitura de arquivos.

### D-H4-09 — Retorno após execução real

A origem permanece imutável enquanto o resultado estiver aberto; somente no
acionamento de `Esc` ocorre a restauração da execução real: encerrar o
resultado; limpar a seleção; recarregar os dados do binding; reaplicar o
filtro; reconciliar foco e cursor; reativar a origem; redesenhar. Esta regra
vale para sucesso, resultado parcial, falha operacional, resultado inválido
e interrupção com código `130`.

Regras de restauração: seleção sempre limpa; dados recarregados do binding;
filtro preservado e reaplicado; foco preservado se o console anterior
continuar válido, com fallback no primeiro console focalizável; cursor
preservado por ID do item anterior se ainda válido, com fallback no primeiro
item navegável; toggle `dry-run` sempre `false` após execução real.

### D-H4-10 — Limpeza por propriedade

Cada camada limpa somente os recursos que criou. O `H-0042` limpa cópia
temporária, resultado temporário e subprocesso antes de entregar o resultado
ao Handoff 4, por `finally`. O `H-0043` mantém o modelo de resultado em
memória e não introduz novos temporários. O Handoff 4 limpa a referência da
origem suspensa, a referência do modelo de resultado e o estado da
transição.

`KeyboardInterrupt` previsto durante o executor: o `H-0042` converte em
código `130` e limpa seus próprios recursos; o Handoff 4 apresenta o
envelope de interrupção; o usuário retorna normalmente. Exceção interna
inesperada do próprio Handoff 4 não é convertida em envelope operacional
artificial; deve limpar referências próprias, restaurar o terminal por
`finally` e propagar o erro — se ocorrer antes da suspensão, a origem
permanece ativa; se ocorrer depois, o processo pode encerrar com erro após
restaurar o terminal. `SIGKILL` e encerramentos não interceptáveis ficam
fora da garantia.

---

## 4. Decisão

Fica adotada, como especialização do Handoff 4 do `ITEM-0006` (ADR-0034
D-SEL-18 a D-SEL-21, D-H3-19 da ADR-0036), a integração do fluxo focal
completo — seleção, execução, apresentação do resultado e retorno —
organizada em quatro camadas:

**Tela de origem e toggle focal de modo (D-H4-01 a D-H4-04).** O Handoff 4
cria futuramente uma instância de tela/demo própria, reaproveitando a
semântica da fixture de oito itens do `H-0041` sem alterar a tela histórica.
Essa mesma tela integra um toggle `[Ins] Dry-Run`, chip de alternância que
alterna reversivelmente entre execução real (estado inicial) e `dry-run`,
sinalizado exclusivamente pela mudança de cor do próprio texto —
`cor_alerta: amarelo` quando ativo, cor normal quando inativo — sem qualquer
outro eco. `cor_alerta` é concretizada no estilo global como consequência
direta desta decisão, absorvendo a capacidade pendente correspondente do
`ITEM-0011`. O toggle é especialização focal deste ciclo, não padronização
universal; a fronteira com a futura generalização do `ITEM-0020` é
explícita, e a ADR substitui pontualmente a proibição de chip de alternância
fixada por D-SEL-19 e as remissões correspondentes em
`contrato_barra_de_menus.md` e nos fora de escopo da ADR-0036, preservando
todas as demais decisões dessas três ADRs.

**Ativação e transição atômica (D-H4-05, D-H4-06).** O chip `Executar` fica
ativo somente com lote reconciliado não vazio, executor focal disponível e
tela de resultado pré-validada. O acionamento segue sequência atômica e
determinística — reconciliar, capturar o modo, preservar a origem, executar
o protocolo focal já entregue por `H-0042`, classificar, construir o modelo
já entregue por `H-0043`, suspender a origem, ativar o resultado — sem
estado visual intermediário e sem reimplementar capacidades das camadas
anteriores.

**Origem suspensa e retornos diferenciados (D-H4-07 a D-H4-09).** A origem
suspensa é referência viva da instância de runtime que abriu o resultado,
nunca um snapshot serializado, e nunca recebe entrada ou mutação enquanto o
resultado está aberto. O retorno após `dry-run` não recarrega dados e
preserva integralmente seleção, filtro, página, foco, cursores e o estado
ligado do toggle. O retorno após execução real sempre limpa a seleção,
recarrega os dados do binding, reaplica o filtro, reconcilia foco e cursor
com fallback determinístico, e desliga o toggle.

**Limpeza por propriedade (D-H4-10).** Cada camada — `H-0042`, `H-0043` e o
próprio Handoff 4 — limpa exclusivamente os recursos que criou, com
interrupção convertida em código `130` pelo `H-0042` e apresentada pelo
Handoff 4, e com exceção interna do próprio Handoff 4 propagada, nunca
convertida em envelope artificial.

Esta decisão não redefine D-SEL-01 a D-SEL-10, não redefine o protocolo do
Handoff 2 fechado pela ADR-0035 e implementado por `H-0042`, não redefine a
identidade, o carregamento ou a regra de escolha da tela de resultado
fechados pela ADR-0036 e implementados por `H-0043`, e não institui binding
definitivo entre Orquestrador e Pipeline.

---

## 5. Consequências

### Positivas

- Fecha as lacunas indispensáveis para integrar, em um único fluxo
  reversível, as três capacidades já entregues pelo `ITEM-0006`
  (`H-0041`, `H-0042`, `H-0043`), permitindo a conclusão do item.
- Introduz a escolha de `dry-run` diretamente na interface como
  especialização focal e testável, sem antecipar a padronização genérica
  ainda pendente do `ITEM-0020`.
- Concretiza `cor_alerta` no estilo global, encerrando a lacuna de
  materialização que mantinha o `ITEM-0011` parcialmente pendente.
- Formaliza a origem suspensa como referência de runtime — e não snapshot
  serializado — evitando duplicação de estado e simplificando a
  restauração.
- Distingue explicitamente as regras de retorno de `dry-run` e de execução
  real, evitando ambiguidade sobre recarregamento de dados, preservação de
  seleção e estado do toggle.
- Fixa a divisão de responsabilidade de limpeza entre as três camadas
  envolvidas, reduzindo risco de resíduos temporários ou de duplicação de
  tratamento de interrupção.

### Custos e restrições

- Exige que a implementação futura crie e mantenha uma nova tela/demo
  específica do Handoff 4, sem contaminar a tela histórica do `H-0041`.
- Exige que o loader e o objeto de estilo resolvido passem a materializar
  `cor_alerta`, ampliando o schema de estilo em runtime além do que o
  `H-0041` já materializou para `cor_inativo`.
- Introduz um segundo estado dinâmico de cor operável simultaneamente ao
  padrão existente de `cor_inativo`, exigindo que o renderer distinga os
  dois sem confundir chip inativo com chip em destaque.
- Exige que a implementação preserve com precisão a diferença entre origem
  suspensa (referência viva) e qualquer forma de snapshot, sob risco de
  duplicar estado ou permitir mutação indevida da origem durante a
  apresentação do resultado.
- Exige tratamento diferenciado e testável para dois fluxos de retorno
  (`dry-run` e execução real), aumentando a superfície de cenários de
  validação em relação a um único fluxo de retorno.

### Artefatos afetados

| Artefato | Aplicação necessária |
|---|---|
| `docs/contratos/contrato_barra_de_menus.md` | Registrar a instância concreta do toggle `[Ins] Dry-Run` como chip de alternância (§23.3) e revogar pontualmente a fronteira que hoje declara ausência de chip de alternância entre `dry-run` e execução real. |
| `docs/contratos/contrato_estilo.md` | Materializar `cor_alerta` na seção 3.5 como campo efetivamente presente em `config/estilo.json` e em `EstiloResolvido`, análogo ao já materializado para `cor_inativo`. |
| `docs/contratos/contrato_console.md` | Especializar a seção 23.6/23.7 com a fronteira comportamental completa do Handoff 4: ativação de `Executar`, transição atômica, origem suspensa e retornos diferenciados. |
| `docs/contratos/contrato_chip.md` | Registrar o toggle `[Ins] Dry-Run` como instância concreta de tipo `alternancia` sem `cor_inativo`, com `cor_alerta` como único eco de estado. |
| `docs/contratos/contrato_json_console.md` | Atualizar a seção 14.11 (fora de escopo) para refletir que o Handoff 4 deixa de estar pendente, preservando o restante do protocolo já fechado. |
| `docs/nomenclatura/10_ESTILO.md` | Registrar a materialização de `cor_alerta` como campo efetivamente presente no estilo global, atualizando a nota de pendência da seção 4.5. |
| `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` | Registrar o toggle `[Ins] Dry-Run` como instância concreta de chip de alternância e a supersessão pontual da nota de ausência de chip de alternância da ADR-0034. |
| `docs/nomenclatura/32_CONSOLE.md` | Avaliar necessidade de termo específico para a origem suspensa como referência de runtime consumida pelo Handoff 4. |
| `docs/adr/INDICE_ADR.md` | Registrar a ADR-0037 após QA favorável. |
| `docs/backlog.md` | Atualizar o estado do `ITEM-0006` para indicar a especialização do Handoff 4 e a criação do handoff correspondente; registrar a capacidade restante do `ITEM-0011` (`cor_alerta`) como endereçada por esta ADR; registrar a fronteira do `ITEM-0020` com a padronização genérica futura. |

---

## 6. Compatibilidade e transição

Esta ADR não executa nenhuma aplicação documental, alteração de contrato,
alteração de nomenclatura, criação de handoff, implementação ou validação
manual — apenas registra a decisão fechada do Handoff 4. Até a aplicação, os
contratos e módulos de nomenclatura listados na seção 5 permanecem no
estado atual.

Esta ADR preserva integralmente:

- D-SEL-01 a D-SEL-10 (núcleo da seleção múltipla, ADR-0034);
- o protocolo focal de execução sintética reversível fechado pela ADR-0035
  (H2-ESP-01 a H2-ESP-18) e implementado por `H-0042`, sem alteração de
  `tela/execucao_focal.py`, de `demo/executor_sintetico.py` nem das
  fixtures `demo/fixtures/h0042_*.json`;
- a identidade, o ciclo de carregamento e a regra de escolha entre
  documento e envelope da tela `resultado_execucao` fechados pela ADR-0036
  (D-H3-01 a D-H3-19) e implementados por `H-0043`, sem alteração de
  `tela/resultado_execucao.py` além do estritamente necessário para
  consumi-lo a partir da origem suspensa;
- a ausência de paginação na tela de resultado (D-SEL-20);
- a separação entre JSON estrutural, conteúdo externo e estado vivo
  (ADR-0026, ADR-0027; `docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md`
  §4.5);
- o estilo global como única autoridade de aparência (`contrato_estilo.md`
  §2, ADR-0030) — `cor_alerta` é adicionada ao schema já vigente, não uma
  nova autoridade de aparência;
- a ausência de hardcoding de cor por funcionalidade no renderer — a
  aplicação de `cor_alerta` reutiliza a tradução canônica já existente
  (`_ANSI_POR_NOME_SEMANTICO`), sem introduzir literal ANSI novo fora dela.

O `ITEM-0020` permanece aberto e não é encerrado por esta ADR: sua
finalidade é reconciliada para a padronização genérica futura, distinta da
especialização focal aqui fechada. O `ITEM-0011` permanece pendente quanto a
`cor_inativo` até fechamento documental próprio, se aplicável; quanto a
`cor_alerta`, permanece pendente até que a implementação e a validação
comprovem a entrega da capacidade aqui especializada.

## 7. Alternativas consideradas

Não há alternativas de desenho a registrar nesta ADR. As decisões D-H4-01 a
D-H4-10 constituem decisão já fechada fornecida ao autor documental; este
documento não escolhe entre opções nem introduz arquitetura, schema,
comportamento visual ou política além do que foi explicitamente decidido.

## 8. Itens fora de escopo

- Binding definitivo com o Pipeline.
- Registry, dispatcher ou catálogo genérico do `ITEM-0004`.
- Pilha, abertura ou retorno genéricos do `ITEM-0005`.
- Paginação do `ITEM-0003`.
- Seleção `Todos` limitada à página atual (item bloqueado, D-SEL-24).
- Seleção compartilhada entre consoles (item bloqueado, D-SEL-24).
- Modos adicionais da tela de resultado do `ITEM-0021` (item bloqueado,
  D-SEL-24).
- Colapso multinível do `ITEM-0007`.
- Padronização universal do toggle real/`dry-run` — permanece com o
  `ITEM-0020`, reconciliado para escopo genérico futuro.
- Persistência do estado `dry-run` fora da instância viva da tela.
- Escolha do nome físico da nova tela demo — fechada no handoff.
- Alteração dos schemas do documento de entrada ou de resultado já
  fechados pela ADR-0035 e pela ADR-0036.
- Implementação, QA, aplicação documental, criação de handoff e commit
  nesta etapa.

## 9. Critérios para aplicação

- [ ] `docs/contratos/contrato_barra_de_menus.md`, `docs/contratos/contrato_estilo.md`,
  `docs/contratos/contrato_console.md`, `docs/contratos/contrato_chip.md` e
  `docs/contratos/contrato_json_console.md` foram atualizados conforme a
  tabela de artefatos afetados (seção 5).
- [ ] Somente os módulos proprietários da nomenclatura efetivamente
  afetados (`10`, `31`, `32`) foram avaliados e, quando material,
  atualizados.
- [ ] `docs/adr/INDICE_ADR.md` foi atualizado somente após QA favorável
  desta ADR.
- [ ] `docs/backlog.md` foi atualizado somente quando o fluxo documental
  determinar mudança material do `ITEM-0006`, do `ITEM-0011` e do
  `ITEM-0020`.
- [ ] Nenhuma implementação de código foi feita durante a aplicação
  documental.
- [ ] Nenhum handoff foi criado na mesma etapa da aplicação documental.
- [ ] Caminhos permanecem relativos à raiz do Orquestrador.
- [ ] A execução de aplicação produziu relatório próprio em
  `docs/relatorios/`.
- [ ] O relatório de aplicação não sobrescreveu relatório de execução
  anterior.
- [ ] A aplicação foi submetida a QA independente.

## 10. Critérios obrigatórios para o futuro handoff

O futuro handoff de implementação deve especificar testes automatizados e
validação manual focal cobrindo, no mínimo:

**Toggle.** Estado inicial em execução real; `Insert` liga o `dry-run` e o
chip fica amarelo; `Insert` desliga e o chip volta à cor normal; nenhum
outro eco além da cor aparece em qualquer transição.

**Ativação.** Lote reconciliado válido ativa `Executar`; lote vazio
inativa; executor indisponível inativa; tela de resultado inválida
inativa.

**Dry-run.** Abertura de `resultado_execucao`; suspensão da origem; ausência
de recarregamento de dados; preservação de seleção, filtro, página, foco e
cursor; manutenção do toggle ligado no retorno.

**Execução real.** Sucesso; resultado parcial; falha operacional; resultado
inválido; interrupção com código `130`.

**Retorno real.** Limpeza de seleção em todos os resultados; recarregamento
do binding; reaplicação do filtro; preservação do cursor por ID quando
válido; fallback de cursor quando inválido; preservação ou reconciliação de
foco; retorno com `dry-run` desligado.

**Suspensão e redimensionamento.** Ausência de entrada ou mutação na
origem; ausência de pilha genérica; `Esc` retornando exatamente à origem que
abriu; preservação do estado semântico; recálculo de geometria para o
terminal vigente.

**Limpeza.** Ausência de temporário remanescente do `H-0042`; descarte de
referências do Handoff 4; restauração do terminal em exceção interna.

O roteiro de validação manual deve descrever previamente cada tecla e o
resultado esperado, registrar o observado, fornecer respostas completas
para exclusão das alternativas não observadas, ser executável em TTY real
em `1920×1200` de tela cheia, e demonstrar separadamente execução real e
`dry-run`. O aceite automatizado da tela de resultado continua respeitando
a referência `80x24` já vigente (D-SEL-20).

## 11. Relação com ADR-0034, ADR-0035, ADR-0036 e com ITEM-0006, ITEM-0011, ITEM-0020

Esta ADR especializa o Handoff 4 já decomposto pela ADR-0034 (D-SEL-21), sob
a divisão de responsabilidades entre Handoff 3 e Handoff 4 fixada pela
ADR-0036 (D-H3-19). Ela não reabre D-SEL-01 a D-SEL-10 nem qualquer outra
decisão de D-SEL-11 a D-SEL-20, D-SEL-22 a D-SEL-26 além da supersessão
pontual explicitamente declarada em D-H4-04. Ela consome, sem redefinir, o
protocolo e o schema fechados pela ADR-0035 e implementados por `H-0042`, e
a identidade, o carregamento e a regra de escolha fechados pela ADR-0036 e
implementados por `H-0043`.

Para o `ITEM-0006`, esta ADR fecha a última especificação necessária antes
da implementação final do item — a autorização de implementação permanece
sujeita a handoff próprio, criado em etapa distinta, e esta ADR não o cria.

Para o `ITEM-0011`, esta ADR absorve e fecha a especificação da parcela
pendente relativa a `cor_alerta`; o item somente poderá ser encerrado no
fechamento documental após implementação e validação comprovarem que essa
capacidade foi entregue.

Para o `ITEM-0020`, esta ADR mantém o item aberto e reconcilia sua
finalidade para a padronização genérica futura da escolha entre execução
real e `dry-run`, distinta da especialização focal do toggle `[Ins]
Dry-Run` aqui fechada; essa padronização exige ADR própria.

## 12. Bloqueios

nenhum
