---
name: relatorio-qa-pos-patch-adr-0030
description: QA pos-patch independente da ADR-0030 sobre carregamento global e materializacao do estilo
metadata:
  type: relatorio
  etapa: QA_POS_PATCH_ADR
  status: concluido
---

# Relatorio QA pos-patch ADR-0030

## 1. Recuperacao pos-reinicializacao

```yaml
recuperacao_pos_reinicializacao:
  relatorio_preexistente: docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0030.md
  classificacao: A
  arquivo_preservado: null
  arquivo_de_saida_efetivo: docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0030.md
```

O relatorio canonico de QA pos-patch nao existia antes desta recuperacao. Nao
havia relatorio parcial a preservar nem caminho de recuperacao a criar.

## 2. Gate inicial

```yaml
arquivo_correto: true
etapa_correta: QA_POS_PATCH_ADR
modo: RECUPERACAO_POS_REINICIALIZACAO
artefato_auditado: docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
numero: ADR-0030
metadata_status: proposta
status_no_corpo: proposta
encerramento: DOCUMENTATION_PATCHED_AWAITING_QA
qa_inicial: docs/relatorios/RELATORIO_QA_ADR-0030.md
relatorio_patch: docs/relatorios/RELATORIO_PATCH_ADR-0030.md
relatorio_parcial_preexistente: null
arquivo_de_saida_efetivo: docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0030.md
stage: VAZIO
status_literal:
  metadata.status: proposta
  secao_status: proposta
ultima_linha_ou_encerramento: DOCUMENTATION_PATCHED_AWAITING_QA
```

O QA inicial e o relatorio de patch foram lidos como historico preservado e
nao foram alterados.

## 3. Autoridades e cadeia historica lidas

```yaml
cadeia_historica_preservada:
  - docs/relatorios/RELATORIO_QA_ADR-0030.md
  - docs/relatorios/RELATORIO_PATCH_ADR-0030.md
  - docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md
leitura_seletiva:
  indice: docs/nomenclatura/00_INDICE.md
  modulos_e_contratos:
    - docs/nomenclatura/01_NUCLEO_COMUM.md
    - docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md
    - docs/nomenclatura/10_ESTILO.md
    - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    - docs/nomenclatura/32_CONSOLE.md
    - docs/contratos/contrato_estilo.md
    - docs/contratos/contrato_chip.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_console.md
    - config/estilo.json
```

## 4. Auditoria dos achados originais

```yaml
- id: QA-ADR0030-001
  status: RESOLVIDO
  evidencia: >
    D5 trata os cinco campos do preset "Colchete" (ADR-0030:205-236):
    delimitadores "[" e "]", caixa_alta com valor atual true e valor final
    decidido false, cor_texto e cor_fundo como sem cor diferenciada. A ADR
    preserva nominalmente "Sair", "Voltar", "Ajuda" e "Verboso" e vincula a
    alteracao concreta de caixa_alta ao ciclo de implementacao (ADR-0030:231-236,
    533-537). As secoes de compatibilidade, validacao e rastreabilidade foram
    alinhadas (ADR-0030:489-492, 563-574, 607-608).
  regressao_introduzida: false
  impacto: >
    O achado original sobre preservacao visual dos chips foi tratado; permanece
    apenas o achado novo QA-POS-ADR0030-001 sobre literal de cor sem acento.

- id: QA-ADR0030-002
  status: RESOLVIDO
  evidencia: >
    A ADR separa decisao do usuario, regra contratual preexistente, evidencia
    do levantamento e decisao tecnica de handoff em 13.1 e 13.2
    (ADR-0030:600-650). D8 nao escolhe nome, modulo ou assinatura do loader
    (ADR-0030:283-296); D9 delimita unidade tecnica e duplicidade raw ao
    handoff (ADR-0030:318-320); D10 limita consumidores a aparencia global
    resolvida, separada de estado vivo e declaracao de tela (ADR-0030:322-345).
  regressao_introduzida: false
  impacto: >
    Genealogia semantica adequada para orientar handoff futuro sem transformar
    levantamento em origem decisoria.

- id: QA-ADR0030-003
  status: RESOLVIDO
  evidencia: >
    A aplicacao documental altera somente documentos normativos
    (ADR-0030:518-527). Alteracoes em config/estilo.json, incluindo
    preset_default de borda/chip e caixa_alta false, pertencem ao ciclo de
    implementacao (ADR-0030:529-549). A promocao de _meta.status esta deferida
    (ADR-0030:592), e valores de cor_inativo, cor_alerta e tiling permanecem
    nao decididos (ADR-0030:586-587).
  regressao_introduzida: false
  impacto: >
    A configuracao executavel nao foi indevidamente incluída na aplicacao
    documental da ADR.

- id: QA-ADR0030-004
  status: RESOLVIDO
  evidencia: >
    D9 preserva a regra contratual de exatamente um caractere conforme R-6,
    mas nao redefine caractere como code point, grapheme cluster ou largura
    visual de terminal (ADR-0030:311, 318). A ADR exige bloqueio documental se
    a autoridade vigente se mostrar insuficiente, nao exige parser raw especial
    e limita duplicidade ao observavel na estrutura materializada
    (ADR-0030:318-320).
  regressao_introduzida: false
  impacto: >
    A unidade tecnica ficar para o handoff nao contradiz a autoridade
    contratual, pois a autoridade vigente estabelece a restricao mas nao fecha
    a unidade operacional Unicode.

- id: QA-ADR0030-005
  status: RESOLVIDO
  evidencia: >
    A matriz nominal de propagacao documental inclui os oito arquivos exigidos
    (ADR-0030:699-708). contrato_estilo.md esta como ATUALIZAR; o indice de
    ADR so deve ser atualizado depois de parecer favoravel do QA; contratos
    consultados nao foram automaticamente marcados para alteracao; e
    nomenclaturas ficaram condicionadas a impacto terminologico real.
  regressao_introduzida: false
  impacto: >
    Nao ha propagacao obrigatoria previsivel omitida no patch.
```

## 5. Ordem dos chips

```yaml
ordem_futura_auditada: "[Esc] -> [✥] -> [⏎] -> [V] -> [?]"
resultado: CONFORME
evidencia:
  contrato_barra_de_menus:
    ordem_canonica_completa: docs/contratos/contrato_barra_de_menus.md:183-190
    declaracao_preserva_ordem: docs/contratos/contrato_barra_de_menus.md:511-532
  adr:
    esclarecimento_bloco_2: docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md:392-405
validacoes:
  politica_declaracao_preserva_chips: true
  declaracao_deve_respeitar_ordem_canonica: true
  renderer_nao_reordena_automaticamente: true
  registro_apenas_esclarecimento_bloco_2: true
  obrigacao_funcional_bloco_1_introduzida: false
```

## 6. Regressões

```yaml
D1_a_D13:
  preset_borda: "Borda Curva"
  preset_chip: "Colchete"
  preset_cursor: "Seta"
  preset_inclusao: "Círculo"
  fallback_silencioso: proibido
  tipo_borda_no_estado_final: ausente
  tela_de_estilo: deferida
  Bloco_2: fora_do_escopo
  Bloco_3: fora_do_escopo
  status_ADR: proposta
hardcoding:
  frase_auditada: "Nenhum símbolo, cor ou caractere de estilo aparece hardcoded no código de produção."
  resultado: CONFORME
  justificativa: >
    A expressao "de estilo" delimita a proibicao ao dominio de aparencia
    configuravel. D1 tambem restringe o escopo a simbolo, cor, caractere de
    borda ou moldura de chip vindos do objeto de estilo resolvido.
regressoes_identificadas: []
```

## 7. Achados novos

```yaml
achados_novos:
  - id: QA-POS-ADR0030-001
    severidade: baixa
    tema: literal_de_cor_padrao_sem_acento
    evidencia: >
      A ADR registra cor_texto e cor_fundo do preset "Colchete" como
      "padrao" em D5 e compatibilidade (ADR-0030:212-226, 234, 491). O
      arquivo material config/estilo.json usa "padrão" com acento para esses
      campos (config/estilo.json:49-50), e o contrato de estilo exemplifica
      nomes semanticos de cor com "padrão" (contrato_estilo.md:101-104).
    regra_ou_autoridade: >
      config/estilo.json e a camada de dados concreta; contrato_estilo.md
      define cor_texto/cor_fundo como nomes semanticos de cor e usa "padrão"
      como literal documentado.
    impacto: >
      A ADR preserva a decisao substantiva de nao introduzir cor nova, mas
      registra um literal diferente do valor material e contratual. Isso pode
      induzir handoff ou implementacao a trocar "padrão" por "padrao" sem
      decisao explicita sobre normalizacao.
    correcao_necessaria: >
      Corrigir a ADR para usar o literal material e contratual "padrão", ou
      registrar explicitamente uma decisao de normalizacao para "padrao" com
      propagacao aos contratos/configuracao aplicaveis.
    decisao_do_usuario_necessaria: false
achados_novos_por_severidade:
  alta: 0
  media: 0
  baixa: 1
```

## 8. Checks finais

```yaml
- comando: git status --short --untracked-files=all
  codigo_saida: 0
  contagem: 5 entradas
  saida_resumo:
    - "?? docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md"
    - "?? docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md"
    - "?? docs/relatorios/RELATORIO_PATCH_ADR-0030.md"
    - "?? docs/relatorios/RELATORIO_QA_ADR-0030.md"
    - "?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0030.md"

- comando: git diff --check
  codigo_saida: 0
  contagem: 0 problemas
  saida_resumo: vazio

- comando: git diff --cached --check
  codigo_saida: 0
  contagem: 0 problemas
  saida_resumo: vazio

- comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest
  codigo_saida: 0
  contagem: 422 testes
  saida_resumo: "422 passed in 16.58s"
```

## 9. Gate minimo do relatorio

```yaml
arquivo_correto: true
etapa_correta: QA_POS_PATCH_ADR
modo: RECUPERACAO_POS_REINICIALIZACAO
artefato_auditado: docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
qa_inicial: docs/relatorios/RELATORIO_QA_ADR-0030.md
relatorio_patch: docs/relatorios/RELATORIO_PATCH_ADR-0030.md
relatorio_parcial_preexistente: null
arquivo_de_saida_efetivo: docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0030.md
status_literal: proposta
ultima_linha_ou_encerramento: ADR_PATCH_REQUIRED
achados_originais:
  QA-ADR0030-001: RESOLVIDO
  QA-ADR0030-002: RESOLVIDO
  QA-ADR0030-003: RESOLVIDO
  QA-ADR0030-004: RESOLVIDO
  QA-ADR0030-005: RESOLVIDO
achados_novos_por_severidade:
  alta: 0
  media: 0
  baixa: 1
bloqueios: []
arquivos_alterados_pelo_QA:
  - docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0030.md
estado_git:
  stage: VAZIO
  entradas_status:
    - "?? docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md"
    - "?? docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md"
    - "?? docs/relatorios/RELATORIO_PATCH_ADR-0030.md"
    - "?? docs/relatorios/RELATORIO_QA_ADR-0030.md"
    - "?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0030.md"
```

## 10. Status final

ADR_PATCH_REQUIRED
