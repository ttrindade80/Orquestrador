---
name: H-0041-selecao-multipla-estado-comandos-e-apresentacao
description: "Autoriza a implementação do Handoff 1 do ITEM-0006 (ADR-0034): estado da seleção múltipla por conjunto de IDs estáveis, comandos Espaço/Enter/Esc, reconciliação, ordenação lógica e indicadores/chips — sem operação externa"
metadata:
  type: handoff_implementacao
  status: READY_FOR_IMPLEMENTATION
  id: H-0041
  data_criacao: 2026-07-28
rastreabilidade:
  contrato_alvo: docs/contratos/contrato_console.md
  adr_relacionadas:
    - docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md
  issues_relacionadas:
    - ITEM-0006
  handoffs_anteriores:
    - H-0040
  revalidacoes_manuais:
    - docs/relatorios/RELATORIO_REVALIDACAO_MANUAL_H-0041_R02.md
  patches_documentais:
    - docs/relatorios/RELATORIO_PATCH_H-0041_HANDOFF_P02.md
---

# H-0041 — Implementar estado, comandos e apresentação da seleção múltipla

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

- Branch `master`, HEAD `721f8f1`, stage vazio, worktree contendo somente artefatos acumulados da ADR-0034 (confirmado por leitura Git real nesta execução).
- ADR-0034 aceita; aplicação documental aprovada (`ADR_APPLICATION_APPROVED`, `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0034_P02.md`), leitura do relatório dispensada.
- `docs/backlog.md`: `ITEM-0006` permanece em `em_andamento` com a redação anterior à aprovação — ainda condiciona a criação deste handoff à conclusão do patch documental e à aprovação do QA pós-patch da aplicação da ADR-0034. Essa condição material já foi satisfeita por `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0034_P02.md` (`ADR_APPLICATION_APPROVED`, achados pendentes: nenhum); o texto do backlog não foi atualizado para refletir essa aprovação, e este handoff não atribui ao relatório autoridade normativa superior à do backlog nem exige um novo patch do backlog antes da implementação:

  ```yaml
  aplicacao_ADR_0034:
    QA_final: ADR_APPLICATION_APPROVED
    evidencia: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0034_P02.md
    achados_pendentes: []

  backlog:
    redacao_atual: ainda_reflete_condicao_pre_aprovacao
    condicao_material: satisfeita_pelo_QA_P02
    afirmacao_de_propagacao_ja_realizada: false

  handoff:
    criacao_autorizada: true
  ```
- `tela/navegacao.py` já contém `processar_espaco(estado)`, que hoje devolve o estado inalterado e documenta explicitamente: "A barra de espaco pertence ao ciclo de selecao multipla (ITEM-0006), fora do escopo do H-0040" — ponto de extensão confirmado por leitura direta do código, não presumido.
- `tela/loader.py` já aceita `"multipla"` em `_POLITICA_SELECAO_VALIDOS` (junto de `"nenhuma"`/`"unica"`), mas não valida nem consome o campo `selecionavel` de item — este passa hoje como campo inerte.
- `tela/renderizador.py` já possui um mecanismo de contexto de runtime (`_navegacao_atual`, populado por `renderizar_tela`) e um padrão de existência dinâmica de chip por `regra_existencia` (usado hoje para `[⇆]`/`[✥]`, ADR-0031 D14). Este é o mecanismo já estabelecido a estender para o chip `Espaço` e o rótulo dinâmico de `[⏎]`.
- O indicador de cursor (`ec`) já é renderizado por `_aplicar_indicador_linhas` usando `estilo.selecionado_simbolo`/`estilo.selecionado_off` como coluna própria e estável (D12/ADR-0031). Não existe hoje nenhuma coluna nem campo de estilo equivalente para o indicador de inclusão (`tg`).
- `config/estilo.json` e `contrato_estilo.md` estão **fora do manifesto de leitura autorizado nesta criação de handoff**; não foi verificado se já existem campos de símbolo (`●`/`○`) utilizáveis para `tg`. Se a implementação constatar sua ausência, aplica-se a seção 14 (Exceção operacional) — este handoff não presume a resposta.
- Nenhuma fixture existente combina, no mesmo console com `distribuicao_matricial`, itens navegáveis e itens não navegáveis lado a lado — a fixture de oito itens (D-SEL-22) é a primeira a exercitar essa combinação; não presumir que o caminho de renderização atual já trata esse caso sem ajuste.

## 3.1 Revalidação manual TTY — Rodada 2 e decisão do usuário (patch P02)

O QA técnico anterior (`docs/relatorios/RELATORIO_QA_H-0041_IMPLEMENTACAO_P03.md`) aprovou a estrutura lógica da seleção múltipla. A segunda revalidação manual em TTY real reprovou a apresentação de estado inativo e o acionamento real de `Enter`/`Todos`:

```yaml
revalidacao_manual:
  rodada: 2
  status: MANUAL_VALIDATION_FAILED
  relatorio: docs/relatorios/RELATORIO_REVALIDACAO_MANUAL_H-0041_R02.md

achados:
  - id: H0041-MANUAL-R02-001
    componente: Enter_Todos
    impacto: "Enter sem seleção não selecionou os quatro itens esperados em TTY real"
  - id: H0041-MANUAL-R02-002
    componente: chip_Enter
    impacto: "rótulo Executar apresentado em caixa baixa, sem distinção visual de estado inativo"
  - id: H0041-MANUAL-R02-003
    componente: chip_Espaco
    impacto: "chip de item não selecionável apresentado como ativo"

decisao_do_usuario:
  cor_inativo:
    valor: cinza
    autoridade_de_configuracao: config/estilo.json
    hardcode_no_renderer: proibido
    capitalizacao_normal_dos_rotulos: preservada
```

Leitura focal confirmou, em `tela/renderizador.py::_texto_chip_barra` (~linhas 1524-1557), que o mecanismo vigente de apresentação de inatividade é `texto.lower()` ("REDUCAO DE ENFASE: rotulo em CAIXA BAIXA", conforme o próprio docstring da função) e que `cor_inativo` é citado ali como "mecanismo normativo" ainda sem valor ANSI concreto. Esse mecanismo de caixa baixa fica **proibido** a partir deste patch. A correção — aplicação de `cor_inativo` (cinza) vindo de `config/estilo.json`, preservando capitalização normal — e a investigação do achado `H0041-MANUAL-R02-001` ficam autorizadas nominalmente na seção 6.5, para o próximo ciclo técnico (P04). Este patch de handoff não implementa.

## 4. Objetivo

Implementar, no console de nível único já navegável (ADR-0031/H-0040), a seleção múltipla por conjunto de IDs estáveis: alternância por `Espaço`, `Todos`/`Executar` por `Enter`, limpeza por `Esc`, reconciliação e ordenação lógica, indicadores `ec`/`tg` e chips `Espaço`/`Enter` correspondentes — sem qualquer operação externa, conforme D-SEL-01 a D-SEL-10 e D-SEL-21 (Handoff 1), demonstrado pela fixture fechada de D-SEL-22 e testado conforme D-SEL-23.

## 5. Manifesto fechado de leitura

```yaml
leitura_integral:
  - docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md
  - docs/contratos/contrato_console.md
  - docs/contratos/contrato_barra_de_menus.md
  - docs/nomenclatura/32_CONSOLE.md
  - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
  - tela/navegacao.py
  - tela/modelo.py

leitura_focal:
  - arquivo: tela/renderizador.py
    comando_busca: >-
      grep -n "_navegacao_atual\|_aplicar_indicador_linhas\|regra_existencia\|
      _texto_chip_barra\|selecionado_simbolo\|selecionado_off\|
      grade_de_itens_para_indicador" tela/renderizador.py
    objetivo: >-
      localizar o dict de contexto de runtime (_navegacao_atual), a
      construção da coluna indicadora ec e o tratamento dinâmico de chips
      (regra_existencia) a estender para tg, chip Espaço e rótulo dinâmico
      de Enter
  - arquivo: tela/loader.py
    comando_busca: >-
      grep -n "_POLITICA_SELECAO_VALIDOS\|politica_selecao\|selecionavel"
      tela/loader.py
    objetivo: >-
      confirmar que "multipla" já é valor aceito e que "selecionavel" ainda
      não é validado nem consumido
  - arquivo: demo/demo.py
    comando_busca: sed -n '159,420p' demo/demo.py
    objetivo: >-
      localizar criar_estado_inicial, processar_comando (dispatch de
      Espaço/Enter/Esc/Tab/setas) e renderizar_estado — pontos de
      integração do estado de seleção
  - arquivo: demo/demo_navegacao.py
    comando_busca: cat demo/demo_navegacao.py
    objetivo: >-
      modelo estrutural do script de demonstração dedicado deste handoff
      (reaproveita demo.main; carrega tela por --tela; não cria fluxo
      paralelo)
  - arquivo: config/telas/demo/h0040_nav_console_unico_linear.json
    comando_busca: cat config/telas/demo/h0040_nav_console_unico_linear.json
    objetivo: >-
      modelo de estrutura JSON de console navegável (itens, políticas,
      distribuição matricial, barra_de_menus) para construir a fixture do
      ITEM-0006

buscas_autorizadas:
  - "grep -rn \"processar_espaco|item_selecionado|politica_selecao\" tela/ demo/ — somente leitura do contexto de cada ocorrência, sem abrir arquivo fora dos já listados"

nao_ler:
  - docs/relatorios/**
  - docs/handoff/**
  - docs/adr/**, exceto ADR-0034
  - docs/contratos/**, exceto os dois contratos listados
  - docs/nomenclatura/**, exceto os dois módulos listados
  - config/estilo.json, docs/contratos/contrato_estilo.md (fora deste manifesto; ver seção 14 se indispensável)
  - docs/arquivo/**
```

Para leitura focal, execute o comando indicado e leia somente sua saída. Não abra o arquivo inteiro por conveniência. Se a saída for insuficiente, pare e solicite expansão focal; não amplie autonomamente o contexto.

Para o patch técnico P04 (seção 6.5), ficam adicionalmente autorizados à leitura integral: `config/estilo.json`; `docs/contratos/contrato_estilo.md` (schema/semântica de `cor_inativo`, ADR-0004); o trecho de `EstiloResolvido`/`carregar_estilo` em `tela/loader.py` (~linhas 2440-2560, já citado acima); `tela/teste_loader.py`. A exclusão desses caminhos no bloco `nao_ler` acima permanece válida para o restante do escopo original deste handoff (H-0040/D-SEL-01 a D-SEL-23) e só é levantada para o campo `cor_inativo`.

## 6. Escopo da implementação

### 6.1 Arquivos e diretórios autorizados

```yaml
arquivos_existentes_a_alterar:
  - caminho: tela/navegacao.py
    finalidade: >-
      reservar, em grade_de_itens, a largura da coluna tg no cálculo de
      min_ws quando o console declarar politica_selecao: "multipla",
      preservando a paridade geométrica com a coluna ec (mesmo princípio
      já aplicado à coluna ec/LARGURA_INDICADOR_COLUNA, AT-0021/PN-0016);
      não altera a semântica de item_selecionado/processar_espaco (D13,
      seleção única) nem qualquer outra função de nível único do H-0040
  - caminho: tela/renderizador.py
    finalidade: >-
      nova coluna tg (paralela e adjacente à coluna ec, nunca sobreposta
      — módulo 32_CONSOLE.md §4.4); extensão do contexto
      _navegacao_atual (ou estrutura equivalente) para carregar a
      seleção corrente por console; extensão do tratamento dinâmico de
      chips para existência/estado do chip Espaço e rótulo dinâmico
      Todos/Executar de [⏎]
  - caminho: demo/demo.py
    finalidade: >-
      criar_estado_inicial (novo campo de runtime para a seleção,
      análogo a cursores); processar_comando (dispatch de
      Espaço/Enter/Esc delegado a tela/selecao.py quando o console
      focado declarar seleção múltipla, preservando o dispatch atual
      para unica/nenhuma); passagem do estado de seleção ao renderer

arquivos_novos_a_criar:
  - caminho: tela/selecao.py
    finalidade: >-
      estado da seleção múltipla, toggle, "selecionar todos", limpeza,
      reconciliação e ordenação lógica; funções puras, sem I/O,
      seguindo o estilo de tela/navegacao.py (nenhum dict recebido é
      mutado; toda transição retorna um novo dict)

fixture:
  - caminho: config/telas/demo/h0041_selecao_multipla_oito_itens.json
    finalidade: fixture fechada de D-SEL-22 (oito itens; seis navegáveis, dois não navegáveis)

demonstracao:
  - caminho: demo/demo_selecao.py
    finalidade: >-
      ponto de entrada TTY dedicado deste handoff, modelado em
      demo/demo_navegacao.py (reaproveita demo.main; não cria sessão
      TUI nem renderer paralelo)

testes_unitarios:
  - caminho: tela/teste_selecao.py
    finalidade: testes unitários do módulo tela/selecao.py
  - caminho: tela/teste_navegacao.py
    finalidade: >-
      testes unitários da reserva de largura da coluna tg em
      grade_de_itens, quando aplicável

testes_de_integracao:
  - caminho: tela/teste_renderizador.py
    finalidade: testes de integração da coluna tg e dos chips dinâmicos (Espaço, Todos/Executar)
  - caminho: demo/teste_demo.py
    finalidade: testes de integração do dispatch de Espaço/Enter/Esc em processar_comando
  - caminho: demo/teste_demo_selecao.py
    finalidade: testes de integração do ponto de entrada TTY dedicado (demo/demo_selecao.py)

relatorio_de_implementacao:
  caminho: docs/relatorios/IMP-0041-selecao-multipla-estado-comandos-e-apresentacao.md
  template: docs/templates/TEMPLATE_RELATORIO_IMPL.md
```

Diretórios ainda inexistentes podem ser criados somente quando aparecerem nominalmente nesta lista — nenhum diretório novo é necessário; todos os arquivos acima cabem em diretórios já existentes.

### 6.2 Arquivos e diretórios preservados ou proibidos

- `docs/adr/**`, `docs/backlog.md`, `docs/contratos/**`, `docs/nomenclatura/**`, `docs/handoff/**` — alteração normativa fora deste ciclo.
- `config/estilo.json` — alteração autorizada exclusivamente para o campo `cor_inativo` (decisão do usuário, seção 3.1; delta nominal em 6.5.2); qualquer outra alteração continua exigindo a seção 14.
- Toda fixture em `config/telas/demo/**` além da listada em 6.1 — nenhum cenário existente pode ser alterado (D-SEL-22 é exclusiva do `ITEM-0006`).
- `tela/distribuicao_matricial.py`, `tela/teste_distribuicao_matricial.py` — fora de escopo.
- `tela/loader.py`, `tela/teste_loader.py` — fora de escopo para `politica_selecao: "multipla"` e o campo `selecionavel` (já aceitos estruturalmente, sem nova validação de carregamento exigida por este handoff); autorizados exclusivamente para o delta de `cor_inativo` descrito em 6.5.3/6.5.6.
- `demo/demo_navegacao.py`, `demo/teste_demo_navegacao.py`, `demo/demo_distribuicao.py`, `demo/diagnostico.py`, `demo/explorar_barra_de_menus.py` e seus testes — preservados; nenhuma regressão de H-0040 ou anteriores é aceitável.
- `tela/modelo.py` — preservado; a seleção é estado de runtime, não campo de modelo (D-SEL-01).

### 6.3 Escopo positivo

- Estado da seleção como conjunto de IDs estáveis, por console, runtime, inicialmente vazio (D-SEL-01, D-SEL-22).
- `Espaço`: alterna a inclusão do item sob cursor quando `selecionavel: true`; não move o cursor; sem efeito em item não selecionável (D-SEL-05).
- `Enter` sem seleção: rótulo `Todos`; seleciona todos os itens `selecionavel: true` navegáveis (snapshot de IDs, D-SEL-01); com zero itens selecionáveis, chip visível e inativo (D-SEL-06).
- `Enter` com seleção: rótulo `Executar`; **inativo** — não existe operação externa neste handoff (D-SEL-07, D-SEL-21).
- `Esc` com seleção ativa: limpa a seleção e permanece na tela; só volta ao comportamento Sair/Voltar depois de limpar (D-SEL-08). `Esc` sem seleção preserva integralmente o comportamento vigente de H-0040 (sair na tela raiz, voltar nas demais).
- Reconciliação: função testável, isolada do binding, que remove IDs inexistentes e itens que deixaram de ser selecionáveis, preservando a ordem lógica (D-SEL-03). Reconciliação vazia após `Enter` não executa nem aplica `Todos` no mesmo acionamento (D-SEL-04).
- Ordenação lógica: referência é a ordem estável do console (mesma ordem de `itens_navegaveis`), nunca ordem de marcação, posição visual, página ou filtro (D-SEL-02, D-SEL-03).
- Indicador `ec`: exclusivo do cursor, já implementado por H-0040 — não alterar sua semântica.
- Indicador `tg`: símbolo de inclusão para selecionável incluído, símbolo de não inclusão para selecionável não incluído, vazio para não selecionável (D-SEL-09).
- Chip `Espaço`: existe quando o console em foco declara `politica_selecao: multipla`; ativo quando o item sob cursor é selecionável, inativo caso contrário (D-SEL-09). Mecanismo de apresentação do estado inativo: seção 6.5.1 (`cor_inativo`, nunca caixa baixa).
- Itens não navegáveis (`item_04`, `item_08` da fixture) permanecem visíveis, nunca recebem cursor, nunca entram na seleção e exibem `tg` vazio.
- Invariante geométrica: a largura útil calculada por `tela/navegacao.py` para o console deve continuar coincidindo exatamente com a área usada pelo renderer quando a coluna `tg` está presente (mesmo princípio de AT-0021/PN-0016 já aplicado a `ec`).

### 6.4 Escopo negativo

- operação consumidora, protocolo de script, dry-run, execução real;
- restauração de fixture, arquivo JSON temporário de entrada ou resultado;
- tela padrão de resultado, perfil `resultado_execucao`, abertura e retorno de tela de resultado, envelope de erro;
- filtro e paginação interativa (inclusive na fixture deste handoff);
- seleção compartilhada entre consoles;
- chip de alternância entre modo de execução (`dry-run`/execução real);
- modo não verboso ou alternável na tela padrão de resultado;
- colapso e expansão multinível;
- registry, dispatcher ou comandos arbitrários.

## 6.5 Patch técnico autorizado — P04 (cor_inativo e correção Enter/Todos)

Esta seção não implementa. Autoriza nominalmente o próximo ciclo técnico (P04), incorporando a decisão da seção 3.1. Nenhum outro arquivo além dos listados em 6.5.6 é autorizado; não autorizar ADR, contratos, nomenclatura ou backlog.

### 6.5.1 Requisito visual obrigatório

```yaml
chip_inativo:
  visibilidade: preservada
  posicao: preservada
  rotulo:
    capitalizacao: normal
    alteracao_para_minusculas: proibida
  cor:
    token_semantico: cor_inativo
    valor_concreto: cinza
    origem: config/estilo.json
  acionamento:
    efeito: nenhum
```

Exemplos:

```yaml
chip_Espaco:
  item_selecionavel:
    rotulo: Marcar
    estado: ATIVO
  item_nao_selecionavel:
    rotulo: Marcar
    estado: INATIVO
    cor: cinza

chip_Enter:
  sem_selecao:
    rotulo: Todos
    estado: ATIVO
  com_selecao:
    rotulo: Executar
    estado: INATIVO
    cor: cinza
```

Proibido como indicador de inatividade: caixa baixa; alteração do texto; remoção do chip; símbolo inventado; cor hardcoded diretamente no renderer.

### 6.5.2 Configuração de estilo

```yaml
config/estilo.json:
  adicionar_ou_definir:
    cor_inativo: cinza
  outras_chaves: preservar
```

A configuração permanece a fonte da decisão visual; o renderer não pode conter literal ANSI ou literal de cor específico para representar inatividade.

### 6.5.3 Loader e representação interna do estilo

Leitura focal de `tela/loader.py` (já citado no manifesto da seção 5) confirma: a classe `EstiloResolvido` (~linha 2440) já carrega campos de cor genéricos por chip (`cor_texto`, `cor_fundo`, ~linhas 2460-2462), mas não possui campo `cor_inativo`; `carregar_estilo` (~linha 2472) não lê hoje nenhuma chave `cor_inativo` de `config/estilo.json`. Delta nominal necessário:

```yaml
loader_ou_modelo_de_estilo:
  - caminho: tela/loader.py
    delta: >-
      adicionar campo cor_inativo a EstiloResolvido; ler cor_inativo de
      config/estilo.json em carregar_estilo; validar presença/tipo
      seguindo o padrão já usado para cor_texto/cor_fundo (V-26)
```

Não há outro arquivo de carregamento ou modelo de estilo indispensável: a cadeia `carregar_estilo → EstiloResolvido → renderer` já transporta genericamente campos de cor sem exigir novo arquivo além do listado.

### 6.5.4 Renderer

```yaml
renderer:
  - caminho: tela/renderizador.py
    delta: >-
      em _texto_chip_barra (~linha 1524), quando inativo=True: aplicar
      cor_inativo recebido de estilo (nunca hardcoded), restaurar a cor
      corretamente apos o chip, preservar capitalizacao normal do rotulo
      (remover texto.lower()); remover do docstring da funcao o
      mecanismo de caixa baixa hoje documentado; nao inferir estado
      pelo rotulo; preservar consoles sem selecao multipla (inativo
      default False, sem alteracao de comportamento)
```

### 6.5.5 Defeito independente — Enter/Todos (H0041-MANUAL-R02-001)

```yaml
H0041-MANUAL-R02-001:
  tecla: Enter
  precondicao: selecao_vazia
  esperado:
    selecao:
      - item_01
      - item_03
      - item_05
      - item_07
  observado: nenhum_item_selecionado
```

Investigar e corrigir no caminho real do TTY: `leitura_da_tecla → dispatch → seleção de todos → atualização do estado → redesenho`. A correção não pode ser considerada comprovada somente por chamada direta de função ou reprodução não interativa. Os testes devem incluir o ponto de entrada e o loop usados pela demonstração TTY (`demo/demo_selecao.py`, `demo/demo.py`), no nível automatizável.

### 6.5.6 Lista nominal autorizada do patch técnico P04

```yaml
configuracao_de_estilo:
  - config/estilo.json

loader_ou_modelo_de_estilo:
  - tela/loader.py

renderer:
  - tela/renderizador.py

dispatch_e_loop_TTY:
  - demo/demo.py
  - demo/demo_selecao.py

fixture:
  - config/telas/demo/h0041_selecao_multipla_oito_itens.json

testes:
  - tela/teste_loader.py
  - tela/teste_renderizador.py
  - demo/teste_demo.py
  - demo/teste_demo_selecao.py

relatorio:
  - docs/relatorios/RELATORIO_PATCH_H-0041_P04.md
```

### 6.5.7 Testes exigidos

```yaml
configuracao:
  - cor_inativo_existe
  - cor_inativo_igual_a_cinza
  - loader_preserva_cor_inativo

chip_Espaco:
  - ativo_em_item_selecionavel
  - cinza_em_item_nao_selecionavel
  - rotulo_Marcar_preservado

chip_Enter:
  - Todos_ativo_sem_selecao
  - Executar_cinza_com_selecao
  - rotulo_Executar_preservado
  - Enter_em_Executar_sem_efeito

Enter_Todos:
  - ponto_de_entrada_real_processa_Enter
  - quatro_itens_sao_selecionados
  - novo_quadro_mostra_quatro_tg
  - chip_Executar_aparece_cinza_no_mesmo_quadro

regressoes:
  - consoles_sem_selecao_multipla
  - selecao_unica
  - Esc
  - reconciliacao_residual
```

Os testes de apresentação devem verificar a sequência/código de cor efetivamente aplicado, sem exigir comparação byte a byte do quadro completo.

### 6.5.8 Revalidação futura obrigatória

Após implementação P04 e QA técnico aprovado, é obrigatória nova revalidação TTY pelo usuário. O roteiro futuro deve preservar os rótulos `Marcar`, `Todos`, `Executar` e avaliar a diferença ativo/inativo pela cor.

## 7. Entradas, fixtures, temporários e saídas

```yaml
entradas_reais: inexistente
fixtures:
  caminho: config/telas/demo/h0041_selecao_multipla_oito_itens.json
  natureza: configuracao_controlada_permanente
  contaminacao_por_execucao: inexistente
configuracoes: nenhuma alteracao em config/telas/demo/** alem da fixture nova
temporarios_operacionais: nenhum
saidas_geradas:
  - docs/relatorios/IMP-0041-selecao-multipla-estado-comandos-e-apresentacao.md
politica_de_sobrescrita: nao_sobrescrever_relatorio_anterior
politica_de_limpeza: nao_aplicavel
```

Não misture entrada real com fixture. Não sobrescreva entrada real sem decisão explícita. Nenhuma evidência material pode permanecer somente em `/tmp`.

## 8. Tarefas

1. Implementar `tela/selecao.py`: estado por IDs, toggle, `Todos`, limpeza, reconciliação, ordenação lógica.
2. Estender `tela/navegacao.py` (reserva de largura da coluna `tg` em `grade_de_itens`) somente quando `politica_selecao: multipla`.
3. Estender `tela/renderizador.py`: coluna `tg`, contexto de seleção, chip `Espaço` e rótulo dinâmico `Todos`/`Executar`.
4. Estender `demo/demo.py`: estado inicial, dispatch de `Espaço`/`Enter`/`Esc` para console com seleção múltipla.
5. Criar `demo/demo_selecao.py` como ponto de entrada TTY dedicado.
6. Criar a fixture `config/telas/demo/h0041_selecao_multipla_oito_itens.json` (D-SEL-22).
7. Escrever os testes unitários e de integração previstos na seção 10.
8. Executar as verificações locais previstas.
9. Criar o relatório próprio desta execução usando o template canônico.

## 9. Critérios de aceite

| ID | Critério | Evidência independente esperada |
|---|---|---|
| CA-01 | Seleção é conjunto de IDs, sem duplicatas, independente do cursor | Teste unitário em `tela/teste_selecao.py` |
| CA-02 | `Espaço` alterna item selecionável sem mover o cursor; sem efeito em item não selecionável | Teste unitário + demonstração |
| CA-03 | `Enter` sem seleção produz exatamente `item_01, item_03, item_05, item_07` | Teste de integração com a fixture de oito itens |
| CA-04 | Ordem do conjunto segue a ordem lógica do console, não a ordem de marcação | Teste unitário de ordenação |
| CA-05 | Reconciliação remove IDs inexistentes e itens que deixaram de ser selecionáveis, preservando ordem | Teste unitário isolado, sem binding |
| CA-06 | `Esc` com seleção limpa e permanece na tela; segundo `Esc` (sem seleção) preserva comportamento vigente | Teste de integração + roteiro TTY |
| CA-07 | `ec` aparece somente no item sob cursor; independe da seleção | Teste de integração |
| CA-08 | `tg` distingue incluído / não incluído / não selecionável (vazio) | Teste de integração |
| CA-09 | `item_04` e `item_08` visíveis, sem cursor, fora da seleção, `tg` vazio | Teste de integração com a fixture |
| CA-10 | Chip `Espaço` reflete corretamente ativo/inativo conforme o item sob cursor | Teste de integração |
| CA-11 | `Executar` permanece inativo; nenhuma operação externa é invocada | Inspeção de código + teste de integração |
| CA-12 | Suíte completa (`PYTHONDONTWRITEBYTECODE=1 python -m pytest`) permanece aprovada, sem regressão em H-0040 ou anteriores | Execução da suíte |
| CA-13 | Chip inativo usa `cor_inativo` (cinza) lido de `config/estilo.json`; nunca caixa baixa nem cor hardcoded no renderer | Teste de integração em `tela/teste_renderizador.py` (seção 6.5.7) |
| CA-14 | `Enter` sem seleção produz os quatro itens esperados através do ponto de entrada e loop TTY real (`demo/demo_selecao.py`), não apenas por chamada direta de função | Teste de integração em `demo/teste_demo_selecao.py` (seção 6.5.7) |

O valor esperado não pode ser derivado da própria saída observada.

CA-13 e CA-14 são exclusivos do patch técnico P04 (seção 6.5); CA-01 a CA-12 permanecem os critérios da implementação original.

## 10. Testes obrigatórios

Execute a partir da raiz:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest
```

Comandos focais (subconjuntos reais, executáveis antes da suíte completa):

```zsh
cd "$(git rev-parse --show-toplevel)" || return 1

PYTHONDONTWRITEBYTECODE=1 python -m pytest -q --tb=short \
  tela/teste_selecao.py tela/teste_navegacao.py

PYTHONDONTWRITEBYTECODE=1 python -m pytest -q --tb=short \
  tela/teste_loader.py tela/teste_renderizador.py demo/teste_demo.py demo/teste_demo_selecao.py

PYTHONDONTWRITEBYTECODE=1 python -m pytest
```

Casos mínimos adicionais exigidos pelo patch técnico P04 (`cor_inativo`, correção Enter/Todos): ver seção 6.5.7.

Casos mínimos exigidos (D-SEL-23):

**Unitários (`tela/teste_selecao.py`):**
- estado da seleção por IDs;
- toggle de item selecionável;
- ausência de efeito em item não selecionável;
- `Todos` sobre o conjunto de selecionáveis;
- `Todos` sem itens selecionáveis;
- limpeza por `Esc`;
- reconciliação de ID inexistente;
- reconciliação de item que deixou de ser selecionável;
- ordenação lógica;
- exclusão de itens não selecionáveis do conjunto;
- independência entre cursor e seleção.

**Integração (`demo/teste_demo_selecao.py` e/ou `demo/teste_demo.py`, `tela/teste_renderizador.py`):**
- carregamento da fixture de oito itens;
- seis alvos navegáveis na ordem `item_01, item_02, item_03, item_05, item_06, item_07`;
- cursor inicial em `item_01`; seleção inicial vazia;
- estados do chip `Espaço`;
- estado do chip `Todos`;
- transição para `Executar`;
- `Executar` inativo;
- indicadores `ec` e `tg`;
- `item_04`/`item_08` visíveis, sem cursor, `tg` vazio.

Casos fora da automação deste handoff: quadro TTY completo com sequências ANSI; filtro; paginação.

## 11. Demonstração operacional

```yaml
cwd: "."
comando: >-
  PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_selecao
  --tela config/telas/demo/h0041_selecao_multipla_oito_itens.json
entrada_ou_fixture: config/telas/demo/h0041_selecao_multipla_oito_itens.json
configuracao: config/estilo.json (via carregar_estilo, sem alteração)
saida_esperada: sessao_tui_interativa_com_console_de_oito_itens
prova_semantica: >-
  cursor inicial em item_01; item_04/item_08 visiveis sem cursor;
  Espaco alterna tg sem mover cursor; Enter sem selecao produz Todos;
  Executar permanece inativo; Esc limpa a selecao antes de sair/voltar
arquivos_persistentes:
  - config/telas/demo/h0041_selecao_multipla_oito_itens.json
temporarios_operacionais: nenhum
limpeza_ou_restauracao: nao_aplicavel
validacao_manual:
  executor_exclusivo: USUARIO_EM_TTY_REAL
```

Código de saída zero, isoladamente, não comprova a entrega.

A partir do patch P02 (seção 6.5), todo `estado=INATIVO`/`(inativo)` no roteiro abaixo significa `cor_inativo` (cinza) aplicado pelo renderer a partir de `config/estilo.json`, com capitalização normal preservada — nunca caixa baixa (ver 6.5.1).

### Roteiro sequencial de validação TTY

O console é de nível único (ADR-0031/H-0040), com itens em lista vertical; a transição entre itens navegáveis usa exclusivamente `Seta para baixo`.

```yaml
- numero: 1
  tecla_acionada: (nenhuma — estado inicial)
  foco_esperado: item_01
  selecao_esperada: []
  ec_esperado: item_01
  tg_esperado: "item_01=nao_incluido, item_03=nao_incluido, item_05=nao_incluido, item_07=nao_incluido, item_02/06=vazio, item_04/08=vazio"
  chips_esperados: "Espaco=ativo, Enter=Todos(ativo)"
  resultado_a_registrar:

- numero: 2
  tecla_acionada: Espaço
  foco_esperado: item_01
  selecao_esperada: [item_01]
  ec_esperado: item_01
  tg_esperado: item_01=incluido
  chips_esperados: "Espaco=ativo, Enter=Executar(inativo)"
  resultado_a_registrar:

- numero: 3
  tecla_acionada: Seta para baixo
  foco_esperado: item_02
  selecao_esperada: [item_01]
  ec_esperado: item_02
  tg_esperado: "item_01=incluido, item_02=vazio"
  chips_esperados: "Espaco=inativo (item_02 nao selecionavel), Enter=Executar(inativo)"
  resultado_a_registrar:

- numero: 4
  tecla_acionada: Espaço
  foco_esperado: item_02
  selecao_esperada: [item_01]
  ec_esperado: item_02
  tg_esperado: item_02=vazio (sem efeito)
  chips_esperados: "Espaco=inativo, Enter=Executar(inativo)"
  resultado_a_registrar:

- numero: 5
  tecla_acionada: Seta para baixo
  foco_esperado: item_03
  selecao_esperada: [item_01]
  ec_esperado: item_03
  tg_esperado: "item_01=incluido, item_03=nao_incluido"
  chips_esperados: "Espaco=ativo, Enter=Executar(inativo)"
  resultado_a_registrar:

- numero: 6
  tecla_acionada: Espaço
  foco_esperado: item_03
  selecao_esperada: [item_01, item_03]
  ec_esperado: item_03
  tg_esperado: "item_01=incluido, item_03=incluido"
  chips_esperados: "Espaco=ativo, Enter=Executar(inativo)"
  resultado_a_registrar:

- numero: 7
  tecla_acionada: Enter
  foco_esperado: item_03
  selecao_esperada: [item_01, item_03]
  ec_esperado: item_03
  tg_esperado: inalterado
  chips_esperados: "Executar inativo — nenhum efeito, nenhuma execucao"
  resultado_a_registrar:

- numero: 8
  tecla_acionada: Esc (primeiro acionamento)
  foco_esperado: item_03
  selecao_esperada: []
  ec_esperado: item_03
  tg_esperado: "todos vazios/nao_incluido"
  chips_esperados: "Enter=Todos(ativo)"
  resultado_a_registrar:

- numero: 9
  tecla_acionada: Enter
  foco_esperado: item_03
  selecao_esperada: "[item_01, item_03, item_05, item_07] nesta ordem logica"
  ec_esperado: item_03
  tg_esperado: "item_01/03/05/07=incluido"
  chips_esperados: "Enter=Executar(inativo)"
  resultado_a_registrar:

- numero: 10
  tecla_acionada: Esc (novo acionamento)
  foco_esperado: item_03
  selecao_esperada: []
  ec_esperado: item_03
  tg_esperado: "todos vazios/nao_incluido"
  chips_esperados: "Enter=Todos(ativo)"
  resultado_a_registrar:
```

## 12. Relatório da execução

Criar um novo relatório em:

```text
docs/relatorios/IMP-0041-selecao-multipla-estado-comandos-e-apresentacao.md
```

Usar obrigatoriamente:

```text
docs/templates/TEMPLATE_RELATORIO_IMPL.md
```

Regras:

- cada execução material produz seu próprio relatório;
- não sobrescrever relatório anterior;
- registrar somente fatos materiais, alterações, verificações, evidências, achados e bloqueios;
- não copiar código, diff completo, handoff, logs extensos ou metodologia narrativa;
- omitir campos e seções vazios;
- teto normal de 900 palavras;
- evidência separada somente quando indispensável por formato, tamanho ou reutilização direta, sempre em `docs/relatorios/` e referenciada no relatório;
- o relatório não aprova formalmente a implementação.

## 13. Resposta terminal

Retorne somente:

```yaml
status: <STATUS_LITERAL>
relatorio: docs/relatorios/IMP-0041-selecao-multipla-estado-comandos-e-apresentacao.md
artefatos:
  - <somente arquivos criados ou alterados>
bloqueios:
  - <somente quando houver>
proxima_acao: <somente quando objetivamente determinada>
```

Omitir campos vazios. Não copiar o relatório nem acrescentar conclusão narrativa.

## 14. Exceção operacional

Arquivo ou diretório fora da lista nominal da seção 6.1 não pode ser alterado silenciosamente — em particular `config/estilo.json`, cuja necessidade de novo campo de símbolo para `tg` não foi verificada nesta autoria.

Se um item externo for estritamente necessário para cumprir o handoff, preservar testes obrigatórios ou evitar aborto desproporcional:

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

A autorização não permite criar semântica, arquitetura, schema, formato ou política nova.

## 15. Condições de bloqueio

Bloquear quando:

- faltar decisão;
- houver contradição documental;
- for necessário inventar formato ou schema além do já fechado pela ADR-0034;
- diretório novo necessário não estiver autorizado;
- houver risco de sobrescrever entrada real;
- o handoff for inexequível;
- a leitura focal autorizada for insuficiente;
- a paridade geométrica entre `tela/navegacao.py` e `tela/renderizador.py` (coluna `tg`) não puder ser preservada sem alterar arquivo fora da lista nominal.

Se o bloqueio ocorrer antes de qualquer resultado material, não crie relatório. Se já houver leitura, verificação, alteração ou evidência que precise sobreviver ao contexto, crie relatório factual do bloqueio.

## 16. Limite de encerramento

Ao concluir implementação, testes locais, demonstração e relatório, pare.

Não faça QA formal.
Não aprove a própria entrega.
Não prepare nem execute commit.
Não inicie outro ciclo.
