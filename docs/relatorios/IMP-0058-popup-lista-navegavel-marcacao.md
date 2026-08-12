# IMP-0058 — Popup: lista navegável e marcação

## Arquivos criados

- `demo/fixtures/h0058_popup_lista_marcacao.py`
- `docs/relatorios/IMP-0058-popup-lista-navegavel-marcacao.md`

## Arquivos alterados

- `tela/renderizacao/popup.py`
- `tela/teste_popup.py`
- `demo/demo.py`
- `demo/teste_demo_popup.py`
- `config/telas/demo/demo.json`

`tela/renderizacao/tela.py` e `demo/fixtures/h0057_popup_texto_dinamico.py` não
precisaram de alteração.

## Comportamento entregue

Foi implementado o envelope `tipo: marcacao`, com validação fechada de campos,
IDs, itens e cardinalidade inicial, além das políticas `exclusiva` e
`multipla`. A instância mantém separadamente declaração, envelope e estado
vivo por ID, com foco inicial, formações coluna/matriz/linha, preenchimento
vertical, navegação toroidal, eixos inativos, marcação exclusiva ou alternada,
ordem declarada e recomposição por resize. A apresentação usa os indicadores
universais resolvidos para foco e inclusão, mantendo instrução não selecionável,
moldura, chips e itens sem wrapping ou placeholders navegáveis.

O despacho modal mantém a mesma instância durante navegação, marcação, resize
e terminal pequeno. `Esc` retorna somente `{"status": "ABORTADO"}`; `Enter`,
carriage return e line feed permanecem sem efeito confirmatório e não há chave
`valor`.

## Testes executados e resultados

- `PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_popup.py demo/teste_demo_popup.py` — 59 passed.
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest` — 1156 passed.
- `git diff --check` — sem achados.

## Demonstração preparada

`config/telas/demo/demo.json` recebeu os acionamentos `e` e `m` para as
fixtures exclusiva e múltipla, cada uma com seis opções. O fluxo permite
observar foco, marcações, recomposição, quadro de terminal pequeno, `[Esc]
Voltar` e retorno `ABORTADO` para validação humana posterior em TTY.

## Desvios

Nenhum.

## Exceções

Nenhuma. O caminho textual anterior foi preservado e não houve alteração em
`tela/renderizacao/tela.py`.

## Bloqueios

Nenhum.
