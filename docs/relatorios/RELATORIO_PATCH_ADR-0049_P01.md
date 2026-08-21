---
name: RELATORIO_PATCH_ADR-0049_P01
description: "Relatório de patch corretivo da ADR-0049 para os achados QA-ADR-0049-01 e QA-ADR-0049-02"
metadata:
  type: relatorio
  etapa: PATCH_ADR
  item: ITEM-0027
  adr: ADR-0049
---

# Relatório — PATCH_ADR (ADR-0049, patch P01)

```yaml
cadeia:
  raiz: docs/adr/ADR-0049-composicao-justificacao-global-texto-tui.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_ADR-0049.md
achados_tratados:
  - QA-ADR-0049-01
  - QA-ADR-0049-02
```

## Delta material aplicado

Alterada exclusivamente a tabela "Artefatos afetados" (§5) da ADR-0049.

- **QA-ADR-0049-01**: as linhas da tabela que nomeavam módulos Python
  concretos (`tela/renderizacao/popup.py`, `tela/renderizacao/conteudo_externo.py`,
  `tela/renderizacao/texto_ansi.py`, `tela/renderizacao/matriz_participantes.py`,
  `tela/renderizacao/paginacao_interna.py`, `tela/renderizacao/console.py`,
  `tela/renderizador.py`) e helpers específicos (`_quebrar_texto`,
  `_justificar_linha`, `_formatar_linha`) foram substituídas por linhas que
  identificam famílias funcionais/consumidores afetados (popup, conteúdo
  externo e seus consumidores, composição com conteúdo ANSI, matriz de
  participantes, paginação interna, fachada pública de renderização), sem
  prescrever módulo, API, assinatura, helper ou mecanismo de reexportação.
  Foi acrescentada uma frase explícita remetendo a definição desses detalhes
  executivos à aplicação (`APLICAR_ADR`) e a handoff futuro, coerente com o
  já disposto em §8.
- **QA-ADR-0049-02**: a preservação nominal de `_truncar_com_marcador` foi
  substituída por requisito puramente comportamental — onde a apresentação
  deliberadamente exigir uma única linha, o truncamento correspondente
  permanece distinto de wrap/composição de parágrafo (D-0027-09), sem
  vincular esse requisito a nome de helper, função concreta ou módulo.

Nenhuma outra seção da ADR foi alterada. As decisões D-0027-01 a D-0027-09
permanecem com o mesmo significado; nenhuma foi reaberta.

## Trechos conceitualmente corrigidos

- §5, subseção "Artefatos afetados" (tabela e parágrafo subsequente).

## Busca de resíduos executada

```zsh
rg -n '_quebrar_texto|_justificar_linha|_formatar_linha|_truncar_com_marcador|tela/renderizador\.py|tela/renderizacao/' docs/adr/ADR-0049-composicao-justificacao-global-texto-tui.md
```

Resultado: ocorrências remanescentes apenas em §2 (Contexto), linhas 31-36,
citando os helpers/módulos atuais como evidência histórica do diagnóstico do
levantamento (o que a TUI mantém hoje), não como prescrição de solução. Não
constituem prescrição de implementação e foram mantidas conforme o critério
de aceitação do achado.

## Verificações

- `rg` de resíduos: executado, resultado analisado semanticamente (ver acima).
- `git diff --check`: sem saída (arquivo ainda não commitado no histórico;
  não há conflitos de whitespace a reportar).
- `git diff`: sem saída pelo mesmo motivo (arquivo untracked, nunca
  commitado — o conteúdo revisado foi conferido por leitura direta do
  arquivo, não por diff contra HEAD).
- `test -f docs/relatorios/RELATORIO_PATCH_ADR-0049_P01.md`: este arquivo.

## Bloqueios

Nenhum. A correção não exigiu escolher módulo, API, assinatura, helper ou
arquitetura concreta não decidida.
