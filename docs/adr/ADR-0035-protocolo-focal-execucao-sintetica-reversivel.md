---
name: ADR-0035-protocolo-focal-execucao-sintetica-reversivel
description: "Especializa o Handoff 2 da ADR-0034: executor sintético de fixtures, cópia de trabalho reversível, documento de resultado de execução em JSON multinível, classificação global e individual, validação da entrada, ciclo de vida de temporários, controles sintéticos e interrupção protegida"
metadata:
  type: adr
  status: aceita e aplicada
  id: ADR-0035
  data: 2026-07-29
  substitui: null
rastreabilidade:
  decisao_usuario: "H2-ESP-01 a H2-ESP-18 — especialização do Handoff 2 do ITEM-0006 (ADR-0034 D-SEL-12 a D-SEL-15, D-SEL-19, D-SEL-21): execução por fixture e executor sintético sem binding real; fronteira simulada restrita a comando→execução→resultado, recebendo diretamente o lote reconciliado da baseline do H-0041; proteção da fixture baseline mediante cópia de trabalho temporária; efeito sintético por item (processado/ignorado/nao_encontrado/falhou) sobre o fato processado:true|false; fixture mista inicial de quatro itens; produção direta do documento de resultado de execução em JSON multinível pelo executor sintético, sem schema operacional intermediário; estrutura multinível conjuntos_campos com seções Resumo e Itens compatível com a referência 80x24; schema único compartilhado por dry-run e execução real, distinguido pelo campo aplicado; classificação de status_global (sucesso/parcial/falha) e código de saída 0 mesmo em resultado parcial; campos individuais obrigatórios e diagnostico condicional; validação estrutural antecipada da entrada com rejeição integral e proibição de normalização silenciosa; diretório temporário exclusivo por invocação com nomes internos fixos e remoção protegida por finally; canais textuais separados sem interpretação de stdout como resultado; localização da fixture de trabalho como arquivo irmão do resultado sem novo campo, flag ou variável; controles sintéticos reservados a teste (__falha_operacional__, __resultado_invalido__, __interrupcao__); protocolo de interrupção com restauração protegida e código 130"
  rfc_origem: null
  issues_relacionadas:
    - ITEM-0006
  contratos_afetados:
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_json_console.md
  handoffs_bloqueados: []
  aplicacao_documental:
    data: 2026-07-29
    relatorio: docs/relatorios/RELATORIO_APLICACAO_ADR-0035.md
    relacoes_materiais:
      - docs/adr/INDICE_ADR.md
      - docs/contratos/contrato_console.md
      - docs/contratos/contrato_json_console.md
      - docs/backlog.md
    delta_terminologico: vazio
    especializa_sem_substituir: docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md
---

# ADR-0035 — Protocolo focal de execução sintética reversível (especialização do Handoff 2 da ADR-0034)

## 1. Status

`aceita e aplicada`

## 2. Contexto

A ADR-0034 fechou, para o `ITEM-0006`, o modelo de seleção múltipla e o fluxo
focal de processamento, organizado em quatro handoffs sequenciais (D-SEL-21).
O Handoff 1 — estado, comandos e apresentação da seleção, sem operação
externa — foi entregue por `H-0041`, com o protocolo de `Espaço`/`Enter`/`Esc`,
reconciliação, ordenação lógica e indicadores `ec`/`tg` sobre a fixture
fechada de oito itens (D-SEL-22). O chip `Executar` permanece inativo na
interface até o Handoff 3.

O Handoff 2 — protocolo focal do binding e execução — permanece aberto.
A ADR-0034 já fechou, em nível geral, o envelope provisório desse protocolo:
arquivo de entrada `selecao_execucao.v1`, invocação por CLI
(`--entrada`/`--resultado`/`--dry-run`), canais textuais separados,
classificação de sucesso por código `0` e JSON válido, e envelope de erro
multinível de campos fixos (D-SEL-12 a D-SEL-15; `contrato_json_console.md`
§14). Esse envelope geral não fecha, porém, o que é indispensável para
implementar e testar o Handoff 2 de forma focal: a natureza sintética da
execução; a fronteira exata do que é simulado; o mecanismo de proteção da
fixture baseline; o efeito concreto de cada execução sobre um item; o
schema do documento de sucesso produzido pelo executor; a classificação
individual e global dos resultados; as regras precisas de validação da
entrada; o ciclo de vida do diretório temporário por invocação; e os
controles sintéticos necessários para provar, em teste, a interrupção e a
restauração protegida exigidas por D-SEL-19.

Este documento fecha essas lacunas como especialização do Handoff 2, sem
reabrir o núcleo da seleção múltipla (D-SEL-01 a D-SEL-10), sem substituir a
ADR-0034, sem definir o binding real entre Orquestrador e Pipeline, sem
antecipar o `ITEM-0004`, sem ativar o chip `Executar` na interface e sem
criar a tela de resultado do Handoff 3 ou integrar o fluxo completo do
Handoff 4.

---

## 3. Decisão explícita do usuário

### H2-ESP-01 — Natureza da execução

O Handoff 2 utiliza fixtures e executor sintético.

```yaml
binding_real: nao_implementado
integracao_com_pipeline: nao_implementada
execucao_mutavel_e_reversivel: confinada_ao_ambiente_demonstrativo
```

### H2-ESP-02 — Fronteira simulada

A simulação cobre somente:

```text
comando
→ execução
→ resultado
```

Não existe consulta sintética para produzir os itens selecionáveis. O
Handoff 2 recebe diretamente a lista ordenada de IDs reconciliados — o
`lote reconciliado` (`docs/nomenclatura/32_CONSOLE.md` §4.6; D-SEL-03,
D-SEL-11) — produzida pela baseline do `H-0041`.

### H2-ESP-03 — Proteção da baseline

A fixture permanente e versionada é imutável. Cada execução real altera
somente uma cópia de trabalho temporária. A baseline nunca é modificada nem
precisa ser regravada para restauração.

### H2-ESP-04 — Efeito sintético por item

Cada item da fixture possui o fato:

```yaml
processado: true|false
```

No `dry-run`, a operação calcula e informa o estado posterior previsto sem
alterar a cópia. Na execução real, altera `processado: false` para
`processado: true` na cópia temporária.

Resultados individuais mínimos:

```text
processado
ignorado
nao_encontrado
falhou
```

Item já processado é `ignorado`. ID textual válido ausente da fixture é
`nao_encontrado`.

### H2-ESP-05 — Baseline mista

A fixture sintética possui inicialmente:

```yaml
item_01:
  processado: false
item_03:
  processado: true
item_05:
  processado: false
item_07:
  processado: false
```

Um cenário adicional pode solicitar ID inexistente sem adicioná-lo à
fixture.

### H2-ESP-06 — Produtor do documento de sucesso

O executor sintético grava diretamente um documento de resultado de
execução (`docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md` §4.5) em JSON
multinível válido. Não existe schema operacional intermediário nem
conversão provisória pelo Orquestrador.

### H2-ESP-07 — Estrutura multinível

O documento de sucesso utiliza:

```yaml
tipo: multinivel
apresentacao: conjuntos_campos
niveis:
  - secao:
      tipo: container
  - registro:
      tipo: container
  - campo:
      tipo: nome_valor
```

Estrutura semântica:

```text
Resumo
└── Execução
    ├── modo
    ├── status
    ├── solicitados
    ├── processados
    ├── ignorados
    ├── nao_encontrados
    └── falhos

Itens
├── item_01
│   ├── resultado
│   ├── aplicado
│   ├── processado_antes
│   └── processado_depois
└── demais registros
```

O documento deve permanecer compacto o suficiente para a futura fixture de
resultado caber integralmente na referência lógica `80x24` (D-SEL-20;
`contrato_json_console.md` §14.8).

Este documento é uso concreto do schema semântico multinível já vigente
(`contrato_json_console.md` §12; `docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md`
§4.4 e §4.5) — não constitui novo tipo de apresentação nem novo valor de
`formato.apresentacao`. Este documento é distinto do envelope de erro
multinível já fechado por D-SEL-15 (`contrato_json_console.md` §14.6): este
H2-ESP fecha o schema do documento de **sucesso** (produzido diretamente
pelo executor quando o protocolo é concluído); o envelope de erro,
produzido pelo Orquestrador quando o resultado está ausente, malformado ou
semanticamente inválido, permanece inalterado.

### H2-ESP-08 — Schema único por modo

`dry-run` e execução real usam exatamente o mesmo schema. O resumo contém:

```yaml
modo: dry_run|executar
```

### H2-ESP-09 — Previsão e aplicação

Os mesmos valores de `resultado` são usados nos dois modos. O campo
individual:

```yaml
aplicado: true|false
```

distingue previsão de alteração persistida.

No `dry-run`:

```yaml
resultado: processado
aplicado: false
processado_antes: false
processado_depois: true
```

Na execução real correspondente:

```yaml
resultado: processado
aplicado: true
processado_antes: false
processado_depois: true
```

### H2-ESP-10 — Status global

Regras:

```yaml
processados_e_ignorados:
  status_global: sucesso

presenca_de_nao_encontrado_ou_falha_individual:
  status_global: parcial

falha_estrutural_ou_operacional_que_impeca_a_operacao:
  status_global: falha
```

Item ignorado por já estar processado é resultado normal de revalidação,
não falha do lote.

### H2-ESP-11 — Código de saída do resultado parcial

Quando o executor conclui o protocolo e produz documento válido, retorna
código `0`, inclusive quando o `status` interno do documento for `parcial`.
Código não zero é reservado a falha operacional, interrupção ou
impossibilidade de concluir o protocolo.

Esta regra opera em camada distinta da classificação de sucesso/falha do
**processo** já fechada por D-SEL-14 (`contrato_console.md` §23,
`contrato_json_console.md` §14.5): código `0` mais JSON válido classifica o
processo como bem-sucedido; o campo `status` interno ao documento (`sucesso`,
`parcial` ou `falha`, conforme H2-ESP-10) descreve o resultado semântico do
lote dentro desse processo bem-sucedido. Um processo classificado como
sucesso pode, portanto, transportar um documento com `status: parcial`.

### H2-ESP-12 — Campos individuais

Campos obrigatórios por resultado individual:

```yaml
- id
- resultado
- aplicado
- processado_antes
- processado_depois
```

Campo condicional:

```yaml
diagnostico:
  presente_somente_em:
    - nao_encontrado
    - falhou
```

Para `nao_encontrado`:

```yaml
aplicado: false
processado_antes: null
processado_depois: null
```

### H2-ESP-13 — Validação da entrada

Rejeitar integralmente, antes de qualquer alteração:

- `schema` ausente ou diferente de `selecao_execucao.v1`;
- `ids` ausente ou não sendo lista;
- lista vazia;
- ID vazio;
- ID não textual;
- IDs duplicados.

Comportamento:

```yaml
codigo_saida: nao_zero
alteracao_da_copia: nenhuma
normalizacao_silenciosa: proibida
processamento_parcial_do_pedido_invalido: proibido
```

ID textual estruturalmente válido, mas inexistente na fixture, não invalida
o pedido — resulta em `nao_encontrado` por item (H2-ESP-04), não em rejeição
estrutural.

### H2-ESP-14 — Diretório temporário por invocação

Cada invocação cria diretório temporário exclusivo:

```text
<diretorio-da-invocacao>/
├── entrada.json
├── resultado.json
└── fixture_trabalho.json
```

Regras:

- `entrada.json` usa `selecao_execucao.v1`;
- `resultado.json` é criado previamente;
- `fixture_trabalho.json` é cópia da baseline;
- os nomes internos são fixos;
- a identidade externa do diretório é única;
- proteção `finally` remove integralmente o diretório;
- sucesso, falha e `KeyboardInterrupt` não deixam resíduos.

Testes podem suspender a remoção somente por mecanismo controlado interno
ao teste, para inspecionar o estado durante a execução. Essa capacidade não
integra a CLI pública provisória.

### H2-ESP-15 — Canais textuais

Cenário normal:

```yaml
stdout: vazio
stderr: vazio
```

Cenários focais:

```yaml
sucesso_com_aviso:
  codigo_saida: 0
  resultado_json: valido
  stderr: texto_deterministico
  classificacao: sucesso

falha_operacional:
  codigo_saida: nao_zero
  stdout: texto_deterministico_opcional
  stderr: diagnostico_deterministico
```

O resultado estruturado provém exclusivamente de `resultado.json`. `stdout`
nunca é interpretado como JSON.

### H2-ESP-16 — Localização da fixture de trabalho

O executor encontra `fixture_trabalho.json` como arquivo irmão de
`resultado.json`. Não adicionar:

- campo de caminho da fixture em `entrada.json`;
- argumento `--fixture`;
- variável de ambiente normativa;
- caminho absoluto hardcoded.

A CLI continua limitada a:

```text
--entrada
--resultado
--dry-run
```

conforme já fixado por D-SEL-12 — nenhum argumento novo é introduzido por
esta ADR.

### H2-ESP-17 — Controles sintéticos

O executor reconhece os seguintes IDs reservados exclusivamente para
testes:

```yaml
__falha_operacional__:
  efeito: >
    produzir stderr determinístico, encerrar com código não zero e não
    representar item real da fixture

__resultado_invalido__:
  efeito: >
    gravar texto JSON deliberadamente inválido em resultado.json e
    encerrar com código 0

__interrupcao__:
  efeito: >
    provocar interrupção depois de uma alteração observável na cópia de
    trabalho, para provar restauração protegida
```

Esses IDs:

- não pertencem ao domínio real;
- não aparecem como itens normais da fixture;
- não instituem protocolo definitivo;
- não podem ser confundidos com `nao_encontrado`.

### H2-ESP-18 — Interrupção

Ao receber `__interrupcao__`, o executor:

1. produz alteração observável na cópia de trabalho;
2. provoca e captura `KeyboardInterrupt` somente para finalizar o
   protocolo;
3. produz documento JSON válido com `status: interrompido`;
4. garante restauração ou descarte da cópia;
5. encerra com código `130`.

A camada invocadora classifica o processo como falha porque o código é não
zero (D-SEL-14). O JSON válido é preservado para o futuro envelope de erro
do Handoff 3.

---

## 4. Decisão

Fica adotado, como especialização do Handoff 2 do `ITEM-0006`
(ADR-0034 D-SEL-12 a D-SEL-15, D-SEL-19, D-SEL-21), um protocolo provisório
de execução sintética reversível organizado em quatro camadas:

**Natureza e fronteira da simulação (H2-ESP-01, H2-ESP-02).** A execução do
Handoff 2 é inteiramente sintética: fixture e executor de demonstração, sem
binding real nem integração com o Pipeline. A simulação cobre exclusivamente
`comando → execução → resultado`; a produção do lote reconciliado que
alimenta essa cadeia permanece responsabilidade já fechada do `H-0041`, não
deste protocolo.

**Proteção da baseline e efeito por item (H2-ESP-03 a H2-ESP-05).** A
fixture sintética versionada e permanente nunca é alterada; toda mutação
ocorre em cópia de trabalho temporária, criada por invocação. O efeito de
cada execução sobre um item é o fato binário `processado`, com quatro
resultados individuais possíveis (`processado`, `ignorado`,
`nao_encontrado`, `falhou`) sobre uma baseline mista de quatro itens.

**Documento de resultado, classificação e validação
(H2-ESP-06 a H2-ESP-13).** O executor grava diretamente o documento de
resultado de execução em JSON multinível `conjuntos_campos`, uso concreto
do schema semântico já vigente, com seções `Resumo` e `Itens` e schema
único compartilhado por `dry-run` e execução real, distinguido pelo campo
`aplicado`. A classificação combina um `status_global` do documento
(`sucesso`, `parcial`, `falha`) com a classificação de processo já fixada
por D-SEL-14 — resultado parcial não implica código de saída não zero. A
entrada é validada estruturalmente antes de qualquer alteração, com
rejeição integral e sem normalização silenciosa.

**Ciclo de vida, canais e controles sintéticos
(H2-ESP-14 a H2-ESP-18).** Cada invocação opera em diretório temporário
exclusivo com nomes internos fixos (`entrada.json`, `resultado.json`,
`fixture_trabalho.json`), removido de forma protegida em toda saída,
inclusive sob interrupção. Os canais `stdout`/`stderr` permanecem textuais,
nunca interpretados como o documento de resultado. Controles sintéticos
reservados (`__falha_operacional__`, `__resultado_invalido__`,
`__interrupcao__`) permitem provar em teste os cenários de falha
operacional, resultado inválido e interrupção com restauração protegida,
sem se tornarem identificadores de domínio.

Esta decisão não altera D-SEL-01 a D-SEL-10, não redefine os argumentos de
CLI já fixados por D-SEL-12, não redefine o envelope de erro multinível já
fechado por D-SEL-15, e não introduz binding definitivo, registry,
dispatcher ou política genérica de execução.

---

## 5. Consequências

### Positivas

- Fecha as lacunas indispensáveis para implementar e testar o Handoff 2 de
  forma focal, sem reabrir o núcleo de seleção múltipla nem antecipar o
  binding real do `ITEM-0004`/Pipeline.
- Formaliza um mecanismo de proteção de baseline (cópia de trabalho
  temporária) reutilizável por qualquer cenário futuro de execução
  reversível, sem exigir restauração manual de fixture permanente.
- Reduz o documento de resultado de execução a um uso concreto do schema
  multinível já vigente, evitando um segundo schema operacional paralelo.
- Torna a classificação de processo (D-SEL-14) e a classificação semântica
  do lote (`status_global`) camadas explicitamente independentes,
  eliminando ambiguidade sobre o significado do código de saída em
  resultado parcial.
- Introduz controles sintéticos isolados e nominalmente reservados,
  permitindo provar falha operacional, resultado inválido e interrupção sem
  contaminar o domínio real de IDs.

### Custos e restrições

- Exige que a implementação mantenha duas fixtures sintéticas distintas e
  não confundíveis: a fixture de navegação/seleção do `H-0041` (oito itens)
  e a fixture de execução deste protocolo (quatro itens mistos).
- Exige gerenciamento cuidadoso de diretório temporário por invocação,
  incluindo remoção protegida sob `KeyboardInterrupt`, sem deixar resíduos.
- Introduz três identificadores reservados (`__falha_operacional__`,
  `__resultado_invalido__`, `__interrupcao__`) que a implementação deve
  impedir de colidir com IDs reais de domínio.
- Adia para a aplicação documental futura o registro terminológico de
  conceitos novos introduzidos aqui (cópia de trabalho, diretório de
  invocação, controles sintéticos), sem reservar posição de nomenclatura
  nesta etapa.

### Artefatos afetados

| Artefato | Aplicação necessária | Estado na aplicação |
|---|---|---|
| `docs/contratos/contrato_console.md` | Registrar a fronteira comportamental do Handoff 2 na operação consumidora (§23), sem duplicar schema de resultado nem CLI. | Aplicado |
| `docs/contratos/contrato_json_console.md` | Especializar §14 com H2-ESP-01 a H2-ESP-18, preservando §14.3 (CLI) e §14.6 (envelope de erro). | Aplicado |
| `docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md` | Avaliar necessidade de termos proprietários novos. | Avaliado — sem alteração; `delta_terminologico` vazio |
| `docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md` | Avaliar necessidade de termos proprietários novos. | Avaliado — sem alteração; `delta_terminologico` vazio |
| `docs/adr/INDICE_ADR.md` | Registrar a ADR-0035 após QA favorável. | Aplicado |
| `docs/backlog.md` | Atualizar o estado material do `ITEM-0006` com esta especialização do Handoff 2. | Aplicado |

---

## 6. Compatibilidade e transição

Aplicação documental realizada em 2026-07-29
(`docs/relatorios/RELATORIO_APLICACAO_ADR-0035.md`). Esta ADR especializa,
mas não substitui, a ADR-0034: o núcleo D-SEL-01 a D-SEL-10 permanece
inalterado. O protocolo aqui fechado permanece explicitamente provisório e
substituível: contratos futuros de binding, script e processamento entre o
Orquestrador e o Pipeline podem redefinir nomes de campo, formato de CLI e
mecanismo de transporte sem reabrir esta ADR, a ADR-0034 ou a seleção
múltipla.

A CLI provisória (`--entrada`, `--resultado`, `--dry-run`), fixada por
D-SEL-12, permanece com os mesmos argumentos. O envelope de erro multinível
(D-SEL-15 / `contrato_json_console.md` §14.6) permanece inalterado. O
documento de sucesso é uso concreto do schema multinível vigente, não nova
apresentação. O futuro binding definitivo pode substituir o protocolo
demonstrativo sem reabrir a seleção múltipla. O Handoff 3 consumirá o
documento de resultado e formará/apresentará envelopes de erro; o Handoff 4
fará a integração completa.

Os módulos de nomenclatura `42` e `43` foram avaliados na aplicação e
permanecem preservados — nenhum termo canônico novo foi instituído.

---

## 7. Alternativas consideradas

| Alternativa | Motivo para rejeitar ou adiar |
|---|---|
| Alterar diretamente a fixture permanente e restaurá-la depois | Rejeitada — risco de contaminação da baseline versionada em caso de falha antes da restauração; a cópia de trabalho temporária elimina esse risco por construção (H2-ESP-03). |
| Simular também a consulta dos itens selecionáveis | Rejeitada — o Handoff 2 recebe diretamente o lote reconciliado do `H-0041`; simular a consulta duplicaria responsabilidade já fechada e ampliaria a fronteira simulada além de `comando → execução → resultado` (H2-ESP-02). |
| Produzir arquivos sintéticos por item | Rejeitada — um único documento de resultado por invocação é suficiente e mais simples de validar (H2-ESP-06, H2-ESP-14). |
| Usar contador global como efeito sintético | Rejeitada — o fato binário `processado` por item é suficiente para distinguir os quatro resultados individuais exigidos (H2-ESP-04). |
| Criar schemas distintos para `dry-run` e execução real | Rejeitada — um schema único distinguido pelo campo `aplicado` evita duplicação e mantém dry-run e execução real comparáveis (H2-ESP-08, H2-ESP-09). |
| Usar valores `seria_processado`/`seria_ignorado` no dry-run | Rejeitada — os mesmos valores de `resultado` usados na execução real (H2-ESP-09) evitam um vocabulário paralelo de previsão. |
| Tratar todo resultado misto como `parcial` | Rejeitada — item ignorado por já estar processado é resultado normal de revalidação, não falha do lote (H2-ESP-10). |
| Retornar código não zero apenas por existir `nao_encontrado` | Rejeitada — o protocolo concluído com documento válido retorna `0` mesmo com `status: parcial`; código não zero é reservado a falha operacional (H2-ESP-11). |
| Normalizar IDs duplicados ou inválidos na entrada | Rejeitada — normalização silenciosa é expressamente proibida; entrada estruturalmente inválida é rejeitada integralmente (H2-ESP-13). |
| Criar temporários independentes sem diretório comum | Rejeitada — um diretório exclusivo por invocação com nomes internos fixos simplifica localização e remoção protegida (H2-ESP-14, H2-ESP-16). |
| Emitir mensagens em todos os cenários normais | Rejeitada — o cenário normal mantém `stdout`/`stderr` vazios; texto determinístico só aparece em cenários focais definidos (H2-ESP-15). |
| Adicionar `--fixture` à CLI | Rejeitada — a fixture de trabalho é localizada por convenção posicional (arquivo irmão do resultado), preservando a CLI já fixada por D-SEL-12 (H2-ESP-16). |
| Adicionar flags especiais de falha à CLI | Rejeitada — os cenários de falha são acionados por IDs de controle sintéticos na entrada, não por novos argumentos (H2-ESP-17). |
| Criar um executor separado por cenário de teste | Rejeitada — um único executor reconhece os controles sintéticos reservados, evitando duplicação de protocolo (H2-ESP-17). |
| Encerrar interrupção com código `0` | Rejeitada — a interrupção encerra com código `130`, preservando a classificação de falha do processo mesmo com JSON válido (H2-ESP-18, D-SEL-14). |

---

## 8. Itens fora de escopo

- Binding real entre Orquestrador e Pipeline.
- Aplicação da minuta genérica de binding nos dois projetos.
- Consulta de dados ou capacidades — a produção dos itens selecionáveis
  permanece no `H-0041`.
- Registry, dispatcher ou catálogo genérico de ações — `ITEM-0004`.
- Idempotência persistente por `request_id`.
- Snapshot e revisão de dados.
- Concorrência ou travas.
- Semântica real de `force`.
- Política real do domínio de input do Pipeline.
- Ativação de `Enter` ou `Executar` na interface — Handoff 3.
- Tela padrão de resultado, sua abertura e retorno — Handoff 3.
- Carregamento e renderização do resultado pela interface — Handoff 3.
- Envelope de erro produzido pela interface — já fechado por D-SEL-15,
  fora do escopo de alteração desta ADR.
- Abertura, suspensão e retorno entre telas — `ITEM-0005`.
- Integração completa dos quatro handoffs — Handoff 4.
- Paginação — `ITEM-0003`.
- Alteração da seleção múltipla já concluída pelo `H-0041`.
- QA, aplicação documental, handoff, implementação, testes de código e
  commit — fora desta execução.

---

## 9. Critérios para aplicação

- [x] `docs/contratos/contrato_json_console.md` §14 foi especializado com
  H2-ESP-01 a H2-ESP-18, preservando integralmente §14.3 (CLI) e §14.6
  (envelope de erro).
- [x] Somente os módulos proprietários da nomenclatura efetivamente afetados
  (`42`, `43`) foram avaliados e, quando material, atualizados
  (avaliação sem alteração; `delta_terminologico` vazio).
- [x] `docs/adr/INDICE_ADR.md` foi atualizado somente após QA favorável
  desta ADR.
- [x] `docs/backlog.md` foi atualizado somente quando o fluxo documental
  determinar mudança material do `ITEM-0006`.
- [x] O `delta_terminologico` desta aplicação foi registrado no relatório de
  aplicação.
- [x] Nenhuma implementação de código foi feita durante a aplicação
  documental.
- [x] Nenhum handoff foi criado na mesma etapa da aplicação documental.
- [x] Caminhos permanecem relativos à raiz do Orquestrador.
- [x] A execução de aplicação produziu relatório próprio em
  `docs/relatorios/`.
- [x] O relatório de aplicação não sobrescreveu relatório de execução
  anterior.
- [ ] A aplicação foi submetida a QA independente.

---

## 10. Relação futura com os Handoffs 2, 3 e 4

Esta ADR fecha exclusivamente as decisões indispensáveis para que o
Handoff 2 seja implementável e testável — executor sintético, cópia de
trabalho, documento de resultado, validação e controles sintéticos. Ela não
autoriza a criação do Handoff 2; a autorização de implementação permanece
sujeita a handoff próprio, criado em etapa distinta.

O Handoff 3 (tela padrão e integração da interface) consumirá o documento
de resultado de execução aqui especializado como conteúdo externo da tela
padrão `perfil: resultado_execucao` (D-SEL-16), sem que esta ADR antecipe a
estrutura de carregamento, abertura ou retorno dessa tela.

O Handoff 4 (integração e validação completa) exercitará o protocolo aqui
fechado em conjunto com a ativação real do chip `Executar`, sem que esta
ADR resolva a integração entre a interface e o executor sintético além do
que já está determinado pela CLI provisória de D-SEL-12.

---

## 11. Bloqueios

nenhum
