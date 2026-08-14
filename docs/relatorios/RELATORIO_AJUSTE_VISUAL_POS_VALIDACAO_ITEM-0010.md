# Relatório — Ajuste visual pós-validação ITEM-0010

## resultado

```yaml
status: AJUSTE_VISUAL_APLICADO
arquivos_alterados:
  - tela/renderizacao/estilo.py
  - demo/demo.py
  - tela/teste_estilo_h0064.py
  - demo/teste_demo_estilo_h0064.py
  - demo/teste_demo_estilo_h0063.py
  - docs/relatorios/RELATORIO_AJUSTE_VISUAL_POS_VALIDACAO_ITEM-0010.md
amostra_chip:
  fonte: tela/renderizacao/estilo.py :: PAYLOAD_CANONICO_CHIP
  antes: "Ab" (caixa_alta true → "AB")
  depois: "A" (caixa_alta true → "A", upper idempotente)
  delimitadores_presets: inalterados
  foreground_background_ansi: inalterados
  catalogo_presets: inalterado
esc_filhos:
  fonte: demo/demo.py :: projeção Barra (override H-0063 removido)
  antes: "[Esc] Retornar aos pais"
  depois: "[Esc] Voltar" (rótulo canônico de navegacao.rotulo_esc_dois_niveis)
  acao: inalterada (Esc filho → pais; candidato/seleção/elegibilidade preservados)
esc_raiz:
  rotulo: "[Esc] Sair" (inalterado)
  acao: saída efetiva da tela / descarte da visita conforme H-0065 (inalterado)
testes:
  h0063: 19 passed
  h0064: 20 passed
  h0065: 25 passed
  h0066: 27 passed
  h0067: 22 passed
  h0063_a_h0067_conjunto: 113 passed
  popup_focal_h0067: 90 passed (tela/teste_popup.py + h0067)
  popup_somente: 68 passed
  suite_completa: 1296 passed
validacao_manual_necessaria: true
validacao_manual_escopo:
  - conferir visualmente amostra de chip `[A]`
  - conferir Barra no nível de filhos: `[Esc] Voltar`
  - confirmar Barra na raiz/pais: `[Esc] Sair`
bloqueios: []
```

## Investigação (fontes reais)

| Alvo | Local nominal | Ação |
|------|---------------|------|
| Payload `Ab`/`AB` das amostras | `tela/renderizacao/estilo.py` — constante `PAYLOAD_CANONICO_CHIP` + `amostra_chip()` | Alterado `"Ab"` → `"A"` |
| Rótulo `Retornar aos pais` | `demo/demo.py` — override pós-`rotulo_esc_dois_niveis` só para a tela de Estilo quando o rótulo canônico era `Voltar` | Override removido; usa o rótulo canônico |

Não houve substituição global cega. Config JSON de presets, contratos globais de chip, código de popup e H-0068 não foram tocados.

Arquivos candidatos inspecionados e **não** alterados (sem fonte real nem expectativa materialmente superada):

- `tela/estilo.py`
- `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json`
- `tela/teste_estilo_h0063.py` / `tela/teste_estilo_h0065.py` / `tela/teste_estilo_h0066.py` / `tela/teste_estilo_h0067.py`
- `demo/teste_demo_estilo_h0065.py` / `demo/teste_demo_estilo_h0066.py` / `demo/teste_demo_estilo_h0067.py`
- código de popup (`tela/renderizacao/popup.py`, etc.)

## Semântica preservada

- Esc em filhos → retorna ao nível de pais; candidato, seleção e Aplicar (se houver divergência) permanecem.
- Esc na raiz/pais → sai da tela; descarte da visita conforme H-0065.
- `caixa_alta` continua aplicada via `.upper()` no payload demonstrativo (agora `"A"`).
- ANSI de `cor_texto`/`cor_fundo` e largura visual (delimitadores + 1 letra) cobertos pelos testes H-0064.

## Popup

Nenhum código de popup alterado. Regressão focal H-0067/P01 (`tela/teste_popup.py` + suítes H-0067): **90 passed**. Overlay/centralização/largura permanecem verdes.

## Limites respeitados

- Sem H-0068, persistência, publicação, baseline, backlog, stage, commit ou push.
