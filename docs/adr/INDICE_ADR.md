---
name: indice-adr
description: Modelo de indice para Architecture Decision Records
metadata:
  type: indice
  scope: orquestrador
---

# Indice — ADRs

## Regra

ADR registra uma decisao arquitetural aprovada ou rejeitada. Uma ADR aceita nao
deve ser editada para mudar decisao; se a decisao mudar, criar nova ADR que
substitui a anterior.

Este indice registra as ADRs aceitas do projeto.

## Como criar ADR

1. Copiar `docs/templates/TEMPLATE_ADR.md`.
2. Nomear como `ADR-NNNN-descricao-curta.md`.
3. Preencher contexto, decisao, consequencias e contratos afetados.
4. Atualizar este indice.
5. Atualizar os contratos afetados antes de gerar handoffs dependentes.

## Decisoes registradas

| ID | Titulo | Status | Data |
|---|---|---|---|
| ADR-0001 | `menu` suporta modo matriz (múltiplas colunas) | aceita | 2026-07-05 |
| ADR-0002 | `menu` usa sobra à direita | aceita | 2026-07-05 |
| ADR-0003 | Vãos elásticos do `menu` | aceita | 2026-07-05 |
| ADR-0004 | `cor_inativo` e `cor_alerta` no schema de estilo | aceita | 2026-07-05 |
| ADR-0005 | lancador não é corpo navegável por [✥] | aceita | 2026-07-06 |
| ADR-0006 | renomeação `dado` para `console` e `Info` para `dashboard` | aceita | 2026-07-06 |
| ADR-0007 | tela de processamento é composição de tipos existentes | aceita | 2026-07-06 |
| ADR-0008 | modelo de configuração por tela | aceita | 2026-07-07 |
| ADR-0009 | caminho, nomenclatura e formato dos JSONs de tela | aceita | 2026-07-07 |
| ADR-0010 | composição hierárquica do corpo e dashboard como elemento funcional | aceita | 2026-07-08 |
| ADR-0011 | terminologia de arranjo: `vertical`/`horizontal` (aliases transicionais `sobreposto`/`lado_a_lado`) | aceita | 2026-07-08 |
| ADR-0012 | `barra_de_menus` declarativa por tela | aceita | 2026-07-08 |
| ADR-0013 | ocupação vertical da janela do terminal pelo corpo (`ocupacao_vertical_terminal`) — distinta de `corpo.arranjo` | aceita | 2026-07-09 |
| ADR-0014 | distribuição horizontal **responsiva** da `barra_de_menus` (`distribuicao = "horizontal"` como alias transitório de `modo = "horizontal_responsiva"`) + regra de alteração por termo específico completo | aceita | 2026-07-09 |
| ADR-0015 | Composição hierárquica e distribuição de área do corpo | aceita | 2026-07-10 |
| ADR-0016 | Execução em tela cheia (TTY) sem cintilação, com Ctrl+C escopado | aceita | 2026-07-10 |
| ADR-0017 | Redimensionamento reativo da TUI — SIGWINCH, ioctl(TIOCGWINSZ), cadeia de dimensões válidas e quadro mínimo de aviso (complementa ADR-0013 e ADR-0016) | aceita | 2026-07-11 |
| ADR-0018 | Semântica da ausência de distribuição e da alocação vertical de área do corpo — distingue arranjo de distribuição; ausência de `corpo.distribuicao` deixa de equivaler ao modo `igual` e preserva a construção orientada pelo conteúdo; distribuição explícita reparte a altura útil com preenchimento interno das áreas (substitui parcialmente a ADR-0015 no ponto ausência ≡ `igual`) | aceita | 2026-07-11 |
| ADR-0019 | Profundidade contada por aninhamento de grupos, multiplicidade estrutural e remoção da cardinalidade global de dashboard — define contagem por níveis de grupos (não por listas `elementos[]`); permite três níveis de grupos; permite múltiplos grupos irmãos e múltiplos elementos funcionais por grupo inclusive no nível 3; remove restrição global de zero ou um dashboard por tela (supera parcialmente ADR-0007 na cardinalidade de `dashboard`; substitui parcialmente ADR-0015 no critério de contagem de profundidade) | aceita | 2026-07-12 |
| ADR-0020 | Especialização bidimensional do nó `grupo` — formaliza os comportamentos `livre` (hierárquico existente) e `matriz` (grade comum com coordenadas explícitas); seletor declarativo `estrutura`; ausência de `estrutura` equivale a `livre`; distribuições obrigatórias e independentes por eixo (`matriz.linhas.distribuicao`, `matriz.colunas.distribuicao`); dimensões 2–4 por eixo; cobertura completa de células; rejeição determinística sem fallback; compatibilidade retroativa integral (especializa ADR-0015, ADR-0018 e ADR-0019) | aceita | 2026-07-12 |
| ADR-0021 | Separação entre demonstração, produto real e política de caminhos — preserva `tela/` como motor compartilhado; prevê `demo/` como aplicação demonstrativa futura; distingue `config/telas/<id>.json` para produto real e `config/telas/demo/<id>.json` para demonstração; preserva `config/estilo.json`; substitui parcialmente a ADR-0009 no ponto de raiz única de telas | aceita | 2026-07-14 |
| ADR-0022 | Ponto de entrada e tela inicial real do Orquestrador — reserva `orquestrador.py` como ponto de entrada futuro do produto real; reserva `config/telas/orquestrador.json` com `id: "orquestrador"` como tela inicial real; define envelope `cabecalho`, `corpo`, `barra_de_menus`; define corpo inicial com `console` e `dashboard` presentes sem entradas; barra mínima com `Esc`, `?` e acesso a estilos; preserva a separação `demo` sem alias nem fallback | aceita | 2026-07-14 |
| ADR-0023 | Largura mínima funcional do `lancador` — quando `area_lancador_w < lancador_caixa_min_w`, nenhuma representação válida do `lancador` é possível; o quadro mínimo canônico global (ADR-0017) substitui integralmente toda a tela normal; fallback local proibido; recuperação automática por redesenho quando área suficiente for restaurada | aceita | 2026-07-15 |

## Exemplo de linha

| ADR-0000 | Escolher formato de persistencia do modulo exemplo | aceita | YYYY-MM-DD |
