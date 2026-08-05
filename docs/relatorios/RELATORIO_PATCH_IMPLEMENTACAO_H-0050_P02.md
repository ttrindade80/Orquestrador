# RELATORIO_PATCH_IMPLEMENTACAO_H-0050_P02

```yaml
cadeia:
  raiz: docs/relatorios/IMP-0050-controle-universal-execucao-real-dry-run.md
  predecessor_imediato: docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0050.md
achados_tratados:
  - MV-H0050-01
  - MV-H0050-02
  - MV-H0050-03
  - MV-H0050-04
patch: P02
status: IMPLEMENTATION_PATCHED_AWAITING_QA
```

## Causas comprovadas

### MV-H0050-01 — símbolos de teclado

As configurações H-0050 declaravam `"tecla": "Espaço"` e `"tecla": "Enter"`
como literais. A barra renderiza o valor declarado; as telas conformes
(`h0041_selecao_multipla_oito_itens`, `h0044`) usam `␣` e `⏎`.
`config/estilo.json` permanece correto e não é autoridade desses rótulos de
tecla. Causa: literais nas configs H-0050.

### MV-H0050-02 — Verboso e Ajuda ausentes

A lista `barra_de_menus.chips` omitia `[V] Verboso` e `[?] Ajuda`. A
composição da barra só apresenta chips declarados; não há injeção automática.
Causa: omissão na declaração da barra.

### MV-H0050-03 — indicador visual de seleção

Sem `distribuicao_matricial`, o console cai no placeholder `(console)` e não
percorre a grade que aplica `incluido_on`/`incluido_off`. A seleção funcional
por Espaço existia no runtime; o marcador visual não. A infraestrutura
(`matriz_participantes` / estilo) estava íntegra. Causa: ausência de
`distribuicao_matricial` na configuração.

### MV-H0050-04 — corpus insuficiente na TTY

O JSON já tinha três itens, mas sem grade matricial só o placeholder
aparecia — um único “item” visual. Causa: mesmo déficit de
`distribuicao_matricial`; ampliou-se o corpus para quatro IDs estáveis com
fixture correspondente.

## Arquivos alterados e delta

| Arquivo | Delta |
|---|---|
| `config/telas/demo/h0050_controle_execucao_universal.json` | `␣`/`⏎`; chips Verboso/Ajuda; `distribuicao_matricial`; barra `horizontal_responsiva` (`maximo: 3`); quatro itens |
| `config/telas/demo/h0050_controle_execucao_universal_dry_run_inicial.json` | Idem; `modo_inicial: dry_run` preservado |
| `demo/fixtures/h0050_execucao_universal_fixture.json` | `item_04` determinístico |
| `tela/testes_renderizador/barra_menus.py` | Provas de símbolos, ordem e largura estreita |
| `demo/teste_demo.py` | Provas de símbolos, barra, indicador, corpus/fluxo |

Não alterados: `config/estilo.json`, `demo/demo.py`,
`tela/renderizacao/barra_menus.py`, proprietário do indicador, H-0044.

## Símbolos, chips e seleção

- Barra: `[␣] Marcar`, `[⏎] Todos|Executar`, `[Ins] Executar|Dry-Run`,
  `[V] Verboso`, `[?] Ajuda`; literais `[Espaço]`/`[Enter]` ausentes.
- Ordem: seleção → Enter → `[Ins]` → Verboso → Ajuda (`[Esc]` primeiro).
- Itens: `→` (cursor) distinto de `○`/`●` (inclusão); Espaço alterna e o chip
  Enter passa a `Executar`.

## Corpus

Quatro itens (`item_01`…`item_04`) em ambas as telas; fixture cobre os quatro.
Seleção de dois IDs gera lote ordenado; secundária inicia em `dry_run`.

## Testes e totais

Acrescentados/ajustados: símbolos Unicode; Verboso/Ajuda e ordem; indicador
e chip Enter; corpus ≥2, lote, modo, retorno, reabertura, `dry_run` inicial.

```text
focais:   254 passed
completos: 1028 passed
```

Comando focal: `teste_loader`, `teste_controle_execucao`, `barra_menus`,
`teste_executor_controle_execucao`, `teste_demo`, `teste_fluxo_execucao`.

## Demonstração automatizada

Ambas as configs: símbolos Unicode; Verboso/Ajuda; marcador; ≥2 itens;
seleção de dois; execução `dry_run`; dois IDs; retorno preservando modo;
reabertura reinicializando; redimensionamento 42 colunas sem perda de chips.
Validação TTY humana permanece pendente.

## Preservações

Insert; `[Ins]` Executar/Dry-Run; `cor_alerta`; `controle_execucao` fechado;
registro universal; captura privada; lote vazio sem execução; reinício por
nova abertura; modo em suspensão/retorno; H-0044 sem delta; `dry_run_ativo`.

## Desvios, exceções e bloqueios

- `linhas.maximo` da barra: 3 (antes 2 implícito/legado) para caber seis chips
  em largura estreita sem omitir — política `nao_omitir_chips` vigente.
- Sem exceção; sem bloqueio técnico.

## Status

```yaml
status: IMPLEMENTATION_PATCHED_AWAITING_QA
relatorio: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0050_P02.md
validacao_manual: pendente_USUARIO_EM_TTY_REAL
proxima_acao: QA_POS_PATCH
```
