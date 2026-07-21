---
name: nomenclatura-fachada-permanente
description: Fachada permanente de compatibilidade e navegação — as definições terminológicas vivem nos módulos proprietários em docs/nomenclatura/
metadata:
  type: fachada
  scope: orquestrador
  status: fachada_permanente
  fase_de_aplicacao: FASE_2_FACHADA_PERMANENTE
  substituicao_do_monolito_executada: true
  auditoria_pre_fachada: APROVADA
  data_conversao: "2026-07-21"
  adr_origem: docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md
  modulo_indice: docs/nomenclatura/00_INDICE.md
  modulo_nucleo: docs/nomenclatura/01_NUCLEO_COMUM.md
---

# NOMENCLATURA — Fachada permanente

> **Este arquivo é uma fachada permanente de compatibilidade e navegação.**
> As definições terminológicas não vivem mais aqui.
> Este arquivo aponta para os módulos proprietários em `docs/nomenclatura/`.
> **É proibido adicionar novas definições diretamente neste arquivo.**

## Regra de uso

Este arquivo existe exclusivamente para:

- preservar compatibilidade com referências ao caminho `docs/NOMENCLATURA.md`;
- oferecer navegação para o índice modular e para o núcleo comum;
- informar o modelo de leitura seletiva.

Nenhuma definição terminológica vive aqui. Toda referência a termo, schema
ou distinção deve ser resolvida pelo módulo proprietário declarado em
`docs/nomenclatura/00_INDICE.md`.

## Como usar a nomenclatura modular

A leitura deve partir do contrato ou da atividade, não da leitura prévia de
todos os módulos.

```yaml
ordem_de_leitura:
  1: ler a documentação inicial do processo (docs/INDICE.md)
  2: consultar docs/nomenclatura/00_INDICE.md
  3: ler docs/nomenclatura/01_NUCLEO_COMUM.md
  4: identificar o contrato ou artefato alvo da atividade
  5: ler os módulos declarados em dependencias_obrigatorias do contrato alvo
  6: ler os módulos de dependencias_condicionais que se aplicam à atividade
  7: consultar módulo adicional somente quando um termo necessário ainda não estiver carregado
```

**Leitura preventiva de todos os módulos é proibida** (D-NOM-03, ADR-0029).

## Ponto de entrada da nomenclatura modular

| Documento | Papel |
|---|---|
| `docs/nomenclatura/00_INDICE.md` | Índice e roteador — localiza o módulo proprietário de cada domínio e termo |
| `docs/nomenclatura/01_NUCLEO_COMUM.md` | Núcleo comum — terminologia transversal necessária para interpretar os demais módulos |

## Mapa de módulos

| Módulo | Domínio |
|---|---|
| `docs/nomenclatura/00_INDICE.md` | Índice e roteador |
| `docs/nomenclatura/01_NUCLEO_COMUM.md` | Núcleo comum e terminologia transversal |
| `docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` | Artefatos de configuração e runtime; separação motor/demo/produto; caminhos canônicos |
| `docs/nomenclatura/10_ESTILO.md` | Estilo universal — borda, chip visual, indicadores, cores, tiling |
| `docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md` | Tela, regiões, corpo, tipos funcionais, arranjo, composição genérica |
| `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` | Layout, redimensionamento reativo, quadro mínimo, paginação |
| `docs/nomenclatura/30_CABECALHO.md` | Cabeçalho — região fixa superior da tela |
| `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` | Barra de menus e chips — região fixa inferior; entidades declarativas |
| `docs/nomenclatura/32_CONSOLE.md` | Console — container interativo genérico de itens |
| `docs/nomenclatura/33_LANCADOR.md` | Lançador — tipo de elemento do corpo para navegação entre telas |
| `docs/nomenclatura/34_DASHBOARD.md` | Dashboard — saída passiva não navegável |
| `docs/nomenclatura/40_GRUPOS_E_DISTRIBUICAO_DE_AREA.md` | Grupos, distribuição de área, ocupação, espaço externo |
| `docs/nomenclatura/41_DISTRIBUICAO_MATRICIAL.md` | Distribuição matricial configurável de nível único |
| `docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md` | Dados externos multinível — envelope declarativo, níveis, schema semântico |
| `docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md` | Carregamento e associação de conteúdo externo ao console |
| `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` | Apresentações e modos multinível do console |
| `docs/nomenclatura/90_ALIASES_E_TERMOS_DESCONTINUADOS.md` | Aliases ativos e termos descontinuados |

## Referências históricas

As seções numeradas do monólito original (`#1-estilo-universal`,
`#3-composicao-de-corpo`, `#4-corpo-tipo-console`, `#5-barra_de_menus`,
`#6-layout-e-largura`, `#7-cabecalho`, `#8-corpo-tipo-lancador`,
`#9-objeto-dashboard`, `#10-tiling`, `#13-decisao-terminologica-lancador`,
`§16`, `§17`, `§18`, `§19`) não existem mais como âncoras neste arquivo.
Referências normativas ativas foram migradas para os módulos proprietários.
Referências em documentos históricos fechados foram preservadas como estão.

O histórico completo do monólito está em
`docs/relatorios/RELATORIO_HISTORICO_NOMENCLATURA_MONOLITICA.md`.

O relatório de aplicação da FASE_2 está em
`docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-2.md`.
