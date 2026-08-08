---
name: IMP-0051-paginacao-universal-pageup-pagedown
description: "Migra a paginação interativa de ,/</./> para PageUp/PageDown e para a notação [PgUp][PgDn] Páginas"
metadata:
  type: relatorio_implementacao
  tipo_execucao: IMPLEMENTACAO
  status: IMPLEMENTED
  handoff_origem: H-0051
  data: "2026-08-07"
rastreabilidade:
  contrato_alvo:
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_chip.md
  adr_relacionadas:
    - docs/adr/ADR-0041-paginacao-universal-por-pageup-e-pagedown.md
    - docs/adr/ADR-0038-paginacao-interativa-limitada-em-console.md
  issues_relacionadas:
    - ITEM-0003
  bugs_abertos: []
  autorizacoes_operacionais: []
  cadeia_raiz: null
  predecessor_imediato: null
  achados_tratados:
    - H-0051-A
    - H-0051-B
---

# IMP-0051 — Relatório de implementação

## 1. Identificação e status

```yaml
handoff: H-0051 — Implementar paginação universal por PageUp/PageDown
tipo_execucao: IMPLEMENTACAO
status_literal: IMPLEMENTED
status_normalizado: IMPLEMENTED
```

## 2. Delta material

- Paginação migrada de `,`/`<`/`.`/`>` para `PageUp`/`PageDown`
  (`\x1b[5~`/`\x1b[6~`); os quatro caracteres antigos não acionam mais
  paginação, sem alias, atalho ou fallback residual.
- `chip_pagina_anterior` (`PgUp`, texto vazio) e `chip_pagina_proxima`
  (`PgDn`, texto `Páginas`) passam a ser apresentados, quando ambos
  renderizados, como bloco visual contíguo `[PgUp][PgDn] Páginas` — sem
  separador e com o rótulo `Páginas` uma única vez. Cada chip permanece um
  controle lógico independente (id, `regra_existencia`, `regra_ativo`
  próprios, avaliados separadamente).
- Consequência necessária: o grupo conta como uma única unidade na
  distribuição em múltiplas linhas da barra (não pode ser dividido entre
  linhas, sob pena de quebrar a contiguidade exigida). Isso reduz de 5 para 4
  as unidades de `h0045_fluxo_execucao_paginado`, tornando o arranjo de 5
  linhas daquele cenário inalcançável (o `linhas.maximo: 5` do JSON permanece
  válido; nenhuma largura o exercita mais nesta fixture). Testes de layout
  recalibrados para os novos valores reais.

## 3. Artefatos criados ou alterados

```yaml
arquivos_criados:
  - caminho: docs/relatorios/IMP-0051-paginacao-universal-pageup-pagedown.md
    finalidade: Relatório desta implementação.
arquivos_alterados:
  - caminho: demo/demo.py
    delta: >-
      Troca ","/"<"/"."/">" por TECLA_PAGE_UP ("\x1b[5~")/TECLA_PAGE_DOWN
      ("\x1b[6~") no laço de comandos; atualiza comentário histórico correlato.
  - caminho: tela/renderizacao/barra_menus.py
    delta: >-
      Tratamento focal em `_linhas_barra`: quando `chip_pagina_anterior` é
      imediatamente seguido de `chip_pagina_proxima`, os dois são renderizados
      como uma única unidade contígua ("[PgUp]" sem padding + "[PgDn]
      Páginas"), preservando `estado_ativo_chips` por id. Sem mecanismo
      genérico novo; nenhum outro chip afetado.
  - caminho: "config/telas/demo/h0045_*.json (11 fixtures, ver lista no handoff §6.2)"
    delta: >-
      chip_pagina_anterior: tecla "<"→"PgUp", texto "Anterior"→"";
      chip_pagina_proxima: tecla ">"→"PgDn", texto "Proxima"→"Páginas".
      Mesma alteração nas 11 fixtures.
  - caminho: demo/teste_demo_paginacao.py
    delta: >-
      Migra comandos/bytes de ","/"<"/"."/">" para TECLA_PAGE_UP/
      TECLA_PAGE_DOWN e sequências TTY reais ("\x1b[5~"/"\x1b[6~"); literais
      esperados atualizados para "[PgUp][PgDn] Páginas"; adiciona helper
      `_sem_ansi`. Preserva intacto o único teste que verifica que os quatro
      caracteres antigos NÃO produzem efeito de paginação.
  - caminho: demo/teste_demo_navegacao.py
    delta: Troca ","/"<"/"."/">" por TECLA_PAGE_UP/TECLA_PAGE_DOWN no teste de geometria inválida (P23).
  - caminho: tela/testes_renderizador/integracao.py
    delta: >-
      Atualiza literais "[<]"/"[>]" para "[PgUp]"/"[PgDn]"; corrige uso de
      "." como avanço funcional para TECLA_PAGE_DOWN (evitava loop sem efeito).
  - caminho: tela/testes_renderizador/barra_menus.py
    delta: >-
      Atualiza literais de chip para a notação canônica; recalibra limiares
      de largura do teste de 1 a 5 linhas (P23) para os novos pesos textuais
      do grupo de paginação unificado.
  - caminho: tela/testes_renderizador/fundamentos.py
    delta: Atualiza literal negativo de ausência de chip para "[PgUp][PgDn] Páginas".
```

## 5. Verificações e evidência

```yaml
verificacoes_executadas:
  - comando_ou_metodo: >-
      pytest demo/teste_demo_paginacao.py demo/teste_demo_navegacao.py
      tela/testes_renderizador/{integracao,barra_menus,fundamentos}.py
    resultado_compacto: "268 passed"
    prova_semantica: >-
      PageUp recua, PageDown avança, bordas sem wrap, página 1/1 com ambos
      controles inativos, ","/"<"/"."/">" sem efeito, "[PgUp][PgDn] Páginas"
      literal, estados independentes por chip, sem regressão nos demais chips.
  - comando_ou_metodo: "pytest (suíte completa)"
    resultado_compacto: "1037 passed"
    prova_semantica: Sem regressão em todo o repositório.
  - comando_ou_metodo: "python tela/teste_renderizador.py (runner histórico)"
    resultado_compacto: "1308 verificações, 0 falharam"
    prova_semantica: Cobertura ampla do renderer (H-0010A a H-0045) sem regressão.
  - comando_ou_metodo: "python demo/demo.py h0045_paginacao_console_unico (pipe)"
    resultado_compacto: "'[PgUp][PgDn] Páginas' e 'página 1/3' no quadro"
    prova_semantica: Ponto de entrada real produz a notação canônica.
criterios_de_aceite:
  - id: "PageUp recua / PageDown avança"
    evidencia: "test_demo_h0045_p01_cadeia_tty_quatro_caracteres_e_chips_pagina_1"
    resultado: OK
  - id: "<,>,,. sem efeito de paginação"
    evidencia: "test_demo_h0045_p11_conjunto_vazio_zero_itens_pagina_unica_chips_inativos_e_resize (loop intacto com os 4 caracteres antigos)"
    resultado: OK
  - id: "página 1/1 com ambos controles inativos"
    evidencia: "test_demo_h0045_p01_chips_visiveis_sem_foco_ambos_inativos"
    resultado: OK
  - id: "[PgUp][PgDn] Páginas contíguo, sem separador, Páginas uma única vez"
    evidencia: "test_h0045_p01_chips_pagina_visiveis_na_pagina_1_com_anterior_inativo, test_barra_preserva_ordem_e_chips_em_multilinha"
    resultado: OK
  - id: "estados ativo/inativo independentes por chip"
    evidencia: "estado_ativo_chips com chip_pagina_anterior/chip_pagina_proxima avaliados separadamente em todos os cenários testados"
    resultado: OK
  - id: "setas internas não atravessam página; demais chips sem regressão"
    evidencia: "suíte canônica completa (268 testes) e suíte total (1037 testes)"
    resultado: OK
```

## 6. Demonstração operacional

```yaml
cwd: "."
comando: "python demo/demo.py h0045_paginacao_console_unico (modo pipe, não-TTY)"
entrada_ou_fixture: config/telas/demo/h0045_paginacao_console_unico.json
saida_observada: >-
  "[Esc] Sair  [PgUp][PgDn] Páginas  [✥] Navegar" e "página 1/3" no quadro
  renderizado (códigos ANSI de cor inativa presentes em torno de [PgUp]).
comparacao_com_esperado: Conforme a notação canônica exigida pelo handoff.
prova_semantica: Confirma o caminho real de entrada, fora do runner de testes.
codigo_de_saida: 0
```

## 8. Estado Git observado

```yaml
branch: master
HEAD: 93b24a2
staged: []
unstaged: >-
  demo/demo.py; demo/teste_demo_paginacao.py; demo/teste_demo_navegacao.py;
  tela/renderizacao/barra_menus.py; tela/testes_renderizador/barra_menus.py;
  tela/testes_renderizador/integracao.py; tela/testes_renderizador/fundamentos.py;
  11 fixtures config/telas/demo/h0045_*.json
nao_rastreados: docs/relatorios/IMP-0051-paginacao-universal-pageup-pagedown.md (este relatório)
divergencias_materiais: []
```

`git diff --check` não reportou problemas de espaço em branco. Documentos
pré-existentes no worktree (ADR-0041, contratos, nomenclatura, backlog,
demais relatórios) foram preservados sem alteração — não fazem parte do
escopo desta implementação.

## 9. Bloqueios, ressalvas e observações para QA

```yaml
bloqueios: []
ressalvas:
  - >-
    O agrupamento contíguo reduz de 5 para 4 as unidades de
    `h0045_fluxo_execucao_paginado`; `linhas.maximo: 5` permanece válido no
    JSON, mas nenhuma largura o exercita mais com esta fixture — consequência
    direta de D-PGU-01 a D-PGU-03, não uma escolha do implementador.
observacoes_para_qa:
  - >-
    Verificar especificamente os critérios 7.1 a 7.6 do handoff usando
    `test_h0045_p01_chips_pagina_visiveis_na_pagina_1_com_anterior_inativo`
    e `test_barra_grupo_paginacao_reduz_arranjo_maximo_pratico_para_quatro`
    (tela/testes_renderizador/barra_menus.py).
validacao_manual:
  executor_exclusivo_quando_TTY: USUARIO
  necessaria: true
  executada: false
  resultado: PENDENTE_USUARIO
  itens_pendentes:
    - Roteiro manual do §8 do handoff (python demo/demo.py h0045_paginacao_console_unico em TTY real).
```
