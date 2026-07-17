# Relatório de QA pós-patch da aplicação da ADR-0026

## 1. Identificação

| Campo | Valor |
|---|---|
| Identificador do relatório | RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0026 |
| Data de execução | 2026-07-17 |
| Etapa executada | QA_APLICACAO_ADR |
| Tipo de QA | POS_PATCH |
| ADR auditada | ADR-0026 — Fornecimento externo de dados ao console por JSON multinível |
| Relatório de aplicação auditado | `docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md` |
| QA de origem do patch | `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0026.md` |
| Papel | Auditor documental independente |

## 2. Escopo

Este relatório verifica exclusivamente o patch da aplicação da ADR-0026,
limitado aos achados `QAAPADR-0026-001` e `QAAPADR-0026-002`, ao escopo real
do patch, à ausência de regressão e à fidelidade da atualização do relatório
de aplicação.

Não foram corrigidos arquivos, alteradas ADRs, alterados contratos, alterados
relatórios anteriores, implementado código, criado handoff, preparado commit
ou executado commit.

## 3. Autoridades e evidências

Foram lidos integralmente:

- `docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md`
- `docs/relatorios/RELATORIO_QA_ADR-0026.md`
- `docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md`
- `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0026.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/adr/INDICE_ADR.md`

Foi consultado o precedente:

- `docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md`

Evidências Git e buscas executadas:

- `git status --short`
- `git diff --name-only`
- `git diff --check`
- `git ls-files --others --exclude-standard`
- `git diff -- docs/contratos/contrato_tela_json.md`
- `git diff -- docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md`
- `git diff -- docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md`
- buscas focais por `A especificação normativa completa está na ADR-0025.`
- buscas focais por formas de status da ADR-0026

Observação operacional: neste checkout, a raiz Git é o diretório atual e os
artefatos estão sob `docs/...`, não sob `scripts/docs/...`. Os comandos foram
executados com os caminhos reais do repositório.

## 4. Estado Git

Estado verificado antes da criação deste relatório:

```yaml
branch: master
head: fb9e5be
stage: vazio
commit_novo: nao_realizado
git_diff_check: sem_erros
workspace:
  modificados:
    - docs/NOMENCLATURA.md
    - docs/adr/INDICE_ADR.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_json_console.md
    - docs/contratos/contrato_tela_json.md
  nao_rastreados:
    - docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md
    - docs/relatorios/RELATORIO_QA_ADR-0026.md
    - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0026.md
```

O conjunto modificado acumulado inclui a aplicação documental da ADR-0026 e
artefatos anteriores do ciclo. O patch pós-QA foi avaliado de forma focal, sem
atribuir automaticamente ao patch todas as diferenças acumuladas contra `HEAD`.

## 5. Verificação do achado QAAPADR-0026-001

```yaml
achado_original: QAAPADR-0026-001
arquivo: docs/contratos/contrato_tela_json.md
status: corrigido
```

Resultado verificado:

- a frase `A especificação normativa completa está na ADR-0025.` não permanece
  no final da seção 31.6 nem no ponto original;
- a busca focal encontrou a frase apenas em relatórios que descrevem o achado
  e a correção, não como regra ativa do contrato;
- o final da seção 31.6 está estruturalmente correto em Markdown;
- os três itens de remissão da seção 31.6 permanecem presentes e separados:
  `contrato_json_console.md` seção 11, `contrato_console.md` seção 19 e
  `docs/NOMENCLATURA.md` seção 17;
- nenhum item da lista foi removido ou incorporado acidentalmente a outro item;
- o diff de `contrato_tela_json.md` mostra a remoção da frase órfã e a
  inserção acumulada da seção 31, sem alteração adicional de regra do contrato
  atribuível ao patch;
- a seção 30 permanece coerente com a ADR-0025 e encerra com a remissão à
  NOMENCLATURA seção 16.

Não há contradição nova com a seção 30 nem com a ADR-0025.

## 6. Verificação do achado QAAPADR-0026-002

```yaml
achado_original: QAAPADR-0026-002
arquivo: docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
status: corrigido
```

As três ocorrências vigentes do status da ADR-0026 foram confirmadas:

```yaml
frontmatter: aceita e aplicada
tabela_de_identificacao: aceita e aplicada
secao_2: aceita e aplicada
```

Resultado verificado:

- as três ocorrências existem realmente;
- todas representam o estado vigente da ADR, não referência histórica;
- a alteração é coerente com o índice e com o precedente da ADR-0025;
- não permanece ocorrência normativa concorrente de `status: aceita` no arquivo
  da ADR-0026;
- o índice registra a ADR-0026 como `aceita e aplicada`;
- data, título e caminho da ADR permanecem coerentes;
- decisão, consequências, pendências e fronteiras arquiteturais da ADR não
  foram modificadas pelo patch;
- não foi reescrito conteúdo fora do status.

## 7. Escopo real do patch

Arquivos confirmados como pertencentes ao patch pós-QA:

```yaml
arquivos_do_patch_confirmados:
  - docs/contratos/contrato_tela_json.md
  - docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md
```

Diferenciação de escopo:

```yaml
conjunto_acumulado_adr_0026:
  modificados_rastreados:
    - docs/NOMENCLATURA.md
    - docs/adr/INDICE_ADR.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_json_console.md
    - docs/contratos/contrato_tela_json.md
  nao_rastreados_preexistentes:
    - docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md
    - docs/relatorios/RELATORIO_QA_ADR-0026.md
    - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0026.md
arquivo_novo_criado_por_este_qa:
  - docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0026.md
arquivos_inesperados_do_patch: []
```

O diff acumulado contra `HEAD` ainda lista arquivos da aplicação original
(`NOMENCLATURA`, `INDICE_ADR`, `contrato_console`, `contrato_json_console` e
`contrato_tela_json`). Esses arquivos não são classificados como inesperados
apenas por estarem presentes no workspace acumulado da ADR-0026.

## 8. Fidelidade do relatório de aplicação

A seção 15 do relatório de aplicação foi verificada.

Resultado:

- identifica corretamente o QA de origem:
  `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0026.md`;
- lista exatamente os dois achados corrigidos:
  `QAAPADR-0026-001` e `QAAPADR-0026-002`;
- descreve fielmente a remoção da frase órfã em `contrato_tela_json.md`;
- descreve fielmente a atualização dos três status da ADR-0026;
- registra verificações executadas, ausência de bloqueios, stage vazio e
  ausência de commit;
- não altera nem apaga o resultado histórico da aplicação original;
- não declara autoaprovação;
- não apresenta o QA pós-patch como já concluído;
- não cria decisão normativa nova.

Nota não corretiva: a seção 15.1 usa o rótulo `arquivos_corrigidos` para listar
os dois artefatos substantivos corrigidos. O próprio
`RELATORIO_APLICACAO_ADR-0026.md` é o artefato atualizado que contém essa
seção e aparece como `relatorio` na classificação final. A redação não produz
inexatidão material nem correção obrigatória, mas a distinção entre
`arquivos_corrigidos` e `arquivos_alterados` deve ser lida com esse contexto.

## 9. Verificação de regressões

Não foram identificadas regressões. O patch não:

- alterou a decisão da ADR-0026;
- inventou vínculo entre tela e fonte;
- inventou protocolo do script;
- tornou obrigatório o tipo `matriz`;
- alterou a ADR-0025;
- reabriu H-0035;
- modificou outro contrato como parte do patch;
- alterou nomenclatura como parte do patch;
- alterou o índice como parte do patch;
- alterou relatório de QA anterior;
- criou arquivo de código, configuração ou demo;
- colocou arquivos no stage;
- realizou commit.

As ocorrências de `origem_dados`, `protocolo`, `tipo: "matriz"` e H-0035
permanecem em contextos de não-decisão, preservação ou referência histórica
coerente com a ADR-0026.

## 10. Arquivos inesperados

```yaml
arquivos_inesperados: []
```

Nenhum arquivo inesperado foi identificado como produzido pelo patch. Os
arquivos modificados e não rastreados já presentes pertencem ao conjunto
acumulado da ADR-0026 ou ao QA anterior.

## 11. Achados

Nenhum achado novo foi identificado.

```yaml
achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 0
```

## 12. Observações

```yaml
observacoes: 1
```

### OBS-QAAPADRPP-0026-001

```yaml
id: OBS-QAAPADRPP-0026-001
severidade: observação
achado_original_relacionado: null
arquivo: docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md
secao_ou_trecho: seção 15.1, campo `arquivos_corrigidos`
regra_afetada: clareza de escopo do patch
evidencia: >
  A seção 15.1 lista `arquivos_corrigidos` com os dois artefatos substantivos
  corrigidos. O próprio relatório de aplicação foi atualizado pelo patch e
  aparece como `relatorio` na classificação final, não nessa lista.
impacto: >
  Não há impacto normativo nem inexatidão material. A leitura exige apenas
  distinguir arquivos substantivamente corrigidos do relatório atualizado para
  registrar o patch.
correcao_necessaria: nenhuma
```

## 13. Classificação final

```yaml
status_literal: ADR_APPLICATION_APPROVED_WITH_NOTES
status_normalizado: Aplicação aprovada após patch, com observação não corretiva
relatorio: docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0026.md
achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 0
observacoes: 1
achados_originais_corrigidos:
  - QAAPADR-0026-001
  - QAAPADR-0026-002
achados_originais_nao_corrigidos: []
regressoes: []
arquivos_do_patch_confirmados:
  - docs/contratos/contrato_tela_json.md
  - docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md
arquivos_inesperados: []
git:
  branch: master
  head: fb9e5be
  stage: vazio
  commit_novo: nao_realizado
  diff_check: sem_erros
  workspace_antes_deste_relatorio: sujo_acumulado_adr_0026
proxima_categoria: CRIAR_HANDOFF
```
