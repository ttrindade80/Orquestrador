---
name: RELATORIO_QA_POS_PATCH_ADR-0028
description: Relatório de QA pós-patch da ADR-0028 — auditoria independente em contexto limpo após PATCH_ADR
metadata:
  type: relatorio_qa_pos_patch
  adr_auditada: ADR-0028
  qa_de_origem: docs/relatorios/RELATORIO_QA_ADR-0028.md
  data: "2026-07-17"
  auditor: independente (contexto limpo)
  status_literal: ADR_APPROVED_WITH_NOTES
---

# Relatório de QA pós-patch — ADR-0028

## 1. Identificação

| Campo | Valor |
|---|---|
| Relatório | RELATORIO_QA_POS_PATCH_ADR-0028.md |
| ADR auditada | ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md |
| QA de origem | RELATORIO_QA_ADR-0028.md |
| Data | 2026-07-17 |
| Ciclo precedente | PATCH_ADR |
| Status recebido | ADR_PATCHED |
| Status anterior | ADR_REJECTED |

---

## 2. Objetivo

Auditar a ADR-0028 pós-patch para verificar se:

- os quatro achados corretivos (QA-001 a QA-004) foram corrigidos integralmente;
- o patch não introduziu regressões normativas, terminológicas ou de escopo;
- as decisões explícitas do usuário (DU-01 a DU-13) permanecem respeitadas;
- as observações QA-005 e QA-006 permanecem como observações não corretivas;
- o estado Git é consistente com o escopo declarado.

---

## 3. Autoridades

### 3.1 Documentos lidos integralmente

| Documento | Status |
|---|---|
| `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md` | Lido integralmente (1387 linhas) |
| `docs/relatorios/RELATORIO_QA_ADR-0028.md` | Lido integralmente |
| `docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md` | Lido integralmente |
| `docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md` | Lido integralmente |

### 3.2 Documentos lidos focalmente

| Documento | Status |
|---|---|
| `docs/contratos/contrato_console.md` | Lido integralmente |
| `docs/contratos/contrato_barra_de_menus.md` | Lido integralmente |

### 3.3 Autoridade externa — limitação de acesso

O arquivo `/mnt/data/CONTRATO_APRESENTACAO_DISTRIBUICAO_CONTEUDO_MULTINIVEL.md` não existe no caminho especificado; o diretório `/mnt/data/` não está disponível nesta sessão.

Verificação de regras do contrato externo foi conduzida por meio de:

1. citações diretas registradas no `RELATORIO_QA_ADR-0028.md` (em especial R-013 para QA-002);
2. referências normativas da própria ADR-0028 às seções do contrato (§43, §33).

Essa limitação não impediu a verificação dos achados QA-001 a QA-004, cujas autoridades primárias são ADR-0026, ADR-0027, `contrato_console.md` e `contrato_barra_de_menus.md` — todos lidos integralmente.

### 3.4 Documento explicitamente excluído

```text
/mnt/data/ESTRUTURA_JSON_CONTEUDO_MATRICIAL_E_MULTINIVEL.md
```

Não utilizado como autoridade, conforme determinado.

---

## 4. Escopo auditado

Arquivo único: `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md`

Verificações executadas: quatro achados originais (QA-001 a QA-004), duas observações (QA-005 e QA-006), busca focal obrigatória por termos normativos, auditoria de regressões em escopo, origem, modos, alternância, responsabilidades, paginação, geometria e decisões adiadas.

---

## 5. Estado Git

```yaml
branch: master
head: f6982d0
git_status_short:
  - "?? docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md"
  - "?? docs/relatorios/RELATORIO_QA_ADR-0028.md"
diff_check: LIMPO (DIFF_CHECK_OK)
stage: VAZIO
outros_arquivos_modificados: nenhum
workspace_inesperado: nenhum
```

O workspace permanece idêntico ao estado declarado. Os dois arquivos são não rastreados (criados no ciclo PATCH_ADR). Nenhum arquivo além dos declarados está presente. O HEAD não se moveu desde o QA de origem. O escopo do patch é verificável e limitado à ADR-0028.

---

## 6. Síntese do QA inicial

O `RELATORIO_QA_ADR-0028.md` (status `ADR_REJECTED`) identificou quatro achados corretivos:

| ID | Seção | Severidade | Exige decisão do usuário |
|---|---|---|---|
| QA-001 | D3 e §35.1 | médio | não |
| QA-002 | §33, V-05 | baixo | não |
| QA-003 | §34 | baixo | não |
| QA-004 | §41 e frontmatter | baixo | não |

E duas observações não corretivas:

| ID | Seção | Severidade |
|---|---|---|
| QA-005 | §43 | observação |
| QA-006 | §25 e D12 | observação |

---

## 7. Síntese do patch

O campo `§47 — Histórico de alterações` da ADR-0028 declara:

> Correção pós-QA (PATCH_ADR): reconciliação terminológica entre carregamento separado e entrega conjunta em D3 e §35.1; remoção do qualificador indevido de V-05; registro terminológico de `modo normal` e `modo não verboso` em §34; inclusão de `docs/contratos/contrato_barra_de_menus.md` entre os documentos afetados no frontmatter e em §41.

A declaração do patch mapeia exatamente sobre os quatro achados QA-001 a QA-004. A auditoria verificou se cada uma das quatro correções foi efetivamente implementada e se não foram introduzidas regressões.

---

## 8. Verificação de QA-001 — Carregamento separado e entrega conjunta

### 8.1 Achado original

Contradição direta entre D3 ("conjuntamente") e §35.1 item 4 ("separadamente") para a mesma ação de entrega dos documentos ao fluxo interno.

### 8.2 Conteúdo das seções após o patch

**D3 — Carregamento separado e entrega conjunta (linhas 249–258):**

```text
1. carregar separadamente o JSON estrutural da tela e o documento JSON
   de conteúdo multinível;
2. entregar os dois documentos conjuntamente ao fluxo interno de
   carregamento, modelo e renderização.

Os documentos são carregados separadamente e entregues conjuntamente
ao fluxo interno, permanecendo distintos e sem incorporação do conteúdo
externo ao JSON estrutural da tela. Entrega conjunta não implica fusão,
cópia ou reinserção de conteúdo.
```

**§35.1 — Ponto de entrada (linhas 1121–1129):**

```text
3. carregar separadamente o documento JSON de conteúdo multinível;
4. entregar os dois documentos conjuntamente ao fluxo interno, mantendo-os
   como entradas distintas sem incorporação do conteúdo externo ao JSON
   estrutural da tela;
5. não copiar o conteúdo externo para dentro do JSON estrutural.
```

### 8.3 Verificações obrigatórias

| # | Verificação | Resultado |
|---|---|---|
| 1 | JSON estrutural e documento externo são carregados separadamente | CONFIRMADO — §7 item 3, D3 item 1, §35.1 item 3 |
| 2 | Ponto de entrada entrega os dois conjuntamente ao fluxo interno | CONFIRMADO — §7 item 4, D3 item 2, §35.1 item 4 |
| 3 | Os dois permanecem entradas distintas | CONFIRMADO — D3 "permanecendo distintos", §35.1 "mantendo-os como entradas distintas" |
| 4 | Entrega conjunta não significa fusão, cópia, incorporação ou reinserção | CONFIRMADO — D3 "Entrega conjunta não implica fusão, cópia ou reinserção de conteúdo" |
| 5 | Responsabilidades compatíveis com ADR-0026 e ADR-0027 | CONFIRMADO — §39 preserva ADR-0026 e ADR-0027 sem contradição |
| 6 | Sem formulações residuais contraditórias | CONFIRMADO — §3.1, §5, §7, §11, §35.1, §39 usam "carregamento separado e entrega conjunta" de forma consistente |

### 8.4 Resultado

**QA-001: CORRIGIDO**

A contradição entre D3 e §35.1 foi eliminada. Ambas as seções usam consistentemente "conjuntamente" para a entrega, com cláusula explicativa que registra que "os documentos são carregados separadamente e entregues conjuntamente ao fluxo interno, permanecendo distintos". A formulação "Entrega conjunta não implica fusão, cópia ou reinserção de conteúdo" foi acrescentada em D3, cobrindo o item 4 da verificação.

---

## 9. Verificação de QA-002 — Validação V-05

### 9.1 Achado original

V-05 continha o qualificador "obrigatório" ausente no contrato externo (R-013: "Um nível do tipo contêiner DEVE declarar o nível de seus filhos"), podendo ser interpretado como enfraquecimento da regra.

### 9.2 V-05 após o patch (linha 1066)

```text
| V-05 | Contêiner sem nível filho declarado | INVÁLIDO |
```

### 9.3 Verificações obrigatórias

| # | Verificação | Resultado |
|---|---|---|
| 1 | Qualificador "obrigatório" removido de V-05 | CONFIRMADO — busca focal: "contêiner obrigatório" não encontrado em nenhuma linha |
| 2 | Qualificador não permanece em tabela, resumo, exemplo ou seção paralela | CONFIRMADO — nenhuma ocorrência encontrada |
| 3 | Não foi criada exceção de "contêiner opcional" | CONFIRMADO — §14.1 mantém "Deve declarar o nível de seus filhos" sem exceção |
| 4 | Regra coerente com o contrato externo (R-013) | CONFIRMADO — R-013: "DEVE declarar o nível de seus filhos" vs V-05: "Contêiner sem nível filho declarado — INVÁLIDO" |
| 5 | Demais validações V-01 a V-15 não alteradas materialmente | CONFIRMADO — somente V-05 foi modificado; as demais 14 validações são idênticas ao QA inicial |

### 9.4 Resultado

**QA-002: CORRIGIDO**

O qualificador "obrigatório" foi removido de V-05. A regra está agora alinhada com R-013 do contrato externo. Nenhuma exceção foi criada. As demais validações V-01 a V-15 permanecem inalteradas.

---

## 10. Verificação de QA-003 — "Modo normal" e "modo não verboso"

### 10.1 Achado original

A tabela de §34 não registrava a diferença entre "modo normal" (`contrato_console.md` §6) e "modo não verboso" (ADR-0028 §§21–22, D9).

### 10.2 Conteúdo de §34 após o patch (linhas 1109–1115)

A seção §34 recebeu uma subseção adicional:

```text
### Diferença adicional: `modo normal` e `modo não verboso`

O `contrato_console.md` (§6) utiliza o termo `modo normal` para o modo
operacional de exibição do console sem quebra de linha, declarando-o como
o default da instância. A ADR-0028 utiliza o termo `modo não verboso`
(§§21–22, D9) para o mesmo comportamento conceitual aplicado às
apresentações de conteúdo multinível no `console`.

Os dois termos descrevem o mesmo comportamento: exibição de cada conteúdo
aplicável em uma única linha física, com truncamento do excedente. Esta
equivalência conceitual é registrada aqui para que a futura aplicação
documental possa reconciliar explicitamente os termos, sem que nenhum
deles seja silenciosamente renomeado ou declarado como já substituído.

A reconciliação terminológica definitiva — incluindo qual dos termos será
adotado como nome concreto no schema — é adiada para a futura aplicação
documental. O registro desta diferença não constitui decisão de valor
padrão para o modo inicial, que permanece adiado conforme §43 item 3
desta ADR e §43 item 3 do contrato externo.
```

### 10.3 Verificações obrigatórias

| # | Verificação | Resultado |
|---|---|---|
| 1 | "modo normal" identificado como terminologia do `contrato_console.md` §6 | CONFIRMADO |
| 2 | "modo não verboso" identificado como terminologia normativa da ADR-0028 | CONFIRMADO |
| 3 | ADR não renomeia silenciosamente o contrato | CONFIRMADO — "sem que nenhum deles seja silenciosamente renomeado" |
| 4 | ADR não declara migração já aplicada | CONFIRMADO — "adiada para a futura aplicação documental" |
| 5 | Futura reconciliação declarada | CONFIRMADO |
| 6 | Correção não escolhe nome definitivo | CONFIRMADO — "incluindo qual dos termos será adotado" é adiado |
| 7 | Correção não decide qual modo é padrão | CONFIRMADO |
| 8 | Decisão sobre valores padrão continua adiada | CONFIRMADO — "O registro desta diferença não constitui decisão de valor padrão" |

### 10.4 Verificação adicional — sinonímia absoluta indevida

A ADR não trata "modo normal" e "modo não verboso" como sinônimos absolutos. A seção registra "equivalência conceitual" e explicitamente conclui que "a futura aplicação documental possa reconciliar explicitamente os termos". A diferença de camadas (contrato de instância de console vs ADR de conteúdo multinível) não foi apagada.

### 10.5 Resultado

**QA-003: CORRIGIDO**

A diferença terminológica entre "modo normal" (`contrato_console.md`) e "modo não verboso" (ADR-0028) foi registrada em §34. A ADR não escolhe nome definitivo, não declara migração e não decide valor padrão.

---

## 11. Verificação de QA-004 — Contrato da barra de menus

### 11.1 Achado original

`docs/contratos/contrato_barra_de_menus.md` não estava listado no frontmatter nem em §41.

### 11.2 Frontmatter após o patch (linha 15)

```yaml
contratos_afetados:
  - docs/contratos/contrato_json_console.md
  - docs/contratos/contrato_console.md
  - docs/contratos/contrato_barra_de_menus.md   ← incluído no patch
  - docs/contratos/contrato_tela_json.md
  - docs/contratos/contrato_composicao_corpo.md
  - docs/NOMENCLATURA.md
  - docs/adr/INDICE_ADR.md
```

### 11.3 §41 após o patch (linha 1260)

```text
| docs/contratos/contrato_barra_de_menus.md | Avaliar se a definição da
ação `[V] Verboso` nas demonstrações de dados do `console` (§23) requer
atualização deste contrato. A ação `[V]` pode já estar parcialmente
coberta pela seção 14 do `contrato_console.md`; a aplicação documental
decidirá se alteração deste contrato é necessária. |
```

### 11.4 Verificações obrigatórias

| # | Verificação | Resultado |
|---|---|---|
| 1 | Caminho correto | CONFIRMADO — `docs/contratos/contrato_barra_de_menus.md` é o caminho real |
| 2 | Contrato listado apenas como afetado | CONFIRMADO — nota diz "Avaliar se...requer atualização", não "atualizado" |
| 3 | ADR não afirma que a ação já foi aplicada | CONFIRMADO |
| 4 | Contrato não foi alterado durante o patch | CONFIRMADO — git status não lista `contrato_barra_de_menus.md` como modificado |
| 5 | Futura aplicação documental deverá avaliar cobertura de `[V] Verboso`, tecla V, alternância reversível, estado visual da sessão | CONFIRMADO — §41 nota cobre exatamente essa avaliação |

### 11.5 Verificação contra `contrato_barra_de_menus.md` real

O `contrato_barra_de_menus.md` §14 ("Modo verboso `[V]`") cobre `[V]` para instâncias de `console` que permitem modo verboso. O §8.3 lista `[V]` como chip de existência condicional. A nota de §41 está correta ao indicar que a cobertura pode ser parcial e que a aplicação documental decidirá.

### 11.6 Resultado

**QA-004: CORRIGIDO**

O `contrato_barra_de_menus.md` está agora listado nominalmente no frontmatter e em §41 com nota de avaliação futura. O contrato não foi alterado. A ADR não afirma aplicação antecipada.

---

## 12. Tratamento de QA-005 — Item matricial nos adiados

### 12.1 Observação original

O contrato externo (§43 item 8) adia "a integração com o contrato de distribuição matricial". A ADR-0028 não lista esse item em seu §43.

### 12.2 Auditoria pós-patch

| Verificação | Resultado |
|---|---|
| Conteúdo matricial continua fora do escopo | CONFIRMADO — §6, §42, §46 linha 2 |
| Nenhuma regra matricial foi reintroduzida | CONFIRMADO — busca focal: "matrici"/"matriz" aparece somente em exclusões e referências históricas |
| Omissão não produz contradição com escopo negativo | CONFIRMADO — §42 exclui explicitamente `tipo: matriz` |

**Resultado:** Observação QA-005 mantida como não corretiva. Nenhuma alteração indicada.

---

## 13. Tratamento de QA-006 — Tensão entre `modo normal` e valores padrão adiados

### 13.1 Observação original

Tensão entre `modo normal` como default no `contrato_console.md` e a decisão adiada sobre valores padrão na ADR-0028.

### 13.2 Auditoria pós-patch

| Verificação | Resultado |
|---|---|
| Patch não decidiu novo default | CONFIRMADO — §25, D12 e §43 item 3 permanecem inalterados |
| Patch não apagou a decisão adiada | CONFIRMADO |
| Patch não declarou `nao_verboso` como valor inicial automático | CONFIRMADO |
| Reconciliação permanece para aplicação documental | CONFIRMADO |
| Sem duas regras normativas incompatíveis sobre modo inicial | CONFIRMADO — §34 registra a tensão e a adia; os dois enunciados descrevem camadas distintas (instância do console vs documento JSON externo) |

A adição da subseção de §34 não resolveu a tensão nem introduziu contradição: ela a registrou para reconciliação futura e adicionou explicitamente: "O registro desta diferença não constitui decisão de valor padrão para o modo inicial, que permanece adiado conforme §43 item 3 desta ADR e §43 item 3 do contrato externo."

**Resultado:** Observação QA-006 mantida como não corretiva. A reconciliação futura está corretamente declarada.

---

## 14. Regressões

### 14.1 Escopo

| Verificação | Resultado |
|---|---|
| Somente console | CONFIRMADO — §6 |
| Somente conteúdo multinível | CONFIRMADO — §6 |
| Sem conteúdo matricial | CONFIRMADO — §6, §42, §46 |

### 14.2 Origem dos dados

| Verificação | Resultado |
|---|---|
| Arquivo JSON externo atualmente | CONFIRMADO — §7 |
| Script do Pipeline futuramente | CONFIRMADO — §8 |
| Mesma fronteira JSON | CONFIRMADO — §9 |
| Protocolo futuro não definido | CONFIRMADO — §43 itens 10–15 |

### 14.3 Modos de apresentação

| Verificação | Resultado |
|---|---|
| Tabela multinível | CONFIRMADO — D8, D15, §17, §36 |
| Hierarquia indentada | CONFIRMADO — D8, D16, §18, §36 |
| Conjunto com campos | CONFIRMADO — D8, D17, §19, §36 |
| Conjunto, subconjunto e campos | CONFIRMADO — D8, D17, §20, §36 |

### 14.4 Alternância

| Verificação | Resultado |
|---|---|
| `[V] Verboso` | CONFIRMADO — §23 |
| Mesma tela | CONFIRMADO — §23 |
| Mesmos dados | CONFIRMADO — §23, §24 |
| Mesmo documento externo | CONFIRMADO — §23, §24 |
| Reversível | CONFIRMADO — D11, §23 |
| Não persistente | CONFIRMADO — §24 |
| Isolada por console | CONFIRMADO — §24 |

### 14.5 Responsabilidades

| Verificação | Resultado |
|---|---|
| Ponto de entrada | CONFIRMADO — §35.1 |
| Loader | CONFIRMADO — §35.2 |
| Modelo | CONFIRMADO — §35.3 |
| Renderizador | CONFIRMADO — §35.4, D14 |

### 14.6 Paginação e geometria

| Verificação | Resultado |
|---|---|
| Repetição de cabeçalho | CONFIRMADO — §17.12, §30.1 |
| Preservação de ancestrais | CONFIRMADO — §18.8, §30.1 |
| Contexto visual não duplicando dados | CONFIRMADO — §30.2 |
| Blocos indivisíveis | CONFIRMADO — §31 |
| Impossibilidade horizontal não resolvida por paginação | CONFIRMADO — §30.4, §32 |
| Recuperação após redimensionamento | CONFIRMADO — D14, §32 |

### 14.7 Decisões adiadas — nenhuma preenchida silenciosamente

| Item adiado | Verificação |
|---|---|
| Nomes de propriedades | §43 item 1 — adiado |
| Versão de schema | §43 item 2 — adiado |
| Valores padrão | §43 item 3 — adiado (incluindo modo padrão) |
| Marcador padrão | §43 item 4 — adiado |
| Profundidade máxima | §43 item 6 — adiado |
| Fallback global | §43 item 7 — adiado |
| Navegação entre páginas | §43 item 8 — adiado |
| Mensagens de validação | §43 item 9 — adiado |
| Protocolo com Pipeline | §43 itens 10–15 — adiado |

**Resultado:** Nenhuma regressão identificada. Nenhuma decisão adiada foi preenchida pelo patch.

---

## 15. Autoridade externa

O contrato `CONTRATO_APRESENTACAO_DISTRIBUICAO_CONTEUDO_MULTINIVEL.md` não está disponível em `/mnt/data/` nesta sessão. A verificação das regras do contrato foi conduzida mediante:

1. citações diretas do relatório QA inicial (R-013 para QA-002);
2. referências explícitas da ADR-0028 ao contrato (§3.3, §43, §33 linha final: "derivam do contrato externo (R-146 a R-160)").

§3.3 confirma que o contrato correto é autoridade normativa e que o documento incorreto (`ESTRUTURA_JSON_CONTEUDO_MATRICIAL_E_MULTINIVEL.md`) foi desautorizado. Essa declaração permanece inalterada pelo patch.

---

## 16. Escopo exclusivo do console

§6 declara: "Esta ADR aplica-se exclusivamente a dados multinível exibidos em componentes do tipo `console`." Cláusula de escopo restringe todos os termos "conteúdo", "dados", "apresentação" e "renderização" ao contexto de conteúdo multinível em `console`. O patch não alterou §6.

---

## 17. Origem atual dos dados

§7 descreve a origem atual como documento JSON externo armazenado em arquivo. Os quatro passos do ponto de entrada (identificar, carregar JSON estrutural, carregar separadamente o documento externo, entregar conjuntamente) estão presentes e inalterados pelo patch.

---

## 18. Origem futura pelo Pipeline

§8 descreve a integração futura: dados em formato JSON; fronteira semântica estável; conteúdo separado do JSON estrutural; independência do `console` quanto ao mecanismo produtor. O patch não alterou §8.

---

## 19. Fronteira em JSON

§9 define o documento JSON de conteúdo multinível como "fronteira semântica estável entre o produtor dos dados e o `console`". Inalterado pelo patch.

---

## 20. Ausência de conteúdo matricial

Busca focal por "matrici" e "matriz" retornou somente:

- §3.3: referência ao arquivo incorreto como autoridade removida;
- §6: `tipo: matriz` listado como fora de escopo;
- §39: ADR-0025/H-0035 listados como não afetados;
- §42: conteúdo matricial listado explicitamente no escopo negativo;
- §46 linha 2: verificação de integridade confirmando ausência.

Nenhuma regra normativa derivada de conteúdo matricial foi encontrada.

---

## 21. Alternância por V

§23 define a tecla `V` como alternador entre verboso e não verboso durante a sessão; barra de menus deve apresentar `[V] Verboso`; a alternância usa mesmos dados, mesma tela, mesmo documento, não troca apresentação, não persiste, é reversível.

§24 lista sete comportamentos que a alternância não deve ter (reescrever JSON externo, JSON estrutural, alterar fixture, substituir dados, persistir globalmente, vazar para outro console, alterar identidade do cenário). Ambas as seções estão inalteradas pelo patch.

---

## 22. Decisões adiadas

§43 lista 15 itens explicitamente adiados. Busca focal por "padrão" e "default" no arquivo:

- ocorrências em §43 itens 3 e 4: corretamente adiadas;
- ocorrências em §28: "A ADR não decide o comportamento padrão desta política; ele fica adiado conforme §43";
- ocorrências em §25: "A definição do valor padrão é adiada para a etapa de schema ou aplicação documental";
- "Por padrão" em §17.3 (caminho completo por linha lógica) e §19.7 (prioridade de truncamento do valor): regras de comportamento do contrato externo, não decisões de schema adiadas;
- §34 subseção nova: "O registro desta diferença não constitui decisão de valor padrão para o modo inicial."

Nenhum valor padrão foi introduzido silenciosamente pelo patch.

---

## 23. Arquivos alterados

O git status confirma que apenas os seguintes arquivos são não rastreados:

```text
docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md
docs/relatorios/RELATORIO_QA_ADR-0028.md
```

Nenhum outro arquivo foi modificado. O patch respeitou o escopo declarado — somente a ADR-0028 foi alterada no ciclo PATCH_ADR.

Após a criação deste relatório, os arquivos não rastreados passam a ser:

```text
docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md
docs/relatorios/RELATORIO_QA_ADR-0028.md
docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0028.md
```

---

## 24. Novos achados

### 24.1 Pesquisa de novos achados

A busca focal e a auditoria de regressões não identificaram defeito normativo, contradição material ou regressão introduzida pelo patch.

Um potencial ponto de observação foi examinado: §11 atribui à ADR-0027 o estabelecimento de "carregamento separado e entrega conjunta", enquanto ADR-0027 D2 e D8 utilizam "entregar separadamente". Essa tensão terminológica foi examinada sob os seguintes critérios:

1. O conteúdo de §11 não foi alterado pelo patch — estava presente na versão original da ADR-0028 e foi classificado como **CONFORME** pelo QA inicial.
2. O título da ADR-0027 é "Carregamento conjunto da tela e do conteúdo externo pelo ponto de entrada", o que torna a atribuição parcialmente defensável.
3. O comportamento real descrito é consistente: os dois documentos são entregues como entidades distintas, sem fusão.
4. A instrução aplicável é: "Não refaça a ADR por preferência editorial."

**Decisão:** a observação não constitui novo achado formal. Não foi introduzida pelo patch e não representa contradição normativa.

### 24.2 Resultado

**Novos achados: NENHUM**

---

## 25. Conclusão

A ADR-0028 após o patch apresenta:

- QA-001 corrigido: D3 e §35.1 agora usam "conjuntamente" de forma consistente, com cláusula explicativa que registra separação dos carregamentos, distinção das entradas e que "Entrega conjunta não implica fusão, cópia ou reinserção de conteúdo";
- QA-002 corrigido: V-05 reformulado para "Contêiner sem nível filho declarado — INVÁLIDO", alinhado com R-013 do contrato externo, sem qualificador indevido em nenhuma seção;
- QA-003 corrigido: §34 recebeu subseção registrando a diferença entre "modo normal" (`contrato_console.md`) e "modo não verboso" (ADR-0028), com declaração explícita de que o registro não constitui decisão de valor padrão;
- QA-004 corrigido: `docs/contratos/contrato_barra_de_menus.md` incluído no frontmatter e em §41 com nota de avaliação futura;
- QA-005 e QA-006 permanecem como observações não corretivas, com o patch tendo registrado explicitamente a tensão terminológica (QA-003/QA-006) sem resolvê-la normalmente;
- nenhuma regressão de escopo, modo, alternância, responsabilidade, paginação, geometria ou decisão adiada foi identificada;
- nenhum novo achado formal.

---

## 26. Status literal

`ADR_APPROVED_WITH_NOTES`

Todos os quatro achados corretivos foram corrigidos. Restam somente as observações não corretivas QA-005 e QA-006, cuja reconciliação futura está declarada no próprio documento.

---

## 27. Status normalizado

```yaml
status_literal: ADR_APPROVED_WITH_NOTES
qa_001: CORRIGIDO
qa_002: CORRIGIDO
qa_003: CORRIGIDO
qa_004: CORRIGIDO
qa_005: OBSERVACAO_NAO_CORRETIVA
qa_006: OBSERVACAO_NAO_CORRETIVA
novos_achados_bloqueantes: nenhum
novos_achados_altos: nenhum
novos_achados_medios: nenhum
novos_achados_baixos: nenhum
novas_observacoes: nenhuma
regressoes: nenhuma
bloqueio_decisao_usuario: false
bloqueio_arquitetural: false
```

---

## 28. Próxima categoria permitida

```yaml
proxima_categoria: APPLY_ADR
descricao: >
  A ADR-0028 está aprovada com notas e pode avançar para aplicação documental.
  A aplicação deverá propagar as regras normativas do conteúdo multinível nos
  contratos afetados listados em §41, formalizar o estado de visualização e
  a semântica da tecla V, registrar diferenças terminológicas e atualizar o
  índice de ADRs. As observações QA-005 e QA-006 não bloqueiam a aplicação,
  mas a aplicação deverá reconciliar explicitamente a ausência do item 8 do
  §43 do contrato externo e a tensão entre `modo normal` e `modo não verboso`
  quando propagar as regras aos contratos.
restricoes:
  - nenhum ciclo de implementação (handoff) pode ser iniciado antes de APPLY_ADR
  - a aplicação documental não deve alterar código
  - a aplicação documental não deve alterar a ADR-0028
  - o contrato_barra_de_menus.md deve ser avaliado durante a aplicação
    para determinar se requer atualização explícita sobre [V] Verboso
```
