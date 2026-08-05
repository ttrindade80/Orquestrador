# Relatório de patch de implementação H-0050 P01

```yaml
cadeia:
  raiz: docs/relatorios/IMP-0050-controle-universal-execucao-real-dry-run.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0050.md
achados_tratados:
  - QA-IMP-0050-01
  - QA-IMP-0050-02
  - QA-IMP-0050-03
  - QA-IMP-0050-04
```

## Arquivos alterados

`tela/carregamento/tela_json.py`, `tela/controle_execucao.py`,
`demo/executor_controle_execucao.py`, `tela/renderizacao/barra_menus.py`,
`demo/demo.py`, as duas configurações demonstrativas H-0050,
`tela/teste_loader.py`, `tela/teste_controle_execucao.py`,
`tela/testes_renderizador/barra_menus.py`, `demo/teste_executor_controle_execucao.py`
e `demo/teste_demo.py`.

## Correções

O chip específico foi materializado como `[Ins] Executar` e `[Ins] Dry-Run`,
com o controle imediatamente após Enter e antes de Verboso/Ajuda quando
presentes. A atividade nos dois modos e o destaque por `cor_alerta` foram
preservados; a barra continua responsiva em largura estreita.

`modo_inicial` agora exige string válida antes da consulta ao conjunto de
modos, produzindo `CONFIGURACAO_INVALIDA` com o caminho
`controle_execucao.modo_inicial` para listas, objetos, nulos, booleanos,
números e valores desconhecidos.

Lote reconciliado vazio não cria captura, não chama executor e não grava
resultado sintético. Lotes não vazios preservam IDs, ordem e modo.

A captura permanece uma dataclass privada, congelada, sem alias público e fora
de `__all__`. O executor demonstrativo não importa seu nome.

## Testes e demonstração

Foram acrescentados testes de tipos não hashable, privacidade/exportação,
imutabilidade, captura do modo, lote vazio com spy, literal/ordem do chip,
redimensionamento, executor sem dependência da classe privada e integração
H-0050.

Testes focais: **250 passed**. Suíte completa: **1.024 passed**. A demonstração
automatizada confirmou os dois rótulos, ordem, ausência de execução vazia,
execução de dois itens em `dry_run`, retorno preservado e nova sessão
reinicializada. A regressão H-0044 permaneceu aprovada pela suíte focal e
completa.

Desvios: nenhum. Exceções: nenhuma. Bloqueios: nenhum de implementação.

Validação manual permanece pendente: necessária, exclusiva de
`USUARIO_EM_TTY_REAL`, não executada, resultado `PENDENTE_USUARIO_TTY`.

```yaml
status: IMPLEMENTATION_PATCHED_AWAITING_QA
relatorio: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0050_P01.md
proxima_acao: QA_POS_PATCH
```
