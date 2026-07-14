# Relatório de Implementação — H-0008 Aplicação demonstrável mínima com borda/sair

## Status

IMPLEMENTATION_COMPLETED

## Arquivos alterados

Arquivos criados:

```text
tela/demo.py                                                — CRIAR
tela/teste_demo.py                                          — CRIAR
docs/relatorios/IMP-0008-aplicacao-demonstravel-borda-sair.md  — CRIAR (este relatório)
```

Arquivos não alterados (confirmação explícita dos arquivos proibidos):

```text
tela/loader.py               — não alterado (H-0001)
tela/modelo.py               — não alterado (H-0002)
tela/renderizador.py         — não alterado (H-0006/H-0007; API consumida, não modificada)
tela/teste_loader.py         — não alterado (H-0001)
tela/teste_modelo.py         — não alterado (H-0002)
tela/teste_renderizador.py   — não alterado (H-0006/H-0007)
tela/diagnostico.py          — não alterado (H-0004; permanece não interativo e determinístico)
tela/teste_diagnostico.py    — não alterado (H-0004/H-0006; nenhuma alteração necessária)
tela/__init__.py             — não alterado
config/telas/orquestrador.json  — não alterado
config/                       — nenhum arquivo alterado
docs/contratos/               — não alterado
docs/adr/                     — não alterado
docs/NOMENCLATURA.md          — não alterado
docs/INDICE.md                — não alterado
docs/backlog.md               — não alterado
docs/issues.md                — não alterado
docs/handoff/                 — não alterado
```

`git diff --stat` e `git diff --name-only` não produzem saída (nenhum arquivo
rastreado foi modificado). Os únicos artefatos novos são os três arquivos
criados listados acima (todos `??` em `git status --short`).

## Resumo da implementação

Foi criada a aplicação demonstrável mínima `tela/demo.py`, que consome a
API entregue pelo H-0007 (`renderizar_tela(modelo, tipo_borda=...)`) sobre
a tela raiz do Orquestrador, carregada via pipeline H-0001 + H-0002.

A demo:

1. Carrega a tela raiz com `carregar_tela(None, "orquestrador")` e
   `construir_modelo(tela_raw)`.
2. Renderiza inicialmente com `tipo_borda="curva"` (default H-0006/H-0007).
3. Lê comandos de `sys.stdin` linha a linha (suporta uso via pipe).
4. O comando interno `b` alterna o estado de borda entre `"curva"` e
   `"reta"` em memória e re-renderiza.
5. O comando interno `s` marca `saindo=True` e encerra o loop sem nova
   renderização.
6. EOF em `sys.stdin` sem `s` encerra normalmente com código 0.
7. Mantém o estado de borda somente em variável local em memória; não
   grava arquivo, não altera JSON, não persiste preferência.
8. Não usa `input()`, não imprime prompt, não imprime mensagens de
   erro/despedida.
9. Não usa bibliotecas de UI; apenas biblioteca padrão do Python.

A API interna congelada do handoff foi implementada exatamente:

```python
def criar_estado_inicial():
    return {"tipo_borda": "curva", "saindo": False}


def processar_comando(estado, comando):
    novo = {"tipo_borda": estado["tipo_borda"], "saindo": estado["saindo"]}
    if comando == "b":
        novo["tipo_borda"] = "reta" if estado["tipo_borda"] == "curva" else "curva"
    elif comando == "s":
        novo["saindo"] = True
    return novo


def renderizar_estado(estado, modelo):
    return renderizar_tela(modelo, tipo_borda=estado["tipo_borda"])


def main():
    tela_raw = carregar_tela(None, "orquestrador")
    modelo = construir_modelo(tela_raw)
    estado = criar_estado_inicial()
    print(renderizar_estado(estado, modelo), end="")
    for linha in sys.stdin:
        comando = linha.strip()
        novo_estado = processar_comando(estado, comando)
        estado = novo_estado
        if estado["saindo"]:
            break
        if comando == "b":
            print(renderizar_estado(estado, modelo), end="")
    return 0
```

Estrutura de `tela/demo.py`: docstring descritiva; `import sys` e
`sys.dont_write_bytecode = True`; bloco `if __name__ == "__main__"` com
bootstrap de `sys.path` (mesmo padrão de `diagnostico.py`); importações
`from tela.loader import carregar_tela`, `from tela.modelo import
construir_modelo, ModeloTela`, `from tela.renderizador import
renderizar_tela`; definições das quatro funções; bloco final
`if __name__ == "__main__": sys.exit(main())`.

Os comandos `b` e `s` são estritamente internos da demo H-0008. Não são
bindings declarativos, não são registry de ações, não são ações genéricas
e não concretizam os chips inertes `[B] Borda` e `[Esc] Sair` do JSON.

## Decisões não tomadas

Este ciclo não implementa e não decide sobre:

- lançador (H-0009 — não autorizado);
- abertura de tela de teste;
- navegação entre telas ou por `tela_destino`;
- registry genérico de ações;
- bindings ativos declarativos do JSON;
- execução real de chips declarativos (`chip_esc`, `chip_borda`, etc.);
- transformação de `[B] Borda` ou `[Esc] Sair` em ação declarativa do JSON;
- dashboard real com dados;
- contrato novo de dashboard;
- pop-up;
- tela de processamento;
- filtros funcionais;
- paginação funcional;
- seleção funcional;
- resize ou largura dinâmica;
- layout responsivo;
- cálculo de largura real de terminal;
- leitura de `config/estilo.json`;
- leitura de `config/layout_console.json`;
- leitura de `config/lancador.json`;
- persistência de `tipo_borda` em arquivo ou variável global;
- impressão de prompt interativo (`input()`);
- transformação de `diagnostico.py` em loop interativo.

## Verificações executadas

Comandos executados a partir do diretório raiz do repositório de scripts
(`/home/tiago/Dropbox/UFRGS/Survey/versao_0_1/scripts`):

```bash
# 1. Integridade do JSON de configuração
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"

# 2. Invariantes H-0001 preservados
python tela/teste_loader.py

# 3. Invariantes H-0002 preservados
python tela/teste_modelo.py

# 4. Invariantes H-0006/H-0007 preservados
python tela/teste_renderizador.py

# 5. Invariantes H-0004/H-0006 preservados
python tela/teste_diagnostico.py

# 6. Testes da demo (H-0008)
python tela/teste_demo.py

# 7. Diagnóstico executável (saída curva H-0006/H-0007, não interativo)
python tela/diagnostico.py

# 8. Demo demonstrável (dois renders: curva e reta)
printf 'b\ns\n' | python tela/demo.py

# 9. Demo com EOF sem 's' (deve encerrar com código 0)
printf '' | python tela/demo.py; echo "exit_code=$?"

# 10. Verificação de bytecode
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print

# 11. Estado do repositório
git status --short
git diff --stat
git diff --name-only
```

## Resultado dos testes

### `python -m json.tool config/telas/orquestrador.json`

```text
orquestrador.json OK
```

### `python tela/teste_loader.py` (H-0001)

```text
Total de verificacoes: 37
Passaram: 37
Falharam: 0
```

Código de saída: `0`.

### `python tela/teste_modelo.py` (H-0002)

```text
Total de verificacoes: 30
Passaram: 30
Falharam: 0
```

Código de saída: `0`.

### `python tela/teste_renderizador.py` (H-0006/H-0007)

```text
Total de verificacoes: 58
Passaram: 58
Falharam: 0
```

Código de saída: `0`.

### `python tela/teste_diagnostico.py` (H-0004/H-0006)

```text
Total de verificacoes: 26
Passaram: 26
Falharam: 0
```

Código de saída: `0`.

### `python tela/teste_demo.py` (H-0008)

```text
== Secao 1 - Estado inicial ==
[PASSOU] criar_estado_inicial() retorna dict - tipo=dict
[PASSOU] estado inicial tem tipo_borda == 'curva' - tipo_borda='curva'
[PASSOU] estado inicial tem saindo == False - saindo=False
[PASSOU] duas chamadas retornam dicts independentes

== Secao 2 - processar_comando ==
[PASSOU] 'b' sobre curva -> tipo_borda == 'reta'
[PASSOU] 'b' sobre reta -> tipo_borda == 'curva'
[PASSOU] 'b' nao altera saindo
[PASSOU] 's' define saindo == True
[PASSOU] 's' nao altera tipo_borda (curva preservado)
[PASSOU] 's' sobre reta preserva tipo_borda == 'reta'
[PASSOU] comando desconhecido 'x' nao altera tipo_borda
[PASSOU] comando desconhecido 'x' nao altera saindo
[PASSOU] string vazia nao altera estado (tipo_borda preservado)
[PASSOU] string vazia nao altera estado (saindo preservado)
[PASSOU] 'B' (maiusculo) nao tem efeito sobre tipo_borda
[PASSOU] 'S' (maiusculo) nao altera saindo
[PASSOU] processar_comando nao modifica o dict original com 'b'
[PASSOU] processar_comando nao modifica o dict original com 's'
[PASSOU] alternancia completa: curva -> reta -> curva

== Secao 3 - renderizar_estado ==
[PASSOU] renderizar_estado com tipo_borda='curva' retorna str - tipo=str
[PASSOU] saida curva comeca com '╭ ORQUESTRADOR'
[PASSOU] saida curva bate com _EXPECTED_CURVA (igualdade estrita)
[PASSOU] renderizar_estado(estado_curva, modelo) == renderizar_tela(modelo, 'curva')
[PASSOU] renderizar_estado com tipo_borda='reta' retorna str - tipo=str
[PASSOU] saida reta comeca com '┌ ORQUESTRADOR'
[PASSOU] saida reta bate com _EXPECTED_RETA (igualdade estrita)
[PASSOU] renderizar_estado(estado_reta, modelo) == renderizar_tela(modelo, 'reta')
[PASSOU] renderizar_estado nao altera estado
[PASSOU] renderizar_estado nao altera modelo.cabecalho

== Secao 4 - Integracao via subprocess (demo completo) ==
[PASSOU] python tela/demo.py com 'b\ns\n' encerra com codigo 0 - returncode=0
[PASSOU] stdout contem render curva inicial ('╭ ORQUESTRADOR')
[PASSOU] stdout contem render reta apos 'b' ('┌ ORQUESTRADOR')
[PASSOU] stdout bate com _EXPECTED_CURVA + _EXPECTED_RETA
[PASSOU] stderr esta vazio - stderr=''
[PASSOU] config/telas/orquestrador.json inalterado apos demo

== EOF sem 's' (encerra com codigo 0) ==
[PASSOU] printf '' | python tela/demo.py encerra com codigo 0 - returncode=0
[PASSOU] stdout com EOF sem 's' contem apenas render curva inicial

== Secao 5 - Preservacao do diagnostico ==
[PASSOU] gerar_diagnostico_tela() nao lanca excecao
[PASSOU] retorno de gerar_diagnostico_tela() e str - tipo=str
[PASSOU] gerar_diagnostico_tela() bate com _EXPECTED_CURVA (default curva)
[PASSOU] python tela/diagnostico.py encerra com codigo 0 - returncode=0
[PASSOU] stdout de diagnostico.py bate com _EXPECTED_CURVA
[PASSOU] diagnostico.py nao contem 'sys.stdin'
[PASSOU] diagnostico.py nao contem 'input('

== Proibicoes de import no modulo tela/demo.py ==
[PASSOU] demo.py nao importa 'json'
[PASSOU] demo.py nao importa 'os'
[PASSOU] demo.py nao importa 'pathlib'
[PASSOU] demo.py nao importa bibliotecas de UI (curses/textual/rich)
[PASSOU] demo.py nao usa subprocess/exec/eval

== Resumo ==
Total de verificacoes: 49
Passaram: 49
Falharam: 0
```

Código de saída: `0`.

### `python tela/diagnostico.py` (H-0004 — não interativo)

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

Código de saída: `0`.

## Demonstração controlada

### `printf 'b\ns\n' | python tela/demo.py`

Saída literal do stdout (render curva inicial + render reta após `b`,
sem separador, saída limpa por `s`):

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
┌ ORQUESTRADOR ──────────────────────────┐
│ Tela raiz do sistema — ponto de entrada│
└────────────────────────────────────────┘

┌ DASHBOARD ─────────────────────────────┐
│ Dashboard de teste                     │
│ Sem dados carregados                   │
└────────────────────────────────────────┘

┌ Menu ──────────────────────────────────┐
│ [Esc] Sair    [B] Borda                │
└────────────────────────────────────────┘
```

Código de saída: `0`.

A saída bate exatamente com `_EXPECTED_CURVA + _EXPECTED_RETA`, conforme
verificado em `tela/teste_demo.py` (Seção 4, igualdade estrita).

### `printf '' | python tela/diagnostico.py` e `printf '' | python tela/demo.py` (EOF sem `s`)

Ambos encerram com código `0`. Com EOF sem `s`, a demo imprime apenas o
render curva inicial e encerra normalmente.

## Verificação de bytecode

```bash
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print
```

Saída: vazia (nenhum `__pycache__` nem `.pyc` em `tela/`). Todos os
módulos do pacote definem `sys.dont_write_bytecode = True` antes das
importações, portanto não há geração de bytecode.

## Estado do repositório

### `git status --short`

```text
?? docs/handoff/H-0008-aplicacao-demonstravel-borda-sair.md
?? docs/relatorios/IMP-0008-aplicacao-demonstravel-borda-sair.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0008_HANDOFF.md
?? tela/demo.py
?? tela/teste_demo.py
```

Os arquivos `docs/handoff/H-0008-*.md` e
`docs/relatorios/RELATORIO_AUDITORIA_H-0008_*.md` já existiam antes do
início da implementação (são a entrada e a auditoria deste ciclo). Os
arquivos criados por esta implementação são `tela/demo.py`,
`tela/teste_demo.py` e este relatório
`docs/relatorios/IMP-0008-aplicacao-demonstravel-borda-sair.md`.

### `git diff --stat`

```text
(vazio)
```

### `git diff --name-only`

```text
(vazio)
```

Nenhum arquivo rastreado foi modificado. Nenhum arquivo em `config/`,
`docs/contratos/`, `docs/adr/`, `docs/handoff/`, `docs/NOMENCLATURA.md`,
`docs/INDICE.md`, `docs/backlog.md` ou `docs/issues.md` foi alterado.

## Ausência de persistência

- `config/telas/orquestrador.json` não foi alterado — confirmado por
  `git diff --name-only` vazio e por verificação de conteúdo antes/depois
  do subprocess em `tela/teste_demo.py` (Seção 4).
- Nenhum arquivo novo foi criado em `config/` ou `tela/` durante a
  execução da demo além dos arquivos-fonte da implementação.
- Uma segunda execução da demo inicia com `tipo_borda="curva"` (estado
  reiniciado em memória).
- `processar_comando` não usa variável global mutável.
- `tela/demo.py` não importa `json`, `os`, `pathlib` nem bibliotecas de
  UI; não abre arquivos em disco além do que `carregar_tela` faz; não
  acessa `config/estilo.json`, `config/layout_console.json` nem
  `config/lancador.json`.

## Comportamento fora de escopo preservado como inerte

Os itens abaixo permanecem inertes e fora de escopo do H-0008, conforme
declarado no handoff e em `config/telas/orquestrador.json`:

- lançador (`lancador_principal.itens == []`);
- navegação entre telas (`tela_destino` pendente em `chip_estilo`);
- registry de ações (`referencias_de_acoes.status == "pendente_DOC-B009"`);
- bindings ativos (`bindings` preservado como declaração inerte);
- execução real de chips declarativos;
- dashboard real com dados (`origem_dados.referencia == "pendente"`);
- filtros funcionais (`filtros` preservado como lista inerte);
- paginação/seleção/resize/largura dinâmica/layout responsivo;
- leitura de `config/estilo.json`, `config/layout_console.json`,
  `config/lancador.json`.

Os comandos `b` e `s` da demo são internos a `tela/demo.py` e não
concretizam os chips `[B] Borda` e `[Esc] Sair` do JSON.

## Observações

- A largura fixa herdada do H-0006 (`TOTAL_WIDTH=42`, `INNER_WIDTH=40`,
  `CONTENT_WIDTH=39`) foi preservada provisoriamente, sem declaração
  normativa de layout. Nenhuma linha visual da saída teve seu comprimento
  alterado; cada linha não vazia da saída permanece com exatamente 42
  caracteres Python (verificado em `tela/teste_renderizador.py`).
- `tela/diagnostico.py` permanece não interativo e determinístico,
  chamando `renderizar_tela(modelo)` sem `tipo_borda` e produzindo a
  saída default curva H-0006/H-0007. Não foi alterado.
- `tela/teste_diagnostico.py` não precisou ser alterado — todas as 26
  verificações continuam passando sem modificação.
- A verificação de bibliotecas de UI em `tela/teste_demo.py` checa
  `import curses`/`from curses`, `import textual`/`from textual`,
  `import rich`/`from rich` (padrão de checagem por instrução de import,
  alinhado aos demais módulos de teste do pacote).
- Commit não realizado — responsabilidade do engenheiro.

## Resultado final

IMPLEMENTATION_COMPLETED
