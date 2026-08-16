# RELATÓRIO — QA_IMPLEMENTAÇÃO H-0072

```yaml
etapa: QA_IMPLEMENTACAO
objeto: H-0072 — capacidade genérica de formatação dos filhos de dois_niveis_por_foco
status: I1_IMPLEMENTATION_APPROVED
```

## Arquivos/diff auditados

`git status --short --untracked-files=all` confirma que o diff real coincide
exatamente com o declarado: 7 arquivos alterados (`tela/modelo.py`,
`tela/carregamento/tela_json.py`, `tela/navegacao.py`,
`tela/renderizacao/console.py`, `tela/renderizacao/conteudo_externo.py`,
`demo/demo.py`, `demo/teste_demo_console.py`) e 5 novos (módulo de
validação, duas fixtures, dois arquivos de teste). Nenhum arquivo fora do
escopo declarado foi tocado. `git diff --stat` das fixtures preservadas
(`h0055_*`, `h0063_estilo_estrutura_navegacao_dois_niveis.json`,
`h0062_estilo.json`) e dos arquivos declarados como não necessários
(`selecao.py`, `designadores.py`, `matriz_participantes.py`,
`teste_loader.py`) retorna vazio — intocados. Inspeção linha a linha de
cada diff confirma fidelidade ao handoff: extração pura em `modelo.py`,
dispatch condicional em `console.py` preservando o caminho vigente quando
`formato_filho_dois_niveis is None`, e toda a geometria nova isolada em
funções novas de `conteudo_externo.py` (0 linhas removidas do código
existente). Nenhum `try/except` novo mascara falha de validação.

## Testes executados

Focais: `216 passed`. Suíte completa: `1415 passed, 1 failed`, ambos
idênticos ao declarado.

## Falha H-0070

Auditada e confirmada não causal por evidência direta de código (mais forte
que a reprodução por `git stash` do relatório): o teste chama diretamente
`_linhas_apresentacao_hierarquia_com_mapa`, função que o diff do H-0072 não
alterou em nenhuma linha (apenas adições após seu término). `ControladorTelaEstilo`/`RuntimeEstilo` (tela/estilo.py, tela/loader.py) também
não constam do diff.

## Demonstração

`demo/teste_demo_h0072_formatacao_generica.py` percorre catálogo → loader
→ modelo → `processar_comando`/`renderizar_estado` → saída física (não
chama o renderer isoladamente). 5/5 passed, confirmado nesta auditoria.

## Requisitos funcionais

Fronteira de responsabilidades, schema/loader (V-DNF-01..11 fechados, sem
fallback), tabulação (unidade inteira, maior valor que cabe), designadores
(reuso de `_texto_designador`, sem tipo novo), apresentação texto/tabela
(sem cabeçalho/borda/título, sem `numero_colunas`), alinhamento global
(calculado sobre todos os pais), espaçamento 3..8, quebra multilinha (sem
novo cursor/toggle/identidade) e resize — todos verificados por código e
por teste correspondente, não triviais.

## Achados materiais

Nenhum.
\n