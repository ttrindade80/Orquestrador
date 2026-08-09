# IMP-0054 — seleção multinível

## Arquivos criados

- `config/telas/demo/h0054_selecao_multinivel.json`
- `config/telas/demo/h0054_selecao_multinivel_conteudo.json`
- `docs/relatorios/IMP-0054-selecao-multinivel.md`

## Arquivos alterados

- `tela/navegacao.py`
- `tela/selecao.py`
- `tela/renderizacao/console.py`
- `tela/renderizacao/conteudo_externo.py`
- `demo/demo.py`
- `tela/teste_navegacao.py`
- `demo/teste_demo_console.py`

## Comportamento entregue

O console cuja configuração declara explicitamente `politica_navegacao.tipo:
selecao_multinivel` usa uma única sequência pré-ordem para raiz, filhos e
netos. O cursor permanece independente da seleção. Espaço alterna folhas e
atua recursivamente sobre descendentes selecionáveis de um pai, sem incluir
descendentes não selecionáveis. A seleção é mantida por IDs e por console,
reconciliada contra IDs existentes, selecionáveis e navegáveis, e preservada
durante foco, cursor e troca de página.

A apresentação `hierarquia` reutiliza `ec` e `tg`, com os símbolos existentes,
e mantém o espaço de não selecionáveis vazio. O chip `[␣] Selecionar` acompanha
a acionabilidade do item corrente; `[Esc] Limpar` conserva a semântica
transversal; Enter permanece sem semântica H-0054. A paginação continua
exclusiva de PageUp/PageDown. Ajuda permanece ativa e por último. O ramo
`arvore_colapsavel` de H-0053 continua separado e sem seleção.

## Testes focais

- `PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_navegacao.py demo/teste_demo_console.py -q`
- Resultado: `77 passed`.

Os testes cobrem política explícita e fallback legado, percurso multinível,
independência cursor/seleção, toggle de folha, alcance recursivo, não
selecionáveis, reconciliação, chips, Enter, Esc, paginação, carregamento
separado, renderização e regressão H-0053.

## Suíte completa

- `PYTHONDONTWRITEBYTECODE=1 python -m pytest`
- Resultado: `1080 passed`.

## Demonstração executável

- `PYTHONDONTWRITEBYTECODE=1 python demo/demo.py h0054_selecao_multinivel`
- Execução não interativa concluída com código zero e quadro H-0054
  renderizado a partir das duas fixtures próprias.

## Validação manual pendente

Ainda dependem de TTY real a inspeção visual da geometria, do posicionamento
de `ec`/`tg`, do percurso com setas, da interação Tab/Shift+Tab, da
acionabilidade visual dos chips, da troca de páginas e da ausência de
comportamento de seleção em H-0053. Nenhuma aprovação manual foi declarada.

## Desvios, exceções e bloqueios

Nenhum desvio ou exceção operacional foi necessário. Nenhum arquivo fora da
lista autorizada foi alterado. Não houve bloqueio.
