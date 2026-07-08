# Relatório de Auditoria — H-0007 Handoff

## Status

AUDIT_APPROVED

## Escopo auditado

Auditoria documental e tecnica minima do handoff:

```text
docs/handoff/H-0007-alternancia-bordas-memoria.md
```

O ciclo auditado foi exclusivamente:

```text
H-0007 - Alternancia de bordas em memoria
```

Nao houve implementacao, correcao de codigo, alteracao do handoff,
alteracao de documentacao normativa, alteracao de configuracao nem execucao
de ciclo de implementacao.

## Arquivos lidos

Arquivos lidos conforme solicitacao:

```text
docs/handoff/H-0007-alternancia-bordas-memoria.md
docs/handoff/H-0006-tela-minima-borda-fixa.md
docs/relatorios/RELATORIO_AUDITORIA_H-0006_HANDOFF.md
docs/relatorios/IMP-0006-tela-minima-borda-fixa.md
docs/relatorios/RELATORIO_QA_H-0006_TELA_MINIMA_BORDA_FIXA.md
tela/modelo.py
tela/renderizador.py
tela/teste_renderizador.py
tela/diagnostico.py
tela/teste_diagnostico.py
config/telas/orquestrador.json
```

Arquivo extra lido:

```text
/home/tiago/.codex/attachments/d995f83d-4e66-42dc-ae1d-2adc5dd6617b/pasted-text.txt
```

Justificativa: continha a solicitacao desta auditoria, a lista de leitura
obrigatoria, os pontos obrigatorios de verificacao e o formato esperado deste
relatorio.

Nao foram lidos contratos, ADRs, `docs/NOMENCLATURA.md`,
`config/estilo.json`, `config/barra_de_menus.json`,
`config/layout_console.json` nem `config/lancador.json`.

## Verificacoes realizadas

1. O handoff autoriza apenas o H-0007 e nao antecipa ciclos futuros.
2. O objetivo tecnico limita a mudanca a alternancia de bordas em memoria.
3. A tela visual H-0006 e declarada como base e a saida default deve ser
   preservada em igualdade estrita.
4. Cabecalho, dashboard placeholder e menu inferior sao preservados.
5. A largura fixa e tratada como heranca tecnica provisoria do H-0006.
6. O handoff nao formaliza largura fixa como regra final de layout.
7. Largura dinamica, resize e calculo por terminal estao proibidos.
8. Leituras de `config/layout_console.json` e `config/lancador.json` estao
   proibidas.
9. Leituras de `config/estilo.json` e `config/barra_de_menus.json` estao
   proibidas.
10. Alteracao de `config/telas/orquestrador.json` esta proibida.
11. Alteracao de contratos, ADRs, NOMENCLATURA, indice, backlog e issues esta
    proibida.
12. A API de borda em memoria esta congelada em
    `renderizar_tela(modelo: ModeloTela, tipo_borda: str = "curva") -> str`.
13. A chamada padrao `renderizar_tela(modelo)` continua valida e deve produzir
    exatamente a saida H-0006.
14. `renderizar_tela(modelo, tipo_borda="curva")` deve ser identica ao
    default.
15. Ha exatamente dois nomes aceitos de borda: `"curva"` e `"reta"`.
16. Os caracteres de `"reta"` estao definidos precisamente:
    `┌`, `┐`, `└`, `┘`, `│`, `─`.
17. O expected output literal para `"reta"` esta definido e e suficiente para
    teste por igualdade estrita.
18. O comportamento para `tipo_borda` invalido esta especificado como
    `RenderizadorErro`, com case sensitivity.
19. Os testes novos exigem igualdade estrita e preservam as secoes H-0006.
20. `[B] Borda` permanece texto inerte, sem captura de teclado.
21. Acoes reais, bindings, loop, registry, navegacao, pop-up, filtros,
    paginacao e selecao estao proibidos.
22. `curses`, `textual`, `rich` e bibliotecas externas de UI estao proibidas.
23. Arquivos permitidos e proibidos estao definidos de forma clara e
    exaustiva.
24. O relatorio `docs/relatorios/IMP-0007-alternancia-bordas-memoria.md` e
    exigido.
25. Os comandos obrigatorios de verificacao estao definidos.

Comando executado nesta auditoria:

```bash
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
```

Resultado:

```text
orquestrador.json OK
```

## Achados

### Bloqueantes

Nenhum bloqueante identificado.

### Nao bloqueantes

Nenhum achado nao bloqueante identificado.

## Avaliacao dos pontos criticos

### API congelada

A API esta clara, suficiente e compativel com o codigo atual.

O renderer atual define `RenderizadorErro`, recebe `ModeloTela` e usa apenas
stdlib e `from tela.modelo import ModeloTela`. A extensao para:

```python
renderizar_tela(modelo: ModeloTela, tipo_borda: str = "curva") -> str
```

e local ao modulo `tela/renderizador.py` e nao exige arquitetura nova.

O handoff congela os nomes aceitos de borda em `"curva"` e `"reta"`, define
que outros valores lancam `RenderizadorErro` e explicita que a validacao e
case-sensitive.

### Compatibilidade com H-0006

A compatibilidade esta adequadamente especificada.

O handoff exige que:

```python
renderizar_tela(modelo)
```

continue produzindo exatamente a saida H-0006, incluindo o `\n` final.
Tambem exige que:

```python
renderizar_tela(modelo, tipo_borda="curva")
```

seja identica ao default.

O `tela/diagnostico.py` atual chama `renderizar_tela(modelo)` sem parametro
adicional. Portanto, mantendo o default `"curva"`, o diagnostico permanece
compativel com H-0006 sem alteracao preferencial.

### Borda alternativa

A borda `"reta"` esta definida com precisao suficiente:

```text
┌ ┐ └ ┘ │ ─
```

O handoff inclui expected output literal completo para
`_EXPECTED_ORQUESTRADOR_RETA`, define que cada linha visual tem 42 caracteres
Python e exige teste por igualdade estrita. Isso e suficiente para
implementacao deterministica e verificavel.

### Tipo de borda invalido

O comportamento esta especificado e e testavel.

Valores fora de `"curva"` e `"reta"` devem lancar `RenderizadorErro`. O
handoff tambem exige teste para `"invalida"` e `"CURVA"`, deixando claro que
a validacao e case-sensitive. Essa regra nao exige arquitetura nova.

### Largura fixa provisoria

O tratamento da largura fixa esta adequado ao escopo.

O handoff preserva:

```python
TOTAL_WIDTH = 42
INNER_WIDTH = 40
CONTENT_WIDTH = 39
_LABEL_MAX = 38
```

como constantes herdadas do H-0006 e declara explicitamente que a preservacao
nao formaliza regra final de layout, nao cumpre contrato final de composicao
de corpo, nao autoriza largura dinamica, nao autoriza resize e nao autoriza
leitura de `config/layout_console.json` ou `config/lancador.json`.

Nao ha indicacao de que o H-0007 resolva sizing/layout final. Se surgir
necessidade de largura dinamica, resize, layout por terminal ou parametros de
`console`/`lancador`, o proprio handoff manda parar com
`ARCHITECTURE_REVIEW_REQUIRED`.

### Ausencia de funcionalidades fora de escopo

O handoff mantem fora do escopo:

- leitura ou persistencia de estilo;
- leitura de configs fora do pipeline/testes ja existentes;
- alteracao de JSON da tela;
- captura de teclado;
- binding da tecla `B`;
- loop de aplicacao;
- acoes reais;
- registry de acoes ou tipos;
- navegacao;
- pop-up;
- dashboard real com dados;
- filtros, paginacao e selecao funcionais;
- bibliotecas de UI;
- cores e escape codes ANSI;
- mais de dois conjuntos de borda;
- estado persistido entre chamadas.

O texto `[B] Borda` permanece explicitamente inerte.

## Conclusao

O handoff H-0007 esta suficientemente fechado, consistente e seguro para ser
entregue ao GLM/OpenCode para implementacao estrita.

Nao ha necessidade de revisao arquitetural antes da implementacao. O ciclo
esta limitado a alternancia de bordas em memoria, preservando a tela visual
H-0006 e mantendo sizing/layout, configuracao, persistencia e interatividade
fora do escopo.

## Recomendacao

Seguir para implementacao estrita do H-0007 conforme o handoff, com atencao
especial a preservacao da saida default H-0006, ao erro `RenderizadorErro`
para `tipo_borda` invalido e a nao alteracao de arquivos fora da lista
autorizada.
