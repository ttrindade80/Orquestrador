# RELATORIO_QA_POS_PATCH_ADR-0019

## 1. Identificação

- Artefato auditado: `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md`
- Categoria processual executada: `QA_ADR` (reauditoria pós-patch)
- Auditor: agente formal de QA da ADR-0019 (pós-patch)
- Data: 2026-07-12
- Branch: `master`
- Commit base: `40015b6 feat: implementa distribuicao horizontal percentual e fracionaria`
- Evidência de origem: `docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md`
- QA anterior (rejeitado): `docs/relatorios/RELATORIO_QA_ADR-0019.md`

## 2. Objetivo

Auditar formalmente a ADR-0019 após o patch do executor, verificando exclusivamente se todos os
achados do QA anterior (QA-001 a QA-004) foram resolvidos sem regressão, ampliação de escopo,
decisão nova ou aplicação documental antecipada.

Limites estritos:
- não corrigir a ADR;
- não aplicar a ADR;
- não alterar ADR-0007, contratos, nomenclatura ou índice;
- não criar handoff;
- não implementar;
- não preparar commit.

O único artefato produzido é este relatório.

## 3. Estado Git inicial

Comandos executados a partir da raiz do repositório Git
(`/home/tiago/Dropbox/UFRGS/Survey/versao_0_1`); os caminhos declarados na documentação são
relativos a `scripts/`.

```text
git rev-parse --show-toplevel
  /home/tiago/Dropbox/UFRGS/Survey/versao_0_1

git log --oneline -1
  40015b6 feat: implementa distribuicao horizontal percentual e fracionaria

git status --short
  ?? scripts/docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
  ?? scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md
  ?? scripts/docs/relatorios/RELATORIO_QA_ADR-0019.md
  ?? scripts/tela/__pycache__/

git diff --stat                   (sem saída)
git diff --name-only              (sem saída)
git diff --check                  (sem saída)
git diff --cached --stat          (sem saída)
git diff --cached --name-only     (sem saída)
```

Estado confirmado: stage vazio, nenhuma alteração rastreada. Coincide com o estado comprovado
informado pelo executor (três arquivos novos não rastreados sob `scripts/docs/` mais o diretório
pré-existente `scripts/tela/__pycache__/`). Como a ADR-0019 é não rastreada, seu conteúdo foi
inspecionado por leitura direta e por `git diff --no-index /dev/null` (mecanismo apropriado para
arquivo novo).

## 4. Artefatos consultados

Autoridades normativas (leitura integral, sem alteração):

- `docs/adr/ADR-0007-tela-processamento-composicao.md`
- `docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md`
- `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`
- `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`
- `docs/NOMENCLATURA.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/adr/INDICE_ADR.md`

Artefato principal do QA (leitura integral):

- `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md`

Evidência de origem (leitura integral):

- `docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md`

QA anterior (leitura integral; evidência do QA rejeitado, não alterado):

- `docs/relatorios/RELATORIO_QA_ADR-0019.md`

Buscas de evidência via `rg` para confirmar: ausência de "nívels", ausência de "especializa",
presença de "supera parcialmente" e "substitui parcialmente", localização de todas as ocorrências
de "zero ou um dashboard" nas autoridades, e presença de ADR-0007 em cada seção da ADR.

Implementação e testes não foram usados como fonte de arquitetura; as citações de `tela/*.py`
existentes na ADR-0019 continuam a figurar apenas na seção de consequências futuras, como
descrição do estado divergente atual, não como autoridade normativa.

## 5. Decisões D1 a D7

Reauditoria da fidelidade de cada decisão após o patch. O patch adicionou a seção "Relação com
ADR-0007", corrigiu a grafia "nívels", padronizou a terminologia da relação com ADR-0015 e refinou
a nota de consequência da NOMENCLATURA. As decisões D1 a D7 em si não foram alteradas em conteúdo
normativo.

### D1 — Contagem por níveis de grupos

Registrada em "D1 — O limite hierárquico é contado por níveis de grupos"
(`ADR-0019:104-131`). Fiel: a profundidade é contada exclusivamente por níveis de grupos (nós
estruturais `grupo`); o corpo raiz não conta como nível de grupo (`ADR-0019:123`); elementos
funcionais não acrescentam nível de grupo (`ADR-0019:125-127`); bloco de definição dos níveis
1, 2 e 3 (`ADR-0019:113-120`). A afirmação "Esta decisão substitui a leitura operacional anterior"
(`ADR-0019:129`) está agora coerente com a seção "Relação com ADR-0015" (ver QA-003).

### D2 — Profundidade máxima de três níveis de grupos

Registrada em "D2 — Profundidade máxima de três níveis de grupos" (`ADR-0019:135-146`). Fiel:
limite três contado em níveis de grupos; grupo de nível 3 válido; grupo de nível 4 inválido;
validação futura deverá distinguir profundidade de grupos de profundidade genérica de listas, sem
definir mensagens nem implementar.

### D3 — Elementos funcionais dentro de um grupo do nível 3

Registrada em "D3" (`ADR-0019:150-160`). Fiel: grupo de nível 3 pode conter um ou mais elementos
funcionais (`console`, `lancador`, `dashboard`); não pode conter outro `grupo`; elementos
funcionais não constituem nível 4 de grupo.

### D4 — Proibição de grupo no nível de grupo 4 ou superior

Registrada em "D4" (`ADR-0019:164-171`). Fiel: `grupo` filho de grupo do nível 3 é estruturalmente
inválido; estruturas no nível 4 ou superior devem ser rejeitadas com erro estrutural determinístico;
a forma exata do erro é decisão de implementação futura.

### D5 — Multiplicidade de grupos irmãos

Registrada em "D5" (`ADR-0019:175-184`). Fiel: múltiplos grupos irmãos permitidos em qualquer
nível permitido; a ADR não introduz cardinalidade máxima para grupos irmãos.

### D6 — Multiplicidade de elementos funcionais dentro de grupos

Registrada em "D6" (`ADR-0019:188-205`). Fiel: grupo — incluindo nível 3 — pode conter mais de um
elemento funcional; regras já existentes (ordem, filhos diretos, arranjo, distribuição, associação
posicional) permanecem em vigor, sem reescrita nem aplicação nesta etapa.

### D7 — Remoção da cardinalidade global de um dashboard por tela

Registrada em "D7" (`ADR-0019:209-233`). Fiel: "zero ou um dashboard por tela" removido como regra
global do tipo; tela pode conter mais de um dashboard; dashboards podem aparecer em grupos
distintos; não há cardinalidade máxima substituta (`ADR-0019:219`); preserva natureza passiva,
navegabilidade, `[✥]`, arranjo, distribuição, estrutura interna e regras específicas de telas
concretas com apenas um dashboard. O patch não alterou o conteúdo normativo de D7.

## 6. Matriz de resolução do patch

| Achado anterior | Correção esperada | Evidência na ADR pós-patch | Resultado |
| --------------- | ----------------- | -------------------------- | --------- |
| QA-001 — CONSEQUENCIA_DOCUMENTAL_INCOMPLETA (ADR-0007 não identificada; relação com ADR-0007 ausente) | Incluir ADR-0007 nos documentos afetados; adicionar seção "Relação com ADR-0007"; declarar superação parcial apenas quanto à cardinalidade "zero ou um dashboard"; declarar que telas de processamento podem conter múltiplos dashboards; preservar os demais pontos da ADR-0007; distinguir regra normativa de categoria de tela de configuração de tela concreta; identificar para aplicação futura as ocorrências relevantes (ponto de decisão 3 e exemplo); não alterar ADR-0007 diretamente | Frontmatter `contratos_afetados` inclui `docs/adr/ADR-0007-tela-processamento-composicao.md` (`ADR-0019:18`); seção "Relação com ADR-0007" (`ADR-0019:385-428`); "supera parcialmente a ADR-0007 exclusivamente nas formulações de cardinalidade" (`ADR-0019:395-396`); "telas de processamento passam a admitir mais de um dashboard" (`ADR-0019:397-398`); preservação dos demais pontos listada (`ADR-0019:408-416`); distinção entre regra de categoria e configuração de tela concreta (`ADR-0019:400-406`); ocorrências para aplicação futura identificadas — ponto de decisão 3 (`ADR-0007:71`) e exemplo (`ADR-0007:123`) (`ADR-0019:418-428`, tabela `ADR-0019:489`, critérios `ADR-0019:533-535`); ADR-0007 não alterada (git diff vazio) | RESOLVIDO |
| QA-002 — grafia "nívels" | Remover "nívels"; substituir por "níveis" sem alterar sentido normativo | `rg "nívels"` em ADR-0019: sem ocorrências; `rg -c "níveis"` em ADR-0019: 22 ocorrências; sentido normativo preservado (substituição meramente ortográfica) | RESOLVIDO |
| QA-003 — terminologia "especializa" × "substitui" | Padronizar terminologia; usar formulação coerente de substituição parcial da regra de contagem da ADR-0015; eliminar concorrência entre "especializa" e "substitui"; preservar ADR-0015 nos demais pontos; não cancelar integralmente ADR-0015 | `rg "especializa"` em ADR-0019: sem ocorrências; seção "Relação com ADR-0015" usa "substitui parcialmente a regra de contagem de profundidade da ADR-0015" (`ADR-0019:449`) e "Esta ADR não reescreve nem cancela a ADR-0015. Substitui somente o critério de contagem de profundidade" (`ADR-0019:456-457`); D1 usa "substitui a leitura operacional anterior" (`ADR-0019:129`) — coerente; ADR-0015 permanece vigente nos demais pontos (`ADR-0019:452-454`) | RESOLVIDO |
| QA-004 — consequência documental da NOMENCLATURA | Identificar revisão normativa substantiva das formulações que contam corpo raiz como nível 0, declaram nível 3 proibido e rejeitam profundidade ≥ 3 pela contagem antiga; apenas identificar, não aplicar | Tabela de documentos a atualizar, linha NOMENCLATURA: "Revisão normativa substantiva (não apenas terminológica): remover ou corrigir as formulações que contam o corpo raiz como nível 0; remover ou corrigir a afirmação 'Nível 3 proibido'; remover ou corrigir a rejeição de estruturas com profundidade ≥ 3 segundo a contagem antiga; alinhar à contagem exclusiva por níveis de grupos e à permissão de três níveis de grupos (D1, D2)" (`ADR-0019:488`); NOMENCLATURA não alterada (git diff vazio); formulações confirmadas em `NOMENCLATURA.md:1149-1150` e `:1154-1155` | RESOLVIDO |

Todos os quatro achados anteriores estão RESOLVIDOS, sem regressão, sem ampliação de escopo, sem
decisão nova e sem aplicação prematura.

## 7. Análise da relação com ADR-0007

A nova seção "Relação com ADR-0007" (`ADR-0019:385-428`) resolve integralmente QA-001. Verificação
ponto a ponto dos oito critérios exigidos:

1. **ADR-0007 entre os documentos afetados**: presente no frontmatter `contratos_afetados`
   (`ADR-0019:18`), na tabela de documentos a atualizar (`ADR-0019:489`) e nos critérios para
   futura aplicação (`ADR-0019:533-535`). Confirmado.
2. **Seção explícita "Relação com ADR-0007"**: existente (`ADR-0019:385`). Confirmado.
3. **Superação parcial somente quanto à cardinalidade "zero ou um dashboard"**: "Essa remoção
   supera parcialmente a ADR-0007 exclusivamente nas formulações de cardinalidade 'zero ou um
   dashboard'" (`ADR-0019:394-396`). Confirmado.
4. **Telas de processamento podem conter múltiplos dashboards**: "telas de processamento passam a
   admitir mais de um dashboard, exatamente como qualquer outra tela" (`ADR-0019:397-398`).
   Confirmado. Este ponto não é decisão pendente — já está decidido em D7 ("inclusive uma tela de
   processamento, pode conter múltiplos dashboards").
5. **Demais pontos da ADR-0007 preservados**: listados explicitamente (`ADR-0019:408-416`) —
   tela de processamento não é quarto tipo de corpo; taxonomia fechada; `console` como região
   interativa; `dashboard` como saída passiva; `lancador` não representa processamento; chips na
   `barra_de_menus`; regras de `[✥]` inalteradas. Confirmado.
6. **Distinção entre regra normativa de categoria de tela e configuração de tela concreta**: a ADR
   explicita que a formulação de ADR-0007 é "uma restrição normativa para a categoria de tela de
   processamento — não a declaração de configuração de uma tela concreta individual" e por isso não
   se enquadra na preservação de "tela concreta" de D7 (`ADR-0019:400-406`). Confirmado.
7. **Identificação das ocorrências para futura aplicação**: ponto de decisão 3 (`ADR-0007:71`) e
   exemplo da seção "Composição conceitual" (`ADR-0007:123`), ambos identificados para substituição
   por formulação sem cardinalidade máxima (`ADR-0019:418-428`, `:489`, `:533-535`). Confirmado por
   leitura direta de `ADR-0007:71` e `:123`.
8. **Não alteração da ADR-0007**: `git diff --stat` vazio; ADR-0007 inalterada. Confirmado.

A afirmação "A D7 prevalece" (`ADR-0019:406`) não constitui decisão nova: é a aplicação lógica de
D7 (decisão explícita do usuário posterior, que remove cardinalidade global do tipo, incluindo a
categoria de tela de processamento) sobre a formulação anterior de ADR-0007. A ADR-0019 não cria
exceção, não cria limite máximo, não cria política nova para telas de processamento.

## 8. Análise da relação com ADR-0015

A seção "Relação com ADR-0015" (`ADR-0019:446-457`) está agora coerente com D1 e resolve QA-003.

- A ADR usa exclusivamente "substitui parcialmente" para descrever a mudança do critério de
  contagem de profundidade (`ADR-0019:449`). A palavra "especializa" foi totalmente removida
  (`rg "especializa"` sem ocorrências).
- D1 usa "substitui a leitura operacional anterior" (`ADR-0019:129`), formulação coerente com a
  relação — não há mais concorrência terminológica.
- A ADR-0015 permanece vigente em todos os demais pontos: arranjo por container, distribuição por
  container, arredondamento, preenchimento de área alocada e demais decisões
  (`ADR-0019:452-454`).
- A ADR-0019 declara expressamente "não reescreve nem cancela a ADR-0015" (`ADR-0019:456`).
- Não houve cancelamento integral indevido da ADR-0015.

Observação terminológica (não bloqueante): a ADR usa "supera parcialmente" para a ADR-0007
(`ADR-0019:395`) e "substitui parcialmente" para a ADR-0015 (`ADR-0019:449`). A distinção é
correta e intencional: a relação com ADR-0007 é supressão/superação de uma cardinalidade (sem
substituição por nova regra de contagem); a relação com ADR-0015 é substituição de um critério de
contagem por outro critério de contagem. Os verbos distintos refletem naturezas distintas de
relação, ambas previstas nas instruções de QA (QA-001 usa "supera"; QA-003 usa "substituição").
Não exige correção.

## 9. Análise da consequência para NOMENCLATURA

A nota de consequência para NOMENCLATURA foi refinada e resolve QA-004.

A tabela de documentos a atualizar, linha NOMENCLATURA (`ADR-0019:488`), agora declara:

> Revisão normativa substantiva (não apenas terminológica): remover ou corrigir as formulações que
> contam o corpo raiz como nível 0; remover ou corrigir a afirmação "Nível 3 proibido"; remover ou
> corrigir a rejeição de estruturas com profundidade ≥ 3 segundo a contagem antiga; alinhar à
> contagem exclusiva por níveis de grupos e à permissão de três níveis de grupos (D1, D2).

Os três pontos exigidos estão explícitos:
- formulações que contam corpo raiz como nível 0 — confirmado em `NOMENCLATURA.md:1149-1150`;
- afirmação "Nível 3 proibido" — confirmado em `NOMENCLATURA.md:1154-1155`;
- rejeição de profundidade ≥ 3 segundo a contagem antiga — confirmado em `NOMENCLATURA.md:1154-1155`.

A ADR apenas identifica a futura revisão. Não altera a NOMENCLATURA (`git diff --stat` vazio). A
classificação como "revisão normativa substantiva (não apenas terminológica)" sinaliza
corretamente a gravidade, corrigindo a subestimação observada no QA anterior.

## 10. Análise de regressões

Verificação de ausência de regressão e de decisão nova introduzida pelo patch:

1. **Nova exceção de cardinalidade**: ausente. D7 remove a cardinalidade global e não cria
   substituta (`ADR-0019:219`). A relação com ADR-0007 não introduz exceção para telas de
   processamento — declara que seguem a regra global.
2. **Limite máximo de dashboards**: ausente. `rg "cardinalidade máxima|limite máximo|máximo de
   dashboards"` retorna apenas declarações negativas ("não introduz cardinalidade máxima",
   "não cria cardinalidade máxima substituta", fora de escopo).
3. **Política nova para telas de processamento**: ausente. A seção "Relação com ADR-0007" aplica D7
   à categoria, não cria política distinta.
4. **Nova cardinalidade para grupos**: ausente. D5 mantém "não introduz cardinalidade máxima para
   grupos irmãos" (`ADR-0019:184`).
5. **Nova estratégia de implementação**: ausente. As consequências futuras para loader, modelo,
   renderizador e testes continuam identificadas, não aplicadas (`ADR-0019:329-351`).
6. **Nova regra de arranjo ou distribuição**: ausente. ADR-0015 e ADR-0018 permanecem vigentes.
7. **Mudança na natureza de dashboard**: ausente. D7 preserva natureza passiva e não navegável
   (`ADR-0019:222-228`).
8. **Alteração da navegação**: ausente. Regras de `[✥]` preservadas (`ADR-0019:416`).
9. **Regra não decidida sobre telas concretas**: ausente. A distinção entre regra normativa de
   categoria e configuração declarativa de tela concreta está explicitada e corresponde ao
   decidido em D7.

### Coerência interna

- **Conflito entre D7 e a nova seção sobre ADR-0007**: ausente. A seção afirma que D7 prevalece
  sobre a cardinalidade de ADR-0007, exatamente o decidido.
- **Trecho que preserve "zero ou um dashboard" como limite para telas de processamento**: ausente.
  A ADR afirma o oposto (`ADR-0019:397-398`).
- **Cancelamento integral de ADR-0007**: ausente. "supera parcialmente" e lista de preservação
  (`ADR-0019:408-416`).
- **Conflito entre "substitui parcialmente" e outras seções**: ausente após padronização.
- **Divergência entre frontmatter, relações, tabela e critérios**: ausente. Os documentos
  afetados são coerentes em frontmatter (`ADR-0019:12-18`), tabela (`ADR-0019:485-490`) e
  critérios (`ADR-0019:526-542`).
- **Exemplos incompatíveis com D1 a D7**: ausente. Os quatro exemplos conceituais
  (`ADR-0019:244-297`) permanecem compatíveis.

### Consequências documentais

A lista de aplicação futura inclui todos os documentos exigidos:

- `docs/adr/ADR-0007-tela-processamento-composicao.md` (`ADR-0019:489`)
- `docs/contratos/contrato_composicao_corpo.md` (`ADR-0019:485`)
- `docs/contratos/contrato_tela_json.md` (`ADR-0019:486`)
- `docs/contratos/contrato_json_tela_minima.md` (`ADR-0019:487`)
- `docs/NOMENCLATURA.md` (`ADR-0019:488`)
- `docs/adr/INDICE_ADR.md` (`ADR-0019:490`)

Todas identificadas, nenhuma aplicada.

Sem regressões identificadas.

## 11. Análise de metadados

- ID correto `ADR-0019` (`ADR-0019:2`, `:22`).
- Status `proposta` (`ADR-0019:6`, `:26`) — adequado para ADR não aprovada.
- Ausência de declaração de aplicação concluída: "Esta ADR não altera código, testes, JSON de
  tela, contratos, nomenclatura, handoffs, relatórios, índice de ADRs, estado operacional ou
  histórico Git. Cria somente este arquivo." (`ADR-0019:564-567`).
- Documentos afetados coerentes entre frontmatter, tabela e critérios.
- Ausência de alteração de arquivos existentes: `git diff --stat` vazio e
  `git diff --cached --stat` vazio.
- `substitui: null` (`ADR-0019:8`) — coerente com o modelo de substituição parcial (mesmo padrão
  das ADRs 0018 e 0015 que também substituem parcialmente ADRs anteriores).
- `handoffs_bloqueados: []` (`ADR-0019:19`) — coerente; a ADR não bloqueia handoff específico.

Sem defeitos de metadados.

## 12. Análise de escopo

Permanecem fora de escopo (`ADR-0019:494-518`), confirmados:

- aplicação da ADR;
- alteração direta da ADR-0007 (git diff vazio);
- atualização dos contratos (git diff vazio);
- atualização da NOMENCLATURA (git diff vazio);
- atualização do índice (git diff vazio);
- implementação;
- testes;
- criação de handoff;
- preparação de commit.

Nenhum item de escopo negativo foi violado.

## 13. Achados novos

Nenhum achado novo bloqueante, alto, médio ou baixo foi identificado.

### Observação (não bloqueante) — OBS-001

- ID: `OBS-001`.
- Severidade: observação.
- Categoria: `TERMINOLOGIA_INTENCIONAL`.
- Descrição: a ADR usa "supera parcialmente" para a relação com ADR-0007 (`ADR-0019:395`) e
  "substitui parcialmente" para a relação com ADR-0015 (`ADR-0019:449`). A distinção é correta
  e reflete naturezas distintas de relação (supressão de cardinalidade vs. substituição de
  critério de contagem), alinhada às instruções de QA-001 e QA-003.
- Decisão ou autoridade afetada: nenhuma.
- Evidência: `ADR-0019:395`, `:449`.
- Impacto: nenhum; mera documentação para futuros leitores.
- Exige patch da ADR: não.
- Exige nova decisão do usuário: não.

## 14. Conclusão

A reauditoria pós-patch confirma que todos os quatro achados do QA anterior foram RESOLVIDOS:

- **QA-001** (média): ADR-0007 agora está incluída nos documentos afetados, possui seção própria
  "Relação com ADR-0007", declara superação parcial apenas quanto à cardinalidade "zero ou um
  dashboard", preserva os demais pontos, distingue regra de categoria de configuração concreta,
  identifica as ocorrências para aplicação futura e não altera ADR-0007 diretamente.
- **QA-002** (baixa): grafia "nívels" removida; "níveis" usado sem alteração de sentido normativo.
- **QA-003** (baixa): "especializa" removido; terminologia padronizada em "substitui parcialmente";
  coerência entre D1 e a relação com ADR-0015; ADR-0015 preservada nos demais pontos.
- **QA-004** (baixa): nota de consequência da NOMENCLATURA refinada para identificar revisão
  normativa substantiva das três formulações conflitantes; NOMENCLATURA não alterada.

As decisões D1 a D7 permanecem fiéis. O patch não introduziu decisão nova, não ampliou escopo, não
criou regressão e não aplicou documentação antecipadamente. A coerência interna, os metadados, o
escopo negativo e as consequências documentais estão corretos. Não há achados novos bloqueantes,
altos, médios ou baixos — apenas uma observação não bloqueante (OBS-001) sobre a distinção
intencional de verbos.

## 15. Status final

```text
ADR_APPROVED
```

Justificativa: QA-001 a QA-004 resolvidos; D1 a D7 fiéis; nenhum defeito que exija alteração;
nenhuma decisão nova; nenhuma aplicação prematura. A observação OBS-001 não exige correção antes
da aplicação.

## 16. Próxima categoria processual (sem executá-la)

A próxima categoria processual permitida é a aplicação documental da ADR-0019, que deverá:

- substituir nos contratos a formulação de nível pela contagem exclusiva por níveis de grupos (D1);
- registrar explicitamente que elementos funcionais em grupo do nível 3 não constituem nível 4 (D3);
- registrar proibição de grupo no nível 4 (D4);
- remover "zero ou um dashboard por tela" como regra global dos contratos (D7);
- revisar na ADR-0007 o ponto de decisão 3 (`ADR-0007:71`) e o exemplo (`ADR-0007:123`);
- revisar NOMENCLATURA seção 14 como revisão normativa substantiva;
- atualizar exemplos normativos;
- registrar ADR-0019 no índice.

Esta categoria não foi executada nesta reauditoria.

## 17. Estado Git final

```text
git status --short
  ?? scripts/docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
  ?? scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md
  ?? scripts/docs/relatorios/RELATORIO_QA_ADR-0019.md
  ?? scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0019.md
  ?? scripts/tela/__pycache__/

git diff --stat                   (sem saída)
git diff --name-only              (sem saída)
git diff --check                  (sem saída)
git diff --cached --stat          (sem saída)
git diff --cached --name-only     (sem saída)
```

O único novo arquivo adicional criado é
`docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0019.md`. Nenhum arquivo rastreado foi alterado. A
ADR-0019, o relatório de levantamento, o relatório de QA anterior e `tela/__pycache__/` permanecem
não rastreados, sem alteração, remoção, movimentação ou stage. Stage permanece vazio.
