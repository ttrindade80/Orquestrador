---
name: relatorio-patch-adr-0030
description: Relatório do patch documental focal da ADR-0030 após QA independente — registra tratamento dos cinco achados obrigatórios e decisão adicional do usuário
metadata:
  type: relatorio
  etapa: PATCH_DOCUMENTAL
  status: concluido
---

# Relatório de Patch — ADR-0030

## 1. Identificação

```yaml
etapa: PATCH_DOCUMENTAL
papel: autor_documental_pos_QA
data: "2026-07-22"
artefato_corrigido: docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
relatorio_patch: docs/relatorios/RELATORIO_PATCH_ADR-0030.md
```

---

## 2. Artefato corrigido

```yaml
arquivo: docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
status_preservado: proposta
ultima_linha: DOCUMENTATION_PATCHED_AWAITING_QA
```

---

## 3. Relatório de QA tratado

```yaml
arquivo: docs/relatorios/RELATORIO_QA_ADR-0030.md
status_do_QA: ADR_PATCH_REQUIRED
preservado_integro: true
alterado_por_este_patch: false
achados_com_patch_obrigatorio:
  - QA-ADR0030-001
  - QA-ADR0030-002
  - QA-ADR0030-003
  - QA-ADR0030-004
  - QA-ADR0030-005
```

---

## 4. Decisão adicional do usuário

```yaml
decisao: >
  A aparência inicial dos chips deve preservar a capitalização atual dos
  textos declarados pelas telas. Exemplos preservados: "Sair", "Voltar",
  "Ajuda", "Verboso".
implicacao: >
  O preset global ativo continua sendo "Colchete". Mas o campo caixa_alta
  deve ter valor_final_decidido: false — diferente do valor atual no arquivo
  (true). A mudança concreta em config/estilo.json pertence ao ciclo de
  implementação do Bloco 1, não à aplicação documental. Este patch registra
  a decisão na ADR.
```

---

## 5. Tratamento de QA-ADR0030-001

```yaml
achado: QA-ADR0030-001
severidade: alta
tema: preservacao_visual_chip
status: TRATADO

alteracoes:
  - secao: "3.2 Correspondência entre hardcodings e presets existentes"
    descricao: >
      Linha do chip atualizada para indicar que a correspondência cobre todos
      os cinco campos e que caixa_alta: true no arquivo não preserva o visual.
      Referência a D5 para análise completa.

  - secao: "D5 — Preservação da aparência vigente de chip"
    descricao: >
      Seção inteiramente reescrita para cobrir todos os cinco campos do preset
      "Colchete": caractere_esquerdo, caractere_direito, caixa_alta, cor_texto,
      cor_fundo. Inclui tabela de análise campo a campo e bloco yaml com o
      registro formal de caixa_alta.

  - secao: "9.1 Preservação da aparência inicial"
    descricao: >
      Atualizada para registrar que a preservação do preset "Colchete" tem
      condições: delimitadores e cores preservam o visual, mas caixa_alta: true
      no arquivo não preserva — a migração deve mudar para false.

  - secao: "11. Validações"
    descricao: >
      Adicionado critério: "chip.presets["Colchete"].caixa_alta é false após
      a migração." Critério final atualizado para mencionar capitalização
      original dos rótulos.

  - secao: "6. Tabela das decisões"
    descricao: >
      D5 atualizado para registrar: "caixa_alta: false para preservar
      capitalização atual dos rótulos".

decisao_nova_utilizada: >
  Decisão explícita do usuário: preservar capitalização atual dos rótulos
  declarados pelas telas ("Sair", "Voltar", "Ajuda", "Verboso") exige que
  caixa_alta seja false no preset resolvido. O valor atual no arquivo (true)
  não preserva o visual vigente.

arquivos:
  - docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
```

---

## 6. Tratamento de QA-ADR0030-002

```yaml
achado: QA-ADR0030-002
severidade: media
tema: genealogia_semantica_D8_D11
status: TRATADO

alteracoes:
  - secao: "13.1 Origem das decisões"
    descricao: >
      Tabela de rastreabilidade expandida para separar D8, D9 e D10 por
      origem real. D8 é dividido em: carregamento e disponibilização
      (decisão do usuário via D1); validação e materialização (regra
      contratual preexistente — contrato_estilo.md §3.3, R-3); nome/módulo
      e não-reler-por-render (decisão técnica do handoff). D9 é dividido em:
      validações de schema e ausência de fallback (regra contratual +
      decisão do usuário A7); unidade técnica e duplicidade raw (handoff).
      D10 é separado como regra contratual preexistente (R-1, R-2).

  - secao: "13.2 Separação genealógica (nova)"
    descricao: >
      Bloco yaml criado com as quatro categorias nominais: decisao_do_usuario,
      regra_contratual_preexistente, evidencia_do_levantamento,
      decisao_tecnica_de_handoff. Cada item é comentado com a decisão ou
      evidência a que se refere.

decisao_nova_utilizada: nenhuma
arquivos:
  - docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
```

---

## 7. Tratamento de QA-ADR0030-003

```yaml
achado: QA-ADR0030-003
severidade: media
tema: aplicacao_documental_configuracao_executavel
status: TRATADO

alteracoes:
  - secao: "2. Status"
    descricao: >
      Texto atualizado para mencionar que a implementação inclui
      config/estilo.json como configuração executável em ciclo próprio.

  - secao: "10.1 Aplicação documental"
    descricao: >
      Removidos os itens que exigiam alterações em config/estilo.json
      (adicionar preset_default em borda e chip) e a mudança de _meta.status.
      A seção passa a declarar explicitamente que altera somente documentos
      normativos. Os quatro itens são: atualizar contrato_estilo.md;
      inspecionar contrato_chip.md; inspecionar contrato_barra_de_menus.md;
      inspecionar contrato_console.md. Frase final registra que a promoção
      de _meta.status é deferida (seção 12).

  - secao: "10.2 Implementação"
    descricao: >
      Reestruturada em duas partes: "Alterações em config/estilo.json"
      (itens 1-3: adicionar preset_default em borda, adicionar preset_default
      em chip, mudar caixa_alta para false) e "Implementação" (itens 4-10:
      loader, validações, disponibilização, remoção de _BORDAS e tipo_borda,
      atualização do renderer e dos testes). Frase final registra que
      _meta.status não está incluído neste ciclo.

  - secao: "12. Decisões deferidas"
    descricao: >
      Adicionada linha: "Promoção de _meta.status de config/estilo.json —
      Critério de promoção não definido; pendências ainda registradas no
      arquivo; a promoção pertence a ciclo futuro com critério explícito."

decisao_nova_utilizada: nenhuma
arquivos:
  - docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
```

---

## 8. Tratamento de QA-ADR0030-004

```yaml
achado: QA-ADR0030-004
severidade: media
tema: validacoes_D9_ambiguidade_operacional
status: TRATADO

alteracoes:
  - secao: "D9 — Validações obrigatórias do loader"
    descricao_restricao_de_caractere: >
      Linha da tabela alterada de "Símbolo ou caractere com comprimento
      diferente de 1 (R-6 do contrato)" para "Símbolo ou caractere com
      comprimento diferente de 1, conforme R-6 do contrato" — preserva a
      exigência contratual sem inventar unidade técnica nova. Acrescentada
      nota explicativa: a ADR não redefine "caractere" como code point,
      grapheme cluster ou largura visual; não introduz nova política de
      largura de terminal; a unidade técnica de medição é decisão do handoff;
      bloqueio documental deve ser registrado se a autoridade contratual se
      mostrar insuficiente.

    descricao_duplicidade: >
      Linha "Opções duplicadas em catálogo | Erro explícito quando
      materialmente aplicável" substituída por "Identificadores ou nomes
      duplicados na estrutura materializada, quando a estrutura materializada
      permita a observação | Erro explícito". Acrescentada nota: chaves
      duplicadas no JSON bruto podem ser descartadas pelo parser; a ADR não
      exige parser raw especial; a validação aplica-se ao que for observável
      na estrutura materializada; a unidade e o mecanismo pertencem ao handoff.

  - secao: "12. Decisões deferidas"
    descricao: >
      Adicionadas duas linhas: "Unidade técnica de medição de 1 caractere
      (R-6)" e "Mecanismo de detecção de duplicidade raw em JSON".

decisao_nova_utilizada: nenhuma
arquivos:
  - docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
```

---

## 9. Tratamento de QA-ADR0030-005

```yaml
achado: QA-ADR0030-005
severidade: baixa
tema: documentos_afetados_incompletos
status: TRATADO

alteracoes:
  - secao: "14. Propagação documental (nova)"
    descricao: >
      Seção criada com matriz explícita classificando cada arquivo em:
      ATUALIZAR, ATUALIZAR_SE_AFETADO, INSPECIONAR_E_PRESERVAR ou
      NAO_APLICAVEL. Avalia nominalmente os oito arquivos exigidos.
      Classificações:
        ATUALIZAR: contrato_estilo.md, docs/adr/INDICE_ADR.md
        ATUALIZAR_SE_AFETADO: contrato_chip.md, 10_ESTILO.md,
          31_BARRA_DE_MENUS_E_CHIPS.md, 32_CONSOLE.md
        INSPECIONAR_E_PRESERVAR: contrato_barra_de_menus.md,
          contrato_console.md
      Nota de distinção entre documentos afetados e autoridades consultadas.

  - secao: "15. Encerramento (renumerada de 14)"
    descricao: >
      A seção de encerramento foi renumerada de 14 para 15 para acomodar
      a nova seção 14 de propagação documental.

decisao_nova_utilizada: nenhuma
arquivos:
  - docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
```

---

## 10. Decisões preservadas

```yaml
preservacoes_confirmadas:
  metadata_status: proposta
  secao_2_status: proposta
  D1_autoridade_global_exclusiva: preservado
  D2_catalogos_e_opcao_ativa: preservado
  D3_escopo_integral: preservado
  preset_Borda_Curva: preservado
  preset_Colchete: preservado
  preset_Seta: preservado
  preset_Circulo: preservado
  ausencia_de_fallback_silencioso: preservado
  separacao_config_global_vs_estado_vivo: preservado
  tela_futura_de_estilo_deferida: preservado
  blocos_2_e_3_fora_do_escopo: preservado
  estado_final_sem_tipo_borda: preservado
  relatorio_de_levantamento: referenciado_sem_alteracao
  relatorio_de_QA_rejeitado: preservado_integro_sem_alteracao
  sem_navegacao_sem_selecao_na_ADR: confirmado
  sem_execucao_na_ADR: confirmado
```

---

## 11. Arquivos alterados e criados

```yaml
arquivos_preexistentes_alterados:
  - path: docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
    natureza: correcao_patch_documental

arquivos_criados:
  - path: docs/relatorios/RELATORIO_PATCH_ADR-0030.md
    natureza: relatorio_desta_etapa

arquivos_preservados_intocados:
  - docs/relatorios/RELATORIO_QA_ADR-0030.md
  - docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md

outros_arquivos_alterados: nenhum
contratos_alterados_neste_ciclo: nenhum
modulos_alterados_neste_ciclo: nenhum
codigo_alterado_neste_ciclo: nenhum
configuracao_alterada_neste_ciclo: nenhum
```

---

## 12. Checks mecânicos

```yaml
ids_dos_achados_no_relatorio:
  QA-ADR0030-001: presente
  QA-ADR0030-002: presente
  QA-ADR0030-003: presente
  QA-ADR0030-004: presente
  QA-ADR0030-005: presente

caixa_alta_false_nas_secoes_materiais_da_ADR:
  D5_bloco_yaml: presente
  D5_tabela_de_correspondencia: presente (coluna análise de preservação visual)
  D5_implicacoes: presente
  D6_tabela_de_decisoes: presente
  secao_9_1: presente
  secao_10_2: presente
  secao_11_criterios: presente

exigencia_meta_status_ativo_removida: true
  local_removido: secao_10_1
  local_registrado: secao_12_decisoes_deferidas

config_estilo_json_classificado_no_ciclo_de_implementacao: true
  local: secao_10_2

genealogia_separada: true
  local_tabela: secao_13_1
  local_categorias_yaml: secao_13_2

status_continua_proposta:
  metadata: true
  secao_2: true

outros_arquivos_alterados_alem_da_ADR_e_relatorio_patch: nenhum

stage_vazio: true
```

---

## 13. Estado Git

```yaml
comando: git status --short
saida:
  - "?? docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md"
  - "?? docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md"
  - "?? docs/relatorios/RELATORIO_PATCH_ADR-0030.md"
  - "?? docs/relatorios/RELATORIO_QA_ADR-0030.md"

comando: git diff --check
saida: vazio
codigo_saida: 0

comando: git diff --cached --check
saida: vazio
codigo_saida: 0

stage: VAZIO
observacao: >
  Todos os arquivos desta etapa (ADR-0030, relatório de levantamento, relatório
  de QA, relatório de patch) permanecem não rastreados. Nenhum arquivo foi
  adicionado ao stage nesta etapa.
```

---

## 14. Bloqueios

```yaml
bloqueios: nenhum
decisoes_do_usuario_pendentes: nenhuma
achados_nao_tratados: nenhum
```

---

## 15. Encerramento

DOCUMENTATION_PATCHED_AWAITING_QA
