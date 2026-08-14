# IMP-0064 — Amostras visuais dos presets na tela de Estilo

```yaml
rastreabilidade:
  etapa: IMPLEMENTAR
  objeto: H-0064
  artefato_principal:
    docs/handoff/H-0064-amostras-visuais-presets-estilo.md
  predecessor: H-0063
  item: ITEM-0010
  adr: ADR-0046

execucao:
  status: IMPLEMENTED
  arquivos_criados:
    - tela/teste_estilo_h0064.py
    - demo/teste_demo_estilo_h0064.py
    - docs/relatorios/IMP-0064-amostras-visuais-presets-estilo.md
  arquivos_alterados:
    - tela/estilo.py
    - tela/renderizacao/estilo.py
  arquivos_removidos: []
  fixture_compartilhada:
    - config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json
  ajuste_fixture: nenhum
```

## Resultado

### fatos_materiais

- A tela normal H-0063 permanece; H-0064 acrescenta amostras visuais em
  cada filho do segundo nível (`borda`, `chip`, `indicadores.selecionado`,
  `indicadores.incluido`).
- Cada filho compõe uma única linha lógica:
  `<nome do preset> + separador canônico ("  ") + <amostra>`.
- Amostra de borda: concatenação compacta dos sete campos do preset em uma
  linha (sem miniatura de três linhas).
- Amostra de chip: `caractere_esquerdo` + payload canônico `Ab`/`AB` +
  `caractere_direito`, com `cor_texto`/`cor_fundo` via helpers ANSI existentes
  (`_codigo_ansi_de_cor` + derivação FG→BG) e reset antes do restante da linha.
- Amostra de selecionado: `simbolo` do preset; incluído: par `on`/`off`
  simultâneo (`on/off`).
- Filhos e amostras continuam derivados dinamicamente de `presets` /
  `PresetEstilo.dados` — sem enumeração hardcoded nem catálogo paralelo.
- Barra de Menus herdada intacta (`politica_paginacao: com`, chip Páginas).
- Navegação (`dois_niveis_por_foco`, Espaço, Esc, resize, paginação) sem
  mutação de candidato, baseline, global ou `config/estilo.json`.
- Sem popup, Aplicar, CONFIRMADO/ABORTADO, demonstração integrada ou
  persistência.

### delta_material

- `tela/renderizacao/estilo.py`: funções de amostra e
  `compor_titulo_com_amostra`; `associar_conteudo_estilo` preservado.
- `tela/estilo.py`: título de cada filho passa a ser a composição nome +
  amostra no momento da projeção.
- Testes dedicados H-0064 (derivação, ANSI/largura, sintético, resize,
  paginação, fronteira); testes H-0063 inalterados e verdes.

### verificacoes_executadas

- `PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_estilo_h0064.py demo/teste_demo_estilo_h0064.py tela/teste_estilo_h0063.py demo/teste_demo_estilo_h0063.py`
  → 39 passed.
- Fixture JSON compartilhada sem alteração; `config/estilo.json` sem delta.
- Probe non-TTY: amostras de borda (`╭─╮││╰─╯`) e chip com payload
  visíveis no quadro após entrar nos filhos; paginação exibe
  `[PgUp][PgDn] Páginas`.

### fronteira_respeitada

- Fora de escopo mantido: candidato, Aplicar, demonstração integrada,
  popup, persistência, publicação, ITEM-0024, ITEM-0032, tiling /
  cor_inativo / cor_alerta / indicadores.concluido.

### validacao_manual

- Não exigida nesta etapa; prevista apenas se o QA considerar necessário
  para legibilidade TTY das amostras compactas e distinção por cor
  (H-0064 §18).
