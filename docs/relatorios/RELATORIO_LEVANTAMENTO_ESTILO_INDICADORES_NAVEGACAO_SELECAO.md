---
name: relatorio-levantamento-estilo-indicadores-navegacao-selecao
description: Levantamento documental e arquitetural sobre estilo, indicadores, navegacao e selecao do console
metadata:
  type: relatorio
  etapa: LEVANTAMENTO_DOCUMENTAL_OU_ARQUITETURAL
  escopo: complementacao_materializacao_relatorio
  status: concluido
---

# Relatorio de levantamento - estilo, indicadores, navegacao e selecao

## 1. Identificacao da etapa

```yaml
etapa: LEVANTAMENTO_DOCUMENTAL_OU_ARQUITETURAL
tipo: complementacao_da_entrega_anterior
acao_executada: materializacao_do_relatorio_obrigatorio_em_arquivo
arquivo_criado: docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md
```

## 2. Objetivo e limites

Objetivo exclusivo: registrar em arquivo os fatos ja levantados sobre
`config/estilo.json`, indicadores de cursor/selecao, materializacao para
runtime e consumo pelo renderer.

Limites aplicados:

- nao repetir investigacao integral;
- nao alterar conclusoes da entrega anterior;
- nao fazer QA da propria entrega;
- nao alterar codigo, configuracao, contratos, nomenclatura, ADRs, handoffs ou testes;
- nao preparar stage, commit ou push;
- nao iniciar etapa seguinte;
- reabrir somente arquivos ja inspecionados para registrar caminho, linha,
  funcao ou trecho exato.

## 3. Raiz real do repositorio

Comando usado:

```bash
git rev-parse --show-toplevel
```

Saida:

```text
/home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador
```

Todos os caminhos abaixo sao relativos a essa raiz.

## 4. Autoridades consultadas

Autoridades terminologicas e contratuais consultadas na execucao anterior e
reabertas seletivamente quando necessario:

- `docs/nomenclatura/00_INDICE.md`
- `docs/nomenclatura/01_NUCLEO_COMUM.md`
- `docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md`
- `docs/nomenclatura/10_ESTILO.md`
- `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`
- `docs/nomenclatura/32_CONSOLE.md`
- `docs/contratos/contrato_estilo.md`
- `docs/contratos/contrato_console.md`
- `docs/contratos/contrato_chip.md`
- `docs/contratos/contrato_barra_de_menus.md`

Evidencias materiais usadas neste relatorio:

- `docs/nomenclatura/32_CONSOLE.md:63`: `Cursor / selecionado` aponta um item e usa indicador `→`.
- `docs/nomenclatura/32_CONSOLE.md:65`: `Selecao` e conjunto nomeado, via `[␣]`, indicador `●`/`○`.
- `docs/nomenclatura/32_CONSOLE.md:97-98`: `ec` recebe `selecionado`; `tg` recebe `incluido`.
- `docs/contratos/contrato_estilo.md:134-147`: `selecionado` e `incluido` como indicadores com presets.
- `docs/contratos/contrato_estilo.md:149-174`: transformacao contratual esperada de presets para campos planos de runtime.

## 5. Arquivos tecnicos inspecionados

Arquivos tecnicos inspecionados nominalmente:

- `config/estilo.json`
- `config/elementos/barra_de_menus.json`
- `config/layouts/layout_console.json`
- `config/layouts/layout_dado.json`
- `tela/loader.py`
- `tela/modelo.py`
- `tela/renderizador.py`
- `tela/teste_loader.py`
- `tela/teste_modelo.py`
- `tela/teste_renderizador.py`
- `demo/demo.py`
- `demo/teste_demo.py`
- `demo/teste_diagnostico.py`
- `demo/teste_demo_console.py`
- `demo/teste_demo_console_modos.py`
- `demo/teste_explorar_barra_de_menus.py`

## 6. Estrutura atual de `config/estilo.json`

`config/estilo.json` declara uma biblioteca global de aparencia com `_meta`,
`borda`, `chip` e `indicadores`.

Estrutura observada:

- `_meta`: identifica o arquivo como `estilo`, declara status
  `rascunho_inicial` e registra pendencias de `cor_inativo`, `cor_alerta` e
  `tiling` em `config/estilo.json:2-12`.
- `borda.presets`: catalogo de presets em `config/estilo.json:13-42`.
- `chip.presets`: catalogo de presets em `config/estilo.json:44-95`.
- `indicadores.concluido`: par direto `on`/`off` em `config/estilo.json:98-100`.
- `indicadores.selecionado`: `off`, `preset_default` e `presets` em
  `config/estilo.json:102-110`.
- `indicadores.incluido`: `preset_default` e `presets` em
  `config/estilo.json:112-119`.

Distincoes:

```yaml
catalogo_de_opcoes:
  borda: config/estilo.json:14-42
  chip: config/estilo.json:45-95
  selecionado: config/estilo.json:105-110
  incluido: config/estilo.json:114-119
opcao_ativa_default:
  borda: ausente_em_config_estilo_json
  chip: ausente_em_config_estilo_json
  selecionado: config/estilo.json:104
  incluido: config/estilo.json:113
estrutura_persistida:
  fonte: config/estilo.json
campos_materializados_em_runtime:
  previsto_em_contrato: docs/contratos/contrato_estilo.md:159-170
  implementado_em_codigo: NAO_CONFIRMADO_COMO_EXISTENTE
estado_vivo_de_execucao:
  borda_demo: demo/demo.py usa estado tipo_borda, conforme levantamento anterior
  cursor_selecao_foco: tela/modelo.py:14-15 declara que o modelo nao cria esse estado
```

## 7. Comparacao entre bordas, chips e indicadores

```yaml
borda:
  catalogo: SIM
  caminho: config/estilo.json:13-42
  preset_default_persistido_no_json: NAO
  escolha_ativa_observada_no_runtime_atual: tipo_borda em renderizar_tela
  evidencia_runtime: tela/renderizador.py:2388-2477
  hardcoding_material: tela/renderizador.py:153-164

chip:
  catalogo: SIM
  caminho: config/estilo.json:44-95
  preset_default_persistido_no_json: NAO
  consumo_do_catalogo_pelo_renderer: NAO_CONFIRMADO
  evidencia_consumo_atual: tela/renderizador.py:1140-1144 monta "[{tecla}]"

indicadores:
  concluido:
    estrutura: par_direto_on_off
    caminho: config/estilo.json:98-100
    presets: NAO
  selecionado:
    estrutura: off_mais_preset_default_mais_presets
    caminho: config/estilo.json:102-110
    preset_default: Seta
  incluido:
    estrutura: preset_default_mais_presets
    caminho: config/estilo.json:112-119
    preset_default: Circulo
```

Conclusao desta comparacao: nem todos seguem o mesmo padrao. Bordas e chips
possuem catalogo, mas nao possuem opcao ativa persistida em `config/estilo.json`.
`selecionado` e `incluido` possuem catalogo e opcao ativa por
`preset_default`. `concluido` permanece como par direto.

## 8. Estrutura completa de `indicadores.selecionado`

Caminho JSON: `indicadores.selecionado`.

Evidencia: `config/estilo.json:102-110`.

```json
{
  "off": " ",
  "preset_default": "Seta",
  "presets": {
    "Seta": {"simbolo": "→"},
    "Mão": {"simbolo": "☛"},
    "Alvo": {"simbolo": "◎"},
    "Ponta": {"simbolo": "➤"}
  }
}
```

Registro:

```yaml
preset_default: Seta
presets_disponiveis:
  Seta:
    simbolo: "→"
  Mao:
    simbolo: "☛"
  Alvo:
    simbolo: "◎"
  Ponta:
    simbolo: "➤"
campo_inativo: off
valor_inativo: " "
quantidade_de_caracteres_permitida:
  prevista_em_contrato: exatamente_1_caractere
  evidencia: docs/contratos/contrato_estilo.md:136-141
validacao_implementada_em_codigo: NAO_CONFIRMADO
preset_atualmente_escolhido: Seta
seta_desejada_presente: SIM
nome_do_preset_com_seta_desejada: Seta
seta_desejada_ativa: SIM
```

## 9. Estrutura completa de `indicadores.incluido`

Caminho JSON: `indicadores.incluido`.

Evidencia: `config/estilo.json:112-119`.

```json
{
  "preset_default": "Círculo",
  "presets": {
    "Círculo": {"on": "●", "off": "○"},
    "Quadrado": {"on": "■", "off": "□"},
    "Estrela": {"on": "★", "off": "☆"},
    "Check": {"on": "✔", "off": "✕"}
  }
}
```

Registro:

```yaml
preset_default: Circulo
presets_disponiveis:
  Circulo:
    on: "●"
    off: "○"
  Quadrado:
    on: "■"
    off: "□"
  Estrela:
    on: "★"
    off: "☆"
  Check:
    on: "✔"
    off: "✕"
uso_documental:
  console: docs/nomenclatura/32_CONSOLE.md:65,97-98
  barra_de_menus_transicional: config/elementos/barra_de_menus.json:92-99
relacao_com_selecao_multipla: indicador_on_off_do_toggle_em_tg
```

## 10. Distincao entre cursor, selecao unica e selecao multipla

Representacao documental atual:

```yaml
item_sob_o_cursor:
  termo_documental: Cursor / selecionado
  semantica: aponta_um_item
  evidencia: docs/nomenclatura/32_CONSOLE.md:63
  indicador_visual: selecionado
  local_no_item: ec
  evidencia_local: docs/nomenclatura/32_CONSOLE.md:97

item_em_foco:
  uso_documental: item_em_foco_em_contratos_de_console_barra_chip
  relacao: alvo_atual_para_enter_e_regras_dinamicas
  observacao: conceito_proximo_ao_item_sob_cursor_no_console

selecao_unica:
  politica: unica
  comportamento: cursor_define_item_alvo_sem_toggle
  evidencia_documental: contrato_console_consultado_na_entrega_anterior

selecao_multipla:
  politica: multipla
  comportamento: toggle_via_espaco
  indicador_visual: incluido
  local_no_item: tg
  evidencia: docs/nomenclatura/32_CONSOLE.md:65,98
```

Divergencia terminologica registrada sem correcao: o usuario usa a expressao
"item sob o cursor"; a documentacao atual usa `Cursor / selecionado` para esse
conceito. O indicador `selecionado` nao representa selecao multipla; ele
representa o cursor. O indicador `incluido` representa marcacao em selecao
multipla.

## 11. Estado do loader e da materializacao para runtime

O contrato de estilo define a materializacao esperada:

- `selecionado`: ler `indicadores.selecionado.preset_default`, buscar em
  `indicadores.selecionado.presets`, extrair `simbolo`, produzir
  `selecionado_simbolo`; ler `indicadores.selecionado.off`, produzir
  `selecionado_off`.
- `incluido`: ler `preset_default`, buscar em `presets`, extrair `on` e `off`,
  produzir `incluido_on` e `incluido_off`.

Evidencia contratual: `docs/contratos/contrato_estilo.md:149-174`.

Estado implementado observado:

- `tela/loader.py` implementa `carregar_tela`, que carrega JSONs de tela em
  `tela/loader.py:1093-1155`.
- `carregar_tela` retorna `cabecalho`, `corpo`, `barra_de_menus`, `_raw` e
  `_config_lancador` em `tela/loader.py:1271-1283`.
- O unico carregamento adicional de configuracao identificado no trecho
  material e `config_lancador`, acionado quando ha `lancador`, em
  `tela/loader.py:1264-1269`.
- Nao foi identificado loader ativo para `config/estilo.json`.
- Nao foi identificada materializacao dos campos planos
  `selecionado_simbolo`, `selecionado_off`, `incluido_on` e `incluido_off`.

Registro:

```yaml
arquivo_e_funcao_responsaveis_por_loader_de_tela:
  arquivo: tela/loader.py
  funcao: carregar_tela
  evidencia: tela/loader.py:1093
loader_de_estilo_ativo:
  status: NAO_CONFIRMADO_COMO_EXISTENTE
materializacao_de_indicadores_para_runtime:
  previsto_no_contrato: SIM
  implementado_no_codigo_ativo: NAO_CONFIRMADO_COMO_EXISTENTE
fallback_para_preset_inexistente:
  implementado: NAO_CONFIRMADO
comportamento_quando_opcao_ativa_nao_existe:
  implementado: NAO_CONFIRMADO
```

## 12. Estado do consumo pelo renderer

O renderer atual consome:

- `tipo_borda` como parametro de `renderizar_tela`, com default `"curva"` em
  `tela/renderizador.py:2388-2391`;
- `_BORDAS[tipo_borda]` em `tela/renderizador.py:2457-2477`;
- chips declarados em `barra_de_menus.chips[]`, formatados por
  `_texto_chip_barra` em `tela/renderizador.py:1140-1144`;
- `barra_de_menus.distribuicao` e `chips[]` em `_linhas_barra`, conforme
  `tela/renderizador.py:1501-1559`.

O renderer atual nao comprova consumo de:

- `config/estilo.json`;
- `indicadores.selecionado.preset_default`;
- `indicadores.selecionado.presets`;
- `indicadores.incluido.preset_default`;
- `indicadores.incluido.presets`;
- campos materializados `selecionado_simbolo`, `selecionado_off`,
  `incluido_on`, `incluido_off`.

## 13. Validacoes previstas e nao implementadas

Validacoes previstas em contrato:

```yaml
simbolo_exatamente_1_caractere:
  evidencia: docs/contratos/contrato_estilo.md:129-141
preset_selecionado_default_existente:
  evidencia_materializacao_prevista: docs/contratos/contrato_estilo.md:162-165
preset_incluido_default_existente:
  evidencia_materializacao_prevista: docs/contratos/contrato_estilo.md:166-167
campos_planos_runtime_obrigatorios:
  evidencia: docs/contratos/contrato_estilo.md:169-174
```

Estado implementado observado:

```yaml
validacao_de_preset_inexistente: NAO_CONFIRMADO
validacao_de_simbolo_vazio: NAO_CONFIRMADO
validacao_de_largura_ou_quantidade_incompativel: NAO_CONFIRMADO
fallback_para_opcao_ativa_inexistente: NAO_CONFIRMADO
```

Nao foi inferido comportamento nao comprovado por codigo ou teste.

## 14. Inventario das ocorrencias materiais e hardcodings

```yaml
- arquivo: config/estilo.json
  linha_ou_funcao: 102-110
  simbolo_ou_campo: indicadores.selecionado, preset_default, "→", "➤"
  natureza:
    - configuracao
  impacto: catalogo desejado ja existe; preset ativo "Seta" contem "→"

- arquivo: config/estilo.json
  linha_ou_funcao: 112-119
  simbolo_ou_campo: indicadores.incluido, preset_default, "●", "○"
  natureza:
    - configuracao
  impacto: catalogo de selecao multipla ja existe; preset ativo "Círculo" contem "●"/"○"

- arquivo: docs/nomenclatura/32_CONSOLE.md
  linha_ou_funcao: 63
  simbolo_ou_campo: "→"
  natureza:
    - default_documentado
  impacto: documenta "Cursor / selecionado" como item apontado pelo cursor

- arquivo: docs/nomenclatura/32_CONSOLE.md
  linha_ou_funcao: 65
  simbolo_ou_campo: "●", "○"
  natureza:
    - default_documentado
  impacto: documenta selecao como conjunto marcado via toggle

- arquivo: docs/nomenclatura/32_CONSOLE.md
  linha_ou_funcao: 97-98
  simbolo_ou_campo: selecionado, incluido, ec, tg
  natureza:
    - default_documentado
  impacto: separa espaco do cursor de espaco de toggle

- arquivo: config/elementos/barra_de_menus.json
  linha_ou_funcao: 92-99
  simbolo_ou_campo: incluido, "●", "○"
  natureza:
    - exemplo_historico
    - configuracao
  impacto: reforca relacao de incluido com selecao multipla; artefato transicional

- arquivo: tela/renderizador.py
  linha_ou_funcao: 153-164
  simbolo_ou_campo: _BORDAS e caracteres de borda
  natureza:
    - hardcoding_de_runtime
  impacto: bordas ainda nao vem de config/estilo.json

- arquivo: tela/renderizador.py
  linha_ou_funcao: 2388-2477
  simbolo_ou_campo: tipo_borda, "curva", "reta"
  natureza:
    - hardcoding_de_runtime
  impacto: escolha ativa de borda e parametro/estado vivo atual, nao opcao ativa persistida em estilo

- arquivo: tela/renderizador.py
  linha_ou_funcao: 1140-1144
  simbolo_ou_campo: "[{tecla}]"
  natureza:
    - hardcoding_de_runtime
  impacto: forma visual do chip nao consome chip.presets de config/estilo.json

- arquivo: tela/renderizador.py
  linha_ou_funcao: 1501-1559
  simbolo_ou_campo: barra_de_menus.chips[], distribuicao, regra_ativo nao avaliada
  natureza:
    - hardcoding_de_runtime
  impacto: renderer percorre declaracao de chips, mas nao usa indicadores de cursor/selecao

- arquivo: tela/modelo.py
  linha_ou_funcao: 8-16
  simbolo_ou_campo: cursor, selecao, foco
  natureza:
    - default_documentado
  impacto: modelo declara explicitamente que nao cria estado vivo de runtime para cursor/selecao/foco

- arquivo: tela/teste_renderizador.py
  linha_ou_funcao: testes de alternancia de borda na entrega anterior
  simbolo_ou_campo: curva/reta e caracteres esperados
  natureza:
    - valor_esperado_de_teste
  impacto: testes cobrem comportamento atual; nao comprovam materializacao de estilo
```

Observacao: assercoes de teste nao foram classificadas automaticamente como
hardcoding de producao.

## 15. Matriz de estado material

```yaml
catalogo_de_caracteres_ja_existe: SIM
evidencia_catalogo_de_caracteres_ja_existe:
  - config/estilo.json:105-110
  - config/estilo.json:114-119

opcao_ativa_ja_existe: SIM
evidencia_opcao_ativa_ja_existe:
  - config/estilo.json:104
  - config/estilo.json:113

seta_desejada_ja_existe: SIM
evidencia_seta_desejada_ja_existe:
  - config/estilo.json:106

seta_desejada_ja_esta_ativa: SIM
evidencia_seta_desejada_ja_esta_ativa:
  - config/estilo.json:104
  - config/estilo.json:106

loader_ja_materializa_a_opcao: NAO
evidencia_loader_ja_materializa_a_opcao:
  - tela/loader.py:1093-1155
  - tela/loader.py:1264-1283
  - docs/contratos/contrato_estilo.md:149-174
justificativa: contrato preve materializacao; codigo ativo inspecionado nao comprova loader de estilo nem campos planos de runtime

renderer_ja_consume_o_valor_materializado: NAO
evidencia_renderer_ja_consume_o_valor_materializado:
  - tela/renderizador.py:1140-1144
  - tela/renderizador.py:1501-1559
  - tela/renderizador.py:2388-2477
justificativa: renderer consome tipo_borda e chips declarados, nao campos materializados de indicadores

validacao_dos_presets_implementada: NAO
evidencia_validacao_dos_presets_implementada:
  - docs/contratos/contrato_estilo.md:149-174
  - tela/loader.py:1093-1155
justificativa: validacao e prevista contratualmente, mas nao foi localizada implementacao ativa para presets de estilo

navegacao_do_console_implementada: NAO
evidencia_navegacao_do_console_implementada:
  - docs/nomenclatura/32_CONSOLE.md:73-88
  - tela/modelo.py:14-15
  - tela/renderizador.py:1501-1526
justificativa: documentacao define navegacao; modelo nao cria estado de cursor/foco e renderer declara que nao avalia regras de estado neste ciclo

selecao_do_console_implementada: NAO
evidencia_selecao_do_console_implementada:
  - docs/nomenclatura/32_CONSOLE.md:63-66
  - docs/nomenclatura/32_CONSOLE.md:97-102
  - tela/modelo.py:14-15
justificativa: documentacao define selecao; modelo nao cria estado de selecao/foco/cursor e nao foi identificado consumo runtime dos indicadores
```

## 16. Conclusao arquitetural

A decisao de usar `→` sem hardcoding e compativel com a configuracao
persistida atual.

Nao e necessario criar um novo catalogo apenas para incluir `→`, porque
`config/estilo.json` ja contem o catalogo de `indicadores.selecionado`, ja
contem o preset `"Seta"` e esse preset ja contem `"→"`.

A lacuna material esta na inexistencia comprovada da carga, materializacao e
utilizacao dos indicadores pelo runtime. O contrato descreve como produzir
`selecionado_simbolo`, `selecionado_off`, `incluido_on` e `incluido_off`, mas
o codigo ativo inspecionado nao comprovou loader de estilo nem consumo desses
campos pelo renderer.

O relatorio nao decide como corrigir essa lacuna.

## 17. Decisoes ainda ausentes

Decisoes ausentes ou nao tomadas por este relatorio:

- se a lacuna de carga/materializacao/consumo exige ADR antes do handoff funcional;
- onde deve viver o loader de estilo;
- qual sera o objeto de estilo ativo em runtime;
- como bordas e chips devem receber opcao ativa/default persistida;
- como tratar preset inexistente;
- como tratar simbolo vazio ou com comprimento/largura incompatível;
- como ligar cursor, selecao unica e selecao multipla ao renderer do console;
- qual simbolo estatico deve aparecer em `tg` quando item navega, mas nao tem
  selecao real.

## 18. Bloqueios

```yaml
bloqueios_para_implementar_navegacao_e_selecao_agora:
  - ausencia_de_loader_ativo_de_estilo
  - ausencia_de_materializacao_de_indicadores_para_runtime
  - ausencia_de_consumo_dos_indicadores_pelo_renderer
  - ausencia_de_estado_vivo_de_cursor_selecao_foco_no_modelo_atual
  - decisao_pendente_sobre_necessidade_de_ADR
bloqueio_deste_relatorio:
  status: nenhum
```

## 19. Estado Git

Os comandos abaixo foram registrados para o estado final desta complementacao,
com este relatorio criado e sem stage preparado.

Comando:

```bash
cd "$(git rev-parse --show-toplevel)"
git status --short
```

Saida:

```text
?? docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md
```

Comando:

```bash
git diff --check
```

Saida:

```text

```

Comando:

```bash
git diff --cached --check
```

Saida:

```text

```

Stage:

```yaml
stage: VAZIO
```

## 20. Encerramento literal

LEVANTAMENTO_CONCLUIDO
