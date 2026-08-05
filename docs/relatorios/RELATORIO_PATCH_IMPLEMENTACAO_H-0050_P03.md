# RELATORIO_PATCH_IMPLEMENTACAO_H-0050_P03

```yaml
cadeia:
  raiz: docs/relatorios/IMP-0050-controle-universal-execucao-real-dry-run.md
  predecessor_imediato: docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0050_R02.md
achados_tratados:
  - MV-H0050-05
  - MV-H0050-06
patch: P03
status: IMPLEMENTATION_PATCHED_AWAITING_QA
```

## Causas comprovadas

### MV-H0050-05 — execução não disponível na demonstração

Enter com lote não vazio já chamava o executor e `_abrir_resultado_controle`.
O defeito estava no `resultado_bruto`: um JSON simples
`{modo, lote_reconciliado, resultado}` falhava em
`resultado_semanticamente_valido` (schema H-0042 multinível). A tela vigente
abria como envelope com `status: falha` e diagnóstico
“O documento de resultado não atende ao schema esperado.”. Modo e IDs
ficavam só no canal de erro, sem documento observável de sucesso — lido na
TTY como execução inexistente; o retorno ficou bloqueado por consequência.

### MV-H0050-06 — comando `Todos` não habilitado

O handler H-0050 consumia Enter antes do bloco H-0041 e, com lote vazio,
fazia apenas fall-through implícito (`pass`) em vez de aplicar
`selecao.selecionar_todos` no mesmo acionamento semântico da tela adotante.
O chip `[⏎] Todos` aparecia; a transição coletiva não estava amarrada de
forma explícita ao binding Enter do controle.

## Correção

Arquivos alterados:

* `demo/demo.py`
* `demo/executor_controle_execucao.py`
* `demo/teste_demo.py`
* `demo/teste_executor_controle_execucao.py`
* `docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0050_P03.md` (este)

### Binding de Enter

Um único acionamento Enter na tela adotante:

* resíduo inválido → só reconcilia;
* lote vazio → `selecionar_todos` (Todos);
* lote não vazio → `controle.executar` → resultado observável.

### Seleção coletiva

Enter vazio seleciona os quatro itens, materializa `●` e troca o chip para
`[⏎] Executar`. Espaço parcial, Insert (modo) e Esc (limpar/sair) seguem os
mecanismos vigentes; Todos não altera o modo.

### Execução parcial e total

Captura privada imutável com IDs na ordem reconciliada; ação resolvida no
registro universal; executor sintético sem consulta à interface. Insert
posterior não retroage na captura já iniciada.

### Resolução, resultado e retorno

`documento_resultado_observavel` (no executor, com `json`) produz
`resultado_bruto` H-0042 válido. `_abrir_resultado_controle` usa a tela
`resultado_execucao` vigente, sem pilha paralela. Esc retorna à mesma
instância (`_modelo_origem_controle` preservado entre comandos); nova
abertura reinicia por `modo_inicial`.

## Testes

Ajustes em `demo/teste_demo.py` e `demo/teste_executor_controle_execucao.py`:

* Todos ativo → quatro IDs/`●`/chip Executar → segundo Enter executa;
* parcial `dry_run` com uma chamada, documento `apresentacao=documento`,
  modo/IDs/`status: sucesso`, Esc preserva instância/modo/seleção;
* modo real sem `DRY_RUN`; lote vazio sem executor; ação ausente/incompatível;
* `resultado_bruto` semanticamente válido; demonstração das duas configs.

## Totais

```text
focais:    267 passed
completos: 1036 passed
```

Demonstração automatizada das duas configurações: Todos, parcial, Enter,
resultado observável, Esc com modo preservado, reabertura por `modo_inicial`.

## Preservações

`[␣] Marcar`, `[⏎] Todos`/`Executar`, `[Ins] Executar`/`Dry-Run`, `[V]`/`[?]`,
ordem da barra, quatro itens, `○`/`●`, `→`, `cor_alerta`, objeto fechado,
registro, captura privada, lote vazio sem execução no mesmo Enter,
redimensionamento, secundária em `dry_run`, H-0044/`dry_run_ativo` sem delta.

## Desvios / exceções / bloqueios

* Serialização do documento observável fica no executor (gate sem `json` em
  `demo.py`).
* Nenhuma API pública nova; `fluxo_execucao.py` e H-0044 intactos.
* Sem bloqueio documental.

## Validação manual pendente

Pendente de `USUARIO_EM_TTY_REAL` (terceira rodada): Todos, execução parcial
`dry_run`, resultado com modo/IDs, Esc preservando `Dry-Run`, reabertura.

## Status e próxima ação

```yaml
status: IMPLEMENTATION_PATCHED_AWAITING_QA
relatorio: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0050_P03.md
artefatos:
  - demo/demo.py
  - demo/executor_controle_execucao.py
  - demo/teste_demo.py
  - demo/teste_executor_controle_execucao.py
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0050_P03.md
proxima_acao: QA_POS_PATCH
```
