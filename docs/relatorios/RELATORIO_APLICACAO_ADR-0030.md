---
name: relatorio-aplicacao-adr-0030
description: Relatório factual da aplicação documental da ADR-0030 — carregamento global e materialização do estilo; registra arquivos alterados, decisões propagadas, inspeções e estado final
metadata:
  type: relatorio
  etapa: APLICAR_ADR
  adr: ADR-0030
  data: "2026-07-22"
---

# Relatório — Aplicação documental da ADR-0030

## 1. Identificação

| Campo | Valor |
|---|---|
| Etapa | APLICAR_ADR |
| ADR | ADR-0030 — Carregamento global e materialização do estilo |
| Data | 2026-07-22 |
| Agente | Aplicação documental automatizada |
| Resultado | CONCLUIDA |

---

## 2. Estado inicial

```yaml
adr_status_antes: proposta
encerramento_transitorio: DOCUMENTATION_PATCHED_AWAITING_QA
indice_adr_entrada_adr_0030: ausente
contrato_estilo_adrs_aplicadas: sem_ADR-0030
modulo_10_ESTILO_termos_preset_catalogo: ausentes
modulo_10_ESTILO_materializacao: ausente
contrato_estilo_secao_3_1_preset_default: ausente
contrato_estilo_secao_3_2_caixa_alta: "true_como_default_global_errado"
contrato_estilo_secoes_3_6_3_7: ausentes
contrato_estilo_regras_R9_R10: ausentes
contrato_estilo_validacoes_D9: ausentes
```

---

## 3. Autoridade de aprovação

```yaml
arquivo: docs/relatorios/RELATORIO_CORRECAO_ENCERRAMENTO_QA_POS_PATCH_02_ADR-0030.md
status_canonico: ADR_APPROVED
achado_final:
  id: QA-POS-ADR0030-001
  status: RESOLVIDO
regressoes: false
achados_novos: []
bloqueios: []
```

---

## 4. Cadeia histórica lida

Todos os relatórios históricos foram lidos como documentos somente leitura.
Nenhum foi alterado.

| Arquivo | Papel |
|---|---|
| `docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md` | Fonte normativa das decisões D1–D13 |
| `docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md` | Levantamento do estado material atual |
| `docs/relatorios/RELATORIO_QA_ADR-0030.md` | QA inicial da ADR |
| `docs/relatorios/RELATORIO_PATCH_ADR-0030.md` | Primeiro patch da ADR |
| `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0030.md` | QA pós-primeiro patch |
| `docs/relatorios/RELATORIO_PATCH_02_ADR-0030.md` | Segundo patch focal (correção de literal "padrao" → "padrão") |
| `docs/relatorios/RELATORIO_QA_POS_PATCH_02_ADR-0030.md` | QA pós-segundo patch |
| `docs/relatorios/RELATORIO_CORRECAO_ENCERRAMENTO_QA_POS_PATCH_02_ADR-0030.md` | Encerramento canônico — ADR_APPROVED |

---

## 5. Arquivos autorizados

### 5.1 Alteração obrigatória executada

| Arquivo | Alterado |
|---|---|
| `docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md` | Sim |
| `docs/adr/INDICE_ADR.md` | Sim |
| `docs/contratos/contrato_estilo.md` | Sim |

### 5.2 Alteração condicional

| Arquivo | Inspecionado | Alterado | Resultado |
|---|---|---|---|
| `docs/contratos/contrato_chip.md` | Sim | Não | INSPECIONADO_E_PRESERVADO |
| `docs/contratos/contrato_barra_de_menus.md` | Sim | Não | INSPECIONADO_E_PRESERVADO |
| `docs/contratos/contrato_console.md` | Sim | Não | INSPECIONADO_E_PRESERVADO |
| `docs/nomenclatura/10_ESTILO.md` | Sim | Sim | ATUALIZADO |
| `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` | Sim | Não | INSPECIONADO_E_PRESERVADO |
| `docs/nomenclatura/32_CONSOLE.md` | Sim | Não | INSPECIONADO_E_PRESERVADO |

### 5.3 Arquivo novo criado

| Arquivo | Status |
|---|---|
| `docs/relatorios/RELATORIO_APLICACAO_ADR-0030.md` | Criado (este arquivo) |

---

## 6. Decisões D1–D13 propagadas

| Decisão | Documento de destino | Evidência da propagação | Resultado |
|---|---|---|---|
| D1 — Autoridade global exclusiva | `contrato_estilo.md` §2 | Nova seção "Regra fundamental e autoridade global" — consumidores, escolha global, proibição per-tela | PROPAGADA |
| D1 — Autoridade global exclusiva | `docs/nomenclatura/10_ESTILO.md` §4.9 | Nova seção "Configuração de aparência vs estado vivo" | PROPAGADA |
| D1 — Autoridade global exclusiva | `docs/adr/INDICE_ADR.md` | Entrada ADR-0030 com "autoridade global exclusiva" | PROPAGADA |
| D2 — Catálogo + `preset_default` | `contrato_estilo.md` §3.1 | "Catálogo e opção ativa" em borda — `borda.preset_default` obrigatório | PROPAGADA |
| D2 — Catálogo + `preset_default` | `contrato_estilo.md` §3.2 | "Catálogo e opção ativa" em chip — `chip.preset_default` obrigatório | PROPAGADA |
| D2 — Catálogo + `preset_default` | `contrato_estilo.md` §4 R-9 | Nova regra R-9 — `preset_default` obrigatório em categorias com catálogo | PROPAGADA |
| D2 — Catálogo + `preset_default` | `docs/nomenclatura/10_ESTILO.md` §3, §4.2, §4.3 | Termos proprietários atualizados; seções 4.2 e 4.3 com catálogo e preset_default | PROPAGADA |
| D3 — Escopo integral | `contrato_estilo.md` §3.1, §3.2, §3.3 | Materialização de borda (7), chip (5), indicadores (6) documentada | PROPAGADA |
| D3 — Escopo integral | `docs/nomenclatura/10_ESTILO.md` §4.8 | Nova tabela de materialização cobrindo todas as seções | PROPAGADA |
| D4 — Preset ativo de borda: "Borda Curva" | `contrato_estilo.md` §3.1, §3.6 | "Preservação visual inicial" em 3.1 e tabela em 3.6 | PROPAGADA |
| D4 — Preset ativo de borda: "Borda Curva" | `docs/nomenclatura/10_ESTILO.md` §4.2 | Preset ativo inicial "Borda Curva" em seção de borda | PROPAGADA |
| D4 — Preset ativo de borda: "Borda Curva" | `docs/adr/INDICE_ADR.md` | Entrada inclui `"Borda Curva"` como preset ativo | PROPAGADA |
| D5 — Preset "Colchete"; `caixa_alta: false` | `contrato_estilo.md` §3.2 | Correção de "caixa_alta: true como default global" → `caixa_alta` per-preset; "Colchete" usa `false` | PROPAGADA |
| D5 — Preset "Colchete"; `caixa_alta: false` | `contrato_estilo.md` §3.6 | Tabela de preservação inclui `caixa_alta: false`, `cor_texto: "padrão"`, `cor_fundo: "padrão"` | PROPAGADA |
| D5 — Preset "Colchete"; `caixa_alta: false` | `docs/nomenclatura/10_ESTILO.md` §4.3 | `caixa_alta` per-preset; "Colchete" usa `false`; capitalização como propriedade do estilo | PROPAGADA |
| D5 — Preset "Colchete"; `caixa_alta: false` | `docs/adr/INDICE_ADR.md` | Entrada inclui `"Colchete"` com `caixa_alta: false` | PROPAGADA |
| D6 — Preset "Seta" | `contrato_estilo.md` §3.6 | Tabela de preservação: `indicadores.selecionado` preset "Seta" | PROPAGADA |
| D6 — Preset "Seta" | `docs/adr/INDICE_ADR.md` | Entrada inclui `"Seta"` (cursor) | PROPAGADA |
| D7 — Preset "Círculo" | `contrato_estilo.md` §3.6 | Tabela de preservação: `indicadores.incluido` preset "Círculo" | PROPAGADA |
| D7 — Preset "Círculo" | `docs/adr/INDICE_ADR.md` | Entrada inclui `"Círculo"` (inclusão) | PROPAGADA |
| D8 — Carregamento único, materialização | `contrato_estilo.md` §2, §3.1, §3.2, §4 R-10 | Nova regra R-10; autoridade global com carregamento único | PROPAGADA |
| D8 — Carregamento único, materialização | `docs/nomenclatura/10_ESTILO.md` §4.8 | Nova seção "Materialização e carregamento global" | PROPAGADA |
| D9 — Validações obrigatórias | `contrato_estilo.md` §5 | 13 novos critérios de validação cobrindo arquivo ausente, JSON inválido, seção ausente, preset_default ausente, catálogo vazio, preset inexistente, campos ausentes, tipos inválidos, string vazia, configuração parcial | PROPAGADA |
| D10 — Consumidores recebem valores resolvidos | `contrato_estilo.md` §2 | "Consumidores recebem o objeto de estilo resolvido — não relêem config/estilo.json" | PROPAGADA |
| D10 — Consumidores recebem valores resolvidos | `docs/nomenclatura/10_ESTILO.md` §4.9 | "Estado vivo não pertence a config/estilo.json" | PROPAGADA |
| D11 — Edição centralizada | `contrato_estilo.md` §3.1, §3.2 | Presets em catálogos são editáveis centralizadamente sem alterar código | PRESERVADA_COMO_DEFERIMENTO |
| D12 — Tela de escolha deferida | `contrato_estilo.md` §3.7 | "Pertence ao handoff do Bloco 1" | PRESERVADA_COMO_DEFERIMENTO |
| D13 — Blocos 2 e 3 fora do escopo | `docs/adr/INDICE_ADR.md` | Entrada indica explicitamente "Blocos 2 e 3 fora do escopo" | PRESERVADA_COMO_DEFERIMENTO |
| D13 — Blocos 2 e 3 fora do escopo | `contrato_estilo.md` | Nenhuma referência a navegação ou seleção introduzida | PRESERVADA_COMO_DEFERIMENTO |

---

## 7. Atualização da ADR-0030

| Campo alterado | Valor anterior | Valor novo |
|---|---|---|
| `metadata.status` | `proposta` | `aceita` |
| Tabela §1 — Status | `proposta` | `aceita` |
| Seção §2 — texto | Aguarda QA / não aplicada | Estado factual: aprovada, aplicação documental concluída, implementação pendente |
| Seção §15 — Encerramento | `DOCUMENTATION_PATCHED_AWAITING_QA` | bloco yaml de status + `APLICACAO_ADR_CONCLUIDA_AGUARDANDO_QA` |

---

## 8. Atualização do índice de ADRs

Adicionada linha ao final da tabela em `docs/adr/INDICE_ADR.md`:

```
| ADR-0030 | Carregamento global e materialização do estilo — ... | aceita | 2026-07-22 |
```

A entrada sintetiza: `config/estilo.json` como autoridade exclusiva; catálogo +
`preset_default`; materialização integral; presets ativos iniciais; remoção
futura de hardcodings; Blocos 2 e 3 fora do escopo; aplicação documental
concluída; QA pendente.

---

## 9. Atualização do contrato de estilo

### 9.1 Alterações executadas

| Seção | Natureza da alteração |
|---|---|
| Metadata `adrs_aplicadas` | Adicionado `ADR-0030-carregamento-global-e-materializacao-do-estilo.md` |
| §2 Regra fundamental | Renomeada para "Regra fundamental e autoridade global"; adicionados: autoridade exclusiva D1, escolha global, consumidores, fronteira com estado vivo |
| §3.1 Borda | Adicionados: "Catálogo e opção ativa", "Materialização", "Preservação visual inicial" com "Borda Curva" |
| §3.2 Chip | Adicionados: "Catálogo e opção ativa", "Materialização", "Preservação visual inicial" com "Colchete"; corrigido caixa_alta de default global errado (`true`) para per-preset (`false` em "Colchete") |
| §3.6 Preservação visual inicial (nova) | Tabela com presets ativos iniciais para todas as categorias |
| §3.7 Fronteira com implementação (nova) | Lista das decisões que pertencem ao handoff do Bloco 1 |
| §4 Regras de uso | Adicionadas R-9 (`preset_default` obrigatório) e R-10 (carregamento único) |
| §5 Critérios de validação | Adicionados 13 critérios cobrindo todas as validações D9 |

### 9.2 Preservado integralmente

- §3.3 Indicadores (incluindo transformação de preset para campos de runtime)
- §3.4 Tiling
- §3.5 Estados dinâmicos de cor
- §4 Regras R-1 a R-8
- §5 Critérios originais

---

## 10. Inspeção do contrato de chip

**Arquivo**: `docs/contratos/contrato_chip.md`

**Inspeção realizada**: Sim.

**Alterado**: Não.

**Evidência de conformidade**:
- §2 "Natureza do chip": "Aparência visual do chip vem do `config/estilo.json`: presets de moldura, cores, caixa alta e caracteres de abertura/fechamento pertencem ao schema de estilo universal." — cobre D1 e D10.
- §12 "Relação com estilo": lista explicitamente os cinco campos (`caractere_esquerdo`, `caractere_direito`, `cor_texto`, `caixa_alta`, `cor_fundo`) como vindos exclusivamente de `config/estilo.json` — cobre D5.
- §13 "Relação com barra_de_menus": conteúdo e ordem dos chips pertencem à declaração da barra — separação correta.
- Hardcoding de valores de cor, caractere ou símbolo é "violação contratual" (§12).

**Justificativa de preservação**: O contrato já comporta integralmente as decisões da ADR-0030 referentes a chips. Nenhum conflito ou omissão normativa direta foi identificado.

---

## 11. Inspeção do contrato da barra de menus

**Arquivo**: `docs/contratos/contrato_barra_de_menus.md`

**Inspeção realizada**: Sim.

**Alterado**: Não.

**Evidência de conformidade**:
- §5 "Fonte dos valores concretos": "`config/estilo.json`: Valores globais de aparência dos chips (presets de chip, `cor_inativo`, `cor_alerta`)" — cobre D1.
- §18 "Estados visuais — relação com contrato_estilo.md": cores de estado dinâmico vêm exclusivamente do schema de estilo ativo.
- R-5: "`config/estilo.json` é a fonte de aparência global."
- R-7: "O renderer consulta `cor_inativo` e `cor_alerta` do objeto de estilo ativo."
- §7 "Ordem canônica" preservada integralmente: `[Esc] → [<][>] → [-][+] → [#] → [⇆] → [✥] → [␣] → [⏎] → específicos → [V] → [?]`

**Justificativa de preservação**: O contrato já registra a origem global da aparência dos chips e a separação entre aparência e declaração da barra. Nenhum conflito normativo direto foi identificado. A capitalização via preset é implicitamente coberta pela delegação a `config/estilo.json` para todos os campos de chip.

---

## 12. Inspeção do contrato do console

**Arquivo**: `docs/contratos/contrato_console.md`

**Inspeção realizada**: Sim.

**Alterado**: Não.

**Evidência de conformidade**:
- §4 (Itens internos) e §7 (Navegação) tratam de estado vivo de cursor — não de símbolos de estilo.
- O contrato não hardcoda símbolos de indicador.
- Sem referência a navegação por setas ou seleção automática como funcionalidade nova.
- Conteúdo multinível, apresentações e modo verboso já formalizados via ADR-0028.

**Justificativa de preservação**: O contrato do console foca em estrutura de container, navegação, seleção e paginação. Não há conflito ou omissão normativa relacionada à ADR-0030 (que trata de aparência global, não de navegação ou seleção). A ADR-0030 D13 exclui explicitamente navegação e seleção do escopo.

---

## 13. Inspeção dos módulos de nomenclatura

### 13.1 `docs/nomenclatura/10_ESTILO.md`

**Inspecionado**: Sim. **Alterado**: Sim.

**Alterações**:
- §3 Termos proprietários: adicionados catálogo de presets, preset ativo/`preset_default`, preset resolvido, materialização, presets de borda e chip, configuração vs estado vivo.
- §4.2 Borda: adicionado catálogo, preset ativo "Borda Curva", materialização.
- §4.3 Chip: adicionado catálogo, preset ativo "Colchete", `caixa_alta` per-preset, capitalização como propriedade do estilo.
- §4.8 (nova): Materialização e carregamento global — tabela completa de seções.
- §4.9 (nova): Configuração de aparência vs estado vivo.
- §5 Distinções obrigatórias: adicionadas distinções de configuração×estado vivo, preset resolvido×hardcoded, símbolo materializado×estado de inclusão.
- §7 Relação com ADRs: adicionada ADR-0030.

**Justificativa de alteração**: A terminologia de catálogo, preset_default, preset resolvido e materialização era ausente. A descrição de borda e chip não mencionava presets. A correção de caixa_alta era necessária.

### 13.2 `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`

**Inspecionado**: Sim. **Alterado**: Não.

**Evidência de conformidade**: §9 delega "Aparência visual do chip (campos de estilo) → módulo 10". O módulo 10 (atualizado) agora contém a terminologia de capitalização como propriedade do estilo. Nenhum conflito com ADR-0030 foi identificado.

**Justificativa de preservação**: A delegação ao módulo 10 é suficiente. A ordem canônica dos chips foi preservada integralmente.

### 13.3 `docs/nomenclatura/32_CONSOLE.md`

**Inspecionado**: Sim. **Alterado**: Não.

**Evidência de conformidade**: §4.4 usa "preset equivalente" para `selecionado` e `incluido` — implicando que os símbolos vêm de presets, não hardcoded. Estado vivo de cursor e seleção são tratados separadamente como mecanismos de navegação. Sem conflito com ADR-0030.

**Justificativa de preservação**: O módulo comporta as decisões da ADR-0030 via "preset equivalente". A distinção símbolo×estado vivo é implicitamente presente. ADR-0030 D13 exclui navegação e seleção do escopo desta aplicação.

---

## 14. Arquivos alterados nesta aplicação documental

| Arquivo | Tipo de alteração |
|---|---|
| `docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md` | Status proposta→aceita; §2 factual; §15 encerramento |
| `docs/adr/INDICE_ADR.md` | Adicionada entrada ADR-0030 |
| `docs/contratos/contrato_estilo.md` | Adições: autoridade global, preset_default borda/chip, materialização, preservação visual, R-9, R-10, 13 validações D9, §3.6, §3.7, fronteira implementação |
| `docs/nomenclatura/10_ESTILO.md` | Adições: novos termos, presets borda/chip, materialização, configuração×estado vivo |
| `docs/relatorios/RELATORIO_APLICACAO_ADR-0030.md` | Criado (este arquivo) |

---

## 15. Arquivos inspecionados e preservados

| Arquivo | Motivo da preservação |
|---|---|
| `docs/contratos/contrato_chip.md` | Já comporta as decisões da ADR-0030; nenhum conflito ou omissão direta |
| `docs/contratos/contrato_barra_de_menus.md` | Já registra origem global da aparência; ordem canônica preservada integralmente |
| `docs/contratos/contrato_console.md` | Foco em navegação/seleção; sem conflito com ADR-0030 |
| `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` | Delegação a módulo 10 suficiente; nenhum conflito |
| `docs/nomenclatura/32_CONSOLE.md` | Usa "preset equivalente"; distinção implicitamente presente |

---

## 16. Configuração e código preservados

```yaml
config_estilo_json:
  alterado: false
  motivo: pertence ao handoff do Bloco 1; não é aplicação documental

codigo_tela:
  alterado: false
  loader_py: inalterado
  renderizador_py: inalterado
  modelo_py: inalterado
  testes: inalterados

jsons_de_tela:
  alterados: false

relatorios_historicos:
  alterados: []
```

---

## 17. Verificações de resíduos

| Termo buscado | Resultado em documentos alterados | Observação |
|---|---|---|
| `preset_default` | Presente em contrato_estilo.md e 10_ESTILO.md | Propagação normativa confirmada |
| `"Borda Curva"` | Presente em contrato_estilo.md, 10_ESTILO.md, INDICE_ADR.md | Propagação D4 confirmada |
| `"Colchete"` | Presente em contrato_estilo.md, 10_ESTILO.md, INDICE_ADR.md | Propagação D5 confirmada |
| `caixa_alta` | Presente — per-preset, não como default global | Correção do texto errado confirmada |
| `cor_texto` | Presente como campo de runtime | Normal |
| `cor_fundo` | Presente como campo de runtime | Normal |
| `"padrão"` (com acento) | Presente em contrato_estilo.md §3.2 e §3.6 | Literal correto mantido |
| `"padrao"` (sem acento) | Ausente dos documentos alterados nesta etapa | Sem regressão |
| `tipo_borda` | Presente apenas como referência histórica em ADR-0030 §3.1 e §3.7 (fronteira) | Não declarado como implementado; correto |
| `_BORDAS` | Presente apenas como referência histórica em ADR-0030 e §3.1 do contrato (não como removido) | Correto — remoção é futura |
| `selecionado_simbolo` | Presente em contrato_estilo.md §3.3, 10_ESTILO.md §4.8 | Materialização documentada |
| `selecionado_off` | Presente em contrato_estilo.md §3.3, 10_ESTILO.md §4.8 | Materialização documentada |
| `incluido_on` | Presente em contrato_estilo.md §3.3, §3.6, 10_ESTILO.md §4.8 | Materialização documentada |
| `incluido_off` | Presente em contrato_estilo.md §3.3, §3.6, 10_ESTILO.md §4.8 | Materialização documentada |
| `concluido_on` | Presente em contrato_estilo.md §3.3, §3.6, 10_ESTILO.md §4.8 | Materialização documentada |
| `concluido_off` | Presente em contrato_estilo.md §3.3, §3.6, 10_ESTILO.md §4.8 | Materialização documentada |

---

## 18. Estado Git

```yaml
arquivos_modificados_rastreados:
  - docs/adr/INDICE_ADR.md
  - docs/contratos/contrato_estilo.md
  - docs/nomenclatura/10_ESTILO.md

arquivos_nao_rastreados_desta_etapa:
  - docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0030.md

stage: VAZIO
commits_gerados: nenhum
push_executado: false
```

---

## 19. Bloqueios

```yaml
bloqueios: nenhum
contradições_normativas: nenhuma
decisoes_pendentes: nenhuma
```

---

## 20. Gate de escopo

```yaml
ADR_alterada: true
indice_ADR_alterado: true
contrato_estilo_alterado: true

contrato_chip:
  inspecionado: true
  alterado: false
  justificativa: Já comporta as decisões da ADR-0030 — seções §2 e §12 cobrem D1, D5 e D10

contrato_barra_de_menus:
  inspecionado: true
  alterado: false
  justificativa: Seções §5, §18, R-5 e R-7 cobrem origem global da aparência; ordem canônica preservada

contrato_console:
  inspecionado: true
  alterado: false
  justificativa: ADR-0030 D13 exclui navegação e seleção do escopo; sem conflito normativo

nomenclatura_10_ESTILO:
  inspecionado: true
  alterado: true
  justificativa: Terminologia de catálogo, preset_default, preset resolvido, materialização era ausente

nomenclatura_31_BARRA_DE_MENUS_E_CHIPS:
  inspecionado: true
  alterado: false
  justificativa: Delegação ao módulo 10 é suficiente; nenhum conflito identificado

nomenclatura_32_CONSOLE:
  inspecionado: true
  alterado: false
  justificativa: Usa "preset equivalente"; distinção símbolo×estado vivo implicitamente presente

config_estilo_alterado: false
codigo_alterado: false
testes_alterados: false
relatorios_historicos_alterados: []
stage: VAZIO
```

---

## 21. Resultado factual

```yaml
etapa: APLICAR_ADR
resultado_factual: CONCLUIDA
qa_da_aplicacao: PENDENTE
proxima_categoria: QA_APLICACAO_ADR
bloqueios: nenhum
```

---

## 22. Encerramento

APLICACAO_ADR_CONCLUIDA_AGUARDANDO_QA
