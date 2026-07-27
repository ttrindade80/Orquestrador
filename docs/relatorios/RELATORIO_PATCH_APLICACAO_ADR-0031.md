---
name: relatorio-patch-aplicacao-adr-0031
description: Patch documental da aplicacao da ADR-0031 apos QA rejeitado
metadata:
  type: relatorio
  etapa: PATCH_APLICACAO_ADR
  adr: ADR-0031
  data: 2026-07-25
  status: ADR_APPLICATION_PATCH_COMPLETED_AWAITING_QA
---

# Relatorio de Patch da Aplicacao Documental - ADR-0031

## 1. Identificacao

```yaml
etapa: PATCH_APLICACAO_ADR
adr: ADR-0031
objeto: aplicacao_documental_rejeitada
qa_rejeitado: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0031.md
relatorio_patch: docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0031.md
data: 2026-07-25
```

## 2. Objeto

Corrigir a aplicacao documental da ADR-0031 nos arquivos autorizados, conforme
os achados `QAAPP31-001` a `QAAPP31-006`, sem alterar a ADR-0031, backlog,
indice, codigo, testes, configuracoes ou handoffs.

## 3. Autoridade

Autoridade aplicada:

1. ADR-0031 para D1-D15.
2. `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0031.md` para localizar os
   defeitos.
3. Contratos para consolidacao comportamental.
4. Nomenclatura para consolidacao terminologica.

O relatorio de aplicacao inicial foi tratado como registro historico, nao como
autoridade superior ao QA que o rejeitou.

## 4. Estado Inicial

```yaml
classificacao_entrada: ADR_APPLICATION_QA_REJECTED
achados_bloqueantes: 0
achados_maiores: 5
achados_menores: 1
notas: 0
stage_inicial: VAZIO
relatorio_patch_preexistente: nao
```

Gate inicial confirmado:

| Check | Resultado |
|---|---|
| ADR-0031 existe | PASSOU |
| Relatorio de QA da ADR existe | PASSOU |
| Relatorio de aplicacao existe | PASSOU |
| Relatorio de QA da aplicacao existe | PASSOU |
| Classificacao `ADR_APPLICATION_QA_REJECTED` existe | PASSOU |
| Achados `QAAPP31-001` a `QAAPP31-006` existem | PASSOU |
| Stage vazio | PASSOU |
| Relatorio de patch ainda nao existia | PASSOU |

## 5. Arquivos Lidos

Leitura integral obrigatoria:

```text
docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
docs/relatorios/RELATORIO_QA_ADR-0031.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0031.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0031.md
docs/contratos/contrato_console.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_chip.md
docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
docs/nomenclatura/32_CONSOLE.md
```

## 6. Arquivos Alterados

```yaml
arquivos_alterados:
  - docs/contratos/contrato_console.md
  - docs/contratos/contrato_barra_de_menus.md
  - docs/contratos/contrato_chip.md
  - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
  - docs/nomenclatura/32_CONSOLE.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0031.md

arquivo_criado:
  - docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0031.md
```

## 7. Limite Material

```yaml
adr_0031_alterada: nao
relatorio_qa_adr_alterado: nao
relatorio_qa_aplicacao_rejeitada_alterado: nao
indice_alterado: nao
backlog_alterado: nao
codigo_alterado: nao
testes_alterados: nao
configuracao_alterada: nao
demos_alteradas: nao
handoff_criado: nao
numero_handoff_reservado: nao
qa_pos_patch_executado: nao
```

## 8. Tratamento de QAAPP31-001

Arquivo: `docs/contratos/contrato_barra_de_menus.md`.

Tratamento:

- A distincao `[⇆]` vs `[✥]` passou a usar foco entre consoles focalizaveis e
  cursor entre itens do console focado.
- A secao de `[✥]` deixou de declarar existencia estatica por "console
  navegavel".
- O estado inativo sem movimento de `[✥]` foi removido: quando nao ha movimento
  possivel, o chip fica ausente.
- `lancador` e `dashboard` permanecem excluidos.
- Ordem canonica, simbolo canonico, demais chips, acoes futuras, selecao
  multipla futura e `DOC-B009` foram preservados.

Estado: `CORRIGIDO`.

## 9. Tratamento de QAAPP31-002

Arquivo: `docs/contratos/contrato_console.md`.

Tratamento:

- A regra remanescente que associava `[⇆]` a multiplos elementos de corpo foi
  substituida por regra baseada em pelo menos dois consoles focalizaveis.
- Foi explicitado que `dashboard`, `lancador`, grupos estruturais, console nao
  navegavel e console navegavel sem itens navegaveis nao entram na lista.
- As regras de composicao, geometria do corpo e remissoes a `dashboard` e
  `lancador` foram preservadas.

Estado: `CORRIGIDO`.

## 10. Tratamento de QAAPP31-003

Arquivo: `docs/contratos/contrato_chip.md`.

Tratamento:

- A definicao conceitual de chip `alternancia` passou a mencionar foco entre
  consoles focalizaveis para `[⇆]`.
- A lista canonica passou a descrever `[⇆]` como foco entre consoles
  focalizaveis.
- Identificador, simbolo, ordem, estilo, natureza contextual e ausencia de chip
  novo foram preservados.

Estado: `CORRIGIDO`.

## 11. Tratamento de QAAPP31-004

Arquivo: `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`.

Tratamento:

- A tabela de distincoes obrigatorias passou a registrar:
  `[⇆]` muda o foco entre consoles focalizaveis; `[✥]` move o cursor entre
  itens do console focado.
- As condicoes de existencia ja consolidadas na secao 4.3 foram preservadas:
  `[⇆]` com pelo menos dois consoles focalizaveis e `[✥]` com console focado
  com mais de um item navegavel.
- A ordem canonica dos chips nao foi redefinida.

Estado: `CORRIGIDO`.

## 12. Tratamento de QAAPP31-005

Arquivo: `docs/nomenclatura/32_CONSOLE.md`.

Tratamento:

- A formulacao "Celula vazia forma seu proprio toroide menor" foi substituida.
- O modulo passou a afirmar que celula vazia nao recebe cursor e nao participa
  do toroide.
- Foi registrado que linha ou coluna sem outro item ocupado no eixo resulta em
  `SEM_MOVIMENTO`.
- Foram negados compensacao de coluna, salto diagonal, busca pelo item mais
  proximo e toroide composto por celulas vazias.
- Os termos `ec`, `tg`, `tx`, item logico, linha fisica, distribuicao vigente e
  paginacao como ciclo futuro foram preservados.

Estado: `CORRIGIDO`.

## 13. Tratamento de QAAPP31-006

Arquivo: `docs/relatorios/RELATORIO_APLICACAO_ADR-0031.md`.

Tratamento:

- O registro historico da aplicacao inicial foi preservado.
- Foi adicionada a secao `Patch posterior ao QA rejeitado`.
- A aplicacao inicial foi qualificada como `REJEITADA_PELO_QA`.
- O patch documental foi registrado como `CONCLUIDO`.
- O QA pos-patch foi registrado como `PENDENTE`.
- A ultima linha foi atualizada para
  `ADR_APPLICATION_PATCH_COMPLETED_AWAITING_QA`.

Estado: `CORRIGIDO`.

## 14. Varredura de Contradicoes Residuais

Varredura contextual realizada nos cinco documentos normativos autorizados para:

```text
elementos de corpo
múltiplos elementos
corpo em foco
console navegável
estado inativo
toróide menor
toroide menor
célula vazia
celula vazia
```

Ocorrencias corrigidas:

| Expressao | Arquivo | Classificacao | Tratamento |
|---|---|---|---|
| `múltiplos elementos de corpo` | `contrato_console.md` | normativa incompatível | substituida por consoles focalizaveis |
| `elementos de corpo diferentes` | `contrato_barra_de_menus.md` | normativa incompatível | substituida por consoles focalizaveis |
| `console navegável` em §11 de `[✥]` | `contrato_barra_de_menus.md` | normativa incompatível | substituida por console focado com >1 item navegavel |
| `estado inativo` para `[✥]` | `contrato_barra_de_menus.md` | normativa incompatível | substituido por ausencia sem movimento |
| `alternância entre elementos de corpo` | `contrato_chip.md` | canonica incompatível | substituida por foco entre consoles focalizaveis |
| `foco entre elementos de corpo` | `contrato_chip.md` | canonica incompatível | substituida por foco entre consoles focalizaveis |
| `corpos` / `corpo em foco` na distincao `[⇆]` x `[✥]` | `31_BARRA_DE_MENUS_E_CHIPS.md` | terminologica incompatível | substituida por consoles focalizaveis e console focado |
| `toróide menor` | `32_CONSOLE.md` | terminologica incompatível | removida e substituida por D8/D9 |

Ocorrencias preservadas com justificativa:

| Expressao | Arquivo | Classificacao | Justificativa |
|---|---|---|---|
| `corpo em foco` em regras de `[Esc]` | `contrato_barra_de_menus.md` | generica historica | Trata selecao ativa do corpo para `Esc`, nao elegibilidade de `[⇆]` ou `[✥]`. |
| `estado inativo` geral | `contrato_chip.md`; `31_BARRA_DE_MENUS_E_CHIPS.md` | generica normativa | Continua valido para chips em geral; `[✥]` tem excecao explicita. |
| `console navegável` em escopo de `lancador`/`dashboard` | contratos e nomenclatura | generica preservada | Indica exclusao historica de `lancador` e `dashboard`; nao redefine foco entre consoles. |
| `célula vazia` | `32_CONSOLE.md`; `contrato_console.md` | normativa compativel | Ocorrencias restantes afirmam exclusao do cursor e do toroide, compatíveis com D8/D9. |

Resultado: nao foram mantidas regras antigas contraditorias no mesmo documento.

## 15. Decisoes D1-D15 Preservadas

| Decisao | Estado |
|---|---|
| D1 | PRESERVADA |
| D2 | PRESERVADA |
| D3 | PRESERVADA |
| D4 | PRESERVADA |
| D5 | PRESERVADA |
| D6 | PRESERVADA |
| D7 | PRESERVADA |
| D8 | PRESERVADA |
| D9 | PRESERVADA |
| D10 | PRESERVADA |
| D11 | PRESERVADA |
| D12 | PRESERVADA |
| D13 | PRESERVADA |
| D14 | PRESERVADA |
| D15 | PRESERVADA |

## 16. Decisoes Deferidas Preservadas

Permanecem deferidas:

- Paginacao interativa (`ITEM-0003`).
- Registro e execucao declarativa de acoes (`ITEM-0004` / `DOC-B009`).
- Abertura e retorno entre telas (`ITEM-0005`).
- Selecao multipla (`ITEM-0006`).
- Navegacao multinivel, expansao e recolhimento (`ITEM-0007`).
- Conteudo composto e heterogeneo (`ITEM-0008`).
- Dashboard passivo (`ITEM-0009`).

## 17. Arquivos Inspecionados e Preservados

```yaml
inspecionados_preservados:
  - docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
  - docs/relatorios/RELATORIO_QA_ADR-0031.md
  - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0031.md
  - docs/adr/INDICE_ADR.md
  - docs/backlog.md
```

## 18. Checks Mecanicos

```yaml
test_relatorio_patch_existe: PASSOU
grep_secoes_relatorio_patch: PASSOU
grep_achados_QAAPP31_001_a_006: PASSOU
tail_relatorio_aplicacao: ADR_APPLICATION_PATCH_COMPLETED_AWAITING_QA
tail_relatorio_patch: ADR_APPLICATION_PATCH_COMPLETED_AWAITING_QA
git_diff_check: PASSOU
git_diff_cached_check: PASSOU
git_diff_no_index_check_relatorio_patch: PASSOU_SEM_ERROS_DE_WHITESPACE
marcadores_de_conflito: AUSENTES
cercas_markdown:
  relatorio_patch: FECHADAS
  relatorio_aplicacao: FECHADAS
newline_final: CONFIRMADO
```

Resultado da varredura residual solicitada:

```yaml
grep_residual:
  encontrados:
    - docs/contratos/contrato_barra_de_menus.md:295
    - docs/contratos/contrato_barra_de_menus.md:299
    - docs/contratos/contrato_barra_de_menus.md:664
  classificacao: PRESERVADO_COM_JUSTIFICATIVA
  motivo: >
    As ocorrencias usam "corpo em foco" apenas nas regras contextuais de Esc
    para selecao ativa; nao definem elegibilidade de [⇆] nem condicao de [✥].
```

## 19. Estado Git Final

Estado observado:

```yaml
stage: VAZIO
commit_executado: nao
arquivos_alterados_nesta_etapa:
  - docs/contratos/contrato_console.md
  - docs/contratos/contrato_barra_de_menus.md
  - docs/contratos/contrato_chip.md
  - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
  - docs/nomenclatura/32_CONSOLE.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0031.md
arquivo_criado: docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0031.md
worktree_contem_alteracoes_preexistentes_fora_desta_etapa: true
```

## 20. Proximo Gate

```yaml
qa_pos_patch: PENDENTE
executar_qa_pos_patch_neste_ciclo: nao
criar_handoff: nao
atualizar_backlog: nao
atualizar_indice: nao
```

## 21. Encerramento

```yaml
resultado: ADR_APPLICATION_PATCH_COMPLETED_AWAITING_QA
adr: ADR-0031
aplicacao_documental:
  patch_concluido: true
  qa_pos_patch: PENDENTE
implementacao: NAO_INICIADA
handoff: NAO_CRIADO
```

## Matriz de Achados

| Achado | Arquivo | Tratamento | Evidencia | Estado |
| ------ | ------- | ---------- | --------- | ------ |
| QAAPP31-001 | `docs/contratos/contrato_barra_de_menus.md` | Reconciliada a regra de `[✥]` para console focado com mais de um item navegavel e ausencia sem movimento | Secao 11 reescrita e distincao `[⇆]`/`[✥]` atualizada | CORRIGIDO |
| QAAPP31-002 | `docs/contratos/contrato_console.md` | Substituida alternancia por multiplos elementos de corpo por consoles focalizaveis | Secao 15 qualificada por D2/D14 | CORRIGIDO |
| QAAPP31-003 | `docs/contratos/contrato_chip.md` | Descricoes canonicas de `[⇆]` atualizadas para foco entre consoles focalizaveis | Secoes 5 e 7 reconciliadas | CORRIGIDO |
| QAAPP31-004 | `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` | Distincao obrigatoria atualizada para consoles focalizaveis e console focado | Tabela da secao 5 reconciliada | CORRIGIDO |
| QAAPP31-005 | `docs/nomenclatura/32_CONSOLE.md` | Removida a ideia de toroide menor de celula vazia | Secao 4.3 alinhada a D8/D9 | CORRIGIDO |
| QAAPP31-006 | `docs/relatorios/RELATORIO_APLICACAO_ADR-0031.md` | Secao posterior ao QA rejeitado adicionada; aplicacao inicial qualificada | Estado inicial rejeitado, patch concluido e QA pos-patch pendente | CORRIGIDO |

ADR_APPLICATION_PATCH_COMPLETED_AWAITING_QA
