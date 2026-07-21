# Relatório de aplicação — ADR-0029 — fase 2

## 1. Identificação

```yaml
etapa_executada: APLICAR_ADR_FASE_2
etapa_de_complementacao: COMPLEMENTAR_RELATORIO_APLICACAO_ADR_FASE_2
fase_canônica: FASE_2_MIGRACAO_DEFINITIVA
alias_descritivo_preservado: FASE_2_CONVERSAO_FACHADA
descricao_operacional: conversao_da_fachada_e_migracao_definitiva_da_autoridade_terminologica
data: "2026-07-21"
adr: docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md
relatorio_fase_1: docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-1.md
pre_condicao:
  relatorio: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0029_FASE-1.md
  status_literal: APLICACAO_ADR_FASE_1_APPROVED_WITH_NOTES
  proxima_categoria: APLICAR_ADR_FASE_2
autoridade_anterior_preservada:
  relatorio: docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0029.md
  status_literal: ADR_APPROVED_WITH_NOTES
limites_executados:
  - nao executar QA
  - nao fazer stage ou commit
  - nao resolver divergencias terminologicas deferidas
  - nao alterar comportamento do sistema
  - nao alterar codigo funcional
  - nao alterar documentos historicos fechados
  - nao alterar ADRs anteriores a ADR-0029
  - nao alterar valores de schema JSON nem chaves funcionais
```

Correção aplicada neste relatório: `FASE_2_CONVERSAO_FACHADA` fica preservada apenas como alias descritivo. A fase canônica operacional é `FASE_2_MIGRACAO_DEFINITIVA`.

## 2. Autoridades

| Documento | Leitura | Uso |
|---|---:|---|
| `docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md` | integral | Decisões D-NOM-01 a D-NOM-16, critérios de aplicação, encerramento |
| `docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-1.md` | integral | Estado produzido pela fase 1 |
| `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0029_FASE-1.md` | integral | Pré-condição imediata da fase 2 |
| `docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-2.md` | integral | Relatório complementado nesta etapa |
| `docs/NOMENCLATURA.md` | integral | Fachada permanente criada |
| `docs/INDICE.md` | integral | Leitura seletiva geral |
| `docs/adr/INDICE_ADR.md` | integral | Status e índice das ADRs |
| `docs/nomenclatura/*.md` | 17 módulos integrais | Autoridade terminológica modular |
| Dez contratos declarados alterados | integral | Dependências e migração de referências |
| Cinco JSONs e `tela/teste_renderizador.py` | integral/seletiva por diffs | Validação de alterações documentais e não funcionais |
| `docs/build_docs/` e documentos históricos | seletiva | Classificação de referências remanescentes |

## 3. Estado de entrada

| Fato de entrada | Evidência | Resultado |
|---|---|---|
| Fase 1 aprovada com notas | `RELATORIO_QA_APLICACAO_ADR-0029_FASE-1.md` encerra com `status_literal: APLICACAO_ADR_FASE_1_APPROVED_WITH_NOTES` e `proxima_categoria: APLICAR_ADR_FASE_2` | CONFIRMADO |
| Monólito ainda vigente antes da fase 2 | Fase 1 preservava `docs/NOMENCLATURA.md` como fonte normativa vigente PRE_FACHADA | CONFIRMADO |
| Módulos existiam em estado PRE_FACHADA antes da fase 2 | Relatório e QA da fase 1 registram 17 módulos materializados para promoção posterior | CONFIRMADO |
| QA pós-patch da ADR | `RELATORIO_QA_POS_PATCH_ADR-0029.md` registra `ADR_APPROVED_WITH_NOTES` | AUTORIDADE_ANTERIOR |

## 4. Escopo executado

```yaml
contagem_declarada_anterior: 36
contagem_reconciliada:
  arquivos_existentes_alterados: 37
  arquivos_criados: 1
  artefatos_tocados_na_fase_2: 38
motivo_da_diferenca: relatorio_criado_e_inventario_nominal_somam_38_artefatos; a_contagem_36_nao_incluia_todos_os_itens_nominais
```

| Nº | Arquivo | Categoria | Estado antes | Ação da fase 2 | Rastreado ou não rastreado |
| -: | ------- | --------- | ------------ | -------------- | -------------------------- |
| 1 | `docs/NOMENCLATURA.md` | fachada | existente | convertido de monólito em fachada | rastreado modificado |
| 2 | `docs/nomenclatura/00_INDICE.md` | módulo | existente da fase 1 | promovido a VIGENTE e leitura seletiva atualizada | não rastreado |
| 3 | `docs/nomenclatura/01_NUCLEO_COMUM.md` | módulo | existente da fase 1 | promovido a VIGENTE | não rastreado |
| 4 | `docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` | módulo | existente da fase 1 | promovido a VIGENTE | não rastreado |
| 5 | `docs/nomenclatura/10_ESTILO.md` | módulo | existente da fase 1 | promovido a VIGENTE | não rastreado |
| 6 | `docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md` | módulo | existente da fase 1 | promovido a VIGENTE | não rastreado |
| 7 | `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` | módulo | existente da fase 1 | promovido a VIGENTE | não rastreado |
| 8 | `docs/nomenclatura/30_CABECALHO.md` | módulo | existente da fase 1 | promovido a VIGENTE | não rastreado |
| 9 | `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` | módulo | existente da fase 1 | promovido a VIGENTE | não rastreado |
| 10 | `docs/nomenclatura/32_CONSOLE.md` | módulo | existente da fase 1 | promovido a VIGENTE | não rastreado |
| 11 | `docs/nomenclatura/33_LANCADOR.md` | módulo | existente da fase 1 | promovido a VIGENTE | não rastreado |
| 12 | `docs/nomenclatura/34_DASHBOARD.md` | módulo | existente da fase 1 | promovido a VIGENTE | não rastreado |
| 13 | `docs/nomenclatura/40_GRUPOS_E_DISTRIBUICAO_DE_AREA.md` | módulo | existente da fase 1 | promovido a VIGENTE | não rastreado |
| 14 | `docs/nomenclatura/41_DISTRIBUICAO_MATRICIAL.md` | módulo | existente da fase 1 | promovido a VIGENTE | não rastreado |
| 15 | `docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md` | módulo | existente da fase 1 | promovido a VIGENTE | não rastreado |
| 16 | `docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md` | módulo | existente da fase 1 | promovido a VIGENTE | não rastreado |
| 17 | `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` | módulo | existente da fase 1 | promovido a VIGENTE | não rastreado |
| 18 | `docs/nomenclatura/90_ALIASES_E_TERMOS_DESCONTINUADOS.md` | módulo | existente da fase 1 | promovido a VIGENTE | não rastreado |
| 19 | `docs/INDICE.md` | documentação geral | existente | leitura seletiva modular | rastreado modificado |
| 20 | `docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md` | documentação geral | existente da fase 1 | status e encerramento atualizados | não rastreado |
| 21 | `docs/adr/INDICE_ADR.md` | documentação geral | existente | linha ADR-0029 atualizada | rastreado modificado |
| 22 | `docs/contratos/contrato_estilo.md` | contrato | existente | dependências e referências migradas | rastreado modificado |
| 23 | `docs/contratos/contrato_composicao_corpo.md` | contrato | existente | dependências e referências migradas | rastreado modificado |
| 24 | `docs/contratos/contrato_barra_de_menus.md` | contrato | existente | dependências e referências migradas | rastreado modificado |
| 25 | `docs/contratos/contrato_cabecalho.md` | contrato | existente | dependências e referências migradas | rastreado modificado |
| 26 | `docs/contratos/contrato_lancador.md` | contrato | existente | dependências e referências migradas | rastreado modificado |
| 27 | `docs/contratos/contrato_console.md` | contrato | existente | dependências e referências migradas | rastreado modificado |
| 28 | `docs/contratos/contrato_chip.md` | contrato | existente | dependências e referências migradas | rastreado modificado |
| 29 | `docs/contratos/contrato_tela_json.md` | contrato | existente | dependências e referências migradas | rastreado modificado |
| 30 | `docs/contratos/contrato_json_console.md` | contrato | existente | dependências e referências migradas | rastreado modificado |
| 31 | `docs/contratos/contrato_json_dashboard.md` | contrato adicional | existente | referência ativa migrada | rastreado modificado |
| 32 | `config/estilo.json` | configuração | existente | `_meta.description` e `_meta.origem` migrados | rastreado modificado |
| 33 | `config/elementos/barra_de_menus.json` | configuração | existente | três campos documentais migrados | rastreado modificado |
| 34 | `config/layouts/layout_console.json` | configuração | existente | `_meta.origem` migrado | rastreado modificado |
| 35 | `config/layouts/layout_dado.json` | configuração | existente | `_meta.origem` migrado | rastreado modificado |
| 36 | `config/layouts/layout_menu.json` | configuração | existente | `_meta.origem` migrado | rastreado modificado |
| 37 | `tela/teste_renderizador.py` | código ou teste | existente | comentário migrado | rastreado modificado |
| 38 | `docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-2.md` | relatório | criado na fase 2 | relatório criado e complementado | não rastreado |

## 5. Fachada criada

```yaml
arquivo: docs/NOMENCLATURA.md
tipo: fachada_de_compatibilidade_e_navegacao
possui_definicoes_proprias: false
indice_modular: docs/nomenclatura/00_INDICE.md
autoridade_terminologica: modulos_proprietarios
autoridade_comportamental: contratos
leitura_preventiva_de_todos_os_modulos: proibida
monolito_anterior_substituido: true
```

| Critério | Evidência | Resultado |
| -------- | --------- | --------- |
| Ausência de definições completas | Texto declara que definições terminológicas não vivem mais no arquivo | CONFORME |
| Ausência de regras comportamentais | Fachada contém regra de uso e navegação, sem algoritmos ou regras de renderer | CONFORME |
| Mapa de compatibilidade das seções antigas | Seção "Referências históricas" lista `#1`, `#3`, `#4`, `#5`, `#6`, `#7`, `#8`, `#9`, `#10`, `#13`, `§16`, `§17`, `§18`, `§19` | CONFORME |
| Links para os 17 módulos | Tabela "Mapa de módulos" lista 00, 01, 02, 10, 20, 21, 30, 31, 32, 33, 34, 40, 41, 42, 43, 44 e 90 | CONFORME |
| Link para relatório histórico | `docs/relatorios/RELATORIO_HISTORICO_NOMENCLATURA_MONOLITICA.md` | CONFORME |
| Orientação de leitura seletiva | Ordem de leitura em sete passos e proibição expressa de leitura preventiva | CONFORME |
| Ausência de simulação de âncoras antigas | Fachada declara que as seções numeradas não existem mais como âncoras normativas | CONFORME |

## 6. Módulos promovidos

| Módulo | Estado anterior | Estado final | Fonte normativa | Fachada | PRE_FACHADA residual | Resultado |
| ------ | --------------- | ------------ | --------------- | ------- | -------------------- | --------- |
| `00_INDICE.md` | PRE_FACHADA | VIGENTE | `funcao: indice_e_roteador`; `nao_proprietario_de_definicoes: true` | referência em prosa à fachada | 0 | CONFORME_COM_EQUIVALENCIA |
| `01_NUCLEO_COMUM.md` | PRE_FACHADA | VIGENTE | `fonte_normativa_do_dominio: este_modulo` | `fachada_de_navegacao: docs/NOMENCLATURA.md` | 0 | CONFORME |
| `02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` | PRE_FACHADA | VIGENTE | `fonte_normativa_do_dominio: este_modulo` | `fachada_de_navegacao: docs/NOMENCLATURA.md` | 0 | CONFORME |
| `10_ESTILO.md` | PRE_FACHADA | VIGENTE | `fonte_normativa_do_dominio: este_modulo` | `fachada_de_navegacao: docs/NOMENCLATURA.md` | 0 | CONFORME |
| `20_TELA_CORPO_E_COMPOSICAO.md` | PRE_FACHADA | VIGENTE | `fonte_normativa_do_dominio: este_modulo` | `fachada_de_navegacao: docs/NOMENCLATURA.md` | 0 | CONFORME |
| `21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` | PRE_FACHADA | VIGENTE | `fonte_normativa_do_dominio: este_modulo` | `fachada_de_navegacao: docs/NOMENCLATURA.md` | 0 | CONFORME |
| `30_CABECALHO.md` | PRE_FACHADA | VIGENTE | `fonte_normativa_do_dominio: este_modulo` | `fachada_de_navegacao: docs/NOMENCLATURA.md` | 0 | CONFORME |
| `31_BARRA_DE_MENUS_E_CHIPS.md` | PRE_FACHADA | VIGENTE | `fonte_normativa_do_dominio: este_modulo` | `fachada_de_navegacao: docs/NOMENCLATURA.md` | 0 | CONFORME |
| `32_CONSOLE.md` | PRE_FACHADA | VIGENTE | `fonte_normativa_do_dominio: este_modulo` | `fachada_de_navegacao: docs/NOMENCLATURA.md` | 0 | CONFORME |
| `33_LANCADOR.md` | PRE_FACHADA | VIGENTE | `fonte_normativa_do_dominio: este_modulo` | `fachada_de_navegacao: docs/NOMENCLATURA.md` | 0 | CONFORME |
| `34_DASHBOARD.md` | PRE_FACHADA | VIGENTE | `fonte_normativa_do_dominio: este_modulo` | `fachada_de_navegacao: docs/NOMENCLATURA.md` | 0 | CONFORME |
| `40_GRUPOS_E_DISTRIBUICAO_DE_AREA.md` | PRE_FACHADA | VIGENTE | `fonte_normativa_do_dominio: este_modulo` | `fachada_de_navegacao: docs/NOMENCLATURA.md` | 0 | CONFORME |
| `41_DISTRIBUICAO_MATRICIAL.md` | PRE_FACHADA | VIGENTE | `fonte_normativa_do_dominio: este_modulo` | `fachada_de_navegacao: docs/NOMENCLATURA.md` | 0 | CONFORME |
| `42_DADOS_EXTERNOS_MULTINIVEL.md` | PRE_FACHADA | VIGENTE | `fonte_normativa_do_dominio: este_modulo` | `fachada_de_navegacao: docs/NOMENCLATURA.md` | 0 | CONFORME |
| `43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md` | PRE_FACHADA | VIGENTE | `fonte_normativa_do_dominio: este_modulo` | `fachada_de_navegacao: docs/NOMENCLATURA.md` | 0 | CONFORME |
| `44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` | PRE_FACHADA | VIGENTE | `fonte_normativa_do_dominio: este_modulo` | `fachada_de_navegacao: docs/NOMENCLATURA.md` | 0 | CONFORME |
| `90_ALIASES_E_TERMOS_DESCONTINUADOS.md` | PRE_FACHADA | VIGENTE | `fonte_normativa_do_dominio: este_modulo` | `fachada_de_navegacao: docs/NOMENCLATURA.md` | 0 | CONFORME |

Buscas executadas em `docs/nomenclatura/`, `docs/NOMENCLATURA.md`, `docs/INDICE.md`, contratos e ADR-0029:

```yaml
PRE_FACHADA_em_modulos: 0
fonte_normativa_ainda_vigente_em_modulos: 0
proprietario_futuro_do_dominio_em_modulos: 0
aguardando_auditoria_documental_em_modulos: 0
substituicao_de_autoridade_executada_false_em_modulos: 0
```

## 7. Índice geral atualizado

| Regra de leitura | Estado anterior | Estado final | Resultado |
| ---------------- | --------------- | ------------ | --------- |
| Identificação da atividade | Leitura linear do monólito como terceira autoridade | Atividade identifica contrato ou artefato alvo antes de carregar módulos | CONFORME |
| Identificação do contrato | Não condicionava nomenclatura por contrato | Contrato alvo governa dependências obrigatórias e condicionais | CONFORME |
| Dependências obrigatórias | Não declaradas por contrato | Carregadas a partir de `dependencias_obrigatorias` | CONFORME |
| Gatilhos condicionais | Não existiam | `dependencias_condicionais` avaliadas por gatilho objetivo | CONFORME |
| Fachada e índice modular | `docs/NOMENCLATURA.md` era fonte de verdade | `docs/NOMENCLATURA.md` é fachada; `00_INDICE.md` é roteador | CONFORME |
| Leitura preventiva integral | Exigida indiretamente pela ordem de leitura | Proibida explicitamente | CONFORME |
| Exigência automática dos 17 módulos | Possível por monólito único | Ausente; leitura seletiva por domínio | CONFORME |
| Seção antiga como autoridade vigente | Seções numeradas do monólito | Destinos modulares e contratos | CONFORME |

## 8. Dependências materializadas por contrato

| Contrato | Obrigatórias | Condicionais | Todos os gatilhos presentes | Caminhos existentes | Referências antigas migradas | Resultado |
| -------- | ------------ | ------------ | --------------------------- | ------------------- | ---------------------------- | --------- |
| `contrato_estilo.md` | 2 | 3 | sim | sim | sim | CONFORME |
| `contrato_composicao_corpo.md` | 3 | 7 | sim | sim | sim | CONFORME |
| `contrato_barra_de_menus.md` | 2 | 4 | sim | sim | sim | CONFORME |
| `contrato_cabecalho.md` | 2 | 2 | sim | sim | sim | CONFORME |
| `contrato_lancador.md` | 2 | 3 | sim | sim | sim | CONFORME |
| `contrato_console.md` | 2 | 5 | sim | sim | sim | CONFORME |
| `contrato_chip.md` | 2 | 5 | sim | sim | sim | CONFORME |
| `contrato_tela_json.md` | 3 | 11 | sim | sim | sim | CONFORME |
| `contrato_json_console.md` | 3 | 4 | sim | sim | sim | CONFORME |

Confirmações físicas:

```yaml
contratos_com_dependencias_nomenclatura: 9
blocos_no_frontmatter: true
YAML_valido_por_inspecao_estrutural: true
duplicacao_de_mecanismo: false
dependencias_obrigatorias_excessivas: false
dependencias_condicionais_sem_gatilho: 0
docs_nomenclatura_00_INDICE_em_dependencias_normativas: false
caminhos_relativos_existentes: true
leitura_preventiva_de_todos_os_modulos: ausente
```

```yaml
contrato_adicional:
  arquivo: docs/contratos/contrato_json_dashboard.md
  alteracao: somente_migracao_de_referencia_ativa
  dependencias_nomenclatura_adicionadas: false
  justificativa: referencia_ativa_comprovadamente_obsoleta
```

## 9. Referências ativas migradas

### 9.1 Contratos

Método: `git diff --unified=0` nos dez contratos; contagem de linhas removidas contendo `NOMENCLATURA.md`. A contagem anterior `31` corresponde somente a ocorrências no corpo dos contratos. Ao incluir `origem_especificacao`, exigido nesta complementação, o total físico reprodutível é `38`.

| Nº | Contrato | Localização | Referência anterior | Referência nova | Ocorrência distinta |
| -: | -------- | ----------- | ------------------- | --------------- | ------------------- |
| 1 | `contrato_estilo.md` | `origem_especificacao` | `docs/NOMENCLATURA.md#1-estilo-universal` | `docs/nomenclatura/10_ESTILO.md` | sim |
| 2 | `contrato_estilo.md` | corpo, escopo | `docs/NOMENCLATURA.md` | `docs/nomenclatura/10_ESTILO.md` | sim |
| 3 | `contrato_estilo.md` | corpo, regra | `docs/NOMENCLATURA.md seção 1` | `docs/nomenclatura/10_ESTILO.md` | sim |
| 4 | `contrato_estilo.md` | corpo, universalidade | `NOMENCLATURA.md seção 1` | `docs/nomenclatura/10_ESTILO.md` | sim |
| 5 | `contrato_composicao_corpo.md` | `origem_especificacao` | `#3`, `#6`, `#8`, `#9`, `#10` em uma string | lista de módulos 20, 21, 33, 34, 10 | sim, uma string |
| 6 | `contrato_composicao_corpo.md` | corpo, escopo | seções 2, 3, 6, 6.1, 8, 9, 10 de `docs/NOMENCLATURA.md` | módulos 20, 21, 33, 34, 10 | sim |
| 7 | `contrato_composicao_corpo.md` | corpo, regra estrutural | seção 3 de `docs/NOMENCLATURA.md` | `20_TELA_CORPO_E_COMPOSICAO.md` | sim |
| 8 | `contrato_composicao_corpo.md` | corpo, nota histórica supersedida | `docs/NOMENCLATURA.md seção 10` | `10_ESTILO.md` | sim |
| 9 | `contrato_composicao_corpo.md` | corpo, prosa da nota | segunda menção a `docs/NOMENCLATURA.md seção 10` | prosa removida sem nova autoridade | sim, remoção documental |
| 10 | `contrato_composicao_corpo.md` | corpo, deferimento | `docs/NOMENCLATURA.md seção 4` | `32_CONSOLE.md` | sim |
| 11 | `contrato_composicao_corpo.md` | corpo, rastreabilidade ADR-0028 | `docs/NOMENCLATURA.md seção 19` | `44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` | sim |
| 12 | `contrato_barra_de_menus.md` | `origem_especificacao` | `docs/NOMENCLATURA.md#5-barra_de_menus` | `31_BARRA_DE_MENUS_E_CHIPS.md` | sim |
| 13 | `contrato_barra_de_menus.md` | corpo, escopo | seção 5 de `docs/NOMENCLATURA.md` | `31_BARRA_DE_MENUS_E_CHIPS.md` | sim |
| 14 | `contrato_barra_de_menus.md` | corpo, política de artefato | `docs/NOMENCLATURA.md seção 0` | `02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` | sim |
| 15 | `contrato_barra_de_menus.md` | corpo, regra estrutural | seção 5.1 de `docs/NOMENCLATURA.md` | `31_BARRA_DE_MENUS_E_CHIPS.md` | sim |
| 16 | `contrato_barra_de_menus.md` | corpo, estados | `docs/NOMENCLATURA.md seção 1.5` | `10_ESTILO.md` | sim |
| 17 | `contrato_barra_de_menus.md` | corpo, ADR-0028 | `docs/NOMENCLATURA.md seção 19` | `44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` | sim |
| 18 | `contrato_cabecalho.md` | `origem_especificacao` | `docs/NOMENCLATURA.md#7-cabecalho` | `30_CABECALHO.md` | sim |
| 19 | `contrato_cabecalho.md` | corpo, escopo | seção 7 de `docs/NOMENCLATURA.md` | `30_CABECALHO.md` | sim |
| 20 | `contrato_cabecalho.md` | corpo, política de artefato | `docs/NOMENCLATURA.md` | `02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` | sim |
| 21 | `contrato_lancador.md` | `origem_especificacao` | `docs/NOMENCLATURA.md#13-decisao-terminologica-lancador` | `33_LANCADOR.md` | sim |
| 22 | `contrato_lancador.md` | corpo, escopo | seção 13 de `docs/NOMENCLATURA.md` | `33_LANCADOR.md` | sim |
| 23 | `contrato_console.md` | `origem_especificacao` | `docs/NOMENCLATURA.md#4-corpo-tipo-console` | `32_CONSOLE.md` | sim |
| 24 | `contrato_console.md` | corpo, ADR-0026 | `docs/NOMENCLATURA.md seção 17` | `42_DADOS_EXTERNOS_MULTINIVEL.md` | sim |
| 25 | `contrato_console.md` | corpo, ADR-0027 | `docs/NOMENCLATURA.md seção 18` | `43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md` | sim |
| 26 | `contrato_console.md` | corpo, ADR-0028 | `docs/NOMENCLATURA.md seção 19` | `44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` | sim |
| 27 | `contrato_chip.md` | `origem_especificacao` | `docs/NOMENCLATURA.md#5-barra_de_menus` | `31_BARRA_DE_MENUS_E_CHIPS.md` | sim |
| 28 | `contrato_chip.md` | corpo, estados | `NOMENCLATURA.md seção 1.5` | `10_ESTILO.md` | sim |
| 29 | `contrato_chip.md` | corpo, relação com barra | `NOMENCLATURA.md seção 5.1.2` | `31_BARRA_DE_MENUS_E_CHIPS.md` | sim |
| 30 | `contrato_tela_json.md` | corpo, pendência ADR-0008 | aplicar contrato em `docs/NOMENCLATURA.md` | atualizar módulos proprietários | sim |
| 31 | `contrato_tela_json.md` | corpo, seção 16 | `docs/NOMENCLATURA.md seção 16` | `41_DISTRIBUICAO_MATRICIAL.md` | sim |
| 32 | `contrato_tela_json.md` | corpo, seção 17 | `docs/NOMENCLATURA.md seção 17` | `42_DADOS_EXTERNOS_MULTINIVEL.md` | sim |
| 33 | `contrato_tela_json.md` | corpo, seção 18 | `docs/NOMENCLATURA.md seção 18` | `43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md` | sim |
| 34 | `contrato_tela_json.md` | corpo, seção 19 | `docs/NOMENCLATURA.md seção 19` | `44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` | sim |
| 35 | `contrato_json_console.md` | corpo, seção 17 | `docs/NOMENCLATURA.md seção 17` | `42_DADOS_EXTERNOS_MULTINIVEL.md` | sim |
| 36 | `contrato_json_console.md` | corpo, seção 18 | `docs/NOMENCLATURA.md seção 18` | `43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md` | sim |
| 37 | `contrato_json_console.md` | corpo, seção 19 | `docs/NOMENCLATURA.md seção 19` | `44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` | sim |
| 38 | `contrato_json_dashboard.md` | corpo, alinhamento dashboard | `docs/NOMENCLATURA.md seção 11` | `34_DASHBOARD.md` | sim |

```yaml
contratos_auditados: 10
ocorrencias_migradas_por_contrato:
  docs/contratos/contrato_estilo.md: 4
  docs/contratos/contrato_composicao_corpo.md: 7
  docs/contratos/contrato_barra_de_menus.md: 6
  docs/contratos/contrato_cabecalho.md: 3
  docs/contratos/contrato_lancador.md: 2
  docs/contratos/contrato_console.md: 4
  docs/contratos/contrato_chip.md: 3
  docs/contratos/contrato_tela_json.md: 5
  docs/contratos/contrato_json_console.md: 3
  docs/contratos/contrato_json_dashboard.md: 1
total_reproduzivel_contratos: 38
observacao: total_31_corresponde_ao_corpo_dos_contratos_sem_os_7_campos_origem_especificacao
```

### 9.2 Configurações

| Arquivo | Caminho JSON do campo | Referência anterior | Referência nova | Resultado |
| ------- | --------------------- | ------------------- | --------------- | --------- |
| `config/estilo.json` | `_meta.description` | `docs/NOMENCLATURA.md secao 1` | `docs/nomenclatura/10_ESTILO.md` | CONFORME |
| `config/estilo.json` | `_meta.origem` | `docs/NOMENCLATURA.md secao 1` | `docs/nomenclatura/10_ESTILO.md` | CONFORME |
| `config/elementos/barra_de_menus.json` | `_meta.origem` | `docs/NOMENCLATURA.md secao 5` | `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` | CONFORME |
| `config/elementos/barra_de_menus.json` | `chips.selecionar.comportamento` | `docs/NOMENCLATURA.md secao 4.2` | `docs/nomenclatura/32_CONSOLE.md` | CONFORME |
| `config/elementos/barra_de_menus.json` | `chips.especificos.existencia.condicao` | `docs/NOMENCLATURA.md secao 5.2` | `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` | CONFORME |
| `config/layouts/layout_console.json` | `_meta.origem` | `docs/NOMENCLATURA.md secao 4` | `docs/nomenclatura/32_CONSOLE.md` | CONFORME |
| `config/layouts/layout_dado.json` | `_meta.origem` | `docs/NOMENCLATURA.md secao 4` | `docs/nomenclatura/32_CONSOLE.md` | CONFORME |
| `config/layouts/layout_menu.json` | `_meta.origem` | `docs/NOMENCLATURA.md secao 8` | `docs/nomenclatura/33_LANCADOR.md` | CONFORME |

```yaml
contagem_declarada_anterior_configs: 7
contagem_reconciliada_configs: 8
motivo_da_diferenca: config_estilo_tem_dois_campos_documentais_alterados; barra_de_menus_tem_tres; layouts_tem_tres
```

### 9.3 Código ou teste

| Arquivo | Linha ou função | Conteúdo anterior | Conteúdo novo | Confirmação |
|---|---|---|---|---|
| `tela/teste_renderizador.py` | linha 7252, comentário antes de `TestCatalogoH0030` | `# contrato_lancador.md 6.1-6.7, NOMENCLATURA.md 6.3/8.1-8.3.` | `# contrato_lancador.md 6.1-6.7, docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md / docs/nomenclatura/33_LANCADOR.md.` | somente comentário; nenhuma instrução executável mudou |

### 9.4 Total

```yaml
referencias_migradas:
  contratos: 38
  configuracoes: 8
  codigo_ou_teste: 1
  total: 47
metodo_de_contagem: ocorrencias_distintas_em_diff_material; inclui_campos_origem_especificacao; exclui_dependencias_nomenclatura_novas_por_nao_serem_substituicoes
```

## 10. Referências remanescentes classificadas

```yaml
consultas:
  - padrao: docs/NOMENCLATURA.md
    diretorios: [docs, config, tela]
    exclusoes: [docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-2.md]
    contagem: 1053
  - padrao: NOMENCLATURA.md
    diretorios: [docs, config, tela]
    exclusoes: [docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-2.md]
    contagem: 1370
  - padrao: "#1-estilo-universal"
    diretorios: [docs, config, tela]
    exclusoes: [relatorio_atual]
    contagem: 4
  - padrao: "#3-"
    diretorios: [docs, config, tela]
    exclusoes: [relatorio_atual]
    contagem: 1
  - padrao: "#4-"
    diretorios: [docs, config, tela]
    exclusoes: [relatorio_atual]
    contagem: 2
  - padrao: "#5-"
    diretorios: [docs, config, tela]
    exclusoes: [relatorio_atual]
    contagem: 3
  - padrao: "#6-"
    diretorios: [docs, config, tela]
    exclusoes: [relatorio_atual]
    contagem: 1
  - padrao: "#7-"
    diretorios: [docs, config, tela]
    exclusoes: [relatorio_atual]
    contagem: 4
  - padrao: "#8-"
    diretorios: [docs, config, tela]
    exclusoes: [relatorio_atual]
    contagem: 1
  - padrao: "#9-"
    diretorios: [docs, config, tela]
    exclusoes: [relatorio_atual]
    contagem: 1
  - padrao: "#10-"
    diretorios: [docs, config, tela]
    exclusoes: [relatorio_atual]
    contagem: 1
  - padrao: "#13-"
    diretorios: [docs, config, tela]
    exclusoes: [relatorio_atual]
    contagem: 3
  - padrao: "seção 17"
    diretorios: [docs, config, tela]
    exclusoes: [relatorio_atual]
    contagem: 33
  - padrao: "seção 18"
    diretorios: [docs, config, tela]
    exclusoes: [relatorio_atual]
    contagem: 38
  - padrao: "seção 19"
    diretorios: [docs, config, tela]
    exclusoes: [relatorio_atual]
    contagem: 33
  - padrao: PRE_FACHADA
    diretorios: [docs, config, tela]
    exclusoes: [relatorio_atual]
    contagem: 34
  - padrao: fonte_normativa_ainda_vigente
    diretorios: [docs, config, tela]
    exclusoes: [relatorio_atual]
    contagem: 1
```

| Arquivo | Referência remanescente | Classificação | Justificativa | Ativa ou histórica | Bloqueia QA |
| ------- | ----------------------- | ------------- | ------------- | ------------------ | ----------- |
| `docs/INDICE.md` | três referências a `docs/NOMENCLATURA.md`/`NOMENCLATURA.md` | REFERENCIA_A_FACHADA | ordem de leitura, árvore de diretórios e tabela de artefatos apontam para fachada existente | ativa como fachada | não |
| `docs/NOMENCLATURA.md` | caminho do próprio arquivo e âncoras antigas `#1`, `#3`, `#4`, `#5`, `#6`, `#7`, `#8`, `#9`, `#10`, `#13`, `§16`-`§19` | REFERENCIA_A_FACHADA | fachada registra compatibilidade e declara que âncoras antigas não são autoridade | ativa como aviso de compatibilidade | não |
| `docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md` | referências ao monólito, PRE_FACHADA e conversão | HISTORICA_FECHADA | ADR descreve problema, decisão e execução; status atual é aplicado | histórica/documental | não |
| `docs/adr/INDICE_ADR.md` | linha ADR-0029 menciona monólito, PRE_FACHADA e fase 2 | HISTORICA_FECHADA | índice resume a decisão aplicada | histórica/documental | não |
| `docs/nomenclatura/00_INDICE.md` | `docs/NOMENCLATURA.md` | REFERENCIA_A_FACHADA | identifica fachada permanente de navegação | ativa como fachada | não |
| `docs/nomenclatura/01_NUCLEO_COMUM.md` | `fachada_de_navegacao` e menções ao papel de schema | REFERENCIA_A_FACHADA / HISTORICA_FECHADA | campo de fachada é esperado; menções de schema preservam contexto ADR-0008 e fase modular | mista classificada | não |
| `docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` | `fachada_de_navegacao`; menções ao papel histórico de schema | REFERENCIA_A_FACHADA / HISTORICA_FECHADA | módulo é proprietário do artefato e da história schema x dados; não reintroduz leitura preventiva | mista classificada | não |
| `docs/nomenclatura/10_ESTILO.md` | `fachada_de_navegacao` | REFERENCIA_A_FACHADA | campo esperado nos módulos proprietários | ativa como fachada | não |
| `docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md` | `fachada_de_navegacao` | REFERENCIA_A_FACHADA | campo esperado nos módulos proprietários | ativa como fachada | não |
| `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` | `fachada_de_navegacao` | REFERENCIA_A_FACHADA | campo esperado nos módulos proprietários | ativa como fachada | não |
| `docs/nomenclatura/30_CABECALHO.md` | `fachada_de_navegacao` | REFERENCIA_A_FACHADA | campo esperado nos módulos proprietários | ativa como fachada | não |
| `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` | `fachada_de_navegacao` | REFERENCIA_A_FACHADA | campo esperado nos módulos proprietários | ativa como fachada | não |
| `docs/nomenclatura/32_CONSOLE.md` | `fachada_de_navegacao` | REFERENCIA_A_FACHADA | campo esperado nos módulos proprietários | ativa como fachada | não |
| `docs/nomenclatura/33_LANCADOR.md` | `fachada_de_navegacao` | REFERENCIA_A_FACHADA | campo esperado nos módulos proprietários | ativa como fachada | não |
| `docs/nomenclatura/34_DASHBOARD.md` | `fachada_de_navegacao` | REFERENCIA_A_FACHADA | campo esperado nos módulos proprietários | ativa como fachada | não |
| `docs/nomenclatura/40_GRUPOS_E_DISTRIBUICAO_DE_AREA.md` | `fachada_de_navegacao` | REFERENCIA_A_FACHADA | campo esperado nos módulos proprietários | ativa como fachada | não |
| `docs/nomenclatura/41_DISTRIBUICAO_MATRICIAL.md` | `fachada_de_navegacao` | REFERENCIA_A_FACHADA | campo esperado nos módulos proprietários | ativa como fachada | não |
| `docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md` | `fachada_de_navegacao` | REFERENCIA_A_FACHADA | campo esperado nos módulos proprietários | ativa como fachada | não |
| `docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md` | `fachada_de_navegacao` | REFERENCIA_A_FACHADA | campo esperado nos módulos proprietários | ativa como fachada | não |
| `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` | `fachada_de_navegacao` | REFERENCIA_A_FACHADA | campo esperado nos módulos proprietários | ativa como fachada | não |
| `docs/nomenclatura/90_ALIASES_E_TERMOS_DESCONTINUADOS.md` | `fachada_de_navegacao`; referência ao §13 do monólito | REFERENCIA_A_FACHADA / HISTORICA_FECHADA | campo esperado e histórico da substituição `menu` -> `lancador` | mista classificada | não |
| `docs/contratos/*.md`, `config/*.json`, `tela/teste_renderizador.py` | busca por `docs/NOMENCLATURA.md`, `NOMENCLATURA.md#`, `NOMENCLATURA.md seção/secao` | sem ocorrência | referências normativas antigas removidas | não aplicável | não |
| Handoffs fechados e relatórios históricos | múltiplas referências antigas | RELATORIO_HISTORICO | documentos encerrados, preservados por restrição da fase | histórica | não |
| `docs/build_docs/` | referências antigas | REFERENCIA_A_ANTIGA_AUTORIDADE | documentos operacionais internos e históricos; não normativos nesta fase | histórica/operacional | não |

## 11. Configurações e comentários atualizados

| Arquivo | Parse JSON | Campos alterados | Alteração funcional | Resultado |
| ------- | ---------- | ---------------- | ------------------- | --------- |
| `config/estilo.json` | OK | `_meta.description`, `_meta.origem` | não | CONFORME |
| `config/elementos/barra_de_menus.json` | OK | `_meta.origem`, `chips.selecionar.comportamento`, `chips.especificos.existencia.condicao` | não | CONFORME |
| `config/layouts/layout_console.json` | OK | `_meta.origem` | não | CONFORME |
| `config/layouts/layout_dado.json` | OK | `_meta.origem` | não | CONFORME |
| `config/layouts/layout_menu.json` | OK | `_meta.origem` | não | CONFORME |

Confirmações:

```yaml
JSON_valido: true
somente_campos_meta_ou_documentais_alterados: true
chave_funcional_adicionada: false
valor_funcional_alterado: false
referencia_para_caminho_inexistente_nas_migracoes: false
```

Para `tela/teste_renderizador.py`:

```yaml
alteracao: comentario
linha: 7252
assert_fixture_parametrizacao_import_ou_codigo_executavel_alterado: false
syntax_check:
  comando: python -B -c "import py_compile; py_compile.compile('tela/teste_renderizador.py', cfile='/tmp/teste_renderizador_adr0029_fase2.pyc', doraise=True)"
  resultado: OK
teste_visual_executado: false
```

## 12. Pendências e deferimentos preservados

| Item | Localização após fase 2 | Estado | Decisão nova introduzida | Resultado |
| ---- | ----------------------- | ------ | ------------------------ | --------- |
| `tx` | Fase 1, NOM-LEV-017; contratos de console/barra | pendência preservada | não | CONFORME |
| `popup_execucao` | Fase 1, NOM-LEV-017; relatório histórico | PENDENTE_SEM_DEFINICAO_APROVADA | não | CONFORME |
| alinhamento horizontal do dashboard | `contrato_json_dashboard.md` seção 9.5; módulo `34`; fase 1 | FUTURA_NAO_BLOQUEANTE | não | CONFORME |
| segunda pauta de estilos de exibição | Fase 1, NOM-LEV-017; relatório histórico | pendência preservada | não | CONFORME |
| campos de navegação do lançador | Fase 1, NOM-LEV-017; módulo `33`/contrato lançador | pendência preservada | não | CONFORME |
| reorganização corpo × dashboard | Fase 1, NOM-LEV-017; módulos `20` e `34` | pendência preservada | não | CONFORME |
| folha × conteudo | módulos `42` e `90` | TERMO_CONCORRENTE_DEFERIDO | não | CONFORME |
| campo × nome_valor | módulos `42` e `90` | TERMO_CONCORRENTE_DEFERIDO | não | CONFORME |
| hierarquia_indentada × hierarquia | módulos `44` e `90` | TERMO_CONCORRENTE_DEFERIDO | não | CONFORME |
| modo normal × modo não verboso | módulo `44`, módulo `90`, contratos de console | divergência deferida | não | CONFORME |
| protocolo produtor/Pipeline | módulo `43`; ADR-0027/ADR-0028 | deferido | não | CONFORME |
| migração legada D23 | módulo `44`; ADR-0028/D23 | deferida | não | CONFORME |

## 13. Atualização da ADR e do índice de ADRs

ADR-0029:

```yaml
metadata:
  status: aceita e aplicada
fase_1_executada: true
qa_fase_1_aprovado: true
fase_2_executada: true
fachada_criada: true
modulos_promovidos_a_vigentes: true
contratos_com_dependencias_materializadas: true
indice_geral_atualizado: true
referencias_ativas_migradas: true
decisoes_semanticas_reabertas: false
implementacao_funcional_afetada: false
status_literal_fisico: ADR_ACCEPTED_AND_APPLIED
status_literal_equivalente_solicitado: ADR_APPLIED_AWAITING_QA
proxima_categoria_fisica: QA_FASE_2
proxima_categoria_equivalente_solicitada: QA_APLICACAO_ADR_FASE_2
```

`docs/adr/INDICE_ADR.md`:

| Critério | Evidência | Resultado |
|---|---|---|
| Somente linha ADR-0029 alterada nesta fase | `git diff --unified=0 -- docs/adr/INDICE_ADR.md` adiciona linha ADR-0029 | CONFORME |
| Status `aceita e aplicada` | linha ADR-0029 | CONFORME |
| Indicação de fase 2 aguardando QA | linha registra FASE_2 executada; ADR encerra com próxima categoria `QA_FASE_2` | CONFORME_COM_EQUIVALENCIA |
| Referência ao relatório da fase 2 | ADR-0029 referencia `RELATORIO_APLICACAO_ADR-0029_FASE-2.md`; índice ADR resume execução | CONFORME |

## 14. Propriedade terminológica final

```yaml
termos_ativos_sem_proprietario: 0
definicoes_duplicadas: 0
regras_ativas_sem_contrato_comprovado: 0
fachada_com_definicoes_proprias: false
contratos_sem_dependencias_entre_os_nove: 0
dependencias_condicionais_sem_gatilho: 0
```

| Termo auditado | Proprietário terminológico | Contrato comportamental | Resultado |
|---|---|---|---|
| `config/estilo.json` | `02` para artefato; `10` para vocabulário interno | `contrato_estilo.md` | CONFORME |
| `barra_de_menus` | `31` | `contrato_barra_de_menus.md`, `contrato_chip.md` | CONFORME |
| grupo estrutural | `40` | `contrato_composicao_corpo.md`, `contrato_tela_json.md` | CONFORME |
| JSON estrutural da tela | `02` | `contrato_tela_json.md` | CONFORME |
| chip | `31` para termo; `10` para aparência | `contrato_chip.md`, `contrato_barra_de_menus.md` | CONFORME |
| loader | `02`/`43` conforme contexto | `contrato_tela_json.md`, `contrato_json_console.md` | CONFORME |
| vão | `21`/`33`/`40` conforme domínio | `contrato_composicao_corpo.md`, `contrato_lancador.md` | CONFORME |
| célula | `40`/`41` | `contrato_composicao_corpo.md`, `contrato_tela_json.md` | CONFORME |
| coluna | `21`/`31`/`32`/`33`/`41` conforme domínio | contratos correspondentes | CONFORME |

## 15. Regras comportamentais preservadas

As alterações em contratos foram restritas a `dependencias_nomenclatura`, `origem_especificacao` e substituições de referência por módulo proprietário. Não houve remoção de regras comportamentais completas. A busca por referências antigas nos contratos e JSONs alterados retornou zero para `docs/NOMENCLATURA.md`, `NOMENCLATURA.md#`, `NOMENCLATURA.md seção` e `NOMENCLATURA.md secao`.

| Domínio | Contrato que preserva comportamento | Resultado |
|---|---|---|
| estilo | `contrato_estilo.md` | CONFORME |
| composição de corpo, grupos, distribuição | `contrato_composicao_corpo.md`, `contrato_tela_json.md` | CONFORME |
| cabeçalho | `contrato_cabecalho.md` | CONFORME |
| barra e chips | `contrato_barra_de_menus.md`, `contrato_chip.md` | CONFORME |
| console | `contrato_console.md`, `contrato_json_console.md` | CONFORME |
| lançador | `contrato_lancador.md` | CONFORME |
| dashboard | `contrato_json_dashboard.md` e composição | CONFORME |
| dados externos e modos | `contrato_console.md`, `contrato_json_console.md`, `contrato_tela_json.md`, `contrato_barra_de_menus.md` | CONFORME |

## 16. Verificações Markdown, YAML e caminhos

Método executado:

```yaml
frontmatter_verificado:
  - docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md
  - 17_modulos_em_docs/nomenclatura
blocos_dependencia_verificados: 9
links_verificados:
  - fachada
  - indice_modular
  - indice_geral
  - contratos
checks:
  conflitos_git: ausentes
  trailing_whitespace: ausente
  newline_final: presente
  fences_markdown_balanceadas: true
  caminhos_absolutos_locais: ausentes
  caminhos_normativos_novos_existentes: true
  caminhos_inexistentes_detectados: somente_exemplos_ou_futuros_reservados
git_diff_check: OK
git_diff_no_index_check_para_nao_rastreados: OK
```

Observação: a varredura ingênua de caminhos encontra `config/cabecalho.json`, `config/lancador.json`, `config/layout_lancador.json`, `config/telas/orquestrador.json`, `config/modulo_exemplo.json`, `tela/modulo_exemplo/` e equivalentes. Esses itens aparecem como exemplos, caminhos futuros ou caminhos explicitamente reservados; não são referências normativas novas da fase 2.

## 17. Verificações funcionais proporcionais

| Verificação | Comando ou método | Resultado |
|---|---|---|
| JSON parse | `json.loads` nos cinco JSONs alterados | OK |
| Referências JSON para módulos | extração de `docs/nomenclatura/*.md` nos valores textuais | todos os caminhos existem |
| Sintaxe Python | `py_compile.compile(..., cfile='/tmp/teste_renderizador_adr0029_fase2.pyc', doraise=True)` | OK |
| Alteração executável em teste | `git diff --unified=0 -- tela/teste_renderizador.py` | somente comentário |
| Teste visual | não executado | respeitado limite da etapa |

## 18. Consistência documental

| Relação | Resultado | Evidência |
| ------------------------------------ | --------- | --------- |
| fachada × índice modular | CONSISTENTE | fachada aponta para `00_INDICE.md`; índice aponta a fachada como navegação |
| fachada × módulos vigentes | CONSISTENTE | 17 módulos `VIGENTE`; 16 proprietários com `fachada_de_navegacao`; 00 como roteador |
| índice geral × leitura seletiva | CONSISTENTE | `docs/INDICE.md` proíbe leitura preventiva e orienta por contrato |
| contratos × dependências | CONSISTENTE | 9 contratos com `dependencias_nomenclatura` |
| dependências × módulos existentes | CONSISTENTE | todos os caminhos em dependências existem |
| ADR × estado aplicado | CONSISTENTE | `metadata.status: aceita e aplicada`; encerramento registra fase 2 |
| índice de ADRs × ADR | CONSISTENTE | linha ADR-0029 em `INDICE_ADR.md` reflete status aplicado |
| relatório × estado físico | CONSISTENTE | contagens reconciliadas contra `git status`, diff e inventário nominal |
| referências antigas × destinos novos | CONSISTENTE | contratos/configs/teste migrados; remanescentes classificadas |
| termos ativos × proprietário | CONSISTENTE | nenhum termo ativo sem proprietário encontrado |
| pendências × histórico | CONSISTENTE | pendências preservadas sem decisão nova |
| aliases × termo atual | CONSISTENTE | módulo `90` preserva aliases e termos concorrentes deferidos |
| módulos × contratos comportamentais | CONSISTENTE | regras completas permanecem nos contratos |

## 19. Estado Git

Comandos executados a partir da raiz:

```text
git branch --show-current
git log -1 --oneline
git status --short
git diff --name-only
git diff --stat
git diff --check
git diff --cached --name-only
git diff --no-index --check /dev/null <arquivo_nao_rastreado>
```

```yaml
branch: master
HEAD: c90349c feat: implementa apresentacoes multinivel com modos por tela
arquivos_rastreados_modificados:
  - config/elementos/barra_de_menus.json
  - config/estilo.json
  - config/layouts/layout_console.json
  - config/layouts/layout_dado.json
  - config/layouts/layout_menu.json
  - docs/INDICE.md
  - docs/NOMENCLATURA.md
  - docs/adr/INDICE_ADR.md
  - docs/contratos/contrato_barra_de_menus.md
  - docs/contratos/contrato_cabecalho.md
  - docs/contratos/contrato_chip.md
  - docs/contratos/contrato_composicao_corpo.md
  - docs/contratos/contrato_console.md
  - docs/contratos/contrato_estilo.md
  - docs/contratos/contrato_json_console.md
  - docs/contratos/contrato_json_dashboard.md
  - docs/contratos/contrato_lancador.md
  - docs/contratos/contrato_tela_json.md
  - tela/teste_renderizador.py
arquivos_nao_rastreados:
  - docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md
  - docs/nomenclatura/
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-1.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-2.md
  - docs/relatorios/RELATORIO_HISTORICO_NOMENCLATURA_MONOLITICA.md
  - docs/relatorios/RELATORIO_LEVANTAMENTO_REORGANIZACAO_NOMENCLATURA.md
  - docs/relatorios/RELATORIO_QA_ADR-0029.md
  - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0029_FASE-1.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0029.md
arquivos_da_fase_2: 38
arquivos_inesperados: []
stage_vazio: true
commit_executado: false
git_diff_check: OK
git_diff_cached_name_only: vazio
```

`git diff --stat` antes da complementação deste relatório registrou 19 arquivos rastreados modificados, `296 insertions(+)` e `1905 deletions(-)`. O relatório atual é não rastreado; a complementação desta etapa altera somente este arquivo.

## 20. Condições para QA

| Condição | Estado | Evidência |
| --------------------------------------- | ------ | --------- |
| fachada criada sem definições próprias | SATISFEITA | `docs/NOMENCLATURA.md` declara fachada e proíbe definições novas |
| 17 módulos vigentes | SATISFEITA | frontmatter dos 17 módulos com `fase_de_aplicacao: VIGENTE` |
| nenhum módulo PRE_FACHADA | SATISFEITA | busca em módulos retornou 0 |
| índice geral com leitura seletiva | SATISFEITA | `docs/INDICE.md` item 3 |
| 9 contratos com dependências | SATISFEITA | nove blocos `dependencias_nomenclatura` |
| condicionais com gatilho | SATISFEITA | todo `modulo` condicional tem `quando` |
| referências normativas antigas migradas | SATISFEITA | contratos/config/teste sem ocorrência normativa antiga |
| referências remanescentes classificadas | SATISFEITA | seção 10 deste relatório |
| regras comportamentais preservadas | SATISFEITA | alterações contratuais restritas a dependências e referências |
| propriedade terminológica preservada | SATISFEITA | seção 14 |
| pendências e deferimentos preservados | SATISFEITA | seção 12 |
| ADR e índice ADR coerentes | SATISFEITA | `status: aceita e aplicada`; linha ADR-0029 no índice |
| JSONs válidos | SATISFEITA | parse dos cinco JSONs OK |
| Python sintaticamente válido | SATISFEITA | `py_compile` OK com saída em `/tmp` |
| consistência documental aprovada | SATISFEITA | seção 18 com resultados `CONSISTENTE` |
| stage vazio | SATISFEITA | `git diff --cached --name-only` vazio |
| QA da fase 2 ainda não executado | SATISFEITA | esta etapa não executou QA |

```yaml
status_literal: APLICACAO_ADR_FASE_2_CONCLUIDA_AGUARDANDO_QA
proxima_categoria: QA_APLICACAO_ADR_FASE_2
```

## 21. Encerramento

```yaml
etapa_executada: COMPLEMENTAR_RELATORIO_APLICACAO_ADR_FASE_2
fase: FASE_2_MIGRACAO_DEFINITIVA
adr: docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md

pre_condicao:
  relatorio: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0029_FASE-1.md
  status_literal: APLICACAO_ADR_FASE_1_APPROVED_WITH_NOTES

fachada:
  arquivo: docs/NOMENCLATURA.md
  criada: true
  possui_definicoes_proprias: false

modulos:
  esperados: 17
  promovidos_a_vigentes: 17
  ainda_PRE_FACHADA: 0
  ainda_apontam_monolito_como_autoridade: 0

contratos:
  esperados_com_dependencias: 9
  atualizados: 9
  sem_dependencias: 0
  condicionais_sem_gatilho: 0
  contrato_adicional_com_referencia_migrada: docs/contratos/contrato_json_dashboard.md

arquivos:
  existentes_alterados: 37
  criados: 1
  artefatos_tocados_na_fase_2: 38

referencias:
  metodo_de_contagem: ocorrencias_distintas_em_diff_material_incluindo_origem_especificacao
  contratos: 38
  configuracoes: 8
  codigo_ou_teste: 1
  total: 47
  ativas_remanescentes: 0
  historicas_preservadas: true

propriedade:
  termos_ativos_sem_proprietario: 0
  definicoes_duplicadas: 0
  regras_ativas_sem_contrato_comprovado: 0
  fachada_com_definicoes_proprias: false

pendencias:
  preservadas: true
  resolvidas_sem_autoridade: 0
  termos_deferidos_canonizados: 0

documentos:
  indice_geral_atualizado: true
  ADR_atualizada: true
  indice_ADR_atualizado: true
  relatorio_atualizado: docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-2.md

verificacoes:
  JSON: OK
  Python: OK
  Markdown_YAML_caminhos: OK
  consistencia_documental: CONSISTENTE

implementacao_funcional_afetada: false
fase_2_executada: true
QA_fase_2_executado: false

git_diff_check: OK
stage_vazio: true
commit_executado: false

status_literal: APLICACAO_ADR_FASE_2_CONCLUIDA_AGUARDANDO_QA
proxima_categoria: QA_APLICACAO_ADR_FASE_2
```

## 22. Patch após o QA da fase 2

### 22.1 QA de origem

```yaml
relatorio_QA:
  arquivo: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0029_FASE-2.md
  status_literal: APLICACAO_ADR_FASE_2_REJECTED
  achados_corretivos: 3
```

### 22.2 Correções

| Achado      | Arquivos corrigidos                                             | Correção executada                                                            | Resultado declarado pelo autor |
| ----------- | --------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------ |
| `QA-F2-001` | `docs/build_docs/instruction.md`, `docs/build_docs/prompts.md` | leitura normativa antiga substituída por leitura seletiva modular             | CORRIGIDO_AGUARDANDO_QA        |
| `QA-F2-002` | módulos `01` e `02`                                             | papel antigo do monólito marcado como histórico; fachada atual sem autoridade | CORRIGIDO_AGUARDANDO_QA        |
| `QA-F2-003` | `docs/adr/INDICE_ADR.md`                                        | fase 2 corrigida aguardando QA pós-patch registrada                           | CORRIGIDO_AGUARDANDO_QA        |

Esses resultados são declarações do autor, não aprovação de QA.

### 22.3 Arquivos alterados pelo patch

```yaml
arquivos_alterados_no_patch:
  - docs/build_docs/instruction.md
  - docs/build_docs/prompts.md
  - docs/nomenclatura/01_NUCLEO_COMUM.md
  - docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md
  - docs/adr/INDICE_ADR.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-2.md
```

`docs/build_docs/to_do.md` não foi alterado: não contém instrução operacional diretamente relacionada a leitura normativa do antigo monólito — as referências a seções do `NOMENCLATURA.md` nos itens `concluido` e `bloqueado_decisao` são registros históricos de origem, não instruções executáveis. O campo `status: em_andamento` não foi tocado.

### 22.4 Relatórios separados

```yaml
relatorio_QA_original_preservado: true
relatorio_QA_original_alterado: false
QA_pos_patch_executado: false
relatorio_QA_pos_patch_criado: false
```

### 22.5 Buscas mecânicas pós-correção

#### 22.5.1 `docs/build_docs/`

Referências remanescentes a `docs/NOMENCLATURA.md`:

| Arquivo | Linha | Contexto | Classificação |
| ------- | ----- | -------- | ------------- |
| `instruction.md` | 15 | `fachada \`docs/NOMENCLATURA.md\`` no escopo da pasta | `FACHADA_DE_NAVEGACAO` |
| `instruction.md` | 80 | `O Codex **nunca lê** \`docs/NOMENCLATURA.md\`` | instrução restritiva — proíbe leitura |
| `instruction.md` | 112 | `Não ler nem citar docs/NOMENCLATURA.md` (dentro do modelo de prompt de extração) | instrução restritiva — proíbe leitura |
| `prompts.md` | 83 | `docs/NOMENCLATURA.md como fachada de navegação` | `FACHADA_DE_NAVEGACAO` |

Nenhuma referência remanescente trata `docs/NOMENCLATURA.md` como fonte normativa completa ou instrui a consultar seções numeradas antigas como autoridade vigente.

#### 22.5.2 Módulos `01` e `02`

Referências remanescentes a `docs/NOMENCLATURA.md` nos módulos:

| Módulo | Linha | Contexto | Classificação |
| ------ | ----- | -------- | ------------- |
| `01` | 17 | `fachada_de_navegacao: docs/NOMENCLATURA.md` (frontmatter YAML) | `FACHADA_DE_NAVEGACAO` |
| `01` | 83–86 | "No antigo monólito, substituído pela fachada... A autoridade vigente deste domínio é o presente módulo... atua somente como fachada" | `HISTORICO_DO_MONOLITO` + estado atual correto |
| `01` | 183–185 | "atribuído ao antigo `docs/NOMENCLATURA.md`; autoridade migrada para os módulos proprietários" | `HISTORICO_DO_MONOLITO` |
| `02` | 17 | `fachada_de_navegacao: docs/NOMENCLATURA.md` (frontmatter YAML) | `FACHADA_DE_NAVEGACAO` |
| `02` | 51 | `papel atual como fachada de compatibilidade e navegação` | estado atual correto |
| `02` | 72 | "No antigo monólito... Atualmente atua somente como fachada de compatibilidade e navegação" | `HISTORICO_DO_MONOLITO` + estado atual correto |
| `02` | 116 | "nos módulos proprietários; `docs/NOMENCLATURA.md` atua somente como fachada" | estado atual correto |

Nenhuma frase restante permite interpretar a fachada como fonte atual de schema ou semântica.

#### 22.5.3 Índice de ADRs

A linha da ADR-0029 em `docs/adr/INDICE_ADR.md` contém:

```text
QA pós-FASE_2 inicial: APLICACAO_ADR_FASE_2_REJECTED;
PATCH_APLICACAO_ADR_FASE_2 aplicado;
aguardando QA_POS_PATCH_APLICACAO_ADR_FASE_2
```

Confirmado mecanicamente via `grep ADR-0029 docs/adr/INDICE_ADR.md`.

### 22.6 Encerramento

```yaml
etapa_executada: PATCH_APLICACAO_ADR_FASE_2
fase: FASE_2_MIGRACAO_DEFINITIVA
QA_origem:
  arquivo: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0029_FASE-2.md
  status_literal: APLICACAO_ADR_FASE_2_REJECTED

achados_tratados:
  QA-F2-001: CORRIGIDO_AGUARDANDO_QA
  QA-F2-002: CORRIGIDO_AGUARDANDO_QA
  QA-F2-003: CORRIGIDO_AGUARDANDO_QA

arquivos_alterados_no_patch:
  - docs/build_docs/instruction.md
  - docs/build_docs/prompts.md
  - docs/nomenclatura/01_NUCLEO_COMUM.md
  - docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md
  - docs/adr/INDICE_ADR.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-2.md

relatorio_QA_original_preservado: true
relatorio_QA_original_alterado: false

verificacoes_mecanicas:
  git_diff_check: OK
  markdown: fences balanceadas; newline final presente; sem trailing whitespace; sem marcadores de conflito
  caminhos: todos os caminhos mencionados nas correções existem
  stage_vazio: true

commit_executado: false
QA_pos_patch_executado: false

status_literal: APLICACAO_ADR_FASE_2_CORRIGIDA_AGUARDANDO_QA_POS_PATCH
proxima_categoria: QA_POS_PATCH_APLICACAO_ADR_FASE_2
```
