---
name: RELATORIO_QA_POS_PATCH_H-0037_IMPLEMENTACAO
description: Auditoria independente pos-patch da implementacao do H-0037
handoff: H-0037
status_literal: IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: REPROVADO_PATCH_NECESSARIO
proxima_categoria: PATCH_IMPLEMENTACAO
---

# Relatorio de QA pos-patch da implementacao do H-0037

## 1. Identificacao

| Campo | Valor |
|---|---|
| Projeto | Orquestrador |
| Etapa executada | QA_POS_PATCH_IMPLEMENTACAO |
| Handoff | `docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md` |
| QA anterior | `docs/relatorios/RELATORIO_QA_H-0037_IMPLEMENTACAO.md` |
| Relatorio de implementacao | `docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md` |
| Resultado | `IMPLEMENTATION_PATCH_REQUIRED` |

## 2. Objetivo

Auditar se o patch declarado como `IMPLEMENTATION_PATCHED` resolveu
integralmente os achados do QA anterior da implementacao do H-0037. Nenhum
codigo, teste, JSON ou documento foi corrigido por este QA, exceto a criacao
deste relatorio.

## 3. Autoridades

Lidos integralmente:

```yaml
docs/relatorios/RELATORIO_QA_H-0037_IMPLEMENTACAO.md: 504 linhas
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md: 470 linhas
docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md: 1718 linhas
docs/relatorios/RELATORIO_QA_POS_PATCH_H-0037_HANDOFF.md: 608 linhas
docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md: 1476 linhas
docs/contratos/contrato_json_console.md: 1258 linhas
docs/contratos/contrato_console.md: 839 linhas
docs/contratos/contrato_tela_json.md: 1469 linhas
docs/contratos/contrato_barra_de_menus.md: 827 linhas
docs/contratos/contrato_composicao_corpo.md: 1947 linhas
```

Autoridades decisivas:

- ADR-0028 D23: telas novas ou revisadas devem declarar politica de modo; ausencia e invalida; default implicito e proibido.
- `contrato_json_console.md` §13.13.1, §13.13.3, §13.13.6 e §13.13.8: `formato.excesso.politica_modo` e obrigatorio para telas novas/revisadas, enquanto H-0036 permanece legado nominal sem inferencia.
- ADR-0028 §33 e `contrato_json_console.md` §13.9: V-01 a V-15 sao validacoes obrigatorias do loader.
- H-0037 §13.4: `h0037_console_tabela_alternavel` abre em modo verboso.

## 4. Estado Git

Comandos executados na raiz real do repositorio:

```yaml
branch: master
head: f6982d08640af1762b8e0e8814b6e90c9421538e
log_1: "f6982d0 docs: corrige whitespace do fechamento H-0036"
stage: vazio
git_diff_check: sem_erros
commit_novo: inexistente
scripts_dir: ausente
```

O prompt indicava `scripts/` como diretorio operacional, mas o checkout atual
nao possui esse diretorio. A suite foi executada a partir da raiz, onde existem
`tela/`, `demo/`, `config/` e `docs/`.

Arquivos rastreados modificados:

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
docs/relatorios/RELATORIO_QA_H-0037_IMPLEMENTACAO.md
docs/relatorios/RELATORIO_QA_POS_PATCH_H-0037_HANDOFF.md
```

Documentacao acumulada anterior: ha varios relatorios ADR-0028 e documentos de
contrato/handoff no workspace. Nao atribuo origem sem evidencia. Artefatos
transitorios encontrados e nao limpos: `tela/__pycache__/*` e
`demo/__pycache__/*`.

## 5. Inventario Do Patch

O executor declarou correcoes em:

```text
demo/demo.py
tela/loader.py
tela/teste_loader.py
demo/teste_demo_console_modos.py
config/telas/demo/h0037_dois_niveis_conteudo.json
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
```

Inventario real: os arquivos acima foram alterados/criados e ha tambem outros
arquivos modificados no workspace, incluindo `tela/modelo.py`,
`tela/renderizador.py`, testes historicos, `demo/teste_demo.py`,
`demo/teste_demo_console.py`, `demo/teste_diagnostico.py`, contratos,
`docs/NOMENCLATURA.md` e `docs/adr/INDICE_ADR.md`.

Arquivos fora do escopo nominal tecnico:

```yaml
docs/NOMENCLATURA.md:
  alteracao: modificado
  autorizacao: fora da lista declarada do patch tecnico; possivelmente acumulado documental
  impacto: deve permanecer registrado
  classificacao: observacao
docs/adr/INDICE_ADR.md:
  alteracao: modificado
  autorizacao: fora da lista declarada do patch tecnico; possivelmente acumulado documental
  impacto: deve permanecer registrado
  classificacao: observacao
docs/contratos/contrato_*.md:
  alteracao: modificados
  autorizacao: fora da lista declarada do patch tecnico; documentos de autoridade ja existentes no workspace
  impacto: base normativa lida, mas nao atribuida ao executor sem evidencia
  classificacao: observacao
tela/modelo.py e tela/renderizador.py:
  alteracao: modificados
  autorizacao: autorizados pelo handoff, mas fora do resumo curto do patch recebido
  impacto: parte da implementacao H-0037
  classificacao: escopo_tecnico_autorizado_no_handoff
__pycache__:
  alteracao: arquivos transitorios nao rastreados
  autorizacao: nao autorizados como artefatos finais
  impacto: higiene de workspace, nao alterado por este QA
  classificacao: transitorio
```

## 6. Integridade

```yaml
python_ast:
  arquivos_verificados: 11
  resultado: VALIDO
json:
  arquivos_verificados: 8
  resultado: VALIDO
conflitos:
  marcadores_git_reais: AUSENTES
  observacao: busca literal ampla encontra separadores comentados em teste_renderizador e citacao documental antiga, nao conflitos
temporarios:
  encontrados:
    - tela/__pycache__
    - demo/__pycache__
  limpos_pelo_QA: false
git_diff_check: sem_erros
```

## 7. Escopo

Nao houve stage, commit, push, validacao visual manual nem limpeza de arquivos.
O patch nao deve ser considerado completo porque ainda ha defeitos corrigiveis
em D23 e V-01.

## 8. H0037-IMPL-QA-001

Achado anterior: modo inicial por `argv` nao aplicado antes da primeira
renderizacao real.

Resultado pos-patch: resolvido.

Evidencias:

- `demo/demo.py:658-659` carrega o modelo inicial e aplica
  `_modo_verboso_de_modelo(modelo)` antes dos ramos TTY e nao-TTY.
- Smoke tecnico direto de `python demo/demo.py h0037_console_tabela_alternavel`
  mostra linhas verbosas da tabela na primeira renderizacao.
- `demo/teste_demo_console_modos.py:362-414` adiciona teste focal de abertura
  por `argv`, com cenario 4 verboso e cenario 3 nao verboso.

## 9. Schema D23

Resultado: nao conforme.

O patch adicionou `_TELAS_LEGADAS_D23` nominal para:

```text
h0036_console_hierarquia
h0036_console_tabela
h0036_console_conjuntos
```

Isso e correto para H-0036. Porem a implementacao tambem aceita qualquer tela
nova/revisada sem `formato.excesso`, porque `carregar_tela` passa
`excesso_declarado=False` quando o bloco esta ausente (`tela/loader.py:1233-1240`)
e `_validar_d23_console` retorna sem erro nesse caso (`tela/loader.py:1427-1431`).

Casos obrigatorios executados em memoria:

```yaml
caso_A_nova_H0037_com_formato_excesso_sem_politica:
  esperado: REJEITADA
  resultado: REJEITADA
caso_B_nova_H0037_sem_bloco_formato_excesso:
  esperado_pela_autoridade: REJEITADA
  resultado: ACEITA
caso_C_H0036_legado_sem_campos_D23:
  esperado: ACEITO
  resultado: ACEITO
caso_D_nova_sem_politica_com_campo_legado_excesso_modo:
  esperado: REJEITADA
  resultado: REJEITADA
caso_E_tile_fora_escopo_console_multinivel_D23:
  esperado: NAO_APLICAVEL_A_D23
  resultado_impl_direta: ACEITA
```

```yaml
regra_excesso_declarado:
  conforme_autoridade: false
  permite_bypass_D23: true
  escopo_real_da_isencao: qualquer console desconhecido sem bloco formato.excesso
  impacto: tela nova sujeita a D23 pode contornar a obrigacao omitindo o bloco inteiro
```

## 10. Risco De Bypass Por Ausencia De `formato.excesso`

O bypass e bloqueante para aprovacao da implementacao. A autoridade nao diz que
ausencia de campo interno torna a tela fora de D23; diz que telas novas ou
revisadas devem declarar a politica e que nao ha default implicito. A isencao
real deve ser nominal/compatibilidade para legado, nao generica por ausencia de
bloco.

## 11. V-01

Resultado: parcialmente conforme.

Casos executados em memoria:

```yaml
V_01:
  ausente: REJEITADO
  nulo: REJEITADO
  vazio: REJEITADO
  sem_coluna_valida: ACEITO_INDEVIDAMENTE
  valido: ACEITO
  conforme: false
```

Evidencia: `tela/loader.py:1710-1718` exige somente que
`formato.tabela.cabecalho` seja uma lista nao vazia. Nao verifica se existe ao
menos uma coluna semanticamente valida. `tela/teste_loader.py:2867-2872` cobre
ausencia, lista vazia e valido, mas nao cobre `cabecalho: [{}]` ou cabecalho sem
coluna util.

## 12. V-04

Resultado: conforme.

Casos executados em memoria:

```yaml
V_04:
  folha_sem_propriedade_filhos: ACEITA
  folha_com_filhos_vazio: REJEITADA
  folha_com_filho_real: REJEITADA
  nome_valor_sem_filhos: ACEITA
  nome_valor_com_filhos_vazio: REJEITADA
  container_valido_com_filhos: ACEITO
  conforme: true
```

Evidencia: `tela/loader.py:1525-1529` e `tela/loader.py:1543-1547` rejeitam
folhas `conteudo` e `nome_valor` quando a chave `filhos` esta presente,
inclusive lista vazia, sem rejeitar container valido.

## 13. V-01 A V-15

Comparacao direta contra a tabela normativa:

```yaml
V-01:
  regra_no_loader: exige cabecalho lista nao vazia
  teste: cobre ausente, vazio e valido
  entrada: cabecalho [{}] sem coluna semanticamente valida
  resultado: ACEITO
  mensagem: ausente
  conforme: false
V-02:
  regra_no_loader: rejeita referencia de nivel filho inexistente em formato.niveis[].filhos
  teste: filho "nao_existe"
  entrada: nivel com filhos referenciando id ausente
  resultado: REJEITADO
  mensagem: V-02
  conforme: true
V-03:
  regra_no_loader: rejeita mais de uma raiz quando filhos sao declarados
  teste: duas raizes reais no grafo de niveis
  entrada: niveis a->b e c raiz independente
  resultado: REJEITADO
  mensagem: V-03
  conforme: true
V-04:
  regra_no_loader: rejeita folha que declara filhos
  teste: conteudo com filhos nao vazio e vazio
  entrada: folha conteudo/nome_valor com filhos
  resultado: REJEITADO
  mensagem: V-04
  conforme: true
V-05:
  regra_no_loader: rejeita container sem filhos declarados ou com filhos vazio
  teste: container sem nivel filho declarado e dados filhos []
  entrada: container sem filhos em formato e dados vazios
  resultado: REJEITADO
  mensagem: V-05 ou validacao estrutural de container
  conforme: true
V-06:
  regra_no_loader: rejeita nome_valor sem nome/valor string em conteudo
  teste: falta "valor"
  entrada: conteudo {"nome": "chave"}
  resultado: REJEITADO
  mensagem: V-06
  conforme: true
V-07:
  regra_no_loader: rejeita numero negativo em formato.espacamento
  teste: margem -1
  entrada: formato.espacamento.margem = -1
  resultado: REJEITADO
  mensagem: V-07
  conforme: true
V-08:
  regra_no_loader: rejeita largura_maxima < largura_minima em coluna
  teste: 5 < 10
  entrada: coluna com largura_minima 10 e largura_maxima 5
  resultado: REJEITADO
  mensagem: V-08
  conforme: true
V-09:
  regra_no_loader: rejeita linhas_nao_verboso > 1
  teste: 3
  entrada: formato.excesso.linhas_nao_verboso = 3
  resultado: REJEITADO
  mensagem: V-09
  conforme: true
V-10:
  regra_no_loader: rejeita excesso.verboso dict sem continuacao
  teste: verboso {}
  entrada: formato.excesso.verboso sem continuacao
  resultado: REJEITADO
  mensagem: V-10
  conforme: true
V-11:
  regra_no_loader: rejeita alinhamento justificado sem escopo
  teste: tipo justificado sem escopo
  entrada: formato.alinhamento.tipo = justificado
  resultado: REJEITADO
  mensagem: V-11
  conforme: true
V-12:
  regra_no_loader: rejeita decimal_composto em no raiz
  teste: raiz com decimal_composto
  entrada: designador composto sem ancestral
  resultado: REJEITADO
  mensagem: V-12
  conforme: true
V-13:
  regra_no_loader: coberto por validacoes de no/nivel inexistente
  teste: dado com nivel inexistente
  entrada: dados[0].nivel = "nao_existe"
  resultado: REJEITADO
  mensagem: validacao estrutural de nivel inexistente
  conforme: true
V-14:
  regra_no_loader: rejeita coluna sem nivel e sem campo
  teste: coluna {"titulo": "Sem origem"}
  entrada: coluna de tabela sem origem
  resultado: REJEITADO
  mensagem: V-14
  conforme: true
V-15:
  regra_no_loader: rejeita politica de modo no documento externo
  teste: politica_modo, modo_inicial ou modo no documento externo
  entrada: campos D23/legado em conteudo externo
  resultado: REJEITADO
  mensagem: V-15
  conforme: true_para_documento_externo; nao_substitui_D23_estrutural
```

## 14. Identidade Compartilhada

`config/telas/demo/h0037_dois_niveis_conteudo.json` e usado por:

```text
h0037_console_nao_verboso
h0037_console_verboso_dois_niveis
```

Resultado:

```yaml
identidade: "H-0037 conteudo_dois_niveis"
consumidores: dois JSONs estruturais distintos associados ao mesmo arquivo real
dados: mesmo documento externo para os dois consumidores
varia_por_tela: false_no_arquivo_de_conteudo
titulos_residuais_verboso_nao_verboso: ausentes_no_titulo
observacao: textos dos filhos ainda mencionam as politicas para explicar o cenario, mas o titulo compartilhado foi neutralizado
H0037_QAPP_001_no_IMP: registrado na secao de identidade semantica e patch
```

## 15. Alinhamento De Dois Niveis

Resultado: parcialmente comprovado, sem novo achado bloqueante independente.

Evidencias observadas:

- cenario 2 renderiza em modo verboso com varias linhas;
- ha dois identificadores de primeiro nivel com mesma identidade neutra;
- linhas de continuacao aparecem alinhadas na saida smoke;
- tabela alternavel nao usa a regra de hierarquia de dois niveis.

Limite: a prova automatica ainda se concentra em saida observavel e nao em
contrato geometrico completo para multiplas paginas/repeticao de contexto. Como
ha achados altos em D23 e V-01, essa parcialidade nao altera o status final.

## 16. Recalibracoes Do Launcher

```yaml
itens_anteriores: 7
itens_adicionados: 4
itens_finais: 11
entradas_historicas_removidas: false
fronteira_21_para_22: justificada_por_aumento_de_itens_e_geometria_do_launcher
PTY_30_para_32: justificada_para_acomodar_11_itens_em_40_colunas
teste_paginacao_ainda_pagina: preservado
teste_sem_paginacao_ainda_nao_pagina: preservado
cobertura_H0034: preservada
classificacao: JUSTIFICADA
```

## 17. Teste Focal

`demo/teste_demo_console_modos.py` executou 63 verificacoes e 0 falhas.

As cinco verificacoes novas acrescentadas cobrem:

```yaml
abertura_por_argv:
  cenario_4_modo_inicial_helper: cobre _modo_verboso_de_modelo True
  cenario_3_modo_inicial_helper: cobre _modo_verboso_de_modelo False
  cenario_4_primeira_renderizacao: cobre main(argv) nao-TTY em modo verboso
  cenario_4_nao_truncado: cobre ausencia do defeito anterior no primeiro quadro
  cenario_3_primeira_renderizacao: cobre main(argv) nao-TTY em modo nao verboso
```

Cobertura focal geral: quatro cenarios, duas politicas fixas, duas alternaveis,
dois modos iniciais, chip presente/ausente, `V` inerte/reversivel,
recarregamento por troca de tela, isolamento, conteudo compartilhado,
identidade comum, associacoes e regressao H-0036.

## 18. Relatorio IMP-0037

O relatorio IMP-0037 foi atualizado e declara:

```yaml
qa_anterior_reprovado: sim
patch_aplicado: sim
10_scripts: sim
2578_verificacoes: sim
zero_falhas: sim
git_diff_check: sem_erros
stage_vazio: declarado
commit_ausente: declarado
validacao_manual_pendente: VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
conclusao: implementacao corrigida e aguardando novo QA independente
```

Nao conforme no conteudo material:

- declara que tiles sem `formato.excesso` ficam isentos de D23, mas a autoridade
  so isenta telas legadas, nao qualquer tela nova que omita o bloco;
- declara V-01 corrigida, mas a implementacao ainda aceita cabecalho sem coluna
  semanticamente valida;
- declara higiene sem arquivos fora da lista nominal, mas o estado real contem
  modificacoes documentais acumuladas e artefatos `__pycache__`.

## 19. Suite Independente

Executada pelo QA a partir da raiz real do repositorio, pois `scripts/` nao
existe:

| Script | Verificacoes | Falhas | Codigo |
|---|---:|---:|---:|
| `tela/teste_loader.py` | 396 | 0 | 0 |
| `tela/teste_modelo.py` | 186 | 0 | 0 |
| `tela/teste_renderizador.py` | 1223 | 0 | 0 |
| `tela/teste_distribuicao_matricial.py` | 36 | 0 | 0 |
| `demo/teste_demo.py` | 363 | 0 | 0 |
| `demo/teste_diagnostico.py` | 48 | 0 | 0 |
| `demo/teste_demo_distribuicao.py` | 109 | 0 | 0 |
| `demo/teste_explorar_barra_de_menus.py` | 38 | 0 | 0 |
| `demo/teste_demo_console.py` | 116 | 0 | 0 |
| `demo/teste_demo_console_modos.py` | 63 | 0 | 0 |
| **Total** | **2578** | **0** |  |

Suite verde nao elimina achados semanticos independentes.

## 20. Smoke Tecnico

Executado sem permanecer bloqueado em TTY:

```yaml
h0037_console_nao_verboso:
  codigo: 0
  primeiro_modo: nao_verboso
  evidencia: saida truncada em uma linha por conteudo longo
h0037_console_verboso_dois_niveis:
  codigo: 0
  primeiro_modo: verboso
  evidencia: texto longo expande em multiplas linhas
h0037_console_alternavel_tres_niveis:
  codigo: 0
  primeiro_modo: nao_verboso
  evidencia: chip V presente e textos longos truncados
h0037_console_tabela_alternavel:
  codigo: 0
  primeiro_modo: verboso
  evidencia: celulas longas ocupam multiplas linhas na primeira renderizacao
```

Isso e smoke tecnico, nao aprovacao visual manual.

## 21. Regressao H-0036

Preservadas:

```text
h0036_console_hierarquia
h0036_console_tabela
h0036_console_conjuntos
h0036_hierarquia_conteudo
h0036_tabela_conteudo
h0036_conjuntos_conteudo
```

Verificado:

- carregamento sem D23 aceito nominalmente para H-0036;
- ausencia de migracao;
- ausencia de chip `[V] Verboso`;
- ausencia de alternancia indevida;
- mesmas associacoes no catalogo;
- testes historicos verdes.

## 22. Validacao Manual

Permanece:

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

Este QA nao executou validacao manual em nome do usuario, nao aprovou
visualmente, nao criou relatorio manual e nao fechou H-0037.

## 23. Achados

### H0037-IMPL-QAPP-001

```yaml
id: H0037-IMPL-QAPP-001
origem: achado anterior H0037-IMPL-QA-002_D23 parcialmente nao resolvido
arquivo: tela/loader.py
evidencia: tela/loader.py:1233-1240 passa excesso_declarado=False quando formato.excesso ausente; tela/loader.py:1427-1431 retorna sem erro para qualquer tela nao legada com excesso_declarado=False
autoridade: ADR-0028 D23; contrato_json_console.md §13.13.1, §13.13.3, §13.13.6
severidade: alto
impacto: tela nova/revisada de console pode burlar D23 omitindo todo o bloco formato.excesso
correcao_exigida: restringir isencao a telas legadas nominalmente reconhecidas ou a elementos realmente fora do escopo D23; nova tela sujeita a D23 sem politica deve ser rejeitada mesmo sem bloco formato.excesso
```

### H0037-IMPL-QAPP-002

```yaml
id: H0037-IMPL-QAPP-002
origem: achado anterior H0037-IMPL-QA-002_V01 parcialmente nao resolvido
arquivo: tela/loader.py; tela/teste_loader.py
evidencia: tela/loader.py:1710-1718 aceita cabecalho como qualquer lista nao vazia; teste em memoria com cabecalho [{}] foi aceito; tela/teste_loader.py:2867-2872 nao cobre cabecalho sem coluna semanticamente valida
autoridade: ADR-0028 §33 V-01; contrato_json_console.md §13.9 V-01
severidade: alto
impacto: tabela sem cabecalho semanticamente valido passa na validacao
correcao_exigida: rejeitar cabecalho sem ao menos uma coluna semanticamente valida e adicionar teste nominal para esse caso
```

## 24. Conclusao

O patch resolveu o modo inicial por `argv`, corrigiu V-04, elevou a suite focal
para 63 verificacoes e manteve a suite canonica com 2578 verificacoes e 0
falhas. Entretanto, nao resolveu integralmente D23 nem V-01. Como ha bypass D23
para tela nova sem `formato.excesso` e V-01 ainda aceita cabecalho sem coluna
semanticamente valida, a implementacao exige novo patch.

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
