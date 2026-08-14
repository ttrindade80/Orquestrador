# Relatório de criação do handoff H-0064

## rastreabilidade

```yaml
etapa: CRIAR_HANDOFF
objeto: H-0064
item: ITEM-0010
adr: ADR-0046
predecessor: H-0063
artefato_principal:
  docs/handoff/H-0064-amostras-visuais-presets-estilo.md
historico:
  H-0062:
    status: substituido
```

## execucao

```yaml
status: HANDOFF_CREATED
arquivos_criados:
  - docs/handoff/H-0064-amostras-visuais-presets-estilo.md
  - docs/relatorios/RELATORIO_CRIACAO_HANDOFF_H-0064.md
```

## resultado

```yaml
handoff:
  docs/handoff/H-0064-amostras-visuais-presets-estilo.md
capacidade:
  - amostras_visuais_dos_presets
arquivos_implementacao_autorizados:
  - tela/estilo.py
  - tela/renderizacao/estilo.py
  - tela/renderizador.py
  - tela/renderizacao/contexto_execucao.py
  - config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json
  - tela/teste_estilo_h0064.py
  - demo/teste_demo_estilo_h0064.py
  - docs/relatorios/IMP-0064-amostras-visuais-presets-estilo.md
testes_requeridos:
  - amostra de borda com os sete campos concretos do preset
  - amostra de chip com delimitadores, caixa_alta, cor_texto e cor_fundo, distinguindo presets que só variam por cor
  - amostra de selecionado com o símbolo concreto do preset
  - amostra de incluido com on/off concretos do preset
  - preset sintético aparece com amostra sem enumeração no código
  - comparação de saída visual/ANSI entre presets de chip com cores diferentes
  - fronteira de estado: navegar/Espaço/Esc não alteram candidato, config/estilo.json, preset_default ou estilo global
  - resize e paginação funcionais com amostras presentes
validacao_manual_prevista:
  - TTY opcional, a critério do QA, para legibilidade de miniaturas, distinção visual entre presets e comportamento após resize
fora_de_escopo:
  - candidato
  - Aplicar
  - demonstracao
  - popup
  - persistencia
  - publicacao
bloqueios: []
```

## Fatos materiais

H-0064 é continuação funcional de H-0063 (READY_FOR_IMPLEMENTATION,
tecnicamente aprovado), não substituição — H-0063 não foi alterado por esta
etapa. O objetivo exclusivo de H-0064 é acrescentar amostras visuais dos
presets aos filhos já existentes das quatro categorias expostas (`borda`,
`chip`, `indicadores.selecionado`, `indicadores.incluido`), preservando
integralmente a estrutura, a navegação `dois_niveis_por_foco`, a fronteira de
estado navegacional/mutação e a Barra de Menus já entregues por H-0063.

A leitura de autoridade cobriu integralmente a ADR-0046 (com foco na seção 2,
que normatiza origem das opções e materialização das amostras) e o H-0063
completo, e focalmente o `contrato_estilo.md` (§§3.1, 3.2, 3.3 e regras R-2,
R-6, R-7) e `docs/nomenclatura/10_ESTILO.md` (§§4.2–4.4), restritos aos
campos concretos de borda, chip, `indicadores.selecionado` e
`indicadores.incluido` e à proibição de hardcode. `config/estilo.json` foi
lido apenas como catálogo concreto atual e não foi alterado.

O código já implementado de H-0063 (`tela/estilo.py`,
`tela/renderizacao/estilo.py`) foi inspecionado para confirmar que os
presets completos já ficam retidos em memória por filho
(`PresetEstilo.dados`), o que permite à amostra reutilizar esses dados sem
nova busca ou catálogo paralelo.

Para os arquivos de implementação, optou-se por evoluir in-loco o
controlador e a integração de renderização já existentes de H-0063 (mesma
tela, mesmo shell declarativo), e por criar evidência de teste/demonstração
dedicada a H-0064 (`tela/teste_estilo_h0064.py`,
`demo/teste_demo_estilo_h0064.py`), preservando os testes estruturais e de
navegação já existentes de H-0063 sem duplicá-los. `config/estilo.json`,
`tela/loader.py`, `tela/navegacao.py`, `tela/selecao.py`,
`tela/renderizacao/tela.py` e `tela/renderizacao/console.py` permanecem como
infraestrutura canônica não autorizada, na mesma linha de H-0063.

O handoff explicitou a fronteira rigorosa: nenhuma capacidade de candidato,
`Aplicar`, demonstração integrada, override local, popup, `CONFIRMADO`/
`ABORTADO`, persistência ou publicação é antecipada. `ITEM-0024` (agrupar
pai+filhos entre páginas) e `ITEM-0032` (política global da Barra) foram
citados como explicitamente fora de escopo, não antecipados por H-0064.

## Execução desta etapa

Somente os dois artefatos documentais acima foram criados. Nenhum código,
ADR, contrato, módulo de nomenclatura ou item de backlog foi alterado.
Nenhum arquivo foi adicionado ao stage, commitado ou enviado ao repositório
remoto. H-0063 não foi reescrito nem teve seu status alterado.
