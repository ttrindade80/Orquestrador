# Relatório de Auditoria — H-0010A Fluxo mínimo de lançador com tela destino

## Status final

QA_APPROVED_WITH_NOTES

## Escopo auditado

Auditoria documental e operacional do handoff:

```text
docs/handoff/H-0010A-fluxo-minimo-lancador-tela-destino.md
```

Objetivo auditado: verificar se o H-0010A está pronto para implementação
estrita por GLM/OpenCode, sem implementação, sem correção de handoff, sem
alteração de JSON, testes, contratos, ADRs e sem commit.

## Arquivos lidos

Arquivos obrigatórios lidos:

```text
docs/handoff/H-0010A-fluxo-minimo-lancador-tela-destino.md
docs/contratos/contrato_processo_desenvolvimento.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_barra_de_menus.md
docs/adr/ADR-0009-caminho-formato-jsons-tela.md
config/telas/orquestrador.json
tela/loader.py
tela/modelo.py
tela/renderizador.py
tela/demo.py
tela/diagnostico.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
tela/teste_demo.py
tela/teste_diagnostico.py
```

## Consultas adicionais justificadas

Consulta adicional:

```text
/home/tiago/.codex/attachments/d0055dfe-6cb0-4cb9-9ed1-40d8b390b3b8/pasted-text.txt
```

Justificativa: arquivo anexado continha a solicitação operacional desta
auditoria.

Também foi executado `rg --files` como inventário inicial do repositório para
confirmar a existência dos artefatos obrigatórios.

## Comandos executados

```bash
git status --short
git diff --stat
git diff --name-only
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_diagnostico.py
python tela/teste_demo.py
python tela/diagnostico.py
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print
```

Resultado observado:

- `git status --short`: apenas `?? docs/handoff/H-0010A-fluxo-minimo-lancador-tela-destino.md`.
- `git diff --stat`: sem saída.
- `git diff --name-only`: sem saída.
- `orquestrador.json OK`.
- Todos os testes e `tela/diagnostico.py` encerraram com código 0.
- `find` para `__pycache__` e `*.pyc`: sem saída.

## Aderência ao contrato de processo

Aderente. O handoff declara escopo, limites de arquivos permitidos/proibidos,
critérios de aceite verificáveis, comandos de verificação, condições de
bloqueio e relatório de implementação esperado.

O handoff não autoriza alteração de contratos, ADRs, NOMENCLATURA, índice,
backlog, issues ou handoffs normativos.

## Aderência ao contrato_tela_json

Aderente. O handoff exige que `destino_minimo.json` contenha `schema`, `id`,
`cabecalho`, `corpo` e `barra_de_menus`, e mantém a tela como declaração JSON
interpretada pelo pipeline loader -> modelo -> renderer.

O dashboard mínimo é tratado como elemento passivo declarado em
`corpo.elementos[]`, sem `config/dashboard.json` e sem implementação de
dashboard real.

## Aderência ao contrato_lancador

Aderente. O handoff exige item real em
`corpo.elementos[id=lancador_principal].itens[]`, com `id`, `chip`, `texto` e
`tela_destino`, e determina que o renderer percorra `itens[]` do modelo/JSON.

O handoff proíbe item hardcoded, chip hardcoded, destino hardcoded e fallback
inventado de item no renderer. Também exige rejeição de `texto` acima de 15
caracteres sem truncamento.

## Aderência ao contrato_barra_de_menus

Aderente. O handoff exige que os chips sejam lidos de
`modelo.barra_de_menus["chips"]`, renderizados na ordem declarada e sem lista
hardcoded universal no renderer.

`orquestrador.json` preserva Esc/Sair declarado na tela raiz, e
`destino_minimo.json` deve declarar Esc/Voltar.

## Aderência à ADR-0009

Aderente. O handoff exige criar:

```text
config/telas/destino_minimo.json
```

e exige que o `id` interno seja `destino_minimo`, coincidente com o nome base
do arquivo. Não cria índice central obrigatório de telas e não cria JSONs
globais por componente.

## Verificação da granularidade

Aderente. O H-0010A define uma capacidade coesa: fluxo mínimo de lançador com
tela destino. Ele não fragmenta a entrega em micro-handoffs por campo, item,
Esc, render de barra ou render da tela destino.

## Verificação de ausência de hardcoding

Aderente. O handoff proíbe expressamente:

- item hardcoded de lançador no renderer;
- lista literal tipo `_ITENS_LANCADOR`;
- chip hardcoded do lançador;
- texto ou `tela_destino` hardcoded;
- chips hardcoded da `barra_de_menus`;
- `[B] Borda` hardcoded na saída do renderer;
- decisão de Sair/Voltar por id hardcoded de tela.

Ressalva não bloqueante: a seção de renderização da barra permite label fixo
`"Menus"` para a caixa. Como a regra crítica auditada é o conteúdo dos chips
vir do JSON, e como isso está explicitamente reforçado no handoff, a ressalva
não impede implementação estrita.

## Verificação de tela_destino e destino_minimo

Aderente. O handoff exige:

- `config/telas/destino_minimo.json`;
- `id = destino_minimo`;
- `schema = tela.v1`;
- `cabecalho`;
- `corpo`;
- `barra_de_menus`;
- dashboard com texto literal `Tela de destino para teste do lancador`;
- `orquestrador.json` apontando `tela_destino: "destino_minimo"`.

`tela_destino` é tratado como dado ativo para navegação mínima da demo, não
como campo inerte ignorado.

## Verificação de navegação mínima

Aderente. O handoff limita a navegação a:

- `tela_atual`;
- `pilha_telas`;
- acionamento de chip do lançador para abrir `tela_destino`;
- Esc em tela interna volta por pop da pilha;
- Esc na raiz sai.

O handoff proíbe registry completo de telas, registry completo de ações,
descoberta automática ampla, índice central, console real, seleção, filtros,
paginação, modo verboso e navegação por `[✥]`.

Ressalva não bloqueante: há inconsistência interna na contagem de renders para
`printf 'b\nd\n\x1b\n\x1b\n' | python tela/demo.py`. Uma seção intermediária
fala em 3 renders, omitindo o render inicial. A seção obrigatória posterior
corrige para 4 renders: inicial curva, orquestrador reta, destino reta,
orquestrador reta. Como a especificação detalhada final é clara, isto não
bloqueia a implementação.

## Verificação de arquivos permitidos/proibidos

Aderente. A lista permitida é suficiente para a capacidade:

```text
config/telas/destino_minimo.json
docs/relatorios/IMP-0010A-fluxo-minimo-lancador-tela-destino.md
config/telas/orquestrador.json
tela/renderizador.py
tela/demo.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
tela/teste_demo.py
tela/teste_diagnostico.py
```

A exclusão de `tela/loader.py` e `tela/modelo.py` é aceitável: o loader atual
carrega telas por `id`, valida a macro obrigatória e preserva elementos; o
modelo atual preserva `itens[]`, `campos[]` e demais campos dos elementos em
`_campos_inertes`, além de preservar `barra_de_menus` como dict.

Os arquivos proibidos incluem contratos, ADRs, NOMENCLATURA, índices, backlog,
issues, configs transicionais globais e `tela/__init__.py`.

## Verificação dos critérios de aceite

Aderente. O handoff contém critérios objetivos para:

- validade de `orquestrador.json` e `destino_minimo.json`;
- coincidência entre id interno e nome base do arquivo;
- tela destino com estrutura macro obrigatória;
- item real do lançador em `orquestrador.json`;
- `tela_destino: "destino_minimo"`;
- texto do item com limite de 15 caracteres;
- rejeição sem truncamento de texto acima do limite;
- renderer sem constante hardcoded de itens;
- renderer sem chips hardcoded de barra;
- render do texto literal de destino;
- Esc Voltar em destino;
- Esc Sair na raiz;
- alternância de borda nas duas telas;
- testes anteriores passando;
- ausência de `__pycache__` e `.pyc`;
- relatório IMP criado;
- ausência de commit.

## Achados bloqueantes

Nenhum.

## Achados não bloqueantes

1. A contagem de renders da sequência `b`, `d`, Esc, Esc aparece de forma
   inconsistente em duas seções. A seção detalhada final estabelece 4 renders,
   que é o comportamento coerente com o render inicial da demo.

2. A seção de barra de menus permite label fixo `"Menus"` na caixa. Como o
   conteúdo dos chips deve vir do JSON e a lista hardcoded é proibida, isto
   não bloqueia, mas o executor deve evitar interpretar esse label como fonte
   de chips ou ações.

## Recomendações

- Durante a implementação, seguir a seção "Verificação de comportamento da
  demo em modo pipe" como fonte operacional para a contagem de renders.
- Manter `renderizador.py` sem leitura direta de arquivo e sem import de
  `json`, `pathlib`, `os` ou `tela.loader`.
- Nos testes atualizados, incluir inspeção de fonte contra constantes de item
  e chips hardcoded, além do caso de `texto` de lançador com mais de 15
  caracteres.

## Conclusão

O H-0010A corrige a lacuna arquitetural do H-0010 original e está apto para
implementação por GLM/OpenCode. As ressalvas encontradas são operacionais e
não impedem execução estrita do handoff.
