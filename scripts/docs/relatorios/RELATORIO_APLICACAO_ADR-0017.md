# Relatório de Aplicação da ADR-0017

## 1. Identificação

```yaml
etapa: APLICAR_ADR
projeto: Orquestrador
ciclo: ADR-0017 (handoff de implementação numerado no momento da criação)
data: 2026-07-11
```

## 2. Versão da ADR aplicada

```text
arquivo: docs/adr/ADR-0017-redimensionamento-reativo-tui.md
linhas: 446
sha256: 84aae1e57f7d22cda251aa976e26d645343a0a3bff60fbd0f1568e35df77ecf5
status: aceita
```

## 3. Relatório de QA autorizador

```text
docs/relatorios/RELATORIO_QA_ADR-0017.md
status registrado: ADR_APPROVED_WITH_NOTES
```

Usado como evidência de aprovação da ADR para a etapa APLICAR_ADR. Os achados
ADR17-QA-001, ADR17-QA-002 e ADR17-QA-003 foram considerados na aplicação; ver
seção 8.

## 4. Arquivos lidos

```text
docs/adr/ADR-0017-redimensionamento-reativo-tui.md
docs/relatorios/RELATORIO_QA_ADR-0017.md
docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md
docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
docs/adr/INDICE_ADR.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_composicao_corpo.md
docs/NOMENCLATURA.md
docs/contratos/contrato_estilo.md          (somente leitura — verificação de contradição)
docs/contratos/contrato_barra_de_menus.md  (somente leitura — verificação de contradição)
docs/contratos/contrato_lancador.md        (somente leitura — verificação de contradição)
docs/contratos/contrato_console.md         (somente leitura — verificação de contradição)
docs/relatorios/RELATORIO_APLICACAO_ADR-0016.md  (referência de padrão de relatório)
```

## 5. Arquivos alterados

```text
docs/adr/INDICE_ADR.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_composicao_corpo.md
docs/NOMENCLATURA.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0017.md   (criado nesta etapa)
```

## 6. Seções criadas ou atualizadas

### `docs/adr/INDICE_ADR.md`

- Adicionada linha de registro da ADR-0017 na tabela de decisões registradas,
  com número, título resumido, status `aceita`, data `2026-07-11` e indicação
  de relação complementar com ADR-0013 e ADR-0016.

### `docs/contratos/contrato_tela_json.md`

- Atualizado último bullet da seção 23 ("Execução TTY da sessão TUI —
  ADR-0016"): substituída a referência a "redimensionamento reativo da janela,
  reserva de handoff futuro" por referência à nova seção 24 (ADR-0017).
- **Adicionada seção 24**: "Redimensionamento reativo da sessão TUI (ADR-0017)",
  com as seguintes subseções normativas:
  - Gatilho (SIGWINCH)
  - Fonte primária e par coerente (ioctl / TIOCGWINSZ)
  - Validade de um par de dimensões
  - Cadeia de obtenção na inicialização (ioctl → LINES/COLUMNS → (80,24))
  - Cadeia de obtenção após SIGWINCH (ioctl → LINES/COLUMNS → últimas dimensões válidas)
  - Redesenho após par válido
  - Preservação da composição declarativa
  - Terminal pequeno demais
  - Preservações da seção 23 (ADR-0016)
  - Plataforma e exclusões
- Seções 24-28 renumeradas para 25-29 (Validação obrigatória, Erro/vazio,
  Hierarquia de defaults, Limite declarativo, Pendências derivadas).

### `docs/contratos/contrato_composicao_corpo.md`

- Adicionada ADR-0017 à lista `adrs_aplicadas` nos metadados.
- Seção 4.7 ("Ocupação vertical da janela — ADR-0013"): adicionado parágrafo
  "Mecanismo de obtenção de dimensões (ADR-0017)" com referência à cadeia
  normativa e confirmação de que o redimensionamento não altera `corpo.arranjo`
  nem `tiling`.
- Seção 5.1 ("Organização horizontal por tipo de conteúdo"): bullet "Largura
  sempre dinâmica" atualizado para "Largura e altura dinâmicas (ADR-0017)" com
  referência à seção 24 de `contrato_tela_json.md` e às restrições de
  composição.
- Seção 5.10 ("Regras dinâmicas de dimensão"): bullet "Terminal muito pequeno"
  atualizado para "Terminal pequeno demais (ADR-0017)" com política de quadro
  mínimo e recuperação automática conforme ADR-0017.
- Seção 7 ("Regras de uso"): adicionadas R-23 (redimensionamento não altera
  composição declarativa) e R-24 (novo par válido aciona recálculo de áreas).
- Seção 8 ("Critérios de validação"): adicionados dois critérios correspondentes
  a R-23 e R-24.
- Seção 9 ("Pendências"): item "Política de terminal muito pequeno" atualizado
  para referenciar ADR-0017 e `contrato_tela_json.md` seção 24.

### `docs/NOMENCLATURA.md`

- Campo `atualizado_em` atualizado para `2026-07-11`.
- Seção 6 ("Layout e largura"): bullet "Redimensionamento reativo" expandido com
  referência à ADR-0017 e à seção 6.2.
- **Adicionada subseção 6.2**: "Termos do redimensionamento reativo da TUI
  (ADR-0017, 2026-07-11)", contendo:
  - Tabela de definições: `redimensionamento reativo da TUI`, `SIGWINCH`,
    `ioctl(TIOCGWINSZ)`, `par de dimensões válido`, `últimas dimensões válidas`,
    `quadro mínimo de terminal pequeno`.
  - Tabela de distinções obrigatórias (não colapsam): inclui distinção com
    `corpo.arranjo`, `tiling`, `ocupacao_vertical_terminal` e `quadro mínimo de
    terminal pequeno` vs. encerramento da sessão.
  - Regras normativas derivadas da ADR-0017.

## 7. Mapeamento entre itens decisórios e documentos de destino

| Item decisório da ADR-0017 | Destino principal |
|---|---|
| 1. Gerenciamento próprio; sem biblioteca de TUI | `contrato_tela_json.md` §24 "Plataforma e exclusões"; `NOMENCLATURA.md` §6.2 regras normativas |
| 2. Gatilho (SIGWINCH) | `contrato_tela_json.md` §24 "Gatilho"; `NOMENCLATURA.md` §6.2 tabela de termos |
| 3. Fonte primária (ioctl/TIOCGWINSZ) | `contrato_tela_json.md` §24 "Fonte primária e par coerente"; `NOMENCLATURA.md` §6.2 |
| 4. Validade das dimensões | `contrato_tela_json.md` §24 "Validade de um par de dimensões"; `NOMENCLATURA.md` §6.2 `par de dimensões válido` |
| 5. Cadeia de obtenção na inicialização | `contrato_tela_json.md` §24 "Cadeia na inicialização" |
| 6. Cadeia de obtenção após SIGWINCH + não-redesenho com par inválido | `contrato_tela_json.md` §24 "Cadeia após SIGWINCH"; `NOMENCLATURA.md` §6.2 `últimas dimensões válidas` e tabela de distinções |
| 7. Redesenho após par válido (redução e ampliação) | `contrato_tela_json.md` §24 "Redesenho após par válido"; `contrato_composicao_corpo.md` R-24, §8 critérios |
| 8. Composição declarativa preservada | `contrato_tela_json.md` §24 "Preservação da composição declarativa"; `contrato_composicao_corpo.md` R-23, §8 critérios; `NOMENCLATURA.md` §6.2 distinções |
| 9. Resultado visual (sem resíduos, scroll, linhas fora) | `contrato_tela_json.md` §24 "Redesenho após par válido" (subitens de resultado visual) |
| 10. Terminal pequeno demais + recuperação automática | `contrato_tela_json.md` §24 "Terminal pequeno demais"; `contrato_composicao_corpo.md` §5.10, §9; `NOMENCLATURA.md` §6.2 `quadro mínimo de terminal pequeno` |
| 11. Preservações da ADR-0016 | `contrato_tela_json.md` §24 "Preservações da seção 23" |
| 12. Plataforma e exclusões | `contrato_tela_json.md` §24 "Plataforma e exclusões"; `NOMENCLATURA.md` §6.2 regras normativas |
| Registro no índice | `docs/adr/INDICE_ADR.md` (nova linha ADR-0017) |

## 8. Tratamento dos achados de QA

### ADR17-QA-001 — detalhe concreto de erro (RenderizadorErro)

Severidade: médio. A ADR menciona `RenderizadorErro` como detalhe de
implementação em terminal pequeno (ADR-0017:204).

**Tratamento aplicado**: nenhum nome de classe, exceção ou artefato técnico
interno foi propagado como requisito normativo. A regra funcional aplicada
nos documentos é:
- terminal pequeno não encerra a sessão TUI;
- exibe quadro mínimo de aviso que cabe nas dimensões atuais;
- recupera automaticamente quando dimensões suficientes forem restauradas.

`RenderizadorErro` não aparece em nenhum documento alterado. A ADR-0017 não
foi corrigida.

### ADR17-QA-002 — condição de não redesenho (ambiguidade na seção de riscos)

Severidade: médio. A seção decisória da ADR-0017 (linhas 154-159) determina
que, quando `ioctl` e `LINES`/`COLUMNS` não produzirem par válido, as últimas
dimensões válidas são conservadas e NÃO ocorre redesenho. A seção de riscos
(linhas 332-335) contém formulação que pode ser lida como autorização para
redesenhar usando dimensões do estado anterior.

**Tratamento aplicado**: a regra propagada nos documentos é exclusivamente a
da seção decisória: sem redesenho quando não há novo par válido. A frase da
seção de riscos NÃO foi propagada. Especificamente:
- `contrato_tela_json.md` §24 "Cadeia após SIGWINCH": "não redesenhar como se
  o tamanho tivesse mudado";
- `contrato_composicao_corpo.md` R-24: "Par inválido não é aplicado; as últimas
  dimensões válidas são mantidas sem que o redesenho seja acionado";
- `NOMENCLATURA.md` §6.2: "Par inválido não é aplicado ao renderer; últimas
  dimensões válidas são mantidas."

A ADR-0017 não foi corrigida.

### ADR17-QA-003 — observação de metadados (contratos_afetados)

Severidade: observação. O campo `contratos_afetados` da ADR-0017 inclui
`docs/NOMENCLATURA.md` e `docs/adr/INDICE_ADR.md`, que não são contratos de
módulo.

**Tratamento aplicado**: a observação não bloqueou a aplicação. Os metadados
da ADR-0017 não foram alterados. Os artefatos foram atualizados conforme a
tabela de consequências da própria ADR-0017 (linhas 301-308).

## 9. Termos adicionados ou consolidados

| Termo | Ação | Documento |
|---|---|---|
| `redimensionamento reativo da TUI` | Definido como termo específico | `NOMENCLATURA.md` §6.2 |
| `SIGWINCH` | Definido como gatilho normativo | `NOMENCLATURA.md` §6.2 |
| `ioctl(TIOCGWINSZ)` | Definido como fonte primária normativa | `NOMENCLATURA.md` §6.2 |
| `par de dimensões válido` | Definido com critério de validade | `NOMENCLATURA.md` §6.2 |
| `últimas dimensões válidas` | Definido com regra de conservação | `NOMENCLATURA.md` §6.2 |
| `quadro mínimo de terminal pequeno` | Definido com comportamento e recuperação automática | `NOMENCLATURA.md` §6.2 |
| `ocupacao_vertical_terminal` | Consolidado na tabela de distinções (não confundir com redimensionamento) | `NOMENCLATURA.md` §6.2 distinções |
| `corpo.arranjo` | Consolidado na tabela de distinções (não alterado por redimensionamento) | `NOMENCLATURA.md` §6.2 distinções |
| `tiling` | Consolidado na tabela de distinções (não alterado por redimensionamento) | `NOMENCLATURA.md` §6.2 distinções |

Nenhum sinônimo concorrente foi criado. "Vertical" e "horizontal" não foram
redefinidos.

## 10. Verificações de resíduos e contradições

### Busca de propagação proibida (ADR17-QA-002)

```bash
rg -n \
  'redesenho pode ocorrer com as dimensões|redesenho pode ocorrer com as dimensoes|redesenhar.*estado anterior' \
  docs/contratos/contrato_tela_json.md \
  docs/contratos/contrato_composicao_corpo.md \
  docs/NOMENCLATURA.md
```

Resultado: sem ocorrências. A frase da seção de riscos da ADR-0017 não foi
propagada.

### Busca de classe concreta normalizada (ADR17-QA-001)

```bash
rg -n 'RenderizadorErro' \
  docs/contratos/contrato_tela_json.md \
  docs/contratos/contrato_composicao_corpo.md \
  docs/NOMENCLATURA.md
```

Resultado: sem ocorrências. `RenderizadorErro` não foi inserido como requisito
normativo.

### Busca de consistência dos termos-chave

```bash
rg -n \
  'SIGWINCH|TIOCGWINSZ|últimas dimensões válidas|terminal pequeno demais|redimensionamento reativo' \
  docs/adr/INDICE_ADR.md \
  docs/contratos/contrato_tela_json.md \
  docs/contratos/contrato_composicao_corpo.md \
  docs/NOMENCLATURA.md
```

Resultado: termos presentes nos documentos corretos, sem ocorrências em
documentos que não deviam ser alterados.

### Verificação de contradição com ADR-0013

A ADR-0013 normatiza que `altura_disponivel` é dimensão explícita do render e
que o corpo deve preencher a área vertical entre `cabecalho` e `barra_de_menus`.
A ADR-0017 provê o mecanismo de obtenção e atualização dessa altura durante a
sessão TTY. As duas ADRs são complementares; nenhuma contradição foi identificada.

### Verificação de contradição com ADR-0016

A ADR-0016 normatiza a política completa de sessão TUI em tela cheia. A ADR-0017
complementa e preserva integralmente todas as políticas da ADR-0016. A seção 24
de `contrato_tela_json.md` inclui subseção "Preservações da seção 23" que
reafirma as políticas da ADR-0016 sem exceções.

### Verificação de arquivos proibidos

Nenhuma alteração foi feita em: `docs/adr/ADR-0017-*`, `docs/relatorios/RELATORIO_QA_ADR-0017.md`,
`docs/contratos/contrato_processo_desenvolvimento.md`, `docs/handoff/`, `config/`, `tela/`,
nem em qualquer outro arquivo de ADR, contrato ou relatório fora da lista permitida.

## 11. Comandos executados

```bash
git status --short
git diff --check
git diff --stat
git diff --name-only
git diff -- docs/adr/INDICE_ADR.md
git diff -- docs/contratos/contrato_tela_json.md
git diff -- docs/contratos/contrato_composicao_corpo.md
git diff -- docs/NOMENCLATURA.md
git diff --no-index /dev/null docs/adr/ADR-0017-redimensionamento-reativo-tui.md
git diff --no-index /dev/null docs/relatorios/RELATORIO_QA_ADR-0017.md
git diff --no-index /dev/null docs/relatorios/RELATORIO_APLICACAO_ADR-0017.md
rg -n 'SIGWINCH|TIOCGWINSZ|últimas dimensões válidas|terminal pequeno demais|redimensionamento reativo' ...
rg -n 'redesenho pode ocorrer com as dimensões|...' ...
rg -n 'RenderizadorErro' ...
```

## 12. Estado Git

```text
HEAD: de0f023 fix: corrige execução TTY em tela cheia
Stage antes das alterações: vazio
Arquivos não rastreados antes das alterações:
  docs/adr/ADR-0017-redimensionamento-reativo-tui.md
  docs/relatorios/RELATORIO_QA_ADR-0017.md
Arquivos modificados por esta etapa (rastreados):
  docs/adr/INDICE_ADR.md
  docs/contratos/contrato_tela_json.md
  docs/contratos/contrato_composicao_corpo.md
  docs/NOMENCLATURA.md
Arquivos criados por esta etapa (não rastreados):
  docs/relatorios/RELATORIO_APLICACAO_ADR-0017.md
Stage após as alterações: vazio (nenhum arquivo foi staged)
```

## 13. Bloqueios e limitações

Nenhum bloqueio identificado. A aplicação prosseguiu sem `BLOCKED_DOCUMENTATION`
nem `BLOCKED_USER_DECISION`.

Limitações documentadas:
- A ADR-0017 menciona `RenderizadorErro` (ADR17-QA-001) sem que isso seja
  normativo por esta ADR; foi tratado conforme orientação: não propagado.
- A frase da seção de riscos da ADR-0017 sobre redesenho (ADR17-QA-002) não foi
  propagada; apenas a regra da seção decisória foi distribuída.
- O campo `contratos_afetados` da ADR-0017 inclui artefatos que não são contratos
  de módulo (ADR17-QA-003); a aplicação foi feita igualmente a todos eles.
- O redimensionamento de `barra_de_menus` com `distribuicao.modo = "horizontal_responsiva"`
  não foi detalhado nesta etapa; a ADR-0017 explicitamente deixa esses detalhes
  no contrato da barra_de_menus. `contrato_barra_de_menus.md` não foi alterado.

## 14. Confirmações finais

- Código (`tela/`, `config/`): não alterado.
- Testes: não alterados.
- ADR-0017 (`docs/adr/ADR-0017-*.md`): não alterada.
- Relatório de QA (`docs/relatorios/RELATORIO_QA_ADR-0017.md`): não alterado.
- Handoffs (`docs/handoff/`): nenhum criado nem alterado.
- Arquivos de ADR além de `INDICE_ADR.md`: nenhum alterado.
- Outros contratos além dos listados: nenhum alterado.
- Commit, stage, push ou alteração de histórico Git: não realizados.
