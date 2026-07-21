# Relatório de QA da aplicação — ADR-0029 — fase 2

## 1. Identificação

```yaml
etapa_executada: QA_APLICACAO_ADR_FASE_2
fase_auditada: FASE_2_MIGRACAO_DEFINITIVA
data_auditoria: 2026-07-21
auditor: Codex
escopo: auditoria_documental_independente
arquivo_criado: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0029_FASE-2.md
```

## 2. Objetivo e limites

Esta auditoria verificou materialmente a aplicação da fase 2 da ADR-0029 no estado físico do repositório. O objetivo foi determinar se a fase `FASE_2_MIGRACAO_DEFINITIVA` pode ser aprovada.

Limites observados: nenhum artefato auditado foi corrigido; nenhum JSON, contrato, módulo, ADR, índice, código ou relatório de aplicação foi alterado; não foi feito stage; não foi feito commit; não foi executada etapa posterior.

## 3. Estado factual de entrada

| Alegação de entrada | Confirmado | Resultado |
|---|---:|---|
| `fachada_criada: true` | sim | CONFORME |
| `modulos_vigentes: 17` | 17 | CONFORME |
| `contratos_com_dependencias: 9` | 9 | CONFORME |
| `contrato_adicional_com_referencia_migrada: 1` | 1 | CONFORME |
| `referencias_migradas.contratos: 38` | 38 | CONFORME |
| `referencias_migradas.configuracoes: 8` | 8 | CONFORME |
| `referencias_migradas.codigo_ou_teste: 1` | 1 | CONFORME |
| `stage_vazio: true` | sim | CONFORME |
| `commit_executado: false` | sim | CONFORME |

Observação de inventário: `git diff --name-only` confirma 19 arquivos rastreados modificados. A contagem declarada de 38 artefatos tocados depende do inventário nominal da fase 2 e de arquivos ainda não rastreados vindos da fase 1; ela é materialmente coerente, mas não é totalmente reprodutível apenas por diff Git.

## 4. Autoridades consultadas

Leitura integral: ADR-0029, QA da fase 1, relatório de aplicação da fase 2, `docs/NOMENCLATURA.md`, `docs/INDICE.md`, `docs/adr/INDICE_ADR.md`, os 17 módulos em `docs/nomenclatura/`, os nove contratos com `dependencias_nomenclatura`, `docs/contratos/contrato_json_dashboard.md`, os cinco JSONs alterados e o trecho alterado de `tela/teste_renderizador.py`.

Leitura seletiva: seção 12 do relatório de aplicação da fase 1; `docs/build_docs/`; buscas dirigidas por referências remanescentes.

## 5. Auditoria da fachada

| Critério | Resultado |
|---|---|
| `tipo: fachada_de_compatibilidade_e_navegacao` | CONFORME |
| `possui_definicoes_proprias: false` | CONFORME |
| índice modular `docs/nomenclatura/00_INDICE.md` | CONFORME |
| autoridade terminológica nos módulos proprietários | CONFORME |
| autoridade comportamental nos contratos | CONFORME |
| leitura preventiva de todos os módulos proibida | CONFORME |
| links para os 17 módulos | CONFORME |
| mapa de compatibilidade das seções antigas | CONFORME |
| referência ao relatório histórico | CONFORME |
| ausência de âncoras antigas simuladas como autoridade vigente | CONFORME |

A explicação de navegação da fachada não foi tratada como definição própria.

## 6. Auditoria dos módulos vigentes

| Módulo | VIGENTE | Proprietário ou roteador | Fachada correta | Resíduo ativo | Resultado |
| ------ | ------- | ------------------------ | --------------- | ------------- | --------- |
| `00_INDICE.md` | sim | roteador | equivalente | não | CONFORME |
| `01_NUCLEO_COMUM.md` | sim | proprietário | sim | sim | ACHADO |
| `02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` | sim | proprietário | sim | sim | ACHADO |
| `10_ESTILO.md` | sim | proprietário | sim | não | CONFORME |
| `20_TELA_CORPO_E_COMPOSICAO.md` | sim | proprietário | sim | não | CONFORME |
| `21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` | sim | proprietário | sim | não | CONFORME |
| `30_CABECALHO.md` | sim | proprietário | sim | não | CONFORME |
| `31_BARRA_DE_MENUS_E_CHIPS.md` | sim | proprietário | sim | não | CONFORME |
| `32_CONSOLE.md` | sim | proprietário | sim | não | CONFORME |
| `33_LANCADOR.md` | sim | proprietário | sim | não | CONFORME |
| `34_DASHBOARD.md` | sim | proprietário | sim | não | CONFORME |
| `40_GRUPOS_E_DISTRIBUICAO_DE_AREA.md` | sim | proprietário | sim | não | CONFORME |
| `41_DISTRIBUICAO_MATRICIAL.md` | sim | proprietário | sim | não | CONFORME |
| `42_DADOS_EXTERNOS_MULTINIVEL.md` | sim | proprietário | sim | não | CONFORME |
| `43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md` | sim | proprietário | sim | não | CONFORME |
| `44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` | sim | proprietário | sim | não | CONFORME |
| `90_ALIASES_E_TERMOS_DESCONTINUADOS.md` | sim | proprietário | sim | não | CONFORME |

Buscas por `PRE_FACHADA`, `fonte_normativa_ainda_vigente`, `proprietario_futuro_do_dominio`, `aguardando_auditoria_documental` e `substituicao_de_autoridade_executada: false` retornaram zero nos módulos. O resíduo ativo identificado é semântico: módulos `01` e `02` ainda descrevem `docs/NOMENCLATURA.md` como schema/semântica sem marcação histórica suficiente.

## 7. Auditoria do índice e da leitura seletiva

`docs/INDICE.md` orienta identificar atividade, contrato ou artefato alvo; carregar dependências obrigatórias; avaliar condicionais; e usar a fachada como navegação. Não exige leitura preventiva integral de `docs/NOMENCLATURA.md`, não exige leitura automática dos 17 módulos e não impõe núcleo comum fora das dependências declaradas.

Resultado: CONFORME.

## 8. Auditoria das dependências dos contratos

| Contrato | Obrigatórias | Condicionais | Gatilhos completos | Caminhos válidos | Resultado |
| -------- | ------------ | ------------ | ------------------ | ---------------- | --------- |
| `contrato_estilo.md` | 2 | 3 | sim | sim | CONFORME |
| `contrato_composicao_corpo.md` | 3 | 7 | sim | sim | CONFORME |
| `contrato_barra_de_menus.md` | 2 | 4 | sim | sim | CONFORME |
| `contrato_cabecalho.md` | 2 | 2 | sim | sim | CONFORME |
| `contrato_lancador.md` | 2 | 3 | sim | sim | CONFORME |
| `contrato_console.md` | 2 | 5 | sim | sim | CONFORME |
| `contrato_chip.md` | 2 | 5 | sim | sim | CONFORME |
| `contrato_tela_json.md` | 3 | 11 | sim | sim | CONFORME |
| `contrato_json_console.md` | 3 | 4 | sim | sim | CONFORME |

Cada contrato tem um único mecanismo `dependencias_nomenclatura`; os blocos são YAML válido; `00_INDICE.md` não aparece como dependência normativa; não há leitura preventiva de todos os módulos.

`docs/contratos/contrato_json_dashboard.md` teve somente a referência ativa à nomenclatura migrada para `docs/nomenclatura/34_DASHBOARD.md`, sem mecanismo parcial de dependências e sem alteração comportamental detectada.

## 9. Comparação com as propostas da fase 1

| Contrato | Proposta da fase 1 | Materialização da fase 2 | Evidência contratual para a mudança | Resultado |
| -------- | ------------------ | ------------------------ | ----------------------------------- | --------- |
| `contrato_estilo.md` | 2 obrigatórias, 3 condicionais | igual | não houve diferença | CONFORME |
| `contrato_composicao_corpo.md` | 3 obrigatórias, 7 condicionais | igual | não houve diferença | CONFORME |
| `contrato_barra_de_menus.md` | 2 obrigatórias, 4 condicionais | igual | não houve diferença | CONFORME |
| `contrato_cabecalho.md` | 2 obrigatórias, 2 condicionais | igual | não houve diferença | CONFORME |
| `contrato_lancador.md` | 2 obrigatórias, 3 condicionais | igual | não houve diferença | CONFORME |
| `contrato_console.md` | 2 obrigatórias, 5 condicionais | igual | não houve diferença | CONFORME |
| `contrato_chip.md` | 2 obrigatórias, 5 condicionais | igual | não houve diferença | CONFORME |
| `contrato_tela_json.md` | 3 obrigatórias, 11 condicionais | igual | não houve diferença | CONFORME |
| `contrato_json_console.md` | 3 obrigatórias, 4 condicionais | igual | não houve diferença | CONFORME |

Não foram identificadas divergências entre a seção 12 da fase 1 e os blocos materializados na fase 2.

## 10. Auditoria das referências migradas

```yaml
referencias_migradas_confirmadas:
  contratos: 38
  configuracoes: 8
  codigo_ou_teste: 1
  total: 47
diferenca_em_relacao_ao_relatorio: nenhuma_para_as_referencias_migradas_declaradas
```

Nos contratos, `git diff --unified=0` confirmou remoções contendo `NOMENCLATURA.md` na distribuição: 4, 7, 6, 3, 2, 4, 3, 5, 3 e 1, totalizando 38. Os campos `origem_especificacao` foram contados uma vez por ocorrência material, e a string múltipla em `contrato_composicao_corpo.md` foi contada como uma ocorrência de origem.

Nos JSONs, as oito substituições ocorreram em `config/estilo.json` (2), `config/elementos/barra_de_menus.json` (3), `config/layouts/layout_console.json` (1), `config/layouts/layout_dado.json` (1) e `config/layouts/layout_menu.json` (1).

Em `tela/teste_renderizador.py`, a alteração está limitada ao comentário antes de `TestCatalogoH0030`.

## 11. Auditoria das referências remanescentes

| Local | Classificação | Resultado |
|---|---|---|
| `docs/INDICE.md` | REFERENCIA_A_FACHADA | CONFORME |
| `docs/NOMENCLATURA.md` | REFERENCIA_A_FACHADA | CONFORME |
| campos `fachada_de_navegacao` dos módulos | REFERENCIA_A_FACHADA | CONFORME |
| ADR-0029 | HISTORICA_FECHADA / estado processual | CONFORME |
| `docs/adr/INDICE_ADR.md` | HISTORICA_FECHADA / estado processual | CONFORME_COM_ACHADO |
| módulos `01` e `02` | REFERENCIA_A_ANTIGA_AUTORIDADE | ACHADO |
| módulo `90` | HISTORICA_FECHADA | CONFORME |
| contratos, configs e teste alterados | sem ocorrência antiga ativa | CONFORME |
| `docs/build_docs/` | RESIDUO_ATIVO_INCORRETO | ACHADO |

Achado principal: `docs/build_docs/instruction.md` e `docs/build_docs/prompts.md` ainda instruem sessões operacionais a usar `docs/NOMENCLATURA.md` e suas seções como fonte de nomes/decisões. A pasta não está arquivada fisicamente e `docs/build_docs/to_do.md` declara `status: em_andamento`, portanto as referências não são apenas históricas fechadas.

Achado adicional: `docs/nomenclatura/01_NUCLEO_COMUM.md` e `docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` ainda descrevem `docs/NOMENCLATURA.md` como responsável por schema e semântica. Após a fase 2, esse caminho é fachada; a autoridade terminológica deve estar nos módulos proprietários.

## 12. Auditoria das regras comportamentais

| Contrato | Alteração apenas documental | Regra removida ou modificada | Resultado |
|---|---|---|---|
| `contrato_estilo.md` | sim | não | CONFORME |
| `contrato_composicao_corpo.md` | sim | não | CONFORME |
| `contrato_barra_de_menus.md` | sim | não | CONFORME |
| `contrato_cabecalho.md` | sim | não | CONFORME |
| `contrato_lancador.md` | sim | não | CONFORME |
| `contrato_console.md` | sim | não | CONFORME |
| `contrato_chip.md` | sim | não | CONFORME |
| `contrato_tela_json.md` | sim | não | CONFORME |
| `contrato_json_console.md` | sim | não | CONFORME |
| `contrato_json_dashboard.md` | sim | não | CONFORME |

As mudanças se limitaram a `dependencias_nomenclatura`, `origem_especificacao`, links/referências documentais e remoção de orientação obsoleta para atualizar o monólito.

## 13. Auditoria da propriedade terminológica

```yaml
termos_ativos_sem_proprietario: 0
definicoes_duplicadas: 0
regras_ativas_sem_contrato_comprovado: 0
fachada_com_definicoes_proprias: false
```

As fronteiras aprovadas na fase 1 foram preservadas: `config/estilo.json`, `barra_de_menus`, grupo estrutural, JSON estrutural da tela, chip, loader, vão, célula e coluna possuem proprietário por domínio ou sentido.

Ressalva corretiva: a propriedade do papel atual de `docs/NOMENCLATURA.md` fica inconsistente nos módulos `01` e `02`, que ainda o descrevem como schema/semântica em vez de fachada.

## 14. Auditoria das pendências e deferimentos

| Pendência ou deferimento | Preservado sem resolução | Resultado |
|---|---|---|
| `tx` | sim | CONFORME |
| `popup_execucao` | sim | CONFORME |
| alinhamento horizontal do dashboard | sim | CONFORME |
| segunda pauta de estilos de exibição | sim | CONFORME |
| campos de navegação do lançador | sim | CONFORME |
| reorganização corpo x dashboard | sim | CONFORME |
| folha x conteudo | sim | CONFORME |
| campo x nome_valor | sim | CONFORME |
| hierarquia_indentada x hierarquia | sim | CONFORME |
| modo normal x modo não verboso | sim | CONFORME |
| protocolo produtor/Pipeline | sim | CONFORME |
| migração legada D23 | sim | CONFORME |

Não foi detectada resolução unilateral, promoção a definição ativa ou canonização indevida dos termos deferidos.

## 15. Auditoria da ADR e do índice de ADRs

Na ADR-0029, o frontmatter registra `status: aceita e aplicada`; o encerramento registra `status_literal: ADR_ACCEPTED_AND_APPLIED` e `proxima_categoria: QA_FASE_2`. A convenção `aceita e aplicada` é compatível com ADRs aplicadas anteriores. A equivalência entre `QA_FASE_2` e `QA_APLICACAO_ADR_FASE_2` é semanticamente plausível, mas é nomenclatura local.

Em `docs/adr/INDICE_ADR.md`, apenas a linha da ADR-0029 foi adicionada. Porém a linha registra QA pós-FASE_1 e não registra de forma inequívoca que a FASE_2 está aguardando QA. Isso é achado corretivo baixo por lacuna processual no índice.

## 16. Auditoria do inventário e do escopo

| Categoria | Declarado | Confirmado |
|---|---:|---:|
| fachada | 1 | 1 |
| módulos | 17 | 17 |
| documentos gerais | 3 | 3 |
| contratos | 10 | 10 |
| configurações | 5 | 5 |
| teste | 1 | 1 |
| relatório criado | 1 | 1 |
| artefatos tocados nominais | 38 | 38 |

Arquivos fora do escopo da fase 2: nenhum detectado entre os arquivos modificados ou declarados. A presença de arquivos não rastreados da fase 1 foi diferenciada e não foi presumida como criação da fase 2.

## 17. Verificações mecânicas e funcionais

| Verificação | Resultado |
|---|---|
| parse YAML da ADR-0029 | OK |
| parse YAML dos 17 módulos | OK |
| parse dos blocos `dependencias_nomenclatura` | OK |
| parse dos cinco JSONs | OK |
| sintaxe de `tela/teste_renderizador.py` | OK |
| caminhos novos em dependências | OK |
| fences Markdown | OK |
| newline final | OK |
| trailing whitespace | OK |
| marcadores de conflito | OK |
| `git diff --check` | OK |
| alteração funcional nos JSONs | não detectada |
| alteração executável no teste | não detectada |

Comando de sintaxe Python executado com bytecode em `/tmp`: `python -B -c "import py_compile; py_compile.compile(...)"`.

## 18. Estado Git

```yaml
branch: master
HEAD: c90349c feat: implementa apresentacoes multinivel com modos por tela
arquivos_rastreados_modificados: 19
arquivos_nao_rastreados_relacionados_adr_0029: 9
git_diff_check: OK
stage_vazio: true
commit_executado: false
```

Comandos executados: `git branch --show-current`, `git log -1 --oneline`, `git status --short`, `git diff --name-only`, `git diff --stat`, `git diff --check` e `git diff --cached --name-only`.

## 19. Achados

| ID | Severidade | Achado | Evidência | Corretivo |
|---|---|---|---|---|
| QA-F2-001 | ALTO | Resíduo ativo incorreto em `docs/build_docs/` ainda orienta uso de `docs/NOMENCLATURA.md` e seções antigas como fonte operacional de decisões/nomenclatura. | `docs/build_docs/instruction.md`, `docs/build_docs/prompts.md`, `docs/build_docs/to_do.md` com `status: em_andamento` | sim |
| QA-F2-002 | MEDIO | Módulos `01` e `02` ainda descrevem `docs/NOMENCLATURA.md` como schema/semântica, o que conflita com a fachada sem autoridade terminológica própria. | `docs/nomenclatura/01_NUCLEO_COMUM.md`, `docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` | sim |
| QA-F2-003 | BAIXO | `docs/adr/INDICE_ADR.md` não indica de forma inequívoca que a fase 2 da ADR-0029 aguarda QA; menciona apenas QA pós-FASE_1. | linha ADR-0029 em `docs/adr/INDICE_ADR.md` | sim |
| OBS-F2-001 | OBSERVACAO | A contagem de 38 artefatos tocados é coerente por inventário nominal, mas não totalmente reproduzível por diff Git porque artefatos da fase 1 seguem não rastreados. | `git status --short`, relatório da fase 2 | não |
| OBS-F2-002 | OBSERVACAO | Os literais `ADR_ACCEPTED_AND_APPLIED` e `QA_FASE_2` são equivalentes semanticamente ao estado aplicado aguardando QA, mas usam nomenclatura local. | ADR-0029 e precedentes ADR-0025 a ADR-0028 | não |

## 20. Status final

```yaml
status_literal: APLICACAO_ADR_FASE_2_REJECTED
status_normalizado: rejected
motivo: achados_corretivos_maiores_que_zero
achados_corretivos: 3
```

## 21. Próxima categoria

```yaml
proxima_categoria: PATCH_APLICACAO_ADR_FASE_2
executada: false
```

## 22. Encerramento

```yaml
etapa_executada: QA_APLICACAO_ADR_FASE_2
fase: FASE_2_MIGRACAO_DEFINITIVA
adr: docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md
relatorio_aplicacao: docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-2.md
relatorio_criado: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0029_FASE-2.md

fachada:
  possui_definicoes_proprias: false
  leitura_seletiva: true
  links_validos: true

modulos:
  esperados: 17
  auditados: 17
  vigentes: 17
  ainda_PRE_FACHADA: 0
  com_autoridade_incorreta: 2

contratos:
  esperados_com_dependencias: 9
  auditados: 9
  sem_dependencias: 0
  condicionais_sem_gatilho: 0
  divergencias_fase_1_fundamentadas: 0
  divergencias_fase_1_sem_fundamento: 0

referencias:
  contratos_declaradas: 38
  contratos_confirmadas: 38
  configuracoes_declaradas: 8
  configuracoes_confirmadas: 8
  codigo_declaradas: 1
  codigo_confirmadas: 1
  total_declarado: 47
  total_confirmado: 47
  normativas_antigas_remanescentes: 3

propriedade:
  termos_ativos_sem_proprietario: 0
  definicoes_duplicadas: 0
  regras_ativas_sem_contrato_comprovado: 0
  pendencias_resolvidas_sem_autoridade: 0

arquivos:
  existentes_alterados_declarados: 37
  existentes_alterados_confirmados: 37
  criados_declarados: 1
  criados_confirmados: 1
  artefatos_tocados_confirmados: 38
  fora_do_escopo: 0

literais:
  status_ADR_fisico: ADR_ACCEPTED_AND_APPLIED
  status_ADR_normalizado: ADR_APPLIED_AWAITING_QA
  proxima_categoria_fisica: QA_FASE_2
  proxima_categoria_normalizada: QA_APLICACAO_ADR_FASE_2

achados_bloqueantes: 0
achados_altos: 1
achados_medios: 1
achados_baixos: 1
observacoes: 2
bloqueios: 0

stage_vazio: true
commit_executado: false

status_literal: APLICACAO_ADR_FASE_2_REJECTED
status_normalizado: rejected
proxima_categoria: PATCH_APLICACAO_ADR_FASE_2
```
