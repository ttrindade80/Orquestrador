---
name: RELATORIO_APLICACAO_ADR-0022
description: Relatorio reconstruido de aplicacao documental da ADR-0022 nos documentos normativos ativos
metadata:
  type: relatorio_aplicacao
  etapa: APLICAR_ADR
  status: CONCLUIDO
  data: "2026-07-14"
  regularizacao_processual: "2026-07-15"
---

# RELATORIO DE APLICACAO — ADR-0022

## 1. Identificacao

Etapa reconstruida: `APLICAR_ADR`.

Etapa de regularizacao que criou este relatorio ausente:

```text
PATCH_APLICACAO_ADR
```

ADR aplicada:

```text
docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md
```

Relatorio de QA da ADR:

```text
docs/relatorios/RELATORIO_QA_ADR-0022.md
```

Relatorio de QA da aplicacao que bloqueou por ausencia deste artefato:

```text
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0022.md
```

Status formal do QA da aplicacao antes desta regularizacao:

```text
BLOCKED_DOCUMENTATION
```

## 2. Motivo da regularizacao

O QA da aplicacao da ADR-0022 registrou o achado bloqueante:

```yaml
id: FND-BLOCKED-01
titulo: Ausencia do relatorio de aplicacao documental da ADR-0022
arquivo: docs/relatorios/RELATORIO_APLICACAO_ADR-0022.md
```

Este relatorio corrige exclusivamente a ausencia do artefato obrigatorio. Ele
nao reaplica a ADR-0022, nao altera os documentos ja aplicados, nao corrige
defeitos laterais, nao cria handoff, nao implementa codigo, nao altera JSON e
nao cria commit.

## 3. Objetivo e limites

Objetivo: reconstruir fielmente o relatorio da aplicacao documental ja
materializada no diff acumulado do workspace, usando a ADR-0022, seu QA
aprovado, o diff real, os documentos normativos alterados, o QA bloqueado da
aplicacao e o estado Git.

Limites respeitados:

- nenhum documento aplicado foi modificado nesta regularizacao;
- nenhum documento normativo foi corrigido;
- nenhum codigo, JSON, teste, schema ou diretorio fisico foi criado ou alterado;
- nenhum commit foi criado;
- o stage permaneceu vazio;
- este arquivo foi o unico artefato criado por `PATCH_APLICACAO_ADR`.

## 4. Autoridades

Foram lidos integralmente:

```text
docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md
docs/relatorios/RELATORIO_QA_ADR-0022.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0022.md
docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0021.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0021.md
```

A ADR-0022 e a autoridade decisoria. O QA bloqueado da aplicacao foi usado
como evidencia e guia de reconciliacao, mas nao substituiu a leitura direta do
diff real.

## 5. Estado Git inicial da regularizacao

Comandos executados a partir da raiz:

```yaml
git_toplevel: /home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador
pwd: /home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador
branch: master
head_abreviado: 0143fd1
ultimo_commit: "0143fd1 chore: migra orquestrador para repositorio independente"
stage: vazio
git_diff_check: sem apontamentos
git_diff_cached_name_only: vazio
relatorio_ausente_confirmado: true
```

Arquivos rastreados modificados no inicio:

```text
docs/INDICE.md
docs/NOMENCLATURA.md
docs/adr/ADR-0008-modelo-configuracao-por-tela.md
docs/adr/ADR-0009-caminho-formato-jsons-tela.md
docs/adr/INDICE_ADR.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_cabecalho.md
docs/contratos/contrato_chip.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_console.md
docs/contratos/contrato_estilo.md
docs/contratos/contrato_json_barra_de_menus.md
docs/contratos/contrato_json_cabecalho.md
docs/contratos/contrato_json_console.md
docs/contratos/contrato_json_dashboard.md
docs/contratos/contrato_json_lancador.md
docs/contratos/contrato_json_tela_minima.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_tela_json.md
```

Arquivos nao rastreados presentes no inicio:

```text
docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md
docs/relatorios/LEVANTAMENTO_PREPARACAO_INTEGRACAO_PIPELINE_ORQUESTRADOR.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0021.md
docs/relatorios/RELATORIO_QA_ADR-0021.md
docs/relatorios/RELATORIO_QA_ADR-0022.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0021.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0022.md
```

Itens adicionais inesperados, caso existentes fora da lista acima, devem
permanecer classificados como:

```yaml
origem: NAO_CONFIRMADA
produzido_pelo_executor: NAO_CONFIRMADO
produzido_pelo_usuario: NAO_CONFIRMADO
```

## 6. Contexto da aplicacao ja executada

A aplicacao documental da ADR-0022 ja estava materializada no diff acumulado
antes desta regularizacao. O diff total possuia 19 arquivos rastreados
modificados, dos quais 17 continham alteracoes diretamente associadas a
ADR-0022 por `git diff -S'ADR-0022' --name-only`.

Os 2 arquivos restantes estavam alterados pelo ciclo da ADR-0021, sem alteracao
associada a ADR-0022:

```text
docs/contratos/contrato_json_lancador.md
docs/contratos/contrato_lancador.md
```

## 7. Metodo de reconstrucao

Foram usados:

- leitura integral das autoridades obrigatorias;
- `git diff -S'ADR-0022' --name-only`;
- diff direto de `docs/INDICE.md`, `docs/NOMENCLATURA.md`, `docs/adr/` e
  `docs/contratos/`;
- busca ampla por referencias a ponto de entrada, tela real, demonstracao,
  `posicao_dashboard`, `Estilos`, cabecalho, alias e fallback;
- verificacao fisica de que `orquestrador.py`, `demo/` e
  `config/telas/demo/` nao foram criados;
- verificacao de ausencia de alteracoes em `config/`, `tela/`, JSONs e testes.

## 8. Documentos alterados pela ADR-0022

```yaml
- arquivo: docs/INDICE.md
  secoes_ou_trechos:
    - Estrutura esperada
    - Artefatos / Config
  regra_anterior: Estrutura ainda centrada em arquivos planos de config e sem reserva explicita do ponto de entrada real.
  regra_aplicada: Registra `orquestrador.py` como futuro ponto de entrada real, `config/telas/orquestrador.json` como tela inicial real com `id: "orquestrador"`, `config/telas/demo/` como raiz futura da demonstracao e `tela/` como motor compartilhado.
  autoridade: docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md

- arquivo: docs/NOMENCLATURA.md
  secoes_ou_trechos:
    - atualizado_em
    - Politica da tela inicial real pela ADR-0022
    - Status dos artefatos JSON
    - referencias historicas ao orquestrador.py legado
  regra_anterior: Nomenclatura distinguia configuracao por tela e politica da ADR-0021, mas nao detalhava a tela inicial real.
  regra_aplicada: Define ponto de entrada real, tela inicial real, identidade `orquestrador`, corpo inicial com `console` e `dashboard` vazios, barra minima e ausencia de alias/fallback com `demo`.
  autoridade: docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md

- arquivo: docs/adr/ADR-0008-modelo-configuracao-por-tela.md
  secoes_ou_trechos:
    - Nota de atualizacao — ADR-0022
  regra_anterior: Modelo declarativo por tela sem aplicacao especifica a tela inicial real do produto.
  regra_aplicada: Registra que a tela real sera declarada por JSON proprio, com `id: "orquestrador"`, envelope canonico e reuso do motor `tela/`.
  autoridade: docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md

- arquivo: docs/adr/ADR-0009-caminho-formato-jsons-tela.md
  secoes_ou_trechos:
    - Nota de atualizacao — ADR-0022
  regra_anterior: A reserva de `config/telas/orquestrador.json` havia ficado dependente da separacao da ADR-0021.
  regra_aplicada: Define `orquestrador.py` usando `config/telas/`, reserva `config/telas/orquestrador.json` para a tela real e preserva ausencia de alias/fallback com `demo`.
  autoridade: docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md

- arquivo: docs/adr/INDICE_ADR.md
  secoes_ou_trechos:
    - tabela de decisoes registradas
  regra_anterior: Indice terminava na ADR-0021.
  regra_aplicada: Adiciona ADR-0022 como aceita, datada de 2026-07-14, com resumo do ponto de entrada real, tela inicial real, envelope, corpo vazio e barra minima.
  autoridade: docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md

- arquivo: docs/contratos/contrato_barra_de_menus.md
  secoes_ou_trechos:
    - rastreabilidade
    - Regra fundamental / Barra minima da tela real inicial
    - Acesso a estilos na tela real inicial
  regra_anterior: Sem regra especifica para a barra minima da tela real ou para item de estilos inerte.
  regra_aplicada: Exige `Esc`, `?` e acesso a estilos na instancia `orquestrador`; proibe destino inexistente, acao temporaria e fallback; condiciona item inerte a validacao vigente.
  autoridade: docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md

- arquivo: docs/contratos/contrato_cabecalho.md
  secoes_ou_trechos:
    - rastreabilidade
    - Presenca e estrutura
  regra_anterior: Cabecalho exigia `titulo` e `descricao`, sem tratamento da tela real do Orquestrador.
  regra_aplicada: Registra que `orquestrador` devera declarar cabecalho, mas valores concretos de `titulo` e `descricao` continuam pendentes e nao podem ser inventados.
  autoridade: docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md

- arquivo: docs/contratos/contrato_chip.md
  secoes_ou_trechos:
    - rastreabilidade
    - Tipos conceituais de chip
  regra_anterior: Tipos de chip nao mencionavam o item especifico de estilos da tela real.
  regra_aplicada: Define acesso a estilos como chip especifico da instancia, sem destino, acao temporaria, alias ou fallback enquanto a tela funcional nao existir.
  autoridade: docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md

- arquivo: docs/contratos/contrato_composicao_corpo.md
  secoes_ou_trechos:
    - rastreabilidade
    - Tela inicial real `orquestrador`
    - regra R-11
    - criterios de validacao
  regra_anterior: Regras historicas do draft demonstrativo de dashboard ainda podiam ser lidas como conteudo do Orquestrador.
  regra_aplicada: Define corpo real com `console` e `dashboard` presentes e sem entradas; proibe dados demonstrativos e nao reintroduz `posicao_dashboard` como regra ativa.
  autoridade: docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md

- arquivo: docs/contratos/contrato_console.md
  secoes_ou_trechos:
    - rastreabilidade
    - Natureza do console
  regra_anterior: Console vazio nao estava vinculado a tela real inicial.
  regra_aplicada: Registra que a tela `orquestrador` tera `console` estruturalmente presente e sem entradas, sem default nem fallback do renderer.
  autoridade: docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md

- arquivo: docs/contratos/contrato_estilo.md
  secoes_ou_trechos:
    - rastreabilidade
    - Natureza
  regra_anterior: Estilo global nao distinguia a exposicao inicial de acesso a estilos da tela funcional futura.
  regra_aplicada: Preserva `config/estilo.json` e declara que acesso a estilos nao autoriza tela funcional, troca de borda, troca de envelope de chips ou persistencia.
  autoridade: docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md

- arquivo: docs/contratos/contrato_json_barra_de_menus.md
  secoes_ou_trechos:
    - rastreabilidade
    - V-8. Acesso a estilos na tela real inicial
  regra_anterior: Validacoes de `chips[]` sem excecao documentada para acesso a estilos ainda sem destino funcional.
  regra_aplicada: Exige `Esc`, `?` e acesso a estilos, proibe destino falso e condiciona criacao fisica da tela a aceitacao de item declarativo nao navegavel.
  autoridade: docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md

- arquivo: docs/contratos/contrato_json_cabecalho.md
  secoes_ou_trechos:
    - rastreabilidade
    - V-5. Textos pertencem ao JSON da tela
  regra_anterior: Campos `titulo` e `descricao` eram obrigatorios genericamente, sem pendencia especifica da tela real.
  regra_aplicada: Mantem obrigatoriedade dos campos e registra que valores concretos da tela `orquestrador` exigem decisao documental antes da criacao fisica.
  autoridade: docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md

- arquivo: docs/contratos/contrato_json_console.md
  secoes_ou_trechos:
    - rastreabilidade
    - observacoes sobre envelope minimo
  regra_anterior: Envelope minimo de console nao estava associado ao console vazio da tela real.
  regra_aplicada: Registra `origem_dados: null` e `itens: []` como forma minima compativel com a semantica de console sem entradas, preservadas as demais politicas obrigatorias.
  autoridade: docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md

- arquivo: docs/contratos/contrato_json_dashboard.md
  secoes_ou_trechos:
    - rastreabilidade
    - observacoes sobre envelope minimo
    - fora de escopo
  regra_anterior: Exemplo de dashboard minimo ainda citava `posicao_dashboard` como campo transicional e draft demonstrativo do Orquestrador.
  regra_aplicada: Registra dashboard real estruturalmente presente e sem entradas via `conteudo.tipo: "placeholder"` e `conteudo.binding: null`; nao reativa `posicao_dashboard`.
  autoridade: docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md

- arquivo: docs/contratos/contrato_json_tela_minima.md
  secoes_ou_trechos:
    - Tela inicial real `orquestrador`
    - Caminhos canonicos e regra de coincidencia de `id`
  regra_anterior: Caminhos haviam sido separados pela ADR-0021, mas conteudo minimo da tela real permanecia reservado.
  regra_aplicada: Reserva `config/telas/orquestrador.json` com `id: "orquestrador"`, envelope `cabecalho`, `corpo`, `barra_de_menus`, corpo com `console` e `dashboard` vazios e cabecalho pendente.
  autoridade: docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md

- arquivo: docs/contratos/contrato_tela_json.md
  secoes_ou_trechos:
    - Natureza do tela.json
    - Corpo
    - barra_de_menus
  regra_anterior: Contrato geral nao especificava o ponto de entrada real nem a instancia inicial real.
  regra_aplicada: Documenta `orquestrador.py`, raiz `config/telas/`, tela `orquestrador`, corpo com `console` e `dashboard` vazios, ausencia de `posicao_dashboard` ativo e item de estilos condicionado.
  autoridade: docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md
```

## 9. Documentos inspecionados sem alteracao da ADR-0022

```yaml
- arquivo: docs/contratos/contrato_json_lancador.md
  referencias_encontradas: `config/telas/demo/<tela_destino>.json` e caminho futuro `config/elementos/lancador.json`, ambos associados a ADR-0021.
  motivo_da_nao_alteracao: A ADR-0022 nao decide itens de `lancador`, destinos de navegacao ou `tela_destino`.
  residuo_normativo: ausente para ADR-0022; alteracao pertence somente a ADR-0021.

- arquivo: docs/contratos/contrato_lancador.md
  referencias_encontradas: caminho futuro `config/elementos/lancador.json`.
  motivo_da_nao_alteracao: O lancador demonstrativo e seus itens nao pertencem a composicao minima da tela real da ADR-0022.
  residuo_normativo: ausente para ADR-0022; alteracao pertence somente a ADR-0021.

- arquivo: docs/contratos/contrato_processo_desenvolvimento.md
  referencias_encontradas: nenhuma referencia material a `orquestrador.py`, `config/telas/orquestrador.json`, `Estilos` ou identidade `demo`/`orquestrador`.
  motivo_da_nao_alteracao: Documento procedimental sem regra ativa de caminho, identidade de tela ou composicao visual afetada pela ADR-0022.
  residuo_normativo: ausente.
```

## 10. Propagacao das decisoes

```yaml
ponto_de_entrada_real: CONFORME
motor_compartilhado_tela: CONFORME
tela_real_config_telas_orquestrador_json: CONFORME
identidade_literal_orquestrador: CONFORME
separacao_de_demo: CONFORME
ausencia_alias_fallback_busca_ambigua: CONFORME
envelope_cabecalho_corpo_barra_de_menus: CONFORME
corpo_console_dashboard_presentes: CONFORME
console_sem_entradas: CONFORME
dashboard_sem_entradas: CONFORME
ausencia_de_dados_demonstrativos: CONFORME
posicao_dashboard_nao_ativa: CONFORME
titulo_descricao_obrigatorios_pendentes: CONFORME
barra_minima_esc_ajuda_estilos: CONFORME
estilos_sem_acao_destino_tecla_binding_inventado: CONFORME
bloqueio_futuro_se_item_inerte_incompativel: CONFORME
pipeline_fora_de_escopo: CONFORME
prova_semantica_futura_runtime: CONFORME
handoff_condicionado_a_coesao: CONFORME
destino_minimo_grupo_minimo_fora_do_escopo: CONFORME
```

## 11. Ponto de entrada

A aplicacao documenta `orquestrador.py` como futuro ponto de entrada real do
produto, diretamente na raiz, sem criar o arquivo e sem definir assinatura de
`main`, argumentos de linha de comando, mecanismo de import, classe, protocolo
com Pipeline ou ciclo de vida.

## 12. Tela real

A aplicacao reserva `config/telas/orquestrador.json` para a tela inicial real,
com identidade literal `orquestrador`, usando a raiz `config/telas/`. A tela
demonstrativa permanece separada na futura raiz `config/telas/demo/`, com
identidade `demo`, sem alias, fallback ou busca ambigua.

## 13. Console vazio

O `console` da tela real foi documentado como elemento estrutural presente e
sem entradas iniciais. A representacao compativel indicada pelo contrato de
JSON e `origem_dados: null` com `itens: []`, preservadas as demais politicas
obrigatorias do envelope.

## 14. Dashboard vazio

O `dashboard` da tela real foi documentado como elemento estrutural presente e
sem dados reais ou demonstrativos. A representacao compativel indicada pelo
contrato e `conteudo.tipo: "placeholder"` com `conteudo.binding: null`. A
aplicacao nao reintroduz `regras_exibicao.posicao_dashboard` como eixo ativo.

## 15. Cabecalho pendente

```yaml
titulo_concreto: PENDENTE_DECISAO_USUARIO
descricao_concreta: PENDENTE_DECISAO_USUARIO
```

Os campos `titulo` e `descricao` continuam obrigatorios. Seus valores concretos
nao foram definidos pela ADR-0022, nao foram inventados na aplicacao e deverao
estar decididos por autoridade documental suficiente antes da criacao fisica de
`config/telas/orquestrador.json`. Se a pendencia permanecer no ciclo de
implementacao, a criacao fisica da tela devera bloquear antes de escrever o
JSON.

## 16. Barra minima

A barra da tela real foi documentada com os itens minimos:

```text
Esc
?
Estilos
```

`Esc` e `?` preservam suas semanticas canonicas. Nenhum atalho adicional,
binding, acao ou destino foi inventado pela aplicacao.

## 17. Analise do item `Estilos`

Os contratos exigem campos validos para chips acionaveis. A tela funcional de
estilos ainda nao existe. A aplicacao nao criou acao, destino, tecla, binding
ou fallback para suprir essa ausencia.

A documentacao aplicada mantem o acesso a estilos como declarativo e
condicionado: se os validadores vigentes permitirem item visivel inicialmente
inerte, a tela podera declara-lo dessa forma; se exigirem acao ou destino
existente para todo item visivel, a futura criacao fisica da tela devera parar
com:

```text
BLOCKED_USER_DECISION
```

Classificacao preservada:

```yaml
runtime_aceita_item_inerte: NAO_CONFIRMADO
tecla_de_estilos: NAO_CONFIRMADA
acao_de_estilos: NAO_CONFIRMADA
tela_destino_de_estilos: NAO_CONFIRMADA
```

## 18. Compatibilidade com ADR-0021

A aplicacao da ADR-0022 depende da ADR-0021 e nao a reabre. A politica
reconciliada e:

```text
produto real:
  ponto de entrada: orquestrador.py
  raiz declarativa: config/telas/
  tela inicial: config/telas/orquestrador.json
  identidade inicial: orquestrador

demonstracao:
  ponto de entrada: demo.py
  raiz declarativa: config/telas/demo/
  identidade inicial: demo
```

O motor `tela/` permanece compartilhado. Nao ha alias entre `demo` e
`orquestrador`, nem fallback entre as raizes.

## 19. Relacao com Pipeline

A aplicacao prepara documentalmente o ponto de entrada real para integracao
futura, mas mantem fora de escopo protocolo, canal, processo pai/filho, eventos,
polling, mensagens, schemas, arquivos de troca, tratamento de falhas e qualquer
integracao concreta com o Pipeline.

```yaml
integracao_com_pipeline: NAO_CONFIRMADA
```

## 20. Demonstracao operacional futura

A aplicacao exige que o futuro handoff/implementacao prove semanticamente em
runtime:

- `orquestrador.py` iniciou a tela real;
- a identidade carregada foi `orquestrador`;
- a raiz usada foi `config/telas/`;
- `demo` nao foi carregado;
- `console` e `dashboard` estao presentes e sem entradas;
- a barra contem os itens obrigatorios;
- dados demonstrativos nao foram exibidos;
- o motor compartilhado foi reutilizado.

Codigo de saida zero, isoladamente, continua insuficiente.

## 21. Buscas e residuos

Busca executada:

```bash
rg -n --glob 'docs/**' 'orquestrador\.py|config/telas/orquestrador\.json|config/telas/demo|id.*orquestrador|id.*demo|posicao_dashboard|Estilos|titulo|descricao|fallback|alias'
```

Classificacao das ocorrencias relevantes:

```yaml
normativa_ativa:
  - docs/INDICE.md
  - docs/NOMENCLATURA.md
  - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
  - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
  - docs/adr/INDICE_ADR.md
  - docs/contratos/contrato_barra_de_menus.md
  - docs/contratos/contrato_cabecalho.md
  - docs/contratos/contrato_chip.md
  - docs/contratos/contrato_composicao_corpo.md
  - docs/contratos/contrato_console.md
  - docs/contratos/contrato_estilo.md
  - docs/contratos/contrato_json_barra_de_menus.md
  - docs/contratos/contrato_json_cabecalho.md
  - docs/contratos/contrato_json_console.md
  - docs/contratos/contrato_json_dashboard.md
  - docs/contratos/contrato_json_tela_minima.md
  - docs/contratos/contrato_tela_json.md
exemplo_normativo:
  - docs/contratos/contrato_json_console.md
  - docs/contratos/contrato_json_dashboard.md
historica:
  - docs/handoff/**
  - docs/relatorios/IMP-*
  - docs/relatorios/RELATORIO_QA_H-*
  - docs/relatorios/RELATORIO_AUDITORIA_*
relatorio:
  - docs/relatorios/RELATORIO_QA_ADR-0022.md
  - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0022.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0021.md
  - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0021.md
handoff:
  - docs/handoff/**
sem_impacto:
  - docs/templates/**
  - docs/backlog.md
superada:
  - mencoes historicas a `config/telas/orquestrador.json` como tela demonstrativa ou raiz antiga, preservadas em documentos fechados
```

Residuos historicos preservados:

- handoffs e relatorios antigos citam `config/telas/orquestrador.json` como
  tela existente de ciclos anteriores;
- ADRs anteriores preservam discussoes sobre `posicao_dashboard`, aliases
  transicionais e fallbacks de contexto diverso;
- essas ocorrencias nao foram alteradas por serem historicas ou fora do escopo
  da aplicacao da ADR-0022.

Nao foram identificados aliases, fallbacks ou buscas ambiguas normativas ativas
entre `demo` e `orquestrador` nos documentos alterados pela ADR-0022.

## 22. Fatos `NAO_CONFIRMADOS`

```yaml
mecanismo_concreto_de_import: NAO_CONFIRMADO
assinatura_de_main: NAO_CONFIRMADA
argumentos_de_linha_de_comando: NAO_CONFIRMADOS
runtime_aceita_item_inerte: NAO_CONFIRMADO
tecla_de_estilos: NAO_CONFIRMADA
acao_de_estilos: NAO_CONFIRMADA
tela_destino_de_estilos: NAO_CONFIRMADA
integracao_com_pipeline: NAO_CONFIRMADA
titulo_concreto: PENDENTE_DECISAO_USUARIO
descricao_concreta: PENDENTE_DECISAO_USUARIO
```

## 23. Itens fora de escopo

Permaneceram fora de escopo:

- criacao de `orquestrador.py`;
- criacao de `config/telas/orquestrador.json`;
- criacao de `demo/`;
- criacao de `config/telas/demo/`;
- migracao fisica de telas demonstrativas;
- implementacao de tela funcional de estilos;
- acao, destino, tecla ou binding para `Estilos`;
- troca de borda;
- troca de envelope de chips;
- persistencia de estilo;
- integracao concreta com Pipeline;
- correcao de `destino_minimo`;
- correcao de `grupo_minimo`;
- testes;
- schema novo;
- handoff;
- commit.

## 24. Escopo fisico preservado

Verificacoes realizadas:

```yaml
orquestrador_py_criado: nao
demo_diretorio_criado: nao
config_telas_demo_criado: nao
config_alterado: nao
tela_alterado: nao
json_substantivo_criado_ou_alterado: nao
teste_alterado: nao
schema_novo_criado: nao
commit_criado: nao
stage: vazio
```

## 25. Criterios objetivos da aplicacao

| Criterio | Verificacao |
|---|---|
| 1. ADR-0022 registrada no indice | `docs/adr/INDICE_ADR.md` contem ADR-0022. |
| 2. Ponto de entrada futuro documentado | `orquestrador.py` registrado como futuro ponto de entrada real. |
| 3. Tela real reservada | `config/telas/orquestrador.json` reservado para a tela real. |
| 4. Identidade distinta de `demo` | `orquestrador` e `demo` tratados como identidades distintas. |
| 5. Envelope canonico documentado | `cabecalho`, `corpo` e `barra_de_menus` preservados. |
| 6. Console presente e sem entradas | Contratos de console registram elemento presente e vazio. |
| 7. Dashboard presente e sem entradas | Contratos de dashboard registram placeholder sem binding e sem dados. |
| 8. Dados demonstrativos excluidos | Draft demonstrativo nao contamina tela real. |
| 9. `posicao_dashboard` nao reintroduzido | Campo permanece transicional/descontinuado, nao eixo ativo da tela real. |
| 10. Cabecalho pendente explicitado | `titulo` e `descricao` obrigatorios, valores pendentes. |
| 11. Barra minima documentada | `Esc`, `?` e acesso a estilos declarados como minimo da instancia real. |
| 12. Item `Estilos` sem acao inventada | Sem destino, acao temporaria, alias ou fallback. |
| 13. Incompatibilidade de item inerte vira bloqueio futuro | `BLOCKED_USER_DECISION` registrado para validadores incompatíveis. |
| 14. Motor compartilhado preservado | `tela/` permanece motor reutilizado. |
| 15. Pipeline fora de escopo | Nenhum protocolo ou integracao concreta foi definido. |
| 16. Prova semantica futura exigida | Runtime futuro deve provar identidade, raiz, corpo e ausencia de dados demo. |
| 17. Implementacao fisica nao antecipada | Nenhum codigo, JSON ou diretorio foi criado. |
| 18. Pendencias de preenchimento preservadas | `titulo`, `descricao`, `destino_minimo` e `grupo_minimo` seguem pendentes conforme escopo. |

## 26. Lista real de arquivos

Arquivos associados a ADR-0022 por `git diff -S'ADR-0022' --name-only`:

```text
docs/INDICE.md
docs/NOMENCLATURA.md
docs/adr/ADR-0008-modelo-configuracao-por-tela.md
docs/adr/ADR-0009-caminho-formato-jsons-tela.md
docs/adr/INDICE_ADR.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_cabecalho.md
docs/contratos/contrato_chip.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_console.md
docs/contratos/contrato_estilo.md
docs/contratos/contrato_json_barra_de_menus.md
docs/contratos/contrato_json_cabecalho.md
docs/contratos/contrato_json_console.md
docs/contratos/contrato_json_dashboard.md
docs/contratos/contrato_json_tela_minima.md
docs/contratos/contrato_tela_json.md
```

Arquivos inspecionados sem alteracao associada a ADR-0022:

```text
docs/contratos/contrato_json_lancador.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_processo_desenvolvimento.md
```

Arquivo criado nesta regularizacao:

```text
docs/relatorios/RELATORIO_APLICACAO_ADR-0022.md
```

## 27. Estado Git final esperado

```yaml
branch: master
head_abreviado: 0143fd1
stage: vazio
commit_criado: nao
arquivo_criado_na_regularizacao:
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0022.md
documentos_aplicados_alterados_na_regularizacao: []
codigo_json_testes_schemas_alterados: []
```

## 28. Bloqueios

Bloqueio processual corrigido por este arquivo:

```yaml
id: FND-BLOCKED-01
status_apos_regularizacao: corrigido
arquivo: docs/relatorios/RELATORIO_APLICACAO_ADR-0022.md
```

Bloqueios futuros preservados:

```yaml
item_estilos_inerte_incompativel_com_validadores: BLOCKED_USER_DECISION
titulo_ou_descricao_concretos_ausentes_na_implementacao: BLOCKED_USER_DECISION
console_vazio_incompatibilizado_por_schema_posterior: BLOCKED_USER_DECISION
dashboard_vazio_incompatibilizado_por_schema_posterior: BLOCKED_USER_DECISION
lacuna_que_exija_inventar_comportamento: BLOCKED_USER_DECISION
```

## 29. Conclusao

A aplicacao documental da ADR-0022 foi reconstruida neste relatorio a partir do
diff real e das autoridades obrigatorias. As decisoes da ADR-0022 foram
propagadas aos 17 documentos normativos identificados, sem implementacao fisica
e sem alteracao adicional nesta regularizacao.

O bloqueio documental por ausencia do relatorio de aplicacao fica sanado pela
criacao deste arquivo. A proxima categoria processual aplicavel, se nenhuma
nova divergencia for encontrada, e:

```text
proxima_categoria: QA_APLICACAO_ADR
```
