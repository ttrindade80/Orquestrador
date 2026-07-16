# Relatorio de QA da ADR-0024

```yaml
status_literal: ARCHITECTURE_REVIEW_REQUIRED
status_normalizado: REVISAO_ARQUITETURAL_REQUERIDA
relatorio: docs/relatorios/RELATORIO_QA_ADR-0024.md
adr_auditada: docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md
aderencia_decisao_usuario:
  resultado: CONFORME
  resumo: >
    A ADR registra integralmente a proibicao de espaco proprio do corpo, proibe
    linhas externas vazias, preenchimento externo, sobra nao atribuida a elemento
    visual, uso de grupo como ocupante visual e permissao implicita por ausencia
    de distribuicao.
coerencia_interna:
  resultado: PARCIALMENTE_CONFORME
  resumo: >
    A norma e coerente como proibicao, mas a propria ADR declara quatro decisoes
    necessarias para implementacao futura sem autoridade ativa que as resolva.
    Isso impede handoff executavel sem revisao arquitetural previa.
autoridades_conflitantes:
  - documento: docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md
    conflito: "clausula 4 autoriza preenchimento com linhas em branco externas"
    tratamento_na_adr: CORRETO
  - documento: docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md
    conflito: "D2 permite sobra externa na ausencia de distribuicao"
    tratamento_na_adr: CORRETO
  - documento: docs/contratos/contrato_composicao_corpo.md
    conflito: "secoes 4.7 e 5.7 preservam preenchimento externo"
    tratamento_na_adr: CORRETO
  - documento: docs/contratos/contrato_tela_json.md
    conflito: "secoes 8 e 9 preservam preenchimento externo"
    tratamento_na_adr: CORRETO
decisoes_adicionais:
  - id: DA-01
    descricao: "mecanismo de expansao de um unico elemento"
    ja_resolvida_por_autoridade_ativa: false
    autoridade: null
    necessaria_para_coerencia_da_adr: false
    necessaria_para_aplicacao_documental: true
    necessaria_para_criar_handoff_exequivel: true
    pode_ser_definida_pelo_executor: false
    classificacao: DECISAO_ARQUITETURAL_NECESSARIA
    justificativa: >
      O caso destino_minimo possui um unico dashboard sem distribuicao. A ADR
      proibe a sobra externa, mas nao decide se a solucao sera distribuicao
      declarativa, regra nova do renderer, novo campo ou outro mecanismo.
  - id: DA-02
    descricao: "distribuicao de area excedente entre multiplos elementos sem distribuicao"
    ja_resolvida_por_autoridade_ativa: false
    autoridade: null
    necessaria_para_coerencia_da_adr: false
    necessaria_para_aplicacao_documental: true
    necessaria_para_criar_handoff_exequivel: true
    pode_ser_definida_pelo_executor: false
    classificacao: DECISAO_ARQUITETURAL_NECESSARIA
    justificativa: >
      A regra da ADR vale para qualquer corpo, nao so para os dois exemplos. Para
      multiplos elementos sem distribuicao, a autoridade ativa ainda proibe tratar
      ausencia como modo igual e nao define quem recebe a sobra.
  - id: DA-03
    descricao: "tratamento de grupo nao integralmente coberto pelos descendentes"
    ja_resolvida_por_autoridade_ativa: false
    autoridade: null
    necessaria_para_coerencia_da_adr: false
    necessaria_para_aplicacao_documental: true
    necessaria_para_criar_handoff_exequivel: true
    pode_ser_definida_pelo_executor: false
    classificacao: DECISAO_ARQUITETURAL_NECESSARIA
    justificativa: >
      O grupo_minimo depende desta decisao: grupo e estrutural, nao visual, mas
      tambem nao existe autoridade ativa que diga como area excedente de grupo
      livre sem distribuicao deve ser transferida ao descendente visual.
  - id: DA-04
    descricao: "comportamento quando o invariante nao puder ser satisfeito"
    ja_resolvida_por_autoridade_ativa: false
    autoridade: null
    necessaria_para_coerencia_da_adr: false
    necessaria_para_aplicacao_documental: true
    necessaria_para_criar_handoff_exequivel: true
    pode_ser_definida_pelo_executor: false
    classificacao: DECISAO_ARQUITETURAL_NECESSARIA
    justificativa: >
      A ADR proibe preenchimento externo e tambem nao autoriza fallback, erro,
      altura minima, alteracao declarativa automatica ou distribuicao implicita.
      Sem regra de falha, um handoff nao consegue especificar criterio completo.
achados_bloqueantes:
  - id: QA-ADR0024-BLOCK-001
    severidade: BLOQUEANTE
    titulo: "DA-01 a DA-04 tornam a futura implementacao nao executavel sem revisao arquitetural"
    evidencia:
      - "ADR-0024:591-610 declara quatro decisoes ausentes necessarias para implementacao."
      - "ADR-0018:113-125 preserva construcao orientada pelo conteudo e sobra externa na ausencia de distribuicao."
      - "contrato_composicao_corpo.md:616-628 repete que ausencia de distribuicao deixa sobra externa."
    impacto: >
      O futuro H-0033 nao pode escolher mecanismo de expansao, politica de
      multiplos elementos, propagacao de area em grupo ou comportamento de falha
      sem criar arquitetura nova.
    recomendacao: "Executar revisao arquitetural especifica antes do handoff de implementacao."
achados_altos: []
achados_medios:
  - id: QA-ADR0024-MED-001
    titulo: "lista de documentos afetados mistura aplicacao documental e implementacao"
    evidencia:
      - "ADR-0024:460-473 lista ADRs, contratos, NOMENCLATURA, indice, renderer e testes no mesmo quadro."
    impacto: >
      A ADR tem secoes separadas de consequencias documentais e tecnicas, mas o
      quadro consolidado nao classifica formalmente aplicacao documental futura
      versus implementacao futura pelo H-0033.
    recomendacao: "Na aplicacao futura, separar documentos normativos de codigo, testes, fixtures e relatorio de implementacao."
achados_baixos:
  - id: QA-ADR0024-LOW-001
    titulo: "referencias internas de secao estao imprecisas"
    evidencia:
      - "ADR-0024:276-279 e 309-311 remetem a secao 20 como decisoes ausentes, mas decisoes ausentes estao na secao 21."
      - "ADR-0024:535-536 remete a secao 19, itens 3 e 4, mas as identidades estao nas secoes 8/9 e nos AC-03/AC-04 da secao 20."
    impacto: "Nao altera a norma, mas reduz precisao operacional do futuro handoff."
observacoes:
  - "A ADR nao inventa algoritmo de expansao, prioridade, distribuicao implicita, fallback, altura minima, alteracao automatica de JSON nem novo tipo de elemento."
  - "A enumeracao de elementos visuais e exatamente console, dashboard e lancador; grupo permanece estrutural."
  - "destino_minimo e grupo_minimo foram identificados corretamente, inclusive a correcao de que nao existe dashboard TESTE em grupo_minimo."
arquivos_observados:
  etapa_observada:
    adr_criada_anteriormente: docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md
    relatorio_criado_neste_qa: docs/relatorios/RELATORIO_QA_ADR-0024.md
  arquivos_no_status_git_final:
    - caminho: docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md
      origem: "ADR criada anteriormente conforme etapa observada"
      produzido_pelo_executor: NAO_CONFIRMADO
      produzido_pelo_usuario: NAO_CONFIRMADO
    - caminho: docs/relatorios/RELATORIO_QA_ADR-0024.md
      origem: "relatorio criado neste QA"
      produzido_pelo_executor: CONFIRMADO
      produzido_pelo_usuario: NAO_CONFIRMADO
  outros_arquivos_no_status_git_final: []
git:
  topo_repositorio: /home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador
  observacao_base_caminhos: >
    O topo Git observado ja e o diretorio operacional que contem docs/ e config/.
    Nao existe subdiretorio scripts/ neste checkout; por isso o comando literal
    com scripts/docs nao aponta para o artefato real.
  comandos:
    - comando: "cd \"$(git rev-parse --show-toplevel)\" && git status --short"
      resultado:
        - "?? docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md"
    - comando: "git diff -- scripts/docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md"
      resultado: "sem saida"
    - comando: "git diff -- docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md"
      resultado: "sem saida; arquivo esta nao rastreado"
    - comando: "git diff --no-index /dev/null docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md"
      resultado: "arquivo novo confirmado; diff exibiu a ADR integral"
    - comando: "git status --short"
      momento: "apos criacao deste relatorio"
      resultado:
        - "?? docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md"
        - "?? docs/relatorios/RELATORIO_QA_ADR-0024.md"
proxima_categoria: ARCHITECTURE_REVIEW_REQUIRED
```

## 1. Escopo

Este QA auditou exclusivamente `docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md`.
Nenhuma correcao foi aplicada a ADR. Nenhum contrato, indice, handoff, codigo,
teste, fixture ou configuracao foi alterado por esta auditoria.

## 2. Autoridades lidas

- `docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md`
- `docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md`
- `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md`
- `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/NOMENCLATURA.md`
- `config/telas/demo/destino_minimo.json`
- `config/telas/demo/grupo_minimo.json`

Relatorios foram tratados como evidencia, nao como autoridade arquitetural.

## 3. Fidelidade a decisao

A ADR registra a decisao material do usuario de forma forte e sem excecoes
indevidas: o corpo e regiao de composicao, nao elemento visual; toda area entre
`cabecalho` e `barra_de_menus` deve pertencer visualmente a `console`,
`dashboard` ou `lancador`; linhas externas vazias, sobra externa e permissao por
ausencia de `distribuicao` ficam proibidas.

Nao foi encontrada formulacao que transforme `grupo` em elemento visual. A ADR
tambem preserva corretamente a diferenca entre espaco externo proibido e espaco
interno permitido dentro da moldura, borda, conteudo ou padding normativo de um
elemento visual.

## 4. Casos concretos

`destino_minimo` foi identificado corretamente:

- tela: `destino_minimo`;
- arquivo: `config/telas/demo/destino_minimo.json`;
- dashboard: `dashboard_teste`;
- titulo: `Teste`;
- comportamento a eliminar: espaco externo entre o dashboard e a
  `barra_de_menus`.

`grupo_minimo` foi identificado corretamente:

- tela: `grupo_minimo`;
- arquivo: `config/telas/demo/grupo_minimo.json`;
- grupo estrutural: `grupo_principal`;
- dashboard interno: `dashboard_conteudo`;
- titulo: `Conteudo`;
- nao existe dashboard `TESTE` nesse caso;
- comportamento a eliminar: espaco externo entre o descendente visual e a
  `barra_de_menus`.

## 5. Relacao com autoridades anteriores

A ADR identifica corretamente as regras conflitantes:

- ADR-0013, clausula 4: preenchimento por linhas em branco externas;
- ADR-0018, D2: permissao de sobra externa quando `distribuicao` esta ausente;
- `contrato_composicao_corpo.md`, secoes 4.7 e 5.7;
- `contrato_tela_json.md`, secoes 8 e 9;
- `NOMENCLATURA.md`, especialmente a semantica da ausencia de distribuicao.

A relacao geral esta clara: regras de ocupacao de altura e distincao
arranjo/distribuicao permanecem validas; somente a permissividade do
preenchimento externo vazio deve ser substituida. A contradicao ativa relevante
foi identificada, mas ainda nao aplicada documentalmente.

## 6. Exequibilidade futura

Os criterios observaveis da ADR sao adequados como alvo de teste: exigem
verificacao semantica linha a linha, multiplas dimensoes, identidade correta das
telas e rejeitam codigo de saida zero como prova suficiente.

Ainda assim, o futuro H-0033 nao fica executavel no estado atual da ADR. Para
implementar sem inventar arquitetura, faltam decisoes sobre expansao de elemento
unico, multiplos elementos sem `distribuicao`, grupos livres com area excedente
e comportamento quando o invariante nao puder ser satisfeito.

## 7. Estado Git e escopo

Comando solicitado, executado no topo Git:

```bash
cd "$(git rev-parse --show-toplevel)"
git status --short
git diff -- scripts/docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md
```

Resultado observado:

```text
?? docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md
```

O `git diff -- scripts/docs/...` nao produziu saida porque o checkout observado
nao possui subdiretorio `scripts/`; o topo Git ja e o diretorio que contem
`docs/` e `config/`. O artefato real da ADR esta em `docs/adr/...` e aparece
como arquivo novo nao rastreado.

Ao final desta auditoria, os artefatos pertencentes a etapa observada sao:

- ADR criada anteriormente: `docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md`;
- relatorio criado neste QA: `docs/relatorios/RELATORIO_QA_ADR-0024.md`.

Estado Git final:

```text
?? docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md
?? docs/relatorios/RELATORIO_QA_ADR-0024.md
```

Nao foi observada outra alteracao no estado Git final.
