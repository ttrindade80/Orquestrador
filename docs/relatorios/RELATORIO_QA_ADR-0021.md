---
name: RELATORIO_QA_ADR-0021
description: Relatorio de auditoria formal da ADR-0021 contra as decisoes do usuario e autoridades normativas vigentes
metadata:
  type: relatorio_qa
  etapa: QA_ADR
  status: CONCLUIDO
  data: "2026-07-14"
---

# RELATÓRIO DE QA — Auditoria Documental da ADR-0021

## 1. Identificação

* **Artefato auditado:** `docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md`
* **Relatório produzido:** `docs/relatorios/RELATORIO_QA_ADR-0021.md`
* **Data da auditoria:** 14 de Julho de 2026
* **Papel:** Auditor documental independente
* **Status formal atribuído:** `ADR_APPROVED_WITH_NOTES`

---

## 2. Objetivo e Limites

**Objetivo:** Auditar formalmente a ADR-0021 para verificar se ela registra fielmente as decisões explícitas do usuário (D1 a D13), se é compatível com as autoridades normativas existentes do repositório, se preserva a coerência de nomenclatura e se segue as convenções formais de ADRs recentes do projeto.

**Limites da etapa:** Esta etapa é estritamente de auditoria de qualidade (QA). Não está autorizada nenhuma correção física de arquivo na ADR, aplicação documental nos contratos ou índice, alteração em código ou configurações, criação de handoffs de implementação ou execução de commits. 

---

## 3. Estado Git Inicial

O estado Git inicial observado é inteiramente convergente com o informado:

* **Branch atual:** `master`
* **HEAD commit:** `0143fd1` (`chore: migra orquestrador para repositorio independente`)
* **Workspace:** Contém exatamente dois arquivos não rastreados que representam a entrada deste ciclo (a ADR-0021 e o Levantamento):
  * `docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md`
  * `docs/relatorios/LEVANTAMENTO_PREPARACAO_INTEGRACAO_PIPELINE_ORQUESTRADOR.md`
* **Stage:** Totalmente vazio (`git diff --cached` sem alterações).
* **Modificações em arquivos rastreados:** Nenhuma (`git diff` vazio).

---

## 4. Autoridades Consultadas

Foram lidos e consultados integralmente os seguintes documentos normativos de referência:

1. `docs/adr/INDICE_ADR.md` — Índice de decisões arquiteturais.
2. `docs/NOMENCLATURA.md` — Glossário e definições de responsabilidades.
3. `docs/adr/ADR-0008-modelo-configuracao-por-tela.md` — Modelo de JSON declarativo por tela.
4. `docs/adr/ADR-0009-caminho-formato-jsons-tela.md` — Caminho canônico inicial `config/telas/<id>.json`.
5. `docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md` — Dashboard como elemento do corpo.
6. `docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md` — Barra declarada explicitamente.
7. `docs/adr/ADR-0014-barra-horizontal-termos-especificos.md` — Termos específicos e distribuição responsiva.
8. `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md` — Árvore de composição do corpo.
9. `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md` — Ausência de distribuição ≠ igual.
10. `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md` — Limites de aninhamento.
11. `docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md` — Estrutura de matriz bidimensional.
12. `docs/contratos/contrato_json_tela_minima.md` — Envelope declarativo mínimo da tela.
13. `docs/contratos/contrato_tela_json.md` — Contrato de acoplamento estilo x tela.
14. `docs/contratos/contrato_estilo.md` — Regras visuais e de presets globais.
15. `docs/contratos/contrato_chip.md` — Definições de chips.
16. `docs/contratos/contrato_composicao_corpo.md` — Regras de montagem do corpo.
17. `docs/contratos/contrato_barra_de_menus.md` — Regras da barra de menus.
18. `docs/contratos/contrato_console.md` — Container de log/dados.
19. `docs/contratos/contrato_lancador.md` — Corpo de navegação.
20. `docs/handoff/H-0031-migracao-repositorio-orquestrador-raiz-independente.md` — Histórico de migração de raiz.
21. `docs/relatorios/IMP-0031-migracao-repositorio-orquestrador-raiz-independente.md` — Relatório de implementação da migração.
22. `docs/relatorios/RELATORIO_QA_H-0031_IMPLEMENTACAO.md` — QA da implementação da raiz.

---

## 5. Estado Factual de Entrada

O estado factual foi validado a partir de `docs/relatorios/LEVANTAMENTO_PREPARACAO_INTEGRACAO_PIPELINE_ORQUESTRADOR.md`. O levantamento demonstra com precisão a estrutura física do repositório, o acoplamento do runtime ao diretório e pacote `tela/`, e a dependência direta dos testes atuais e subprocessos em relação a caminhos específicos de arquivos como `config/telas/orquestrador.json` e scripts sob `tela/`. Essa base factual confirma a necessidade de uma ADR estrutural para governar a migração sem compatibilidade transiente mas de forma controlada para não quebrar a suíte.

---

## 6. Auditoria D1 a D13

Abaixo apresenta-se o resultado da auditoria detalhada de conformidade da ADR-0021 para cada uma das 13 decisões explícitas estabelecidas pelo usuário:

* **D1 — Motor compartilhado (CONFORME):** A decisão está fielmente registrada na seção `### D1 — Motor compartilhado de telas`. Ela estabelece a permanência de `tela/` como diretório na raiz operacional, lista explicitamente todos os 4 módulos funcionais e os 3 scripts de testes correspondentes, exige sua reutilização pela demonstração e pelo futuro `orquestrador.py` e proíbe terminantemente qualquer duplicação funcional ou segunda implementação do loader/modelo/renderizador.
* **D2 — Aplicação demonstrativa separada (CONFORME):** Registrado na seção `### D2 — Aplicacao demonstrativa`. Planeja a futura criação da pasta `demo/` na raiz operacional e identifica nominalmente os 3 scripts demonstrativos/exploratórios e seus 3 arquivos de testes a serem migrados. A ADR-0021 abstém-se corretamente de fixar detalhes de implementação como assinaturas de funções, caminhos concretos de imports ou necessidade de `demo/__init__.py`.
* **D3 — Telas demonstrativas (CONFORME):** Registrado na seção `### D3 — Telas declarativas da demonstracao`. Define a futura criação de `config/telas/demo/` e especifica a lista nominal de todas as 15 telas declarativas de teste/demonstração atualmente sob `config/telas/` a serem migradas. Mantém explícito que os IDs das telas não serão alterados nesta etapa, exceto a tela raiz.
* **D4 — Identidade da demonstração (CONFORME):** Registrado na seção `### D4 — Identidade da demonstracao`. Define que a atual `config/telas/orquestrador.json` representará exclusivamente a demonstração e será futuramente migrada para `config/telas/demo/demo.json`, alterando seu ID interno para `demo`. O ponto de entrada demonstrativo iniciará pela identidade `demo` e é explicitada a proibição de alias/fallback silencioso entre `demo` e `orquestrador`.
* **D5 — Reserva das telas do produto real (CONFORME):** Registrado na seção `### D5 — Telas do Orquestrador real`. O diretório `config/telas/` permanece reservado para as telas do produto real. É explicitly esclarecido que a futura `config/telas/orquestrador.json` real não tem seu conteúdo, composição ou implementação governados ou desenhados por esta ADR.
* **D6 — Duas raízes declarativas explícitas (CONFORME):** Registrado na seção `### D6 — Politica de resolucao das telas`. Estabelece que o motor compartilhado utilizará raízes declarativas distintas dependendo do ponto de entrada (`config/telas/demo/` para demonstração e `config/telas/` para produto). A ADR proíbe explicitamente busca ambígua, fallback silencioso, cópia duplicada de arquivos e tratamento de telas demonstrativas como produto. Abstém-se de prescrever assinaturas de funções do loader ou mecanismo de injeção de parâmetros.
* **D7 — Migração sem compatibilidade transitória (CONFORME):** Registrado na seção `### D7 — Ausencia de compatibilidade transitoria`. Confirma a migração direta sem a persistência de wrappers, aliases de pacotes, cópias duplicadas de scripts/JSONs, fallback silencioso ou alias entre os IDs `demo` e `orquestrador`. Exige que todos os imports, subprocessos e testes afetados sejam atualizados no mesmo ciclo.
* **D8 — Organização dos JSON gerais (CONFORME):** Registrado na seção `### D8 — Organizacao dos JSON gerais de configuracao`. Define a criação futura de `config/layouts/` e `config/elementos/` e distribui os 6 arquivos de configuração geral (`layout_console.json`, `layout_dado.json`, `layout_menu.json` para layouts; `cabecalho.json`, `barra_de_menus.json`, `lancador.json` para elementos). Deixa claro que a movimentação física de arquivos não altera schema, conteúdo, semântica ou status documental (os obsoletos/transicionais continuam com essa classificação).
* **D9 — Preservação do estilo global (CONFORME):** Registrado na seção `### D9 — Preservacao de \`config/estilo.json\``. O arquivo `config/estilo.json` permanece inalterado em seu caminho atual, sem ser movido para as pastas de layouts, elementos ou telas. Uma reorganização dos estilos é explicitamente vinculada a decisões documentais futuras sobre a tela de estilos.
* **D10 — Reutilização declarativa (CONFORME):** Registrado na seção `### D10 — Reutilizacao entre demonstracao e produto`. Estabelece a demonstração como ambiente contínuo de testes e validação visual de capacidades declarativas. Uma nova tela declarativa que use apenas capacidades já implementadas pode ser criada unicamente por JSON. A transferência conceitual de uma tela demonstrativa para o produto real deve reaproveitar integralmente o loader, modelo, renderizador e contratos, impedindo a reescrita do motor.
* **D11 — Divisão condicionada do futuro handoff (CONFORME):** Registrado na seção `### D11 — Tamanho do futuro handoff`. Registra a intenção de um handoff único de implementação, porém condicionado à extensão e à coesão física. Se a lista nominal de alterações for excessiva ou envolver tópicos independentes, o handoff deverá ser dividido, sem que isso altere a decisão de arquitetura desta ADR.
* **D12 — Separação da futura tela real (CONFORME):** Registrado na seção `## Fora do escopo` (linhas 516-536). Mantém explicitamente fora de escopo: a criação de `orquestrador.py`, sua responsabilidade, o conteúdo de `config/telas/orquestrador.json` real, composição mínima do produto, cabeçalho, console ou dashboard vazios, atalhos de barra, navegação ou implementação da tela de estilos e a integração concreta com o Pipeline.
* **D13 — Pendências de preenchimento não resolvidas (CONFORME):** Registrado na seção `## Pendencias funcionais conhecidas` (linhas 540-579). Registra sem resolver os problemas de preenchimento de área do `destino_minimo` e `grupo_minimo`, mantendo o estado de causa, configuração/natureza e solução como `NAO_CONFIRMADA`. Abstém-se de assumir soluções e exige levantamento focal reproduzível futuro.

---

## 7. Coerência Estrutural

A ADR-0021 apresenta excelente coerência estrutural de longo prazo. A arquitetura de diretórios proposta estabelece uma fronteira nítida de responsabilidades:

1. **Motor Compartilhado:** `tela/` (contendo apenas lógica limpa e reutilizável de infraestrutura de visualização e seus testes básicos).
2. **Ambiente de Demonstração (Código/Testes):** `demo/` (pontos de entrada de visualização e scripts experimentais e seus respectivos testes).
3. **Ambiente de Demonstração (Configurações):** `config/telas/demo/` (arquivos JSON históricos, do catálogo e de regressão).
4. **Ambiente do Produto Real (Configurações):** `config/telas/` (telas exclusivas e ativas do orquestrador em produção).
5. **Configurações Gerais de Layout:** `config/layouts/` (ajustes geométricos estruturais por tipo de container).
6. **Configurações Gerais de Elementos:** `config/elementos/` (parâmetros de exibição padrão de cabeçalho, barra de menus e lançador).
7. **Aparência/Estilo Universal:** `config/estilo.json` (presets visuais globais).

Esta separação impede contaminações mútuas de responsabilidades (por exemplo, misturar comportamento demonstrativo e dados de testes com arquivos de telas reais do produto).

---

## 8. Compatibilidade com ADRs Anteriores

A ADR-0021 mantém compatibilidade conceitual estrita e explícita com o arcabouço normativo do projeto:

* **Compatibilidade com ADR-0008:** Preserva integralmente o modelo declarativo por tela. Toda a composição continua sendo orientada pela declaração do arquivo JSON de cada tela.
* **Compatibilidade e Relação com ADR-0009:** Identifica de forma clara a substituição parcial da política de caminhos de arquivos JSON. Em vez de uma única raiz plana `config/telas/<id>.json`, introduz-se a raiz secundária `config/telas/demo/<id>.json` para o escopo demonstrativo, preservando o arquivo global de estilo `config/estilo.json` em seu local isolado. O relacionamento entre as duas políticas concorrentes é explicitado com base no ponto de entrada executor.
* **Compatibilidade com Semânticas Funcionais (ADRs 0010, 0012, 0014, 0015, 0018, 0019, 0020):** Registra formalmente que as regras de composição, de barras declarativas, de distribuição responsiva, de profundidade de grupos e de matriz bidimensional compartilhada de grupos permanecem totalmente intocadas. A mera reorganização de diretórios e caminhos de arquivos em disco não redefine nem reescreve as regras lógico-visuais de renderização do motor.
* **Relação com H-0031:** Respeita e mantém a raiz independente estabelecida pelo ciclo H-0031, apenas refinando e organizando os componentes internos do repositório de forma limpa.

---

## 9. Consequências

A seção `## Consequencias` lista de forma realista e detalhada todos os custos, impactos positivos, restrições e riscos associados à implementação da decisão:

* Identifica a necessidade futura de atualização em lote de imports Python e subprocessos em testes de regressão;
* Alerta para a mudança necessária de comandos de console canônicos e documentação operacional;
* Registra o risco associado à extensão e coesão dos handoffs e proíbe expressamente a duplicação ou fragmentação do motor;
* Aceita o custo de não possuir uma compatibilidade transiente (que exigirá esforço maior de migração atômica de testes e scripts de entrada no ciclo de aplicação correspondente).

---

## 10. Documentos Afetados

A ADR-0021 identifica com precisão os documentos que deverão ser atualizados no ciclo documental da etapa `APLICAR_ADR`:

* **Mínimos exigidos e identificados (CONFORME):**
  * `docs/adr/INDICE_ADR.md`
  * `docs/NOMENCLATURA.md`
  * `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`
  * `docs/adr/ADR-0009-caminho-formato-jsons-tela.md`
  * `docs/contratos/contrato_json_tela_minima.md`
  * `docs/contratos/contrato_tela_json.md`
* **Outros identificados de forma exaustiva (CONFORME):**
  * Contratos adicionais: `contrato_composicao_corpo.md`, `contrato_barra_de_menus.md`, `contrato_chip.md`, `contrato_cabecalho.md`, `contrato_estilo.md`, `contrato_json_barra_de_menus.md`, `contrato_json_cabecalho.md`, `contrato_json_lancador.md`, `contrato_lancador.md`.
  * Documentos operacionais e históricos: `docs/INDICE.md`, `H-0030`, `H-0031`, `IMP-0030`, `IMP-0031`, `RELATORIO_QA_H-0031_IMPLEMENTACAO.md`, além do Levantamento preparatório.

Isso demonstra rastreabilidade documental impecável.

---

## 11. Critérios de Aplicação

Os critérios de aplicação futura são extraídos de forma objetiva ao longo do corpo da decisão:

* É estabelecida a verificação lógica de não haver buscas ambíguas ou fallbacks silenciosos entre as duas raízes de telas;
* É exigida a preservação atômica da suíte de testes (com as atualizações necessárias dos caminhos literais);
* Mantém-se clara a preservação do caminho de `config/estilo.json` e a reserva da tela real para uma ADR futura de design visual e Pipeline.

Contudo, observa-se que a ADR-0021 não agrupa esses critérios em uma seção dedicada denominada "Critérios de aplicação" ou "Critérios para futura aplicação", padrão observado nas ADRs recentes do projeto (como ADR-0018, 0019, 0020). Essa ausência foi classificada como um achado de severidade baixa (ver seção 14).

---

## 12. Escopo Negativo

O escopo negativo está explícito e é altamente defensivo. A ADR-0021 não decide nem implementa o produto real, `orquestrador.py`, a tela raiz de produção, chips de estilo ativos, integração com o Pipeline ou correção direta das pendências de layout de `destino_minimo` e `grupo_minimo`. Isso garante que a ADR atue puramente como uma decisão de organização de caminhos e separação estrutural de diretórios, sem introduzir decisões de design visual ou lógica operacional prematura.

---

## 13. Terminologia e Convenção

* **Terminologia (CONFORME):** Faz uso totalmente coerente e padronizado dos termos `demonstração`, `produto real` e `motor compartilhado`. Trata os diretórios novos (`demo/`, `config/telas/demo/`, `config/layouts/`, `config/elementos/`) de forma estritamente projetada (futuros), sem tratá-los como já criados.
* **Convenção Formal (CONFORME):** A estrutura da ADR-0021 é extremamente limpa, apresentando o frontmatter em YAML completo de rastreabilidade (com contratos afetados listados), título claro, status de autoria ("aceita"), data correspondente, contexto factual fundamentado, decisões bem delimitadas, relação inequívoca com ADRs anteriores, consequências realistas, listagem de documentos potencialmente afetados, escopo negativo bem delineado e registro neutro de pendências funcionais conhecidas.

---

## 14. Achados

Abaixo estão listados e classificados formalmente todos os achados identificados na auditoria:

### Achado 1 — Estrutural/Convenção

```yaml
id: ACHADO_01_ESTRUTURA_CRITERIOS_AUSENTES
severidade: baixo
titulo: Ausência de cabeçalho dedicado para critérios de aplicação
evidencia: A ADR-0021 não possui as seções "## Critérios para futura aplicação" ou "## Critérios para futuro handoff" presentes no índice e no corpo, divergindo das convenções formais de ADRs recentes (ADR-0018, ADR-0019, ADR-0020).
decisao_ou_autoridade_afetada: Convenção estrutural recente do projeto (ADR-0017 a ADR-0020).
impacto: Baixo. Embora a substância das regras e critérios de aceite futuros esteja descrita de forma robusta e verificável nas próprias decisões e consequências, a ausência das seções dedicadas quebra ligeiramente a consistência visual e o padrão organizacional das ADRs mais recentes do repositório.
correcao_necessaria: Recomenda-se que, no ciclo documental de aplicação (APLICAR_ADR) ou em um patch documental corretivo futuro, sejam estruturados de forma destacada os critérios objetivos que governarão a validação do handoff de implementação decorrente da ADR-0021.
```

### Achado 2 — Estado/Rastreabilidade

```yaml
id: ACHADO_02_INDICE_ADR_NAO_ATUALIZADO
severidade: observacao
titulo: Índice de ADRs desatualizado em relação à criação da ADR-0021
evidencia: O arquivo docs/adr/INDICE_ADR.md não registra a ADR-0021 em sua lista de decisões registradas.
decisao_ou_autoridade_afetada: docs/adr/INDICE_ADR.md
impacto: Nenhum para esta etapa. A atualização do índice de ADRs pertence exclusivamente à etapa documental seguinte de aplicação (APLICAR_ADR), não constituindo um defeito de escrita ou concepção da ADR-0021 em si.
correcao_necessaria: Garantir que o índice seja devidamente acrescido com a entrada da ADR-0021 no momento em que se iniciar a etapa processual APLICAR_ADR.
```

---

## 15. Estado Git Final

O estado Git final do repositório após a execução desta auditoria permanece rigorosamente intacto e em conformidade com as restrições impostas:

* O arquivo de relatório de QA foi criado em `docs/relatorios/RELATORIO_QA_ADR-0021.md`;
* Nenhum outro arquivo foi criado, alterado, movido, renomeado ou excluído;
* O stage do Git permanece inteiramente limpo (sem arquivos adicionados via `git add`);
* Nenhum commit foi realizado;
* Não houve alteração física na ADR-0021, em contratos, nomenclaturas, código ou testes funcionais do projeto.

---

## 16. Status Final

```text
status_literal: ADR_APPROVED_WITH_NOTES
```

**Justificativa:** A ADR-0021 é fiel, extremamente coerente, não inventa ou assume decisões técnicas não especificadas, preserva a suíte de testes funcionais atual e mapeia de forma exaustiva o plano conceitual de migração estrutural do repositório. Está pronta para ser aplicada. A única observação formal diz respeito ao desvio menor de layout em relação aos cabeçalhos dedicados de critérios de aplicação, o qual não impede o seu aproveitamento e aceitação imediata.

---

## 17. Próxima Categoria Processual

```text
proxima_categoria: APLICAR_ADR
```

**Justificativa:** Sendo a ADR-0021 aprovada com notas de QA, a próxima etapa processual materialmente adequada é o ciclo de aplicação documental e atualização de contratos (`APLICAR_ADR`), que atualizará os documentos de nomenclatura, índice e contratos apontados pela rastreabilidade da ADR, preparando o repositório para o subsequente handoff físico de implementação.

---

## Saída Padrão no Relatório

```text
status_literal: ADR_APPROVED_WITH_NOTES
status_normalizado: ADR_APPROVED_WITH_NOTES
relatorio: docs/relatorios/RELATORIO_QA_ADR-0021.md
achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 1
observacoes: 2
git: clean_with_report
proxima_categoria: APLICAR_ADR
```
