---
name: relatorio-qa-aplicacao-adr-0030
description: QA documental independente da aplicacao da ADR-0030
metadata:
  type: relatorio_qa
  etapa: QA_APLICACAO_ADR
  adr: ADR-0030
  data: "2026-07-22"
---

# Relatorio - QA da aplicacao documental da ADR-0030

## 1. Gate minimo

```yaml
arquivo_correto: true
etapa_correta: QA_APLICACAO_ADR
adr_auditada: docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
relatorio_aplicacao_auditado: docs/relatorios/RELATORIO_APLICACAO_ADR-0030.md
arquivo_de_saida_efetivo: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0030.md

status_ADR:
  metadata.status: aceita
  status_na_identificacao: aceita
  status_na_secao_2: aceita
encerramento_ADR: APLICACAO_ADR_CONCLUIDA_AGUARDANDO_QA

arquivos_declarados_como_alterados:
  - docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
  - docs/adr/INDICE_ADR.md
  - docs/contratos/contrato_estilo.md
  - docs/nomenclatura/10_ESTILO.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0030.md
arquivos_materialmente_alterados:
  rastreados_modificados:
    - docs/adr/INDICE_ADR.md
    - docs/contratos/contrato_estilo.md
    - docs/nomenclatura/10_ESTILO.md
  nao_rastreados_relacionados_a_cadeia_ADR_0030:
    - docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0030.md
    - docs/relatorios/RELATORIO_CORRECAO_ENCERRAMENTO_QA_POS_PATCH_02_ADR-0030.md
    - docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md
    - docs/relatorios/RELATORIO_PATCH_02_ADR-0030.md
    - docs/relatorios/RELATORIO_PATCH_ADR-0030.md
    - docs/relatorios/RELATORIO_QA_ADR-0030.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_02_ADR-0030.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0030.md
arquivos_declarados_como_preservados:
  - docs/contratos/contrato_chip.md
  - docs/contratos/contrato_barra_de_menus.md
  - docs/contratos/contrato_console.md
  - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
  - docs/nomenclatura/32_CONSOLE.md
preservacoes_confirmadas:
  - docs/contratos/contrato_chip.md
  - docs/contratos/contrato_barra_de_menus.md
  - docs/contratos/contrato_console.md
  - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
  - docs/nomenclatura/32_CONSOLE.md
  - config/estilo.json
  - tela/
desvios_de_escopo: []

decisoes_D1_D13: ver_matriz_secao_9
contradicoes_ativas:
  - QA-APLICACAO-ADR0030-001
termos_antigos_ativos:
  tipo_borda: MIGRACAO_FUTURA
  _BORDAS: MIGRACAO_FUTURA
  padrao_sem_acento: FORA_DO_ESCOPO_LINGUISTICO
implementacao_indevida: false

achados_por_severidade:
  bloqueante: 0
  alta: 0
  media: 1
  baixa: 0
  observacao: 0
bloqueios: []
arquivos_alterados_pelo_QA:
  - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0030.md
estado_git: stage_vazio
pytest:
  status: passou
  total: 422
status_final: ADR_APPLICATION_REJECTED
```

## 2. Estado Git inicial

```yaml
raiz: /home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador
branch: master
HEAD: 2caf036 test: adota pytest como padrao unico
stage: VAZIO
git_diff_check: sem_apontamentos
git_diff_cached_check: sem_apontamentos
arquivos_modificados:
  - docs/adr/INDICE_ADR.md
  - docs/contratos/contrato_estilo.md
  - docs/nomenclatura/10_ESTILO.md
arquivos_nao_rastreados:
  - docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0030.md
  - docs/relatorios/RELATORIO_CORRECAO_ENCERRAMENTO_QA_POS_PATCH_02_ADR-0030.md
  - docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md
  - docs/relatorios/RELATORIO_PATCH_02_ADR-0030.md
  - docs/relatorios/RELATORIO_PATCH_ADR-0030.md
  - docs/relatorios/RELATORIO_QA_ADR-0030.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_02_ADR-0030.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0030.md
arquivos_inesperados: []
impossibilidades_de_atribuicao_de_proveniencia:
  - os artefatos novos da cadeia ADR-0030 estao nao rastreados; a autoria exata nao pode ser provada por diff contra HEAD, mas a cadeia material permite auditar conteudo e escopo
```

## 3. Existencia dos artefatos

```yaml
artefatos_obrigatorios:
  docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md: existe
  docs/adr/INDICE_ADR.md: existe
  docs/contratos/contrato_estilo.md: existe
  docs/nomenclatura/10_ESTILO.md: existe
  docs/relatorios/RELATORIO_APLICACAO_ADR-0030.md: existe
cadeia_historica_completa:
  docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md: existe
  docs/relatorios/RELATORIO_QA_ADR-0030.md: existe
  docs/relatorios/RELATORIO_PATCH_ADR-0030.md: existe
  docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0030.md: existe
  docs/relatorios/RELATORIO_PATCH_02_ADR-0030.md: existe
  docs/relatorios/RELATORIO_QA_POS_PATCH_02_ADR-0030.md: existe
  docs/relatorios/RELATORIO_CORRECAO_ENCERRAMENTO_QA_POS_PATCH_02_ADR-0030.md: existe
```

## 4. ADR

```yaml
metadata.status: aceita
status_na_identificacao: aceita
status_na_secao_2: aceita
ultima_linha: APLICACAO_ADR_CONCLUIDA_AGUARDANDO_QA
ADR_aprovada: true
aplicacao_documental_executada: true
qa_da_aplicacao: pendente
configuracao_executavel_migrada: false
implementacao_executada: false
Bloco_1_concluido:
  explicitado_na_secao_status: false
  inferivel_por_contexto: false
```

A ADR nao afirma loader implementado, renderer convertido, `config/estilo.json`
migrado, testes atualizados, hardcodings removidos, navegacao ou selecao
implementadas. A omissao material e a ausencia da distincao explicita
`Bloco_1_concluido: false`, exigida pelo roteiro desta auditoria.

## 5. Indice de ADRs

```yaml
numero: ADR-0030
titulo: Carregamento global e materialização do estilo
status: aceita
data: 2026-07-22
resultado: CONFORME
```

A entrada representa `config/estilo.json` como autoridade global exclusiva,
catalogo com `preset_default`, materializacao integral, presets ativos globais,
preservacao visual inicial, remocao futura de hardcodings e Blocos 2 e 3 fora
do escopo. Nao registra implementacao concluida.

## 6. Contratos e nomenclatura

```yaml
contrato_estilo:
  autoridade_global_de_aparencia: config/estilo.json
  escolha: global
  escolha_por_tela: nao_concorrente
  borda:
    presets: obrigatorio
    preset_default: obrigatorio
    preset_inicial: "Borda Curva"
    campos_runtime: 7
  chip:
    presets: obrigatorio
    preset_default: obrigatorio
    preset_inicial: "Colchete"
    campos_runtime:
      - caractere_esquerdo
      - caractere_direito
      - cor_texto
      - caixa_alta
      - cor_fundo
  indicadores:
    selecionado:
      preset_inicial: "Seta"
    incluido:
      preset_inicial: "Círculo"
    concluido:
      estrutura: par_direto_on_off
  validacoes_D9: propagadas
  fronteira_com_implementacao: preservada

contrato_chip:
  preservacao_correta: true
  compatibilidade:
    - aparencia_origem_estilo_global
    - cinco_campos_do_preset
    - caixa_alta_controla_apresentacao
    - conteudo_e_ordem_pertencem_a_barra

contrato_barra_de_menus:
  preservacao_correta: true
  ordem_canonica_preservada: true
  renderer_sem_reordenacao_automatica_quando_declaracao: true
  ordem_futura_Bloco_2: "[Esc] -> [✥] -> [⏎] -> [V] -> [?]"
  comportamento_Bloco_1_criado: false

contrato_console:
  preservacao_correta: true
  separa_simbolos_materializados_de_estado_vivo: suficiente
  comportamento_novo_introduzido: false

nomenclatura_10_ESTILO:
  alteracao_compativel: true
  define_estilo_global: true
  distingue_catalogo_preset_ativo_preset_resolvido: true
  distingue_configuracao_persistida_de_runtime: true
  distingue_aparencia_de_estado_vivo: true
  arquitetura_concreta_introduzida: false
  implementacao_concluida_declarada: false

nomenclatura_31_BARRA_DE_MENUS_E_CHIPS:
  preservacao_correta: true
  compatibilidade: aparência delegada ao modulo 10; conteudo e ordem preservados

nomenclatura_32_CONSOLE:
  preservacao_correta: true
  compatibilidade: indicadores como presets equivalentes; cursor e inclusao como estados vivos futuros
```

## 7. Configuracao, codigo e testes

```yaml
config/estilo.json:
  alterado_por_git_diff: false
  borda.preset_default: ausente
  chip.preset_default: ausente
  chip.presets.Colchete.caixa_alta: true
  _meta.status: rascunho_inicial
  classificacao: pendencia_de_implementacao_nao_falha_da_aplicacao_documental

codigo_e_testes:
  tela_diff: vazio
  scripts_dir: ausente_no_layout_atual
  testes_dir: ausente_no_layout_atual
  testes_em_tela: sem_diff
  alteracao_atribuivel_a_aplicacao_documental: false
```

## 8. Residuos e contradicoes

```yaml
preset_default: ATIVA_E_CONFORME
Borda_Curva: ATIVA_E_CONFORME
Colchete: ATIVA_E_CONFORME
caixa_alta: ATIVA_E_CONFORME
cor_texto: ATIVA_E_CONFORME
cor_fundo: ATIVA_E_CONFORME
padrão: ATIVA_E_CONFORME
padrao:
  classificacao: FORA_DO_ESCOPO
  evidencia: ocorre apenas em texto linguistico sem acento em config/estilo.json _meta.pendencias; nao ocorre como valor de cor_texto/cor_fundo
tipo_borda: MIGRACAO_FUTURA
_BORDAS: MIGRACAO_FUTURA
selecionado_simbolo: ATIVA_E_CONFORME
selecionado_off: ATIVA_E_CONFORME
incluido_on: ATIVA_E_CONFORME
incluido_off: ATIVA_E_CONFORME
concluido_on: ATIVA_E_CONFORME
concluido_off: ATIVA_E_CONFORME
navegacao: MIGRACAO_FUTURA
selecao: MIGRACAO_FUTURA
Enter: MIGRACAO_FUTURA
contradicoes_ativas:
  - ausencia_explicita_de_Bloco_1_concluido_false_na_ADR
```

## 9. Matriz de propagacao D1-D13

| Decisao | ADR | Indice | Contrato de estilo | Outros contratos | Nomenclatura | Relatorio de aplicacao | Resultado |
| ------- | --- | ------ | ------------------ | ---------------- | ------------ | ---------------------- | --------- |
| D1 | PROPAGADA | PROPAGADA | PROPAGADA | PRESERVADA_POR_REFERENCIA | PROPAGADA | PROPAGADA | PROPAGADA |
| D2 | PROPAGADA | PROPAGADA | PROPAGADA | NAO_APLICAVEL | PROPAGADA | PROPAGADA | PROPAGADA |
| D3 | PROPAGADA | PROPAGADA | PROPAGADA | PRESERVADA_POR_REFERENCIA | PROPAGADA | PROPAGADA | PROPAGADA |
| D4 | PROPAGADA | PROPAGADA | PROPAGADA | NAO_APLICAVEL | PROPAGADA | PROPAGADA | PROPAGADA |
| D5 | PROPAGADA | PROPAGADA | PROPAGADA | PRESERVADA_POR_REFERENCIA | PROPAGADA | PROPAGADA | PROPAGADA |
| D6 | PROPAGADA | PROPAGADA | PROPAGADA | PRESERVADA_POR_REFERENCIA | PROPAGADA | PROPAGADA | PROPAGADA |
| D7 | PROPAGADA | PROPAGADA | PROPAGADA | PRESERVADA_POR_REFERENCIA | PROPAGADA | PROPAGADA | PROPAGADA |
| D8 | PROPAGADA | PROPAGADA | PROPAGADA | PRESERVADA_POR_REFERENCIA | PROPAGADA | PROPAGADA | PROPAGADA |
| D9 | PROPAGADA | NAO_APLICAVEL | PROPAGADA | NAO_APLICAVEL | PRESERVADA_POR_REFERENCIA | PROPAGADA | PROPAGADA |
| D10 | PROPAGADA | NAO_APLICAVEL | PROPAGADA | PRESERVADA_POR_REFERENCIA | PROPAGADA | PROPAGADA | PROPAGADA |
| D11 | PROPAGADA | NAO_APLICAVEL | PROPAGADA | NAO_APLICAVEL | PRESERVADA_POR_REFERENCIA | PRESERVADA_COMO_DEFERIMENTO | PROPAGADA |
| D12 | PROPAGADA | NAO_APLICAVEL | PRESERVADA_COMO_DEFERIMENTO | NAO_APLICAVEL | PRESERVADA_POR_REFERENCIA | PRESERVADA_COMO_DEFERIMENTO | PRESERVADA_COMO_DEFERIMENTO |
| D13 | PROPAGADA | PROPAGADA | PRESERVADA_COMO_DEFERIMENTO | PRESERVADA_POR_REFERENCIA | PRESERVADA_POR_REFERENCIA | PRESERVADA_COMO_DEFERIMENTO | PRESERVADA_COMO_DEFERIMENTO |

## 10. Fidelidade do relatorio de aplicacao

```yaml
estado_inicial: registrado
autoridade_da_aprovacao: registrada
arquivos_autorizados: registrados
arquivos_realmente_alterados: registrados
documentos_inspecionados_e_preservados: registrados
propagacao_D1_D13: registrada
configuracao_preservada: registrada_e_confirmada
codigo_preservado: registrado_e_confirmado
testes_preservados: registrado_e_confirmado
stage_vazio: registrado_e_confirmado
QA_da_aplicacao_pendente: registrado
proxima_categoria: QA_APLICACAO_ADR
encerramento: APLICACAO_ADR_CONCLUIDA_AGUARDANDO_QA
inexatidao_material:
  - o relatorio nao identifica a ausencia obrigatoria de Bloco_1_concluido_false na ADR aplicada
```

## 11. Achados

```yaml
- id: QA-APLICACAO-ADR0030-001
  severidade: media
  tema: status_e_encerramento_da_ADR
  arquivo: docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
  evidencia: >
    A secao 2 da ADR registra status aceita, aplicacao documental executada,
    QA da aplicacao pendente, config/estilo.json nao migrado e implementacao
    nao realizada. O encerramento tambem registra configuracao_executavel_migrada:
    false e implementacao_executada: false. Nenhuma dessas secoes materializa
    explicitamente Bloco_1_concluido: false.
  autoridade: >
    Roteiro desta auditoria, secao 3: a secao de status deve distinguir
    ADR_aprovada: true, aplicacao_documental_executada: true,
    qa_da_aplicacao: pendente, configuracao_executavel_migrada: false,
    implementacao_executada: false e Bloco_1_concluido: false.
  impacto: >
    A ADR aplicada deixa ambigua a fronteira entre aplicacao documental
    concluida e Bloco 1 concluido. Isso e corrigivel documentalmente, mas
    impede aprovar a aplicacao nos termos estritos do gate solicitado.
  correcao_necessaria: >
    Registrar explicitamente na ADR, na secao de status ou encerramento,
    Bloco_1_concluido: false, preservando que a aplicacao documental esta
    concluida e que a implementacao/migracao do Bloco 1 permanece futura.
  decisao_do_usuario_necessaria: false
```

## 12. Checks finais

```yaml
- comando: git status --short --untracked-files=all
  codigo_saida: 0
  contagem: 13 entradas
  resumo:
    - " M docs/adr/INDICE_ADR.md"
    - " M docs/contratos/contrato_estilo.md"
    - " M docs/nomenclatura/10_ESTILO.md"
    - "?? docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md"
    - "?? docs/relatorios/RELATORIO_APLICACAO_ADR-0030.md"
    - "?? docs/relatorios/RELATORIO_CORRECAO_ENCERRAMENTO_QA_POS_PATCH_02_ADR-0030.md"
    - "?? docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md"
    - "?? docs/relatorios/RELATORIO_PATCH_02_ADR-0030.md"
    - "?? docs/relatorios/RELATORIO_PATCH_ADR-0030.md"
    - "?? docs/relatorios/RELATORIO_QA_ADR-0030.md"
    - "?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0030.md"
    - "?? docs/relatorios/RELATORIO_QA_POS_PATCH_02_ADR-0030.md"
    - "?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0030.md"

- comando: git diff --name-only
  codigo_saida: 0
  contagem: 3 arquivos
  resumo:
    - docs/adr/INDICE_ADR.md
    - docs/contratos/contrato_estilo.md
    - docs/nomenclatura/10_ESTILO.md

- comando: git diff --stat
  codigo_saida: 0
  contagem: "3 arquivos, 210 insercoes, 12 remocoes"
  resumo: "docs/adr/INDICE_ADR.md | 1 +; docs/contratos/contrato_estilo.md | 146 linhas; docs/nomenclatura/10_ESTILO.md | 75 linhas"

- comando: git diff --check
  codigo_saida: 0
  contagem: 0 apontamentos
  resumo: vazio

- comando: git diff --cached --name-only
  codigo_saida: 0
  contagem: 0 arquivos
  resumo: vazio

- comando: git diff --cached --stat
  codigo_saida: 0
  contagem: 0 arquivos
  resumo: vazio

- comando: git diff --cached --check
  codigo_saida: 0
  contagem: 0 apontamentos
  resumo: vazio

- comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest
  codigo_saida: 0
  contagem: 422 testes
  resumo: "422 passed in 16.61s"
```

## 13. Parecer final

```yaml
resultado: ADR_APPLICATION_REJECTED
estado_normalizado: PATCH_DOCUMENTAL_NECESSARIO
proxima_categoria: PATCH_DOCUMENTACAO
fundamento: existe defeito documental corrigivel sem decisao nova
```

ADR_APPLICATION_REJECTED
