---
name: RELATORIO_QA_APLICACAO_ADR-0028
description: Relatório de QA independente da aplicação documental da ADR-0028 aos documentos normativos ativos do projeto
metadata:
  type: relatorio_qa_aplicacao
  adr: ADR-0028
  data: "2026-07-17"
  status: ADR_APPLICATION_APPROVED_WITH_NOTES
---

# Relatório de QA da Aplicação — ADR-0028

---

## 1. Metadados

| Campo | Valor |
|---|---|
| ADR auditada | `ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md` |
| Etapa auditada | `APLICAR_ADR` |
| Relatório de aplicação inspecionado | `docs/relatorios/RELATORIO_APLICACAO_ADR-0028.md` |
| QA anterior | `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0028.md` (status: `ADR_APPROVED_WITH_NOTES`) |
| Data desta auditoria | 2026-07-17 |
| Papel do auditor | Auditor documental independente |
| Status final | `ADR_APPLICATION_APPROVED_WITH_NOTES` |

---

## 2. Identificação da auditoria

Este relatório é produzido por auditor independente da etapa `APLICAR_ADR`. O
auditor não participou da elaboração da ADR-0028, dos ciclos de QA anteriores
nem da execução da aplicação documental.

O objeto desta auditoria é verificar se:

1. Todas as decisões aprovadas da ADR-0028 (D1–D22) foram propagadas de forma
   integral aos documentos normativos ativos;
2. Somente os documentos autorizados foram alterados;
3. As autoridades ativas ADR-0026 e ADR-0027 foram preservadas;
4. Nenhuma nova decisão foi introduzida além das já aprovadas;
5. Nenhuma decisão adiada foi preenchida;
6. Nenhuma implementação foi antecipada;
7. Nenhuma contradição normativa ativa persiste após a aplicação;
8. O relatório de aplicação reflete fielmente o diff real e os documentos reais.

Esta auditoria **não aprova** a aplicação com base apenas no resumo do autor.

---

## 3. Premissas e limitações

- A auditoria parte do HEAD `f6982d0`, estado final após `APLICAR_ADR`.
- O auditor leu diretamente todos os documentos listados na seção 4.
- Os documentos ADR-0028, `RELATORIO_APLICACAO`, `RELATORIO_QA_ADR-0028` e
  `RELATORIO_QA_POS_PATCH_ADR-0028` são arquivos não rastreados (`??`) porque
  foram criados durante os ciclos anteriores (ADR, QA, PATCH_ADR) sem commit.
  Esta condição é esperada e não é anomalia desta etapa.
- O auditor não verificou artefatos de implementação (código, configuração,
  fixtures) porque nenhum deveria ter sido alterado.
- O auditor não tem acesso às intenções do autor da aplicação — apenas ao estado
  dos documentos e ao diff real.

---

## 4. Escopo normativo auditado

| Documento | Tipo | Modificado nesta etapa |
|---|---|---|
| `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md` | ADR aplicada | Sim (untracked modificado) |
| `docs/adr/INDICE_ADR.md` | Índice normativo | Sim (rastreado M) |
| `docs/NOMENCLATURA.md` | Glossário normativo | Sim (rastreado M) |
| `docs/contratos/contrato_json_console.md` | Contrato normativo | Sim (rastreado M) |
| `docs/contratos/contrato_console.md` | Contrato normativo | Sim (rastreado M) |
| `docs/contratos/contrato_tela_json.md` | Contrato normativo | Sim (rastreado M) |
| `docs/contratos/contrato_composicao_corpo.md` | Contrato normativo | Sim (rastreado M) |
| `docs/contratos/contrato_barra_de_menus.md` | Contrato normativo | Sim (rastreado M) |
| `docs/relatorios/RELATORIO_APLICACAO_ADR-0028.md` | Relatório de etapa | Criado (untracked novo) |
| `docs/adr/ADR-0026-...md` | Autoridade ativa | Não modificado |
| `docs/adr/ADR-0027-...md` | Autoridade ativa | Não modificado |
| `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0028.md` | Autorização de aplicação | Não modificado |

---

## 5. Verificação Git

| Verificação | Resultado |
|---|---|
| Branch | master |
| HEAD | f6982d0 (`docs: corrige whitespace do fechamento H-0036`) |
| `git diff --check` | OK — sem erros de whitespace |
| Arquivos com `M` rastreado | 7: `INDICE_ADR.md`, `NOMENCLATURA.md`, `contrato_json_console.md`, `contrato_console.md`, `contrato_tela_json.md`, `contrato_composicao_corpo.md`, `contrato_barra_de_menus.md` |
| Arquivos `??` (não rastreados) | 4: ADR-0028, RELATORIO_APLICACAO, RELATORIO_QA_ADR-0028, RELATORIO_QA_POS_PATCH_ADR-0028 |
| Arquivos de código/configuração alterados | Nenhum — confirmado por inspeção direta |

O ADR-0028 aparece como `??` porque nunca foi commitado (criado nos ciclos
anteriores e não rastreado pelo git). A aplicação documental modificou o ADR
(status, §2, §47), mas o git continua a registrá-lo como `??`. Esta condição
é esperada e não constitui anomalia.

---

## 6. Verificação do relatório de aplicação

### 6.1 Divergência interna de contagem — análise

O `RELATORIO_APLICACAO_ADR-0028.md` apresenta uma inconsistência interna entre
suas seções:

| Fonte | Declaração | Total implícito |
|---|---|---|
| Seção 4 (lista principal) | 8 arquivos alterados + 1 criado | **9** |
| Seção 14, verificação #2 | "7 arquivos modificados + 1 criado (este relatório)" | **8** |
| Seção 15 (Bloqueios) | "9 arquivos da lista autorizada" | **9** |

**Análise do auditor:**

- Os 7 arquivos rastreados com `M` são: `INDICE_ADR.md`, `NOMENCLATURA.md`,
  `contrato_json_console.md`, `contrato_console.md`, `contrato_tela_json.md`,
  `contrato_composicao_corpo.md`, `contrato_barra_de_menus.md`.
- O ADR-0028 é untracked (`??`) mas foi modificado nesta etapa (status atualizado,
  §2 e §47 inseridos). Sua condição de `??` no git não altera o fato de que foi
  alterado pela `APLICAR_ADR`.
- O `RELATORIO_APLICACAO` foi criado nesta etapa (untracked novo).

**Contagem correta:** 8 arquivos alterados (7 rastreados + ADR-0028 untracked) +
1 arquivo criado (RELATORIO_APLICACAO) = **9 total**.

A seção 4 e a seção 15 estão corretas. A verificação #2 (seção 14) erra por
contar apenas os arquivos `M` rastreados, omitindo o ADR-0028 da contagem.

Este achado está registrado como **APLIC-QA-001** (severidade: Médio — inconsistência
no relatório de aplicação, não na aplicação em si).

### 6.2 Declaração de não auto-aprovação

O RELATORIO_APLICACAO declara explicitamente (seção 16): "Este relatório não
declara a aplicação aprovada." — **CONFORME**.

### 6.3 Declaração de ausência de bloqueios

Seção 15 declara: nenhum `BLOCKED_USER_DECISION` e nenhum `BLOCKED_DOCUMENTATION`
foram acionados. O auditor confirma que todos os 9 documentos autorizados foram
alterados. — **CONFORME**.

### 6.4 Decisões adiadas listadas

Seção 12 lista 15 itens adiados, correspondendo aos §43 itens 1–15 da ADR-0028
mais a reconciliação terminológica `modo normal`/`modo não verboso`. O auditor
verifica: a lista está completa e nenhum item adiado foi preenchido. — **CONFORME**.

---

## 7. Verificação da ADR-0028

| Campo verificado | Esperado | Encontrado | Status |
|---|---|---|---|
| `metadata.status` (frontmatter) | `aceita e aplicada` | `aceita e aplicada` | CONFORME |
| §1 tabela de identificação — Status | `aceita e aplicada` | `aceita e aplicada` | CONFORME |
| §2 — referência ao RELATORIO_APLICACAO | Presente | Presente — pointer explícito | CONFORME |
| §47 Histórico — entrada de aplicação | Presente | Presente — entrada datada 2026-07-17 com escopo declarado "D1–D22 propagadas" | CONFORME |
| V-05 sem qualificador "obrigatório" | Ausente | Ausente — `\| V-05 \| Contêiner sem nível filho declarado \| INVÁLIDO \|` | CONFORME |
| §34 — equivalência `modo normal`/`modo não verboso` registrada sem resolução | Presente | Presente — "Diferença adicional: `modo normal` e `modo não verboso`" com adiamento explícito | CONFORME |
| D3/§35.1 — "conjuntamente" com cláusula anti-fusão | Presente | Presente — "Entrega conjunta não implica fusão, cópia ou reinserção de conteúdo" | CONFORME |
| Decisões D1–D22 — presença das seções normativas | §§13–43 | §§13–43 presentes e completos | CONFORME |
| Decisões adiadas §43 | 15 itens | 15 itens presentes | CONFORME |

A ADR-0028 não foi alterada além do previsto (status, §2, §47). Nenhuma nova
decisão foi inserida no corpo normativo. — **CONFORME**.

---

## 8. Verificação do INDICE_ADR.md

| Campo verificado | Status |
|---|---|
| Nova linha de ADR-0028 adicionada | CONFORME |
| Status: `aceita e aplicada` | CONFORME |
| Data: 2026-07-17 | CONFORME |
| Título da linha — completo e fiel ao ADR | CONFORME |
| Posição: após ADR-0027, sem salto numérico | CONFORME |
| ADR-0026 e ADR-0027 — intactas, inalteradas | CONFORME |
| Nenhuma linha removida ou reordenada | CONFORME |
| ADR-0025 — status `aceita e aplicada` — inalterado | CONFORME |

A linha de ADR-0028 no INDICE_ADR.md reproduz fielmente o título completo e o
escopo da ADR, sem truncamentos ou distorções. — **CONFORME**.

---

## 9. Verificação do NOMENCLATURA.md

| Campo verificado | Status |
|---|---|
| Seção 19 criada como seção adicional | CONFORME |
| §19.1 — escopo exclusivo ao `console` com conteúdo multinível | CONFORME |
| §19.2 — 17 termos definidos (lista completa auditada) | CONFORME |
| Termos presentes: `conteúdo multinível do console`, `documento JSON externo de conteúdo`, `modo não verboso`, `modo verboso`, `alternância por V`, `estado visual da sessão`, `modo inicial`, `linha lógica`, `linha física`, `contexto visual repetido`, `contêiner`, `folha`, `campo nome-valor`, `designador`, `escopo de alinhamento`, `[V] Verboso`, `impossibilidade geométrica (multinível)` | CONFORME — todos os 17 termos presentes |
| §19.3 — diferenças terminológicas registradas sem resolução: `folha`/`conteudo`, `campo`/`nome_valor`, `hierarquia_indentada`/`hierarquia` | CONFORME |
| §19.4 — equivalência `modo normal` × `modo não verboso` registrada sem resolução | CONFORME |
| §19.5 — distinções obrigatórias | CONFORME |
| §19.6 — decisões deferidas (8 itens) | CONFORME |
| `modo normal` nas seções anteriores (§6 do contrato_console etc.) — NÃO removido | CONFORME — `modo normal` preservado nas seções pré-existentes |
| Nenhuma nova seção temática criada além da §19 | CONFORME |
| Nenhum termo pré-existente redefinido ou removido | CONFORME |

A seção 19 do NOMENCLATURA.md está completa, coerente com a ADR-0028 e não
altera as seções preexistentes. — **CONFORME**.

---

## 10. Verificação do contrato_json_console.md

| Campo verificado | Status |
|---|---|
| Seção 13 criada | CONFORME |
| §13.1 — escopo exclusivo | CONFORME |
| §13.2 — modelo hierárquico (raiz única) | CONFORME |
| §13.3 — tabela de correspondência: contêiner=`container`, folha=`conteudo`, campo nome-valor=`nome_valor` | CONFORME |
| §13.4 — três modos de apresentação: `tabela`, `hierarquia`, `conjuntos_campos` | CONFORME |
| §13.5 — modo não verboso (6 regras) | CONFORME |
| §13.6 — modo verboso (6 regras) | CONFORME |
| §13.7 — paginação e contexto por apresentação | CONFORME |
| §13.8 — impossibilidade geométrica (delegação a ADR-0017/ADR-0023) | CONFORME |
| §13.9 — validações V-01 a V-15 (tabela completa; V-05 sem "obrigatório") | CONFORME |
| §13.10 — responsabilidades das camadas (ponto de entrada, loader, modelo, renderer) | CONFORME |
| §13.11 — cenários de demonstração obrigatórios | CONFORME |
| §13.12 — remissões cruzadas | CONFORME |
| Nenhum nome de propriedade de schema renomeado | CONFORME |
| Nenhum protocolo Pipeline definido | CONFORME |
| Nenhum conteúdo matricial introduzido | CONFORME |

**Achado APLIC-QA-002 (Baixo):** §13.4 descreve as estruturas `conjuntos_campos`
de dois e três níveis em uma linha combinada ("em dois ou três níveis"), em vez
de separar os dois cenários como a ADR-0028 §§19–20 faz. A remissão explícita
a ADR-0028 §§19–20 preserva o acesso às regras completas; não há contradição
normativa. Registrado como observação — não bloqueante.

Seção 13 conforme. — **CONFORME COM OBSERVAÇÃO (APLIC-QA-002)**.

---

## 11. Verificação do contrato_console.md

| Campo verificado | Status |
|---|---|
| Seção 21 criada | CONFORME |
| §21.1 — escopo exclusivo ao console com conteúdo multinível | CONFORME |
| §21.2 — modo não verboso | CONFORME |
| §21.3 — modo verboso | CONFORME |
| §21.4 — equivalência `modo normal`/`modo não verboso` registrada sem resolução; reconciliação explicitamente adiada | CONFORME |
| §21.5 — alternância pela tecla V | CONFORME |
| §21.6 — estado visual da sessão (lista de proibições de persistência) | CONFORME |
| §21.7 — modo inicial pelo campo `excesso`; ausência = comportamento indefinido (sem valor padrão escolhido) | CONFORME |
| §21.8 — redimensionamento | CONFORME |
| §21.9 — paginação e impossibilidade geométrica | CONFORME |
| §21.10 — remissões cruzadas | CONFORME |
| §6 (`modo normal` como default) — NÃO modificado, preservado integralmente | CONFORME |
| Nenhum conflito entre §6 e §21 — §21 é escopado exclusivamente ao conteúdo multinível | CONFORME |
| Nenhuma generalização para `dashboard` ou `lancador` | CONFORME |

Seção 21 conforme. §6 preexistente intacto. — **CONFORME**.

---

## 12. Verificação do contrato_tela_json.md

| Campo verificado | Status |
|---|---|
| Seção 33 criada | CONFORME |
| §33.1 — JSON estrutural não contém dados de conteúdo multinível | CONFORME |
| §33.2 — JSON estrutural não armazena modo de visualização | CONFORME |
| §33.3 — associação feita pelo ponto de entrada (sem campo de vínculo no JSON estrutural) | CONFORME |
| §33.4 — responsabilidades preservadas (remissão a ADR-0026, ADR-0027) | CONFORME |
| §33.5 — remissões cruzadas | CONFORME |
| Nenhum caminho de fixture, script ou protocolo Pipeline inserido | CONFORME |
| Nenhuma propriedade nova criada no schema do JSON estrutural | CONFORME |

Seção 33 conforme. — **CONFORME**.

---

## 13. Verificação do contrato_composicao_corpo.md

| Campo verificado | Status |
|---|---|
| Seção 12 criada | CONFORME |
| §12.1 — área útil entregue ao console (sem dados de origem) | CONFORME |
| §12.2 — tabela: linha lógica vs. linha física | CONFORME |
| §12.3 — paginação vertical | CONFORME |
| §12.4 — impossibilidade geométrica horizontal; paginação não resolve o horizontal; delegação a ADR-0017/ADR-0023 | CONFORME |
| §12.5 — recuperação após redimensionamento | CONFORME |
| §12.6 — tabela de separação de responsabilidades | CONFORME |
| §12.7 — remissões cruzadas | CONFORME |
| Nenhuma política global de fallback visual criada | CONFORME |
| Nenhuma referência a conteúdo matricial | CONFORME |

Seção 12 conforme. — **CONFORME**.

---

## 14. Verificação do contrato_barra_de_menus.md

| Campo verificado | Status |
|---|---|
| Seção 22 criada | CONFORME |
| §22.1 — existência condicional derivada do `tela.json` (referência a R-3 e seção 20) | CONFORME |
| §22.2 — semântica da alternância (reversível, sem persistência, sem troca de dados) | CONFORME |
| §22.3 — estado de sessão (não gravado em nenhum arquivo) | CONFORME |
| §22.4 — isolamento (não vaza para outra instância) | CONFORME |
| §22.5 — inaplicabilidade fora do escopo (não se aplica a `dashboard`, `lancador`, console sem multinível) | CONFORME |
| §22.6 — posição canônica: mesma posição da seção 7 deste contrato (após chips específicos, antes de `[?]`) | CONFORME |
| §22.7 — remissões cruzadas (contrato_console §21, contrato_json_console §13, NOMENCLATURA §19) | CONFORME |
| Seção 7 (ordem canônica dos grupos de chips) — NÃO modificada | CONFORME |
| Seção 14 (`[V]` modo verboso geral) — NÃO modificada | CONFORME |
| Nenhuma label dinâmica declarada para `[V] Verboso` | CONFORME |
| Nenhuma generalização a outros componentes | CONFORME |

**Observação APLIC-QA-003:** As seções 14 e 22 tratam do chip `[V]` em contextos
distintos (geral vs. multinível) sem referência cruzada entre si. A seção 22.5
é suficiente para delimitar o escopo, mas a ausência de remissão de §22 para §14
(ou vice-versa) pode gerar dúvida na implementação. Registrado como observação
não corretiva — não bloqueante.

Seção 22 conforme. — **CONFORME COM OBSERVAÇÃO (APLIC-QA-003)**.

---

## 15. Preservação das autoridades ativas

### 15.1 ADR-0026

A ADR-0026 (`docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md`)
permanece autoridade ativa sobre:

- separação entre JSON estrutural da tela e documento externo de conteúdo;
- envelope declarativo `{tipo, formato, dados}`;
- princípio de que o console recebe JSON com estrutura independente da origem.

Verificação: nenhum arquivo de decisão da ADR-0026 foi modificado. Os contratos
propagados fazem referência à ADR-0026 como autoridade anterior e preservam suas
fronteiras. — **CONFORME**.

### 15.2 ADR-0027

A ADR-0027 (`docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md`)
permanece autoridade ativa sobre:

- responsabilidade do ponto de entrada pelo carregamento separado e entrega conjunta;
- schema semântico multinível: envelope raiz, três apresentações, três tipos de nível, forma dos nós, designadores;
- 20 validações mínimas.

Verificação: as 20 validações da ADR-0027 não foram alteradas. As validações
V-01 a V-15 da ADR-0028 são declaradas explicitamente como complemento, não como
substituição. A correspondência entre tipos conceituais e nomes de schema
(`container`, `conteudo`, `nome_valor`) foi registrada sem renomear nenhum campo.
— **CONFORME**.

### 15.3 Nenhuma ADR ativa foi substituída ou contradita

Verificação: o INDICE_ADR.md preserva intactas as entradas de ADR-0001 a
ADR-0027. Nenhuma ADR ativa foi marcada como substituída, revogada ou
contraditada pela aplicação da ADR-0028. — **CONFORME**.

---

## 16. Integridade de D1 a D22

| Decisão | Propagada em | Verificação |
|---|---|---|
| D1 — Conteúdo externo ao JSON estrutural | `contrato_tela_json.md` §33.1; `contrato_console.md` §21.1 | CONFORME |
| D2 — Documento JSON como fronteira de consumo | `contrato_json_console.md` §13.1; `contrato_console.md` §21.1 | CONFORME |
| D3 — Carregamento separado e entrega conjunta | `contrato_json_console.md` §13.10; `contrato_tela_json.md` §33.3 | CONFORME |
| D4 — Estrutura independente da apresentação | `contrato_json_console.md` §13.4 | CONFORME |
| D5 — Designadores independentes da estrutura | `docs/NOMENCLATURA.md` §19.2 (`designador`) | CONFORME |
| D6 — Estrutura hierárquica declarada | `contrato_json_console.md` §13.2 | CONFORME |
| D7 — Tipos conceituais de nível | `contrato_json_console.md` §13.3; `docs/NOMENCLATURA.md` §19.2 | CONFORME |
| D8 — Cenários de apresentação multinível | `contrato_json_console.md` §13.11 | CONFORME |
| D9 — Modo não verboso | `contrato_json_console.md` §13.5; `contrato_console.md` §21.2; `docs/NOMENCLATURA.md` §19.2 | CONFORME |
| D10 — Modo verboso | `contrato_json_console.md` §13.6; `contrato_console.md` §21.3; `docs/NOMENCLATURA.md` §19.2 | CONFORME |
| D11 — Alternância pela tecla V | `contrato_console.md` §21.5; `contrato_barra_de_menus.md` §22.2 | CONFORME |
| D12 — Modo inicial | `contrato_console.md` §21.7; `docs/NOMENCLATURA.md` §19.2 (`modo inicial`) | CONFORME |
| D13 — Conteúdo declarativo do JSON | `contrato_json_console.md` §13.5–13.6; `contrato_tela_json.md` §33.2 | CONFORME |
| D14 — Responsabilidade do renderizador | `contrato_json_console.md` §13.10; `contrato_composicao_corpo.md` §12.1–12.5 | CONFORME |
| D15 — Tabela multinível | `contrato_json_console.md` §13.4; `docs/NOMENCLATURA.md` §19.2 | CONFORME |
| D16 — Hierarquia indentada | `contrato_json_console.md` §13.4; `docs/NOMENCLATURA.md` §19.2 | CONFORME |
| D17 — Conjuntos e campos | `contrato_json_console.md` §13.4; `docs/NOMENCLATURA.md` §19.2 | CONFORME |
| D18 — Quebra de palavras | `contrato_json_console.md` §13.6 | CONFORME |
| D19 — Paginação e contexto | `contrato_json_console.md` §13.7; `contrato_composicao_corpo.md` §12.3; `docs/NOMENCLATURA.md` §19.2 | CONFORME |
| D20 — Impossibilidade geométrica | `contrato_json_console.md` §13.8; `contrato_composicao_corpo.md` §12.4; `contrato_console.md` §21.9; `docs/NOMENCLATURA.md` §19.2 | CONFORME |
| D21 — Validações V-01 a V-15 | `contrato_json_console.md` §13.9 | CONFORME |
| D22 — Demonstração e validação | `contrato_json_console.md` §13.11 | CONFORME |

Todas as 22 decisões foram propagadas. Nenhuma decisão foi parcialmente
propagada ou omitida. — **CONFORME**.

---

## 17. Integridade das decisões adiadas

| Item adiado (ADR-0028 §43) | Status na aplicação |
|---|---|
| 1. Nomes definitivos das propriedades do JSON de conteúdo multinível | Adiado — preservado |
| 2. Versão inicial do schema | Adiado — preservado |
| 3. Valores padrão (incluindo modo inicial quando campo ausente) | Adiado — preservado; `contrato_console.md` §21.7 declara "comportamento não definido" |
| 4. Marcador padrão de truncamento | Adiado — preservado |
| 5. Estilos de designador obrigatórios no schema | Adiado — preservado |
| 6. Limites máximos de profundidade | Adiado — preservado |
| 7. Política global de fallback visual para impossibilidade no conteúdo multinível | Adiado — preservado |
| 8. Estratégia concreta de navegação entre páginas | Adiado — preservado |
| 9. Formato de mensagens de validação | Adiado — preservado |
| 10. Protocolo de integração com o Pipeline | Adiado — preservado |
| 11. Comando, repositório e localização do script do Pipeline | Adiado — preservado |
| 12. Transporte do JSON produzido pelo Pipeline | Adiado — preservado |
| 13. Persistência intermediária | Adiado — preservado |
| 14. Timeout | Adiado — preservado |
| 15. Tratamento de falha ou indisponibilidade do Pipeline | Adiado — preservado |
| Reconciliação terminológica `modo normal`/`modo não verboso` | Adiada — registrada sem resolução em NOMENCLATURA.md §19.4 e contrato_console.md §21.4 |

Nenhuma decisão adiada foi preenchida. O item 3 merece nota adicional: a
aplicação registrou que ausência do campo de excesso = comportamento indefinido,
o que é compatível com o adiamento (não é um valor padrão escolhido, é a
ausência de definição explicitamente documentada). — **CONFORME**.

---

## 18. Verificação de ausência de antecipação de implementação

| Verificação | Resultado |
|---|---|
| Nenhum arquivo de código alterado (`.py`, etc.) | CONFIRMADO |
| Nenhum arquivo de configuração alterado (`.json`, `.toml`, etc.) | CONFIRMADO |
| Nenhum fixture alterado ou criado | CONFIRMADO |
| Nenhum handoff criado | CONFIRMADO |
| Nenhum protocolo Pipeline inventado | CONFIRMADO — itens 10–15 de §43 permanecem adiados |
| Nenhum valor padrão escolhido para campo ausente | CONFIRMADO — §21.7 do contrato_console.md declara "comportamento não definido" |
| Nenhum nome de propriedade de schema renomeado ou fixado | CONFIRMADO |
| Nenhum caminho de fixture ou script inserido em contratos | CONFIRMADO |

Nenhuma implementação foi antecipada. — **CONFORME**.

---

## 19. Verificação de ausência de novas decisões implícitas

Verificações realizadas pelo auditor:

1. **Equivalência `modo normal`/`modo não verboso`**: registrada como equivalência
   conceitual observada, com reconciliação explicitamente adiada. Não constitui
   decisão tomada. — CONFORME.

2. **Correspondência tipológica (contêiner/folha/campo → container/conteudo/nome_valor)**:
   registrada como correspondência descritiva para fins de implementação futura,
   sem renomear campos do schema atual. Não constitui nova decisão. — CONFORME.

3. **Impossibilidade geométrica horizontal**: delegação às políticas ADR-0017/ADR-0023
   era prevista pela ADR-0028. Não é nova decisão. — CONFORME.

4. **`[V] Verboso` como chip exclusivo do console multinível**: deriva diretamente
   de D11 e D8. Não é nova decisão. — CONFORME.

5. **Comportamento indefinido quando campo `excesso` ausente**: não é um valor
   padrão escolhido; é o registro explícito da ausência de definição, conforme
   o adiamento do item 3 do §43. Não é nova decisão. — CONFORME.

Nenhuma nova decisão normativa foi introduzida além das 22 aprovadas. — **CONFORME**.

---

## 20. Resolução da divergência na contagem de arquivos

**Divergência identificada** (conforme escopo desta auditoria):

- A lista principal (seção 4 do RELATORIO_APLICACAO) apresenta 8 arquivos
  alterados + 1 criado = 9 total.
- A verificação #2 (seção 14 do RELATORIO_APLICACAO) declara "7 arquivos
  modificados + 1 criado" = 8 total.
- A seção 15 (Bloqueios) cita "9 arquivos da lista autorizada".

**Causa raiz:** O ADR-0028 é arquivo não rastreado (`??`) pelo git, mas foi
modificado nesta etapa. O `git status --short` exibe `??` para esse arquivo, não
`M`. A verificação #2 contou apenas os arquivos com `M` no git (7 arquivos
rastreados), ignorando o ADR-0028 que é `??` mas foi concretamente modificado
durante `APLICAR_ADR`.

**Resolução do auditor:**

A contagem correta, do ponto de vista da etapa `APLICAR_ADR`, é:

- 8 arquivos **alterados**: 7 rastreados com `M` + ADR-0028 (untracked modificado
  nesta etapa)
- 1 arquivo **criado**: `RELATORIO_APLICACAO_ADR-0028.md` (untracked novo)
- **Total: 9 arquivos**

A seção 4 (lista) e a seção 15 (Bloqueios) refletem a realidade. A verificação
#2 da seção 14 é uma contagem incompleta — não falha na aplicação, mas
inconsistência interna do relatório de aplicação.

**Classificação:** APLIC-QA-001 (Médio — inconsistência no instrumento de
verificação, não na aplicação propriamente dita).

---

## 21. Achados identificados

### APLIC-QA-001 — Médio

**Título:** Contagem incorreta na verificação #2 do relatório de aplicação

**Localização:** `docs/relatorios/RELATORIO_APLICACAO_ADR-0028.md`, seção 14,
linha da verificação #2

**Descrição:** A verificação #2 declara "7 arquivos modificados + 1 criado
(este relatório)" = 8 arquivos. A contagem correta é 8 alterados + 1 criado
= 9 arquivos. O ADR-0028 foi modificado nesta etapa (status, §2 e §47
atualizados) mas é contado como ausente por ser `??` no git, não `M`.

**Impacto:** Inconsistência interna do relatório de aplicação. A aplicação
concretamente cobriu todos os 9 arquivos corretos; a falha é apenas na linha
de verificação sumária.

**Bloqueante:** Não.

---

### APLIC-QA-002 — Baixo

**Título:** §13.4 do contrato_json_console.md condensa dois cenários de
`conjuntos_campos` em linha única

**Localização:** `docs/contratos/contrato_json_console.md`, §13.4

**Descrição:** A ADR-0028 §§19–20 distingue os cenários de `conjuntos_campos`
em dois níveis (grupo–campo) e três níveis (grupo–subgrupo–campo) como
estruturas separadas. A seção §13.4 do contrato combina ambos numa linha
"em dois ou três níveis" com remissão a ADR-0028 §§19–20.

**Impacto:** Apresentação condensada, sem contradição normativa. As regras
completas são acessíveis via remissão à ADR-0028.

**Bloqueante:** Não.

---

### APLIC-QA-003 — Observação

**Título:** Seções 14 e 22 do contrato_barra_de_menus coexistem sem
referência cruzada entre si

**Localização:** `docs/contratos/contrato_barra_de_menus.md`, §14 e §22

**Descrição:** A seção 14 (pré-existente) define `[V]` para o console em
geral; a seção 22 (nova) define `[V] Verboso` para demonstrações de conteúdo
multinível. O escopo é delimitado por §22.5, mas não há referência de §22
para §14 (nem o contrário), o que pode causar ambiguidade para implementadores
que encontrem os dois chips com o mesmo rótulo `[V]` em contextos diferentes.

**Impacto:** Risco de ambiguidade na implementação futura. Não há contradição
normativa presente.

**Bloqueante:** Não.

---

## 22. Classificação dos achados

| Código | Severidade | Bloqueante | Descrição resumida |
|---|---|---|---|
| APLIC-QA-001 | Médio | Não | Contagem incorreta na verificação #2 do RELATORIO_APLICACAO (7+1=8 quando correto é 8+1=9) |
| APLIC-QA-002 | Baixo | Não | §13.4 do contrato_json_console comprime dois cenários distintos de conjuntos_campos em linha combinada |
| APLIC-QA-003 | Observação | Não | §14 e §22 do contrato_barra_de_menus coexistem sem referência cruzada entre si |

Nenhum achado bloqueante.

---

## 23. Verificações aprovadas

| Verificação | Resultado |
|---|---|
| Todos os 22 documentos normalizados foram lidos diretamente | APROVADO |
| D1–D22 propagados integralmente | APROVADO |
| ADR-0026 preservada e intacta | APROVADO |
| ADR-0027 preservada e intacta (incluindo 20 validações) | APROVADO |
| V-01 a V-15 complementam, não substituem as 20 validações da ADR-0027 | APROVADO |
| V-05 sem qualificador "obrigatório" | APROVADO |
| `modo normal` não removido do contrato_console.md §6 | APROVADO |
| Equivalências terminológicas registradas sem resolução | APROVADO |
| Nenhum valor padrão para modo inicial escolhido | APROVADO |
| Nenhum protocolo Pipeline definido | APROVADO |
| Nenhuma propriedade de schema renomeada | APROVADO |
| Nenhuma generalização ao `dashboard` ou `lancador` | APROVADO |
| `RELATORIO_APLICACAO` declara explicitamente não auto-aprovar | APROVADO |
| Nenhuma decisão adiada preenchida | APROVADO |
| Nenhum arquivo de código alterado | APROVADO |
| Seção 15 do RELATORIO_APLICACAO lista os 9 arquivos corretamente | APROVADO |
| Remissões cruzadas entre contratos verificadas e corretas | APROVADO |
| ADR-0028 §47 atualizado com entrada de aplicação | APROVADO |
| INDICE_ADR.md linha de ADR-0028 sem erros | APROVADO |
| Nenhuma linha existente do INDICE_ADR.md removida ou alterada | APROVADO |

---

## 24. Verificações com ressalvas

| Verificação | Resultado | Ressalva |
|---|---|---|
| Verificação #2 do RELATORIO_APLICACAO — contagem de arquivos | COM RESSALVA | Declara 7+1=8; correto seria 8+1=9 (APLIC-QA-001) |
| §13.4 — distinção entre cenários de conjuntos_campos | COM RESSALVA | Dois cenários condensados em linha única com remissão cruzada (APLIC-QA-002) |
| §14 e §22 do contrato_barra_de_menus — coexistência do chip [V] | COM RESSALVA | Ausência de referência cruzada entre as seções (APLIC-QA-003) |

---

## 25. Verificações não realizadas / bloqueadas

Nenhuma verificação foi bloqueada. Todos os 13 documentos do escopo normativo
foram lidos diretamente pelo auditor.

---

## 26. Status por documento

| Documento | Status |
|---|---|
| ADR-0028 | CONFORME |
| INDICE_ADR.md | CONFORME |
| NOMENCLATURA.md | CONFORME |
| contrato_json_console.md | CONFORME COM OBSERVAÇÃO (APLIC-QA-002) |
| contrato_console.md | CONFORME |
| contrato_tela_json.md | CONFORME |
| contrato_composicao_corpo.md | CONFORME |
| contrato_barra_de_menus.md | CONFORME COM OBSERVAÇÃO (APLIC-QA-003) |
| RELATORIO_APLICACAO_ADR-0028.md | CONFORME COM ACHADO (APLIC-QA-001 — inconsistência interna na contagem) |

---

## 27. Status por decisão

Todas as decisões D1–D22 foram verificadas individualmente (seção 16). Nenhuma
decisão com status diferente de CONFORME foi identificada.

| Bloco de decisões | Status |
|---|---|
| D1–D3 (fronteiras JSON) | CONFORME |
| D4–D7 (estrutura hierárquica, tipos) | CONFORME |
| D8 (cenários de demonstração) | CONFORME |
| D9–D13 (modos verboso/não verboso, alternância, modo inicial) | CONFORME |
| D14 (responsabilidade do renderizador) | CONFORME |
| D15–D17 (apresentações: tabela, hierarquia, conjuntos) | CONFORME COM OBSERVAÇÃO (D17 / APLIC-QA-002) |
| D18 (quebra de palavras) | CONFORME |
| D19 (paginação e contexto) | CONFORME |
| D20 (impossibilidade geométrica) | CONFORME |
| D21 (validações V-01–V-15) | CONFORME |
| D22 (demonstração e validação) | CONFORME |

---

## 28. Confronto com o relatório de aplicação

| Item declarado no RELATORIO_APLICACAO | Verificado pelo auditor | Resultado |
|---|---|---|
| Status da ADR-0028 atualizado para `aceita e aplicada` | Sim — frontmatter, §1, §2 | CONFIRMADO |
| §47 da ADR-0028 atualizado | Sim — entrada datada 2026-07-17 presente | CONFIRMADO |
| ADR-0028 adicionada ao INDICE_ADR.md | Sim — linha presente e correta | CONFIRMADO |
| Seção 19 criada em NOMENCLATURA.md (17 termos) | Sim — todos os 17 termos verificados | CONFIRMADO |
| Seção 13 criada em contrato_json_console.md (§§13.1–13.12) | Sim — todas as subsecções presentes | CONFIRMADO |
| Seção 21 criada em contrato_console.md (§§21.1–21.10) | Sim — todas as subsecções presentes | CONFIRMADO |
| Seção 33 criada em contrato_tela_json.md (§§33.1–33.5) | Sim — todas as subsecções presentes | CONFIRMADO |
| Seção 12 criada em contrato_composicao_corpo.md (§§12.1–12.7) | Sim — todas as subsecções presentes | CONFIRMADO |
| Seção 22 criada em contrato_barra_de_menus.md (§§22.1–22.7) | Sim — todas as subsecções presentes | CONFIRMADO |
| Nenhum arquivo de código alterado | Sim — confirmado por inspeção | CONFIRMADO |
| ADR-0026 e ADR-0027 preservadas | Sim — INDICE_ADR.md intacto; contratos não alterados | CONFIRMADO |
| Declaração de não auto-aprovação | Sim — seção 16 do RELATORIO_APLICACAO | CONFIRMADO |
| 15 itens adiados listados (§43) | Sim — seção 12 lista 15 itens + reconciliação terminológica | CONFIRMADO |
| Verificação #2: "7 modificados + 1 criado" | PARCIALMENTE — contagem incompleta; correto é 8+1=9 | APLIC-QA-001 |

---

## 29. Confronto com o QA anterior (RELATORIO_QA_POS_PATCH_ADR-0028)

O `RELATORIO_QA_POS_PATCH_ADR-0028.md` autorizou `APPLY_ADR` com status
`ADR_APPROVED_WITH_NOTES`, declarando como corrigidos QA-001 a QA-004.

| Achado do QA pós-patch | Status declarado | Verificado pelo auditor |
|---|---|---|
| QA-001 — D3 vs §35.1 (contradição "conjuntamente"/fusão) | CORRIGIDO | CONFIRMADO — §35.1 usa "conjuntamente" com cláusula "Entrega conjunta não implica fusão" |
| QA-002 — V-05 com "obrigatório" | CORRIGIDO | CONFIRMADO — V-05: `\| Contêiner sem nível filho declarado \| INVÁLIDO \|` sem "obrigatório" |
| QA-003 — §34 sem registro de `modo normal`/`modo não verboso` | CORRIGIDO | CONFIRMADO — §34 contém "Diferença adicional: `modo normal` e `modo não verboso`" com adiamento explícito |
| QA-004 — contrato_barra_de_menus ausente dos `contratos_afetados` | CORRIGIDO | CONFIRMADO — `contrato_barra_de_menus.md` listado no frontmatter e em §41 da ADR-0028 |
| QA-005 (observação) | Mantido como observação | Verificado — sem implicação corretiva |
| QA-006 (observação) | Mantido como observação | Verificado — sem implicação corretiva |

As correções QA-001 a QA-004 do ciclo pós-patch estão presentes na ADR-0028 e
foram propagadas aos contratos. — **CONFORME**.

---

## 30. Verificação do autorizado no QA anterior

O `RELATORIO_QA_POS_PATCH_ADR-0028.md` autorizou `APPLY_ADR` após confirmar
que todos os quatro achados corretivos foram resolvidos.

O auditor desta etapa verifica que:

1. As correções dos QA-001 a QA-004 estão presentes na ADR-0028 em sua versão
   atual — confirmado.
2. As correções foram propagadas aos contratos normativos — confirmado (ver
   seções 7–14 deste relatório).
3. Os QA-005 e QA-006 (observações) não exigiam ação corretiva e permanecem
   registrados como observações — confirmado.

A autorização do QA anterior foi devidamente exercida. — **CONFORME**.

---

## 31. Pendências para próximos passos

As pendências abaixo são informativas; nenhuma bloqueia a aprovação desta
auditoria de aplicação.

| # | Pendência | Origem |
|---|---|---|
| 1 | Definir valor padrão do modo inicial quando campo `excesso` ausente | ADR-0028 §43 item 3 |
| 2 | Definir nomes definitivos das propriedades do JSON de conteúdo multinível | ADR-0028 §43 item 1 |
| 3 | Reconciliar terminologia `modo normal`/`modo não verboso` | ADR-0028 §43 |
| 4 | Protocolo Pipeline completo (itens 10–15 do §43) | ADR-0028 §43 |
| 5 | Demais itens adiados do §43 (items 4–9) | ADR-0028 §43 |

---

## 32. Impedimentos para handoff

A aplicação documental desta ADR não cria handoff imediato. Os impedimentos
pré-existentes que bloqueiam a criação de handoff para ADR-0028 são:

1. Valor padrão do modo inicial indefinido (§43 item 3).
2. Nomes definitivos das propriedades do JSON indefinidos (§43 item 1).
3. Reconciliação terminológica `modo normal`/`modo não verboso` pendente.
4. Protocolo Pipeline indefinido (§43 itens 10–15).

Estas pendências são impedimentos normativos, não desta auditoria de aplicação.

---

## 33. Resumo executivo

A aplicação documental da ADR-0028 propagou integralmente as 22 decisões
aprovadas (D1–D22) aos 8 documentos normativos autorizados e criou o relatório
de aplicação como nono arquivo.

O auditor não identificou nenhum achado bloqueante. Foram identificados:

- **APLIC-QA-001** (Médio, não bloqueante): inconsistência interna no relatório
  de aplicação — a verificação #2 cita 7+1=8 arquivos quando o correto é 8+1=9.
  A lista principal e a seção de bloqueios do mesmo relatório apresentam a
  contagem correta de 9.

- **APLIC-QA-002** (Baixo, não bloqueante): §13.4 do contrato_json_console.md
  condensa dois cenários distintos de `conjuntos_campos` em linha única; as
  regras completas estão na ADR-0028 e acessíveis via remissão.

- **APLIC-QA-003** (Observação, não bloqueante): seções 14 e 22 do
  contrato_barra_de_menus tratam do chip `[V]` em contextos distintos sem
  referência cruzada entre si.

As autoridades ADR-0026 e ADR-0027 foram preservadas. Nenhuma decisão adiada
foi preenchida. Nenhuma implementação foi antecipada. Nenhum arquivo fora da
lista autorizada foi modificado.

---

## 34. Achados formais

| Código | Severidade | Bloqueante | Localização | Título |
|---|---|---|---|---|
| APLIC-QA-001 | Médio | Não | RELATORIO_APLICACAO §14 ver. #2 | Contagem incorreta: 7+1=8 em vez de 8+1=9 |
| APLIC-QA-002 | Baixo | Não | contrato_json_console.md §13.4 | Dois cenários de conjuntos_campos condensados em linha única |
| APLIC-QA-003 | Observação | Não | contrato_barra_de_menus.md §14 e §22 | Coexistência de seções sobre [V] sem referência cruzada |

---

## 35. Recomendações

1. **APLIC-QA-001**: Corrigir a verificação #2 da seção 14 do RELATORIO_APLICACAO
   para "8 arquivos alterados + 1 criado (este relatório) = 9 total" em eventual
   revisão do relatório. Não urgente — não afeta a integridade da aplicação.

2. **APLIC-QA-002**: Em futuro refinamento do contrato_json_console.md, considerar
   expandir §13.4 para separar os cenários de dois e três níveis de `conjuntos_campos`
   em linhas distintas. Não urgente — remissão existente é suficiente para
   implementação.

3. **APLIC-QA-003**: Em futuro refinamento do contrato_barra_de_menus.md,
   considerar adicionar remissão de §14 para §22 e vice-versa para explicitar
   a distinção de escopo. Não urgente — §22.5 é suficiente para a norma atual.

As recomendações acima são opcionais para aprovação desta etapa.

---

## 36. Status final

```
ADR_APPLICATION_APPROVED_WITH_NOTES
```

A aplicação documental da ADR-0028 está aprovada. Os três achados identificados
(APLIC-QA-001, APLIC-QA-002, APLIC-QA-003) são não bloqueantes. A etapa
`APLICAR_ADR` pode ser considerada concluída.

---

## 37. Saída final

```yaml
status_literal: ADR_APPLICATION_APPROVED_WITH_NOTES
status_normalizado: aprovada_com_notas
relatorio: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0028.md
adr_auditada: docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md
relatorio_aplicacao_inspecionado: docs/relatorios/RELATORIO_APLICACAO_ADR-0028.md
achados_bloqueantes: 0
achados_nao_bloqueantes: 3
achados:
  - codigo: APLIC-QA-001
    severidade: medio
    bloqueante: false
    localizacao: "RELATORIO_APLICACAO_ADR-0028.md §14 verificação #2"
    titulo: "Contagem incorreta no resumo de verificação (7+1=8; correto é 8+1=9)"
  - codigo: APLIC-QA-002
    severidade: baixo
    bloqueante: false
    localizacao: "contrato_json_console.md §13.4"
    titulo: "Dois cenários distintos de conjuntos_campos condensados em linha combinada"
  - codigo: APLIC-QA-003
    severidade: observacao
    bloqueante: false
    localizacao: "contrato_barra_de_menus.md §14 e §22"
    titulo: "Coexistência de seções sobre [V] sem referência cruzada entre elas"
decisoes_verificadas: 22
decisoes_propagadas: 22
decisoes_omitidas: 0
autoridades_preservadas:
  - ADR-0026
  - ADR-0027
decisoes_adiadas_preenchidas: 0
implementacao_antecipada: false
arquivos_nao_autorizados_alterados: 0
proxima_etapa: COMMIT_ADR
```
