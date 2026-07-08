# Relatório de Implementação — H-0010A Fluxo mínimo de lançador com tela destino

## Status

IMPLEMENTATION_COMPLETED

## Escopo implementado

Implementado o fluxo mínimo de lançador com tela destino, tornando o
renderer declarativo (lê todo conteúdo do modelo/JSON) e adicionando
navegação mínima local na demo (`tela_atual` + `pilha_telas`).

Especificamente:

1. Criada a tela `config/telas/destino_minimo.json` — tela completa
   mínima com `schema`, `id`, `cabecalho`, `corpo` (1 dashboard com
   campo `fonte: "literal"`) e `barra_de_menus` (chips `Esc Voltar` e
   `? Ajuda`).
2. Atualizado `config/telas/orquestrador.json` com item real em
   `corpo.elementos[id=lancador_principal].itens[]`, apontando
   `tela_destino: "destino_minimo"`; removido o campo `pendencia_itens`
   do elemento.
3. Reescrito `tela/renderizador.py` para percorrer
   `modelo.corpo.elementos[]` e `modelo.barra_de_menus["chips"]` em
   ordem declarada, produzindo uma caixa por elemento (console,
   dashboard, lancador) mais a caixa da barra de menus.
4. Rejeição de item de lançador com `texto` acima de 15 caracteres via
   `RenderizadorErro` — sem truncamento, sem abreviação.
5. Atualizada `tela/demo.py` com estado `tela_atual`/`pilha_telas` e
   `processar_comando(estado, comando, modelo=None)` suportando
   navegação mínima: chip de lançador empilha e troca de tela; Esc em
   tela interna volta via pop; Esc na raiz sai.
6. Atualizados os cinco arquivos de teste com `_EXPECTED_*` refletindo
   o novo output declarativo e novas verificações de navegação,
   hardcoding e limite de 15 caracteres.

## Arquivos criados

```text
config/telas/destino_minimo.json
docs/relatorios/IMP-0010A-fluxo-minimo-lancador-tela-destino.md
```

## Arquivos alterados

```text
config/telas/orquestrador.json
tela/renderizador.py
tela/demo.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
tela/teste_demo.py
tela/teste_diagnostico.py
```

Arquivos explicitamente NÃO alterados (justificadamente fora do escopo
aprovado): `tela/loader.py`, `tela/modelo.py`, `tela/diagnostico.py`,
`tela/__init__.py`, todos os `config/*.json` globais e todos os
arquivos normativos (`docs/contratos/`, `docs/adr/`,
`docs/NOMENCLATURA.md`, `docs/INDICE.md`, `docs/backlog.md`,
`docs/issues.md`, `docs/handoff/`).

## Decisões não tomadas

Nenhuma decisão arquitetural nova foi tomada. Todas as escolhas de
implementação seguiram estritamente o handoff aprovado
`docs/handoff/H-0010A-fluxo-minimo-lancador-tela-destino.md` e as
notas obrigatórias da auditoria
`docs/relatorios/RELATORIO_AUDITORIA_H-0010A_HANDOFF.md`:

- A contagem de renders da sequência `b d Esc Esc` segue a seção
  detalhada final (4 renders, conforme Nota 1 da auditoria).
- O label fixo `"Menus"` da caixa da barra é apenas rótulo visual e
  não vira fonte de chips/ações (Nota 2 da auditoria).
- Renderização de cada chip em linha própria (determinística, dentro
  da largura) — escolha operacional permitida pelo handoff ("em uma
  ou mais linhas de conteúdo").
- Placeholder `"(console)"` mantido como única exceção declarada de
  texto não proveniente do JSON (marcador explícito de escopo).

## Como o JSON dirige o comportamento

A tela é inteiramente definida pelo JSON. O renderer apenas interpreta
o `ModeloTela` recebido:

- **Cabecalho**: `titulo` (uppercased) vira o label da caixa;
  `descricao` vira a linha de conteúdo.
- **Console**: cada elemento de `tipo: "console"` vira uma caixa cujo
  label é `titulo` do elemento (fallback `"CONSOLE"`). Conteúdo fixo
  `"(console)"` (placeholder de escopo).
- **Dashboard**: cada elemento de `tipo: "dashboard"` vira uma caixa
  cujo label é `titulo` do elemento (fallback `"DASHBOARD"`). Para
  cada campo em `_campos_inertes["campos"]` com `fonte: "literal"`,
  o `valor` vira uma linha de conteúdo. Campos com outra `fonte`
  (ex.: `"pendente"`) são ignorados — sem texto, sem erro, sem
  placeholder. Por isso o `dashboard_info` do orquestrador (todos os
  campos `pendente`) renderiza como caixa sem conteúdo, e o
  `dashboard_teste` do destino_minimo renderiza o texto literal.
- **Lancador**: cada elemento de `tipo: "lancador"` vira uma caixa cujo
  label é `titulo` do elemento (fallback `"LANCADOR"`). Para cada item
  em `_campos_inertes["itens"]`, a linha `"[{chip}] {texto}"` é
  produzida. Itens com `texto` acima de 15 caracteres são rejeitados.
  Lista vazia produz caixa sem conteúdo.
- **Barra de menus**: lê `modelo.barra_de_menus["chips"]` na ordem
  declarada. Cada chip vira uma linha `"[{tecla}] {texto}"`. O label da
  caixa é o fixo `"Menus"` (rótulo visual, sem efeito comportamental).

Exemplos concretos do JSON dirigindo a diferença de comportamento:

- `orquestrador.json` declara `chip_esc.texto: "Sair"` → renderer
  exibe `"[Esc] Sair"`.
- `destino_minimo.json` declara `chip_esc.texto: "Voltar"` → renderer
  exibe `"[Esc] Voltar"`.
- A diferença de texto (Sair/Voltar) vem do JSON, não de exceção
  hardcoded por id de tela.
- A decisão Sair/Voltar (comportamento) vem do estado da `pilha_telas`
  na demo, não do renderer nem do id de tela.

## Como o renderer evita hardcoding de itens/chips

`tela/renderizador.py` não contém literais de itens do lançador nem de
chips da barra de menus. Verificado por inspeção de fonte em
`tela/teste_renderizador.py` (função `teste_inspecao_fonte_hardcoded`),
que confirma a ausência das strings:

```text
"[d] Destino"      (item do lancador do orquestrador.json)
"Destino"          (texto do item)
"[Esc] Sair"       (chip do orquestrador.json)
"[Esc] Voltar"     (chip do destino_minimo.json)
"Voltar"           (texto do chip)
"Sair"             (texto do chip)
"Páginas"          (chip do orquestrador.json)
"destino_minimo"   (tela_destino do item)
"Dashboard de teste" (placeholder antigo removido)
binding interno "[B] Borda" da demo (nunca declarado no JSON)
```

O renderer percorre estruturas genéricas (`_campos_inertes["itens"]`,
`_campos_inertes["campos"]`, `barra_de_menus["chips"]`) com format
strings `"[{0}] {1}"`. Não há `_ITENS_LANCADOR`, `_CHIPS_BARRA` ou
equivalentes. As únicas constantes de texto no módulo são:

- `_PLACEHOLDER_CONSOLE = "(console)"` — exceção declarada no handoff
  como marcador de escopo do elemento console.
- `_LABEL_BARRA = "Menus"` — label fixo permitido pelo handoff para a
  caixa da barra (rótulo visual, não fonte de chips/ações).

O renderer também:

- não importa `json`, `os`, `pathlib` nem `tela.loader`;
- não abre nem lê arquivos (`open`, `read_text`, `read_bytes`);
- não usa `subprocess`, `exec`, `eval`;
- não decide Sair/Voltar por id de tela;
- não avalia `regra_existencia` nem `regra_ativo`.

## Como a navegação mínima funciona

Estado da demo (`tela/demo.py`):

```python
{
    "tipo_borda": "curva",
    "saindo": False,
    "tela_atual": "orquestrador",
    "pilha_telas": [],
}
```

Regras (implementadas em `processar_comando`):

```text
chip de lancador == comando:
    push tela_atual em pilha_telas
    tela_atual = item.tela_destino

Esc (ou "s") com pilha_telas nao vazia:
    tela_atual = pilha_telas[-1]
    pilha_telas = pilha_telas[:-1]

Esc (ou "s") com pilha_telas vazia:
    saindo = True

"b":
    alterna tipo_borda
```

A decisão Sair/Voltar depende apenas do estado da pilha — não do id da
tela corrente. O renderer é declarativo; a demo implementa o fluxo
mínimo de navegação. `main()` recarrega o modelo via
`carregar_tela(None, tela_atual)` sempre que `tela_atual` muda, e
renderiza após alternar borda ou mudar de tela.

Compatibilidade: o terceiro argumento `modelo` de `processar_comando`
é opcional (default `None`); quando omitido, o comportamento de `"b"`,
`"s"` e `"\x1b"` é preservado. Estados legados sem `tela_atual` ou
`pilha_telas` recebem defaults (`"orquestrador"` e `[]`).

Não implementa: registry completo de telas, registry completo de
ações, descoberta automática ampla, índice central de telas, console
real, dashboard real com dados externos, seleção, filtros, paginação,
modo verboso, navegação por `[✥]`, nem validação funcional de
`tela_destino` no loader.

## Verificações executadas

### Validade dos JSONs

```bash
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
python -m json.tool config/telas/destino_minimo.json >/dev/null && echo "destino_minimo.json OK"
```

Resultado: ambos `OK`.

### Testes unitários e de integração

```bash
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_diagnostico.py
python tela/teste_demo.py
python tela/diagnostico.py
```

Resultado: todos encerraram com código de saída 0.

### Verificação de comportamento da demo em modo pipe

Sequência mínima:

```bash
printf 'b\n\x1b\n' | python tela/demo.py
```

Resultado: 2 renders (orquestrador curva inicial + orquestrador reta
após `b`); saída limpa; código 0.

Sequência completa de navegação:

```bash
printf 'b\nd\n\x1b\n\x1b\n' | python tela/demo.py
```

Resultado: 4 renders (orquestrador curva inicial + orquestrador reta
após `b` + destino_minimo reta após `d` + orquestrador reta após Esc
em destino); código 0. Interpretação alinhada à Nota 1 da auditoria
(seção detalhada final do handoff).

Sequência de navegação sem alternância de borda:

```bash
printf 'd\n\x1b\n\x1b\n' | python tela/demo.py
```

Resultado: 3 renders (orquestrador curva inicial + destino_minimo
curva após `d` + orquestrador curva após Esc em destino); código 0.

### Verificações de cache e estado Git

```bash
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print
```

Resultado: ambos vazios (nenhum arquivo de cache).

## Resultado dos testes

```text
python tela/teste_loader.py        -> exit 0 (42 verificacoes, 0 falhas)
python tela/teste_modelo.py        -> exit 0 (34 verificacoes, 0 falhas)
python tela/teste_renderizador.py  -> exit 0 (102 verificacoes, 0 falhas)
python tela/teste_diagnostico.py   -> exit 0 (28 verificacoes, 0 falhas)
python tela/teste_demo.py          -> exit 0 (95 verificacoes, 0 falhas)
python tela/diagnostico.py         -> exit 0
```

Cobertura adicional incluída (recomendações obrigatórias da auditoria):

- inspeção de fonte contra constantes hardcoded de itens do lançador
  (função `teste_inspecao_fonte_hardcoded` em `teste_renderizador.py`);
- inspeção de fonte contra chips hardcoded da barra de menus;
- teste de rejeição de texto de item de lançador com mais de 15
  caracteres, sem truncamento (`teste_erros_renderizador`);
- teste de aceitação de texto com exatamente 15 caracteres;
- inspeção de fonte confirmando acesso legítimo a `_campos_inertes`
  (renderer declarativo H-0010A);
- testes de navegação unitários (`teste_navegacao_minima`) e via
  subprocess (`teste_navegacao_subprocess`).

## Observações

- A auditoria aprovou o handoff com `QA_APPROVED_WITH_NOTES`
  (0 bloqueantes, 2 não bloqueantes). Ambas as notas foram
  incorporadas obrigatoriamente:
  - **Nota 1** (contagem de renders da sequência `b d Esc Esc`):
    seguida a seção detalhada final — comportamento coerente de 4
    renders no modo pipe. Confirmado em modo pipe.
  - **Nota 2** (label fixo `"Menus"` da caixa): o label é apenas
    rótulo visual (`_LABEL_BARRA = "Menus"`); a lista de chips,
    textos e ações vem do `barra_de_menus["chips"]` do JSON. O label
    não vira fonte de comportamento.
- Nenhum `__pycache__` ou `.pyc` foi criado durante os testes
  (`sys.dont_write_bytecode = True` preservado em todos os módulos).
- Nenhum commit foi realizado (CA-20).
- Nenhum arquivo normativo foi alterado (CA-17).

## Git status final

```text
 M config/telas/orquestrador.json
 M tela/demo.py
 M tela/renderizador.py
 M tela/teste_demo.py
 M tela/teste_diagnostico.py
 M tela/teste_loader.py
 M tela/teste_modelo.py
 M tela/teste_renderizador.py
?? config/telas/destino_minimo.json
?? docs/handoff/H-0010A-fluxo-minimo-lancador-tela-destino.md
?? docs/relatorios/IMP-0010A-fluxo-minimo-lancador-tela-destino.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0010A_HANDOFF.md
```

`git diff --stat`:

```text
 scripts/config/telas/orquestrador.json |  10 +-
 scripts/tela/demo.py                   | 156 ++++++++---
 scripts/tela/renderizador.py           | 255 ++++++++++++------
 scripts/tela/teste_demo.py             | 454 ++++++++++++++++++++++++++++-----
 scripts/tela/teste_diagnostico.py      |  74 ++++--
 scripts/tela/teste_loader.py           |  45 +++-
 scripts/tela/teste_modelo.py           |  34 ++-
 scripts/tela/teste_renderizador.py     | 429 +++++++++++++++++++++++++------
 8 files changed, 1174 insertions(+), 283 deletions(-)
```

Os arquivos `docs/handoff/H-0010A-*.md` e
`docs/relatorios/RELATORIO_AUDITORIA_H-0010A_*.md` são pré-existentes
(criados pelo processo de engenharia/auditoria antes da implementação)
e não foram alterados pelo executor. O `docs/relatorios/IMP-0010A-*.md`
é o relatório de implementação criado neste ciclo (previsto no
handoff). Nenhum arquivo normativo foi alterado.
