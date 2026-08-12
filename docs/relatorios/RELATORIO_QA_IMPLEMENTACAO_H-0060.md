# Relatório QA da implementação H-0060

status: IMPLEMENTATION_REJECTED

## Arquivos auditados

- `docs/handoff/H-0060-resize-responsivo-formacoes-popup-marcacao.md`
- `docs/relatorios/IMP-0060-resize-responsivo-formacoes-popup-marcacao.md`
- `tela/renderizacao/popup.py`
- `tela/teste_popup.py`
- `demo/teste_demo_popup.py`
- `demo/fixtures/h0058_popup_lista_marcacao.py`
- `pytest.ini`

## Diff e escopo verificados

Foi executado o diff focal solicitado:

```text
git diff -- tela/renderizacao/popup.py tela/teste_popup.py demo/teste_demo_popup.py demo/fixtures/h0058_popup_lista_marcacao.py docs/relatorios/IMP-0060-resize-responsivo-formacoes-popup-marcacao.md
```

O diff mostrou alterações somente em `tela/renderizacao/popup.py`,
`tela/teste_popup.py` e `demo/teste_demo_popup.py`. A fixture H-0058 não
apresentou diff. O relatório IMP e os demais artefatos documentais aparecem
como arquivos não rastreados no `git status --short`; não foram atribuídos à
implementação H-0060 além do relatório IMP declarado.

Também foi executado `git status --short`. Os caches gerados pela execução da
suíte foram removidos antes da conclusão. Nenhum arquivo auditado foi alterado
pelo QA.

## Testes independentes

- `python -m pytest tela/teste_popup.py`: **61 passed**.
- `python -m pytest demo/teste_demo_popup.py`: **15 passed**.
- `python -m pytest`: **1173 passed**; `pytest.ini` confirmou `testpaths = tela demo`.
- `git diff --check`: **sem achados**.

## Conclusão dos requisitos críticos

A inspeção do código confirma, no escopo focal, a prioridade coluna → matriz
→ linha, a avaliação de candidatas pela quantidade real de colunas, o mínimo
de duas linhas para matriz, o preenchimento vertical sem placeholders, a
largura integral dos indicadores e texto, o overhead de instrução/chips, o
vão compartilhado de dois espaços, a preservação do estado vivo e a
navegação por eixo. Não foi introduzido fluxo paralelo de SIGWINCH no diff
focal.

Os testes independentes passam, mas a cobertura não comprova integralmente os
casos obrigatórios do handoff. Os achados abaixo impedem a aprovação.

## Achados

### QA-IMP-0060-001

- requisito violado: os testes devem comprovar `linha → matriz` no crescimento e `matriz → coluna` no crescimento.
- evidência focal: `tela/teste_popup.py:742-780` e `demo/teste_demo_popup.py:246-282` exercitam `coluna → matriz → linha → coluna`; não há recomposição partindo de `linha` para uma matriz válida, nem transição direta de uma matriz para coluna por crescimento.
- impacto: a reversibilidade completa exigida para resize não fica objetivamente demonstrada pelos testes, embora o algoritmo focal aparente suportar as transições.
- correção necessária: adicionar testes focais com dimensões de crescimento que afirmem `linha → matriz` e `matriz → coluna`, preservando identidade da instância, cursor e marcações.

### QA-IMP-0060-002

- requisito violado: quando nenhuma formação permitida cabe, os testes devem comprovar o comportamento vigente de geometria insuficiente/quadro mínimo de terminal pequeno, sem aceitar saída arbitrária.
- evidência focal: `demo/teste_demo_popup.py:220-233` usa `assert "terminal" not in pequeno.lower() or len(pequeno.splitlines()) == 5`, uma disjunção que passa sem demonstrar quadro mínimo, insuficiência geométrica, ausência de truncamento, paginação ou placeholders.
- impacto: uma regressão que devolva conteúdo inadequado ainda poderia satisfazer essa asserção; o caso obrigatório de terminal pequeno não possui evidência objetiva suficiente.
- correção necessária: afirmar o resultado concreto do fluxo vigente de terminal pequeno para dimensões sem formação válida e afirmar que os seis itens continuam sem truncamento, paginação, reticências ou placeholders.

### QA-IMP-0060-003

- requisito violado: os testes devem comprovar que wrapping da instrução e chips em múltiplas linhas reduzem efetivamente a altura disponível aos itens.
- evidência focal: `tela/teste_popup.py:628-652` apenas calcula `esperado` a partir do próprio `layout` retornado e compara `layout["altura"]`; não testa uma fronteira de formação/insuficiência nem materializa `renderizar_popup` para demonstrar o efeito da altura disponível.
- impacto: a asserção pode continuar passando mesmo se a seleção de formação deixar de usar corretamente o overhead para decidir quantas linhas físicas estão disponíveis.
- correção necessária: adicionar casos de fronteira que comparem dimensões com instrução/chips em uma linha e em múltiplas linhas, afirmando a formação ou a insuficiência resultante e a saída materializada.
