# QA do handoff H-0029

## 1. Identificação

*   **Identificador do Handoff:** H-0029
*   **Título:** Distribuição de containers com cardinalidade unitária
*   **Ciclo Atual:** H-0029
*   **Status Declarado no Handoff:** READY_FOR_IMPLEMENTATION (Status normalizado atual: HANDOFF_CREATED)
*   **Data do Relatório de QA:** 2026-07-12
*   **Auditor:** opencode (Auditor de QA Independente)

## 2. Arquivos e autoridades consultadas

Para a elaboração desta auditoria de QA, foram lidos e analisados integralmente os seguintes documentos:

1.  **Handoff de Entrada:**
    *   `scripts/docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md`
2.  **Evidência de Levantamento Motivadora:**
    *   `scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_OCUPACAO_CORPO_STUB_B_DESTINO_MINIMO.md`
3.  **Contratos Ativos e Normas:**
    *   `scripts/docs/contratos/contrato_composicao_corpo.md`
4.  **Decisões Arquiteturais (ADRs) Ativas:**
    *   `scripts/docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`
    *   `scripts/docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`
    *   `scripts/docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md`
    *   `scripts/docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md`
5.  **Handoffs Anteriores (Integridade e Suporte Histórico):**
    *   `scripts/docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md`
    *   `scripts/docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md`
    *   `scripts/docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md`
    *   `scripts/docs/handoff/H-0028-matriz-de-grupos-coordenadas-explicitas.md`

## 3. Estado Git observado

A verificação do estado real na raiz do repositório Git foi realizada com o comando:
```bash
git status --short
```

O resultado obtido confirma com precisão milimétrica o estado documental limpo do repositório:
```text
?? scripts/docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md
?? scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_OCUPACAO_CORPO_STUB_B_DESTINO_MINIMO.md
```

Nenhum arquivo de código fonte (`*.py`), JSON de configuração (`config/telas/*.json`), contrato ou documento normativo foi modificado ou rastreado no ciclo atual. A única adição é o arquivo de handoff `H-0029-distribuicao-containers-cardinalidade-unitaria.md` e o relatório de levantamento `RELATORIO_LEVANTAMENTO_OCUPACAO_CORPO_STUB_B_DESTINO_MINIMO.md`.

## 4. Decisão e autoridade

O handoff H-0029 demonstra aderência absoluta e sem concessões às decisões expressas pelo usuário e às autoridades normativas ativas:

*   **Aderência à decisão do usuário:** O H-0029 restringe-se exclusivamente ao escopo de corrigir os erros de distribuição em containers hierárquicos com exatamente um filho (cardinalidade unitária).
*   **Hierarquia e Independência de Níveis:** Preserva inequivocamente que a distribuição declarada em um container atua exclusivamente sobre os filhos diretos deste, sem propagação implícita ou herança automática para ancestrais ou descendentes.
*   **Ausência de Distribuição vs. Distribuição Explícita:** Mantém a separação semântica rígida exigida pela ADR-0018: a ausência de distribuição não se traduz em default implícito para o modo `igual`, preservando o comportamento natural do conteúdo, enquanto a distribuição explícita atua de forma determinística alocando área física útil.
*   **Tratamento do H-0025:** O handoff H-0029 lista adequadamente o H-0025 como precedente, porém não assume sua implementação como garantida ou fechada, em plena conformidade com o cenário histórico não confirmado do H-0025. O handoff extrai regras somente dos contratos e das ADRs ativas superiores, de forma matematicamente segura.

## 5. Escopo positivo e negativo

Os limites de escopo do H-0029 estão descritos de forma rigorosa e inequívoca, eliminando qualquer risco de vazamento de escopo:

*   **Escopo Positivo:** Limitado exclusivamente à reprodução e correção de containers de cardinalidade unitária com distribuição explícita, cobrindo cenários com `igual` com um filho, `fracao [1]` e `percentual [100]`, containers verticais (e horizontais se afetarem o mesmo fluxo), composições de dois ou mais níveis contendo containers unitários, terminais com múltiplas dimensões úteis e área insuficiente.
*   **Escopo Negativo:** Exclui explicitamente qualquer uma das seguintes atividades futuras e não autorizadas:
    *   Criação de novas telas (2x2, 3x2, 2x4).
    *   Substituição ou criação de telas de console único ou dashboard único.
    *   Inclusão de telas no lançador.
    *   Implementação de navegação ou seleção no console.
    *   Execução simulada de ações ou mock de conteúdo a partir de JSONs de teste.
    *   Novas políticas normativas de altura mínima, overflow, truncamento ou paginação.
    *   Qualquer alteração em `orquestrador.json`, `destino_minimo.json` ou `stub_b.json`.
    *   Alterações documentais substantivas em ADRs, contratos ou índices.
    *   Criação de commits ou modificações do histórico Git.

## 6. Definição do defeito

O handoff H-0029 é exemplar ao distinguir com clareza os termos específicos necessários para isolar e sanar o defeito sem prescrever patches especulativos prematuros:

*   Distingue adequadamente: corpo com único elemento funcional, corpo com único grupo, grupo com único elemento funcional, grupo ou corpo com múltiplos elementos, container raiz, grupo aninhado, cardinalidade, arranjo, distribuição, cota recebida do pai e área interna disponível ao filho.
*   Ele proíbe explicitamente que o implementador assuma de antemão qual linha ou função Python contêm o defeito, determinando no item 7 uma rotina de investigação obrigatória que rastreie o cálculo de pesos, cotas, larguras, alturas e passagens de parâmetros antes de aplicar qualquer alteração.

## 7. Cardinalidade unitária e independência entre níveis

A semântica de cardinalidade unitária está formalizada com exatidão matemática:

*   **Atribuição Total:** Determina que um único filho sob distribuição explícita deve receber 100% da área útil disponível no container pai.
*   **Equivalência Geométrica:** Trata `igual` com um filho, `fracao [1]` e `percentual [100]` (quando este último for autorizado e aplicável) como formas geometricamente equivalentes e intercambiáveis de cardinalidade unitária.
*   **Preservação Estrutural:** Assegura que bordas, molduras e preenchimento pertençam à cota calculada, garantindo que a soma exata das cotas coincida perfeitamente com a área distribuível.
*   **Preservação de Cardinalidade > 1:** Garante que comportamentos corretos em containers com dois ou mais filhos permaneçam intactos.
*   **Independência de Níveis:** A distribuição de um container (seja corpo raiz ou grupo) permanece restrita aos seus filhos imediatos, eliminando qualquer risco de expansão indevida ou interferência mútua entre níveis de hierarquia.

## 8. Matriz e estratégia de testes

A matriz mínima de testes especificada na Seção 12 é abrangente, focal e estritamente aderente às necessidades de validação técnica do defeito:

*   **Casos Cobertos:**
    *   Corpo distribuído com um elemento funcional (modos `igual`, `fracao [1]`, `percentual [100]`).
    *   Corpo distribuído com um grupo (e grupo interno sem distribuição).
    *   Corpo sem distribuição e grupo interno com distribuição explícita unitária.
    *   Ambos os níveis com distribuição explícita unitária simultânea.
    *   Preservação de dois ou mais filhos sob distribuição.
    *   Preservação da semântica de ausência de distribuição (altura natural preservada).
    *   Comportamento em múltiplos terminais e área insuficiente determinística.
*   **Isolamento de Testes:** A estratégia de testes divide perfeitamente os testes unitários com estruturas sintéticas, testes de integração loader -> modelo -> renderer com JSON existente, regressões da suíte canônica do projeto e testes focais. Não exige testes dispersos ou sem relação lógica comprovada com a cardinalidade unitária.

## 9. Arquivos permitidos e proibidos

O handoff H-0029 define uma lista fechada de arquivos, mitigando riscos de dispersão de código ou alterações não documentadas:

*   **Arquivos Permitidos:**
    *   `tela/renderizador.py`
    *   `tela/teste_renderizador.py`
    *   `tela/teste_loader.py`
    *   `tela/teste_modelo.py`
    *   `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md`
*   **Restrições e Exceções:**
    *   `tela/loader.py` e `tela/modelo.py` são expressamente proibidos de alteração pré-autorizada. Se a investigação do implementador detectar necessidade material de alterá-los, este deve suspender o trabalho e registrar `ARCHITECTURE_REVIEW_REQUIRED`.
    *   `config/telas/grupo_minimo.json` é a única exceção declarativa permitida sob critérios extremamente estritos: apenas se indispensável para testes de integração com JSON real e validada pelos contratos vigentes.
*   **Arquivos Proibidos:** Todos os demais, incluindo os arquivos normativos ativos (`docs/adr/`, `docs/contratos/`, `docs/NOMENCLATURA.md`), o relatório de levantamento em si, e os JSONs de tela `orquestrador.json`, `destino_minimo.json` e `stub_b.json`.

## 10. Critérios de aceite

Os 17 critérios de aceite listados na Seção 15 do handoff são objetivos, claros, mensuráveis e passíveis de verificação automatizada ou visual precisa:

*   Eles fornecem especificações exatas sobre quantidade total de linhas produzidas, largura física, cota de altura recebida pelo único filho, soma das cotas de distribuição, posicionamento das bordas de moldura e da `barra_de_menus`, ausência absoluta de sobreposição e lacunas externas indevidas.
*   Asseguram a aprovação plena da suíte canônica (1133/1133) e a manutenção das semânticas normativas e preservações.

## 11. Validação automatizada, pseudo-TTY e TTY real

O handoff H-0029 implementa um excelente mecanismo de governança sobre a homologação de layout:

*   **Regra de Aprovação Visual:** Proíbe expressamente o implementador de autoaprovar o layout visual ou declarar homologação baseada apenas em critério humano subjetivo.
*   **Divisão de Camadas:** Separa os testes automatizados unitários/integração do uso opcional de pseudo-TTY (para validar dimensões geométricas específicas) e da validação humana em TTY real.
*   **Garantia de Governança:** Exige obrigatoriamente que, se houver necessidade de validação em TTY real, o relatório registre formalmente:
    ```text
    VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
    ```
    Isso assegura que o usuário final detenha o controle soberano sobre a aprovação estética e operacional.

## 12. Achados

### Achado ACH-01
*   **id:** ACH-01
*   **severidade:** observação
*   **local:** scripts/docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md
*   **regra_ou_autoridade:** Metadados de Status do Handoff
*   **problema:** O arquivo físico de handoff declara em seus metadados `status: READY_FOR_IMPLEMENTATION`, enquanto o ciclo foi apresentado na chamada de prompt atual como `status_literal: HANDOFF_CREATED` / `status_normalizado: HANDOFF_CREATED`.
*   **impacto:** Divergência nominal inofensiva e puramente documental na marcação de estado. Não impacta a implementabilidade técnica, as regras, a lógica ou o escopo do handoff.
*   **correcao_necessaria:** Nenhuma necessária pelo Auditor de QA. O implementador do H-0029 poderá transicionar o status após aprovação deste relatório, ou o repositório pode continuar o fluxo operacional normal de acordo com as instruções da próxima etapa.

## 13. Classificação final

A classificação final atribuída a este handoff é:

**H1_HANDOFF_APPROVED**

*   **Justificativa:** O handoff H-0029 está extraordinariamente bem-estruturado, maduro, robusto, preciso e completo. Ele se alinha integralmente com todas as decisões do usuário e ADRs ativas, define com perfeição o escopo positivo/negativo, a estratégia de testes e critérios objetivos de aceite de forma a guiar o implementador em contexto limpo com absoluto rigor e segurança técnica, sem a necessidade de tomar qualquer decisão arquitetural nova.

## 14. Próxima categoria permitida

A próxima categoria permitida para o fluxo de desenvolvimento do ciclo H-0029 é:

**IMPLEMENTAR**
