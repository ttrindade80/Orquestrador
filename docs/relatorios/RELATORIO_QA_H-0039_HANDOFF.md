---
name: relatorio-qa-h-0039-handoff
description: Auditoria independente do handoff H-0039, sem alteracao do artefato auditado
metadata:
  type: relatorio
  etapa: QA_HANDOFF
  handoff_auditado: H-0039
  data: "2026-07-22"
---

# Relatorio QA - H-0039 Handoff

## 1. Gate minimo

```yaml
arquivo_correto: true
etapa_correta: QA_HANDOFF
handoff_auditado: H-0039
arquivo_handoff: docs/handoff/H-0039-carregamento-global-materializacao-estilo.md
arquivo_relatorio: docs/relatorios/RELATORIO_QA_H-0039_HANDOFF.md
hash_inicial: 6445892c48fc8fcd75bb96ae1c0a1b38dc7c385d47290b82c20c4fe55e8e4b7e
hash_final: 6445892c48fc8fcd75bb96ae1c0a1b38dc7c385d47290b82c20c4fe55e8e4b7e
handoff_alterado_durante_QA: false

status_handoff_declarado: HANDOFF_CRIADO_AGUARDANDO_QA
encerramento_handoff: HANDOFF_CREATED_AWAITING_QA

status_literal: H2_HANDOFF_PATCH_REQUIRED
status_normalizado: H2
proxima_categoria: PATCH_HANDOFF
```

## 2. Versao auditada

Comandos executados antes da analise:

```yaml
versao_auditada:
  caminho: docs/handoff/H-0039-carregamento-global-materializacao-estilo.md
  sha256: 6445892c48fc8fcd75bb96ae1c0a1b38dc7c385d47290b82c20c4fe55e8e4b7e
  quantidade_de_linhas: 1011
  tamanho_em_bytes: 45326
  data_de_modificacao: "2026-07-22 13:13:39.520184533 -0300"
```

Hash final conferido ao fim: igual ao inicial.

## 3. Autoridades lidas

```yaml
autoridades_lidas:
  handoff:
    - docs/handoff/H-0039-carregamento-global-materializacao-estilo.md
  normativas:
    - docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
    - docs/contratos/contrato_estilo.md
    - docs/contratos/contrato_chip.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_console.md
    - docs/nomenclatura/10_ESTILO.md
    - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    - docs/nomenclatura/32_CONSOLE.md
  historicas:
    - docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0030.md
    - docs/relatorios/RELATORIO_CORRECAO_QA_APLICACAO_ADR-0030.md
  codigo_e_testes:
    - config/estilo.json
    - tela/loader.py
    - tela/renderizador.py
    - tela/teste_loader.py
    - tela/teste_renderizador.py
    - demo/demo.py
    - demo/teste_demo.py
    - demo/teste_demo_console_modos.py
    - demo/demo_distribuicao.py
```

## 4. Estado Git

```yaml
raiz: /home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador
git_log_1: "2caf036 test: adota pytest como padrao unico"
stage_inicial: vazio
diff_check_inicial: passou
diff_cached_check_inicial: passou
diff_name_only_inicial:
  - docs/adr/INDICE_ADR.md
  - docs/contratos/contrato_estilo.md
  - docs/nomenclatura/10_ESTILO.md
diff_stat_inicial: "3 files changed, 210 insertions(+), 12 deletions(-)"
arquivos_untracked_relevantes:
  - docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
  - docs/handoff/H-0039-carregamento-global-materializacao-estilo.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0030.md
  - docs/relatorios/RELATORIO_CORRECAO_ENCERRAMENTO_QA_POS_PATCH_02_ADR-0030.md
  - docs/relatorios/RELATORIO_CORRECAO_QA_APLICACAO_ADR-0030.md
  - docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md
  - docs/relatorios/RELATORIO_PATCH_02_ADR-0030.md
  - docs/relatorios/RELATORIO_PATCH_ADR-0030.md
  - docs/relatorios/RELATORIO_QA_ADR-0030.md
  - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0030.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_02_ADR-0030.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0030.md
observacao: >
  H-0039 existe como artefato nao rastreado. Os demais arquivos nao
  rastreados/modificados pertencem ao ciclo documental ADR-0030 preexistente
  e foram registrados sem atribuir sua criacao ao H-0039.
arquivos_alterados_pelo_QA:
  - docs/relatorios/RELATORIO_QA_H-0039_HANDOFF.md
stage_final: vazio
```

## 5. Identificacao e numeracao

```yaml
numero: conforme
titulo: conforme
adr_base: conforme
bloco: 1
estado_inicial: BASE_DOCUMENTAL_APROVADA
estado_final_esperado: HANDOFF_CRIADO_AGUARDANDO_QA
ultima_linha: HANDOFF_CREATED_AWAITING_QA
sem_reserva_de_numero: true
sem_sufixo: true
nao_se_declara_aprovado: true
nao_declara_implementacao_executada: true
nao_mistura_blocos_2_ou_3: true
```

## 6. Matriz D1-D13

| Decisao | Exigencia da ADR | Tratamento no H-0039 | Resultado |
|---|---|---|---|
| D1 | `config/estilo.json` como autoridade global exclusiva | Declara objetivo, proibe renderer abrir/decidir preset/fallback e remove hardcodings | COBERTA |
| D2 | Catalogo + `preset_default` | Exige `preset_default` em `borda` e `chip`; preserva defaults de indicadores | COBERTA |
| D3 | Carregamento integral das secoes vigentes | Mapeia borda, chip, concluido, selecionado e incluido para runtime | COBERTA |
| D4 | Preset ativo `"Borda Curva"` | Exige adicionar default e preservar sete caracteres | COBERTA |
| D5 | Preset `"Colchete"` com `caixa_alta: false` | Exige default, colchetes, cores `"padrão"` e `caixa_alta: false` | COBERTA |
| D6 | Indicador selecionado `"Seta"` | Preserva default e materializa `selecionado_simbolo`/`selecionado_off` | COBERTA |
| D7 | Indicador incluido `"Círculo"` | Preserva default e materializa `incluido_on`/`incluido_off` | COBERTA |
| D8 | Carregamento unico, validacao, materializacao e entrega aos consumidores | Define `carregar_estilo`, `EstiloResolvido`, chamada uma vez no ponto de entrada | COBERTA |
| D9 | Validacoes obrigatorias, sem fallback, sem estilo parcial | Lista V-01 a V-29, `EstiloErro`, ausencia de fallback e limite de duplicidade raw | COBERTA |
| D10 | Consumidores recebem representacao resolvida | Renderer recebe `estilo` e nao escolhe presets | COBERTA |
| D11 | Edicao centralizada em categorias existentes | Mantem config como fonte e nao cria presets concorrentes | COBERTA_POR_REFERENCIA |
| D12 | Tela futura de estilo deferida | Exclui tela, persistencia e troca durante sessao | PRESERVADA_COMO_DEFERIMENTO |
| D13 | Blocos 2 e 3 fora do escopo | Exclui navegacao, selecao unica e selecao multipla | PRESERVADA_COMO_DEFERIMENTO |

## 7. Estado inicial tecnico

```yaml
estado_inicial_confirmado:
  config_estilo:
    _meta.status: rascunho_inicial
    borda.preset_default: ausente
    chip.preset_default: ausente
    chip.presets.Colchete.caixa_alta: true
    selecionado.preset_default: "Seta"
    incluido.preset_default: "Círculo"
  runtime:
    loader_de_estilo_ativo: ausente
    estilo_resolvido: ausente
  renderer:
    _BORDAS: existente
    tipo_borda: existente
    formato_de_chip_hardcoded: existente
  baseline_pytest:
    esperado: 422
    observado: "422 passed"
```

## 8. Representacao runtime

```yaml
representacao_runtime:
  borda:
    campos: [canto_superior_esquerdo, canto_superior_direito, canto_inferior_esquerdo, canto_inferior_direito, traco_superior, traco_inferior, lateral]
    resultado: COBERTA
  chip:
    campos: [caractere_esquerdo, caractere_direito, cor_texto, caixa_alta, cor_fundo]
    resultado: COBERTA
  indicadores:
    campos: [concluido_on, concluido_off, selecionado_simbolo, selecionado_off, incluido_on, incluido_off]
    resultado: COBERTA
  campos_comportamentais_de_navegacao_misturados: false
  validavel_isoladamente: true
  renderer_recebe_valores_resolvidos: true
  renderer_escolhe_presets: false
```

## 9. Validacoes

| Condicao invalida | Criterio no handoff | Teste exigido | Resultado |
|---|---|---|---|
| arquivo ausente | V-01, `EstiloErro` | sim | COBERTA |
| JSON invalido | V-02, `EstiloErro` | sim | COBERTA |
| secao obrigatoria ausente | V-03 a V-05 | sim | COBERTA |
| `preset_default` ausente | V-06 a V-09 | sim | COBERTA |
| catalogo obrigatorio vazio | V-10 a V-13 | sim | COBERTA |
| preset inexistente | V-14 a V-17, sem fallback | sim | COBERTA |
| campo obrigatorio ausente | V-18 a V-23 | sim | COBERTA |
| tipo invalido | V-24 a V-26 | sim | COBERTA |
| simbolo vazio | V-28 | sim | COBERTA |
| regra de comprimento | V-27, `len() != 1` | sim | COBERTA |
| duplicidade observavel | declara limite: raw JSON nao exigido; materializada impossivel em `dict` | registrar limite | COBERTA |
| ausencia de fallback | V-14 a V-17 e CA-S3 | sim | COBERTA |
| estilo parcial | V-29 e CA-L18 | sim | COBERTA |

Unidade de caractere: o handoff reconhece R-6 e escolhe `len(s) == 1` como mecanismo tecnico executavel; declara limite de code points versus largura visual, sem criar politica geral de Unicode. Resultado: COBERTA.

## 10. Inventario de consumidores

Buscas executadas:

```bash
rg -n --glob '*.py' 'renderizar_tela\s*\(' .
rg -n --glob '*.py' 'tipo_borda' .
rg -n --glob '*.py' '_BORDAS' .
rg -n --glob '*.py' '\[\{tecla\}\]' .
rg -n --glob '*.py' 'carregar_tela\s*\(' .
rg -n --glob '*.py' 'selecionado_simbolo|selecionado_off|incluido_on|incluido_off|concluido_on|concluido_off' .
find demo tela -maxdepth 2 -type f -name '*.py' -print
rg -n --glob '*.py' '"b"|tipo_borda|Borda Curva|Borda Reta' demo tela
```

```yaml
inventario_consumidores:
  - arquivo: tela/renderizador.py
    linha_ou_simbolo: "renderizar_tela, _BORDAS, _texto_chip_barra"
    mudanca_necessaria: "trocar tipo_borda por estilo e consumir campos resolvidos"
    autorizado_nominalmente_no_handoff: true
    classificacao: AUTORIZADO_E_OBRIGATORIO
  - arquivo: tela/teste_renderizador.py
    linha_ou_simbolo: "varias chamadas com e sem tipo_borda; imports de _BORDAS"
    mudanca_necessaria: "atualizar todos os testes para assinatura com estilo"
    autorizado_nominalmente_no_handoff: true
    classificacao: AUTORIZADO_E_OBRIGATORIO
  - arquivo: tela/loader.py
    linha_ou_simbolo: "novo carregar_estilo / EstiloResolvido"
    mudanca_necessaria: "implementar loader de estilo"
    autorizado_nominalmente_no_handoff: true
    classificacao: AUTORIZADO_E_OBRIGATORIO
  - arquivo: tela/teste_loader.py
    linha_ou_simbolo: "novos testes de estilo"
    mudanca_necessaria: "testes positivos e negativos do loader"
    autorizado_nominalmente_no_handoff: true
    classificacao: AUTORIZADO_E_OBRIGATORIO
  - arquivo: demo/demo.py
    linha_ou_simbolo: "estado tipo_borda; comando b; renderizar_estado"
    mudanca_necessaria: "carregar estilo, remover tipo_borda/b e passar estilo"
    autorizado_nominalmente_no_handoff: true
    classificacao: AUTORIZADO_E_OBRIGATORIO
  - arquivo: demo/teste_demo.py
    linha_ou_simbolo: "testes de tipo_borda e renderizar_tela"
    mudanca_necessaria: "remover/adaptar expectativas de borda e passar estilo"
    autorizado_nominalmente_no_handoff: true
    classificacao: AUTORIZADO_E_OBRIGATORIO
  - arquivo: demo/teste_demo_console_modos.py
    linha_ou_simbolo: "tipo_borda no estado e chamadas diretas"
    mudanca_necessaria: "remover expectativas de tipo_borda e passar estilo"
    autorizado_nominalmente_no_handoff: true
    classificacao: AUTORIZADO_E_OBRIGATORIO
  - arquivo: demo/demo_distribuicao.py
    linha_ou_simbolo: "estado tipo_borda; comando b; chamadas diretas"
    mudanca_necessaria: "carregar/passar estilo e remover alternancia"
    autorizado_nominalmente_no_handoff: true
    classificacao: AUTORIZADO_E_OBRIGATORIO
  - arquivo: demo/diagnostico.py
    linha_ou_simbolo: "renderizar_tela(modelo)"
    mudanca_necessaria: "carregar/passar EstiloResolvido ou adaptar helper conforme assinatura final"
    autorizado_nominalmente_no_handoff: false
    classificacao: OMITIDO
  - arquivo: demo/teste_diagnostico.py
    linha_ou_simbolo: "renderizar_tela(... largura/altura) em linhas 364, 435, 458"
    mudanca_necessaria: "atualizar chamadas/expectativas para novo parametro estilo"
    autorizado_nominalmente_no_handoff: false
    classificacao: OMITIDO
  - arquivo: demo/teste_demo_console.py
    linha_ou_simbolo: "renderizar_tela(... largura/altura) em linhas 199, 210, 221, 233"
    mudanca_necessaria: "passar estilo obrigatorio apos nova assinatura"
    autorizado_nominalmente_no_handoff: false
    classificacao: OMITIDO
```

`rg` nao encontrou campos materializados (`selecionado_simbolo`, `incluido_on`, etc.) no codigo atual.

## 11. Lista nominal

```yaml
lista_nominal:
  nucleo_minimo:
    config/estilo.json: AUTORIZADO_E_OBRIGATORIO
    tela/loader.py: AUTORIZADO_E_OBRIGATORIO
    tela/renderizador.py: AUTORIZADO_E_OBRIGATORIO
    tela/teste_loader.py: AUTORIZADO_E_OBRIGATORIO
    tela/teste_renderizador.py: AUTORIZADO_E_OBRIGATORIO
  adicionais_declarados:
    demo/demo.py: AUTORIZADO_E_OBRIGATORIO
    demo/teste_demo.py: AUTORIZADO_E_OBRIGATORIO
    demo/teste_demo_console_modos.py: AUTORIZADO_E_OBRIGATORIO
    demo/demo_distribuicao.py: AUTORIZADO_E_OBRIGATORIO
  relatorio_implementacao:
    docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0039_CARREGAMENTO_ESTILO.md: AUTORIZADO_E_OBRIGATORIO
  arquivos_omitidos:
    - demo/diagnostico.py
    - demo/teste_diagnostico.py
    - demo/teste_demo_console.py
```

A palavra "condicionais" nos quatro arquivos de `demo/` declarados nao bloqueia a edicao: o proprio handoff afirma que eles foram incluidos porque a necessidade ja foi confirmada. O defeito esta nos consumidores omitidos, nao nessa classificacao.

## 12. Escopo negativo e consistencia

```yaml
escopo_negativo:
  navegacao_por_setas: excluida
  cursor_movel: excluido
  selecao_unica: excluida
  selecao_multipla: excluida
  toggle_por_espaco: excluido
  enter_como_execucao: excluido
  registry_de_acoes: excluido
  chips_novos_como_comportamento: excluido
  reordenacao_de_chips: excluida
  tela_de_escolha_de_estilo: excluida
  persistencia_de_escolha: excluida
  troca_de_estilo_durante_sessao: excluida
  alteracao_de_meta_status: excluida
  cor_inativo_cor_alerta_tiling: deferidos
  blocos_2_e_3: excluidos
contradicoes_internas:
  - "A assinatura proposta exige estilo obrigatorio, mas a lista nominal cobre principalmente chamadores com tipo_borda e omite chamadores sem tipo_borda."
```

## 13. Testes, demonstracao e validacao manual

```yaml
testes:
  positivos_loader: exigidos
  materializacao_completa: exigida
  negativos_validacoes: exigidos
  ausencia_de_fallback: exigida
  estilo_nao_parcial: exigido
  consumo_borda_renderer: exigido
  consumo_cinco_campos_chip: exigido
  caixa_alta_false: exigido
  remocao_BORDAS: exigida
  remocao_tipo_borda: exigida
  atualizacao_testes_demo: parcialmente_exigida_com_omissoes
  regressao_telas_existentes: exigida
  descoberta_pytest: exigida
  preservacao_testes_anteriores: exigida
  gate_canonico: "PYTHONDONTWRITEBYTECODE=1 python -m pytest"
demonstracao:
  ponto_de_entrada: demo/demo.py
  comando: "python demo/demo.py"
  cenario: config/telas/demo/demo.json
  borda_e_chips_expostos: true
  redimensionamento_maximizar_restaurar_reduzir: previsto
  capitalizacao_bordas_colchetes: previsto
validacao_manual:
  exclusiva_do_usuario: true
  status_exigido: VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

Resultado: testes e demonstracao estao em geral cobertos, mas a atualizacao de testes de demo esta incompleta por omissao de consumidores.

## 14. Relatorio da implementacao futura

```yaml
relatorio_futuro_exigido: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0039_CARREGAMENTO_ESTILO.md
conteudo_previsto:
  estado_inicial: sim
  decisoes_tecnicas: sim
  arquivos_alterados: sim
  configuracao_migrada: sim
  representacao_produzida: sim
  hardcodings_removidos: sim
  chamadas_migradas: sim
  testes: sim
  suite_focal: sim
  suite_canonica: sim
  demonstracao: sim
  validacao_manual_pendente: sim
  arquivos_fora_da_lista_autorizados: sim
  stage_vazio: sim
  encerramento: sim
```

## 15. Achados

```yaml
achados:
  - id: QA-H0039-001
    severidade: alta
    tema: lista_nominal_incompleta
    arquivo_ou_secao: "H-0039 secoes 7.4, 14.2, 18.4 CA-T7"
    evidencia: >
      O handoff substitui a assinatura por renderizar_tela(modelo, estilo,
      largura, altura, verboso), mas autoriza nominalmente apenas os
      consumidores com tipo_borda em demo/demo.py, demo/teste_demo.py,
      demo/teste_demo_console_modos.py e demo/demo_distribuicao.py. A busca
      material encontrou chamadas diretas sem tipo_borda em demo/diagnostico.py,
      demo/teste_diagnostico.py e demo/teste_demo_console.py que tambem
      quebrariam quando estilo se torna argumento obrigatorio.
    autoridade: "ADR-0030 D8/D10; contrato_estilo.md R-1/R-10; H-0039 assinatura final"
    impacto: >
      O executor nao teria autorizacao nominal inequívoca para alterar todos
      os consumidores necessarios; a implementacao completa exigiria parar
      para autorizacao ou deixaria a suite quebrada.
    correcao_necessaria: >
      Patch do handoff para incluir esses arquivos, ou ajustar explicitamente
      a estrategia de compatibilidade se `estilo` nao for obrigatorio em todos
      os chamadores.
    decisao_do_usuario_necessaria: false
    classificacao_H_sugerida: H2_HANDOFF_PATCH_REQUIRED
```

```yaml
achados_por_severidade:
  bloqueante: 0
  alta: 1
  media: 0
  baixa: 0
  observacao: 0
bloqueios: []
arquivos_omitidos:
  - demo/diagnostico.py
  - demo/teste_diagnostico.py
  - demo/teste_demo_console.py
```

## 16. Checks finais

```yaml
pytest:
  comando: "PYTHONDONTWRITEBYTECODE=1 python -m pytest"
  codigo_saida: 0
  contagem: "422 passed"
  resumo: "collected 422 items; 422 passed in 16.66s"
diff_check_final:
  comando: git diff --check
  codigo_saida: 0
  resumo: sem_saida
diff_cached_check_final:
  comando: git diff --cached --check
  codigo_saida: 0
  resumo: sem_saida
sha256_final:
  comando: "sha256sum docs/handoff/H-0039-carregamento-global-materializacao-estilo.md"
  valor: 6445892c48fc8fcd75bb96ae1c0a1b38dc7c385d47290b82c20c4fe55e8e4b7e
comparacao_hash: igual
estado_git:
  stage: vazio
  unico_arquivo_criado_pelo_QA: docs/relatorios/RELATORIO_QA_H-0039_HANDOFF.md
```

## 17. Classificacao final

O handoff e fiel a ADR-0030 nas decisoes centrais e e tecnicamente especifico o bastante para implementar loader, representacao resolvida, validacoes e migracao do renderer. Entretanto, a lista nominal de arquivos esta incompleta diante da nova assinatura obrigatoria de `renderizar_tela`, omitindo consumidores reais em `demo/`.

Classificacao: `H2_HANDOFF_PATCH_REQUIRED`

Proxima categoria: `PATCH_HANDOFF`

H2_HANDOFF_PATCH_REQUIRED
