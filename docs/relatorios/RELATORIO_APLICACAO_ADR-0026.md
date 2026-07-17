# Relatório de Aplicação da ADR-0026

## 1. Identificação

| Campo | Valor |
|---|---|
| **Identificador do Relatório** | RELATORIO_APLICACAO_ADR-0026 |
| **Data de Execução** | 2026-07-17 |
| **ADR Aplicada** | ADR-0026 — Fornecimento externo de dados ao console por JSON multinível |
| **Arquivo da ADR** | `docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md` |
| **QA de Referência** | `docs/relatorios/RELATORIO_QA_ADR-0026.md` |
| **Classificação QA** | `ADR_APPROVED` — 0 achados em todas as severidades |
| **Categoria executada** | `APLICAR_ADR` |
| **Etapa anterior concluída** | H-0035 / ADR-0025, commit `fb9e5be`, branch `master` |

---

## 2. Escopo da aplicação

Esta etapa executa exclusivamente `APLICAR_ADR`: propaga às autoridades
normativas ativas as 13 decisões aprovadas pela ADR-0026. A aplicação é
estritamente documental.

**Não está no escopo desta etapa:**

- implementação de código;
- QA da aplicação;
- alteração da decisão arquitetural;
- completar decisões deferidas;
- criar handoff;
- reservar número de handoff;
- criar commit;
- criar novo contrato, schema ou exemplo permanente com nome não aprovado;
- inventar campo de vínculo ainda não decidido;
- inventar protocolo de script;
- transformar o tipo matricial em escopo obrigatório.

---

## 3. Estado inicial do repositório (antes das edições)

```yaml
branch: master
commit_head: fb9e5be
workspace: LIMPO
stage: VAZIO
arquivos_untracked_esperados:
  - docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
  - docs/relatorios/RELATORIO_QA_ADR-0026.md
arquivos_alterados_anteriores: nenhum
```

O estado inicial foi confirmado por `git status` antes de qualquer edição,
correspondendo exatamente ao estado declarado no `RELATORIO_QA_ADR-0026.md`.

---

## 4. Autoridades lidas nesta etapa

| Documento | Tipo | Papel nesta aplicação |
|---|---|---|
| `docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md` | ADR | Autoridade primária — decisões a propagar |
| `docs/relatorios/RELATORIO_QA_ADR-0026.md` | Relatório QA | Confirmação de classificação `ADR_APPROVED` e lista de documentos afetados |
| `docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md` | ADR | Autoridade anterior — confirmar preservação |
| `docs/adr/INDICE_ADR.md` | Índice | Alvo de atualização — formato a seguir |
| `docs/NOMENCLATURA.md` | Glossário | Alvo de atualização — seções 1–16 lidas integralmente |
| `docs/contratos/contrato_tela_json.md` | Contrato | Alvo de atualização — 1247 linhas lidas integralmente |
| `docs/contratos/contrato_console.md` | Contrato | Alvo de atualização — 517 linhas lidas integralmente |
| `docs/contratos/contrato_json_console.md` | Contrato | Alvo de atualização — 385 linhas lidas integralmente |
| `docs/contratos/contrato_composicao_corpo.md` | Contrato | Avaliado — 1856 linhas lidas integralmente — preservado |
| `docs/contratos/contrato_json_dashboard.md` | Contrato | Avaliado — 368 linhas lidas integralmente — preservado |
| `docs/contratos/contrato_json_lancador.md` | Contrato | Avaliado — 314 linhas lidas integralmente — preservado |
| `docs/contratos/contrato_lancador.md` | Contrato | Avaliado — 592 linhas lidas integralmente — preservado |

---

## 5. Decisões propagadas

As 13 decisões da seção 6 da ADR-0026 foram propagadas aos documentos
normativos conforme descrito nas seções seguintes deste relatório.

| # | Decisão (ADR-0026, seção 6) | Propagada em |
|---|---|---|
| D1 | O conteúdo de runtime do console terá origem externa | NOMENCLATURA §17.1, contrato_console §19.1, contrato_json_console §11.1 |
| D2 | O JSON estrutural da tela não será o repositório desses dados de runtime | contrato_tela_json §31.1, NOMENCLATURA §17.1 |
| D3 | O console receberá os dados por meio de um JSON externo | contrato_json_console §11.1, contrato_console §19.1 |
| D4 | O documento externo seguirá um envelope declarativo | contrato_json_console §11.2, NOMENCLATURA §17.1 |
| D5 | O formato inicial de interesse é `tipo: "multinivel"` | contrato_json_console §11.3, NOMENCLATURA §17.1 |
| D6 | O bloco `formato` descreve a intenção de apresentação | contrato_json_console §11.2, NOMENCLATURA §17.1 |
| D7 | O bloco `dados` contém a estrutura semântica | contrato_json_console §11.2, NOMENCLATURA §17.1 |
| D8 | Os níveis são declarados explicitamente | contrato_json_console §11.3, NOMENCLATURA §17.1 |
| D9 | Os dados chegam previamente estruturados para a apresentação multinível | contrato_json_console §11.3, contrato_console §19.2 |
| D10 | O consumidor não reconstrói, descobre nem infere a hierarquia | contrato_console §19.3, contrato_json_console §11.3, NOMENCLATURA §17.4 |
| D11 | O renderizador continua calculando geometria, dimensões, quebras, truncamentos, alinhamentos, paginação, posições e recuperação | contrato_console §19.4, contrato_json_console §11.4, NOMENCLATURA §17.3 |
| D12 | No sistema final, um script produzirá ou devolverá o documento de dados | contrato_console §19.5, INDICE_ADR linha ADR-0026 |
| D13 | O contrato de invocação do script permanece para decisão futura | contrato_console §19.7, contrato_json_console §11.8 |

---

## 6. Princípio normativo central

O princípio normativo central da ADR-0026 foi propagado de forma literal nos
seguintes pontos:

```text
O JSON externo declara a intenção de apresentação e o conteúdo semântico.
O renderizador calcula a representação física na área disponível.
```

| Local | Seção |
|---|---|
| `docs/NOMENCLATURA.md` | §17.2 |
| `docs/contratos/contrato_tela_json.md` | §31.5 |
| `docs/contratos/contrato_console.md` | §19.6 |
| `docs/contratos/contrato_json_console.md` | §11.5 |

---

## 7. Documentos alterados

### 7.1 `docs/adr/INDICE_ADR.md`

**Alteração:** Adicionada linha da ADR-0026 após a linha da ADR-0025.

**Formato seguido:** idêntico ao da ADR-0025 (`aceita e aplicada`, data
`2026-07-17`, título com as decisões-chave resumidas).

**Linhas adicionadas:** 1

---

### 7.2 `docs/NOMENCLATURA.md`

**Alteração:** Adicionada seção 17 — "Fornecimento externo de dados ao console
por JSON multinível (ADR-0026)" — após a seção 16.5 (fim da seção 16, ADR-0025).

**Subseções criadas:**

| Subseção | Conteúdo |
|---|---|
| §17.1 | Termos fundamentais (13 termos normalizados) |
| §17.2 | Princípio normativo central com lista de conteúdo proibido no documento externo |
| §17.3 | Fronteiras de responsabilidade (5 componentes) |
| §17.4 | Distinções obrigatórias (5 pares) |
| §17.5 | Decisões deferidas (9 itens não são termos ativos) |

**Termos canonizados:**

- `JSON estrutural da tela`
- `JSON externo de conteúdo`
- `conteúdo de runtime do console`
- `conteúdo multinível`
- `envelope declarativo`
- `bloco tipo`
- `bloco formato`
- `bloco dados`
- `níveis declarados`
- `produtor de dados` (futuro)
- `consumidor`
- `representação semântica`
- `representação física calculada`

**Linhas adicionadas:** 83

---

### 7.3 `docs/contratos/contrato_tela_json.md`

**Alterações:**

1. **Frontmatter `adrs_aplicadas`**: adicionada
   `docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md`.

2. **Seção 31**: "Fronteira entre JSON estrutural da tela e conteúdo externo
   do console (ADR-0026)" adicionada após a seção 30.9.

**Subseções criadas:**

| Subseção | Conteúdo |
|---|---|
| §31.1 | Responsabilidade do JSON estrutural — não é repositório de runtime |
| §31.2 | Origem externa do conteúdo com envelope conceitual mínimo |
| §31.3 | Vínculo entre tela e fonte — explicitamente não decidido |
| §31.4 | Responsabilidades preservadas do tela.json |
| §31.5 | Princípio normativo (literal da ADR-0026) |
| §31.6 | Remissões cruzadas |

**Linhas adicionadas:** 66

---

### 7.4 `docs/contratos/contrato_console.md`

**Alterações:**

1. **Frontmatter `adrs_aplicadas`**: adicionada
   `docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md`.

2. **Seção 19**: "Fronteira do console como consumidor de conteúdo externo
   (ADR-0026)" adicionada após a seção 18.

**Subseções criadas:**

| Subseção | Conteúdo |
|---|---|
| §19.1 | Conteúdo de runtime tem origem externa |
| §19.2 | Conteúdo chega previamente estruturado |
| §19.3 | Fronteira do consumidor — proibições e limites |
| §19.4 | Fronteira do renderizador — responsabilidades exclusivas |
| §19.5 | Integração com o script produtor (protocolo não decidido) |
| §19.6 | Princípio normativo (literal da ADR-0026) |
| §19.7 | Decisões deferidas — lista explícita |
| §19.8 | Remissões cruzadas |

**Linhas adicionadas:** 77

---

### 7.5 `docs/contratos/contrato_json_console.md`

**Alterações:**

1. **Frontmatter `adrs_aplicadas`**: adicionada
   `docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md`.

2. **Seção 11**: "Envelope declarativo do documento externo de conteúdo
   (ADR-0026)" adicionada após a seção 10.5.

**Subseções criadas:**

| Subseção | Conteúdo |
|---|---|
| §11.1 | JSON estrutural × documento externo — distinção explícita |
| §11.2 | Envelope declarativo mínimo com tabela de responsabilidades por bloco |
| §11.3 | Foco inicial: `tipo: "multinivel"` e obrigação de níveis declarados |
| §11.4 | Restrição: lista de conteúdo proibido no documento externo |
| §11.5 | Princípio normativo (literal da ADR-0026) |
| §11.6 | Campo `origem_dados` — explicitamente não declarado como vínculo final |
| §11.7 | Compatibilidade com JSONs existentes |
| §11.8 | Decisões deferidas — lista explícita |
| §11.9 | Remissões cruzadas |

**Linhas adicionadas:** 95

---

## 8. Documentos preservados

### 8.1 `docs/contratos/contrato_composicao_corpo.md`

**Status:** Preservado sem alteração.

**Razão:** Leitura integral (1856 linhas) não identificou formulação que
confundisse composição estrutural do corpo com conteúdo de runtime do console
nem que atribuísse ao compositor responsabilidade de reconstrução de hierarquia.
A linha 476 ("conteúdo e campos vêm da instância declarada no `tela.json`")
refere-se ao `dashboard`, não ao `console`, e trata de campos estruturais
declarativos — sem conflito com a ADR-0026.

---

### 8.2 `docs/contratos/contrato_json_dashboard.md`

**Status:** Preservado sem alteração.

**Razão:** O contrato é específico ao `dashboard`. Não contém referências de
origem de dados de runtime que conflitem com a ADR-0026. A seção 9 (ADR-0025)
permanece intacta.

---

### 8.3 `docs/contratos/contrato_json_lancador.md`

**Status:** Preservado sem alteração.

**Razão:** O contrato é específico ao `lancador`. Não contém vocabulário de
origem de conteúdo que conflite com a ADR-0026. A seção 9 (ADR-0025) permanece
intacta.

---

### 8.4 `docs/contratos/contrato_lancador.md`

**Status:** Preservado sem alteração.

**Razão:** O contrato define comportamento do `lancador`. Não contém
referências a script produtor, JSON externo de conteúdo nem fronteiras de
consumidor que precisassem ser reconciliadas com a ADR-0026.

---

### 8.5 `docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md`

**Status:** Preservado sem alteração.

**Razão:** Autoridade primária desta etapa. Não deve ser editada em
`APLICAR_ADR`.

---

### 8.6 `docs/relatorios/RELATORIO_QA_ADR-0026.md`

**Status:** Preservado sem alteração.

**Razão:** Relatório de QA de referência. Não deve ser alterado pela aplicação.

---

### 8.7 `docs/adr/ADR-0025-*` e demais ADRs anteriores

**Status:** Preservados sem alteração.

**Razão:** ADRs aceitas não são editadas quando uma nova ADR é aceita. A
ADR-0026 não substitui nenhuma ADR anterior.

---

### 8.8 `config/telas/`, `config/telas/demo/`, `demo/`

**Status:** Preservados sem alteração.

**Razão:** A ADR-0026 explicitamente lista esses artefatos como alvos de
reconciliação futura ("quando o fluxo estiver operacional"), não desta etapa
de aplicação documental.

---

## 9. Busca de resíduos

Foram buscadas formulações que pudessem indicar conteúdo de runtime embutido
no JSON estrutural, hierarquia inferida pelo consumidor, ou responsabilidade
geométrica atribuída ao documento externo.

### 9.1 Termos pesquisados

- `dados codificados no JSON`
- `conteúdo embutido`
- `hierarquia inferida`
- `inferir hierarquia`
- `reconstruir hierarquia`
- `conteúdo hardcoded`
- `conteúdo.*tela\.json`

### 9.2 Resultado

**Nenhum resíduo conflitante encontrado** nos documentos normativos alterados
e nos documentos preservados avaliados.

As únicas ocorrências dos termos de busca encontradas são:

1. Seção §17 da NOMENCLATURA.md, coluna "Não confundir com" de
   `consumidor / loader`: expressão "reconstruir hierarquia" aparece como
   proibição explícita, não como formulação ativa concorrente.

2. Seção §17.4 da NOMENCLATURA.md, distinção `níveis declarados × hierarquia
   inferida`: aparece como distinção normativa proibitiva.

Ambas as ocorrências são formulações normativas corretas produzidas por esta
aplicação, não resíduos de formulações anteriores.

---

## 10. Limite de aplicação respeitado

A aplicação não inventou nenhum dos seguintes itens, que permanecem para
decisão futura conforme a ADR-0026:

| Item não decidido | Confirmação |
|---|---|
| Nome do campo de vínculo entre tela e fonte | Não inventado — seções §31.3, §11.6 registram a não-decisão |
| Protocolo de comunicação com o script | Não inventado — seções §19.5, §11.8 registram a não-decisão |
| Assinatura, argumentos, códigos de saída do script | Não inventados |
| Execução síncrona ou assíncrona | Não decidida |
| Caminho e ciclo de vida do documento externo | Não decididos |
| APIs, classes e módulos do consumidor/loader | Não decididos |
| Suporte ao `tipo: "matriz"` na primeira implementação | Não mandatado |
| Comportamento diante de fonte ausente ou inválida | Não decidido |
| Navegação, seleção, expansão, recolhimento | Não decididos |
| Paginação interativa de conteúdo multinível | Não decidida |

---

## 11. Compatibilidade com ADR-0025 e H-0035

- A ADR-0025 (distribuição matricial configurável de nível único) permanece
  vigente e não foi alterada por esta aplicação.
- O H-0035 permanece fechado, commit `fb9e5be` intocado.
- A seção 10 de `contrato_json_console.md` (ADR-0025) foi preservada
  integralmente; a nova seção 11 (ADR-0026) foi adicionada após ela.
- A distinção `nível único × multinível` (NOMENCLATURA §16.3) foi
  complementada pela nova seção 17 sem contradição.

---

## 12. Remissões cruzadas criadas

Todas as seções adicionadas contêm remissões explícitas entre si, formando
uma rede coerente de referências cruzadas:

| Documento / Seção | Aponta para |
|---|---|
| NOMENCLATURA §17 | — (referência terminológica de chegada) |
| contrato_tela_json §31.6 | contrato_json_console §11; contrato_console §19; NOMENCLATURA §17 |
| contrato_console §19.8 | contrato_json_console §11; contrato_tela_json §31; NOMENCLATURA §17 |
| contrato_json_console §11.9 | contrato_console §19; contrato_tela_json §31; NOMENCLATURA §17 |
| INDICE_ADR | ADR-0026 (linha de índice) |

---

## 13. Estado final do repositório (após edições)

```yaml
branch: master
commit_head: fb9e5be
workspace: SUJO (5 arquivos modificados, não commitados)
stage: VAZIO
arquivos_modificados:
  - docs/NOMENCLATURA.md
  - docs/adr/INDICE_ADR.md
  - docs/contratos/contrato_console.md
  - docs/contratos/contrato_json_console.md
  - docs/contratos/contrato_tela_json.md
arquivos_untracked:
  - docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
  - docs/relatorios/RELATORIO_QA_ADR-0026.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md
commit: NÃO REALIZADO (fora do escopo desta etapa)
```

---

## 14. Achados

Nenhum achado de severidade bloqueante, alta, média ou baixa foi identificado
durante esta aplicação documental.

Nenhum documento normativo apresentou formulação ativa que conflitasse com as
decisões da ADR-0026. Nenhum resíduo normativo concorrente foi encontrado.
Nenhuma decisão deferida foi antecipada ou inventada.

---

## 15. Patch da aplicação (PATCH_APLICACAO_ADR)

### 15.1 Identificação do patch

```yaml
etapa: PATCH_APLICACAO_ADR
data: "2026-07-17"
qa_de_origem: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0026.md
achados_corrigidos:
  - QAAPADR-0026-001
  - QAAPADR-0026-002
arquivos_corrigidos:
  - docs/contratos/contrato_tela_json.md
  - docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
```

### 15.2 Correção de QAAPADR-0026-001

**Arquivo:** `docs/contratos/contrato_tela_json.md`

**Problema:** A linha `A especificação normativa completa está na ADR-0025.` aparecia
como última linha do arquivo, imediatamente após o último bullet de §31.6, sem linha em
branco separadora. O QA identificou que essa linha era o encerramento do bloco de
remissões da seção 30 (ADR-0025), que havia permanecido como última linha do arquivo
antes da inserção de §31 na etapa `APLICAR_ADR`. Após a inserção, a linha ficou
deslocada, aparecendo como continuação de §31.6 (seção sobre ADR-0026) com referência
à ADR-0025.

**Correção aplicada:** A linha foi removida. A remoção foi autorizada pois a frase
estava deslocada do seu contexto semântico original e era redundante: §31.6 já provê
as remissões necessárias para o conteúdo da ADR-0026 (`contrato_json_console.md` §11,
`contrato_console.md` §19, `docs/NOMENCLATURA.md` §17), e a seção 30.9 já contém
referências às autoridades da ADR-0025 (`A terminologia canônica está em
docs/NOMENCLATURA.md seção 16`).

**Linha removida:** `A especificação normativa completa está na ADR-0025.`

**Novo último conteúdo de §31.6 (após correção):**
```
- `docs/NOMENCLATURA.md` — seção 17: terminologia canônica da ADR-0026.
```

### 15.3 Correção de QAAPADR-0026-002

**Arquivo:** `docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md`

**Problema:** O arquivo da ADR-0026 continha `status: aceita` no frontmatter YAML,
na tabela de identificação (seção 1) e na seção 2. O `INDICE_ADR.md` registrava a
ADR-0026 com status `aceita e aplicada`. Inconsistência de rastreabilidade: arquivo
da ADR e índice declaravam estados diferentes.

**Correção aplicada:** Atualizados os três campos de status no arquivo da ADR-0026:

| Local | Antes | Depois |
|---|---|---|
| Frontmatter YAML (`metadata.status`) | `aceita` | `aceita e aplicada` |
| Tabela de identificação (seção 1) | `aceita` | `aceita e aplicada` |
| Seção 2 | `` `aceita` `` | `` `aceita e aplicada` `` |

Precedente seguido: ADR-0025 contém `status: aceita e aplicada` em todos os campos
correspondentes.

### 15.4 Verificações executadas

- Frase órfã não permanece em §31.6 de `contrato_tela_json.md`. ✓
- Não há separação de Markdown incorreta no final de §31.6 após a remoção. ✓
- A ADR-0026 contém `status: aceita e aplicada` nos três campos (frontmatter,
  tabela, seção 2). ✓
- O `INDICE_ADR.md` permanece coerente com a ADR (ambos com `aceita e aplicada`). ✓
- Nenhuma decisão deferida foi alterada. ✓
- Nenhuma regra normativa além dos dois achados foi modificada. ✓
- Nenhum relatório de QA foi alterado. ✓
- Nenhum arquivo fora da lista autorizada foi alterado. ✓
- Nenhum arquivo foi colocado no stage. ✓
- Nenhum commit foi realizado. ✓
- `git diff --check`: sem erros de whitespace. ✓

### 15.5 Bloqueios

Nenhum bloqueio encontrado. As correções foram aplicadas sem necessidade de nova
decisão arquitetural ou normativa.

---

## 16. Classificação final

```yaml
status_literal: APLICACAO_CONCLUIDA
status_normalizado: Aplicação documental da ADR-0026 concluída sem achados
relatorio: docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md
adr_aplicada: docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
documentos_alterados: 5
documentos_preservados: 8
linhas_adicionadas_total: 322
achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 0
residuos_conflitantes: 0
decisoes_deferidas_inventadas: 0
campos_de_vinculo_inventados: 0
protocolos_inventados: 0
commit: nao_realizado
proxima_categoria: aguarda_instrucao_do_usuario
```
