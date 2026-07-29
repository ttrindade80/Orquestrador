---
name: H-0042-protocolo-focal-execucao-sintetica-reversivel
description: "Autoriza a implementação do Handoff 2 do ITEM-0006 (ADR-0034, especializada pela ADR-0035): protocolo focal de execução sintética reversível — motor focal compartilhado, executor sintético, dry-run, execução real sobre cópia temporária, documento de resultado multinível, controles sintéticos, interrupção e limpeza protegida"
metadata:
  type: handoff_implementacao
  status: READY_FOR_IMPLEMENTATION
  id: H-0042
  data_criacao: 2026-07-29
rastreabilidade:
  contrato_alvo: docs/contratos/contrato_json_console.md
  adr_relacionadas:
    - docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md
    - docs/adr/ADR-0035-protocolo-focal-execucao-sintetica-reversivel.md
  issues_relacionadas:
    - ITEM-0006
  handoffs_anteriores:
    - H-0041
---

# H-0042 — Implementar o protocolo focal de execução sintética reversível

## 1. Etapa única

Este handoff autoriza exclusivamente:

`IMPLEMENTAR`

Ele não autoriza QA, aprovação, commit ou início de outro ciclo.

## 2. Ordem de autoridade

1. decisão explícita do usuário;
2. ADRs aprovadas e aplicadas;
3. contratos ativos;
4. este handoff.

Se houver falta, divergência ou decisão nova necessária, bloquear.

## 3. Estado comprovado

- Branch `master`, HEAD `f4b5df1`, stage vazio; worktree contendo somente os
  artefatos acumulados da ADR-0035 (`docs/adr/ADR-0035-...md` novo;
  `docs/relatorios/RELATORIO_QA_ADR-0035.md`,
  `docs/relatorios/RELATORIO_APLICACAO_ADR-0035.md`,
  `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0035.md` novos;
  `docs/adr/INDICE_ADR.md`, `docs/backlog.md`,
  `docs/contratos/contrato_console.md`,
  `docs/contratos/contrato_json_console.md` modificados) — confirmado por
  leitura Git real nesta execução.
- ADR-0035: `status: aceita e aplicada`; `qa_adr: ADR_APPROVED`;
  `qa_aplicacao: ADR_APPLICATION_APPROVED`; `achados_pendentes: []`
  (transportado pelo estado mínimo desta etapa; leitura de relatório
  dispensada).
- `docs/backlog.md`, `ITEM-0006`: `Status: em_andamento`; "Próxima ação"
  aponta exatamente para a criação deste Handoff 2 (confirmado por leitura
  direta).
- `H-0041` concluído no commit `f4b5df1`: `tela/selecao.py::selecao(console,
  estado)` já devolve a seleção reconciliada (D-SEL-03) e ordenada pela
  ordem lógica do console (D-SEL-02) — fonte direta do `lote reconciliado`
  que alimenta o campo `ids` de `selecao_execucao.v1` deste handoff; nenhuma
  nova função de reconciliação é necessária ou autorizada.
- `demo/demo.py` (leitura focal: `criar_estado_inicial`, `processar_comando`,
  `renderizar_estado`, `main`, `KeyboardInterrupt`) confirma que o ciclo de
  estado da sessão TUI permanece o único vigente e que `Enter` com seleção
  continua sem dispatch para operação externa — o chip `Executar` permanece
  inativo (D-SEL-07/D-SEL-21). Este handoff não pode alterar esse dispatch.
- `demo/teste_demo_selecao.py` (leitura focal) confirma o padrão vigente de
  teste de integração via `subprocess`/PTY do ponto de entrada TTY do
  H-0041 (usado para `H0041-MANUAL-R02-001`) — modelo reaproveitável de
  invocação de processo externo com captura separada de código, `stdout` e
  `stderr`, já validado no projeto.
- `tela/teste_selecao.py` (leitura focal) confirma que `selecao.selecao`
  devolve a lista já reconciliada e ordenada (D-SEL-02/D-SEL-03), pronta
  para alimentar `ids` sem redefinição de reconciliação por este handoff.
- Não existem hoje `tela/execucao_focal.py`, `demo/executor_sintetico.py`,
  `demo/demo_execucao_focal.py` nem o diretório `demo/fixtures/` —
  confirmado por ausência no estado Git e nos manifestos de leitura.
- `contrato_json_console.md` §14 e `contrato_console.md` §23.6 já fecham,
  como aplicação da ADR-0035, a autoridade comportamental completa do
  protocolo, do documento de resultado e dos controles sintéticos deste
  handoff — este documento autoriza a implementação dessas decisões já
  fechadas; não reabre nem redecide seu conteúdo.

### Fronteira arquitetural obrigatória

```yaml
binding_real: nao_definido
pipeline_real: nao_invocado
registry_generico: fora_de_escopo
dispatcher_generico: fora_de_escopo
consulta_de_dados: fora_de_escopo
interface_TUI:
  Enter_Executar: inativo
  abertura_resultado: inexistente_neste_handoff
```

A implementação autorizada por este handoff é prova focal de protocolo e
execução. Não pode ser descrita, documentada ou comunicada como binding
definitivo entre Orquestrador e Pipeline.

## 4. Objetivo

Implementar, de forma isolada e testável sem depender da ativação do chip
`Executar` nem da tela de resultado, o protocolo focal de execução
sintética reversível do Handoff 2 do `ITEM-0006` (ADR-0034 D-SEL-12 a
D-SEL-15, D-SEL-19, D-SEL-21; especialização ADR-0035 H2-ESP-01 a
H2-ESP-18):

```text
lote reconciliado de IDs
→ entrada selecao_execucao.v1
→ invocação direta de executor sintético
→ resultado.json multinível
→ classificação do processo
→ inspeção dos efeitos
→ limpeza integral dos temporários
```

## 5. Manifesto fechado de leitura

```yaml
leitura_integral:
  - docs/adr/ADR-0035-protocolo-focal-execucao-sintetica-reversivel.md
  - tela/selecao.py
  - demo/demo_selecao.py

leitura_focal:
  - arquivo: docs/contratos/contrato_json_console.md
    comando_busca: sed -n '1282,1636p' docs/contratos/contrato_json_console.md
    objetivo: >-
      ler exclusivamente a seção 14 (protocolo provisório de execução
      focal e envelope de resultado) — autoridade comportamental completa
      do documento de resultado, CLI, diretório temporário, canais,
      classificação e controles sintéticos
    limite: 360 linhas
    ler_somente_saida_da_busca: true
  - arquivo: docs/contratos/contrato_console.md
    comando_busca: sed -n '1111,1256p' docs/contratos/contrato_console.md
    objetivo: >-
      ler exclusivamente a seção 23 (seleção múltipla e operação focal) —
      fronteira comportamental do Handoff 2 sobre a entrada da operação
      consumidora e remissões
    limite: 150 linhas
    ler_somente_saida_da_busca: true
  - arquivo: demo/demo.py
    comando_busca: >-
      grep -n "criar_estado_inicial\|processar_comando\|renderizar_estado\|
      main\|KeyboardInterrupt" demo/demo.py
    objetivo: >-
      confirmar que o dispatch de Enter/Executar permanece intocado; este
      handoff não integra a sessão TUI nem o loop principal
    limite: 80 linhas
    ler_somente_saida_da_busca: true
  - arquivo: tela/teste_selecao.py
    comando_busca: >-
      grep -n "reconcili\|orden\|todos\|ids\|selecion" tela/teste_selecao.py
    objetivo: >-
      confirmar a forma já disponível da saída reconciliada/ordenada de
      tela/selecao.py, reaproveitada como modelo do campo ids das fixtures
      de entrada, sem redefinir reconciliação ou seleção
    limite: 160 linhas
    ler_somente_saida_da_busca: true

buscas_autorizadas: []

nao_ler:
  - docs/relatorios/**
  - docs/adr/**, exceto ADR-0035
  - docs/handoff/**
  - docs/contratos/**, exceto os dois trechos focais listados acima
  - docs/nomenclatura/**
  - docs/arquivo/**
  - outras demonstrações e testes além dos listados
  - configuração de telas (config/telas/**)
  - documentos do sistema de prompts
```

Para leitura focal, execute o comando indicado e leia somente sua saída.
Não abra o arquivo inteiro por conveniência. Se a saída for insuficiente,
pare e solicite expansão focal; não amplie autonomamente o contexto.

## 6. Escopo da implementação

### 6.1 Arquivos e diretórios autorizados

```yaml
arquivos_novos_a_criar:
  motor_focal_compartilhado:
    - caminho: tela/execucao_focal.py
      finalidade: >-
        preparar entrada e temporários, invocar o processo autorizado,
        capturar código/stdout/stderr, preservar o conteúdo bruto de
        resultado.json, classificar o processo (D-SEL-14) e garantir
        limpeza protegida
    - caminho: tela/teste_execucao_focal.py
      finalidade: >-
        testes unitários e de integração da invocação focal,
        classificação, temporários, canais, falhas e interrupção

  executor_e_demonstracao_sinteticos:
    - caminho: demo/executor_sintetico.py
      finalidade: >-
        CLI sintética que lê selecao_execucao.v1, localiza
        fixture_trabalho.json como irmã de resultado.json, executa
        dry-run ou mutação real e grava o documento multinível
    - caminho: demo/demo_execucao_focal.py
      finalidade: >-
        demonstração não interativa e reproduzível dos cenários
        autorizados, reutilizando tela/execucao_focal.py, sem ativar a
        interface
    - caminho: demo/teste_executor_sintetico.py
      finalidade: >-
        testes focais da CLI, validação da entrada, efeito por item,
        documento estruturado, canais e controles sintéticos
    - caminho: demo/teste_demo_execucao_focal.py
      finalidade: >-
        testes da demonstração completa, baseline imutável, cópia
        temporária, limpeza e resultados observáveis

fixture:
  diretorio_novo:
    - caminho: demo/fixtures/
      condicao: criar_somente_se_ainda_nao_existir
  arquivos:
    - caminho: demo/fixtures/h0042_fixture_execucao.json
    - caminho: demo/fixtures/h0042_entrada_sucesso.json
    - caminho: demo/fixtures/h0042_entrada_sucesso_aviso.json
    - caminho: demo/fixtures/h0042_entrada_parcial.json
    - caminho: demo/fixtures/h0042_entrada_falha_operacional.json
    - caminho: demo/fixtures/h0042_entrada_resultado_invalido.json
    - caminho: demo/fixtures/h0042_entrada_interrupcao.json

relatorio_de_implementacao:
  caminho: docs/relatorios/IMP-0042-protocolo-focal-execucao-sintetica-reversivel.md
  template: docs/templates/TEMPLATE_RELATORIO_IMPL.md
```

Diretórios ainda inexistentes podem ser criados somente quando aparecerem
nominalmente nesta lista — `demo/fixtures/` é o único diretório novo
autorizado, e somente se ainda não existir. Nenhum outro diretório novo é
necessário.

### 6.2 Arquivos e diretórios preservados ou proibidos

```text
demo/demo.py
demo/demo_selecao.py
demo/teste_demo.py
demo/teste_demo_selecao.py
tela/selecao.py
tela/navegacao.py
tela/renderizador.py
tela/loader.py
config/estilo.json
config/telas/demo/h0041_selecao_multipla_oito_itens.json
```

Nenhum arquivo existente precisa ser alterado para entregar este handoff.
Preservação adicional:

- `docs/adr/**`, `docs/backlog.md`, `docs/contratos/**`,
  `docs/nomenclatura/**`, `docs/handoff/**` (exceto o próprio arquivo
  criado por este handoff) — alteração normativa fora deste ciclo.
- Qualquer arquivo permanente de resultado fora do diretório temporário de
  cada invocação — proibido; nenhum `resultado.json` permanente pode ser
  criado.
- Qualquer arquivo além da lista nominal da seção 6.1 — exige a exceção
  operacional da seção 14 antes de qualquer alteração.

### 6.3 Escopo positivo

- Validação estrita de `selecao_execucao.v1`, com rejeição integral e sem
  normalização silenciosa.
- Invocação do executor sintético por processo separado (subprocesso),
  nunca por chamada direta de função quando se tratar da prova de
  protocolo real.
- Captura separada de código de saída, `stdout` e `stderr`.
- Diretório temporário exclusivo por invocação, com nomes internos fixos
  (`entrada.json`, `resultado.json`, `fixture_trabalho.json`) e limpeza
  protegida por `finally` em sucesso, falha e interrupção.
- Baseline permanente imutável; toda mutação ocorre exclusivamente em
  cópia de trabalho temporária.
- `dry-run` (previsão sem alteração) e execução real (alteração da cópia).
- Documento de resultado multinível (`conjuntos_campos`), com seções
  `Resumo` e `Itens`, schema único para os dois modos.
- Classificação de `status_global` (`sucesso`/`parcial`/`falha`) e
  classificação de processo (código `0` + JSON válido) como camadas
  independentes — resultado parcial retorna código `0`.
- Controles sintéticos reservados (`__falha_operacional__`,
  `__resultado_invalido__`, `__interrupcao__`), exclusivos de teste e
  demonstração.
- Preservação literal (byte a byte) de resultado inválido produzido pelo
  controle `__resultado_invalido__`.
- Interrupção protegida: alteração observável antes da interrupção,
  documento válido com `status: interrompido`, código `130`, limpeza
  garantida.
- Inspeção automatizada dos efeitos e da limpeza por mecanismo interno de
  teste, sem nova opção pública na CLI.

### 6.4 Escopo negativo

- Binding real entre Orquestrador e Pipeline.
- Pipeline real, consulta sintética de itens selecionáveis, registry,
  dispatcher, catálogo de ações.
- `request_id`, snapshot, idempotência persistente, concorrência, travas,
  `force`, comando shell declarativo.
- Ativação de `Enter`/`Executar` na interface; alteração da seleção
  múltipla já concluída pelo H-0041.
- Carregamento do resultado no console; tela `resultado_execucao`;
  envelope visual de erro; abertura e retorno entre telas; paginação.
- Modo não verboso da apresentação do resultado.
- Alteração de contrato, ADR, nomenclatura ou backlog.
- Criação de arquivo permanente de resultado.

## 6.5 Protocolo técnico obrigatório

Esta seção não decide nada novo — organiza, para a implementação, as
decisões já fechadas por H2-ESP-01 a H2-ESP-18 (ADR-0035) e propagadas em
`contrato_json_console.md` §14 e `contrato_console.md` §23.6.

### 6.5.1 Entrada e validação (`selecao_execucao.v1`)

```json
{
  "schema": "selecao_execucao.v1",
  "ids": ["item_01", "item_03"]
}
```

Rejeitar integralmente antes de qualquer mutação quando:

- a raiz não for objeto;
- `schema` estiver ausente ou divergente de `selecao_execucao.v1`;
- `ids` estiver ausente ou não for array;
- a lista estiver vazia;
- algum ID não for string;
- algum ID for vazio;
- houver ID duplicado.

```yaml
normalizacao_silenciosa: proibida
processamento_parcial_do_pedido_invalido: proibido
alteracao_da_copia_em_rejeicao: nenhuma
codigo_saida_em_rejeicao: nao_zero
```

ID textual estruturalmente válido, porém ausente da fixture, não invalida
o pedido — resulta em `nao_encontrado` por item (6.5.4), não em rejeição
estrutural.

### 6.5.2 CLI do executor sintético

```text
python -m demo.executor_sintetico \
  --entrada <entrada.json> \
  --resultado <resultado.json> \
  [--dry-run]
```

Não autorizar nenhum argumento além destes três. Em particular, não
autorizar `--fixture`, flags de falha, flags de interrupção, comando shell
arbitrário, caminho do Pipeline, binding ou configuração em variável de
ambiente.

O executor deriva `fixture_trabalho.json` como arquivo irmão de
`resultado.json` — localização por convenção posicional, sem novo campo,
flag ou variável.

A opção `--fixture` pertence exclusivamente ao ponto de entrada
demonstrativo `demo.demo_execucao_focal` (seção 11) — nunca ao executor
sintético nem ao protocolo provisório de CLI.

### 6.5.3 Diretório temporário por invocação

A camada invocadora (`tela/execucao_focal.py`) cria, por invocação:

```text
<diretorio-exclusivo>/
├── entrada.json
├── resultado.json
└── fixture_trabalho.json
```

Regras:

```yaml
entrada.json: copia_da_entrada_permanente_selecionada
resultado.json: criado_previamente_pela_camada_invocadora
fixture_trabalho.json: copia_da_baseline_permanente
baseline_permanente: nunca_alterada
identidade_do_diretorio: unica_por_invocacao
nomes_internos: fixos
limpeza: finally_remove_integralmente_o_diretorio
residuos_em_sucesso_falha_ou_interrupcao: nenhum
inspecao_por_teste: mecanismo_interno_nao_integra_a_CLI_publica
```

### 6.5.4 Semântica sintética por item

Baseline sintética demonstrativa (imutável, permanente):

```yaml
item_01:
  processado: false
item_03:
  processado: true
item_05:
  processado: false
item_07:
  processado: false
```

Para cada ID normal, na ordem recebida:

```yaml
processado_false:
  dry_run:
    resultado: processado
    aplicado: false
    processado_antes: false
    processado_depois: true
    altera_fixture: false
  executar:
    resultado: processado
    aplicado: true
    processado_antes: false
    processado_depois: true
    altera_fixture_trabalho: true

processado_true:
  resultado: ignorado
  aplicado: false
  processado_antes: true
  processado_depois: true

id_inexistente:
  resultado: nao_encontrado
  aplicado: false
  processado_antes: null
  processado_depois: null
  diagnostico: texto_deterministico
```

Resultados individuais permitidos: `processado`, `ignorado`,
`nao_encontrado`, `falhou`.

### 6.5.5 Documento estruturado de resultado

```yaml
tipo: multinivel
formato:
  apresentacao: conjuntos_campos
  niveis:
    - secao: container
    - registro: container
    - campo: nome_valor
dados:
  - secao Resumo
  - secao Itens
```

O schema concreto deve seguir integralmente `contrato_json_console.md`
§12 (schema semântico multinível) e §14.9 (documento de sucesso).

Resumo mínimo:

```text
modo
status
solicitados
processados
ignorados
nao_encontrados
falhos
```

Valores de `modo`: `dry_run`, `executar`.

Status global:

```yaml
sucesso:
  - processados
  - ignorados
  - processados_e_ignorados
parcial:
  - existe_nao_encontrado
  - existe_falha_individual
falha:
  - protocolo_nao_concluido
```

Campos por registro normal: `id`, `resultado`, `aplicado`,
`processado_antes`, `processado_depois`. `diagnostico` existe somente em
`nao_encontrado` ou `falhou`.

O documento deve ser determinístico e compacto — os documentos produzidos
pelas entradas permanentes de sucesso e parcial devem caber integralmente
na referência lógica `80x24` (D-SEL-20; `contrato_json_console.md` §14.8),
sem paginação, truncamento ou omissão.

### 6.5.6 Código de saída e canais

```yaml
resultado_valido_sucesso_ou_parcial:
  codigo_saida: 0
falha_operacional:
  codigo_saida: nao_zero
interrupcao:
  codigo_saida: 130
```

Cenário normal: `stdout` e `stderr` vazios.

Dois cenários de sucesso são distinguidos por canal, sem afetar
`status_global` nem `codigo_saida`:

```yaml
sucesso_normal:
  exemplo: item_01 e item_03
  stdout: vazio
  stderr: vazio

sucesso_com_aviso:
  exemplo: somente item_03
  stdout: vazio
  stderr: "AVISO: nenhum item foi alterado; todos ja estavam processados.\n"
  codigo_saida: 0
  status_global: sucesso
```

O gatilho de `sucesso_com_aviso` é exclusivamente o estado normal dos itens:
o pedido é estruturalmente válido e todos os IDs normais solicitados já se
encontram `processado: true` na fixture de trabalho no momento da
invocação — nenhum ID novo, campo, argumento de CLI ou variável de
ambiente aciona esse aviso. Pedidos mistos, contendo ao menos um item
processável (`processado: false`) além de item já processado, permanecem
no cenário `sucesso_normal` (`stdout` e `stderr` vazios). O aviso pertence
exclusivamente ao executor sintético demonstrativo, não é novo status, não
é resultado individual novo, não é ID reservado e não institui
comportamento do futuro binding real.

Regras:

- `resultado.json` é a única fonte do documento estruturado;
- `stdout` nunca é interpretado como JSON;
- `stderr` com código `0` não altera a classificação;
- falha focal pode produzir `stderr` determinístico;
- a camada invocadora preserva separadamente código, `stdout`, `stderr`,
  existência do resultado e conteúdo bruto do arquivo.

A classificação de processo (`tela/execucao_focal.py`) exige
simultaneamente código `0` **e** `resultado.json` sintaticamente válido —
código `0` isolado (caso de `__resultado_invalido__`) não classifica o
processo como sucesso.

### 6.5.7 Controles sintéticos e interrupção

```yaml
__falha_operacional__:
  natureza: nao_e_item_de_dominio
  equivale_a_nao_encontrado: false
  stderr: deterministico
  codigo_saida: nao_zero
  alteracao_persistente: nenhuma
  resultado_json_valido_exigido: false

__resultado_invalido__:
  resultado_json: texto_deliberadamente_invalido
  codigo_saida: 0
  preservacao: byte_a_byte_pela_camada_invocadora
  correcao_normalizacao_ou_reserializacao: proibida
  envelope_visual_de_erro: fora_de_escopo_deste_handoff

__interrupcao__:
  sequencia:
    1: processar_eventual_id_normal_anterior
    2: tornar_observavel_a_alteracao_na_copia
    3: provocar_KeyboardInterrupt
    4: capturar_somente_para_finalizar_o_protocolo
    5: gravar_json_valido_com_status_interrompido
    6: encerrar_com_codigo_130
    7: garantir_limpeza_do_diretorio_temporario
  disponibilidade_do_json_antes_da_limpeza: obrigatoria_para_uso_futuro_pelo_Handoff_3
```

Estes três IDs não pertencem ao domínio real, não aparecem como itens
normais das fixtures, não instituem protocolo definitivo e não podem ser
confundidos com `nao_encontrado`.

## 7. Entradas, fixtures, temporários e saídas

```yaml
entradas_reais: inexistente

fixtures:
  baseline_permanente: demo/fixtures/h0042_fixture_execucao.json
  entradas_permanentes:
    - demo/fixtures/h0042_entrada_sucesso.json
    - demo/fixtures/h0042_entrada_sucesso_aviso.json
    - demo/fixtures/h0042_entrada_parcial.json
    - demo/fixtures/h0042_entrada_falha_operacional.json
    - demo/fixtures/h0042_entrada_resultado_invalido.json
    - demo/fixtures/h0042_entrada_interrupcao.json
  natureza: configuracao_controlada_permanente
  contaminacao_por_execucao: inexistente
```

Conteúdo exato de `demo/fixtures/h0042_entrada_sucesso_aviso.json` (gatilho do
cenário `sucesso_com_aviso`, §6.5.6 — pedido contendo somente o ID já
processado `item_03` na baseline):

```json
{
  "schema": "selecao_execucao.v1",
  "ids": ["item_03"]
}
```

```yaml
configuracoes: nenhuma alteracao em config/** por este handoff

temporarios_operacionais:
  localizacao: diretorio_exclusivo_por_invocacao_criado_em_tempo_de_execucao
  conteudo: entrada.json, resultado.json, fixture_trabalho.json
  ciclo_de_vida: criado_e_removido_dentro_da_mesma_invocacao
  residuo_permitido: nenhum

saidas_geradas:
  - docs/relatorios/IMP-0042-protocolo-focal-execucao-sintetica-reversivel.md

politica_de_sobrescrita: nao_sobrescrever_relatorio_anterior
politica_de_limpeza: >-
  todo temporario operacional e removido dentro da propria invocacao;
  nenhuma evidencia material pode permanecer somente em diretorio
  temporario do sistema operacional apos o termino do processo
```

Não misture entrada real com fixture. Não sobrescreva entrada real sem
decisão explícita. Nenhuma evidência material pode permanecer somente em
`/tmp`.

## 8. Tarefas

1. Implementar `tela/execucao_focal.py`: validação estrita de
   `selecao_execucao.v1`; preparação do diretório temporário e dos três
   arquivos internos; invocação do processo autorizado por subprocesso;
   captura separada de código/`stdout`/`stderr`; preservação do conteúdo
   bruto de `resultado.json`; classificação do processo (código `0` **e**
   JSON válido); limpeza protegida por `finally`.
2. Implementar `demo/executor_sintetico.py`: CLI `--entrada`/`--resultado`/
   `--dry-run`; leitura de `fixture_trabalho.json` como irmã de
   `resultado.json`; efeito sintético por item (6.5.4); gravação direta do
   documento multinível (6.5.5); reconhecimento dos três controles
   sintéticos (6.5.7).
3. Criar as fixtures permanentes nominais em `demo/fixtures/` (baseline
   mista de quatro itens e as seis entradas `selecao_execucao.v1`).
4. Implementar `demo/demo_execucao_focal.py`: ponto de entrada não
   interativo que prepara o temporário, copia entrada e baseline, invoca o
   executor via `tela/execucao_focal.py`, mostra resumo humano fora de
   `resultado.json`, comprova efeitos antes da limpeza e a remoção do
   temporário.
5. Escrever os testes unitários e de integração previstos na seção 10.
6. Executar as verificações locais previstas (seção 10).
7. Executar as quatro invocações de demonstração reproduzível previstas
   na seção 11.
8. Criar o relatório próprio desta execução usando o template canônico.

## 9. Critérios de aceite

| ID | Critério | Evidência independente esperada |
|---|---|---|
| CA-01 | Entrada válida produz documento multinível válido | Teste de integração em `demo/teste_executor_sintetico.py` com `h0042_entrada_sucesso.json` |
| CA-02 | Entrada inválida é rejeitada integralmente, sem normalização | Testes unitários em `tela/teste_execucao_focal.py`/`demo/teste_executor_sintetico.py` cobrindo todos os casos de 6.5.1 |
| CA-03 | Dry-run não altera a cópia | Teste de integração comparando `fixture_trabalho.json` antes/depois em `--dry-run` |
| CA-04 | Execução real altera somente a cópia | Teste de integração comparando `fixture_trabalho.json` (alterado) e baseline permanente (inalterada) |
| CA-05 | Item já processado é ignorado | Teste com `item_03` (`processado: true` na baseline) |
| CA-06 | ID inexistente produz resultado parcial com código `0` | Teste de integração com `h0042_entrada_parcial.json` |
| CA-07 | Ordem dos IDs recebidos é preservada nos registros | Teste de integração verificando ordem em `Itens` |
| CA-08 | `stdout` nunca é fonte do resultado | Teste de canal com `stdout` contendo texto semelhante a JSON, resultado lido exclusivamente de `resultado.json` |
| CA-09 | Pedido válido contendo somente IDs já processados produz resultado estruturado de sucesso, código `0` e aviso determinístico em `stderr`, sem alteração da classificação | Teste focal do executor; teste da demonstração; execução nominal reproduzível — todos com `h0042_entrada_sucesso_aviso.json` |
| CA-10 | Falha operacional produz código não zero | Teste de integração com `h0042_entrada_falha_operacional.json` |
| CA-11 | Resultado inválido é preservado literalmente (byte a byte) | Teste de integração com `h0042_entrada_resultado_invalido.json` comparando o texto bruto |
| CA-12 | Interrupção produz JSON válido e código `130` | Teste de integração com `h0042_entrada_interrupcao.json` |
| CA-13 | Limpeza ocorre em todos os términos (sucesso, parcial, entrada inválida, falha, resultado inválido, interrupção) | Testes de temporários em `tela/teste_execucao_focal.py` |
| CA-14 | Baseline permanente nunca é alterada | Comparação do conteúdo de `demo/fixtures/h0042_fixture_execucao.json` antes/depois de toda a suíte |
| CA-15 | Controles sintéticos não são itens do domínio nem equivalem a `nao_encontrado` | Teste verificando ausência dos IDs de controle na fixture e tratamento distinto |
| CA-16 | Chip `Executar` e interface permanecem inalterados | Inspeção de código (nenhuma alteração em `demo/demo.py`, `demo/demo_selecao.py`, `tela/renderizador.py`) + suíte de regressão do H-0041 |
| CA-17 | Nenhuma autoridade documental (ADR, contrato, nomenclatura, backlog) é alterada | `git status`/`git diff --name-only` restrito ao handoff e aos artefatos nominais de código, fixture e relatório |
| CA-18 | Suíte completa permanece aprovada, sem regressão | Execução de `PYTHONDONTWRITEBYTECODE=1 python -m pytest` |

O valor esperado não pode ser derivado da própria saída observada.

Formulação fechada de CA-09:

```yaml
CA-09:
  criterio: >
    pedido válido contendo somente IDs já processados produz resultado
    estruturado de sucesso, código 0 e aviso determinístico em stderr,
    sem alteração da classificação
  fixture: demo/fixtures/h0042_entrada_sucesso_aviso.json
  evidencia:
    - teste focal do executor
    - teste da demonstração
    - execução nominal reproduzível
```

## 10. Testes obrigatórios

Execute a partir da raiz:

```zsh
cd "$(git rev-parse --show-toplevel)" || return 1

PYTHONDONTWRITEBYTECODE=1 python -m pytest -q --tb=short \
  tela/teste_execucao_focal.py \
  demo/teste_executor_sintetico.py \
  demo/teste_demo_execucao_focal.py

PYTHONDONTWRITEBYTECODE=1 python -m pytest -q --tb=short \
  tela/teste_selecao.py \
  demo/teste_demo_selecao.py

PYTHONDONTWRITEBYTECODE=1 python -m pytest
```

Casos mínimos exigidos:

**Entrada e protocolo:**
schema válido; schema ausente; schema divergente; `ids` ausente; `ids` não
array; lista vazia; ID vazio; ID não string; duplicata; ausência de
normalização; pedido inválido sem alteração da cópia.

**Dry-run:**
`item_01` resulta em `processado`; `aplicado: false`; estado posterior
previsto `true`; fixture de trabalho permanece inalterada; baseline
permanente permanece idêntica.

**Execução real:**
`item_01` muda para `true` na cópia; `item_03` resulta em `ignorado`;
ordem dos registros preservada; documento válido; status `sucesso`;
código `0`; canais vazios; baseline permanente intacta.

**Parcial:**
`item_01` processado; `item_inexistente` como `nao_encontrado`; estados
`null`; diagnóstico presente; status `parcial`; código `0`; uma entrada
por ID; ordem preservada.

**Canais:**
cenário normal sem saída textual; `stdout` semelhante a JSON nunca usado
como resultado; resultado estruturado lido exclusivamente do arquivo.

**Sucesso com aviso (CA-09; `h0042_entrada_sucesso_aviso.json`):**
entrada contendo somente `item_03`; todos os IDs normais solicitados já
processados na fixture de trabalho; emissão exata do aviso em `stderr`
(`"AVISO: nenhum item foi alterado; todos ja estavam processados.\n"`);
código `0`; `status_global: sucesso`; resultado individual do registro
`item_03` igual a `ignorado`; ausência de mutação na cópia de trabalho e
na baseline permanente; `stderr` não interpretado como resultado JSON —
o documento estruturado provém exclusivamente de `resultado.json`; teste
focal do executor (`demo/teste_executor_sintetico.py`) e teste da
demonstração (`demo/teste_demo_execucao_focal.py`) como evidências
reproduzíveis próprias de CA-09.

**Sucesso normal misto (regressão do cenário normal):**
cenário misto `item_01` + `item_03` (`h0042_entrada_sucesso.json`)
continua com `stdout` e `stderr` vazios — a presença de item já
processado junto de item processável não aciona o aviso.

**Controles:**
falha operacional com código não zero; resultado inválido com código `0`;
preservação byte a byte do texto inválido; controle não tratado como
`nao_encontrado`; ausência dos controles na baseline.

**Interrupção:**
alteração observável antes da interrupção; JSON válido com
`status: interrompido`; código `130`; classificação externa de falha;
captura dos canais; limpeza integral; baseline intacta.

**Temporários:**
diretórios distintos em invocações distintas; nomes internos fixos;
resultado criado previamente; cópia criada a partir da baseline; limpeza
em sucesso, parcial, entrada inválida, falha, resultado inválido e
interrupção; nenhum resíduo fora do mecanismo controlado de inspeção.

**Regressão:**
testes existentes do H-0041 permanecem aprovados; chip `Executar`
permanece inativo; nenhum arquivo existente é alterado; suíte completa
aprovada.

Fora da automação deste handoff: quadro TTY completo com sequências ANSI;
filtro; paginação.

## 11. Demonstração operacional

```yaml
cwd: "."
comando_dry_run: >-
  PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_execucao_focal
  --entrada demo/fixtures/h0042_entrada_sucesso.json
  --fixture demo/fixtures/h0042_fixture_execucao.json
  --dry-run
comando_execucao_real: >-
  PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_execucao_focal
  --entrada demo/fixtures/h0042_entrada_sucesso.json
  --fixture demo/fixtures/h0042_fixture_execucao.json
entrada_ou_fixture:
  - demo/fixtures/h0042_entrada_sucesso.json
  - demo/fixtures/h0042_fixture_execucao.json
configuracao: nenhuma
saida_esperada: >-
  resumo humano fora de resultado.json; documento estruturado válido
  observável antes da limpeza; codigo_saida 0 no cenario demonstrativo
prova_semantica: >-
  o diretorio temporario e preparado; entrada e baseline sao copiadas; o
  executor sintetico e invocado; os efeitos sobre a copia sao observaveis
  antes da limpeza; a baseline permanente permanece intacta apos a
  execucao; o diretorio temporario e removido ao final
arquivos_persistentes:
  - demo/fixtures/h0042_fixture_execucao.json
  - demo/fixtures/h0042_entrada_sucesso.json
  - demo/fixtures/h0042_entrada_sucesso_aviso.json
  - demo/fixtures/h0042_entrada_parcial.json
  - demo/fixtures/h0042_entrada_falha_operacional.json
  - demo/fixtures/h0042_entrada_resultado_invalido.json
  - demo/fixtures/h0042_entrada_interrupcao.json
temporarios_operacionais: diretorio_exclusivo_por_invocacao_removido_ao_final
limpeza_ou_restauracao: automatica_por_finally_na_camada_invocadora
validacao_manual:
  executor_exclusivo: NAO_APLICAVEL_EVIDENCIA_AUTOMATIZADA
```

A opção `--fixture` pertence somente ao ponto de entrada demonstrativo
`demo.demo_execucao_focal` — não ao executor sintético nem ao protocolo
provisório de CLI (6.5.2).

A demonstração deve também permitir demonstrar nominalmente, sem adicionar
flags de falha ao executor:

```text
h0042_entrada_parcial.json
h0042_entrada_falha_operacional.json
h0042_entrada_resultado_invalido.json
h0042_entrada_interrupcao.json
```

Comando nominal do cenário `sucesso_com_aviso` (CA-09; §6.5.6):

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_execucao_focal \
  --entrada demo/fixtures/h0042_entrada_sucesso_aviso.json \
  --fixture demo/fixtures/h0042_fixture_execucao.json
```

Esta invocação deve comprovar: documento de resultado JSON válido; status
global `sucesso`; resultado individual do registro `item_03` igual a
`ignorado`; código de saída `0`; `stdout` vazio; `stderr` exatamente igual
a `"AVISO: nenhum item foi alterado; todos ja estavam processados.\n"`;
nenhuma mutação na cópia de trabalho; baseline permanente intacta; limpeza
integral do diretório temporário.

Código de saída zero, isoladamente, não comprova a entrega. Este Handoff 2
não exige TTY real nem validação visual humana — a evidência obrigatória é
automatizada e reproduzível: resultado JSON válido nos cenários
aplicáveis; conteúdo bruto preservado no cenário inválido; mutação
observável somente na cópia; baseline intacta; código e canais corretos;
temporários removidos.

## 12. Relatório da execução

Criar um novo relatório em:

```text
docs/relatorios/IMP-0042-protocolo-focal-execucao-sintetica-reversivel.md
```

Usar obrigatoriamente:

```text
docs/templates/TEMPLATE_RELATORIO_IMPL.md
```

Regras:

- cada execução material produz seu próprio relatório;
- não sobrescrever relatório anterior;
- registrar somente fatos materiais, alterações, verificações, evidências,
  achados e bloqueios;
- não copiar código, diff completo, handoff, logs extensos ou metodologia
  narrativa;
- omitir campos e seções vazios;
- teto normal de 900 palavras;
- evidência separada somente quando indispensável por formato, tamanho ou
  reutilização direta, sempre em `docs/relatorios/` e referenciada no
  relatório;
- o relatório não aprova formalmente a implementação.

## 13. Resposta terminal

Retorne somente:

```yaml
status: <STATUS_LITERAL>
relatorio: docs/relatorios/IMP-0042-protocolo-focal-execucao-sintetica-reversivel.md
artefatos:
  - <somente arquivos criados ou alterados>
bloqueios:
  - <somente quando houver>
proxima_acao: <somente quando objetivamente determinada>
```

Omitir campos vazios. Não copiar o relatório nem acrescentar conclusão
narrativa.

## 14. Exceção operacional

Arquivo ou diretório fora da lista nominal da seção 6.1 não pode ser
alterado silenciosamente.

Se um item externo for estritamente necessário para cumprir o handoff,
preservar testes obrigatórios ou evitar aborto desproporcional:

```yaml
status: AUTORIZACAO_ADICIONAL_NECESSARIA
caminho:
motivo:
escopo:
mudanca_esperada:
impacto_sem_autorizacao:
```

1. pare antes da alteração;
2. informe item, motivo, escopo exato e mudança esperada;
3. peça autorização explícita ao usuário.

A autorização não permite criar semântica, arquitetura, schema, formato ou
política nova. Em particular, a exceção operacional deste handoff nunca
pode autorizar: binding real; mudança do protocolo já fechado por
H2-ESP-01 a H2-ESP-18; alteração de contrato; ativação da interface
(`Enter`/`Executar`); alteração do H-0041; arquitetura genérica de
registry ou dispatcher.

## 15. Condições de bloqueio

Bloquear quando:

- faltar decisão;
- houver contradição documental;
- for necessário inventar formato ou schema além do já fechado pela
  ADR-0035 e por `contrato_json_console.md` §14;
- diretório novo necessário não estiver autorizado;
- houver risco de sobrescrever entrada real;
- o handoff for inexequível;
- a leitura focal autorizada for insuficiente;
- a separação entre CLI provisória do executor (`--entrada`,
  `--resultado`, `--dry-run`) e a opção `--fixture` do ponto de entrada
  demonstrativo não puder ser preservada sem alterar arquivo fora da lista
  nominal.

Se o bloqueio ocorrer antes de qualquer resultado material, não crie
relatório. Se já houver leitura, verificação, alteração ou evidência que
precise sobreviver ao contexto, crie relatório factual do bloqueio.

## 16. Limite de encerramento

Ao concluir implementação, testes locais, demonstração e relatório, pare.

Não faça QA formal.
Não aprove a própria entrega.
Não prepare nem execute commit.
Não inicie outro ciclo.

O Handoff 3 permanece responsável pela tela padrão de resultado e pelo
envelope visual de erro. O Handoff 4 permanece responsável pela
integração completa entre a interface, o chip `Executar` e o protocolo
aqui implementado.
