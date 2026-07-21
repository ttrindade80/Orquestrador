---
name: adr-0029-nomenclatura-modular-e-leitura-seletiva
description: Formaliza a substituição da nomenclatura monolítica por uma base terminológica modular com leitura seletiva por atividade e domínio, preservando fachada permanente e autoridade dos contratos sobre comportamento
metadata:
  type: adr
  scope: documentacao
  status: aceita e aplicada
  data: "2026-07-20"
  substitui: null
rastreabilidade:
  rfc_origem: null
  issues_relacionadas: []

  documentos_afetados:
    - docs/NOMENCLATURA.md
    - docs/INDICE.md
    - docs/adr/INDICE_ADR.md

  contratos_afetados:
    - docs/contratos/contrato_estilo.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_cabecalho.md
    - docs/contratos/contrato_lancador.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_chip.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_json_console.md

  handoffs_bloqueados: []
---

# ADR-0029 — Nomenclatura modular e leitura seletiva

## 1. Identificação

| Campo | Valor |
|---|---|
| Número | ADR-0029 |
| Título | Nomenclatura modular e leitura seletiva |
| Status | aceita e aplicada |
| Data | 2026-07-20 |
| Origem | Decisão explícita do usuário |
| Relatório de levantamento | `docs/relatorios/RELATORIO_LEVANTAMENTO_REORGANIZACAO_NOMENCLATURA.md` |

---

## 2. Status

`aceita e aplicada`

A FASE_1_MATERIALIZACAO_PRE_FACHADA foi executada em 2026-07-20: os 17 módulos foram
criados sob `docs/nomenclatura/`; o relatório de aplicação e o relatório histórico
foram produzidos. A ADR está aceita com as observações não corretivas
OBS-QA-POS-ADR0029-001 e OBS-QA-POS-ADR0029-002 do QA pós-patch
(`docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0029.md`, status: ADR_APPROVED_WITH_NOTES).
A FASE_2_CONVERSAO_FACHADA foi executada em 2026-07-21: `docs/NOMENCLATURA.md` foi
convertido em fachada permanente conforme D-NOM-12; os 17 módulos passaram de
PRE_FACHADA para VIGENTE como autoridade terminológica; `docs/INDICE.md` adotou leitura
seletiva em vez de leitura integral obrigatória; 9 contratos declararam dependências
obrigatórias e condicionais e tiveram referências por seção migradas para os módulos
proprietários; arquivos de configuração e código fonte foram atualizados. O relatório
de aplicação da FASE_2 está em `docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-2.md`.

---

## 3. Contexto

### 3.1 Estado atual de `docs/NOMENCLATURA.md`

O levantamento documental (`docs/relatorios/RELATORIO_LEVANTAMENTO_REORGANIZACAO_NOMENCLATURA.md`, 2026-07-20) comproviu os seguintes fatos sobre o documento atual:

- `docs/NOMENCLATURA.md` possui 1856 linhas (`status: parcial`).
- O documento mistura responsabilidades distintas em um único arquivo:
  - terminologia, schemas e distinções conceituais;
  - regras comportamentais completas e algoritmos;
  - decisões de ADRs referenciadas ao longo do texto;
  - aliases e termos descontinuados;
  - pendências em aberto (seções 11, 17.5, 18.6, 19.6, 19.7.5);
  - levantamento histórico do Codex sobre código legado (linhas 1103–1120);
  - status transitório de artefatos JSON (linhas 89–101);
  - lista parcial de ADRs aceitas (seção 12);
  - caminhos futuros e reservados.
- `docs/INDICE.md` exige sua leitura como terceiro item da ordem documental obrigatória.
- Contratos ativos citam o documento por seção numerada (`#1`, `#3`, `#5`, `#7`, `#13`, `§16.2`, `§17.2`).
- Código-fonte (`tela/renderizador.py`) cita seções por número nos comentários.
- Handoffs H-0035, H-0036 e H-0037 referenciam seções específicas.

### 3.2 Problema observado

```yaml
problema_observado:
  - docs/NOMENCLATURA.md tornou-se um documento monolítico
  - o levantamento comprovou 1856 linhas
  - o documento mistura terminologia, schemas, regras comportamentais, algoritmos,
    aliases, pendências, histórico, decisões deferidas e estados transitórios
  - atividades focais são obrigadas a carregar conteúdo de domínios não relacionados
  - consumidores citam tanto o documento inteiro quanto seções e âncoras específicas
```

### 3.3 Comportamento desejado

```yaml
comportamento_desejado:
  - organizar a nomenclatura em módulos canônicos por responsabilidade e domínio
  - permitir que cada atividade leia somente o núcleo e os módulos necessários
  - preservar uma única fonte proprietária para cada definição terminológica
  - manter os contratos como autoridade do comportamento normativo completo
  - classificar e retirar do glossário conteúdo histórico, pendente ou transitório
```

### 3.4 Gatilho e direção de leitura

```yaml
estado_inicial:
  - docs/NOMENCLATURA.md contém as definições e responsabilidades acumuladas
  - docs/INDICE.md exige sua leitura como documento central
  - contratos, handoffs e código contêm referências ao caminho e a seções numeradas

gatilho_primario:
  - identificação do contrato, artefato ou domínio diretamente envolvido na atividade

direcao:
  - partir do índice e do núcleo comum para os módulos proprietários estritamente necessários
  - nunca partir da leitura preventiva de todos os módulos

ordem:
  - ler a documentação inicial do processo
  - consultar o índice da nomenclatura
  - ler o núcleo comum
  - identificar o artefato ou contrato alvo
  - ler os módulos obrigatórios e condicionais declarados pelo contrato alvo
  - consultar módulo adicional somente quando um termo necessário ainda não estiver carregado

fallback:
  - quando um termo necessário não estiver nos módulos carregados, consultar docs/nomenclatura/00_INDICE.md
  - localizar o módulo proprietário
  - ler somente esse módulo
  - não carregar todo o diretório preventivamente
```

### 3.5 Divergência de status da ADR-0018

O levantamento identificou que `docs/adr/INDICE_ADR.md` registra ADR-0018 como `aceita`, mas o arquivo `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md` contém `status: proposta` no frontmatter. Essa divergência é um assunto documental separado, não bloqueante desta ADR, e deve ser tratada em etapa própria.

---

## 4. Decisão

### 4.1 Decisões aprovadas

#### D-NOM-01 — Modularização

```yaml
decisao: substituir a nomenclatura monolítica por uma base modular
origem: DECISAO_EXPLICITA_USUARIO
```

#### D-NOM-02 — Leitura seletiva

```yaml
decisao: cada atividade deve carregar somente os módulos terminológicos necessários
origem: DECISAO_EXPLICITA_USUARIO
```

#### D-NOM-03 — Proibição de leitura preventiva

```yaml
decisao: é proibida a leitura preventiva de todos os módulos de nomenclatura
origem: DECISAO_EXPLICITA_USUARIO
```

#### D-NOM-04 — Princípio de organização

```yaml
decisao: a organização deve usar índice pequeno, núcleo transversal, módulos por domínio
         e separação do histórico
origem: DECISAO_EXPLICITA_USUARIO
```

#### D-NOM-05 — Histórico

```yaml
decisao: todo conteúdo histórico deve ser identificado e organizado como histórico,
         sem permanecer misturado às definições vigentes
origem: DECISAO_EXPLICITA_USUARIO
```

#### D-NOM-06 — Autoridade comportamental

```yaml
decisao: contratos permanecem como autoridade do comportamento completo, validade,
         processamento, erros e critérios de aceite
origem: DECISAO_EXPLICITA_USUARIO
```

#### D-NOM-07 — Propriedade única

```yaml
decisao: cada definição terminológica possui exatamente um módulo proprietário
origem: DECISAO_EXPLICITA_USUARIO
```

Outros módulos e contratos podem referenciar o termo, mas não podem redefini-lo. Especializações comportamentais permanecem no contrato proprietário.

#### D-NOM-08 — Estrutura modular-base

Criar futuramente, sob `docs/nomenclatura/`:

```text
00_INDICE.md
01_NUCLEO_COMUM.md
02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md

10_ESTILO.md
20_TELA_CORPO_E_COMPOSICAO.md
21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md

30_CABECALHO.md
31_BARRA_DE_MENUS_E_CHIPS.md
32_CONSOLE.md
33_LANCADOR.md
34_DASHBOARD.md

40_GRUPOS_E_DISTRIBUICAO_DE_AREA.md
41_DISTRIBUICAO_MATRICIAL.md
42_DADOS_EXTERNOS_MULTINIVEL.md
43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md
44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md

90_ALIASES_E_TERMOS_DESCONTINUADOS.md
```

Origem: `DECISAO_EXPLICITA_USUARIO`

#### D-NOM-09 — Separação das capacidades multinível

```yaml
42_DADOS_EXTERNOS_MULTINIVEL:
  responsabilidade:
    - JSON estrutural versus JSON externo
    - envelope declarativo
    - níveis e estrutura semântica
    - representação semântica versus representação física
    - produtor e consumidor como conceitos

43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO:
  responsabilidade:
    - ponto de entrada
    - associação externa por cenário
    - loader
    - fixture
    - carregamento separado
    - entrega separada ao fluxo

44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE:
  responsabilidade:
    - tabela
    - hierarquia
    - conjuntos de campos
    - modo verboso
    - modo não verboso
    - alternância
    - política de modo
    - modo inicial
```

Origem: `DECISAO_EXPLICITA_USUARIO`

#### D-NOM-10 — Dependências pertencem aos contratos

Cada contrato ativo deve futuramente declarar nominalmente:

```yaml
dependencias_obrigatorias:
dependencias_condicionais:
```

O contrato é o proprietário dessa declaração. A lista de dependências não deve ser mantida em segundo lugar no índice terminológico — ela deriva dos próprios contratos e pode ser refletida como visão de navegação.

Origem: `DECISAO_EXPLICITA_USUARIO`

#### D-NOM-11 — Papel do índice terminológico

`docs/nomenclatura/00_INDICE.md` deve:

- localizar o proprietário de cada domínio e termo;
- explicar a leitura seletiva;
- servir como navegação;
- apontar para os contratos e módulos relacionados.

`docs/nomenclatura/00_INDICE.md` não deve:

- redefinir termos;
- manter uma segunda lista normativa independente de dependências;
- obrigar leitura preventiva de todos os módulos.

Quando apresentar roteamento por contrato, deve ser uma visão de navegação derivada das declarações dos próprios contratos.

Origem: `DECISAO_EXPLICITA_USUARIO`

#### D-NOM-12 — Fachada permanente

`docs/NOMENCLATURA.md` deve ser mantido permanentemente como fachada de compatibilidade.

A fachada deve:

- apontar para `docs/nomenclatura/00_INDICE.md`;
- apontar para `docs/nomenclatura/01_NUCLEO_COMUM.md`;
- explicar a leitura seletiva;
- proibir novas definições diretamente em seu conteúdo.

A fachada não preserva automaticamente âncoras e referências antigas por número de seção. Toda referência antiga deve ser migrada nominalmente antes da substituição do conteúdo monolítico.

Origem: `DECISAO_EXPLICITA_USUARIO`

#### D-NOM-13 — Núcleo comum restrito

`01_NUCLEO_COMUM.md` deve conter somente terminologia transversal necessária para interpretar os demais módulos:

- autoridade terminológica;
- termo canônico;
- alias;
- termo descontinuado;
- schema;
- configuração concreta;
- estado de runtime;
- elemento funcional;
- container estrutural;
- conteúdo;
- produtor;
- consumidor;
- loader;
- modelo;
- renderizador;
- regra de consulta ao módulo proprietário.

A explicação detalhada de ADR, handoff, QA, relatório e fluxo de desenvolvimento permanece na documentação do processo e não deve ampliar o núcleo terminológico.

Origem: `DECISAO_EXPLICITA_USUARIO`

#### D-NOM-14 — Fronteira entre composição e grupos

```yaml
20_TELA_CORPO_E_COMPOSICAO:
  - tela e regiões
  - corpo
  - tipos funcionais
  - containers
  - filhos diretos
  - arranjo vertical e horizontal
  - cardinalidade
  - relação com tiling
  - composição genérica

40_GRUPOS_E_DISTRIBUICAO_DE_AREA:
  - grupo como nó estrutural
  - profundidade
  - distribuição entre filhos
  - modos de distribuição
  - ausência de distribuição
  - ocupação integral
  - espaço externo proibido
  - grupo livre
  - matriz de grupos
```

Nenhum dos dois módulos pode redefinir o conteúdo proprietário do outro.

Origem: `DECISAO_EXPLICITA_USUARIO`

#### D-NOM-15 — Migração inicialmente estrutural

A futura primeira migração deve ser predominantemente estrutural.

É proibido aproveitar a divisão para:

- renomear termos ativos;
- alterar schemas;
- reconciliar decisões deferidas;
- modificar comportamento;
- introduzir defaults;
- remover compatibilidade;
- reescrever regras por preferência editorial.

Quando uma regra completa estiver no glossário e também no contrato:

- preservar a definição e as distinções no módulo terminológico;
- manter o comportamento normativo completo no contrato;
- verificar que nenhuma obrigação desapareceu.

Origem: `DECISAO_EXPLICITA_USUARIO`

#### D-NOM-16 — Auditoria antes da fachada

O conteúdo monolítico somente pode ser substituído pela fachada depois de uma auditoria documental confirmar:

- todos os termos ativos possuem proprietário;
- nenhuma definição ativa foi perdida;
- nenhuma definição ativa ficou duplicada;
- regras comportamentais completas permanecem nos contratos;
- dependências dos contratos foram declaradas;
- referências antigas foram migradas;
- pendências e histórico foram classificados;
- aliases permanecem localizáveis;
- a ordem de leitura foi atualizada;
- a leitura preventiva deixou de ser exigida.

Origem: `DECISAO_EXPLICITA_USUARIO`

---

## 5. Escopo e limites

### 5.1 Variantes e coexistências

```yaml
variantes_e_coexistencias:
  - docs/NOMENCLATURA.md permanece como fachada permanente
  - a fachada coexiste com docs/nomenclatura/
  - a fachada não contém definições normativas novas
  - contratos continuam como autoridade comportamental
  - módulos de nomenclatura são autoridade das definições terminológicas
  - referências antigas por seção podem coexistir apenas durante a migração
  - a substituição do conteúdo monolítico pela fachada depende de auditoria de
    preservação normativa e migração das referências
```

### 5.2 Decisões indispensáveis

```yaml
DECISAO_INDISPENSAVEL:
  - nenhuma
```

### 5.3 Deferimentos não bloqueantes

```yaml
DEFERIMENTO_NAO_BLOQUEANTE:
  - mapeamento termo a termo da migração
  - conteúdo textual final de cada módulo
  - lista exata de dependências de cada contrato
  - classificação individual de cada pendência como issue ou backlog
  - localização individual de cada levantamento histórico
  - reconciliação semântica de termos concorrentes já deferidos em ADRs anteriores
  - estratégia de migração de telas legadas relacionada à ADR-0028
  - correção da divergência documental de status encontrada na ADR-0018
```

### 5.4 Fora do escopo desta ADR

```yaml
FORA_DO_ESCOPO:
  - modificar definições terminológicas vigentes
  - alterar schemas ou valores aceitos
  - alterar comportamento de interface
  - alterar código ou configuração
  - reconciliar modo normal e modo não verboso
  - implementar a integração com o Pipeline
  - executar a migração documental
  - criar handoff
  - realizar stage ou commit
```

---

## 6. Responsabilidade documental

| Conteúdo | Proprietário documental |
|---|---|
| Termo, significado, tipo e distinção | módulo de nomenclatura |
| Regra comportamental completa | contrato |
| Decisão, motivação e alternativas | ADR |
| Evidência de aplicação ou implementação | relatório correspondente |
| Bug, impedimento ou decisão pendente | `docs/issues.md` |
| Trabalho futuro reconhecido e ainda não iniciado | `docs/backlog.md` |
| Levantamento do sistema anterior | relatório ou anexo histórico apropriado |
| Lista e estado das ADRs | `docs/adr/INDICE_ADR.md` |
| Alias e termo descontinuado ainda relevante | `90_ALIASES_E_TERMOS_DESCONTINUADOS.md` |
| Estado transitório de migração | relatório de aplicação ou documento de estado apropriado |

A classificação individual de cada item existente no monólito pertence à futura aplicação, não a esta ADR.

---

## 7. Compatibilidade e referências

Esta ADR registra os seguintes princípios de compatibilidade que devem orientar a migração futura:

- Manter o caminho `docs/NOMENCLATURA.md` não preserva sozinho as referências por seção; contratos, handoffs, relatórios e comentários de código que citam seções antigas precisam de migração nominal.
- Referências históricas em documentos fechados não devem ser reescritas sem autoridade.
- Documentos normativos ativos devem apontar para o novo módulo proprietário.
- Aliases permanecem localizáveis no módulo `90_ALIASES_E_TERMOS_DESCONTINUADOS.md`.
- A migração deve diferenciar referência ativa, histórica e explicativa.
- A fachada não deve simular âncoras antigas com definições duplicadas.

Consumidores com referências por seção identificados pelo levantamento:

| Consumidor | Tipo | Seções referenciadas |
|---|---|---|
| `docs/contratos/contrato_estilo.md` | contrato | `#1` |
| `docs/contratos/contrato_composicao_corpo.md` | contrato | `#3`, `#6`, `#8`, `#9`, `#10` |
| `docs/contratos/contrato_barra_de_menus.md` | contrato | `#5` |
| `docs/contratos/contrato_cabecalho.md` | contrato | `#7` |
| `docs/contratos/contrato_lancador.md` | contrato | `#13`, `#6`, `#8` |
| `docs/contratos/contrato_console.md` | contrato | `#4`, `#17`–`#19` |
| `docs/handoff/H-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md` | handoff | `§16.2` |
| `docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md` | handoff | `§17.2` |
| `tela/renderizador.py` | código | `6.3`, `8.1`–`8.3` |

---

## 8. Invariantes da futura aplicação

As seguintes invariantes são normativas e devem ser respeitadas durante toda a migração futura:

1. Uma definição ativa possui um único proprietário.
2. O índice não redefine.
3. A fachada não redefine.
4. O contrato não cria sinônimo sem atualização do módulo proprietário.
5. O módulo terminológico não substitui o contrato comportamental.
6. Conteúdo histórico não se apresenta como vigente.
7. Pendência não se apresenta como regra.
8. Item futuro não se apresenta como critério atual.
9. Leitura seletiva deve ser nominal e declarada.
10. Módulo adicional só é carregado quando necessário.
11. Todos os consumidores ativos devem ser atualizados.
12. Migração estrutural não altera semântica.
13. Divergência normativa encontrada durante a aplicação bloqueia o movimento do bloco afetado.
14. Nenhuma regra pode desaparecer por parecer duplicada.
15. Referências históricas preservadas devem continuar identificadas como históricas.
16. A fachada somente substitui o monólito após auditoria documental aprovada.

---

## 9. Relação com ADRs anteriores

Esta ADR altera a organização documental e a política de leitura. Ela não altera o comportamento funcional definido pelas ADRs anteriores nem reabre decisões semânticas já aprovadas.

As ADRs a seguir continuam sendo autoridade das decisões que formalizaram. Qualquer divergência de status ou conteúdo encontrada em ADR anterior é assunto documental separado.

| ADR | Conteúdo consolidado na nomenclatura | Relação com esta ADR |
|---|---|---|
| ADR-0008 | Modelo de configuração por tela; política schema × dados; responsabilidade de `NOMENCLATURA.md`, `estilo.json` e `tela.json` | O módulo `02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` herdará essa terminologia; a política schema × dados permanece vigente |
| ADR-0011 | Terminologia `vertical`/`horizontal`; aliases transicionais `sobreposto`/`lado_a_lado` | Os aliases migrarão para `90_ALIASES_E_TERMOS_DESCONTINUADOS.md`; a terminologia canônica permanece nos módulos de composição |
| ADR-0014 | Distribuição horizontal responsiva da `barra_de_menus`; regra de alteração por termo específico completo | A terminologia migra para `31_BARRA_DE_MENUS_E_CHIPS.md`; a autoridade da regra permanece no contrato e na ADR |
| ADR-0015 | Composição hierárquica e distribuição de área do corpo | Conteúdo distribuído entre `20_TELA_CORPO_E_COMPOSICAO.md` e `40_GRUPOS_E_DISTRIBUICAO_DE_AREA.md` conforme D-NOM-14 |
| ADR-0017 | Redimensionamento reativo; SIGWINCH; cadeia de dimensões válidas; quadro mínimo | A terminologia migra para `21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`; o comportamento normativo permanece no contrato |
| ADR-0018 | Semântica da ausência de distribuição; distinção arranjo × distribuição | Terminologia migra para `40_GRUPOS_E_DISTRIBUICAO_DE_AREA.md`; divergência de status desta ADR é deferimento não bloqueante |
| ADR-0019 | Profundidade por aninhamento de grupos; multiplicidade estrutural | Terminologia migra para `40_GRUPOS_E_DISTRIBUICAO_DE_AREA.md` |
| ADR-0020 | Especialização bidimensional do nó `grupo`; `livre` e `matriz`; coordenadas explícitas | Terminologia migra para `40_GRUPOS_E_DISTRIBUICAO_DE_AREA.md` |
| ADR-0021 | Separação demo × produto real; política de caminhos | Terminologia migra para `02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` |
| ADR-0022 | Ponto de entrada real; tela inicial real; identidade `orquestrador` | Terminologia migra para `02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` |
| ADR-0023 | Largura mínima funcional do `lancador`; `area_lancador_w`; `lancador_caixa_min_w` | Terminologia migra para `33_LANCADOR.md` |
| ADR-0024 | Proibição de preenchimento vazio externo do corpo; DA-01 a DA-04 | Terminologia migra para `20_TELA_CORPO_E_COMPOSICAO.md` e `40_GRUPOS_E_DISTRIBUICAO_DE_AREA.md` |
| ADR-0025 | `distribuicao_matricial`; formação responsiva e fixa; dimensionamento e espaçamento | Terminologia migra para `41_DISTRIBUICAO_MATRICIAL.md` |
| ADR-0026 | JSON externo de conteúdo; envelope declarativo `{tipo, formato, dados}`; produtor | Terminologia migra para `42_DADOS_EXTERNOS_MULTINIVEL.md` conforme D-NOM-09 |
| ADR-0027 | Ponto de entrada; carregamento separado; associação externa por cenário; schema semântico multinível | Terminologia migra para `43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md` conforme D-NOM-09 |
| ADR-0028 | Apresentações `tabela`, `hierarquia`, `conjuntos_campos`; modo verboso e não verboso; `politica_modo`; `modo_inicial`; D23 | Terminologia migra para `44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` conforme D-NOM-09; reconciliação semântica `modo normal` × `modo não verboso` permanece deferida |

---

## 10. Consequências

```yaml
consequencias:
  positivas:
    - redução do contexto carregado em atividades focais
    - localização explícita do proprietário de cada termo
    - separação entre vocabulário, comportamento, decisão e histórico
    - impedimento formal de novas definições diretamente na fachada
    - facilitação de leitura seletiva declarada por contrato

  custos:
    - necessidade de atualizar contratos e consumidores
    - necessidade de auditar referências por seção em contratos, handoffs e código
    - necessidade de manter módulos e dependências sincronizados entre si e com os contratos
    - custo inicial de inventário, migração e QA documental
    - coexistência temporária do monólito com a estrutura modular durante a transição
```

---

## 11. Critérios para futura aplicação

A aplicação desta ADR somente poderá ser considerada concluída quando:

1. todos os módulos aprovados em D-NOM-08 existirem sob `docs/nomenclatura/`;
2. `docs/nomenclatura/00_INDICE.md` localizar todos os domínios e apontar para os módulos proprietários;
3. `docs/nomenclatura/01_NUCLEO_COMUM.md` permanecer transversal e restrito ao conteúdo definido em D-NOM-13;
4. cada termo ativo possuir exatamente um módulo proprietário;
5. os contratos ativos declararem suas dependências obrigatórias e condicionais;
6. `docs/INDICE.md` usar leitura seletiva em vez de leitura integral obrigatória de `docs/NOMENCLATURA.md`;
7. pendências e histórico presentes no monólito estiverem classificados e movidos para seus documentos proprietários;
8. aliases e termos descontinuados estiverem localizáveis em `90_ALIASES_E_TERMOS_DESCONTINUADOS.md`;
9. referências normativas ativas que citam seções antigas estiverem migradas para os novos módulos;
10. as regras comportamentais completas continuarem nos contratos, nenhuma obrigação normativa desaparecer durante a migração e nenhuma definição terminológica ativa permanecer duplicada entre módulos proprietários ou na fachada;
11. nenhuma regra tiver desaparecido por parecer duplicada com outra já existente no contrato;
12. houver relatório de aplicação documentando cada movimento de bloco;
13. houver QA documental da aplicação confirmando as invariantes da seção 8;
14. somente após todos os critérios acima confirmados `docs/NOMENCLATURA.md` for convertido em fachada permanente conforme D-NOM-12.

Esses critérios são para a futura aplicação. Esta ADR não autoriza executá-la.

---

## 12. Alternativas consideradas

| Alternativa | Motivo para não adotar |
|---|---|
| Manter o monólito como única fonte | Impossibilita leitura seletiva; força carregamento de domínios não relacionados em atividades focais |
| Dividir por tipo de conteúdo (schema, regra, histórico) sem separação por domínio | Não atende à decisão aprovada de organizar a nomenclatura em módulos por domínio. |
| Mover todo conteúdo para os contratos e eliminar o glossário | Contratos são autoridade comportamental, não terminológica; elimina o ponto de resolução de termos transversais |
| Criar módulos e manter cópia normativa também na fachada | Viola a propriedade única (D-NOM-07) e cria risco de divergência entre fachada e módulo |

---

## 13. Encerramento

```yaml
decisao_documental: NOMENCLATURA_MODULAR_E_LEITURA_SELETIVA
estrutura_modular_definida: true
fachada_permanente_definida: true
dependencias_por_contrato_definidas: true
migracao_executada: true
modulos_criados: 17
implementacao_funcional_afetada: false
decisoes_semanticas_reabertas: false
status_literal: ADR_ACCEPTED_AND_APPLIED
proxima_categoria: QA_FASE_2
FASE_1_MATERIALIZACAO_PRE_FACHADA:
  data: "2026-07-20"
  executada: true
  modulos_materializados: 17
  contratos_alterados: false
  indice_geral_alterado: false
  nomenclatura_monolitica_alterada: false
  relatorio: docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-1.md
FASE_2_CONVERSAO_FACHADA:
  data: "2026-07-21"
  executada: true
  fachada_permanente_criada: true
  modulos_promovidos_a_vigente: 17
  contratos_com_dependencias_declaradas: 9
  contrato_adicional_referencia_migrada: docs/contratos/contrato_json_dashboard.md
  referencias_ativas_migradas: true
  indice_geral_alterado: true
  nomenclatura_monolitica_convertida_em_fachada: true
  relatorio: docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-2.md
```
