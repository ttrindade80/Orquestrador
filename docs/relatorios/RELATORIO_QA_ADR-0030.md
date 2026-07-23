---
name: relatorio-qa-adr-0030
description: QA documental independente da ADR-0030 sobre carregamento global e materializacao do estilo
metadata:
  type: relatorio
  etapa: QA_ADR
  status: concluido
---

# Relatorio QA ADR-0030

## 1. Gate minimo

```yaml
arquivo_correto: true
etapa_correta: QA_ADR
artefato_auditado: docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
status_literal:
  metadata.status: proposta
  secao_status: proposta
ultima_linha_ou_encerramento: ADR_PATCHED_AWAITING_QA
achados_por_severidade:
  alta: 1
  media: 3
  baixa: 1
bloqueios: []
arquivos_alterados_pelo_QA:
  - docs/relatorios/RELATORIO_QA_ADR-0030.md
estado_git:
  stage: VAZIO
  observacao: ADR-0030 e relatorio de levantamento estavam nao rastreados antes deste QA
status_final: ADR_PATCH_REQUIRED
```

## 2. Estado e integridade da ADR

```yaml
arquivo_correto: true
numero_ADR: ADR-0030
metadata_status: proposta
status_no_corpo: proposta
encerramento: ADR_PATCHED_AWAITING_QA
origem_declarada: decisao_explicita_do_usuario
stage: VAZIO
```

A ADR nao se declara aceita, aprovada, aplicada ou implementada. O status em
front matter esta em `proposta` e a secao 2 afirma que a ADR aguarda QA
independente antes de aplicacao documental e implementacao.

## 3. Autoridades lidas

Leitura seletiva executada a partir de `docs/nomenclatura/00_INDICE.md`.
Foram lidos somente os modulos exigidos pelo roteiro:

- `docs/nomenclatura/01_NUCLEO_COMUM.md`
- `docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md`
- `docs/nomenclatura/10_ESTILO.md`
- `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`
- `docs/nomenclatura/32_CONSOLE.md`
- `docs/contratos/contrato_estilo.md`
- `docs/contratos/contrato_chip.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_console.md`
- `config/estilo.json`
- `docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md`

## 4. Conclusao semantica

A ADR preserva o eixo decisorio principal do usuario: `config/estilo.json` como
fonte global exclusiva de aparencia, escolha global, catalogo com opcao ativa,
preservacao da aparencia inicial, tela de alteracao deferida e separacao entre
os tres blocos.

O QA, porem, encontrou problemas corrigiveis antes da aprovacao:
rastreabilidade superatribui decisoes tecnicas ao usuario; a preservacao visual
do preset de chip esta incompleta; a secao de aplicacao documental inclui
alteracao de configuracao executavel e ativacao de `_meta.status` sem criterio
suficiente; e D9 precisa delimitar validacoes cuja semantica operacional ainda
esta ambigua.

## 5. Achados

```yaml
- id: QA-ADR0030-001
  severidade: alta
  tema: preservacao_visual_chip
  evidencia: >
    A ADR declara que o preset "Colchete" reproduz exatamente a moldura atual
    considerando apenas caractere_esquerdo e caractere_direito
    (ADR-0030:187-207, 429-431). Mas o proprio ciclo de implementacao exige
    consumir tambem cor_texto, caixa_alta e cor_fundo (ADR-0030:466-472).
    Em config/estilo.json, "Colchete" contem cor_texto "padrao",
    cor_fundo "padrao" e caixa_alta true (config/estilo.json:46-51).
    O renderer atual monta "[{tecla}] {texto}" sem aplicar uppercase
    (tela/renderizador.py:1140-1144), e os JSONs de tela usam textos como
    "Sair", "Voltar", "Ajuda" e "Verboso".
  regra_ou_autoridade: >
    Decisao explicita do usuario: primeira implementacao preserva a aparencia
    atualmente utilizada. contrato_estilo.md:89-112 define os cinco campos de
    chip, incluindo caixa_alta; contrato_chip.md:12 define que aparencia visual
    do chip vem do estilo.
  impacto: >
    Consumir integralmente o preset "Colchete" com caixa_alta true pode alterar
    a aparencia inicial dos chips, embora a ADR declare preservacao exata. A
    correspondencia esta provada apenas para delimitadores, nao para todos os
    campos que a propria ADR manda consumir.
  correcao_necessaria: >
    Completar a analise de preservacao visual do chip para todos os cinco
    campos do preset. A ADR deve explicitar se caixa_alta e cores preservam a
    aparencia vigente, se algum campo fica fora do Bloco 1, ou se o preset/
    contrato devera ser ajustado para manter o visual atual.
  decisao_do_usuario_necessaria: true

- id: QA-ADR0030-002
  severidade: media
  tema: genealogia_semantica_D8_D11
  evidencia: >
    A rastreabilidade agrupa D8-D11 como "Decisao explicita do usuario"
    (ADR-0030:530). D8 define ordem de carregamento, validacao, materializacao,
    disponibilizacao e nao releitura por render (ADR-0030:247-260). D9 define
    matriz detalhada de erros do loader (ADR-0030:262-280). D10 define contrato
    de consumidores (ADR-0030:282-305). Parte dessas regras decorre de
    contrato_estilo.md:149-174 e R-1 a R-8, ou e escolha tecnica para handoff.
  regra_ou_autoridade: >
    As decisoes explicitas do usuario cobrem fonte global exclusiva, listas de
    opcoes com opcao ativa, escolha global, edicao centralizada, preservacao
    visual, tela futura e divisao em tres blocos. O levantamento e evidencia
    material, nao origem decisoria.
  impacto: >
    A ADR usa coerencia contratual e inferencia tecnica como se fossem prova de
    origem no usuario. Isso prejudica a genealogia exigida entre decisao do
    usuario, evidencia material, regra contratual preexistente e escolha tecnica
    do handoff.
  correcao_necessaria: >
    Separar a origem de D8-D11 item a item: o que vem diretamente do usuario,
    o que vem dos contratos vigentes, o que vem do levantamento, e o que deve
    permanecer como decisao tecnica do handoff.
  decisao_do_usuario_necessaria: false

- id: QA-ADR0030-003
  severidade: media
  tema: aplicacao_documental_configuracao_executavel
  evidencia: >
    A secao 10.1 classifica como "Aplicacao documental" a alteracao de
    config/estilo.json, incluindo adicionar preset_default em borda e chip e
    mudar _meta.status de "rascunho_inicial" para "ativo" (ADR-0030:457-462).
    O modulo 02 define config/estilo.json como configuracao concreta em config/,
    isto e, documento que guarda valores concretos lidos em runtime. O arquivo
    atual declara status "rascunho_inicial" e pendencias de cor_inativo,
    cor_alerta e tiling (config/estilo.json:2-11).
  regra_ou_autoridade: >
    Configuracao concreta guarda valores concretos de execucao em config/; nao
    e artefato docs. A decisao explicita do usuario autorizou fonte global e
    opcao ativa, mas nao definiu criterio para promover _meta.status a "ativo".
  impacto: >
    Alteracao de configuracao executavel pode ser aplicada antes do ciclo de
    implementacao/validacao correspondente. A mudanca de status para "ativo"
    fica sem criterio material claro, especialmente com pendencias ainda
    registradas no proprio arquivo.
  correcao_necessaria: >
    Reclassificar alteracoes em config/estilo.json como migracao de
    configuracao dentro do ciclo de handoff/implementacao, ou justificar
    explicitamente por que pertencem a aplicacao documental. Definir criterio
    para _meta.status "ativo" ou retirar essa exigencia da ADR.
  decisao_do_usuario_necessaria: false

- id: QA-ADR0030-004
  severidade: media
  tema: validacoes_D9_ambiguidade_operacional
  evidencia: >
    D9 exige "comprimento diferente de 1" para simbolos/caracteres e "opcoes
    duplicadas em catalogo" (ADR-0030:275-278). O contrato vigente R-6 fala em
    exatamente 1 caractere para preservar alinhamento colunar
    (contrato_estilo.md:258-262). Em JSON objeto, chaves duplicadas podem ser
    perdidas pelo parser antes de chegar a estrutura materializada, salvo
    validacao raw especifica.
  regra_ou_autoridade: >
    contrato_estilo.md R-6 autoriza a restricao de exatamente 1 caractere, mas
    nao define unidade tecnica de medicao (code point, grapheme cluster ou
    largura visual de terminal). O roteiro de QA exige distinguir comprimento
    Unicode de largura visual.
  impacto: >
    O handoff pode implementar validacoes incompatíveis entre si: contar
    codepoints, contar caracteres percebidos, medir largura de terminal, ou
    tentar detectar duplicidade apos parse JSON quando a informacao ja pode ter
    sido descartada.
  correcao_necessaria: >
    Delimitar D9 conforme a autoridade vigente: validar "1 caractere" sem
    inventar politica de largura visual, ou explicitar que largura terminal e
    duplicidade raw ficam deferidas/especificadas pelo handoff. Definir quando
    "opcoes duplicadas" e materialmente aplicavel.
  decisao_do_usuario_necessaria: false

- id: QA-ADR0030-005
  severidade: baixa
  tema: documentos_afetados_incompletos
  evidencia: >
    O front matter lista config/estilo.json, tela/renderizador.py e
    tela/loader.py como documentos afetados (ADR-0030:14-17), e contratos
    afetados (ADR-0030:19-23). A secao 13 lista autoridades consultadas, mas a
    secao de migracao so cita contrato_estilo.md como documento normativo a
    atualizar (ADR-0030:457-462), apesar de contrato_chip.md,
    contrato_barra_de_menus.md e contrato_console.md serem declarados afetados
    e de D1-D3 impactarem nomenclatura de estilo.
  regra_ou_autoridade: >
    O roteiro exige auditar documentos normativos afetados, configuracao
    afetada, componentes tecnicos futuros, indices/modulos a atualizar e
    ausencia de handoff criado.
  impacto: >
    A aplicacao posterior pode atualizar somente contrato_estilo.md e deixar
    inconsistencias previsiveis em contratos afetados ou modulos de
    nomenclatura, especialmente sobre preset_default de borda/chip e consumo
    integral dos campos de chip.
  correcao_necessaria: >
    Tornar a lista de propagacao documental explicita: quais contratos e
    modulos devem ser atualizados, quais apenas consultados, e se
    docs/adr/INDICE_ADR.md deve ser atualizado apenas apos aceite da ADR.
  decisao_do_usuario_necessaria: false
```

## 6. Itens auditados sem achado bloqueante

```yaml
autoridade_global:
  resultado: aderente_com_ressalvas_de_rastreabilidade
  observacao: D1 distingue aparencia global de declaracao comportamental da tela.

fronteiras_runtime:
  resultado: suficiente
  observacao: D8 e D10 excluem estado vivo de navegacao, selecao, cursor e foco.

modelo_catalogo:
  resultado: aderente_com_ressalva_de_origem
  observacao: Preserva indicadores.selecionado e indicadores.incluido com preset_default; preserva concluido como par direto; nao uniformiza concluido.

borda:
  resultado: correspondencia_material_exata
  observacao: "Borda Curva" reproduz os sete caracteres atuais de _BORDAS["curva"].

cursor:
  resultado: correspondencia_material_exata
  observacao: preset "Seta" preserva simbolo "→".

incluido:
  resultado: correspondencia_material_exata
  observacao: preset "Circulo" preserva on "●" e off "○".

escopo_integral:
  resultado: suficiente_com_deferimentos
  observacao: A ADR le as secoes reais vigentes e defere cor_inativo, cor_alerta e tiling como pendencias, sem inventar valores.

separacao_blocos:
  resultado: suficiente
  observacao: Navegacao, selecao unica, Enter, selecao multipla, toggle e tela de resultados permanecem fora do Bloco 1.

migracao_tipo_borda:
  resultado: suficiente
  observacao: Estado final unico sem coexistencia permanente; tolerancia transitoria limitada ao ciclo de implementacao.
```

## 7. Genealogia resumida

```yaml
decisao_do_usuario:
  - config/estilo.json como fonte global e exclusiva de aparencia
  - arquivo com catalogos/listas de opcoes e opcao ativa
  - escolha global, nao por tela
  - novas opcoes por edicao centralizada em categorias existentes
  - primeira implementacao preserva aparencia vigente
  - tela de escolha de estilo deferida
  - tres blocos independentes com ADR, handoff e implementacao proprios

evidencia_do_levantamento:
  - borda e chip possuem catalogos sem preset_default
  - indicadores.selecionado e indicadores.incluido ja possuem preset_default
  - concluido e par direto
  - renderer hardcoda borda e moldura de chip
  - nao ha loader ativo de estilo confirmado

regra_contratual_preexistente:
  - campos obrigatorios de borda, chip e indicadores
  - materializacao dos indicadores para campos planos
  - proibicao de hardcoding de estilo
  - objeto de estilo ativo por sessao
  - restricao de exatamente 1 caractere

escolha_tecnica_de_handoff:
  - nome/assinatura do loader ou camada equivalente
  - mecanismo de deteccao de duplicidade raw em JSON
  - unidade tecnica de validacao Unicode se precisar exceder o literal contratual
  - estrategia de transicao de chamadas que ainda fornecem tipo_borda
```

## 8. Decisoes deferidas

```yaml
deferidas_corretamente:
  - tela de escolha de estilo
  - persistencia da escolha
  - pre-visualizacao
  - restauracao de padrao
  - troca durante sessao
  - reinicializacao
  - valores de cor_inativo
  - valores de cor_alerta
  - valor de tiling
  - simbolo estatico em tg
  - conversao de concluido em catalogo
  - Bloco 2
  - Bloco 3
deferida_e_exigida_simultaneamente: []
```

## 9. Checks executados

```yaml
- comando: git status --short
  codigo_saida: 0
  contagem: 2 entradas
  saida_resumo:
    - "?? docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md"
    - "?? docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md"

- comando: git diff --check
  codigo_saida: 0
  contagem: 0 problemas

- comando: git diff --cached --check
  codigo_saida: 0
  contagem: 0 problemas

- comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest
  codigo_saida: 0
  contagem: 422 testes
  saida_resumo: "422 passed in 16.60s"
```

## 10. Estado Git

```yaml
stage: VAZIO
relatorio_criado: docs/relatorios/RELATORIO_QA_ADR-0030.md
arquivos_nao_rastreados_antes_do_QA:
  - docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
  - docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md
alteracoes_permitidas_pelo_QA:
  - docs/relatorios/RELATORIO_QA_ADR-0030.md
```

## 11. Status final

ADR_PATCH_REQUIRED
