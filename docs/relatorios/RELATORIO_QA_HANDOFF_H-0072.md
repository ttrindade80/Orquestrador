# Relatório QA_HANDOFF — H-0072

## Escopo

Auditoria exclusiva de
`docs/handoff/H-0072-formatacao-generica-filhos-dois-niveis-por-foco.md`,
sem correção, sem implementação, sem criação de H-0073.

## Verificações materiais realizadas

- **Fidelidade às autoridades**: as capacidades descritas (tabulação
  5..10, designador `decimal_composto`/`alfabetico_maiusculo`/`nenhum`,
  apresentação `texto`/`tabela`, colunas por `tabela.colunas[].campo`,
  espaçamento 3..8) correspondem literalmente ao schema fechado em
  ADR-0047 §4.13, `contrato_tela_json.md` §36 e ao comportamento de
  `contrato_console.md` §25. Nenhuma decisão nova é introduzida.
- **Separação JSON/conteúdo/renderer**: §8–§10 e §12–§19 do handoff
  preservam a fronteira de `contrato_json_console.md` §15 — conteúdo
  permanece exclusivo do documento externo, geometria calculada
  permanece exclusiva do renderer.
- **Exequibilidade nominal**: todos os arquivos existentes citados em
  §4.1–§4.3 foram confirmados no repositório, com números de linha
  precisos (`tela/modelo.py` L361/L489; `tela/carregamento/tela_json.py`
  L442; `teste_navegacao.py` L2032). O novo módulo
  `tela/carregamento/formato_dois_niveis_por_foco.py` é coerente com o
  precedente `d23_console.py`, confirmado existente. `designadores.py`
  já implementa `decimal_composto` e `alfabetico_maiusculo`, sustentando
  a promessa de reuso sem tipo novo.
- **Preservação de H-0055/H-0063 e não antecipação de H-0073**: nenhuma
  das duas fixtures contém `formato.dois_niveis_por_foco.filho`; o
  handoff proíbe explicitamente sua alteração (§5, §7, §26).
- **Cobertura de testes**: os 18 casos de §21 cobrem semanticamente
  todos os pontos exigidos (unidade deslocada, três tabulações, três
  designadores, texto, tabela multi-coluna, alinhamento entre pais,
  espaçamento mín/máx, sobra, quebra, continuação, resize, os onze
  casos V-DNF-01 a V-DNF-11, preservação de navegação).
- **Escopo de arquivos**: nenhum arquivo necessário está ausente;
  nenhum arquivo autorizado é estranho à capacidade; nenhuma descoberta
  arquitetural ampla é transferida para IMPLEMENTAR (§4 fecha o
  levantamento).

## Status

`H1_HANDOFF_APPROVED`
\n