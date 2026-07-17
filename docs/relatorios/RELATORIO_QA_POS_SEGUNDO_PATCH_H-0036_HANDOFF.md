# Relatório de QA pós-segundo-patch do H-0036

## 1. Identificação

```yaml
etapa_executada: QA_HANDOFF
tipo_qa: POS_SEGUNDO_PATCH
handoff: H-0036
titulo: Fornecimento externo de dados ao console por JSON multinivel
arquivo_auditado: docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md
estado_auditado: CORRIGIDO_AGUARDANDO_QA
implementacao: NAO_INICIADA
auditoria: independente_de_handoff
```

## 2. Escopo da auditoria

Auditoria exclusiva da correcao de `QAHPP-0036-001`, da correcao de
`QAHPP-0036-002`, da ausencia de regressoes no restante do H-0036 e da
exequibilidade final da futura implementacao.

Nenhuma correcao foi feita no handoff. Nenhum codigo, teste, JSON, demo, ADR,
contrato ou relatorio anterior foi alterado. Este relatorio e o unico arquivo
criado por esta etapa.

## 3. Autoridades e evidências examinadas

Foram lidos integralmente ou conferidos por leitura documental completa e buscas
focais de verificacao:

```text
docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md
docs/relatorios/RELATORIO_QA_H-0036_HANDOFF.md
docs/relatorios/RELATORIO_QA_POS_PATCH_H-0036_HANDOFF.md
docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0027.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_console.md
docs/contratos/contrato_json_console.md
```

Tambem foram consultados nominalmente os 26 arquivos `h0035_*.json` em
`config/telas/demo/`, o estado Git, a lista de arquivos nao rastreados e buscas
por artefatos de implementacao antecipada.

## 4. Estado Git

Comandos executados antes da criacao deste relatorio:

```bash
git status --short
git diff --check
git ls-files --others --exclude-standard
git branch --show-current
git rev-parse --short HEAD
git status --short -- docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md
git diff --cached --stat
```

Estado confirmado:

```yaml
branch: master
head: fb9e5be
stage: vazio
commit_novo: nao_realizado
diff_check: sem_erros
handoff_status: "?? docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md"
```

`git status --short` antes deste relatorio continha os artefatos documentais
acumulados da ADR-0026, ADR-0027 e H-0036:

```text
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_console.md
 M docs/contratos/contrato_json_console.md
 M docs/contratos/contrato_tela_json.md
?? docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
?? docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
?? docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0027.md
?? docs/relatorios/RELATORIO_QA_ADR-0026.md
?? docs/relatorios/RELATORIO_QA_ADR-0027.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0026.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0027.md
?? docs/relatorios/RELATORIO_QA_H-0036_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0027.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0026.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0036_HANDOFF.md
```

Arquivos inesperados antes deste relatorio: nenhum fora do conjunto documental
acumulado ja declarado.

## 5. Estado e histórico do H-0036

Confirmado no handoff:

```yaml
handoff: H-0036
estado: CORRIGIDO_AGUARDANDO_QA
qa_handoff_inicial: H3_BLOCKED_DOCUMENTATION
qa_pos_primeiro_patch: H2_HANDOFF_PATCH_REQUIRED
qa_pos_segundo_patch: NAO_REALIZADO
implementacao: NAO_INICIADA
commit: NAO_REALIZADO
numero_preservado: true
novo_handoff_criado_ou_reservado: false
documento_autoaprova: false
```

O historico do QA inicial foi preservado com os achados `QAH-0036-001`,
`QAH-0036-002` e `QAH-0036-003`. O historico do primeiro patch foi preservado
com origem em `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0036_HANDOFF.md`,
classificacao `H2_HANDOFF_PATCH_REQUIRED` e achados `QAHPP-0036-001` e
`QAHPP-0036-002`.

## 6. Verificação de QAHPP-0036-001

Resultado: corrigido.

O inventario do H-0035 no handoff contem 26 entradas e cada entrada possui os
oito campos exigidos:

```yaml
campos_por_entrada:
  - arquivo
  - possui_console
  - possui_conteudo_de_runtime_do_console
  - materialmente_afetado_pela_ADR0027
  - classificacao
  - acao_no_H0036
  - json_externo_correspondente
  - justificativa
campos_ausentes: []
```

Contagem mecanica do bloco:

```yaml
total: 26
ALTERAR_E_SEPARAR: 2
PRESERVAR_SEM_ALTERACAO: 24
NAO_APLICAVEL: 0
```

A consulta direta dos JSONs confirmou 26 arquivos reais. Apenas estes dois
possuem elemento `console` com conteudo de runtime:

```yaml
config/telas/demo/h0035_console_com.json:
  existe: true
  possui_console: true
  possui_conteudo_de_runtime_do_console: true
  itens: 12
  distribuicao_matricial: true
  classificacao_handoff: ALTERAR_E_SEPARAR
  json_externo_correspondente: config/telas/demo/h0035_console_com_conteudo.json
  justificativa_compativel: true

config/telas/demo/h0035_console_sem.json:
  existe: true
  possui_console: true
  possui_conteudo_de_runtime_do_console: true
  itens: 2
  distribuicao_matricial: false
  classificacao_handoff: ALTERAR_E_SEPARAR
  json_externo_correspondente: config/telas/demo/h0035_console_sem_conteudo.json
  justificativa_compativel: true
```

Os outros 24 arquivos existem, estao classificados como
`PRESERVAR_SEM_ALTERACAO`, possuem `acao_no_H0036: nenhuma`,
`json_externo_correspondente: NENHUM` e justificativa factual especifica. A
inspecao direta confirmou que eles nao contem conteudo de runtime do console
que exija separacao.

Conclusao: o futuro executor nao precisa descobrir quais arquivos sao afetados,
deduzir os JSONs externos correspondentes ou reinterpretar justificativas
ausentes.

## 7. Inventário nominal dos 26 JSONs

| Arquivo | Conteudo de runtime do console | Classificacao | Acao | JSON externo |
|---|---:|---|---|---|
| `config/telas/demo/h0035_catalogo.json` | nao | PRESERVAR_SEM_ALTERACAO | nenhuma | NENHUM |
| `config/telas/demo/h0035_centralizado_h_colunas.json` | nao | PRESERVAR_SEM_ALTERACAO | nenhuma | NENHUM |
| `config/telas/demo/h0035_console_com.json` | sim | ALTERAR_E_SEPARAR | separar | `config/telas/demo/h0035_console_com_conteudo.json` |
| `config/telas/demo/h0035_console_sem.json` | sim | ALTERAR_E_SEPARAR | separar | `config/telas/demo/h0035_console_sem_conteudo.json` |
| `config/telas/demo/h0035_dashboard_com.json` | nao | PRESERVAR_SEM_ALTERACAO | nenhuma | NENHUM |
| `config/telas/demo/h0035_dashboard_sem.json` | nao | PRESERVAR_SEM_ALTERACAO | nenhuma | NENHUM |
| `config/telas/demo/h0035_esquerda_margens_min_max.json` | nao | PRESERVAR_SEM_ALTERACAO | nenhuma | NENHUM |
| `config/telas/demo/h0035_h_margens_limitadas.json` | nao | PRESERVAR_SEM_ALTERACAO | nenhuma | NENHUM |
| `config/telas/demo/h0035_h_uniforme.json` | nao | PRESERVAR_SEM_ALTERACAO | nenhuma | NENHUM |
| `config/telas/demo/h0035_lancador_com.json` | nao | PRESERVAR_SEM_ALTERACAO | nenhuma | NENHUM |
| `config/telas/demo/h0035_lancador_sem.json` | nao | PRESERVAR_SEM_ALTERACAO | nenhuma | NENHUM |
| `config/telas/demo/h0035_matriz_fixa_cabe.json` | nao | PRESERVAR_SEM_ALTERACAO | nenhuma | NENHUM |
| `config/telas/demo/h0035_matriz_fixa_quadro_minimo.json` | nao | PRESERVAR_SEM_ALTERACAO | nenhuma | NENHUM |
| `config/telas/demo/h0035_minimo_fixo_excedido.json` | nao | PRESERVAR_SEM_ALTERACAO | nenhuma | NENHUM |
| `config/telas/demo/h0035_pref_colunas.json` | nao | PRESERVAR_SEM_ALTERACAO | nenhuma | NENHUM |
| `config/telas/demo/h0035_pref_linhas.json` | nao | PRESERVAR_SEM_ALTERACAO | nenhuma | NENHUM |
| `config/telas/demo/h0035_quatro_centralizados.json` | nao | PRESERVAR_SEM_ALTERACAO | nenhuma | NENHUM |
| `config/telas/demo/h0035_resto_horizontal.json` | nao | PRESERVAR_SEM_ALTERACAO | nenhuma | NENHUM |
| `config/telas/demo/h0035_resto_vertical.json` | nao | PRESERVAR_SEM_ALTERACAO | nenhuma | NENHUM |
| `config/telas/demo/h0035_tres_centralizados.json` | nao | PRESERVAR_SEM_ALTERACAO | nenhuma | NENHUM |
| `config/telas/demo/h0035_um_centralizado.json` | nao | PRESERVAR_SEM_ALTERACAO | nenhuma | NENHUM |
| `config/telas/demo/h0035_uma_coluna.json` | nao | PRESERVAR_SEM_ALTERACAO | nenhuma | NENHUM |
| `config/telas/demo/h0035_uma_linha.json` | nao | PRESERVAR_SEM_ALTERACAO | nenhuma | NENHUM |
| `config/telas/demo/h0035_v_margens_min.json` | nao | PRESERVAR_SEM_ALTERACAO | nenhuma | NENHUM |
| `config/telas/demo/h0035_v_margens_min_max.json` | nao | PRESERVAR_SEM_ALTERACAO | nenhuma | NENHUM |
| `config/telas/demo/h0035_v_uniforme.json` | nao | PRESERVAR_SEM_ALTERACAO | nenhuma | NENHUM |

## 8. Verificação de QAHPP-0036-002

Resultado: corrigido.

Os dois arquivos originalmente conflitantes continuam autorizados para
`ALTERAR` na lista nominal da futura implementacao:

```yaml
demo/teste_demo_distribuicao.py:
  categoria_autorizada: ALTERAR
  preservados_sem_alteracao_28_1: false
  subsecao_28_2: alteracao_autorizada + responsabilidade_historica_preservada
  proibido: false
  conflito: false

config/telas/demo/demo.json:
  categoria_autorizada: ALTERAR
  preservados_sem_alteracao_28_1: false
  subsecao_28_2: alteracao_autorizada + responsabilidade_historica_preservada
  proibido: false
  conflito: false
```

A subsecao "Arquivos com alteracao autorizada e responsabilidade historica
preservada" nao volta a proibir a alteracao exigida na lista nominal. Ela
preserva finalidade historica, nao imutabilidade.

## 9. Confronto entre listas de arquivos

Confronto nominal entre arquivos a alterar/criar, preservados sem alteracao,
preservados quanto ao comportamento e proibicoes:

| Arquivo | categoria_autorizada | categoria_preservacao | categoria_proibicao | conflito |
|---|---|---|---|---|
| `tela/loader.py` | ALTERAR | nenhuma | nenhuma | nao |
| `tela/modelo.py` | ALTERAR | nenhuma | nenhuma | nao |
| `tela/renderizador.py` | ALTERAR | comportamento sem conteudo externo preservado | nao abrir JSONs | nao |
| `tela/teste_loader.py` | ALTERAR | nenhuma | nenhuma | nao |
| `tela/teste_modelo.py` | ALTERAR | nenhuma | nenhuma | nao |
| `tela/teste_renderizador.py` | ALTERAR | nenhuma | nenhuma | nao |
| `demo/demo.py` | ALTERAR | ponto de entrada real preservado | nenhuma | nao |
| `demo/teste_demo.py` | ALTERAR | nenhuma | nenhuma | nao |
| `demo/teste_diagnostico.py` | ALTERAR | nenhuma | nenhuma | nao |
| `demo/teste_demo_distribuicao.py` | ALTERAR | responsabilidade historica preservada | nenhuma | nao |
| `config/telas/demo/h0035_console_com.json` | ALTERAR | estrutura e distribuicao_matricial preservadas | nao reinserir runtime | nao |
| `config/telas/demo/h0035_console_sem.json` | ALTERAR | estrutura preservada | nao reinserir runtime | nao |
| `config/telas/demo/demo.json` | ALTERAR | responsabilidade historica preservada | nenhuma | nao |
| `config/telas/demo/h0036_console_hierarquia.json` | CRIAR | nenhuma | nenhuma | nao |
| `config/telas/demo/h0036_console_tabela.json` | CRIAR | nenhuma | nenhuma | nao |
| `config/telas/demo/h0036_console_conjuntos.json` | CRIAR | nenhuma | nenhuma | nao |
| `config/telas/demo/h0036_hierarquia_conteudo.json` | CRIAR | nenhuma | sem resultados fisicos | nao |
| `config/telas/demo/h0036_tabela_conteudo.json` | CRIAR | nenhuma | sem resultados fisicos | nao |
| `config/telas/demo/h0036_conjuntos_conteudo.json` | CRIAR | nenhuma | sem resultados fisicos | nao |
| `config/telas/demo/h0035_console_com_conteudo.json` | CRIAR | identidade historica preservada | sem resultados fisicos | nao |
| `config/telas/demo/h0035_console_sem_conteudo.json` | CRIAR | identidade historica preservada | sem resultados fisicos | nao |
| `demo/teste_demo_console.py` | CRIAR | nenhuma | nenhuma | nao |
| `docs/relatorios/IMP-0036-fornecimento-externo-dados-console-json-multinivel.md` | CRIAR | nao autoaprovar implementacao | nenhuma | nao |
| `docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md` | nenhuma | preservado sem alteracao | nao alterar ADR | nao |
| `docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md` | nenhuma | preservado sem alteracao | nao alterar ADR | nao |
| `docs/relatorios/RELATORIO_QA_H-0036_HANDOFF.md` | nenhuma | preservado sem alteracao | nenhuma | nao |
| `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0036_HANDOFF.md` | nenhuma | historico preservado | nenhuma | nao |
| `docs/contratos/contrato_tela_json.md` | nenhuma | preservado sem alteracao | nao alterar contratos | nao |
| `docs/contratos/contrato_console.md` | nenhuma | preservado sem alteracao | nao alterar contratos | nao |
| `docs/contratos/contrato_json_console.md` | nenhuma | preservado sem alteracao | nao alterar contratos | nao |
| `docs/NOMENCLATURA.md` | nenhuma | preservado sem alteracao | nao alterar nomenclatura | nao |
| `docs/adr/INDICE_ADR.md` | nenhuma | preservado sem alteracao | nenhuma | nao |
| `tela/distribuicao_matricial.py` | nenhuma | preservado sem alteracao | nenhuma | nao |
| `tela/teste_distribuicao_matricial.py` | nenhuma | preservado sem alteracao | nenhuma | nao |
| `demo/demo_distribuicao.py` | nenhuma | preservado sem alteracao | nenhuma | nao |
| `demo/diagnostico.py` | nenhuma | preservado sem alteracao | nenhuma | nao |
| `demo/explorar_barra_de_menus.py` | nenhuma | preservado sem alteracao | nenhuma | nao |
| `demo/teste_explorar_barra_de_menus.py` | nenhuma | preservado sem alteracao | nenhuma | nao |
| 24 arquivos `h0035_*.json` preservados em §11 | nenhuma | PRESERVAR_SEM_ALTERACAO | nenhuma | nao |

Nao foi encontrada sobreposicao nominal incompatível entre autorizados,
preservados sem alteracao e proibidos.

## 10. Lista nominal da futura implementação

Contagem confirmada da secao 15.1:

```yaml
arquivos_a_alterar: 13
arquivos_a_criar: 10
caminhos_unicos: 23
duplicatas: false
curingas: false
diretorios_genericos: false
caminho_novo_introduzido_pelo_segundo_patch: nao_detectado
remocao_acidental: nao_detectada
```

Arquivos especialmente verificados e presentes:

```text
demo/demo.py
demo/teste_demo.py
demo/teste_diagnostico.py
demo/teste_demo_distribuicao.py
demo/teste_demo_console.py
config/telas/demo/demo.json
```

## 11. Fixtures permanentes

As cinco fixtures externas permanecem autorizadas nominalmente como arquivos
novos em `config/telas/demo/`:

```yaml
fixtures_confirmadas:
  - config/telas/demo/h0036_hierarquia_conteudo.json
  - config/telas/demo/h0036_tabela_conteudo.json
  - config/telas/demo/h0036_conjuntos_conteudo.json
  - config/telas/demo/h0035_console_com_conteudo.json
  - config/telas/demo/h0035_console_sem_conteudo.json
removidas: false
renomeadas: false
preservadas_existentes: false
proibidas: false
classificacao: CRIAR
apresentacoes_cobertas:
  - hierarquia
  - tabela
  - conjuntos_campos
```

## 12. Preservação do schema e das validações

Preservado o nucleo normativo:

```yaml
schema_preservado: true
envelope: true
tres_apresentacoes: [tabela, hierarquia, conjuntos_campos]
tres_tipos_de_nivel: [container, conteudo, nome_valor]
niveis_declarados: true
nos: true
filhos: true
designadores: true
resultados_fisicos_proibidos: true
validacoes_preservadas: 20
```

As 20 validacoes permanecem nominalmente presentes: raiz objeto; `tipo` presente,
correto e igual a `"multinivel"`; `formato`; `dados`; apresentacao; niveis;
campos de nivel; unicidade de IDs; tipos de nivel; nos com `id` e `nivel`;
referencia a nivel declarado; formas `container`, `conteudo` e `nome_valor`;
recursao por filhos; ordem preservada; compatibilidade por apresentacao; e
ausencia de resultados fisicos calculados.

## 13. Preservação do demo.py e catálogo

Confirmado:

```yaml
demo_py_obrigatorio: true
carrega_dois_documentos_separadamente: true
associacao_externa_no_catalogo_ou_mecanismo_do_demo_py: true
campo_de_vinculo_no_json_estrutural: proibido
cenario_sem_conteudo_coberto: true
demo_dedicado_como_prova_unica: proibido
```

## 14. Preservação dos testes e suíte canônica

Permanecem previstos testes de loader, modelo, renderizador, integracao,
catalogo, smoke e regressao do H-0035.

```yaml
baseline_atual: 8 scripts
baseline_futuro: 9 scripts
novo_script: demo/teste_demo_console.py
suite_canonica_preservada: true
```

## 15. Preservação da validação manual

O roteiro de validacao manual permanece com 12 passos e cobre abertura do
cenario `h0036_console_hierarquia`, prova de identidade textual, confirmacao de
conteudo externo fora do JSON estrutural, maximizacao, restauracao, reducoes,
redimensionamento livre, quadro minimo, recuperacao, retorno ao catalogo,
cenario sem conteudo e ausencia de vazamento.

Permanece obrigatorio registrar:

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

ate retorno do usuario.

## 16. Rastreabilidade do segundo patch

Confirmada secao factual contendo:

```yaml
qa_de_origem: docs/relatorios/RELATORIO_QA_POS_PATCH_H-0036_HANDOFF.md
classificacao_de_origem: H2_HANDOFF_PATCH_REQUIRED
achados_corrigidos:
  - QAHPP-0036-001
  - QAHPP-0036-002
```

As correcoes estao descritas: inventario dos 26 JSONs completado com
`json_externo_correspondente` e justificativa nominal; conflito entre arquivos
autorizados e preservados sem alteracao removido por reclassificacao em
subsecao propria.

O documento preserva os resultados historicos e nao se autoaprova.

## 17. Exequibilidade final

Resultado: implementacao exequivel.

A futura implementacao pode comecar sem nova ADR, decisao do usuario, escolha de
schema, descoberta de arquivo afetado, escolha de caminho de fixture, escolha de
ponto de entrada, escolha de apresentacao a cobrir, conflito de permissoes ou
arquivo necessario fora da lista.

Autoridade suficiente confirmada para:

```yaml
alterar_os_13_arquivos: true
criar_os_10_arquivos: true
separar_os_2_jsons_H0035: true
preservar_os_outros_24_jsons_H0035: true
criar_as_5_fixtures_externas: true
alterar_demo_py: true
implementar_as_20_validacoes: true
cobrir_as_3_apresentacoes: true
executar_os_9_scripts: true
apresentar_validacao_manual_ao_usuario: true
criar_relatorio_de_implementacao: true
```

## 18. Ausência de implementação antecipada

Confirmado por estado Git, buscas focais e ausencia de arquivos futuros:

```yaml
codigo_alterado_pelo_segundo_patch: false
teste_alterado_pelo_segundo_patch: false
demo_py_alterado: false
json_criado_ou_alterado_pelo_segundo_patch: false
fixture_criada: false
implementacao_executada: false
validacao_manual_concluida: false
stage_preparado: false
commit_realizado: false
```

O repositorio ainda nao possui `h0036_*`, `_conteudo.json`,
`demo/teste_demo_console.py` nem o relatorio `IMP-0036`, coerente com
`implementacao: NAO_INICIADA`.

## 19. Escopo real do segundo patch

O arquivo autorizado para a etapa de patch era:

```text
docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md
```

A verificacao direta confirma que nao ha evidencia de codigo, teste, `demo.py`,
JSON ou fixture alterado/criado pela etapa do segundo patch. O workspace contem
artefatos documentais acumulados anteriores da ADR-0026, ADR-0027 e H-0036, ja
declarados e nao tratados como inesperados.

Depois da criacao deste relatorio, o unico arquivo novo desta etapa de QA e:

```text
docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0036_HANDOFF.md
```

## 20. Regressões

Nenhuma regressao documental material foi identificada.

```yaml
schema: preservado
validacoes: preservadas
fixtures: preservadas
demo_py: preservado_no_escopo_obrigatorio
catalogo: preservado
suite_canonica: preservada
validacao_manual: preservada
relatorio_implementacao: preservado
conflitos_de_classificacao: nenhum
```

## 21. Achados

Nenhum novo defeito foi identificado.

```yaml
achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 0
observacoes: 2
```

## 22. Observações

```yaml
observacoes:
  - id: OBS-QAHPP2-0036-001
    severidade: observacao
    descricao: >
      O workspace permanece sujo por artefatos documentais acumulados da
      ADR-0026, ADR-0027 e H-0036. Isso e coerente com o estado declarado e nao
      foi classificado como inesperado.
    correcao_necessaria: nenhuma
  - id: OBS-QAHPP2-0036-002
    severidade: observacao
    descricao: >
      Como o handoff H-0036 esta nao rastreado, nao ha diff rastreado isolando
      mecanicamente cada linha do segundo patch. A auditoria validou diretamente
      o conteudo atual do handoff e o estado real dos arquivos tecnicos/JSONs.
    correcao_necessaria: nenhuma
```

## 23. Classificação final

```yaml
status_literal: H1_HANDOFF_APPROVED
status_normalizado: Handoff aprovado para implementacao
relatorio: docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0036_HANDOFF.md

achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 0
observacoes: 2

QAHPP-0036-001_corrigido: true
QAHPP-0036-002_corrigido: true

inventario_H0035_completo: true
inventario_H0035_total: 26
inventario_H0035_afetados: 2
inventario_H0035_preservados: 24
inventario_H0035_campos_por_linha: 8
inventario_H0035_justificativas_confirmadas: true

conflitos_de_classificacao_remanescentes: 0
arquivos_a_alterar_confirmados: 13
arquivos_a_criar_confirmados: 10
fixtures_confirmadas: true
schema_preservado: true
validacoes_preservadas: true
demo_py_preservado_no_escopo: true
catalogo_preservado: true
suite_canonica_preservada: true
validacao_manual_preservada: true
relatorio_implementacao_preservado: true
regressoes: 0
implementacao_exequivel: true
arquivos_inesperados: []
git:
  branch: master
  head: fb9e5be
  stage: vazio
  commit_novo: nao_realizado
  diff_check: sem_erros
  arquivo_criado_nesta_etapa: docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0036_HANDOFF.md
proxima_categoria: IMPLEMENTAR
```
