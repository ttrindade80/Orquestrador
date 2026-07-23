---
name: relatorio-patch-h-0039-handoff
description: Relatório do patch focal do handoff H-0039 — tratamento do achado QA-H0039-001 (lista nominal incompleta)
metadata:
  type: relatorio
  etapa: PATCH_HANDOFF
  handoff_corrigido: H-0039
  achado_tratado: QA-H0039-001
  data: "2026-07-22"
---

# Relatório de Patch — H-0039 Handoff

## 1. Identificação

| Campo | Valor |
|---|---|
| Etapa | PATCH_HANDOFF |
| Handoff corrigido | H-0039 — Carregamento global e materialização do estilo |
| Arquivo corrigido | `docs/handoff/H-0039-carregamento-global-materializacao-estilo.md` |
| Relatório do patch | `docs/relatorios/RELATORIO_PATCH_H-0039_HANDOFF.md` |
| Data | 2026-07-22 |

---

## 2. Handoff corrigido

```yaml
arquivo: docs/handoff/H-0039-carregamento-global-materializacao-estilo.md
numero: H-0039
titulo: Carregamento global e materialização do estilo
adr_base: ADR-0030
bloco: 1
```

---

## 3. Relatório de QA de origem

```yaml
arquivo: docs/relatorios/RELATORIO_QA_H-0039_HANDOFF.md
etapa: QA_HANDOFF
classificacao: H2_HANDOFF_PATCH_REQUIRED
proxima_categoria: PATCH_HANDOFF
```

---

## 4. Hash da versão rejeitada

```yaml
versao_anterior:
  sha256: 6445892c48fc8fcd75bb96ae1c0a1b38dc7c385d47290b82c20c4fe55e8e4b7e
  quantidade_de_linhas: 1011
  tamanho_em_bytes: 45326
  data_de_modificacao: "2026-07-22 13:13:39.520184533 -0300"
```

Hash confirmado antes do patch:

```bash
$ sha256sum docs/handoff/H-0039-carregamento-global-materializacao-estilo.md
6445892c48fc8fcd75bb96ae1c0a1b38dc7c385d47290b82c20c4fe55e8e4b7e  docs/handoff/H-0039-carregamento-global-materializacao-estilo.md
```

---

## 5. Achado tratado

```yaml
achado: QA-H0039-001
status: TRATADO
severidade: alta
tema: lista_nominal_incompleta
natureza: ampliacao_focal_da_lista_nominal
decisao_semantica_alterada: false
decisao_do_usuario_necessaria: false
```

**Descrição original (QA)**: O handoff substitui a assinatura de `renderizar_tela` por `renderizar_tela(modelo, estilo, largura, altura, verboso)`, mas autorizava nominalmente apenas os consumidores com `tipo_borda`. A busca material encontrou chamadas diretas sem `tipo_borda` em `demo/diagnostico.py`, `demo/teste_diagnostico.py` e `demo/teste_demo_console.py`, que também quebrariam quando `estilo` se tornar argumento obrigatório.

---

## 6. Evidência material

A assinatura final proposta pelo H-0039 exige que todos os consumidores recebam o estilo resolvido. O QA comprovou consumidores omitidos:

```yaml
consumidores_omitidos:
  - arquivo: demo/diagnostico.py
    linha_ou_simbolo: "renderizar_tela(modelo)"
    mudanca_necessaria: "carregar/passar EstiloResolvido conforme assinatura final"
    autorizado_nominalmente_no_handoff_anterior: false

  - arquivo: demo/teste_diagnostico.py
    linha_ou_simbolo: "renderizar_tela(... largura/altura) em linhas 364, 435, 458"
    mudanca_necessaria: "atualizar chamadas para novo parâmetro estilo"
    autorizado_nominalmente_no_handoff_anterior: false

  - arquivo: demo/teste_demo_console.py
    linha_ou_simbolo: "renderizar_tela(... largura/altura) em linhas 199, 210, 221, 233"
    mudanca_necessaria: "passar estilo obrigatório após nova assinatura"
    autorizado_nominalmente_no_handoff_anterior: false
```

Sem autorização nominal desses arquivos:
- a implementação teria de parar e solicitar exceção;
- ou deixaria consumidores quebrados;
- ou não atingiria a migração integral contratada pela ADR-0030 D8/D10.

---

## 7. Arquivos adicionados à lista nominal

```yaml
adicionados_a_lista_nominal:
  - arquivo: demo/diagnostico.py
    necessidade: chamada direta de renderizar_tela sem estilo resolvido
    simbolo_ou_fluxo_afetado: fluxo de diagnóstico e renderização do modelo
    classificacao: AUTORIZADO_E_OBRIGATORIO

  - arquivo: demo/teste_diagnostico.py
    necessidade: testes com chamadas diretas de renderizar_tela
    simbolo_ou_fluxo_afetado: cenários de renderização do diagnóstico
    classificacao: AUTORIZADO_E_OBRIGATORIO

  - arquivo: demo/teste_demo_console.py
    necessidade: testes com chamadas diretas de renderizar_tela
    simbolo_ou_fluxo_afetado: cenários de console e dimensões de renderização
    classificacao: AUTORIZADO_E_OBRIGATORIO
```

**Lista nominal consolidada após o patch:**

```text
config/estilo.json
tela/loader.py
tela/renderizador.py
tela/teste_loader.py
tela/teste_renderizador.py

demo/demo.py
demo/teste_demo.py
demo/teste_demo_console_modos.py
demo/demo_distribuicao.py
demo/diagnostico.py
demo/teste_diagnostico.py
demo/teste_demo_console.py

docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0039_CARREGAMENTO_ESTILO.md
```

---

## 8. Seções reconciliadas

| Seção | Mudança |
|---|---|
| 2.3 Artefatos técnicos inspecionados | Adicionados 3 arquivos com nota de identificação QA-H0039-001 |
| 5.4 Chamadores de `renderizar_tela` | Renomeada (era "Chamadores que fornecem tipo_borda"); expandida com subgrupo de chamadores sem `tipo_borda` |
| 7.4 Migração dos chamadores | Adicionados 3 novos arquivos na tabela de migração; texto introdutório ampliado para cobrir todos os chamadores |
| 14.2 Arquivos de demonstração — consumidores obrigatórios | Renomeada (era "Arquivos condicionais — chamadores com tipo_borda"); introdução atualizada; 3 novos arquivos adicionados em YAML com `classificacao: AUTORIZADO_E_OBRIGATORIO` |
| 15.3 Adaptações nos arquivos de demo | Nova subseção — adaptações específicas de `demo/diagnostico.py`, `demo/teste_diagnostico.py` e `demo/teste_demo_console.py` |
| 15.4 Suite focal | Renumerada (era 15.3) |
| 15.5 Suite canônica | Renumerada (era 15.4) |
| 18.4 Compatibilidade | Adicionados CA-T8 a CA-T12; adicionado bloco `inventario_final_de_consumidores` |
| 19 Relatório de implementação | Item 6 ampliado; item 6a adicionado com comandos `rg` obrigatórios e requisito de registro de inventário final |
| 20.1 Riscos identificados | Risco de "chamador não detectado" atualizado para refletir inventário completo (8 arquivos) |
| 20.2 Bloqueios potenciais | Bloqueio de "caller inesperado" reformulado para cobrir qualquer chamador fora da lista nominal |
| 21 Estado final esperado | Adicionado `renderizar_tela_sem_estilo: zero_ocorrencias_ativas_incompativeis` e bloco `inventario_consumidores` |

---

## 9. Decisões preservadas

```yaml
preservadas_integralmente:
  numero_handoff: H-0039
  titulo: Carregamento global e materialização do estilo
  adr_base: ADR-0030
  EstiloResolvido: inalterado (18 campos, frozen dataclass)
  carregar_estilo: inalterado
  mecanismo_len_s_1: inalterado
  validacoes_V01_a_V29: inalteradas
  presets_e_literais: inalterados
  estado_final_sem_BORDAS: inalterado
  estado_final_sem_tipo_borda: inalterado
  escopo_negativo: inalterado
  demonstracao: inalterada
  validacao_manual_exclusiva_usuario: inalterada
  relatorio_implementacao_previsto: inalterado
  baseline_422_testes: inalterado
  blocos_2_e_3_fora_do_escopo: inalterado
  estrategia_sem_compatibilidade_permanente: inalterada
  estilo_nao_tornado_opcional: confirmado
```

---

## 10. Arquivos alterados e criados

```yaml
arquivos_alterados_preexistentes:
  - docs/handoff/H-0039-carregamento-global-materializacao-estilo.md

arquivos_criados:
  - docs/relatorios/RELATORIO_PATCH_H-0039_HANDOFF.md

outros_arquivos_alterados: nenhum
stage: VAZIO
```

---

## 11. Rastreabilidade de hash

```yaml
versao_anterior:
  sha256: 6445892c48fc8fcd75bb96ae1c0a1b38dc7c385d47290b82c20c4fe55e8e4b7e
  quantidade_de_linhas: 1011
  tamanho_em_bytes: 45326
  data_de_modificacao: "2026-07-22 13:13:39.520184533 -0300"

versao_pos_patch:
  sha256: db293dd7f07b5a1023744e6c98eae701f25f873a359ac405288fec836b412b18
  quantidade_de_linhas: 1108
  tamanho_em_bytes: 51437
  data_de_modificacao: "2026-07-22 13:36:15.026665322 -0300"
```

Hashes distintos confirmados. A versão anterior permanece registrada neste relatório e no `RELATORIO_QA_H-0039_HANDOFF.md` (hash intocado como registro histórico).

---

## 12. Checks

```yaml
git_status:
  comando: "git status --short --untracked-files=all"
  handoff_no_stage: false
  relatorio_no_stage: false
  stage: VAZIO

git_diff_check:
  comando: git diff --check
  codigo_saida: 0
  erros_whitespace: nenhum

git_diff_cached_check:
  comando: git diff --cached --check
  codigo_saida: 0
  erros_whitespace: nenhum

whitespace_handoff:
  comando: "git diff --no-index --check /dev/null docs/handoff/H-0039-carregamento-global-materializacao-estilo.md"
  ocorrencias_trailing_whitespace: 0

whitespace_relatorio:
  comando: "git diff --no-index --check /dev/null docs/relatorios/RELATORIO_PATCH_H-0039_HANDOFF.md"
  ocorrencias_trailing_whitespace: 0

pytest:
  executado_nesta_etapa: false
  motivo: etapa documental — pytest não é parte dos checks exigidos do PATCH_HANDOFF
```

---

## 13. Estado Git

```yaml
raiz: /home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador
branch: master
ultimo_commit: "2caf036 test: adota pytest como padrao unico"
stage_antes_do_patch: vazio
stage_apos_o_patch: vazio
arquivos_modificados_fora_do_escopo: nenhum
```

---

## 14. Bloqueios

```yaml
bloqueios: []
```

Nenhum bloqueio encontrado. O achado QA-H0039-001 foi classificado como `decisao_do_usuario_necessaria: false` — a necessidade dos 3 arquivos é evidente pela assinatura final contratada e pelas evidências materiais do QA.

---

## 15. Encerramento

```yaml
achado: QA-H0039-001
status: TRATADO
natureza: ampliacao_focal_da_lista_nominal
decisao_semantica_alterada: false
decisao_do_usuario_necessaria: false

handoff_corrigido: docs/handoff/H-0039-carregamento-global-materializacao-estilo.md
relatorio_patch_criado: docs/relatorios/RELATORIO_PATCH_H-0039_HANDOFF.md

arquivos_adicionados_a_lista_nominal:
  - demo/diagnostico.py
  - demo/teste_diagnostico.py
  - demo/teste_demo_console.py

secoes_reconciliadas:
  - "2.3 Artefatos técnicos inspecionados"
  - "5.4 Chamadores de renderizar_tela (renomeada e expandida)"
  - "7.4 Migração dos chamadores (ampliada)"
  - "14.2 Arquivos de demonstração — consumidores obrigatórios (renomeada e expandida)"
  - "15.3 Adaptações nos arquivos de demo (nova subseção)"
  - "15.4 Suite focal (renumerada)"
  - "15.5 Suite canônica (renumerada)"
  - "18.4 Compatibilidade (CA-T8 a CA-T12 + inventario_final)"
  - "19 Relatório de implementação (item 6a adicionado)"
  - "20.1 Riscos (atualizado)"
  - "20.2 Bloqueios (atualizado)"
  - "21 Estado final esperado (inventário adicionado)"

hash_anterior: 6445892c48fc8fcd75bb96ae1c0a1b38dc7c385d47290b82c20c4fe55e8e4b7e
hash_novo: db293dd7f07b5a1023744e6c98eae701f25f873a359ac405288fec836b412b18

arquivos_alterados_preexistentes:
  - docs/handoff/H-0039-carregamento-global-materializacao-estilo.md

arquivos_criados:
  - docs/relatorios/RELATORIO_PATCH_H-0039_HANDOFF.md

outros_arquivos_alterados: nenhum
stage: VAZIO

estado_final: HANDOFF_CRIADO_AGUARDANDO_QA
```

HANDOFF_CREATED_AWAITING_QA
