---
name: RELATORIO_QA_POS_PATCH_2_H-0037_IMPLEMENTACAO
description: Auditoria independente do segundo patch focal da implementacao do H-0037
handoff: H-0037
status_literal: IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: REPROVADO_PATCH_NECESSARIO
proxima_categoria: PATCH_IMPLEMENTACAO
---

# Relatorio de QA pos-patch 2 da implementacao do H-0037

## 1. Identificacao

| Campo | Valor |
|---|---|
| Projeto | Orquestrador |
| Etapa executada | `QA_POS_PATCH_IMPLEMENTACAO` |
| Handoff | `docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md` |
| QA anterior | `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0037_IMPLEMENTACAO.md` |
| Relatorio de implementacao | `docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md` |
| Branch | `master` |
| HEAD | `f6982d08640af1762b8e0e8814b6e90c9421538e` |
| Resultado | `IMPLEMENTATION_PATCH_REQUIRED` |

## 2. Objetivo

Auditar se o segundo patch focal resolveu os dois achados altos do QA
pos-patch anterior:

- `H0037-IMPL-QAPP-001`: bypass do D23;
- `H0037-IMPL-QAPP-002`: V-01 aceita cabecalho sem coluna valida.

Este QA nao corrigiu codigo, testes, JSONs ou documentos existentes, nao
executou validacao manual, nao preparou stage, nao fez commit e nao fez push.
Foi criado somente este relatorio.

## 3. Autoridades

Arquivos lidos:

```yaml
docs/relatorios/RELATORIO_QA_H-0037_IMPLEMENTACAO.md: lido
docs/relatorios/RELATORIO_QA_POS_PATCH_H-0037_IMPLEMENTACAO.md: lido
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md: lido
docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md: lido
docs/relatorios/RELATORIO_QA_POS_PATCH_H-0037_HANDOFF.md: lido
docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md: lido
docs/contratos/contrato_json_console.md: lido
docs/contratos/contrato_console.md: lido
docs/contratos/contrato_tela_json.md: lido
docs/contratos/contrato_composicao_corpo.md: lido
docs/contratos/contrato_barra_de_menus.md: lido
tela/loader.py: lido
tela/teste_loader.py: lido
demo/teste_demo_console_modos.py: lido
```

Autoridades decisivas:

- `contrato_json_console.md` secao 13.13: telas novas ou revisadas de console
  multinivel devem declarar `formato.excesso.politica_modo`; nao existe default
  implicito; ausencia e invalida.
- `contrato_tela_json.md` secao 33.6: a obrigacao D23 pertence ao JSON
  estrutural da tela.
- `contrato_json_console.md` secao 13.9: V-01 rejeita tabela sem cabecalho;
  V-14 rejeita coluna de tabela sem `nivel` ou `campo` de origem.
- `contrato_json_console.md` secao 13.13.8 e `contrato_tela_json.md` secao
  33.6.3: telas criadas antes de D23 permanecem validas sem `politica_modo`.
- H-0036 documenta a adaptacao de `h0035_console_com` e `h0035_console_sem`
  para consumir conteudo externo antes de D23.

## 4. Estado Git

Comandos executados na raiz real do repositorio:

```yaml
branch: master
head: f6982d08640af1762b8e0e8814b6e90c9421538e
log_1: "f6982d0 docs: corrige whitespace do fechamento H-0036"
stage: vazio
git_diff_check: sem_erros
git_diff_cached_name_status: vazio
commit_novo: inexistente
scripts_dir: ausente_no_checkout
```

O prompt indicava `scripts/` como diretorio operacional, mas o checkout atual
contem diretamente `config/`, `demo/`, `docs/` e `tela/`. Os comandos tecnicos
foram executados a partir da raiz real.

Arquivos modificados rastreados no workspace:

```text
config/telas/demo/demo.json
demo/demo.py
demo/teste_demo.py
demo/teste_demo_console.py
demo/teste_diagnostico.py
docs/NOMENCLATURA.md
docs/adr/INDICE_ADR.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_console.md
docs/contratos/contrato_json_console.md
docs/contratos/contrato_tela_json.md
tela/loader.py
tela/modelo.py
tela/renderizador.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
```

Arquivos nao rastreados relevantes:

```text
config/telas/demo/h0037_console_alternavel_tres_niveis.json
config/telas/demo/h0037_console_nao_verboso.json
config/telas/demo/h0037_console_tabela_alternavel.json
config/telas/demo/h0037_console_verboso_dois_niveis.json
config/telas/demo/h0037_dois_niveis_conteudo.json
config/telas/demo/h0037_tabela_conteudo.json
config/telas/demo/h0037_tres_niveis_conteudo.json
demo/teste_demo_console_modos.py
docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md
docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
docs/relatorios/RELATORIO_*ADR-0028*.md
docs/relatorios/RELATORIO_QA_H-0037_*.md
docs/relatorios/RELATORIO_QA_POS_PATCH_H-0037_*.md
```

Para arquivos inesperados:

```yaml
origem: NAO_CONFIRMADA
produzido_pelo_executor: NAO_CONFIRMADO
```

Artefatos transitorios: nenhum `__pycache__`, `*.pyc`, `*.tmp`, `*.bak`,
`*.swp` ou `*~` encontrado ao final da auditoria.

## 5. Inventario Do Segundo Patch

O executor declarou alteracoes focais em:

```text
tela/loader.py
tela/teste_loader.py
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
```

O diff do workspace nao permite isolar com certeza somente o segundo patch,
pois ha alteracoes acumuladas do H-0037 e documentos ainda nao rastreados.
Nao ha evidencia suficiente para atribuir arquivos adicionais ao segundo patch.

```yaml
arquivo_adicional_confirmado_do_segundo_patch: nenhum
arquivos_acumulados:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
```

## 6. Integridade

```yaml
python_ast:
  tela/loader.py: OK
  tela/teste_loader.py: OK
  demo/teste_demo_console_modos.py: OK
json_loads:
  config/telas/demo/demo.json: OK
  config/telas/demo/h0037_console_nao_verboso.json: OK
  config/telas/demo/h0037_console_verboso_dois_niveis.json: OK
  config/telas/demo/h0037_console_alternavel_tres_niveis.json: OK
  config/telas/demo/h0037_console_tabela_alternavel.json: OK
  config/telas/demo/h0037_dois_niveis_conteudo.json: OK
  config/telas/demo/h0037_tres_niveis_conteudo.json: OK
  config/telas/demo/h0037_tabela_conteudo.json: OK
conflitos_git:
  marcadores: ausentes
temporarios:
  encontrados: []
git_diff_check: sem_erros
```

## 7. Escopo

O segundo patch focal alterou a regra D23 por `_console_em_escopo_d23` e
ampliou `_TELAS_LEGADAS_D23` para cinco IDs. A auditoria confirma que a ausencia
simples de `formato.excesso` deixou de ser bypass. Porem ha bypass remanescente
por campo isolado de envelope e ha defeito em V-01 para objetos/chaves com
valores vazios.

## 8. `_console_em_escopo_d23`

Implementacao real em `tela/loader.py`:

- `_TELAS_LEGADAS_D23`: cinco IDs nominais.
- `_CAMPOS_ENVELOPE_PRE_ADR_0028`: `itens`, `origem_dados`,
  `politica_composicao`, `politica_navegacao`, `politica_selecao`,
  `politica_paginacao`, `politica_exibicao`.
- `_console_em_escopo_d23(elemento, id_tela)` retorna `False` se qualquer campo
  acima existir no elemento; caso contrario retorna `id_tela not in
  _TELAS_LEGADAS_D23`.

Conclusao obrigatoria:

```yaml
funcao_console_em_escopo_d23:
  criterio_real: "qualquer campo de envelope no elemento => fora_de_D23; senao id nominal legado => fora_de_D23; demais => em_D23"
  criterios_positivos: "ausencia de campos de envelope e id fora do inventario legado"
  criterios_negativos: "presenca isolada de qualquer campo de envelope; id legado nominal"
  depende_do_id: sim_para_legado_nominal
  depende_de_campos_isolados: sim
  permite_hibrido: sim
  permite_bypass_por_envelope: sim
  conforme_autoridade: false
```

O problema e corrigivel localmente: a presenca isolada de um campo de envelope
nao basta para provar que a tela e envelope contratual completo, nem pode
silenciar D23 em consumidor novo ou estrutura hibrida.

## 9. Matriz Adversarial D23

Casos executados com JSONs temporarios e `carregar_tela`:

| Caso | Esperado | Observado | Conforme |
|---|---|---|---|
| D23-A consumidor valido com politica | ACEITO | ACEITO | sim |
| D23-B consumidor sem `politica_modo` | REJEITADO | REJEITADO | sim |
| D23-C consumidor sem `formato.excesso` | REJEITADO | REJEITADO | sim |
| D23-D ID arbitrario sem D23 | REJEITADO | REJEITADO | sim |
| D23-E + `itens: []` isolado | REJEITADO ou hibrido invalido | ACEITO | nao |
| D23-E + `origem_dados: null` isolado | REJEITADO ou hibrido invalido | ACEITO | nao |
| D23-E + `politica_exibicao` isolado | REJEITADO ou hibrido invalido | ACEITO | nao |
| D23-E + `politica_navegacao` isolado | REJEITADO ou hibrido invalido | ACEITO | nao |
| D23-F `itens` + `formato.excesso` valido | autoridade deveria distinguir ou rejeitar hibrido | ACEITO como fora_de_D23 | nao |
| D23-F `itens` sem politica | REJEITADO ou hibrido invalido | ACEITO | nao |
| D23-G envelope historico minimo completo | PRESERVA_COMPORTAMENTO_ANTERIOR | ACEITO | sim |
| D23-H `excesso.modo` legado em tela nova | REJEITADO | REJEITADO | sim |
| D23-I politica desconhecida | REJEITADO | REJEITADO | sim |
| D23-J tipo incorreto | REJEITADO | REJEITADO | sim |

Resultado: `H0037-IMPL-QAPP-001` nao foi resolvido integralmente. O bypass por
omissao de `formato.excesso` foi fechado, mas surgiu/permaneceu bypass por campo
isolado de envelope.

## 10. Inventario Legado

IDs legados reconhecidos em `_TELAS_LEGADAS_D23`:

```yaml
H_0036:
  - h0036_console_hierarquia
  - h0036_console_tabela
  - h0036_console_conjuntos
H_0035:
  - h0035_console_com
  - h0035_console_sem
total: 5
```

Classificacao dos cinco JSONs reais:

```yaml
- id: h0036_console_hierarquia
  ciclo_de_origem: H-0036
  tipo: console
  apresentacao: hierarquia
  usa_conteudo_externo: true
  usa_multinivel: true
  possui_formato_excesso: false
  possui_campos_D23: false
  carregava_antes_do_H_0037: sim
  necessita_compatibilidade: sim
  autoridade_para_isencao: "contrato_json_console 13.13.8; handoff H-0037 30.2"
  resultado: ACEITO
- id: h0036_console_tabela
  ciclo_de_origem: H-0036
  tipo: console
  apresentacao: tabela
  usa_conteudo_externo: true
  usa_multinivel: true
  possui_formato_excesso: false
  possui_campos_D23: false
  carregava_antes_do_H_0037: sim
  necessita_compatibilidade: sim
  autoridade_para_isencao: "contrato_json_console 13.13.8; handoff H-0037 30.2"
  resultado: ACEITO
- id: h0036_console_conjuntos
  ciclo_de_origem: H-0036
  tipo: console
  apresentacao: conjuntos_campos
  usa_conteudo_externo: true
  usa_multinivel: true
  possui_formato_excesso: false
  possui_campos_D23: false
  carregava_antes_do_H_0037: sim
  necessita_compatibilidade: sim
  autoridade_para_isencao: "contrato_json_console 13.13.8; handoff H-0037 30.2"
  resultado: ACEITO
- id: h0035_console_com
  ciclo_de_origem: H-0035_adaptado_em_H-0036
  tipo: console
  apresentacao: hierarquia
  usa_conteudo_externo: true
  usa_multinivel: true
  possui_formato_excesso: false
  possui_campos_D23: false
  carregava_antes_do_H_0037: sim
  necessita_compatibilidade: sim
  autoridade_para_isencao: "handoff/IMP H-0036 documentam migracao para conteudo externo antes de D23"
  resultado: ACEITO
- id: h0035_console_sem
  ciclo_de_origem: H-0035_adaptado_em_H-0036
  tipo: console
  apresentacao: hierarquia
  usa_conteudo_externo: true
  usa_multinivel: true
  possui_formato_excesso: false
  possui_campos_D23: false
  carregava_antes_do_H_0037: sim
  necessita_compatibilidade: sim
  autoridade_para_isencao: "handoff/IMP H-0036 documentam migracao para conteudo externo antes de D23"
  resultado: ACEITO
```

## 11. Telas H-0035

As duas telas H-0035 incluidas sao `h0035_console_com` e
`h0035_console_sem`. Elas foram materialmente adaptadas em H-0036 para consumir
documentos externos `h0035_console_com_conteudo` e
`h0035_console_sem_conteudo`. A inclusao no inventario legado e justificada
para preservar telas existentes pre-D23 que ja estavam no fluxo de conteudo
externo.

```yaml
expansao_classificada_como: EXPANSAO_JUSTIFICADA_PELA_AUTORIDADE
observacao: "os testes novos D23-04 cobrem apenas os tres IDs H-0036; a auditoria independente confirmou os dois IDs H-0035"
```

## 12. Tentativa De Bypass Por Envelope

A tentativa de adicionar campos isolados de envelope a uma tela nova consumidora
de console foi aceita para `itens`, `origem_dados`, `politica_exibicao` e
`politica_navegacao`. Isso retira indevidamente a tela do escopo D23.

Evidencia de codigo: `tela/loader.py` usa `any(campo in elemento for campo in
_CAMPOS_ENVELOPE_PRE_ADR_0028)` e retorna `False` para D23 sem validar se o
envelope esta completo ou se a estrutura e hibrida/incompativel.

## 13. Estruturas Hibridas

Estruturas com `formato.excesso` e `itens` foram aceitas. Estruturas com
`formato.excesso` sem politica e `origem_dados` tambem foram aceitas. Nao foi
encontrada autoridade explicita que permita essa precedencia por ordem de
`if/else`. Na ausencia de precedencia normativa, a estrutura hibrida deveria
ser rejeitada ou classificada por uma regra documental explicita.

## 14. `_coluna_reconhecivel`

Implementacao real:

```yaml
string: reconhecivel_se entrada != ""
dict: reconhecivel_se contem_qualquer_chave_em ["titulo", "nivel", "campo"]
outros_tipos: false
```

Conclusao obrigatoria:

```yaml
coluna_reconhecivel:
  formas_autorizadas: "contrato exige cabecalho de tabela; fixtures reais usam strings; objetos nao tem forma detalhada na autoridade lida"
  string_simples_autorizada: "praticada pelas fixtures H-0036/H-0037; autoridade nao detalha alternativa"
  campos_minimos: "implementacao usa mera presenca de titulo/nivel/campo"
  valores_vazios_aceitos: true
  mistura_valida_invalida: aceita_se_alguma_coluna_reconhecivel
  separacao_V01_V14: parcial
  conforme_autoridade: false
```

O defeito corrigivel e aceitar valores semanticamente vazios (`null`, `""` ou
string so com espacos) apenas porque a chave existe ou a string nao e `""`.

## 15. Matriz V-01

Casos executados por `validar_conteudo_externo`:

| Entrada de cabecalho | Observado |
|---|---|
| propriedade ausente | V-01 |
| `null` | V-01 |
| `[]` | V-01 |
| `[null]` | V-01 |
| `[1]` | V-01 |
| `[true]` | V-01 |
| `[{}]` | V-01 |
| `[{"titulo": null}]` | ACEITO |
| `[{"titulo": ""}]` | ACEITO |
| `[{"nivel": null}]` | ACEITO |
| `[{"campo": null}]` | ACEITO |
| `[{"campo": ""}]` | ACEITO |
| `[""]` | V-01 |
| `["   "]` | ACEITO |
| `["Coluna"]` | ACEITO |
| coluna reconhecivel sem origem em `formato.tabela.colunas` | V-14 |
| coluna plenamente valida por `nivel` | ACEITO |
| coluna plenamente valida por `campo` | ACEITO |
| duas colunas validas | ACEITO |
| mistura de invalida e valida | ACEITO |

Resultado: `H0037-IMPL-QAPP-002` nao foi resolvido integralmente.

## 16. Separacao V-01/V-14

```yaml
V_01:
  significado: nenhuma_coluna_estruturalmente_reconhecivel
V_14:
  significado: coluna_reconhecivel_sem_origem_de_valor
resultado:
  V_01_nao_absorve_V14: parcial
  V_14_nao_aceita_nao_coluna: parcial
  mensagens_distinguiveis: sim_quando_entrada_chega_em_V14
  testes_usam_entradas_distintas: parcialmente
```

Problema no teste novo: `tela/teste_loader.py` caso "V-01 vs V-14" define
`cabecalho = []` e `colunas = [{"titulo": "Sem origem"}]`. A rejeicao observada
e V-01 antes de V-14, mas o teste aceita qualquer `TelaEstruturaInvalida`; logo
o rótulo do teste nao prova a separacao que declara. O teste V-14 posterior com
`cabecalho` valido realmente chega em V-14.

## 17. Testes Adicionados

Resumo dos testes novos auditados:

```yaml
D23-01:
  regra_provada: "nova tela com formato.excesso sem politica rejeita"
  entrada: carregar_tela temporario
  resultado_observado: rejeita
  testa_comportamento_real: true
  apenas_testa_funcao_auxiliar: false
  conforme: true
D23-02:
  regra_provada: "nova tela sem formato.excesso rejeita"
  resultado_observado: rejeita
  conforme: true
D23-03:
  regra_provada: "ID alternativo nao isenta"
  resultado_observado: rejeita
  conforme: true
D23-04:
  regra_provada: "tres H-0036 legadas aceitam"
  resultado_observado: aceita
  conforme: true
  lacuna: "nao cobre os dois IDs H-0035 incluidos no inventario"
D23-05:
  regra_provada: "excesso.modo legado nao substitui politica"
  resultado_observado: rejeita
  conforme: true
D23-06:
  regra_provada: "envelope pre-ADR-0028 preserva comportamento"
  resultado_observado: aceita
  conforme: parcial
  lacuna: "nao prova envelope completo como contrato; nao testa campo isolado"
D23-07:
  regra_provada: "nova tela com politica valida aceita"
  resultado_observado: aceita
  conforme: true
verificacoes_diretas_de_auxiliar:
  testa_funcao_privada: true
  valor: suplementar
  suficiente_sozinha: false
V01_casos_1_a_7b:
  regra_provada: "ausencia/lista sem entrada reconhecivel rejeita"
  resultado_observado: rejeita
  conforme: true
V01_vs_V14:
  regra_provada_declarada: "coluna reconhecivel sem origem rejeita por V-14"
  resultado_observado_independente: "rejeita por V-01 por cabecalho vazio"
  conforme: false
V01_casos_9_10_10b:
  regra_provada: "strings validas e mistura com valida aceitam"
  resultado_observado: aceita
  conforme: parcial
lacunas:
  bypass_por_campo_de_envelope: ausente
  hibrido: ausente
  copia_renomeada_de_H0035: ausente
  valores_vazios_em_objeto_de_cabecalho: ausente
```

Pelo menos parte dos testes atravessa `carregar_tela`. Nao ha dependencia
exclusiva de funcao privada, mas as lacunas acima deixam o patch sem prova
semantica suficiente.

## 18. Preservacao Das Correcoes Anteriores

```yaml
modo_inicial:
  h0037_console_nao_verboso: nao_verboso
  h0037_console_verboso_dois_niveis: verboso_efetivo
  h0037_console_alternavel_tres_niveis: nao_verboso
  h0037_console_tabela_alternavel: verboso
tecla_V:
  telas_fixas: inerte
  telas_alternaveis: reversivel
V_04:
  folha_sem_filhos: aceita
  folha_com_filhos_vazio: rejeitada
  folha_com_filho_real: rejeitada
conteudo_compartilhado:
  identidade: H-0037 conteudo_dois_niveis
  varia_por_tela: false
recalibracoes_launcher:
  resultado_anterior: JUSTIFICADA
regressao_H_0036:
  preservada: true
```

Observacao: `_modo_verboso_de_modelo` retorna `False` para
`somente_verboso`, mas `_verboso_efetivo` aplica a politica fixa e produz
modo efetivo verboso. Nao reabro como achado dentro do escopo deste QA.

## 19. Relatorio IMP-0037

O relatorio registra corretamente:

```yaml
QA_de_origem: sim
dois_achados_tratados: sim
arquivos_alterados: sim
cinco_IDs_legados: sim
10_scripts: sim
2601_verificacoes: sim
zero_falhas: sim
git_diff_check: sim
stage_vazio: sim
commit_ausente: sim
validacao_manual_pendente: sim
ausencia_de_autoaprovacao: sim
```

Nao conforme materialmente:

- declara impossibilidade de bypass por envelope, mas campos isolados de
  envelope ainda contornam D23;
- declara V-01 corrigida, mas objetos de cabecalho com valores vazios sao
  aceitos;
- apresenta como regra suficiente que qualquer campo de envelope tira o console
  do escopo D23, sem autoridade para estruturas hibridas.

## 20. Suite Independente

Executada pelo QA com `PYTHONDONTWRITEBYTECODE=1`:

| Script | Verificacoes | Falhas | Codigo |
|---|---:|---:|---:|
| `tela/teste_loader.py` | 419 | 0 | 0 |
| `tela/teste_modelo.py` | 186 | 0 | 0 |
| `tela/teste_renderizador.py` | 1223 | 0 | 0 |
| `tela/teste_distribuicao_matricial.py` | 36 | 0 | 0 |
| `demo/teste_demo.py` | 363 | 0 | 0 |
| `demo/teste_diagnostico.py` | 48 | 0 | 0 |
| `demo/teste_demo_distribuicao.py` | 109 | 0 | 0 |
| `demo/teste_explorar_barra_de_menus.py` | 38 | 0 | 0 |
| `demo/teste_demo_console.py` | 116 | 0 | 0 |
| `demo/teste_demo_console_modos.py` | 63 | 0 | 0 |
| **Total** | **2601** | **0** | **0** |

A suite verde nao e prova suficiente de conformidade semantica.

## 21. Smoke Tecnico

Smokes nao interativos executados:

```yaml
h0037_console_nao_verboso:
  codigo_saida: 0
  modo_efetivo: nao_verboso
  chip_V: ausente
h0037_console_verboso_dois_niveis:
  codigo_saida: 0
  modo_efetivo: verboso
  chip_V: ausente
h0037_console_alternavel_tres_niveis:
  codigo_saida: 0
  modo_efetivo: nao_verboso
  chip_V: presente
h0037_console_tabela_alternavel:
  codigo_saida: 0
  modo_efetivo: verboso
  chip_V: presente
```

Isto nao e aprovacao visual manual.

## 22. Validacao Manual

Permanece:

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

Este QA nao executou validacao humana, nao simulou aprovacao visual, nao criou
relatorio de validacao manual e nao liberou fechamento.

## 23. Achados

### H0037-IMPL-QAPP2-001

```yaml
id: H0037-IMPL-QAPP2-001
arquivo: tela/loader.py
funcao_ou_teste: _console_em_escopo_d23
evidencia: "campos isolados como itens, origem_dados, politica_exibicao ou politica_navegacao fazem a funcao retornar fora_de_D23; telas temporarias novas sem politica foram aceitas ao adicionar esses campos"
autoridade: "contrato_json_console.md 13.13; contrato_tela_json.md 33.6; regra do prompt D23-E/D23-F"
severidade: alta
tipo: DEFEITO_IMPLEMENTACAO
impacto: "tela nova sujeita a D23 consegue contornar politica_modo apenas adicionando campo de envelope; hibridos sao aceitos sem autoridade"
correcao_exigida: "validar envelope completo ou rejeitar hibrido; nao usar presenca isolada de campo como isencao D23"
```

### H0037-IMPL-QAPP2-002

```yaml
id: H0037-IMPL-QAPP2-002
arquivo: tela/loader.py; tela/teste_loader.py
funcao_ou_teste: _coluna_reconhecivel; teste V-01 vs V-14
evidencia: "[{\"titulo\": null}], [{\"titulo\": \"\"}], [{\"nivel\": null}], [{\"campo\": null}], [{\"campo\": \"\"}] e [\"   \"] foram aceitos; teste rotulado V-01 vs V-14 rejeita por V-01 devido cabecalho vazio"
autoridade: "contrato_json_console.md 13.9 V-01/V-14; exigencia do prompt de nao aceitar chave com valor semanticamente vazio sem autoridade expressa"
severidade: alta
tipo: DEFEITO_IMPLEMENTACAO
impacto: "cabecalho sem coluna semanticamente valida pode passar; a separacao V-01/V-14 fica parcialmente nao comprovada"
correcao_exigida: "exigir valores semanticamente nao vazios para a forma reconhecivel e ajustar teste para distinguir V-01 de V-14 por mensagem/entrada"
```

## 24. Conclusao

O segundo patch melhorou D23 ao rejeitar consumidores novos que omitem
`formato.excesso` e justificou adequadamente a inclusao das duas telas H-0035
no inventario legado. Entretanto, os dois achados altos ainda nao estao
resolvidos integralmente:

- D23 ainda possui bypass por campo isolado de envelope e aceita estruturas
  hibridas sem autoridade;
- V-01 ainda aceita colunas com valores semanticamente vazios, e um teste
  declara V-14 sem de fato provar V-14 naquele caso.

## 25. Status Literal

```text
IMPLEMENTATION_PATCH_REQUIRED
```

## 26. Status Normalizado

```text
REPROVADO_PATCH_NECESSARIO
```

## 27. Proxima Categoria

```yaml
proxima_categoria: PATCH_IMPLEMENTACAO
implementacao_aprovada: false
```
