# Relatório QA pós-patch de implementação H-0050 P01

```yaml
cadeia:
  raiz: docs/relatorios/IMP-0050-controle-universal-execucao-real-dry-run.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0050_P01.md
etapa: QA_POS_PATCH
patch: P01
status: QA_POS_PATCH_APROVADO
achados:
  QA-IMP-0050-01: PASSOU
  QA-IMP-0050-02: PASSOU
  QA-IMP-0050-03: PASSOU
  QA-IMP-0050-04: PASSOU
testes_focais_reproduzidos: 250
testes_completos_declarados: 1024
testes_completos_reexecutados: false
validacao_manual: PENDENTE_USUARIO_TTY
bloqueios_funcionais: nenhum
```

## Conclusão

Os quatro achados autorizados foram retestados e passaram semanticamente. A
demonstração automatizada também passou: os dois modos iniciais, alternância
por `Insert`, lote vazio sem chamada, lote de dois itens, modo e IDs no
resultado, retorno e reinicialização de nova sessão.

Não foi feito novo patch nem validação visual em nome do usuário.

## Evidências de execução

| Escopo | Comando | Resultado |
|---|---|---|
| Conjunto H-0050 autorizado | `pytest -q tela/teste_loader.py tela/teste_controle_execucao.py tela/testes_renderizador/barra_menus.py demo/teste_executor_controle_execucao.py demo/teste_demo.py` | 223 passed |
| Regressão focal H-0044 | `pytest -q tela/teste_fluxo_execucao.py` | 27 passed |
| Total focal reproduzido | soma dos dois conjuntos acima | 250 passed |
| Casos H-0050 nomeados | mesmos cinco arquivos, `-k h0050` | 16 passed, 207 deselected |

Os 1.024 testes completos permanecem apenas como total declarado no relatório
P01; não foram reexecutados, porque isso exigiria ampliar a leitura além do
manifesto fechado desta auditoria.

## QA-IMP-0050-01 — literal, ordem e estado visual

PASSOU.

- As telas H-0050 renderizam `[Ins] Executar` e `[Ins] Dry-Run`; o literal
  `[Insert]` não aparece.
- O controle é reposicionado depois de Enter e antes de Verboso/Ajuda,
  preservando a ordem relativa dos demais chips.
- `Insert` alterna o modo; `dry_run` fica destacado com `cor_alerta` e não
  recebe `cor_inativo`.
- O cenário sintético de largura estreita preserva o chip e sua semântica.
- O H-0044 permaneceu isolado: a busca focal não encontrou metadado H-0050 no
  JSON integrado, e sua regressão passou com 27 testes.

Evidências principais: `tela/renderizacao/barra_menus.py`,
`demo/demo.py`, as duas configurações H-0050 e o teste de renderização
`test_h0050_chip_controle_tem_rotulo_dinamico_ordem_atividade_e_cor_alerta`.

## QA-IMP-0050-02 — tipos inválidos em `modo_inicial`

PASSOU.

Lista, objeto, `null`, booleano, número e valor desconhecido foram rejeitados
antes da consulta aos modos válidos, com `TelaEstruturaInvalida`,
`CONFIGURACAO_INVALIDA` e o caminho `controle_execucao.modo_inicial`.
Não escaparam `TypeError`, `KeyError` ou exceção interna. Propriedade
adicional no objeto de controle também foi rejeitada; não há coerção nem
default.

Evidências: `tela/carregamento/tela_json.py` e os testes H-0050 finais de
`tela/teste_loader.py`.

## QA-IMP-0050-03 — lote vazio

PASSOU.

O fluxo reconcilia a seleção e retorna antes de `controle.executar` quando o
lote está vazio. Um spy confirmou zero chamadas e nenhum
`resultado_controle_execucao`. Com dois itens, o resultado preservou
`["item_01", "item_02"]`, a ordem, o modo `dry_run` e o marcador `DRY_RUN`.

Evidências: `demo/demo.py`, `tela/controle_execucao.py`,
`demo/teste_executor_controle_execucao.py` e os testes H-0050 de
`demo/teste_demo.py`.

## QA-IMP-0050-04 — captura privada

PASSOU.

`_RequisicaoExecucaoCapturada` permanece privada, congelada e fora de
`__all__`. Não existe o alias público `RequisicaoExecucaoCapturada`; o
executor demonstrativo não importa a classe. A captura preserva lote, ordem e
modo, não consulta a interface, e a alternância posterior do controle não
altera uma captura já criada.

Evidências: `tela/controle_execucao.py`,
`demo/executor_controle_execucao.py` e o teste do executor.

## Correspondência com P01

Os 12 artefatos listados em “Arquivos alterados” no relatório P01 estão
presentes no estado de trabalho: seis como modificados e seis como arquivos
novos. Portanto, a correspondência do conjunto declarado foi confirmada no
estado de trabalho; um `git diff` isolado mostra somente os seis modificados,
pois não inclui os seis arquivos novos.

O estado de trabalho também contém outros arquivos modificados ou novos fora
do conjunto autorizado, incluindo documentação e artefatos auxiliares. Eles
não foram lidos nem auditados, conforme o manifesto fechado; sua proveniência
e eventual relação com P01 permanecem fora desta conclusão.

O relatório P01 corresponde aos quatro comportamentos retestados, à
demonstração, à preservação do H-0044 e ao total focal de 250 quando o teste
H-0044 é incluído. A declaração de 1.024 testes completos não foi
independentemente reproduzida nesta etapa. A validação manual em TTY real
continua pendente, conforme declarado em P01.
