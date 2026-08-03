---
name: REL-PATCH-H-0045-P10-diagnostico-modo-verboso-multilinha
description: "Corrige a validabilidade material de paginação verbosa multilinha"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_IMPLEMENTACAO
  status: IMPLEMENTATION_PATCHED
  data: 2026-08-01
rastreabilidade:
  etapa: DIAGNOSTICO_E_PATCH_IMPLEMENTACAO
  objeto: h0045_paginacao_modo_verboso_multilinha
  cadeia_raiz: docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P09.md
  achados_tratados: [VM-H0045-R06-002]
---

# REL-PATCH-H-0045-P10 — Patch de implementação

## Diagnóstico e causa raiz

`[V] Verboso` é normativo apenas quando a instância declara
`politica_modo: alternavel`; o contrato prevê tecla V e chip nesse caso. O
H-0045 não exige alternância para este cenário, e os comandos de paginação
normativos são `,`/`<` e `.`/`>`. A fixture é um envelope legado fixo, com
`politica_exibicao.verboso: true` e `modo_inicial: verboso`; portanto nasce
verbosa e não deve exibir `[V]`. O loader rejeita misturar esse envelope com
marcadores D23 em `formato.excesso`, preservação aplicada neste patch.

Os quatro itens eram strings curtas de uma linha, sem estrutura multinível ou
quebras explícitas; os testes anteriores não comprovavam conteúdo multilinha.
As políticas finais são `permitir_quebra`, `evitar_quebra`, default
`evitar_quebra` e default `evitar_quebra`. O renderer já suportava quebra
textual longa, mas o mapa físico calculava a altura com a largura total do
console, enquanto a renderização usava a largura real da célula matricial.
Essa divergência, somada à fixture insuficiente, confirmou a causa raiz
combinada fixture + autoridade do renderer. A regra de terminal mínimo não foi
alterada: 80×9 ainda renderiza; em 80×8 o resolver emite corretamente o quadro
`terminal pequeno demais` por insuficiência geométrica do corpo.

## Delta aplicado

- A fixture recebeu conteúdo determinístico com tokens `segmento_01`–`segmento_26`, mantendo quatro itens e cobrindo fragmentação real.
- `tela/renderizador.py` passou a calcular o mapa com a largura efetiva de cada célula e a reutilizar essa largura ao materializar fragmentos.
- `demo/demo.py` interpreta `politica_exibicao` somente no caminho legado sem `politica_modo`, preservando a semântica D23.
- Foram adicionados testes reais da fixture em `demo/teste_demo_paginacao.py` e teste do mapa/fragmentos em `tela/teste_renderizador.py`.

Em 80×24, as linhas físicas são `longo_01=23`, `longo_02=7`, `curto_03=3`,
`curto_04=3`, distribuídas em 3 páginas: `16`; `7+7`; `3+3`. Em 80×15,
o total muda para 6 páginas. O cursor aparece apenas na primeira linha do
item lógico; a continuação não recebe cursor. A demonstração sem TTY do comando
solicitado produziu conteúdo multilinha e `página 1/3`; os comandos de página
foram cobertos pela cadeia TTY automatizada existente e pelos novos testes.

## Verificações

```yaml
focais: 363 passed
expandidos: 574 passed
suite_completa: 806 passed
manual_usuario: pendente (não executada)
etapas_preservadas: 6/17..13/17
retomada: R07_CONSOLIDADA em 14/17
```

Nenhum documento normativo foi alterado por este patch. Stage e commit não
foram executados. O QA pós-patch e a validação manual permanecem pendentes.
