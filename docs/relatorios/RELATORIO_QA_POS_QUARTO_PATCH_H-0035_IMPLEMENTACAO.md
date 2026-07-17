---
id: RELATORIO_QA_POS_QUARTO_PATCH_H-0035_IMPLEMENTACAO
tipo: qa_implementacao
handoff: H-0035
rodada: POS_QUARTO_PATCH
data: 2026-07-17
status_literal: I5_MANUAL_VALIDATION_REQUIRED
status_normalizado: MANUAL_VALIDATION_REQUIRED
---

# RELATORIO QA POS QUARTO PATCH H-0035 IMPLEMENTACAO

## 1. Identificacao

Etapa executada: `QA_POS_PATCH`.

Rodada auditada:

```text
POS_QUARTO_PATCH
```

Relatorio criado nesta etapa:

```text
docs/relatorios/RELATORIO_QA_POS_QUARTO_PATCH_H-0035_IMPLEMENTACAO.md
```

Este QA nao corrigiu codigo, testes, JSONs, demos, contratos, ADRs, handoff,
indices, nomenclatura, relatorios anteriores ou relatorio de implementacao.
Nenhum commit foi preparado ou executado. A validacao visual em TTY real nao foi
realizada por este QA.

## 2. Objetivo

Auditar exclusivamente os achados metodologicos do quarto patch:

```text
VM-H0035-METODO-ALTO-001
VM-H0035-METODO-MEDIO-001
VM-H0035-METODO-MEDIO-002
```

Confirmar tambem ausencia de regressao em:

```text
VM-H0035-IMP-ALTO-001
VM-H0035-IMP-MEDIO-001
QA-H0035-IMP-ALTO-001
QA-H0035-IMP-MEDIO-001
QA-H0035-POS-PATCH-BAIXO-001
QA-H0035-IMP-BAIXO-001
```

## 3. Autoridades lidas

Lidos integralmente:

```text
docs/handoff/H-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
docs/relatorios/IMP-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
docs/relatorios/RELATORIO_QA_H-0035_IMPLEMENTACAO.md
docs/relatorios/RELATORIO_QA_POS_PATCH_H-0035_IMPLEMENTACAO.md
docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0035_IMPLEMENTACAO.md
docs/relatorios/RELATORIO_QA_POS_TERCEIRO_PATCH_H-0035_IMPLEMENTACAO.md
```

Arquivos atuais lidos ou auditados materialmente:

```text
config/telas/demo/h0035_*.json
config/telas/demo/h0035_catalogo.json
demo/demo_distribuicao.py
demo/teste_demo_distribuicao.py
demo/teste_diagnostico.py
```

Contratos e ADR-0025 foram consultados apenas para confirmar vocabulario,
limite de texto do lancador, preservacao de ausencia do campo e ausencia de
semantica nova.

## 4. Estado Git inicial

Comandos executados antes da criacao deste relatorio:

```text
git status --short
git diff --stat
git diff --name-only
git diff --check
git diff --cached --name-only
```

Resultado material:

```yaml
arquivos_rastreados_modificados:
  implementacao_H0035_ou_patches:
    - demo/teste_diagnostico.py
    - tela/loader.py
    - tela/modelo.py
    - tela/renderizador.py
    - tela/teste_loader.py
    - tela/teste_modelo.py
    - tela/teste_renderizador.py
  documentais_preexistentes_do_ciclo_ADR0025:
    - docs/NOMENCLATURA.md
    - docs/adr/INDICE_ADR.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_json_console.md
    - docs/contratos/contrato_json_dashboard.md
    - docs/contratos/contrato_json_lancador.md
    - docs/contratos/contrato_lancador.md
    - docs/contratos/contrato_tela_json.md
arquivos_nao_rastreados:
  configuracoes_h0035: 26
  codigo_demo_teste_h0035:
    - demo/demo_distribuicao.py
    - demo/teste_demo_distribuicao.py
    - tela/distribuicao_matricial.py
    - tela/teste_distribuicao_matricial.py
  documentos_do_ciclo:
    - docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
    - docs/handoff/H-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
    - docs/relatorios/IMP-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md
    - docs/relatorios/RELATORIO_QA_ADR-0025.md
    - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0025.md
    - docs/relatorios/RELATORIO_QA_H-0035_HANDOFF.md
    - docs/relatorios/RELATORIO_QA_H-0035_IMPLEMENTACAO.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0025.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0025.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_H-0035_HANDOFF.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_H-0035_IMPLEMENTACAO.md
    - docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0035_IMPLEMENTACAO.md
    - docs/relatorios/RELATORIO_QA_POS_TERCEIRO_PATCH_H-0035_IMPLEMENTACAO.md
  temporarios_ja_presentes_no_inicio:
    - demo/__pycache__/
    - tela/__pycache__/
stage: vazio
git_diff_check: limpo
git_diff_cached: vazio
```

Para os arquivos inesperados ou fora do escopo focal do quarto patch:

```yaml
origem: NAO_CONFIRMADA
produzido_pelo_executor: NAO_CONFIRMADO
produzido_pelo_usuario: NAO_CONFIRMADO
```

`git diff --name-only` lista apenas os 15 rastreados modificados e nao cobre os
arquivos nao rastreados. A correspondencia com o escopo autorizado do quarto
patch foi avaliada por leitura direta dos arquivos nao rastreados e do relatorio
de implementacao.

## 5. Escopo do quarto patch

Arquivos efetivamente atribuiveis ao quarto patch por declaracao do relatorio de
implementacao e por leitura material:

```yaml
configuracoes_json:
  - config/telas/demo/h0035_catalogo.json
  - config/telas/demo/h0035_pref_linhas.json
  - config/telas/demo/h0035_pref_colunas.json
  - config/telas/demo/h0035_matriz_fixa_cabe.json
  - config/telas/demo/h0035_matriz_fixa_quadro_minimo.json
  - config/telas/demo/h0035_centralizado_h_colunas.json
  - config/telas/demo/h0035_esquerda_margens_min_max.json
  - config/telas/demo/h0035_h_uniforme.json
  - config/telas/demo/h0035_h_margens_limitadas.json
  - config/telas/demo/h0035_v_margens_min.json
  - config/telas/demo/h0035_v_margens_min_max.json
  - config/telas/demo/h0035_v_uniforme.json
  - config/telas/demo/h0035_resto_horizontal.json
  - config/telas/demo/h0035_resto_vertical.json
  - config/telas/demo/h0035_console_com.json
  - config/telas/demo/h0035_lancador_com.json
  - config/telas/demo/h0035_dashboard_com.json
demo_e_testes:
  - demo/demo_distribuicao.py
  - demo/teste_demo_distribuicao.py
  - demo/teste_diagnostico.py
relatorio_de_implementacao:
  - docs/relatorios/IMP-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
arquivos_criados_pelo_quarto_patch: []
arquivos_proibidos_atribuidos_ao_quarto_patch: []
```

O arquivo rastreado `demo/teste_diagnostico.py` foi alterado apenas no caso
`h0035_matriz_fixa_cabe`, usando pipeline direto com `largura=80, altura=30`.
A alteracao esta diretamente relacionada a fixture 3x4, pois a largura padrao
42 nao comporta quatro colunas de 13 caracteres.

## 6. Catalogo canonico

`config/telas/demo/h0035_catalogo.json` possui exatamente 25 itens e 25 comandos
unitarios, unicos, sem `10`-`25`.

Mapeamento confirmado:

```yaml
"1": h0035_pref_linhas
"2": h0035_pref_colunas
"3": h0035_matriz_fixa_cabe
"4": h0035_matriz_fixa_quadro_minimo
"5": h0035_centralizado_h_colunas
"6": h0035_esquerda_margens_min_max
"7": h0035_h_uniforme
"8": h0035_h_margens_limitadas
"9": h0035_v_margens_min
"A": h0035_v_margens_min_max
"B": h0035_v_uniforme
"C": h0035_um_centralizado
"D": h0035_tres_centralizados
"E": h0035_quatro_centralizados
"F": h0035_minimo_fixo_excedido
"G": h0035_uma_linha
"H": h0035_uma_coluna
"I": h0035_resto_horizontal
"J": h0035_resto_vertical
"K": h0035_console_com
"L": h0035_console_sem
"M": h0035_lancador_com
"N": h0035_lancador_sem
"O": h0035_dashboard_com
"P": h0035_dashboard_sem
```

O texto mais longo dos itens tem 15 caracteres. O limite decorre do contrato do
lancador (`verificacao.texto.max_caracteres == 15`) e nao de schema novo criado
por H-0035. Os titulos curtos nao substituem a identidade completa: as
descricoes do cabecalho e `descrever_tela` preservam objetivo, formacao, ordem,
consumidor e politicas.

## 7. Identidade detalhada

`descrever_tela` foi estendido para retornar:

```yaml
nome:
familia:
formacao:
ordem:
consumidor:
politica_horizontal:
politica_vertical:
objetivo:
tecla:
estado:
```

Os dados sao obtidos do modelo carregado e da configuracao efetiva. A tecla de
catalogo nao e derivavel apenas do modelo da tela de destino; por isso
`descrever_tela` retorna `tecla: n/a`. O comando real permanece no catalogo.

Exemplos materiais:

| tecla catalogo | nome | formacao | ordem | consumidor | pol_h | pol_v | objetivo resumido |
|---|---|---|---|---|---|---|---|
| 1 | h0035_pref_linhas | preferencia_linhas | por_linha | dashboard | inicio | inicio | 12 partic. pref_linhas |
| 3 | h0035_matriz_fixa_cabe | 3x4 | por_linha | dashboard | uniforme | uniforme | matriz fixa 3x4 H+V |
| 7 | h0035_h_uniforme | preferencia_linhas | por_linha | dashboard | uniforme | inicio | politica horizontal uniforme |
| B | h0035_v_uniforme | preferencia_linhas | por_linha | dashboard | inicio | uniforme | politica vertical uniforme |
| K | h0035_console_com | preferencia_colunas | por_linha | console | inicio | inicio | console com DM |
| P | h0035_dashboard_sem | n/a | n/a | dashboard | n/a | n/a | dashboard sem DM |

## 8. Participantes

Tabela de cardinalidade das fixtures alteradas ou relevantes:

| fixture | participantes esperados | participantes encontrados | rotulos distintos | resultado |
|---|---:|---:|---:|---|
| h0035_pref_linhas | >=12 | 12 | 12 | PASS |
| h0035_pref_colunas | >=12 | 12 | 12 | PASS |
| h0035_matriz_fixa_cabe | 12 | 12 | 12 | PASS |
| h0035_matriz_fixa_quadro_minimo | 16 | 16 | 16 | PASS |
| h0035_centralizado_h_colunas | >=12 | 12 | 12 | PASS |
| h0035_esquerda_margens_min_max | >=12 | 12 | 12 | PASS |
| h0035_h_uniforme | >=12 | 12 | 12 | PASS |
| h0035_h_margens_limitadas | >=12 | 12 | 12 | PASS |
| h0035_v_margens_min | >=12 | 12 | 12 | PASS |
| h0035_v_margens_min_max | >=12 | 12 | 12 | PASS |
| h0035_v_uniforme | >=12 | 12 | 12 | PASS |
| h0035_resto_horizontal | 7 | 7 | 7 | PASS |
| h0035_resto_vertical | 7 | 7 | 7 | PASS |
| h0035_console_com | >=12 | 12 | 12 | PASS |
| h0035_lancador_com | >=12 | 12 | 12 | PASS |
| h0035_dashboard_com | >=12 | 12 | 12 | PASS |

Fixtures nominais preservadas:

```yaml
h0035_um_centralizado: 1
h0035_tres_centralizados: 3
h0035_quatro_centralizados: 4
```

Os dashboards ampliados usam rotulos sequenciais `P01` a `P12` ou `P16`; os
restos usam `P01` a `P07`. Nao foram observados participantes perdidos,
duplicados ou fora de ordem.

## 9. Geometria e metodo manual

Resultados materiais do teste `teste_fixtures_geometria`:

```yaml
pref_linhas:
  tamanho_amplo: 120x22
  geometria_ampla: [2, 6]
  tamanho_reduzido: 78x22
  geometria_reduzida: [3, 4]
  tamanho_minimo: n/a
  estado_minimo: normal
pref_colunas:
  tamanho_amplo: 78x22
  geometria_ampla: [12, 1]
  tamanho_reduzido: 78x4
  geometria_reduzida: [4, 3]
  tamanho_minimo: n/a
  estado_minimo: normal
matriz_fixa_cabe:
  amplo: 100x20 -> formacao [3, 4], x0=9, y_linha2=9
  reduzido: 70x10 -> formacao [3, 4], x0=3, y_linha2=4
  politica_horizontal: uniforme
  politica_vertical: uniforme
matriz_fixa_quadro_minimo:
  pequeno: 40x10 -> fallback=true
  amplo: 120x40 -> formacao [4, 4]
  determinismo: confirmado em segunda reducao e segunda recuperacao
h_uniforme:
  formacao: [3, 4]
  x_100: 9
  x_70: 3
v_uniforme:
  formacao: [4, 3]
  y_30: 11
  y_15: 5
resto_horizontal:
  formacao: [1, 7]
  vao_h0: 3
  margem_esq: 2
resto_vertical:
  formacao: [3, 3]
  margem_sup: 5
  margem_inf: 4
```

O teste possui 45 chamadas estaticas a `_registrar`. Na execucao verde, a secao
emite 44 verificacoes porque uma chamada e ramo de falha individual de contagem;
o script completo confirma 99 verificacoes, contra 54 da rodada anterior.

Classificacao do inventario:

```yaml
teste_fixtures_geometria:
  verificacoes_declaradas: 45
  verificacoes_reais:
    chamadas_estaticas_registrar_na_funcao: 45
    emitidas_na_execucao_verde_da_secao: 44
    incremento_total_do_script: 45
  valores_independentes: sim
  chama_motor_para_esperado: nao
  chama_motor_para_obtido: sim
  estados_amplos: cobertos
  estados_reduzidos: cobertos
  estados_minimos: cobertos_para_matriz_4x4
  propriedades_nao_cobertas: nenhuma_bloqueante_observada
```

O metodo manual pos-quarto-patch ficou tecnicamente reproduzivel: o catalogo
permite percorrer `1,2,3,4,5,6,7,8,9,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P`, com
identidade e objetivo suficientes para saber a propriedade a observar. A
pendencia remanescente e repetir a validacao humana em TTY real.

## 10. Consumidores com e sem campo

Comparacao dos pares:

```yaml
console:
  com: h0035_console_com, 12 itens, possui distribuicao_matricial
  sem: h0035_console_sem, 2 itens, sem distribuicao_matricial
lancador:
  com: h0035_lancador_com, 12 itens, possui distribuicao_matricial
  sem: h0035_lancador_sem, 3 itens, sem distribuicao_matricial
dashboard:
  com: h0035_dashboard_com, 12 campos, possui distribuicao_matricial
  sem: h0035_dashboard_sem, 3 campos, sem distribuicao_matricial
```

As fixtures `sem` nao receberam `distribuicao_matricial` e preservam o
comportamento historico. Nao foi observada correcao silenciosa do H-0034.

## 11. Ajuste em demo/teste_diagnostico.py

Classificacao:

```yaml
teste_diagnostico:
  alteracao_necessaria: true
  dentro_da_autorizacao: true
  prova_fortalecida_ou_preservada: preservada
  acomodacao_cega: false
```

Evidencia: somente `h0035_matriz_fixa_cabe` usa pipeline direto
`carregar_tela -> construir_modelo -> renderizar_tela` com `largura=80,
altura=30`. O teste continua verificando identidade material (`H0035 MATRIZ
3X4`) e nao usa largura derivada do proprio resultado. Nao houve `skip`,
exclusao de assercao ou reducao de cobertura.

## 12. Pseudo-TTY

`demo/teste_demo_distribuicao.py` usa `pty.openpty`, `TIOCSWINSZ`, tecla unica e
entrada sem Enter. A selecao sequencial cobre todas as 25 telas, incluindo no
minimo:

```text
1 2 3 4 7 B K L M N O P
```

Tambem ha prova de reducao para quadro minimo e recuperacao por ampliacao na
tela `h0035_pref_linhas`. Pseudo-TTY nao substitui observacao humana.

## 13. Validacao dos JSONs

Comando executado para cada `config/telas/demo/h0035_*.json`:

```text
python -m json.tool <arquivo>
```

Resultado:

```yaml
jsons_h0035_verificados: 26
jsons_sintaticamente_validos: 26
jsons_carregados_pelo_loader_real: 26
jsons_invalidos: []
```

## 14. Testes focais

```yaml
pytest_demo_distribuicao:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_demo_distribuicao.py -q --tb=short
  collected: 13
  passed: 13
  failed: 0
  skipped: 0
  warnings: 0
script_demo_distribuicao:
  comando: PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo_distribuicao.py
  verificacoes: 99
  falhas: 0
diagnostico:
  comando: PYTHONDONTWRITEBYTECODE=1 python demo/teste_diagnostico.py
  verificacoes: 41
  falhas: 0
```

Smoke:

```yaml
comando: PYTHONDONTWRITEBYTECODE=1 python demo/demo_distribuicao.py
exit_code: 0
identidade_material:
  nome: h0035_catalogo
  consumidor: lancador
  estado: normal
chips_visiveis: 1-9 e A-P
```

## 15. Suite canonica

Oito scripts executados da raiz:

```yaml
tela/teste_loader.py: 303
tela/teste_modelo.py: 169
tela/teste_renderizador.py: 1191
tela/teste_distribuicao_matricial.py: 36
demo/teste_demo.py: 358
demo/teste_diagnostico.py: 41
demo/teste_demo_distribuicao.py: 99
demo/teste_explorar_barra_de_menus.py: 38
total: 2235
falhas: 0
```

## 16. Preservacao dos patches anteriores

Confirmado:

```yaml
fronteira_interna_do_participante: preservada
conteudo_integral_entregue_ao_helper: preservado
ausencia_de_truncamento_na_camada_externa: preservada
teste_com_spy: preservado
contagem_31_arquivos_criados_no_ciclo: preservada
comandos_catalogo_um_caractere: preservados
normalizacao_local_maiusculas_minusculas: preservada
H0034_corrigido_silenciosamente: false
```

Evidencia adicional: `tela/teste_renderizador.py` passou com 1191 verificacoes;
`_linhas_distribuicao_matricial` continua chamando
`_renderizar_participante_na_celula`, e a condicao `cx < cel_x_fim` permanece
apenas na fronteira interna.

## 17. Item futuro sem numero (criterio retificado)

A primeira versao deste QA buscou, no relatorio de implementacao, o item futuro:

```text
fornecimento externo de dados aos elementos de tela
```

Resultado da busca material:

```yaml
busca_executada:
  - fornecimento externo
  - FORA_DO_ESCOPO_H0035
  - NAO_ATRIBUIDO
  - implementado
  - dados aos elementos
registro_encontrado: nenhum
implementacao_antecipada_observada: false
```

Tambem nao foi encontrada evidencia de implementacao antecipada desse item:

```yaml
novo_handoff: nao_observado
reserva_de_numero: nao_observada
arquivo_de_runtime: nao_observado
leitura_externa_de_JSON: nao_observado
alteracao_do_lancador_produtivo: nao_observado
campo_novo_nos_JSONs_estruturais: nao_observado
codigo_antecipado: nao_observado
```

A ausencia de implementacao antecipada esta adequada e permanece correta.

A ausencia de registro no relatorio de implementacao **nao e defeito**: o item
futuro nao pertence ao escopo do H-0035 (decisao do usuario, registrada na secao
sobre a retificacao do criterio gerencial). O tratamento futuro do item sera
formalizado por ADR em outro ciclo.

## 18. Retificacao de criterio gerencial

A primeira versao deste QA classificou o resultado como
`I2_IMPLEMENTATION_PATCH_REQUIRED` porque o relatorio de implementacao nao
registrava o item futuro "fornecimento externo de dados aos elementos de tela".
Esse criterio foi introduzido incorretamente pelo prompt gerencial do QA e nao
possui autoridade documental valida para o escopo do H-0035.

```yaml
criterio_invalido:
  origem: prompt_gerencial_do_QA
  descricao: exigencia_de_registrar_item_futuro_no_IMP_0035
  autoridade_documental: inexistente
  autorizado_pelo_usuario: false
  efeito_original: classificacao_I2
  tratamento: criterio_revogado

responsabilidade:
  implementador: nenhuma
  auditor: nenhuma_por_ter_seguido_o_prompt_recebido
  gerente: criterio_incorreto_introduzido_no_prompt
```

Nao se atribui o erro ao executor da implementacao. Nao se atribui o erro ao
auditor, que seguiu o criterio recebido.

Decisao do usuario registrada apenas como contexto desta retificacao (este
registro nao cria ADR, nao insere o requisito no sistema e nao cria/reservar
handoff):

```yaml
decisao_do_usuario:
  item: fornecimento_externo_de_dados_aos_elementos_de_tela
  tratamento: ADR_FUTURA
  pertence_ao_H0035: false
  deve_constar_no_IMP_0035: false
  implementacao_atual: nao_autorizada
  handoff_futuro: nao_criado
  numero_reservado: false
```

Efeito da retificacao:

```yaml
classificacao_anterior:
  status: I2_IMPLEMENTATION_PATCH_REQUIRED
  resultado: RETIFICADO
  motivo: baseado_em_criterio_gerencial_sem_autoridade
status_vigente:
  status_literal: I5_MANUAL_VALIDATION_REQUIRED
  status_normalizado: MANUAL_VALIDATION_REQUIRED
```

O item futuro foi removido de achados bloqueantes, achados altos, achados medios,
achados baixos obrigatorios, condicoes para `I2` e da conclusao de patch
necessario. O achado `QA-H0035-POS-QUARTO-PATCH-BAIXO-001` e desconsiderado como
defeito de fidelidade.

## 19. Fidelidade do relatorio de implementacao

Confirmado na secao do quarto patch:

```yaml
validacao_recebida: sim
normalizacao_para_inconclusiva: sim
ausencia_de_falha_funcional_confirmada: sim
tres_achados_metodologicos: sim
arquivos_alterados: sim
participantes_por_fixture: sim
ordem_canonica: sim
identidade_detalhada: sim
H_V_combinado: sim
45_verificacoes: parcialmente_fiel
ajuste_do_diagnostico: sim
suite_real: sim
nenhum_arquivo_criado: sim
stage_vazio: sim
validacao_manual_pendente: sim
item_futuro_sem_numero: ausente_nao_e_defeito
```

A linha `item_futuro_sem_numero: ausente_nao_e_defeito` registra apenas o fato
material de que o item futuro nao consta do `IMP-0035`. Apos a retificacao da
secao 18, essa ausencia nao e defeito de fidelidade, porque o item nao pertence
ao escopo do H-0035.

Nota sobre as 45 verificacoes: o relatorio e fiel quanto ao incremento total do
script `demo/teste_demo_distribuicao.py` de 54 para 99. A funcao
`teste_fixtures_geometria` contem 45 chamadas estaticas a `_registrar`, mas a
execucao verde emite 44 verificacoes nessa secao porque uma chamada e ramo de
falha. Isso nao altera o resultado funcional do QA.

## 20. Reavaliacao dos achados metodologicos

```yaml
VM-H0035-METODO-ALTO-001:
  resultado: CORRIGIDO
  evidencia: >
    Fixtures relevantes foram ampliadas para 12 participantes, matriz 4x4 tem
    16 participantes, restos tem 7 participantes, e rotulos sequenciais
    distinguem ordem, perda e duplicacao.
VM-H0035-METODO-MEDIO-001:
  resultado: CORRIGIDO
  evidencia: >
    Catalogo tem 25 itens em ordem canonica, comandos unitarios 1-9/A-P,
    ausencia de 10-25, textos ate 15 caracteres e selecao integral testada.
VM-H0035-METODO-MEDIO-002:
  resultado: CORRIGIDO
  evidencia: >
    H uniforme, V uniforme e matriz 3x4 H+V tem politicas identificaveis por
    identidade e coordenadas; pares com/sem DM distinguem consumidores.
```

## 21. Achados anteriores

```yaml
VM-H0035-IMP-ALTO-001:
  resultado: PRESERVADO_CORRIGIDO
  evidencia: catalogo permanece com comandos de um caractere e PTY cobre 27 teclas.
VM-H0035-IMP-MEDIO-001:
  resultado: PRESERVADO_CORRIGIDO
  evidencia: teste de catalogo preserva 25 selecoes, fronteiras e regressao de prefixos.
QA-H0035-IMP-ALTO-001:
  resultado: PRESERVADO_CORRIGIDO
  evidencia: helper interno recebe conteudo integral; suite renderizador 1191 PASS.
QA-H0035-IMP-MEDIO-001:
  resultado: PRESERVADO_CORRIGIDO
  evidencia: teste com spy e teste de fronteira interna permanecem ativos.
QA-H0035-POS-PATCH-BAIXO-001:
  resultado: PRESERVADO_CORRIGIDO
  evidencia: contagens atuais coerentes; renderizador 1191, demo_distribuicao 99.
QA-H0035-IMP-BAIXO-001:
  resultado: PRESERVADO_CORRIGIDO
  evidencia: total real de arquivos criados no ciclo permanece 31; quarto patch criou 0.
```

## 22. Achado novo (retificado)

A primeira versao deste QA registrou o achado
`QA-H0035-POS-QUARTO-PATCH-BAIXO-001`, fundamentado no criterio gerencial
invalido de exigir o registro do item futuro no `IMP-0035`. Apos a retificacao da
secao 18, esse achado e desconsiderado como defeito de fidelidade.

```yaml
achado_retificado:
  id: QA-H0035-POS-QUARTO-PATCH-BAIXO-001
  fundamento: criterio_gerencial_sem_autoridade
  tratamento: desconsiderado_como_defeito_de_fidelidade
  nao_ha_outro_achado_novo_neste_patch: true
```

Nao existe outro achado novo, bloqueante, alto, medio ou baixo obrigatorio neste
patch.

```yaml
achados_bloqueantes: []
achados_altos: []
achados_medios: []
achados_baixos: []
```

## 23. Estado Git final deste QA

Antes da escrita deste relatorio, `git diff --check` e
`git diff --cached --name-only` estavam limpos/vazios. O unico arquivo criado
pela rodada original deste QA e este relatorio. A retificacao posterior alterou
apenas este relatorio.

```yaml
codigo_testes_jsons_demos_alterados_pelo_QA: false
relatorio_implementacao_alterado_pelo_QA: false
stage: vazio
commit: nao_realizado
```

## 24. Conclusao

Os tres achados metodologicos do quarto patch estao corrigidos. O metodo manual
agora e sequencial, as fixtures tem cardinalidade suficiente, H/V/combinado sao
identificaveis por identidade e por coordenadas, e nao houve regressao
automatizada nos achados tecnicos anteriores, que permanecem corrigidos. A suite
canonica passou com 2235 verificacoes e 0 falhas, e os 26 JSONs do H-0035 foram
validados sintaticamente e carregados pelo loader real.

Nao existe patch tecnico nem patch documental pendente dentro do H-0035. O item
futuro "fornecimento externo de dados aos elementos de tela" nao integra este
ciclo: sua ausencia do `IMP-0035` nao e defeito e seu tratamento sera formalizado
por ADR em outro ciclo, sem criacao ou reserva de handoff nesta etapa.

A unica pendencia do H-0035 e repetir a validacao humana em TTY real.

## 25. Status literal

```text
I5_MANUAL_VALIDATION_REQUIRED
```

## 26. Status normalizado

```text
MANUAL_VALIDATION_REQUIRED
```

## 27. Proxima categoria

```text
VALIDACAO_MANUAL
```
