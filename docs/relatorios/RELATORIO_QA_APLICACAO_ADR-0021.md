---
name: RELATORIO_QA_APLICACAO_ADR-0021
description: Relatório de auditoria de qualidade da aplicação da ADR-0021 nos documentos normativos ativos
metadata:
  type: relatorio_qa_aplicacao
  etapa: QA_APLICACAO_ADR
  status: CONCLUIDO
  data: "2026-07-14"
---

# RELATÓRIO DE QA — Auditoria da Aplicação da ADR-0021

## 1. Identificação

* **Artefato auditado:** Aplicação da ADR-0021 nos documentos normativos ativos autorizados
* **Relatório de aplicação correspondente:** `docs/relatorios/RELATORIO_APLICACAO_ADR-0021.md`
* **Relatório produzido:** `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0021.md`
* **Data da auditoria:** 14 de Julho de 2026
* **Papel:** Auditor documental independente
* **Status formal atribuído:** `ADR_APPLICATION_APPROVED`

---

## 2. Objetivo e Limites

**Objetivo:** Auditar formalmente o resultado do ciclo `APLICAR_ADR` para a ADR-0021. Esta auditoria valida se a propagação das decisões de separação estrutural (demonstração, produto real, motor compartilhado), política de caminhos de telas e organização de configurações gerais foi executada com precisão absoluta, sem contradições, sem implementações físicas antecipadas e com total fidelidade do relatório de aplicação contra o diff real e o estado Git.

**Limites da etapa:** Esta etapa é estritamente de garantia de qualidade (QA) da aplicação documental. Não está autorizada nenhuma etapa substantiva posterior (como implementação física de código, movimentação de arquivos, criação de diretórios ou commits novos).

---

## 3. Estado Git Real x Declarado

A verificação factual do repositório confirma a exatidão das declarações do executor:

* **Raiz operacional:** `/home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador` (coincide com a raiz Git)
* **Branch ativo:** `master` (conforme declarado)
* **HEAD commit:** `0143fd1` (conforme declarado; commit message: `chore: migra orquestrador para repositorio independente`)
* **Stage do Git:** Vazio (sem alterações indexadas)
* **Cometimentos novos:** Nenhum (preservado em `0143fd1`)
* **Alterações de código ou configuração física:** Rigorosamente nenhuma.
* **Correspondência do Diff:** O `git diff` contém exatamente as alterações nos 13 arquivos rastreados listados na declaração e no relatório de aplicação.
* **Artefatos não rastreados do ciclo:**
  - `docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md`
  - `docs/relatorios/LEVANTAMENTO_PREPARACAO_INTEGRACAO_PIPELINE_ORQUESTRADOR.md`
  - `docs/relatorios/RELATORIO_QA_ADR-0021.md`
  - `docs/relatorios/RELATORIO_APLICACAO_ADR-0021.md`
* **Itens adicionais inesperados:**
  Nenhum item adicional inesperado foi produzido pelo ciclo. Para itens existentes fora do rastreamento Git antes do ciclo (diretórios `.agents/` e `.codex/` na raiz operacional):
  ```yaml
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
  ```

---

## 4. Auditoria por Documento Alterado

Abaixo apresenta-se a auditoria de cada um dos 13 arquivos alterados:

```yaml
arquivo: docs/INDICE.md
necessidade_da_alteracao: Sincronizar o mapeamento global da estrutura física esperada e o papel de cada artefato de configuração com a separação estrutural e de caminhos decidida na ADR-0021.
trechos_modificados: Seção "Estrutura esperada" (estruturação futura sob config/ e demo/) e linha "Config" na tabela "Artefatos".
regra_anterior: Arquivos de parâmetros planos em config/; ausência de telas/ ou diretórios novos; pacote tela/ contendo código de testes/demo de forma misturada.
regra_resultante: Define tela/ como motor compartilhado; demo/ como diretório futuro de pontos de entrada da demonstração; config/telas/ como raiz real; config/telas/demo/ como raiz demonstrativa futura; config/layouts/ e config/elementos/ como diretórios de configurações gerais futuras; config/estilo.json mantido no local.
autoridade: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
aderencia: CONFORME
```

```yaml
arquivo: docs/NOMENCLATURA.md
necessidade_da_alteracao: Introduzir as definições da política estrutural da ADR-0021 para diferenciar formalmente a demonstração, o produto real e o motor de tela, além de planejar a localização física dos arquivos de parametrização externa.
trechos_modificados: Nova seção "Política estrutural da ADR-0021 (2026-07-14)" com tabela de glossário; alteração de caminhos na tabela "Status dos artefatos JSON (modelo ADR-0008)"; atualização de referências textuais nas seções 4.4, 5.1.3, 7.1, 7.4, 8.4 e resumos históricos nas seções 10 e 11.
regra_anterior: Definições planas sem separação de escopos de execução (demo x produto real x motor); caminhos de layout e parâmetros de elementos planos diretamente em config/.
regra_resultante: Conceitualização de "motor compartilhado", "aplicação demonstrativa", "produto real", "tela demonstrativa", "tela do produto real", "raiz declarativa da demonstração" e "raiz declarativa do produto". Caminhos futuros de layouts e elementos mapeados formalmente sob config/layouts/ e config/elementos/, marcando que os transicionais e obsoletos herdam essas pastas.
autoridade: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
aderencia: CONFORME
```

```yaml
arquivo: docs/adr/ADR-0008-modelo-configuracao-por-tela.md
necessidade_da_alteracao: Inserir nota de atualização por rastreabilidade, explicitando a coexistência com as duas raízes declarativas introduzidas pela ADR-0021.
trechos_modificados: Introdução da seção "## Nota de atualização — ADR-0021 (2026-07-14)" no início do corpo.
regra_anterior: Modelo declarativo por tela baseado em arquivo único plano por tela, sem regras de raízes por escopo.
regra_resultante: Preserva integralmente a essência histórica da ADR-0008, mas esclarece que as telas passam a ser organizadas em duas raízes distintas (config/telas/<id>.json para o produto real e config/telas/demo/<id>.json para demonstração).
autoridade: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
aderencia: CONFORME
```

```yaml
arquivo: docs/adr/ADR-0009-caminho-formato-jsons-tela.md
necessidade_da_alteracao: Registrar de forma clara a superação parcial da política de raiz canônica única de JSONs de telas, mapeando o papel e a reserva de caminhos de forma robusta.
trechos_modificados: Introdução da seção "## Nota de atualização — ADR-0021 (2026-07-14)" no início do corpo.
regra_anterior: Todo JSON de tela do projeto deve residir estritamente no caminho plano config/telas/<id>.json.
regra_resultante: Superação parcial histórica registrada; config/telas/ permanece reservada para o produto real, enquanto a demonstração passa a usar a nova raiz config/telas/demo/. É estabelecido que a identidade demonstrativa será config/telas/demo/demo.json (id: "demo"), orquestrador.json é reservado ao produto real, e são proibidos aliases ou fallbacks.
autoridade: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
aderencia: CONFORME
```

```yaml
arquivo: docs/adr/INDICE_ADR.md
necessidade_da_alteracao: Registrar formalmente a ADR-0021 na lista histórica de decisões arquiteturais do projeto.
trechos_modificados: Adição de linha dedicada para a ADR-0021 na tabela de decisões.
regra_anterior: Lista de decisões terminava na ADR-0020.
regra_resultante: ADR-0021 registrada como aceita, datada de 2026-07-14, com título e breve resumo das superações de raiz de telas.
autoridade: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
aderencia: CONFORME
```

```yaml
arquivo: docs/contratos/contrato_barra_de_menus.md
necessidade_da_alteracao: Atualizar o contrato da barra de menus para referenciar o caminho futuro de parametrização geral sob o diretório de elementos.
trechos_modificados: Tabela de referências de aparência na seção 2 ("Natureza e escopo"), regra R-5 ("Separação de responsabilidade") e seção "Pendências em aberto".
regra_anterior: Referência a config/barra_de_menus.json.
regra_resultante: Referência ao caminho futuro previsto config/elementos/barra_de_menus.json.
autoridade: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
aderencia: CONFORME
```

```yaml
arquivo: docs/contratos/contrato_cabecalho.md
necessidade_da_alteracao: Atualizar o contrato do cabeçalho para apontar para o novo caminho futuro sob a pasta de elementos.
trechos_modificados: Seção 1 ("Objetivo"), seção 2 ("Natureza"), seção 3 ("Escopo"), seção 4 ("Schema de apresentação"), seção 5 ("Schema - titulo"), seção 6 ("Schema - descricao"), regras R-3, R-4 e critérios de aceitação.
regra_anterior: Referência a config/cabecalho.json.
regra_resultante: Referência ao caminho futuro previsto config/elementos/cabecalho.json, deixando explícito que as propriedades não estão hardcoded.
autoridade: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
aderencia: CONFORME
```

```yaml
arquivo: docs/contratos/contrato_composicao_corpo.md
necessidade_da_alteracao: Atualizar as referências de arquivos de parametrização externa de consoles e lançadores para seus respectivos diretórios futuros conceituais.
trechos_modificados: Seção "Valores parametrizados de layout do console" (seção 5.1), seção 6 ("Lancador") e critérios de validação.
regra_anterior: Referência a config/layout_console.json, config/layout_dado.json e config/lancador.json.
regra_resultante: Referência aos caminhos futuros config/layouts/layout_console.json, config/layouts/layout_dado.json e config/elementos/lancador.json.
autoridade: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
aderencia: CONFORME
```

```yaml
arquivo: docs/contratos/contrato_json_cabecalho.md
necessidade_da_alteracao: Atualizar a especificação do JSON de cabeçalho para coincidir com a nova política de caminhos de parametrizações.
trechos_modificados: Seção "Objetivo", seção 4 ("JSON minimo"), tabela de campos, regras V-5, V-6, seção "Fora de escopo" e critérios de aceitação.
regra_anterior: Referência a config/cabecalho.json.
regra_resultante: Referência ao caminho futuro previsto config/elementos/cabecalho.json, a ser lido em tempo de execução quando criado.
autoridade: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
aderencia: CONFORME
```

```yaml
arquivo: docs/contratos/contrato_json_lancador.md
necessidade_da_alteracao: Atualizar a especificação semântica de validação do destino de navegação do lançador e apontar para o caminho de parâmetros reorganizado.
trechos_modificados: Regra V-7 ("tela_destino é campo declarativo válido") e seção "Fora de escopo".
regra_anterior: Validava existência estritamente em config/telas/<tela_destino>.json; referenciava config/lancador.json.
regra_resultante: Valida a existência do JSON de destino na raiz declarativa explícita do ponto de entrada correspondente (config/telas/ para produto real, config/telas/demo/ para demonstração). Referencia o caminho futuro previsto config/elementos/lancador.json.
autoridade: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
aderencia: CONFORME
```

```yaml
arquivo: docs/contratos/contrato_json_tela_minima.md
necessidade_da_alteracao: Atualizar a política estrutural de caminhos e regra de coincidência de ID do envelope declarativo da tela para suportar as duas raízes declarativas concorrentes e suas restrições.
trechos_modificados: Seção 7 ("Caminhos canônicos e regra de coincidência de id") e critérios de aceite.
regra_anterior: Caminho canônico único config/telas/<id>.json; exemplo de id correspondia a orquestrador.json na pasta comum.
regra_resultante: Estipula duas raízes (config/telas/ e config/telas/demo/); coincidência obrigatória do ID nas duas raízes; define id: "demo" em config/telas/demo/demo.json como identidade demonstrativa; reserva orquestrador.json ao produto real sem conteúdo definido; proíbe aliases e fallbacks.
autoridade: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
aderencia: CONFORME
```

```yaml
arquivo: docs/contratos/contrato_lancador.md
necessidade_da_alteracao: Atualizar todas as menções à fonte de parametrização de layout do tipo lançador para a nova localização estrutural futura de elementos.
trechos_modificados: Seção 2 ("Natureza"), seção 5.2 ("Espaco chip-texto"), seção 6.5 ("Alinhamento horizontal"), regra R-6 ("Proibição de hardcoding"), critérios de aceitação e seção "Pendências em aberto".
regra_anterior: Referência a config/lancador.json.
regra_resultante: Referência ao caminho futuro previsto config/elementos/lancador.json.
autoridade: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
aderencia: CONFORME
```

```yaml
arquivo: docs/contratos/contrato_tela_json.md
necessidade_da_alteracao: Mapear a localização física da declaração de telas nos novos caminhos de raízes concorrentes e formalizar as restrições associadas ao loader.
trechos_modificados: Introdução da seção "Natureza do tela.json" com a política da ADR-0021.
regra_anterior: Sem especificação explícita de localização física das telas ou divisão de raízes declarativas.
regra_resultante: Define caminhos de produto real (config/telas/<id>.json) e demonstração (config/telas/demo/<id>.json), o uso explícito de cada uma dependendo do ponto de entrada e as proibições estritas de fallbacks silenciosos, buscas ambíguas e duplicações.
autoridade: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
aderencia: CONFORME
```

---

## 5. Documentos Inspecionados Sem Alteração

A decisão de não alterar os documentos abaixo foi rigorosamente auditada e está correta:

* **`docs/contratos/contrato_chip.md`**
  - *Ocorrências relacionadas:* Referencia `config/estilo.json` nas linhas 49 e 321.
  - *Natureza:* Especifica que a aparência visual dos chips é derivada da biblioteca global `config/estilo.json`.
  - *Justificativa de não alteração:* Totalmente conforme. Como `config/estilo.json` foi explicitamente preservado em seu caminho plano e original pela decisão D9 da ADR-0021, o contrato não sofreu impacto estrutural em seus caminhos.
  - *Resíduo normativo:* Nenhum.

* **`docs/contratos/contrato_estilo.md`**
  - *Ocorrências relacionadas:* Múltiplas referências explícitas a `config/estilo.json` como fonte canônica de presets de borda e chip.
  - *Natureza:* Contrato do módulo de estilo universal.
  - *Justificativa de não alteração:* Totalmente conforme. Em consonância com a decisão D9 da ADR-0021, o arquivo `config/estilo.json` não foi movido, preservando a integridade integral das regras descritas neste contrato.
  - *Resíduo normativo:* Nenhum.

* **`docs/contratos/contrato_json_barra_de_menus.md`**
  - *Ocorrências relacionadas:* Nenhuma referência literal de caminho física de parametrização geral é declarada neste contrato.
  - *Natureza:* Define estritamente o formato/schema interno da seção `barra_de_menus` no JSON de tela de cada instância.
  - *Justificativa de não alteração:* Totalmente conforme. As alterações de caminhos físicos de arquivos gerais em `config/` (como a introdução de `config/elementos/barra_de_menus.json`) não afetam o schema mínimo ou o comportamento das instâncias declaradas no próprio `tela.json`. Por ser um contrato estrito de schema de instância, sua não alteração é tecnicamente impecável.
  - *Resíduo normativo:* Nenhum.

A ausência de contradições ativas ou regras remanescentes incorretas nesses três contratos confirma a completude e robustez da aplicação documental.

---

## 6. Relatório de Aplicação

O relatório de aplicação (`docs/relatorios/RELATORIO_APLICACAO_ADR-0021.md`) é um artefato de altíssima fidelidade. Uma conferência ponto a ponto do relatório de aplicação contra o diff real gerou as seguintes constatações:

1. **Identificação:** Presente e correta, identificando a etapa `APLICAR_ADR`, a ADR-0021 e o relatório de QA da ADR com status `ADR_APPROVED_WITH_NOTES`.
2. **Objetivo e limites:** Perfeitamente delimitados. O relatório atesta com precisão que não houve movimentação física, criação de diretórios ou implementações de código de runtime antecipadas.
3. **ADR e QA de autoridade:** Correto, indicando a incorporação por rastreabilidade das notas do QA de autoridade.
4. **Estado Git inicial:** Fiel e convergente com o estado factual no início do ciclo (HEAD `0143fd1`, stage limpo).
5. **Documentos inspecionados:** Lista de forma exaustiva todas as autoridades e documentos lidos.
6. **Documentos alterados:** A lista declarada de 13 arquivos rastreados coincide de forma absoluta e literal com o diff real do Git.
7. **Documentos autorizados não alterados:** Apresenta justificativa sólida e tecnicamente precisa para a não alteração dos contratos de estilo, chips e JSON da barra de menus.
8. **Propagação das decisões:** Mapeia a propagação das decisões estruturais (motor, aplicação demonstrativa, duas raízes declarativas, caminhos de layouts/elementos, etc.) aos respectivos arquivos de destino de forma impecável.
9. **Tratamento da ADR-0008:** Documenta com precisão a inserção da nota de atualização datada.
10. **Tratamento da ADR-0009:** Documenta com precisão o registro da superação parcial e as regras de reserva do ID e caminho.
11. **Atualização dos índices:** Registra fidedignamente o acréscimo da linha na tabela de ADRs em `INDICE_ADR.md` e a reorganização geométrica dos diretórios conceituais futuros em `INDICE.md`.
12. **Nomenclatura:** Reflete o acréscimo das definições de terminologias e caminhos futuros na nomenclatura.
13. **Contratos:** Descreve com maestria as alterações pontuais em cada um dos contratos afetados, alinhados com o diff real.
14. **Critérios objetivos da aplicação da ADR-0021:** Apresenta uma tabela de critérios de verificação extremamente rica e auditável.
15. **Busca de referências antes e depois:** Fornece comandos reais do `rg` e as respectivas classificações e resíduos observados de forma transparente.
16. **Resíduos históricos preservados:** Identifica as razões legítimas para preservação de menções antigas em arquivos históricos e corporações de ADRs originais.
17. **Fatos NAO_CONFIRMADOS:** Mapeia de forma honesta e factual itens cujo runtime ou destino permanecem pendentes ou não confirmados.
18. **Itens fora de escopo preservados:** Preserva a defensibilidade do escopo negativo de forma convergente com as restrições da ADR.
19. **Arquivos alterados:** Lista literal idêntica.
20. **Estado Git final:** Registra as expectativas de arquivos rastreados modificados e não rastreados gerados.
21. **Bloqueios:** Registra "nenhum" de forma correta.
22. **Conclusão:** Finaliza o artefato de forma profissional e coesa.

O relatório de aplicação é, portanto, uma peça documental exemplar de controle e auditoria e é considerado **totalmente fiel** ao diff real.

---

## 7. Status Final

```text
status_literal: ADR_APPLICATION_APPROVED
```

**Justificativa:** A aplicação da ADR-0021 foi realizada com precisão metodológica excepcional. Todas as decisões arquiteturais foram perfeitamente propagadas aos documentos normativos afetados, os conceitos de motor compartilhado e escopos de execução foram adequadamente destacados e os contratos atualizados com foco estritamente futuro e conceitual, resguardando o repositório de qualquer quebra prematura ou acoplamento nocivo. O relatório de aplicação é integralmente fiel ao diff físico real do Git.

---

## 8. Próxima Categoria Processual

```text
proxima_categoria: BASE_DOCUMENTAL_APROVADA
```

**Justificativa:** A aplicação documental da ADR-0021 foi aprovada. A base documental governada por essa ADR está aprovada, sem patch da aplicação pendente. Essa decisão não autoriza implementação física direta: a próxima atividade substantiva será determinada pelo gerente conforme as decisões ainda reservadas à segunda ADR e o fluxo documental obrigatório, incluindo a conclusão da segunda ADR e do fluxo documental correspondente antes de qualquer handoff abrangente de implementação.

---

## Saída Padrão no Relatório

```text
status_literal: ADR_APPLICATION_APPROVED
status_normalizado: ADR_APPLICATION_APPROVED
relatorio: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0021.md
achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 0
observacoes: 0
git: clean_with_report
proxima_categoria: BASE_DOCUMENTAL_APROVADA
```
