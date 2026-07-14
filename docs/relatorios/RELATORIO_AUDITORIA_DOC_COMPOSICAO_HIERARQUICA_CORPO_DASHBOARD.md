---
name: RELATORIO_AUDITORIA_DOC_COMPOSICAO_HIERARQUICA_CORPO_DASHBOARD
description: Auditoria documental da ADR-0010 e contratos relacionados para liberar a sequência H-0011A-D de composição hierárquica do corpo
metadata:
  type: relatorio_auditoria_documental
  status: DOCUMENTATION_BLOCKED
  data: 2026-07-08
  escopo:
    - docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_processo_desenvolvimento.md
    - docs/NOMENCLATURA.md
---

# Relatório de Auditoria Documental — Composição hierárquica do corpo e dashboard

## Status final

DOCUMENTATION_BLOCKED

## Conclusão executiva

A documentação criada pelo Claude Code acerta a direção arquitetural principal:
`dashboard` deixa de ser exceção/eixo próprio no contrato central de composição
e passa a ser elemento funcional do corpo, junto com `console` e `lancador`.
A ADR-0010 está registrada, preserva a taxonomia fechada e delimita a sequência
H-0011A-D sem transformar esta etapa em implementação do Orquestrador real.

Entretanto, a liberação documental ainda deve ficar bloqueada. Permanecem
contradições normativas ativas em documentos do próprio escopo de autoridade:

1. `docs/NOMENCLATURA.md` seção 1.4 ainda declara que `tiling` nunca decide a
   posição do `dashboard` porque esse seria "eixo próprio".
2. `docs/contratos/contrato_json_tela_minima.md` ainda declara que
   `corpo.arranjo` é relevante apenas para 2+ elementos `console`/`lancador` e
   não decide `dashboard`, que seria determinado por `posicao_dashboard`.
3. `docs/contratos/contrato_json_dashboard.md` ainda declara
   `regras_exibicao.posicao_dashboard` como posição independente de `arranjo` e
   `tiling`.

Esses textos não são apenas históricos: estão em contratos/glossário ativos.
Logo, a documentação ainda não está apta para liberar H-0011A-D sem nova rodada
documental.

---

## Leitura realizada

Lidos obrigatoriamente:

```text
docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
docs/adr/INDICE_ADR.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_processo_desenvolvimento.md
docs/NOMENCLATURA.md
docs/relatorios/IMP-DOC-composicao-hierarquica-corpo-dashboard.md
docs/handoff/H-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md
docs/relatorios/RELATORIO_AUDITORIA_H-0011_HANDOFF.md
```

Lidos por coerência:

```text
docs/adr/ADR-0006-renomeacao-console-dashboard.md
docs/adr/ADR-0007-tela-processamento-composicao.md
docs/adr/ADR-0008-modelo-configuracao-por-tela.md
docs/adr/ADR-0009-caminho-formato-jsons-tela.md
docs/contratos/contrato_json_tela_minima.md
docs/contratos/contrato_json_dashboard.md
```

---

## Comandos obrigatórios executados

### `git status --short`

```text
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_processo_desenvolvimento.md
 M docs/contratos/contrato_tela_json.md
?? docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
?? docs/handoff/H-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md
?? docs/relatorios/IMP-DOC-composicao-hierarquica-corpo-dashboard.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0011_HANDOFF.md
```

### `git diff --stat`

```text
 scripts/docs/NOMENCLATURA.md                       | 11 +--
 scripts/docs/adr/INDICE_ADR.md                     |  1 +
 .../docs/contratos/contrato_composicao_corpo.md    | 81 ++++++++++++++--------
 .../contratos/contrato_processo_desenvolvimento.md | 47 ++++++++++++-
 scripts/docs/contratos/contrato_tela_json.md       | 21 +++++-
 5 files changed, 125 insertions(+), 36 deletions(-)
```

Observação: `git diff --stat` não inclui arquivos não rastreados. Portanto,
ADR-0010, o relatório de implementação documental, o H-0011 e a auditoria
H-0011 aparecem somente em `git status --short`.

### `git diff --name-only`

```text
scripts/docs/NOMENCLATURA.md
scripts/docs/adr/INDICE_ADR.md
scripts/docs/contratos/contrato_composicao_corpo.md
scripts/docs/contratos/contrato_processo_desenvolvimento.md
scripts/docs/contratos/contrato_tela_json.md
```

### Diffs específicos

Foram verificados:

```bash
git diff -- docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
git diff -- docs/adr/INDICE_ADR.md
git diff -- docs/contratos/contrato_composicao_corpo.md
git diff -- docs/contratos/contrato_tela_json.md
git diff -- docs/contratos/contrato_processo_desenvolvimento.md
git diff -- docs/NOMENCLATURA.md
```

Resultado relevante:

- `ADR-0010` é arquivo não rastreado; `git diff -- <arquivo>` não mostra seu
  conteúdo enquanto não for adicionado ao índice.
- `INDICE_ADR.md` adiciona a linha da ADR-0010.
- `contrato_composicao_corpo.md` remove a regra central de
  `posicao_dashboard` como eixo separado e declara `dashboard` como elemento
  funcional do corpo.
- `contrato_tela_json.md` passa a admitir evolução hierárquica de
  `corpo.elementos[]`, preservando compatibilidade com lista plana.
- `contrato_processo_desenvolvimento.md` adiciona a regra de mudanças
  declarativas em JSON.
- `NOMENCLATURA.md` atualiza as seções 3 e 10, mas não atualiza a seção 1.4.

---

## Classificação das ocorrências textuais

Comando executado:

```bash
grep -R "posicao_dashboard\|posição do dashboard\|Posição do dashboard\|dashboard.*eixo\|eixo.*dashboard\|dashboard.*não.*afetado.*tiling\|tiling.*dashboard" docs/NOMENCLATURA.md docs/contratos docs/adr -n
```

Classificação:

| Ocorrência | Classificação | Justificativa |
|---|---|---|
| `docs/NOMENCLATURA.md:138` | contradição bloqueante | Seção 1.4 ativa ainda diz que `tiling` nunca decide posição do `dashboard` porque seria eixo próprio. Contradiz ADR-0010 e as seções 3/10 atualizadas. |
| `docs/NOMENCLATURA.md:278` | regra ativa coerente | Linha atualizada: dashboard segue composição geral; `posicao_dashboard` descontinuado. |
| `docs/NOMENCLATURA.md:878` | regra ativa coerente | Seção 10 atualizada conforme ADR-0010. |
| `docs/contratos/contrato_json_tela_minima.md:120` | contradição bloqueante | Contrato ativo ainda separa `dashboard` de `arranjo` e remete a `posicao_dashboard`. |
| `docs/contratos/contrato_json_tela_minima.md:150` | contradição bloqueante | Reitera que `corpo.arranjo` não decide `dashboard`, independente de `arranjo`/`tiling`. |
| `docs/contratos/contrato_json_dashboard.md:88` | nota não bloqueante isolada | Exemplo JSON com campo legado pode sobreviver temporariamente, desde que rotulado como compatibilidade. Hoje o contrato não faz essa ressalva no entorno. |
| `docs/contratos/contrato_json_dashboard.md:98` | contradição bloqueante | Texto normativo ativo diz que `posicao_dashboard` declara posição relativa no corpo. |
| `docs/contratos/contrato_json_dashboard.md:114` | contradição bloqueante | Tabela ativa diz que `posicao_dashboard` é independente de `arranjo` e `tiling`. |
| `docs/contratos/contrato_json_dashboard.md:145-146` | contradição bloqueante | Regra V-7 ativa declara independência de `arranjo`/`tiling`. |
| `docs/contratos/contrato_composicao_corpo.md:128-129` | regra ativa coerente | Declara ausência/presença de dashboard como elemento, não eixo universal separado. |
| `docs/contratos/contrato_composicao_corpo.md:149-157` | regra ativa coerente | Descontinua `posicao_dashboard` como eixo separado e limita compatibilidade a H-0011A. |
| `docs/contratos/contrato_composicao_corpo.md:267` | regra ativa coerente | Reforça descontinuação no alinhamento horizontal. |
| `docs/contratos/contrato_composicao_corpo.md:359` | regra ativa coerente | Reforça em seção de tiling. |
| `docs/contratos/contrato_composicao_corpo.md:425` | regra ativa coerente | R-5 atualizado corretamente. |
| `docs/contratos/contrato_composicao_corpo.md:493-494` | regra ativa coerente | Critério de validação atualizado; compatibilidade legada explicitada. |
| `docs/contratos/contrato_composicao_corpo.md:541-542` | regra ativa coerente | Pendência de migração do campo legado está clara. |
| `docs/adr/ADR-0006-renomeacao-console-dashboard.md:144` | histórico/rastreabilidade aceitável | ADR antiga registra tarefa de aplicação da renomeação; não decide posicionamento atual. |
| `docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md:*` | histórico/rastreabilidade aceitável e regra ativa coerente | A ADR cita o problema antigo para descontinuá-lo e registra a decisão nova. |

---

## Auditoria por critério

### 1. ADR-0010

Resultado: aprovada com ressalva externa.

- Status `aceita`: adequado.
- Registrada em `docs/adr/INDICE_ADR.md`.
- Não altera ADRs antigas diretamente.
- Registra que `dashboard` segue composição geral do corpo.
- Registra `console`, `lancador` e `dashboard` como elementos funcionais.
- Preserva taxonomia fechada.
- Define composição hierárquica apenas no nível mínimo para H-0011A-D.
- Não cria novos tipos de corpo.
- Não cria foco multi-console, Tab, pop-up, seleção multi-console, execução
  multi-console ou política completa de Enter.
- Não transforma Orquestrador real completo em escopo desta etapa.

Ressalva: a ADR é coerente, mas sua aplicação documental ainda não alcançou
todos os contratos ativos que continuam contradizendo a decisão.

### 2. `contrato_composicao_corpo.md`

Resultado: aprovado.

O contrato central foi corrigido de forma compatível com a decisão do gerente:
`dashboard` é elemento funcional do corpo, passivo e não navegável por `[✥]`;
`console` segue como único tipo navegável por `[✥]`; `lancador` segue não
navegável por `[✥]`; `posicao_dashboard` foi descontinuado como eixo separado
e preservado apenas como compatibilidade temporária para H-0011A.

Não foram encontrados novos comportamentos de runtime fora de contrato nem
mistura indevida de campos internos de `dashboard` com responsabilidade do
compositor.

### 3. `contrato_tela_json.md`

Resultado: aprovado.

O contrato admite evolução de `corpo.elementos[]` para estrutura hierárquica,
preserva a lista plana atual, não exige migração imediata de JSONs e delimita
H-0011A-D sem fechar schema amplo demais antes das etapas incrementais.

### 4. `contrato_processo_desenvolvimento.md`

Resultado: aprovado.

A regra de JSON declarativo está segura porque exige simultaneamente schema já
suportado, loader/modelo preservando e validando campos, renderer/binding
interpretando a declaração, ausência de novo comportamento de código, ausência
de novo tipo estrutural, ausência de nova ação/navegação/binding/regra de
renderização, ausência de mudança contratual e ausência de mudança
arquitetural.

Também exige ciclo formal para novo binding, nova validação estrutural, nova
regra de renderização, nova navegação, nova ação, novo tipo estrutural, mudança
de contrato, mudança de arquitetura ou alteração de código. A regra não vira
autorização genérica para alterar JSON com efeito estrutural ainda não suportado.

### 5. `NOMENCLATURA.md`

Resultado: reprovado.

As seções 3 e 10 foram atualizadas corretamente, mas a seção 1.4 ainda contém
linguagem ativa de `dashboard` como eixo próprio separado. Isso contradiz
ADR-0010 e o contrato central atualizado.

Não há reintrodução de `Info` como tipo ativo nem confusão nova entre
`dashboard`, `console`, `lancador` e `barra_de_menus`. A distinção entre
schema/semântica e dados concretos permanece adequada.

### 6. Escopo Git

Resultado: aprovado.

Verificações adicionais:

```bash
git status --short tela config tests
git diff --name-only -- tela config tests
git status --short config/telas/orquestrador.json config/telas/stub_b.json config/telas/destino_minimo.json
git diff -- config/telas/orquestrador.json config/telas/stub_b.json config/telas/destino_minimo.json
```

Todos retornaram vazio.

Conclusão de escopo:

- Não houve alteração em `tela/`.
- Não houve alteração em `config/`.
- Não houve alteração em `tests/`.
- Nenhum JSON de configuração foi alterado, incluindo:
  - `config/telas/orquestrador.json`;
  - `config/telas/stub_b.json`;
  - `config/telas/destino_minimo.json`.

---

## Achados bloqueantes

### B-1. `NOMENCLATURA.md` ainda mantém `dashboard` como eixo próprio em seção ativa

`docs/NOMENCLATURA.md` seção 1.4 ainda afirma que `tiling` se aplica apenas a
`console`/`lancador` e "nunca decide posição do objeto `dashboard`", pois esse
seria "eixo próprio". Essa frase contradiz diretamente a ADR-0010 e as seções
3 e 10 atualizadas do mesmo arquivo.

### B-2. `contrato_json_tela_minima.md` contradiz ADR-0010

O contrato ativo ainda declara que `arranjo` é relevante para 2+ elementos
`console`/`lancador` e que não decide a posição do `dashboard`, determinada
por `posicao_dashboard`. Isso mantém exatamente a exceção que a ADR-0010
pretende remover.

### B-3. `contrato_json_dashboard.md` contradiz ADR-0010

O contrato ativo do envelope mínimo de `dashboard` ainda trata
`regras_exibicao.posicao_dashboard` como regra normal de posicionamento
independente de `arranjo` e `tiling`. O campo poderia permanecer apenas como
legado/compatibilidade em H-0011A, mas o contrato atual ainda o apresenta como
regra ativa.

### B-4. Relatório de implementação documental não detectou as contradições remanescentes

`IMP-DOC-composicao-hierarquica-corpo-dashboard.md` reporta
`DOCUMENTATION_COMPLETED`, mas sua própria lista de verificações não registra a
busca textual obrigatória ampla nem as ocorrências remanescentes nos contratos
incrementais de JSON. O status final informado pelo relatório de implementação
não é suficiente para liberar a documentação.

---

## Achados não bloqueantes

1. `ADR-0010` e `IMP-DOC-composicao-hierarquica-corpo-dashboard.md` estão
   não rastreados. Isso é esperado antes de `git add`, mas deve ser considerado
   na entrega final.
2. `H-0011` e `RELATORIO_AUDITORIA_H-0011_HANDOFF.md` também aparecem não
   rastreados no estado atual. Como a tarefa atual é auditoria documental e
   esses arquivos foram tratados como leitura obrigatória, isto é condição de
   rastreabilidade, não alteração de código.
3. A ocorrência de `posicao_dashboard` no exemplo JSON de
   `contrato_json_dashboard.md` poderia ser aceitável como compatibilidade
   temporária, desde que o contrato fosse reescrito para marcar o campo como
   legado/descontinuado. No estado atual, o entorno normativo torna a ocorrência
   bloqueante.

---

## Recomendação

Antes de liberar H-0011A-D, executar uma correção documental limitada:

```text
docs/NOMENCLATURA.md
docs/contratos/contrato_json_tela_minima.md
docs/contratos/contrato_json_dashboard.md
docs/relatorios/IMP-DOC-composicao-hierarquica-corpo-dashboard.md
```

Objetivo da correção:

- remover a linguagem ativa de `dashboard` como eixo próprio na seção 1.4 de
  `NOMENCLATURA.md`;
- alinhar os contratos incrementais de JSON à ADR-0010;
- manter `posicao_dashboard` apenas como campo legado/compatibilidade para
  H-0011A, se necessário;
- registrar no relatório de implementação a busca textual e a resolução das
  ocorrências remanescentes.

Não há recomendação de alterar código, testes ou JSONs de configuração nesta
etapa.

---

## Decisão da auditoria

A documentação está parcialmente correta, mas não liberada.

Status recomendado para a sequência H-0011A-D:

```text
ARCHITECTURE_REVIEW_REQUIRED
```

Motivo: persistem contradições normativas ativas sobre `dashboard` como eixo
próprio/`posicao_dashboard` independente em `NOMENCLATURA.md` e contratos JSON
incrementais ativos.
