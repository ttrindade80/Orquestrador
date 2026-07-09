# RELATORIO_AUDITORIA_H-0015_HANDOFF

Auditoria do handoff `docs/handoff/H-0015-ocupacao-vertical-janela-terminal-corpo.md`
(H-0015 — Ocupação vertical da janela do terminal pelo corpo; base ADR-0013).

Auditor: opencode/GLM (modo somente leitura; nenhum arquivo de código, contrato,
ADR, configuração ou teste foi alterado; nenhum commit realizado).

## Status final

```
AUDIT_APPROVED_WITH_NOTES
```

Aprovação condicionada ao tratamento do achado `ACH-H15-01` (alta severidade)
antes ou durante a implementação. O núcleo de implementação (renderer + demo +
testes novos + contabilidade + política de erro + representação das linhas em
branco) está completo, determinístico, alinhado à ADR-0013 e isolado da
ADR-0014. Não há decisão arquitetural nova, não há contradição com ADR/contrato
e não há mistura de ADR-0014/H-0016.

## Arquivos analisados

Handoff alvo:
- `docs/handoff/H-0015-ocupacao-vertical-janela-terminal-corpo.md`

ADRs:
- `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md`
- `docs/adr/ADR-0014-barra-horizontal-termos-especificos.md`
- `docs/adr/INDICE_ADR.md`

Contratos:
- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_lancador.md`
- `docs/contratos/contrato_console.md`

Configs:
- `config/telas/orquestrador.json`
- `config/telas/grupo_minimo.json`
- `config/telas/destino_minimo.json`
- `config/telas/stub_b.json`

Código/testes:
- `tela/renderizador.py`
- `tela/demo.py`
- `tela/diagnostico.py`
- `tela/teste_renderizador.py`
- `tela/teste_demo.py`
- `tela/teste_diagnostico.py`

## Comandos executados

```
git log --oneline -6
git status --short
python -c "from tela.renderizador import renderizar_tela ..."   # contagem de linhas
python -c "import shutil; shutil.get_terminal_size(...)"         # fallback em pipe
python tela/teste_loader.py / teste_modelo / teste_renderizador / teste_demo / teste_diagnostico
python -c "subprocess demo com input=''"                          # linhas do stdout
ls scripts/docs/relatorios/
```

Resultados:
- `git status --short` → apenas `?? scripts/docs/handoff/H-0015-...md` (condizente com o estado esperado).
- `git diff --stat` / `git diff --name-only` → vazos (nenhuma alteração rastreada).
- Contagem atual (`largura=42`): orquestrador=16, grupo_minimo=10, destino_minimo=10, stub_b=10.
- `shutil.get_terminal_size(fallback=(80,24))` em contexto pipe/não-tty → `columns=80, lines=24` (fallback). No shell da auditoria `COLUMNS=0 LINES=0` (tratados como inválidos → fallback).
- Demo via subprocess com `input=''` → exit 0, stdout com 16 linhas, stderr vazio, sem `__pycache__`.
- As 5 suítes de teste passam (exit 0) no HEAD base `4762583` (baseline limpo).

## Resumo executivo

O H-0015 está maduro: alinha-se à ADR-0013 (inclusive fechando a pendência do
item 9 — representação exata das linhas em branco), isola totalmente a
ADR-0014/H-0016, distingue com clareza `ocupacao_vertical_terminal` de
`corpo.arranjo = "vertical"`, define contabilidade determinística de linhas
(verificada contra o `orquestrador.json` real: 3+9+4=16), fixa a representação
das linhas de preenchimento como linhas físicas de `" " * total_w` (escolha
que preserva os invariantes existentes `"\n\n" not in saida` e
`len(ln) == largura` para toda linha não vazia), define política determinística
de erro (`RenderizadorErro`, sem truncamento silencioso) e preserva o caminho
`altura=None` idêntico ao atual.

Foi identificado **um achado de alta severidade** (`ACH-H15-01`): o handoff
afirma, na seção de `teste_demo.py`, que "os casos existentes não precisam ser
alterados, pois `altura=None` é o default e o comportamento sem altura continua
idêntico". Isso é **falso para os testes de integração por subprocess** de
`tela/teste_demo.py`, que invocam `python tela/demo.py`: após o H-0015 a demo
propaga `altura` (fallback 24 em pipe), inserindo linhas de preenchimento, e as
verificações de igualdade estrita existentes (que comparam contra
`renderizar_tela(..., largura=80)` sem `altura`, 16 linhas) passam a falhar —
quebrando o critério de aceite obrigatório CA-25. Três achados adicionais de
baixa/nota tratam de orientação sobre `strip()`/`splitlines()` em testes,
determinismo da altura em subprocess e de uma omissão menor na "Leitura
obrigatória".

Como `tela/teste_demo.py` está na lista de arquivos permitidos ("alterar
obrigatório") e CA-22..CA-26 obrigam a executar as suítes, o implementador
conseguirá detectar e corrigir o problema dentro do escopo permitido; por isso
a classificação é `AUDIT_APPROVED_WITH_NOTES` (e não `AUDIT_REJECTED`). O
achado `ACH-H15-01` deve, contudo, ser endereçado — preferencialmente
corrigindo-se a afirmação do handoff antes da implementação.

## Verificação de aderência à ADR-0013

Conforme.

- Item 1/2 (largura já dinâmica; altura como dimensão explícita do render):
  `renderizar_tela` ganha `altura: int | None = None`; `demo.py` lê
  `tamanho_terminal.lines` e propaga. OK.
- Item 3 (corpo ocupa altura entre cabeçalho e barra_de_menus):
  `L_corpo_disponivel = altura - L_cab - L_barra`; preenchimento inserido entre
  o último box do corpo e o box da barra. OK.
- Item 4 (preencher com linhas em branco quando conteúdo < disponível):
  `L_corpo_fill = max(0, L_corpo_disponivel - L_corpo_conteudo)`. OK.
- Item 5 (preenchimento é do renderer, não do JSON): escopo negativo proíbe
  adicionar campo de altura ao JSON; `config/` proibido; `loader.py` proibido. OK.
- Item 6/7 (não altera semântica de `corpo.arranjo`; "vertical" é composição):
  reiterado no Contexto, na relação com ADR-0013, em CA-18 e no escopo negativo
  ("NÃO reinterpretar corpo.arranjo"). OK.
- Item 8 (uso de termo específico): handoff usa `altura`, `altura_disponivel`,
  `L_corpo_disponivel`, `L_corpo_fill` — termos específicos, não a substring
  "vertical" isolada. OK.
- Item 9 (decisão sobre representação das linhas em branco, pendente da ADR):
  **fechada** neste handoff — "linhas físicas de `largura` espaços"
  (`linha_branca = " " * total_w`), fora de qualquer caixa bordeada. OK (ponto
  forte).
- Item 10 (ADR não implementa código): o handoff assume a implementação; não
  contraria a ADR (que é normativa). OK.

Consequências obrigatórias da ADR-0013 (renderer recebe altura; demo propaga
`.lines`; testes validam ocupação vertical; contratos distinguem os termos)
estão total ou parcialmente atendidas: renderer/demo/testes — pelo handoff;
contratos — já registram `ocupacao_vertical_terminal`/`altura_disponivel`
(ver `contrato_composicao_corpo.md` §4.7 e `contrato_tela_json.md` §9).

## Verificação de isolamento da ADR-0014

Conforme (isolamento forte).

O handoff declara ADR-0014 como `adrs_fora_de_escopo` e dedica a seção
"ADR-0014 — explicitamente fora deste ciclo", listando os itens proibidos
(`barra_de_menus.distribuicao.modo = "horizontal_responsiva"`, quebra
multilinha de chips, `coluna_a_coluna`, `linha_a_linha`, âncoras, overflow da
barra, erro de layout da barra). O escopo negativo repete esses itens e os
atribui ao H-0016. CA-34 exige explicitamente que ADR-0014 não seja
implementada. A propagação de altura não toca em `_linhas_barra` (a barra
continua com um chip por linha, comportamento atual). Sem vazamento de escopo.

## Verificação de escopo positivo

Conforme.

- `demo.py`: ler largura+altura em uma única chamada
  (`shutil.get_terminal_size(fallback=(80,24))`); `renderizar_estado` ganha
  `altura=None` e repassa; todas as chamadas em `main()` repassam `altura`.
  Especificação precisa (antes/depois). OK.
- `renderizador.py`: assinatura `altura: int | None = None`; lógica de
  preenchimento quando `altura is not None`; caminho `altura is None`
  inalterado. Instruções F-2.1..F-2.5 precisas, inclusive como calcular
  `L_cab` (`partes[0].count("\n") + 1`), `L_barra` (prévia de
  `_linhas_barra` + 2) e `L_corpo_conteudo` (soma das caixas em `partes[1:]`).
  OK.
- `teste_renderizador.py` e `teste_demo.py`: novos casos de altura explícita,
  altura mínima, overflow, `altura=None` idêntico, fluxo g/d/b/Esc. OK.
- Criação de `docs/relatorios/IMP-0015-...md`. OK.

## Verificação de escopo negativo

Conforme.

Estão explicitamente proibidos: distribuição horizontal responsiva da barra,
quebra/âncoras/overflow de chips, segundo elemento no grupo, arranjo
horizontal, aninhamento, percentual/fração, console real, foco/seleção,
navegação por `[✥]`, paginação, filtros, modo verboso, registry novo de
ações/telas, alterar contratos/ADRs/NOMENCLATURA/INDICE/backlog/issues, alterar
semântica de chips, hardcodar chips, reordenar/truncar/omitir/completar chips,
reinterpretar `corpo.arranjo = "vertical"`, adicionar campo de altura ao JSON,
persistir altura entre chamadas/sessões, fazer commit.

## Verificação de arquivos permitidos/proibidos

Conforme (suficiente e mínimo).

Permitidos:
- Alterar obrigatório: `tela/renderizador.py`, `tela/demo.py`,
  `tela/teste_renderizador.py`, `tela/teste_demo.py`.
- Alterar condicional: `tela/teste_diagnostico.py` (apenas se testes existentes
  quebrarem; expectativa: não — diagnóstico usa `altura=None`).
- Criar: `docs/relatorios/IMP-0015-...md`.

Proibidos (corretos e completos): `docs/adr/`, `docs/contratos/`,
`docs/NOMENCLATURA.md`, `docs/INDICE.md`, `docs/backlog.md`, `docs/issues.md`,
`docs/handoff/`, `config/`, `tela/loader.py`, `tela/modelo.py`,
`tela/diagnostico.py`, `tela/__init__.py`, `tela/teste_loader.py`,
`tela/teste_modelo.py`, e "qualquer arquivo não listado como permitido". A
lista coincide com a árvore real de arquivos e com o fato de que a propagação
de altura exige tocar apenas renderer+demo (+ seus testes). `loader.py`/
`modelo.py` de fato não precisam mudar (confirmado: nenhum novo campo JSON).

Nota (ver `ACH-H15-04`): a "Leitura obrigatória" não lista
`tela/teste_diagnostico.py`, embora o liste como "alterar condicional".

## Verificação de critérios de aceite

CA-01..CA-38 cobrem: contagem exata de linhas (`count("\n") == altura`),
largura por linha, preenchimento com `" " * largura`, cabeçalho no topo, barra
no rodapé, posição das linhas de preenchimento, preservação de `altura=None`/
`largura=None`, `RenderizadorErro` em terminal pequeno (duas condições
distintas: `L_cab + L_barra > altura` e `L_corpo_conteudo > L_corpo_disponivel`),
mensagem descritiva, sem truncamento silencioso, demo lendo `.columns`/`.lines`
em uma chamada, `renderizar_estado` repassando ambos, fluxo g/d/b/Esc,
subprocess exit 0/stderr vazio, execução das 5 suítes, preservação de
loader/modelo/diagnostico/configs/contratos/ADRs/NOMENCLATURA, não-implementação
da ADR-0014, escopo de arquivos, criação do IMP-0015, ausência de commit e de
`__pycache__`.

A contabilidade declarada foi verificada contra o `orquestrador.json` real:
- `console "Itens"` → 1 linha de conteúdo (`(console)`) → caixa 3 linhas.
- `dashboard "Info"` → 0 campos `fonte="literal"` → 0 linhas de conteúdo → caixa 2 linhas.
- `lancador "Navegar"` → 2 itens → caixa 4 linhas.
- `cabecalho` → 1 descrição → caixa 3 linhas; `barra` → 2 chips → caixa 4 linhas.
Total = 3+9+4 = 16, batendo com a execução real (`largura=42` → 16 linhas) e
com a tabela de exemplos do handoff (altura 16→16; 20→4 fill; 24→8 fill;
15→`RenderizadorErro`; 6→`RenderizadorErro`).

Atenção especial (solicitada na auditoria) — análise das cinco questões:
- "linhas só de espaços contam como linhas do corpo?": resolvido pela separação
  `L_corpo_conteudo` (caixas) × `L_corpo_fill` (preenchimento físico entre
  corpo e barra); as linhas de preenchimento **não** estão dentro de caixa e
  **não** são novo elemento; contam para `altura` mas não para `L_corpo_conteudo`.
  Adequadamente especificado.
- "splitlines() preserva a contagem?": o handoff recomenda `count("\n") == altura`
  (robusto) e o equivalente `split("\n")` com `altura+1` elementos (último `""`).
  `str.splitlines()` também retorna exatamente `altura` elementos (a saída só
  contém `\n`). Consistente. (Ver `ACH-H15-02` para orientação explícita ausente.)
- "testes não devem usar strip()": o handoff **não** proíbe `strip()`
  explicitamente, mas CA-05 + o teste "verificar que cada uma tem exatamente 42
  espaços" exigem verificação por linha sem descaracterizar. (Ver `ACH-H15-02`.)
- "cada linha de preenchimento tem largura = largura renderizada": CA-05 e
  `" " * total_w` (`total_w = largura`). OK.
- "barra_de_menus termina no rodapé": CA-07 fixa que a última linha não vazia
  termina com `╯`/`┘`; como o box da barra é anexado após o preenchimento e a
  saída termina com `base + "\n"`, o rodapé é a base da barra. OK.

## Verificação de testes exigidos

Conforme, com ressalva (`ACH-H15-01`).

Novos casos exigidos em `teste_renderizador.py`: altura>conteúdo
(`count("\n")==24`, barra preservada); altura mínima sem fill; overflow do
corpo → `RenderizadorErro`; altura insuficiente para cabeçalho+barra →
`RenderizadorErro`; `altura=None` idêntico; linhas de preenchimento com
exatamente `largura` espaços.

Novos casos exigidos em `teste_demo.py`: `renderizar_estado` aceita `altura`;
`altura=None` idêntico a sem altura; fluxo g/d/b/Esc por subprocess com altura
explícita (exit 0, stderr vazio, "GRUPO MINIMO" no stdout).

Scripts de verificação por linha de comando e checagem de cache/estado git
também são exigidos.

Observação positiva: a escolha `" " * total_w` preserva os invariantes
existentes (`"\n\n" not in saida` e `len(ln)==largura` para toda linha não
vazia) — verificado pela leitura de `teste_renderizador.py` e `teste_demo.py`.

## Achados

### ACH-H15-01
- Severidade: **alta**
- Evidência: O handoff afirma (seção "Escopo positivo", item 4 —
  `tela/teste_demo.py`, e na seção "Testes obrigatórios"): *"Os casos existentes
  não precisam ser alterados, pois `altura=None` é o default e o comportamento
  sem altura continua idêntico."* Isso é verdadeiro para chamadas diretas à API
  (`renderizar_estado`/`renderizar_tela` sem `altura`), mas **falso para os
  testes de integração por subprocess** em `tela/teste_demo.py`, que executam
  `python tela/demo.py`. Após o H-0015 a `main()` da demo propaga `altura`
  (lida de `shutil.get_terminal_size(fallback=(80,24))`); em contexto de
  pipe/não-tty o fallback é `lines=24` (verificado). O Orquestrador hoje gera
  16 linhas em qualquer largura; com `altura=24` passará a gerar 24 (8 linhas
  de preenchimento). Os seguintes checkpoints existentes comparam o stdout do
  subprocess contra `renderizar_tela(..., largura=80)` **sem** `altura` (16
  linhas) e passarão a falhar:
  - `teste_integracao_subprocess`: `proc.stdout == saida_esperada`
    (`esperado_curva_80 + esperado_reta_80`);
  - `teste_eof_sem_s`: `proc.stdout == esperado_curva_80`;
  - `teste_navegacao_subprocess`: `bate_nav`, `bate_nav_borda`, `bate_nav_grupo`
    (igualdades estritas contra `renderizar_tela(..., largura=80)` sem altura).
- Impacto: Seguir literalmente a instrução "não precisam ser alterados" leva ao
  **rompimento de CA-25** (`python tela/teste_demo.py → exit 0`). Há contradição
  interna entre essa afirmação e o critério de aceite obrigatório CA-25. Não é
  bloqueante arquitetural (o arquivo `tela/teste_demo.py` está na lista de
  "alterar obrigatório" e CA-22..CA-26 obrigam a rodar as suítes), mas exige
  que o implementador desobedieça a afirmação do handoff e atualize essas
  igualdades estritas.
- Recomendação: Corrigir o handoff: em `teste_demo.py`, os casos existentes de
  igualdade estrita por subprocess **precisam** ser atualizados para considerar
  o `altura` propagado (ex.: computar o esperado com `altura=24`/fallback, ou
  fixar `COLUMNS`/`LINES` no `env` do subprocess e computar o esperado com o
  mesmo `altura`, ou relaxar para checagens de substring). Alternativamente,
  instruir explicitamente o implementador a fazê-lo e registrar a decisão no
  IMP-0015. Para `teste_renderizador.py` a afirmação "não precisam ser
  alterados" é correta (nenhuma chamada passa `altura`), não requer mudança.

### ACH-H15-02
- Severidade: **baixa**
- Evidência: A "atenção especial" pede garantia de que testes não usem
  `strip()` destruindo a evidência das linhas de preenchimento e que a
  contagem via `splitlines()` preserve o esperado. O handoff recomenda
  `count("\n") == altura` (robusto) e mostra o equivalente `split("\n")`
  (`altura+1` elementos), mas **não** explicita que: (a) testes de largura de
  linha de preenchimento não devem aplicar `.strip()`; (b) `splitlines()`
  também retorna exatamente `altura` elementos (a saída só contém `\n`).
- Impacto: Baixo — CA-05 e o caso de teste "verificar que cada uma tem
  exatamente 42 espaços" já induzem a checagem por linha sem `strip`. Risco
  residual de teste mal escrito.
- Recomendação: Adicionar nota explícita: testes de preenchimento devem
  verificar `len(linha) == largura` por linha identificada como preenchimento,
  sem `strip()`; preferir `count("\n") == altura` para a contagem total;
  registrar que `splitlines()` retorna `altura` elementos.

### ACH-H15-03
- Severidade: **baixa**
- Evidência: O novo teste por subprocess do handoff ("fluxo g/d/b/Esc com
  altura explícita") checa apenas exit/stderr/substring — robusto. Porém os
  testes de igualdade estrita existentes dependem de `altura` determinístico.
  Em `teste_demo.py`, `env_sem_columns` remove apenas `COLUMNS`, não `LINES`;
  se `LINES` estiver exportado com valor positivo ou houver tty controladora, o
  `altura` propagado pode diferir de 24, tornando as igualdades estritas
  não-determinísticas entre ambientes. (Na auditoria, `COLUMNS=0 LINES=0` →
  inválidos → fallback 24 determinístico.)
- Impacto: Baixo-médio — portabilidade dos testes de igualdade estrita por
  subprocess.
- Recomendação: Para asserções determinísticas por subprocess, definir
  explicitamente `COLUMNS` e `LINES` no `env` do subprocess (ou confiar no
  fallback) e computar o esperado com o mesmo `altura`.

### ACH-H15-04
- Severidade: **nota**
- Evidência: A "Leitura obrigatória" lista `tela/diagnostico.py` mas não
  `tela/teste_diagnostico.py`; ainda assim "Arquivos permitidos" marca
  `tela/teste_diagnostico.py` como "alterar condicional". Um implementador
  poderia ser instruído a editar um arquivo que não foi orientado a ler.
- Impacto: Mínimo — a expectativa é de que não precise mudar (diagnóstico usa
  `altura=None`).
- Recomendação: Incluir `tela/teste_diagnostico.py` na "Leitura obrigatória"
  como referência, ou declarar explicitamente que é somente leitura de
  referência neste ciclo.

## Conclusão

O H-0015 é implementável, determinístico e alinhado à ADR-0013, com isolamento
exemplar da ADR-0014/H-0016 e distinção clara entre `ocupacao_vertical_terminal`
e `corpo.arranjo = "vertical"`. A contabilidade de linhas foi confirmada contra
o `orquestrador.json` real (16 = 3+9+4); a escolha de linhas de preenchimento
como `" " * total_w` preserva os invariantes existentes (`"\n\n"` ausente e
largura uniforme). O único ponto material é o achado `ACH-H15-01`: a afirmação
"casos existentes não precisam ser alterados" é **incorreta** para os testes de
subprocess de `tela/teste_demo.py` e, se seguida literalmente, rompe CA-25.
Como o arquivo está no escopo permitido e a execução das suítes é obrigatória,
o problema é detectável e corrigível dentro do escopo — daí a classificação
`AUDIT_APPROVED_WITH_NOTES`. Recomenda-se corrigir a afirmação do handoff antes
de iniciar a implementação (ou instruir explicitamente o ajuste das igualdades
estritas de subprocess e registrá-lo no IMP-0015).

## Próxima ação recomendada

1. Corrigir o handoff H-0015 quanto a `ACH-H15-01` (retificar a afirmação sobre
   `tela/teste_demo.py` ou instruir o ajuste das igualdades estritas de
   subprocess, considerando `altura=24`/fallback e `COLUMNS`/`LINES` no `env`).
2. Opcionalmente incorporar as notas `ACH-H15-02`/`ACH-H15-03`/`ACH-H15-04`.
3. Após ajuste, reclassificar para `AUDIT_APPROVED` e liberar para implementação
   pelo executor, mantendo o bloqueio de `AUDIT_REJECTED`/`ARCHITECTURE_REVIEW_REQUIRED`
   reservado para casos de lacuna arquitetural ou mistura de ADR-0014 (não
   aplicáveis aqui).
