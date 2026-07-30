---
name: H-0044-integracao-fluxo-focal-dry-run-restauracao-origem
description: "Autoriza a implementacao do Handoff 4 do ITEM-0006 (especializado pela ADR-0037): integracao do fluxo focal — selecao, toggle [Ins] Dry-Run com cor_alerta, ativacao de Executar, consumo de H-0042/H-0043, origem suspensa por referencia viva e retornos diferenciados dry-run/real"
metadata:
  type: handoff_implementacao
  status: READY_FOR_IMPLEMENTATION
  id: H-0044
  data_criacao: 2026-07-29
rastreabilidade:
  contrato_alvo:
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_chip.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_estilo.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_json_console.md
  adr_principal:
    - docs/adr/ADR-0037-integracao-do-fluxo-focal-com-dry-run-e-restauracao-da-origem.md
  adrs_relacionadas:
    - docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md
    - docs/adr/ADR-0035-protocolo-focal-execucao-sintetica-reversivel.md
    - docs/adr/ADR-0036-carregamento-e-apresentacao-da-tela-padrao-de-resultado.md
  issues_relacionadas:
    - ITEM-0006
    - ITEM-0011
    - ITEM-0020
  handoffs_anteriores:
    - H-0041
    - H-0042
    - H-0043
---

# H-0044 — Integrar fluxo focal com dry-run e restauração da origem

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

```yaml
item:
  id: ITEM-0006
  estado: em_andamento
  handoffs_concluidos:
    - H-0041
    - H-0042
    - H-0043
  proxima_entrega: H-0044

ADR_principal:
  caminho: docs/adr/ADR-0037-integracao-do-fluxo-focal-com-dry-run-e-restauracao-da-origem.md
  status: aceita
  QA_ADR: ADR_APPROVED
  aplicacao_documental: concluida
  QA_APLICACAO_inicial: ADR_APPLICATION_REJECTED
  achado:
    - QA-APLICACAO-ADR0037-001
  patch:
    status: ADR_APPLICATION_PATCHED
    resultado:
      metadata_status: aceita
      secao_1_status: aceita
      decisoes_D_H4_preservadas: 10
  conferencia_direta_do_gerente:
    status: APROVADA
    achados_pendentes: []

baseline_funcional:
  branch: master
  HEAD: 8af243c336ca5eb3bdc7ae888009ab404c883ab6
  H_0041:
    capacidade: selecao_multipla
    commit: f4b5df1
  H_0042:
    capacidade: protocolo_focal_execucao_sintetica_reversivel
    commit: 6ecc4cd
  H_0043:
    capacidade: carregamento_e_apresentacao_resultado_execucao
    commit: 8af243c
```

Estado Git confirmado nesta autoria: branch `master`, HEAD
`8af243c336ca5eb3bdc7ae888009ab404c883ab6`, stage vazio; worktree acumulado
somente com artefatos documentais da ADR-0037 (sem implementação iniciada).

Interfaces públicas confirmadas por leitura direta:

```yaml
H_0042:
  simbolo: tela.execucao_focal.executar_protocolo_focal
  assinatura: >-
    (caminho_entrada, caminho_fixture, *, dry_run=False,
    antes_da_limpeza=None, cwd=None)
  retorno:
    - codigo_saida
    - stdout
    - stderr
    - resultado_bruto
    - classificacao
  limpeza_temporarios: finally_antes_do_retorno

H_0043:
  simbolos:
    - tela.resultado_execucao.DocumentoRuntime
    - tela.resultado_execucao.construir_modelo_resultado
    - tela.resultado_execucao.carregar_sessao_resultado
  entrada_runtime:
    codigo_saida: int
    stdout: str
    stderr: str
    resultado_bruto: str | None

estilo:
  config_estilo_json:
    cor_alerta: amarelo
    cor_inativo: cinza
  EstiloResolvido:
    cor_alerta: ainda_nao_materializado_pelo_loader
  renderer:
    _ANSI_POR_NOME_SEMANTICO.amarelo: presente
    consumo_de_cor_alerta_em_chip: pendente_deste_handoff

navegacao_e_modelo:
  alterar_por_padrao: false
  finalidade: preservar_instancia_viva_e_reconciliar_foco_cursor
```

Fronteiras de backlog confirmadas por leitura focal: `ITEM-0006` em
andamento com próxima ação nesta criação; `ITEM-0011` aguarda comprovação
runtime de `cor_alerta`; `ITEM-0020` permanece aberto para padronização
genérica futura.

## 4. Objetivo

Autorizar uma capacidade coesa e verificável:

```text
selecionar itens na tela de origem
→ escolher execução real ou dry-run por Insert
→ acionar Executar
→ consumir o executor focal do H-0042
→ construir o resultado pelo H-0043
→ suspender a origem
→ apresentar resultado_execucao
→ retornar por Esc
→ restaurar a origem conforme o modo executado
```

O H-0044 conclui a implementação funcional dos quatro handoffs do
`ITEM-0006`, sem executar ainda seu fechamento documental ou Git.

Nome físico da tela de origem (decisão nominal deferida pela ADR-0037,
fechada aqui):

```yaml
id_tela: h0044_fluxo_execucao_integrado
arquivo: config/telas/demo/h0044_fluxo_execucao_integrado.json
```

A tela histórica `config/telas/demo/h0041_selecao_multipla_oito_itens.json`
permanece intacta.

## 5. Manifesto fechado de leitura

```yaml
leitura_integral:
  - docs/templates/TEMPLATE_HANDOFF_IMPLEMENTACAO.md
  - docs/adr/ADR-0037-integracao-do-fluxo-focal-com-dry-run-e-restauracao-da-origem.md
  - docs/handoff/H-0041-selecao-multipla-estado-comandos-e-apresentacao.md
  - docs/handoff/H-0042-protocolo-focal-execucao-sintetica-reversivel.md
  - docs/handoff/H-0043-carregamento-apresentacao-tela-padrao-resultado.md
  - docs/contratos/contrato_barra_de_menus.md
  - docs/contratos/contrato_chip.md
  - docs/contratos/contrato_console.md
  - docs/contratos/contrato_estilo.md
  - docs/contratos/contrato_tela_json.md
  - docs/contratos/contrato_json_console.md
  - docs/nomenclatura/10_ESTILO.md
  - docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md
  - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
  - docs/nomenclatura/32_CONSOLE.md
  - config/estilo.json
  - config/telas/demo/h0041_selecao_multipla_oito_itens.json
  - config/telas/demo/resultado_execucao.json
  - demo/fixtures/h0042_fixture_execucao.json
  - tela/execucao_focal.py
  - tela/resultado_execucao.py
  - tela/selecao.py
  - tela/loader.py
  - tela/renderizador.py
  - demo/demo.py
  - docs/templates/TEMPLATE_RELATORIO_IMPL.md

leitura_focal:
  - arquivo: tela/modelo.py
    comando_busca: >-
      rg -n "ModeloTela|ElementoCorpo|construir_modelo" tela/modelo.py
    objetivo: >-
      confirmar como preservar a instancia viva e atualizar somente seu
      conteudo
  - arquivo: tela/navegacao.py
    comando_busca: >-
      rg -n "lista_foco|cursores|foco_console|grade_de_itens" tela/navegacao.py
    objetivo: preservar e reconciliar foco e cursor sem redefinir navegacao
  - arquivo: tela/teste_execucao_focal.py
    comando_busca: >-
      rg -n "executar_protocolo_focal|dry_run|codigo.?130|temporario|130"
      tela/teste_execucao_focal.py
    objetivo: identificar garantias ja provadas pelo H-0042
  - arquivo: tela/teste_resultado_execucao.py
    comando_busca: >-
      rg -n "construir|documento|envelope|resultado_execucao"
      tela/teste_resultado_execucao.py
    objetivo: identificar interface e garantias ja provadas pelo H-0043
  - arquivo: demo/teste_demo.py
    comando_busca: >-
      rg -n "PTY|Enter|Esc|SIGWINCH|pilha_telas" demo/teste_demo.py
    objetivo: >-
      integrar o novo fluxo sem criar mecanismo generico concorrente
  - arquivo: docs/backlog.md
    comando_busca: rg -n "ITEM-0006|ITEM-0011|ITEM-0020" docs/backlog.md
    objetivo: confirmar fronteiras e estado vigente

buscas_autorizadas:
  - termos: >-
      dry_run, cor_alerta, cor_inativo, estado_ativo_chips, origem_suspensa,
      pilha_telas, Executar, Todos, Insert, resultado_execucao,
      executar_protocolo_focal, codigo_saida, resultado_bruto, SIGWINCH
    escopo: somente_arquivos_enumerados_neste_manifesto

nao_ler:
  - docs/relatorios/**
  - docs/HISTORICO.md
  - docs/arquivo/**
  - qualquer outro handoff
  - qualquer outro modulo de nomenclatura
  - historico Git alem dos comandos de baseline
  - diretorios recursivamente
```

Para leitura focal, execute o comando indicado e leia somente sua saída. Não
abra o arquivo inteiro por conveniência. Se a saída for insuficiente, pare e
solicite expansão focal; não amplie autonomamente o contexto.

## 6. Escopo da implementação

### 6.1 Arquivos e diretórios autorizados

```yaml
arquivos_novos_a_criar:
  tela_integrada:
    - caminho: config/telas/demo/h0044_fluxo_execucao_integrado.json
      finalidade: >-
        nova tela de origem com oito itens, selecao multipla, chip Executar
        funcional e chip especifico [Ins] Dry-Run

  coordenador_focal:
    - caminho: tela/fluxo_execucao.py
      finalidade: >-
        manter o estado focal da transicao; preservar uma unica origem
        suspensa; coordenar H-0041, H-0042 e H-0043; distinguir retorno
        dry-run e real; limpar somente referencias proprias

  testes_focais:
    - caminho: tela/teste_fluxo_execucao.py
      finalidade: >-
        provar transicao, suspensao, retornos, reconciliacao, limpeza e
        ausencia de pilha generica

  relatorio_implementacao:
    - caminho: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0044.md
      template: docs/templates/TEMPLATE_RELATORIO_IMPL.md

arquivos_existentes_com_alteracao_autorizada_mas_nao_obrigatoria:
  - tela/loader.py
  - tela/teste_loader.py
  - tela/renderizador.py
  - tela/teste_renderizador.py
  - tela/resultado_execucao.py
  - tela/teste_resultado_execucao.py
  - demo/demo.py
  - demo/teste_demo.py
```

Autorização máxima não significa obrigação. Arquivos sem delta necessário
permanecem intactos. Diretórios novos não são necessários — todos os caminhos
cabem em diretórios já existentes.

### 6.2 Arquivos e diretórios preservados ou proibidos

```text
tela/execucao_focal.py
tela/teste_execucao_focal.py
tela/selecao.py
tela/navegacao.py
tela/modelo.py
demo/executor_sintetico.py
demo/demo_execucao_focal.py
demo/teste_executor_sintetico.py
demo/teste_demo_execucao_focal.py
config/telas/demo/h0041_selecao_multipla_oito_itens.json
config/telas/demo/resultado_execucao.json
demo/fixtures/h0042_fixture_execucao.json
demo/fixtures/h0042_*.json
demo/fixtures/h0043_*.json
config/estilo.json
```

`config/estilo.json` já contém `cor_alerta: amarelo`; a implementação somente
deve consumi-la — não alterá-la.

Preservação adicional:

- `docs/adr/**`, `docs/backlog.md`, `docs/adr/INDICE_ADR.md`,
  `docs/contratos/**`, `docs/nomenclatura/**`, `docs/handoff/**` (exceto o
  próprio arquivo deste handoff, já criado) — alteração normativa fora deste
  ciclo;
- qualquer arquivo além da lista nominal da seção 6.1 — exige a exceção
  operacional da seção 14 antes de qualquer alteração.

### 6.3 Escopo positivo

- Tela de origem `h0044_fluxo_execucao_integrado` com oito itens selecionáveis
  e cenários reproduzíveis via seleção visível.
- Chip `[Ins] Dry-Run` (tipo `alternancia`), sempre visível e operável,
  estado inicial desligado, eco exclusivo por `cor_alerta`.
- Materialização de `cor_alerta` em `EstiloResolvido` e consumo pelo
  renderer via conjunto/mapa de chips destacados em runtime.
- Ativação cumulativa de `Executar` (lote reconciliado não vazio + executor
  disponível + `resultado_execucao` pré-validada).
- Transição atômica origem → resultado sem quadro vazio, sem “Processando”,
  sem thread de fundo.
- Origem suspensa como referência viva única (não snapshot, não pilha
  genérica).
- Retorno dry-run sem recarga e com seleção/filtro/página/foco/cursor/toggle
  preservados.
- Retorno real com limpeza de seleção, uma recarga focal, filtro reaplicado,
  foco/cursor reconciliados e `dry_run_ativo=false`.
- Limpeza por propriedade entre H-0042, H-0043 e H-0044.
- Demonstração única por `python demo/demo.py h0044_fluxo_execucao_integrado`.

### 6.4 Escopo negativo

- alteração do protocolo `selecao_execucao.v1`;
- alteração do executor sintético;
- alteração das fixtures H-0042;
- alteração da tela H-0041;
- alteração da tela estrutural `resultado_execucao`;
- novo schema de documento ou envelope;
- nova apresentação de console;
- paginação;
- modo não verboso da tela de resultado;
- chip `[V]` no resultado;
- binding definitivo com Pipeline;
- registry ou dispatcher genérico;
- pilha genérica de telas;
- persistência do toggle fora da sessão;
- thread, processamento assíncrono ou tela de carregamento;
- novos controles de `dry-run` além de `Insert`;
- novo estilo, preset ou cor;
- alteração de ADR, contrato, nomenclatura, backlog ou índice;
- stage ou commit.

## 6.5 Protocolo técnico obrigatório

### 6.5.1 Forma da tela `h0044_fluxo_execucao_integrado`

A nova tela:

- reutiliza a composição, seleção múltipla, navegação e distribuição da tela
  H-0041 (console único, `politica_selecao: multipla`,
  `distribuicao_matricial` equivalente);
- possui exatamente oito itens selecionáveis (`navegavel: true`,
  `selecionavel: true`);
- não copia nem modifica
  `config/telas/demo/h0041_selecao_multipla_oito_itens.json`;
- usa IDs compatíveis com o executor focal do H-0042;
- permite reproduzir todos os cenários obrigatórios por seleção visível.

Lista fechada dos oito itens (confrontada com
`demo/fixtures/h0042_fixture_execucao.json`):

```yaml
itens:
  - id: item_01
    papel: normal_pendente
    na_fixture: true
    processado_baseline: false
  - id: item_05
    papel: normal_pendente
    na_fixture: true
    processado_baseline: false
  - id: item_03
    papel: normal_ja_processado
    na_fixture: true
    processado_baseline: true
  - id: item_07
    papel: normal_adicional
    na_fixture: true
    processado_baseline: false
  - id: item_inexistente
    papel: id_textual_ausente_da_fixture
    na_fixture: false
    rotulo: Item inexistente (ausente da fixture)
  - id: __falha_operacional__
    papel: controle_sintetico
    rotulo: Controle — falha operacional
  - id: __resultado_invalido__
    papel: controle_sintetico
    rotulo: Controle — resultado inválido
  - id: __interrupcao__
    papel: controle_sintetico
    rotulo: Controle — interrupção

composicao_exigida:
  itens_normais_pendentes: 2   # item_01, item_05 (item_07 e adicional)
  item_normal_ja_processado: 1 # item_03
  id_textual_ausente_da_fixture: 1  # item_inexistente
  controles_sinteticos: 3
  item_normal_adicional: 1     # item_07
  total: 8
```

Regras:

- IDs normais presentes existem literalmente na fixture H-0042;
- `item_inexistente` é identificador textual válido e inexistente na fixture
  (já usado pelo cenário parcial H-0042);
- controles sintéticos aparecem como itens demonstrativos claramente
  rotulados; não são termos canônicos nem ações produtivas;
- todos os oito itens preservam a mesma mecânica de cursor e seleção
  múltipla do H-0041;
- nenhum item oculto é injetado na seleção;
- o lote enviado ao H-0042 corresponde exatamente à seleção visível,
  reconciliada e ordenada.

### 6.5.2 Barra de menus da origem

Materializar a barra com a forma real vigente dos chips (sem schema novo),
além dos chips aplicáveis do H-0041:

```yaml
chips_obrigatorios:
  - id: chip_esc
    forma: equivalente_H0041  # Esc / Sair
  - id: chip_espaco
    forma: equivalente_H0041  # ␣ / Marcar
  - id: chip_enter
    forma: equivalente_H0041  # ⏎ / Todos|Executar dinamico
  - id: chip_dry_run
    tipo: alternancia
    tecla: Ins
    texto: Dry-Run
    regra_existencia: sempre
    regra_ativo: sempre
    forma_exibicao: visivel_ativo
```

Semântica do `[Ins] Dry-Run`:

```yaml
tipo: alternancia
estado_inicial: desligado
tecla_fisica: Insert
sempre_visivel: true
sempre_operavel: true

desligado:
  modo: execucao_real
  cor: cor_texto_normal

ligado:
  modo: dry_run
  cor: cor_alerta

eco_adicional:
  mensagem: false
  popup: false
  status: false
  alteracao_de_rotulo: false
```

O chip não usa `cor_inativo`. Posicionamento: faixa canônica de chips
específicos (após `[⏎]`). Proibido inventar chaves como `regra_destaque`,
`estado_visual`, `cor_por_chip` ou `preset_dry_run`. O estado ligado é
transportado em runtime e entregue ao renderer sem ser persistido no JSON.

### 6.5.3 Extensão focal do estilo

```yaml
EstiloResolvido:
  novo_campo_obrigatorio: cor_alerta

carregar_estilo:
  origem: config/estilo.json
  validacao: equivalente_e_proporcional_a_cor_inativo

renderer:
  entrada_runtime: conjunto_ou_mapa_de_chips_destacados
  hardcoding_do_id_dry_run: proibido
  hardcoding_de_ANSI: proibido
  cor_aplicada: estilo.cor_alerta
  estado_logico_ativo: permanece_true
```

Invariantes:

- o renderer não decide quando `dry-run` está ligado;
- o renderer recebe o estado já resolvido;
- somente o texto integral do chip `[Ins] Dry-Run` recebe amarelo;
- a cor não vaza para chips posteriores;
- cálculo de largura ignora ANSI;
- nenhum outro chip muda de cor;
- ausência de destaque preserva todos os quadros anteriores.

### 6.5.4 Estado focal de runtime (`tela/fluxo_execucao.py`)

Módulo específico do H-0044. Não criar gerenciador genérico de telas nem
dispatcher. Representação equivalente obrigatória:

```yaml
estado_fluxo_focal:
  origem_ativa: referencia_para_instancia_viva
  origem_suspensa: zero_ou_uma_referencia
  modelo_resultado: zero_ou_um
  dry_run_ativo: booleano
  transicao_em_andamento: booleano
```

Invariantes:

- `origem_ativa` e `origem_suspensa` nunca representam duas cópias
  concorrentes;
- a mesma instância viva é suspensa;
- nenhuma serialização ou snapshot é criado;
- nenhuma lista ou pilha genérica de telas é criada;
- estruturas genéricas preexistentes em `demo/demo.py` (`pilha_telas`) não
  devem ser ampliadas para representar o fluxo H-0044;
- a origem suspensa não recebe entrada nem mutação;
- `resultado_execucao` recebe exclusivamente `Esc`;
- teclas diferentes de `Esc` na tela de resultado não alteram a origem.

### 6.5.5 Pré-validação e ativação de `Executar`

Antes de permitir execução:

- confirmar disponibilidade da interface pública do H-0042
  (`executar_protocolo_focal`);
- carregar e validar antecipadamente a tela estrutural
  `resultado_execucao`;
- manter o modelo ou a estrutura pré-validada disponível à sessão;
- não reler a tela de resultado a cada render.

O chip `Executar` fica ativo somente quando:

```yaml
condicoes_cumulativas:
  - lote_reconciliado_nao_vazio
  - executor_focal_disponivel
  - tela_resultado_execucao_prevalidada
```

Se a reconciliação esvaziar o lote:

```yaml
executar: false
selecionar_todos_no_mesmo_enter: false
selecao_final: vazia
rotulo_final: Todos
```

O cursor corrente não limita o lote. `Enter` sem seleção continua executando
somente a semântica `Todos` do H-0041. `Enter` com seleção válida aciona o
fluxo focal.

### 6.5.6 Sequência atômica

Ordem obrigatória:

```text
reconciliar seleção
→ congelar o lote ordenado
→ capturar dry_run_ativo
→ preservar a referência da origem
→ materializar entrada temporária selecao_execucao.v1 do lote
→ executar tela.execucao_focal.executar_protocolo_focal
→ receber codigo_saida, stdout, stderr e resultado_bruto
→ construir DocumentoRuntime e o modelo por
  tela.resultado_execucao.construir_modelo_resultado
→ somente então suspender a origem
→ ativar resultado_execucao
```

A entrada temporária `selecao_execucao.v1` é artefato operacional do H-0044
para alimentar a API pública já existente do H-0042 (que recebe caminhos de
arquivo). Não altera o protocolo nem `tela/execucao_focal.py`.

Proibido:

- suspender a origem antes de existir resultado apresentável;
- abrir quadro vazio de resultado;
- apresentar “Processando”;
- executar em thread de fundo;
- permitir entrada concorrente;
- duplicar classificação do H-0042;
- duplicar escolha documento/envelope do H-0043;
- imprimir resultado pronto sem passar pelo loader, modelo e renderer.

Sucesso, parcial, falha semântica, falha operacional, resultado inválido e
interrupção `130` abrem a mesma tela.

### 6.5.7 Retorno após `dry-run`

No `Esc` da tela de resultado:

```text
descartar runtime do resultado
→ limpar referências próprias do H4
→ reativar a mesma origem
→ redesenhar
```

Preservar:

```yaml
dados_carregados: mesma_instancia
recarregar_origem: false
selecao: mesma
filtro: mesmo
pagina: mesma
foco: mesmo
cursor_por_console: mesmo
dry_run_ativo: true
```

O usuário precisa pressionar `Insert` para desligar o modo.

Redimensionamento ocorrido durante o resultado:

```yaml
estado_semantico: preservado
geometria: recalculada_para_terminal_atual
arquivos_relidos: nenhum
```

### 6.5.8 Retorno após execução real

A origem permanece imutável enquanto o resultado está ativo. Somente no
`Esc`:

```text
descartar resultado
→ limpar seleção
→ executar recarregador focal da origem
→ reaplicar filtro
→ reconciliar foco
→ reconciliar cursor por ID
→ definir dry_run_ativo=false
→ reativar origem
→ redesenhar
```

A referência da instância de runtime da origem permanece a mesma; o conteúdo
vinculado pode ser atualizado dentro dela.

```yaml
selecao: sempre_vazia

filtro:
  preservar_valor: true
  reaplicar_sobre_dados_recarregados: true

foco:
  console_anterior_valido: preservar
  caso_contrario: primeiro_console_focalizavel

cursor:
  item_anterior_por_ID_valido: preservar
  caso_contrario: primeiro_item_navegavel

dry_run_ativo: false
```

Aplicar a sucesso, parcial, falha operacional, resultado inválido e
interrupção `130`.

Recarregador focal da demonstração:

```yaml
natureza: focal_da_demonstracao_H0044
binding_generico: false
registry: false
altera_fixture_baseline_H0042: false
fonte: entradas_permanentes_autorizadas
injetavel_ou_observavel_em_testes: true
chamadas:
  dry_run: 0
  execucao_real_no_retorno: 1
```

A prova de recarga distingue: identidade da instância (mesma referência),
recarga de conteúdo (chamada ao recarregador) e reconstrução (dados
rederivados das entradas permanentes sem mutar a baseline).

### 6.5.9 Limpeza por propriedade

```yaml
H_0042:
  limpa:
    - copia_temporaria
    - resultado_temporario
    - subprocesso
  antes_de_entregar_resultado: true

H_0043:
  cria_temporarios: false
  mantem: modelo_em_memoria

H_0044:
  limpa:
    - referencia_origem_suspensa
    - referencia_modelo_resultado
    - estado_transicao
    - entrada_temporaria_selecao_execucao
```

`KeyboardInterrupt` do executor:

- é convertido pelo H-0042 em código `130`;
- abre o envelope normal de interrupção;
- não encerra o TTY;
- retorna por `Esc`.

Exceção inesperada do próprio H-0044:

- não vira envelope operacional;
- limpa referências próprias;
- restaura alternate screen e terminal por `finally`;
- propaga o erro;
- não deixa a origem parcialmente mutada.

`SIGKILL` e encerramentos não interceptáveis permanecem fora da garantia.

### 6.5.10 Integração em `demo/demo.py`

Ponto de entrada único:

```bash
python demo/demo.py h0044_fluxo_execucao_integrado
```

Não criar demonstrador auxiliar substituto. O dispatch de `Enter`/`Executar`,
`Insert` e `Esc` no fluxo integrado deve delegar a `tela/fluxo_execucao.py`
sem ampliar `pilha_telas` como mecanismo do H-0044.

Baseline permanente do executor:

```text
demo/fixtures/h0042_fixture_execucao.json
```

Permanece imutável antes e depois de qualquer cenário.

## 7. Entradas, fixtures, temporários e saídas

```yaml
entradas_reais: inexistente

fixtures:
  tela_origem: config/telas/demo/h0044_fluxo_execucao_integrado.json
  tela_resultado_estrutural: config/telas/demo/resultado_execucao.json
  baseline_executor: demo/fixtures/h0042_fixture_execucao.json
  natureza: configuracao_controlada_permanente
  contaminacao_por_execucao: inexistente

configuracoes:
  estilo: config/estilo.json  # somente consumo; sem alteracao

temporarios_operacionais:
  H_0042: diretorio_exclusivo_por_invocacao_limpo_por_finally
  H_0044: entrada_temporaria_selecao_execucao_v1_por_acionamento

saidas_geradas:
  - docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0044.md

politica_de_sobrescrita: nao_sobrescrever_relatorio_anterior
politica_de_limpeza: >-
  temporarios H-0042 e entrada temporaria H-0044 removidos na propria
  invocacao/transicao; nenhum residuo permanente alem dos artefatos nominais
```

Não misture entrada real com fixture. Não sobrescreva entrada real sem
decisão explícita. Nenhuma evidência material pode permanecer somente em
`/tmp`.

## 8. Tarefas

1. Criar `config/telas/demo/h0044_fluxo_execucao_integrado.json` com os oito
   itens da seção 6.5.1 e a barra da seção 6.5.2.
2. Materializar `cor_alerta` em `EstiloResolvido`/`carregar_estilo` e
   estender o renderer para destaque runtime sem hardcoding.
3. Implementar `tela/fluxo_execucao.py` com estado focal, ativação,
   transição atômica, retornos diferenciados e limpeza própria.
4. Integrar o fluxo em `demo/demo.py` (dispatch `Insert`/`Enter`/`Esc`) sem
   pilha genérica nova e sem demonstrador auxiliar.
5. Criar `tela/teste_fluxo_execucao.py` e estender testes autorizados
   conforme a seção 10.
6. Executar as verificações locais previstas.
7. Criar o relatório próprio desta execução usando o template canônico.

## 9. Critérios de aceite

| ID | Critério | Evidência independente esperada |
|---|---|---|
| CA-H0044-01 | Manifesto nominal respeitado | `git status --short` comparado à seção 6.1 |
| CA-H0044-02 | Tela H0044 criada sem alterar H0041 | Inspeção de caminhos + diff negativo em `h0041_*.json` |
| CA-H0044-03 | Oito itens e cenários reproduzíveis | Teste de carregamento + seleção dos IDs da seção 6.5.1 |
| CA-H0044-04 | `cor_alerta` materializada no runtime | `tela/teste_loader.py` + inspeção de `EstiloResolvido` |
| CA-H0044-05 | Toggle `Insert` sem eco adicional | Teste focal de estado + quadro sem mensagem/popup/status |
| CA-H0044-06 | `Executar` com ativação cumulativa | Testes de lote/executor/pré-validação |
| CA-H0044-07 | Transição atômica | Teste de ordem: origem ativa até modelo válido; suspensão depois |
| CA-H0044-08 | Origem suspensa única e mesma instância | Teste de identidade (`is`) da referência |
| CA-H0044-09 | Retorno dry-run sem recarga | Contador do recarregador = 0 + seleção preservada |
| CA-H0044-10 | Retorno real com recarga e seleção limpa | Contador = 1 + seleção vazia |
| CA-H0044-11 | Foco e cursor reconciliados | Testes de preservação por ID e fallbacks |
| CA-H0044-12 | Interrupção 130 apresentada sem encerrar TTY | Envelope + sessão TTY permanece após código 130 |
| CA-H0044-13 | Limpeza por propriedade | Ausência de temporários H-0042 e refs H-0044 limpas |
| CA-H0044-14 | Redimensionamento preserva estado semântico | SIGWINCH no resultado sem releitura; retorno com geometria atual |
| CA-H0044-15 | H0041/H0042/H0043 sem regressão | Suíte focal regressiva da seção 10 |
| CA-H0044-16 | Suíte completa aprovada | `PYTHONDONTWRITEBYTECODE=1 python -m pytest` |
| CA-H0044-17 | Validação manual pendente e integralmente roteirizada | Seção 11.1 com dez RVMs, comando integral repetido em cada roteiro, IDs concretos, sequências físicas completas, procedimento concreto de redimensionamento (dois terminais) e respostas aplicáveis completas; sem preenchimento nesta etapa |

O valor esperado não pode ser derivado da própria saída observada.

## 10. Testes obrigatórios

Execute a partir da raiz:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest \
  tela/teste_fluxo_execucao.py \
  tela/teste_loader.py \
  tela/teste_renderizador.py \
  tela/teste_resultado_execucao.py \
  demo/teste_demo.py

PYTHONDONTWRITEBYTECODE=1 python -m pytest \
  tela/teste_execucao_focal.py \
  tela/teste_resultado_execucao.py \
  tela/teste_fluxo_execucao.py

PYTHONDONTWRITEBYTECODE=1 python -m pytest
```

Casos mínimos exigidos:

### Estilo e renderer

- `cor_alerta` ausente é erro de estilo;
- `cor_alerta: amarelo` é materializada;
- chip ativo destacado fica amarelo;
- chip ativo não destacado mantém cor normal;
- chip inativo continua cinza;
- destaque não torna chip inativo;
- ANSI não altera largura;
- cor não vaza;
- regressões visuais anteriores permanecem idênticas.

### Toggle

- estado inicial desligado;
- primeiro `Insert` liga;
- segundo `Insert` desliga;
- seleção, foco e cursor não mudam;
- nenhum outro eco é gerado;
- tecla não age enquanto resultado está ativo.

### Ativação

- lote reconciliado válido ativa;
- lote vazio inativa;
- executor indisponível inativa;
- tela de resultado inválida inativa;
- reconciliação que esvazia não executa `Todos` no mesmo acionamento.

### Transição

- origem continua ativa durante execução e construção do resultado;
- suspensão ocorre somente após modelo válido;
- origem suspensa é a mesma instância;
- não existe pilha genérica nova;
- resultado usa a interface real de H-0043
  (`construir_modelo_resultado` / `DocumentoRuntime`).

### Retorno de `dry-run`

- mesma instância;
- zero chamadas ao recarregador;
- seleção preservada;
- filtro, página, foco e cursor preservados;
- toggle permanece ligado.

### Retorno real

- uma chamada ao recarregador;
- seleção limpa para todos os tipos de resultado;
- filtro reaplicado;
- cursor preservado por ID;
- fallback para primeiro item;
- foco preservado ou reconciliado;
- toggle desligado.

### Falhas e limpeza

- falha operacional;
- resultado inválido;
- interrupção `130`;
- exceção interna antes da suspensão;
- exceção interna depois da suspensão;
- referências H-0044 limpas;
- fixture baseline H-0042 inalterada;
- nenhum temporário H-0042 remanescente;
- terminal restaurado.

### Redimensionamento

- `SIGWINCH` no resultado não relê origem;
- retorno usa dimensões atuais;
- estado semântico permanece.

Fora da automação deste handoff: preenchimento dos roteiros manuais da
seção 11.1.

## 11. Demonstração operacional

```yaml
cwd: "."
comando: python demo/demo.py h0044_fluxo_execucao_integrado
entrada_ou_fixture:
  - config/telas/demo/h0044_fluxo_execucao_integrado.json
  - demo/fixtures/h0042_fixture_execucao.json
  - config/telas/demo/resultado_execucao.json
configuracao: config/estilo.json (somente consumo)
saida_esperada: sessao_tui_integrada_origem_e_resultado
prova_semantica: >-
  a mesma tela permite, por selecao visivel: sucesso; sucesso com itens
  normais; parcial (ID existente + ausente); item ja processado; falha
  operacional; resultado invalido; interrupcao; dry-run; execucao real
  posterior sobre a mesma selecao preservada apos dry-run
arquivos_persistentes:
  - config/telas/demo/h0044_fluxo_execucao_integrado.json
  - demo/fixtures/h0042_fixture_execucao.json
temporarios_operacionais: limpos_por_invocacao
limpeza_ou_restauracao: automatica_por_camada
validacao_manual:
  executor_exclusivo: USUARIO_EM_TTY_REAL
```

Código de saída zero, isoladamente, não comprova a entrega.

### 11.1 Roteiro de validação manual (usuário)

Ambiente:

```yaml
terminal: TTY_real
resolucao: 1920x1200
modo: tela_cheia
comando: python demo/demo.py h0044_fluxo_execucao_integrado
```

Instrução geral: em cada roteiro, apagar todas as alternativas não
observadas e manter somente o resultado real. Não executar nem preencher
durante a implementação.

Ordem física dos oito itens na tela de origem, do topo para a base — base
determinística para a navegação por `Seta para cima`/`Seta para baixo` a
partir do cursor inicial, que se posiciona em `item_01` na abertura da
demonstração (console único, coluna única, `ordem: por_linha`, equivalente
à distribuição de H-0041; todos os oito itens são `navegavel: true` e
`selecionavel: true` conforme seção 6.5.1):

```yaml
posicao_1: item_01
posicao_2: item_05
posicao_3: item_03
posicao_4: item_07
posicao_5: item_inexistente
posicao_6: __falha_operacional__
posicao_7: __resultado_invalido__
posicao_8: __interrupcao__
```

Para `item_01`, `item_03`, `item_05` e `item_07`, esta etapa do handoff não
fixa texto de exibição distinto do próprio ID (seção 6.5.1 registra apenas
`papel` e `processado_baseline` para esses quatro itens); por isso o rótulo
usado nos roteiros abaixo é o ID literal. Para `item_inexistente`,
`__falha_operacional__`, `__resultado_invalido__` e `__interrupcao__`, o
rótulo é o já registrado na seção 6.5.1.

Gabarito completo de alternativas (cada roteiro usa somente o subconjunto
aplicável ao seu objetivo):

```text
CONFORME
CHIP_DRY_RUN_NAO_APARECE
COR_DRY_RUN_INCORRETA
ECO_VISUAL_INDEVIDO
SELECAO_ALTERADA_PELO_TOGGLE
EXECUTAR_INATIVO_INDEVIDAMENTE
EXECUCAO_NAO_OCORRE
RESULTADO_INCORRETO
TELA_RESULTADO_VAZIA
ORIGEM_MUTADA_DURANTE_RESULTADO
RETORNO_NAO_OCORRE
SELECAO_NAO_PRESERVADA
SELECAO_NAO_LIMPA
FILTRO_NAO_PRESERVADO
PAGINA_NAO_PRESERVADA
FOCO_NAO_PRESERVADO
CURSOR_NAO_PRESERVADO
FALLBACK_INCORRETO
DRY_RUN_MODO_INCORRETO_NO_RETORNO
INTERRUPCAO_ENCERROU_TTY
CODIGO_DE_INTERRUPCAO_INCORRETO
REDIMENSIONAMENTO_INCORRETO
ORIGEM_RECARREGADA_NO_DRY_RUN
RESIDUO_TEMPORARIO
SEGUNDO_ESC_NAO_ENCERROU
ERRO_DE_EXECUCAO
```

```yaml
id: RVM-H0044-01
objetivo: >-
  comprovar que Insert liga e desliga o chip [Ins] Dry-Run (cor_alerta) sem
  eco adicional e sem alterar selecao, foco ou cursor
ambiente:
  terminal: TTY_real
  resolucao: 1920x1200
  modo: tela_cheia
comando: python demo/demo.py h0044_fluxo_execucao_integrado
estado_inicial:
  - tela de origem h0044_fluxo_execucao_integrado aberta
  - cursor em item_01
  - selecao vazia
  - dry_run desligado; chip [Ins] Dry-Run em cor normal
itens_utilizados: []
sequencia_fisica:
  - Insert
  - Insert
resultado_esperado:
  - apos o primeiro Insert, o texto integral do chip [Ins] Dry-Run fica em amarelo (cor_alerta); nenhum outro chip muda de cor; sem mensagem, popup ou status adicional
  - apos o segundo Insert, o chip [Ins] Dry-Run retorna a cor normal
estado_apos_retorno:
  - selecao permanece vazia
  - cursor permanece em item_01
  - dry_run desligado
observado:
respostas_possiveis:
  - CONFORME
  - CHIP_DRY_RUN_NAO_APARECE
  - COR_DRY_RUN_INCORRETA
  - ECO_VISUAL_INDEVIDO
  - SELECAO_ALTERADA_PELO_TOGGLE
  - ERRO_DE_EXECUCAO
instrucao_de_registro: >-
  Mantenha somente a alternativa observada e apague todas as demais.
```

```yaml
id: RVM-H0044-02
objetivo: >-
  comprovar que a execucao em dry-run preserva selecao, filtro, pagina, foco
  e cursor no retorno por Esc, mantendo o chip [Ins] Dry-Run amarelo
ambiente:
  terminal: TTY_real
  resolucao: 1920x1200
  modo: tela_cheia
comando: python demo/demo.py h0044_fluxo_execucao_integrado
estado_inicial:
  - tela de origem aberta
  - cursor em item_01
  - selecao vazia
  - dry_run desligado
itens_utilizados:
  - id: item_01
    rotulo: item_01
sequencia_fisica:
  - Insert
  - Espaço
  - Enter
  - Esc
resultado_esperado:
  - apos Insert, chip [Ins] Dry-Run fica amarelo; cursor permanece em item_01
  - apos Espaço, item_01 fica selecionado; cursor permanece em item_01
  - apos Enter, resultado_execucao e apresentado em modo dry-run com o resultado de item_01
  - apos Esc, a origem e reativada
estado_apos_retorno:
  - selecao = [item_01]
  - filtro, pagina, foco e cursor preservados (cursor em item_01)
  - dry_run permanece ligado; chip ainda amarelo
  - zero chamadas ao recarregador
observado:
respostas_possiveis:
  - CONFORME
  - EXECUTAR_INATIVO_INDEVIDAMENTE
  - EXECUCAO_NAO_OCORRE
  - RESULTADO_INCORRETO
  - TELA_RESULTADO_VAZIA
  - SELECAO_NAO_PRESERVADA
  - FILTRO_NAO_PRESERVADO
  - PAGINA_NAO_PRESERVADA
  - FOCO_NAO_PRESERVADO
  - CURSOR_NAO_PRESERVADO
  - DRY_RUN_MODO_INCORRETO_NO_RETORNO
  - RETORNO_NAO_OCORRE
  - ERRO_DE_EXECUCAO
instrucao_de_registro: >-
  Mantenha somente a alternativa observada e apague todas as demais.
```

```yaml
id: RVM-H0044-03
objetivo: >-
  comprovar, em uma unica execucao reproduzivel, que a mesma selecao usada em
  dry-run e reaproveitada pela execucao real subsequente sem refazer a
  selecao, e que a selecao so e limpa apos a execucao real
ambiente:
  terminal: TTY_real
  resolucao: 1920x1200
  modo: tela_cheia
comando: python demo/demo.py h0044_fluxo_execucao_integrado
estado_inicial:
  - tela de origem aberta
  - cursor em item_01
  - selecao vazia
  - dry_run desligado
itens_utilizados:
  - id: item_01
    rotulo: item_01
sequencia_fisica:
  - Espaço
  - Insert
  - Enter
  - Esc
  - Insert
  - Enter
  - Esc
resultado_esperado:
  - apos Espaço e Insert, item_01 selecionado e dry_run ligado
  - apos o primeiro Enter, resultado_execucao apresentado em modo dry-run
  - apos o primeiro Esc, origem reativada com selecao [item_01] preservada e dry_run ligado
  - apos o segundo Insert, dry_run desligado, sem repetir o Espaço (selecao nao refeita)
  - apos o segundo Enter, resultado_execucao apresentado em modo real usando a mesma selecao [item_01]
  - apos o segundo Esc, origem reativada
estado_apos_retorno:
  - selecao vazia
  - dry_run desligado
  - uma chamada ao recarregador
  - filtro reaplicado; foco e cursor reconciliados
observado:
respostas_possiveis:
  - CONFORME
  - DRY_RUN_MODO_INCORRETO_NO_RETORNO
  - SELECAO_NAO_LIMPA
  - SELECAO_NAO_PRESERVADA
  - EXECUCAO_NAO_OCORRE
  - RESULTADO_INCORRETO
  - ERRO_DE_EXECUCAO
instrucao_de_registro: >-
  Mantenha somente a alternativa observada e apague todas as demais.
```

```yaml
id: RVM-H0044-04
objetivo: >-
  comprovar retorno real com selecao limpa e cursor preservado pelo ID apos
  navegacao fisica explicita ate item_05
ambiente:
  terminal: TTY_real
  resolucao: 1920x1200
  modo: tela_cheia
comando: python demo/demo.py h0044_fluxo_execucao_integrado
estado_inicial:
  - tela de origem aberta
  - cursor em item_01
  - selecao vazia
  - dry_run desligado
itens_utilizados:
  - id: item_05
    rotulo: item_05
sequencia_fisica:
  - Seta para baixo × 1
  - Espaço
  - Enter
  - Esc
resultado_esperado:
  - apos Seta para baixo × 1, cursor movido de item_01 para item_05
  - apos Espaço, item_05 selecionado
  - apos Enter, resultado_execucao apresentado em modo real com o resultado de item_05
  - apos Esc, origem reativada
estado_apos_retorno:
  - selecao vazia
  - cursor permanece em item_05 (item ainda navegavel)
  - dry_run desligado
  - filtro preservado
observado:
respostas_possiveis:
  - CONFORME
  - SELECAO_NAO_LIMPA
  - CURSOR_NAO_PRESERVADO
  - FALLBACK_INCORRETO
  - FILTRO_NAO_PRESERVADO
  - DRY_RUN_MODO_INCORRETO_NO_RETORNO
  - ERRO_DE_EXECUCAO
instrucao_de_registro: >-
  Mantenha somente a alternativa observada e apague todas as demais.
```

```yaml
id: RVM-H0044-05
objetivo: >-
  comprovar resultado parcial combinando um ID normal pendente (item_01) e o
  ID textual ausente da fixture (item_inexistente)
ambiente:
  terminal: TTY_real
  resolucao: 1920x1200
  modo: tela_cheia
comando: python demo/demo.py h0044_fluxo_execucao_integrado
estado_inicial:
  - tela de origem aberta
  - cursor em item_01
  - selecao vazia
  - dry_run desligado
itens_utilizados:
  - id: item_01
    rotulo: item_01
  - id: item_inexistente
    rotulo: Item inexistente (ausente da fixture)
sequencia_fisica:
  - Espaço
  - Seta para baixo × 4
  - Espaço
  - Enter
  - Esc
resultado_esperado:
  - apos o primeiro Espaço, item_01 selecionado; cursor permanece em item_01
  - apos Seta para baixo × 4, cursor movido de item_01 para item_inexistente
  - apos o segundo Espaço, item_inexistente selecionado
  - apos Enter, resultado_execucao apresenta status parcial (item_01 processado; item_inexistente ausente da fixture)
  - apos Esc, origem reativada
estado_apos_retorno:
  - selecao vazia
  - dry_run desligado
  - filtro preservado
observado:
respostas_possiveis:
  - CONFORME
  - RESULTADO_INCORRETO
  - EXECUCAO_NAO_OCORRE
  - SELECAO_NAO_LIMPA
  - ERRO_DE_EXECUCAO
instrucao_de_registro: >-
  Mantenha somente a alternativa observada e apague todas as demais.
```

```yaml
id: RVM-H0044-06
objetivo: comprovar o envelope de falha operacional do controle sintetico __falha_operacional__
ambiente:
  terminal: TTY_real
  resolucao: 1920x1200
  modo: tela_cheia
comando: python demo/demo.py h0044_fluxo_execucao_integrado
estado_inicial:
  - tela de origem aberta
  - cursor em item_01
  - selecao vazia
  - dry_run desligado
itens_utilizados:
  - id: __falha_operacional__
    rotulo: Controle — falha operacional
sequencia_fisica:
  - Seta para baixo × 5
  - Espaço
  - Enter
  - Esc
resultado_esperado:
  - apos Seta para baixo × 5, cursor movido de item_01 para __falha_operacional__
  - apos Espaço, __falha_operacional__ selecionado
  - apos Enter, resultado_execucao apresenta envelope de falha operacional
  - apos Esc, origem reativada
estado_apos_retorno:
  - selecao vazia
  - dry_run desligado
observado:
respostas_possiveis:
  - CONFORME
  - RESULTADO_INCORRETO
  - TELA_RESULTADO_VAZIA
  - ORIGEM_MUTADA_DURANTE_RESULTADO
  - ERRO_DE_EXECUCAO
instrucao_de_registro: >-
  Mantenha somente a alternativa observada e apague todas as demais.
```

```yaml
id: RVM-H0044-07
objetivo: comprovar o envelope de resultado invalido do controle sintetico __resultado_invalido__
ambiente:
  terminal: TTY_real
  resolucao: 1920x1200
  modo: tela_cheia
comando: python demo/demo.py h0044_fluxo_execucao_integrado
estado_inicial:
  - tela de origem aberta
  - cursor em item_01
  - selecao vazia
  - dry_run desligado
itens_utilizados:
  - id: __resultado_invalido__
    rotulo: Controle — resultado inválido
sequencia_fisica:
  - Seta para baixo × 6
  - Espaço
  - Enter
  - Esc
resultado_esperado:
  - apos Seta para baixo × 6, cursor movido de item_01 para __resultado_invalido__
  - apos Espaço, __resultado_invalido__ selecionado
  - apos Enter, resultado_execucao apresenta envelope de resultado invalido
  - apos Esc, origem reativada
estado_apos_retorno:
  - selecao vazia
  - dry_run desligado
observado:
respostas_possiveis:
  - CONFORME
  - RESULTADO_INCORRETO
  - TELA_RESULTADO_VAZIA
  - ERRO_DE_EXECUCAO
instrucao_de_registro: >-
  Mantenha somente a alternativa observada e apague todas as demais.
```

```yaml
id: RVM-H0044-08
objetivo: >-
  comprovar a interrupcao estruturada (codigo 130) do controle sintetico
  __interrupcao__ sem encerrar o TTY
ambiente:
  terminal: TTY_real
  resolucao: 1920x1200
  modo: tela_cheia
comando: python demo/demo.py h0044_fluxo_execucao_integrado
estado_inicial:
  - tela de origem aberta
  - cursor em item_01
  - selecao vazia
  - dry_run desligado
itens_utilizados:
  - id: __interrupcao__
    rotulo: Controle — interrupção
sequencia_fisica:
  - Seta para baixo × 7
  - Espaço
  - Enter
  - Esc
resultado_esperado:
  - apos Seta para baixo × 7, cursor movido de item_01 para __interrupcao__
  - apos Espaço, __interrupcao__ selecionado
  - apos Enter, resultado_execucao apresenta envelope de interrupcao
  - apos Esc, origem reativada
estado_apos_retorno:
  - codigo_saida: 130
  - TTY_encerrado: false
  - retorno_por_Esc: verdadeiro
  - selecao vazia
  - dry_run desligado
observado:
respostas_possiveis:
  - CONFORME
  - RESULTADO_INCORRETO
  - RETORNO_NAO_OCORRE
  - INTERRUPCAO_ENCERROU_TTY
  - CODIGO_DE_INTERRUPCAO_INCORRETO
  - ERRO_DE_EXECUCAO
instrucao_de_registro: >-
  Mantenha somente a alternativa observada e apague todas as demais.
```

```yaml
id: RVM-H0044-09
objetivo: >-
  comprovar que o redimensionamento (SIGWINCH) durante resultado_execucao
  recalcula a geometria e retorna com as dimensoes restauradas, sem reler a
  origem e sem alterar o estado semantico
ambiente:
  terminal: TTY_real
  resolucao: 1920x1200
  modo: tela_cheia
comando: python demo/demo.py h0044_fluxo_execucao_integrado
estado_inicial:
  - tela de origem aberta
  - cursor em item_01
  - selecao vazia
  - dry_run desligado
itens_utilizados:
  - id: item_01
    rotulo: item_01
```

Procedimento com dois terminais (Linux, reproduzível):

#### Terminal A

Antes de iniciar a demonstração:

```bash
tty > /tmp/h0044_tty
stty size > /tmp/h0044_tty_size
python demo/demo.py h0044_fluxo_execucao_integrado
```

Sequência física, para selecionar item_01, abrir resultado_execucao e
manter a tela de resultado aberta:

```text
Espaço
Enter
```

#### Terminal B

Enquanto o resultado estiver aberto, executar exatamente:

```bash
stty -F "$(cat /tmp/h0044_tty)" rows 30 cols 100
sleep 1
read linhas colunas < /tmp/h0044_tty_size
stty -F "$(cat /tmp/h0044_tty)" rows "$linhas" cols "$colunas"
```

#### Terminal A (continuação)

```text
Esc
```

Limpeza auxiliar:

```bash
rm -f /tmp/h0044_tty /tmp/h0044_tty_size
```

```yaml
resultado_esperado:
  enquanto_resultado_esta_aberto:
    - resultado_execucao reage ao SIGWINCH e recalcula a geometria
    - origem suspensa nao e recarregada
    - origem suspensa nao recebe mutacao
  ao_pressionar_Esc:
    - resultado e descartado
    - retorno real executa uma recarga focal
    - selecao e limpa
    - filtro e reaplicado
    - foco e cursor sao reconciliados
    - origem e reativada com as dimensoes restauradas
estado_apos_retorno:
  - origem reativada com as dimensoes restauradas
  - execucao real realizou uma recarga focal somente no retorno
  - selecao vazia
  - dry_run desligado
  - estado semantico reconciliado conforme retorno real
  - residuos temporarios auxiliares removidos (/tmp/h0044_tty, /tmp/h0044_tty_size)
observado:
respostas_possiveis:
  - CONFORME
  - REDIMENSIONAMENTO_INCORRETO
  - ORIGEM_MUTADA_DURANTE_RESULTADO
  - SELECAO_NAO_LIMPA
  - RESIDUO_TEMPORARIO
  - ERRO_DE_EXECUCAO
instrucao_de_registro: >-
  Mantenha somente a alternativa observada e apague todas as demais.
```

```yaml
id: RVM-H0044-10
objetivo: >-
  comprovar que o primeiro Esc retorna exatamente a origem e que o segundo
  Esc, sem selecao e na tela raiz, encerra a sessao conforme a regra vigente
ambiente:
  terminal: TTY_real
  resolucao: 1920x1200
  modo: tela_cheia
comando: python demo/demo.py h0044_fluxo_execucao_integrado
estado_inicial:
  - tela de origem aberta
  - cursor em item_01
  - selecao vazia
  - dry_run desligado
itens_utilizados:
  - id: item_07
    rotulo: item_07
sequencia_fisica:
  - Seta para baixo × 3
  - Espaço
  - Enter
  - Esc
  - Esc
resultado_esperado:
  - apos Seta para baixo × 3, cursor movido de item_01 para item_07
  - apos Espaço, item_07 selecionado
  - apos Enter, resultado_execucao apresentado em modo real
  - apos o primeiro Esc, origem reativada com selecao vazia (retorno real)
  - apos o segundo Esc, sem selecao e na tela raiz, a sessao encerra conforme a regra vigente de Esc sem selecao na tela raiz
estado_apos_retorno:
  - sessao encerrada
  - TTY liberado
observado:
respostas_possiveis:
  - CONFORME
  - RETORNO_NAO_OCORRE
  - SEGUNDO_ESC_NAO_ENCERROU
  - SELECAO_NAO_LIMPA
  - ERRO_DE_EXECUCAO
instrucao_de_registro: >-
  Mantenha somente a alternativa observada e apague todas as demais.
```

## 12. Relatório da execução

Criar um novo relatório em:

```text
docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0044.md
```

Usar obrigatoriamente:

```text
docs/templates/TEMPLATE_RELATORIO_IMPL.md
```

Conteúdo compacto obrigatório:

```yaml
- status
- handoff
- ADR_principal
- arquivos_criados
- arquivos_alterados
- arquivos_preservados
- delta_por_camada
- tela_h0044
- itens_e_cenarios
- materializacao_cor_alerta
- toggle_Insert
- ativacao_Executar
- transicao_atomica
- retorno_dry_run
- retorno_execucao_real
- reconciliacao_foco_cursor
- limpeza_por_propriedade
- testes_focais
- testes_regressivos_H0041_H0042_H0043
- suite_completa
- demonstracao_integrada
- validacao_manual_pendente
- git_diff_check
- stage
- residuos
- bloqueios
```

Regras: cada execução material produz seu próprio relatório; não sobrescrever
relatório anterior; registrar somente fatos materiais; não copiar código,
diff completo, handoff, logs extensos ou metodologia narrativa; omitir campos
e seções vazios; teto normal de 600 palavras, até 900 quando houver conteúdo
material não resumível; o relatório não aprova formalmente a implementação.

## 13. Resposta terminal

Retorne somente:

```yaml
status: <STATUS_LITERAL>
relatorio: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0044.md
artefatos:
  - <somente arquivos criados ou alterados>
bloqueios:
  - <somente quando houver>
proxima_acao: <somente quando objetivamente determinada>
```

Omitir campos vazios. Não copiar o relatório nem acrescentar conclusão
narrativa.

## 14. Exceção operacional

Arquivo ou diretório fora da lista nominal (seção 6.1) não pode ser alterado
silenciosamente.

Se um item externo for estritamente necessário:

1. pare antes da alteração;
2. identifique a necessidade antes de qualquer mudança;
3. retorne:

```yaml
status: LEITURA_ADICIONAL_NECESSARIA
arquivo: <caminho>
motivo: <necessidade_material>
alteracao_realizada: false
```

ou, quando a leitura já for suficiente e a alteração externa for inevitável:

```yaml
status: HANDOFF_SCOPE_EXTENSION_REQUIRED
arquivo: <caminho>
motivo: <necessidade_material>
alteracao_realizada: false
```

Não ampliar o manifesto autonomamente. A autorização explícita do usuário não
permite criar semântica, arquitetura, schema, formato ou política nova.

## 15. Condições de bloqueio

Bloquear quando:

- faltar decisão;
- houver contradição documental;
- for necessário inventar formato ou schema;
- diretório novo necessário não estiver autorizado;
- houver risco de sobrescrever entrada real;
- o handoff for inexequível;
- a leitura focal autorizada for insuficiente.

Bloqueios reconhecidos deste ciclo:

```yaml
bloqueios:
  - conflito entre ADR-0037 e contratos aplicados
  - impossibilidade de compor os oito itens com a fixture H-0042
  - ausencia de interface publica utilizavel do H-0042
  - ausencia de interface publica utilizavel do H-0043
  - necessidade de alterar schema ou arquivo preservado
  - necessidade de decisao material nova
```

Se o bloqueio ocorrer antes de qualquer resultado material, não crie
relatório. Se já houver leitura, verificação, alteração ou evidência que
precise sobreviver ao contexto, crie relatório factual do bloqueio.

## 16. Limite de encerramento

Ao concluir implementação, testes locais, demonstração e relatório, pare.

Não faça QA formal.
Não aprove a própria entrega.
Não prepare nem execute commit.
Não inicie outro ciclo.

## 17. Verificação interna obrigatória (autoria deste handoff)

```yaml
capacidade_coesa: true
arquivo_tela_e_modulo_focal_com_nomes_definidos: true
lista_de_implementacao_nominal_e_suficiente: true
arquivos_preservados_nao_necessarios_para_tarefas_autorizadas: true
oito_itens_permitem_todos_os_cenarios: true
dry_run_seguido_de_execucao_real_com_mesma_selecao: true
retorno_real_prova_recarga_com_fixture_baseline_imutavel: true
testes_distinguem_identidade_recarga_e_reconstrucao: true
validacao_manual_com_teclas_e_gabarito_completos: true
relatorio_com_caminho_e_template_existentes: true
decisao_material_em_aberto: false
etapa_administrativa_separada_criada: false
```

Esta verificação pertence ao próprio handoff; nenhuma etapa ou relatório
separado de exequibilidade foi criado.
