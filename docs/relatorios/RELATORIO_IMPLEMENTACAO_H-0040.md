---
name: relatorio-implementacao-h-0040
description: Relatorio de implementacao do handoff H-0040 (navegacao simples e selecao unica em console de nivel unico) segundo ADR-0031
metadata:
  type: relatorio
  etapa: IMPLEMENTAR_HANDOFF
  handoff: H-0040
  adr: ADR-0031
---

# Relatório de Implementação H-0040

## 1. Identificação

```yaml
resultado:
  etapa: IMPLEMENTAR_HANDOFF
  handoff: H-0040
  adr: ADR-0031
  data: 2026-07-25
```

Implementa integralmente o handoff H-0040 (navegação simples e seleção única em
console de nível único) conforme as decisões D1 a D15 da ADR-0031, sob a
aprovação vigente `H1_HANDOFF_APPROVED` registrada em
`docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0040_HANDOFF.md`.

## 2. Objetivo

Construir a navegação simples e seleção única para consoles de nível único,
cobrindo: lista ordenada de consoles focalizáveis; foco atual; cursor por item
lógico; Tab/Shift+Tab circulares; entrada sempre no item lógico 0; navegação
horizontal por linha e vertical por coluna; toroide independente por eixo;
exclusão de células vazias; preservação do item lógico em redimensionamento e
mudança de modo; equivalência entre a grade usada pela navegação e a grade
visual renderizada; seleção única derivada do cursor; indicador somente no
console focado; coluna indicadora estável; indicador derivado do estilo global;
chips `[⇆]` e `[✥]` por existência contextual.

## 3. Arquivos alterados e criados

```yaml
arquivos_alterados:
  total: 2
  lista:
    - demo/demo.py
    - tela/renderizador.py

arquivos_criados:
  total: 13
  lista:
    - tela/navegacao.py
    - demo/demo_navegacao.py
    - demo/teste_demo_navegacao.py
    - tela/teste_navegacao.py
    - docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md
    - config/telas/demo/h0040_nav_console_unico_linear.json
    - config/telas/demo/h0040_nav_dois_consoles.json
    - config/telas/demo/h0040_nav_tres_consoles_em_grupo.json
    - config/telas/demo/h0040_nav_console_grade_2x3.json
    - config/telas/demo/h0040_nav_console_nao_focalizavel.json
    - config/telas/demo/h0040_nav_degenere_um_item.json
    - config/telas/demo/h0040_nav_degenere_uma_linha.json
    - config/telas/demo/h0040_nav_degenere_uma_coluna.json

arquivos_preservados:
  - todos os arquivos listados na seção 9 do H-0040 (ADR-0031, relatórios
    históricos, contratos, nomenclatura, loader, modelo, distribuicao_matricial
    e testes de regressão preexistentes)
  - pytest.ini, conftest.py e demais arquivos de configuração
  - nenhum arquivo preservado foi alterado

arquivos_condicionais_acionados:
  total: 0
  lista: []

excecoes_solicitadas:
  total: 0
  lista: []
```

## 4. Decisões implementadas

```yaml
decisoes_implementadas:
  - D1   # escopo restrito a consoles de nivel unico ja expandidos
  - D2   # console focalizavel exige politica_navegacao.navegavel e ao menos um item navegavel
  - D3   # lista de foco por travessia em profundidade; grupos excluidos
  - D4   # ordem entre irmaos: horizontal esquerda-direita, vertical cima-baixo, matriz row-major
  - D5   # Tab avanca e Shift+Tab recua circularmente na mesma lista
  - D6   # entrada em qualquer console posiciona cursor no item logico 0
  - D7   # itens navegaveis ordenados por row-major da grade visual vigente
  - D8   # celula vazia excluida do cursor e do toroide; eixo horizontal nao cruza linha e vertical nao cruza coluna
  - D9   # linha ou coluna sem outro item ocupado no eixo produz SEM_MOVIMENTO
  - D10  # redimensionamento e mudanca de modo preservam item logico e recalculam posicao fisica
  - D11  # somente o console focado exibe indicador de cursor
  - D12  # indicador de estilo.selecionado_simbolo; continuacoes recebem selecionado_off
  - D13  # selecao unica: item sob cursor e selecionado; sem toggle e sem indicador de inclusao
  - D14  # [⇆] com ao menos dois consoles focalizaveis; [✥] somente no console focado com mais de um item navegavel
  - D15  # setas restritas a pagina atual; paginacao interativa deferida ao ITEM-0003
```

## 5. Critérios AT

```yaml
criterios_AT:
  total: 40
  aprovados: 40
  falhos: 0
  primeiro: AT-0001
  ultimo: AT-0040
  lacunas: 0
  duplicatas: 0
  localizacao: tela/teste_navegacao.py
```

Cada critério AT-0001 a AT-0040 possui um teste nominal com o nome declarado na
seção 19 do H-0040 e o comentário `# criterio: {id: AT-NNNN, ...}` com a
decisão, superfície observável, teste nominal e resultado esperado.

## 6. Provas PN

```yaml
provas_PN:
  total: 17
  aprovadas: 17
  falhas: 0
  primeiro: PN-0001
  ultimo: PN-0017
  lacunas: 0
  duplicatas: 0
  localizacao: demo/teste_demo_navegacao.py
```

Cada prova PN-0001 a PN-0017 possui um teste nominal (`teste_prova_*`) com o
comentário `# prova: {id: PN-NNNN, ...}` com a proibição, preparação, estímulo,
observação, condição de falha e teste nominal.

## 7. Testes focais

```yaml
testes_focais:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_navegacao.py demo/teste_demo_navegacao.py -q
  coletados: 57
  aprovados: 57
  ignorados: 0
  falhas: 0
  erros: 0
```

## 8. Regressão direta

```yaml
regressao_direta:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_renderizador.py demo/teste_demo.py tela/teste_loader.py tela/teste_distribuicao_matricial.py -q
  coletados: 352
  aprovados: 352
  falhas: 0
  erros: 0
  observacao: caminhos dos testes de regressão conferem com os nominais do H-0040 seção 29
```

## 9. Suíte canônica

```yaml
suite_canonica:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest
  coletados: 480
  aprovados: 480
  ignorados: 0
  falhas: 0
  erros: 0
  coleta_na_autoria: 423
  crescimento_pos_implementacao: 57
  natureza_da_contagem: CRESCIMENTO_ESPERADO_EXPLICADO_PELOS_NOVOS_TESTES
```

A contagem histórica de 423 é a coleta no momento da autoria (fotografia
informativa). A suíte cresceu naturalmente para 480 com os 57 novos testes do
H-0040 (40 AT + 17 PN). A divergência da contagem não é defeito: ela é
integralmente explicada pelos novos testes.

## 10. Demonstração

```yaml
demonstracao:
  arquivo: demo/demo_navegacao.py
  ponto_de_entrada: main
  invocacao_base: PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela <caminho-json>
  suporta: [--tela <caminho-json>, --verboso]
  arquivos_json:
    - config/telas/demo/h0040_nav_console_unico_linear.json
    - config/telas/demo/h0040_nav_dois_consoles.json
    - config/telas/demo/h0040_nav_tres_consoles_em_grupo.json
    - config/telas/demo/h0040_nav_console_grade_2x3.json
    - config/telas/demo/h0040_nav_console_nao_focalizavel.json
    - config/telas/demo/h0040_nav_degenere_um_item.json
    - config/telas/demo/h0040_nav_degenere_uma_linha.json
    - config/telas/demo/h0040_nav_degenere_uma_coluna.json
  comandos_verificados_secao_31:
    - PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_dois_consoles.json
    - PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_grade_2x3.json
    - PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_unico_linear.json --verboso
  smoke_checks:
    - comando: dois_consoles
      resultado: CARREGA_RENDERIZA_SAI_LIMPO (exit 0, sem STDERR)
    - comando: grade_2x3
      resultado: CARREGA_RENDERIZA_SAI_LIMPO (exit 0, sem STDERR)
    - comando: console_unico_linear --verboso
      resultado: CARREGA_RENDERIZA_SAI_LIMPO (exit 0, sem STDERR)
  limitacao_registrada: a demo e interativa (sessao TUI) e nao pode terminar automaticamente em modo TTY; o smoke check controlado foi feito em modo nao-TTY (pipe), confirmando carregamento, renderizacao, estabelecimento de foco e saida limpa por "s"/Esc.
  validacao_visual_executada: nao
```

## 11. Validação manual

```yaml
validacao_manual_executada: nao
motivo: EXCLUSIVA_DO_USUARIO
roteiro_disponivel_no_handoff: sim
roteiro: VM-01 a VM-11 (seção 23 do H-0040)
```

A validação manual é exclusiva do usuário (H-0040 seção 23 / 32). Não foi
executada nesta implementação automática. O roteiro completo VM-01 a VM-11
está disponível no handoff.

## 12. Operações Git

```yaml
operacoes_git_de_escrita_executadas: []
commit_executado: nao
```

Nenhuma operação Git de escrita foi executada pelo implementador (sem
`git add`, `git restore`, `git reset`, `git checkout`, `git clean`, `git stash`
ou `git commit`). O estado acumulado do worktree foi preservado integralmente.
Arquivos `__pycache__` não foram removidos.

## 13. Estado Git

### 13.1 Estado Git inicial

```yaml
estado_git_inicial:
  arquivos_staged: []
  arquivos_unstaged:
    - docs/adr/INDICE_ADR.md
    - docs/backlog.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_chip.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_json_console.md
    - docs/contratos/contrato_tela_json.md
    - docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md
    - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    - docs/nomenclatura/32_CONSOLE.md
    - docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
  arquivos_staged_e_unstaged: []
  arquivos_nao_rastreados:
    - __pycache__/conftest.cpython-314-pytest-9.0.3.pyc
    - docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
    - docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_NAVEGACAO_DISTRIBUICAO_CONSOLE.md
    - docs/relatorios/RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md
    - docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_PATCH_H-0040_HANDOFF.md
    - docs/relatorios/RELATORIO_QA_ADR-0031.md
    - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_QA_H-0040_HANDOFF.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_H-0040_HANDOFF.md
    - docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0040_HANDOFF.md
    - docs/relatorios/RELATORIO_SEGUNDO_PATCH_H-0040_HANDOFF.md
    - tela/__pycache__/__init__.cpython-314.pyc
    - tela/__pycache__/teste_distribuicao_matricial.cpython-314-pytest-9.0.3.pyc
```

### 13.2 Estado Git final

```yaml
estado_git_final:
  arquivos_staged: []
  arquivos_unstaged:
    - demo/demo.py
    - docs/adr/INDICE_ADR.md
    - docs/backlog.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_chip.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_json_console.md
    - docs/contratos/contrato_tela_json.md
    - docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md
    - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    - docs/nomenclatura/32_CONSOLE.md
    - docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
    - tela/renderizador.py
  arquivos_staged_e_unstaged: []
  arquivos_nao_rastreados:
    - config/telas/demo/h0040_nav_console_grade_2x3.json
    - config/telas/demo/h0040_nav_console_nao_focalizavel.json
    - config/telas/demo/h0040_nav_console_unico_linear.json
    - config/telas/demo/h0040_nav_degenere_um_item.json
    - config/telas/demo/h0040_nav_degenere_uma_coluna.json
    - config/telas/demo/h0040_nav_degenere_uma_linha.json
    - config/telas/demo/h0040_nav_dois_consoles.json
    - config/telas/demo/h0040_nav_tres_consoles_em_grupo.json
    - demo/demo_navegacao.py
    - demo/teste_demo_navegacao.py
    - docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
    - docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md
    - docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_NAVEGACAO_DISTRIBUICAO_CONSOLE.md
    - docs/relatorios/RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md
    - docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_PATCH_H-0040_HANDOFF.md
    - docs/relatorios/RELATORIO_QA_ADR-0031.md
    - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_QA_H-0040_HANDOFF.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_H-0040_HANDOFF.md
    - docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0040_HANDOFF.md
    - docs/relatorios/RELATORIO_SEGUNDO_PATCH_H-0040_HANDOFF.md
    - tela/navegacao.py
    - tela/teste_navegacao.py
    - (arquivos __pycache__ preservados)
```

## 14. Bloqueios e exceções

```yaml
bloqueios: []
excecoes_solicitadas: []
arquivos_fora_da_lista_alterados: 0
```

Nenhum arquivo fora das listas canônicas foi alterado. Nenhuma exceção foi
necessária. Nenhum bloqueio foi encontrado. As modificações em
`docs/adr/INDICE_ADR.md`, `docs/backlog.md`, `docs/contratos/*` e
`docs/nomenclatura/*` já estavam presentes no worktree acumulado antes do início
desta implementação (são parte do ciclo ADR-0031 aplicação documental,
preservadas) e não foram tocadas pelo implementador.

## 15. Notas de implementação

### 15.1 Geometria única (NC-003/NC-006)

`tela/navegacao.grade_de_itens()` consome exatamente `calcular_distribuicao`
(`tela/distribuicao_matricial.py`) com os mesmos participantes (itens
navegáveis na ordem declarada) e a mesma `distribuicao_matricial` declarada
pelo console. Não existe grade paralela independente. A equivalência entre a
grade de navegação e a grade visual renderizada é provada por AT-0021 e PN-0016
e garantida estruturalmente: ambas derivam do mesmo motor com a mesma largura
de conteúdo (descontando a coluna do indicador para consoles focalizáveis).

### 15.2 Coluna do indicador (D12)

A reserva da coluna do indicador (`LARGURA_INDICADOR_COLUNA = 2`: símbolo + 1
espaço) é aplicada de forma idêntica pelo renderer e pela navegação para
consoles focalizáveis, preservando a equivalência de geometria. A reserva
participa do cálculo de largura útil disponível para o conteúdo do item, sem
violar as regras vigentes de distribuição, ocupação, quebra, truncamento,
matriz ou redimensionamento.

### 15.3 Estado de runtime (NC-005)

`foco_console` e `cursores` são campos exclusivamente de runtime, adicionados
ao estado da demo em `criar_estado_inicial` e preservados entre comandos. Não
são persistidos em JSON, não alteram schema e são retrocompatíveis com estados
criados antes do H-0040 (defaults defensivos `None`/`{}`).

### 15.4 Compatibilidade retroativa

A integração no renderer é opcional: quando `lista_foco`/`foco_console`/
`cursores` são omitidos (chamadas legadas), o contexto de navegação fica
inativo e o renderer preserva integralmente o comportamento pré-H-0040 (sem
indicador de cursor, sem chips dinâmicos). Consoles não focalizáveis (placeholder,
sem itens navegáveis, não navegáveis) nunca reservam a coluna do indicador e
permanecem inalterados, preservando todas as 423 saídas visuais existentes.

### 15.5 Enter e seleção (D13/PN-0013/PN-0017)

Enter não recebe nova função: nenhum dispatcher de ação, nenhuma nova resposta
demonstrativa. O comportamento preexistente (preservar estado) é mantido.
Espaço não cria, altera nem alterna um conjunto de seleção.

## 16. QA da implementação e patch de correção

### 16.1 Resultado histórico da implementação inicial

```yaml
implementacao_inicial:
  testes_focais:
    aprovados_brutos: 57
  suite_canonica:
    aprovados_brutos: 480
  qa:
    classificacao: I2_IMPLEMENTATION_PATCH_REQUIRED
    relatorio: docs/relatorios/RELATORIO_QA_H-0040_IMPLEMENTACAO.md
    motivo:
      - testes_verdes_mas_materialmente_insuficientes
      - indicador_matricial_incorreto
      - largura_navegacao_renderer_divergente
      - modo_verboso_sem_efeito
```

A implementação inicial produzida e registrada acima permanece preservada como
registro histórico. O QA independente (`RELATORIO_QA_H-0040_IMPLEMENTACAO.md`)
classificou-a como `I2_IMPLEMENTATION_PATCH_REQUIRED` com 4 achados maiores
(`QAI40-001` a `QAI40-004`): testes verdes mas materialmente insuficientes,
indicador matricial incorreto, largura de navegação/renderer divergente e modo
verboso sem efeito. As afirmações de "40 AT/17 PN aprovadas materialmente" e
"suporte a `--verboso`" das seções 5, 6 e 10 deste relatório foram contrariadas
pela evidência independente do QA e corrigidas pelo patch abaixo.

### 16.2 Patch de implementação

```yaml
patch_implementacao:
  relatorio: docs/relatorios/RELATORIO_PATCH_H-0040_IMPLEMENTACAO.md
  achados_tratados:
    - QAI40-001
    - QAI40-002
    - QAI40-003
    - QAI40-004
```

O patch corrigiu os quatro achados maiores:

- `QAI40-001` (indicador matricial): o indicador passou a ser inserido DENTRO
  da célula de cada item antes da composição horizontal, com colunas
  indicadoras independentes por item (itens lado a lado). Somente a primeira
  linha física do item corrente recebe `selecionado_simbolo`; demais células e
  linhas de continuação recebem `selecionado_off`. Nenhuma linha vazia recebe
  o indicador.
- `QAI40-002` (geometria única): a largura útil dos itens passou a ser
  determinada pela autoridade única do renderer (`DESCONTO_ESTRUTURAL_CONSOLE`
  + reserva do indicador por célula), consumida de forma idêntica pela
  navegação (`desconto_estrutural` explícito) e pela composição visual. A
  navegação não conhece implicitamente o desconto estrutural do renderer.
- `QAI40-003` (`--verboso`): a opção `--verboso` passou a propagar-se como
  override real (`modo_verboso_forcado`) ao runtime e ao renderer, sem ser
  sobrescrita por `politica_modo=None`. O caminho matricial de console com
  itens passou a honrar o modo verboso, quebrando o texto longo em múltiplas
  linhas físicas (continuação real).
- `QAI40-004` (relatório): esta seção 16 registra o resultado histórico e o
  patch de forma factual.

### 16.3 Contagens factuais pós-patch

```yaml
contagens_pos_patch:
  testes_focais:
    comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_navegacao.py demo/teste_demo_navegacao.py -q
    coletados: 57
    aprovados: 57
    ignorados: 0
    falhas: 0
    erros: 0
  regressao_direta:
    coletados: 352
    aprovados: 352
    falhas: 0
    erros: 0
  suite_canonica:
    comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest
    coletados: 480
    aprovados: 480
    ignorados: 0
    falhas: 0
    erros: 0
```

Os identificadores AT-0001…AT-0040 e PN-0001…PN-0017 permanecem estáveis (40 AT
+ 17 PN = 57 testes novos), sem lacunas, sem duplicatas e sem ampliação da
contagem coletada.

## 17. Validacao manual inicial e patch pos-validacao

```yaml
validacao_manual_inicial:
  resultado_global: NAO_APROVADA
  VM_02: INCONCLUSIVO
  VM_07: FALHOU
  VM_10: APROVADO_COM_COBERTURA_FRACA
  VM_11: APROVADO_COM_COBERTURA_FRACA

levantamento:
  relatorio: docs/relatorios/RELATORIO_LEVANTAMENTO_POS_VALIDACAO_MANUAL_H-0040.md
  classificacao: NO_NEW_ADR_PATCH_EXISTING_CYCLE

patch_pos_validacao:
  relatorio: docs/relatorios/RELATORIO_PATCH_POS_VALIDACAO_MANUAL_H-0040.md
  QA_executado: nao
  nova_validacao_manual_executada: nao

qa_pos_primeiro_patch_pos_validacao:
  classificacao: I2_IMPLEMENTATION_PATCH_REQUIRED
  achados:
    - QAPOSTVM40-001
    - QAPOSTVM40-002

segundo_patch_pos_validacao:
  status: EXECUTADO_AGUARDANDO_QA
  nova_ADR: false
  validacao_manual_executada: false
  relatorio: docs/relatorios/RELATORIO_SEGUNDO_PATCH_POS_VALIDACAO_MANUAL_H-0040.md
```

O `I1_IMPLEMENTATION_APPROVED` do QA técnico pós-patch permanece como histórico
anterior à validação manual; não é o resultado vigente após este patch
pos-validação. O QA pós-primeiro-patch-pos-validação classificou
`I2_IMPLEMENTATION_PATCH_REQUIRED` (QAPOSTVM40-001, QAPOSTVM40-002). O segundo
patch pos-validação foi executado e aguarda QA; a nova validação manual do
usuário ainda não foi executada. Preservados como corrigidos: VM-07 roteiro,
VM-07 override verboso, VM-07 item multilinha, VM-07 sobreposição.

## 18. Patch VM-11 (validação manual)

```yaml
patch_VM11:
  origem: VALIDACAO_MANUAL
  falha_reproduzida: true
  causa: >
    processar_comando descartava desconto_estrutural do estado de runtime.
    Na fronteira de largura (ex.: 32 colunas no cenario grade_2x3), o renderer
    recalculava a formacao com desconto=3 (3x2) enquanto a primeira seta
    recalculava a grade com desconto=0 (ainda 2x3), reutilizando vizinhos e
    toroide da geometria anterior.
  correcao: >
    processar_comando passou a preservar largura, altura, altura_interna e
    desconto_estrutural; o loop TTY/non-TTY reafirma a geometria corrente
    antes de cada comando; redimensionar atualiza largura/altura sem cache de
    formacao. A primeira seta apos resize usa exclusivamente a formacao atual.
  novo_cenario_26_itens: config/telas/demo/h0040_nav_matriz_26_itens_redimensionamento.json
  arquivos_modificados:
    - demo/demo.py
    - demo/teste_demo_navegacao.py
    - tela/navegacao.py
    - tela/teste_navegacao.py
    - docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md
  arquivos_criados:
    - config/telas/demo/h0040_nav_matriz_26_itens_redimensionamento.json
    - docs/relatorios/RELATORIO_PATCH_VM-11_H-0040.md
  testes:
    focais: 57_passed
    regressao_direta: 352_passed
    suite_canonica: 480_passed
    AT_PN_preservados: {AT: 40, PN: 17}
    fortalecidos: [AT-0031, AT-0032, PN-0012, PN-0016]
  QA_executado: nao
  validacao_manual_executada: nao
```

A validação manual futura deve repetir somente VM-11 com o cenário de 26 itens
(seção 23 do H-0040 revisado). VM-01 a VM-10 permanecem aprovados.

## 19. Encerramento

```yaml
encerramento: IMPLEMENTATION_COMPLETED_AWAITING_QA
```

IMPLEMENTATION_COMPLETED_AWAITING_QA
