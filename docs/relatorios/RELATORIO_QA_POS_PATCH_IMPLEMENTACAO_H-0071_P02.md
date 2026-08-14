# RELATÓRIO QA PÓS-PATCH IMPLEMENTAÇÃO H-0071 P02

```yaml
item: ITEM-0010
adr: ADR-0046
handoff: H-0071
patch: P02
status: I3_HANDOFF_PATCH_REQUIRED
cadeia.raiz: docs/relatorios/IMP-0071-correcao-chips-multitecla-barra-menus-estilo.md
cadeia.predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0071_P02.md
```

## 1. Resultado das reexecuções

- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tela/teste_renderizador.py`: **371 passed**.
- `PYTHONDONTWRITEBYTECODE=1 python tela/teste_renderizador.py`: código **1**; 1308 verificações, 1306 passaram e falharam somente as duas inspeções abaixo.
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q demo/teste_diagnostico.py`: **6 passed, 1 error**.
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q --tb=short`: **1370 passed, 1 error**.

## 2. Caminho de `fundamentos.py`

`find tela -type f -name 'fundamentos.py' -print` retornou exatamente:
`tela/testes_renderizador/fundamentos.py`.

## 3. INSPECAO-01 — `estilo.cor_texto`

**Classificação: `TESTE_FONTE_DESATUALIZADO_PELO_H0071`.**

A inspeção está em `tela/testes_renderizador/fundamentos.py:966-973` e exige a
literal `estilo.cor_texto` no texto de `tela/renderizacao/barra_menus.py`.
Ela não encontra essa forma literal. O trecho real é
`_texto_chip_barra`, em `barra_menus.py:123-160`, que chama
`compor_chip_multitecla([tecla], estilo, ...)`.

O acesso semântico ocorre no mecanismo autorizado e compartilhado
`tela/renderizacao/estilo.py::_conteudo_chip`: `cor_texto` é lido via
`_valor_estilo` (`:85`) e convertido em ANSI (`:97`), tanto para a Barra
real quanto para `amostra_chip`. Isso implementa diretamente os requisitos
H-0071 de consumo do estilo global, composição única e ausência de mecanismo
visual paralelo. Não há alternativa autorizada mais adequada: a delegação
ao compositor compartilhado é a forma vigente necessária.

A invariável histórica protegida é válida: o renderer deve consumir a cor de
texto do estilo, e não hardcodar uma cor. Porém, a inspeção verifica apenas a
forma antiga de implementação (acesso direto na Barra), não o comportamento
nem a delegação vigente.

## 4. INSPECAO-02 — `estilo.cor_fundo`

**Classificação: `TESTE_FONTE_DESATUALIZADO_PELO_H0071`.**

A inspeção está em `fundamentos.py:975-980` e repete a busca literal
`estilo.cor_fundo` em `barra_menus.py`; essa literal também não existe. O
trecho de produção é o mesmo `_texto_chip_barra`, que delega ao compositor.

Em `estilo.py::_conteudo_chip`, `cor_fundo` é lido em `:86`, convertido em
fundo ANSI em `:98-99`, com fallback para os campos assimétricos e resets
contidos em `:123-142`. Isso materializa diretamente H-0071: fundo dentro da
unidade visual, sem vazamento, incluindo `cor_fundo_esquerdo` e
`cor_fundo_direito`. A inspeção continua protegendo a intenção arquitetural
de consumo do fundo global, mas analisa somente uma forma antiga e paralela,
superada pela composição compartilhada exigida pelo H-0071.

## 5. Diferença entre pytest e runner direto

`tela/teste_renderizador.py` importa `main` do runner e, no bloco direto
(`:300-301`), executa `sys.exit(main())`. Assim, `python tela/teste_renderizador.py`
executa o conjunto de gates internos do runner, incluindo
`teste_inspecao_fonte_hardcoded`, além dos testes funcionais. A coleta
`pytest tela/teste_renderizador.py` não chama esse `main()`; por isso retorna
371 passed e não reproduz essas duas inspeções como gates do runner direto.

## 6. Camada responsável e situação do diagnóstico

O resíduo pertence à camada de teste estrutural em
`tela/testes_renderizador/fundamentos.py`, arquivo não autorizado pelo
H-0071. Não há defeito de produção demonstrado e não se deve alterar
`demo/teste_diagnostico.py`. Seu erro de teardown em
`teste_invariantes_anteriores` é derivado exclusivamente do código 1 do
runner direto; não é uma falha independente do diagnóstico.

## 7. Conclusão e bloqueios

As duas inspeções devem ser adaptadas em camada posterior para reconhecer o
compositor compartilhado e preservar a invariável comportamental, sem
reintroduzir acessos diretos ou mecanismo paralelo na Barra. Portanto, o
P02 não pode ser aprovado como `I1`: requer atualização de handoff para
autorizar essa adaptação em `fundamentos.py`.

Bloqueio: inspeções de fonte desatualizadas em arquivo fora do escopo
autorizado; a suíte canônica permanece não-zero pelo erro derivado.
