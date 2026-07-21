# Relatório de aplicação — ADR-0029 — fase 1

## 1. Identificação

```yaml
etapa_executada: PATCH_APLICACAO_ADR_FASE_1
fase: FASE_1_MATERIALIZACAO_PRE_FACHADA
data_base: 2026-07-20
data_patch: 2026-07-21
adr: docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md
relatorio_atualizado: docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-1.md
papel_exercido: correcao focal dos problemas materiais identificados no bloqueio anterior
limite_executado:
  - nao executar QA
  - nao executar fase 2
  - nao converter docs/NOMENCLATURA.md em fachada
  - nao alterar contratos
  - nao alterar monolito
  - nao fazer stage
  - nao fazer commit
```

## 2. Autoridades

Autoridades abertas integralmente nesta complementação:

| Documento | Evidência material usada |
|---|---|
| `docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md` | D-NOM-01 a D-NOM-16; critérios da seção 11; status `aceita`; D-NOM-16 exige auditoria antes da fachada |
| `docs/relatorios/RELATORIO_LEVANTAMENTO_REORGANIZACAO_NOMENCLATURA.md` | Inventário NOM-LEV-001 a NOM-LEV-028; seção 6 de termos; seção 7 de consumidores; seção 9 de responsabilidades distintas |
| `docs/relatorios/RELATORIO_QA_ADR-0029.md` | Achados originais da ADR antes do patch |
| `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0029.md` | Status `ADR_APPROVED_WITH_NOTES`; observações não corretivas |
| `docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-1.md` | Evidências preservadas: 17 módulos, 2 relatórios, ADR e índice ADR alterados, fase 2 não executada |
| `docs/relatorios/RELATORIO_HISTORICO_NOMENCLATURA_MONOLITICA.md` | Histórico de instância de dashboard, substituições, caminhos, pendências NOM-LEV-017 a 019 |
| `docs/NOMENCLATURA.md` | Monólito vigente; 1856 linhas; origem dos blocos NOM-LEV |
| `docs/nomenclatura/*.md` | 17 módulos abertos; frontmatter PRE_FACHADA; termos proprietários; proveniência |
| `docs/contratos/*.md` | Nove contratos consumidores exigidos abertos; referências a `docs/NOMENCLATURA.md` e seções antigas confirmadas |

Contratos exigidos e abertos integralmente: `contrato_estilo.md`, `contrato_composicao_corpo.md`, `contrato_barra_de_menus.md`, `contrato_cabecalho.md`, `contrato_lancador.md`, `contrato_console.md`, `contrato_chip.md`, `contrato_tela_json.md`, `contrato_json_console.md`.

## 3. Escopo e limite pré-fachada

Fatos preservados do relatório anterior:

- A fase 1 criou a estrutura modular sob `docs/nomenclatura/`.
- A fase 1 criou `docs/relatorios/RELATORIO_HISTORICO_NOMENCLATURA_MONOLITICA.md`.
- A fase 1 criou este relatório de aplicação.
- A fase 1 alterou `docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md`.
- A fase 1 alterou `docs/adr/INDICE_ADR.md`.
- A fase 1 não converteu `docs/NOMENCLATURA.md` em fachada.
- A fase 1 não alterou contratos, `docs/INDICE.md`, `docs/backlog.md`, `docs/issues.md`, código nem configuração.

Fato novo desta complementação: após o patch focal, as lacunas materiais identificadas no bloqueio anterior foram resolvidas ou reclassificadas com autoridade. A fase 2 permanece não autorizada porque o QA da fase 1 ainda não foi executado e porque a migração das referências antigas pertence à fase 2.

## 4. Arquivos criados

| Arquivo | Tipo | Evidência |
|---|---|---|
| `docs/nomenclatura/00_INDICE.md` | módulo índice | existe; frontmatter `fase_de_aplicacao: PRE_FACHADA`; seções de leitura seletiva |
| `docs/nomenclatura/01_NUCLEO_COMUM.md` | módulo | existe; termos transversais; proveniência NOM-LEV-002 e 003 |
| `docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` | módulo | existe; termos de artefato; proveniência NOM-LEV-003 e 004 |
| `docs/nomenclatura/10_ESTILO.md` | módulo | existe; proveniência NOM-LEV-006 |
| `docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md` | módulo | existe; proveniência NOM-LEV-007, 008, 016, 021 |
| `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` | módulo | existe; proveniência NOM-LEV-012 |
| `docs/nomenclatura/30_CABECALHO.md` | módulo | existe; proveniência NOM-LEV-013 |
| `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` | módulo | existe; proveniência NOM-LEV-011 |
| `docs/nomenclatura/32_CONSOLE.md` | módulo | existe; proveniência NOM-LEV-009 e 010 |
| `docs/nomenclatura/33_LANCADOR.md` | módulo | existe; proveniência NOM-LEV-014, 020 e 012 parcial |
| `docs/nomenclatura/34_DASHBOARD.md` | módulo | existe; proveniência NOM-LEV-015 |
| `docs/nomenclatura/40_GRUPOS_E_DISTRIBUICAO_DE_AREA.md` | módulo | existe; proveniência NOM-LEV-022, 023 e 021 parcial |
| `docs/nomenclatura/41_DISTRIBUICAO_MATRICIAL.md` | módulo | existe; proveniência NOM-LEV-024 |
| `docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md` | módulo | existe; proveniência NOM-LEV-025 |
| `docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md` | módulo | existe; proveniência NOM-LEV-026 |
| `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` | módulo | existe; proveniência NOM-LEV-027 e 028 |
| `docs/nomenclatura/90_ALIASES_E_TERMOS_DESCONTINUADOS.md` | módulo | existe; aliases e termos descontinuados; proveniência ampla |
| `docs/relatorios/RELATORIO_HISTORICO_NOMENCLATURA_MONOLITICA.md` | relatório | existe; histórico e pendências preservados |
| `docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-1.md` | relatório | este arquivo; atualizado nesta complementação |

## 5. Arquivos alterados

### 5.1 Alterações da fase 1 original

| Arquivo | Alteração declarada na fase 1 |
|---|---|
| `docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md` | status e seção de aplicação atualizados; encerramento registra fase 1 aplicada |
| `docs/adr/INDICE_ADR.md` | linha ADR-0029 adicionada |

A ADR e o índice ADR não foram alterados no patch `PATCH_APLICACAO_ADR_FASE_1` nem no patch residual `PATCH_APLICACAO_ADR_FASE_1_RESIDUAL`.

### 5.2 Alterações do patch `PATCH_APLICACAO_ADR_FASE_1`

| Arquivo | Alteração |
|---|---|
| `docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` | fronteira `config/estilo.json` declarada explicitamente |
| `docs/nomenclatura/10_ESTILO.md` | fronteira vocabulário × artefato declarada |
| `docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md` | remoção de duplicatas `barra_de_menus` e `grupo` dos termos proprietários |
| `docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md` | seção 8A com termos concorrentes deferidos |
| `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` | seção 8A com termos concorrentes deferidos |
| `docs/nomenclatura/90_ALIASES_E_TERMOS_DESCONTINUADOS.md` | seção 4A com termos concorrentes localizáveis |
| `docs/relatorios/RELATORIO_HISTORICO_NOMENCLATURA_MONOLITICA.md` | seções 2.5, 2.6, 2.7, 2.8, 3 e 4 corrigidas |
| `docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-1.md` | este arquivo |

## 6. Arquivos preservados

| Arquivo ou grupo | Estado declarado | Evidência |
|---|---|---|
| `docs/NOMENCLATURA.md` | preservado integralmente | `git status --short` não mostra alteração rastreada no monólito; monólito permanece fonte vigente PRE_FACHADA |
| `docs/INDICE.md` | preservado | `git status --short` não mostra alteração |
| `docs/backlog.md` | preservado | `git status --short` não mostra alteração |
| `docs/issues.md` | preservado | `git status --short` não mostra alteração |
| `docs/contratos/*.md` | preservados | `git status --short` não mostra alteração nos nove contratos |
| `docs/handoff/` | preservado | `git status --short` não mostra alteração |
| `tela/` | preservado | `git status --short` não mostra alteração |
| `demo/` | preservado | `git status --short` não mostra alteração |
| `config/` | preservado | `git status --short` não mostra alteração |

## 7. Mapeamento NOM-LEV-001 a NOM-LEV-028

| ID | Conteúdo do levantamento | Destino autorizado | Destino materializado | Fragmentos | Módulo proprietário | Histórico ou pendência | Regra preservada em contrato | Resultado |
| -- | ------------------------ | ------------------ | --------------------- | ---------- | ------------------- | ---------------------- | ---------------------------- | --------- |
| NOM-LEV-001 | Frontmatter/metadados do monólito, linhas 1-11 | metadados preservados no relatório de aplicação; não todo módulo 02 | não aparece em proveniência de `02`; relatório histórico corrigido remove atribuição indevida de NOM-LEV-001 a caminhos históricos | sim | METADADO_DE_ORIGEM_PRESERVADO_NO_RELATORIO | nome, tipo, escopo, status, origem, data, condição parcial do monólito preservados factualmente neste relatório | não aplicável | CONFORME |
| NOM-LEV-002 | Regra de fonte única de nomes, linhas 15-25 | `01_NUCLEO_COMUM.md`; `00_INDICE.md` quando aplicável | `01` proveniência NOM-LEV-002; `00` explica leitura seletiva | sim | `01` | não | regra de consulta não é contrato específico | CONFORME |
| NOM-LEV-003 | Política schema × dados, linhas 27-56 | `01` e `02` | `01` e `02` declaram proveniência NOM-LEV-003 | sim | `02` para artefatos; `01` para conceitos transversais | não | `contrato_tela_json.md`, `contrato_estilo.md` | CONFORME |
| NOM-LEV-004 | Motor/demo/produto real, linhas 57-87 | `02`; histórico para futuro/transitório | `02` proveniência NOM-LEV-004 | sim | `02` | caminhos reservados preservados como reservados | `contrato_tela_json.md` | CONFORME |
| NOM-LEV-005 | Status transitório de artefatos JSON, linhas 89-105 | relatório histórico | relatório histórico seção 2.6 preserva NOM-LEV-005 nominalmente; módulo `02` declara não incluir status transitório e remete ao relatório histórico | sim | ESTADO_TRANSITORIO_HISTORICO — destino: RELATORIO_HISTORICO_NOMENCLATURA_MONOLITICA.md | sem definição terminológica ativa | não aplicável | CONFORME |
| NOM-LEV-006 | Estilo universal, linhas 109-233 | `10`, `20`, `90` quando alias | `10` proveniência NOM-LEV-006; `20` contém arranjo; `90` contém alias | sim | `10` para estilo | aliases em `90` | `contrato_estilo.md`, `contrato_chip.md`, `contrato_composicao_corpo.md` | CONFORME |
| NOM-LEV-007 | Estrutura base de tela e `tela.json`, linhas 234-327 | `20`; `02` para artefato | `20` declara NOM-LEV-007; `02` possui `tela.json` | sim | `20`/`02` por sentido | não | `contrato_tela_json.md` | CONFORME |
| NOM-LEV-008 | Eixos de composição por classe, linhas 328-358 | `20` | `20` declara NOM-LEV-008 | não | `20` | não | `contrato_composicao_corpo.md`, `contrato_tela_json.md` | CONFORME |
| NOM-LEV-009 | Console, cursor, seleção e lote, linhas 359-398 | `32` | `32` declara NOM-LEV-009 | não | `32` | relação filtro/seleção adiada | `contrato_console.md`, `contrato_barra_de_menus.md` | CONFORME |
| NOM-LEV-010 | Navegação/layout de console, linhas 399-531 | `32`; contrato para regra completa | `32` declara NOM-LEV-010 | não | `32` | pendência `tx` vinculada | `contrato_console.md` | CONFORME |
| NOM-LEV-011 | `barra_de_menus`, chips, distribuição, linhas 532-682 | `31`; `10` para forma visual; `44` para `[V]` | `31` declara NOM-LEV-011; `10` e `44` referenciam aspectos | sim | `31` | estrutura `aciona processo` pendente | `contrato_barra_de_menus.md`, `contrato_chip.md` | CONFORME |
| NOM-LEV-012 | Layout, largura, redimensionamento, lançador, linhas 683-825 | `21` e `33` | `21` declara NOM-LEV-012; `33` declara NOM-LEV-012 parcial | sim | `21` geral; `33` largura do lançador | não | `contrato_tela_json.md`, `contrato_lancador.md` | CONFORME |
| NOM-LEV-013 | Cabeçalho, linhas 826-892 | `30` | `30` declara NOM-LEV-013 | não | `30` | caminho de config é artefato em `02` | `contrato_cabecalho.md`, `contrato_tela_json.md` | CONFORME |
| NOM-LEV-014 | Corpo tipo `lancador`, linhas 893-986 | `33` | `33` declara NOM-LEV-014 | não | `33` | histórico `menu` separado | `contrato_lancador.md` | CONFORME |
| NOM-LEV-015 | `dashboard`, linhas 987-1045 | `34`; relatório histórico para instância | `34` declara NOM-LEV-015; relatório histórico preserva instância; alinhamento pendente classificado em NOM-LEV-017 (não NOM-LEV-019) | sim | `34` para tipo universal | instância raiz preservada; alinhamento pendente em NOM-LEV-017; contrato próprio (`contrato_json_dashboard.md`) existe no repositório, seção 9.5 classifica alinhamento como pendência futura | `contrato_composicao_corpo.md`; `contrato_json_dashboard.md` (fora dos nove, mas existente) | CONFORME |
| NOM-LEV-016 | Tiling, linhas 1049-1072 | `10`, `20`, `90` | `20` declara NOM-LEV-016; `10` define `tiling`; `90` aliases | sim | `10`/`20` por sentido | alias sem prioridade formal | `contrato_estilo.md`, `contrato_composicao_corpo.md` | CONFORME |
| NOM-LEV-017 | Pendências em aberto, linhas 1074-1101 | histórico/pendências; não módulo | relatório histórico 2.5 lista NOM-LEV-017; `32` registra pendência `tx` como NAO_CONFIRMADO | sim | NAO_CONFIRMADO | pendência `tx` | NAO_CONFIRMADO | CONFORME |
| NOM-LEV-018 | Levantamento Codex de legado, linhas 1103-1130 | histórico; não módulo | relatório histórico seção 2.5 (NOM-LEV-018) preserva nominalmente `teste_classe_c.py`, `teste_combo.py`, relação `[#]`×`[␣]` e demais itens do levantamento Codex | sim | LEVANTAMENTO_HISTORICO — destino: RELATORIO_HISTORICO_NOMENCLATURA_MONOLITICA.md | histórico sem decisão normativa | não aplicável | CONFORME |
| NOM-LEV-019 | Lista parcial de ADRs aceitas, linhas 1132-1142 | índice ADR; histórico preservado no relatório histórico | relatório histórico seção 2.5 (NOM-LEV-019) registra corretamente a lista parcial de ADRs; alinhamento dashboard corrigido para NOM-LEV-017 | sim | `docs/adr/INDICE_ADR.md` para lista atual; relatório histórico para registro histórico | lista parcial histórica; NOM-LEV-019 não representa dashboard | não aplicável | CONFORME |
| NOM-LEV-020 | Decisão `lancador` × `menu`, linhas 1146-1215 | `33` e `90`; relatório histórico | `33`, `90` e relatório histórico preservam | sim | `33` para termo atual; `90` para alias | histórico de substituição | `contrato_lancador.md` | CONFORME |
| NOM-LEV-021 | Composição hierárquica, linhas 1216-1287 | `20` e `40`; contrato para regra | `20` e `40` declaram NOM-LEV-021 | sim | `20` composição; `40` distribuição | não | `contrato_composicao_corpo.md`, `contrato_tela_json.md` | CONFORME |
| NOM-LEV-022 | Ausência de distribuição e espaço externo, linhas 1288-1370 | `40` | `40` declara NOM-LEV-022 | não | `40` | divergência ADR-0018 permanece externa | `contrato_composicao_corpo.md`, `contrato_tela_json.md` | CONFORME |
| NOM-LEV-023 | `grupo` livre/matriz, linhas 1371-1447 | `40` | `40` declara NOM-LEV-023 | não | `40` | termos inválidos remetidos a contrato | `contrato_composicao_corpo.md`, `contrato_tela_json.md` | CONFORME |
| NOM-LEV-024 | `distribuicao_matricial`, linhas 1448-1534 | `41` | `41` declara NOM-LEV-024 | não | `41` | fora de escopo permanece histórico | `contrato_tela_json.md`, `contrato_json_console.md` | CONFORME |
| NOM-LEV-025 | JSON externo de conteúdo, linhas 1535-1615 | `42` | `42` declara NOM-LEV-025 | não | `42` | decisões deferidas ADR-0026 | `contrato_console.md`, `contrato_json_console.md`, `contrato_tela_json.md` | CONFORME |
| NOM-LEV-026 | Carregamento conjunto, linhas 1618-1718 | `43` | `43` declara NOM-LEV-026 | não | `43` | decisões deferidas ADR-0027 | `contrato_console.md`, `contrato_json_console.md`, `contrato_tela_json.md` | CONFORME |
| NOM-LEV-027 | Apresentações e modos, linhas 1721-1804 | `44` | `44` declara NOM-LEV-027 | não | `44` | divergência modo normal × não verboso | `contrato_console.md`, `contrato_json_console.md`, `contrato_barra_de_menus.md` | CONFORME |
| NOM-LEV-028 | Política de modo D23, linhas 1806-1856 | `44` | `44` declara NOM-LEV-028; relatório histórico também cita divergência em NOM-LEV-028 | não | `44` | migração legada deferida | `contrato_console.md`, `contrato_json_console.md`, `contrato_barra_de_menus.md` | CONFORME |

## 8. Inventário de termos proprietários

| Termo | Definição preservada | Módulo proprietário | Outros módulos que mencionam | Contrato comportamental | ADR de origem | Alias relacionado | Duplicação indevida | Evidência |
| ----- | -------------------- | ------------------- | ---------------------------- | ----------------------- | ------------- | ----------------- | ------------------- | --------- |
| `docs/NOMENCLATURA.md` | schema e semântica; monólito vigente PRE_FACHADA | `02` | `01`, todos módulos frontmatter | vários | ADR-0008, ADR-0029 | não | não — LAC-0029-002 resolvida; duplicação indevida ativa: nenhuma | `02` seção 4.1 |
| `tela.json` | declaração concreta da tela | `02` | `20`, `30`, `31`, contratos JSON | `contrato_tela_json.md` | ADR-0008 | não | referência permitida em `20` se não redefinir | `02` seção 4.1; `20` seção 4.7 |
| `config/estilo.json` | biblioteca global de aparência — artefato e caminho | `02` (artefato/caminho); `10` (vocabulário de estilo) | `10` referencia como local de materialização | `contrato_estilo.md` | ADR-0008 | não | REFERENCIA_PERMITIDA_COM_FRONTEIRA_EXPLICITA: `02` é proprietário do artefato; `10` é proprietário do vocabulário; fronteira declarada em ambos os módulos | `02` seção 2 e 4.1; `10` seção 2 e 3 |
| `barra_de_menus` | região fixa inferior/instância declarada | `31` | `20` referencia como região concreta | `contrato_barra_de_menus.md`, `contrato_chip.md` | ADR-0012 | não | REFERENCIA_PERMITIDA: `31` proprietário exclusivo da definição específica; `20` cita como região concreta sem redefinir; fronteira declarada em `20` seção 2 e 3 | `31` seção 3; `20` seção 2 e 3 (termos referenciados) |
| `chip` — forma visual | campos visuais de estilo do chip | `10` | `31` | `contrato_estilo.md`, `contrato_chip.md` | ADR-0004 | não | SENTIDOS_DISTINTOS_COMPROVADOS | `10` seção 4.3; `31` seção 4.2 |
| `chip` — entidade de interface | tecla/símbolo acionável ou informativo | `31` | `10`, `32`, `44` | `contrato_chip.md`, `contrato_barra_de_menus.md` | ADR-0012, ADR-0014 | não | SENTIDOS_DISTINTOS_COMPROVADOS | `31` seção 4.2 |
| `lancador` | elemento do corpo para navegação por `tela_destino` | `33` | `20`, `31`, `90` | `contrato_lancador.md` | ADR-0001 a ADR-0006, ADR-0023 | `menu` | não | `33` seção 4.1 |
| `menu` | termo descontinuado para corpo tipo lançador | `90` | `33`, histórico | `contrato_lancador.md` para termo atual | ADR-0006/decisão 2026-07-06 | `lancador` | não; alias histórico | `90` seção 3.1 |
| `console` | container interativo e navegável genérico | `32` | `20`, `42`, `43`, `44` | `contrato_console.md` | ADR-0006, ADR-0026 a 0028 | `dado` | não | `32` seção 4.1 |
| `dado` | termo descontinuado para container navegável | `90` | `32` | `contrato_console.md` para termo atual | ADR-0006 | `console` | não | `90` seção 3.1 |
| `dashboard` | saída passiva formatada | `34` | `20`, histórico | `contrato_composicao_corpo.md`; contrato próprio fora dos nove | ADR-0006, ADR-0008 | `Info` | não | `34` seção 4 |
| `Info` | termo descontinuado para dashboard | `90` | `34`, histórico | NAO_CONFIRMADO nos nove | ADR-0006 | `dashboard` | não | `90` seção 3.1 |
| `tiling` | preferência global de arranjo | `10` | `20`, `90` | `contrato_estilo.md`, `contrato_composicao_corpo.md` | ADR-0011 | `sobreposto`, `lado_a_lado` | não | `10` seção 4.6 |
| `sobreposto` | alias transitório de arranjo | `90` | `10`, `20` | `contrato_composicao_corpo.md` | ADR-0011 | `vertical`/`lado_a_lado` | não; relação sem prioridade formal | `90` seção 3.2 |
| `lado_a_lado` | alias transitório de arranjo | `90` | `10`, `20` | `contrato_composicao_corpo.md` | ADR-0011 | `horizontal`/`sobreposto` | não; relação sem prioridade formal | `90` seção 3.2 |
| `corpo.arranjo` | ordem/composição dos filhos diretos | `20` | `10`, `40` | `contrato_composicao_corpo.md` | ADR-0011, ADR-0015 | `sobreposto`, `lado_a_lado` | não | `20` seção 4.4 |
| `ocupacao_vertical_terminal` | preenchimento da altura disponível | `21` | `10`, `20`, `40` | `contrato_composicao_corpo.md`, `contrato_tela_json.md` | ADR-0013 | não | referência permitida | `21` seção 4.3 |
| `cor_inativo` | cor aplicada a estado inativo | `10` | `31` | `contrato_estilo.md`, `contrato_chip.md` | ADR-0004 | não | não | `10` seção 4.5 |
| `cor_alerta` | cor aplicada a limite/alerta | `10` | NAO_CONFIRMADO | `contrato_estilo.md` | ADR-0004 | não | não | `10` seção 4.5 |
| `grupo` — origem/categoria do dado | categoria do dado no console | `32` | `40` distingue | `contrato_console.md` | NAO_CONFIRMADO | não | SENTIDOS_DISTINTOS_COMPROVADOS | `32` seção 4.2 |
| `grupo` — nó estrutural | container estrutural do corpo | `40` | `20` cita como espécie de container (sem redefinir) | `contrato_composicao_corpo.md` | ADR-0015, ADR-0020 | não | REFERENCIA_PERMITIDA: `40` proprietário exclusivo; `20` apenas cita como espécie; fronteira declarada em `20` seção 2 | `40` seção 4; `20` seção 2 e 3 (termos referenciados) |
| `cursor`/`selecionado` | item apontado por navegação | `32` | `10` como indicador visual | `contrato_console.md` | ADR-0005 | não | SENTIDOS_DISTINTOS_COMPROVADOS | `32` seção 4.2 |
| `seleção` | conjunto nomeado de elementos | `32` | `31` por chip `[␣]` | `contrato_console.md`, `contrato_barra_de_menus.md` | NAO_CONFIRMADO | não | não | `32` seção 4.2 |
| `lote` | unidade de execução derivada da seleção | `32` | `31` por `[⏎]` | `contrato_console.md` | NAO_CONFIRMADO | não | não | `32` seção 4.2 |
| `ec` | espaço do cursor no item do console | `32` | `31` por barra | `contrato_console.md` | NAO_CONFIRMADO | não | não | `32` seção 4.4 |
| `tg` | espaço de toggle no item do console | `32` | `31` por barra/chip | `contrato_console.md`, `contrato_chip.md` | NAO_CONFIRMADO | não | não | `32` seção 4.4 |
| `tx` | texto do item do console | `32` | histórico pendência | `contrato_console.md` | NAO_CONFIRMADO | não | regra de ajuste pendente | `32` seção 4.4; histórico 2.5 |
| `[✥]` | dica visual de navegação por setas | `31` para chip; `32` para navegação | `32` | `contrato_barra_de_menus.md`, `contrato_console.md` | ADR-0005 | não | referência permitida | `31` seção 4.3; `32` seção 4.3 |
| `[Esc]` | chip contextual Sair/Voltar/Limpar | `31` | `32` por seleção | `contrato_barra_de_menus.md` | ADR-0012 | não | não | `31` seção 4.5 |
| `[⏎]` | chip Todos/Executar/Visualizar | `31` | `32` por lote/ação | `contrato_barra_de_menus.md` | NAO_CONFIRMADO | não | não | `31` seção 4.5 |
| `[V]` | chip de modo verboso em tela alternável | `31` | `44` | `contrato_barra_de_menus.md`, `contrato_console.md` | ADR-0028 | não | referência permitida | `31` seção 4.3; `44` seção 4.5 |
| `SIGWINCH` | sinal POSIX de redimensionamento | `21` | código | `contrato_tela_json.md` | ADR-0017 | não | não | `21` seção 4.2 |
| `ioctl(TIOCGWINSZ)` | fonte primária de dimensões TTY | `21` | código | `contrato_tela_json.md` | ADR-0017 | não | não | `21` seção 4.2 |
| `quadro mínimo de terminal pequeno` | quadro substituto quando tela não cabe | `21` | `33`, `41` | `contrato_tela_json.md`, `contrato_lancador.md` | ADR-0017, ADR-0023 | não | referência permitida | `21` seção 4.2 |
| `area_lancador_w` | largura total alocada ao lançador | `33` | `21` distingue | `contrato_lancador.md` | ADR-0023 | não | não | `33` seção 4.4 |
| `lancador_caixa_min_w` | largura mínima total da caixa do lançador | `33` | `21` distingue | `contrato_lancador.md` | ADR-0023 | não | não | `33` seção 4.4 |
| `coluna_minima_content_w` | largura mínima de conteúdo de coluna válida | `33` | NAO_CONFIRMADO | `contrato_lancador.md` | ADR-0023 | não | não | `33` seção 4.4 |
| `popup_execucao` | janela temporária de saída de execução (item pendente) | NAO_APLICAVEL_ENQUANTO_PENDENTE | relatório histórico NOM-LEV-017 | NAO_CONFIRMADO | NAO_CONFIRMADO | não | PENDENTE_SEM_DEFINICAO_APROVADA — não é termo ativo; não requer proprietário nesta fase; contido em NOM-LEV-017 (bloco geral de pendências); não bloqueia QA da fase 1 | levantamento seção 6; relatório histórico seção 2.5 NOM-LEV-017 |
| `matriz de grupos` | grade bidimensional do nó `grupo` | `40` | `41` distingue | `contrato_composicao_corpo.md` | ADR-0020 | não | não | `40` seção 4.5 |
| `célula` — matriz de grupos | interseção linha/coluna em grupo matriz | `40` | `41` | `contrato_composicao_corpo.md` | ADR-0020 | não | SENTIDOS_DISTINTOS_COMPROVADOS | `40` seção 4.5 |
| `coluna` — lançador | coluna calculada do lançador | `33` | `41` | `contrato_lancador.md` | ADR-0001 | não | SENTIDOS_DISTINTOS_COMPROVADOS | `33` seção 4.3 |
| `coluna` — distribuição matricial | faixa vertical/célula da distribuição | `41` | `40` | `contrato_json_console.md`, `contrato_tela_json.md` | ADR-0025 | não | SENTIDOS_DISTINTOS_COMPROVADOS | `41` seção 3 |
| `vão` — lançador | espaço entre colunas do lançador | `33` | `41` | `contrato_lancador.md` | ADR-0003 | não | SENTIDOS_DISTINTOS_COMPROVADOS | `33` seção 2 |
| `vão` — distribuição matricial | espaçamento interno da grade ADR-0025 | `41` | `33` | `contrato_json_console.md`, `contrato_tela_json.md` | ADR-0025 | não | SENTIDOS_DISTINTOS_COMPROVADOS | `41` seção 3 |
| `distribuicao_matricial` | campo declarativo de elemento funcional | `41` | `40`, `33` distinguem | `contrato_tela_json.md`, `contrato_json_console.md` | ADR-0025 | não | não | `41` seção 4 |
| `dado externo` | dado fornecido ao console por envelope | `42` | `43`, `44` | `contrato_console.md`, `contrato_json_console.md` | ADR-0026 | não | não | `42` seção 3 |
| `JSON estrutural da tela` | documento de configuração da interface | `02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` | `42_DADOS_EXTERNOS_MULTINIVEL.md`, `43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md`, `44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` | `contrato_tela_json.md` | ADR-0026 | não | REFERENCIA_PERMITIDA_COM_FRONTEIRA_EXPLICITA | `02` seção 2 e 3; `42` seção 2 e 5 |
| `JSON externo de conteúdo` | documento externo de runtime do console | `42` | `43`, `44` | `contrato_json_console.md` | ADR-0026 | não | não | `42` seção 4 |
| `conteúdo multinível` | hierarquia declarada explicitamente | `42` | `44` | `contrato_json_console.md` | ADR-0026, ADR-0027 | não | não | `42` seção 4 |
| `loader` — conceito transversal | produtor/etapa geral | `01` | `43` | contratos variados | ADR-0026, ADR-0027 | não | SENTIDOS_DISTINTOS_COMPROVADOS se `43` for papel específico | `01` termos; `43` termos |
| `loader` — papel no carregamento externo | produtor de conteúdo para console | `43` | `01` | `contrato_console.md`, `contrato_json_console.md` | ADR-0027 | não | SENTIDOS_DISTINTOS_COMPROVADOS | `43` seção 2 |
| `folha` | correspondência histórica com `conteudo` (schema) | NAO_APLICAVEL — TERMO_CONCORRENTE_DEFERIDO | módulo `42` seção 8A; módulo `90` seção 4A | `contrato_json_console.md` | ADR-0028 | `conteudo` | TERMO_CONCORRENTE_DEFERIDO_LOCALIZAVEL — não é termo ativo; não bloqueia QA fase 1; reconciliação requer nova ADR | `42` seção 8A; `90` seção 4A |
| `campo` | correspondência histórica com `nome_valor` (schema) | NAO_APLICAVEL — TERMO_CONCORRENTE_DEFERIDO | módulo `42` seção 8A; módulo `90` seção 4A | `contrato_json_console.md` | ADR-0028 | `nome_valor` | TERMO_CONCORRENTE_DEFERIDO_LOCALIZAVEL — não é termo ativo; não bloqueia QA fase 1; reconciliação requer nova ADR | `42` seção 8A; `90` seção 4A |
| `hierarquia_indentada` | correspondência histórica com `hierarquia` (schema) | NAO_APLICAVEL — TERMO_CONCORRENTE_DEFERIDO | módulo `44` seção 8A; módulo `90` seção 4A | `contrato_json_console.md` | ADR-0028 | `hierarquia` | TERMO_CONCORRENTE_DEFERIDO_LOCALIZAVEL — não é termo ativo; não bloqueia QA fase 1; reconciliação requer nova ADR | `44` seção 8A; `90` seção 4A |
| `modo normal` | modo compacto anterior/equivalente conceitual | `44` como divergência preservada | `32`, `90` | `contrato_console.md` | ADR-0028 preserva divergência | `modo não verboso` | DIVERGENCIA_TERMINOLOGICA_DEFERIDA_PRESERVADA — dois termos coexistentes; reconciliação não tomada; não bloqueia QA fase 1; bloqueia renomeação ou eliminação unilateral | `44` seção 4.4; `90` seção 4 |
| `modo não verboso` | modo compacto da apresentação multinível | `44` | `32`, `90` | `contrato_console.md`, `contrato_json_console.md` | ADR-0028 | `modo normal` | divergência deferida | `44` seção 4.3 |
| `politica_modo` | política por tela no JSON estrutural | `44` | código/config | `contrato_json_console.md`, `contrato_tela_json.md` | ADR-0028 D23 | não | não | `44` seção 4.5 |
| `somente_nao_verboso` | valor da política de modo | `44` | código/config | `contrato_json_console.md` | ADR-0028 D23 | não | não | levantamento seção 6; `44` seção 4.5 |
| `alternavel` | valor da política de modo que habilita alternância | `44` | `31` por `[V]` | `contrato_barra_de_menus.md`, `contrato_json_console.md` | ADR-0028 D23 | não | não | `44` seção 4.5 |

## 9. Definições separadas de regras comportamentais

| Módulo | Definições preservadas | Regras completas omitidas do módulo | Contrato que preserva as regras | Regra sem contrato comprovado | Resultado |
| ------ | ---------------------- | ----------------------------------- | ------------------------------- | ----------------------------- | --------- |
| `00_INDICE.md` | navegação e leitura seletiva | dependências normativas por contrato | contratos individuais futuramente, D-NOM-10 | nenhuma | CONFORME |
| `01_NUCLEO_COMUM.md` | autoridade terminológica, termo canônico, alias, schema, runtime, loader/modelo/renderizador | comportamento completo de qualquer componente | todos os contratos ativos | nenhuma | CONFORME |
| `02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` | artefatos, caminhos, separação motor/demo/produto; fronteira com `10` declarada explicitamente | comportamento de loader/renderizador e validação de `tela.json` | `contrato_tela_json.md`, `contrato_estilo.md` | nenhuma — NOM-LEV-005 preservado nominalmente no relatório histórico (seção 2.6) | CONFORME |
| `10_ESTILO.md` | vocabulário de estilo, borda, chip visual, indicadores, cores, `tiling`; fronteira com `02` declarada: `config/estilo.json` como artefato pertence a `02` | regras de aplicação visual e comportamento dos chips | `contrato_estilo.md`, `contrato_chip.md`, `contrato_barra_de_menus.md` | nenhuma | CONFORME |
| `20_TELA_CORPO_E_COMPOSICAO.md` | tela, regiões, tipos, arranjo, composição hierárquica; `barra_de_menus` e `grupo` removidos dos termos proprietários; fronteiras com `31` e `40` declaradas explicitamente | composição normativa completa, validação, arredondamento | `contrato_composicao_corpo.md`, `contrato_tela_json.md` | nenhuma | CONFORME |
| `21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` | SIGWINCH, dimensões válidas, quadro mínimo, paginação | cadeia completa de redimensionamento, fallback, redesenho | `contrato_tela_json.md` seção 24 | nenhuma | CONFORME |
| `30_CABECALHO.md` | cabeçalho, título, descrição, schema de apresentação | renderização e validação completa do cabeçalho | `contrato_cabecalho.md` | nenhuma | CONFORME |
| `31_BARRA_DE_MENUS_E_CHIPS.md` | barra, chips, ordem, estado, distribuição | ações, existência/ativo, rótulos, validação | `contrato_barra_de_menus.md`, `contrato_chip.md` | nenhuma | CONFORME |
| `32_CONSOLE.md` | console, cursor, seleção, lote, grupo-dado, ec/tg/tx | navegação, seleção, ação, filtros, paginação | `contrato_console.md`, `contrato_barra_de_menus.md` | pendência `tx` sem decisão vigente | CONFORME_COM_PENDENCIA_NAO_BLOQUEANTE |
| `33_LANCADOR.md` | lançador, item, fila/matriz, largura mínima | cálculo de colunas, rejeição de texto, fallback | `contrato_lancador.md`, `contrato_composicao_corpo.md` | nenhuma | CONFORME |
| `34_DASHBOARD.md` | dashboard, saída passiva, marcadores e campos; define termo ativo; aponta para contrato existente; alinhamento pendente registrado como PENDENCIA_PRESERVADA_NAO_BLOQUEANTE_DA_FASE_1 (origem NOM-LEV-017, não NOM-LEV-019) | comportamento de instância | `contrato_composicao_corpo.md`; `contrato_json_dashboard.md` (existe no repositório; seção 9.5 classifica alinhamento como pendência futura não bloqueante) | nenhuma regra ativa sem contrato | CONFORME |
| `40_GRUPOS_E_DISTRIBUICAO_DE_AREA.md` | grupo estrutural, distribuição, matriz de grupos, DA-01 a DA-04 | validação completa, arredondamento, rejeição | `contrato_composicao_corpo.md`, `contrato_tela_json.md` | nenhuma | CONFORME |
| `41_DISTRIBUICAO_MATRICIAL.md` | distribuição matricial, formação, margem, vão, fallback | precedência, geometria, validação | `contrato_tela_json.md`, `contrato_json_console.md` | contratos JSON de dashboard/lancador existem mas não integram os nove exigidos | CONFORME_COM_DEFERIMENTO_PRESERVADO |
| `42_DADOS_EXTERNOS_MULTINIVEL.md` | dado externo, envelope, níveis, schema semântico; `folha` e `campo` registrados na seção 8A como TERMO_CONCORRENTE_DEFERIDO (não são termos ativos) | validação do documento externo | `contrato_console.md`, `contrato_json_console.md`, `contrato_tela_json.md` | nenhuma regra ativa sem contrato | CONFORME |
| `43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md` | carregamento, vínculo, momento, origem declarada | fluxo completo de carregamento/associação | `contrato_console.md`, `contrato_json_console.md`, `contrato_tela_json.md` | protocolo produtor/Pipeline deferido | CONFORME_COM_DEFERIMENTO_PRESERVADO |
| `44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` | apresentações, modos, D23, política; `hierarquia_indentada` registrada na seção 8A como TERMO_CONCORRENTE_DEFERIDO; divergência `modo normal`×`modo não verboso` preservada como DIVERGENCIA_TERMINOLOGICA_DEFERIDA_PRESERVADA | regra completa de modo, validações D23 | `contrato_console.md`, `contrato_json_console.md`, `contrato_barra_de_menus.md` | nenhuma regra ativa sem contrato; divergência corretamente preservada como deferida | CONFORME |
| `90_ALIASES_E_TERMOS_DESCONTINUADOS.md` | alias, descontinuado, rastreabilidade | comportamento nenhum | não aplicável | relação `lado_a_lado` × `sobreposto` sem prioridade formal | CONFORME_COM_PENDENCIA_NAO_BLOQUEANTE |

Regras completas retiradas ou não assumidas pelos módulos:

```yaml
- regra: redimensionamento reativo completo
  origem_no_monolito: docs/NOMENCLATURA.md §6.2, NOM-LEV-012
  modulo_terminologico: docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md
  contrato_que_a_preserva: docs/contratos/contrato_tela_json.md
  secao_do_contrato: "24"
  obrigacao_preservada: SIGWINCH, dimensões válidas, últimas dimensões, redesenho e quadro mínimo
  resultado: CONFORME
- regra: cálculo de colunas do lançador
  origem_no_monolito: docs/NOMENCLATURA.md §8.3, NOM-LEV-014
  modulo_terminologico: docs/nomenclatura/33_LANCADOR.md
  contrato_que_a_preserva: docs/contratos/contrato_lancador.md
  secao_do_contrato: "seções 6.1 a 6.7 (disposição, largura de coluna, organização interna, alinhamento horizontal, distribuição de espaço, espaçamento vertical, largura mínima e fallback ADR-0023)"
  obrigacao_preservada: disposição fila/matriz, largura de coluna, sub-colunas chip/texto, alinhamento, distribuição de espaço, largura mínima funcional, fallback global
  resultado: CONFORME
- regra: distribuição hierárquica, arredondamento e rejeição de composição inválida
  origem_no_monolito: docs/NOMENCLATURA.md §14-15, NOM-LEV-021 a 023
  modulo_terminologico: docs/nomenclatura/40_GRUPOS_E_DISTRIBUICAO_DE_AREA.md
  contrato_que_a_preserva: docs/contratos/contrato_composicao_corpo.md
  secao_do_contrato: "5.7 a 5.24"
  obrigacao_preservada: modos de distribuição, matriz, validações e exemplos
  resultado: CONFORME
- regra: navegação, seleção e cursor do console
  origem_no_monolito: docs/NOMENCLATURA.md §4, NOM-LEV-009 e 010
  modulo_terminologico: docs/nomenclatura/32_CONSOLE.md
  contrato_que_a_preserva: docs/contratos/contrato_console.md
  secao_do_contrato: "7 a 13"
  obrigacao_preservada: navegação, seleção, Enter, filtros, paginação e colunas
  resultado: CONFORME_COM_PENDENCIA_TX
- regra: chips e barra
  origem_no_monolito: docs/NOMENCLATURA.md §5, NOM-LEV-011
  modulo_terminologico: docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
  contrato_que_a_preserva: docs/contratos/contrato_barra_de_menus.md e docs/contratos/contrato_chip.md
  secao_do_contrato: "barra seções 8 a 22; chip seções 8 a 17"
  obrigacao_preservada: existência, ativo/inativo, ordem, ações, relação com console e modo verboso
  resultado: CONFORME
- regra: distribuição matricial
  origem_no_monolito: docs/NOMENCLATURA.md §16, NOM-LEV-024
  modulo_terminologico: docs/nomenclatura/41_DISTRIBUICAO_MATRICIAL.md
  contrato_que_a_preserva: docs/contratos/contrato_tela_json.md e docs/contratos/contrato_json_console.md
  secao_do_contrato: "tela_json 30; json_console 10"
  obrigacao_preservada: campo, formação, compatibilidade e fallback
  resultado: CONFORME
- regra: dados externos, carregamento e apresentações
  origem_no_monolito: docs/NOMENCLATURA.md §17-19, NOM-LEV-025 a 028
  modulo_terminologico: docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md, 43, 44
  contrato_que_a_preserva: contrato_console.md, contrato_json_console.md, contrato_tela_json.md, contrato_barra_de_menus.md
  secao_do_contrato: "console 19-21; json_console 11-13; tela_json 31-33; barra 22"
  obrigacao_preservada: fronteira JSON, carregamento, modos, D23 e chip V
  resultado: CONFORME — termos concorrentes (folha/campo/hierarquia_indentada) reclassificados como TERMO_CONCORRENTE_DEFERIDO; não são termos ativos sem proprietário
- regra: dashboard ativo
  origem_no_monolito: docs/NOMENCLATURA.md §9, NOM-LEV-015
  modulo_terminologico: docs/nomenclatura/34_DASHBOARD.md
  contrato_que_a_preserva: docs/contratos/contrato_json_dashboard.md
  secao_do_contrato: "seções 1-9 (objetivo, natureza, escopo, JSON mínimo, campos obrigatórios, validação, fora de escopo, critérios de aceite, distribuição matricial); alinhamento horizontal em seção 9.5 classificado como pendência futura não bloqueante"
  obrigacao_preservada: dashboard como tipo passivo, campos obrigatórios, validação, composição com contrato_composicao_corpo.md; alinhamento explicitamente preservado como pendência
  resultado: CONFORME
```

## 10. Histórico classificado

| Item | Origem no monólito | Destino histórico | Norma ativa preservada em outro local | Resultado |
| ---- | ------------------ | ----------------- | ------------------------------------- | --------- |
| Instância da tela raiz do Orquestrador | §9, NOM-LEV-015 | `RELATORIO_HISTORICO_NOMENCLATURA_MONOLITICA.md` seção 2.1 | tipo `dashboard` em `34`; composição em contrato | CONFORME |
| `menu` → `lancador` | §13, NOM-LEV-020 | relatório histórico 2.2; módulo `90` | `lancador` em `33`; contrato_lancador | CONFORME |
| `Info` → `dashboard` | ADR-0006; §9 | relatório histórico 2.3; módulo `90` | `dashboard` em `34` | CONFORME |
| `dado` → `console` | ADR-0006; §4 | relatório histórico 2.3; módulo `90` | `console` em `32` | CONFORME |
| Caminhos `config/lancador.json`, `config/cabecalho.json` | ADR-0021; §2 | relatório histórico 2.4 | caminhos canônicos em `02`, `30`, `33` | CONFORME |
| Levantamento Codex legado `teste_classe_c.py`/`teste_combo.py` | §11, NOM-LEV-018 | relatório histórico seção 2.5 (NOM-LEV-018) preserva nominalmente `teste_classe_c.py`, `teste_combo.py` e relação `[#]`×`[␣]` | não aplicável | CONFORME |
| Lista parcial ADR-0001 a ADR-0004 | §12, NOM-LEV-019 | relatório histórico seção 2.5 (NOM-LEV-019) preserva lista parcial histórica; autoridade atual é `docs/adr/INDICE_ADR.md`; contradição com dashboard corrigida | índice ADR | CONFORME |
| Divergência `modo normal` × `modo não verboso` | §19, NOM-LEV-028 | relatório histórico 2.7; módulo `44` | contratos console/json_console | CONFORME |

## 11. Pendências classificadas

| Item | Origem | Classificação | Autoridade | Documento futuro | Resultado |
| ---- | ------ | ------------- | ---------- | ---------------- | --------- |
| Pendência `tx` | NOM-LEV-017; §4/§11 | PENDENCIA_PRESERVADA_NAO_BLOQUEANTE_DA_FASE_1 | relatório histórico seção 2.5 NOM-LEV-017 | `docs/issues.md` se impedimento; `docs/backlog.md` se trabalho planejado | CONFORME |
| `popup_execucao` | NOM-LEV-017; §11 | PENDENTE_SEM_DEFINICAO_APROVADA — PENDENCIA_PRESERVADA_NAO_BLOQUEANTE_DA_FASE_1 | relatório histórico seção 2.5 NOM-LEV-017 | decisão futura | CONFORME |
| Alinhamento horizontal do dashboard | §9, §11; NOM-LEV-017 (não NOM-LEV-019) | PENDENCIA_PRESERVADA_NAO_BLOQUEANTE_DA_FASE_1; `contrato_json_dashboard.md` seção 9.5 classifica como FUTURA_NAO_BLOQUEANTE | relatório histórico seção 2.5 NOM-LEV-017; `contrato_json_dashboard.md` § 9.5 | decisão futura | CONFORME |
| Segunda pauta de estilos de exibição | NOM-LEV-017; §11 | PENDENCIA_PRESERVADA_NAO_BLOQUEANTE_DA_FASE_1 | relatório histórico seção 2.5 NOM-LEV-017 | decisão futura | CONFORME |
| Campos de navegação do lançador | NOM-LEV-017; §11 | PENDENCIA_PRESERVADA_NAO_BLOQUEANTE_DA_FASE_1 | relatório histórico seção 2.5 NOM-LEV-017 | decisão futura | CONFORME |
| Reorganização corpo × dashboard | NOM-LEV-017; §11 | PENDENCIA_PRESERVADA_NAO_BLOQUEANTE_DA_FASE_1 | relatório histórico seção 2.5 NOM-LEV-017 | decisão futura | CONFORME |
| Relação `[#]` × `[␣]` | NOM-LEV-018; §11 | HISTORICO_LEVANTAMENTO_CODEX — PENDENCIA_PRESERVADA_NAO_BLOQUEANTE_DA_FASE_1 | relatório histórico seção 2.5 NOM-LEV-018 | decisão futura | CONFORME |
| Decisões deferidas ADR-0026 | §17.5 | DEFERIMENTO_DA_ADR_DE_ORIGEM — PENDENCIA_PRESERVADA_NAO_BLOQUEANTE_DA_FASE_1 | relatório histórico seção 2.7 (antiga 2.6) | ADR futura | CONFORME |
| Decisões deferidas ADR-0027 | §18.6 | DEFERIMENTO_DA_ADR_DE_ORIGEM — PENDENCIA_PRESERVADA_NAO_BLOQUEANTE_DA_FASE_1 | levantamento NOM-LEV-026; contratos | ADR futura | CONFORME |
| Migração legada D23 | §19.7.5, NOM-LEV-028 | DEFERIMENTO_DA_ADR_DE_ORIGEM — PENDENCIA_PRESERVADA_NAO_BLOQUEANTE_DA_FASE_1 | ADR-0028/D23; contratos | ADR ou handoff futuro | CONFORME |

## 12. Dependências propostas por contrato

```yaml
- contrato: docs/contratos/contrato_estilo.md
  dependencias_obrigatorias: [01_NUCLEO_COMUM.md, 10_ESTILO.md]
  dependencias_condicionais: [20_TELA_CORPO_E_COMPOSICAO.md, 31_BARRA_DE_MENUS_E_CHIPS.md, 90_ALIASES_E_TERMOS_DESCONTINUADOS.md]
  gatilho_de_cada_dependencia_condicional:
    20: tiling ou arranjo de corpo
    31: chip como entidade de interface
    90: alias sobreposto/lado_a_lado
  evidencia_de_cada_dependencia: contrato_estilo.md linhas 10, 26, 48, 245; modulo 10 seção 6
  modulos_expressamente_desnecessarios: [32_CONSOLE.md, 33_LANCADOR.md, 34_DASHBOARD.md, 42_DADOS_EXTERNOS_MULTINIVEL.md, 43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md, 44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md]
  referencias_antigas_a_migrar: docs/NOMENCLATURA.md#1-estilo-universal; seção 1
- contrato: docs/contratos/contrato_composicao_corpo.md
  dependencias_obrigatorias: [01_NUCLEO_COMUM.md, 20_TELA_CORPO_E_COMPOSICAO.md, 40_GRUPOS_E_DISTRIBUICAO_DE_AREA.md]
  dependencias_condicionais: [10_ESTILO.md, 21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md, 33_LANCADOR.md, 34_DASHBOARD.md, 41_DISTRIBUICAO_MATRICIAL.md, 44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md, 90_ALIASES_E_TERMOS_DESCONTINUADOS.md]
  gatilho_de_cada_dependencia_condicional:
    10: tiling ou estilo
    21: redimensionamento/paginação/ocupacao_vertical_terminal
    33: regra ou área de lancador
    34: dashboard
    41: distribuição interna de participantes
    44: área física do console multinível
    90: alias transicional
  evidencia_de_cada_dependencia: origem_especificacao com #3, #6, #8, #9, #10; seções 5.7-5.24, 11, 12
  modulos_expressamente_desnecessarios: [30_CABECALHO.md, 42_DADOS_EXTERNOS_MULTINIVEL.md, 43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md]
  referencias_antigas_a_migrar: docs/NOMENCLATURA.md#3, #6, #8, #9, #10; seção 4; seção 19
- contrato: docs/contratos/contrato_barra_de_menus.md
  dependencias_obrigatorias: [01_NUCLEO_COMUM.md, 31_BARRA_DE_MENUS_E_CHIPS.md]
  dependencias_condicionais: [10_ESTILO.md, 32_CONSOLE.md, 44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md, 90_ALIASES_E_TERMOS_DESCONTINUADOS.md]
  gatilho_de_cada_dependencia_condicional:
    10: estados visuais e cor_inativo
    32: chips [✥], [␣], [#], [⏎] ligados a console
    44: chip [V]
    90: distribuição horizontal transitória
  evidencia_de_cada_dependencia: contrato_barra_de_menus.md linhas 10, 39, 109, 222, 808; módulo 31 seção 6
  modulos_expressamente_desnecessarios: [30_CABECALHO.md, 34_DASHBOARD.md, 42_DADOS_EXTERNOS_MULTINIVEL.md, 43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md]
  referencias_antigas_a_migrar: docs/NOMENCLATURA.md#5-barra_de_menus; seções 0, 1.5, 19
- contrato: docs/contratos/contrato_cabecalho.md
  dependencias_obrigatorias: [01_NUCLEO_COMUM.md, 30_CABECALHO.md]
  dependencias_condicionais: [02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md, 10_ESTILO.md]
  gatilho_de_cada_dependencia_condicional:
    02: caminho config/elementos/cabecalho.json
    10: apresentação visual/estilo
  evidencia_de_cada_dependencia: contrato_cabecalho.md linhas 10, 25, 93; módulo 30 seção 6
  modulos_expressamente_desnecessarios: [32_CONSOLE.md, 33_LANCADOR.md, 34_DASHBOARD.md, 40_GRUPOS_E_DISTRIBUICAO_DE_AREA.md, 41_DISTRIBUICAO_MATRICIAL.md, 42_DADOS_EXTERNOS_MULTINIVEL.md, 43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md, 44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md]
  referencias_antigas_a_migrar: docs/NOMENCLATURA.md#7-cabecalho; seção 7
- contrato: docs/contratos/contrato_lancador.md
  dependencias_obrigatorias: [01_NUCLEO_COMUM.md, 33_LANCADOR.md]
  dependencias_condicionais: [20_TELA_CORPO_E_COMPOSICAO.md, 21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md, 90_ALIASES_E_TERMOS_DESCONTINUADOS.md]
  gatilho_de_cada_dependencia_condicional:
    20: composição do corpo que contém lançador
    21: largura/terminal/quadro mínimo geral
    90: histórico menu -> lancador
  evidencia_de_cada_dependencia: contrato_lancador.md linhas 10, 36; módulo 33 seção 6
  modulos_expressamente_desnecessarios: [30_CABECALHO.md, 32_CONSOLE.md, 34_DASHBOARD.md, 42_DADOS_EXTERNOS_MULTINIVEL.md, 43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md, 44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md]
  referencias_antigas_a_migrar: docs/NOMENCLATURA.md#13-decisao-terminologica-lancador; seções 6 e 8
- contrato: docs/contratos/contrato_console.md
  dependencias_obrigatorias: [01_NUCLEO_COMUM.md, 32_CONSOLE.md]
  dependencias_condicionais: [31_BARRA_DE_MENUS_E_CHIPS.md, 42_DADOS_EXTERNOS_MULTINIVEL.md, 43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md, 44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md, 90_ALIASES_E_TERMOS_DESCONTINUADOS.md]
  gatilho_de_cada_dependencia_condicional:
    31: chips de navegação/seleção/filtro
    42: conteúdo externo
    43: carregamento externo
    44: apresentações e modos
    90: dado -> console ou modo normal
  evidencia_de_cada_dependencia: contrato_console.md linhas 11, 594, 674, 706, 796; módulo 32 seção 6
  modulos_expressamente_desnecessarios: [30_CABECALHO.md, 34_DASHBOARD.md]
  referencias_antigas_a_migrar: docs/NOMENCLATURA.md#4-corpo-tipo-console; seções 17, 18, 19
- contrato: docs/contratos/contrato_chip.md
  dependencias_obrigatorias: [01_NUCLEO_COMUM.md, 31_BARRA_DE_MENUS_E_CHIPS.md]
  dependencias_condicionais: [10_ESTILO.md, 32_CONSOLE.md, 33_LANCADOR.md, 34_DASHBOARD.md, 90_ALIASES_E_TERMOS_DESCONTINUADOS.md]
  gatilho_de_cada_dependencia_condicional:
    10: forma visual do chip
    32: chip de console
    33: distinção com lancador
    34: distinção com dashboard
    90: termo descontinuado ou alias
  evidencia_de_cada_dependencia: contrato_chip.md linhas 11, 59, 307; módulo 31 seção 6
  modulos_expressamente_desnecessarios: [42_DADOS_EXTERNOS_MULTINIVEL.md, 43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md]
  referencias_antigas_a_migrar: docs/NOMENCLATURA.md#5-barra_de_menus; seção 1.5; seção 5.1.2
- contrato: docs/contratos/contrato_tela_json.md
  dependencias_obrigatorias: [01_NUCLEO_COMUM.md, 02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md, 20_TELA_CORPO_E_COMPOSICAO.md]
  dependencias_condicionais: [30_CABECALHO.md, 31_BARRA_DE_MENUS_E_CHIPS.md, 32_CONSOLE.md, 33_LANCADOR.md, 34_DASHBOARD.md, 40_GRUPOS_E_DISTRIBUICAO_DE_AREA.md, 41_DISTRIBUICAO_MATRICIAL.md, 42_DADOS_EXTERNOS_MULTINIVEL.md, 43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md, 44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md, 90_ALIASES_E_TERMOS_DESCONTINUADOS.md]
  gatilho_de_cada_dependencia_condicional: seção/elemento configurado no JSON da tela
  evidencia_de_cada_dependencia: contrato_tela_json.md seções 7-33; linhas 1248, 1313, 1371, 1420
  modulos_expressamente_desnecessarios: []
  referencias_antigas_a_migrar: seções 16, 17, 18, 19 de docs/NOMENCLATURA.md
- contrato: docs/contratos/contrato_json_console.md
  dependencias_obrigatorias: [01_NUCLEO_COMUM.md, 32_CONSOLE.md, 42_DADOS_EXTERNOS_MULTINIVEL.md]
  dependencias_condicionais: [41_DISTRIBUICAO_MATRICIAL.md, 43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md, 44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md, 90_ALIASES_E_TERMOS_DESCONTINUADOS.md]
  gatilho_de_cada_dependencia_condicional:
    41: campo distribuicao_matricial
    43: origem_dados/carregamento
    44: apresentação, modo, D23
    90: modo normal/excesso.modo legado
  evidencia_de_cada_dependencia: contrato_json_console.md linhas 485, 870, 1044, 1208; seções 10-13
  modulos_expressamente_desnecessarios: [30_CABECALHO.md, 33_LANCADOR.md, 34_DASHBOARD.md, 40_GRUPOS_E_DISTRIBUICAO_DE_AREA.md]
  referencias_antigas_a_migrar: seções 17, 18, 19 de docs/NOMENCLATURA.md
```

## 13. Referências antigas inventariadas

Busca nominal executada para `docs/NOMENCLATURA.md`, `NOMENCLATURA.md`, `§1` a `§19` e `#1-` a `#19-`.

Resumo material da busca no repositório:

| Classificação | Arquivos | Ocorrências | Evidência |
|---|---:|---:|---|
| ATIVA_NORMATIVA | 17 | 67 | contratos, ADR-0029, índice ADR e configs ainda citam monólito/seções |
| ATIVA_EXPLICATIVA | 21 | 91 | `docs/INDICE.md`, `docs/build_docs/*` e módulos PRE_FACHADA |
| CODIGO_COMENTARIO | 2 | 19 | comentários em `tela/loader.py` e `tela/renderizador.py` |
| TESTE | 3 | 5 | comentários/docstrings em testes |
| HISTORICA_FECHADA | 64 | 363 | ADRs e handoffs anteriores |
| RELATORIO_HISTORICO | 242 | 2167 | relatórios fechados |
| NAO_CONFIRMADO | 1 | 8 | o próprio monólito |

Inventário nominal das ocorrências ativas e diretamente migráveis:

| Arquivo | Tipo | Referência atual | Classificação | Novo módulo candidato | Ação da fase 2 | Alterar documento histórico |
| ------- | ---- | ---------------- | ------------- | --------------------- | -------------- | --------------------------- |
| `docs/INDICE.md` | índice | linhas 32, 68, 115, 122 citam `docs/NOMENCLATURA.md` e seção 0 | ATIVA_EXPLICATIVA | `00`, `01`, `02` | migrar ordem de leitura para índice modular | NAO |
| `docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md` | ADR | linhas 15, 65, 69, 81, 300, 415, 486, 503, 504, 540 | ATIVA_NORMATIVA | não migrar como referência histórica da própria ADR; manter rastreável | avaliar se a ADR deve apontar para relatório atualizado | NAO |
| `docs/adr/INDICE_ADR.md` | índice ADR | linha 59 | ATIVA_NORMATIVA | `00`/ADR-0029 | manter ou ajustar após fase 2 | NAO |
| `docs/contratos/contrato_estilo.md` | contrato | linhas 10, 26, 48, 245; `#1-estilo-universal`, seção 1 | ATIVA_NORMATIVA | `10_ESTILO.md`; condicional `20`, `31`, `90` | migrar origem e remissões | NAO |
| `docs/contratos/contrato_composicao_corpo.md` | contrato | linhas 10, 47, 75, 607, 609, 1740, 1926; `#3`, `#6`, `#8`, `#9`, `#10`, seções 4 e 19 | ATIVA_NORMATIVA | `20`, `21`, `33`, `34`, `40`, `44` | migrar origem múltipla | NAO |
| `docs/contratos/contrato_barra_de_menus.md` | contrato | linhas 10, 39, 95, 109, 222, 808; `#5` e seções 0, 1.5, 19 | ATIVA_NORMATIVA | `31`, `10`, `32`, `44`, `90` | migrar origem e remissões | NAO |
| `docs/contratos/contrato_cabecalho.md` | contrato | linhas 10, 25, 93; `#7-cabecalho` | ATIVA_NORMATIVA | `30`, condicional `02` | migrar origem | NAO |
| `docs/contratos/contrato_lancador.md` | contrato | linhas 10, 36; `#13-decisao-terminologica-lancador` | ATIVA_NORMATIVA | `33`, `90` | migrar origem; preservar histórico `menu` | NAO |
| `docs/contratos/contrato_console.md` | contrato | linhas 11, 594, 674, 706, 776, 796, 839; `#4`, seções 17-19 e `§6` | ATIVA_NORMATIVA | `32`, `42`, `43`, `44`, `90` | migrar origem e remissões | NAO |
| `docs/contratos/contrato_chip.md` | contrato | linhas 11, 59, 307; `#5`, seções 1.5 e 5.1.2 | ATIVA_NORMATIVA | `31`, `10` | migrar origem e remissões | NAO |
| `docs/contratos/contrato_tela_json.md` | contrato | linhas 1112, 1248, 1313, 1371, 1420; seções 16-19 | ATIVA_NORMATIVA | `02`, `20`, `41`, `42`, `43`, `44` | migrar remissões | NAO |
| `docs/contratos/contrato_json_console.md` | contrato | linhas 485, 870, 1019, 1044, 1208; seções 17-19 e `§12.7` | ATIVA_NORMATIVA | `32`, `41`, `42`, `43`, `44`, `90` | migrar remissões | NAO |
| `config/estilo.json` | config | linhas 4-5 citam seção 1 | ATIVA_NORMATIVA | `10_ESTILO.md` | migrar metadado de origem | NAO |
| `config/elementos/barra_de_menus.json` | config | linhas 5, 99, 130 citam seções 4, 5, 5.2 | ATIVA_NORMATIVA | `31`, `32` | migrar origem/comentários declarativos | NAO |
| `config/layouts/layout_console.json` | config | linha 5 cita seção 4 | ATIVA_NORMATIVA | `32_CONSOLE.md` | migrar origem | NAO |
| `config/layouts/layout_dado.json` | config | linha 5 cita seção 4 | ATIVA_NORMATIVA | `32` e `90` | migrar e decidir nome legado | NAO |
| `config/layouts/layout_menu.json` | config | linha 5 cita seção 8 | ATIVA_NORMATIVA | `33` e `90` | migrar e decidir nome legado | NAO |
| `tela/teste_renderizador.py` | teste/código | linha 7252 cita `NOMENCLATURA.md 6.3/8.1-8.3` | TESTE | `21`, `33` | atualizar comentário em fase 2 ou etapa própria | NAO |
| `tela/loader.py` | código | linhas 1236, 1351, 1388, 1405, 1515, 1518, 1527, 1546, 1599, 1605, 1618, 1686 e outras citam parágrafos de ADR/contrato | CODIGO_COMENTARIO | `44`, contratos | revisar apenas se referência antiga apontar ao monólito; maioria é contrato/ADR | NAO |
| `tela/renderizador.py` | código | linhas 1473, 1513, 1547, 1690 citam contratos/handoff | CODIGO_COMENTARIO | contratos, `31` | não é migração direta do monólito salvo vínculo de contexto | NAO |
| `docs/nomenclatura/*.md` | módulos PRE_FACHADA | todos têm `fonte_normativa_ainda_vigente: docs/NOMENCLATURA.md`; proveniência por § | ATIVA_EXPLICATIVA | próprios módulos | substituir somente após fachada/QA | NAO |

Ocorrências históricas fechadas não devem ser reescritas sem autoridade: 64 arquivos ADR/handoff e 242 relatórios contêm 2530 ocorrências combinadas. Ação candidata: manter como histórico ou migrar apenas quando o documento ainda for normativo ativo.

## 14. Duplicações temporárias entre monólito e módulos

| Termo ou bloco | Monólito | Módulo | Tipo | Permitida nesta fase | Condição para remoção |
| -------------- | -------- | ------ | ---- | -------------------- | --------------------- |
| Fonte única de nomes | linhas 15-25 | `00`, `01` | DUPLICACAO_TRANSITORIA_PRE_FACHADA | SIM | QA da fase 1 e conversão controlada da fachada |
| Schema × dados | §0 | `01`, `02` | DUPLICACAO_TRANSITORIA_PRE_FACHADA | SIM | contratos e referências antigas migrados |
| Estilo universal | §1 | `10` | DUPLICACAO_TRANSITORIA_PRE_FACHADA | SIM | `contrato_estilo.md` apontar ao módulo |
| Tela/corpo/composição | §2-3, §14 | `20`, `40` | DUPLICACAO_TRANSITORIA_PRE_FACHADA | SIM | propriedade 20/40 auditada sem duplicação |
| Console | §4 | `32` | DUPLICACAO_TRANSITORIA_PRE_FACHADA | SIM | contrato console migrado |
| Barra/chips | §5 | `31` | DUPLICACAO_TRANSITORIA_PRE_FACHADA | SIM | contratos barra/chip migrados |
| Layout/redimensionamento | §6 | `21`, `33` | DUPLICACAO_TRANSITORIA_PRE_FACHADA | SIM | contrato_tela_json e contrato_lancador migrados |
| Cabeçalho | §7 | `30` | DUPLICACAO_TRANSITORIA_PRE_FACHADA | SIM | contrato_cabecalho migrado |
| Lançador | §8, §13 | `33`, `90` | DUPLICACAO_TRANSITORIA_PRE_FACHADA | SIM | histórico `menu` preservado e remissões migradas |
| Dashboard | §9 | `34`, relatório histórico | DUPLICACAO_TRANSITORIA_PRE_FACHADA | SIM | instância e pendência separadas sem conflito NOM-LEV-019 |
| Distribuição matricial | §16 | `41` | DUPLICACAO_TRANSITORIA_PRE_FACHADA | SIM | contratos JSON migrados |
| Dados externos/carregamento/modos | §17-19 | `42`, `43`, `44` | DUPLICACAO_TRANSITORIA_PRE_FACHADA | SIM | termos sem proprietário resolvidos |

## 15. Duplicações indevidas entre módulos

| Termo | Módulo 1 | Módulo 2 | Natureza da repetição | Proprietário correto | Estado |
| ----- | -------- | -------- | --------------------- | -------------------- | ------ |
| `JSON estrutural da tela` | `02` | `42` | artefato geral versus referência na fronteira multinível; `02` é proprietário do artefato; `42` referencia o termo para delimitar a fronteira com o JSON externo | `02` | REFERENCIA_PERMITIDA_COM_FRONTEIRA_EXPLICITA |
| `barra_de_menus` | `20` | `31` | `31` é proprietário exclusivo da definição específica; `20` removeu `barra_de_menus` dos termos proprietários e a cita apenas como região concreta com declaração explícita de fronteira | `31` para definição específica; `20` para referência de região | REFERENCIA_PERMITIDA |
| `config/estilo.json` | `02` | `10` | fronteira tornada explícita: `02` é proprietário do artefato/caminho; `10` é proprietário do vocabulário; `10` removeu `config/estilo.json` dos termos proprietários; ambos os módulos declaram a fronteira explicitamente | `02` para artefato; `10` para vocabulário | REFERENCIA_PERMITIDA_COM_FRONTEIRA_EXPLICITA |
| `grupo` estrutural | `20` | `40` | `40` é proprietário exclusivo do nó estrutural; `20` removeu `grupo` dos termos proprietários e o cita apenas como espécie de container com declaração explícita de fronteira | `40`; `20` cita apenas | REFERENCIA_PERMITIDA |
| `container estrutural` | `01` | `20` | conceito transversal e classificação de composição | `01` para conceito geral; `20` para uso em tela | REFERENCIA_PERMITIDA |
| `elemento funcional` | `01` | `20` | conceito transversal e classificação de composição | `01` para conceito geral; `20` para tipos do corpo | REFERENCIA_PERMITIDA |
| `loader` | `01` | `43` | conceito transversal versus papel no carregamento externo | `01` geral; `43` papel contextual | SENTIDOS_DISTINTOS_COMPROVADOS |
| `tela.json` | `02` | `20` | artefato/caminho versus declaração configurável da composição | `02` para artefato; `20` referência de uso | REFERENCIA_PERMITIDA |
| `ocupacao_vertical_terminal` | `20` | `21` | `20` referencia; `21` define | `21` | REFERENCIA_PERMITIDA |
| `vão` | `33` | `41` | sentidos por domínio diferentes | `33` lançador; `41` distribuição matricial | SENTIDOS_DISTINTOS_COMPROVADOS |
| `célula` | `40` | `41` | matriz de grupos versus distribuição matricial | `40`/`41` por sentido | SENTIDOS_DISTINTOS_COMPROVADOS |
| `coluna` | `33` | `41` | coluna do lançador versus coluna de grade | `33`/`41` por sentido | SENTIDOS_DISTINTOS_COMPROVADOS |

Não há mais `DEFINICAO_DUPLICADA` entre módulos após as correções do patch. As
fronteiras estão declaradas explicitamente. Referências permitidas e distintas
permanecem na tabela acima.

## 16. Lacunas e contradições

Tabela de tratamento do patch:

| ID | Estado anterior | Correção aplicada | Estado final |
| -- | --------------- | ----------------- | ------------ |
| LAC-0029-001 | BLOQUEADO_POR_CONTRADICAO (NOM-LEV-019 atribuído a dashboard) | Relatório histórico corrigido: NOM-LEV-017 = pendências (inclui dashboard); NOM-LEV-018 = Codex legado; NOM-LEV-019 = lista parcial ADRs; atribuição indevida NOM-LEV-001/caminhos também corrigida | RESOLVIDO |
| LAC-0029-002 | DEFINICAO_DUPLICADA (`config/estilo.json` em `02` e `10`) | Fronteira declarada explicitamente: `02` = artefato/caminho; `10` = vocabulário; `10` removeu do proprietário e declara referência permitida | RESOLVIDO |
| LAC-0029-003 | DEFINICAO_DUPLICADA (`barra_de_menus` em `20` e `31`) | `20` removeu `barra_de_menus` dos termos proprietários; fronteira com `31` declarada; `20` cita como região concreta apenas | RESOLVIDO |
| LAC-0029-004 | DEFINICAO_DUPLICADA (`grupo` estrutural em `20` e `40`) | `20` removeu `grupo` dos termos proprietários; fronteira com `40` declarada; `20` cita como espécie de container apenas | RESOLVIDO |
| LAC-0029-005 | TERMO_ATIVO_SEM_PROPRIETARIO (`popup_execucao`, `folha`, `campo`, `hierarquia_indentada`) | `popup_execucao` reclassificado como PENDENTE_SEM_DEFINICAO_APROVADA (NOM-LEV-017); `folha`/`campo` classificados como TERMO_CONCORRENTE_DEFERIDO em `42` seção 8A e `90` seção 4A; `hierarquia_indentada` classificada em `44` seção 8A e `90` seção 4A; nenhum desses é termo ativo | RECLASSIFICADO_COM_AUTORIDADE |
| LAC-0029-006 | REGRA_SEM_CONTRATO_COMPROVADO (pendências sem decisão; `34` sem contrato próprio nos nove) | Pendências classificadas como PENDENCIA_PRESERVADA_NAO_BLOQUEANTE_DA_FASE_1; `contrato_json_dashboard.md` existe no repositório e preserva regras do dashboard; alinhamento em seção 9.5 como FUTURA_NAO_BLOQUEANTE; `tx` é pendência, não regra vigente sem contrato | RECLASSIFICADO_COM_AUTORIDADE |
| LAC-0029-007 | REFERENCIA_ATIVA_SEM_MIGRACAO (17 arquivos, 67 ocorrências) | Condição da fase 2, não da fase 1; referências inventariadas em seção 13; migração será executada na fase 2 | PENDENCIA_DA_FASE_2 |
| LAC-0029-008 | CONTRADICAO_ENTRE_RELATORIO_E_ESTADO_FISICO (NOM-LEV-001 a 006 agrupados genericamente em `02`) | Registros individuais: NOM-LEV-001 = METADADO_DE_ORIGEM_PRESERVADO; NOM-LEV-002 = `01`/`00`; NOM-LEV-003 = `01`/`02`; NOM-LEV-004 = `02`/histórico; NOM-LEV-005 = ESTADO_TRANSITORIO_HISTORICO (relatório histórico seção 2.6); NOM-LEV-006 = `10`/`20`/`90` | RESOLVIDO |

```yaml
NOM-LEV-001:
  tratamento: METADADO_DE_ORIGEM_PRESERVADO_NO_RELATORIO
  modulo_proprietario: NAO_APLICAVEL
  definicao_terminologica_ativa: false
  cobertura: nome, tipo, escopo, status, origem, data de atualização, condição parcial do monólito preservados factualmente neste relatório

NOM-LEV-002:
  destinos:
    - 01_NUCLEO_COMUM.md
    - 00_INDICE.md

NOM-LEV-003:
  destinos:
    - 01_NUCLEO_COMUM.md
    - 02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md

NOM-LEV-004:
  destinos:
    - 02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md
    - RELATORIO_HISTORICO_NOMENCLATURA_MONOLITICA.md para caminhos históricos e estados reservados

NOM-LEV-005:
  destino:
    - RELATORIO_HISTORICO_NOMENCLATURA_MONOLITICA.md (seção 2.6)
  tratamento: ESTADO_TRANSITORIO_HISTORICO
  modulo_proprietario: NAO_APLICAVEL
  definicao_terminologica_ativa: false

NOM-LEV-006:
  destinos:
    - 10_ESTILO.md
    - 20_TELA_CORPO_E_COMPOSICAO.md
    - 90_ALIASES_E_TERMOS_DESCONTINUADOS.md quando houver alias
```

## 17. Condições para a fase 2

| Condição | Estado | Evidência |
| ------------------------------------------ | ------ | --------- |
| 17 módulos existem | SATISFEITA | `docs/nomenclatura/` contém os 17 arquivos esperados |
| 28 blocos mapeados corretamente | SATISFEITA | NOM-LEV-001 = METADADO_DE_ORIGEM; NOM-LEV-005 = ESTADO_TRANSITORIO_HISTORICO (relatório histórico seção 2.6); NOM-LEV-017/018/019 corrigidos em relatório histórico seção 2.5 |
| todos os termos ativos têm proprietário | SATISFEITA | `popup_execucao` = PENDENTE_SEM_DEFINICAO_APROVADA (não é termo ativo); `folha`/`campo`/`hierarquia_indentada` = TERMO_CONCORRENTE_DEFERIDO (não são termos ativos — seções 8A dos módulos `42`/`44` e seção 4A do módulo `90`) |
| não há definições duplicadas entre módulos | SATISFEITA | `barra_de_menus`: proprietário `31`, referência em `20` com fronteira declarada; `config/estilo.json`: artefato em `02`, vocabulário em `10` com fronteiras declaradas; `grupo` estrutural: proprietário `40`, referência em `20` com fronteira declarada |
| regras completas permanecem nos contratos | SATISFEITA | pendência `tx` = PENDENCIA_PRESERVADA_NAO_BLOQUEANTE_DA_FASE_1; alinhamento dashboard = FUTURA_NAO_BLOQUEANTE (contrato_json_dashboard.md seção 9.5); `popup_execucao` = pendência sem definição aprovada, não regra vigente |
| dependências por contrato estão propostas | SATISFEITA | seção 12 deste relatório |
| referências antigas estão inventariadas | SATISFEITA | seção 13; 350 arquivos/2720 ocorrências encontrados, com ativa normativa listada; migração é condição da fase 2, não da fase 1 |
| histórico está classificado | SATISFEITA | NOM-LEV-017 = bloco geral de pendências; NOM-LEV-018 = Codex legado; NOM-LEV-019 = lista parcial de ADRs; classificações corretas no relatório histórico seção 2.5 |
| pendências estão classificadas | SATISFEITA | NOM-LEV-017 registra todas as pendências como PENDENCIA_PRESERVADA_NAO_BLOQUEANTE_DA_FASE_1; nenhuma pendência promovida a regra sem contrato |
| monólito permanece intacto | SATISFEITA | `git status --short` sem `docs/NOMENCLATURA.md` alterado |
| contratos permanecem intactos | SATISFEITA | `git status --short` sem `docs/contratos/` alterado |
| índice geral permanece intacto | SATISFEITA | `git status --short` sem `docs/INDICE.md` alterado |
| relatório está completo | SATISFEITA | seções 1 a 19 presentes e corretas após patch |
| QA da fase 1 ainda está pendente | SATISFEITA | nenhuma QA executada nesta complementação |

Fase 2 não autorizada. Todas as condições materiais de bloqueio foram resolvidas. `QA_APLICACAO_ADR_FASE_1` é a próxima categoria obrigatória.

## 18. Estado Git

Comandos exigidos, executados a partir da raiz:

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
```

Comandos finais executados após esta atualização:

```text
git diff --check
saida: <vazio>

git diff --cached --name-only
saida: <vazio>
```

Checagem de arquivos não rastreados novos com `git diff --no-index --check /dev/null <arquivo>`:

| Arquivo | Resultado |
|---|---|
| `docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md` | sem erro de whitespace |
| `docs/nomenclatura/00_INDICE.md` | sem erro de whitespace |
| `docs/nomenclatura/01_NUCLEO_COMUM.md` | sem erro de whitespace |
| `docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` | sem erro de whitespace |
| `docs/nomenclatura/10_ESTILO.md` | sem erro de whitespace |
| `docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md` | sem erro de whitespace |
| `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` | sem erro de whitespace |
| `docs/nomenclatura/30_CABECALHO.md` | sem erro de whitespace |
| `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` | sem erro de whitespace |
| `docs/nomenclatura/32_CONSOLE.md` | sem erro de whitespace |
| `docs/nomenclatura/33_LANCADOR.md` | sem erro de whitespace |
| `docs/nomenclatura/34_DASHBOARD.md` | sem erro de whitespace |
| `docs/nomenclatura/40_GRUPOS_E_DISTRIBUICAO_DE_AREA.md` | sem erro de whitespace |
| `docs/nomenclatura/41_DISTRIBUICAO_MATRICIAL.md` | sem erro de whitespace |
| `docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md` | sem erro de whitespace |
| `docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md` | sem erro de whitespace |
| `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` | sem erro de whitespace |
| `docs/nomenclatura/90_ALIASES_E_TERMOS_DESCONTINUADOS.md` | sem erro de whitespace |
| `docs/relatorios/RELATORIO_HISTORICO_NOMENCLATURA_MONOLITICA.md` | sem erro de whitespace |
| `docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-1.md` | sem erro de whitespace |
| `docs/relatorios/RELATORIO_LEVANTAMENTO_REORGANIZACAO_NOMENCLATURA.md` | sem erro de whitespace |
| `docs/relatorios/RELATORIO_QA_ADR-0029.md` | sem erro de whitespace |
| `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0029.md` | sem erro de whitespace |

Confirmações após patch:

- todos os arquivos criados estão não rastreados ou listados nominalmente acima;
- arquivo rastreado com modificação pendente: somente `docs/adr/INDICE_ADR.md` (registro da ADR-0029 no índice — alteração da fase 1, não do patch);
- arquivos modificados pelo patch (todos dentro de `docs/nomenclatura/` e `docs/relatorios/` não rastreados — aparecem sob `??` no git status):
  - `docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` (fronteira `config/estilo.json`)
  - `docs/nomenclatura/10_ESTILO.md` (fronteira vocabulário × artefato)
  - `docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md` (remoção duplicatas `barra_de_menus` e `grupo`)
  - `docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md` (seção 8A termos concorrentes deferidos)
  - `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` (seção 8A termos concorrentes deferidos)
  - `docs/nomenclatura/90_ALIASES_E_TERMOS_DESCONTINUADOS.md` (seção 4A termos concorrentes localizáveis)
  - `docs/relatorios/RELATORIO_HISTORICO_NOMENCLATURA_MONOLITICA.md` (seções 2.5, 2.6, 2.7, 2.8, 3 e 4 corrigidas)
  - `docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-1.md` (este arquivo)
- ausência de arquivo inesperado: nenhum caminho fora de `docs/adr/`, `docs/nomenclatura/` e `docs/relatorios/` aparece no status;
- stage vazio: confirmado por `git diff --cached --name-only` (saída vazia);
- nenhum commit executado;
- monólito intacto;
- contratos intactos;
- índice geral intacto;
- backlog e issues intactos;
- código e configurações intactos.

## 19. Encerramento

```yaml
etapa_executada: PATCH_APLICACAO_ADR_FASE_1
fase: FASE_1_MATERIALIZACAO_PRE_FACHADA
adr: docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md

modulos_esperados: 17
modulos_existentes: 17
NOM_LEV_esperados: 28
NOM_LEV_reconciliados: 28

contagem_de_termos_no_inventario:
  termos_ativos: 49          # todos com módulo proprietário; popup_execucao/folha/campo/hierarquia_indentada excluídos
  termos_pendentes: 2        # popup_execucao (PENDENTE_SEM_DEFINICAO_APROVADA) + alinhamento_dashboard (FUTURA_NAO_BLOQUEANTE)
  pendencias_NOM_LEV_017: 6  # tx, popup_execucao, alinhamento_dashboard, segunda_pauta_estilos, campos_navegacao_lancador, reorganizacao_corpo_dashboard
  termos_concorrentes_deferidos: 3  # folha → conteudo, campo → nome_valor, hierarquia_indentada → hierarquia
  aliases_ativos: 2          # sobreposto, lado_a_lado
  divergencias_terminologicas_ativas: 1  # modo_normal × modo_nao_verboso
  termos_descontinuados: 3   # menu, dado, Info

termos_ativos_sem_proprietario: 0
definicoes_duplicadas_entre_modulos: 0
regras_ativas_sem_contrato_comprovado: 0
referencias_antigas_inventariadas: 2720

lacunas:
  LAC-0029-001: RESOLVIDO       # NOM-LEV-017/018/019 corrigidos no relatório histórico seções 2.5 e 3
  LAC-0029-002: RESOLVIDO       # config/estilo.json: 02=artefato, 10=vocabulário; fronteiras declaradas
  LAC-0029-003: RESOLVIDO       # barra_de_menus: proprietário 31; referência permitida em 20
  LAC-0029-004: RESOLVIDO       # grupo estrutural: proprietário 40; referência permitida em 20
  LAC-0029-005: RECLASSIFICADO_COM_AUTORIDADE  # popup_execucao=PENDENTE; folha/campo/hierarquia_indentada=TERMO_CONCORRENTE_DEFERIDO
  LAC-0029-006: RECLASSIFICADO_COM_AUTORIDADE  # pendências = PENDENCIA_PRESERVADA_NAO_BLOQUEANTE_DA_FASE_1
  LAC-0029-007: PENDENCIA_DA_FASE_2            # migração de 17 arquivos normativos e 67 ocorrências
  LAC-0029-008: RESOLVIDO       # NOM-LEV-001 a 006 com registros individuais; NOM-LEV-001=METADADO, NOM-LEV-005=ESTADO_TRANSITORIO_HISTORICO

relatorio_historico: docs/relatorios/RELATORIO_HISTORICO_NOMENCLATURA_MONOLITICA.md
relatorio_aplicacao_atualizado: docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-1.md

arquivos_alterados_no_patch:
  - docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md
  - docs/nomenclatura/10_ESTILO.md
  - docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md
  - docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md
  - docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
  - docs/nomenclatura/90_ALIASES_E_TERMOS_DESCONTINUADOS.md
  - docs/relatorios/RELATORIO_HISTORICO_NOMENCLATURA_MONOLITICA.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-1.md

arquivos_alterados_no_patch_residual:
  - docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md
  - docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-1.md

monolito_preservado_integralmente: true
contratos_alterados: false
indice_geral_alterado: false
issues_alterado: false
backlog_alterado: false
codigo_alterado: false

stage_vazio: true
commit_executado: false

status_literal: APLICACAO_ADR_FASE_1_CONCLUIDA_AGUARDANDO_QA
proxima_categoria: QA_APLICACAO_ADR_FASE_1
```

## 20. Encerramento do patch residual

```yaml
etapa_executada: PATCH_APLICACAO_ADR_FASE_1_RESIDUAL
fase: FASE_1_MATERIALIZACAO_PRE_FACHADA

residuos_corrigidos:
  secao_3_estado_antigo: substituida por formulacao factual pos-patch; removida afirmacao de bloqueios remanescentes
  secao_5_lista_de_arquivos: distingue alteracoes_da_fase_1_original (ADR e INDICE_ADR) de alteracoes_do_patch_PATCH_APLICACAO_ADR_FASE_1 (oito arquivos)
  propriedade_JSON_estrutural_da_tela: modulo 02 declarado proprietario com fronteira explicita; 42 referencia com fronteira explicita; NAO_CONFIRMADO removido
  residuo_config_estilo_no_inventario: removido da coluna de duplicacao de docs/NOMENCLATURA.md; LAC-0029-002 ja estava resolvida
  campo_de_arquivos_do_encerramento: modulos_alterados_no_patch substituido por arquivos_alterados_no_patch; patch_residual acrescentado

proprietario_JSON_estrutural_da_tela: 02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md
referencia_multinivel_em_42: REFERENCIA_PERMITIDA_COM_FRONTEIRA_EXPLICITA
definicoes_duplicadas_entre_modulos: 0
termos_ativos_sem_proprietario: 0
regras_ativas_sem_contrato_comprovado: 0

arquivos_alterados_no_patch_residual:
  - docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md
  - docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-1.md
git_diff_check: sem erros de whitespace
stage_vazio: true
commit_executado: false

status_literal: APLICACAO_ADR_FASE_1_CONCLUIDA_AGUARDANDO_QA
proxima_categoria: QA_APLICACAO_ADR_FASE_1
```
