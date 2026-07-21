# Relatório de QA da aplicação — ADR-0029 — fase 1

## 1. Identificação

```yaml
etapa_executada: QA_APLICACAO_ADR_FASE_1
fase_auditada: FASE_1_MATERIALIZACAO_PRE_FACHADA
data_auditoria: 2026-07-21
auditor: Codex
escopo: auditoria_documental_independente
```

## 2. Objetivo e limites

Esta auditoria verificou a materialização documental da fase 1 da aplicação da ADR-0029. O objetivo foi confirmar se a base modular PRE_FACHADA está pronta para aprovação, preservando o monólito vigente e sem executar a fase 2.

Limites observados: nenhum artefato auditado foi corrigido; a fase 2 não foi executada; `docs/NOMENCLATURA.md` não foi convertido em fachada; contratos, módulos, índices, ADR, relatórios anteriores, backlog, issues, código e configurações não foram alterados por esta auditoria.

## 3. Estado factual de entrada

| Item | Esperado | Confirmado | Resultado |
|---|---:|---:|---|
| ADR status | aceita | aceita | CONFORME |
| Fase 1 | aplicada | aplicada | CONFORME |
| Fase 2 | nao_executada | nao_executada | CONFORME |
| Módulos esperados | 17 | 17 | CONFORME |
| Módulos existentes | 17 | 17 | CONFORME |
| Blocos NOM-LEV esperados | 28 | 28 no levantamento e 28 no relatório de aplicação | CONFORME |
| Status literal da aplicação | APLICACAO_ADR_FASE_1_CONCLUIDA_AGUARDANDO_QA | confirmado | CONFORME |
| Termos ativos sem proprietário | 0 | 0 | CONFORME |
| Definições duplicadas entre módulos | 0 | 0 | CONFORME |
| Regras ativas sem contrato comprovado | 0 | 0 | CONFORME |
| Branch | master | master | CONFORME |
| HEAD | c90349c | c90349c feat: implementa apresentacoes multinivel com modos por tela | CONFORME |
| Stage | vazio | vazio | CONFORME |
| Commit da fase | nao_executado | nao_executado | CONFORME |

## 4. Autoridades consultadas

Foram consultadas as autoridades exigidas: ADR-0029, levantamento, QA da ADR, QA pós-patch, relatório histórico, relatório de aplicação da fase 1, `docs/NOMENCLATURA.md`, `docs/INDICE.md`, `docs/adr/INDICE_ADR.md`, os 17 módulos de `docs/nomenclatura/` e os 11 contratos indicados.

Consultas seletivas adicionais: buscas em `docs/`, `config/`, `tela/` e `demo/` para referências antigas; comandos Git exigidos; validação YAML dos frontmatters da ADR-0029 e dos módulos.

## 5. Auditoria da estrutura modular

Todos os módulos possuem arquivo físico, título coerente, frontmatter carregável, `fase_de_aplicacao: PRE_FACHADA`, indicação de `docs/NOMENCLATURA.md` como fonte vigente, `substituicao_de_autoridade_executada: false`, responsabilidade delimitada, termos proprietários, definições, distinções, relações com contratos/ADRs, conteúdo excluído e proveniência.

| Módulo | Existe | PRE_FACHADA | Responsabilidade delimitada | Termos proprietários coerentes | Proveniência | Resultado |
|---|---|---|---|---|---|---|
| `00_INDICE.md` | sim | sim | sim | sim | sim | CONFORME |
| `01_NUCLEO_COMUM.md` | sim | sim | sim | sim | sim | CONFORME |
| `02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` | sim | sim | sim | sim | sim | CONFORME |
| `10_ESTILO.md` | sim | sim | sim | sim | sim | CONFORME |
| `20_TELA_CORPO_E_COMPOSICAO.md` | sim | sim | sim | sim | sim | CONFORME |
| `21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` | sim | sim | sim | sim | sim | CONFORME |
| `30_CABECALHO.md` | sim | sim | sim | sim | sim | CONFORME |
| `31_BARRA_DE_MENUS_E_CHIPS.md` | sim | sim | sim | sim | sim | CONFORME |
| `32_CONSOLE.md` | sim | sim | sim | sim | sim | CONFORME |
| `33_LANCADOR.md` | sim | sim | sim | sim | sim | CONFORME |
| `34_DASHBOARD.md` | sim | sim | sim | sim | sim | CONFORME_COM_NOTA |
| `40_GRUPOS_E_DISTRIBUICAO_DE_AREA.md` | sim | sim | sim | sim | sim | CONFORME |
| `41_DISTRIBUICAO_MATRICIAL.md` | sim | sim | sim | sim | sim | CONFORME |
| `42_DADOS_EXTERNOS_MULTINIVEL.md` | sim | sim | sim | sim | sim | CONFORME_COM_NOTA |
| `43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md` | sim | sim | sim | sim | sim | CONFORME |
| `44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` | sim | sim | sim | sim | sim | CONFORME_COM_NOTA |
| `90_ALIASES_E_TERMOS_DESCONTINUADOS.md` | sim | sim | sim | sim | sim | CONFORME_COM_NOTA |

Notas: as seções `4A`/`8A` localizam deferimentos e termos concorrentes; não são defeito. O módulo `34` preserva alinhamento do dashboard como pendência, não como regra ativa.

## 6. Auditoria NOM-LEV-001 a NOM-LEV-028

| ID | Conteúdo original | Destino materializado | Preservação | Classificação | Resultado |
|---|---|---|---|---|---|
| NOM-LEV-001 | Metadados do monólito | Relatório de aplicação | preservado | METADADO_DE_ORIGEM_PRESERVADO_NO_RELATORIO | CONFORME |
| NOM-LEV-002 | Fonte única de nomes | `01`, `00` | preservado | regra terminológica | CONFORME |
| NOM-LEV-003 | Schema x dados | `01`, `02` | preservado | artefato/conceito transversal | CONFORME |
| NOM-LEV-004 | Motor/demo/produto | `02`, histórico | preservado | estrutural/reservado | CONFORME |
| NOM-LEV-005 | Status transitório JSON | relatório histórico | preservado | ESTADO_TRANSITORIO_HISTORICO | CONFORME |
| NOM-LEV-006 | Estilo universal | `10`, `20`, `90` | preservado | estilo/alias | CONFORME |
| NOM-LEV-007 | Estrutura de tela | `20`, `02` | preservado | tela/artefato | CONFORME |
| NOM-LEV-008 | Eixos de composição | `20` | preservado | distinção | CONFORME |
| NOM-LEV-009 | Console e seleção | `32` | preservado | termo/regra | CONFORME |
| NOM-LEV-010 | Navegação console | `32`, contratos | preservado | regra comportamental | CONFORME |
| NOM-LEV-011 | Barra e chips | `31`, `10`, `44` | preservado | barra/chips | CONFORME |
| NOM-LEV-012 | Layout/redimensionamento/largura | `21`, `33` | preservado | regra/termo | CONFORME |
| NOM-LEV-013 | Cabeçalho | `30` | preservado | componente | CONFORME |
| NOM-LEV-014 | Lançador | `33` | preservado | componente | CONFORME |
| NOM-LEV-015 | Dashboard | `34`, histórico | preservado | tipo universal + instância histórica | CONFORME |
| NOM-LEV-016 | Tiling | `10`, `20`, `90` | preservado | estilo/composição | CONFORME |
| NOM-LEV-017 | Pendências em aberto | relatório histórico e módulos pontuais | preservado | PENDENCIA_PRESERVADA_NAO_BLOQUEANTE_DA_FASE_1 | CONFORME |
| NOM-LEV-018 | Levantamento Codex legado | relatório histórico | preservado | LEVANTAMENTO_HISTORICO | CONFORME |
| NOM-LEV-019 | Lista parcial antiga de ADRs | relatório histórico, `INDICE_ADR` atual | preservado | HISTORICO; autoridade atual em `docs/adr/INDICE_ADR.md` | CONFORME |
| NOM-LEV-020 | `menu` -> `lancador` | `33`, `90`, histórico | preservado | substituição histórica | CONFORME |
| NOM-LEV-021 | Composição hierárquica | `20`, `40` | preservado | composição/distribuição | CONFORME |
| NOM-LEV-022 | Ausência de distribuição | `40` | preservado | distribuição | CONFORME |
| NOM-LEV-023 | Grupo livre/matriz | `40` | preservado | grupo estrutural | CONFORME |
| NOM-LEV-024 | Distribuição matricial | `41` | preservado | distribuição matricial | CONFORME |
| NOM-LEV-025 | JSON externo | `42` | preservado | dados externos | CONFORME |
| NOM-LEV-026 | Carregamento conjunto | `43` | preservado | carregamento | CONFORME |
| NOM-LEV-027 | Apresentações e modos | `44` | preservado | apresentação | CONFORME |
| NOM-LEV-028 | Política de modo D23 | `44`, histórico | preservado | D23/deferimento legado | CONFORME |

Nenhum bloco desapareceu, recebeu numeração errada, foi promovido indevidamente de histórico/pendência para regra ativa, ou foi atribuído a módulo incompatível sem rastreabilidade.

## 7. Auditoria de propriedade terminológica

| Fronteira | Estado auditado | Resultado |
|---|---|---|
| `config/estilo.json` | `02` é proprietário do artefato/caminho; `10` é proprietário do vocabulário de estilo | CONFORME |
| `barra_de_menus` | `31` é proprietário específico; `20` referencia como região concreta | CONFORME |
| `grupo` estrutural | `40` é proprietário; `20` referencia genericamente; `32` usa sentido de categoria do dado | CONFORME |
| `JSON estrutural da tela` | `02` é proprietário do termo/artefato; `42` usa referência de fronteira | CONFORME |

Sentidos distintos confirmados: chip visual (`10`) x chip entidade de interface (`31`); grupo nó estrutural (`40`) x grupo categoria do dado (`32`); loader transversal (`01`) x papel contextual (`43`); vão do lançador (`33`) x vão da distribuição matricial (`41`); célula de matriz de grupos (`40`) x célula de distribuição matricial (`41`); coluna do lançador (`33`) x coluna de distribuição matricial (`41`).

Resultado geral: termos ativos têm exatamente um proprietário; termos pendentes não foram contados como ativos; termos concorrentes deferidos estão localizáveis; termos descontinuados estão em `90` com termo atual.

## 8. Auditoria de pendências e deferimentos

| Item | Classificação confirmada | Resultado |
|---|---|---|
| `tx` | regra de ajuste pendente | CONFORME |
| `popup_execucao` | PENDENTE_SEM_DEFINICAO_APROVADA | CONFORME |
| alinhamento horizontal do dashboard | PENDENCIA_PRESERVADA_NAO_BLOQUEANTE_DA_FASE_1 | CONFORME |
| segunda pauta de estilos de exibição | pendência preservada | CONFORME |
| campos de navegação do lançador | pendência preservada | CONFORME |
| reorganização corpo x dashboard | pendência preservada | CONFORME |
| `folha` | TERMO_CONCORRENTE_DEFERIDO_LOCALIZAVEL | CONFORME |
| `campo` | TERMO_CONCORRENTE_DEFERIDO_LOCALIZAVEL | CONFORME |
| `hierarquia_indentada` | TERMO_CONCORRENTE_DEFERIDO_LOCALIZAVEL | CONFORME |
| modo normal x modo não verboso | DIVERGENCIA_TERMINOLOGICA_DEFERIDA_PRESERVADA | CONFORME |
| migração legada D23 | deferimento preservado | CONFORME |
| protocolo produtor/Pipeline | deferimento preservado | CONFORME |

Esses itens permanecem localizáveis, não foram resolvidos unilateralmente e não bloqueiam a fase 1. Bloqueiam apenas eliminação ou renomeação futura sem decisão.

## 9. Auditoria da preservação contratual

| Regra | Módulo terminológico | Contrato esperado | Seção esperada | Resultado |
|---|---|---|---|---|
| Redimensionamento reativo | `21` | `contrato_tela_json.md` | seção 24 | CONFORME |
| Cálculo de colunas do lançador | `33` | `contrato_lancador.md` | seções 6.1 a 6.7 | CONFORME |
| Composição hierárquica e distribuição | `40` | `contrato_composicao_corpo.md` | seções 5.7 a 5.24 | CONFORME |
| Navegação, seleção e cursor | `32` | `contrato_console.md` | seções 7 a 13 | CONFORME |
| Barra e chips | `31` | contratos da barra e chip | seções declaradas | CONFORME |
| Distribuição matricial | `41` | contratos JSON | seções declaradas | CONFORME |
| Dados externos | `42` | contratos console/JSON/tela | seções declaradas | CONFORME |
| Carregamento | `43` | contratos console/JSON/tela | seções declaradas | CONFORME |
| Apresentações e modos | `44` | contratos console/JSON/barra | seções declaradas | CONFORME |
| Dashboard ativo | `34` | `contrato_json_dashboard.md` | seções 1 a 9 | CONFORME |

As obrigações permanecem nos contratos. Os módulos terminológicos não assumem autoridade comportamental completa e as pendências foram separadas das regras ativas.

## 10. Auditoria das dependências propostas

| Contrato | Obrigatórias coerentes | Condicionais coerentes | Gatilhos objetivos | Leitura preventiva evitada | Resultado |
|---|---|---|---|---|---|
| `contrato_estilo.md` | sim | sim | sim | sim | CONFORME |
| `contrato_composicao_corpo.md` | sim | sim | sim | sim | CONFORME |
| `contrato_barra_de_menus.md` | sim | sim | sim | sim | CONFORME |
| `contrato_cabecalho.md` | sim | sim | sim | sim | CONFORME |
| `contrato_lancador.md` | sim | sim | sim | sim | CONFORME |
| `contrato_console.md` | sim | sim | sim | sim | CONFORME |
| `contrato_chip.md` | sim | sim | sim | sim | CONFORME |
| `contrato_tela_json.md` | sim | sim | sim | sim | CONFORME |
| `contrato_json_console.md` | sim | sim | sim | sim | CONFORME |

As listas são propostas da fase 1 e ainda não foram aplicadas aos contratos. `00_INDICE.md` não foi transformado em dependência normativa; `90_ALIASES...` é condicional quando aplicável.

## 11. Auditoria das referências antigas

O relatório de aplicação declara `referencias_antigas_inventariadas: 2720`, `arquivos_ATIVA_NORMATIVA: 17` e `ocorrencias_ATIVA_NORMATIVA: 67`. A busca dirigida confirmou ocorrências ativas nos alvos exigidos: `docs/INDICE.md`, `docs/contratos/`, `config/estilo.json`, `config/elementos/barra_de_menus.json`, `config/layouts/layout_console.json`, `config/layouts/layout_dado.json`, `config/layouts/layout_menu.json` e `tela/teste_renderizador.py`.

Reprodução mecânica adicional:

```text
rg -o "NOMENCLATURA" docs config tela demo | wc -l
1678

rg -o "NOMENCLATURA\\.md|docs/NOMENCLATURA" docs config tela demo | wc -l
1440
```

Essa contagem independente usa escopo/padrão mais estrito que o inventário declarado e não reproduz as 2720 ocorrências. A diferença é registrada como observação não corretiva, pois a amostragem dirigida confirma a existência, classificação, módulo futuro plausível e ação de fase 2 para as referências normativas relevantes. Documentos históricos não foram marcados para reescrita indevida.

## 12. Auditoria do relatório histórico

O relatório histórico preserva factualmente: instância da tela raiz; substituições `menu` -> `lancador`, `Info` -> `dashboard`, `dado` -> `console`; caminhos históricos; NOM-LEV-005; NOM-LEV-017; NOM-LEV-018 com `teste_classe_c.py` e `teste_combo.py`; NOM-LEV-019 como lista parcial de ADRs; divergência `modo normal` x `modo não verboso`; migração legada D23.

O relatório histórico não se apresenta como fonte normativa, não redefine termos ativos, não cria decisão e não associa NOM-LEV-019 ao dashboard.

## 13. Auditoria do estado pré-fachada

| Item | Estado | Resultado |
|---|---|---|
| `docs/NOMENCLATURA.md` | preservado e fonte normativa vigente | CONFORME |
| Módulos | PRE_FACHADA | CONFORME |
| Autoridade definitiva dos módulos | não assumida | CONFORME |
| Fachada | não criada | CONFORME |
| Fase 2 | não executada | CONFORME |

A coexistência entre monólito e módulos é `DUPLICACAO_TRANSITORIA_PRE_FACHADA`, permitida nesta fase. A condição de remoção está registrada: QA da fase 1 e conversão controlada da fachada/migração das referências antigas na fase 2.

## 14. Auditoria da coerência interna

| Seção do relatório de aplicação | Verificação | Resultado |
|---|---|---|
| 3 | descreve estado pós-patch e mantém fase 2 pendente | CONFORME |
| 5 | distingue fase original, patch principal e patch residual | CONFORME |
| 8 | registra `JSON estrutural da tela` com proprietário `02` | CONFORME |
| 9 | separa regras comportamentais dos módulos terminológicos | CONFORME |
| 15 | não deixa `DEFINICAO_DUPLICADA` ativa | CONFORME |
| 16 | trata as oito lacunas | CONFORME |
| 17 | não autoriza fase 2 antes do QA | CONFORME_COM_NOTA |
| 18 | Git coerente com o estado físico | CONFORME |
| 19 | registra oito arquivos do patch principal e três do residual | CONFORME |
| 20 | encerra formalmente o patch residual | CONFORME |

Nota editorial: a menção a “seções 1 a 19” na seção 17 é tratada como observação não corretiva, pois as 20 seções existem e o encerramento residual está íntegro.

## 15. Verificações Markdown e caminhos

| Verificação | Resultado |
|---|---|
| Frontmatter YAML da ADR-0029 e dos 17 módulos | CONFORME |
| Fences Markdown | CONFORME por contagem par nos artefatos auditados |
| Tabelas e títulos | CONFORME |
| Caminhos relativos existentes | CONFORME na amostragem dirigida |
| Caminho absoluto local persistido | não encontrado nos artefatos alvo | CONFORME |
| Marcadores de conflito | não encontrados | CONFORME |
| Newline final | presente | CONFORME |
| Trailing whitespace | não encontrado | CONFORME |
| Arquivo fora do escopo criado por esta auditoria | não | CONFORME |

`git diff --no-index --check /dev/null` não emitiu erros de whitespace para a ADR-0029, módulos e relatórios novos auditados.

## 16. Estado Git

Comandos executados a partir da raiz:

```text
git branch --show-current
master

git log -1 --oneline
c90349c feat: implementa apresentacoes multinivel com modos por tela

git status --short
 M docs/adr/INDICE_ADR.md
?? docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md
?? docs/nomenclatura/
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-1.md
?? docs/relatorios/RELATORIO_HISTORICO_NOMENCLATURA_MONOLITICA.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_REORGANIZACAO_NOMENCLATURA.md
?? docs/relatorios/RELATORIO_QA_ADR-0029.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0029.md

git diff --name-only
docs/adr/INDICE_ADR.md

git diff --stat
 docs/adr/INDICE_ADR.md | 1 +
 1 file changed, 1 insertion(+)

git diff --check
sem saída

git diff --cached --name-only
sem saída
```

Confirmações: branch e HEAD esperados; stage vazio; nenhum commit executado; `docs/NOMENCLATURA.md`, contratos, `docs/INDICE.md`, backlog, issues, código e configurações sem diff rastreado. Somente `docs/adr/INDICE_ADR.md` aparece como arquivo rastreado modificado. Os novos artefatos permanecem não rastreados.

## 17. Achados

| ID | Severidade | CONFORME | NAO_CONFORME | EVIDENCIA | IMPACTO |
|---|---|---|---|---|---|
| OBS-QA-APP-ADR0029-F1-001 | OBSERVACAO | Sim | Não | Busca estrita reproduziu 1678/1440 ocorrências, não 2720; amostragem dirigida confirmou as referências ativas exigidas | Sem impacto corretivo; registrar diferença de escopo da contagem |
| OBS-QA-APP-ADR0029-F1-002 | OBSERVACAO | Sim | Não | Seção 17 menciona “seções 1 a 19”, embora o relatório tenha 20 seções e encerramento residual íntegro | Nota editorial sem ambiguidade material |

Não foram encontrados achados bloqueantes, altos, médios ou baixos corretivos.

## 18. Status final

```text
APLICACAO_ADR_FASE_1_APPROVED_WITH_NOTES
```

Justificativa: nenhum achado corretivo foi identificado. Há somente observações não corretivas.

## 19. Próxima categoria

```text
APLICAR_ADR_FASE_2
```

Esta auditoria não executou a próxima categoria.

## 20. Encerramento

```yaml
etapa_executada: QA_APLICACAO_ADR_FASE_1
fase: FASE_1_MATERIALIZACAO_PRE_FACHADA
adr: docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md
relatorio_aplicacao: docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-1.md
relatorio_criado: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0029_FASE-1.md

modulos_esperados: 17
modulos_auditados: 17
blocos_NOM_LEV_esperados: 28
blocos_NOM_LEV_auditados: 28

termos_ativos_sem_proprietario: 0
definicoes_duplicadas_entre_modulos: 0
regras_ativas_sem_contrato_comprovado: 0
pendencias_indevidamente_promovidas: 0
termos_deferidos_indevidamente_canonizados: 0
referencias_antigas_inventariadas: 2720
lacunas_originais_resolvidas: 8

achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 0
observacoes: 2
bloqueios: 0

monolito_preservado: true
contratos_preservados: true
indice_geral_preservado: true
fase_2_executada: false
stage_vazio: true
commit_executado: false

status_literal: APLICACAO_ADR_FASE_1_APPROVED_WITH_NOTES
status_normalizado: aprovado_com_observacoes
proxima_categoria: APLICAR_ADR_FASE_2
```
