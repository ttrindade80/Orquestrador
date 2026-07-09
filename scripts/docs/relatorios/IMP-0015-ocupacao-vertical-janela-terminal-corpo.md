# IMP-0015 — Ocupação vertical da janela do terminal pelo corpo

## Status

`IMPLEMENTATION_COMPLETED`

Ciclo H-0015 implementado a partir do handoff
`docs/handoff/H-0015-ocupacao-vertical-janela-terminal-corpo.md` (base `4762583`),
sob a auditoria `AUDIT_APPROVED_WITH_NOTES` de
`docs/relatorios/RELATORIO_AUDITORIA_H-0015_HANDOFF.md`. Os achados
`ACH-H15-01`/`ACH-H15-02`/`ACH-H15-03`/`ACH-H15-04` foram tratados como
esclarecimentos obrigatórios (ver seção específica abaixo).

## Resumo

Implementada a ADR-0013 (ocupação vertical da janela do terminal pelo corpo).
Agora a tela ocupa a altura recebida do terminal quando a altura é suficiente:

- `tela/renderizador.py`: `renderizar_tela` passou a aceitar
  `altura: int | None = None`. Quando `altura` é informada e suficiente, a
  saída tem exatamente `altura` linhas; o renderer insere linhas físicas de
  `largura` espaços entre o último box de elemento do corpo e o box da
  `barra_de_menus`. Esse preenchimento é do renderer (não do JSON), não é novo
  arranjo nem novo elemento do corpo e não reinterpreta `corpo.arranjo`.
  Quando `altura is None`, o comportamento atual é preservado integralmente.
  Terminal pequeno gera `RenderizadorErro` determinístico (sem truncamento
  silencioso).
- `tela/demo.py`: `main()` lê largura **e** altura em uma única chamada de
  `shutil.get_terminal_size(fallback=(80, 24))`; `renderizar_estado` ganhou
  `altura=None` e repassa ao renderer; todas as chamadas em `main()` propagam
  a altura.
- `tela/teste_renderizador.py` e `tela/teste_demo.py`: novos casos de altura
  explícita, altura mínima, overflow do corpo, terminal pequeno, `altura=None`
  idêntico, largura das linhas de preenchimento, barra no rodapé e fluxo
  `g/d/b/Esc` preservado; ajuste das igualdades estritas de subprocess para
  considerar `altura=24` (fallback).

Base: `4762583 — docs: registra ocupacao vertical e barra responsiva`.

## Arquivos alterados/criados

Alterados (somente arquivos da lista "Alterar obrigatório" do handoff):

- `scripts/tela/renderizador.py`
  - Adicionado helper `_contar_linhas(caixa_str)` (`count("\n") + 1`).
  - Assinatura de `renderizar_tela` recebe `altura: int | None = None`;
    docstring atualizado documentando o novo parâmetro e seus lançamentos.
  - Extraídas as `linhas_barra` uma vez (reutilizadas para contagem e caixa).
  - Quando `altura is not None`: cálculo de `L_cab`, `L_barra`,
    `L_corpo_conteudo`; checagens de `L_cab + L_barra <= altura` e
    `L_corpo_conteudo <= L_corpo_disponivel` com `RenderizadorErro` descritivo;
    `L_corpo_fill = L_corpo_disponivel - L_corpo_conteudo`; inserção de
    `L_corpo_fill` linhas físicas de `" " * total_w` antes do box da barra.
  - Quando `altura is None`: caminho atual tomado integralmente (nenhuma
    alteração de comportamento).

- `scripts/tela/demo.py`
  - `main()`: `shutil.get_terminal_size(fallback=(80, 24))` em uma chamada,
    derivando `largura = tamanho_terminal.columns` e
    `altura = tamanho_terminal.lines`.
  - `renderizar_estado(estado, modelo, largura=None, altura=None)`: repassa
    `altura` ao renderer.
  - As duas chamadas a `renderizar_estado` em `main()` passam `altura=altura`.
  - Nenhuma outra linha de `demo.py` alterada.

- `scripts/tela/teste_renderizador.py`
  - Nova função `teste_altura_explicita()` cobrindo CA-01..CA-14 (altura=16,
    altura=24, altura mínima sem fill, contagem/largura/posição das linhas de
    preenchimento, barra no rodapé, `altura=None` idêntico, borda reta,
    overflow do corpo e terminal pequeno com `RenderizadorErro` descritivo,
    determinismo); registrada em `main()`.
  - Os casos existentes não foram alterados (`altura=None` é o default).

- `scripts/tela/teste_demo.py`
  - Nova constante `_ALTURA_SUBPROCESS = 24` e nota de determinismo.
  - `env_sem_columns` → `env_sem_dimensoes` (remove `COLUMNS` **e** `LINES`),
    forçando o fallback determinístico `(80, 24)` em subprocess.
  - Todas as saídas esperadas dos testes de subprocess passaram a ser
    computadas com `largura=_LARGURA_SUBPROCESS, altura=_ALTURA_SUBPROCESS`
    (igualdades estritas agora refletem a altura propagada).
  - Nova função `teste_renderizar_estado_altura()` cobrindo altura explícita
    via `renderizar_estado`, `altura=None` idêntico, consistência com
    `renderizar_tela`, barra no rodapé, invariante de largura e não alteração
    de estado/modelo; registrada em `main()`.
  - Adicionada verificação de determinismo de altura no subprocess do
    grupo_minimo (72 newlines = 3 renders × 24).

Criado:

- `scripts/docs/relatorios/IMP-0015-ocupacao-vertical-janela-terminal-corpo.md`
  (este arquivo).

Nenhum arquivo fora da lista de permitidos foi alterado. `config/`,
`tela/loader.py`, `tela/modelo.py`, `tela/diagnostico.py`, `tela/__init__.py`,
`tela/teste_diagnostico.py`, `docs/contratos/`, `docs/adr/`,
`docs/NOMENCLATURA.md`, `docs/INDICE.md`, `docs/backlog.md`, `docs/issues.md`
permanecem sem diff.

## Implementação realizada

### Contabilidade de linhas e representação das linhas de preenchimento

Conforme a seção "Contabilidade de linhas e representação das linhas em
branco" do handoff (fechando a pendência do item 9 da ADR-0013):

- `_contar_linhas(caixa_str) = caixa_str.count("\n") + 1` (caixa sem
  trailing newline).
- `L_cab = _contar_linhas(partes[0])` (cabeçalho é `partes[0]`).
- `L_barra = len(linhas_barra) + 2` (`_linhas_barra(...)` prévia + topo/base).
- `L_corpo_conteudo = sum(_contar_linhas(p) for p in partes[1:])`.
- `L_corpo_disponivel = altura - L_cab - L_barra`.
- `L_corpo_fill = max(0, L_corpo_disponivel - L_corpo_conteudo)`.
- Linhas de preenchimento: `" " * total_w`, inseridas como bloco entre o
  último box do corpo e o box da `barra_de_menus` (fora de qualquer caixa
  bordeada). Preserva os invariantes existentes (`"\n\n" not in saida` e
  `len(ln) == largura` para toda linha não vazia).

### Política para terminal pequeno (determinística)

Conforme o handoff:

- Se `altura` for fornecida e `L_cab + L_barra > altura`:
  `RenderizadorErro("altura insuficiente: terminal com {altura} linhas nao
  comporta cabecalho ({L_cab}) + barra_de_menus ({L_barra})")`.
- Se `altura` for fornecida e `L_corpo_conteudo > L_corpo_disponivel`:
  `RenderizadorErro("altura insuficiente: corpo requer {L_corpo_conteudo}
  linhas mas area disponivel e {L_corpo_disponivel} linhas (altura=...,
  cabecalho=..., barra=...)")`.

Nunca truncar, nunca omitir caixas silenciosamente.

### Contabilidade verificada — Orquestrador (largura=42, altura=24)

Confirmada contra `config/telas/orquestrador.json`:

| Quantidade | Valor |
|---|---|
| `L_cab` | 3 (1 topo + 1 descrição + 1 base) |
| `L_corpo_conteudo` | 9 (ITENS=3, INFO=2, NAVEGAR=4) |
| `L_barra` | 4 (1 topo + 2 chips + 1 base) |
| altura natural (sem fill) | 16 |
| `L_corpo_disponivel` (altura=24) | 24 − 3 − 4 = 17 |
| `L_corpo_fill` (altura=24) | 17 − 9 = 8 |
| Saída (altura=24) | 24 linhas (`saida.count("\n") == 24`) |

Tabela de exemplos confirmada pela execução real (largura=42):

| altura | Comportamento |
|---|---|
| `None` | 16 linhas (comportamento atual) |
| 16 | 16 linhas (sem preenchimento) |
| 24 | 24 linhas (8 linhas de preenchimento de 42 espaços) |
| 15 | `RenderizadorErro` (corpo overflow: requer 9, disponível 8) |
| 6 | `RenderizadorErro` (insuficiente: 3 + 4 = 7 > 6) |

Contagem natural das demais telas (largura=42, sem altura): `grupo_minimo`,
`destino_minimo` e `stub_b` produzem 10 linhas cada; com `altura=24` todas
passam a ocupar 24 linhas.

## Tratamento dos achados da auditoria

### ACH-H15-01 (alta severidade — tratado como esclarecimento obrigatório)

O handoff afirma que "os casos existentes de `teste_demo.py` não precisam ser
alterados". Isso é **falso** para os testes de integração por subprocess
(`teste_integracao_subprocess`, `teste_eof_sem_s`, `teste_navegacao_subprocess`),
que executam `python tela/demo.py` e comparam o stdout por igualdade estrita
contra `renderizar_tela(..., largura=80)` **sem** altura (16 linhas por render).
Após o H-0015, a `main()` da demo propaga `altura` (fallback `lines=24` em
pipe/não-tty), fazendo cada render passar a 24 linhas (8 de preenchimento);
as igualdades estritas existentes quebrariam CA-25.

**Tratamento**: como autorizado pelo gerente (correção operacional da
ambiguidade), as igualdades estritas de subprocess foram atualizadas. Todas as
saídas esperadas dos testes de subprocess passaram a ser computadas com
`renderizar_tela(..., largura=_LARGURA_SUBPROCESS, altura=_ALTURA_SUBPROCESS)`
(`_ALTURA_SUBPROCESS = 24`). Os casos de API direta
(`renderizar_estado`/`renderizar_tela` sem `altura`) permanecem com `altura=None`
(default) e continuam idênticos ao comportamento anterior — nesses a afirmação
"não precisam ser alterados" é correta e foi respeitada.

### ACH-H15-02 (baixa severidade)

Evitar `strip()` que destrua a evidência das linhas de preenchimento.
**Tratamento**: nos novos testes, as linhas de preenchimento são identificadas
e validadas comparando a linha **inteira** contra `" " * largura`
(`ln == fill_esperado`), sem `strip()`. A contagem total usa
`saida.count("\n") == altura`. Registrado também que `split("\n")` retorna
`altura + 1` elementos (último `""`) e `splitlines()` retorna `altura`
elementos.

### ACH-H15-03 (baixa-média severidade)

Garantir determinismo da altura em subprocess. **Tratamento**: o env dos
subprocess (`env_sem_dimensoes`) passou a remover **ambas** as variáveis
`COLUMNS` e `LINES` (antes removia apenas `COLUMNS`). Em pipe/não-tty,
`shutil.get_terminal_size(fallback=(80, 24))` então usa deterministicamente o
fallback `(80, 24)`, tornando as igualdades estritas portáveis entre
ambientes. O esperado é computado com a mesma `altura=24`. Verificação
explícita adicionada: o subprocess `'g\n\x1b\n\x1b\n'` produz exatamente
`72 = 3 × 24` newlines.

### ACH-H15-04 (nota)

Considerar `teste_diagnostico.py` quando o output esperado mudar.
**Tratamento**: `tela/teste_diagnostico.py` foi lido como referência. O
diagnóstico chama `renderizar_tela(modelo)` sem `largura` nem `altura`, logo
opera no caminho `altura=None` (comportamento preservado). A suíte
`python tela/teste_diagnostico.py` foi executada e segue exit 0 (28/28
verificações), sem necessidade de alteração — portanto o arquivo não foi
modificado (mantém-se na lista "alterar condicional" sem uso).

## Testes executados

```
python tela/teste_loader.py        → exit 0
python tela/teste_modelo.py        → exit 0
python tela/teste_renderizador.py  → exit 0
python tela/teste_demo.py          → exit 0
python tela/teste_diagnostico.py   → exit 0
```

Scripts de verificação determinística do handoff (todos OK):

- `renderizar_tela(modelo, largura=42, altura=24)` → `linhas: 24` (CA-02).
- `renderizar_tela(modelo, largura=42, altura=6)` → `RenderizadorErro`
  (CA-11).
- `renderizar_tela(modelo, largura=42)` ==
  `renderizar_tela(modelo, largura=42, altura=None)` (CA-09).
- Subprocess `python tela/demo.py` com `input='g\n\x1b\n\x1b\n'` → exit 0,
  `GRUPO MINIMO` no stdout, stderr vazio (CA-19..CA-21).

Novos casos adicionados:

- Em `teste_renderizador.py` (`teste_altura_explicita`, 20 verificações):
  altura>N_conteúdo (24 linhas, barra preservada), altura mínima (16) sem
  fill, altura=16 idêntico a `altura=None`, contagem/largura/posição das
  linhas de preenchimento (8 fills de 42 espaços), invariante `"\n\n"`
  ausente, `altura=None` preserva comportamento, largura=60+altura=24,
  borda reta no rodapé, overflow do corpo → `RenderizadorErro`,
  terminal pequeno → `RenderizadorErro`, limite `L_cab+L_barra` →
  `RenderizadorErro`, determinismo.
- Em `teste_demo.py` (`teste_renderizar_estado_altura`, 8 verificações):
  `renderizar_estado` aceita altura (24 linhas), altura mínima (16) sem
  fill, `altura=None` idêntico a sem altura, consistência com
  `renderizar_tela`, barra no rodapé, invariante de largura, não altera
  estado nem modelo; além disso ajuste das igualdades estritas de subprocess
  (agora com altura=24) e verificação de determinismo de altura (72
  newlines).

## Resultados

- `teste_renderizador.py`: 133/133 verificações, 0 falhas.
- `teste_demo.py`: 117/117 verificações, 0 falhas.
- `teste_diagnostico.py`: 28/28 verificações, 0 falhas.
- `teste_loader.py` / `teste_modelo.py`: exit 0 (sem `[FALHOU]`, sem
  traceback).
- `git diff --name-only` limita-se a `scripts/tela/renderizador.py`,
  `scripts/tela/demo.py`, `scripts/tela/teste_renderizador.py`,
  `scripts/tela/teste_demo.py`.
- Nenhum `__pycache__` nem `*.pyc` deixado no workspace.

Status final: **PASSOU**.

## Limitações conhecidas

- A demo lê o tamanho do terminal uma vez em `main()` (no início) e o
  reutiliza durante toda a sessão; um redimensionamento do terminal no meio
  da sessão não é reagido. Isso é aceitável para este ciclo (o fallback
  `(80, 24)` já garante comportamento defensivo) e está documentado no
  handoff como limitação esperada.
- A `demo` não captura `RenderizadorErro` em terminal muito pequeno: em um
  TTY real com altura insuficiente, a exceção propagaria (comportamento
  determinístico e descritivo, não silencioso). O handoff não exige captura
  na demo neste ciclo; os subprocess de teste usam altura=24 (suficiente) e
  não acionam esse caminho.
- O preenchimento vertical é puramente do renderer; não há persistência da
  altura entre chamadas/sessões e não há campo de altura no JSON (por
  decisão da ADR-0013 e do escopo negativo do handoff).

## Confirmação de fora de escopo

- **ADR-0014 não foi implementada**: nenhum item de
  `barra_de_menus.distribuicao.modo = "horizontal_responsiva"` foi
  implementado. Não houve quebra multilinha de chips, `coluna_a_coluna`,
  `linha_a_linha`, âncoras de chip, overflow da `barra_de_menus` nem erro de
  layout da barra. A barra continua com um chip por linha (comportamento
  atual). Esses itens pertencem ao H-0016.
- `corpo.arranjo = "vertical"` não foi alterado, removido nem reinterpretado:
  continua significando ordem/composição dos elementos (ADR-0011). A
  ocupação vertical da janela usa o termo específico `altura`/`L_corpo_*`
  (ADR-0013), distinto da composição.
- Não foi implementado: grupo com 2 elementos, layout horizontal,
  aninhamento, percentual/fração, console real, foco, seleção, navegação por
  `[✥]`, paginação, filtros, modo verboso, registry novo de ações/telas,
  mudança de schema/contratos/ADRs/NOMENCLATURA, hardcoding de chips no
  renderer, nem novo campo de altura no JSON.
- Nenhum commit foi realizado pelo executor.
