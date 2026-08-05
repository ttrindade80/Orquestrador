---
name: RELATORIO_PATCH_HANDOFF_H-0050_P04
description: "Correção documental focal do achado QA-H0050-P02-01 no handoff H-0050 (patch P04)"
metadata:
  type: relatorio_patch
  etapa: PATCH_HANDOFF
  patch: P04
  data: 2026-08-05
---

# Relatório do patch documental P04 do handoff H-0050

```yaml
cadeia:
  raiz: docs/handoff/H-0050-controle-universal-execucao-real-dry-run.md
  objeto_corrigido: docs/handoff/H-0050-controle-universal-execucao-real-dry-run.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_POS_PATCH_HANDOFF_H-0050_P03.md

achados_tratados:
  - QA-H0050-P02-01

patch:
  id: P04
```

## Omissões corrigidas

`QA-H0050-P02-01` apontou três lacunas documentais remanescentes após o P03.
As três foram corrigidas por uma nova subseção, "Indicadores de seleção,
transição de Enter e chips no redimensionamento", inserida imediatamente após
a subseção de preservações funcionais criada pelo P03 (sem reescrevê-la):

1. **Indicadores `○`/`●` e cursor `→`**: o handoff agora declara
   nominalmente `item não selecionado → ○` e `item selecionado → ●`, que
   Espaço no item selecionável corrente alterna `○ ↔ ●`, e que o cursor `→`
   permanece distinto dos indicadores. Evidência: símbolos e indicadores por
   `R03-07`; alternância individual por Espaço por `QA-Impl-P03`, sem
   atribuir à R03 prova direta da tecla Espaço.
2. **Transição `[⏎] Todos` → `[⏎] Executar`**: declarada nominalmente a
   sequência seleção vazia → `[⏎] Todos`; Enter em Todos seleciona todos os
   itens, não chama o executor e o chip passa para `[⏎] Executar`; seleção
   não vazia → `[⏎] Executar`. Evidência: `R03-01`, `R03-02` e
   `QA-Impl-P03`.
3. **Chips acessíveis no redimensionamento**: declarado nominalmente que em
   terminal estreito e após redimensionamentos os chips permanecem
   acessíveis, nenhum chip obrigatório desaparece, os rótulos permanecem
   completos e semanticamente identificáveis, `[Ins] Real`/`[Ins] Simulação`
   não são truncados de forma ambígua e `[⏎] Todos`/`[⏎] Executar`
   continuam distinguíveis, sem criar requisito de largura fixa. Evidência:
   `R03-07` e `QA-Impl-P03` quando aplicável.

Uma tabela-resumo equivalente à exigida foi incluída ao final da nova
subseção, replicando as três linhas de comportamento/regra/evidência.

## Ausência de alteração funcional

Nenhum rótulo, critério de aceite, valor interno (`executar`/`dry_run`),
tecla (`Espaço`, `Insert`), símbolo previamente definido ou evidência
anterior foi alterado. A subseção de preservações funcionais do P03 e a
distinção `Todos`/lote vazio permanecem intactas. D-DRY-12 e a aprovação
manual R03 (7/7 critérios) permanecem preservadas sem reabertura.

## Arquivos alterados

- `docs/handoff/H-0050-controle-universal-execucao-real-dry-run.md`:
  `patch_atual` de P03 para P04 (frontmatter e estado transportado), nova
  subseção com as três declarações, e fecho documental (seção 16) atualizado
  para referenciar o relatório P04 e a próxima ação `QA_POS_PATCH_HANDOFF_P04`.

## Verificações

- `rg` de conteúdo confirmou `○`, `●`, `→`, `[⏎] Todos`, `[⏎] Executar`,
  "chip passa", "chips permanecem", "acessíveis", "rótulos completos" e
  "terminal estreito" presentes e corretamente atribuídos no handoff.
- `git diff --check` não apontou erro de espaço em branco.
- `git status --porcelain` mostra ambos os arquivos autorizados como não
  rastreados (`??`); nenhum arquivo está staged; nenhum commit foi realizado.

## Bloqueios

Nenhum.

```yaml
status: HANDOFF_PATCHED_AWAITING_QA
relatorio: docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0050_P04.md
artefatos:
  - docs/handoff/H-0050-controle-universal-execucao-real-dry-run.md
proxima_acao: QA_POS_PATCH_HANDOFF_P04
```
