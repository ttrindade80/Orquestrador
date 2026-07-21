# Relatório de Levantamento — Pendências Console, Processo e Prompts

```yaml
etapa: LEVANTAMENTO_DOCUMENTAL_OU_ARQUITETURAL
resultado_geral: >
  Levantamento neutro concluído. Foram localizadas evidências documentais,
  declarativas e materiais sobre os cinco itens investigados. Nenhum arquivo
  fora deste relatório foi criado ou alterado.
data: 2026-07-21
```

---

## 1. Objetivo e limites

Objetivo: investigar factualmente o que foi documentado, implementado, testado
ou deixado pendente nos cinco itens abaixo:

1. Funcionalidades futuras do console (2.1)
2. Descrição do cabeçalho com pouca largura (2.2)
3. Continuidade entre H-0025 e H-0026 (2.3)
4. Compatibilidade da suíte legada com pytest (2.4)
5. Regras do sistema de prompts originadas no H-0030 (2.5)

Limites observados:

- não houve implementação;
- não houve criação de ADR, handoff, contrato ou correção de código;
- não houve QA de entregáveis;
- não houve escolha entre alternativas de comportamento;
- arquivo criado: somente este relatório.

---

## 2. Artefatos consultados

### 2.1 Índices e backlog

- `docs/INDICE.md`
- `docs/nomenclatura/00_INDICE.md`
- `docs/backlog.md` — modelo vazio (sem itens reais)
- `docs/issues.md` — modelo vazio (sem itens reais)

### 2.2 Contratos consultados

- `docs/contratos/contrato_console.md`
- `docs/contratos/contrato_cabecalho.md` (via LEVANTAMENTO_REVISOES_H-0030)
- `docs/contratos/contrato_processo_desenvolvimento.md`

### 2.3 ADRs e handoffs consultados

- `docs/adr/INDICE_ADR.md`
- `docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md`
- `docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md`
- `docs/handoff/H-0030-catalogo-telas-utilizaveis.md` (parcial)
- `docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md` (parcial)
- `docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md` (parcial)
- `docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md` (via nome e commits)

### 2.4 Relatórios consultados

- `docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md`
- `docs/relatorios/RELATORIO_VERIFICACAO_FECHAMENTO_H-0025.md`
- `docs/relatorios/RELATORIO_QA_H-0030_HANDOFF.md` (parcial)
- `docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0030.md` (parcial)
- `docs/relatorios/RELATORIO_ORIGEM_ERROS_PYTEST_LEGADO.md`
- `docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0030.md` (parcial)

### 2.5 Sistema de prompts consultado

- `/home/tiago/Dropbox/UFRGS/Prompts/Gerente_Orquestrador/Regras/00_INDICE_PROMPTS.md`
- `/home/tiago/Dropbox/UFRGS/Prompts/Gerente_Orquestrador/Regras/02_CONTRATO_GERENTE.md`
- `/home/tiago/Dropbox/UFRGS/Prompts/Gerente_Orquestrador/Regras/03_FLUXOS_E_CLASSIFICACAO.md`
- `/home/tiago/Dropbox/UFRGS/Prompts/Gerente_Orquestrador/Regras/04_MINUTAS_HANDOFF_IMPLEMENTACAO.md`
- `/home/tiago/Dropbox/UFRGS/Prompts/Gerente_Orquestrador/Regras/06_MINUTAS_QA_PATCH_FECHAMENTO.md`
- `/home/tiago/Dropbox/UFRGS/Prompts/Gerente_Orquestrador/Regras/RELATORIO_RECONSTRUCAO_SISTEMA_PROMPTS_2026-07-21.md`
- `/home/tiago/Dropbox/UFRGS/Prompts/Gerente_Orquestrador/Regras/20260720/RELATORIO_REVISAO_REGRAS_H-0028_H-0030.md`
- `/home/tiago/Dropbox/UFRGS/Prompts/Gerente_Orquestrador/Regras/20260720/04_MINUTAS_HANDOFF_IMPLEMENTACAO.md`

---

## 3. Comandos executados

```bash
git log --oneline --decorate -n 30
git status --short
ls docs/relatorios/
ls docs/handoff/
find . -name "02_CONTRATO_GERENTE.md" -o -name "03_FLUXOS_E_CLASSIFICACAO.md" ...
find /home/tiago/Dropbox/UFRGS -maxdepth 8 -name "02_CONTRATO_GERENTE.md" ...
grep -n "excecao focal|excecao operacional|..." (vários arquivos)
grep -rn "pytest|seis scripts|suite.can" docs/
ls tela/teste_*.py demo/teste_*.py
```

---

## 4. Estado Git observado

```yaml
branch: master
HEAD: 23f49d0 docs: aplica nomenclatura modular e leitura seletiva
stage: vazio
workspace: COM_ARQUIVOS_NAO_RASTREADOS
arquivos_modificados: []
arquivos_nao_rastreados:
  - docs/relatorios/RELATORIO_LEVANTAMENTO_PENDENCIAS_CONSOLE_PROCESSO_E_PROMPTS.md
```

Evidência: `git status --short --untracked-files=all` retornou exatamente:

```
?? docs/relatorios/RELATORIO_LEVANTAMENTO_PENDENCIAS_CONSOLE_PROCESSO_E_PROMPTS.md
```

Observação: `.pytest_cache/` não aparece na saída de
`git status --short --untracked-files=all`, indicando que não é classificado
como arquivo não rastreado pelo git. O diretório pode existir no filesystem,
mas seu estado no git é:

```yaml
cache_presente_no_filesystem: true
estado_no_git: IGNORADO_OU_NAO_LISTADO
```

---

## 5. Item 2.1 — Funcionalidades futuras do console

### 5.1 Origem das demandas

O `contrato_console.md` (ativo, versão 0.1) define o console como container
genérico de itens heterogêneos. Ele fecha as seguintes funcionalidades como
decisão normativa contratual:

- §7: **Navegação** por item via `[✥]` — regra ativa
- §8: **Seleção** por políticas `nenhuma`, `unica` e `multipla` — regra ativa
- §9: **Ação de Enter** (`[⏎]`) por item em foco — regra ativa
- §19 e §20: **Conteúdo externo** (ADR-0026, ADR-0027) — regra ativa

Backlog e issues não contêm itens reais: os dois arquivos estão em formato
de modelo com apenas exemplos.

### 5.2 Investigação 1 — Navegação entre itens

```yaml
origem_da_demanda: contrato_console.md §7
backlog_issue_planejamento: NAO_LOCALIZADO (backlog e issues são modelos)
adr_ou_decisao_arquitetural: parcial (ADR-0005 define que lancador nao e navegavel; NAO_LOCALIZADA ADR especifica de implementacao do cursor do console)
contrato_comportamental: PRESENTE (contrato_console.md §7, §14)
handoff: NAO_LOCALIZADO
relatorio_de_implementacao: NAO_LOCALIZADO
relatorio_de_qa: NAO_LOCALIZADO
validacao_manual: NAO_LOCALIZADO
codigo: NAO_LOCALIZADO
testes: NAO_LOCALIZADO
commit: NAO_LOCALIZADO
pendencia_registrada: >
  contrato_console.md §18: "Implementação do cursor: mecanismo de navegação
  interna, posição corrente, wrap toroidal detalhado e tratamento de célula
  vazia pertencem à implementação futura."
  H-0036 §12.2 e H-0037 §26: excluem explicitamente navegação, seleção,
  expansão, recolhimento e paginação interativa.
estado_material: DOCUMENTADO_NAO_IMPLEMENTADO
```

### 5.3 Investigação 2 — Seleção de itens

```yaml
origem_da_demanda: contrato_console.md §8
backlog_issue_planejamento: NAO_LOCALIZADO
adr_ou_decisao_arquitetural: PRESENTE (contrato define politica_selecao)
contrato_comportamental: PRESENTE (contrato_console.md §8)
handoff: NAO_LOCALIZADO
relatorio_de_implementacao: NAO_LOCALIZADO
relatorio_de_qa: NAO_LOCALIZADO
codigo: NAO_LOCALIZADO
testes: NAO_LOCALIZADO
commit: NAO_LOCALIZADO
pendencia_registrada: >
  contrato_console.md §18: fora de escopo.
  H-0036 §12.2 e H-0037 §26: seleção explicitamente excluída.
estado_material: DOCUMENTADO_NAO_IMPLEMENTADO
```

### 5.4 Investigação 3 — Execução simulada de ações

```yaml
origem_da_demanda: contrato_console.md §9
backlog_issue_planejamento: NAO_LOCALIZADO
adr_ou_decisao_arquitetural: >
  Decisão normativa: ação pertence ao item, deve ser declarativa e
  registrada (whitelist); ADR-0016 (KeyboardInterrupt).
contrato_comportamental: PRESENTE (contrato_console.md §9, §10)
handoff: NAO_LOCALIZADO
relatorio_de_implementacao: NAO_LOCALIZADO
relatorio_de_qa: NAO_LOCALIZADO
codigo: NAO_LOCALIZADO
testes: NAO_LOCALIZADO
commit: NAO_LOCALIZADO
pendencia_registrada: >
  contrato_console.md §18: "Registry completo de ações (DOC-B009): pendente."
  H-0036 e H-0037: excluem ações de Enter.
estado_material: DOCUMENTADO_NAO_IMPLEMENTADO
```

### 5.5 Investigação 4 — Exibição de conteúdo proveniente de JSON de testes

Esta investigação exige distinção precisa entre:

- conteúdo externo (JSON de runtime fornecido ao console);
- JSON estrutural (tela.json que declara o console);
- apresentações multinível;
- modos verboso/não verboso.

#### 5.5.1 Relação com ciclos anteriores

O H-0036 implementou o **fornecimento externo de dados ao console** por JSON
multinível com três apresentações (`hierarquia`, `tabela`, `conjuntos_campos`).
O H-0037 implementou as **apresentações multinível com modos por tela**
(políticas `somente_verboso`, `somente_nao_verboso`, `alternavel`).

Esses dois ciclos cobrem materialmente o item 4:

- fixtures JSON permanentes com conteúdo real (não placeholder);
- carregamento separado pelo `demo.py` (ADR-0027);
- modelo valida e transporta o conteúdo;
- renderizador exibe nas apresentações disponíveis;
- modos de visualização por política declarada no JSON estrutural.

#### 5.5.2 Relação material com conteúdo externo e com JSON estrutural

```yaml
conteudo_externo_vs_json_estrutural:
  conteudo_externo: documento JSON separado do tela.json; fornecido ao loader
    pelo demo.py; não incorporado ao JSON estrutural da tela.
  json_estrutural: tela.json declara o elemento console e sua política de
    formato; não transporta dados de runtime.
  distinguidos_materialmente: sim, pelos contratos, ADRs (0026, 0027) e pela
    implementação (H-0036).
```

#### 5.5.3 Estado material

```yaml
origem_da_demanda: contrato_console.md §19, §20, §21; ADR-0026, ADR-0027, ADR-0028
backlog_issue_planejamento: NAO_LOCALIZADO formalmente; demanda presente nos contratos
adr_ou_decisao_arquitetural: PRESENTE (ADR-0026, ADR-0027, ADR-0028 com D23)
contrato_comportamental: PRESENTE (contrato_console.md §19 a §21; contrato_json_console.md)
handoff: PRESENTE (H-0036, H-0037)
relatorio_de_implementacao: PRESENTE (IMP-0036, IMP-0037)
relatorio_de_qa:
  handoff: RELATORIO_QA_H-0036_HANDOFF.md, RELATORIO_QA_H-0037_HANDOFF.md
  implementacao: RELATORIO_QA_H-0036_IMPLEMENTACAO.md, RELATORIO_QA_H-0037_IMPLEMENTACAO.md
validacao_manual: RELATORIO_VALIDACAO_MANUAL_H-0037.md (localizado na listagem)
codigo: PRESENTE (tela/renderizador.py, tela/loader.py, tela/modelo.py; demo/demo.py)
testes: PRESENTE (demo/teste_demo_console.py, demo/teste_demo_console_modos.py)
commit:
  H-0036: "9957efd feat: implementa fornecimento externo de dados ao console"
  H-0037: "c90349c feat: implementa apresentacoes multinivel com modos por tela"
estado_material: CONCLUIDO_E_COMPROVADO
limitacao_registrada: >
  Navegação, seleção, expansão, recolhimento e paginação interativa de
  conteúdo multinível foram explicitamente excluídos do escopo do H-0036
  (§12.2) e do H-0037 (§26). Permanecem DOCUMENTADO_NAO_IMPLEMENTADO.
```

---

## 6. Item 2.2 — Descrição do cabeçalho com pouca largura

### 6.1 Evidências encontradas

Este item foi investigado pelo `LEVANTAMENTO_REVISOES_H-0030.md` (pontos 1 e 2)
com a seguinte conclusão:

```yaml
problema_observado: >
  Quando a largura do terminal é reduzida, a descrição do cabeçalho é cortada
  sem reticências e sem quebra de linha. Observado durante a validação manual
  do H-0030.
comportamento_atual_documentado: >
  contrato_cabecalho.md: max_caracteres define número máximo e texto
  excedente é truncado antes da renderização. Nenhuma regra normativa ativa
  determina quebra por largura ou reticências por overflow horizontal.
comportamento_atual_implementado: >
  tela/renderizador.py::_linha_conteudo: corte por content_w sem reticências
  e sem segunda linha. Comprovado por evidência executável no LEVANTAMENTO_H-0030.
decisoes_ja_fechadas: >
  truncamento por max_caracteres existe e é normativo; nenhuma decisão existe
  sobre quebra vs reticências para overflow horizontal.
decisoes_ainda_abertas:
  - escolha entre quebra em até duas linhas ou truncamento com reticências;
  - forma das reticências ("..." ou caractere único);
  - comportamento quando exceder duas linhas;
  - interação entre max_caracteres e largura do terminal;
  - adaptação durante redimensionamento.
artefato_que_registra_o_bloqueio: >
  docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md, §7, classificacao:
  REGRA_AUSENTE / bloqueio: BLOCKED_USER_DECISION.
```

### 6.2 Estado atual confirmado

O `LEVANTAMENTO_REVISOES_H-0030.md` registra que nenhuma decisão foi tomada
sobre quebra vs reticências. O H-0034, H-0035, H-0036 e H-0037 não abordaram
esse ponto. Nenhum ciclo posterior ao levantamento alterou o cabeçalho.

```text
BLOCKED_USER_DECISION
```

Eventual criação de ADR depende de decisão explícita do usuário sobre qual
comportamento adotar (quebra em até duas linhas **ou** truncamento com
reticências).

---

## 7. Item 2.3 — Continuidade entre H-0025 e H-0026

### 7.1 H-0025

#### 7.1.1 Existência e objetivo

Arquivo: `docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md`
Objetivo: implementar a distribuição vertical explícita da altura útil do corpo
entre seus filhos diretos nos modos `igual`, `percentual` e `fracao`,
substituindo operacionalmente o H-0024 bloqueado.

#### 7.1.2 Relação com H-0024

O H-0024 foi bloqueado durante a implementação por colisão normativa. A
ADR-0018 resolveu o bloqueio distinguindo ausência de `distribuicao` (preserva
conteúdo natural) de distribuição explícita (aloca área). O H-0025 cita
explicitamente esse histórico (§2) e declara que substitui operacionalmente o
H-0024, que permanece preservado como evidência histórica.

#### 7.1.3 Cadeia documental do H-0025

```yaml
handoff_existente: sim
status_do_handoff: proposto (cabeçalho) — mas aprovado pelo QA
qa_do_handoff:
  arquivo: docs/relatorios/RELATORIO_QA_H-0025_HANDOFF.md
  status: H1_HANDOFF_APPROVED
implementacao:
  arquivo: docs/relatorios/IMP-0026-distribuicao-vertical-explicita-area-corpo.md
  existente: sim
qa_da_implementacao:
  arquivo: docs/relatorios/RELATORIO_QA_H-0025_IMPLEMENTACAO.md
  status: I1_IMPLEMENTATION_APPROVED
verificacao_de_fechamento:
  arquivo: docs/relatorios/RELATORIO_VERIFICACAO_FECHAMENTO_H-0025.md
  status: CLOSURE_READY_FOR_COMMIT_PREPARATION
commit:
  hash: 1cc0dff
  mensagem: "feat: implementa distribuicao vertical explicita do corpo"
  COMPROVADO: sim (presente em git log)
```

**H-0025_IMPLEMENTACAO: CONCLUIDA_E_COMPROVADA**
**H-0025_COMMIT: COMPROVADO (`1cc0dff`)**

Não é necessário usar o estado posterior (H-0026) como prova do H-0025. A
cadeia documental do H-0025 é completa e independente.

### 7.2 H-0026

#### 7.2.1 Existência e objetivo

Arquivo: `docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md`
Objetivo: implementar a distribuição horizontal explícita do corpo nos modos
`percentual` e `fracao`, reutilizando o algoritmo de maiores restos do H-0025.

#### 7.2.2 Relação declarada com H-0025

O H-0026 declara explicitamente (§2 e §7.1) que o H-0025 é dependência
satisfeita:

```text
H-0025: fechado e implementado (IMP-0026).
```

Cita o commit `1cc0dff` no estado comprovado do repositório (§4.1):

```text
commit:  1cc0dff feat: implementa distribuicao vertical explicita do corpo
```

#### 7.2.3 Cadeia documental do H-0026

```yaml
handoff_existente: sim
qa_do_handoff:
  arquivo: docs/relatorios/RELATORIO_QA_H-0026_HANDOFF.md
  existente: sim (localizado na listagem de relatorios)
implementacao:
  arquivo: docs/relatorios/IMP-0027-distribuicao-horizontal-percentual-fracao-corpo.md
  existente: sim (localizado na listagem)
qa_da_implementacao:
  arquivo: docs/relatorios/RELATORIO_QA_H-0026_IMPLEMENTACAO.md
  existente: sim
verificacao_de_fechamento:
  arquivo: docs/relatorios/RELATORIO_VERIFICACAO_FECHAMENTO_H-0026.md
  existente: sim
commit:
  hash: 40015b6
  mensagem: "feat: implementa distribuicao horizontal percentual e fracionaria"
  COMPROVADO: sim (presente em git log)
```

### 7.3 Consistência documental

A relação declarada entre H-0025 e H-0026 é consistente: o H-0026 usa a
implementação do H-0025 (loader e modelo aceitam `corpo.distribuicao`) e
estende somente o renderizador para o eixo horizontal.

Não existe uso indevido de estado posterior como prova do anterior: a cadeia
completa do H-0025 foi verificada independentemente.

---

## 8. Item 2.4 — Compatibilidade da suíte legada com pytest

### 8.1 Definição atual da suíte canônica

Desde o H-0031 (migração do repositório), a suíte canônica era definida como
"seis scripts com código de saída zero" (IMP-0031 registrado em 1796/1796).

No estado atual do repositório (HEAD `23f49d0`), os scripts de teste são:

```text
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
tela/teste_distribuicao_matricial.py
demo/teste_demo.py
demo/teste_diagnostico.py
demo/teste_explorar_barra_de_menus.py
demo/teste_demo_distribuicao.py
demo/teste_demo_console.py
demo/teste_demo_console_modos.py
```

Total: 10 arquivos de teste. Os ciclos H-0035, H-0036 e H-0037 adicionaram
scripts além dos seis originais. A definição de "seis scripts" é histórica
(válida no H-0031); o número atual não foi formalmente redocumentado como
nova suíte canônica.

### 8.2 Referências documentais ao pytest

```yaml
primeiro_aparecimento: H-0028 (handoff que introduziu pytest como gate)
investigacao_historica: docs/relatorios/RELATORIO_ORIGEM_ERROS_PYTEST_LEGADO.md
status_do_relatorio: ORIGIN_CONFIRMED_NEVER_PYTEST_COMPATIBLE
causa_dos_erros: >
  10 funções com parâmetros posicionais (tmp_base, modelo, resultado_esperado)
  coletadas pelo pytest desde a origem; nunca foram fixtures pytest; sempre
  foram helpers do main() interno dos scripts.
```

### 8.3 Configuração existente para pytest

```yaml
conftest_py: NUNCA_EXISTIU
pytest_ini: NUNCA_EXISTIU
pyproject_toml: NUNCA_EXISTIU
setup_cfg: NUNCA_EXISTIU
tox_ini: NUNCA_EXISTIU
pytest_cache:
  cache_presente_no_filesystem: true
  estado_no_git: IGNORADO_OU_NAO_LISTADO
  evidencia: pytest foi executado mas sem configuração formal
```

### 8.4 Testes que funcionam ou não por coleta automática

O relatório `RELATORIO_ORIGEM_ERROS_PYTEST_LEGADO.md` comprovou:

- todos os testes das classes `test_` (prefixo canônico pytest) passam sem erro;
- 10 funções com prefixo `teste_` e parâmetros posicionais geram erro de coleta;
- esses 10 erros existem desde o primeiro commit de cada função;
- a execução direta (suíte canônica) sempre retornou 100% de aprovação.

Após os ciclos H-0035, H-0036 e H-0037, o repositório adicionou novos testes
que também usam a convenção `test_` (compatível com pytest). O número exato de
erros de coleta do pytest no estado atual não foi verificado neste levantamento.

### 8.5 Decisão de abrir ou não o ciclo

```yaml
decisao_explícita_de_abrir_ciclo: NAO_LOCALIZADA
alternativas_documentadas: sim (RELATORIO_ORIGEM_ERROS_PYTEST_LEGADO.md §20:
  4 alternativas técnicas listadas sem prioridade)
estado_classificado: OPCIONAL_NAO_INICIADO
abertura_do_ciclo_depende_de_decisao_do_usuario: sim
```

---

## 9. Item 2.5 — Regras do sistema de prompts originadas no H-0030

### 9.1 Localização dos arquivos

Os arquivos `00_INDICE_PROMPTS.md`, `02_CONTRATO_GERENTE.md`,
`03_FLUXOS_E_CLASSIFICACAO.md`, `04_MINUTAS_HANDOFF_IMPLEMENTACAO.md` e
`06_MINUTAS_QA_PATCH_FECHAMENTO.md` **não existem no repositório Git**.

Estão em:

```text
/home/tiago/Dropbox/UFRGS/Prompts/Gerente_Orquestrador/Regras/
```

Versões históricas (backups datados) estão em subpastas `20260712/`,
`20260713/`, `20260720/`, `20260721/`.

### 9.2 Origem das regras

O relatório
`/home/tiago/Dropbox/UFRGS/Prompts/Gerente_Orquestrador/Regras/20260720/RELATORIO_REVISAO_REGRAS_H-0028_H-0030.md`
registra que as quatro regras investigadas foram identificadas como lacunas
nos ciclos H-0028 a H-0030, com propagação realizada em 2026-07-20.

Houve uma **reconstrução integral** em 2026-07-21 (`RELATORIO_RECONSTRUCAO_SISTEMA_PROMPTS_2026-07-21.md`)
que focou em mistura de autoria/QA, proibição de `PREPARAR_COMMIT`, referências
desatualizadas do índice e leitura seletiva da nomenclatura.

### 9.3 Mapa de leitura do 00_INDICE_PROMPTS.md

O `00_INDICE_PROMPTS.md` (vigente, data 2026-07-21) aponta para:

- seção 5.3: criar ou corrigir handoff → `04_MINUTAS_HANDOFF_IMPLEMENTACAO.md:
  Criar ou corrigir handoff`
- seção 5.5: implementar handoff → `04_MINUTAS_HANDOFF_IMPLEMENTACAO.md:
  Implementar handoff aprovado`
- seção 5.7: QA de implementação → `06_MINUTAS_QA_PATCH_FECHAMENTO.md:
  QA de implementação`

Os títulos referenciados foram verificados como existentes nos arquivos
correspondentes. O mapa de leitura aponta para títulos corretos.

### 9.4 Verificação por regra

#### Regra 1 — Separar as limitações do autor do handoff das permissões da futura implementação

```yaml
regra: >
  As restrições de escopo do autor documental não devem contaminar as
  permissões que o handoff concede ao futuro executor de implementação.
arquivos_em_que_aparece:
  - /Regras/20260720/04_MINUTAS_HANDOFF_IMPLEMENTACAO.md (linha 13 e 42):
    "sem confundir as restrições do autor documental com as permissões da
    futura implementação" — EXPLÍCITA
  - /Regras/20260720/00_INDICE_PROMPTS.md (linha 180):
    "separadas formalmente as permissões do autor do handoff e da futura
    implementação" — EXPLÍCITA
  - /Regras/04_MINUTAS_HANDOFF_IMPLEMENTACAO.md (vigente):
    campo "regra_de_excecao" na estrutura obrigatória (linha 85) — IMPLÍCITA;
    sem texto explícito sobre separação de escopos.
  - /Regras/02_CONTRATO_GERENTE.md (vigente): AUSENTE
  - /Regras/03_FLUXOS_E_CLASSIFICACAO.md (vigente): AUSENTE
  - /Regras/06_MINUTAS_QA_PATCH_FECHAMENTO.md (vigente): AUSENTE
cobertura: PARCIAL
lacuna_exata: >
  A versão 2026-07-20 continha texto explícito sobre separação em
  04_MINUTAS_HANDOFF_IMPLEMENTACAO.md e em 00_INDICE_PROMPTS.md.
  A reconstrução de 2026-07-21 não preservou esse texto explícito na versão
  vigente de 04_MINUTAS. O campo "regra_de_excecao" na estrutura obrigatória
  do handoff implica a separação, mas não a enuncia.
alteracao_documental_ainda_necessaria: >
  NAO_CONFIRMADO se a reconstrução teve intenção de omitir ou se foi lacuna.
  Requer decisão do usuário antes de qualquer correção.
```

#### Regra 2 — Não criar proibições que tornem o handoff inexequível

```yaml
regra: >
  O handoff deve ser verificado quanto à coerência entre arquivos autorizados,
  testes, suíte canônica, demonstração e relatório, de modo que a lista nominal
  não torne a entrega impossível.
arquivos_em_que_aparece:
  - /Regras/20260720/RELATORIO_REVISAO_REGRAS_H-0028_H-0030.md (linha 29):
    "O H-0030 mostrou que uma lista nominal pode ser segura e ainda assim
    tornar o handoff inexequível." — ORIGEM DOCUMENTADA
  - /Regras/04_MINUTAS_HANDOFF_IMPLEMENTACAO.md (vigente, linha 94):
    "não autorizar arquivo 'talvez necessário' como modificável" — PARCIAL
    (cobre arquivos desnecessários, não o risco de inexequibilidade)
  - /Regras/02_CONTRATO_GERENTE.md (vigente): AUSENTE
  - /Regras/03_FLUXOS_E_CLASSIFICACAO.md (vigente): AUSENTE
  - /Regras/06_MINUTAS_QA_PATCH_FECHAMENTO.md (vigente): AUSENTE
cobertura: PARCIAL
lacuna_exata: >
  A regra foi identificada como lacuna no relatório de revisão de 2026-07-20,
  mas não foi encontrada como regra normativa explícita nos arquivos vigentes.
  A verificação de exequibilidade do handoff não consta como etapa obrigatória
  em nenhum dos quatro arquivos inspecionados.
alteracao_documental_ainda_necessaria: >
  SIM — a regra não está explicitamente propagada nos arquivos vigentes como
  verificação obrigatória de criação de handoff.
```

#### Regra 3 — Permitir exceção focal quando o executor: parar antes, justificar, delimitar, receber autorização, registrar

```yaml
regra: >
  Quando um arquivo fora da lista nominal for estritamente necessário, o
  executor deve: (1) parar antes da alteração; (2) justificar a necessidade;
  (3) delimitar o escopo; (4) receber autorização explícita do usuário;
  (5) registrar a autorização no relatório.
arquivos_em_que_aparece:
  - /Regras/03_FLUXOS_E_CLASSIFICACAO.md (vigente, §7.1, linhas 186-195):
    "pausa; justificativa; escopo exato; autorização explícita do usuário;
    registro no relatório; auditoria do QA somente contra a autorização" — COMPLETA
  - /Regras/04_MINUTAS_HANDOFF_IMPLEMENTACAO.md (vigente, "Arquivo externo
    à lista", linhas 151-162): "parar antes da alteração; solicitar autorização
    explícita; arquivo, necessidade, risco_de_nao_alterar, escopo_exato,
    nova_semantica" — PARCIAL (falta "registrar no relatório" explicitamente)
  - /Regras/02_CONTRATO_GERENTE.md (vigente): AUSENTE
  - /Regras/06_MINUTAS_QA_PATCH_FECHAMENTO.md (vigente): menciona "exceção
    operacional focal" na linha 306 mas sem o procedimento completo — PARCIAL
cobertura: PARCIAL
lacuna_exata: >
  03_FLUXOS tem cobertura completa (§7.1). 04_MINUTAS cobre 4 das 5 condições
  mas omite "registrar a autorização no relatório" como passo explícito.
  02_CONTRATO_GERENTE e 06_MINUTAS_QA não repetem o procedimento completo.
alteracao_documental_ainda_necessaria: >
  Dependendo da interpretação: o 03_FLUXOS cobre a regra completamente; a
  ausência nos demais arquivos pode ser lacuna ou escolha de não repetir.
  Requer decisão do usuário.
```

#### Regra 4 — Limitar a exceção para que não autorize nova arquitetura, schema, política ou semântica

```yaml
regra: >
  A exceção operacional não autoriza o executor a introduzir nova arquitetura,
  schema, política ou semântica.
arquivos_em_que_aparece:
  - /Regras/03_FLUXOS_E_CLASSIFICACAO.md (vigente, §7.1, linha 197):
    "Não autoriza nova arquitetura, schema, política ou semântica." — COMPLETA
  - /Regras/04_MINUTAS_HANDOFF_IMPLEMENTACAO.md (vigente, "Arquivo externo
    à lista", linha 160): campo "nova_semantica: true|false" — PARCIAL
    (cobre semântica como campo de declaração, não enuncia o limite completo)
  - /Regras/02_CONTRATO_GERENTE.md (vigente): AUSENTE
  - /Regras/06_MINUTAS_QA_PATCH_FECHAMENTO.md (vigente): AUSENTE
cobertura: PARCIAL
lacuna_exata: >
  03_FLUXOS contém a regra completa e normativa. 04_MINUTAS a captura
  parcialmente via campo "nova_semantica". 02_CONTRATO_GERENTE e
  06_MINUTAS_QA não a enunciam.
alteracao_documental_ainda_necessaria: >
  Dependendo da interpretação: 03_FLUXOS é a autoridade operacional e
  contém a regra completa. Requer decisão do usuário sobre se é necessário
  repetir nos demais arquivos.
```

---

## 10. Matriz obrigatória

| ID | Item | Planejamento localizado | Regra/decisão localizada | ADR/contrato | Handoff | Implementação | QA | Validação | Commit | Estado material | Pendência real | Evidências |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2.1.1 | Navegação entre itens do console | Não | Sim (contrato §7) | Parcial (ADR-0005) | Não | Não | Não | Não | Não | DOCUMENTADO_NAO_IMPLEMENTADO | Handoff futuro | contrato_console.md §7, §18; H-0037 §26 |
| 2.1.2 | Seleção de itens do console | Não | Sim (contrato §8) | Não | Não | Não | Não | Não | Não | DOCUMENTADO_NAO_IMPLEMENTADO | Handoff futuro | contrato_console.md §8, §18; H-0036 §12.2 |
| 2.1.3 | Execução simulada de ações | Não | Sim (contrato §9) | Parcial (ADR-0016) | Não | Não | Não | Não | Não | DOCUMENTADO_NAO_IMPLEMENTADO | Handoff futuro (DOC-B009) | contrato_console.md §9, §10, §18 |
| 2.1.4 | Exibição de conteúdo de JSON de testes | Não | Sim | ADR-0026, 0027, 0028 | H-0036, H-0037 | Sim | Sim | Sim | 9957efd, c90349c | CONCLUIDO_E_COMPROVADO | Nenhuma (nav/seleção excluídas) | IMP-0036, IMP-0037; commits comprovados |
| 2.2 | Cabeçalho com pouca largura | Não (backlog modelo) | Parcial (max_caracteres) | Não | Não | Não | Não | Não | Não | BLOCKED_USER_DECISION | Decisão: quebra vs reticências | LEVANTAMENTO_H-0030 §7; contrato_cabecalho |
| 2.3a | H-0025 existência e objetivo | Sim | Sim (ADR-0018) | ADR-0018 | H-0025 | IMP-0026 | I1_APPROVED | OBS-H0025-001 | 1cc0dff | CONCLUIDO_E_COMPROVADO | Nenhuma | VERIF_FECHAMENTO_H-0025 |
| 2.3b | H-0026 existência e objetivo | Sim | Sim (ADR-0015, 0018) | ADR-0015, 0018 | H-0026 | IMP-0027 | Sim | NAO_CONFIRMADA | 40015b6 | CONCLUIDO_E_COMPROVADO | Nenhuma | H-0026 §7.1; git log |
| 2.4 | Compatibilidade da suíte com pytest | Sim (H-0028 introduziu) | Não (sem decisão) | Não | Não | Não | Não | Não | Não | OPCIONAL_NAO_INICIADO | Decisão do usuário | RELATORIO_ORIGEM_ERROS_PYTEST_LEGADO.md |
| 2.5.R1 | Regra: separar limitações do autor | Sim (revisão 2026-07-20) | Sim (versão 20260720) | Não | Não | Não | Não | Não | Não | PARCIALMENTE_REALIZADO | Propagação explícita nos vigentes | 04_MINUTAS vigente sem texto explícito |
| 2.5.R2 | Regra: não criar proibições inexequíveis | Sim (revisão 2026-07-20) | Sim (versão 20260720) | Não | Não | Não | Não | Não | Não | PARCIALMENTE_REALIZADO | Propagação explícita nos vigentes | 04_MINUTAS linha 94 parcial |
| 2.5.R3 | Regra: permitir exceção focal (5 condições) | Sim (revisão 2026-07-20) | Sim | Não | Não | Não | Não | Não | Não | PARCIALMENTE_REALIZADO | Completar em 04_MINUTAS e 06_MINUTAS | 03_FLUXOS §7.1 completo; 04_MINUTAS parcial |
| 2.5.R4 | Regra: limitar exceção (arquitetura/schema) | Sim (revisão 2026-07-20) | Sim | Não | Não | Não | Não | Não | Não | PARCIALMENTE_REALIZADO | Propagar em 02_CONTRATO e 06_MINUTAS | 03_FLUXOS §7.1 completo; demais ausentes |

---

## 11. Reconciliação com o LEVANTAMENTO_REVISOES_H-0030.md

### 11.1 Conclusões ainda válidas

- **Ponto 1 (quebra de descrição)**: ainda válido. Nenhuma decisão foi tomada.
  Autoridade normativa ausente. Implementação atual corta por largura sem
  quebra nem reticências. Classificação `REGRA_AUSENTE` permanece.

- **Ponto 2 (reticências)**: ainda válido. A decisão normativa sobre reticências
  por overflow horizontal permanece ausente. Classificação
  `BLOCKED_USER_DECISION` permanece.

### 11.2 Conclusões superadas por ciclos posteriores

- **Ponto 3 (lançador em fila/matriz)**: O levantamento identificou que a
  implementação renderizava um item por linha sem calcular fila/matriz. O
  **H-0034** (`be9612a feat: implementa distribuicao responsiva do lancador`)
  implementou materialmente a distribuição responsiva do lançador. Esta
  conclusão foi **superada** pelo H-0034.

- **Pontos 4 e 5 (espaço em destino_minimo e grupo_minimo)**: Conclusão
  `NENHUMA_ACAO_NECESSARIA` permanece válida. O preenchimento externo do corpo
  foi atribuído corretamente ao comportamento normativo (ADR-0013, H-0015).
  Nenhum ciclo posterior alterou esse comportamento.

### 11.3 Itens que permanecem bloqueados

- Pontos 1 e 2 do levantamento (cabeçalho) — aguardam decisão do usuário.

### 11.4 Fatos que o relatório tratou como NAO_CONFIRMADO

- "dashboard TESTE em grupo_minimo = NAO_CONFIRMADO": o dashboard real em
  `grupo_minimo` é `Conteudo`, não `Teste`. Não foi alterado por nenhum ciclo
  posterior.

### 11.5 Divergências factuais

Nenhuma divergência factual foi encontrada entre as conclusões do
`LEVANTAMENTO_REVISOES_H-0030.md` e o estado atual verificável, exceto pelo
ponto 3 (lançador), que foi resolvido pelo H-0034 após a data do levantamento.

---

## 12. Conclusão esperada

```yaml
itens_concluidos:
  - 2.1.4: exibição de conteúdo de JSON de testes (H-0036 + H-0037)
  - 2.3a: H-0025 (implementação e commit comprovados)
  - 2.3b: H-0026 (implementação e commit comprovados)

itens_parcialmente_realizados:
  - 2.5.R1: regra separação autor/executor (presente em 20260720, ausente explicitamente nos vigentes)
  - 2.5.R2: regra exequibilidade do handoff (parcial em 04_MINUTAS vigente)
  - 2.5.R3: exceção focal com 5 condições (completa em 03_FLUXOS, parcial em 04_MINUTAS)
  - 2.5.R4: limite da exceção (completa em 03_FLUXOS, ausente em 02_CONTRATO e 06_MINUTAS)

itens_planejados_nao_iniciados:
  - 2.1.1: navegação entre itens (contratado, não implementado)
  - 2.1.2: seleção de itens (contratado, não implementado)
  - 2.1.3: execução simulada de ações (contratado, não implementado; DOC-B009 pendente)

itens_bloqueados_por_decisao:
  - 2.2: descrição do cabeçalho com pouca largura (BLOCKED_USER_DECISION)

itens_opcionais:
  - 2.4: compatibilidade da suíte legada com pytest (OPCIONAL_NAO_INICIADO)

itens_nao_confirmados:
  - Validação manual formal do H-0026: RELATORIO_VERIFICACAO_FECHAMENTO_H-0026
    existe mas não foi lido integralmente; o commit foi confirmado por git log.
  - Número atual de erros de coleta do pytest no estado HEAD 23f49d0: não
    verificado neste levantamento (apenas o estado do versao_0_1 foi documentado
    no RELATORIO_ORIGEM_ERROS_PYTEST_LEGADO).
  - Se a suíte canônica atual é formalmente 6 ou 10 scripts: a documentação
    histórica diz 6; o estado atual tem 10; não foi encontrado relatório que
    redefina formalmente o número canônico.

tarefas_documentais_ainda_necessarias:
  - Propagação explícita da Regra 1 (separação autor/executor) nos vigentes
    02_CONTRATO_GERENTE.md e 04_MINUTAS_HANDOFF_IMPLEMENTACAO.md.
  - Propagação explícita da Regra 2 (inexequibilidade) nos quatro arquivos.
  - Completar Regra 3 em 04_MINUTAS (adicionar "registrar no relatório").
  - Propagar Regra 4 em 02_CONTRATO_GERENTE e 06_MINUTAS_QA_PATCH_FECHAMENTO.
  - Redefinir formalmente a suíte canônica atual (6 ou mais scripts) após
    os ciclos H-0035, H-0036 e H-0037.
  - Decisão normativa sobre o comportamento do cabeçalho com pouca largura
    (quebra vs reticências), para que ADR possa ser criada.

tarefas_documentais_ja_propagadas:
  - Regra 3 e Regra 4 estão completamente presentes em 03_FLUXOS_E_CLASSIFICACAO.md.
  - Exceção operacional está presente como cláusula nos handoffs H-0032 a H-0037
    (handoffs do repositório Git, não do sistema de prompts).
  - Mapa de leitura do 00_INDICE_PROMPTS.md aponta para títulos corretos.

proximas_decisoes_do_usuario:
  - Escolher entre quebra em até duas linhas ou reticências para a descrição
    do cabeçalho com pouca largura (DECISAO_FOCAL → CRIAR_ADR).
  - Decidir se o ciclo de compatibilidade pytest deve ser aberto
    (AGUARDAR_DECISAO_DO_USUARIO).
  - Decidir se as Regras 1 e 2 devem ser explicitamente re-propagadas nos
    arquivos do sistema de prompts após a reconstrução de 2026-07-21
    (AGUARDAR_DECISAO_DO_USUARIO).
  - Definir formalmente o número canônico de scripts da suíte de testes
    após H-0035, H-0036, H-0037 (DECISAO_FOCAL).

proxima_etapa_permitida:
  - item_2.2_cabecalho: DECISAO_FOCAL (definir comportamento) → CRIAR_ADR
  - item_2.1.1_navegacao: AGUARDAR_DECISAO_DO_USUARIO (abrir handoff?)
  - item_2.1.2_selecao: AGUARDAR_DECISAO_DO_USUARIO (abrir handoff?)
  - item_2.1.3_execucao_simulada: AGUARDAR_DECISAO_DO_USUARIO (DOC-B009)
  - item_2.4_pytest: AGUARDAR_DECISAO_DO_USUARIO
  - item_2.5_regras_prompts: AGUARDAR_DECISAO_DO_USUARIO (re-propagar ou não)
  - suite_canonica_numero: DECISAO_FOCAL (formalizar contagem atual)

estado_git_observado:
  branch: master
  HEAD: 23f49d0
  stage: vazio
  workspace: COM_ARQUIVOS_NAO_RASTREADOS
  arquivos_nao_rastreados:
    - docs/relatorios/RELATORIO_LEVANTAMENTO_PENDENCIAS_CONSOLE_PROCESSO_E_PROMPTS.md

stage_observado: vazio
```

---

LEVANTAMENTO_CONCLUIDO
