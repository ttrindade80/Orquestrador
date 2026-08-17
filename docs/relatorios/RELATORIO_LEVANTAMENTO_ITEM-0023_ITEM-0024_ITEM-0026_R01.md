# Levantamento factual — ITEM-0023, ITEM-0024 e ITEM-0026

## 1. Escopo e baseline

Este documento registra somente constatações sobre o estado encontrado no
repositório. Não registra decisão arquitetural, proposta de solução, ADR,
handoff, implementação ou QA. Os relatórios históricos em `docs/relatorios/**`
não foram usados como fonte.

Baseline antes da criação deste relatório:

| Campo | Constatação | Evidência |
|---|---|---|
| Branch | `master` | `git branch --show-current` |
| HEAD | `3a8425a0c198dc3bcd43a1392e210993332eab53` | `git rev-parse HEAD` |
| Worktree | limpo; saída `## master...origin/master`, sem caminhos alterados | `git status --short --branch` |
| Data do levantamento | 2026-08-16 | contexto de execução |

Arquivos-base consultados integralmente: `docs/backlog.md` e
`docs/HISTORICO.md`. A busca obrigatória

```text
rg --files | rg 'DEFINICOES_DIFERIDAS_MULTINIVEL_PARA_CICLOS_FUTUROS\.md$'
```

não produziu resultado. O arquivo
`DEFINICOES_DIFERIDAS_MULTINIVEL_PARA_CICLOS_FUTUROS.md` está
`NAO_LOCALIZADO` neste estado do repositório. Portanto, nenhuma definição
atribuída exclusivamente a esse arquivo pode ser tratada como confirmada ou
como implementação.

Também foram consultados, por relação material:

- decisões: `docs/adr/ADR-0041-paginacao-universal-por-pageup-e-pagedown.md`,
  `docs/adr/ADR-0042-navegacao-multinivel-do-console.md` e
  `docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md`;
- handoffs: `docs/handoff/H-0053-arvore-colapsavel.md`,
  `docs/handoff/H-0055-dois-niveis-por-foco.md`,
  `docs/handoff/H-0063-tela-estilo-estrutura-navegacao-dois-niveis.md`,
  `docs/handoff/H-0072-formatacao-generica-filhos-dois-niveis-por-foco.md` e
  `docs/handoff/H-0073-aplicacao-formatacao-telas-dois-niveis-por-foco.md`;
- distinção de infraestrutura anterior:
  `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`,
  `docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md`
  e `docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md`;
- produto, configuração e testes: `tela/selecao.py`, `tela/navegacao.py`,
  `tela/renderizacao/console.py`,
  `tela/renderizacao/conteudo_externo.py`, `tela/paginacao.py`,
  `tela/modelo.py`, `tela/carregamento/formato_dois_niveis_por_foco.py`,
  `demo/demo.py`, os testes focais de navegação/formatação e as fixtures
  `h0055`, `h0063` e `h0072`.

O histórico Git focal confirma a entrada da navegação de dois níveis no
commit `cbd9946` (`feat: implementa dois niveis por foco no console`) e a
entrada da formatação posterior no HEAD `3a8425a` (`feat: formata filhos em
dois niveis por foco`). A entrada histórica do ITEM-0007 declara que os
H-0052 a H-0055 concluíram o item e separaram as capacidades futuras em
ITEM-0023 a ITEM-0026 (`docs/HISTORICO.md:396-401`).

### Convenção de classificação

As classificações usadas nas matrizes são exatamente as solicitadas:
`IMPLEMENTADO_CONFIRMADO`, `IMPLEMENTADO_PARCIAL`,
`DECIDIDO_NAO_IMPLEMENTADO`, `DEFERIDO_EXPLICITAMENTE`,
`ABERTO_PARA_DECISAO`, `NAO_CONFIRMADO` e `NAO_APLICAVEL`.

## 2. ITEM-0026

### 2.1 Estado do backlog

O backlog registra o ITEM-0026 como `Tipo: implementacao`, `Status: planejado`,
com a descrição de persistir no JSON de dados a escolha runtime de exatamente
um filho por pai em `dois_niveis_por_foco`. Os pré-requisitos são ITEM-0007
concluído e especificação/decisão própria para persistência; a próxima ação é
iniciar essa especificação sem implementar nessa etapa
(`docs/backlog.md:87-93`).

O histórico registra ITEM-0007 como concluído pelos H-0052, H-0053, H-0054 e
H-0055 (`docs/HISTORICO.md:396-401`). Não há entrada de encerramento para
ITEM-0026 em `docs/HISTORICO.md`.

### 2.2 Definições/decisões localizadas

As seguintes decisões estão fechadas para o runtime predecessor, mas não
fecham a persistência do ITEM-0026:

| Decisão | Classificação | Evidência factual |
|---|---|---|
| Cada pai tem exatamente uma escolha exclusiva e obrigatória de filho. | `IMPLEMENTADO_CONFIRMADO` | H-0055 §2.1, especialmente `docs/handoff/H-0055-dois-niveis-por-foco.md:95-104`; ADR-0042 descreve a política no cabeçalho e no escopo material (`docs/adr/ADR-0042-navegacao-multinivel-do-console.md:1-18`). |
| Espaço em outro filho transfere a escolha somente dentro do pai-alvo; Espaço no já escolhido é idempotente. | `IMPLEMENTADO_CONFIRMADO` | H-0055:95-104; `tela/selecao.py:202-221`. |
| Cursor e escolha são mecanismos distintos. | `IMPLEMENTADO_CONFIRMADO` | H-0055:102-104; `tela/selecao.py:141-157`; teste `teste_h0055_escolha_inicial_transferencia_idempotencia_e_isolamento` em `tela/teste_navegacao.py:2104-2124`. |
| O valor inicial é o primeiro filho direto listado no JSON de dados. | `IMPLEMENTADO_CONFIRMADO` | H-0055:38-41 e 254-259; `tela/selecao.py:185-199,224-233`; `demo/demo.py:521-527`. |
| A escolha de runtime não é gravada no JSON e é descartada ao sair/reabrir. | `DECIDIDO_NAO_IMPLEMENTADO` | H-0055:254-262, 289-297 e 387-394. |
| A persistência futura pertence ao ITEM-0026 e exige especificação/decisão própria. | `DEFERIDO_EXPLICITAMENTE` | H-0055:260-262 e 296; backlog `docs/backlog.md:91-93`. |

Não foi localizado documento de decisão próprio do ITEM-0026. O arquivo de
definições diferidas obrigatório também está `NAO_LOCALIZADO`; isso não fornece
um schema ou campo de persistência.

### 2.3 Implementação comprovada

#### Escolha runtime

Existe escolha runtime de exatamente um filho por pai. A função
`_reconciliar_ids_dois_niveis` percorre cada pai, conserva um filho marcado se
ele existir e, caso contrário, escolhe `pai.filhos[0]`
(`tela/selecao.py:185-199`). A função de transferência remove as escolhas do
mesmo pai e insere o novo ID, depois reconcilia todos os pais
(`tela/selecao.py:202-221`). O estado é armazenado como lista de IDs em
`estado["selecoes"][console.id]`, não como campo do nó ou do JSON
(`tela/selecao.py:37-60`).

#### Foco entre pai e filhos

Entrar nos filhos posiciona o cursor no filho escolhido do pai corrente
(`tela/navegacao.py:669-687`). Retornar ao pai somente atualiza o cursor para o
pai correspondente e devolve o mesmo estado de escolhas
(`tela/navegacao.py:690-708`). O teste focal confirma que mover o cursor entre
filhos não transfere a escolha, que a transferência mantém o cursor e que
retornar aos pais preserva `selecoes` (`tela/teste_navegacao.py:2104-2124`).

#### Independência entre pais

O teste inicializa `a1` e `b1`, transfere somente `a1` para `a2` e verifica
`["a2", "b1"]` (`tela/teste_navegacao.py:2107-2124`). A implementação também
limita a remoção ao conjunto de filhos de `pai_alvo`
(`tela/selecao.py:207-220`).

#### Ausência de escrita/restauração persistente

`criar_estado_inicial` cria `selecoes` vazio em memória
(`demo/demo.py:293-329`). A preparação de H-0055 materializa escolhas no
estado de runtime (`demo/demo.py:521-527`). O caminho de processamento copia
`selecoes` entre comandos e declara explicitamente que nunca persiste em JSON
(`demo/demo.py:814-828`). H-0055 declara que sair ou reabrir não altera o JSON
nem persiste a escolha (`docs/handoff/H-0055-dois-niveis-por-foco.md:390-394`).

Não há campo de escolha de filho na fixture estrutural
`config/telas/demo/h0055_dois_niveis_por_foco.json:22-53`; os filhos e sua
ordem estão no documento de dados
`config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json:23-74`. H-0055
também fecha que a materialização inicial não cria campo, schema ou enum
(`docs/handoff/H-0055-dois-niveis-por-foco.md:38-41`) e que a fixture não tem
campo novo de filho ativo (`docs/handoff/H-0055-dois-niveis-por-foco.md:197-209`).

O schema efetivamente validado para o bloco adicional posterior de
`dois_niveis_por_foco` aceita somente `tabulacao`, `designador`,
`apresentacao` e `tabela` (`tela/carregamento/formato_dois_niveis_por_foco.py:167-214`).
Esse bloco é formatação de filhos, não reserva de persistência da escolha.

### 2.4 Matriz factual do que falta

| Requisito/capacidade | Classificação | Estado factual e evidência |
|---|---|---|
| Escolha runtime de exatamente um filho por pai | `IMPLEMENTADO_CONFIRMADO` | Implementada em `tela/selecao.py:185-233` e coberta por `tela/teste_navegacao.py:2104-2124`. |
| Valor inicial pelo primeiro filho direto listado | `IMPLEMENTADO_CONFIRMADO` | Implementada em `tela/selecao.py:194-198,224-233`; confirmada pelo teste `:2107-2110`. |
| Permanência ao mover foco entre pai e filhos | `IMPLEMENTADO_CONFIRMADO` | `entrar_nivel_filhos` usa a escolha (`tela/navegacao.py:669-687`); retorno não altera `selecoes` (`:690-708`); teste `tela/teste_navegacao.py:2076-2085`. |
| Independência das escolhas de pais diferentes | `IMPLEMENTADO_CONFIRMADO` | Implementação por `pai_alvo` em `tela/selecao.py:207-220`; teste `tela/teste_navegacao.py:2107-2124`. |
| Escrita da escolha em JSON ou outro armazenamento persistente | `DECIDIDO_NAO_IMPLEMENTADO` | H-0055:254-262 e 289-297 proíbe a escrita neste ciclo; o runtime usa `estado["selecoes"]` (`tela/selecao.py:37-60`). |
| Restauração da escolha em nova execução | `DECIDIDO_NAO_IMPLEMENTADO` | H-0055:390-394 declara descarte ao sair/reabrir; `criar_estado_inicial` começa com `selecoes: {}` (`demo/demo.py:314-326`). |
| Schema/campo reservado para persistência | `DECIDIDO_NAO_IMPLEMENTADO` | H-0055:38-41 exclui campo/schema/enum para a materialização inicial; não há campo correspondente nas fixtures `h0055` e o validador do bloco posterior só aceita formatação (`tela/carregamento/formato_dois_niveis_por_foco.py:167-214`). |
| Ciclo posterior implementando persistência | `NAO_CONFIRMADO` | H-0063 confirma que a escolha é runtime e não altera `config/estilo.json`, `preset_default` ou publicação (`docs/handoff/H-0063-tela-estilo-estrutura-navegacao-dois-niveis.md:128-141`). H-0072/H-0073 tratam formatação, não persistência (`docs/handoff/H-0073-aplicacao-formatacao-telas-dois-niveis-por-foco.md:73-78,210-217`). Não foi localizado ciclo posterior de persistência. |
| Especificação/decisão própria para a persistência | `ABERTO_PARA_DECISAO` | O backlog mantém a próxima ação como iniciar especificação própria (`docs/backlog.md:91-93`) e H-0055 atribui a decisão ao ITEM-0026 (`docs/handoff/H-0055-dois-niveis-por-foco.md:260-262`). |

### 2.5 Pré-requisitos

| Pré-requisito vigente no backlog | Estado | Evidência |
|---|---|---|
| ITEM-0007 concluído | `SATISFEITO` | `docs/HISTORICO.md:396-401`; commit `cbd9946` implementa `dois_niveis_por_foco`. |
| Especificação/decisão própria para persistência | `NAO_SATISFEITO` | O backlog ainda manda iniciar a especificação (`docs/backlog.md:91-93`); H-0055 afirma que ela pertence ao ITEM-0026 (`docs/handoff/H-0055-dois-niveis-por-foco.md:260-262`). |

O conjunto de pré-requisitos está `PARCIAL`: o predecessor foi concluído, mas
a especificação/decisão de persistência não foi confirmada.

O `Status: planejado` representa o estado factual do ITEM-0026: a persistência
não está implementada e a decisão própria continua ausente. A descrição do
item é compatível com o código atual.

### 2.6 Estado factual resultante

O runtime de escolha exclusiva por pai está implementado e confirmado. A
persistência em JSON, a restauração em nova execução e o schema/campo para isso
estão deliberadamente fora de H-0055 e continuam sem implementação. O ITEM-0026
tem estado factual composto: runtime predecessor
`IMPLEMENTADO_CONFIRMADO`; persistência alvo `DECIDIDO_NAO_IMPLEMENTADO`; decisão
própria `ABERTO_PARA_DECISAO`.

## 3. ITEM-0023

### 3.1 Estado do backlog

O backlog registra o ITEM-0023 como `Tipo: implementacao`, `Status: bloqueado`.
A descrição exige `Pai: filho_ativo`, preservação do filho lógico/estrutural,
promoção somente visual, ausência de duplicação na lista inferior e recomposição
quando outro filho se tornar ativo. O item exclui Enter, execução,
confirmação, cancelamento, prévia e persistência
(`docs/backlog.md:95-101`).

O pré-requisito declarado é ITEM-0007 concluído e definições fechadas mantidas
no arquivo externo de definições diferidas (`docs/backlog.md:100`). ITEM-0007
está concluído, mas o arquivo externo está `NAO_LOCALIZADO` neste repositório.

### 3.2 Definições/decisões localizadas

#### Decisões explicitamente fora do ciclo predecessor

ADR-0042 lista `Pai: filho_ativo` como apresentação do filho ativo promovido
junto ao pai, reservada ao ITEM-0023, e lista separadamente a promoção visual
(`docs/adr/ADR-0042-navegacao-multinivel-do-console.md:712-721`). A mesma ADR
registra que nenhuma implementação do ciclo de navegação poderia antecipar
essas capacidades (`docs/adr/ADR-0042-navegacao-multinivel-do-console.md:693-704`)
e seu critério de aplicação repete que `Pai: filho_ativo` e a nova distribuição
de grupos não seriam antecipados (`:761-767`).

H-0055 proíbe criar `Pai: filho_ativo`, promoção visual, nova geometria ou nova
linguagem visual (`docs/handoff/H-0055-dois-niveis-por-foco.md:119-138`) e
repete no critério de aceite que não pode existir `Pai: filho_ativo`
(`docs/handoff/H-0055-dois-niveis-por-foco.md:387-394`).

#### Arquivo de definições diferidas

O backlog afirma que existem definições fechadas preservadas externamente, mas
a busca obrigatória não encontrou o arquivo. Assim:

| Parte atribuída ao ITEM-0023 | Situação da definição no arquivo solicitado |
|---|---|
| texto/apresentação `Pai: filho_ativo` | `NAO_CONFIRMADO` — arquivo `NAO_LOCALIZADO`; há somente o registro de deferimento em ADR-0042/H-0055. |
| promoção somente visual junto ao pai | `NAO_CONFIRMADO` — não há o arquivo que o backlog declara como fonte. |
| remoção da duplicação do filho promovido da lista inferior | `NAO_CONFIRMADO` — não há definição localizada no arquivo; não foi encontrada implementação correspondente. |
| recomposição quando a escolha mudar | `NAO_CONFIRMADO` — não há definição localizada no arquivo; há apenas a escolha runtime existente, sem composição promovida. |

Definição diferida não foi tratada como implementação.

### 3.3 Implementação comprovada

Existe um mecanismo runtime de filho escolhido por pai, que é a fonte de estado
compatível com a futura ideia de ativo, mas ele não é uma apresentação
`filho_ativo`. A implementação usa os nomes e os campos de escolha de H-0055:
`_reconciliar_ids_dois_niveis`, `_transferir_escolha_dois_niveis` e
`inicializar_escolhas_dois_niveis` (`tela/selecao.py:185-233`). A entrada nos
filhos posiciona o cursor no escolhido (`tela/navegacao.py:669-687`).

A projeção física atual mantém a ordem pai, filhos, próximo pai. O caminho de
formatação genérica declara expressamente que aplica-se exclusivamente aos nós
filho, que os pais preservam sua composição e que a saída continua em
pré-ordem (`tela/renderizacao/conteudo_externo.py:285-305`). O dispatcher do
renderer troca somente a formatação dos filhos quando o bloco declarativo
existe e mantém o caminho hierárquico para os pais
(`tela/renderizacao/console.py:159-198`).

As fixtures atuais também não têm um campo `filho_ativo`: H-0055 declara
explicitamente que a fixture estrutural não cria esse campo
(`docs/handoff/H-0055-dois-niveis-por-foco.md:197-209`), enquanto a fixture de
conteúdo mantém cada filho dentro de `pai.filhos`
(`config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json:23-74`).

H-0072/H-0073 implementaram a formatação de filhos, e não a promoção do filho
escolhido. H-0073 delimita a aplicação como declarativa, sem capacidade nova,
sem alteração de conteúdo, navegação ou seleção
(`docs/handoff/H-0073-aplicacao-formatacao-telas-dois-niveis-por-foco.md:73-78`)
e diz que a capacidade existente é apenas aplicada às telas reais
(`:210-217`). O código da formatação mede e emite cada pai e cada filho como
entradas separadas (`tela/renderizacao/conteudo_externo.py:373-408`).

### 3.4 Matriz factual do que falta

| Requisito/capacidade | Classificação | Estado factual e evidência |
|---|---|---|
| Conceito runtime relacionado a filho ativo | `IMPLEMENTADO_PARCIAL` | Há escolha exclusiva runtime por pai (`tela/selecao.py:185-233`), mas a autoridade usa `filho escolhido`, não um estado/apresentação `filho_ativo` (H-0055:106-117). |
| Apresentação visual `Pai: filho_ativo` ou equivalente | `DECIDIDO_NAO_IMPLEMENTADO` | Explicitamente reservada ao ITEM-0023 e proibida em H-0055: `docs/adr/ADR-0042-navegacao-multinivel-do-console.md:712-721`; `docs/handoff/H-0055-dois-niveis-por-foco.md:129-134,387-394`. |
| Promoção visual do filho escolhido junto ao pai | `DECIDIDO_NAO_IMPLEMENTADO` | ADR-0042:714-717 e H-0055:129-134. |
| Filho promovido deixar de aparecer duplicado na lista inferior | `DECIDIDO_NAO_IMPLEMENTADO` | A saída atual é pré-ordem separada de pai e filhos (`tela/renderizacao/conteudo_externo.py:285-301,373-408`); não há caminho de remoção/realocação do filho promovido. |
| Trocar o filho escolhido recompor a apresentação promovida | `DECIDIDO_NAO_IMPLEMENTADO` | A troca atual somente atualiza `estado["selecoes"]` (`tela/selecao.py:202-221`); a apresentação alvo foi explicitamente excluída por H-0055:119-138. |
| Filho continuar lógico e estruturalmente filho | `IMPLEMENTADO_CONFIRMADO` | O conteúdo mantém `pai.filhos` (`config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json:23-74`); H-0072 preserva IDs e emite pai/filhos em pré-ordem (`tela/renderizacao/conteudo_externo.py:285-301`). |
| Definições fechadas no arquivo externo indicado pelo backlog | `NAO_CONFIRMADO` | Arquivo `DEFINICOES_DIFERIDAS_MULTINIVEL_PARA_CICLOS_FUTUROS.md` `NAO_LOCALIZADO`; somente o deferimento geral foi localizado. |
| Definições do ITEM-0023 implementadas por ciclos posteriores | `NAO_CONFIRMADO` | H-0072/H-0073 comprovam formatação dos filhos, mas não a promoção; H-0073:73-78,210-217 e código `tela/renderizacao/console.py:165-198`. |
| Formatação genérica de filhos confundida com promoção do ativo | `NAO_APLICAVEL` | São caminhos distintos: H-0072 aplica somente ao nível filho (`tela/renderizacao/conteudo_externo.py:290-305`), enquanto ADR-0042 reserva promoção ao ITEM-0023 (`docs/adr/ADR-0042-navegacao-multinivel-do-console.md:714-717`). |
| Partes restantes que exigem decisão | `ABERTO_PARA_DECISAO` | O backlog manda iniciar especificação própria somente para partes abertas (`docs/backlog.md:99-101`), e a fonte declarada das definições fechadas não está presente. |

### 3.5 Pré-requisitos

| Pré-requisito vigente no backlog | Estado | Evidência |
|---|---|---|
| ITEM-0007 concluído | `SATISFEITO` | `docs/HISTORICO.md:396-401`; commit `cbd9946`. |
| Definições fechadas no arquivo externo indicado | `NAO_CONFIRMADO` | Busca obrigatória sem resultado; o backlog referencia o arquivo em `docs/backlog.md:100`, mas o arquivo está `NAO_LOCALIZADO`. |

O conjunto de pré-requisitos está `PARCIAL`. O `Status: bloqueado` não é
contradito pela ausência da apresentação alvo e pela fonte de definições não
localizada. A condição textual “após ITEM-0007” da próxima ação, contudo, já
foi satisfeita: ITEM-0007 foi encerrado em `docs/HISTORICO.md:396-401`. A
descrição funcional do alvo permanece atual; ela não afirma que a capacidade já
foi implementada.

### 3.6 Estado factual resultante

O mecanismo runtime de filho escolhido e a preservação do filho como nó lógico
existem. A capacidade específica do ITEM-0023 — promoção visual, texto
`Pai: filho_ativo`, remoção da duplicação inferior e recomposição visual — está
`DECIDIDO_NAO_IMPLEMENTADO`. As definições que o backlog afirma estarem
externamente fechadas estão `NAO_CONFIRMADO` porque o arquivo não foi localizado.

## 4. ITEM-0024

### 4.1 Estado do backlog

O backlog registra o ITEM-0024 como `Tipo: implementacao`, `Status: bloqueado`.
Sua descrição exige distribuição visual dos blocos completos de pais e filhos
multinível, incluindo múltiplas colunas e linhas, preservação de ordem, quebra
horizontal, margens, espaçamentos, compactação local de um único grupo e
continuidade entre páginas, sem alteração dos toroides
(`docs/backlog.md:103-109`).

O pré-requisito é ITEM-0007 concluído e o mesmo arquivo externo de definições
diferidas (`docs/backlog.md:108`). ITEM-0007 está concluído
(`docs/HISTORICO.md:396-401`), mas o arquivo de definições está
`NAO_LOCALIZADO`.

### 4.2 Definições/decisões localizadas

ADR-0042 reserva ao ITEM-0024 a nova distribuição geométrica de grupos,
compactação/otimização de layout e nova política de quebra entre grupos
(`docs/adr/ADR-0042-navegacao-multinivel-do-console.md:712-721`). A ADR também
declara que a aplicação não deve antecipar essas capacidades
(`docs/adr/ADR-0042-navegacao-multinivel-do-console.md:698-704,761-767`).

H-0055 preserva qualquer geometria matricial já declarada, mas afirma que o
handoff não cria distribuição, colunas, recuos ou alinhamentos
(`docs/handoff/H-0055-dois-niveis-por-foco.md:170-180`). Isso não é uma decisão
de distribuição dos blocos completos pai+filhos.

O arquivo indicado pelo backlog não foi localizado. Logo, cada definição
atribuída exclusivamente a esse arquivo permanece:

| Parte atribuída ao ITEM-0024 | Situação da definição no arquivo solicitado |
|---|---|
| múltiplas colunas e linhas para grupos completos `pai + filhos` | `NAO_CONFIRMADO` |
| ordem dos grupos, quebra horizontal, margens e espaçamentos entre grupos | `NAO_CONFIRMADO` |
| compactação local de grupo único | `NAO_CONFIRMADO` |
| continuidade entre páginas e política de manter/dividir grupo | `NAO_CONFIRMADO` |

As linhas acima não tratam o requisito do backlog como implementação nem como
definição fechada; registram somente que a fonte declarada não está disponível.

### 4.3 Implementação comprovada

#### Geometria interna dos filhos — existente, mas distinta

ADR-0047 fecha exclusivamente a apresentação física dos filhos, sem
redesenhar navegação ou seleção (`docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md:329-346`).
O código efetivamente implementa:

- tabulação declarativa min/max e escolha do maior valor que cabe
  (`tela/renderizacao/conteudo_externo.py:268-305,415-447`);
- deslocamento da unidade inteira `ec`, `tg`, designador e conteúdo
  (`tela/renderizacao/conteudo_externo.py:447-455`; ADR-0047:366-379);
- designador configurável e apresentações `texto`/`tabela`
  (`tela/renderizacao/conteudo_externo.py:315-324,457-475`; validador em
  `tela/carregamento/formato_dois_niveis_por_foco.py:167-214`);
- alinhamento medido sobre todos os filhos, inclusive pais diferentes
  (`tela/renderizacao/conteudo_externo.py:340-371`; ADR-0047:441-452);
- espaçamento local entre colunas e compactação da tabulação/espaçamento para
  caber (`tela/renderizacao/conteudo_externo.py:457-475`; ADR-0047:454-464);
- quebra de conteúdo em linhas físicas adicionais sem nova identidade lógica e
  recálculo em resize (`docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md:466-482`;
  `docs/handoff/H-0072-formatacao-generica-filhos-dois-niveis-por-foco.md:411-423`).

As fixtures reais materializam essa capacidade: H-0055 declara tabulação 5..10,
designador `A)` e texto (`config/telas/demo/h0055_dois_niveis_por_foco.json:42-51`),
H-0063 declara tabulação 5..10, tabela `preset`/`amostra` e espaçamento 3..8
(`config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json:39-53`),
e H-0072 contém fixtures de texto, tabela e ausência de designador
(`config/telas/demo/h0072_formatacao_generica_dois_niveis_por_foco.json:22-107`).
Os testes reais verificam a saída `Pai`/`Filho`, tabulação, ordem de
`ec`/`tg`/designador/conteúdo e preservação da navegação
(`demo/teste_demo_h0073_h0055_reconciliado.py:112-171`;
`tela/teste_navegacao.py:2224-2248`).

Essa implementação não é distribuição de grupos completos. O renderer, quando
trata `dois_niveis_por_foco`, chama a projeção multinível linear; o ramo de
`distribuicao_matricial` só é alcançado depois, para consoles fora desse caminho
(`tela/renderizacao/console.py:246-307`). A função de formatação entrega
entradas em pré-ordem `pai, seus filhos, próximo pai`
(`tela/renderizacao/conteudo_externo.py:285-301`).

#### Paginação existente

O mapa físico do caminho multinível atribui a cada entrada pai/filho sua própria
identidade e marca cada entrada com a política
`permitir_quebra_somente_se_maior_que_pagina`
(`tela/renderizacao/console.py:283-305`). A paginação mantém uma entrada junta se
ela couber; se a própria entrada exceder a página, ela é fragmentada
(`tela/paginacao.py:97-134`). Como pai e cada filho são entradas distintas, essa
política não mantém um grupo inteiro `pai + filhos` unido entre páginas. A
autoridade de paginação existente é item/entrada, não grupo completo. A
representação e as teclas seguem ADR-0041 (`docs/adr/ADR-0041-paginacao-universal-por-pageup-e-pagedown.md:250-273`).

#### Infraestrutura de grupos e matrizes anterior

Há implementação de composição de grupos estruturais do corpo: ADR-0015 define
`grupo` como nó estrutural que recebe uma área e redistribui essa área entre
filhos diretos (`docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md:58-89`);
H-0027 descreve composição recursiva por container, arranjos vertical/horizontal
e distribuição por filhos diretos (`docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md:477-555`).
Também existe distribuição matricial de nível único dentro de um elemento, mas
ADR-0025 distingue essa capacidade da composição hierárquica e proíbe achatar
níveis ou reorganizar descendentes implicitamente
(`docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md:44-67,187-224`).

Essas capacidades operam em `corpo/grupo` ou nos participantes imediatos de um
elemento. Não há evidência de que tenham sido aplicadas à sequência de nós
`pai.filhos` do console `dois_niveis_por_foco`; elas são infraestrutura
reutilizável em sentido geral, não implementação do ITEM-0024.

### 4.4 Matriz factual do que falta

| Requisito/capacidade | Classificação | Estado factual e evidência |
|---|---|---|
| Distribuição dos grupos completos `pai + filhos` em múltiplas colunas | `DECIDIDO_NAO_IMPLEMENTADO` | ADR-0042 reserva nova distribuição de grupos ao ITEM-0024 (`:719-721`); o caminho multinível produz lista linear e não usa o ramo matricial (`tela/renderizacao/console.py:246-307`). |
| Distribuição dos grupos completos em múltiplas linhas | `DECIDIDO_NAO_IMPLEMENTADO` | A mesma separação vale para linhas: `h0055` usa `corpo.arranjo: vertical` (`config/telas/demo/h0055_dois_niveis_por_foco.json:22-24`) e a sequência do console continua pai/filhos em pré-ordem. |
| Preservação explícita da ordem dos grupos na distribuição futura | `IMPLEMENTADO_PARCIAL` | A ordem declarada de pais e filhos é preservada na projeção linear (`tela/renderizacao/conteudo_externo.py:373-408`; conteúdo `h0055`:23-74), mas não existe a distribuição de grupos na qual essa ordem seria aplicada. |
| Quebra horizontal entre grupos completos | `DECIDIDO_NAO_IMPLEMENTADO` | Nova política de quebra entre grupos foi explicitamente reservada ao ITEM-0024 (`docs/adr/ADR-0042-navegacao-multinivel-do-console.md:719-721`). |
| Margens entre grupos completos | `NAO_CONFIRMADO` | Não há definição localizada no arquivo diferido; existem margens em outras capacidades de composição, mas não no caminho `pai.filhos` do console. ADR-0025 declara seu escopo como nível único (`docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md:63-67`). |
| Espaçamentos entre grupos completos | `NAO_CONFIRMADO` | O espaçamento 3..8 comprovado é entre colunas da apresentação tabular de cada filho, não entre grupos (`tela/renderizacao/conteudo_externo.py:457-475`; `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json:45-50`). Não foi localizada decisão externa do ITEM-0024. |
| Compactação local de um único grupo completo | `DECIDIDO_NAO_IMPLEMENTADO` | Há compactação local da tabulação/espaçamento dos filhos, mas ADR-0042 reserva compactação/otimização de layout de grupos (`:719-721`); o renderer não constrói um bloco único `pai + filhos`. |
| Continuidade de grupos completos entre páginas | `DECIDIDO_NAO_IMPLEMENTADO` | O mapa/paginator opera entrada a entrada (`tela/renderizacao/console.py:283-305`; `tela/paginacao.py:97-134`), não por grupo. |
| Política para manter grupo unido ou dividi-lo entre páginas | `IMPLEMENTADO_PARCIAL` | Cada entrada individual fica junta quando cabe e pode ser fragmentada quando excede a página (`tela/paginacao.py:123-134`); a unidade completa pai+filhos não é tratada como uma entrada. |
| Mudanças na geometria preservarem toroides/navegação existentes | `IMPLEMENTADO_CONFIRMADO` | A formatação posterior não altera a navegação: H-0072 exclui alteração de política/toroides/seleção (`docs/handoff/H-0072-formatacao-generica-filhos-dois-niveis-por-foco.md:228-245`), `_mover_dois_niveis` usa a topologia estrutural (`tela/navegacao.py:942-957`) e o teste confirma navegação/seleção após formatação (`tela/teste_navegacao.py:2224-2248`). Isso confirma a preservação da infraestrutura existente, não uma nova geometria de grupos. |
| Geometria/formatação interna dos filhos | `IMPLEMENTADO_CONFIRMADO` | ADR-0047/H-0072/H-0073 e código/testes acima comprovam tabulação, designadores, texto/tabela, alinhamento, espaçamento, wrap e resize. |
| Geometria/distribuição dos grupos completos `pai + filhos` | `DECIDIDO_NAO_IMPLEMENTADO` | Não é o mesmo caminho da formatação interna; a implementação comum de `grupo`/matriz é de outra camada e não é consumida pelo caminho multinível (`tela/renderizacao/console.py:159-198,246-307`; ADR-0025:187-224). |
| Definições fechadas no arquivo externo indicado pelo backlog | `NAO_CONFIRMADO` | Arquivo `DEFINICOES_DIFERIDAS_MULTINIVEL_PARA_CICLOS_FUTUROS.md` `NAO_LOCALIZADO`. |
| Decisões restantes do ITEM-0024 | `ABERTO_PARA_DECISAO` | O backlog exige ciclo próprio de especificação de geometria/layout (`docs/backlog.md:107-109`); as regras alegadamente fechadas externamente não podem ser reproduzidas porque sua fonte não está presente. |

### 4.5 Pré-requisitos

| Pré-requisito vigente no backlog | Estado | Evidência |
|---|---|---|
| ITEM-0007 concluído | `SATISFEITO` | `docs/HISTORICO.md:396-401`; commit `cbd9946`. |
| Definições fechadas no arquivo externo indicado | `NAO_CONFIRMADO` | Busca obrigatória sem resultado; referência em `docs/backlog.md:108`. |

O conjunto de pré-requisitos está `PARCIAL`. O `Status: bloqueado` permanece
compatível com o fato de a capacidade alvo não ter implementação e de a fonte
externa indicada não estar disponível. A condição “após ITEM-0007” da próxima
ação já foi satisfeita; portanto, essa parte textual da próxima ação está
desatualizada como condição temporal. A descrição do alvo permanece factual.

### 4.6 Estado factual resultante

Existe infraestrutura de composição de grupos do corpo e distribuição matricial
de nível único, e existe formatação interna de filhos de
`dois_niveis_por_foco`. Nenhuma dessas evidências comprova distribuição dos
blocos completos `pai + filhos` por colunas/linhas, quebra horizontal entre
grupos, margens/espaçamentos de grupos, compactação de grupo ou continuidade de
grupo entre páginas. A capacidade alvo do ITEM-0024 está
`DECIDIDO_NAO_IMPLEMENTADO`; as definições detalhadas que o backlog atribui ao
arquivo externo estão `NAO_CONFIRMADO`.

## 5. Relações entre os três itens

| Relação | Constatação factual | Evidência |
|---|---|---|
| ITEM-0023 depende de ITEM-0026 | `NAO_CONFIRMADO`; não há dependência documentada. O ITEM-0023 exclui persistência e o H-0055 deixa a persistência para ITEM-0026, mas a promoção visual pode ser separada do armazenamento. | `docs/backlog.md:99`; `docs/handoff/H-0055-dois-niveis-por-foco.md:129-134,260-262`. |
| ITEM-0026 depende de ITEM-0023 | `NAO_CONFIRMADO`; não há dependência documentada. Persistência é sobre `estado["selecoes"]`/escolha runtime, que já existe sem promoção visual. | `tela/selecao.py:37-60,185-233`; `docs/backlog.md:91-93`. |
| ITEM-0024 depende de ITEM-0023 | `NAO_CONFIRMADO`; o backlog separa explicitamente a distribuição e manda não incorporar apresentação de filho ativo. | `docs/backlog.md:107-109`; ADR-0042:714-721. |
| ITEM-0024 depende de ITEM-0026 | `NAO_CONFIRMADO`; não há código ou documento que faça a geometria depender de persistência. | `docs/backlog.md:107-109`; H-0055:254-262. |
| Execução independente | Confirmada no escopo documental: ITEM-0023 trata apresentação, ITEM-0024 trata geometria e ITEM-0026 trata persistência; os próprios textos excluem as outras capacidades. | `docs/backlog.md:91-109`; `docs/adr/ADR-0042-navegacao-multinivel-do-console.md:712-723`. |
| Implementação comum entre ITEM-0023 e ITEM-0026 | Confirmada como base já existente: ambos podem consumir a escolha runtime por pai em `estado["selecoes"]`; a persistência e a promoção não estão acopladas no código atual. | `tela/selecao.py:37-60,185-233`; `tela/navegacao.py:669-708`. |
| Implementação comum entre ITEM-0023/0024 e H-0072/H-0073 | Parcial e delimitada: H-0072/H-0073 reutilizam `dois_niveis_por_foco` e formatam filhos, mas não implementam promoção nem distribuição de grupos completos. | `tela/renderizacao/console.py:159-198`; H-0073:73-78,210-217. |
| Infraestrutura de grupos/matriz reduz o alvo do ITEM-0024 | `NAO_CONFIRMADO` como redução de escopo funcional. A infraestrutura existe em `corpo/grupo` e nível único, mas ADR-0025 proíbe achatar/reorganizar descendentes e o caminho multinível não a consome. | ADR-0015:58-89; H-0027:477-555; ADR-0025:63-67,187-224; `tela/renderizacao/console.py:246-307`. |

Não foi encontrada dependência arquitetural adicional além das fronteiras
documentadas acima.

## 6. Divergências entre backlog e estado real

1. **Pré-requisito temporal já satisfeito.** Os três itens ainda citam
   ITEM-0007 concluído como pré-requisito, mas o histórico registra sua
   conclusão (`docs/HISTORICO.md:396-401`). Nos ITEM-0023 e ITEM-0024, a frase
   “Apos ITEM-0007” da próxima ação já não descreve uma condição futura.

2. **Fonte externa declarada não reproduzível.** ITEM-0023 e ITEM-0024 dizem
   que as definições fechadas estão em
   `DEFINICOES_DIFERIDAS_MULTINIVEL_PARA_CICLOS_FUTUROS.md`
   (`docs/backlog.md:100,108`), mas a busca obrigatória não localizou o arquivo.
   O estado factual dessas definições é `NAO_CONFIRMADO`; o backlog não pode
   ser usado sozinho como prova de que elas estão fechadas.

3. **Capacidade adjacente posterior não refletida nos três textos.** O histórico
   registra ADR-0047/H-0072/H-0073 como concluídos e o HEAD contém código,
   configurações e testes compatíveis (`docs/HISTORICO.md:426-431`;
   `tela/renderizacao/conteudo_externo.py:285-475`). Isso não contradiz as
   descrições dos três itens, porque a formatação interna de filhos não é a
   promoção visual do ITEM-0023 nem a distribuição de grupos completos do
   ITEM-0024. É uma omissão de estado adjacente, não evidência de conclusão dos
   itens-alvo.

4. **Status dos itens.** `ITEM-0026: planejado` é compatível com a ausência da
   persistência e da decisão própria. `ITEM-0023: bloqueado` e
   `ITEM-0024: bloqueado` não são contraditos pelo estado alvo não implementado
   e pela fonte de definições não localizada. O que está desatualizado é a
   condição temporal “após ITEM-0007”, não uma prova de que os status devam ser
   trocados.

5. **Histórico.** `docs/HISTORICO.md` não registra os três itens como encerrados,
   enquanto os mantém no backlog, coerentemente com as constatações acima.

## 7. Resumo comparativo

| Item | Já implementado | Decidido/não implementado | Aberto | Pré-requisitos | Status factual |
|---|---|---|---|---|---|
| ITEM-0026 | Escolha exclusiva runtime por pai; inicialização pelo primeiro filho; independência entre pais; preservação entre níveis/foco. | Persistência JSON/outro armazenamento, restauração em nova execução e campo/schema de persistência: `DECIDIDO_NAO_IMPLEMENTADO`. | Especificação/decisão própria de persistência: `ABERTO_PARA_DECISAO`. | ITEM-0007 `SATISFEITO`; decisão própria `NAO_SATISFEITA`; conjunto `PARCIAL`. | `planejado` representa o estado do alvo. |
| ITEM-0023 | Escolha runtime relacionada e preservação do filho como nó lógico/estrutural: `IMPLEMENTADO_PARCIAL`/`IMPLEMENTADO_CONFIRMADO`; formatação genérica de filhos é capacidade adjacente. | `Pai: filho_ativo`, promoção, não duplicação e recomposição visual: `DECIDIDO_NAO_IMPLEMENTADO`. | Definições do arquivo externo e partes ainda abertas: `NAO_CONFIRMADO`/`ABERTO_PARA_DECISAO`. | ITEM-0007 `SATISFEITO`; definições externas `NAO_CONFIRMADAS`; conjunto `PARCIAL`. | `bloqueado` é compatível com o alvo ausente; condição “após ITEM-0007” está satisfeita. |
| ITEM-0024 | Formatação interna de filhos e infraestrutura geral de grupos/matrizes em camadas distintas; ordem linear pai/filhos preservada. | Distribuição de grupos completos, quebra/margens/espaçamentos de grupos, compactação de grupo e continuidade entre páginas: `DECIDIDO_NAO_IMPLEMENTADO` ou `NAO_CONFIRMADO` conforme a parte. | Geometria detalhada atribuída ao arquivo externo: `NAO_CONFIRMADO`; ciclo próprio de geometria/layout: `ABERTO_PARA_DECISAO`. | ITEM-0007 `SATISFEITO`; definições externas `NAO_CONFIRMADAS`; conjunto `PARCIAL`. | `bloqueado` é compatível com o alvo ausente; condição “após ITEM-0007” está satisfeita. |

## Evidência final de materialização

Este arquivo é o único arquivo criado/alterado por este levantamento:

```text
docs/relatorios/RELATORIO_LEVANTAMENTO_ITEM-0023_ITEM-0024_ITEM-0026_R01.md
```
