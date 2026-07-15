---
name: RELATORIO_QA_ADR-0022
description: Relatório de auditoria de qualidade da ADR-0022 - Ponto de entrada e tela inicial real do Orquestrador
metadata:
  type: relatorio_qa_adr
  etapa: QA_ADR
  status: CONCLUIDO
  data: "2026-07-14"
---

# RELATÓRIO DE QA — Auditoria Documental da ADR-0022

## 1. Identificação

* **Artefato auditado:** `docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md` (ADR-0022 - Ponto de entrada e tela inicial real do Orquestrador)
* **Relatório produzido:** `docs/relatorios/RELATORIO_QA_ADR-0022.md`
* **Data da auditoria:** 14 de Julho de 2026
* **Papel:** Auditor documental independente
* **Status formal atribuído:** `ADR_APPROVED`

---

## 2. Objetivo e Limites

**Objetivo:** Auditar formalmente a ADR-0022 contra as decisões explícitas do usuário, a ADR-0021 aprovada e aplicada documentalmente, os contratos normativos ativos, as ADRs relacionadas, o estado físico real do repositório e o escopo negativo definido. Esta auditoria assegura que o projeto da ADR-0022 é fiel, coerente e livre de invenções técnicas prematuras ou acoplamentos indevidos, estando pronto para aprovação.

**Limites da etapa:** Esta etapa é estritamente de garantia de qualidade (QA) e auditoria documental (`QA_ADR`). Nenhuma correção direta da ADR, aplicação de suas decisões aos documentos de destino, criação de arquivos substantivos (como `orquestrador.py` ou JSON de tela real), execução de código, movimentações físicas ou commits novos estão autorizados nesta etapa.

---

## 3. Estado Git Inicial

A verificação factual do repositório no início desta etapa gerou os seguintes registros:

* **Raiz operacional:** `/home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador` (coincidente com a raiz Git)
* **Branch ativo:** `master`
* **HEAD commit:** `0143fd1` (commit message: `chore: migra orquestrador para repositorio independente`)
* **Stage do Git:** Vazio (nenhuma alteração indexada para commit)
* **Alterações de código ou configuração física de runtime:** Nenhuma.
* **Cometimentos novos:** Nenhum (preservado em `0143fd1`)
* **Alterações na árvore de trabalho rastreadas:** 13 arquivos modificados decorrentes do ciclo documental concluído da ADR-0021.
* **Novos arquivos não rastreados encontrados (untracked):**
  - `docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md`
  - `docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md` (artefato principal desta auditoria)
  - `docs/relatorios/LEVANTEMENTO_PREPARACAO_INTEGRACAO_PIPELINE_ORQUESTRADOR.md`
  - `docs/relatorios/RELATORIO_APLICACAO_ADR-0021.md`
  - `docs/relatorios/RELATORIO_QA_ADR-0021.md`
  - `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0021.md`

Qualquer item não rastreado adicional pré-existente (como diretórios `.agents/` ou `.codex/` se houver) é classificado sob o controle padrão:
```yaml
origem: NAO_CONFIRMADA
produzido_pelo_executor: NAO_CONFIRMADO
produzido_pelo_usuario: NAO_CONFIRMADO
```

---

## 4. Autoridades Consultadas

Os seguintes documentos normativos ativos e relatórios homologados foram lidos integralmente e serviram de base analítica para esta auditoria:

1. `docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md` (Aceita e base para a política de caminhos concorrentes)
2. `docs/relatorios/RELATORIO_QA_ADR-0021.md` (QA de autoridade da ADR-0021)
3. `docs/relatorios/RELATORIO_APLICACAO_ADR-0021.md` (Relatório de aplicação documental da ADR-0021)
4. `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0021.md` (QA da aplicação aprovada com status `ADR_APPLICATION_APPROVED`)
5. `docs/adr/ADR-0008-modelo-configuracao-por-tela.md` (Nota de atualização agregada)
6. `docs/adr/ADR-0009-caminho-formato-jsons-tela.md` (Superação parcial de caminho canônico único)
7. `docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md` (Tiling de elementos do corpo)
8. `docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md` (Barra declarativa por instância de tela)
9. `docs/adr/ADR-0014-barra-horizontal-termos-especificos.md` (Distribuição horizontal responsiva e quebra multilinha)
10. `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md` (Nó estrutural grupo e árvore de até 3 níveis)
11. `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md` (Ausência de distribuição não é igual)
12. `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md` (Cardinalidade de dashboards e limites)
13. `docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md` (Comportamento estrutural de grupo com matriz 2D)
14. `docs/contratos/contrato_json_tela_minima.md` (Formato e campos mínimos do arquivo JSON de tela)
15. `docs/contratos/contrato_tela_json.md` (Contrato macro do schema `tela.v1`)
16. `docs/contratos/contrato_composicao_corpo.md` (Regras de layout de corpo, arranjo e tiling)
17. `docs/contratos/contrato_console.md` (Especificação semântica do container genérico interativo)
18. `docs/contratos/contrato_json_console.md` (Envelope mínimo do console com itens vazios)
19. `docs/contratos/contrato_json_dashboard.md` (Envelope mínimo do dashboard com placeholder)
20. `docs/contratos/contrato_barra_de_menus.md` (Invariantes e comportamento dos chips da barra inferior)
21. `docs/contratos/contrato_json_barra_de_menus.md` (Formato JSON de barra de menus na instância)
22. `docs/contratos/contrato_chip.md` (Metadados conceituais de chip)
23. `docs/contratos/contrato_estilo.md` (Biblioteca universal de presets visuais e cores de terminal)
24. `docs/contratos/contrato_cabecalho.md` (Apresentação e renderização da região fixa superior)
25. `docs/contratos/contrato_json_cabecalho.md` (Campos titulo e descricao no JSON de tela)
26. `docs/contratos/contrato_json_lancador.md` (Campos e validação de tela_destino)
27. `docs/contratos/contrato_lancador.md` (Composição de acionadores de navegação de corpo)
28. `docs/NOMENCLATURA.md` (Manual terminológico de referência unificada)

---

## 5. Estado Físico

A auditoria factual e física do repositório confirma a exatidão das premissas registradas na ADR-0022 sobre o estado atual antes da futura implementação:

1. **`orquestrador.py`:** Não existe fisicamente na raiz do repositório.
2. **`demo/`:** Não existe fisicamente como diretório.
3. **`config/telas/demo/`:** Não existe fisicamente como diretório.
4. **`config/telas/orquestrador.json`:** Existe fisicamente na raiz declarativa plana, mas seu conteúdo atual representa e pertence de fato à demonstração original (a ser futuramente migrada pela ADR-0021 para `config/telas/demo/demo.json`).
5. **Novas telas e código:** Nenhuma tela declarativa real nova foi criada e nenhum código deste ciclo de preparação foi implementado ou alterado.

Esta verificação atesta que a ADR-0022 descreve o estado de transição física futuro de forma impecável, reconhecendo o conflito físico temporário e planejando a resolução sem mentir sobre o estado físico corrente.

---

## 6. Auditoria D1 a D13

As treze decisões fundamentais registradas na ADR-0022 foram avaliadas minuciosamente:

* **D1 — Ponto de entrada real (CONFORME):** Define `orquestrador.py` na raiz do repositório como o ponto de entrada principal do produto real. Exige expressamente a reutilização do motor compartilhado `tela/`. Mantém rigorosamente fora de decisão a assinatura de `main`, os argumentos de linha de comando, as classes, as funções de runtime, os mecanismos de import e o tratamento de erros, preservando o foco meramente declarativo e conceitual.
* **D2 — Identidade da tela real (CONFORME):** Reserva o arquivo `config/telas/orquestrador.json` para o produto real e estipula que seu campo `"id"` deve conter obrigatoriamente o valor literal `"orquestrador"`. O ponto de entrada utilizará a raiz `config/telas/`. Proíbe com clareza a existência de aliases, fallbacks silenciosos ou buscas ambíguas entre as identidades `orquestrador` e `demo`.
* **D3 — Envelope estrutural (CONFORME):** Exige que a tela real seja modelada com base no envelope canônico existente: `cabecalho`, `corpo` e `barra_de_menus`. Preserva os esquemas e contratos existentes de forma precisa, sem tentar introduzir regiões ou elementos inéditos.
* **D4 — Corpo inicial (CONFORME):** Define que o corpo será composto por dois elementos estruturais: `console` e `dashboard`. Ambos devem estar presentes na hierarquia inicial e começar sem dados instanciados de conteúdo. A ADR estabelece explicitamente a distinção crítica entre "elemento estrutural presente" e "conteúdo de exibição vazio", garantindo que "sem entradas" não seja interpretado de forma errônea como a remoção física dos próprios containers do JSON de tela.
* **D5 — Ausência de dados demonstrativos (CONFORME):** Proíbe expressamente a importação ou cópia de dados, textos, consoles de diagnóstico, lançadores demonstrativos, catálogos de demonstração ou qualquer conteúdo fictício para o arquivo real da tela. Exige que a tela real e a demonstrativa sejam arquivos físicos distintos. De forma impecável, a ADR não prescreve o diff textual concreto do JSON de transição atual, deixando esse trabalho para o handoff de aplicação/implementação.
* **D6 — Cabeçalho (CONFORME):** Exige o `cabecalho` declarativo em conformidade com as regras vigentes. Não inventa títulos, descrições, versões fictícias, indicadores dinâmicos ou estado de Pipeline não autorizados pelo usuário. Registra adequadamente que a falta de decisão do usuário sobre os valores de `titulo` e `descricao` concretos (obrigatórios por contrato) constitui um bloqueio processual explícito (`BLOCKED_USER_DECISION`) a ser resolvido no handoff ou por outra autoridade documental, impedindo o executor de preenchê-los por mera suposição arbitrária.
* **D7 — Barra mínima (CONFORME):** Exige que a barra de menus da tela real declare, no mínimo, os chips `Esc`, `?` eStyles (acesso a estilos). Preserva a grafia e papéis canônicos normatizados. Não inventa novos atalhos literais, teclas ou comportamentos.
* **D8 — Item `Estilos` (CONFORME):** Preve o item Styles na barra inicial, mas adverte que a tela funcional correspondente pertence a ciclos posteriores. Proíbe a criação de navegação para destino inexistente, fallback para demonstração ou ações temporárias não decididas. Propõe brilhantemente que o item permaneça visível e inerte se o contrato de barra permitir e, caso as regras de validação vigentes no momento da aplicação exijam obrigatoriamente uma ação de destino cadastrada para todo item visível, a aplicação documental futura deverá parar formalmente com `BLOCKED_USER_DECISION`.
* **D9 — Reutilização do motor (CONFORME):** Proíbe qualquer cópia ou duplicação do loader, renderizador, modelo ou das semânticas de composição. Toda diferença operacional entre a demonstração e o produto real é definida via metadados de configuração e pontos de entrada distintos.
* **D10 — Relação com Pipeline (CONFORME):** Declara formalmente fora de escopo toda a mecânica de integração (processos pai/filho, schemas de mensagens, canais de comunicação, polling, arquivos de troca, falhas). O ponto de entrada real `orquestrador.py` fica apenas conceitualmente preparado na raiz, sem que a integração física seja antecipada.
* **D11 — Demonstração operacional futura (CONFORME):** Define critérios exigentes de demonstração semântica para o handoff de aplicação: comprovação de que a identidade carregada é `orquestrador`, a raiz é a do produto real, a tela `demo` não foi carregada, console e dashboard estão presentes de forma vazia e os chips da barra estão em conformidade. Afirma de forma precisa que código de saída zero isolado é insuficiente e não antecipa fixtures ou comandos de smoke test prematuros.
* **D12 — Handoff condicionado à coesão (CONFORME):** Deixa a cargo do gerente a avaliação futura sobre se a migração física da ADR-0021 e a implementação substantiva da ADR-0022 cabem em um único lote ou devem ser divididas para garantir a auditabilidade. Não impõe amarras prematuras.
* **D13 — Pendências independentes (CONFORME):** Mantém as lacunas históricas `destino_minimo` e `grupo_minimo` de fora da ADR-0022, declarando-as pendentes de análise focada posterior.

---

## 7. Compatibilidade com ADR-0021

A ADR-0022 estabelece uma relação de dependência lógica e hierárquica perfeita com a ADR-0021:

1. **Reutilização do motor:** Coincide na exigência de que `tela/` permaneça como único motor de runtime e que `orquestrador.py` e `demo.py` herdem esse mesmo loader/renderizador sem bifurcações.
2. **Separação física:** Adota a nova política de caminhos de tela concorrentes (produto real em `config/telas/` e demonstração futura em `config/telas/demo/`).
3. **Preservação de Estilo:** Respeita a preservação física e conceitual de `config/estilo.json` sem propor reorganizações paralelas ou movimentações de caminhos antes da futura tela funcional de estilos.
4. **Resolução de Conflitos:** Trata o arquivo `config/telas/orquestrador.json` no estado transicional atual como sendo da demonstração e prevê sua movimentação física futura para `config/telas/demo/demo.json` (mudando seu ID interno para `"demo"`), deixando o caminho original livre para acolher a tela real com o ID `"orquestrador"`.
5. **Inexistência de Aliases:** Não cria aliases nem mecanismos de busca difusos entre os dois escopos, preservando a higienização arquitetural da ADR-0021.

Não há qualquer colisão, reabertura de escopo ou contradição em relação às decisões tomadas e aprovadas na ADR-0021.

---

## 8. Console e Dashboard Vazios

Os contratos vigentes de console e dashboard foram auditados para certificar a viabilidade técnica de sua presença estrutural sem conteúdo ativo:

* **Console Vazio:** O `contrato_json_console.md` (Seção 4) especifica como formato de envelope mínimo válido o campo `itens: []` associado a `origem_dados: null` e `politica_navegacao.navegavel: false`. Essa representação é totalmente compatível com a semântica "sem entradas iniciais" e permite a renderização estéril do container.
* **Dashboard Vazio:** O `contrato_json_dashboard.md` (Seção 4) especifica formalmente que um dashboard sem conteúdo ativo é um envelope que declara `conteudo.tipo: "placeholder"` e `conteudo.binding: null`. Isso define um estado estruturalmente presente, mas semanticamente estéril de dados (conteúdo de reserva), em perfeita harmonia com o escopo da ADR-0022.
* **Coexistência no Corpo:** O `contrato_composicao_corpo.md` e a `ADR-0010` autorizam a coexistência de múltiplos elementos do tipo console e dashboard no mesmo corpo, organizados em arranjo vertical ou horizontal sob o sistema de tiling declarativo.

Desta forma, a exigência da presença inicial de ambos os containers sem entradas é plenamente amparada pelos contratos ativos, sem gerar anomalias ou configurações inválidas de schema.

---

## 9. Cabeçalho

Os contratos de cabeçalho (`contrato_cabecalho.md` e `contrato_json_cabecalho.md`) exigem que o cabeçalho possua os campos textuais `titulo` (string não-vazia) e `descricao` (string presente) como campos obrigatórios de instância de tela.

* **Tratamento de Valores Pendentes:** A ADR-0022 não inventa títulos ou descrições concretas sem autorização do usuário e reconhece expressamente essa lacuna como uma pendência documental.
* **Mitigação Processual:** Para evitar que o executor crie um arquivo de tela real inválido frente ao schema em tempo de implementação, a ADR-0022 institui uma regra de bloqueio explícita: antes de aplicar/implementar fisicamente a tela real, os valores concretos do cabeçalho devem ser definidos por autoridade suficiente ou, caso essa definição seja ausente e considerada indispensável, a aplicação documental futura deverá parar formalmente com `BLOCKED_USER_DECISION`.
* **Conformidade:** Esse desenho processual é extremamente maduro e resguarda a qualidade técnica do projeto sem ocultar ou atropelar as lacunas de escopo.

---

## 10. Barra Mínima

A `barra_de_menus` da tela real inicial proposta pela ADR-0022 deve conter no mínimo `Esc`, `?` e Styles (Acesso a estilos).

* **Representações Canônicas:** Os chips `Esc` e `?` possuem representações, semânticas de rótulo e comportamentos contratuais rigidamente normatizados em `contrato_barra_de_menus.md` (Seção 8 e 9). `Esc` atua de forma contextual (Limpar seleção, Sair ou Voltar) e `?` aciona ajuda. O projeto respeita essas semânticas canônicas de forma irretocável.
* **Acoplamentos:** A ADR-0022 não propõe nenhum atalho físico adicional, símbolo ou ação técnica não contratada, limitando-se ao envelope funcional previsto na barra declarativa por instância (ADR-0012).

---

## 11. Item `Estilos`

O item de acesso a estilos representa um desafio técnico para o formato declarativo puro da barra de menus nesta etapa:

* **Restrição Contratual:** O `contrato_json_barra_de_menus.md` (V-4) e o `contrato_barra_de_menus.md` (Item 20 de validação) exigem que todo chip acionável possua `tecla`, `texto` e `acao` válidos e registrados/whitelisted; a ausência de ação em chip acionável é erro de validação. Por outro lado, a tela de estilos ainda não existe e não há ação registrada ou destino válido para ela.
* **Tratamento Adequado na ADR-0022:** A ADR-0022 resolve esse impasse através de condicionamento explícito:
  - Estipula que o item deve ser visível na barra declarativa.
  - Proíbe a criação de ações temporárias, fallbacks para a demonstração ou caminhos falsos para telas de estilos inexistentes.
  - Exige que o item seja inicialmente declarativo e não navegável, caso as regras ativas de validação o permitam (por exemplo, como um item informativo ou inerte).
  - Caso os validadores e schemas de validação de chips ativos no momento da aplicação exijam obrigatoriamente um destino acionável e não permitam o item inerte, a aplicação futura deverá parar formalmente com `BLOCKED_USER_DECISION`.
* **Conclusão:** Este tratamento processual é impecável. Evita acoplamentos espúrios e garante a conformidade com as regras de validação estritas dos contratos sem forçar soluções improvisadas ou degradadas.

---

## 12. Relação com Pipeline

A ADR-0022 estabelece uma barreira de escopo irretocável em relação ao projeto Pipeline:

* **Limite Declarativo:** Embora `orquestrador.py` seja reservado na raiz do repositório como o ponto de entrada principal do produto real, toda a mecânica de sua integração física e de dados com o Pipeline (processos pai/filho, sincronização, eventos, polling, schemas de mensagens, tratamento de falhas) é declarada explicitamente como fora de escopo.
* **Integridade:** Isso preserva a autonomia e auditabilidade do repositório Orquestrador, permitindo preparar sua identidade visual e estrutural mínima de forma independente e estável antes de iniciar os fluxos de integração interprocessos.

---

## 13. Demonstração Operacional Futura

A ADR-0022 define de forma explícita as condições de contorno e critérios de aceite semânticos para comprovar a eficácia da futura implementação:

* **Suficiência Semântica:** Exige uma prova reproduzível que valide em runtime o carregamento da identidade `orquestrador`, a raiz `config/telas/`, a presença dos containers de console e dashboard vazios e os itens canônicos da barra, além da exclusão de qualquer dado ou carregamento da tela `demo`.
* **Rejeição de Falsos Positivos:** Declara expressamente que a verificação por mero código de saída zero (exit code 0) isolado é insuficiente para aceitação, forçando a implementação futura a produzir evidências factuais das asserções declaradas.
* **Independência de Fixtures:** Não fixa precipitadamente comandos exatos, testes ou ferramentas específicas de TUI para a demonstração, mantendo as opções em aberto para o handoff correspondente.

---

## 14. Documentos Afetados

A identificação de documentos potencialmente afetados listada na ADR-0022 é perfeitamente aderente ao levantamento material e estrutural do projeto:

* **Documentos Mínimos:**
  - `docs/adr/INDICE_ADR.md`
  - `docs/INDICE.md`
  - `docs/NOMENCLATURA.md`
  - `docs/contratos/contrato_json_tela_minima.md`
  - `docs/contratos/contrato_tela_json.md`
  - `docs/contratos/contrato_composicao_corpo.md`
  - `docs/contratos/contrato_console.md`
  - `docs/contratos/contrato_barra_de_menus.md`
  - `docs/contratos/contrato_chip.md`
  - `docs/contratos/contrato_estilo.md`
  - `docs/contratos/contrato_cabecalho.md`

* **Documentos Adicionais Relevantes Mapados:**
  - `docs/contratos/contrato_json_console.md`
  - `docs/contratos/contrato_json_dashboard.md`
  - `docs/contratos/contrato_json_barra_de_menus.md`
  - `docs/contratos/contrato_json_cabecalho.md`
  - `docs/contratos/contrato_lancador.md`
  - `docs/contratos/contrato_json_lancador.md`

Todos os caminhos citados usam a convenção de caminhos relativos partindo da raiz do repositório, sem prefixos de projeto ou caminhos absolutos, em estrito alinhamento com a convenção de caminhos unificada do projeto.

---

## 15. Critérios de Aplicação

Os 12 critérios para a futura aplicação documental listados na ADR-0022 são:

1. Explícitos, objetivos e mensuráveis;
2. Totalmente consistentes com as decisões de separação estrutural e política de caminhos da ADR-0021;
3. Focados rigorosamente nos limites conceituais e normativos da documentação;
4. Suficientes para balizar a implementação substantiva do futuro handoff sem introduzir decisões ou suposições ocultas ou arbitrárias.

Isso assegura que o processo de aplicação seja determinístico e facilmente auditável pela garantia de qualidade em ciclos futuros.

---

## 16. Escopo Negativo

A ADR-0022 define de forma robusta e precisa o escopo negativo, proibindo explicitamente quaisquer decisões ou ações que não pertençam ao escopo exclusivo do registro documental de decisões vigentes:

* **Proibições de Implementação Física:** Não cria, altera, move, renomeia ou remove nenhum arquivo de runtime ou parametrização física (como `orquestrador.py`, `config/telas/orquestrador.json` real, `demo/` ou as pastas de layouts/elementos).
* **Proibições de Escopo Funcional:** Não implementa a tela funcional de estilos, troca de bordas, troca de envelopes de chips, persistência de seleção de estilo, correção de preenchimento ou redimensionamento de containers do corpo, mantendo-os intocados.
* **Proibições de Integração:** Não define assinaturas de funções, argumentos de linha de comando ou protocolos reais do Pipeline.
* **Proibições Processuais:** Proíbe a realização de commits, atualizações de testes físicos, alteração de índices, aplicação das decisões ou handoffs nesta etapa.

O escopo negativo foi rigorosamente respeitado durante todo o artefato, garantindo a sua blindagem metodológica.

---

## 17. Terminologia e Convenção

A ADR-0022 exibe excelente conformidade terminológica e formal:

* **Uso de Termos:** Distingue de forma exemplar "ponto de entrada" (scripts executáveis de boot), "motor compartilhado" (runtime reutilizável em `tela/`) e "tela declarativa" (arquivos de parametrização JSON). Utiliza os termos "demonstração" e "produto real" de forma perfeitamente discriminada.
* **Conformidade de Convenção Formal:** Contém frontmatter YAML completo contendo nome, descrição, metadados e rastreabilidade corretos. O corpo está estruturado de acordo com o template universal de ADRs (Status, Data, Contexto, Problema, Forças e Restrições, Decisões por seção, Consequências positivas/negativas, Compatibilidade, Documentos afetados, Critérios de aplicação, Demonstração operacional, Itens fora de escopo, Pendências, Bloqueios, Relação com handoffs e Controle de alterações).

Não foram identificadas quaisquer quebras de padrão formal ou editorial.

---

## 18. Achados

A auditoria exaustiva não identificou nenhum defeito material, incoerência ou omissão em relação às regras governativas vigentes. Os achados limitam-se a observações normativas ricas de valor para as etapas futuras:

### Observação 01 (Não-bloqueante)
```yaml
id: OBS-001
severidade: observacao
titulo: Nota preventiva sobre dependência do campo regras_exibicao.posicao_dashboard
arquivo: docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md
evidencia: Linhas 121-123 e seções sobre o envelope do corpo estrutural do dashboard.
decisao_ou_autoridade_afetada: docs/contratos/contrato_json_dashboard.md (Seção 4) e ADR-0010.
impacto: Baixo. O contrato do dashboard estipula o campo regras_exibicao.posicao_dashboard como um campo transicional descontinuado e superado pela ADR-0010. A modelagem do corpo da tela real inicial proposta na ADR-0022 deve ter seu posicionamento governado unicamente pelas regras declarativas do corpo (tiling), sem depender deste campo transicional para alinhamento físico.
correcao_necessaria: Nenhuma correção na ADR. Apenas atentar no momento da futura aplicação para que a declaração da tela real de orquestrador não reintroduza o campo descontinuado regras_exibicao.posicao_dashboard como eixo ativo de alinhamento.
```

### Observação 02 (Não-bloqueante)
```yaml
id: OBS-002
severidade: observacao
titulo: Exigência técnica de definição dos campos obrigatórios do cabeçalho
arquivo: docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md
evidencia: Linha 292-315 ("Cabecalho").
decisao_ou_autoridade_afetada: docs/contratos/contrato_json_cabecalho.md (V-2 e V-3).
impacto: Baixo. Os campos titulo (string não-vazia) e descricao (string presente) são campos mínimos obrigatórios em toda tela. O fato de a ADR-0022 deixar esses valores em aberto como pendência do usuário é perfeitamente mitigado pelo gatilho do BLOCKED_USER_DECISION.
correcao_necessaria: Nenhuma correção na ADR. No handoff de aplicação substantiva correspondente, os valores para "titulo" e "descricao" do Orquestrador real devem ser estabelecidos ou gerados de acordo com as instruções diretas do usuário antes da criação física da tela.
```

---

## 19. Estado Git Final

O estado Git após a conclusão e gravação deste relatório de auditoria apresenta-se como segue:

* **Raiz operacional:** `/home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador`
* **Branch ativo:** `master`
* **HEAD commit:** `0143fd1` (sem criação de novos commits)
* **Stage do Git:** Vazio (sem arquivos indexados)
* **Status do Git:**
  - Somente o arquivo `docs/relatorios/RELATORIO_QA_ADR-0022.md` foi adicionado como novo arquivo não rastreado no workspace (`??`).
  - O arquivo auditado `docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md` permanece intacto e sem modificações de conteúdo.
  - Nenhum código, teste físico, JSON substantivo ou arquivo normativo foi alterado, criado ou deletado.

---

## 20. Status Final

```text
status_literal: ADR_APPROVED
```

**Justificativa:** A ADR-0022 é um artefato documental exemplar de alta fidelidade técnica. Ela registra com precisão as decisões relativas ao ponto de entrada real `orquestrador.py` e à tela declarativa real inicial sem antecipar implementações físicas e sem realizar invenções arquiteturais ou de integração com o Pipeline. Suas decisões e limites encontram-se em perfeita harmonia com os contratos ativos e com as definições de separação e política de caminhos da ADR-0021, mitigando de forma limpa as lacunas por meio de regras de bloqueio formal (`BLOCKED_USER_DECISION`).

---

## 21. Próxima Categoria

```text
proxima_categoria: APLICAR_ADR
```

**Justificativa:** A ADR-0022 está formalmente aprovada em auditoria de garantia de qualidade, sem apresentar deficiências materiais de escopo, modelagem ou conflitos arquiteturais. O projeto está pronto para avançar para a sua etapa de aplicação documental (`APLICAR_ADR`), onde suas decisões, consequências, referências de caminhos e critérios serão propagados e integrados formalmente aos documentos normativos e contratos afetados, mantendo-se a proibição estrita de qualquer implementação física nesta fase do ciclo.

---

## Saída Padrão no Relatório

```text
status_literal: ADR_APPROVED
status_normalizado: ADR_APPROVED
relatorio: docs/relatorios/RELATORIO_QA_ADR-0022.md
achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 0
observacoes: 2
git: clean_with_report
proxima_categoria: APLICAR_ADR
```
