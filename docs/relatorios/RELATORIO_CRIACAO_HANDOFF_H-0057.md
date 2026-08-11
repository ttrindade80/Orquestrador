# Relatório de criação — H-0057

```yaml
status: HANDOFF_CREATED
handoff: H-0057
baseline_commit: 1211a70
```

Foi criado o handoff da segunda entrega incremental de ITEM-0017, usando
H-0056 concluído como baseline. O escopo ficou restrito a geometria dinâmica,
wrapping de texto, alinhamentos após wrapping, altura derivada, chips em várias
linhas, resize reativo, últimas dimensões válidas e integração ao quadro geral
de terminal pequeno.

Caminhos de implementação foram resolvidos nominalmente em
`tela/renderizacao/popup.py`, `tela/renderizacao/tela.py`,
`tela/teste_popup.py`, `demo/demo.py`, `demo/teste_demo_popup.py` e
`config/telas/demo/demo.json`. Foi definido o novo fixture
`demo/fixtures/h0057_popup_texto_dinamico.py` e o relatório futuro
`docs/relatorios/IMP-0057-popup-geometria-dinamica-wrapping-resize.md`.

Os testes especificados cobrem largura, wrapping, três alinhamentos, altura,
chips, resize, terminal pequeno, regressão H-0056 e a suíte canônica
`PYTHONDONTWRITEBYTECODE=1 python -m pytest`, com referência de `1118 passed`.
Também foi definida demonstração em TTY real com recomposição por largura e
altura, restauração automática, bloqueio modal e retorno por `Esc`.

Foram explicitamente excluídos H-0058 e H-0059, listas, marcações, Enter,
confirmação, payload confirmado, compatibilidade de retorno, paginação e
qualquer mudança de estilo global. Nenhum bloqueio ou decisão adicional ficou
pendente. Não houve implementação, QA, stage ou commit.
