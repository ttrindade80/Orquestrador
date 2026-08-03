---
name: RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P18
descricao: "Correcao focal do bloqueio IMP-H0045-P17-001: cinco testes desatualizados pela largura corrigida do PATCH_IMPLEMENTACAO P17"
metadata:
  tipo: relatorio_patch_implementacao
  status: IMPLEMENTATION_PATCHED
  handoff: H-0045
  bloqueio_corrigido: IMP-H0045-P17-001
  data: "2026-08-02"
---

# RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P18

## 1. Escopo executado

Corrigido exclusivamente o bloqueio `IMP-H0045-P17-001` (§21 do handoff
H-0045), transportado por `RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P17.md`.
Nenhum código produtivo foi alterado; a correção de largura já aplicada por
P17 em `tela/renderizador.py`/`tela/teste_renderizador.py` foi preservada
sem reversão.

**Arquivos alterados (2, os únicos autorizados):**

- `demo/teste_demo_paginacao.py`
- `demo/teste_demo_navegacao.py`

## 2. Testes corrigidos (5, os únicos nominados em §21.3)

1. `test_demo_h0045_p10_fixture_real_verbosa_multilinha_paginada_sem_perdas`
   — total de páginas 3→2. Com a largura corrigida o item 1 (11 linhas)
   cabe inteiro na página 1; o item 2 (`evitar_quebra`) não aproveita o
   resíduo de 5 linhas e inicia a página 2. A prova de continuação real
   (`segmento_13`) foi realocada para a página 1 (onde o item agora está
   inteiro); ausência de perda, ordem e cursor/página reconciliados foram
   preservados. `mapa_fisico_de_itens` passou a ser recalculado após o laço
   de renders (efeito colateral pré-existente e independente deste patch:
   o valor calculado antes do laço diverge do estado físico produzido pelos
   renders).
2. `test_demo_h0045_p10_dimensao_menor_repagina_sem_perda_e_cursor_correto`
   — total 6→4; cursor final 2→3 (`curto_04` inicia a última página);
   retorno via `<` 5→3. Nenhuma outra asserção alterada.
3. `test_demo_h0045_p11_politicas_quebra_fixture_real_seis_paginas_sem_perdas`
   — total 6→2 (os quatro itens cabem em duas páginas nesta geometria).
   Corpo reescrito para provar, na nova distribuição: `evitar_quebra` não
   aproveita resíduo disponível (prova mais direta da política que a
   versão anterior); `permitir_quebra_somente_se_maior_que_pagina` aproveita
   resíduo quando cabe inteiro; ausência de perda/duplicação; cursor e
   página reconciliados nas duas páginas. A fragmentação de item entre
   páginas permanece provada pelo teste irmão (item 4 abaixo).
4. `test_demo_h0045_p11_politicas_quebra_dimensao_menor_deriva_da_politica`
   — total 11→4 (permanece o teste que prova fragmentação real entre
   páginas, incluindo página só de continuação); `evitar_quebra` 6→2 linhas;
   soma de fragmentos de `permitir_quebra` 31→11.
5. `teste_prova_mudanca_modo_nao_reinicia_item_zero` — o texto do item i3
   foi alongado (mantendo `Gamma`/`texto-longo`/`Iota`/`Kappa`) apenas para
   a renderização verbosa em memória, preservando `len(linhas_com_gamma)
   >= 2`. A verificação via CLI real (subprocess) usa uma cópia temporária
   da mesma tela (gerada em `tempfile.TemporaryDirectory`, nunca persistida
   no repositório) com o mesmo texto alongado para a chamada `--verboso`; a
   chamada não-verbosa continua usando a fixture original em disco,
   inalterada. Isso foi necessário porque, com a largura corrigida, o texto
   original passou a caber em uma única linha em ambos os modos também via
   CLI, tornando `p_nv.stdout != p_v.stdout` falso — falha adicional exposta
   pela mesma causa raiz de P17, dentro do mesmo teste nominado.

Nenhuma verificação semântica foi removida; onde a distribuição física
mudou substancialmente (testes 1 e 3), as asserções dependentes de página
foram reconstruídas mantendo as mesmas provas de ausência de perda,
ausência de duplicação, ordem, política de quebra e reconciliação de
cursor/página.

## 3. Resultados das suítes obrigatórias

```
tela/teste_renderizador.py + demo/teste_demo_paginacao.py + demo/teste_demo_navegacao.py
417 passed

+ tela/teste_paginacao.py
430 passed

suíte completa
856 passed
```

## 4. `git diff --check`

Executado sobre os quatro arquivos (`tela/renderizador.py`,
`tela/teste_renderizador.py`, `demo/teste_demo_paginacao.py`,
`demo/teste_demo_navegacao.py`): saída vazia, sem erros de espaço em
branco.

## 5. Bloqueios

Nenhum. `IMP-H0045-P17-001` está corrigido; suíte completa verde.
`VM-H0045-R06-001` e `QA-H0045-P08-001` permanecem não resolvidos.
`VM-H0045-R07-001` permanece pendente de QA pós-patch e validação manual
focal (`python demo/demo.py h0045_validacao_continuacao`), fora do escopo
desta execução.
