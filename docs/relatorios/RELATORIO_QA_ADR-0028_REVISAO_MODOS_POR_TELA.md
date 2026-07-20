---
name: RELATORIO_QA_ADR-0028_REVISAO_MODOS_POR_TELA
description: Auditoria independente da ADR-0028 após decisão do usuário sobre política de modo de apresentação por tela — verifica se D23 e demais alterações do patch são conformes, completos e não contraditórios
metadata:
  type: relatorio_qa_revisao_modos_por_tela
  adr: ADR-0028
  data: "2026-07-17"
  status_recebido: ADR_PATCHED
  status_literal: ADR_REJECTED
---

# Relatório de QA — ADR-0028: Revisão de Modos por Tela

---

## 1. Identificação

* **Projeto:** Orquestrador
* **Documento Auditado:** `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md`
* **Etapa:** `QA_ADR` (auditoria independente pós-patch de modos por tela)
* **Status Recebido:** `ADR_PATCHED`
* **Status Final Literal:** `ADR_REJECTED`
* **Status Final Normalizado:** `rejeitada`
* **Data da Auditoria:** 17 de julho de 2026

---

## 2. Objetivo

Este relatório constitui uma auditoria documental independente do patch incorporado à ADR-0028 após decisão explícita do usuário sobre política de modo de apresentação da tela. O objetivo é verificar se a ADR-0028 — em seu estado atual pós-patch — é conforme, completa e internamente não contraditória em relação à nova decisão.

O escopo desta auditoria está estritamente restrito a:

1. Ler e auditar a ADR-0028 pós-patch;
2. Contrastar seu conteúdo com a nova decisão do usuário (§5 deste relatório);
3. Produzir este relatório com o resultado factual da auditoria.

**Proibições absolutas desta auditoria:** corrigir a ADR; alterar contratos; alterar o handoff H-0037; implementar qualquer funcionalidade; preparar stage ou commit; aceitar automaticamente as conclusões do autor do patch.

---

## 3. Autoridades

| Documento | Papel nesta Auditoria |
|---|---|
| Decisão explícita do usuário (§5 deste relatório) | Autoridade suprema — prevalece sobre todos os relatórios anteriores |
| `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md` | Documento auditado |
| `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0028.md` | Histórico — não autoridade para esta auditoria |
| `docs/relatorios/RELATORIO_APLICACAO_ADR-0028.md` | Histórico — não autoridade para esta auditoria |
| `docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0028.md` | Histórico — não autoridade para esta auditoria |
| `docs/relatorios/RELATORIO_QA_H-0037_HANDOFF.md` | Histórico — aprovação anterior não vale após nova decisão do usuário |
| `docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md` | Referência para avaliação de impacto |
| `docs/contratos/contrato_console.md` | Referência para avaliação de divergências esperadas |
| `docs/contratos/contrato_barra_de_menus.md` | Referência para avaliação de divergências esperadas |
| `docs/contratos/contrato_json_console.md` | Referência para avaliação de divergências esperadas |

---

## 4. Estado Git

* **Branch:** master
* **HEAD:** `f6982d0`
* **Whitespace:** `git diff --check` retornou saída limpa, sem erros de whitespace.
* **Escopo do patch confirmado:** o patch alterou somente a ADR-0028. Todos os demais arquivos modificados no workspace decorrem de etapas anteriores autorizadas (aplicação documental D1–D22).
* **Arquivos modificados rastreáveis (status `M`):**
  - `docs/NOMENCLATURA.md`
  - `docs/adr/INDICE_ADR.md`
  - `docs/contratos/contrato_barra_de_menus.md`
  - `docs/contratos/contrato_composicao_corpo.md`
  - `docs/contratos/contrato_console.md`
  - `docs/contratos/contrato_json_console.md`
  - `docs/contratos/contrato_tela_json.md`
* **ADR-0028:** não rastreada (status `??`) — lida diretamente pelo auditor.

---

## 5. Decisão Nova do Usuário

A seguinte decisão foi comunicada explicitamente pelo usuário e constitui a autoridade superior para esta auditoria. Nenhum relatório de QA anterior, nenhuma aprovação anterior e nenhuma conclusão do autor do patch tem precedência sobre ela.

### 5.1 Enunciado da decisão

O modo verboso ou não verboso é uma escolha da tela, não de uma política global. Cada tela declara individualmente sua política de modo de apresentação. Uma tela pode ser:

a) **somente verbosa** — apenas exibe em modo verboso; nunca oferece alternância; chip `[V] Verboso` não obrigatório;
b) **somente não verbosa** — apenas exibe em modo não verboso; nunca oferece alternância; chip `[V] Verboso` não obrigatório;
c) **alternável** — oferece os dois modos; chip `[V] Verboso` obrigatório; tecla `V` aplicável; modo inicial deve ser declarado e pode ser verboso ou não verboso.

### 5.2 Regras derivadas da decisão

1. Telas de modo único (a e b): sempre iniciam em seu único modo; tecla `V` não é aplicável; chip `[V] Verboso` não é obrigatório.
2. Telas alternáveis (c): chip `[V] Verboso` é obrigatório; tecla `V` é aplicável; modo inicial deve ser declarado.
3. Cenários mínimos de demonstração futura: quatro, cobrindo as três políticas.
4. O cenário de dois níveis em modo verboso deve alinhar o início dos conteúdos do nível 2 conforme a largura dos textos identificadores do nível 1.

### 5.3 Quatro cenários mínimos

| Cenário | Política | Detalhe |
|---|---|---|
| 1 | somente não verbosa | conteúdo com truncamento por `...`; sem chip; sem alternância |
| 2 | somente verbosa | conteúdo de dois níveis, várias linhas físicas; sem chip; sem alternância |
| 3 | alternável | três níveis; inicia não verbosa; chip obrigatório; alternância por `V` |
| 4 | alternável | tabela; inicia verbosa; chip obrigatório; alternância por `V` |

---

## 6. Verificação 1 — Política Declarada pela Tela

**Questão:** a ADR estabelece que a política de modo é propriedade declarada individualmente por cada tela de console multinível?

**Texto auditado:** D23 (linhas 371–380): *"Cada tela de console multinível deve declarar sua política de modo de apresentação. A política admite três classes conceituais: [...]"*

**Resultado:**
- A política é declarada pela tela, não é global nem inferida. ✓
- As três classes são nomeadas explicitamente: somente verbosa, somente não verbosa, alternável. ✓
- A política não é definida por chip, nem por estado de runtime, nem por inferência de conteúdo. ✓

**Classificação:** `CONFORME`

---

## 7. Verificação 2 — Tela Somente Verbosa

**Questão:** a ADR especifica completamente o comportamento de uma tela somente verbosa?

**Texto auditado:** D23(a) (linha 375): *"somente verbosa — a tela sempre abre em modo verboso; não há alternância por V; o chip [V] Verboso não é obrigatório; o comportamento visual segue as regras do modo verboso"*

**Resultado:**
- Inicia necessariamente em modo verboso: declarado em D23(a) e em D12 (linha 324). ✓
- Permanência no único modo garantida por ausência de alternância: D11 (linha 318) e D23(a). ✓
- Chip `[V] Verboso` não obrigatório: D23(a). ✓
- Tecla `V` não é ação aplicável: D11 (linha 318). ✓
- Comportamento visual segue regras do modo verboso (§22): D23(a). ✓
- Regras de quebra e continuação preservadas e aplicáveis: §22 (referenciado por D23(a)). ✓

**Classificação:** `CONFORME`

---

## 8. Verificação 3 — Tela Somente Não Verbosa

**Questão:** a ADR especifica completamente o comportamento de uma tela somente não verbosa?

**Texto auditado:** D23(b) (linha 377): *"somente não verbosa — a tela sempre abre em modo não verboso; não há alternância por V; o chip [V] Verboso não é obrigatório; o comportamento visual segue as regras do modo não verboso; truncamento com ... permanece válido quando aplicável"*

**Resultado:**
- Inicia necessariamente em modo não verboso: D23(b) e D12 (linha 324). ✓
- Permanência no único modo garantida por ausência de alternância: D11 e D23(b). ✓
- Chip `[V] Verboso` não obrigatório: D23(b). ✓
- Tecla `V` não é ação aplicável: D11 (linha 318). ✓
- Truncamento com `...` explicitamente declarado como válido quando aplicável: D23(b). ✓
- Uma linha física por conteúdo e truncamento com marcador: §21 (referenciado por D9). ✓
- O modo não verboso é uma política declarada — não é apenas estado de runtime após pressionar `V`. ✓

**Classificação:** `CONFORME`

---

## 9. Verificação 4 — Tela Alternável

**Questão:** a ADR especifica completamente o comportamento de uma tela alternável?

**Texto auditado:** D23(c) (linha 379): *"alternável — a tela suporta os dois modos; o chip [V] Verboso é obrigatório; a tecla V alterna entre os dois modos; a alternância é reversível; a tela deve declarar o modo inicial, que pode ser verboso ou não verboso"*

**Resultado:**
- Suporta dois modos: D23(c). ✓
- Chip `[V] Verboso` obrigatório: D23(c) e §23 (linhas 900–906). ✓
- Tecla `V` aplicável e alterna entre os dois modos: D23(c) e D11. ✓
- Alternância reversível: D23(c) e D11 (linha 316: *"uma segunda ativação retorna ao modo anterior"*). ✓
- Modo inicial deve ser declarado: D23(c), D12 (linha 325), §25 (linha 934). ✓
- Modo inicial pode ser verboso ou não verboso: D23(c) e §25 (linha 934). ✓
- Estado de visualização isolado por console, não persistido, não vazado: §24 (linhas 914–924). ✓
- Ao recarregar ou trocar de cenário, modo inicial é restaurado pela configuração declarativa: §24 (linha 924) e §25 (linha 938). ✓

**Classificação:** `CONFORME`

---

## 10. Verificação 5 — Significado do Chip e da Tecla V

**Questão:** o chip `[V] Verboso` representa exclusivamente a disponibilidade da alternância?

**Texto auditado:** §23 (linhas 906): *"O chip [V] Verboso é obrigatório somente em telas alternáveis. Sua presença representa a disponibilidade da alternância."*

**Resultado:**
- O chip representa disponibilidade de alternância: §23. ✓
- O chip não define a política de modo da tela por si só. ✓
- A tecla `V` alterna entre verboso e não verboso: D11, §23 (linha 898). ✓
- A tecla `V` não é aplicável em telas de modo único: D11 (linha 318), §23 (linha 906). ✓
- Nenhuma outra propriedade é alternada pela tecla `V`. ✓
- O chip não muda de rótulo entre os modos (nenhuma decisão de rótulo dinâmico foi tomada). ✓

**Classificação:** `CONFORME`

---

## 11. Verificação 6 — Modo Inicial

**Questão:** o modo inicial é determinístico e está declarado corretamente para as três políticas?

**Texto auditado:**
- D12 (linhas 322–327): modo inicial determinado pela política de D23; telas de modo único iniciam no único modo; telas alternáveis devem declarar o modo inicial; *"A pergunta 'como uma tela alternável inicia?' não é mais uma lacuna aberta."*
- §25 (linhas 930–938): repetição normativa completa; obrigação de declarar existe; mecanismo de schema adiado por §43.

**Resultado:**
- Tela somente verbosa: inicia necessariamente em modo verboso. ✓
- Tela somente não verbosa: inicia necessariamente em modo não verboso. ✓
- Tela alternável: modo inicial pode ser verboso ou não verboso; obrigação de declarar existe. ✓
- Não existe mais lacuna aberta sobre modo inicial de telas alternáveis. ✓
- Ao recarregar ou trocar de cenário, modo inicial é reproduzível pela configuração declarativa. ✓
- A primeira ativação de `V` vai para o estado oposto; a segunda ativação restaura o inicial: D11. ✓
- O nome concreto do campo schema está adiado: §43 item 3, §25. ✓

**Classificação:** `CONFORME`

---

## 12. Verificação 7 — Ausência de Configuração e Telas Legadas

**Questão:** a ADR distingue telas multinível novas abrangidas pela nova política de telas legadas ainda sem declaração? O "default quando ausente" adiado cria contradição com a obrigação de declarar de D23?

**Texto auditado:**
- D23 (linha 373): *"Cada tela de console multinível deve declarar sua política de modo de apresentação"* — obrigação universal.
- §43 item 3 (linha 1351): *"valores padrão quando configuração estiver ausente"* — adiado.
- §39 (linhas 1265–1272): *"H-0036: As três apresentações multinível implementadas [...] e suas fixtures permanecem válidas."*

**Análise:**
D23 usa obrigação universal (*"deve declarar"*). Ao mesmo tempo, §43 item 3 inclui *"valores padrão quando configuração estiver ausente"* como decisão adiada — o que implica a existência prevista de telas sem declaração.

§39 declara H-0036 como válido. As fixtures H-0036 existentes não declaram a nova política de modo (o campo nem existe no schema ainda). Há uma tensão semântica:
- Se D23 é obrigação universal, H-0036 seria não conforme.
- Se H-0036 permanece válido (§39), então D23 não é obrigação universal para telas pré-existentes.

A ADR não distingue explicitamente "telas novas abrangidas" de "telas legadas ainda sem declaração de política". §43 item 3 implica que haverá telas sem declaração, mas não resolve formalmente se isso é permitido como estado transitório ou uma exceção permanente para legados.

**Classificação:** `BAIXO` — Tensão interpretativa, não contradição bloqueante. Não impede aplicação da ADR a novas telas. A tensão decorre de ausência de distinção explícita, não de decisão incorreta.

---

## 13. Verificação 8 — Suficiência do Schema

**Questão:** o schema atual é suficiente para representar as cinco necessidades criadas pela nova decisão?

**As cinco representações necessárias:**
1. Política fixa verbosa (somente verbosa)
2. Política fixa não verbosa (somente não verbosa)
3. Política alternável
4. Modo inicial verboso (em telas alternáveis)
5. Modo inicial não verboso (em telas alternáveis)

**Schema existente auditado:**
- `excesso.modo: "verboso"` é o único valor de schema estabelecido.
- Esse valor representa "modo inicial verboso" para telas alternáveis (necessidade 4) em H-0037.
- Ele não representa as necessidades 1, 2, 3 e 5 de forma formalizada.

**Avaliação:**
O schema existente é insuficiente para representar todas as cinco necessidades. No entanto, a ADR reconhece isso explicitamente em §43 item 3 (linha 1351): *"nomes concretos dos campos para declaração da política de modo de apresentação da tela e do modo inicial em telas alternáveis (conceito decidido em D23 e §25; mecanismo concreto de schema adiado)"*.

As extensões de schema necessárias são:
- Um novo campo para declarar a política da tela (somente_verbosa / somente_nao_verbosa / alternavel);
- Ou extensão dos valores de `excesso.modo` para incluir `"nao_verboso"` (modo inicial não verboso).

Esses campos não exigem nova decisão arquitetural — D23 decide os conceitos; os nomes e valores são detalhes de schema que podem ser decididos na etapa de aplicação documental.

**Classificação:** `INSUFICIENTE_MAS_APLICAVEL_SEM_NOVA_DECISAO` — a insuficiência é esperada, reconhecida e devidamente adiada em §43 item 3.

---

## 14. Verificação 9 — Chip [V] Verboso

**Questão:** o chip `[V] Verboso` está corretamente restrito a telas alternáveis?

**Texto auditado:**
- §23 (linha 906): *"O chip [V] Verboso é obrigatório somente em telas alternáveis."*
- D23(a): chip não obrigatório em somente verbosa.
- D23(b): chip não obrigatório em somente não verbosa.
- D23(c): chip obrigatório em alternável.

**Resultado:**
- Chip obrigatório somente em alternáveis: correto e explícito. ✓
- Chip ausente em somente verbosa: correto. ✓
- Chip ausente em somente não verbosa: correto. ✓
- Chip não é generalizado a nenhum outro tipo de tela (dashboard, lancador): escopo negativo §42 preserva isso. ✓
- Chip representa disponibilidade da alternância, não rótulo de estado atual. ✓

**Classificação:** `CONFORME`

---

## 15. Verificação 10 — Tecla V

**Questão:** a tecla `V` está corretamente restrita a telas alternáveis e não produz efeitos indevidos?

**Texto auditado:**
- D11 (linhas 312–318): *"A tecla V atua exclusivamente em telas alternáveis [...]. Em telas de modo único (somente verbosa ou somente não verbosa), a tecla V não é ação aplicável da tela."*
- §23 (linha 898): *"A tecla V atua exclusivamente em telas alternáveis, alternando entre os modos verboso e não verboso durante a sessão."*
- §24 (linhas 914–922): estado visual da sessão não reescreve JSON; não persiste; não vaza.

**Resultado:**
- Tecla `V` age exclusivamente em telas alternáveis. ✓
- Tecla `V` não é ação aplicável em telas de modo único. ✓
- Alternância não altera policy declarada. ✓
- Alternância não reescreve JSON externo. ✓
- Alternância não persiste além da sessão. ✓
- Alternância não vaza para outros consoles. ✓

**Classificação:** `CONFORME`

---

## 16. Verificação 11 — Cenário Somente Não Verboso

**Questão:** o cenário mínimo de tela somente não verbosa está completamente especificado em §36.2?

**Texto auditado:** §36.2 cenário 1 (linha 1215): *"Tela somente não verbosa — com conteúdo que produza truncamento por ...; sem chip [V] Verboso; sem alternância por V"*

**Resultado:**
- Conteúdo maior que a área útil, com truncamento por `...`: especificado. ✓
- Ausência de chip `[V] Verboso`: especificado. ✓
- Ausência de alternância por `V`: especificado. ✓
- Uma linha física por conteúdo no modo não verboso: §21 (referenciado por D9). ✓
- Dados originais preservados no JSON (somente exibição truncada): §24 e D21. ✓
- O cenário cobre a política somente não verbosa conforme a decisão do usuário. ✓

**Classificação:** `CONFORME`

---

## 17. Verificação 12 — Cenário Somente Verboso de Dois Níveis

**Questão:** o cenário mínimo de tela somente verbosa com dois níveis está completamente especificado?

**Texto auditado:** §36.2 cenário 2 (linha 1217): *"Tela somente verbosa — com conteúdo de dois níveis exibido em várias linhas físicas; sem chip [V] Verboso; sem alternância por V"*

**Resultado:**
- Duas linhas físicas múltiplas: especificado. ✓
- Dois níveis hierárquicos: especificado. ✓
- Ausência de chip `[V] Verboso`: especificado. ✓
- Ausência de alternância por `V`: especificado. ✓
- Regra de alinhamento do conteúdo de nível 2: §36.3 (linha 1231). ✓ (ver achado QA-MODOS-001 abaixo)
- O cenário cobre a política somente verbosa conforme a decisão do usuário. ✓

**Classificação:** `CONFORME COM RESSALVA QA-MODOS-001` — a regra de alinhamento existe mas tem escopo não especificado (ver §28 deste relatório).

---

## 18. Verificação 13 — Regra de Alinhamento de Dois Níveis

**Questão:** a regra de §36.3 é suficientemente específica para produzir implementações determinísticas e compatíveis?

**Texto auditado:** §36.3 (linha 1231): *"No cenário de tela somente verbosa com conteúdo de dois níveis (cenário 2 de §36.2), o início do conteúdo do nível 2 deve respeitar a coluna determinada pelo maior texto do nível 1, preservando alinhamento visual entre as ocorrências."*

**Análise:**

A regra estabelece:
1. Que o nível 2 deve alinhar-se à coluna determinada pelo maior texto do nível 1. — CLARO.
2. Que o alinhamento deve ser preservado entre as ocorrências de nível 2. — CLARO.

O que a regra NÃO estabelece:
- **Qual o escopo da medição de "maior texto do nível 1".**

A ADR em §27 (linhas 970–978) define cinco escopos possíveis de alinhamento:
```text
irmãos
grupo
nível
página
conteúdo completo
```

E a ADR em §13.6 (linha 418) exige: *"A mesma configuração, os mesmos dados e a mesma área útil devem produzir o mesmo resultado"* (Determinismo).

E §13.7 (linha 422): *"Larguras, alinhamentos e designadores calculados para uma renderização não devem variar entre páginas, salvo quando a configuração declarar explicitamente escopo por página."*

Sem especificação do escopo em §36.3:
- Um implementador poderia calcular o "maior texto do nível 1" entre irmãos imediatos.
- Outro poderia calcular no escopo do conteúdo completo.
- Um terceiro poderia calcular por página.

Cada escolha produziria uma coluna de alinhamento diferente com os mesmos dados — violando §13.6 (Determinismo).

Além disso, o próprio prompt desta auditoria estabelece: *"a ADR não precisa conter algoritmo detalhado. Entretanto, não pode usar formulação tão vaga que diferentes implementações produzam geometrias incompatíveis."*

§36.3, como escrita, permite que implementações distintas produzam geometrias incompatíveis.

**Classificação:** `DEFEITO MÉDIO — QA-MODOS-001` (ver §28 deste relatório)

---

## 19. Verificação 14 — Cenário Alternável de Três Níveis

**Questão:** o cenário 3 de §36.2 está especificado e pode ser implementado?

**Texto auditado:** §36.2 cenário 3 (linhas 1219–1225):
```text
Tela alternável de três níveis — iniciando em modo não verboso; com chip [V] Verboso;
alternância para modo verboso pela tecla V; conteúdo no formato:

1. valor
  1.1 valor
      1.1.1 texto
```

**Resultado:**
- Três níveis hierárquicos especificados com exemplos de designadores. ✓
- Política: alternável. ✓
- Modo inicial: não verboso — conceito decidido por D23(c). ✓
- Chip `[V] Verboso` obrigatório: especificado. ✓
- Alternância para modo verboso pela tecla `V`: especificado. ✓
- Segunda ativação de `V` restaura modo não verboso: garantido por D11 (reversibilidade). ✓

**Limitação conhecida e esperada:** o modo inicial não verboso para tela alternável não pode ser declarado no schema atual, pois o único valor definido é `excesso.modo: "verboso"`. Nenhum valor equivalente para não verboso existe. Esta limitação é reconhecida pela ADR em §43 item 3 e não constitui defeito do cenário especificado — apenas uma dependência do schema ainda não resolvida.

**Classificação:** `CONFORME — dependente de schema (ver Verificação 8 e achado QA-MODOS-003)`

---

## 20. Verificação 15 — Tabela Alternável

**Questão:** o cenário 4 de §36.2 está especificado e pode ser implementado?

**Texto auditado:** §36.2 cenário 4 (linha 1227): *"Tabela alternável — iniciando em modo verboso; com chip [V] Verboso; com possibilidade de alternância para modo não verboso pela tecla V."*

**Resultado:**
- Apresentação tabular: especificada (§17 fornece as regras de tabela). ✓
- Política: alternável. ✓
- Modo inicial: verboso — representável no schema atual (`excesso.modo: "verboso"`). ✓
- Chip `[V] Verboso` obrigatório: especificado. ✓
- Alternância para modo não verboso pela tecla `V`: especificado. ✓
- Possibilidade de retorno ao modo verboso: garantida por D11 (reversibilidade). ✓
- Este é o único cenário que pode ser implementado imediatamente com o schema atual. ✓

**Classificação:** `CONFORME`

---

## 21. Verificação 16 — Quatro Cenários Mínimos

**Questão:** os quatro cenários mínimos cobrem as três políticas e os estados de modo necessários?

| Cenário | Política | Modo Inicial | Chip | Tecla V |
|---|---|---|---|---|
| 1 — somente não verbosa | somente não verbosa | não verboso (único) | não | não |
| 2 — somente verbosa | somente verbosa | verboso (único) | não | não |
| 3 — alternável três níveis | alternável | não verboso (declarado) | sim | sim |
| 4 — tabela alternável | alternável | verboso (declarado) | sim | sim |

**Resultado:**
- As três políticas (somente verbosa, somente não verbosa, alternável) estão cobertas. ✓
- Tela alternável com início não verboso (cenário 3): conceito presente, schema a resolver. ✓
- Tela alternável com início verboso (cenário 4): presente e implementável. ✓
- Nenhum cenário mistura políticas (uma tela = uma política). ✓
- §36.1 (linha 1209) confirma que telas de modo único não precisam de alternância e que telas alternáveis permitem observar os mesmos dados nos dois modos. ✓

**Classificação:** `CONFORME`

---

## 22. Verificação 17 — Decisões Adiadas Atualizadas

**Questão:** §43 foi atualizado para refletir o que o patch decidiu e o que permanece em aberto?

**Texto auditado:** §43 item 3 (linha 1351): *"nomes concretos dos campos para declaração da política de modo de apresentação da tela e do modo inicial em telas alternáveis (conceito decidido em D23 e §25; mecanismo concreto de schema adiado); valores padrão quando configuração estiver ausente"*

**O que saiu da lista de itens em aberto com o patch (resolvido por D23):**
- Existência e definição das três classes de política. ✓
- Obrigação de declarar modo inicial em telas alternáveis. ✓
- Permissão de iniciar tela alternável em qualquer dos dois modos. ✓
- Aplicabilidade condicional do chip `[V] Verboso`. ✓
- Inaplicabilidade da tecla `V` em telas de modo único. ✓

**O que permanece em §43:**
- Nomes concretos dos campos de schema para política e modo inicial. ✓
- Valores padrão quando configuração estiver ausente. ✓
- Todos os demais itens 1, 2, 4–15 preservados. ✓

**Resultado:** §43 item 3 está atualizado. A nota parentética *"(conceito decidido em D23 e §25; mecanismo concreto de schema adiado)"* é precisa. ✓

**Classificação:** `CONFORME`

---

## 23. Verificação 18 — Ausência de Resíduos Contraditórios

**Questão:** a ADR contém formulações residuais que contradigam a nova decisão?

**Formulações investigadas:**

| Formulação residual buscada | Resultado |
|---|---|
| "modo não verboso somente como estado de runtime" | Não encontrado. D23(b) e §25 estabelecem não verboso como política declarada. |
| "somente verboso tem representação no schema" generalizada | Não encontrado. §43 item 3 reconhece insuficiência. |
| "modo inicial sempre verboso" | Não encontrado. D23(c) e §25 permitem explicitamente ambos os modos iniciais. |
| "chip [V] em todo console multinível" | Não encontrado. §23 limita chip a telas alternáveis. |
| "tecla V aplicável a telas fixas" | Não encontrado. D11 e §23 excluem telas de modo único. |
| "modo inicial de tela alternável indefinido" | Não encontrado. D12 e §25 declaram obrigação de declarar. |
| "política de modo único proibida" | Não encontrado. D23 as define como classes legítimas. |

**Resultado:** Nenhum resíduo contraditório encontrado no corpo normativo da ADR. ✓

**Classificação:** `CONFORME`

---

## 24. Verificação 19 — Preservação das Decisões D1–D22

**Questão:** as decisões D1–D22, preservadas pela etapa de aplicação documental anterior, permanecem intactas no patch?

**Resultado:**

| Decisão | Verificação |
|---|---|
| D1 — Origem externa dos dados | §7, §9: preservado. ✓ |
| D2 — Origem futura pelo Pipeline | §8: preservado. ✓ |
| D3 — Fronteira semântica em JSON | §9: preservado. ✓ |
| D4–D7 — Tipos, estrutura hierárquica | §13: preservado. ✓ |
| D8 — Demonstrações | §36: preservado (expandido, não alterado). ✓ |
| D9–D10 — Modos não verboso / verboso | §21, §22: preservados. ✓ |
| D11–D12 — Tecla V e modo inicial | Reescritos para restringir/expandir conforme D23 — alteração autorizada pelo patch. ✓ |
| D13–D22 — Demais decisões | Verificados como intocados. ✓ |

**Nota sobre D11 e D12:** a reescrita desses itens no patch é a alteração central e autorizada — ela refina D11 (restringindo `V` a telas alternáveis) e D12 (determinando modo inicial via D23). Não é regressão; é o propósito do patch.

**Classificação:** `CONFORME`

---

## 25. Verificação 20 — Escopo Negativo

**Questão:** o patch introduziu itens fora do escopo negativo declarado em §42?

**Texto auditado:** §42 (linhas 1317–1341) — lista de exclusões, incluindo: conteúdo matricial; dashboard; lancador; implementação; navegação interativa; expansão/recolhimento; nova política global de fallback; persistência global.

**Resultado:**
- Nenhuma menção a conteúdo matricial. ✓
- Nenhuma alteração de dashboard ou lancador. ✓
- Nenhuma implementação de funcionalidade. ✓
- Nenhuma navegação interativa ou expansão/recolhimento. ✓
- Nenhuma política global de fallback nova. ✓
- Nenhuma persistência global. ✓

**Classificação:** `CONFORME`

---

## 26. Verificação 21 — Efeito sobre Documentos Posteriores

**Questão:** o patch alterou documentos além da ADR-0028?

**Estado verificado:** git status confirma que o patch alterou somente a ADR-0028. Todos os demais arquivos em estado modificado ou não rastreado no workspace decorrem de etapas anteriores autorizadas.

**Impactos documentais conhecidos (registrados, não executados):**
- A aplicação documental anterior (D1–D22) foi feita antes da existência de D23 e não a incorpora.
- Os contratos aplicados (contrato_console.md §21.5, §21.7; contrato_barra_de_menus.md §22.1; contrato_json_console.md §13.11) refletem o estado pré-D23 e apresentam divergências esperadas (§6 deste relatório para detalhes).
- O handoff H-0037 foi bloqueado (`BLOQUEADO_POR_MUDANCA_DOCUMENTAL`) precisamente por estas divergências.

**Classificação:** `CONFORME — escopo do patch restrito à ADR-0028`

---

## 27. Decisões Adiadas

As seguintes decisões permanecem em aberto e são corretamente reconhecidas em §43:

1. **Schema concreto para declaração de política de modo da tela** (somente verbosa / somente não verbosa / alternável) — nomes de campos e valores não decididos; conceito decidido em D23.
2. **Schema concreto para modo inicial de telas alternáveis** — inclui representação de "não verboso" como modo inicial; conceito decidido em §25; campo e valor não decididos.
3. **Valores padrão quando configuração estiver ausente** — comportamento de telas sem declaração de política (relevante para legados como H-0036).
4. Todos os demais itens 1, 2, 4–15 de §43 permanecem adiados e intocados.

---

## 28. Achados

### QA-MODOS-001 — Escopo da medição de alinhamento em §36.3 não especificado

* **Seção:** §36.3 (linha 1231)
* **Severidade:** `MÉDIO`
* **Natureza:** `CORRETIVO`

**Descrição:**

§36.3 estabelece que o conteúdo do nível 2 deve alinhar-se à coluna *"determinada pelo maior texto do nível 1"*. A regra é clara quanto ao critério de alinhamento (maior texto do nível 1 determina a coluna) e quanto ao resultado (alinhamento visual entre as ocorrências). Porém, não especifica o **escopo da medição** — isto é, o conjunto de textos de nível 1 sobre o qual o "maior" é calculado.

A ADR em §27 (linhas 970–978) lista explicitamente cinco escopos possíveis: irmãos, grupo, nível, página, conteúdo completo. Sem que §36.3 declare qual se aplica, implementações distintas poderão escolher escopos diferentes e produzir colunas de alinhamento divergentes com os mesmos dados — violando o Determinismo declarado em §13.6 (linha 418).

Exemplos de geometrias incompatíveis com a mesma fixture:
- Escopo "irmãos": coluna calculada somente entre os nós irmãos do nível 1 imediatamente visíveis.
- Escopo "conteúdo completo": coluna calculada sobre todos os textos de nível 1 do documento inteiro.
- Escopo "página": coluna recalculada por página, violando §13.7.

A regra de §36.3 cumpre o critério do prompt desta auditoria de "formulação tão vaga que diferentes implementações produzam geometrias incompatíveis" — e portanto não está adequadamente especificada.

**Evidência de contradição interna:** §36.3 afirma *"preservando alinhamento visual entre as ocorrências"* — o que implica consistência. Mas sem escopo, dois renderizadores produziriam colunas distintas com os mesmos dados, violando essa consistência e §13.6.

**Correção recomendada:** Acrescentar o escopo à formulação de §36.3. Sugestão compatível com §13.7 e com §27: *"no escopo do conteúdo completo do cenário"*. Não exige nova decisão do usuário — os escopos já estão definidos no vocabulário da ADR (§27) e a escolha é determinável sem input externo.

**Exige nova decisão do usuário:** Não.

---

### QA-MODOS-002 — D23 não distingue telas novas de telas legadas

* **Seção:** D23 (linha 373), §43 item 3 (linha 1351), §39 (linha 1267)
* **Severidade:** `BAIXO`
* **Natureza:** `CORRETIVO`

**Descrição:**

D23 usa obrigação universal: *"Cada tela de console multinível deve declarar sua política de modo de apresentação"*. Simultaneamente, §43 item 3 inclui como item a ser decidido futuramente os *"valores padrão quando configuração estiver ausente"* — o que pressupõe telas sem declaração. E §39 declara as fixtures H-0036 como *"válidas"*, embora elas pré-datem D23 e não declarem política de modo.

A ADR não distingue explicitamente entre:
- telas novas abrangidas pela política de D23 (que devem declarar);
- telas legadas (H-0036 e equivalentes) ainda sem declaração (que permanecem válidas per §39).

Isso cria uma tensão de leitura: se a obrigação é universal, H-0036 seria não conforme; mas §39 a declara válida. A resolução pragmática existe implicitamente (legados são transitoriamente isentos), mas não está explicitada no texto.

**Correção recomendada:** Adicionar uma nota em D23 ou em §39 indicando que telas pré-existentes à D23 (como H-0036) permanecem válidas sem declaração de política até que uma decisão de migração futura seja tomada. Não exige nova decisão do usuário.

**Exige nova decisão do usuário:** Não.

---

### QA-MODOS-003 — Cenário 3 de §36.2 não implementável com schema atual

* **Seção:** §36.2 cenário 3, §43 item 3
* **Severidade:** `OBSERVAÇÃO`
* **Natureza:** `NÃO CORRETIVO`

**Descrição:**

O cenário 3 (tela alternável de três níveis, iniciando em modo não verboso) exige que o schema permita declarar modo inicial não verboso. O único valor de schema atualmente estabelecido é `excesso.modo: "verboso"`. Não existe `excesso.modo: "nao_verboso"` nem campo equivalente.

Esta limitação é consequência direta da decisão corretamente adiada em §43 item 3 e não constitui defeito da ADR. O conceito está decidido (D23(c), §25); o mecanismo de schema é o que está adiado. A ADR reconhece esta situação implicitamente ao incluir os nomes de campos e valores de schema na lista de itens pendentes.

Esta observação é registrada para que o ciclo de schema leve em conta que o cenário 3 só poderá ser demonstrado após a extensão do schema.

---

### QA-MODOS-004 — Contratos aplicados não refletem D23

* **Seção:** contrato_console.md §21.5 e §21.7; contrato_barra_de_menus.md §22.1; contrato_json_console.md §13.11
* **Severidade:** `OBSERVAÇÃO`
* **Natureza:** `NÃO CORRETIVO`

**Descrição:**

A aplicação documental anterior (RELATORIO_APLICACAO_ADR-0028) propagou D1–D22 antes da existência de D23. Os contratos resultantes apresentam divergências previsíveis:

- `contrato_console.md §21.5`: *"A barra de menus das demonstrações de dados multinível do console apresenta o chip [V] Verboso"* — sem restrição a telas alternáveis. Em conflito com D23 e §23.
- `contrato_console.md §21.7`: não menciona modo inicial para telas fixas nem a distinção de três políticas.
- `contrato_barra_de_menus.md §22.1`: usa *"permitir alternância verbosa"* sem vocabulário das três classes.
- `contrato_json_console.md §13.11`: *"Os mesmos dados devem ser observáveis nos modos verboso e não verboso na mesma tela"* — incompatível com telas de modo único.

Estas divergências são **esperadas** e serão resolvidas pela futura re-aplicação documental de D23. Não constituem defeito da ADR pós-patch — constituem estado transitório decorrente da sequência correta de ciclos documentais.

---

## 29. Resíduos (Achados Anteriores)

### Da aprovação anterior (RELATORIO_QA_POS_PATCH_ADR-0028)

| Achado anterior | Status nesta auditoria |
|---|---|
| QA-005 (observação sobre `V-05.qualifier`) | Preservado — fora do escopo desta auditoria |
| QA-006 (observação sobre impacto em outros módulos) | Preservado — fora do escopo desta auditoria |

Estes achados permanecem como observações históricas. Nenhum dos dois foi invalidado nem agravado pelo patch.

---

## 30. Preservações

As seguintes propriedades normativas da ADR-0028 foram verificadas como intactas após o patch:

| Propriedade | Verificado em |
|---|---|
| Origem externa dos dados em JSON | §7, §9 |
| Origem futura pelo Pipeline | §8 |
| Fronteira semântica em JSON (não matricial) | §9, §42 |
| Modelo hierárquico e tabular | §13, §17, §18, §19–20 |
| Paginação e contexto entre páginas | §30, §31 |
| Impossibilidade geométrica | §32 |
| Responsabilidades das camadas | §35 |
| Validações V-01 a V-15 | §33 |
| Decisões adiadas íntegras | §43 |
| Compatibilidade com ADR-0025, ADR-0026, ADR-0027, H-0036 | §39 |

---

## 31. Escopo Negativo (desta Auditoria)

Este relatório **não** fez e **não** autoriza:

- Correção da ADR-0028;
- Alteração de contratos;
- Alteração do handoff H-0037;
- Implementação de qualquer funcionalidade;
- Stage ou commit;
- Declaração de que a aplicação documental anterior continua válida como aplicação final da ADR;
- Aprovação do H-0037 como pronto para implementação;
- Criação de novo número de handoff.

---

## 32. Impacto sobre Aplicação Documental Anterior

A aplicação documental anterior (RELATORIO_APLICACAO_ADR-0028, status `ADR_APPLICATION_APPROVED_WITH_NOTES`) propagou D1–D22. Com a adição de D23, essa aplicação está incompleta e não pode ser considerada a aplicação final da ADR.

**Ações necessárias quando a ADR for aprovada:**
- Uma nova etapa de aplicação documental deverá propagar D23 aos contratos afetados;
- Os contratos atuais não estão errados — refletem um estado anterior autorizado — mas precisarão ser atualizados;
- A nova aplicação não requer re-aprovação da aplicação anterior (que permanece historicamente válida para D1–D22).

---

## 33. Impacto sobre o Handoff H-0037

O handoff H-0037 está operacionalmente bloqueado (`BLOQUEADO_POR_MUDANCA_DOCUMENTAL`). O QA anterior do H-0037 (`H1_HANDOFF_APPROVED`) foi emitido antes da nova decisão do usuário e **não libera** implementação no estado atual.

**Inconsistências do H-0037 em relação à nova decisão:**

| Seção H-0037 | Problema |
|---|---|
| §5: *"chip [V] Verboso na barra de menus de cada tela de demonstração"* | Incompatível com D23: chip obrigatório somente em alternáveis |
| Todos os quatro cenários H-0037: iniciando em modo verboso e alternáveis | Incompatível com §36.2: cenários 1 e 2 devem ser de modo único |
| §14.2: somente `excesso.modo: "verboso"` no schema | Bloqueia o cenário 3 de §36.2 (alternável iniciando não verboso) |
| §17, §25.1, §25.2: fixture assume chip em toda tela | Incompatível com telas de modo único |

**Ações necessárias para liberar H-0037:**
1. A ADR-0028 deve ser aprovada (após correção de QA-MODOS-001 e QA-MODOS-002);
2. A aplicação documental deve ser re-executada incorporando D23;
3. O H-0037 deve ser **patched** para incluir cenários de modo único e revisar fixtures;
4. O schema deve ser estendido (valor para modo inicial não verboso) para viabilizar o cenário 3;
5. Um novo QA do H-0037 revisado deve ser emitido.

**Não é necessário criar um novo número de handoff** — o H-0037 deve ser patched dentro do mesmo número.

---

## 34. Conclusão

O patch incorporou a decisão do usuário sobre política de modo de apresentação da tela de forma substancialmente correta. As três classes de política (somente verbosa, somente não verbosa, alternável) estão definidas em D23 com seus comportamentos completos. As restrições do chip `[V] Verboso` e da tecla `V` às telas alternáveis estão corretas. Os quatro cenários mínimos de §36.2 cobrem as três políticas. O modo inicial está determinístico para todas as políticas. As decisões adiadas foram corretamente atualizadas em §43.

**Contudo, foram identificados dois achados corretivos:**

1. **QA-MODOS-001 (MÉDIO):** §36.3 não especifica o escopo da medição do "maior texto do nível 1" para a regra de alinhamento do cenário de dois níveis. Isso viola o Determinismo (§13.6) ao permitir que implementações distintas produzam geometrias incompatíveis com os mesmos dados. A correção não exige nova decisão do usuário.

2. **QA-MODOS-002 (BAIXO):** D23 não distingue telas novas abrangidas da nova política de telas legadas (H-0036) ainda sem declaração, criando tensão com §39 e §43 item 3. A correção não exige nova decisão do usuário.

A presença de QA-MODOS-001 — um defeito de especificação que viola o Determinismo declarado pela própria ADR — resulta em rejeição desta revisão.

---

## 35. Status Literal

```text
ADR_REJECTED
```

---

## 36. Status Normalizado

```text
rejeitada
```

---

## 37. Próxima Categoria

```yaml
proxima_categoria: PATCH_ADR
escopo_do_patch:
  - "§36.3: acrescentar escopo da medição de alinhamento (QA-MODOS-001 — corretivo médio)"
  - "D23 ou §39: distinguir explicitamente telas novas de telas legadas sem declaração (QA-MODOS-002 — corretivo baixo)"
nova_decisao_do_usuario_necessaria: false
observacoes_nao_corretivas:
  - "QA-MODOS-003: schema insuficiente para cenário 3 (esperado; bloqueia apenas demonstração, não conceito)"
  - "QA-MODOS-004: contratos divergentes da D23 (esperado; serão resolvidos pela futura re-aplicação)"
```

(Fim do Relatório)
