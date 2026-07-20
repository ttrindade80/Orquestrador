---
name: RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0028
description: Auditoria pós-patch do processo de aplicação documental da ADR-0028 aos contratos e nomenclaturas do projeto
metadata:
  type: relatorio_qa_pos_patch_aplicacao
  adr: ADR-0028
  data: "2026-07-17"
  status_recebido: APLICACAO_ADR_PATCHED
  status_literal: ADR_APPLICATION_APPROVED_WITH_NOTES
---

# Relatório de QA Pós-Patch da Aplicação — ADR-0028

---

## 1. Identificação

* **Projeto:** Orquestrador
* **Documento Auditado:** `docs/relatorios/RELATORIO_APLICACAO_ADR-0028.md` (versão corrigida) e `docs/contratos/contrato_json_console.md`
* **Etapa:** `QA_POS_PATCH_APLICACAO_ADR`
* **Status Final Literal:** `ADR_APPLICATION_APPROVED_WITH_NOTES`
* **Status Final Normalizado:** `aprovada_com_notas`
* **Data da Auditoria:** 17 de julho de 2026

---

## 2. Objetivo

Auditar de forma independente e focal o patch da aplicação da ADR-0028 para determinar se os achados corretivos identificados no ciclo inicial de QA foram devidamente resolvidos, se o patch permaneceu estritamente dentro do escopo autorizado, se não houve regressões normativas ou alteração de decisões D1–D22, e se a documentação do projeto está pronta para ser considerada formalmente aprovada.

---

## 3. Autoridades

| Documento | Função / Papel |
|---|---|
| `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md` | Autoridade de decisão primária aprovada |
| `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0028.md` | QA inicial da aplicação; fonte dos achados corretivos originais e observações |
| `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0028.md` | QA pós-patch da ADR; referência para preservações e regressões |

---

## 4. Escopo

O escopo desta auditoria está restrito à verificação das correções aplicadas sobre:
1. `docs/relatorios/RELATORIO_APLICACAO_ADR-0028.md` (Correção do achado `APLIC-QA-001`)
2. `docs/contratos/contrato_json_console.md` (Correção do achado `APLIC-QA-002`)

Qualquer outra alteração normativa, comportamental, de código ou de configuração fora deste limite físico de escopo é proibida.

---

## 5. Estado Git

O estado Git atual do workspace foi inspecionado na raiz do projeto:

* **Branch:** master
* **HEAD:** `f6982d0`
* **Whitespace:** `git diff --check` retornou saída limpa, sem erros de whitespace.
* **Arquivos Modificados Rastreáveis (status M):**
  - `docs/NOMENCLATURA.md`
  - `docs/adr/INDICE_ADR.md`
  - `docs/contratos/contrato_barra_de_menus.md`
  - `docs/contratos/contrato_composicao_corpo.md`
  - `docs/contratos/contrato_console.md`
  - `docs/contratos/contrato_json_console.md`
  - `docs/contratos/contrato_tela_json.md`
* **Arquivos Não Rastreáveis (status ??):**
  - `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md`
  - `docs/relatorios/RELATORIO_APLICACAO_ADR-0028.md`
  - `docs/relatorios/RELATORIO_QA_ADR-0028.md`
  - `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0028.md`
  - `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0028.md`

**Análise do Auditor:** O patch de correção permaneceu estritamente restrito aos dois arquivos autorizados (`RELATORIO_APLICACAO_ADR-0028.md` e `contrato_json_console.md`). Os demais arquivos modificados ou não rastreados provêm das etapas anteriores autorizadas e não sofreram alterações decorrentes do patch.

---

## 6. QA de Origem

O relatório de QA inicial da aplicação (`docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0028.md`) declarou status `ADR_APPLICATION_APPROVED_WITH_NOTES`. Contudo, devido aos achados corretivos `APLIC-QA-001` (Médio) e `APLIC-QA-002` (Baixo), o gerente do projeto normalizou o status para `ADR_APPLICATION_REJECTED`, exigindo a emissão de um patch corretivo específico, cujo resultado é auditado neste relatório.

---

## 7. Patch Recebido

O patch recebido foi classificado sob o status literal de `APLICACAO_ADR_PATCHED`. O escopo real de alterações feitas pelo desenvolvedor limitou-se a:
- Ajuste do totalizadores e resumos físicos de contagem de arquivos no relatório de aplicação;
- Expansão de seções normativas no contrato JSON do console para detalhar individualmente os cenários estruturais previstos.

---

## 8. Verificação de APLIC-QA-001

* **Achado Original:** O relatório de aplicação declarava uma contagem incorreta ("7 arquivos modificados + 1 criado") na sua verificação #2, falhando em considerar o arquivo `ADR-0028` como modificado por ele estar em estado não rastreado (`??`) no Git.
* **Ações Corretivas Executadas:**
  - O resumo de verificação #2 da Seção 14 do `RELATORIO_APLICACAO_ADR-0028.md` foi corrigido para: `"Confirmado: 8 arquivos modificados + 1 criado (este relatório) = 9 total"`.
  - A Seção 18 do mesmo relatório foi adicionada para descrever faticamente as ações corretivas.
* **Verificações Focais:**
  - O relatório agora descreve nominalmente os 8 arquivos modificados e 1 arquivo criado, totalizando os 9 arquivos reais.
  - Não restam contagens em conflito (como "7+1", "sete modificados" ou outra expressão divergente).
  - O ADR-0028 está corretamente classificado como modificado pela etapa de aplicação.
  - Não foram incluídos relatórios de QA como criados pela aplicação.
  - A nova Seção 18 do relatório de aplicação registra faticamente o processo de correção pós-QA sem efetuar auto-declaração de aprovação.
* **Classificação:** `CORRIGIDO`

---

## 9. Verificação de APLIC-QA-002

* **Achado Original:** A seção §13.4 de `docs/contratos/contrato_json_console.md` condensava em uma única formulação "em dois ou três níveis" os dois cenários estruturais mínimos de `conjuntos_campos` que deveriam ser tratados como distintos.
* **Ações Corretivas Executadas:**
  - A seção §13.4 de `contrato_json_console.md` foi reescrita e expandida para elencar nominalmente os cenários de dois níveis (conjunto com campos nome-valor) e três níveis (conjunto, subconjunto e campos nome-valor).
  - A redação estabelece que o uso da mesma apresentação não torna as estruturas semanticamente equivalentes e que cada cenário exige demonstração e validação próprias.
* **Verificações Focais:**
  - O cenário de dois níveis aparece nominalmente.
  - O cenário de três níveis aparece nominalmente.
  - Ambos estão expressamente inseridos no modo conceitual `conjuntos_campos`.
  - Foi estabelecido que a igualdade na apresentação visual não gera equivalência semântica.
  - Cada cenário exige demonstração e validação individualizadas.
  - Não foram criados novos valores de schema ou novos modos de apresentação.
  - Não foi fixado um limite global de profundidade rígido igual a 3.
  - Não foi introduzido conteúdo matricial e as especificações de tabela e hierarquia indentada permaneceram intocadas pelo patch.
* **Classificação:** `CORRIGIDO`

---

## 10. Tratamento de APLIC-QA-003

* **Observação Original:** Coexistência das seções 14 e 22 de `docs/contratos/contrato_barra_de_menus.md` contendo referências ao chip `[V]` sem indicação de referência cruzada recíproca.
* **Ações Corretivas Executadas:** Nenhuma (o patch não estava autorizado a modificar este arquivo).
* **Verificações Focais:**
  - O arquivo `docs/contratos/contrato_barra_de_menus.md` não sofreu qualquer alteração pelo patch (conforme verificado em diff local).
  - O chip `[V] Verboso` não foi alterado de nomenclatura.
  - A tecla `V` não recebeu novas semânticas de comportamento.
  - Nenhuma referência cruzada foi adicionada artificialmente.
  - A observação continua em seu estado original não corretivo, sem produzir qualquer contradição normativa material no projeto.
* **Classificação:** `OBSERVACAO_PRESERVADA`

---

## 11. Inventário Real

O inventário real e fático resultante da consolidação pós-patch é o seguinte:

### 11.1 Arquivos Modificados Durante a Etapa de Aplicação
1. `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md`
2. `docs/adr/INDICE_ADR.md`
3. `docs/NOMENCLATURA.md`
4. `docs/contratos/contrato_json_console.md`
5. `docs/contratos/contrato_console.md`
6. `docs/contratos/contrato_tela_json.md`
7. `docs/contratos/contrato_composicao_corpo.md`
8. `docs/contratos/contrato_barra_de_menus.md`

### 11.2 Arquivos Criados Durante a Etapa de Aplicação
9. `docs/relatorios/RELATORIO_APLICACAO_ADR-0028.md`

### 11.3 Total Consolidados
* **Modificados:** 8
* **Criados:** 1
* **Total Geral:** 9

---

## 12. Ausência de Regressão

A auditoria confirma que o patch não introduziu qualquer tipo de regressão normativa sobre os pilares fundamentais estabelecidos pelo projeto e pela ADR-0028:

* **Escopo:** Mantido estritamente para o console e conteúdos multiníveis, livre de conteúdos matriciais ou generalizações indevidas para dashboard ou lançadores.
* **Origem dos dados:** Mantida a separação rigorosa em JSON externo armazenado em arquivo (atual) ou gerado faticamente via pipeline (futuro), preservando a fronteira em JSON estável.
* **Separação dos documentos:** O carregamento continua separado e a entrega conjunta, sendo explicitamente proibida a fusão de documentos ou cópia de dados dinâmicos para o JSON estrutural.
* **Apresentações:** Tabela multinível, hierarquia indentada e conjuntos com campos continuam especificados de forma determinística e com cenários estruturais de dois e três níveis nominalmente distinguidos.
* **Modos visuais:** Alternância interativa, reversível, isolada por console e de sessão por tecla `V` ou chip `[V] Verboso` mantida intacta e não persistente.

---

## 13. Fidelidade do Relatório de Aplicação

O relatório de aplicação `RELATORIO_APLICACAO_ADR-0028.md` reflete fielmente os arquivos reais pós-patch:
- Descreve nominal e categoricamente os arquivos afetados de forma coerente com o Git;
- Documentou a correção pós-QA de `APLIC-QA-001` e `APLIC-QA-002` em seção apropriada (§18);
- Preservou o histórico de decisões e status das ADRs sem adulterar o fluxo original de QA;
- Não declarou auto-aprovação fática;
- Manteve as decisões D1–D22 e as decisões adiadas íntegras e coerentes com a realidade do repositório.

---

## 14. Decisões D1–D22

Todas as decisões D1 a D22 estabelecidas pela ADR-0028 foram rigorosa e adequadamente propagadas pelas seções dos contratos sem qualquer atenuação ou desvio semântico do seu escopo aprovado:
- **D1–D3 (Fronteiras JSON):** Confirmado (`contrato_tela_json.md` §33, `contrato_console.md` §21, `contrato_json_console.md` §13.10).
- **D4–D7 (Tipos e Estrutura):** Confirmado (`contrato_json_console.md` §13.2-13.4, `docs/NOMENCLATURA.md` §19.2).
- **D8 (Demonstrações):** Confirmado (`contrato_json_console.md` §13.11).
- **D9–D13 (Modos, Alternância, Início):** Confirmado (`contrato_json_console.md` §13.5-13.6, `contrato_console.md` §21.2-21.7).
- **D14 (Renderer):** Confirmado (`contrato_json_console.md` §13.10, `contrato_composicao_corpo.md` §12).
- **D15–D17 (Apresentações):** Confirmado (`contrato_json_console.md` §13.4).
- **D18–D20 (Word Wrap, Paginação, Impossibilidade):** Confirmado (`contrato_json_console.md` §13.6-13.8).
- **D21–D22 (Validações e Testes):** Confirmado (`contrato_json_console.md` §13.9, §13.11).

---

## 15. Decisões Adiadas

Nenhuma decisão originalmente adiada pela ADR-0028 §43 foi preenchida ou tomada faticamente no patch:
1. Nomes definitivos das propriedades JSON;
2. Versão do schema;
3. Valores de modo inicial padrão (ausência continua descrita como comportamento indefinido);
4. Marcador padrão de truncamento;
5. Estilos obrigatórios de designador;
6. Limites máximos de profundidade;
7. Fallback global de impossibilidade;
8. Navegação concreta;
9. Mensagens de validação;
10. Protocolo de integração, transporte, persistência e timeouts do Pipeline.

---

## 16. Escopo Negativo

Não houve qualquer transgressão do escopo negativo da ADR-0028. Nenhuma implementação em código, modificação de arquivos alheios à aplicação ou invenção conceitual foi executada.

---

## 17. Novos Achados

Uma inspeção minuciosa dos arquivos alterados no patch não revelou novos desvios, inconsistências textuais ou contradições materiais.

* **APLIC-QAPP-001:** Não identificado.
* **APLIC-QAPP-002:** Não identificado.

---

## 18. Conclusão

O patch documental da aplicação da ADR-0028 foi executado com precisão e conformidade regulamentar integral.
- O erro de contagem foi saneado, estabelecendo faticamente 9 arquivos envolvidos (`APLIC-QA-001` - Corrigido).
- Os cenários de conjuntos e campos foram divididos nominalmente, preservando suas identidades estruturais distintas (`APLIC-QA-002` - Corrigido).
- A observação não corretiva de barra de menus foi rigorosamente preservada sem alterações indevidas de escopo (`APLIC-QA-003` - Preservada).
- Não há novos achados corretivos ou regressões.

A aplicação documental da ADR-0028 está declarada formalmente aprovada com notas (devido à coexistência da tecla V sem referência cruzada em barra de menus, que é uma observação não corretiva legítima).

---

## 19. Status Literal

```text
ADR_APPLICATION_APPROVED_WITH_NOTES
```

---

## 20. Status Normalizado

```text
aprovada_com_notas
```

---

## 21. Próxima Categoria

```yaml
proxima_categoria: CRIAR_HANDOFF
```

(Fim do Relatório)
