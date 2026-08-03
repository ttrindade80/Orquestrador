---
name: RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P17
description: "Correcao focal de VM-H0045-R07-001 (largura horizontal do ramo matricial verboso) em tela/renderizador.py, com cobertura nova em tela/teste_renderizador.py; bloqueio reportado para dois arquivos fora do escopo autorizado cujas asserções ficaram desatualizadas pela correção"
metadata:
  type: relatorio_patch_implementacao
  status: IMPLEMENTATION_BLOCKED
  id: H-0045-P17
  data_criacao: "2026-08-02"
---

# Relatório — Patch de Implementação H-0045 P17

## Arquivos alterados

- `tela/renderizador.py` — `_linhas_distribuicao_matricial` e
  `_larguras_mapa_fisico_matricial`.
- `tela/teste_renderizador.py` — 5 novos testes (`test_h0045_ph07_*`) e ajuste
  de 1 assertiva pré-existente (`test_h0045_p10_...`, valor de página fixo
  substituído por valor derivado do plano recalculado).

Nenhum outro arquivo foi alterado.

## Causa corrigida

Confirmada a causa apontada pelo handoff (§20.1): no ramo verboso da grade
matricial, o requisito mínimo de largura de texto (`texto_min`) era limitado
a um teto fixo de aproximadamente metade da área útil, mesmo quando a
formação declarada permite no máximo **uma** célula por linha (`colunas:
{minimo: 1, maximo: 1}` — padrão de todos os consoles paginados H-0045). Como
o motor de distribuição (`calcular_distribuicao`, política `uniforme`) atribui
à célula exatamente o mínimo requisitado — sem esticar para preencher espaço
sobrando —, esse teto se tornava a largura final exibida, desperdiçando
metade da área.

**Cálculo anterior:** `teto = (area_w - ind_w) // 2`, aplicado
incondicionalmente, em ambas as funções.

**Cálculo vigente:** quando a formação declarada limita a no máximo uma
célula por linha (`formacao.colunas.fixo`/`maximo <= 1`), `teto = area_w -
ind_w - margem_esq - margem_dir` (toda a largura útil real); caso contrário,
o teto histórico (`// 2`) é preservado sem alteração. A detecção usa apenas
`elemento.distribuicao_matricial["formacao"]["colunas"]`, já disponível nas
duas funções — nenhum novo acoplamento externo.

## Medições (tela `h0045_paginacao_modo_verboso_multilinha`, coluna única)

| Largura ext. | Área interna útil | Largura textual atribuída | Maior linha física | Resíduo até margem direita |
|---|---|---|---|---|
| 80  | 77  | 75  | 76  | 2 (margens) |
| 120 | 117 | 115 | 115 | 2 (margens) |
| 160 | 157 | 155 | 155 | 2 (margens) |
| 200 | 197 | 195 | 194 | 2 (margens) |

O resíduo (2) corresponde exatamente à margem esquerda + direita declaradas
(1+1) — nenhum desconto além dos estruturais reais (indicador já incluso na
largura da célula). A "maior linha física" cresce monotonicamente com a
largura e ultrapassa a metade da área útil em todos os casos (76 > 38, 194 >
98 etc.), provando a remoção do teto.

## Coerência renderer / mapa físico

Teste `test_h0045_ph07_coerencia_renderer_mapa_fisico` instrumenta
`calcular_distribuicao` (monkeypatch) durante uma chamada real de
`renderizar_tela` e compara a largura de célula capturada com o valor
independente de `_larguras_mapa_fisico_matricial`, nas quatro larguras: **75,
115, 155, 195 em ambos os lados**, igualdade exata.

## Regressões executadas

1. `tela/teste_renderizador.py` — **349 passed** (344 pré-existentes + 5
   novos), inclui regressão H-0037 (`teste_h0037_qapp7_verb_sem_corte_
   silencioso`, reexecutada via wrapper pytest) e as cinco telas exigidas.
2. `tela/teste_paginacao.py` — **13 passed**.
3. `python -m pytest -q` (suíte completa) — **851 passed, 5 failed**.
4. `git diff --check -- tela/renderizador.py tela/teste_renderizador.py` —
   sem problemas de espaço em branco.

## Desvio confirmado por reversão controlada

As 5 falhas da suíte completa foram isoladas por reversão temporária e
reaplicação dos dois trechos corrigidos: com a fórmula antiga, os 5 testes
passam; com a fórmula corrigida, falham. Confirma-se que são consequência
direta e esperada da correção (texto que antes precisava de 2+ linhas físicas
agora cabe em menos linhas, reduzindo `total_paginas`), não regressão nova.

## Bloqueio

status: IMPLEMENTATION_BLOCKED

caminho: `demo/teste_demo_paginacao.py`, `demo/teste_demo_navegacao.py`

motivo: ambos os arquivos contêm asserções numéricas fixas (`total_paginas ==
3/6/11`, contagem de linhas físicas `>= 2`) calibradas contra o cálculo
antigo, incorreto, de largura (teto de metade da área). A correção deste
patch — autorizada e restrita a `tela/renderizador.py`/`tela/teste_
renderizador.py` pela §20 do handoff — altera legitimamente esses valores
físicos (menos linhas por item, menos páginas), tornando as asserções
desatualizadas. Nenhum dos dois arquivos está na lista de arquivos permitidos
deste patch (`tela/renderizador.py`, `tela/teste_renderizador.py`), portanto
a correção das asserções não pode ser aplicada por este ciclo.

mudanca_necessaria:
- `demo/teste_demo_paginacao.py`: atualizar os valores esperados de
  `plano["total_paginas"]` em 4 testes (`test_demo_h0045_p10_fixture_real_
  verbosa_multilinha_paginada_sem_perdas`: 3→2;
  `test_demo_h0045_p10_dimensao_menor_repagina_sem_perda_e_cursor_correto`:
  6→4; `test_demo_h0045_p11_politicas_quebra_fixture_real_seis_paginas_sem_
  perdas`: 6→2; `test_demo_h0045_p11_politicas_quebra_dimensao_menor_deriva_
  da_politica`: 11→4) e quaisquer asserções dependentes desses totais
  (distribuição de fragmentos por página, se houver).
- `demo/teste_demo_navegacao.py`: em
  `teste_prova_mudanca_modo_nao_reinicia_item_zero`, o item verboso
  "Gamma..." agora cabe em 1 linha física na largura do cenário (antes exigia
  2+); a asserção `len(linhas_com_gamma) >= 2` precisa de um cenário com
  texto suficientemente mais longo, ou de expectativa ajustada, para
  continuar provando continuação real em modo verboso.

Nenhuma dessas alterações foi aplicada — ambos os arquivos permanecem
intocados, conforme escopo autorizado.

## Limite respeitado

Não foi executado QA, validação manual, stage ou commit. Não foi alterada
documentação normativa. Nenhum arquivo fora de `tela/renderizador.py` e
`tela/teste_renderizador.py` foi modificado.
