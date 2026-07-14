# Relatório de QA — H-0006 Tela mínima com borda fixa

## Status

QA_APPROVED_WITH_NOTES

## Escopo auditado

QA pós-implementação do ciclo:

```text
H-0006 — Tela mínima com borda fixa
```

Foi verificada a aderência ao handoff H-0006, à ressalva da auditoria sobre
`cabecalho: dict`, à pureza/determinismo do renderer e à ausência de regressão
nos ciclos anteriores executáveis.

Não foram feitas correções de implementação, testes ou documentação normativa.
Este relatório é a única escrita realizada durante o QA.

## Arquivos lidos

Arquivos da leitura obrigatória:

```text
docs/handoff/H-0006-tela-minima-borda-fixa.md
docs/relatorios/RELATORIO_AUDITORIA_H-0006_HANDOFF.md
docs/relatorios/IMP-0006-tela-minima-borda-fixa.md
tela/modelo.py
tela/renderizador.py
tela/teste_renderizador.py
tela/diagnostico.py
tela/teste_diagnostico.py
config/telas/orquestrador.json
```

Arquivo extra lido:

```text
/home/tiago/.codex/attachments/da594e3f-7f6d-4662-a935-c52ac5ebe74a/pasted-text.txt
```

Justificativa: continha a solicitação de QA e os comandos/critério de aceite
desta tarefa.

Não foram lidos contratos, ADRs, `docs/NOMENCLATURA.md`,
`config/estilo.json` nem `config/barra_de_menus.json`.

## Comandos executados

```bash
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_diagnostico.py
python tela/diagnostico.py
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print
git status --short
git diff --stat
git diff --name-only
grep -R "config/estilo.json\|config/barra_de_menus.json\|curses\|textual\|rich" -n tela || true
grep -R "titulo\|descricao\|cabecalho" -n tela/renderizador.py tela/modelo.py
rg "^(import|from) (curses|textual|rich)\b|^(import|from) .*\b(curses|textual|rich)\b" tela
git diff -- tela/modelo.py
git diff -- docs/contratos docs/adr docs/NOMENCLATURA.md docs/INDICE.md docs/backlog.md docs/issues.md config
```

Também foi feita uma inspeção pontual da saída de `renderizar_tela` para
confirmar `\n` final e largura Python de 42 caracteres nas linhas visuais.

## Resultado dos testes

```text
python -m json.tool config/telas/orquestrador.json
orquestrador.json OK
```

```text
python tela/teste_loader.py
Total de verificacoes: 37
Passaram: 37
Falharam: 0
```

```text
python tela/teste_modelo.py
Total de verificacoes: 30
Passaram: 30
Falharam: 0
```

```text
python tela/teste_renderizador.py
Total de verificacoes: 36
Passaram: 36
Falharam: 0
```

```text
python tela/teste_diagnostico.py
Total de verificacoes: 26
Passaram: 26
Falharam: 0
```

```text
python tela/diagnostico.py
```

Produziu a tela H-0006 esperada com três caixas:

```text
╭ ORQUESTRADOR ──────────────────────────╮
│ Tela raiz do sistema — ponto de entrada│
╰────────────────────────────────────────╯

╭ DASHBOARD ─────────────────────────────╮
│ Dashboard de teste                     │
│ Sem dados carregados                   │
╰────────────────────────────────────────╯

╭ Menu ──────────────────────────────────╮
│ [Esc] Sair    [B] Borda                │
╰────────────────────────────────────────╯
```

Cache/bytecode:

```text
find tela -type d -name '__pycache__' -print
```

Saída vazia.

```text
find tela -type f -name '*.pyc' -print
```

Saída vazia.

## Verificação de escopo Git

Antes da criação deste relatório de QA, `git status --short` retornou:

```text
 M tela/renderizador.py
 M tela/teste_diagnostico.py
 M tela/teste_renderizador.py
?? docs/handoff/H-0006-tela-minima-borda-fixa.md
?? docs/relatorios/IMP-0006-tela-minima-borda-fixa.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0006_HANDOFF.md
```

`git diff --stat` retornou:

```text
 scripts/tela/renderizador.py       | 122 ++++++++++++++-----------
 scripts/tela/teste_diagnostico.py  | 112 ++++++++++-------------
 scripts/tela/teste_renderizador.py | 183 +++++++++++++++----------------------
 3 files changed, 194 insertions(+), 223 deletions(-)
```

`git diff --name-only` retornou:

```text
scripts/tela/renderizador.py
scripts/tela/teste_diagnostico.py
scripts/tela/teste_renderizador.py
```

Conclusão de escopo:

- O diff rastreado contém somente os 3 arquivos de código autorizados pelo
  H-0006.
- `docs/relatorios/IMP-0006-tela-minima-borda-fixa.md` existe e aparece como
  arquivo novo/não rastreado, conforme a atenção especial do pedido.
- `docs/handoff/H-0006-tela-minima-borda-fixa.md` e
  `docs/relatorios/RELATORIO_AUDITORIA_H-0006_HANDOFF.md` também aparecem como
  não rastreados. Eles são artefatos contextuais obrigatórios do ciclo e já
  estavam descritos no relatório de implementação como não rastreados
  pré-existentes; por isso foram tratados como ressalva de higiene Git, não
  como falha funcional da implementação.
- `git diff -- tela/modelo.py` não mostrou alterações.
- `git diff -- docs/contratos docs/adr docs/NOMENCLATURA.md docs/INDICE.md docs/backlog.md docs/issues.md config`
  não mostrou alterações.

## Verificação de aderência ao handoff

1. `renderizar_tela(modelo: ModeloTela) -> str` continua sendo a entrada
   principal.
2. O renderer consome `ModeloTela`; não carrega JSON bruto.
3. Não há leitura de `config/estilo.json`.
4. Não há leitura de `config/barra_de_menus.json`.
5. Não há alteração de estado, gravação de arquivo ou execução de ação.
6. A saída é determinística.
7. A saída bate em igualdade estrita com o expected output do handoff.
8. Cada linha visual tem `TOTAL_WIDTH = 42` caracteres Python.
9. A saída termina com `\n`.
10. O cabeçalho usa `modelo.cabecalho.get(...)`, compatível com a API real.
11. `tela/modelo.py` não tem diff.
12. O dashboard é apenas placeholder: `Dashboard de teste` e
    `Sem dados carregados`.
13. `[Esc] Sair` e `[B] Borda` aparecem apenas como texto inerte.
14. Não há alternância de bordas.
15. Não há estado ativo de borda.
16. Não há loop de aplicação.
17. Não há navegação.
18. Não há ação real, binding ativo ou registry.
19. Não há filtro, paginação funcional, seleção ou pop-up.
20. Não há dashboard real com dados.
21. Não há import de `curses`, `textual` ou `rich`. O grep amplo encontrou
    apenas uso da palavra "textual" em docstring de `tela/modelo.py`; a busca
    específica por import retornou vazia.
22. O diff rastreado contém somente arquivos autorizados; há ressalva Git para
    artefatos contextuais não rastreados.
23. Nenhum arquivo normativo tem diff.
24. `docs/relatorios/IMP-0006-tela-minima-borda-fixa.md` existe e registra
    comandos/resultados.
25. `tela/teste_renderizador.py` cobre H-0006 com igualdade estrita.
26. `tela/teste_diagnostico.py` foi atualizado para preservar o diagnóstico
    executável no novo formato.
27. Os testes H-0001 a H-0005 aplicáveis continuam passando; H-0001 e H-0002
    passaram diretamente, e o diagnóstico integrado preserva a cadeia com o
    renderer H-0006.

## Achados

### Bloqueantes

Nenhum.

### Não bloqueantes

1. `git status --short` mostra artefatos contextuais do ciclo H-0006 como
   não rastreados:
   `docs/handoff/H-0006-tela-minima-borda-fixa.md`,
   `docs/relatorios/RELATORIO_AUDITORIA_H-0006_HANDOFF.md` e
   `docs/relatorios/IMP-0006-tela-minima-borda-fixa.md`.
   O IMP é esperado como novo/não rastreado. Os outros dois foram tratados
   como ressalva de higiene Git por serem documentos de contexto do próprio
   ciclo, não alterações rastreadas da implementação.
2. O grep amplo por `textual` retorna ocorrência em docstring de
   `tela/modelo.py` (`Representacao textual auditavel do modelo`). A busca
   específica por imports de `curses`, `textual` ou `rich` retorna vazia.

## Avaliação dos pontos críticos

### API real de cabecalho

`ModeloTela.cabecalho` é `dict` em `tela/modelo.py`. A implementação usa:

```python
titulo = modelo.cabecalho.get("titulo", "(ausente)")
descricao = modelo.cabecalho.get("descricao", "(ausente)")
```

Não há dependência em `.titulo` ou `.descricao`, e `tela/modelo.py` não foi
alterado.

### Expected output e largura fixa

A saída bate com a constante `_EXPECTED_ORQUESTRADOR` dos testes. A inspeção
pontual confirmou `s.endswith("\n") is True` e 42 caracteres Python em todas
as linhas visuais não vazias:

```text
1  42  ╭ ORQUESTRADOR ...
2  42  │ Tela raiz do sistema ...
3  42  ╰...
5  42  ╭ DASHBOARD ...
6  42  │ Dashboard de teste ...
7  42  │ Sem dados carregados ...
8  42  ╰...
10 42  ╭ Menu ...
11 42  │ [Esc] Sair    [B] Borda ...
12 42  ╰...
```

### Chips inertes

`[Esc] Sair` e `[B] Borda` são strings hardcoded na caixa de menu. Não há
binding, registry, ação real, navegação ou alteração de estado associada.

### Ausência de funcionalidades fora de escopo

Não foram encontrados loop de aplicação, alternância de borda, estado ativo de
borda, leitura de configuração de estilo/menu, navegação, filtro, paginação,
seleção, pop-up, dashboard real com dados ou bibliotecas de UI.

### Substituição do formato H-0005

A substituição do formato textual estrutural H-0005 pela tela visual H-0006 é
aceitável neste ciclo. Os testes antigos de loader/modelo passam, o diagnóstico
continua executável, o renderer permanece puro e determinístico, e a cobertura
do renderer foi trocada por igualdade estrita contra o expected output H-0006.

## Conclusão

A implementação adere ao handoff H-0006 nos critérios funcionais, de pureza,
determinismo, largura fixa, uso da API real de `cabecalho`, inércia de chips e
ausência de funcionalidades fora de escopo.

Não há bloqueante técnico identificado.

## Recomendação

Aprovar o ciclo H-0006 com notas. Antes de fechamento operacional do ciclo,
regularizar no Git os artefatos documentais não rastreados do próprio H-0006,
incluindo o relatório IMP-0006 e os documentos contextuais que ainda aparecem
como `??`.
