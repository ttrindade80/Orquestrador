# Relatório de QA pós-patch — H-0055 P02

```yaml
status: I5_MANUAL_VALIDATION_REQUIRED
cadeia:
  raiz: docs/relatorios/IMP-0055-dois-niveis-por-foco.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0055_P02.md
achados_retestados:
  - MV-H0055-001
  - MV-H0055-002
```

## Verificações focais

- `tela/navegacao.py` deriva `Sair`/`Voltar` do cursor corrente; entrada,
  retorno e toroides preservam seleção e foco conforme o nível.
- `demo/demo.py` despacha Esc para o pai antes do ramo genérico e exclui
  `dois_niveis_por_foco` de `[Esc] Limpar`; os demais consoles preservam o
  caminho anterior.
- A fixture declara literalmente `somente_nao_verboso`, sem `modo_inicial`
  e sem chip `[V]`. O loader aceita somente a combinação nominal H-0055/D23;
  as rejeições gerais permanecem no ramo original.
- Os testes exercitam comportamento, renderização, transferência de escolha,
  idempotência, retorno, ausência de `[V]` e rejeições focais. Testes focais:
  `94 passed`.
- O diff autorizado permanece restrito aos seis arquivos previstos e ao delta
  dos dois achados. O relatório P02 registra suíte canônica aprovada e smoke
  com código zero.

## Resultado

`MV-H0055-001` e `MV-H0055-002` estão conformes na evidência automatizável.
Resta exclusivamente validação visual/interativa em TTY real, não executada
nesta etapa.
