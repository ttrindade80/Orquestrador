---
name: H-0050-controle-universal-execucao-real-dry-run
description: "Materializa o controle universal reutilizável de escolha entre execução real e dry-run, com configuração fechada, registro autoritativo de ações, modo único por instância e captura privada explícita."
metadata:
  type: handoff_implementacao
  status: HANDOFF_PATCHED_AWAITING_QA
  id: H-0050
  data_criacao: 2026-08-04
  etapa: PATCH_HANDOFF
  patch_atual: P06
rastreabilidade:
  contrato_alvo: ITEM-0020
  adr_relacionadas:
    - docs/adr/ADR-0040-padronizacao-universal-do-controle-de-execucao-real-e-dry-run.md
  contratos_relacionados:
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_registro_acoes.md
  issues_relacionadas:
    - ITEM-0020
  handoffs_anteriores:
    - docs/handoff/H-0044-integracao-fluxo-focal-dry-run-restauracao-origem.md
---

# H-0050 — Implementar controle universal de execução real e `dry-run`

## 1. Etapa única

Este handoff autoriza exclusivamente:

`IMPLEMENTAR`

Ele não autoriza QA, aprovação, aplicação documental, commit, reconciliação do
H-0044 nem alteração de autoridade documental.

## 2. Ordem de autoridade

1. decisões explícitas D-DRY-01 a D-DRY-12;
2. ADR-0040 aceita e aplicada documentalmente;
3. `docs/contratos/contrato_tela_json.md`,
   `docs/contratos/contrato_registro_acoes.md`, os contratos de console e JSON
   vigentes e a nomenclatura enumerada no manifesto;
4. este handoff.

D-DRY-10 determina que `controle_execucao` é objeto fechado. D-DRY-11 e
`contrato_registro_acoes.md` determinam que a autoridade de categoria e de
compatibilidade pertence à implementação registrada da ação. Não há bloqueio
por falta de autoridade sobre propriedades internas adicionais, categoria,
modos aceitos ou registro autoritativo. Bloquear somente diante de contradição
documental real ou de decisão material nova não coberta por essas autoridades.

D-DRY-12 reconcilia exclusivamente os rótulos visuais do modo corrente:
`executar` apresenta `[Ins] Real` e `dry_run` apresenta `[Ins] Simulação`.
Essa decisão é posterior à validação manual R03 e não reabre decisões,
requisitos ou achados anteriores.

## 3. Estado transportado

```yaml
item:
  id: ITEM-0020
  status: em_andamento
adr:
  id: ADR-0040
  status: aceita
  decisoes_aprovadas:
    - D-DRY-01
    - D-DRY-02
    - D-DRY-03
    - D-DRY-04
    - D-DRY-05
    - D-DRY-06
    - D-DRY-07
    - D-DRY-08
    - D-DRY-09
    - D-DRY-10
    - D-DRY-11
    - D-DRY-12
  aplicacao_documental:
    estado_material: APROVADA
handoff:
  id: H-0050
  precondicao: correcoes_documentais_D-DRY-10_e_D-DRY-11_aplicadas
  patch_predecessor: P05
  estado_funcional_anterior: IMPLEMENTADO_E_VALIDADO
  qa_posterior_necessario: true
validacao_manual_anterior:
  rodada: R03
  status: MANUAL_VALIDATION_APPROVED
  criterios_conformes: 7
  criterios_totais: 7
preservacao:
  h0044: sem_delta
```

## 4. Objetivo e capacidade coesa

Entregar uma infraestrutura universal e reutilizável para toda tela que declare
`controle_execucao`, use referências resolvíveis no registro e tenha todas as
ações de processo relevantes compatíveis:

```text
carregar controle_execucao fechado
→ resolver ações relevantes no registro autoritativo
→ validar categorias e compatibilidade
→ criar modo corrente por instância
→ alternar e representar o modo
→ capturar o modo no acionamento
→ entregar captura privada e explícita à ação registrada
```

A demonstração H-0050 é prova permanente dessa infraestrutura, não fonte de
autoridade e não exceção por ID, nome ou texto. A segunda configuração, aberta
em `dry_run`, prova o outro valor inicial com a mesma infraestrutura e fixture.

### Reconciliação visual de D-DRY-12

O controle universal apresenta o modo corrente, não a ação de processamento:

```text
[⏎] Executar
→ ação que inicia o processamento do lote reconciliado

[Ins] Real / [Ins] Simulação
→ modo corrente em que a futura execução será realizada
```

O rótulo anterior `[Ins] Executar` e o rótulo anterior `[Ins] Dry-Run` são
referências `HISTORICA_SUBSTITUIDA` do controle universal, substituídas por
D-DRY-12. Não há ocorrência normativa antiga vigente. A substituição é apenas
visual: `executar` e `dry_run` continuam sendo os valores internos, e `Insert`
continua alternando o modo.

### Preservações funcionais de D-DRY-12

D-DRY-12 altera exclusivamente os rótulos do controle por `Insert`
(`[Ins] Real` e `[Ins] Simulação`) e não reimplementa seleção nem execução.
Os comportamentos abaixo, já implementados e provados antes da decisão,
permanecem preservados sem reimplementação. A evidência abreviada
`QA-Impl-P03` referencia
`docs/relatorios/RELATORIO_QA_POS_PATCH_IMPLEMENTACAO_H-0050_P03.md`.

| Comportamento preservado | Regra | Evidência anterior |
|---|---|---|
| Alternância individual por Espaço | Espaço alterna somente o item selecionável corrente. | QA-Impl-P03 |
| Itens não selecionáveis | Espaço não altera itens não selecionáveis. | QA-Impl-P03 |
| Seleção parcial | O lote pode conter subconjunto dos itens. | R03-03 e QA-Impl-P03 |
| Seleção coletiva | `Todos` continua permitindo seleção coletiva. | R03-01 e QA-Impl-P03 |
| Enter com seleção vazia | Aciona a semântica de `Todos`, sem chamar o executor. | R03-01 e QA-Impl-P03 |
| Execução total | Após `Todos`, Enter em `Executar` processa o lote total reconciliado. | R03-02 e QA-Impl-P03 |
| Execução parcial | Com seleção parcial, Enter em `Executar` processa somente os itens selecionados. | R03-03 e QA-Impl-P03 |
| Ordem reconciliada | Os IDs chegam ao executor na ordem reconciliada, sem alteração. | R03-04 e QA-Impl-P03 |
| Lote vazio na fronteira de execução | Um lote reconciliado vazio entregue diretamente ao controle de execução não chama o executor. | QA-Impl-P03 |
| `Insert` não altera a seleção | `Insert` alterna somente o modo, sem tocar na seleção. | QA-Impl-P03 |
| `Todos` não altera o modo | `Todos` altera somente a seleção, sem tocar no modo corrente. | QA-Impl-P03 |
| Execução parcial e total em ambos os modos | Execução parcial e total funcionam tanto em `executar` quanto em `dry_run`. | R03-02, R03-03 e QA-Impl-P03 |
| Acionamento semântico único de Enter | `[⏎] Todos` e `[⏎] Executar` continuam usando o mesmo acionamento semântico de Enter (seleciona quando o lote está vazio, executa quando não está). | QA-Impl-P03 |
| Valores internos entregues ao executor | O executor continua recebendo os valores internos `executar` ou `dry_run`. | R03-04 e QA-Impl-P03 |
| Retorno, nova abertura e redimensionamento | Permanecem conforme já documentados nas seções 6.3 e 14. | R03-05, R03-06, R03-07 e QA-Impl-P03 |

#### Distinção entre `Todos` e lote vazio na fronteira de execução

Na interação normal da tela, Enter com seleção vazia aciona `Todos` e não
chama o executor.

Na fronteira do controle de execução, uma requisição com lote reconciliado
vazio é rejeitada ou encerrada sem chamada ao executor.

Estas duas situações são distintas e não podem ser confundidas: nenhuma delas
significa que Enter com seleção vazia sai da tela, falha ou executa um lote
vazio.

#### Indicadores de seleção, transição de Enter e chips no redimensionamento

O controle de seleção usa dois indicadores nominais para cada item
selecionável:

```text
item não selecionado → ○
item selecionado → ●
```

Espaço no item selecionável corrente alterna `○` ↔ `●`. O cursor `→`
permanece distinto dos indicadores de seleção. Item não selecionável não
alterna por Espaço. Seleção parcial e seleção coletiva permanecem
preservadas. Os símbolos e indicadores são evidenciados por `R03-07`; a
alternância individual por Espaço é evidenciada por `QA-Impl-P03`. A R03 não
é atribuída como prova direta da tecla Espaço.

O chip de Enter transita nominalmente conforme o estado da seleção:

```text
seleção vazia
→ [⏎] Todos

Enter em Todos
→ seleciona todos os itens selecionáveis
→ não chama o executor
→ chip passa para [⏎] Executar

seleção não vazia
→ [⏎] Executar
```

Permanece preservada a distinção já documentada: o primeiro Enter em `Todos`
realiza seleção coletiva sem execução; o Enter em `Executar` processa o lote
reconciliado.

Em terminal estreito e depois de redimensionamentos, os chips permanecem
acessíveis, nenhum chip obrigatório desaparece e os rótulos permanecem
completos e semanticamente identificáveis: `[Ins] Real` e `[Ins] Simulação`
não são truncados de forma ambígua, e `[⏎] Todos` e `[⏎] Executar` continuam
distinguíveis. A barra pode ocupar mais linhas quando necessário, e o retorno
à largura normal não mantém linhas adicionais desnecessárias. Não há
requisito de largura fixa.

| Comportamento | Regra preservada | Evidência |
|---|---|---|
| Indicador individual | Espaço alterna o item selecionável entre `○` e `●`; cursor `→` permanece distinto | R03-07 + QA-Impl-P03 |
| Transição Todos/Executar | Seleção vazia mostra `[⏎] Todos`; após selecionar todos sem executar, mostra `[⏎] Executar` | R03-01, R03-02 + QA-Impl-P03 |
| Redimensionamento | Chips obrigatórios permanecem completos, acessíveis e distinguíveis em terminal estreito e após retorno à largura normal | R03-07 + QA-Impl-P03 quando aplicável |

## 5. Manifesto fechado de leitura

```yaml
leitura_integral:
  - docs/handoff/H-0050-controle-universal-execucao-real-dry-run.md
  - docs/relatorios/RELATORIO_QA_HANDOFF_H-0050.md
  - docs/adr/ADR-0040-padronizacao-universal-do-controle-de-execucao-real-e-dry-run.md
  - docs/contratos/contrato_tela_json.md
  - docs/contratos/contrato_registro_acoes.md
  - docs/contratos/contrato_json_console.md
  - docs/contratos/contrato_console.md
  - docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md
  - docs/nomenclatura/32_CONSOLE.md
  - docs/templates/TEMPLATE_HANDOFF_IMPLEMENTACAO.md
leitura_focal:
  - arquivo: demo/demo.py
    comando_busca: >-
      rg -n -C 5
      'Insert|KEY_IC|KEY_INSERT|acao_enter|executar|resultado_execucao|recarreg|carregar_tela'
      demo/demo.py
    finalidade: localizar captura real da tecla, acionamento e ciclo de abertura
    limite: 260
    ler_somente_saida_da_busca: true
  - arquivo: tela/carregamento/tela_json.py
    comando_busca: >-
      rg -n -C 4
      'acao_enter|controle_execucao|validar|campo|configuracao'
      tela/carregamento/tela_json.py
    finalidade: confirmar proprietário da validação e referências de ações
    limite: 180
    ler_somente_saida_da_busca: true
  - arquivo: tela/modelo.py
    comando_busca: >-
      rg -n -C 4
      'acao_enter|_raw|ModeloTela|estado|runtime'
      tela/modelo.py
    finalidade: confirmar transporte da configuração e limite do estado vivo
    limite: 180
    ler_somente_saida_da_busca: true
  - arquivo: tela/renderizacao/barra_menus.py
    comando_busca: >-
      rg -n -C 4
      'chips_especificos|estado_ativo_chips|cor_alerta|Insert|Executar|Dry-Run'
      tela/renderizacao/barra_menus.py
    finalidade: confirmar proprietário do chip e da aparência
    limite: 200
    ler_somente_saida_da_busca: true
  - arquivo: tela/navegacao.py
    comando_busca: >-
      rg -n -C 4
      'abrir|recarreg|suspens|retorn|instancia|pilha'
      tela/navegacao.py
    finalidade: confirmar limites do ciclo de vida
    limite: 180
    ler_somente_saida_da_busca: true
  - arquivo: tela/resultado_execucao.py
    comando_busca: >-
      rg -n -C 4
      'origem|retorn|resultado|sessao|modelo'
      tela/resultado_execucao.py
    finalidade: confirmar preservação sem alteração da tela de resultado
    limite: 160
    ler_somente_saida_da_busca: true
  - arquivo: demo/teste_demo.py
    comando_busca: >-
      rg -n -C 3
      'Insert|acao_enter|resultado_execucao|recarreg|H-0044|h0044'
      demo/teste_demo.py
    finalidade: confirmar integração e regressões da demonstração
    limite: 200
    ler_somente_saida_da_busca: true
buscas_autorizadas:
  escopo:
    - tela
    - demo
  termos:
    - acao_enter
    - executar_acao
    - resolver_acao
    - registro_acoes
    - registrar_acao
    - KEY_IC
    - KEY_INSERT
    - lote_reconciliado
  finalidade: identificar proprietários vigentes e impedir omissão de caminho indispensável.
nao_ler:
  - outros_relatorios
  - outras_ADRs
  - outros_handoffs
  - outros_contratos
  - outros_modulos_de_nomenclatura
  - backlog_indice_e_historico
  - codigo_do_Pipeline
  - historico_Git
  - arquivos_por_proximidade_tematica
```

Ler somente as saídas focais. Se faltar arquivo indispensável, parar antes de
alterar com `LEITURA_ADICIONAL_NECESSARIA`, informando caminho e alvo exatos.

## 6. Escopo da implementação

### 6.1 Arquivos autorizados

```yaml
arquivos:
  - caminho: tela/carregamento/tela_json.py
    operacao: alterar
    finalidade: validar o objeto raiz fechado controle_execucao.
    limites: >-
      exigir somente modo_inicial, sem default nem estado vivo; não criar
      metadados de compatibilidade no JSON.
  - caminho: tela/registro_acoes.py
    operacao: criar
    finalidade: >-
      manter registros autoritativos de ações, resolver ações pela identidade
      vigente e fornecer categoria e modos implementados sem depender da tela.
    limites: >-
      não criar dispatcher geral, descoberta automática, plugin system,
      persistência, configuração paralela ou migração global.
  - caminho: tela/controle_execucao.py
    operacao: criar
    finalidade: >-
      validar elegibilidade por registro, manter modo por instância, alternar,
      produzir o chip específico e construir a captura privada imutável.
    limites: >-
      não criar estado global, protocolo público, persistência, dispatcher ou
      dependência de H-0044.
  - caminho: tela/renderizacao/barra_menus.py
    operacao: alterar
    finalidade: representar o chip específico universal e sua ordem/alerta.
    limites: >-
      não criar chip canônico, não alterar chips existentes nem inferir o modo
      por ID ou rótulo.
  - caminho: demo/executor_controle_execucao.py
    operacao: criar
    finalidade: consumir somente a captura privada e a fixture sintética.
    limites: sem acesso a tela, modelo, controlador, renderer ou estado global.
  - caminho: demo/demo.py
    operacao: alterar
    finalidade: >-
      registrar a ação demonstrativa no registro universal e tratar no ponto
      real a captura de Insert, Enter, suspensão, retorno, abertura e recarga.
    limites: preservar integralmente todos os caminhos H-0044.
  - caminho: config/telas/demo/h0050_controle_execucao_universal.json
    operacao: criar
    finalidade: demonstração principal, iniciada em executar.
    limites: controle_execucao contém exclusivamente modo_inicial.
  - caminho: config/telas/demo/h0050_controle_execucao_universal_dry_run_inicial.json
    operacao: criar
    finalidade: demonstração adicional, iniciada em dry_run.
    limites: divergir apenas em identidade, textos necessários e modo_inicial.
  - caminho: demo/fixtures/h0050_execucao_universal_fixture.json
    operacao: criar
    finalidade: baseline sintética determinística e imutável.
  - caminho: tela/teste_loader.py
    operacao: alterar
    finalidade: testar validação do objeto fechado e ausência de default.
  - caminho: tela/teste_registro_acoes.py
    operacao: criar
    finalidade: >-
      testar registro, resolução, enumerações, subconjuntos de modos, falha
      fechada e elegibilidade de telas adotantes.
  - caminho: tela/teste_controle_execucao.py
    operacao: criar
    finalidade: testar modo por instância, captura privada e ciclo de vida.
  - caminho: tela/testes_renderizador/barra_menus.py
    operacao: alterar
    finalidade: testar presença, ordem, rótulo, atividade e cor resolvida do chip.
  - caminho: demo/teste_executor_controle_execucao.py
    operacao: criar
    finalidade: provar isolamento do executor e modo capturado.
  - caminho: demo/teste_demo.py
    operacao: alterar
    finalidade: provar o roteiro integrado H-0050 e a fronteira com H-0044.
  - caminho: docs/relatorios/IMP-0050-controle-universal-execucao-real-dry-run.md
    operacao: criar
    finalidade: relatório factual da implementação.
```

Não houve proprietário vigente mais adequado nas buscas autorizadas; o
registro fica nominalmente em `tela/registro_acoes.py` e seu teste em
`tela/teste_registro_acoes.py`. `tela/renderizador.py` permanece fachada não
alterável: o manifesto não autoriza sua modificação. A captura física de
`Insert` pertence a `demo/demo.py`, não a essa fachada.

### 6.2 Arquivos preservados ou proibidos

- `config/telas/demo/h0044_fluxo_execucao_integrado.json`;
- `tela/fluxo_execucao.py` e `tela/teste_fluxo_execucao.py`;
- `tela/resultado_execucao.py` e `tela/navegacao.py`;
- `tela/renderizador.py`;
- ADR-0037, H-0044, contratos, ADRs, nomenclatura, índice, backlog e histórico;
- toda configuração, fixture, código e teste do H-0044, salvo os ramos novos e
  explicitamente isolados dentro de `demo/demo.py` e `demo/teste_demo.py`.

### 6.3 Escopo positivo

- `controle_execucao` é objeto opcional fechado: quando presente, contém
  exatamente `modo_inicial`, aceita somente `executar` ou `dry_run`, não tem
  default nem estado de runtime e rejeita propriedade interna adicional.
- O registro é infraestrutura reutilizável e autoridade de cada ação. Toda
  entrada resolvida declara `categoria` em `processo`, `navegacao` ou
  `visualizacao`; ação de processo declara somente os valores realmente
  implementados em `modos_execucao_aceitos`.
- Para tela adotante, identificar ações relevantes exclusivamente por campos e
  referências já vigentes; resolver cada uma no registro; exigir categoria
  válida; exigir modos de processo; exigir ambos os modos em todo processo; e
  falhar antes da execução diante de ausência ou insuficiência. Navegação e
  visualização são resolvidas e classificadas, mas não exigem ambos os modos.
- Criar um modo corrente único por instância, alternado apenas por `Insert`,
  com chip `[Ins] Real` ou `[Ins] Simulação`, ativo nos dois estados. O
  rótulo é a indicação primária; em `dry_run`, o texto usa a cor resolvida por
  `cor_alerta` como reforço. `[⏎] Executar` permanece o chip de ação que
  inicia o processamento.
- No acionamento de processo, reconciliar o lote pelos mecanismos vigentes,
  capturar o modo e entregar somente a captura privada à ação registrada.
- Registrar a ação sintética H-0050 pelo mesmo mecanismo, como `processo` com
  ambos os modos. A associação fica em `demo/demo.py`, sem metadado no JSON e
  sem exceção reconhecida por identidade da demonstração.
- Preservar o modo em suspensão e retorno da mesma origem. Seleção, foco,
  cursor e página preservam as estruturas existentes; o modo é a nova
  obrigação específica deste controle. Nova abertura ou recarga cria nova
  instância iniciada por `modo_inicial`.

### 6.5 Aplicação futura focal de D-DRY-12

O patch de implementação posterior deve alterar somente o necessário para
apresentar `[Ins] Real` e `[Ins] Simulação`, quando os literais forem
realmente proprietários da camada. São candidatas, sem autorização automática
para alterar todas elas:

- composição da barra de menus;
- configuração demonstrativa;
- testes da barra e da demonstração;
- textos de fixture ou resultado que exponham o rótulo;
- roteiro de validação manual.

Nenhuma dessas camadas pode alterar o schema, os valores internos `executar`
e `dry_run`, o registro de ações, a requisição capturada, o executor, o
resultado, a tecla `Insert`, a atividade do controle ou o H-0044. O patch de
implementação posterior exige QA automatizado focal próprio e validação manual
complementar dos novos rótulos.

### 6.4 Escopo negativo

- criar campo de compatibilidade, categoria ou modos aceitos no `tela.json`;
- registry configurado por arquivo, descoberta, reflexão, varredura ou
  migração global de ações;
- inferir compatibilidade por ID, nome, texto, rótulo, script, flag,
  adaptador ou comportamento observado;
- alterar protocolo público vigente ou apresentar a representação interna como
  protocolo universal;
- alterar a especialização ADR-0037/H-0044, arquivos preservados ou o ciclo
  próprio da tela de resultado;
- persistir modo, associá-lo a console, item, foco, cursor, página, seleção ou
  identidade do lote; criar dispatcher, plugin system ou estado global;
- stage ou commit.

## 7. Configuração, registro, runtime e requisição

### 7.1 Configuração fechada

```json
{
  "controle_execucao": {
    "modo_inicial": "executar"
  }
}
```

Ausência do objeto significa não adoção. Quando presente, objeto, campo,
tipo, valor, ausência do campo e propriedade interna adicional são validados
de forma fechada; configuração inválida falha como `CONFIGURACAO_INVALIDA` com
caminho preciso. Os únicos valores de configuração permanecem `executar` e
`dry_run`; `real` e `simulacao` não são valores aceitos, aliases ou campos.
Extensão futura exige nova decisão e atualização contratual.

### 7.2 Registro e elegibilidade

O registro resolve a referência já vigente para uma entrada autoritativa. Ação
ausente, identidade não resolvida, categoria ausente ou desconhecida, processo
sem `modos_execucao_aceitos`, valor de modo desconhecido ou processo sem ambos
os modos produz falha fechada antes de execução. Ações legadas não precisam ser
migradas, mas uma não registrada não pode ser usada como processo por tela
adotante. O JSON não declara nem duplica esses metadados.

### 7.3 Estado, representação e captura privada

O controlador recebe configuração validada e registro já resolvido, pertence à
instância aberta e não é gravado em `ModeloTela._raw` nem no JSON. A transição é:

```text
abertura ou recarga → novo modo = modo_inicial
Insert              → executar ↔ dry_run
suspensão e retorno → mesma instância, mesmo modo
encerramento        → descartar sem escrita
```

A implementação cria em `tela/controle_execucao.py` uma dataclass privada,
congelada e não serializada, por exemplo `RequisicaoExecucaoCapturada`, com o
lote reconciliado em sua ordem vigente e o modo capturado. Essa estrutura é
detalhe interno reversível: não muda a identidade do lote, não é API, não
substitui protocolo público e não pode ser alterada por `Insert` posterior. O
executor H-0050 recebe somente essa captura e a fixture.

## 8. Entradas, fixtures, temporários e saídas

```yaml
entradas_reais:
  - configuracoes_estruturais_H-0050
  - interacoes_de_selecao_Insert_Enter_Esc_reabertura_e_recarga
fixtures:
  - demo/fixtures/h0050_execucao_universal_fixture.json
temporarios_operacionais:
  necessidade: somente_se_o_executor_sintetico_precisar_de_copia_de_trabalho
  limpeza: finally_em_sucesso_falha_e_interrupcao
  proibicao: nao_alterar_config_ou_docs
saidas_persistentes:
  - somente_arquivos_nominais_deste_handoff
politica_de_sobrescrita:
  fixture_baseline: nunca
  H-0044: nunca
```

## 9. Tarefas autorizadas

1. Validar o objeto fechado e transportar apenas sua configuração inicial.
2. Criar o registro, resolver as referências vigentes e aplicar a elegibilidade
   de tela adotante antes de executar.
3. Criar controlador por instância e a captura privada imutável.
4. Derivar o chip específico na barra e tratar `Insert` no ponto real em
   `demo/demo.py`.
5. Registrar e integrar a ação sintética H-0050, o executor, a fixture e as
   duas configurações, sem tocar H-0044.
6. Preservar suspensão/retorno da origem e reinicializar somente em nova
   abertura ou recarga.
7. Implementar os testes, executar as verificações previstas e criar o
   relatório `IMP-0050` pelo template canônico.
8. Manter a validação TTY exclusivamente para `USUARIO_EM_TTY_REAL`, registrando
   pendência factual até observação humana.

## 10. Testes obrigatórios

| Área | Casos e expectativa |
|---|---|
| Objeto | ausência válida; dois modos válidos; campo ausente, tipo/valor inválido e propriedade adicional rejeitados; sem default. |
| Registro | categoria válida em cada valor; categoria ausente ou desconhecida; processo com ambos, apenas executar, apenas dry_run e sem modos; ação ausente; falha fechada. |
| Elegibilidade | navegação e visualização fora da exigência de ambos; tela sem controle não exige compatibilidade; tela adotante com processo de um modo é rejeitada; todos os processos com ambos são aceitos. |
| Anti-inferência | compatibilidade não deriva de nome, texto, script ou adaptador; registro não depende do JSON; ação demonstrativa resolve pelo mesmo registro. |
| Runtime e requisição | um modo por instância; Insert alterna os dois; captura contém lote reconciliado e modo; identidade/ordem do lote preservadas; alteração posterior não retroage; executor não consulta interface. |
| Barra e ciclo | chip específico, ordenado, ativo e com cor resolvida por cor_alerta; suspensão/retorno preservam; reabertura/recarga reinicializam; redimensionamento preserva semântica. |
| Reconciliação D-DRY-12 | `executar` apresenta `[Ins] Real` com aparência ativa normal; `dry_run` apresenta `[Ins] Simulação` com `cor_alerta`; ambos permanecem ativos e alternáveis por Insert; `[⏎] Todos` e `[⏎] Executar` permanecem inalterados. |
| Regressão | H-0044 não recebe delta nem regressão. |

Executar a partir da raiz:

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_loader.py tela/teste_registro_acoes.py tela/teste_controle_execucao.py tela/testes_renderizador/barra_menus.py demo/teste_executor_controle_execucao.py demo/teste_demo.py tela/teste_fluxo_execucao.py
PYTHONDONTWRITEBYTECODE=1 python -m pytest
```

## 11. Demonstração operacional e validação manual

O roteiro automatizado abre a configuração principal, seleciona dois itens,
alterna por Insert, aciona Enter, prova o modo recebido e os IDs reconciliados,
retorna preservando o modo e reabre/recarrega para provar `modo_inicial`.
Depois abre a configuração secundária em `dry_run`. Também confirma que H-0044
permanece em seu fluxo próprio. A R03 aprovou integralmente o comportamento
funcional anterior (7 de 7 critérios); D-DRY-12 foi decidida depois e não torna
a R03 uma falha. A implementação posterior exige QA automatizado focal próprio.
Uma validação manual complementar deve conferir somente os novos rótulos e
suas preservações visuais, sem repetir os sete critérios funcionais da R03,
salvo regressão detectada pelo QA.

```yaml
cwd: "."
comando: python demo/demo.py h0050_controle_execucao_universal
configuracao: config/telas/demo/h0050_controle_execucao_universal.json
fixture: demo/fixtures/h0050_execucao_universal_fixture.json
prova_semantica: modo recebido, lote reconciliado, retorno e reinicializacao
arquivos_persistentes: somente os declarados neste handoff
validacao_manual:
  executor_exclusivo: USUARIO_EM_TTY_REAL
  roteiro: >-
    Abrir a tela com modo inicial executar; confirmar [Ins] Real; pressionar
    Insert; confirmar [Ins] Simulação com cor_alerta; confirmar que [⏎]
    Executar continua separado; executar um lote em Simulação; confirmar que o
    resultado interno continua sendo dry_run; retornar e confirmar [Ins]
    Simulação; reabrir e confirmar [Ins] Real; redimensionar e confirmar os
    rótulos completos.
  gabarito:
    resultado_observado:
      - CONFORME
      - 'DIVERGENTE: <etapa e comportamento visual/funcional observado>'
```

## 12. Critérios de aceite

| ID | Critério | Evidência independente esperada |
|---|---|---|
| CA-01 | Objeto fechado validado. | Testes de loader com propriedade adicional e valores inválidos. |
| CA-02 | Registro universal reutilizável é a autoridade. | Teste proprietário de registro e resolução. |
| CA-03 | Categorias e modos são fechados e falham de forma fechada. | Matriz de entradas incompletas, inválidas e válidas. |
| CA-04 | Ação H-0050 usa o mesmo registro, sem exceção por ID. | Teste integrado de resolução da ação demonstrativa. |
| CA-05 | Não há metadado de compatibilidade no JSON. | Inspeção de configuração e teste anti-inferência. |
| CA-06 | Requisição é privada, explícita, imutável e reversível. | Teste do executor antes/depois de Insert. |
| CA-07 | Não há migração global e H-0044 não recebe delta. | Diff nominal e regressão H-0044. |
| CA-08 | Modo e chip obedecem ciclo de vida por instância. | Testes de controlador, barra e roteiro integrado. |
| CA-09 | O estado interno `executar` apresenta `[Ins] Real`. | Teste focal de renderização e demonstração. |
| CA-10 | O estado interno `dry_run` apresenta `[Ins] Simulação`. | Teste focal de renderização e demonstração. |
| CA-11 | `Insert` alterna `Real` → `Simulação` e `Simulação` → `Real`. | Teste focal da alternância por instância. |
| CA-12 | `[Ins] Real` usa aparência ativa normal. | Teste focal da aparência resolvida. |
| CA-13 | `[Ins] Simulação` usa `cor_alerta`. | Teste focal da aparência resolvida. |
| CA-14 | Os dois chips permanecem ativos. | Teste de atividade nos dois estados. |
| CA-15 | `[⏎] Executar` permanece inalterado e separado do modo. | Teste da barra e inspeção visual. |
| CA-16 | `[⏎] Todos` permanece inalterado. | Teste da barra e regressão de seleção coletiva. |
| CA-17 | Seleção e execução continuam funcionais. | Teste integrado do lote reconciliado. |
| CA-18 | O resultado continua recebendo `executar` ou `dry_run`. | Teste do executor e da requisição capturada. |
| CA-19 | Configuração e requisição não usam `real` ou `simulacao`. | Inspeção do schema, fixtures e captura. |
| CA-20 | Nova abertura continua obedecendo a `modo_inicial`. | Teste de reabertura e recarga. |
| CA-21 | Retorno continua preservando o estado interno da mesma instância. | Teste de suspensão e retorno. |
| CA-22 | H-0044 permanece sem delta. | Diff nominal e regressão focal. |
| CA-23 | Terminal estreito exibe os chips com rótulos completos. | QA automatizado focal e roteiro manual complementar. |

## 13. Relatório da execução

Criar exclusivamente:

```text
docs/relatorios/IMP-0050-controle-universal-execucao-real-dry-run.md
```

Usar `docs/templates/TEMPLATE_RELATORIO_IMPL.md`, com fatos de arquivos,
registro, captura privada, demonstração, testes, preservações, bloqueios e
estado da validação manual. Não reproduzir este handoff nem aprovar a entrega.

## 14. Preservações e exceção focal

Permanecem materialmente inalterados D-DRY-01 a D-DRY-11, e D-DRY-12 é
incorporada somente quanto à apresentação. Permanecem preservados o chip
específico não canônico, `Insert`, os valores internos `executar` e `dry_run`,
`controle_execucao.modo_inicial`, a enumeração fechada do schema, o estado vivo
no runtime, a atividade nos dois estados, a aparência ativa normal de
`executar`, `cor_alerta` de `dry_run`, `[⏎] Todos`, `[⏎] Executar`, seleção,
execução, captura privada, registro universal, falha fechada, retorno,
reinicialização, redimensionamento, `dry_run_ativo` e a especialização
ADR-0037/H-0044. Todos os achados `MV-H0050-01` a `MV-H0050-06` permanecem
resolvidos, assim como a aprovação manual R03.

Os únicos rótulos vigentes do controle universal são `[Ins] Real` e
`[Ins] Simulação`. As ocorrências `[Ins] Executar` e `[Ins] Dry-Run` do
controle universal só podem aparecer como `HISTORICA_SUBSTITUIDA`; não são
ocorrências normativas vigentes. O `[Ins] Dry-Run` focal do H-0044 é
`ESPECIALIZACAO_FOCAL_H0044`, permanece inalterado e não é controle universal.
`DEFEITO_REMANESCENTE`: nenhum.
A ausência de Insert em resultado decorre de o controle pertencer à tela de
origem e não cria política global nova.

## 15. Condições de bloqueio

```yaml
BLOCKED_USER_DECISION:
  quando: decisao_material_nova_for_indispensavel
BLOCKED_DOCUMENTATION:
  quando: autoridades aplicadas forem contraditórias
LEITURA_ADICIONAL_NECESSARIA:
  quando: saida_focal_nao_bastar
  resposta: caminho_e_alvo_exatos
```

Não contornar bloqueio por inferência, leitura ampla, alteração de autoridade
ou ampliação silenciosa do manifesto.

## 16. Limite de encerramento e resposta terminal

Este patch documental atualiza somente o H-0050, cria o relatório P06 e para.
Não implementar, testar, validar TTY, fazer QA formal do próprio patch,
aprovar a própria entrega, preparar stage ou commit, nem iniciar reconciliação
do H-0044. A implementação posterior deverá alterar somente a apresentação,
executar QA automatizado focal e registrar a validação manual complementar.

Retornar somente:

```yaml
status: HANDOFF_PATCHED_AWAITING_QA
relatorio: docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0050_P06.md
artefatos:
  - docs/handoff/H-0050-controle-universal-execucao-real-dry-run.md
proxima_acao: QA_POS_PATCH_HANDOFF_P06
```

## 17. Consolidação final

Esta seção registra o estado documental vigente após o QA técnico final e as
validações manuais. O frontmatter e a seção 16 permanecem como histórico do
patch documental P06; não representam o estado final do ciclo.

~~~yaml
estado_final: IMPLEMENTATION_APPROVED
handoff:
  id: H-0050
  estado: concluido
item:
  id: ITEM-0020
  estado: concluido
ADR:
  id: ADR-0040
  status: aceita_e_aplicada
implementacao:
  status_final: IMPLEMENTATION_APPROVED
  patch_final: P04
  testes_focais: 268_passed
  suite_completa: 1037_passed
  prova_isolada_h0050: 17_passed
  valores_internos:
    - executar
    - dry_run
  rotulos_visuais:
    executar: "[Ins] Real"
    dry_run: "[Ins] Simulação"
validacao_manual:
  funcional:
    rodada: R03
    resultado: MANUAL_VALIDATION_APPROVED
    criterios: 7_de_7
  complementar_visual:
    rodada: R04
    resultado: MANUAL_VALIDATION_APPROVED
    criterios: 4_de_4
preservacao:
  h0044: sem_delta
  rotulo_focal_h0044: "[Ins] Dry-Run"
bloqueios: []
proxima_acao: FECHAMENTO_MANUAL
~~~
