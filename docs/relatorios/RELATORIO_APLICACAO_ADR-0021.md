---
name: RELATORIO_APLICACAO_ADR-0021
description: Relatorio de aplicacao documental da ADR-0021 nos documentos normativos ativos autorizados
metadata:
  type: relatorio_aplicacao
  etapa: APLICAR_ADR
  status: CONCLUIDO
  data: "2026-07-14"
---

# RELATORIO DE APLICACAO — ADR-0021

## 1. Identificacao

Etapa executada: `APLICAR_ADR`.

ADR aplicada:

```text
docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
```

Relatorio de QA de autoridade:

```text
docs/relatorios/RELATORIO_QA_ADR-0021.md
```

Status formal do QA:

```text
ADR_APPROVED_WITH_NOTES
```

## 2. Objetivo e limites

Objetivo: propagar a decisao ja aprovada na ADR-0021 aos documentos
normativos ativos autorizados.

Limites respeitados:

- nao houve implementacao de codigo;
- nao houve movimentacao fisica de arquivos;
- nao houve criacao de `demo/`, `config/telas/demo/`, `config/layouts/`,
  `config/elementos/`, JSON, teste, schema ou `orquestrador.py`;
- nao houve QA funcional da aplicacao;
- nao houve alteracao da ADR-0021 aprovada;
- nao houve commit nem preparo de commit.

## 3. ADR e QA de autoridade

A ADR-0021 foi tratada como autoridade da decisao. O relatorio de QA foi usado
como validacao formal, sem criar regra nova.

O achado baixo `ACHADO_01_ESTRUTURA_CRITERIOS_AUSENTES` nao foi corrigido na
ADR. Foi absorvido neste relatorio por rastreabilidade e por criterios
objetivos de aplicacao.

## 4. Estado Git inicial

Comandos executados a partir da raiz do repositorio:

```yaml
git_toplevel: /home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador
pwd: /home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador
branch: master
head_abreviado: 0143fd1
stage: vazio
git_diff_name_only: vazio
git_diff_cached_name_only: vazio
git_diff_check: sem apontamentos
```

Arquivos nao rastreados iniciais:

```text
docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
docs/relatorios/LEVANTAMENTO_PREPARACAO_INTEGRACAO_PIPELINE_ORQUESTRADOR.md
docs/relatorios/RELATORIO_QA_ADR-0021.md
```

Nenhum item adicional inesperado foi observado no `git status --short`.

## 5. Documentos inspecionados

Autoridades lidas integralmente:

```text
docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
docs/relatorios/RELATORIO_QA_ADR-0021.md
docs/relatorios/LEVANTAMENTO_PREPARACAO_INTEGRACAO_PIPELINE_ORQUESTRADOR.md
```

Documentos ativos autorizados inspecionados:

```text
docs/adr/INDICE_ADR.md
docs/INDICE.md
docs/NOMENCLATURA.md
docs/adr/ADR-0008-modelo-configuracao-por-tela.md
docs/adr/ADR-0009-caminho-formato-jsons-tela.md
docs/contratos/contrato_json_tela_minima.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_chip.md
docs/contratos/contrato_cabecalho.md
docs/contratos/contrato_estilo.md
docs/contratos/contrato_json_barra_de_menus.md
docs/contratos/contrato_json_cabecalho.md
docs/contratos/contrato_json_lancador.md
docs/contratos/contrato_lancador.md
```

## 6. Documentos alterados

```text
docs/adr/INDICE_ADR.md
docs/INDICE.md
docs/NOMENCLATURA.md
docs/adr/ADR-0008-modelo-configuracao-por-tela.md
docs/adr/ADR-0009-caminho-formato-jsons-tela.md
docs/contratos/contrato_json_tela_minima.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_cabecalho.md
docs/contratos/contrato_json_cabecalho.md
docs/contratos/contrato_json_lancador.md
docs/contratos/contrato_lancador.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0021.md
```

## 7. Documentos autorizados nao alterados e justificativa

```yaml
- arquivo: docs/contratos/contrato_chip.md
  justificativa: referencias a config/estilo.json permanecem corretas; nao havia regra ativa de caminho afetada pela ADR-0021.
- arquivo: docs/contratos/contrato_estilo.md
  justificativa: contrato ja preserva config/estilo.json como biblioteca global; alteracao seria cosmetica.
- arquivo: docs/contratos/contrato_json_barra_de_menus.md
  justificativa: nao continha caminho normativo materialmente afetado nas buscas focais.
```

## 8. Propagacao de cada decisao estrutural

```yaml
motor_compartilhado_tela:
  aplicado_em:
    - docs/NOMENCLATURA.md
    - docs/INDICE.md
  regra: tela/ e motor compartilhado; demo/ nao duplica loader, modelo ou renderizador.
aplicacao_demonstrativa:
  aplicado_em:
    - docs/NOMENCLATURA.md
    - docs/INDICE.md
  regra: demo/ e diretorio futuro, ainda nao criado.
duas_raizes_declarativas:
  aplicado_em:
    - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
    - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
    - docs/contratos/contrato_json_tela_minima.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_json_lancador.md
  regra: produto real usa config/telas/<id>.json; demonstracao usa config/telas/demo/<id>.json.
identidade_demonstrativa:
  aplicado_em:
    - docs/contratos/contrato_json_tela_minima.md
  regra: config/telas/demo/demo.json com id demo; sem alias demo/orquestrador.
migracao_direta:
  aplicado_em:
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_json_tela_minima.md
  regra: proibidos fallback silencioso, busca ambigua, duplicacao de JSON e alias de ID.
configuracoes_gerais:
  aplicado_em:
    - docs/NOMENCLATURA.md
    - docs/INDICE.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_cabecalho.md
    - docs/contratos/contrato_json_cabecalho.md
    - docs/contratos/contrato_lancador.md
    - docs/contratos/contrato_json_lancador.md
  regra: caminhos futuros config/layouts/* e config/elementos/* propagados.
estilo_global:
  aplicado_em:
    - docs/INDICE.md
    - docs/NOMENCLATURA.md
    - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
    - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
  regra: config/estilo.json preservado.
reutilizacao_declarativa:
  aplicado_em:
    - docs/NOMENCLATURA.md
    - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
  regra: mudancas expressaveis por JSON nao exigem duplicacao de motor.
limites:
  aplicado_em:
    - todos_os_documentos_alterados
  regra: nao foi definido comportamento de loader, orquestrador.py, tela real, schema ou integracao com Pipeline.
```

## 9. Atualizacao da ADR-0008

Foi acrescentada nota de atualizacao datada de 2026-07-14.

```yaml
arquivo: docs/adr/ADR-0008-modelo-configuracao-por-tela.md
trechos_ou_secoes:
  - Nota de atualizacao — ADR-0021
regra_anterior: modelo declarativo por tela sem decidir organizacao fisica final.
regra_aplicada: modelo preservado; duas raizes declarativas registradas.
autoridade: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
```

## 10. Atualizacao da ADR-0009

Foi acrescentada nota de atualizacao datada de 2026-07-14.

```yaml
arquivo: docs/adr/ADR-0009-caminho-formato-jsons-tela.md
trechos_ou_secoes:
  - Nota de atualizacao — ADR-0021
regra_anterior: raiz unica config/telas/<id>.json.
regra_aplicada: raiz do produto preservada; raiz demonstrativa config/telas/demo/<id>.json introduzida.
autoridade: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
```

## 11. Atualizacao dos indices

```yaml
- arquivo: docs/adr/INDICE_ADR.md
  trechos_ou_secoes:
    - tabela de decisoes registradas
  regra_anterior: ADR-0021 ausente.
  regra_aplicada: ADR-0021 adicionada com status aceita, data 2026-07-14 e sintese da substituicao parcial da ADR-0009.
  autoridade: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
- arquivo: docs/INDICE.md
  trechos_ou_secoes:
    - Estrutura esperada
    - Artefatos
  regra_anterior: estrutura listava config/*.json planos e tela/ com entradas demonstrativas.
  regra_aplicada: estrutura passou a distinguir tela/ como motor, demo/ futuro, config/telas/, config/telas/demo/, config/layouts/ e config/elementos/.
  autoridade: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
```

## 12. Atualizacao da nomenclatura

```yaml
arquivo: docs/NOMENCLATURA.md
trechos_ou_secoes:
  - Politica estrutural da ADR-0021
  - Status dos artefatos JSON
  - Parametrizacoes externas de console, barra_de_menus, cabecalho e lancador
regra_anterior: glossario distinguia JSON por tela e artefatos transicionais, mas nao separava demonstracao, produto real e motor compartilhado.
regra_aplicada: termos motor compartilhado, aplicacao demonstrativa, produto real, tela demonstrativa, tela do produto real, raiz declarativa da demonstracao e raiz declarativa do produto foram diferenciados.
autoridade: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
```

## 13. Atualizacao dos contratos

```yaml
- arquivo: docs/contratos/contrato_json_tela_minima.md
  trechos_ou_secoes:
    - Caminhos canonicos e regra de coincidencia de id
    - Criterios de aceite documental
  regra_anterior: caminho canonico unico config/telas/<id>.json.
  regra_aplicada: duas raizes declarativas; sem alias demo/orquestrador; tela real reservada.
  autoridade: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
- arquivo: docs/contratos/contrato_tela_json.md
  trechos_ou_secoes:
    - Natureza do tela.json
  regra_anterior: natureza declarativa sem politica explicita de raizes por ponto de entrada.
  regra_aplicada: produto real e demonstracao usam raizes distintas; proibidos fallback, duplicacao e alias.
  autoridade: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
- arquivo: docs/contratos/contrato_composicao_corpo.md
  trechos_ou_secoes:
    - Valores parametrizados de layout
    - criterios de validacao
  regra_anterior: caminhos config/layout_console.json, config/layout_dado.json e config/lancador.json.
  regra_aplicada: caminhos futuros config/layouts/layout_console.json, config/layouts/layout_dado.json e config/elementos/lancador.json.
  autoridade: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
- arquivo: docs/contratos/contrato_barra_de_menus.md
  trechos_ou_secoes:
    - Fonte dos valores concretos
    - Regras normativas
    - Pendencias
  regra_anterior: config/barra_de_menus.json como artefato transicional.
  regra_aplicada: futuro caminho config/elementos/barra_de_menus.json.
  autoridade: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
- arquivo: docs/contratos/contrato_cabecalho.md
  trechos_ou_secoes:
    - Distincao fundamental
    - Presenca e estrutura
    - Fonte dos valores concretos
    - Schemas de apresentacao
    - Criterios de validacao
  regra_anterior: config/cabecalho.json.
  regra_aplicada: futuro caminho config/elementos/cabecalho.json.
  autoridade: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
- arquivo: docs/contratos/contrato_json_cabecalho.md
  trechos_ou_secoes:
    - objetivo
    - valores concretos
    - limites entre cabecalho e apresentacao
    - criterios
  regra_anterior: config/cabecalho.json.
  regra_aplicada: futuro caminho config/elementos/cabecalho.json.
  autoridade: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
- arquivo: docs/contratos/contrato_json_lancador.md
  trechos_ou_secoes:
    - validacao de tela_destino
    - fora de escopo
  regra_anterior: destino validado somente em config/telas/<tela_destino>.json; parametros em config/lancador.json.
  regra_aplicada: destino validado na raiz explicita do ponto de entrada; parametros em config/elementos/lancador.json.
  autoridade: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
- arquivo: docs/contratos/contrato_lancador.md
  trechos_ou_secoes:
    - Fonte dos valores concretos
    - Layout interno
    - Regras normativas
    - Criterios
    - Pendencias
  regra_anterior: config/lancador.json.
  regra_aplicada: futuro caminho config/elementos/lancador.json.
  autoridade: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
```

## 14. Criterios objetivos da aplicacao da ADR-0021

| Criterio | Verificacao |
|---|---|
| 1. Indice atualizado | `docs/adr/INDICE_ADR.md` contem ADR-0021. |
| 2. Politica das duas raizes propagada | `contrato_json_tela_minima.md`, `contrato_tela_json.md` e `contrato_json_lancador.md` registram produto real e demonstracao. |
| 3. Papel compartilhado de `tela/` propagado | `docs/NOMENCLATURA.md` e `docs/INDICE.md` definem `tela/` como motor compartilhado. |
| 4. Papel futuro de `demo/` propagado | `docs/NOMENCLATURA.md` e `docs/INDICE.md` tratam `demo/` como futuro e nao criado. |
| 5. Caminhos de `config/layouts/` e `config/elementos/` propagados | Nomenclatura e contratos afetados usam os caminhos futuros aprovados. |
| 6. `config/estilo.json` preservado | Nao foi substituido por caminho novo; contratos de estilo/chip ficaram intactos. |
| 7. Ausencia de fallback e aliases normativos | Contratos de tela registram proibicao de fallback silencioso, busca ambigua, duplicacao e alias demo/orquestrador. |
| 8. Ausencia de contradicoes ativas | ADR-0008 e ADR-0009 receberam notas explicitas de atualizacao; residuos antigos preservados como historicos. |
| 9. Ausencia de implementacao antecipada | Nenhum arquivo de codigo ou configuracao foi criado ou alterado. |
| 10. Conteudo da tela real preservado para a ADR seguinte | Contrato minimo declara `config/telas/orquestrador.json` reservado ao produto real e sem conteudo definido nesta etapa. |

## 15. Busca de referencias antes e depois

Busca antes de editar:

```bash
rg -n --glob 'docs/**' 'config/telas|config/estilo\.json|config/cabecalho\.json|config/barra_de_menus\.json|config/lancador\.json|config/layout_console\.json|config/layout_dado\.json|config/layout_menu\.json|tela/|demo/|orquestrador\.py'
```

Classificacao:

```yaml
normativa_ativa:
  - docs/NOMENCLATURA.md
  - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
  - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
  - docs/contratos/contrato_json_tela_minima.md
  - docs/contratos/contrato_tela_json.md
  - docs/contratos/contrato_composicao_corpo.md
  - docs/contratos/contrato_barra_de_menus.md
  - docs/contratos/contrato_cabecalho.md
  - docs/contratos/contrato_json_cabecalho.md
  - docs/contratos/contrato_json_lancador.md
  - docs/contratos/contrato_lancador.md
historica:
  - docs/handoff/**
  - docs/relatorios/IMP-*
  - docs/relatorios/RELATORIO_QA_H-*
  - docs/relatorios/RELATORIO_AUDITORIA_*
relatorio:
  - docs/relatorios/LEVANTAMENTO_PREPARACAO_INTEGRACAO_PIPELINE_ORQUESTRADOR.md
  - docs/relatorios/RELATORIO_QA_ADR-0021.md
ocorrencia_sem_impacto:
  - docs/contratos/contrato_chip.md
  - docs/contratos/contrato_estilo.md
```

Busca depois das alteracoes focais:

```bash
rg -n 'config/lancador\.json|config/layout_console\.json|config/layout_dado\.json|config/layout_menu\.json|config/barra_de_menus\.json|config/cabecalho\.json|config/telas/<|config/telas/orquestrador\.json' docs/NOMENCLATURA.md docs/INDICE.md docs/adr/ADR-0008-modelo-configuracao-por-tela.md docs/adr/ADR-0009-caminho-formato-jsons-tela.md docs/contratos/contrato_json_tela_minima.md docs/contratos/contrato_tela_json.md docs/contratos/contrato_composicao_corpo.md docs/contratos/contrato_barra_de_menus.md docs/contratos/contrato_cabecalho.md docs/contratos/contrato_json_cabecalho.md docs/contratos/contrato_json_lancador.md docs/contratos/contrato_lancador.md
```

Resultado classificado:

```yaml
residuos_historicos_preservados:
  - docs/adr/ADR-0008-modelo-configuracao-por-tela.md: alternativa historica sobre config/lancador.json.
  - docs/adr/ADR-0009-caminho-formato-jsons-tela.md: corpo historico da decisao original, agora com nota de superacao parcial.
  - docs/NOMENCLATURA.md: mencoes historicas a config/lancador.json na decisao terminologica de 2026-07-06.
normativa_ativa_atualizada:
  - docs/contratos/contrato_json_tela_minima.md
  - docs/contratos/contrato_tela_json.md
  - docs/contratos/contrato_composicao_corpo.md
  - docs/contratos/contrato_barra_de_menus.md
  - docs/contratos/contrato_cabecalho.md
  - docs/contratos/contrato_json_cabecalho.md
  - docs/contratos/contrato_json_lancador.md
  - docs/contratos/contrato_lancador.md
```

## 16. Residuos historicos preservados

Foram preservados:

- referencias antigas em handoffs e relatorios historicos;
- corpo original da ADR-0008;
- corpo original da ADR-0009;
- mencoes historicas da nomenclatura sobre `config/lancador.json`.

Esses residuos nao foram substituidos automaticamente porque registram estado
historico ou decisao anterior explicitamente relacionada a nota de atualizacao.

## 17. Fatos `NAO_CONFIRMADOS`

```yaml
origem_de_agentes_e_codex_na_raiz: NAO_CONFIRMADA
consumidor_runtime_atual_de_config_elementos: NAO_CONFIRMADO
consumidor_runtime_atual_de_config_layouts: NAO_CONFIRMADO
conteudo_da_futura_tela_real: NAO_CONFIRMADO
comportamento_do_futuro_orquestrador_py: NAO_CONFIRMADO
```

Nao houve item adicional inesperado no estado Git inicial. Se futuramente
surgir item adicional, deve iniciar com:

```yaml
origem: NAO_CONFIRMADA
produzido_pelo_executor: NAO_CONFIRMADO
produzido_pelo_usuario: NAO_CONFIRMADO
```

## 18. Itens fora de escopo preservados

Permaneceram fora de escopo:

- criacao ou comportamento de `orquestrador.py`;
- conteudo da futura tela real;
- `console` vazio;
- `dashboard` vazio;
- barra real com `Esc`, `?` e acesso a estilos;
- tela funcional de estilos;
- navegacao para estilos;
- integracao concreta com Pipeline;
- correcao de `destino_minimo`;
- correcao de `grupo_minimo`;
- schema novo;
- mecanismo concreto do loader.

## 19. Arquivos alterados

```text
docs/INDICE.md
docs/NOMENCLATURA.md
docs/adr/ADR-0008-modelo-configuracao-por-tela.md
docs/adr/ADR-0009-caminho-formato-jsons-tela.md
docs/adr/INDICE_ADR.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_cabecalho.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_json_cabecalho.md
docs/contratos/contrato_json_lancador.md
docs/contratos/contrato_json_tela_minima.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_tela_json.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0021.md
```

## 20. Estado Git final

Estado final esperado apos a criacao deste relatorio:

```yaml
branch: master
head_abreviado: 0143fd1
stage: vazio
arquivos_rastreados_modificados:
  - docs/INDICE.md
  - docs/NOMENCLATURA.md
  - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
  - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
  - docs/adr/INDICE_ADR.md
  - docs/contratos/contrato_barra_de_menus.md
  - docs/contratos/contrato_cabecalho.md
  - docs/contratos/contrato_composicao_corpo.md
  - docs/contratos/contrato_json_cabecalho.md
  - docs/contratos/contrato_json_lancador.md
  - docs/contratos/contrato_json_tela_minima.md
  - docs/contratos/contrato_lancador.md
  - docs/contratos/contrato_tela_json.md
arquivos_nao_rastreados_preservados:
  - docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
  - docs/relatorios/LEVANTAMENTO_PREPARACAO_INTEGRACAO_PIPELINE_ORQUESTRADOR.md
  - docs/relatorios/RELATORIO_QA_ADR-0021.md
arquivo_nao_rastreado_criado:
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0021.md
git_diff_check: sem apontamentos
git_diff_cached_name_only: vazio
commit_criado: nao
```

## 21. Bloqueios

```text
nenhum
```

Nenhuma condicao de `BLOCKED_DOCUMENTATION` foi atingida.

## 22. Conclusao

A ADR-0021 foi aplicada documentalmente aos documentos normativos ativos
autorizados. A aplicacao propagou a separacao entre motor compartilhado,
aplicacao demonstrativa futura e produto real, a politica de duas raizes
declarativas, os caminhos futuros de `config/layouts/` e `config/elementos/`, e
a preservacao de `config/estilo.json`.

O achado baixo do QA foi tratado por rastreabilidade neste relatorio, sem
alterar a ADR aprovada.

```text
proxima_categoria: QA_APLICACAO_ADR
```
