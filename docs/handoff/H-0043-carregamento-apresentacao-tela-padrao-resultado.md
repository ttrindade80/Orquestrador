---
name: H-0043-carregamento-apresentacao-tela-padrao-resultado
description: "Autoriza a implementacao do Handoff 3 do ITEM-0006 (especializado pela ADR-0036): tela estatica resultado_execucao, ciclo de carregamento unico do JSON estrutural e do documento de runtime, escolha deterministica entre documento de resultado e envelope de erro, construcao do modelo composto em memoria, apresentacao no console unico e seis cenarios em 80x24"
metadata:
  type: handoff_implementacao
  status: READY_FOR_IMPLEMENTATION
  id: H-0043
  data_criacao: 2026-07-29
rastreabilidade:
  contrato_alvo:
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_json_console.md
  adr_relacionadas:
    - docs/adr/ADR-0036-carregamento-e-apresentacao-da-tela-padrao-de-resultado.md
    - docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md
    - docs/adr/ADR-0035-protocolo-focal-execucao-sintetica-reversivel.md
  issues_relacionadas:
    - ITEM-0006
  handoffs_anteriores:
    - H-0041
    - H-0042
---

# H-0043 — Carregamento e apresentação da tela padrão de resultado

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
ADR-0036:
  criacao: concluida
  QA_ADR_final: ADR_APPROVED
  aplicacao_documental: concluida
  QA_APLICACAO_ADR_final: ADR_APPLICATION_APPROVED

patch_aplicacao_ADR-0036:
  id: P01
  achado_tratado:
    - QA-APLICACAO-ADR0036-001
  novos_achados: []
  regressao_material: nenhuma

H-0042:
  status: I1_IMPLEMENTATION_APPROVED
  testes_focais: 80
  testes_regressivos: 35
  suite_completa: 639
  demonstracoes: 7 conformes
  validacao_manual: nao_aplicavel

ITEM-0006:
  estado: em_andamento
  handoffs_concluidos:
    - Handoff_1 (H-0041)
    - Handoff_2 (H-0042)
  proxima_entrega: H-0043
  permanece_pendente:
    - implementacao_do_Handoff_3 (este handoff)
    - Handoff_4

stage_transportado: vazio
bloqueios_transportados: nenhum
```

Este estado é suficiente para iniciar a implementação. Não reler relatórios de
QA ou de aplicação da ADR-0036 apenas para reconfirmar os status acima.

### Fronteira arquitetural obrigatória (ADR-0036 D-H3-19)

A ADR-0036 substitui pontualmente, quanto à tela `resultado_execucao`, a
divisão de responsabilidades entre Handoff 3 e Handoff 4 originalmente
fixada pela ADR-0034 (D-SEL-21).

| Camada | H-0043 (este handoff) | Handoff 4 (fora deste handoff) |
|---|---|---|
| Tela estática | Carrega, valida perfil/schema | — |
| Documento de runtime | Recebe separadamente, valida | — |
| Escolha documento/envelope | Decide e materializa | — |
| Modelo composto | Constrói em memória, preserva em redesenho/SIGWINCH | — |
| Apresentação | Renderiza no console único e passivo | — |
| Chip `Executar` | Não ativa | Ativa |
| Abertura da tela de resultado | Não abre | Abre |
| Suspensão da tela de origem | Não suspende | Suspende |
| Retorno e restauração | Não implementa | Implementa |

É proibido a este handoff antecipar qualquer responsabilidade listada na
coluna do Handoff 4.

## 4. Objetivo

Implementar, para o `ITEM-0006`, a capacidade de:

1. carregar a tela estática e reutilizável `resultado_execucao`;
2. receber separadamente um documento de runtime produzido ou capturado pelo
   fluxo focal do H-0042 (`tela/execucao_focal.py`, preservado e inalterado);
3. validar tela, perfil e documento antes da construção do modelo;
4. escolher deterministicamente entre apresentar o documento de resultado
   válido ou materializar um envelope de erro;
5. construir um modelo composto em memória;
6. apresentar o conteúdo no console único da tela;
7. preservar o modelo durante redesenhos e `SIGWINCH` (sem releitura de
   arquivos);
8. demonstrar seis cenários completos em terminal `80x24`, acessíveis por
   `demo/demo.py`.

Este handoff **não** ativa o chip `Executar`, não abre a tela a partir de uma
tela de origem, não suspende a origem e não implementa retorno/restauração —
essas capacidades pertencem exclusivamente ao Handoff 4.

## 5. Manifesto fechado de leitura

```yaml
leitura_integral:
  - docs/adr/ADR-0036-carregamento-e-apresentacao-da-tela-padrao-de-resultado.md
  - docs/contratos/contrato_tela_json.md (secao 34)
  - docs/contratos/contrato_composicao_corpo.md (secao 3.1.1)
  - docs/contratos/contrato_barra_de_menus.md (secao 23.4-23.5)
  - docs/contratos/contrato_console.md (secao 23.6-23.8)
  - docs/contratos/contrato_json_console.md (secao 14)
  - tela/loader.py
  - tela/execucao_focal.py
  - demo/demo.py
  - demo/executor_sintetico.py
  - demo/demo_execucao_focal.py

leitura_focal:
  - arquivo: docs/adr/ADR-0035-protocolo-focal-execucao-sintetica-reversivel.md
    comando_busca: grep -n "^### H2-ESP" docs/adr/ADR-0035-protocolo-focal-execucao-sintetica-reversivel.md
    objetivo: >-
      localizar H2-ESP-06 a H2-ESP-18 (schema do documento de sucesso,
      classificacao, canais, controles sinteticos e interrupcao) ja lidos
      integralmente na criacao deste handoff
  - arquivo: docs/handoff/H-0042-protocolo-focal-execucao-sintetica-reversivel.md
    comando_busca: grep -n "^### 6.5" docs/handoff/H-0042-protocolo-focal-execucao-sintetica-reversivel.md
    objetivo: >-
      confirmar o protocolo tecnico ja entregue (entrada/validacao, CLI,
      diretorio temporario, semantica por item, documento estruturado,
      codigo de saida/canais, controles sinteticos) sem redefini-lo
  - arquivo: docs/backlog.md
    comando_busca: grep -n "ITEM-0006" -A 10 docs/backlog.md
    objetivo: confirmar estado do item e proxima acao
  - arquivo: docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md
    comando_busca: grep -n "tela de resultado\|origem suspensa" docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md
    objetivo: terminologia vigente de tela de resultado e origem suspensa
  - arquivo: docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md
    comando_busca: grep -n "documento de resultado de execucao\|envelope de erro multinivel" docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md
    objetivo: terminologia canonica do documento de resultado e do envelope
  - arquivo: docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md
    comando_busca: grep -n "4.5" docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md
    objetivo: carregamento do documento de resultado de execucao
  - arquivo: docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
    comando_busca: grep -n "somente_verboso\|politica de modo" docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
    objetivo: politica de modo somente_verboso e ausencia do chip [V]
  - arquivo: docs/templates/TEMPLATE_RELATORIO_IMPL.md
    comando_busca: cat docs/templates/TEMPLATE_RELATORIO_IMPL.md
    objetivo: template canonico do relatorio de implementacao exigido na secao 12

buscas_autorizadas:
  - termo: "resultado_execucao"
    escopo: tela/, demo/, config/telas/demo/
  - termo: "console_resultado"
    escopo: tela/, demo/
  - termo: "selecao_execucao.v1"
    escopo: tela/execucao_focal.py, demo/executor_sintetico.py
  - termo: "codigo_saida|resultado_json|stdout|stderr|130"
    escopo: tela/execucao_focal.py, docs/contratos/contrato_json_console.md
  - termo: "conjuntos_campos"
    escopo: tela/loader.py, tela/renderizador.py, docs/contratos/contrato_json_console.md
  - termo: "SIGWINCH"
    escopo: demo/demo.py
  - termo: "politica_modo"
    escopo: tela/loader.py, tela/renderizador.py, demo/demo.py
  - termo: "def carregar|def validar|def renderizar"
    escopo: tela/loader.py, tela/renderizador.py

nao_ler:
  - docs/relatorios/** (exceto o proprio relatorio a ser criado por este handoff)
  - demo/fixtures/h0042_*.json (usar apenas como dependencia referenciada, sem
    releitura extensa alem do necessario para reproduzir o schema)
  - qualquer arquivo fora deste manifesto
```

Para leitura focal, execute o comando indicado e leia somente sua saída. Não
abra o arquivo inteiro por conveniência. Se a saída for insuficiente, pare e
solicite expansão focal; não amplie autonomamente o contexto.

## 6. Escopo da implementação

### 6.1 Arquivos e diretórios autorizados

```yaml
arquivos_novos_a_criar:
  modulo_focal_da_tela_de_resultado:
    - caminho: tela/resultado_execucao.py
      finalidade: >-
        validar compatibilidade do perfil resultado_execucao; receber o
        documento de runtime; classificar documento vs. envelope de erro
        (D-H3-10); materializar o envelope determinístico quando aplicável;
        preservar texto bruto de resultado_json; construir ou coordenar a
        construcao do modelo composto em memoria; expor ao renderer um
        modelo ja validado e classificado
    - caminho: tela/teste_resultado_execucao.py
      finalidade: >-
        testes unitarios e de integracao do modulo: validacao de perfil,
        escolha documento/envelope, schema do envelope, preservacao literal,
        carregamento unico e nao-releitura em redesenho/SIGWINCH

  tela_estatica:
    - caminho: config/telas/demo/resultado_execucao.json
      finalidade: tela estatica e reutilizavel do perfil resultado_execucao

  fixtures_documento_de_runtime:
    - caminho: demo/fixtures/h0043_resultado_sucesso.json
    - caminho: demo/fixtures/h0043_resultado_parcial.json
    - caminho: demo/fixtures/h0043_resultado_falha_semantica.json
    - caminho: demo/fixtures/h0043_envelope_falha_operacional.json
    - caminho: demo/fixtures/h0043_envelope_resultado_invalido.json
    - caminho: demo/fixtures/h0043_envelope_interrupcao.json

  fixtures_quadro_esperado_80x24:
    - caminho: demo/fixtures/h0043_quadro_sucesso_80x24.txt
    - caminho: demo/fixtures/h0043_quadro_parcial_80x24.txt
    - caminho: demo/fixtures/h0043_quadro_falha_semantica_80x24.txt
    - caminho: demo/fixtures/h0043_quadro_falha_operacional_80x24.txt
    - caminho: demo/fixtures/h0043_quadro_resultado_invalido_80x24.txt
    - caminho: demo/fixtures/h0043_quadro_interrupcao_80x24.txt

  relatorio_de_implementacao:
    caminho: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0043.md
    template: docs/templates/TEMPLATE_RELATORIO_IMPL.md
```

Diretórios ainda inexistentes podem ser criados somente quando aparecerem
nominalmente nesta lista. `demo/fixtures/` já existe (criado pelo H-0042);
nenhum diretório novo é necessário.

```yaml
arquivos_existentes_com_alteracao_autorizada_mas_nao_obrigatoria:
  - tela/loader.py
  - tela/teste_loader.py
  - tela/renderizador.py
  - tela/teste_renderizador.py
  - demo/demo.py
  - demo/teste_demo.py
```

A autorização é máxima, não obrigatória. Arquivo sem delta necessário deve
permanecer intacto. `tela/modelo.py` e `tela/navegacao.py` **não** integram
esta lista — não podem ser alterados; se a implementação concluir que uma
alteração em `tela/modelo.py` é estritamente necessária, aplicar a exceção
operacional da seção 14 antes de qualquer alteração.

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
demo/fixtures/h0042_*.json
config/estilo.json
```

Preservação adicional:

- `docs/adr/**`, `docs/backlog.md`, `docs/adr/INDICE_ADR.md`,
  `docs/contratos/**`, `docs/nomenclatura/**`, `docs/handoff/**` (exceto o
  próprio arquivo deste handoff, já criado) — alteração normativa fora deste
  ciclo.
- Qualquer arquivo permanente de resultado fora de fixture nominal — proibido.
- Qualquer arquivo além da lista nominal da seção 6.1 — exige a exceção
  operacional da seção 14 antes de qualquer alteração.

### 6.3 Escopo positivo

- Carregamento único do `tela.json` estrutural e do documento de runtime por
  cenário, cada um validado antes da construção do modelo.
- Validação do campo raiz `perfil: resultado_execucao` e da estrutura
  obrigatória do perfil (console único passivo, sem seleção, sem paginação,
  `politica_modo: somente_verboso`, chip único `Esc`/`Voltar`).
- Escolha determinística entre apresentar o documento de resultado original
  (código `0` e documento válido, qualquer `status` semântico interno) e
  materializar o envelope de erro multinível (código não zero, resultado
  ausente, malformado ou semanticamente inválido).
- Envelope de erro com exatamente seis campos em ordem fixa (`status`,
  `diagnostico`, `codigo_saida`, `stdout`, `stderr`, `resultado_json`),
  `status: falha` único, diagnósticos canônicos determinísticos.
- Preservação literal (byte a byte) do texto de `resultado_json`, válido ou
  inválido, sem correção, normalização, reserialização ou inferência.
- Interrupção (`codigo_saida: 130`) sempre produzindo envelope com
  diagnóstico `A execução foi interrompida.`, preservando eventual resultado
  prévio gravado antes da interrupção.
- Construção de um modelo composto em memória, reutilizado integralmente em
  redesenho e `SIGWINCH`, sem releitura de `tela.json` nem do documento de
  runtime.
- Seis cenários de demonstração acessíveis por `demo/demo.py`, cada um com
  fixture, quadro `80x24` esperado e comparação automatizada integral.

### 6.4 Escopo negativo

- Ativação do chip `Executar`.
- Abertura da tela de resultado a partir de uma tela de origem (via `Enter`
  ou qualquer outro acionamento).
- Suspensão de tela de origem, pilha genérica de telas, retorno e
  restauração — exclusivos do Handoff 4.
- Redefinição de `selecao_execucao.v1` ou do protocolo do H-0042.
- Alteração de `tela/execucao_focal.py`, de `demo/executor_sintetico.py`, de
  `demo/demo_execucao_focal.py` ou das fixtures `h0042_*`.
- Integração com o Pipeline real; binding definitivo Orquestrador/Pipeline.
- Registry ou dispatcher genérico de ações.
- Escolha de `dry-run` pela interface.
- Paginação, truncamento ou omissão de conteúdo.
- Modo não verboso ou alternável na tela de resultado; chip `[V]`.
- Colapso multinível; `cor_alerta`; alteração de `config/estilo.json`.
- Criação de tela dinamicamente em runtime.
- Persistência do modelo composto além da sessão/cenário atual.
- Alteração de contratos, ADRs, nomenclatura ou backlog.
- Stage ou commit.

## 6.5 Protocolo técnico obrigatório

### 6.5.1 Estrutura normativa de `config/telas/demo/resultado_execucao.json`

```yaml
schema: tela.v1
id: resultado_execucao
perfil: resultado_execucao

cabecalho:
  titulo: Resultado da execução
  descricao: Resultado estruturado da operação realizada.

corpo:
  arranjo: vertical
  elementos:
    - id: console_resultado
      tipo: console
      titulo: Resultado
      formato:
        excesso:
          politica_modo: somente_verboso

barra_de_menus:
  distribuicao: horizontal
  chips:
    - id: esc
      tecla: Esc
      texto: Voltar
      acao: voltar
```

Regras vinculantes:

- ausência de `corpo.distribuicao` (cardinalidade unitária — DA-01,
  `contrato_composicao_corpo.md` §5.7); não declarar `distribuicao` neste
  corpo;
- nenhum segundo `console`, `dashboard`, `lancador` ou `grupo`;
- `console_resultado` é o único elemento de `corpo.elementos[]`;
- `console_resultado` é um consumidor D23 puro (ADR-0028 D23;
  `tela/loader.py::_console_em_escopo_d23`): declara somente `id`, `tipo`,
  `titulo` e `formato.excesso.politica_modo`; nenhum campo do envelope
  clássico pré-ADR-0028 (`origem_dados`, `itens`, `politica_composicao`,
  `politica_navegacao`, `politica_selecao`, `politica_paginacao`,
  `politica_exibicao`) é declarado neste elemento — envelope clássico e
  marcador D23 permanecem mutuamente exclusivos no mesmo elemento, conforme
  a regra vigente de `_console_em_escopo_d23`, que este handoff não relaxa;
- `politica_modo: somente_verboso` é obrigatória (ADR-0028 D23) porque o
  console é consumidor de conteúdo multinível externo; `modo_inicial` não é
  declarado (proibido em política fixa — `contrato_json_console.md` §13.13.3);
  nenhuma regra de truncamento (`overflow_normal` ou equivalente) é
  declarada — truncamento é proibido (ADR-0036 §8; seção 6.4 deste handoff);
- as decisões semânticas de D-H3-01 a D-H3-08 (console passivo, sem
  navegação, sem seleção, sem paginação, sem modo alternável, conteúdo
  externo separado, console único) decorrem do perfil `resultado_execucao`,
  dos contratos e do modelo composto validado em `tela/resultado_execucao.py`
  — não do envelope clássico pré-ADR-0028, que não integra a forma JSON
  estática deste elemento;
- `barra_de_menus.chips` contém exclusivamente o chip `Esc`/`Voltar`; nenhum
  outro chip (`[⏎]`, `[✥]`, `[⇆]`, `[␣]`, `[V]`, `[?]`, específico) pode ser
  declarado;
- a tela é estática e preconstruída — o loader não a gera dinamicamente.

### 6.5.2 Validação do perfil pelo loader

O loader deve, ao carregar uma tela com `perfil: resultado_execucao`
(`contrato_tela_json.md` §34.2, §34.4):

- validar a presença e o valor do campo raiz `perfil`;
- reconhecer o perfil `resultado_execucao`;
- validar que `corpo.elementos[]` contém exatamente um elemento, do tipo
  `console`, sem `distribuicao` declarada e sem outro elemento funcional;
- validar que o console declarado é consumidor D23 puro
  (`_console_em_escopo_d23`): declara somente `id`, `tipo`, `titulo` e
  `formato.excesso.politica_modo`; nenhum campo do envelope clássico
  pré-ADR-0028 (`origem_dados`, `itens`, `politica_composicao`,
  `politica_navegacao`, `politica_selecao`, `politica_paginacao`,
  `politica_exibicao`) pode estar presente no mesmo elemento;
- exigir `politica_modo: somente_verboso`; rejeitar `modo_inicial`
  declarado em qualquer forma;
- validar que `barra_de_menus.chips` contém exatamente um chip (`Esc`/
  `Voltar`) e nenhum outro;
- rejeitar, com erro de domínio determinístico (reutilizando as classes de
  exceção já existentes em `tela/loader.py`, sem inventar hierarquia nova):
  ausência de `perfil`; valor de `perfil` desconhecido; dois ou mais
  consoles; presença de `dashboard`/`lancador`/`grupo`; qualquer campo do
  envelope clássico pré-ADR-0028 presente no console D23; `politica_modo`
  diferente de `somente_verboso`; `modo_inicial` declarado; chip adicional;
  ausência do chip `Esc`/`Voltar`; chip `[V]` presente.

A passividade do console (sem navegação, sem seleção, sem paginação, sem
modo alternável) decorre da ausência desses campos no consumidor D23 puro e
do perfil `resultado_execucao` — não de um valor declarado de
`navegavel`/`politica_selecao`/`politica_paginacao`, que não integram a
forma estrutural aceita para este elemento.

Esta validação é estrutural (tela + perfil). Ela não decide documento versus
envelope — essa decisão pertence exclusivamente ao módulo
`tela/resultado_execucao.py` (seção 6.5.4). Nenhuma alteração desta seção
relaxa `tela/loader.py::_console_em_escopo_d23`; a implementação deve
conformar o novo artefato à regra existente, não relaxar a regra para
aceitar campos do envelope clássico junto do marcador D23.

### 6.5.3 Documento de runtime — forma de entrada recebida pelo módulo

O documento de runtime é entregue ao módulo **separadamente** do
`tela.json`, pelo ponto de entrada (`demo/demo.py`), nunca embutido no JSON
estrutural (`origem_dados: null` permanece; nenhum novo campo de caminho ou
binding genérico é criado).

A forma de entrada reutiliza, sem redefinir, os nomes de campo já entregues
pelo retorno de `tela.execucao_focal.executar_protocolo_focal` (H-0042):

```yaml
documento_de_runtime_capturado:
  codigo_saida: int
  stdout: str
  stderr: str
  resultado_bruto: str | None   # texto bruto exato de resultado.json, ou None se ausente
```

As fixtures `demo/fixtures/h0043_*.json` (seção 6.1) devem seguir esta forma.
Para os cenários 1-3 (documento válido), `resultado_bruto` contém o texto do
documento de sucesso H-0042 (`contrato_json_console.md` §14.9) já válido.
Para os cenários 4-6 (envelope), `resultado_bruto` contém o texto capturado
(válido, inválido ou ausente conforme o cenário) e `codigo_saida` reflete a
classificação operacional correspondente. Este handoff não exige que o
demonstrador invoque `tela.execucao_focal.executar_protocolo_focal` por
subprocesso a cada cenário — as fixtures representam a captura equivalente,
já congelada, do fluxo focal do H-0042. A invocação ao vivo do executor
sintético é permitida, mas não obrigatória; se usada, deve reutilizar
`tela/execucao_focal.py` sem alterá-lo.

### 6.5.4 Ciclo de carregamento e construção do modelo (D-H3-09)

```yaml
inicio_do_cenario:
  carregar_tela_json: uma_vez
  validar_schema_e_perfil: antes_da_construcao
  carregar_documento_runtime: uma_vez
  validar_documento: antes_da_construcao
  construir_modelo_composto_em_memoria: true

redesenho_ou_SIGWINCH:
  reler_tela_json: false
  reler_documento_runtime: false
  reutilizar_modelo_composto: true
  recalcular_representacao_fisica: true
```

Um teste automatizado deve comprovar que o redesenho: não reabre a tela
estrutural; não reabre o documento externo; não incorpora alterações
realizadas nos arquivos depois da construção do modelo; recalcula somente a
representação física para as novas dimensões. Não criar cache global ou
persistente — o modelo pertence à sessão/cenário atual.

### 6.5.5 Regra de escolha entre documento e envelope (D-H3-10)

Ordem de decisão vinculante (a interrupção tem precedência sobre a regra
genérica de código não zero, pois ambas compartilham `codigo_saida != 0`):

```text
1. codigo_saida == 130               -> envelope, diagnostico=interrupcao
2. codigo_saida != 0 (e != 130)      -> envelope, diagnostico=codigo_nao_zero
3. codigo_saida == 0 e resultado_bruto is None
                                      -> envelope, diagnostico=resultado_ausente
4. codigo_saida == 0 e resultado_bruto nao decodifica como JSON
                                      -> envelope, diagnostico=resultado_malformado
5. codigo_saida == 0 e JSON valido mas nao atende ao schema esperado
                                      -> envelope, diagnostico=resultado_semanticamente_invalido
6. codigo_saida == 0 e documento sintatica e semanticamente valido
                                      -> apresentar documento original
                                         (qualquer status semantico interno:
                                         sucesso, parcial ou falha)
```

A validação sintática e semântica do documento (passos 4-6) deve **reutilizar**
as funções já existentes e testadas de `tela/execucao_focal.py`
(`resultado_json_sintaticamente_valido`, `resultado_semanticamente_valido`),
sem duplicar nem redefinir essa lógica. Este handoff não altera
`tela/execucao_focal.py`.

Um documento válido com `status: falha` (`contrato_json_console.md` §14.5.1)
continua sendo apresentado diretamente — nunca convertido em envelope.

### 6.5.6 Estrutura normativa do envelope de erro

```yaml
tipo: multinivel
apresentacao: conjuntos_campos
campos_obrigatorios_em_ordem_fixa:
  - status
  - diagnostico
  - codigo_saida
  - stdout
  - stderr
  - resultado_json
status: falha
```

O envelope deve ser expresso como documento `conjuntos_campos` compatível
com o schema semântico multinível já vigente (`contrato_json_console.md`
§12): um nível `container` (o conjunto único do envelope) com seis filhos de
nível `nome_valor`, na ordem fixa acima — reaproveitando a mesma forma
estrutural (`conjunto` com campos `nome_valor`, dois níveis) já prevista por
`contrato_json_console.md` §13.4 para `conjuntos_campos`, sem criar
apresentação nova. Nenhum campo adicional pode ser intercalado; a ordem é
normativa; o renderer não reordena os campos.

Diagnósticos canônicos (usar exatamente):

```yaml
codigo_nao_zero: A execução terminou com código de saída não zero.
resultado_ausente: A execução não produziu o documento de resultado.
resultado_malformado: O documento de resultado não contém JSON válido.
resultado_semanticamente_invalido: O documento de resultado não atende ao schema esperado.
interrupcao: A execução foi interrompida.
```

`stdout` e `stderr` não substituem o diagnóstico, não são concatenados a ele
e não alteram sua classificação.

### 6.5.7 Canais `stdout`/`stderr` e campo `resultado_json`

```yaml
stdout:
  ausente_ou_vazio: { exibicao: indisponível }
stderr:
  ausente_ou_vazio: { exibicao: indisponível }

resultado_json:
  sem_conteudo: { valor: null, exibicao: indisponível }
  com_conteudo: { tipo: string, valor: texto_bruto_exato }
```

Devem ser preservados espaços, quebras de linha, ordem das chaves e
indentação originais de `resultado_bruto`; é permitido somente o escape
necessário para transportar o texto como string JSON dentro do campo
`nome_valor` do envelope. É proibido corrigir, normalizar, reserializar ou
inferir conteúdo — tanto para texto válido quanto inválido.

### 6.5.8 Apresentação visual do erro

```yaml
estilo_especial: false
moldura_especial: false
cor_alerta: nao_utilizada
```

A falha é comunicada somente pelos campos `status`, `diagnostico` e
`codigo_saida`. É proibido hardcodar cor, alterar `config/estilo.json` ou
criar moldura/estado visual especial no renderer para o envelope.

### 6.5.9 Responsabilidades do módulo `tela/resultado_execucao.py`

O módulo deve:

- validar a compatibilidade do perfil da tela com `resultado_execucao`
  (coordenando com a validação estrutural do loader, seção 6.5.2, sem
  duplicá-la desnecessariamente);
- receber a forma de entrada do documento de runtime (seção 6.5.3) sem
  redefinir o protocolo do H-0042;
- classificar a apresentação como documento direto ou envelope (seção
  6.5.5);
- materializar o envelope determinístico (seção 6.5.6);
- preservar o texto bruto de `resultado_json` (seção 6.5.7);
- construir ou coordenar a construção do modelo composto em memória —
  expressando tanto o documento original quanto o envelope como documento
  `conteudo_externo` multinível válido, para reaproveitar sem alteração o
  caminho genérico de construção de modelo já existente no motor
  compartilhado (`tela/modelo.py`, preservado);
- expor ao renderer um modelo já validado e classificado.

O módulo não deve: executar o processo focal (isso pertence a
`tela/execucao_focal.py`, invocado ou não pelo ponto de entrada); selecionar
itens; abrir telas; manter pilha de navegação; suspender/restaurar origem;
renderizar ANSI diretamente; redefinir o renderer; acessar
`config/estilo.json` para escolher cor; persistir estado além da
sessão/cenário atual.

### 6.5.10 Limites do loader (quando alterado)

Alterações em `tela/loader.py`, se necessárias, devem limitar-se a: aceitar
e validar o campo raiz `perfil`; validar a estrutura específica de
`resultado_execucao` (seção 6.5.2); impedir conteúdo de runtime incorporado
ao JSON estrutural; impedir releitura automática em redesenho. Não criar
resolução global de bindings ou catálogo genérico de perfis.

### 6.5.11 Limites do renderer (quando alterado)

Alterações em `tela/renderizador.py`, se necessárias, devem limitar-se a
consumir o modelo já validado e classificado, apresentar o console passivo,
respeitar a apresentação `conjuntos_campos` já suportada, recalcular
representação física em redimensionamento, sem reler arquivos, sem decidir
documento versus envelope, sem gerar diagnóstico, sem reordenar campos, sem
criar estilo especial e sem implementar paginação para este perfil. Toda
classificação deve ocorrer antes do renderer, em `tela/resultado_execucao.py`.

### 6.5.12 Ponto de entrada demonstrativo (`demo/demo.py`)

`demo/demo.py` deve incluir os seis cenários H-0043, cada um acessível por
`python demo/demo.py <identificador>` (mecanismo já existente de
`_tela_inicial_de_argv`/`_carregar_modelo_por_id`). Os identificadores devem
ser exatamente os nomes-base das fixtures de documento de runtime:

```text
h0043_resultado_sucesso
h0043_resultado_parcial
h0043_resultado_falha_semantica
h0043_envelope_falha_operacional
h0043_envelope_resultado_invalido
h0043_envelope_interrupcao
```

Todos os seis identificadores resolvem para a mesma tela estrutural
`resultado_execucao` e para a fixture de mesmo nome. Como o catálogo
genérico atual (`_CATALOGO_CONTEUDO_EXTERNO`) mapeia 1:1 id-de-tela para
id-de-conteúdo, este handoff autoriza um mecanismo de despacho adicional em
`demo/demo.py` (ex.: catálogo próprio para os seis identificadores de
cenário do perfil `resultado_execucao`) que: carregue sempre a mesma tela
`resultado_execucao.json`; localize a fixture de documento de runtime
correspondente; entregue ambos, separadamente, ao módulo
`tela/resultado_execucao.py` para construção do modelo. A distribuição
concreta entre funções pode seguir os padrões reais do repositório, desde
que preserve: carregamento único por cenário; nenhuma cópia do documento
externo para dentro do objeto bruto do `tela.json`; nenhum bypass do
loader/módulo/renderer.

É proibido: imprimir quadros prontos diretamente; abrir a tela a partir do
chip `Executar`; criar origem suspensa; implementar retorno/restauração;
substituir `demo/demo.py` por demonstrador auxiliar. Nenhum auxiliar novo
está autorizado pelo manifesto (seção 6.1) — não criar arquivo auxiliar. O
encerramento de cada cenário reutiliza exclusivamente o mecanismo já
existente: `Esc` com `pilha_telas` vazia define `saindo = True` (o rótulo do
chip é `Voltar`, mas como a tela é aberta diretamente por argumento de linha
de comando — sem tela de origem empilhada —, o comportamento efetivo é
encerrar a demonstração; isto não é o retorno/restauração do Handoff 4).

## 7. Entradas, fixtures, temporários e saídas

```yaml
entradas_reais: inexistente

fixtures:
  documento_de_runtime:
    - demo/fixtures/h0043_resultado_sucesso.json
    - demo/fixtures/h0043_resultado_parcial.json
    - demo/fixtures/h0043_resultado_falha_semantica.json
    - demo/fixtures/h0043_envelope_falha_operacional.json
    - demo/fixtures/h0043_envelope_resultado_invalido.json
    - demo/fixtures/h0043_envelope_interrupcao.json
  quadro_esperado_80x24:
    - demo/fixtures/h0043_quadro_sucesso_80x24.txt
    - demo/fixtures/h0043_quadro_parcial_80x24.txt
    - demo/fixtures/h0043_quadro_falha_semantica_80x24.txt
    - demo/fixtures/h0043_quadro_falha_operacional_80x24.txt
    - demo/fixtures/h0043_quadro_resultado_invalido_80x24.txt
    - demo/fixtures/h0043_quadro_interrupcao_80x24.txt
  natureza: configuracao_controlada_permanente
  contaminacao_por_execucao: inexistente

configuracoes:
  - config/telas/demo/resultado_execucao.json

temporarios_operacionais: nenhum_novo_neste_handoff
saidas_geradas: nenhuma_saida_permanente_alem_das_fixtures_nominais
politica_de_sobrescrita: fixtures_sao_permanentes_e_versionadas
politica_de_limpeza: nao_aplicavel_sem_temporarios_novos
```

Não misturar entrada real com fixture. Nenhuma evidência material pode
permanecer somente em `/tmp`.

## 8. Tarefas

1. Criar `config/telas/demo/resultado_execucao.json` conforme a seção
   6.5.1, ajustando a forma JSON aos schemas reais vigentes.
2. Implementar `tela/resultado_execucao.py` com as responsabilidades da
   seção 6.5.9 (validação de perfil coordenada com o loader, escolha
   documento/envelope, materialização do envelope, construção do modelo
   composto).
3. Estender `tela/loader.py` somente se necessário, dentro dos limites da
   seção 6.5.10.
4. Estender `tela/renderizador.py` somente se necessário, dentro dos
   limites da seção 6.5.11.
5. Criar as seis fixtures de documento de runtime e as seis fixtures de
   quadro esperado `80x24` (seção 6.1).
6. Integrar os seis cenários em `demo/demo.py` conforme a seção 6.5.12.
7. Criar `tela/teste_resultado_execucao.py` com os casos nominais e
   negativos da seção 10.
8. Estender `tela/teste_loader.py`, `tela/teste_renderizador.py` e
   `demo/teste_demo.py` somente com os casos necessários e não cobertos
   pelo item 7.
9. Executar as verificações locais da seção 10 e a demonstração da seção
   11.
10. Criar o relatório desta execução usando o template canônico (seção
    12).

## 9. Critérios de aceite

| ID | Critério | Evidência independente esperada |
|---|---|---|
| CA-01 | Todos os arquivos criados/alterados estão dentro do manifesto (seção 6.1) | `git status --short` comparado ao manifesto |
| CA-02 | A tela estrutural `resultado_execucao` é válida e reutilizável | `tela/teste_loader.py` — carregamento sem erro |
| CA-03 | O console `console_resultado` é consumidor D23 puro (`id`, `tipo`, `titulo`, `formato.excesso.politica_modo`), `politica_modo: somente_verboso`, `modo_inicial` ausente, nenhum campo do envelope clássico pré-ADR-0028 presente | `tela/teste_resultado_execucao.py` e `tela/teste_loader.py` — inspeção do modelo e rejeição do loader |
| CA-04 | Somente `Esc`/`Voltar` está declarado na barra | teste de validação da barra |
| CA-05 | O conteúdo de runtime não é incorporado ao `tela.json` (é entregue separadamente) e o comportamento do console é passivo (navegação, seleção, paginação e truncamento ausentes), sem exigir os campos clássicos removidos como prova | inspeção do JSON criado + teste de ausência de campo de caminho + `tela/teste_resultado_execucao.py` — inspeção do modelo e do quadro renderizado |
| CA-06 | Tela e documento são carregados uma única vez por cenário | teste com contador/mock de chamadas de carregamento |
| CA-07 | Redesenho/SIGWINCH não relêem arquivos | teste com mutação do arquivo após construção do modelo |
| CA-08 | Documento válido com código `0` é apresentado diretamente | teste dos cenários sucesso/parcial |
| CA-09 | Falha semântica válida não é convertida em falha operacional | teste do cenário falha_semantica |
| CA-10 | Código não zero sempre produz envelope | teste com JSON válido + código não zero |
| CA-11 | Envelope tem exatamente seis campos na ordem normativa | teste de ordem exata |
| CA-12 | Diagnósticos, canais e `resultado_json` obedecem ao contrato | testes por diagnóstico canônico |
| CA-13 | Interrupção usa código `130` | teste do cenário interrupção |
| CA-14 | Nenhum estilo especial ou `cor_alerta` introduzido | inspeção do renderer e de `config/estilo.json` (inalterado) |
| CA-15 | Os seis quadros `80x24` coincidem integralmente com as expectativas | comparação byte a byte automatizada |
| CA-16 | Não há paginação, truncamento ou omissão | inspeção dos quadros e do modelo |
| CA-17 | Os seis cenários funcionam por `demo/demo.py` | execução manual de cada `python demo/demo.py <id>` |
| CA-18 | H-0042 e seleção existente não regridem | suíte de regressão (seção 10) |
| CA-19 | A suíte completa passa | `PYTHONDONTWRITEBYTECODE=1 python -m pytest` |
| CA-20 | O stage permanece vazio ao final | `git status --short` |
| CA-21 | Não há resíduos temporários | inspeção de `/tmp` e do repositório |
| CA-22 | O relatório de implementação está completo | leitura do relatório criado |

O valor esperado não pode ser derivado da própria saída observada.

## 10. Testes obrigatórios

Execute a partir da raiz:

```zsh
cd "$(git rev-parse --show-toplevel)" || return 1

PYTHONDONTWRITEBYTECODE=1 python -m pytest -q --tb=short \
  tela/teste_resultado_execucao.py \
  tela/teste_loader.py \
  tela/teste_renderizador.py \
  demo/teste_demo.py

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

**Tela e perfil:** tela `resultado_execucao` válida (console consumidor D23
puro, `politica_modo: somente_verboso`, `modo_inicial` ausente); ausência de
`perfil`; perfil desconhecido; perfil correto com dois consoles; perfil
correto com outro elemento funcional; consumidor D23 com `origem_dados`;
consumidor D23 com `itens`; consumidor D23 com `politica_composicao`;
consumidor D23 com `politica_navegacao`; consumidor D23 com
`politica_selecao`; consumidor D23 com `politica_paginacao`; consumidor D23
com `politica_exibicao`; consumidor D23 com `modo_inicial`; consumidor D23
com overflow de truncamento (`overflow_normal` ou equivalente); consumidor
D23 com `politica_modo` diferente de `somente_verboso`; chip adicional;
ausência de `Esc`/`Voltar`; chip `[V]` presente; apresentação fixa indevida
na tela; conteúdo de runtime incorporado ao `tela.json`.

**Escolha documento/envelope:** sucesso válido com código zero; parcial
válido com código zero; falha semântica válida com código zero; código não
zero com JSON válido; código não zero sem resultado; resultado ausente com
código zero; JSON malformado; documento semanticamente inválido;
interrupção com código `130`; interrupção com resultado prévio.

**Envelope:** ordem exata dos seis campos; todos os campos presentes;
`status: falha`; cada um dos cinco diagnósticos canônicos; canais vazios
exibidos como `indisponível`; `resultado_json: null` exibido como
`indisponível`; texto válido preservado literalmente; texto inválido
preservado literalmente; ausência de correção ou reserialização; ausência
de estilo especial.

**Sessão e redimensionamento:** tela carregada uma vez; documento carregado
uma vez; modelo preservado em memória; alteração posterior da fixture não
muda a sessão já construída; `SIGWINCH` recalcula dimensões; `SIGWINCH` não
relê arquivos; quadro reconstruído sem resíduos; política de terminal
pequeno vigente preservada.

**Integração e regressão:** seis cenários acessíveis por `demo/demo.py`;
nenhum cenário faz bypass do fluxo (loader → módulo → renderer); H-0042
permanece funcional; seleção múltipla existente permanece funcional;
execução sintética e reversível permanece funcional; sessão TTY e fluxo
não-TTY existentes permanecem funcionais; suíte completa permanece
aprovada.

Fora da automação deste handoff: binding real com o Pipeline; ativação do
chip `Executar`; abertura/retorno entre telas.

## 11. Demonstração operacional

```yaml
cwd: "."
comum_a_todos_os_cenarios:
  terminal: 80x24
  campos_visiveis_documento: conforme o documento H-0042 (Resumo/Itens)
  campos_visiveis_envelope: [status, diagnostico, codigo_saida, stdout, stderr, resultado_json]
  chip_visivel: [Esc — Voltar]
  ausencia: [chip Executar, chip [V], paginacao, abertura de outra tela]
  condicao_de_encerramento: Esc encerra a demonstracao (pilha_telas vazia)

cenarios:
  - id: h0043_resultado_sucesso
    comando: python demo/demo.py h0043_resultado_sucesso
    fixture: demo/fixtures/h0043_resultado_sucesso.json
    quadro_esperado: demo/fixtures/h0043_quadro_sucesso_80x24.txt
    apresentacao: documento_original (status semantico sucesso)
  - id: h0043_resultado_parcial
    comando: python demo/demo.py h0043_resultado_parcial
    fixture: demo/fixtures/h0043_resultado_parcial.json
    quadro_esperado: demo/fixtures/h0043_quadro_parcial_80x24.txt
    apresentacao: documento_original (status semantico parcial)
  - id: h0043_resultado_falha_semantica
    comando: python demo/demo.py h0043_resultado_falha_semantica
    fixture: demo/fixtures/h0043_resultado_falha_semantica.json
    quadro_esperado: demo/fixtures/h0043_quadro_falha_semantica_80x24.txt
    apresentacao: documento_original (status semantico falha; codigo_saida 0)
  - id: h0043_envelope_falha_operacional
    comando: python demo/demo.py h0043_envelope_falha_operacional
    fixture: demo/fixtures/h0043_envelope_falha_operacional.json
    quadro_esperado: demo/fixtures/h0043_quadro_falha_operacional_80x24.txt
    apresentacao: envelope_de_erro (codigo_saida nao zero; JSON valido preservado em resultado_json)
  - id: h0043_envelope_resultado_invalido
    comando: python demo/demo.py h0043_envelope_resultado_invalido
    fixture: demo/fixtures/h0043_envelope_resultado_invalido.json
    quadro_esperado: demo/fixtures/h0043_quadro_resultado_invalido_80x24.txt
    apresentacao: envelope_de_erro (texto invalido preservado literalmente)
  - id: h0043_envelope_interrupcao
    comando: python demo/demo.py h0043_envelope_interrupcao
    fixture: demo/fixtures/h0043_envelope_interrupcao.json
    quadro_esperado: demo/fixtures/h0043_quadro_interrupcao_80x24.txt
    apresentacao: envelope_de_erro (codigo_saida 130; resultado previo preservado)
```

Código de saída zero, isoladamente, não comprova a entrega. A comparação do
quadro produzido pelo fluxo real com o arquivo esperado deve ser integral
(sem normalização de espaços, sem recorte, sem snapshot parcial).

### 11.1 Roteiro de validação manual

Roteiro destinado exclusivamente ao usuário, para execução após a
implementação e antes do fechamento manual. O usuário deve apagar as
opções não observadas e manter somente o resultado real.

```yaml
id: RVM-H0043-01
cenario: sucesso
comando: python demo/demo.py h0043_resultado_sucesso
passos:
  - abrir em terminal 80x24
  - observar o console único apresentando o documento de resultado
  - pressionar Esc
resultado_esperado: >-
  quadro identico ao arquivo h0043_quadro_sucesso_80x24.txt; unico chip
  visivel Esc — Voltar; Esc encerra a demonstracao
respostas_possiveis:
  - CONFORME
  - DIVERGENCIA_VISUAL
  - CONTEUDO_AUSENTE
  - CONTEUDO_TRUNCADO
  - PAGINACAO_INDEVIDA
  - CHIP_INDEVIDO
  - CAMPO_FORA_DE_ORDEM
  - TEXTO_BRUTO_ALTERADO
  - ERRO_DE_EXECUCAO
observacao:
```

```yaml
id: RVM-H0043-02
cenario: parcial
comando: python demo/demo.py h0043_resultado_parcial
passos:
  - abrir em terminal 80x24
  - observar o console apresentando o documento com status parcial
  - pressionar Esc
resultado_esperado: >-
  quadro identico ao arquivo h0043_quadro_parcial_80x24.txt; documento
  original apresentado diretamente (nao convertido em envelope)
respostas_possiveis:
  - CONFORME
  - DIVERGENCIA_VISUAL
  - CONTEUDO_AUSENTE
  - CONTEUDO_TRUNCADO
  - PAGINACAO_INDEVIDA
  - CHIP_INDEVIDO
  - CAMPO_FORA_DE_ORDEM
  - TEXTO_BRUTO_ALTERADO
  - ERRO_DE_EXECUCAO
observacao:
```

```yaml
id: RVM-H0043-03
cenario: falha_semantica
comando: python demo/demo.py h0043_resultado_falha_semantica
passos:
  - abrir em terminal 80x24
  - observar o console apresentando o documento com status falha e codigo_saida 0
  - pressionar Esc
resultado_esperado: >-
  quadro identico ao arquivo h0043_quadro_falha_semantica_80x24.txt;
  documento original apresentado diretamente, sem conversao em envelope de
  erro
respostas_possiveis:
  - CONFORME
  - DIVERGENCIA_VISUAL
  - CONTEUDO_AUSENTE
  - CONTEUDO_TRUNCADO
  - PAGINACAO_INDEVIDA
  - CHIP_INDEVIDO
  - CAMPO_FORA_DE_ORDEM
  - TEXTO_BRUTO_ALTERADO
  - ERRO_DE_EXECUCAO
observacao:
```

```yaml
id: RVM-H0043-04
cenario: falha_operacional
comando: python demo/demo.py h0043_envelope_falha_operacional
passos:
  - abrir em terminal 80x24
  - observar o envelope de erro com os seis campos na ordem normativa
  - conferir que resultado_json preserva o JSON valido produzido apesar do codigo nao zero
  - pressionar Esc
resultado_esperado: >-
  quadro identico ao arquivo h0043_quadro_falha_operacional_80x24.txt;
  status falha; diagnostico "A execução terminou com código de saída não
  zero."; resultado_json com o texto bruto exato
respostas_possiveis:
  - CONFORME
  - DIVERGENCIA_VISUAL
  - CONTEUDO_AUSENTE
  - CONTEUDO_TRUNCADO
  - PAGINACAO_INDEVIDA
  - CHIP_INDEVIDO
  - CAMPO_FORA_DE_ORDEM
  - TEXTO_BRUTO_ALTERADO
  - ERRO_DE_EXECUCAO
observacao:
```

```yaml
id: RVM-H0043-05
cenario: resultado_invalido
comando: python demo/demo.py h0043_envelope_resultado_invalido
passos:
  - abrir em terminal 80x24
  - observar o envelope de erro
  - conferir que resultado_json preserva o texto invalido literalmente (sem correcao)
  - pressionar Esc
resultado_esperado: >-
  quadro identico ao arquivo h0043_quadro_resultado_invalido_80x24.txt;
  diagnostico "O documento de resultado não contém JSON válido." ou "...não
  atende ao schema esperado.", conforme o caso da fixture
respostas_possiveis:
  - CONFORME
  - DIVERGENCIA_VISUAL
  - CONTEUDO_AUSENTE
  - CONTEUDO_TRUNCADO
  - PAGINACAO_INDEVIDA
  - CHIP_INDEVIDO
  - CAMPO_FORA_DE_ORDEM
  - TEXTO_BRUTO_ALTERADO
  - ERRO_DE_EXECUCAO
observacao:
```

```yaml
id: RVM-H0043-06
cenario: interrupcao
comando: python demo/demo.py h0043_envelope_interrupcao
passos:
  - abrir em terminal 80x24
  - observar o envelope de erro com codigo_saida 130
  - conferir que resultado_json preserva o resultado eventualmente produzido antes da interrupcao
  - pressionar Esc
resultado_esperado: >-
  quadro identico ao arquivo h0043_quadro_interrupcao_80x24.txt; status
  falha; diagnostico "A execução foi interrompida."
respostas_possiveis:
  - CONFORME
  - DIVERGENCIA_VISUAL
  - CONTEUDO_AUSENTE
  - CONTEUDO_TRUNCADO
  - PAGINACAO_INDEVIDA
  - CHIP_INDEVIDO
  - CAMPO_FORA_DE_ORDEM
  - TEXTO_BRUTO_ALTERADO
  - ERRO_DE_EXECUCAO
observacao:
```

Não executar nem preencher esta validação manual durante a implementação.

## 12. Relatório da execução

Criar um novo relatório em:

```text
docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0043.md
```

Usar obrigatoriamente:

```text
docs/templates/TEMPLATE_RELATORIO_IMPL.md
```

O relatório deve registrar, de forma compacta:

```yaml
- status
- handoff
- ADR_principal
- arquivos_criados
- arquivos_alterados
- arquivos_preservados
- delta_por_camada
- testes_focais
- testes_de_regressao
- suite_completa
- demonstracoes_80x24
- preservacao_literal_resultado_json
- prova_de_carregamento_unico
- prova_de_nao_releitura_em_SIGWINCH
- validacao_manual_pendente
- git_diff_check
- stage
- residuos
- bloqueios
```

Regras: cada execução material produz seu próprio relatório; não sobrescrever
relatório anterior; registrar somente fatos materiais; não copiar código,
diff completo, handoff, logs extensos ou quadros completos; omitir campos e
seções vazios; teto normal de 600 palavras, até 900 quando houver conteúdo
material não resumível; o relatório não aprova formalmente a implementação.

## 13. Resposta terminal

Retorne somente:

```yaml
status: <STATUS_LITERAL>
relatorio: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0043.md
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
silenciosamente — isto inclui, em particular, `tela/modelo.py` e
`tela/navegacao.py`.

Se um item externo for estritamente necessário para cumprir o handoff,
preservar testes obrigatórios ou evitar aborto desproporcional:

1. pare antes da alteração;
2. registre e retorne:

```yaml
status: I3_HANDOFF_PATCH_REQUIRED
arquivo_necessario:
evidencia:
impacto:
```

3. peça autorização explícita ao usuário antes de alterar o arquivo externo.

A autorização não permite criar semântica, arquitetura, schema, formato ou
política nova. A correção segue:
`PATCH_HANDOFF → QA_HANDOFF → PATCH_IMPLEMENTACAO → QA_IMPLEMENTACAO`. Não
ampliar o manifesto silenciosamente.

## 15. Condições de bloqueio

### Bloqueio documental

```yaml
status: H3_BLOCKED_DOCUMENTATION
ponto:
autoridades_em_conflito:
decisao_necessaria:
```

Usar somente quando ADR-0036 e os contratos vigentes forem insuficientes ou
contraditórios.

### Evidência incompleta

```yaml
status: H4_QA_EVIDENCE_INCOMPLETE
evidencia_faltante:
comando_necessario:
```

Usar quando a capacidade estiver implementada, mas faltar somente evidência
reproduzível.

### Patch de handoff necessário durante implementação

```yaml
status: I3_HANDOFF_PATCH_REQUIRED
arquivo_ou_regra:
evidencia:
```

Não transformar necessidade de arquivo adicional em alteração não
autorizada (ver seção 14).

Bloquear também quando: faltar decisão; houver contradição documental; for
necessário inventar formato ou schema; diretório novo necessário não
estiver autorizado; houver risco de sobrescrever entrada real; o handoff for
inexequível; a leitura focal autorizada for insuficiente.

Se o bloqueio ocorrer antes de qualquer resultado material, não criar
relatório. Se já houver leitura, verificação, alteração ou evidência que
precise sobreviver ao contexto, criar relatório factual do bloqueio.

## 16. Limite de encerramento

Ao concluir implementação, testes locais, demonstração e relatório, pare.

Não faça QA formal.
Não aprove a própria entrega.
Não prepare nem execute commit.
Não inicie outro ciclo.

## 17. Verificação interna obrigatória (autoria deste handoff)

```yaml
todos_os_arquivos_do_manifesto_existem_ou_estao_marcados_como_novos: true
nenhuma_obrigacao_exige_arquivo_fora_do_manifesto: true
comandos_de_teste_correspondem_ao_repositorio_real: true
seis_cenarios_cabem_em_80x24: true
quadros_esperados_exequiveis_sem_paginacao_ou_truncamento: true
demonstracao_usa_demo_demo_py: true
fluxo_nao_antecipa_Handoff_4: true
renderer_nao_recebe_responsabilidade_de_classificacao: true
novo_modulo_nao_recebe_responsabilidade_de_execucao: true
relatorio_de_implementacao_produzivel_pelo_template_vigente: true
sem_contradicao_entre_testes_demo_manifesto_e_criterios_de_aceite: true
```

Esta verificação pertence ao próprio handoff; nenhuma etapa ou relatório
separado de exequibilidade foi criado.
