---
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTATION_BLOCKED
identificador: RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P20
achado: VM-H0045-R06-001
data: "2026-08-02"
---

# Relatório — Patch de Implementação H-0045 P20 (VM-H0045-R06-001)

## Causa localizada

`VM-H0045-R06-001` exige que o chip `[Esc]` exiba texto dinâmico ("Sair" ou
"Limpar") conforme haja ou não seleção ativa no console focado, no mesmo
espírito do rótulo dinâmico já existente para `[Enter]` ("Todos"/"Executar").

A busca autorizada (`rg` em `tela`, `demo`, `config/telas/demo`) localizou o
mecanismo que já implementa rótulo dinâmico de chip: o campo
`forma_exibicao`. Ele é interpretado em **um único ponto de todo o código**:

```
tela/renderizador.py:2337-2348
```

onde `forma_exibicao == "rotulo_dinamico_selecao"` substitui o `texto` do
chip `[Enter]` pelo valor calculado por `tela.selecao.rotulo_enter`. Não há
nenhuma outra interpretação de `forma_exibicao` em `demo/demo.py`,
`tela/navegacao.py`, `tela/loader.py` ou qualquer outro módulo (confirmado
por busca dedicada — `forma_exibicao` só aparece nesse trecho de
`renderizador.py` e nos comentários que o descrevem).

Os JSONs de fixture (`h0045_paginacao_console_unico.json`,
`h0045_dois_consoles_paginas_independentes.json`,
`h0044_fluxo_execucao_integrado.json`, `h0041_selecao_multipla_oito_itens.json`)
declaram o chip Esc com `"texto": "Sair"` estático e
`"forma_exibicao": "visivel_ativo"` — nunca dinâmico.

O tratamento funcional do primeiro `Esc` (limpar seleção sem sair) já está
correto e implementado em `demo/demo.py:459-479`: quando o console focado
declara seleção múltipla e a seleção reconciliada não está vazia, o primeiro
`Esc` chama `selecao.limpar` e retorna sem tocar `pilha_telas`/`saindo`; só
com seleção vazia o `Esc` segue o fluxo Sair/Voltar de H-0040. Ou seja, a
**ação** já é a correta — o defeito é exclusivamente a indicação **visual**
do chip, que nunca reflete essa alternância.

## Bloqueio

A única forma de corrigir o rótulo do chip sem duplicar a autoridade de
composição da barra em outra camada é estender o mesmo mecanismo de
`forma_exibicao` dentro de `tela/renderizador.py::_linhas_barra` (novo valor,
ex. `rotulo_dinamico_esc`, resolvido por uma função companheira de
`tela.selecao`, ex. `rotulo_esc(estado, console)` → `"Limpar"` quando há
seleção não vazia, `"Sair"` caso contrário), e materializar esse valor
exatamente como já ocorre para `[Enter]`.

`tela/renderizador.py` e `tela/teste_renderizador.py` estão fechados por este
handoff desde `PATCH_HANDOFF P05` (§6.2, §19.6): nenhuma nova alteração é
autorizada salvo autorização nominal específica e cumulativa (evidência nova,
relatório, autorização posterior do usuário/gerente). As únicas exceções já
concedidas são `VM-H0045-R07-001` (§20) e os cinco testes bloqueadores do P17
(§21) — nenhuma delas cobre o chip Esc. Pelo contrário, o próprio handoff
registra `VM-H0045-R06-001` três vezes (§19.7, §20.7, §21.7) como achado
"preservado fora deste patch" / "não resolvido".

Não há caminho alternativo dentro dos arquivos autorizados (`demo/demo.py`,
`tela/selecao.py`, `tela/fluxo_execucao.py`, testes correspondentes,
configurações JSON) capaz de produzir o rótulo dinâmico: `demo/demo.py` não
compõe a barra de menus — apenas repassa estado para `renderizar_estado`
(que delega inteiramente a `tela/renderizador.py`); e adicionar a lógica de
decisão de texto fora do renderer duplicaria, em outra camada, a autoridade
de composição de chips já centralizada ali (mesmo princípio anti-duplicação
já aplicado a paginação por D-TEC-04).

Conforme a instrução de escopo deste patch, a implementação para antes de
tocar em arquivo fora do escopo autorizado.

status: IMPLEMENTATION_BLOCKED
caminho: tela/renderizador.py (função `_linhas_barra`, mecanismo `forma_exibicao`, linhas ~2337-2348)
motivo: arquivo fechado pelo handoff vigente (§6.2, §19.6); nenhuma das duas exceções já concedidas (§20 VM-H0045-R07-001; §21 testes do P17) cobre VM-H0045-R06-001, que é explicitamente listado (§19.7, §20.7, §21.7) como não resolvido/não autorizado por nenhum patch anterior
mudanca_necessaria: nova seção de autorização nominal no handoff (análoga a §20/§21), autorizando `tela/renderizador.py`/`tela/teste_renderizador.py` restritos a: (1) novo valor de `forma_exibicao` para o chip Esc (ex. `rotulo_dinamico_esc`); (2) função companheira em `tela/selecao.py` (ex. `rotulo_esc`) que devolve "Limpar" com seleção não vazia e "Sair" caso contrário, reconciliada a partir do console focado; (3) atualização dos JSONs de fixture que declaram o chip Esc para o novo `forma_exibicao`; nenhuma outra função do renderer tocada

## Arquivos alterados

Nenhum. Nenhuma alteração de código foi aplicada — a implementação parou
antes de tocar `tela/renderizador.py`, o único arquivo onde a correção real
poderia ser feita.

## Testes

Não executados. Sem alteração de código, não há delta a validar; a suíte
completa permanece no estado herdado dos patches anteriores (P17/P18/P19),
já reportado verde nos relatórios correspondentes.

## `git diff --check`

Não aplicável — nenhuma alteração em arquivo de texto foi introduzida por
este patch.

## Próxima ação recomendada

Solicitar ao usuário/gerente uma seção de autorização nominal equivalente a
§20/§21 do handoff, cobrindo especificamente `VM-H0045-R06-001` e os dois
arquivos (`tela/renderizador.py`, `tela/teste_renderizador.py`) antes de
reabrir este patch.
