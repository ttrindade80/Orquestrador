---
name: RELATORIO_PATCH_HANDOFF_H-0045_P08
description: "Autoriza focalmente a atualização de cinco testes (demo/teste_demo_paginacao.py e demo/teste_demo_navegacao.py) desatualizados pela correção de largura horizontal aplicada pelo PATCH_IMPLEMENTACAO P17, mantendo o P17 IMPLEMENTATION_BLOCKED até essa correção"
metadata:
  type: relatorio_patch_handoff
  status: HANDOFF_PATCHED
  id: H-0045-P08
  data_criacao: "2026-08-02"
---

# Relatório — Patch de Handoff H-0045 P08

## Arquivo alterado

- `docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md` — nova
  seção 21 ("Autorização focal dos testes bloqueadores do P17") e nota de
  cruzamento em §6.2. Nenhum outro arquivo foi alterado.

## Bloqueio tratado

`IMP-H0045-P17-001` — o `PATCH_IMPLEMENTACAO P17` corrigiu
`VM-H0045-R07-001` (largura horizontal) em `tela/renderizador.py` e
`tela/teste_renderizador.py` (escopo já autorizado por §20), o que
legitimamente reduziu linhas físicas por item e número de páginas em
cenários já cobertos por teste. Cinco asserções ficaram desatualizadas em
dois arquivos fora do escopo autorizado do P17, e o patch foi reportado
`IMPLEMENTATION_BLOCKED`.

## Arquivos e testes autorizados

Adicionalmente aos já autorizados por §20, a nova §21 autoriza,
exclusivamente:

- `demo/teste_demo_paginacao.py` — quatro testes:
  `test_demo_h0045_p10_fixture_real_verbosa_multilinha_paginada_sem_perdas`
  (3→2), `test_demo_h0045_p10_dimensao_menor_repagina_sem_perda_e_cursor_correto`
  (6→4), `test_demo_h0045_p11_politicas_quebra_fixture_real_seis_paginas_sem_perdas`
  (6→2), `test_demo_h0045_p11_politicas_quebra_dimensao_menor_deriva_da_politica`
  (11→4);
- `demo/teste_demo_navegacao.py` — um teste:
  `teste_prova_mudanca_modo_nao_reinicia_item_zero`.

Nenhuma alteração de código produtivo adicional é autorizada
(`tela/paginacao.py`, `demo/demo.py`,
`demo/casos_validacao_paginacao.py`, configurações JSON, contratos, ADR,
nomenclatura, ou qualquer outro arquivo de código/teste permanecem fora de
escopo).

## Preservação da intenção dos testes

A §21 exige que a correção atualize apenas as expectativas numéricas
incompatíveis com a largura corrigida (e as asserções dependentes da
distribuição de fragmentos, quando necessário), preservando integralmente
a prova de ausência de perda, ausência de repetição, ordem dos itens,
política de quebra, cursor/página reconciliados e repaginação conforme a
geometria. Para `teste_prova_mudanca_modo_nao_reinicia_item_zero`, a
correção preferida é alongar o texto de teste para continuar produzindo
duas ou mais linhas físicas na largura corrigida; é expressamente proibido
enfraquecer `len(linhas_com_gamma) >= 2` para aceitar uma única linha.

## Suítes futuras exigidas

Registrados em §21.5: suíte focal (`tela/teste_renderizador.py` +
`demo/teste_demo_paginacao.py` + `demo/teste_demo_navegacao.py`), suíte
focal ampliada (incluindo `tela/teste_paginacao.py`), suíte completa
(`python -m pytest -q`) e `git diff --check` sobre os quatro arquivos
envolvidos no delta (renderer + os dois testes bloqueadores).

## Verificações

Confirmado que a §21 nova: registra `IMP-H0045-P17-001`; autoriza
nominalmente somente os dois arquivos bloqueadores, adicionalmente a §20;
limita a alteração aos cinco testes identificados; preserva o sentido
semântico deles; não autoriza código produtivo adicional; determina que o
próximo `PATCH_IMPLEMENTACAO` continue sobre o delta já aplicado por P17
sem reverter `tela/renderizador.py`; exige suíte completa verde antes de
QA; mantém a validação manual focal (`python demo/demo.py
h0045_validacao_continuacao`) pendente ao usuário, sem reabrir validações
anteriores (§12, §19.5, §20.6); preserva `VM-H0045-R06-001` e
`QA-H0045-P08-001` como abertos.

`git diff --check -- docs/handoff/H-0045-paginacao-interativa-limitada-em-console.md`
— sem problemas de espaço em branco.

## Bloqueios

Nenhum.

## Limite respeitado

Não foi executado QA, validação manual, stage ou commit. Nenhum código,
teste, configuração, contrato ou ADR foi alterado — apenas o handoff.
