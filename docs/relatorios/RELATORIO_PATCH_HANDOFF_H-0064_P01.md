---
name: REL-PATCH-H0064-P01-barra-payload-chip-e-composicao-uma-linha
description: "Delta factual do patch P01 sobre o handoff H-0064: fecha a Barra de Menus herdada com paginação, define o payload canônico Ab/AB da amostra de chip e substitui a miniatura de borda de três linhas e a estratégia de composição por um modelo de item lógico único em uma linha física"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_HANDOFF
  status: HANDOFF_PATCHED
  data: "2026-08-12"
---

# RELATORIO_PATCH_HANDOFF_H-0064_P01

```yaml
rastreabilidade:
  etapa: PATCH_HANDOFF
  objeto: H-0064
  patch: P01
  predecessor:
    docs/relatorios/RELATORIO_QA_HANDOFF_H-0064.md

resultado:
  status: HANDOFF_PATCHED
  achados_tratados:
    - H0064-QA-001
    - H0064-QA-002
    - H0064-QA-003
  achados_pendentes: []
  arquivos_alterados:
    - docs/handoff/H-0064-amostras-visuais-presets-estilo.md
  arquivos_criados:
    - docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0064_P01.md
  decisoes:
    barra: >-
      §13 reescrita para declarar explicitamente que H-0064 não altera a
      Barra de Menus e preserva literalmente a barra herdada de H-0063,
      incluindo o chip chip_paginas ([PgUp][PgDn] Páginas) quando
      politica_paginacao: com. A ordem exibida passa a citar a sequência
      canônica de contrato_barra_de_menus.md §7 (Esc → PgUp/PgDn → ... → ✥
      → ␣ → ... → ?), fechando a contradição entre a sequência literal
      antiga (só Esc/✥/␣/?) e a fixture h0063, que já declara paginação.
      Nenhum chip novo, reordenação nova ou política global nova foi
      introduzida; ITEM-0032 permanece fora de escopo.
    chip_payload: >-
      §7 reescrita definindo a amostra de chip como três partes
      (caractere_esquerdo + payload_canônico + caractere_direito), com
      payload_canônico fixado literalmente como "Ab" — mesmo texto para
      todos os presets, sem mapa por nome e sem if/switch sobre o preset.
      Nova §7.1 fecha a aplicação de cor_texto/cor_fundo sobre o payload
      Ab/AB e exige reset ANSI antes do restante da linha, reutilizando os
      helpers normais existentes (tela/renderizacao/texto_ansi.py) sem
      novo protocolo ANSI.
    borda: >-
      §6 substitui a preferência por miniatura de três linhas (incompatível
      com o modo não verboso de H-0063) por uma amostra compacta de borda em
      uma linha, definida pela concatenação canto_superior_esquerdo +
      traco_superior + canto_superior_direito + lateral + lateral +
      canto_inferior_esquerdo + traco_inferior + canto_inferior_direito (ou
      equivalente documentalmente explícito), preservando os sete campos
      concretos sem escolha por nome de preset.
    renderer: >-
      Nova §12 fecha a estratégia de composição (H0064-QA-003): cada filho
      permanece um único nó lógico em uma única linha física, sem extensão
      multiline do Console, sem renderer paralelo e sem novo modo de item
      lógico; nome + separador canônico + amostra (§10, reescrita) compõem
      um único texto no mesmo nó já usado por H-0063. §15 foi reduzida à
      lista mínima justificada (tela/estilo.py, tela/renderizacao/estilo.py,
      fixture JSON h0063, testes/demo dedicados a H-0064, IMP-0064);
      tela/renderizador.py e tela/renderizacao/contexto_execucao.py saíram
      da lista de autorização por ausência de necessidade material sob o
      modelo de uma linha, passando a constar como infraestrutura
      consumida sem alteração, junto de conteudo_externo.py.
  verificacoes_executadas:
    - "leitura integral de H-0064 e do RELATORIO_QA_HANDOFF_H-0064.md"
    - "leitura focal de H-0063, da fixture h0063_estilo_estrutura_navegacao_dois_niveis.json, de contrato_console.md (itens/composição/dois_niveis_por_foco/paginação), contrato_barra_de_menus.md (ordem canônica §7, PgUp/PgDn §24) e contrato_estilo.md/10_ESTILO.md (schema de chip e borda)"
    - "confirmação de que tela/renderizacao/texto_ansi.py já existe como helper de largura visual ANSI, reutilizável sem novo protocolo"
    - "grep de 'miniatura'/'três linhas' no handoff corrigido: somente ocorrências explicativas da mudança permanecem"
    - "conferência de numeração de seções (## 1 a ## 20) preservada após as edições"
    - "git diff --check sobre os dois arquivos tocados: sem problemas de espaço em branco"
  bloqueios: []
```

## Síntese do delta

Os três achados do QA (`H0064-QA-001`, `H0064-QA-002`, `H0064-QA-003`) foram
tratados exclusivamente no corpo do handoff `H-0064`, sem tocar código, ADR,
contratos, nomenclatura, backlog ou configuração, e sem criar H-0065.

**H0064-QA-001 (Barra de Menus)** — a antiga §13 listava apenas `[Esc]`,
`[✥]`, `[␣]` e `[?]`, contradizendo a fixture de H-0063, que já declara
`politica_paginacao: com` e o chip `chip_paginas`. A nova §13 fecha essa
contradição declarando explicitamente que a Barra herdada inclui
`[PgUp][PgDn] Páginas` na posição canônica quando aplicável, sem introduzir
nenhuma novidade de chip, ordem ou política.

**H0064-QA-002 (payload de chip)** — a antiga §7 exigia os cinco campos do
chip sem definir sobre qual conteúdo textual `cor_texto`, `cor_fundo` e
`caixa_alta` atuariam, deixando em aberto o risco de hardcode por preset ou
de amostras indistinguíveis. A nova §7 fixa o payload canônico `Ab`,
igual para todos os presets, com transformação observável por `caixa_alta`
(`Ab`/`AB`), e a nova §7.1 fecha a aplicação de cor e o reset ANSI usando os
helpers já existentes.

**H0064-QA-003 (composição)** — a antiga §6 exigia miniatura de três linhas
e as antigas §§12/15 autorizavam ajustes difusos em `tela/renderizador.py` e
`tela/renderizacao/contexto_execucao.py` sem fechar se a amostra caberia no
modo não verboso de item único por linha. A correção fixa a decisão de um
único nó lógico por linha física (nova §12), reduz a borda a uma amostra de
uma linha (§6 reescrita), reformula `nome + amostra` como uma composição de
linha única com separador canônico (§10 reescrita) e reduz a lista de
arquivos autorizados (§15 reescrita) ao mínimo necessário sob esse modelo.

Os critérios de aceite (§16) e os testes mínimos (§17) foram revisados para
refletir as três correções, incluindo os seis critérios objetivos exigidos
para a amostra de chip (diferença ANSI por `cor_texto`, diferença ANSI por
`cor_fundo`, payload `Ab`/`AB` por `caixa_alta`, ausência de vazamento de
reset e largura visual sem contar códigos ANSI).

Nenhum achado ficou pendente. `git diff --check` foi executado sobre os dois
arquivos tocados nesta etapa e não indicou problema. Nenhum stage, commit ou
push foi realizado.
