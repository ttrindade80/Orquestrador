# Relatorio de QA - H-0010A Fluxo minimo de lancador com tela destino

## Status final

QA_APPROVED_WITH_NOTES

## Escopo verificado

Foi verificada a implementacao do H-0010A contra o handoff, a auditoria do
handoff, o relatorio de implementacao, contratos diretamente relevantes e ADR
aplicavel.

Escopo funcional verificado:

- criacao de `config/telas/destino_minimo.json`;
- inclusao de item real no `lancador_principal` do `orquestrador.json`;
- renderizacao declarativa de `console`, `dashboard`, `lancador` e
  `barra_de_menus`;
- ausencia de hardcoding funcional de itens do lancador e chips da barra no
  renderer;
- navegacao minima local na demo via `tela_atual` e `pilha_telas`;
- fluxo `b`, `d`, Esc, Esc em modo pipe;
- preservacao dos ciclos anteriores.

## Arquivos lidos

```text
docs/handoff/H-0010A-fluxo-minimo-lancador-tela-destino.md
docs/relatorios/RELATORIO_AUDITORIA_H-0010A_HANDOFF.md
docs/relatorios/IMP-0010A-fluxo-minimo-lancador-tela-destino.md
docs/contratos/contrato_processo_desenvolvimento.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_barra_de_menus.md
docs/adr/ADR-0009-caminho-formato-jsons-tela.md
config/telas/orquestrador.json
config/telas/destino_minimo.json
tela/renderizador.py
tela/demo.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
tela/teste_demo.py
tela/teste_diagnostico.py
```

Tambem foram consultados por status/diff os arquivos proibidos ou sensiveis
listados no handoff.

## Comandos executados

```bash
git status --short
git diff --stat
git diff --name-only
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
python -m json.tool config/telas/destino_minimo.json >/dev/null && echo "destino_minimo.json OK"
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_diagnostico.py
python tela/teste_demo.py
python tela/diagnostico.py
printf 'b\nd\n\x1b\n\x1b\n' | python tela/demo.py
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print
git diff --name-only -- tela/loader.py tela/modelo.py tela/diagnostico.py tela/__init__.py docs/contratos docs/adr docs/NOMENCLATURA.md docs/INDICE.md docs/backlog.md docs/issues.md config/estilo.json config/lancador.json config/barra_de_menus.json config/cabecalho.json config/layout_console.json config/layout_dado.json config/layout_menu.json
rg -n "\[d\] Destino|\[Esc\] Sair|\[Esc\] Voltar|destino_minimo|Dashboard de teste|Sem dados carregados|Páginas|Voltar|Sair" tela/renderizador.py
rg -n "import (json|os|pathlib)|from (json|os|pathlib|tela\.loader)|open\(|read_text|read_bytes|carregar_tela|if .*tela.*orquestrador|tela_atual.*orquestrador|tela\.id|modelo\.id" tela/renderizador.py tela/demo.py
rg -n "texto.*16|1234567890123456|acima do limite|15 caracteres|RenderizadorErro" tela/teste_renderizador.py tela/teste_demo.py tela/teste_loader.py tela/teste_modelo.py tela/teste_diagnostico.py
```

## Resultado dos testes

```text
python tela/teste_loader.py        -> exit 0; 42 verificacoes, 0 falhas
python tela/teste_modelo.py        -> exit 0; 34 verificacoes, 0 falhas
python tela/teste_renderizador.py  -> exit 0; 102 verificacoes, 0 falhas
python tela/teste_diagnostico.py   -> exit 0; 28 verificacoes, 0 falhas
python tela/teste_demo.py          -> exit 0; 95 verificacoes, 0 falhas
python tela/diagnostico.py         -> exit 0
```

Total observado nos cinco testes: 301 verificacoes, 0 falhas.

## Verificacao dos JSONs de tela

`orquestrador.json` e `destino_minimo.json` sao JSONs validos.

`config/telas/destino_minimo.json` contem as chaves obrigatorias `schema`,
`id`, `cabecalho`, `corpo` e `barra_de_menus`. O `id` e `destino_minimo` e
coincide com o nome base do arquivo.

O corpo declara um dashboard simples com campo literal contendo:

```text
Tela de destino para teste do lancador
```

A barra de menus da tela destino declara `Esc` com texto `Voltar`.

## Verificacao do item real do lancador

`config/telas/orquestrador.json` contem `corpo.elementos[]` com
`id = lancador_principal` e uma lista `itens[]` com item real:

```text
chip = d
texto = Destino
tela_destino = destino_minimo
```

O texto `Destino` tem 7 caracteres e respeita o limite de 15 caracteres. O
campo antigo `pendencia_itens` nao permanece no elemento.

## Verificacao de renderizacao declarativa

`tela/renderizador.py` renderiza a partir do `ModeloTela` recebido:

- cabecalho a partir de `modelo.cabecalho`;
- corpo a partir de `modelo.corpo.elementos`;
- dashboard a partir de `_campos_inertes["campos"]` com `fonte: "literal"`;
- lancador a partir de `_campos_inertes["itens"]`;
- barra a partir de `modelo.barra_de_menus["chips"]`.

Nao foi encontrado fallback de item inventado pelo renderer. Lista vazia de
itens produz caixa vazia, conforme especificacao.

## Verificacao de ausencia de hardcoding

`tela/renderizador.py` nao importa `json`, `pathlib`, `os` nem `tela.loader`.
Tambem nao usa `open`, `read_text` ou `read_bytes`.

A busca por literais funcionais proibidos nao encontrou itens/chips hardcoded
no codigo executavel do renderer. A unica ocorrencia de `Sair/Voltar` esta em
comentario/docstring explicando que a decisao nao ocorre por id de tela.

Constantes fixas observadas e aceitas:

- `_PLACEHOLDER_CONSOLE = "(console)"`, excecao declarada pelo handoff;
- `_LABEL_BARRA = "Menus"`, rotulo visual aceito pela auditoria.

O label `Menus` nao e fonte de chips nem de acoes; os chips sao lidos do JSON.

## Verificacao da navegacao minima

`tela/demo.py` usa estado local com:

```text
tela_atual
pilha_telas
```

O chip `d` do lancador abre `destino_minimo`, empilhando a tela atual. Esc em
tela interna desempilha e volta para `orquestrador`; Esc em raiz define
`saindo = True`.

Nao foi encontrado registry completo de telas, registry completo de acoes nem
descoberta automatica ampla. A demo carrega o modelo pelo id da tela atual e a
decisao Sair/Voltar depende da pilha, nao de excecao por `id` de tela.

A alternancia de borda por `b` permanece preservada nas duas telas e o modo
pipe permanece deterministico.

## Verificacao da sequencia de pipe

Comando executado:

```bash
printf 'b\nd\n\x1b\n\x1b\n' | python tela/demo.py
```

Resultado observado: exit 0 e 4 renders:

1. Orquestrador inicial com borda curva;
2. Orquestrador com borda reta apos `b`;
3. `destino_minimo` com borda reta apos `d`;
4. Orquestrador com borda reta apos Esc em destino.

O Esc final em Orquestrador saiu sem render extra indevido.

## Verificacao de Esc Sair / Voltar

`orquestrador.json` declara `Esc` como `Sair`. `destino_minimo.json` declara
`Esc` como `Voltar`.

O comportamento da demo usa o contexto da pilha:

- pilha nao vazia: volta para a tela anterior;
- pilha vazia: sai.

Nao foi encontrada decisao comportamental do tipo `if tela.id == "orquestrador"`.

## Verificacao da rejeicao de texto longo

`tela/teste_renderizador.py` cobre item de lancador com `texto` de 16
caracteres (`1234567890123456`).

O comportamento observado e testado:

- levanta `RenderizadorErro`;
- menciona o limite de 15 caracteres;
- preserva o texto recusado na mensagem;
- nao trunca nem abrevia automaticamente.

Tambem ha teste aceitando texto com exatamente 15 caracteres.

## Verificacao de arquivos permitidos/proibidos

Arquivos modificados por diff:

```text
config/telas/orquestrador.json
tela/demo.py
tela/renderizador.py
tela/teste_demo.py
tela/teste_diagnostico.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
```

Arquivos novos esperados da implementacao:

```text
config/telas/destino_minimo.json
docs/relatorios/IMP-0010A-fluxo-minimo-lancador-tela-destino.md
```

Arquivos proibidos ou sensiveis verificados sem diff:

```text
tela/loader.py
tela/modelo.py
tela/diagnostico.py
tela/__init__.py
docs/contratos/
docs/adr/
docs/NOMENCLATURA.md
docs/INDICE.md
docs/backlog.md
docs/issues.md
config/estilo.json
config/lancador.json
config/barra_de_menus.json
config/cabecalho.json
config/layout_console.json
config/layout_dado.json
config/layout_menu.json
```

Observacao de estado Git: `git status --short` tambem mostra como nao
rastreados `docs/handoff/H-0010A-fluxo-minimo-lancador-tela-destino.md` e
`docs/relatorios/RELATORIO_AUDITORIA_H-0010A_HANDOFF.md`. O proprio handoff
declara excecao para o arquivo de handoff, criado antes da implementacao; o
relatorio de auditoria e artefato processual obrigatorio lido neste QA. Nao ha
diff nesses arquivos e nao ha evidencia de alteracao funcional fora do escopo.

## Verificacao de artefatos de cache

Os comandos:

```bash
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print
```

nao produziram saida. Nenhum `__pycache__` ou `.pyc` foi encontrado em `tela/`.

## Verificacao do relatorio de implementacao

`docs/relatorios/IMP-0010A-fluxo-minimo-lancador-tela-destino.md` existe e
descreve:

- escopo implementado;
- arquivos criados;
- arquivos alterados;
- como o JSON dirige o comportamento;
- como o renderer evita hardcoding de itens/chips;
- funcionamento da navegacao minima;
- verificacoes executadas;
- resultado dos testes;
- git status final.

O conteudo do relatorio e coerente com os resultados observados neste QA.

## Achados bloqueantes

Nenhum.

## Achados nao bloqueantes

1. O working tree contem artefatos processuais nao rastreados alem dos arquivos
   da implementacao (`docs/handoff/H-0010A-...` e
   `docs/relatorios/RELATORIO_AUDITORIA_H-0010A_HANDOFF.md`). Eles sao
   coerentes com o processo documentado e foram usados como entrada obrigatoria
   do QA, mas devem ser lembrados na revisao humana antes de eventual commit.

## Conclusao

A implementacao do H-0010A esta aderente ao handoff aprovado e aos contratos
verificados. O fluxo minimo de lancador com tela destino funciona em modo pipe,
o renderer opera de forma declarativa, os testes obrigatorios passam e nao ha
alteracoes detectadas em arquivos proibidos.

Status final: `QA_APPROVED_WITH_NOTES`.
