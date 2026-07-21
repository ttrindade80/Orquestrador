---
name: nomenclatura-layout-redimensionamento-paginacao
description: Terminologia transversal de dimensões, largura, altura, layout, redimensionamento reativo, SIGWINCH, ioctl, quadro mínimo, paginação e indicadores de página
metadata:
  type: nomenclatura
  scope: layout_redimensionamento_paginacao
  fase_de_aplicacao: VIGENTE
---

# Layout, redimensionamento e paginação

## 1. Estado

```yaml
fase_de_aplicacao: VIGENTE
fonte_normativa_do_dominio: este_modulo
fachada_de_navegacao: docs/NOMENCLATURA.md
substituicao_de_autoridade_executada: true
auditoria_pre_fachada_aprovada: true
```

## 2. Responsabilidade

Este módulo é proprietário da terminologia transversal de:
- dimensões da tela;
- largura e altura;
- layout;
- redimensionamento reativo da TUI;
- `SIGWINCH` e `ioctl(TIOCGWINSZ)` como conceitos;
- `par de dimensões válido` e `últimas dimensões válidas`;
- `quadro mínimo de terminal pequeno` (definição geral);
- paginação e indicador de página;
- truncamento e excesso quando gerais.

Grandezas exclusivas do lançador (`area_lancador_w`, `lancador_caixa_min_w`,
`coluna_minima_content_w`) pertencem ao módulo `33`.

## 3. Termos proprietários

- `redimensionamento reativo da TUI`
- `SIGWINCH`
- `ioctl(TIOCGWINSZ)`
- `par de dimensões válido`
- `últimas dimensões válidas`
- `quadro mínimo de terminal pequeno` (definição canônica)
- largura de tela (dinâmica)
- paginação
- indicador de paginação
- `ocupacao_vertical_terminal`

## 4. Definições

### 4.1 Largura de tela

Sempre dinâmica, calculada a partir da largura real do terminal. Sem perfis
fixos pré-definidos.

### 4.2 Termos do redimensionamento reativo (ADR-0017)

| Termo | Definição |
|---|---|
| `redimensionamento reativo da TUI` | Capacidade de detectar mudança de tamanho da janela do terminal em sessão TTY ativa (via `SIGWINCH`), obter novo par válido de dimensões e redesenhar o quadro sem encerrar a sessão |
| `SIGWINCH` | Sinal POSIX recebido quando a janela do terminal muda de tamanho; gatilho normativo do redimensionamento reativo em sessão TTY ativa |
| `ioctl(TIOCGWINSZ)` | Chamada de sistema que obtém as dimensões atuais da janela do terminal; fonte primária normativa de largura e altura durante sessão TTY |
| `par de dimensões válido` | Par (largura, altura) em que ambos os valores estão presentes, podem ser interpretados como inteiros e são maiores que zero; único estado que pode ser aplicado ao renderer |
| `últimas dimensões válidas` | O par (largura, altura) mais recente que satisfez os critérios de validade; conservado quando a obtenção pós-`SIGWINCH` não produz par válido; não é substituído pelo fallback fixo durante sessão já ativa |
| `quadro mínimo de terminal pequeno` | Quadro substituto exibido quando as dimensões são válidas mas insuficientes para a tela normal; comunica inequivocamente "terminal pequeno demais"; cabe nas dimensões atuais; é substituído automaticamente pela tela normal quando dimensões suficientes forem restauradas |

### 4.3 `ocupacao_vertical_terminal` (ADR-0013)

Preenchimento da altura da janela do terminal pelo renderer. Conceito distinto
de `corpo.arranjo = "vertical"` (ADR-0013):

- `corpo.arranjo = "vertical"`: composição/ordem dos elementos do corpo.
- `ocupacao_vertical_terminal`: preenchimento da altura disponível.

Os dois conceitos coexistem independentemente: uma tela com `corpo.arranjo = "horizontal"`
também deve poder ocupar a altura disponível.

### 4.4 Indicador de paginação (§6.1)

Quando o corpo tem paginação, a última linha da própria borda do corpo exibe
o indicador de página, ancorado à direita, no formato `─ página X/Y ─`.

O indicador pertence à borda do corpo paginado, não ao layout geral da tela.
Cada corpo exibe sua própria paginação dentro da própria borda, independente
de posição na tela.

### 4.5 Regras normativas derivadas do redimensionamento (ADR-0017)

- Redimensionamento não altera `corpo.arranjo`, `tiling`, chips nem elementos declarados.
- Redimensionamento não cria fallback de composição baseado em largura ou altura.
- Par inválido não é aplicado ao renderer; `últimas dimensões válidas` são mantidas.
- Fallback fixo `(80, 24)` somente na inicialização sem fontes válidas; nunca
  substitui `últimas dimensões válidas` durante sessão ativa.
- `quadro mínimo de terminal pequeno` não encerra a sessão; recuperação é automática.
- `ncurses`, `curses`, `textual` e `rich` permanecem proibidos para esta capacidade.

## 5. Distinções obrigatórias

| Termo | Significado | Não confundir com |
|---|---|---|
| `redimensionamento reativo da TUI` | Detecção de `SIGWINCH` e redesenho com novo par válido em sessão TTY | `corpo.arranjo` ou `tiling` (composição declarativa, não sessão TTY) |
| `par de dimensões válido` | Par (largura > 0, altura > 0) de fonte normativa | Par parcial ou zerado — não aplicável ao renderer |
| `últimas dimensões válidas` | Par conservado durante sessão quando nova obtenção falha | Fallback fixo `(80, 24)` — este só se aplica na inicialização sem fontes válidas |
| `ocupacao_vertical_terminal` | Preenchimento da altura disponível (ADR-0013) | `corpo.arranjo = "vertical"` (composição dos elementos do corpo, ADR-0011) |
| `corpo.arranjo` | Ordem/composição dos elementos do corpo declarada no `tela.json` | Resultado visual do redimensionamento — o redimensionamento não altera `corpo.arranjo` |
| `tiling` | Preferência de arranjo do estilo ou fixação pela classe de tela | Resultado de redimensionamento |
| `quadro mínimo de terminal pequeno` | Aviso exibido quando tela não cabe mas sessão permanece ativa | Encerramento da sessão TUI |

## 6. Relação com contratos

- `contrato_tela_json.md`: política normativa completa do redimensionamento
  (seção 24). Os termos aqui definidos são a autoridade terminológica.
- `contrato_composicao_corpo.md`: usa `ocupacao_vertical_terminal`.

## 7. Relação com ADRs

- ADR-0013: `ocupacao_vertical_terminal`; distinção de `corpo.arranjo`.
- ADR-0017: redimensionamento reativo; `SIGWINCH`; cadeia de dimensões válidas;
  `quadro mínimo de terminal pequeno`.
- ADR-0023: aciona o mesmo `quadro mínimo de terminal pequeno` por insuficiência
  de área do `lancador` — grandezas específicas do `lancador` pertencem ao módulo `33`.
- ADR-0025: aciona o mesmo `quadro mínimo de terminal pequeno` por impossibilidade
  geométrica da distribuição matricial.

## 8. Aliases ou termos descontinuados relacionados

Nenhum neste módulo.

## 9. Conteúdo que não pertence a este módulo

- Grandezas de largura específicas do `lancador` (`area_lancador_w`,
  `lancador_caixa_min_w`, `coluna_minima_content_w`) → módulo `33`.
- Composição do corpo → módulo `20`.
- Distribuição de área entre filhos → módulo `40`.
- Comportamento normativo completo do redimensionamento → `contrato_tela_json.md`.

## 10. Proveniência da migração

```yaml
origem_no_monolito:
  secao: "§6 (linhas 683-825)"
  intervalo_ou_bloco: "NOM-LEV-012"
origem_normativa: ADR-0013, ADR-0017, ADR-0023
contratos_relacionados:
  - contrato_tela_json.md
  - contrato_composicao_corpo.md
  - contrato_lancador.md
adrs_relacionadas:
  - ADR-0013
  - ADR-0017
  - ADR-0023
  - ADR-0025
tratamento:
  - PRESERVADO
  - SEPARADO_DE_REGRA_COMPORTAMENTAL
partes_NAO_CONFIRMADAS: []
```
