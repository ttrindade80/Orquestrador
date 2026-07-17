---
name: H-0036-fornecimento-externo-dados-console-json-multinivel
description: Implementação do recebimento de conteúdo externo multinível no console — carregamento separado pelo demo.py, 20 validações semânticas, modelo, três apresentações, demonstração real pelo ponto de entrada existente e revisão dos JSONs do H-0035 afetados
metadata:
  type: handoff_implementacao
  status: CORRIGIDO_AGUARDANDO_QA
  id: H-0036
  data_criacao: "2026-07-17"
  data_correcao: "2026-07-17"
rastreabilidade:
  adr_principal: docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
  adr_corretiva: docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
  contratos_aplicados:
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_json_console.md
  relatorios_autoridade:
    - docs/relatorios/RELATORIO_QA_ADR-0026.md
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md
    - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0026.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0026.md
    - docs/relatorios/RELATORIO_QA_ADR-0027.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0027.md
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0027.md
    - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0027.md
    - docs/relatorios/RELATORIO_QA_H-0036_HANDOFF.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_H-0036_HANDOFF.md
  handoffs_anteriores:
    - docs/handoff/H-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
---

# H-0036 — Fornecimento externo de dados ao console por JSON multinível

## 1. Identificação

| Campo | Valor |
|---|---|
| Handoff | H-0036 |
| Título | Fornecimento externo de dados ao console por JSON multinível |
| ADR base | ADR-0026 (`aceita e aplicada`, 2026-07-17) |
| ADR corretiva | ADR-0027 (`aceita e aplicada`, 2026-07-17) |
| Arquivo | `docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md` |
| Data de criação | 2026-07-17 |
| Data de correção | 2026-07-17 |
| Ciclo anterior fechado | H-0035 / ADR-0025 / commit `fb9e5be` |

---

## 2. Estado comprovado

```yaml
ultimo_ciclo_concluido:
  handoff: H-0035
  titulo: distribuicao matricial configuravel de nivel unico do conteudo dos elementos
  adr: ADR-0025
  commit: fb9e5be
  branch: master
  status: CONCLUIDO

ciclo_documental_adr_0026:
  adr: ADR-0026
  status_adr: aceita e aplicada
  qa_adr: ADR_APPROVED
  aplicacao: APLICACAO_CONCLUIDA
  qa_aplicacao: ADR_APPLICATION_APPROVED_WITH_NOTES
  achados_bloqueantes: 0

ciclo_documental_adr_0027:
  adr: ADR-0027
  status_adr: aceita e aplicada
  qa_adr_inicial: ARCHITECTURE_REVIEW_REQUIRED (QAADR-0027-001: schema de dados[] ausente)
  patch_adr: CONCLUIDO
  qa_adr_pos_patch: ADR_APPROVED
  aplicacao: APLICACAO_CONCLUIDA
  qa_aplicacao: ADR_APPLICATION_APPROVED_WITH_NOTES
  achados_bloqueantes: 0

qa_handoff_inicial:
  relatorio: docs/relatorios/RELATORIO_QA_H-0036_HANDOFF.md
  status: H3_BLOCKED_DOCUMENTATION
  achados_bloqueantes: 3
  achado_001: mecanismo de entrega sem autoridade normativa ativa
  achado_002: config/conteudo/ como convencao global sem autoridade
  achado_003: schema de dados[] e validacoes deixados para implementacao

resolucao_dos_achados:
  QAH-0036-001: resolvido pela ADR-0027 (D2, D3, D7, D8; contratos §20, §32)
  QAH-0036-002: resolvido pela ADR-0027 (D6, §7.4; contrato_json_console §12.8)
  QAH-0036-003: resolvido pela ADR-0027 (D11, D13; contrato_json_console §12)

primeiro_patch_handoff:
  status: CORRIGIDO_AGUARDANDO_QA
  qa_pos_primeiro_patch: H2_HANDOFF_PATCH_REQUIRED
  qa_de_origem: docs/relatorios/RELATORIO_QA_H-0036_HANDOFF.md

segundo_patch_handoff:
  status: CORRIGIDO_AGUARDANDO_QA
  qa_de_origem: docs/relatorios/RELATORIO_QA_POS_PATCH_H-0036_HANDOFF.md
  classificacao_de_origem: H2_HANDOFF_PATCH_REQUIRED
  achados_corrigidos:
    - QAHPP-0036-001
    - QAHPP-0036-002
  qa_pos_segundo_patch: NAO_REALIZADO

git_antes_da_criacao_deste_handoff:
  branch: master
  head: fb9e5be
  workspace: sujo_acumulado_adr_0026_adr_0027 (nao commitado)
  stage: vazio
  commit_novo: nao_realizado
  git_diff_check: sem_erros
```

---

## 3. Autoridades

Documentos lidos integralmente como base normativa deste handoff:

```text
docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
docs/relatorios/RELATORIO_QA_ADR-0026.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0026.md
docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0026.md
docs/relatorios/RELATORIO_QA_ADR-0027.md
docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0027.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0027.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0027.md
docs/relatorios/RELATORIO_QA_H-0036_HANDOFF.md
docs/NOMENCLATURA.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_console.md
docs/contratos/contrato_json_console.md
docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
docs/handoff/H-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
docs/relatorios/IMP-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
```

Autoridade final para nomes, semântica e fronteiras: ADR-0026, ADR-0027 e os
contratos ativos listados acima. O handoff inicial reprovado (`H3_BLOCKED_DOCUMENTATION`)
não é autoridade normativa superior à ADR-0027 aplicada.

---

## 4. Contexto

### 4.1 Ciclo anterior

O H-0035 (ADR-0025) implementou a distribuição matricial configurável de nível único
do conteúdo dos elementos. O ciclo produziu 26 configurações permanentes `h0035_*.json`
em `config/telas/demo/`. A ADR-0025 preservou o papel do renderizador no cálculo de
geometria e excluiu a composição multinível do seu escopo.

### 4.2 ADR-0026: separação estrutura-conteúdo

A ADR-0026 (`aceita e aplicada`) formalizou a separação entre:

- **configuração estrutural da tela** (`tela.json`): composição e configuração da
  interface, sem dados de runtime do console;
- **documento externo de conteúdo**: dados de runtime fornecidos externamente ao
  console por JSON declarativo com envelope `{tipo, formato, dados}`;
- **resultado calculado**: representação física produzida exclusivamente pelo
  renderizador.

### 4.3 Bloqueio documental e ADR-0027

O QA do handoff original (`H3_BLOCKED_DOCUMENTATION`) identificou três lacunas:

1. o mecanismo de entrega do documento ao console não tinha autoridade normativa;
2. a localização `config/conteudo/` foi introduzida como convenção global sem
   autoridade;
3. o schema de `dados[]` e as validações foram deixados para decisão da
   implementação via exceção operacional.

A ADR-0027 (`aceita e aplicada`) resolveu as três lacunas:

- **D2, D3, D7, D8**: `demo/demo.py` é responsável por carregar os dois documentos
  separadamente e associá-los por cenário, sem campo de vínculo no JSON estrutural;
- **D6, §7.4**: as fixtures seguem a organização existente do repositório, sem
  diretório global definitivo de runtime;
- **D11, D13**: schema semântico multinível e 20 validações mínimas são decididos
  e obrigatórios.

### 4.4 Inspeção dos JSONs do H-0035

A inspeção confirmou que, dos 26 arquivos `h0035_*.json`, somente dois contêm
campo `itens` com conteúdo de runtime no elemento console:

- `config/telas/demo/h0035_console_com.json` — 12 itens (`"P01 linha"` a `"P12 linha"`)
  com configuração `distribuicao_matricial`;
- `config/telas/demo/h0035_console_sem.json` — 2 itens (`"Linha alfa"`, `"Linha bravo"`)
  sem `distribuicao_matricial`.

Os demais 24 arquivos não possuem elemento console com conteúdo de runtime e
permanecem intactos.

### 4.5 Estado atual do renderizador

A função `_linhas_console` em `tela/renderizador.py` retorna atualmente apenas:

```python
return [_PLACEHOLDER_CONSOLE]  # "(console)"
```

O H-0036 substitui esse comportamento para exibir conteúdo real recebido do
documento externo, preservando o placeholder quando não houver conteúdo externo.

### 4.6 Relação com o produtor final

No orquestrador final, um script produzirá o documento externo buscando dados no
projeto Pipeline. O protocolo concreto permanece para decisão futura. Este handoff
prepara a fronteira de consumo, não o produtor final.

---

## 5. Objetivo

Implementar, como capacidade coesa e única, o recebimento e exibição de conteúdo
externo multinível no console:

1. o ponto de entrada `demo/demo.py` carrega separadamente o JSON estrutural e o
   JSON externo de conteúdo para cada cenário aplicável;
2. o loader valida o documento externo segundo as 20 validações semânticas e o
   schema da ADR-0027 D11/D13;
3. o modelo representa o conteúdo semanticamente, preservando origens separadas;
4. o renderizador exibe as três apresentações (`tabela`, `hierarquia`,
   `conjuntos_campos`) a partir do modelo, sem abrir arquivos;
5. as fixtures são permanentes, nominalmente definidas, organizadas na estrutura
   existente do repositório;
6. os JSONs do H-0035 materialmente afetados são revisados: conteúdo removido do
   estrutural, JSON externo correspondente criado;
7. testes, smoke tests e demonstração manual cobrem as três apresentações e os
   cenários sem conteúdo externo.

---

## 6. Capacidade coesa e fluxo obrigatório

```text
JSON estrutural da tela ─┐
                          ├─> demo/demo.py (carregamento e associação por cenário)
JSON externo de conteúdo ┘
                                   ↓
                     loader ou camada equivalente (leitura e 20 validações)
                                   ↓
                          modelo (conteúdo semântico, origens preservadas)
                                   ↓
                               renderizador
                                   ↓
                       representação física na área do console
```

Regras invioláveis do fluxo:

- o ponto de entrada abre os dois arquivos e os entrega separadamente;
- o loader lê, decodifica e valida;
- o modelo transporta o conteúdo sem lógica geométrica;
- o renderizador produz a representação física;
- o renderizador **não** abre arquivos;
- o modelo **não** escolhe qual arquivo carregar;
- o conteúdo **não** é reinserido no objeto bruto do JSON estrutural.

---

## 7. Base de caminhos

Raiz operacional = raiz Git do projeto. Todos os caminhos são relativos à raiz:

```text
config/
demo/
docs/
tela/
```

Não usar prefixo `scripts/`. Não prefixar com o nome do projeto.

---

## 8. Decisões fechadas (não reabrir)

| ID | Decisão | Autoridade |
|---|---|---|
| D-ADR26-1 | Conteúdo de runtime do console tem origem externa | ADR-0026 D1; `contrato_console.md` §19.1 |
| D-ADR26-2 | JSON estrutural da tela NÃO contém dados de runtime | ADR-0026 D2; `contrato_tela_json.md` §31.1 |
| D-ADR26-3 | Console recebe dados por JSON externo com envelope `{tipo, formato, dados}` | ADR-0026 D3–D4; `contrato_json_console.md` §11.1–11.2 |
| D-ADR26-5 | Formato inicial: `tipo: "multinivel"` | ADR-0026 D5; `contrato_json_console.md` §11.3 |
| D-ADR26-6 | Bloco `formato` descreve intenção de apresentação, não resultados calculados | ADR-0026 D6; `contrato_json_console.md` §11.2 |
| D-ADR26-7 | Bloco `dados` contém estrutura semântica com níveis explícitos | ADR-0026 D7–D8; `contrato_json_console.md` §11.2–11.3 |
| D-ADR26-9 | Dados chegam previamente estruturados; consumidor NÃO reconstrói hierarquia | ADR-0026 D9–D10; `contrato_console.md` §19.2–19.3 |
| D-ADR26-11 | Renderizador mantém responsabilidade exclusiva sobre representação física | ADR-0026 D11; `contrato_console.md` §19.4; `contrato_json_console.md` §11.4 |
| D-ADR27-1 | Dois documentos separados; JSON estrutural não volta a conter runtime | ADR-0027 D1, D4, D8 |
| D-ADR27-2 | `demo/demo.py` é responsável por carregar os dois documentos e associá-los | ADR-0027 D2, D3, D8; `contrato_console.md` §20.1; `contrato_tela_json.md` §32.2 |
| D-ADR27-3 | A demonstração integrada ocorre por `demo/demo.py`; demo auxiliar não é prova única | ADR-0027 D3, §8 |
| D-ADR27-5 | JSONs do H-0035 materialmente afetados são revisados pelo H-0036 | ADR-0027 D5, §7.3; `contrato_tela_json.md` §32.5 |
| D-ADR27-6 | Fixtures seguem a organização existente; sem diretório global definitivo | ADR-0027 D6, §7.4; `contrato_json_console.md` §12.8 |
| D-ADR27-7 | Associação no catálogo do `demo.py`; sem campo de vínculo no JSON estrutural | ADR-0027 D7; `contrato_tela_json.md` §32.1 |
| D-ADR27-11 | Schema semântico multinível decidido e obrigatório (D11.1–D11.6 da ADR-0027) | ADR-0027 D11, D13; `contrato_json_console.md` §12 |
| — | Documento externo NÃO contém resultados físicos calculados | `NOMENCLATURA.md` §17.2; `contrato_json_console.md` §12.6 |
| — | `tipo: "matriz"` NÃO incluído nesta implementação | ADR-0026 §9; `contrato_json_console.md` §11.8 |
| — | ADR-0025 e H-0035 preservados integralmente | ADR-0026 §10 |

O executor não decide nenhum desses itens. Se a implementação exigir decidir
semântica não fechada, aplicar as condições de bloqueio (§24).

---

## 9. Decisões deferidas (não implementar sem autoridade)

As seguintes decisões permanecem para ciclos futuros:

| Item deferido | Fonte normativa |
|---|---|
| Forma de vínculo entre `tela.json` e documento externo no produto final | `contrato_tela_json.md` §31.3; ADR-0027 §14 |
| Nome de variável, classe, função, dicionário, assinatura, argumento de linha de comando do mecanismo de associação no `demo.py` | ADR-0027 D7, §14 |
| APIs e classes definitivas do consumidor/loader | ADR-0026 §14; ADR-0027 §14 |
| Protocolo do script produtor futuro (nome, localização, execução, argumentos, transporte, códigos de saída, timeout, autenticação) | ADR-0027 §9.3, §14 |
| Diretório global definitivo de dados de runtime do produto | ADR-0027 §14 |
| Comportamento diante de fonte ausente ou inválida além do documentado | ADR-0027 §14; `contrato_json_console.md` §11.8 |
| Suporte a `tipo: "matriz"` | ADR-0026 §9; ADR-0027 §14 |
| Navegação, seleção, expansão, recolhimento, paginação interativa | `contrato_console.md` §19.7 |
| Cache, atualização automática, persistência, versionamento, autenticação | ADR-0026 §14; ADR-0027 §14 |

---

## 10. Fronteiras de responsabilidade

| Componente | Responsabilidade neste handoff | Fora de responsabilidade |
|---|---|---|
| Ponto de entrada (`demo/demo.py`) | Identificar cenário; carregar JSON estrutural; carregar JSON externo quando aplicável; associar por cenário; entregar entradas separadas ao fluxo | Calcular geometria; escolher apresentação da tela |
| Documento externo (fixture) | Transportar `tipo`, intenção de apresentação, níveis declarados e dados semânticos | Resultados físicos calculados; configuração estrutural da tela |
| Loader (`tela/loader.py`) | Ler e decodificar o arquivo; executar as 20 validações semânticas; produzir representação interna | Vincular `tela.json` ao documento externo; abrir o JSON estrutural (responsabilidade do `demo.py`) |
| Modelo (`tela/modelo.py`) | Transportar conteúdo multinível; preservar origens separadas e ordem semântica | Calcular geometria; abrir arquivos; escolher fonte |
| Renderizador (`tela/renderizador.py`) | Exibir conteúdo recebido do modelo nas três apresentações; preservar placeholder quando ausente; calcular geometria e designadores | Abrir arquivos; receber entrada raw (JSON bruto) |
| JSON estrutural da tela | Declarar configuração estrutural da interface | Conter conteúdo de runtime; conter campo de vínculo |
| Demo e testes | Carregar documentos separadamente; provar identidade semântica | Definir mecanismo de vínculo do produto |

---

## 11. Inventário de inspeção dos JSONs do H-0035

Inspecionados nominalmente todos os 26 arquivos `h0035_*.json` em
`config/telas/demo/`. Classificação completa:

```yaml
inventario_H0035:
  - arquivo: config/telas/demo/h0035_catalogo.json
    possui_console: false
    possui_conteudo_de_runtime_do_console: false
    materialmente_afetado_pela_ADR0027: false
    classificacao: PRESERVAR_SEM_ALTERACAO
    acao_no_H0036: nenhuma
    json_externo_correspondente: NENHUM
    justificativa: >
      É o catálogo de cenários da demonstração; contém elemento lancador com
      25 entradas de navegação; não possui elemento console nem conteúdo de
      runtime do console; não participa da separação estrutural-conteúdo do
      H-0036.

  - arquivo: config/telas/demo/h0035_centralizado_h_colunas.json
    possui_console: false
    possui_conteudo_de_runtime_do_console: false
    materialmente_afetado_pela_ADR0027: false
    classificacao: PRESERVAR_SEM_ALTERACAO
    acao_no_H0036: nenhuma
    json_externo_correspondente: NENHUM
    justificativa: >
      Contém elemento dashboard com configuração de centralização horizontal em
      colunas; não possui elemento console nem conteúdo de runtime do console.

  - arquivo: config/telas/demo/h0035_console_com.json
    possui_console: true
    possui_conteudo_de_runtime_do_console: true
    materialmente_afetado_pela_ADR0027: true
    classificacao: ALTERAR_E_SEPARAR
    acao_no_H0036: >
      Remover o conteúdo de runtime do JSON estrutural, preservando a configuração
      da tela e a distribuição matricial; criar e associar o JSON externo
      correspondente.
    json_externo_correspondente: config/telas/demo/h0035_console_com_conteudo.json
    justificativa: >
      O arquivo contém elemento console com 12 itens de runtime (P01 linha a
      P12 linha) e configuração distribuicao_matricial que deve ser preservada
      após a separação; é materialmente afetado pela separação
      estrutural-conteúdo exigida pela ADR-0027 D5.

  - arquivo: config/telas/demo/h0035_console_sem.json
    possui_console: true
    possui_conteudo_de_runtime_do_console: true
    materialmente_afetado_pela_ADR0027: true
    classificacao: ALTERAR_E_SEPARAR
    acao_no_H0036: >
      Remover o conteúdo de runtime do JSON estrutural, preservando a configuração
      da tela; criar e associar o JSON externo correspondente.
    json_externo_correspondente: config/telas/demo/h0035_console_sem_conteudo.json
    justificativa: >
      O arquivo contém elemento console com 2 itens de runtime (Linha alfa,
      Linha bravo) sem distribuicao_matricial; representa o cenário histórico
      sem distribuição matricial e é materialmente afetado pela separação
      estrutural-conteúdo exigida pela ADR-0027 D5.

  - arquivo: config/telas/demo/h0035_dashboard_com.json
    possui_console: false
    possui_conteudo_de_runtime_do_console: false
    materialmente_afetado_pela_ADR0027: false
    classificacao: PRESERVAR_SEM_ALTERACAO
    acao_no_H0036: nenhuma
    json_externo_correspondente: NENHUM
    justificativa: >
      Contém elemento dashboard com distribuição matricial configurada; não
      possui elemento console nem conteúdo de runtime do console.

  - arquivo: config/telas/demo/h0035_dashboard_sem.json
    possui_console: false
    possui_conteudo_de_runtime_do_console: false
    materialmente_afetado_pela_ADR0027: false
    classificacao: PRESERVAR_SEM_ALTERACAO
    acao_no_H0036: nenhuma
    json_externo_correspondente: NENHUM
    justificativa: >
      Contém elemento dashboard sem distribuição matricial configurada; não
      possui elemento console nem conteúdo de runtime do console.

  - arquivo: config/telas/demo/h0035_esquerda_margens_min_max.json
    possui_console: false
    possui_conteudo_de_runtime_do_console: false
    materialmente_afetado_pela_ADR0027: false
    classificacao: PRESERVAR_SEM_ALTERACAO
    acao_no_H0036: nenhuma
    json_externo_correspondente: NENHUM
    justificativa: >
      Contém elemento dashboard com configuração de margens esquerda mínima e
      máxima na distribuição matricial; não possui elemento console nem
      conteúdo de runtime do console.

  - arquivo: config/telas/demo/h0035_h_margens_limitadas.json
    possui_console: false
    possui_conteudo_de_runtime_do_console: false
    materialmente_afetado_pela_ADR0027: false
    classificacao: PRESERVAR_SEM_ALTERACAO
    acao_no_H0036: nenhuma
    json_externo_correspondente: NENHUM
    justificativa: >
      Contém elemento dashboard com configuração de margens horizontais limitadas;
      não possui elemento console nem conteúdo de runtime do console.

  - arquivo: config/telas/demo/h0035_h_uniforme.json
    possui_console: false
    possui_conteudo_de_runtime_do_console: false
    materialmente_afetado_pela_ADR0027: false
    classificacao: PRESERVAR_SEM_ALTERACAO
    acao_no_H0036: nenhuma
    json_externo_correspondente: NENHUM
    justificativa: >
      Contém elemento dashboard com configuração de distribuição horizontal
      uniforme; não possui elemento console nem conteúdo de runtime do console.

  - arquivo: config/telas/demo/h0035_lancador_com.json
    possui_console: false
    possui_conteudo_de_runtime_do_console: false
    materialmente_afetado_pela_ADR0027: false
    classificacao: PRESERVAR_SEM_ALTERACAO
    acao_no_H0036: nenhuma
    json_externo_correspondente: NENHUM
    justificativa: >
      Contém elemento lancador com 12 itens de navegação; não possui elemento
      console; os itens pertencem ao lancador, não ao mecanismo de fornecimento
      externo do console; não participa da separação estrutural-conteúdo.

  - arquivo: config/telas/demo/h0035_lancador_sem.json
    possui_console: false
    possui_conteudo_de_runtime_do_console: false
    materialmente_afetado_pela_ADR0027: false
    classificacao: PRESERVAR_SEM_ALTERACAO
    acao_no_H0036: nenhuma
    json_externo_correspondente: NENHUM
    justificativa: >
      Contém elemento lancador com 3 itens de navegação; não possui elemento
      console; os itens pertencem ao lancador, não ao mecanismo de fornecimento
      externo do console; não participa da separação estrutural-conteúdo.

  - arquivo: config/telas/demo/h0035_matriz_fixa_cabe.json
    possui_console: false
    possui_conteudo_de_runtime_do_console: false
    materialmente_afetado_pela_ADR0027: false
    classificacao: PRESERVAR_SEM_ALTERACAO
    acao_no_H0036: nenhuma
    json_externo_correspondente: NENHUM
    justificativa: >
      Contém elemento dashboard com configuração de matriz fixa dentro do espaço
      disponível; não possui elemento console nem conteúdo de runtime do console.

  - arquivo: config/telas/demo/h0035_matriz_fixa_quadro_minimo.json
    possui_console: false
    possui_conteudo_de_runtime_do_console: false
    materialmente_afetado_pela_ADR0027: false
    classificacao: PRESERVAR_SEM_ALTERACAO
    acao_no_H0036: nenhuma
    json_externo_correspondente: NENHUM
    justificativa: >
      Contém elemento dashboard com configuração de matriz fixa no quadro
      mínimo; não possui elemento console nem conteúdo de runtime do console.

  - arquivo: config/telas/demo/h0035_minimo_fixo_excedido.json
    possui_console: false
    possui_conteudo_de_runtime_do_console: false
    materialmente_afetado_pela_ADR0027: false
    classificacao: PRESERVAR_SEM_ALTERACAO
    acao_no_H0036: nenhuma
    json_externo_correspondente: NENHUM
    justificativa: >
      Contém elemento dashboard com configuração de mínimo fixo excedido pelo
      espaço disponível; não possui elemento console nem conteúdo de runtime
      do console.

  - arquivo: config/telas/demo/h0035_pref_colunas.json
    possui_console: false
    possui_conteudo_de_runtime_do_console: false
    materialmente_afetado_pela_ADR0027: false
    classificacao: PRESERVAR_SEM_ALTERACAO
    acao_no_H0036: nenhuma
    json_externo_correspondente: NENHUM
    justificativa: >
      Contém elemento dashboard com configuração de preferência de colunas na
      distribuição matricial; não possui elemento console nem conteúdo de
      runtime do console.

  - arquivo: config/telas/demo/h0035_pref_linhas.json
    possui_console: false
    possui_conteudo_de_runtime_do_console: false
    materialmente_afetado_pela_ADR0027: false
    classificacao: PRESERVAR_SEM_ALTERACAO
    acao_no_H0036: nenhuma
    json_externo_correspondente: NENHUM
    justificativa: >
      Contém elemento dashboard com configuração de preferência de linhas na
      distribuição matricial; não possui elemento console nem conteúdo de
      runtime do console.

  - arquivo: config/telas/demo/h0035_quatro_centralizados.json
    possui_console: false
    possui_conteudo_de_runtime_do_console: false
    materialmente_afetado_pela_ADR0027: false
    classificacao: PRESERVAR_SEM_ALTERACAO
    acao_no_H0036: nenhuma
    json_externo_correspondente: NENHUM
    justificativa: >
      Contém elemento dashboard com quatro elementos centralizados na grade
      matricial; não possui elemento console nem conteúdo de runtime do console.

  - arquivo: config/telas/demo/h0035_resto_horizontal.json
    possui_console: false
    possui_conteudo_de_runtime_do_console: false
    materialmente_afetado_pela_ADR0027: false
    classificacao: PRESERVAR_SEM_ALTERACAO
    acao_no_H0036: nenhuma
    json_externo_correspondente: NENHUM
    justificativa: >
      Contém elemento dashboard com configuração de distribuição do espaço
      restante horizontal; não possui elemento console nem conteúdo de runtime
      do console.

  - arquivo: config/telas/demo/h0035_resto_vertical.json
    possui_console: false
    possui_conteudo_de_runtime_do_console: false
    materialmente_afetado_pela_ADR0027: false
    classificacao: PRESERVAR_SEM_ALTERACAO
    acao_no_H0036: nenhuma
    json_externo_correspondente: NENHUM
    justificativa: >
      Contém elemento dashboard com configuração de distribuição do espaço
      restante vertical; não possui elemento console nem conteúdo de runtime
      do console.

  - arquivo: config/telas/demo/h0035_tres_centralizados.json
    possui_console: false
    possui_conteudo_de_runtime_do_console: false
    materialmente_afetado_pela_ADR0027: false
    classificacao: PRESERVAR_SEM_ALTERACAO
    acao_no_H0036: nenhuma
    json_externo_correspondente: NENHUM
    justificativa: >
      Contém elemento dashboard com três elementos centralizados na grade
      matricial; não possui elemento console nem conteúdo de runtime do console.

  - arquivo: config/telas/demo/h0035_uma_coluna.json
    possui_console: false
    possui_conteudo_de_runtime_do_console: false
    materialmente_afetado_pela_ADR0027: false
    classificacao: PRESERVAR_SEM_ALTERACAO
    acao_no_H0036: nenhuma
    json_externo_correspondente: NENHUM
    justificativa: >
      Contém elemento dashboard configurado em formação de uma coluna; não
      possui elemento console nem conteúdo de runtime do console.

  - arquivo: config/telas/demo/h0035_uma_linha.json
    possui_console: false
    possui_conteudo_de_runtime_do_console: false
    materialmente_afetado_pela_ADR0027: false
    classificacao: PRESERVAR_SEM_ALTERACAO
    acao_no_H0036: nenhuma
    json_externo_correspondente: NENHUM
    justificativa: >
      Contém elemento dashboard configurado em formação de uma linha; não
      possui elemento console nem conteúdo de runtime do console.

  - arquivo: config/telas/demo/h0035_um_centralizado.json
    possui_console: false
    possui_conteudo_de_runtime_do_console: false
    materialmente_afetado_pela_ADR0027: false
    classificacao: PRESERVAR_SEM_ALTERACAO
    acao_no_H0036: nenhuma
    json_externo_correspondente: NENHUM
    justificativa: >
      Contém elemento dashboard com um único elemento centralizado; não possui
      elemento console nem conteúdo de runtime do console.

  - arquivo: config/telas/demo/h0035_v_margens_min.json
    possui_console: false
    possui_conteudo_de_runtime_do_console: false
    materialmente_afetado_pela_ADR0027: false
    classificacao: PRESERVAR_SEM_ALTERACAO
    acao_no_H0036: nenhuma
    json_externo_correspondente: NENHUM
    justificativa: >
      Contém elemento dashboard com configuração de margem vertical mínima;
      não possui elemento console nem conteúdo de runtime do console.

  - arquivo: config/telas/demo/h0035_v_margens_min_max.json
    possui_console: false
    possui_conteudo_de_runtime_do_console: false
    materialmente_afetado_pela_ADR0027: false
    classificacao: PRESERVAR_SEM_ALTERACAO
    acao_no_H0036: nenhuma
    json_externo_correspondente: NENHUM
    justificativa: >
      Contém elemento dashboard com configuração de margens verticais mínima e
      máxima; não possui elemento console nem conteúdo de runtime do console.

  - arquivo: config/telas/demo/h0035_v_uniforme.json
    possui_console: false
    possui_conteudo_de_runtime_do_console: false
    materialmente_afetado_pela_ADR0027: false
    classificacao: PRESERVAR_SEM_ALTERACAO
    acao_no_H0036: nenhuma
    json_externo_correspondente: NENHUM
    justificativa: >
      Contém elemento dashboard com configuração de distribuição vertical
      uniforme; não possui elemento console nem conteúdo de runtime do console.

contagens_finais:
  total_inspecionado: 26
  ALTERAR_E_SEPARAR: 2
  PRESERVAR_SEM_ALTERACAO: 24
  NAO_APLICAVEL: 0
  jsons_externos_correspondentes:
    - config/telas/demo/h0035_console_com_conteudo.json
    - config/telas/demo/h0035_console_sem_conteudo.json
```

### 11.1 Ação obrigatória nos arquivos afetados

Para `config/telas/demo/h0035_console_com.json`:

- remover o campo `itens` do elemento console;
- preservar a configuração `distribuicao_matricial` e toda configuração estrutural;
- criar `config/telas/demo/h0035_console_com_conteudo.json` com os 12 itens
  convertidos para `tipo: "multinivel"` (apresentação `hierarquia`, nível único
  `tipo: "conteudo"`, designador `nenhum`);
- atualizar o catálogo do `demo.py` para associar o cenário `h0035_console_com`
  ao seu JSON externo correspondente;
- atualizar `demo/teste_demo_distribuicao.py` para carregar os dois arquivos
  separadamente no pipeline de testes;
- provar que o conteúdo não ficou duplicado.

Para `config/telas/demo/h0035_console_sem.json`:

- remover o campo `itens` do elemento console;
- preservar toda configuração estrutural restante;
- criar `config/telas/demo/h0035_console_sem_conteudo.json` com os 2 itens
  convertidos para `tipo: "multinivel"` (mesma forma que o arquivo acima);
- atualizar o catálogo do `demo.py`;
- atualizar testes que dependiam do conteúdo anterior;
- provar que o conteúdo não ficou duplicado.

A revisão desses arquivos não reabre nem invalida o fechamento do H-0035.
É uma adaptação autorizada pelo H-0036 conforme a ADR-0027 D5.

---

## 12. Localização das fixtures permanentes

### 12.1 Organização escolhida

Após inspecionar o repositório, todos os arquivos permanentes de fixtures e
configurações de demonstração estão em `config/telas/demo/`. Não existe diretório
separado de conteúdo. As novas fixtures externas permanentes do H-0036 seguem
a mesma organização, distinguindo-se dos JSONs estruturais pelo sufixo
`_conteudo.json`:

- JSONs estruturais: `config/telas/demo/h0036_console_*.json`
- JSONs externos de conteúdo: `config/telas/demo/h0036_*_conteudo.json`
- JSONs externos H-0035: `config/telas/demo/h0035_console_*_conteudo.json`

Essa localização:

- permanece dentro de `config/telas/demo/`, a única organização de fixtures e
  configurações de demo existente no repositório;
- distingue claramente JSON estrutural (sem sufixo `_conteudo`) de JSON de conteúdo
  (com sufixo `_conteudo`);
- é permanente e repetível sem dependência de convenção global de runtime;
- é adequada somente ao ciclo de teste e demonstração;
- não é apresentada como diretório global de runtime do produto;
- não confunde o documento de conteúdo com um `tela.json` (conteúdo não tem
  campo `schema: "tela.v1"`).

Esta escolha **não** cria `config/conteudo/` como convenção global definitiva.

### 12.2 Cenários e associações nominais

O catálogo do `demo.py` deve associar, para cada cenário com conteúdo externo:

| ID do cenário | JSON estrutural | JSON externo de conteúdo |
|---|---|---|
| `h0036_console_hierarquia` | `config/telas/demo/h0036_console_hierarquia.json` | `config/telas/demo/h0036_hierarquia_conteudo.json` |
| `h0036_console_tabela` | `config/telas/demo/h0036_console_tabela.json` | `config/telas/demo/h0036_tabela_conteudo.json` |
| `h0036_console_conjuntos` | `config/telas/demo/h0036_console_conjuntos.json` | `config/telas/demo/h0036_conjuntos_conteudo.json` |
| `h0035_console_com` | `config/telas/demo/h0035_console_com.json` | `config/telas/demo/h0035_console_com_conteudo.json` |
| `h0035_console_sem` | `config/telas/demo/h0035_console_sem.json` | `config/telas/demo/h0035_console_sem_conteudo.json` |

Cenários sem conteúdo externo (todos os demais `h0035_*` e demais telas) **não
possuem** JSON externo associado e preservam o placeholder ou comportamento
histórico. A ausência de associação deve ser representada explicitamente no catálogo
(não implícita, não herdada de outro cenário).

---

## 13. Schema semântico obrigatório

O schema está definido pela ADR-0027 D11 (D11.1–D11.6) e pelo
`contrato_json_console.md` §12. Não está deferido. O executor não pode escolher,
modificar ou excepcionar o schema via exceção operacional.

### 13.1 Envelope raiz

```json
{
  "tipo": "multinivel",
  "formato": {
    "apresentacao": "hierarquia",
    "niveis": []
  },
  "dados": []
}
```

Regras: raiz objeto; `tipo` obrigatório = `"multinivel"`; `formato` obrigatório e
objeto; `dados` obrigatório e array; `formato.apresentacao` obrigatório;
`formato.niveis` obrigatório e array.

### 13.2 Apresentações previstas

```text
tabela
hierarquia
conjuntos_campos
```

O H-0036 não pode ser reduzido silenciosamente a uma única apresentação. O
executor deve implementar e provar as três.

### 13.3 Tipos de nível

```text
container
conteudo
nome_valor
```

### 13.4 Campos da declaração de nível

```text
id           — string não vazia e única em formato.niveis
tipo         — do conjunto previsto
conteudo     — nome do campo semântico (container/conteudo) ou objeto {nome, valor} (nome_valor)
designador   — política declarativa
```

### 13.5 Campos comuns dos nós

```text
id           — obrigatório
nivel        — obrigatório; referencia id de nível declarado
```

### 13.6 Hierarquia por filhos

A hierarquia é declarada exclusivamente por `filhos` (array de nós filhos).
Não deve ser inferida por nome, posição, prefixo, ID, dado de domínio ou
convenção externa.

### 13.7 Designadores

O JSON declara a política; o renderizador calcula o marcador concreto.

Tipos previstos:

```text
nenhum  simbolo  decimal  alfabetico_minusculo  alfabetico_maiusculo
romano_minusculo  romano_maiusculo  decimal_composto  personalizado
```

O documento externo **não** armazena a numeração concreta já calculada.

### 13.8 Resultados físicos proibidos no documento externo

```text
largura efetiva              altura efetiva
quantidade física calculada  posição final
coordenada física final      página calculada
quebra física pronta         truncamento já aplicado
distribuição concreta        células vazias calculadas
geometria final              numeração concreta de designadores
```

---

## 14. Vinte validações semânticas obrigatórias

O loader ou camada equivalente deve implementar nominalmente estas 20 validações
(ADR-0027 D13; `contrato_json_console.md` §12.5):

1. raiz é objeto;
2. `tipo` presente e do tipo correto;
3. `tipo` igual a `"multinivel"`;
4. `formato` presente e objeto;
5. `dados` presente e array;
6. `formato.apresentacao` presente;
7. `formato.apresentacao` pertence ao conjunto previsto;
8. `formato.niveis` presente e array;
9. cada item de `formato.niveis` possui `id`, `tipo`, `conteudo` e `designador`;
10. IDs de nível não vazios e únicos em `formato.niveis`;
11. tipos de nível pertencem ao conjunto previsto;
12. cada nó em `dados` possui `id` e `nivel`;
13. `nivel` de cada nó referencia item declarado em `formato.niveis`;
14. nós de tipo `container` possuem campo semântico declarado e `filhos` como array;
15. nós de tipo `conteudo` possuem campo semântico declarado;
16. nós de tipo `nome_valor` possuem campos de nome e valor declarados;
17. filhos são validados recursivamente com as mesmas regras;
18. a ordem dos arrays é preservada pelo consumidor;
19. campos específicos da apresentação são compatíveis com `formato.apresentacao`;
20. o documento não contém resultados físicos calculados.

Use as classes de erro existentes no loader (`TelaErro`, `TelaEstruturaInvalida`
ou equivalentes) quando compatíveis. Não invente classes de erro ou mensagens
não exigidas pelos contratos.

---

## 15. Arquivos autorizados para a futura implementação

### 15.1 Tabela completa

| Arquivo | Estado atual | Ação | Responsabilidade | Critério que exige o arquivo |
|---|---|---|---|---|
| `tela/loader.py` | EXISTENTE | ALTERAR | Adicionar carregamento, decodificação e 20 validações do documento externo | D-ADR26-3; ADR-0027 D11, D13; `contrato_json_console.md` §12.5 |
| `tela/modelo.py` | EXISTENTE | ALTERAR | Adicionar representação interna do conteúdo multinível com origens separadas | ADR-0027 D8; `contrato_console.md` §20.3 |
| `tela/renderizador.py` | EXISTENTE | ALTERAR | Atualizar `_linhas_console` para exibir as três apresentações; preservar placeholder | ADR-0026 D11; ADR-0027 D8; `contrato_console.md` §20.4 |
| `tela/teste_loader.py` | EXISTENTE | ALTERAR | Adicionar testes das 20 validações, três apresentações, tipos de nível, recursão, designadores, ausência de geometria | ADR-0027 D13; §17.1 deste handoff |
| `tela/teste_modelo.py` | EXISTENTE | ALTERAR | Adicionar testes de entradas separadas, preservação de origens e ordem, níveis, pais e filhos | §17.2 deste handoff |
| `tela/teste_renderizador.py` | EXISTENTE | ALTERAR | Adicionar testes das três apresentações, designadores concretos, placeholder vs. conteúdo, ausência de abertura de arquivo | §17.3 deste handoff |
| `demo/demo.py` | EXISTENTE | ALTERAR | Adicionar catálogo/mecanismo de associação cenário → {JSON estrutural, JSON externo}; carregar os dois documentos separadamente | ADR-0027 D2, D7; `contrato_console.md` §20.1 |
| `demo/teste_demo.py` | EXISTENTE | ALTERAR | Atualizar para refletir catálogo e launcher alterados pelo H-0036 | Regressão da alteração do `demo.py` |
| `demo/teste_diagnostico.py` | EXISTENTE | ALTERAR | Adicionar testes do pipeline `carregar → carregar_externo → construir → renderizar` para cenários H-0036; atualizar referências ao h0035_console_com | §17.4 deste handoff; regressão |
| `demo/teste_demo_distribuicao.py` | EXISTENTE | ALTERAR | Atualizar para carregar os dois arquivos separadamente nos cenários `h0035_console_com` e `h0035_console_sem` | Regressão da revisão dos JSONs do H-0035 |
| `config/telas/demo/h0035_console_com.json` | EXISTENTE | ALTERAR | Remover campo `itens`; preservar `distribuicao_matricial` e estrutura restante | ADR-0027 D5; §11 deste handoff |
| `config/telas/demo/h0035_console_sem.json` | EXISTENTE | ALTERAR | Remover campo `itens`; preservar estrutura restante | ADR-0027 D5; §11 deste handoff |
| `config/telas/demo/demo.json` | EXISTENTE | ALTERAR | Adicionar entradas de launcher para os cenários H-0036, se o mecanismo de catálogo do `demo.py` exigir entradas no JSON estrutural | Navegação pelos cenários H-0036 via `demo.py` |
| `config/telas/demo/h0036_console_hierarquia.json` | NOVO | CRIAR | JSON estrutural da tela de console para cenário `hierarquia` | §12.2 deste handoff |
| `config/telas/demo/h0036_console_tabela.json` | NOVO | CRIAR | JSON estrutural da tela de console para cenário `tabela` | §12.2 deste handoff |
| `config/telas/demo/h0036_console_conjuntos.json` | NOVO | CRIAR | JSON estrutural da tela de console para cenário `conjuntos_campos` | §12.2 deste handoff |
| `config/telas/demo/h0036_hierarquia_conteudo.json` | NOVO | CRIAR | Fixture externa permanente para apresentação `hierarquia`; deve conter identificador exclusivo com string `"H-0036"` | §16 deste handoff |
| `config/telas/demo/h0036_tabela_conteudo.json` | NOVO | CRIAR | Fixture externa permanente para apresentação `tabela` | §16 deste handoff |
| `config/telas/demo/h0036_conjuntos_conteudo.json` | NOVO | CRIAR | Fixture externa permanente para apresentação `conjuntos_campos` | §16 deste handoff |
| `config/telas/demo/h0035_console_com_conteudo.json` | NOVO | CRIAR | JSON externo correspondente ao `h0035_console_com.json`; contém os 12 itens em `tipo: "multinivel"` | ADR-0027 D5; §11 deste handoff |
| `config/telas/demo/h0035_console_sem_conteudo.json` | NOVO | CRIAR | JSON externo correspondente ao `h0035_console_sem.json`; contém os 2 itens em `tipo: "multinivel"` | ADR-0027 D5; §11 deste handoff |
| `demo/teste_demo_console.py` | NOVO | CRIAR | Testes do catálogo do `demo.py` com conteúdo multinível; três apresentações; cenários com e sem conteúdo; identidade semântica; ponto de entrada real | §17.5 deste handoff |
| `docs/relatorios/IMP-0036-fornecimento-externo-dados-console-json-multinivel.md` | NOVO | CRIAR | Relatório de implementação | §25 deste handoff |

### 15.2 Inspeção técnica confirmada

A inspeção confirmou os seguintes símbolos relevantes:

**`tela/loader.py`:** `carregar_tela`, classes `TelaErro`, `TelaEstruturaInvalida`,
`TelaTipoDesconhecido` e demais.

**`tela/modelo.py`:** `construir_modelo`, `_construir_elementos_recursivo`,
classes `ModeloTela`, `Corpo`, `ElementoCorpo`, `ModeloTelaErro`.

**`tela/renderizador.py`:** `renderizar_tela`, `_linhas_console` (retorna
`[_PLACEHOLDER_CONSOLE]`), `_PLACEHOLDER_CONSOLE = "(console)"`,
`_caixa_de_elemento`, `_linhas_dashboard`, `_linhas_lancador`,
`_quadro_minimo_global`.

**Testes existentes:** `tela/teste_loader.py`, `tela/teste_modelo.py`,
`tela/teste_renderizador.py`, `tela/teste_distribuicao_matricial.py`,
`demo/teste_demo.py`, `demo/teste_diagnostico.py`,
`demo/teste_demo_distribuicao.py`, `demo/teste_explorar_barra_de_menus.py`.

### 15.3 Separação entre etapa do autor e etapa da implementação

A etapa `PATCH_HANDOFF` alterou exclusivamente o arquivo deste handoff.
Esta limitação vale somente para o autor. A futura implementação está
autorizada a alterar e criar os arquivos nominais listados em §15.1.

---

## 16. Fixtures permanentes: requisitos

### 16.1 Três fixtures principais do H-0036

Cada uma das três fixtures principais deve cobrir uma das apresentações previstas:

| Fixture | Apresentação | Caminho |
|---|---|---|
| Fixture hierarquia | `hierarquia` | `config/telas/demo/h0036_hierarquia_conteudo.json` |
| Fixture tabela | `tabela` | `config/telas/demo/h0036_tabela_conteudo.json` |
| Fixture conjuntos_campos | `conjuntos_campos` | `config/telas/demo/h0036_conjuntos_conteudo.json` |

### 16.2 Complexidade mínima obrigatória das fixtures (em conjunto)

As fixtures principais devem, em conjunto, provar:

- ao menos três níveis hierárquicos em pelo menos uma fixture;
- mais de um nó em pelo menos dois níveis em pelo menos uma fixture;
- nó do tipo `container`;
- nó do tipo `conteudo`;
- nó do tipo `nome_valor`;
- relação recursiva por `filhos`;
- preservação da ordem;
- designador declarativo (não numeração calculada);
- conteúdo textual reconhecível;
- par nome–valor;
- identidade semântica exclusiva em cada fixture;
- blocos específicos compatíveis com cada apresentação (`tabela` apenas em
  `tabela`, `campos` apenas em `conjuntos_campos`).

### 16.3 Identificador exclusivo para prova de identidade

A fixture `h0036_hierarquia_conteudo.json` (ou outra designada como fixture
principal da demonstração manual) deve conter texto exclusivo que inclua a string
`"H-0036"` e não apareça em nenhum outro artefato do sistema. Esse texto deve
ser visível na área do console quando a fixture for carregada.

O smoke test e a validação manual usarão esse texto como prova de identidade.

### 16.4 Fixtures dos cenários H-0035 afetados

Requisitos para `h0035_console_com_conteudo.json`:

- `tipo: "multinivel"`, apresentação `hierarquia`, nível único `tipo: "conteudo"`;
- campo `conteudo` indicando o nome do campo textual (ex.: `"texto"`);
- designador `nenhum`;
- 12 nós com os textos originais `"P01 linha"` a `"P12 linha"` (IDs e texto
  preservados para manter a identidade do cenário original);
- sem geometria calculada.

Requisitos para `h0035_console_sem_conteudo.json`:

- mesma estrutura;
- 2 nós com os textos `"Linha alfa"` e `"Linha bravo"` (IDs e texto preservados).

### 16.5 Proibições absolutas

O conteúdo `"(console)"` (placeholder) não deve aparecer na área do console
quando o documento externo estiver carregado. Nenhuma fixture deve:

- conter resultados físicos calculados;
- duplicar conteúdo no JSON estrutural correspondente;
- depender de edição temporária do usuário;
- conter dados codificados em Python (teste, demo, modelo ou renderizador).

---

## 17. Associação externa no `demo.py`

### 17.1 O que o `demo.py` deve fazer

A futura implementação deve alterar `demo/demo.py` para que ele:

1. identifique o cenário escolhido;
2. localize o JSON estrutural da tela;
3. localize o JSON externo de conteúdo quando o cenário possuir conteúdo externo;
4. carregue os dois documentos separadamente;
5. mantenha a distinção entre suas origens ao longo de todo o fluxo;
6. entregue a configuração estrutural e o conteúdo semântico como entradas separadas;
7. preserve o comportamento atual para cenários sem conteúdo externo (sem alterar
   o resultado para cenários não afetados).

A associação pode ficar num catálogo interno ou mecanismo equivalente do ponto de
entrada. Ela **não pode** ser criada como campo no JSON estrutural da tela.

### 17.2 O que o handoff não fixa

O handoff não determina:

- nome de variável, função, classe ou estrutura interna do catálogo;
- assinatura da função de carregamento duplo;
- forma interna do dicionário de associação;
- argumento de linha de comando.

Esses detalhes são de implementação, desde que preservem as regras normativas.

### 17.3 O que a implementação deve documentar

O relatório de implementação deve registrar:

- como o catálogo foi implementado no `demo.py`;
- a API interna efetiva (mesmo que não prescrita aqui);
- quais cenários são acessíveis e por qual método (tecla, número, item de menu);
- como a ausência de conteúdo externo é representada no catálogo.

---

## 18. Demonstração real

### 18.1 Ponto de entrada obrigatório

```text
demo/demo.py
```

O comportamento do H-0036 deve ser acessível e reproduzível por esse ponto de
entrada. Demo dedicado ou auxiliar pode existir somente se:

- houver justificativa concreta;
- não substituir o `demo.py` como única prova da integração;
- o comportamento também for acessível pelo fluxo real;
- não duplicar desnecessariamente a lógica de carregamento.

### 18.2 Comportamento durante redimensionamento

| Evento | Comportamento esperado |
|---|---|
| Maximização | Recalcular; conteúdo permanece visível |
| Restauração | Recalcular; conteúdo permanece visível |
| Redução horizontal | Recalcular |
| Redução vertical | Recalcular |
| Redimensionamento livre | Recalcular |
| Terminal abaixo do quadro mínimo | Ativar estado canônico `quadro mínimo de terminal pequeno` |
| Aumento após quadro mínimo | Reconstruir deterministicamente |

Reutilizar o mecanismo canônico global (`_quadro_minimo_global`). Não criar
fallback local concorrente.

---

## 19. Testes obrigatórios

### 19.1 Loader (em `tela/teste_loader.py`)

| Caso a cobrir |
|---|
| Documento válido com envelope mínimo completo: aceito |
| JSON sintaticamente inválido: rejeitado com erro de domínio |
| Raiz não-objeto (array, string, número, null): rejeitada |
| `tipo` ausente: rejeitado |
| `tipo` diferente de `"multinivel"`: rejeitado |
| `tipo: "multinivel"`: aceito |
| `formato` ausente: rejeitado |
| `formato` não-objeto: rejeitado |
| `dados` ausente: rejeitado |
| `dados` não-array: rejeitado |
| `formato.apresentacao` ausente: rejeitado |
| `formato.apresentacao` inválida: rejeitada |
| `formato.niveis` ausente ou não-array: rejeitado |
| Nível sem `id`: rejeitado |
| Nível sem `tipo`: rejeitado |
| Nível com tipo inválido: rejeitado |
| Nível sem `conteudo`: rejeitado |
| Nível sem `designador`: rejeitado |
| IDs de nível duplicados: rejeitados |
| Nó sem `id`: rejeitado |
| Nó sem `nivel`: rejeitado |
| Nó com `nivel` não declarado: rejeitado |
| Nó `container` sem `filhos`: rejeitado |
| Nó `conteudo` sem campo semântico declarado: rejeitado |
| Nó `nome_valor` sem campos de nome/valor: rejeitado |
| Filhos validados recursivamente |
| Presença de campo de resultado físico calculado na raiz: rejeitado |
| Campos específicos de apresentação incompatíveis: rejeitados |
| Fixture `h0036_hierarquia_conteudo.json`: carregada com sucesso |
| Fixture `h0036_tabela_conteudo.json`: carregada com sucesso |
| Fixture `h0036_conjuntos_conteudo.json`: carregada com sucesso |
| Fixture `h0035_console_com_conteudo.json`: carregada com sucesso |
| Fixture `h0035_console_sem_conteudo.json`: carregada com sucesso |

Testes unitários de rejeição podem construir variações inválidas mínimas em
memória. As fontes válidas exibidas e os cenários integrados devem usar
arquivos JSON permanentes.

### 19.2 Modelo (em `tela/teste_modelo.py`)

| Caso a cobrir |
|---|
| Entradas separadas (estrutural e conteúdo) preservam origens distintas |
| Preservação da ordem semântica de `dados` |
| Conteúdo semântico não reorganizado pelo modelo |
| Níveis declarados acessíveis separadamente da configuração estrutural |
| Pais e filhos preservados como declarados |
| Nó `container` representado com filhos acessíveis |
| Nó `conteudo` representado com campo semântico acessível |
| Nó `nome_valor` representado com nome e valor acessíveis |
| Ausência de leitura de arquivo pelo modelo |
| Ausência de cálculo físico no modelo |

### 19.3 Renderizador (em `tela/teste_renderizador.py`)

| Caso a cobrir |
|---|
| Apresentação `hierarquia`: exibe conteúdo hierárquico sem placeholder |
| Apresentação `tabela`: exibe conteúdo em forma de tabela sem placeholder |
| Apresentação `conjuntos_campos`: exibe conjuntos de campos sem placeholder |
| Designadores concretos calculados pelo renderizador (não vindos do JSON) |
| Conteúdo textual exibido nos nós `conteudo` |
| Pares nome–valor exibidos nos nós `nome_valor` |
| Hierarquia exibida a partir de `filhos` |
| Console sem conteúdo externo: placeholder `"(console)"` presente |
| Console com conteúdo externo: placeholder ausente |
| Conteúdo não duplicado entre JSON estrutural e externo |
| Identidade semântica do H-0036 confirmada na saída do renderizador |
| Telas existentes sem conteúdo externo: comportamento preservado (regressão) |
| Ausência de abertura de arquivo pelo renderizador |
| Truncamento e redimensionamento como cálculo (sem geometria no JSON) |

### 19.4 Testes de integração (em `demo/teste_diagnostico.py`)

| Caso a cobrir |
|---|
| Pipeline `h0036_hierarquia`: carregar tela + carregar externo + construir modelo + renderizar |
| Pipeline `h0036_tabela`: idem |
| Pipeline `h0036_conjuntos_campos`: idem |
| Pipeline `h0035_console_com` com externo: carregar dois arquivos + construir + renderizar |
| Pipeline `h0035_console_sem` com externo: idem |
| Configuração de cada tela de demo válida e reconhecida |

### 19.5 Testes do `demo.py` e do catálogo (em `demo/teste_demo_console.py`)

| Caso a cobrir |
|---|
| Catálogo com cenário com conteúdo: estrutural e externo corretos |
| Catálogo com cenário sem conteúdo: ausência de conteúdo representada explicitamente |
| Arquivo estrutural carregado é o correto para cada cenário |
| Arquivo externo carregado é o correto para cada cenário |
| Ausência de mistura de conteúdo entre cenários |
| Identidade semântica da fixture principal confirmada na saída |
| Apresentação `hierarquia` acessível pelo `demo.py` |
| Apresentação `tabela` acessível pelo `demo.py` |
| Apresentação `conjuntos_campos` acessível pelo `demo.py` |
| Ponto de entrada real (`demo/demo.py`) é executável |
| Cenário `h0035_console_com` carrega externo; placeholder ausente |
| Cenário `h0035_console_sem` carrega externo; placeholder ausente |
| Cenário sem conteúdo: placeholder presente; nenhum externo carregado |

### 19.6 Smoke tests semânticos

Para cada cenário integrado, o smoke deve confirmar:

```yaml
cenario: <id>
json_estrutural_esperado: <caminho exato>
json_externo_esperado: <caminho exato ou NENHUM>
identificador_semantico_esperado: <texto exclusivo que deve aparecer na saída>
conteudo_incorreto_que_deve_estar_ausente: <texto de outro cenário>
placeholder_esperado_ou_ausente: AUSENTE quando externo presente; PRESENTE quando ausente
```

Código de saída zero não é prova suficiente. O smoke deve verificar conteúdo
material na saída.

### 19.7 Regressão do H-0035

| Caso a cobrir |
|---|
| `h0035_console_com` após separação: carrega dois arquivos; distribuicao_matricial preservada; identidade original presente |
| `h0035_console_sem` após separação: carrega dois arquivos; comportamento sem matriz preservado |
| Demais cenários H-0035 não afetados: comportamento inalterado |
| Distribuição matricial configurável preservada (sem regressão do ADR-0025) |
| Conteúdo não duplicado: `itens` ausente do JSON estrutural; conteúdo presente no externo |

### 19.8 Independência dos valores esperados

Os valores esperados nos testes de validação devem ser derivados dos contratos
ativos, não da saída do próprio loader ou renderizador. Testes de rejeição devem
exigir a classe correta de erro de domínio e verificar dados materiais da mensagem.

---

## 20. Suíte canônica

### 20.1 Baseline verificado (H-0035)

A inspeção confirmou os seguintes scripts existentes, todos passando:

```bash
PYTHONDONTWRITEBYTECODE=1 python tela/teste_loader.py
PYTHONDONTWRITEBYTECODE=1 python tela/teste_modelo.py
PYTHONDONTWRITEBYTECODE=1 python tela/teste_renderizador.py
PYTHONDONTWRITEBYTECODE=1 python tela/teste_distribuicao_matricial.py
PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo.py
PYTHONDONTWRITEBYTECODE=1 python demo/teste_diagnostico.py
PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo_distribuicao.py
PYTHONDONTWRITEBYTECODE=1 python demo/teste_explorar_barra_de_menus.py
```

Total baseline: 8 scripts.

### 20.2 Adição pelo H-0036

Após a implementação, a suíte canônica inclui:

```bash
PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo_console.py
```

Total esperado após H-0036: 9 scripts.

### 20.3 Higiene de whitespace

```bash
git diff --check
```

### 20.4 Obrigações do executor

O executor deve registrar no relatório de implementação:

- comandos exatos executados;
- contagens obtidas em cada script;
- falhas identificadas;
- baseline encontrado antes das alterações;
- baseline final após a implementação;
- justificativa de qualquer alteração no conjunto canônico.

---

## 21. Validação manual

### 21.1 Aplicabilidade

A mudança altera o comportamento visual do console. A validação manual em TTY
real é obrigatória.

### 21.2 Termos usados neste roteiro

- **"console"**: área retangular da interface que exibe o conteúdo do documento externo.
- **"fixture hierarquia"**: `config/telas/demo/h0036_hierarquia_conteudo.json` —
  o documento externo principal de demonstração.
- **"identificador exclusivo"**: texto presente na fixture hierarquia contendo
  a string `"H-0036"`, que confirma qual documento foi carregado.
- **"placeholder"**: texto `"(console)"` exibido quando não há conteúdo externo.
- **"quadro mínimo"**: estado da interface quando o terminal é pequeno demais.
- **"cenário sem conteúdo"**: tela cujo catálogo não associa JSON externo.

### 21.3 Roteiro de validação manual

Execute na raiz do projeto:

```bash
python demo/demo.py
```

**Passo 1 — Abrir o cenário `h0036_console_hierarquia`**

Use o método de seleção documentado pelo implementador (tecla, número ou item
de menu) para abrir a tela do cenário `h0036_console_hierarquia`.

Confirme: a interface abre e o console exibe conteúdo da fixture hierarquia.

Resultado esperado: o identificador exclusivo da fixture (string `"H-0036"`) aparece
no console.

---

**Passo 2 — Confirmar o conteúdo externo correto**

Confirme: o texto do identificador exclusivo está visível na área do console.

Resultado esperado: texto com `"H-0036"` presente no console.

---

**Passo 3 — Confirmar que o conteúdo não está no JSON estrutural**

Confirme: o JSON estrutural `h0036_console_hierarquia.json` não contém o texto
do identificador exclusivo (verificação fora do TTY, por inspeção do arquivo).

Resultado esperado: o conteúdo está somente no JSON externo, não no estrutural.

---

**Passo 4 — Maximizar a janela**

Maximize o terminal e observe a interface.

Resultado esperado: a interface se reorganiza; o conteúdo permanece legível.

---

**Passo 5 — Restaurar ao tamanho normal**

Restaure o terminal ao tamanho normal.

Resultado esperado: a interface se reorganiza; o conteúdo continua visível.

---

**Passo 6 — Reduzir horizontalmente**

Reduza o terminal horizontalmente.

Resultado esperado: o conteúdo permanece visível com truncamento ou ajuste.

---

**Passo 7 — Reduzir verticalmente**

Reduza o terminal verticalmente.

Resultado esperado: o conteúdo permanece visível com ajuste.

---

**Passo 8 — Redimensionamento livre**

Arraste o terminal para diferentes tamanhos.

Resultado esperado: o conteúdo permanece visível em tamanhos razoáveis.

---

**Passo 9 — Produzir o quadro mínimo**

Reduza o terminal até abaixo do quadro mínimo (`LARGURA_MINIMA_TELA = 10`,
`ALTURA_MINIMA_TELA = 6`).

Resultado esperado: o quadro mínimo canônico aparece; a sessão não quebra.

---

**Passo 10 — Recuperação após aumento do terminal**

Após o quadro mínimo, aumente o terminal ao tamanho normal.

Resultado esperado: o conteúdo da fixture retorna sem resíduos do quadro mínimo.

---

**Passo 11 — Retornar ao catálogo e abrir cenário sem conteúdo**

Volte ao catálogo de cenários e abra uma tela sem conteúdo externo (qualquer
cenário H-0035 não afetado ou outra tela sem associação).

Resultado esperado: o placeholder `"(console)"` aparece na área do console.

---

**Passo 12 — Ausência de vazamento do conteúdo anterior**

Confirme que o texto do identificador exclusivo da fixture hierarquia não
aparece na nova tela.

Resultado esperado: o conteúdo do cenário anterior não vaza para o cenário sem conteúdo.

### 21.4 Declaração de resultado

O executor registra no relatório de implementação:

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

até que o usuário informe o resultado de cada passo. O executor e o QA **não
podem** declarar aprovação visual em nome do usuário.

Variantes possíveis:

```text
VALIDACAO_MANUAL_INCONCLUSIVA  — cenário não pôde ser reproduzido
MANUAL_VALIDATION_FAILED       — cenário reproduzido e resultado incorreto
```

---

## 22. Cenários sem conteúdo

Preservar explicitamente o comportamento das telas sem documento externo. Os
testes devem confirmar:

- continuam carregando sem erro;
- não tentam abrir arquivo inexistente;
- preservam o placeholder `"(console)"` ou comportamento histórico previsto;
- não recebem conteúdo de outro cenário por herança ou engano;
- não têm associação anterior criada implicitamente.

---

## 23. Critérios de aceite

| # | Critério | Como verificar |
|---|---|---|
| 1 | Documento externo válido é carregado e aceito | Teste focado no loader |
| 2 | `tipo: "multinivel"` reconhecido | Teste focado no loader |
| 3 | 20 validações semânticas implementadas e testadas | Testes nominais do loader |
| 4 | Três apresentações implementadas e provadas | Testes focados no renderizador |
| 5 | Três tipos de nível implementados e provados | Testes do loader e renderizador |
| 6 | Conteúdo semântico representado no modelo | Teste focado no modelo |
| 7 | Origens separadas preservadas no modelo | Teste focado no modelo |
| 8 | Console recebe conteúdo externo correto | Teste integrado do renderizador |
| 9 | Identidade semântica confirmada textualmente | Smoke test |
| 10 | Conteúdo NÃO duplicado no JSON estrutural | Teste do modelo/renderizador |
| 11 | Hierarquia NÃO inferida; exibida como declarada | Teste do modelo |
| 12 | Resultados físicos calculados NÃO presentes no documento externo | Teste do loader |
| 13 | Documentos inválidos rejeitados com erro de domínio material | Testes de rejeição no loader |
| 14 | Telas sem conteúdo externo preservam o placeholder | Teste de regressão no renderizador |
| 15 | `demo/demo.py` carrega os dois documentos separadamente | Teste do catálogo |
| 16 | Catálogo sem mistura entre cenários | Smoke tests por cenário |
| 17 | `h0035_console_com.json` sem campo `itens`; conteúdo no externo | Inspeção + teste |
| 18 | `h0035_console_sem.json` sem campo `itens`; conteúdo no externo | Inspeção + teste |
| 19 | Distribuição matricial do H-0035 preservada | Suíte de regressão |
| 20 | ADR-0025 e H-0035 integralmente preservados | Suíte canônica verde |
| 21 | `tipo: "matriz"` NÃO incorporado | Inspeção do código |
| 22 | Script produtor final NÃO implementado | Inspeção do código |
| 23 | Suíte canônica (9 scripts) verde | Execução da suíte completa |
| 24 | Demonstração permanente e repetível pelo `demo.py` | Demo executável |
| 25 | Validação manual registrada pelo usuário | Relatório de implementação |

---

## 24. Escopo negativo (fora do escopo)

Estão explicitamente fora do escopo deste handoff:

- criação ou alteração de ADR;
- alteração de contratos ativos;
- alteração da nomenclatura;
- implementação do script produtor final;
- definição do protocolo de vínculo entre `tela.json` e documento externo no produto;
- suporte ao tipo `"matriz"` no mecanismo de fornecimento externo;
- navegação interativa nos níveis do conteúdo multinível;
- expansão ou recolhimento de nós;
- paginação interativa do conteúdo multinível;
- cache do documento externo;
- atualização automática do conteúdo externo;
- versionamento do documento externo ou do produtor;
- stdout como transporte;
- arquivos temporários de integração;
- autenticação;
- persistência;
- migração automática das telas existentes;
- comportamento diante de fonte ausente ou inválida além do documentado;
- diretório global definitivo de dados de runtime do produto;
- commit;
- início de ciclo posterior.

**Não estão fora do escopo** (foram excluídos indevidamente do handoff original e
agora estão explicitamente incluídos):

- schema semântico de `dados[]` — decidido e obrigatório (ADR-0027 D11);
- 20 validações semânticas — obrigatórias (ADR-0027 D13);
- três apresentações — obrigatórias;
- alteração do `demo/demo.py` — obrigatória;
- revisão dos JSONs do H-0035 afetados — obrigatória;
- criação dos JSONs externos correspondentes — obrigatória;
- fixtures permanentes — obrigatórias.

---

## 25. Exceção operacional

```text
Se durante a implementação um arquivo fora da lista nominal for estritamente
necessário para cumprir o handoff, preservar a suíte obrigatória ou evitar
aborto desproporcional da entrega, o executor deve parar antes da alteração e
pedir autorização explícita ao usuário.

O pedido deve informar:
- arquivo;
- motivo;
- escopo exato;
- mudança esperada.

A autorização não permite criar nova semântica, arquitetura ou política.
Quando autorizada, a alteração deve ser registrada no relatório de
implementação e auditada pelo QA dentro do escopo concedido.
```

Esta cláusula **somente** se aplica a arquivo técnico inesperadamente necessário.
Ela **não** autoriza o executor a decidir:

- schema semântico (decidido pela ADR-0027 D11);
- validações (decididas pela ADR-0027 D13);
- forma dos nós ou níveis (decidida pelo contrato_json_console §12);
- apresentações previstas (definidas pela ADR-0027 D11.2);
- localização geral das fixtures (definida em §12.1);
- responsabilidade do `demo.py` (definida pela ADR-0027 D2, D7).

---

## 26. Condições de bloqueio

Parar com:

```text
H3_BLOCKED_DOCUMENTATION
```

se: faltar contrato indispensável; existir contradição normativa ativa; não for
possível listar nominalmente os arquivos necessários; a implementação exigir alterar
autoridade documental; a capacidade exigir decidir semântica não fechada sem
autorização.

Parar com:

```text
BLOCKED_USER_DECISION
```

se: qualquer decisão indispensável não estiver coberta por este handoff ou pela
exceção operacional.

Não completar lacunas silenciosamente. Não inventar arquitetura. Não criar
permissões genéricas.

---

## 27. Relatório de implementação

Autorizado a criar:

```text
docs/relatorios/IMP-0036-fornecimento-externo-dados-console-json-multinivel.md
```

O relatório deve conter, no mínimo:

1. identificação;
2. handoff executado;
3. autoridades;
4. estado Git inicial;
5. arquivos alterados;
6. arquivos criados;
7. inventário dos JSONs do H-0035 (confirmando a classificação do §11);
8. JSONs estruturais modificados (campos removidos, campos preservados);
9. JSONs externos criados (caminhos, estrutura, identificador exclusivo);
10. associação implementada no `demo.py` (mecanismo, API interna efetiva);
11. função de carregamento do documento externo (localização, assinatura efetiva);
12. 20 validações implementadas (casos cobertos, classes de erro usadas);
13. três apresentações implementadas;
14. três tipos de nível implementados;
15. fixtures permanentes (caminho, identificador exclusivo, estrutura de níveis);
16. testes (loader, modelo, renderizador — casos cobertos e contagens);
17. smoke tests (por cenário — resultado confirmado);
18. suíte canônica (9 scripts — comandos, contagens, falhas);
19. demonstração (método de acesso, cenários demonstrados);
20. resultado da validação manual (informado pelo usuário);
21. preservação do H-0035 (confirmada);
22. fronteira futura com o Pipeline;
23. exceções operacionais solicitadas e autorizadas;
24. estado Git final;
25. `git diff --check`;
26. limitações conhecidas;
27. conclusão factual.

O relatório **não** pode declarar aprovação da própria implementação.

---

## 28. Arquivos preservados ou proibidos

### 28.1 Preservados sem alteração pela futura implementação

```text
docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
docs/relatorios/RELATORIO_QA_ADR-0026.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0026.md
docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0026.md
docs/relatorios/RELATORIO_QA_ADR-0027.md
docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0027.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0027.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0027.md
docs/relatorios/RELATORIO_QA_H-0036_HANDOFF.md
docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
docs/handoff/H-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
docs/relatorios/IMP-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
docs/NOMENCLATURA.md
docs/adr/INDICE_ADR.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_console.md
docs/contratos/contrato_json_console.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_json_dashboard.md
docs/contratos/contrato_json_lancador.md
docs/contratos/contrato_lancador.md
tela/distribuicao_matricial.py
tela/teste_distribuicao_matricial.py
demo/demo_distribuicao.py
demo/diagnostico.py
demo/explorar_barra_de_menus.py
demo/teste_explorar_barra_de_menus.py
config/telas/demo/destino_minimo.json
config/telas/demo/grupo_minimo.json
config/telas/demo/stub_b.json
```

Também preservados: todas as telas `h0029_*`, `h0030_*`; os 24 arquivos
`h0035_*.json` classificados como `PRESERVAR_SEM_ALTERACAO` em §11; demais ADRs,
contratos, índices, handoffs históricos e relatórios históricos; qualquer
arquivo não relacionado ao console ou ao novo mecanismo de fornecimento externo.

### 28.2 Arquivos com alteração autorizada e responsabilidade histórica preservada

Os dois arquivos a seguir estão autorizados para `ALTERAR` na seção §15.1.
Eles não são preservados sem alteração. A exigência de preservação refere-se
à responsabilidade funcional histórica, não à imutabilidade do arquivo.

```yaml
- arquivo: demo/teste_demo_distribuicao.py
  alteracao_autorizada: true
  preservacao_exigida: >
    Preservar a responsabilidade histórica de testar a demonstração de
    distribuição e adicionar somente a cobertura necessária aos cenários
    adaptados pelo H-0036.

- arquivo: config/telas/demo/demo.json
  alteracao_autorizada: true
  preservacao_exigida: >
    Preservar a identidade e a finalidade histórica da configuração do
    launcher da demonstração, permitindo somente a atualização nominal exigida
    pela integração dos cenários do H-0036.
```

### 28.3 Comportamentos preservados

- O placeholder `"(console)"` permanece ativo quando não houver conteúdo
  externo — compatibilidade retroativa com todas as telas existentes.
- A capacidade `distribuicao_matricial` (ADR-0025, H-0035) permanece inalterada
  como mecanismo; seus dados passam a vir do documento externo.
- Dashboard e lançador não participam do novo mecanismo.
- Nenhuma migração automática das telas existentes.
- Nenhum vínculo implícito criado entre telas existentes e o novo mecanismo.

### 28.4 Proibições explícitas na futura implementação

- Não alterar ADR-0026, ADR-0027, contratos aplicados nem nomenclatura.
- Não implementar o script produtor final.
- Não inventar protocolo de vínculo entre `tela.json` e documento externo.
- Não incluir suporte a `tipo: "matriz"` sem autoridade explícita.
- Não implementar navegação, seleção, expansão, recolhimento ou paginação
  interativa de conteúdo multinível.
- Não reinserir conteúdo de runtime no JSON estrutural.
- Não codificar conteúdo válido exibido em Python (teste, demo, modelo ou renderizador).
- Não criar diretório global de runtime do produto.
- Não fazer stage nem commit.
- Não iniciar ciclo posterior.

---

## 29. Rastreabilidade dos achados corrigidos

```yaml
qa_de_origem: docs/relatorios/RELATORIO_QA_H-0036_HANDOFF.md

achados_corrigidos:
  QAH-0036-001:
    descricao_original: >
      Mecanismo de entrega do documento externo ao console (carregamento por
      caminho de arquivo, loader com caminho, demo carregando diretamente a
      fixture) sem autoridade normativa ativa.
    correcao: >
      demo/demo.py passa a ser o ponto de entrada responsável pelo carregamento
      separado dos dois documentos e pela associação externa por cenário, sem
      campo de vínculo no JSON estrutural e sem o renderizador abrir arquivos.
      Autoridade: ADR-0027 D2, D3, D7, D8; contrato_console §20; contrato_tela_json §32.
    secoes_corrigidas: "§4.3, §6, §8, §10, §15, §17, §23"

  QAH-0036-002:
    descricao_original: >
      Handoff propunha config/conteudo/ como primeira convenção de localização de
      documentos externos de conteúdo, sem autoridade normativa ativa para essa
      convenção.
    correcao: >
      Fixtures permanentes ficam em config/telas/demo/, seguindo a organização
      existente do repositório, com sufixo _conteudo.json para distingui-las dos
      JSONs estruturais. Não é criado diretório global definitivo de runtime.
      Caminhos nominais exatos definidos em §12.1 e §15.1.
      Autoridade: ADR-0027 D6, §7.4; contrato_json_console §12.8.
    secoes_corrigidas: "§4.3, §12, §15.1, §16, §23, §28"

  QAH-0036-003:
    descricao_original: >
      Handoff exigia validações e provas de níveis, hierarquia, identificadores e
      campos obrigatórios, mas afirmava que o schema interno de dados[] e as
      validações seriam definidos pela implementação ou por exceção operacional.
    correcao: >
      Schema semântico (envelope, apresentações, tipos de nível, forma dos nós,
      designadores, relação por filhos), 20 validações mínimas e resultados
      proibidos são agora requisitos fechados do H-0036, incorporados em §13 e §14.
      A exceção operacional não autoriza decidir schema.
      Autoridade: ADR-0027 D11, D13; contrato_json_console §12.
    secoes_corrigidas: "§4.3, §9, §13, §14, §15, §19, §22, §24, §23"

autoridade_corretiva:
  adr: ADR-0027
  status: aceita e aplicada
  qa_adr_inicial: ARCHITECTURE_REVIEW_REQUIRED
  qa_adr_pos_patch: ADR_APPROVED
  qa_aplicacao: ADR_APPLICATION_APPROVED_WITH_NOTES
```

---

### 29.1 Segundo patch do handoff

```yaml
segundo_patch_do_handoff:
  qa_de_origem: docs/relatorios/RELATORIO_QA_POS_PATCH_H-0036_HANDOFF.md
  classificacao_de_origem: H2_HANDOFF_PATCH_REQUIRED
  achados_corrigidos:
    - QAHPP-0036-001
    - QAHPP-0036-002

  QAHPP-0036-001:
    correcao: >
      Inventário dos 26 JSONs completado com JSON externo correspondente e
      justificativa nominal por arquivo; contagens finais registradas em §11.

  QAHPP-0036-002:
    correcao: >
      Removida a contradição entre arquivos autorizados para alteração e arquivos
      preservados sem alteração; demo/teste_demo_distribuicao.py e
      config/telas/demo/demo.json foram removidos da lista de §28.1 e
      registrados em §28.2 com alteração autorizada e responsabilidade
      histórica preservada.

achados_originais_preservados:
  QAH-0036-001_corrigido: true
  QAH-0036-002_corrigido: true
  QAH-0036-003_corrigido: true
```

---

## 30. Verificação de coerência

| # | Verificação | Resultado |
|---|---|---|
| 1 | O H-0036 original foi corrigido (mesmo arquivo, mesmo número) | Confirmado — arquivo preservado, número inalterado |
| 2 | Nenhum novo handoff criado | Confirmado |
| 3 | ADR-0027 aparece como autoridade corretiva | Confirmado — §3, §4.3, §8, §29 |
| 4 | Três achados mapeados e corrigidos | Confirmado — §29 |
| 5 | `demo/demo.py` autorizado a alterar | Confirmado — §15.1 |
| 6 | Demo dedicado não é a única prova | Confirmado — §18.1 |
| 7 | Todos os JSONs válidos exibidos são permanentes | Confirmado — §12, §15.1, §16 |
| 8 | JSONs do H-0035 inspecionados nominalmente | Confirmado — §11 (26 arquivos) |
| 9 | Cada JSON afetado possui ação e arquivo externo correspondente | Confirmado — §11.1 |
| 10 | Nenhum JSON não afetado incluído sem motivo | Confirmado — §11 (24 classificados como PRESERVAR) |
| 11 | Caminhos de fixtures são exatos | Confirmado — §12.1, §12.2, §15.1 |
| 12 | `config/conteudo/` não existe como convenção global silenciosa | Confirmado — §12.1 proíbe explicitamente |
| 13 | Três apresentações estão no escopo | Confirmado — §5, §13.2, §19, §23 |
| 14 | Três tipos de nível estão no escopo | Confirmado — §13.3, §19, §23 |
| 15 | Vinte validações estão no escopo | Confirmado — §14 |
| 16 | Schema não está deferido | Confirmado — §9 (removido dos deferidos), §13 (obrigatório) |
| 17 | Renderizador não abre arquivos | Confirmado — §6, §10, §14, §23 |
| 18 | Modelo não escolhe a fonte | Confirmado — §6, §10, §14 |
| 19 | Conteúdo não volta ao JSON estrutural | Confirmado — §8 D-ADR27-1, §10, §28.3 |
| 20 | Cenário sem conteúdo coberto | Confirmado — §22, §19.7 |
| 21 | Testes são nominais | Confirmado — §19 (casos por nome) |
| 22 | Comandos são exatos | Confirmado — §20 |
| 23 | Suíte canônica foi inspecionada (8 scripts verificados) | Confirmado — §20.1 |
| 24 | Demonstração usa `demo.py` | Confirmado — §18 |
| 25 | Validação manual prevista | Confirmado — §21 |
| 26 | Relatório de implementação autorizado | Confirmado — §27 |
| 27 | Nenhum arquivo necessário está simultaneamente preservado e proibido | Confirmado — §15.1 vs §28.4 sem sobreposição |
| 28 | Nenhuma decisão do Pipeline antecipada | Confirmado — §9, §24 |
| 29 | Somente o handoff foi alterado nesta etapa | Confirmado — escopo PATCH_HANDOFF |
| 30 | `git diff --check` limpo | Confirmado na verificação pós-patch |
| 31 | QAHPP-0036-001 corrigido: inventário dos 26 JSONs com 8 campos por arquivo | Confirmado — §11 com json_externo_correspondente e justificativa nominal |
| 32 | QAHPP-0036-002 corrigido: nenhum arquivo em categorias incompatíveis | Confirmado — §15.1 vs §28.1 e §28.2 sem conflito |
| 33 | Segundo patch rastreado nominalmente | Confirmado — §29.1 e §31 |

---

## 31. Estado do handoff

```yaml
handoff: H-0036
estado: CORRIGIDO_AGUARDANDO_QA
qa_handoff_inicial: H3_BLOCKED_DOCUMENTATION
qa_handoff_inicial_relatorio: docs/relatorios/RELATORIO_QA_H-0036_HANDOFF.md
qa_pos_primeiro_patch: H2_HANDOFF_PATCH_REQUIRED
qa_pos_primeiro_patch_relatorio: docs/relatorios/RELATORIO_QA_POS_PATCH_H-0036_HANDOFF.md
qa_pos_segundo_patch: NAO_REALIZADO
implementacao: NAO_INICIADA
commit: NAO_REALIZADO
proxima_categoria: QA_HANDOFF
```
