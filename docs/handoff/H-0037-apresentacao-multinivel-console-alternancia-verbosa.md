---
name: H-0037-apresentacao-multinivel-console-alternancia-verbosa
description: Implementação das quatro apresentações de console multinível com políticas de modo distintas (D23) — somente não verbosa, somente verbosa em dois níveis, alternável em três níveis iniciando não verbosa, tabela alternável iniciando verbosa; chip [V] Verboso exclusivo nas telas alternáveis; tecla V restrita às alternáveis; testes de schema e comportamentais; ADR-0028 com D23 incorporado
metadata:
  type: handoff_implementacao
  status: AGUARDANDO_QA
  id: H-0037
  data_criacao: "2026-07-17"
  data_patch: "2026-07-18"
rastreabilidade:
  adr_principal: docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md
  contratos_aplicados:
    - docs/contratos/contrato_json_console.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_composicao_corpo.md
  relatorios_autoridade:
    - docs/relatorios/RELATORIO_QA_ADR-0028.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0028.md
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0028.md
    - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0028.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0028.md
    - docs/relatorios/RELATORIO_QA_ADR-0028_REVISAO_MODOS_POR_TELA.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0028_REVISAO_MODOS_POR_TELA.md
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md
    - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md
    - docs/relatorios/RELATORIO_QA_H-0037_HANDOFF.md
  handoffs_anteriores:
    - docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md
---

# H-0037 — Apresentação multinível no console com política de modo por tela

## 1. Identificação

| Campo | Valor |
|---|---|
| Handoff | H-0037 |
| Título | Apresentação multinível no console com política de modo por tela (D23) |
| ADR base | ADR-0028 (`aceita e aplicada`, 2026-07-17/18 — inclui D23) |
| Arquivo | `docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md` |
| Data de criação | 2026-07-17 |
| Data do patch | 2026-07-18 |
| Ciclo anterior fechado | H-0036 / ADR-0026 + ADR-0027 / commit `f6982d0` |

---

## 2. Estado comprovado

```yaml
ciclo_anterior_concluido:
  handoff: H-0036
  titulo: fornecimento externo de dados ao console por JSON multinivel
  adrs: ADR-0026 + ADR-0027
  commit: f6982d0
  branch: master
  status: CONCLUIDO
  baseline_suíte: 9 scripts / 2423 verificacoes / 0 falhas

ciclo_documental_adr_0028:
  adr: ADR-0028
  status_adr: aceita e aplicada (inclui D23)
  data_aplicacao_inicial: "2026-07-17"
  data_patch_D23: "2026-07-18"
  qa_adr_inicial: ADR_APPROVED_WITH_NOTES
  aplicacao_inicial: CONCLUIDA (D1-D22)
  qa_aplicacao_inicial: ADR_APPLICATION_APPROVED_WITH_NOTES
  qa_adr_revisao_modos: ADR_APPROVED_WITH_NOTES (QA-MODOS-001, QA-MODOS-002 corrigidos)
  aplicacao_D23: CONCLUIDA
  qa_aplicacao_D23_pos_patch: ADR_APPLICATION_APPROVED_WITH_NOTES
  achados_bloqueantes_no_qa_pos_patch_D23: 0
  campos_canonicos_D23:
    politica: formato.excesso.politica_modo
    modo_inicial: formato.excesso.modo_inicial
    localizacao: JSON estrutural da tela (elemento console)
  proxima_categoria_autorizada: PATCH_HANDOFF → IMPLEMENTAR

git_antes_do_patch_deste_handoff:
  branch: master
  head: f6982d0
  mensagem_head: "docs: corrige whitespace do fechamento H-0036"
  workspace: sujo_acumulado_adr_0028_completo (nao commitado)
  stage: vazio
  commit_novo: nao_realizado
  git_diff_check: sem_erros
```

---

## 3. Autoridades

Documentos lidos integralmente como base normativa deste handoff:

```text
docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md
docs/relatorios/RELATORIO_QA_ADR-0028.md
docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0028.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0028.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0028.md
docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0028.md
docs/relatorios/RELATORIO_QA_ADR-0028_REVISAO_MODOS_POR_TELA.md
docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0028_REVISAO_MODOS_POR_TELA.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md
docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md
docs/contratos/contrato_json_console.md
docs/contratos/contrato_console.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_composicao_corpo.md
docs/NOMENCLATURA.md
docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md
docs/relatorios/IMP-0036-fornecimento-externo-dados-console-json-multinivel.md
docs/relatorios/RELATORIO_QA_H-0037_HANDOFF.md
```

Autoridade final para nomes, semântica e fronteiras: ADR-0028 (incluindo D23) e os
contratos ativos listados acima.

---

## 4. Contexto

### 4.1 Ciclo anterior

O H-0036 (ADR-0026 + ADR-0027) implementou o fornecimento externo de dados ao
console por JSON multinível. Esse ciclo entregou:

- separação entre JSON estrutural e documento externo de conteúdo;
- carregamento separado pelo `demo.py` e associação por catálogo;
- schema semântico multinível com 20 validações (ADR-0027);
- três apresentações: `tabela`, `hierarquia`, `conjuntos_campos`;
- fixtures: `h0036_console_{hierarquia,tabela,conjuntos}.json` e seus
  documentos externos correspondentes;
- suíte canônica: 9 scripts, 2423 verificações, 0 falhas.

### 4.2 Lacunas resolvidas pela ADR-0028 (incluindo D23)

O H-0036 não implementou:

1. **política de modo por tela** (D23): cada tela nova declara se é somente
   verbosa, somente não verbosa ou alternável;
2. **alternância verbosa** em telas alternáveis: tecla `V` alterna entre os
   modos durante a sessão;
3. **estado de sessão**: modo visual isolado por console, não persistente;
4. **modo inicial declarado pela política da tela** (`formato.excesso.modo_inicial`
   no JSON estrutural para telas alternáveis);
5. **quatro cenários de demonstração** com políticas distintas conforme §36.2
   da ADR-0028;
6. **chip `[V] Verboso`** na barra de menus, exclusivo de telas alternáveis.

A ADR-0028 com D23 (`aceita e aplicada`) formaliza todas essas decisões. Suas
regras foram propagadas para os contratos ativos. Este handoff implementa as
obrigações resultantes.

### 4.3 Fixtures do H-0036 são regressão, não substituição

As fixtures do H-0036 (`h0036_*.json`) permanecem válidas e intactas. O H-0037
cria quatro novas telas estruturais e três documentos externos para os cenários
de demonstração da ADR-0028 §36.2. Nenhuma fixture do H-0036 é removida nem
alterada.

---

## 5. Objetivo

Implementar, como capacidade coesa e única, as quatro demonstrações permanentes
de apresentação multinível no console com política de modo por tela (D23):

1. **Quatro telas com políticas distintas** conforme ADR-0028 §36.2:
   tela somente não verbosa, tela somente verbosa em dois níveis, tela
   alternável em três níveis (inicia não verbosa), tabela alternável (inicia
   verbosa);
2. **Três documentos externos de conteúdo**: dois níveis (compartilhado entre
   as telas fixas), três níveis e tabela;
3. **Tecla V** no `demo.py`: exclusiva de telas alternáveis, alterna modo
   durante a sessão sem troca de tela nem persistência;
4. **Inicialização do modo** a partir da política declarada no JSON estrutural;
5. **Recuperação do modo inicial** ao trocar de tela ou recarregar;
6. **Chip `[V] Verboso`** na barra de menus somente das telas alternáveis;
7. **Testes de schema** (aceitação e rejeição) e **testes comportamentais**
   por tipo de política;
8. **Validação manual em TTY real**;
9. **Regressão completa**: suíte canônica de 9 scripts preservada.

---

## 6. Capacidade coesa e fluxo obrigatório

```text
JSON estrutural (h0037_console_*.json)     ─┐
  └─ formato.excesso.politica_modo           │
  └─ formato.excesso.modo_inicial (se altern.)├─> demo/demo.py
JSON externo (h0037_*_conteudo.json)       ─┘   (carregamento e catálogo)
                                                      ↓
                             loader (20 val. ADR-0027 + 15 val. ADR-0028 + D23)
                                                      ↓
                                    modelo (conteúdo semântico + política de modo)
                                                      ↓
                         renderizador (não verboso: 1 linha + truncamento)
                                          (verboso: múltiplas linhas físicas)
                                                      ↓
                                              área visual do console

               Tecla V → somente em telas alternáveis → flip do estado de sessão
```

Regras invioláveis do fluxo:

- a política de modo é lida do JSON estrutural da tela (não do documento externo);
- o `demo.py` associa por catálogo (`_CATALOGO_CONTEUDO_EXTERNO`), sem campo
  de vínculo no JSON estrutural;
- o loader valida 20 validações ADR-0027, 15 validações V-01–V-15 e os campos D23;
- o modelo transporta o conteúdo multinível e a política de modo sem calcular geometria;
- o renderizador calcula representação física para cada modo;
- o estado da sessão é mantido por instância de console, não persiste;
- o JSON externo **não** é reescrito durante a alternância;
- o JSON estrutural **não** contém conteúdo de runtime;
- a política **não** é declarada no documento externo de conteúdo;
- a tecla `V` **não** é exposta nem ativa em telas de modo único.

---

## 7. Base de caminhos

Raiz operacional = raiz Git do projeto. Todos os caminhos são relativos à raiz:

```text
config/
demo/
docs/
tela/
```

Não usar prefixo `scripts/`. Não prefixar com o nome do projeto.

---

## 8. Schema D23 — política de modo por tela

Esta seção documenta os campos canônicos aprovados pela D23 e propagados para
`contrato_json_console.md` §13.13.

### 8.1 Campos canônicos

Os campos são declarados no JSON estrutural da tela, dentro do elemento `console`:

```yaml
politica:
  caminho: formato.excesso.politica_modo
  valores:
    - somente_verboso
    - somente_nao_verboso
    - alternavel

modo_inicial:
  caminho: formato.excesso.modo_inicial
  valores:
    - verboso
    - nao_verboso
  quando: somente se politica_modo for "alternavel"
```

A política é declarada no JSON estrutural da tela. O documento externo de
conteúdo não contém `politica_modo` nem `modo_inicial`.

### 8.2 Regras por política

#### `somente_verboso`

```json
{
  "formato": {
    "excesso": {
      "politica_modo": "somente_verboso"
    }
  }
}
```

- `modo_inicial` deve estar **ausente**;
- a tela sempre permanece verbosa;
- não oferece alternância;
- não exibe chip de alternância.

#### `somente_nao_verboso`

```json
{
  "formato": {
    "excesso": {
      "politica_modo": "somente_nao_verboso"
    }
  }
}
```

- `modo_inicial` deve estar **ausente**;
- a tela sempre permanece não verbosa;
- não oferece alternância;
- não exibe chip de alternância;
- truncamento com `...` é válido quando aplicável.

#### `alternavel`

```json
{
  "formato": {
    "excesso": {
      "politica_modo": "alternavel",
      "modo_inicial": "nao_verboso"
    }
  }
}
```

ou:

```json
{
  "formato": {
    "excesso": {
      "politica_modo": "alternavel",
      "modo_inicial": "verboso"
    }
  }
}
```

- `modo_inicial` é **obrigatório**;
- `[V] Verboso` é obrigatório na barra de menus;
- `V` alterna entre os modos;
- a alternância é reversível.

### 8.3 Matriz de validade

| `politica_modo` | `modo_inicial` | Válido? |
|---|---|---|
| `"somente_verboso"` | ausente | **VÁLIDO** |
| `"somente_nao_verboso"` | ausente | **VÁLIDO** |
| `"alternavel"` | `"verboso"` | **VÁLIDO** |
| `"alternavel"` | `"nao_verboso"` | **VÁLIDO** |
| `"alternavel"` | ausente | **INVÁLIDO** — modo inicial obrigatório |
| `"alternavel"` | valor desconhecido | **INVÁLIDO** — valor fora de `{"verboso", "nao_verboso"}` |
| `"somente_verboso"` | qualquer valor | **INVÁLIDO** — modo inicial proibido em política fixa |
| `"somente_nao_verboso"` | qualquer valor | **INVÁLIDO** — modo inicial proibido em política fixa |
| valor desconhecido | qualquer | **INVÁLIDO** |
| ausente (tela nova ou revisada) | qualquer | **INVÁLIDO** — ausência de política é inválida |

Fonte: `contrato_json_console.md` §13.13.3.

### 8.4 Campo `excesso.modo` (legado — não usar nas telas H-0037)

O campo `excesso.modo` que aparece no exemplo normativo de §12.7 do contrato
(dentro do **documento externo** de conteúdo) é o mecanismo anterior ao D23 e
está supersedido para telas novas ou revisadas.

O mecanismo D23 está no JSON **estrutural** da tela. O campo legado está no
**documento externo**. Eles não conflitam no mesmo arquivo.

As telas H-0037 **não devem** usar `excesso.modo` no documento externo como
declaração de política. A política pertence exclusivamente ao JSON estrutural
via `formato.excesso.politica_modo`.

### 8.5 Telas legadas H-0036

As telas H-0036 não declaram `politica_modo` nem `modo_inicial`. Esta ausência
não é tratada como inválido pelo loader para telas legadas. Elas não recebem
política por inferência nem são reinterpretadas automaticamente.

Fonte: `contrato_json_console.md` §13.13.8.

### 8.6 Localização da política

| Responsabilidade | JSON estrutural da tela | Documento externo de conteúdo |
|---|---|---|
| Política de modo (`politica_modo`) | **Sim** | **Não** |
| Modo inicial (`modo_inicial`) | **Sim** | **Não** |
| Dados de conteúdo semântico | Não | Sim |
| Tipo de apresentação (`tabela`, `hierarquia`, `conjuntos_campos`) | Não | Sim |
| Estado de visualização da sessão | Não (runtime) | Não |

---

## 9. Decisões fechadas (não reabrir)

| ID | Decisão | Autoridade |
|---|---|---|
| D-ADR28-D1 | Conteúdo multinível permanece externo ao JSON estrutural | ADR-0028 D1; `contrato_tela_json.md` §33.1 |
| D-ADR28-D2 | Console recebe documento JSON com mesma estrutura independente da origem | ADR-0028 D2; `contrato_json_console.md` §13.1 |
| D-ADR28-D3 | Carregamento separado e entrega conjunta; sem fusão de documentos | ADR-0028 D3; `contrato_json_console.md` §13.10 |
| D-ADR28-D4 | Estrutura hierárquica independente da apresentação visual | ADR-0028 D4; `contrato_json_console.md` §13.2 |
| D-ADR28-D5 | Designadores independentes da estrutura declarada | ADR-0028 D5 |
| D-ADR28-D6 | Estrutura hierárquica declarada explicitamente em `niveis[]` | ADR-0028 D6; `contrato_json_console.md` §13.2 |
| D-ADR28-D7 | Tipos conceituais: contêiner, folha, campo | ADR-0028 D7; `contrato_json_console.md` §13.3 |
| D-ADR28-D8 | Quatro cenários de demonstração obrigatórios com políticas distintas | ADR-0028 D8, §36.2; `contrato_json_console.md` §13.11, §13.13.10 |
| D-ADR28-D9 | Modo não verboso: uma linha física por conteúdo, excedente truncado | ADR-0028 D9; `contrato_json_console.md` §13.5 |
| D-ADR28-D10 | Modo verboso: múltiplas linhas físicas calculadas pelo renderizador | ADR-0028 D10; `contrato_json_console.md` §13.6 |
| D-ADR28-D11 | Tecla `V` alterna entre modos **somente em telas alternáveis** | ADR-0028 D11; `contrato_console.md` §21.5 |
| D-ADR28-D12 | Modo inicial determinado pela política da tela (D23) | ADR-0028 D12, §25; `contrato_json_console.md` §13.13 |
| D-ADR28-D13 | JSON externo declara apenas conteúdo semântico e políticas declarativas | ADR-0028 D13; `contrato_json_console.md` §13.10 |
| D-ADR28-D14 | Renderizador tem responsabilidade exclusiva sobre geometria física | ADR-0028 D14; `contrato_json_console.md` §13.10 |
| D-ADR28-D15 | Tabela multinível com cabeçalho; cabeçalho repetido por página | ADR-0028 D15; `contrato_json_console.md` §13.4, §13.7 |
| D-ADR28-D16 | Hierarquia indentada: uma linha lógica por nó | ADR-0028 D16; `contrato_json_console.md` §13.4 |
| D-ADR28-D17 | `conjuntos_campos`: cenários distintos por quantidade de níveis | ADR-0028 D17; `contrato_json_console.md` §13.4 |
| D-ADR28-D21 | Validações V-01–V-15 obrigatórias no loader | ADR-0028 D21; `contrato_json_console.md` §13.9 |
| D-ADR28-D22 | Demonstrações e testes semânticos obrigatórios conforme §36 e §37 | ADR-0028 D22 |
| D-ADR28-D23 | Política de modo por tela: somente verbosa / somente não verbosa / alternável | ADR-0028 D23; `contrato_json_console.md` §13.13 |
| — | Estado verboso/não verboso é de sessão; não persiste | `contrato_console.md` §21.6; `contrato_barra_de_menus.md` §22.3 |
| — | Alternância não reescreve JSON externo nem JSON estrutural | `contrato_console.md` §21.6; `contrato_barra_de_menus.md` §22.3 |
| — | Chip `[V] Verboso` exclusivo de telas com `politica_modo: "alternavel"` | ADR-0028 D23, §23; `contrato_barra_de_menus.md` §22.1, §22.8 |
| — | Modo inicial restaurado ao trocar de tela ou recarregar | `contrato_console.md` §21.6; `contrato_barra_de_menus.md` §22.3 |
| — | H-0036 fixtures preservadas sem alteração | ADR-0028 §39; `contrato_json_console.md` §12.8, §13.13.8 |
| — | Alinhamento no cenário verboso de dois níveis: escopo `conteúdo completo` | ADR-0028 §36.3; `contrato_json_console.md` §13.13.11 |
| — | Política não declarada no documento externo de conteúdo | `contrato_json_console.md` §13.13.6, §13.13.9 |

O executor não decide nenhum desses itens.

---

## 10. Decisões deferidas (não implementar sem autoridade)

| Item deferido | Fonte normativa |
|---|---|
| Nomes definitivos das propriedades JSON de conteúdo multinível | ADR-0028 §43 item 1 |
| Versão inicial do schema | ADR-0028 §43 item 2 |
| Estratégia de migração das telas legadas e eventual representação de compatibilidade no loader | ADR-0028 §43 item 3 (schema concreto dos campos decidido em D23; migração adiada) |
| Marcador padrão de truncamento | ADR-0028 §43 item 4 |
| Estilos de designador obrigatórios no schema | ADR-0028 §43 item 5 |
| Limites máximos de profundidade | ADR-0028 §43 item 6 |
| Política global de fallback visual para impossibilidade no conteúdo multinível | ADR-0028 §43 item 7 |
| Estratégia concreta de navegação entre páginas | ADR-0028 §43 item 8 |
| Formato de mensagens de validação | ADR-0028 §43 item 9 |
| Protocolo de integração com o Pipeline (itens 10–15) | ADR-0028 §43 itens 10–15 |
| Reconciliação terminológica definitiva entre `modo normal` e `modo não verboso` | `contrato_console.md` §21.4 |
| Referência cruzada entre seções 14 e 22 do `contrato_barra_de_menus.md` | APLIC-QA-003 (observação não corretiva) |

---

## 11. Fronteiras de responsabilidade

| Componente | Responsabilidade neste handoff | Fora de responsabilidade |
|---|---|---|
| `demo/demo.py` | Identificar cenário; carregar JSON estrutural e externo; associar por catálogo; ler `politica_modo` e `modo_inicial` do JSON estrutural; capturar tecla V somente em telas alternáveis; restaurar modo ao trocar de tela | Calcular geometria; persistir estado; reescrever JSON |
| JSON estrutural (h0037_console_*.json) | Declarar estrutura da tela; declarar `politica_modo` e, quando alternável, `modo_inicial`; declarar chip `[V] Verboso` na `barra_de_menus` somente em telas alternáveis | Conteúdo de runtime; campo de vínculo; estado de sessão |
| Documento externo (h0037_*_conteudo.json) | Declarar `tipo`, `formato.apresentacao`, `formato.niveis`, `dados` | Política de modo; modo inicial; resultados físicos calculados |
| Loader | Validar 20 validações ADR-0027 + 15 validações V-01–V-15 + campos D23 (`politica_modo`, `modo_inicial`); produzir representação interna | Abrir arquivos; decidir modo de sessão |
| Modelo | Transportar conteúdo multinível e política de modo; preservar origens separadas | Calcular geometria; abrir arquivos |
| Renderizador | Calcular representação física para modo não verboso (1 linha + truncamento) e verboso (quebras de linha); acatar modo corrente | Abrir arquivos; persistir estado; manter estado de sessão |

---

## 12. Localização das fixtures permanentes

```text
config/telas/demo/
```

Os sete arquivos novos seguem a organização existente do repositório:

| Arquivo | Tipo | Conteúdo |
|---|---|---|
| `config/telas/demo/h0037_console_nao_verboso.json` | JSON estrutural | Tela somente não verbosa; sem chip `[V]` |
| `config/telas/demo/h0037_console_verboso_dois_niveis.json` | JSON estrutural | Tela somente verbosa; sem chip `[V]` |
| `config/telas/demo/h0037_console_alternavel_tres_niveis.json` | JSON estrutural | Tela alternável; chip `[V] Verboso` obrigatório |
| `config/telas/demo/h0037_console_tabela_alternavel.json` | JSON estrutural | Tela alternável de tabela; chip `[V] Verboso` obrigatório |
| `config/telas/demo/h0037_dois_niveis_conteudo.json` | Documento externo | Conteúdo de dois níveis; compartilhado entre cenários 1 e 2 |
| `config/telas/demo/h0037_tres_niveis_conteudo.json` | Documento externo | Conteúdo de três níveis |
| `config/telas/demo/h0037_tabela_conteudo.json` | Documento externo | Conteúdo tabular |

O compartilhamento do documento externo entre os cenários 1 e 2 é intencional:
prova que o mesmo conteúdo produz resultado visual diferente conforme a política
da tela, sem troca de dados.

---

## 13. Os quatro cenários de demonstração

### 13.1 Cenário 1 — somente não verboso

| Campo | Valor |
|---|---|
| Identificador da tela | `h0037_console_nao_verboso` |
| JSON estrutural | `config/telas/demo/h0037_console_nao_verboso.json` |
| Documento externo | `config/telas/demo/h0037_dois_niveis_conteudo.json` |
| Política de modo | `somente_nao_verboso` |
| Modo inicial | NAO_APLICAVEL (único) |
| Chip `[V] Verboso` | ausente |
| Comando de entrada | `python demo/demo.py h0037_console_nao_verboso` |
| Identidade semântica | string `"H-0037 nao_verboso"` verificável no documento externo |

Comportamento obrigatório:

- texto excedente apresentado com `...` visível;
- o marcador participa do cálculo da largura;
- dados originais não alterados;
- pressionar `V` não produz efeito (política fixa);
- ausência do chip confirmada.

Requisitos mínimos do documento externo compartilhado:

- `formato.apresentacao` declarado (`hierarquia` ou `conjuntos_campos`);
- ao menos dois níveis de estrutura;
- identificadores do primeiro nível com larguras diferentes;
- conteúdo suficientemente longo para truncamento no modo não verboso;
- conteúdo suficientemente longo para múltiplas linhas no modo verboso.

### 13.2 Cenário 2 — somente verboso em dois níveis

| Campo | Valor |
|---|---|
| Identificador da tela | `h0037_console_verboso_dois_niveis` |
| JSON estrutural | `config/telas/demo/h0037_console_verboso_dois_niveis.json` |
| Documento externo | `config/telas/demo/h0037_dois_niveis_conteudo.json` |
| Política de modo | `somente_verboso` |
| Modo inicial | NAO_APLICAVEL (único) |
| Chip `[V] Verboso` | ausente |
| Comando de entrada | `python demo/demo.py h0037_console_verboso_dois_niveis` |
| Identidade semântica | string `"H-0037 verboso_dois_niveis"` verificável no documento externo |

O documento externo é o mesmo do cenário 1. As duas telas devem permanecer
estruturalmente distintas e usar políticas diferentes. O compartilhamento prova
que a política pertence à tela, não aos dados.

Formato visual esperado:

```text
identificador 1:  texto longo que pode ocupar várias linhas
identificador 2:  outro texto longo que pode ocupar várias linhas
```

Alinhamento obrigatório (§36.3 da ADR-0028):

```yaml
elementos_medidos: todos_os_identificadores_do_primeiro_nivel
escopo: conteudo_logico_completo_do_cenario
resultado: coluna_comum_para_inicio_do_segundo_nivel
recalculo_por_pagina: proibido
continuacao: mesma_coluna
```

A maior largura dos identificadores do primeiro nível determina a coluna inicial
comum do conteúdo do segundo nível. A coluna permanece estável entre páginas,
não muda com repetição visual de contexto, é usada pelas linhas de continuação
e não se transforma em largura fixa global para outras telas.

Pressionar `V` não altera a tela.

### 13.3 Cenário 3 — alternável em três níveis

| Campo | Valor |
|---|---|
| Identificador da tela | `h0037_console_alternavel_tres_niveis` |
| JSON estrutural | `config/telas/demo/h0037_console_alternavel_tres_niveis.json` |
| Documento externo | `config/telas/demo/h0037_tres_niveis_conteudo.json` |
| Política de modo | `alternavel` |
| Modo inicial | `nao_verboso` |
| Chip `[V] Verboso` | `[V] Verboso` (obrigatório) |
| Comando de entrada | `python demo/demo.py h0037_console_alternavel_tres_niveis` |
| Identidade semântica | string `"H-0037 alternavel_tres_niveis"` verificável |

Estrutura mínima do documento externo:

```text
1. valor
  1.1 valor
      1.1.1 texto longo
```

O conteúdo deve ser suficientemente longo para:

- truncar no modo inicial não verboso;
- ocupar várias linhas no modo verboso;
- preservar designadores, ordem, relações e dados após alternância.

Alternância esperada:

- abre não verbosa;
- primeira ativação de `V` liga o modo verboso;
- segunda ativação retorna ao modo não verboso;
- recarregar a tela restaura o modo inicial não verboso;
- o estado não vaza para outra tela;
- o documento externo não é alterado.

### 13.4 Cenário 4 — tabela alternável

| Campo | Valor |
|---|---|
| Identificador da tela | `h0037_console_tabela_alternavel` |
| JSON estrutural | `config/telas/demo/h0037_console_tabela_alternavel.json` |
| Documento externo | `config/telas/demo/h0037_tabela_conteudo.json` |
| Política de modo | `alternavel` |
| Modo inicial | `verboso` |
| Chip `[V] Verboso` | `[V] Verboso` (obrigatório) |
| Comando de entrada | `python demo/demo.py h0037_console_tabela_alternavel` |
| Identidade semântica | string `"H-0037 tabela_alternavel"` verificável |

Comportamento esperado:

- abre em modo verboso; células longas podem ocupar várias linhas;
- a altura da linha lógica segue a célula mais alta;
- primeira ativação de `V` muda para não verboso;
- no modo não verboso, cada célula aplicável ocupa uma linha física;
- excesso é truncado;
- segunda ativação restaura o modo verboso;
- cabeçalho, colunas, ordem e dados permanecem iguais antes e depois.

### 13.5 Conteúdo compartilhado entre os cenários 1 e 2

O documento externo `h0037_dois_niveis_conteudo.json` é associado a duas telas
estruturalmente distintas com políticas distintas. Esta associação prova que:

```yaml
documento_externo: mesmo
politica_da_tela: diferente
resultado_visual: diferente_conforme_politica
dados: identicos
```

A diferença visual não é causada por troca de dados. A política pertence à tela.

---

## 14. Declaração de política no JSON estrutural

### 14.1 Localização

A política de modo é declarada no JSON **estrutural** da tela, dentro do elemento
`console`, no campo `formato.excesso`:

```json
{
  "tipo": "console",
  "formato": {
    "excesso": {
      "politica_modo": "somente_nao_verboso"
    }
  }
}
```

O documento externo de conteúdo não contém este campo.

### 14.2 Política `somente_nao_verboso` (cenários 1)

```json
{
  "formato": {
    "excesso": {
      "politica_modo": "somente_nao_verboso"
    }
  }
}
```

- `modo_inicial` ausente;
- modo sempre não verboso;
- sem alternância;
- sem chip.

### 14.3 Política `somente_verboso` (cenário 2)

```json
{
  "formato": {
    "excesso": {
      "politica_modo": "somente_verboso"
    }
  }
}
```

- `modo_inicial` ausente;
- modo sempre verboso;
- sem alternância;
- sem chip.

### 14.4 Política `alternavel` com modo inicial não verboso (cenário 3)

```json
{
  "formato": {
    "excesso": {
      "politica_modo": "alternavel",
      "modo_inicial": "nao_verboso"
    }
  }
}
```

- `modo_inicial` obrigatório;
- chip `[V] Verboso` obrigatório;
- `V` alterna.

### 14.5 Política `alternavel` com modo inicial verboso (cenário 4)

```json
{
  "formato": {
    "excesso": {
      "politica_modo": "alternavel",
      "modo_inicial": "verboso"
    }
  }
}
```

- `modo_inicial` obrigatório;
- chip `[V] Verboso` obrigatório;
- `V` alterna.

### 14.6 Restauração do modo inicial

Ao recarregar a tela ou navegar para outro cenário e retornar, o modo inicial
é relido da política declarada no JSON estrutural. O estado de sessão anterior
não persiste.

---

## 15. Validações obrigatórias

O loader ou camada equivalente deve rejeitar documentos inválidos. As validações
abaixo somam-se às 20 da ADR-0027 (`contrato_json_console.md` §12.5).

### 15.1 Validações V-01 a V-15 (ADR-0028)

| Código | Condição | Status |
|---|---|---|
| V-01 | Tabela sem cabeçalho | INVÁLIDO |
| V-02 | Referência a nível filho inexistente | INVÁLIDO |
| V-03 | Múltiplas raízes | INVÁLIDO |
| V-04 | Folha que declara filhos | INVÁLIDO |
| V-05 | Contêiner sem nível filho declarado | INVÁLIDO |
| V-06 | Campo nome–valor sem origem do valor | INVÁLIDO |
| V-07 | Medidas negativas (margens, recuos, vãos, preenchimentos) | INVÁLIDO |
| V-08 | Largura máxima inferior à mínima | INVÁLIDO |
| V-09 | Modo não verboso configurado para mais de uma linha | INVÁLIDO |
| V-10 | Modo verboso sem regra de alinhamento da continuação | INVÁLIDO |
| V-11 | Justificação sem escopo | INVÁLIDO |
| V-12 | Designador composto que depende de ancestral inexistente | INVÁLIDO |
| V-13 | Dados incompatíveis com a estrutura declarada | INVÁLIDO |
| V-14 | Coluna de tabela sem nível ou campo de origem | INVÁLIDO |
| V-15 | Condição excepcional possível sem política explícita declarada | INVÁLIDO |

Fonte: `contrato_json_console.md` §13.9.

### 15.2 Validações D23

O loader deve rejeitar as seguintes combinações para telas novas ou revisadas:

| Condição | Status |
|---|---|
| `politica_modo` ausente em tela nova ou revisada | INVÁLIDO |
| `politica_modo` com valor desconhecido | INVÁLIDO |
| `politica_modo: "alternavel"` sem `modo_inicial` | INVÁLIDO |
| `politica_modo: "alternavel"` com `modo_inicial` de valor desconhecido | INVÁLIDO |
| `politica_modo: "somente_verboso"` com `modo_inicial` presente | INVÁLIDO |
| `politica_modo: "somente_nao_verboso"` com `modo_inicial` presente | INVÁLIDO |
| `politica_modo` declarado no documento externo de conteúdo | INVÁLIDO |

Fonte: `contrato_json_console.md` §13.13.3, §13.13.6.

---

## 16. Comportamento da tecla V

### 16.1 Alternância — exclusiva de telas alternáveis

A tecla `V` atua **somente** em telas com `politica_modo: "alternavel"`:

- primeira ativação: alterna do modo atual para o oposto;
- segunda ativação: retorna ao modo anterior;
- alternância usa os mesmos dados, a mesma tela, o mesmo documento externo;
- não troca a apresentação;
- não persiste alteração;
- não reescreve o JSON externo nem o JSON estrutural.

Em telas com política fixa (`somente_verboso` ou `somente_nao_verboso`), a tecla
`V` não é ação aplicável da tela.

Fonte: ADR-0028 D11, D23; `contrato_console.md` §21.5.

### 16.2 Escopo da alternância

A alternância afeta exclusivamente a instância de `console` com conteúdo
multinível externo da tela corrente. Ela não:

- vaza para outra instância de `console` na mesma tela;
- vaza para outro cenário;
- persiste preferência global.

Fonte: `contrato_console.md` §21.6; `contrato_barra_de_menus.md` §22.4.

### 16.3 Telas fixas

Em telas somente verbosas ou somente não verbosas, a tecla `V` não produz efeito.
O console sem conteúdo multinível externo não expõe nem utiliza a tecla `V`.

### 16.4 Redimensionamento

Após redimensionamento do terminal, o modo visual da sessão é preservado. O
renderizador recalcula a representação física com o modo corrente.

Fonte: `contrato_console.md` §21.8.

---

## 17. Chip `[V] Verboso` na barra de menus

### 17.1 Obrigatoriedade exclusiva nas telas alternáveis H-0037

O chip `[V] Verboso` é obrigatório somente nos JSON estruturais das telas com
`politica_modo: "alternavel"`. A existência do chip é derivada da declaração
no JSON estrutural, não inferida pelo renderizador.

```yaml
h0037_console_nao_verboso:
  chip_V: ausente

h0037_console_verboso_dois_niveis:
  chip_V: ausente

h0037_console_alternavel_tres_niveis:
  chip_V: obrigatorio

h0037_console_tabela_alternavel:
  chip_V: obrigatorio
```

Fonte: `contrato_barra_de_menus.md` §22.1, §22.8; ADR-0028 D23, §23.

### 17.2 Inferência proibida

A presença do chip **não pode ser usada** para inferir a política de modo. A
política vem do JSON estrutural, campo `formato.excesso.politica_modo`.

### 17.3 Formato declarativo

O chip `[V] Verboso` segue o formato de ação declarativa do contrato. O texto
canônico é `"Verboso"` e a tecla é `"V"`. Não exigir alteração dinâmica do
texto do chip.

Fonte: `contrato_barra_de_menus.md` §22.6.

### 17.4 Inaplicabilidade

O chip `[V]` não se aplica a `dashboard`, `lancador`, `console` sem conteúdo
multinível externo, distribuição matricial de nível único, nem telas com política
fixa (`somente_verboso`, `somente_nao_verboso`).

Fonte: `contrato_barra_de_menus.md` §22.5.

### 17.5 Observação não corretiva APLIC-QA-003

As seções 14 e 22 do `contrato_barra_de_menus.md` contêm referências ao chip
`[V]` sem referência cruzada recíproca. Esta coexistência é observação
não corretiva (APLIC-QA-003). O executor não adiciona referências cruzadas nem
altera contratos para resolver esta observação.

---

## 18. Arquivos autorizados para a futura implementação

### 18.1 Criar

```text
config/telas/demo/h0037_console_nao_verboso.json
config/telas/demo/h0037_console_verboso_dois_niveis.json
config/telas/demo/h0037_console_alternavel_tres_niveis.json
config/telas/demo/h0037_console_tabela_alternavel.json

config/telas/demo/h0037_dois_niveis_conteudo.json
config/telas/demo/h0037_tres_niveis_conteudo.json
config/telas/demo/h0037_tabela_conteudo.json

demo/teste_demo_console_modos.py

docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
```

### 18.2 Alterar

```text
tela/loader.py
tela/modelo.py
tela/renderizador.py

tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py

demo/demo.py
demo/teste_demo.py
demo/teste_diagnostico.py
demo/teste_demo_console.py
demo/teste_explorar_barra_de_menus.py

config/telas/demo/demo.json
```

Alterações autorizadas:

- `tela/loader.py`: implementar validação de D23 (`politica_modo`, `modo_inicial`),
  validações V-01–V-15 e lógica de modo inicial a partir da política;
- `tela/modelo.py`: transportar política de modo junto ao conteúdo multinível;
- `tela/renderizador.py`: implementar renderização para modo não verboso e verboso
  conforme política corrente;
- `demo/demo.py`: adicionar as quatro entradas do catálogo e implementar tecla `V`
  exclusiva para telas alternáveis;
- `config/telas/demo/demo.json`: adicionar as quatro entradas dos novos cenários.

### 18.3 Relatórios futuros (mencionar, não autorizar criação)

O executor cria somente `IMP-0037`. Os demais são criados por outras etapas:

```text
docs/relatorios/RELATORIO_QA_H-0037_IMPLEMENTACAO.md
  — criado pelo auditor independente após a implementação

docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0037.md
  — criado após validação em TTY real pelo usuário
```

### 18.4 Proibição de criação de arquivos fora da lista

Qualquer arquivo fora das listas acima exige autorização explícita do usuário
via exceção operacional (§27). Se algum arquivo listado não precisar efetivamente
de alteração, o executor deve registrar isso no relatório de implementação.

---

## 19. Fixtures permanentes: requisitos

### 19.1 JSON estrutural (h0037_console_*.json)

Cada JSON estrutural deve conter:

- `"schema": "tela.v1"`;
- `"id"` igual ao identificador do cenário;
- `"cabecalho"` com `"titulo"` e `"descricao"` identificáveis;
- `"corpo"` com elemento `console` único contendo o campo `formato.excesso.politica_modo`;
- `"barra_de_menus"` com chip `[V] Verboso` somente nas telas alternáveis, e chip `Esc`/Voltar.

O JSON estrutural **não** deve conter:
- dados de runtime do console;
- campo de vínculo para o documento externo;
- resultados físicos calculados;
- `politica_modo` no documento externo.

### 19.2 Documento externo (h0037_*_conteudo.json)

Cada documento externo deve conter:

- `"tipo": "multinivel"`;
- `"formato"` com `"apresentacao"`, `"niveis"` e campos de espaçamento;
- `"dados"` com estrutura compatível com os níveis declarados;
- identidade semântica exclusiva verificável.

O documento externo **não** deve conter:
- `politica_modo`;
- `modo_inicial`;
- `excesso.modo` (campo legado supersedido para telas novas);
- resultados físicos calculados;
- configuração estrutural da tela;
- campo de vínculo para o JSON estrutural.

### 19.3 Dados suficientes para observação em ambos os modos

Os documentos externos devem ter conteúdo suficientemente rico para que:

- no modo não verboso, ao menos uma linha seja truncada;
- no modo verboso, ao menos uma linha se expanda além de uma linha física.

O documento compartilhado (`h0037_dois_niveis_conteudo.json`) deve satisfazer
ambas as condições, pois é usado tanto na tela não verbosa (cenário 1) quanto
na tela verbosa (cenário 2).

### 19.4 Identidade semântica

Strings sugeridas (o executor pode ajustar desde que sejam verificáveis):

```yaml
h0037_console_nao_verboso:           "H-0037 nao_verboso"
h0037_console_verboso_dois_niveis:   "H-0037 verboso_dois_niveis"
h0037_console_alternavel_tres_niveis: "H-0037 alternavel_tres_niveis"
h0037_console_tabela_alternavel:     "H-0037 tabela_alternavel"
```

---

## 20. Associação no `demo.py`

### 20.1 Catálogo

A associação entre JSON estrutural e documento externo é realizada pelo
catálogo `_CATALOGO_CONTEUDO_EXTERNO` em `demo/demo.py`.

Entradas a adicionar:

```python
"h0037_console_nao_verboso":            "h0037_dois_niveis_conteudo",
"h0037_console_verboso_dois_niveis":    "h0037_dois_niveis_conteudo",
"h0037_console_alternavel_tres_niveis": "h0037_tres_niveis_conteudo",
"h0037_console_tabela_alternavel":      "h0037_tabela_conteudo",
```

O compartilhamento de `h0037_dois_niveis_conteudo` entre as duas primeiras
entradas deve ser explícito e verificável nos testes.

### 20.2 Lógica da tecla V

A função `processar_comando` (ou equivalente) deve ser estendida para:

1. reconhecer o comando `"V"` (ou tecla correspondente);
2. verificar se a tela corrente tem `politica_modo: "alternavel"`;
3. somente então alternar o estado de sessão;
4. em telas fixas, ignorar a tecla `V` sem efeito;
5. não persistir o estado além da sessão corrente.

### 20.3 Inicialização do modo

Ao carregar um JSON estrutural com `politica_modo: "alternavel"`, o modo inicial
da sessão para aquela tela é definido pelo campo `modo_inicial` declarado no
mesmo JSON estrutural.

Em telas fixas, o modo é determinado pela política e não pode ser alterado.

### 20.4 Restauração ao trocar de tela

Ao navegar para outra tela e retornar (ou ao recarregar), o modo é relido do
JSON estrutural da tela. O estado de sessão anterior não é preservado entre
navegações.

---

## 21. Demonstração real

### 21.1 Ponto de entrada

```bash
python demo/demo.py <id_tela>
```

Comandos de entrada diretos por cenário:

```bash
python demo/demo.py h0037_console_nao_verboso
python demo/demo.py h0037_console_verboso_dois_niveis
python demo/demo.py h0037_console_alternavel_tres_niveis
python demo/demo.py h0037_console_tabela_alternavel
```

### 21.2 Navegação pelo launcher

O launcher raiz deve conter entradas para os quatro novos cenários H-0037,
permitindo navegação a partir da tela demo raiz.

---

## 22. Testes obrigatórios

### 22.1 Fundamento normativo

Os testes semânticos derivam de ADR-0028 §37, propagado via D-ADR28-D22.

### 22.2 Testes de schema — casos válidos

Os testes devem aceitar:

- `somente_verboso` sem `modo_inicial`;
- `somente_nao_verboso` sem `modo_inicial`;
- `alternavel` com `modo_inicial: "verboso"`;
- `alternavel` com `modo_inicial: "nao_verboso"`;
- telas legadas H-0036 preservadas sem campos D23.

### 22.3 Testes de schema — casos inválidos

Os testes devem rejeitar:

- política ausente em tela nova H-0037;
- política com valor desconhecido;
- política fixa com `modo_inicial` presente;
- `alternavel` sem `modo_inicial`;
- `alternavel` com `modo_inicial` de valor desconhecido;
- tipo incorreto nos campos;
- política declarada no JSON externo de conteúdo;
- chip inferindo política (proibido por construção);
- texto longo inferindo política (proibido por construção);
- `excesso.modo` antigo inferindo política (proibido por construção).

O relatório de implementação deverá mapear cada rejeição ao arquivo e ao teste
correspondente.

### 22.4 Rejeições V-01 a V-15

Os testes devem cobrir casos de rejeição para cada validação V-01 a V-15. Não
basta testar apenas que documentos válidos são aceitos.

| Validação | Cenário de rejeição mínimo |
|---|---|
| V-01 | Tabela sem cabeçalho — rejeitar no cenário de tabela |
| V-02 | Referência a nível filho inexistente |
| V-03 | Múltiplas raízes — comum a todos os cenários |
| V-04 | Folha que declara filhos |
| V-05 | Contêiner sem nível filho declarado |
| V-06 | Campo nome–valor sem origem do valor |
| V-07 | Medida negativa |
| V-08 | Largura máxima inferior à mínima |
| V-09 | Modo não verboso para mais de uma linha |
| V-10 | Modo verboso sem alinhamento de continuação |
| V-11 | Justificação sem escopo |
| V-12 | Designador composto com ancestral inexistente |
| V-13 | Dados incompatíveis com a estrutura — nos cenários de conjuntos |
| V-14 | Coluna de tabela sem origem — no cenário de tabela |
| V-15 | Condição excepcional sem política |

### 22.5 Testes comportamentais — telas fixas

Para os cenários 1 e 2:

- política carregada corretamente do JSON estrutural;
- modo determinado pela política;
- ausência do chip `[V] Verboso`;
- `V` não altera a apresentação;
- ausência de estado alternável;
- dados externos preservados.

### 22.6 Testes comportamentais — telas alternáveis

Para os cenários 3 e 4:

| # | Prova |
|---|---|
| 1 | Qual tela foi aberta (ID do JSON estrutural) |
| 2 | Qual JSON externo foi associado (catálogo) |
| 3 | Qual apresentação foi selecionada (`formato.apresentacao`) |
| 4 | Qual era o modo inicial (lido da política) |
| 5 | Que `V` alterou efetivamente o modo |
| 6 | Que segunda ativação de `V` restaurou o modo anterior |
| 7 | Que os dados não mudaram durante a alternância |
| 8 | Que a troca não vazou para outra tela |
| 9 | Que o comportamento se recupera após redimensionamento |

**Código de saída zero não é prova semântica suficiente** (ADR-0028 §37).

### 22.7 Testes de conteúdo compartilhado

Para os cenários 1 e 2:

```yaml
documento_externo: mesmo (h0037_dois_niveis_conteudo)
politica_da_tela: diferente
resultado_visual: diferente_conforme_politica
dados: identicos
```

### 22.8 Testes de redimensionamento

Provar:

- recálculo no modo atual;
- preservação da política;
- preservação do estado de sessão nas telas alternáveis;
- quadro mínimo quando aplicável;
- recuperação quando o espaço volta;
- ausência de mudança indevida de modo.

### 22.9 Independência dos valores esperados

Os valores esperados nos testes de validação devem ser derivados dos contratos
ativos, não da saída do próprio loader ou renderizador.

---

## 23. Suíte canônica

### 23.1 Baseline verificado (H-0036)

```bash
PYTHONDONTWRITEBYTECODE=1 python tela/teste_loader.py
PYTHONDONTWRITEBYTECODE=1 python tela/teste_modelo.py
PYTHONDONTWRITEBYTECODE=1 python tela/teste_renderizador.py
PYTHONDONTWRITEBYTECODE=1 python tela/teste_distribuicao_matricial.py
PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo.py
PYTHONDONTWRITEBYTECODE=1 python demo/teste_diagnostico.py
PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo_distribuicao.py
PYTHONDONTWRITEBYTECODE=1 python demo/teste_explorar_barra_de_menus.py
PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo_console.py
```

Total baseline: 9 scripts / 2423 verificações / 0 falhas.

O executor deverá medir a baseline real antes de qualquer alteração.

### 23.2 Adição pelo H-0037

Após a implementação, a suíte canônica inclui:

```bash
PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo_console_modos.py
```

O script `demo/teste_demo_console_modos.py` deve cobrir:

- telas fixas (cenários 1 e 2);
- telas alternáveis (cenários 3 e 4);
- comportamento de `V` ausente nas fixas;
- alternância nas alternáveis;
- conteúdo compartilhado entre cenários 1 e 2;
- isolamento entre telas.

A suíte prevista passa a possuir **dez scripts** com a criação deste arquivo.
Não prometer previamente o número final exato de verificações.

### 23.3 Higiene de whitespace

```bash
git diff --check
```

### 23.4 Comando canônico

O comando canônico é `PYTHONDONTWRITEBYTECODE=1 python <script>`, executado
a partir da raiz do projeto. Os scripts são executados diretamente, **não**
via `pytest`.

### 23.5 Obrigações do executor

O executor deve registrar no relatório de implementação:

- comandos exatos executados;
- contagens obtidas em cada script;
- falhas identificadas;
- baseline encontrado antes das alterações;
- baseline final após a implementação;
- justificativa de qualquer alteração no conjunto canônico.

---

## 24. Validação manual

### 24.1 Aplicabilidade

A implementação altera o comportamento visual do console. A validação manual
em TTY real é obrigatória conforme ADR-0028 §38.

### 24.2 Termos usados neste roteiro

- **"console"**: área retangular da interface que exibe o conteúdo.
- **"modo verboso"**: cada conteúdo pode ocupar múltiplas linhas físicas.
- **"modo não verboso"**: cada conteúdo ocupa uma linha física; excedente truncado.
- **"tela fixa"**: tela com política `somente_verboso` ou `somente_nao_verboso`.
- **"tela alternável"**: tela com política `alternavel`.
- **"modo inicial"**: modo com que a tela abre, conforme a política.

### 24.3 Roteiro de validação manual

#### Tela 1 — somente não verbosa

```bash
python demo/demo.py h0037_console_nao_verboso
```

Verificar:

- o texto aparece em uma linha;
- o final cortado mostra `...`;
- o chip `[V] Verboso` não existe na interface;
- pressionar `V` não muda o conteúdo.

---

#### Tela 2 — somente verbosa

```bash
python demo/demo.py h0037_console_verboso_dois_niveis
```

Verificar:

- os textos longos continuam em linhas abaixo;
- os textos do segundo nível começam na mesma coluna (alinhamento estável);
- o chip `[V] Verboso` não existe;
- pressionar `V` não muda a apresentação.

---

#### Tela 3 — alternável em três níveis

```bash
python demo/demo.py h0037_console_alternavel_tres_niveis
```

Verificar:

- inicialmente o texto está truncado (modo não verboso);
- o chip `[V] Verboso` aparece na barra de menus;
- pressionar `V` expande o texto em várias linhas;
- pressionar `V` novamente volta ao estado inicial;
- os níveis `1.`, `1.1` e `1.1.1` permanecem identificáveis antes e depois.

---

#### Tela 4 — tabela alternável

```bash
python demo/demo.py h0037_console_tabela_alternavel
```

Verificar:

- inicialmente as células longas ocupam várias linhas (modo verboso);
- o chip `[V] Verboso` aparece na barra de menus;
- pressionar `V` reduz células a uma linha, truncando quando necessário;
- pressionar `V` novamente volta ao modo inicial;
- cabeçalhos e dados não mudam.

---

#### Telas fixas — confirmar V inerte

Para as telas 1 e 2:

- pressionar `V` várias vezes;
- confirmar que nada muda;
- confirmar que não há erro.

---

#### Telas alternáveis — verificar não persistência

Estando em modo não verboso na tela 3:

- navegar para outra tela e retornar;
- confirmar que a tela 3 reabre no modo inicial não verboso.

---

#### Telas alternáveis — verificar isolamento

Com a tela 3 em modo verboso:

- abrir a tela 4;
- confirmar que a tela 4 abre em modo verboso (conforme sua própria política);
- o estado da tela 3 não contamina a tela 4.

---

#### Regressão H-0036

```bash
python demo/demo.py h0036_console_hierarquia
```

Verificar:

- cenário H-0036 abre normalmente;
- console exibe conteúdo H-0036;
- a tecla `V` não produz efeito inesperado.

---

#### Redimensionamento

Para cada tela:

- maximizar;
- restaurar;
- diminuir;
- aumentar livremente.

Observar:

- estabilidade;
- quadro mínimo quando faltar espaço;
- recuperação quando o espaço voltar;
- preservação do modo e dos dados nas telas alternáveis.

---

### 24.4 Resultado esperado

Todos os passos devem passar. O resultado da validação manual é informado
pelo usuário.

Até o retorno do usuário, usar:

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

O resultado deve ser registrado futuramente em:

```text
docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0037.md
```

---

## 25. Critérios de aceite

### 25.1 Fixtures e política

- [ ] `h0037_console_nao_verboso.json` existe com `politica_modo: "somente_nao_verboso"` e sem chip;
- [ ] `h0037_console_verboso_dois_niveis.json` existe com `politica_modo: "somente_verboso"` e sem chip;
- [ ] `h0037_console_alternavel_tres_niveis.json` existe com `politica_modo: "alternavel"`, `modo_inicial: "nao_verboso"` e chip `[V] Verboso`;
- [ ] `h0037_console_tabela_alternavel.json` existe com `politica_modo: "alternavel"`, `modo_inicial: "verboso"` e chip `[V] Verboso`;
- [ ] `h0037_dois_niveis_conteudo.json` existe sem `politica_modo` nem `modo_inicial`;
- [ ] `h0037_tres_niveis_conteudo.json` existe sem `politica_modo` nem `modo_inicial`;
- [ ] `h0037_tabela_conteudo.json` existe com cabeçalho declarado.

### 25.2 Catálogo e comportamento da tecla V

- [ ] As quatro entradas estão no catálogo `_CATALOGO_CONTEUDO_EXTERNO` do `demo.py`;
- [ ] `h0037_dois_niveis_conteudo` está associado a duas telas distintas;
- [ ] A tecla `V` alterna o modo somente nos cenários 3 e 4;
- [ ] A tecla `V` não produz efeito nos cenários 1 e 2;
- [ ] O modo inicial é lido da política ao abrir cada cenário;
- [ ] Ao trocar de cenário, o modo inicial é restaurado;
- [ ] A alternância não reescreve o documento externo nem o JSON estrutural;
- [ ] A alternância não vaza para outros consoles.

### 25.3 Testes

- [ ] `demo/teste_demo_console_modos.py` existe, cobre telas fixas e alternáveis, e inclui os 9 provas semânticas;
- [ ] Testes de rejeição D23 cobrem todos os casos inválidos listados em §22.3;
- [ ] Testes de rejeição V-01–V-15 cobrem todos os 15 casos;
- [ ] A suíte canônica conta ao menos 10 scripts, verificações acima de 2423, 0 falhas.

### 25.4 Validação manual

- [ ] Os passos do roteiro foram executados e aprovados pelo usuário.

### 25.5 Regressão

- [ ] Os 9 scripts da suíte H-0036 passam sem falhas;
- [ ] Os cenários H-0036 acessíveis pelo launcher continuam funcionando;
- [ ] Nenhuma fixture ou comportamento anterior foi alterado.

### 25.6 Higiene

- [ ] `git diff --check` sem erros;
- [ ] Relatório de implementação criado em `docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md`.

---

## 26. Escopo negativo (fora do escopo)

Estão explicitamente fora do escopo deste handoff:

- criação ou alteração de ADR;
- alteração de contratos ativos;
- alteração da nomenclatura;
- alteração das fixtures H-0036 (`h0036_*.json`);
- conteúdo matricial (`tipo: matriz`);
- distribuição matricial;
- dashboards;
- lançador;
- implementação do script produtor final (Pipeline);
- protocolo de transporte;
- navegação interativa;
- expansão ou recolhimento;
- persistência global;
- edição dos documentos externos;
- migração das telas H-0036;
- nova versão de schema;
- novo default;
- reconciliação terminológica definitiva entre `modo normal` e `modo não verboso`;
- adição de referência cruzada entre seções 14 e 22 do `contrato_barra_de_menus.md`;
- commit;
- push.

---

## 27. Exceção operacional

```text
Se durante a implementação um arquivo fora da lista nominal for estritamente
necessário para cumprir o handoff, preservar a suíte obrigatória ou evitar
a interrupção da entrega, o executor deve parar antes de alterá-lo.

Deve informar:

- arquivo;
- motivo;
- escopo exato;
- mudança esperada.

Somente autorização explícita do usuário permite a alteração.

A autorização não permite introduzir nova semântica, arquitetura ou política.
```

Esta cláusula **somente** se aplica a arquivo técnico inesperadamente necessário.
Ela **não** autoriza o executor a decidir:

- schema semântico (decidido pelas ADRs-0026/0027/0028 com D23);
- validações V-01–V-15 e campos D23 (decididas pelas ADRs e contratos);
- forma dos nós ou níveis (decidida por `contrato_json_console.md` §12);
- apresentações previstas (definidas por `contrato_json_console.md` §13.4);
- localização geral das fixtures (definida em §12);
- responsabilidade do `demo.py` (definida pela ADR-0027 D2, D7);
- campos canônicos D23 (`politica_modo`, `modo_inicial`) — decididos.

Não usar essa exceção para omissões já conhecidas. Os arquivos técnicos
conhecidos devem estar nominalmente listados em §18.

---

## 28. Condições de bloqueio

Parar com:

```text
BLOCKED_DOCUMENTATION
```

se: faltar contrato indispensável; existir contradição normativa ativa; não for
possível listar nominalmente os arquivos necessários; a implementação exigir
alterar autoridade documental; a capacidade exigir decidir semântica não fechada
sem autorização.

Parar com:

```text
BLOCKED_EVIDENCE
```

se: não for possível confirmar arquivos, ponto de entrada ou suíte; os arquivos
técnicos citados não existirem no repositório.

Não completar lacunas silenciosamente. Não inventar arquitetura. Não criar
permissões genéricas.

---

## 29. Relatório de implementação

Autorizado a criar:

```text
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
```

O relatório deve registrar:

1. identificação e handoff executado;
2. autoridades;
3. estado Git inicial;
4. baseline medido antes das alterações;
5. arquivos alterados e criados;
6. implementação por camada;
7. campos D23 (`politica_modo`, `modo_inicial`) — localização e validação;
8. matriz de validade implementada (10 entradas);
9. tratamento do campo antigo `excesso.modo` (legado, não usado nos H-0037);
10. quatro telas com políticas distintas;
11. três documentos externos de conteúdo;
12. conteúdo compartilhado entre cenários 1 e 2;
13. barra de menus — chip apenas nas alternáveis;
14. tecla `V` — exclusiva das alternáveis;
15. testes de rejeição D23 (cada caso mapeado ao arquivo e teste);
16. testes de rejeição V-01–V-15 (cada caso mapeado);
17. testes comportamentais — telas fixas;
18. testes comportamentais — telas alternáveis;
19. suíte canônica — comandos, contagens, falhas;
20. identidade semântica verificável;
21. regressão H-0036;
22. redimensionamento automatizável;
23. pendência de TTY real (`VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO`);
24. exceções autorizadas;
25. limitações conhecidas;
26. diff final;
27. `git diff --check`.

O executor **não pode** declarar aprovação formal da própria implementação.

---

## 30. Arquivos preservados ou proibidos

### 30.1 Preservados sem alteração pela futura implementação

```text
docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md
docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
docs/relatorios/RELATORIO_QA_ADR-0028.md
docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0028.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0028.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0028.md
docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0028.md
docs/relatorios/RELATORIO_QA_ADR-0028_REVISAO_MODOS_POR_TELA.md
docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0028_REVISAO_MODOS_POR_TELA.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md
docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md
docs/relatorios/RELATORIO_QA_H-0037_HANDOFF.md
docs/contratos/contrato_json_console.md
docs/contratos/contrato_console.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_json_dashboard.md
docs/contratos/contrato_json_lancador.md
docs/contratos/contrato_lancador.md
docs/NOMENCLATURA.md
docs/adr/INDICE_ADR.md
docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md
docs/relatorios/IMP-0036-fornecimento-externo-dados-console-json-multinivel.md
config/telas/demo/h0036_console_hierarquia.json
config/telas/demo/h0036_hierarquia_conteudo.json
config/telas/demo/h0036_console_tabela.json
config/telas/demo/h0036_tabela_conteudo.json
config/telas/demo/h0036_console_conjuntos.json
config/telas/demo/h0036_conjuntos_conteudo.json
config/telas/demo/h0035_console_com.json
config/telas/demo/h0035_console_sem.json
config/telas/demo/h0035_console_com_conteudo.json
config/telas/demo/h0035_console_sem_conteudo.json
tela/distribuicao_matricial.py
tela/teste_distribuicao_matricial.py
demo/demo_distribuicao.py
demo/diagnostico.py
demo/explorar_barra_de_menus.py
demo/teste_demo_distribuicao.py
```

Também preservados: todos os arquivos `h0029_*`, `h0030_*`, `h0035_*`;
demais ADRs, contratos, índices, handoffs históricos e relatórios históricos;
qualquer arquivo não relacionado ao console multinível ou à política de modo.

### 30.2 Compatibilidade H-0036

As telas legadas H-0036:

```text
h0036_console_hierarquia
h0036_console_tabela
h0036_console_conjuntos

h0036_hierarquia_conteudo
h0036_tabela_conteudo
h0036_conjuntos_conteudo
```

- não recebem campos D23 (`politica_modo`, `modo_inicial`);
- não são reinterpretadas automaticamente como uma das três políticas;
- não são migradas;
- não passam a exibir `[V] Verboso`;
- devem continuar funcionando como antes.

O teste de regressão deve comprovar a preservação.

### 30.3 Comportamentos preservados

- O placeholder `"(console)"` permanece ativo quando não houver conteúdo externo.
- Os cenários H-0036 permanecem funcionais e sem regressão.
- A capacidade `distribuicao_matricial` (ADR-0025, H-0035) permanece inalterada.
- Dashboard e lançador não participam da alternância verbosa.
- Nenhuma migração automática das telas existentes.

### 30.4 Proibições explícitas na futura implementação

- Não alterar ADR-0028 nem contratos aplicados.
- Não alterar fixtures do H-0036 nem do H-0035.
- Não implementar o script produtor final.
- Não definir comportamento padrão quando `politica_modo` está ausente em telas novas.
- Não implementar navegação, seleção, expansão, recolhimento ou paginação interativa.
- Não reinserir conteúdo de runtime no JSON estrutural.
- Não persistir o estado de modo além da sessão.
- Não fazer stage nem commit.

---

## 31. Verificação de coerência

| # | Verificação | Resultado |
|---|---|---|
| 1 | ADR-0028 aceita e aplicada, incluindo D23 | Confirmado |
| 2 | Próxima categoria autorizada é PATCH_HANDOFF → IMPLEMENTAR | Confirmado |
| 3 | Quatro cenários de demonstração com políticas distintas | Confirmado |
| 4 | `politica_modo` é o campo canônico no JSON estrutural | Confirmado |
| 5 | `modo_inicial` obrigatório apenas em `alternavel` | Confirmado |
| 6 | Chip `[V] Verboso` exclusivo das telas alternáveis | Confirmado |
| 7 | Tecla `V` exclusiva das telas alternáveis | Confirmado |
| 8 | Documento externo não contém política de modo | Confirmado |
| 9 | Conteúdo compartilhado entre cenários 1 e 2 | Confirmado |
| 10 | Alinhamento de dois níveis determinístico (escopo `conteúdo completo`) | Confirmado |
| 11 | Sete arquivos de fixture nomeados | Confirmado |
| 12 | Todos os arquivos técnicos necessários autorizados | Confirmado |
| 13 | Todos os casos inválidos possuem prova de rejeição exigida | Confirmado |
| 14 | Relatórios posteriores nominalmente separados | Confirmado |
| 15 | Suíte futura possui `teste_demo_console_modos.py` | Confirmado |
| 16 | Roteiro manual direto e reproduzível para as quatro telas | Confirmado |
| 17 | H-0036 permanece preservado | Confirmado |
| 18 | Sem conteúdo matricial no escopo | Confirmado |
| 19 | Sem integração concreta com Pipeline | Confirmado |
| 20 | Sem autorização de commit | Confirmado |
| 21 | Fixtures H-0036 nominalmente listadas como preservadas | Confirmado |
| 22 | `excesso.modo` antigo não é forma canônica para H-0037 | Confirmado |
| 23 | Baseline: 9 scripts / 2423 verificações / 0 falhas | Confirmado |
| 24 | Comando canônico é execução direta (não pytest) | Confirmado |

---

## 32. Estado do handoff

```yaml
status: AGUARDANDO_QA
criado_em: "2026-07-17"
patched_em: "2026-07-18"
motivo_do_patch: incorporacao_de_D23_e_correccoes_de_completude_QA_H-0037
proximo_passo: QA_POS_PATCH_HANDOFF
```

(Fim do handoff)
