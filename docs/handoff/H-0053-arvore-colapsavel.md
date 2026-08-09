---
name: H-0053-arvore-colapsavel
description: "Ativa a política de navegação arvore_colapsavel (ADR-0042 D-MULTI-05) sobre a fundação de H-0052: percurso hierárquico visível por ↑/↓, expansão/recolhimento por Espaço, sem seleção, sem Todos, sem Enter, integrado a foco/cursor e subordinado à paginação da ADR-0041"
metadata:
  type: handoff_implementacao
  status: CONCLUIDO
  id: H-0053
  data_criacao: "2026-08-08"
rastreabilidade:
  contrato_alvo: docs/contratos/contrato_console.md
  adr_relacionadas:
    - docs/adr/ADR-0042-navegacao-multinivel-do-console.md
    - docs/adr/ADR-0041-paginacao-universal-por-pageup-e-pagedown.md
    - docs/adr/ADR-0043-ajuda-universal-e-chip-contextual-de-expandir-recolher.md
    - docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
    - docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
    - docs/adr/ADR-0028-apresentacoes-multinivel-e-modo-verboso-console.md
  issues_relacionadas:
    - ITEM-0007
  handoffs_anteriores:
    - H-0052
---

# H-0053 — Ativar navegação `arvore_colapsavel` sobre o console

```yaml
handoff: H-0053
adr: ADR-0042
item: ITEM-0007
ordem_no_ciclo: "2/4"
capacidade: arvore_colapsavel
predecessor_tecnico: H-0052
```

A quantidade `2/4` é registro operacional do ciclo de quatro handoffs
aprovado pelo usuário para `ITEM-0007` (H-0052 fundação/compatibilidade,
H-0053 `arvore_colapsavel`, H-0054 `selecao_multinivel`, H-0055
`dois_niveis_por_foco`), não obrigação normativa da ADR-0042.

## 1. Etapa única

Este handoff permanece H-0053 e foi concluído após a reconciliação documental,
com QA do handoff, QA da implementação, validação da alteração declarativa e
validação manual aprovados. Não autoriza commit nem o início de outro ciclo
(H-0054, H-0055, ITEM-0023, ITEM-0024).

## 2. Ordem de autoridade

1. decisão explícita do usuário (D-MULTI-01 a D-MULTI-13, ADR-0042 e
   D-CHIP-01 a D-CHIP-12, ADR-0043);
2. ADR-0042 (aceita, aplicada), ADR-0041 (aceita, aplicada), ADR-0043
   (aceita e aplicada, QA da aplicação aprovado), ADR-0026/0027/0028
   (aceitas, aplicadas);
3. `contrato_console.md`, `contrato_json_console.md`,
   `contrato_barra_de_menus.md`, `contrato_chip.md`,
   `31_BARRA_DE_MENUS_E_CHIPS.md`, `32_CONSOLE.md`;
4. este handoff.

Se houver falta, divergência ou decisão nova necessária, bloquear conforme
§17.1 e §18 deste handoff.

## 3. Estado comprovado

```yaml
ADR-0042: aceita, aplicada, QA_aplicacao=ADR_APPLICATION_APPROVED
ADR-0043:
  status: aceita_e_aplicada
  QA_ADR: ADR_APPROVED
  QA_APLICACAO: ADR_APPLICATION_APPROVED
  papel:
    - Ajuda_universal
    - chip_contextual_Expandir_Recolher
    - invariavel_cursor_arvore
H-0052:
  implementacao: IMPLEMENTED
  validacao_manual: MANUAL_VALIDATION_APPROVED
  entrega:
    - "tela/navegacao.py::tipo_navegacao_efetivo(elemento) — resolve o
       literal declarado em politica_navegacao.tipo; fallback nivel_unico
       apenas quando o campo tipo está ausente (D-MULTI-13); NÃO coage
       arvore_colapsavel/selecao_multinivel/dois_niveis_por_foco."
    - "tela/navegacao.py::console_e_focalizavel(elemento) — hoje retorna
       SEMPRE False quando tipo_navegacao_efetivo == 'arvore_colapsavel'
       (linhas 85-87: 'if tipo != \"nivel_unico\": return False'). Este é
       o stub que H-0053 substitui pela ativação real desta política."
    - "tela/carregamento/envelope_pre_adr_0028.py — valida que tipo, quando
       presente, pertence ao conjunto fechado de cinco literais e rejeita
       tabela+navegavel:true. arvore_colapsavel já é aceito como literal
       válido; nenhuma mudança de validação estrutural é necessária para
       H-0053 (ver §8.2)."
H-0053:
  implementacao: EXISTENTE
  patches_implementacao: [P01, P02]
  validacao_manual: MANUAL_VALIDATION_APPROVED
  fatos_ja_aprovados:
    - estado_inicial
    - navegacao_vertical
    - colapso_reabertura_apos_P02
  proxima_etapa: CONCLUIDO
navegacao_multinivel_de_arvore_colapsavel:
  especificacao: vigente
  implementacao: existente
  nova_alteracao: somente_apos_QA_HANDOFF
```

## 4. Objetivo

Ativar `arvore_colapsavel` como política de navegação real e observável em
TTY: um console cujo `politica_navegacao` declara
`{"navegavel": true, "tipo": "arvore_colapsavel"}` passa a ser focalizável;
`↑` percorre a sequência hierárquica atualmente visível em direção ao item
anterior quando houver item alcançável segundo o mecanismo vigente; `↓`
percorre-a em direção ao item posterior nas mesmas condições. `Espaço` sobre
um nó com filhos abre ou fecha esse ramo; fechar um ramo remove seus
descendentes do percurso e mantém o próprio ramo como item corrente. Não há
seleção, `Todos` ou nova semântica de `Enter`; a paginação (quando aplicável)
permanece exclusivamente a da ADR-0041 e a projeção navegável fica restrita
à página atual.

Nenhuma outra capacidade do `ITEM-0007` (`selecao_multinivel`,
`dois_niveis_por_foco`) é antecipada.

Esta reconciliação P02 incorpora a ADR-0043 sem substituir a semântica da
ADR-0042: a fixture deverá declarar `[?] Ajuda`, e a árvore focalizada deverá
expor o chip contextual de `Espaço` derivado do item corrente. A mudança de
cursor pode alterar imediatamente o rótulo e o estado desse chip; não há
estado válido de árvore focalizada sem cursor/item corrente navegável.

## 5. Manifesto fechado de leitura

```yaml
leitura_integral:
  - docs/adr/ADR-0042-navegacao-multinivel-do-console.md
  - docs/contratos/contrato_console.md (mínimo: §7, §19-§22, §24)
  - docs/contratos/contrato_json_console.md (mínimo: §7.1, §11-§12)
  - docs/nomenclatura/32_CONSOLE.md (§4.10)
  - docs/contratos/contrato_barra_de_menus.md
  - docs/contratos/contrato_chip.md
  - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
  - docs/adr/ADR-0043-ajuda-universal-e-chip-contextual-de-expandir-recolher.md
  - docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
  - docs/adr/ADR-0041-paginacao-universal-por-pageup-e-pagedown.md
  - docs/backlog.md (ITEM-0007)
leitura_focal:
  - arquivo: docs/handoff/H-0052-fundacao-e-compatibilidade-das-politicas-de-navegacao.md
    comando_busca: |
      rg -n 'tipo_navegacao_efetivo|resolver|console_e_focalizavel|arvore_colapsavel|Escopo futuro nominal|Arquivos preservados' docs/handoff/H-0052-fundacao-e-compatibilidade-das-politicas-de-navegacao.md
    objetivo: confirmar o ponto de intervenção exato deixado por H-0052 e os
      arquivos preservados que H-0053 não pode reabrir sem exceção
  - arquivo: tela/navegacao.py
    comando_busca: |
      rg -n 'tipo_navegacao_efetivo|console_e_focalizavel|lista_foco|cursores|mover_cima|mover_baixo|mover_esquerda|mover_direita|exibir_chip_navegar' tela/navegacao.py
    objetivo: localizar o dispatch, o cursor e as quatro funções de movimento
  - arquivo: tela/modelo.py
    comando_busca: |
      rg -n 'class NoConteudo|class ConteudoExterno|class NivelConteudo|filhos|conteudo_externo' tela/modelo.py
    objetivo: confirmar a representação hierárquica canônica (ConteudoExterno/NoConteudo)
  - arquivo: tela/renderizacao/conteudo_externo.py
    comando_busca: |
      rg -n '_linhas_apresentacao_hierarquia|def recorrer|no.filhos' tela/renderizacao/conteudo_externo.py
    objetivo: localizar o renderer vigente da apresentação hierarquia
  - arquivo: tela/renderizacao/console.py
    comando_busca: |
      rg -n 'conteudo_externo|indicador|item_logico|ind_w' tela/renderizacao/console.py
    objetivo: localizar o ponto de composição entre conteúdo externo e coluna indicadora
  - arquivo: demo/demo.py
    comando_busca: |
      rg -n '_CATALOGO_CONTEUDO_EXTERNO|id_conteudo_externo_de|mover_cima|mover_baixo|processar_espaco|comando == \" \"' demo/demo.py
    objetivo: localizar o catálogo cenário→conteúdo e o bloco de dispatch de teclas
buscas_autorizadas:
  - "config/telas/demo/h0036_console_hierarquia.json e h0036_hierarquia_conteudo.json — fixture de referência estrutural para apresentacao hierarquia (ler integralmente, são a base do par estrutural/externo desta capacidade)"
  - "tela/teste_navegacao.py — ler cabeçalhos de teste e helpers _console()/_item() (linhas 1-60) para reutilizar o padrão de fixture local de teste"
nao_ler:
  - docs/relatorios/**, salvo o relatório próprio desta execução após criado
  - branch de erro da tentativa multinível anterior (qualquer forma de leitura, diff ou comparação)
  - docs/nomenclatura/ fora de 32 e 44
```

Para leitura focal, execute o comando indicado e leia a saída; abra apenas os
trechos materialmente indicados por ela. Se a saída for insuficiente para
fechar uma decisão de escopo, use `LEITURA_ADICIONAL_NECESSARIA` (§18) — não
amplie autonomamente o contexto.

## 6. Escopo da implementação

### 6.1 Arquivos e diretórios autorizados

```text
tela/navegacao.py
tela/renderizacao/console.py
tela/renderizacao/conteudo_externo.py
demo/demo.py
tela/teste_navegacao.py
demo/teste_demo_console.py
```

E pode **criar** (caminho nominal fechado):

```text
config/telas/demo/h0053_arvore_colapsavel.json
config/telas/demo/h0053_arvore_colapsavel_conteudo.json
docs/relatorios/IMP-0053-arvore-colapsavel.md
```

Nenhum outro arquivo de código, teste ou configuração pode ser alterado sem
passar pela cláusula de exceção (§17.1).

### 6.2 Arquivos e diretórios preservados ou proibidos

```text
docs/adr/ADR-0042-navegacao-multinivel-do-console.md
docs/adr/ADR-0041-paginacao-universal-por-pageup-e-pagedown.md
docs/contratos/contrato_console.md
docs/contratos/contrato_json_console.md
docs/nomenclatura/32_CONSOLE.md
docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
docs/backlog.md
tela/modelo.py
tela/loader.py
tela/carregamento/envelope_pre_adr_0028.py
tela/carregamento/conteudo_externo.py
tela/distribuicao_matricial.py
tela/paginacao.py
tela/selecao.py
tela/renderizacao/designadores.py
demo/demo_navegacao.py
tela/teste_loader.py
tela/teste_paginacao.py
demo/teste_demo_paginacao.py
config/telas/demo/h0030_console_unico.json
config/telas/demo/h0036_console_hierarquia.json
config/telas/demo/h0036_hierarquia_conteudo.json
config/telas/demo/h0036_console_tabela.json
config/telas/demo/h0036_console_conjuntos.json
config/telas/demo/h0037_*.json
config/telas/demo/h0040_nav_console_unico_linear.json
config/telas/demo/h0045_*.json
config/telas/demo/h0052_*.json
```

Qualquer necessidade de tocar um destes é cláusula de exceção (§17.1), não
alteração automática — especialmente `tela/carregamento/envelope_pre_adr_0028.py`,
cuja validação de `tipo` já aceita `arvore_colapsavel` como literal válido
(H-0052 §7.3); H-0053 não precisa e não deve adicionar validação estrutural
nova ali (ver §8.2 sobre o tratamento de ausência de `conteudo_externo`).

### 6.3 Escopo positivo

1. `console_e_focalizavel` reconhece `arvore_colapsavel` como focalizável
   quando há conteúdo hierárquico navegável (§8.2).
2. Nova função pura de derivação da sequência hierárquica visível a partir de
   `elemento.conteudo_externo` e do estado de ramos fechados (§8.3).
3. `↑`/`↓` movem o cursor na projeção navegável da sequência (§8.4, §8.10).
4. `Espaço` alterna aberto/fechado do ramo corrente quando ele possui filhos;
   no-op sobre folha (§8.6).
5. Estado de expansão/recolhimento é estado de runtime, no mesmo dicionário
   de estado que já hospeda `cursores`/`selecoes` (§8.5, §8.6).
6. `[✥] Navegar` reflete a disponibilidade real de movimento na árvore
   na página atual (§8.8, §8.10).
7. O renderer da apresentação `hierarquia` passa a: (a) omitir descendentes
   de ramos fechados; (b) desenhar o indicador de item corrente na linha do
   nó sob cursor, somente quando o console está focado (§8.9, §8.10).
8. Fixture permanente com profundidade/ramificação suficiente e demonstração
   TTY real via `demo/demo_navegacao.py` (§10.2, §13).
9. Regressão de `nivel_unico`, `tabela`, paginação (ADR-0041) e das três
   políticas ainda inertes (`selecao_multinivel`, `dois_niveis_por_foco`).

### 6.4 Escopo negativo

```text
selecao_multinivel (H-0054)
dois_niveis_por_foco (H-0055)
Pai: filho_ativo (ITEM-0023)
distribuição geométrica de grupos multinível (ITEM-0024)
Todos
semântica de Enter
semântica nova para ←/→
paginação concorrente
execução, confirmação, cancelamento, persistência, prévia
qualquer leitura/comparação/reaproveitamento da tentativa multinível anterior
alteração de tela/carregamento/envelope_pre_adr_0028.py
alteração de tela/modelo.py (a representação ConteudoExterno/NoConteudo já está fechada por ADR-0026/0027; H-0053 apenas a consome)
```

## 7. Entradas, fixtures, temporários e saídas

```yaml
entrada_real: nenhuma (console de demonstração; sem binding a dado real)
fixtures:
  - config/telas/demo/h0053_arvore_colapsavel.json (estrutural)
  - config/telas/demo/h0053_arvore_colapsavel_conteudo.json (documento externo multinível, apresentacao "hierarquia")
temporarios: nenhum
saida_persistente: nenhuma (estado de expansão/recolhimento é exclusivamente
  de runtime; nunca gravado em JSON, nunca uma "segunda árvore" persistida)
saida_de_teste: saída padrão dos testes automatizados (pytest); nenhum arquivo novo fora do escopo de §6.1
sobrescrita: proibida sobre qualquer fixture preservada (§6.2)
limpeza: não aplicável (sem temporários operacionais)
```

## 8. Especificação de comportamento a implementar

### 8.1 Representação hierárquica canônica (não recriar)

A hierarquia real já existe e está fechada pela ADR-0026/ADR-0027, em
`tela/modelo.py`:

```text
ConteudoExterno
  .apresentacao : str            # "hierarquia" para esta capacidade
  .niveis        : list[NivelConteudo]
  .nos           : list[NoConteudo]     # nós de topo, em ordem de documento

NoConteudo
  .id       : str
  .nivel    : str                 # referencia formato.niveis[].id
  .filhos   : list[NoConteudo]     # hierarquia declarada, na ordem original
```

`elemento.conteudo_externo` (campo do `ElementoCorpo`, propagado pelo modelo
a todo console da tela — `tela/modelo.py::_propagar_conteudo_externo`) é a
ÚNICA fonte de hierarquia consumida por `arvore_colapsavel`. O console
`._campos_inertes["itens"]` (lista plana, sem relação pai/filho, consumida
por `itens_navegaveis`/`grade_de_itens` para `nivel_unico`) NÃO é usado por
esta política — não possui campo de filhos no schema de item
(`contrato_console.md` §4) e inventar um duplicaria a hierarquia já fechada
pela ADR-0026/0027. Isso fecha a questão "qual estrutura vigente representa
a hierarquia real": é `ConteudoExterno`/`NoConteudo`, não `itens`.

### 8.2 `console_e_focalizavel` — ativação real de `arvore_colapsavel`

Em `tela/navegacao.py`, o bloco atual (linhas 85-87):

```python
tipo = tipo_navegacao_efetivo(elemento)
if tipo != "nivel_unico":
    return False
```

precisa distinguir os três casos hoje unificados sob "sempre False":
`tabela` (permanece sempre `False` — §22.13 do contrato, D-MULTI-04, já
correto), `arvore_colapsavel` (H-0053 ativa) e `selecao_multinivel` /
`dois_niveis_por_foco` (continuam `False` — inertes, fora de escopo, H-0054/
H-0055).

Regra para `arvore_colapsavel`:

```text
console_e_focalizavel == True quando:
  tipo_navegacao_efetivo(elemento) == "arvore_colapsavel"
  E politica_navegacao.get("navegavel") é verdadeiro
  E elemento.conteudo_externo não é None
  E elemento.conteudo_externo.nos não é vazio
```

Console `arvore_colapsavel` sem `conteudo_externo` associado (ou com `nos`
vazio) NÃO é focalizável — não é erro estrutural, é o mesmo tratamento já
dado pelo restante do módulo a "console navegável sem item navegável" (§22.1
do contrato: "console_navegavel_sem_itens_com_navegavel_true: entra_na_lista_
de_foco: false"). Por isso `tela/carregamento/envelope_pre_adr_0028.py` não
precisa de nova validação: a ausência de conteúdo hierárquico é tratada em
tempo de foco, não em tempo de carga — `conteudo_externo` só é resolvido
depois da validação estrutural da tela, por associação separada
(ADR-0026 §19.1, §20.1).

### 8.3 Sequência hierárquica visível (derivação, sem segunda árvore)

Nova função pura em `tela/navegacao.py`, por exemplo
`sequencia_visivel_arvore(elemento, estado)`:

Esta derivação mantém duas camadas distintas: a hierarquia e sua ordem lógica
completas, fornecidas por `ConteudoExterno`/`NoConteudo`; e a projeção
atualmente renderizável e navegável, resultante da ordem lógica após a
exclusão dos descendentes de ramos fechados e, quando houver paginação, da
restrição à página vigente. A projeção da página é fornecida pela
infraestrutura de paginação existente; este handoff não define seu algoritmo.

- lê `elemento.conteudo_externo.nos`;
- lê `estado.get("ramos_fechados", {}).get(elemento.id, frozenset())` — o
  conjunto de `id`s de nó atualmente fechados nesse console (§8.5);
- percorre a hierarquia lógica em pré-ordem (pai antes dos filhos, ordem de
  documento entre
  irmãos — mesma ordem de `ConteudoExterno.nos`/`NoConteudo.filhos`,
  preservada pelo modelo);
- para cada nó visitado, inclui o próprio nó na sequência; só desce a
  `filhos` quando `no.id` NÃO está no conjunto de ramos fechados;
- aplica à ordem estrutural a projeção da página atual quando o console
  estiver paginado;
- retorna a lista de `NoConteudo` (ou de seus `id`s — decisão de menor
  solução do implementador) na ordem do universo da página que pode receber
  cursor e ser representado pelo renderer.

Esta função é recalculada a cada chamada, a partir da hierarquia canônica e
do estado de runtime — o mesmo princípio já usado por `grade_de_itens` para
`nivel_unico` (nenhuma estrutura paralela cacheada). Não é uma segunda
árvore semântica: é uma projeção linear transitória da árvore já existente.
O cursor, o renderer e `[✥] Navegar` consomem a mesma projeção da combinação
árvore/página; um nó pertencente a outra página não entra nesse universo até
que essa página seja ativada pelo mecanismo vigente.

### 8.4 Movimento vertical (`↑`/`↓`)

`mover_baixo`/`mover_cima` (`tela/navegacao.py`) precisam de um ramo para
`tipo_navegacao_efetivo(console) == "arvore_colapsavel"`, usando
`sequencia_visivel_arvore` e `estado["cursores"][console.id]` como índice
linear na sequência da página atual.

`↓` percorre a sequência visível em direção ao item posterior quando houver
item alcançável segundo o mecanismo vigente. `↑` percorre a mesma sequência
em direção ao item anterior quando houver item alcançável segundo o mecanismo
vigente. Nos limites cuja política não foi fechada pela autoridade vigente,
H-0053 não acrescenta comportamento próprio.

`mover_direita`/`mover_esquerda` (e o núcleo `_mover_horizontal`) **não são
alterados**: o guard já vigente `if tipo_navegacao_efetivo(console) !=
"nivel_unico": return estado` já os torna no-op para `arvore_colapsavel` sem
qualquer mudança de código — isso fecha, por construção, a exigência de que
`←`/`→` não ganhem semântica nova nem herdem acidentalmente a navegação
horizontal de `nivel_unico`. Nenhuma modificação é permitida nessas duas
funções nem no núcleo `_mover_horizontal`.

Entrada em `arvore_colapsavel` por Tab/Shift+Tab já funciona sem mudança:
`avancar_foco`/`recuar_foco` já fazem `cursores[console.id] = 0` em toda
entrada (D6/ADR-0031, preservado), que aqui aponta para o primeiro item
alcançável da projeção vigente. Nenhuma seta ativa outra página. Após
`PageUp`/`PageDown`, a reconciliação do cursor segue a infraestrutura vigente
da ADR-0041; H-0053 não cria regra concorrente.

### 8.5 Estado de expansão/recolhimento (runtime, mesmo padrão de `cursores`)

O estado de expansão/recolhimento é armazenado em uma nova chave do MESMO
dicionário de estado de runtime que já hospeda
`foco_console`, `cursores` e `selecoes` — por exemplo `ramos_fechados`, um
`dict` `console.id -> frozenset/set de id de nó fechado`.

```text
id de nó no conjunto de ramos_fechados[console] => esse ramo está fechado
id ausente do conjunto                             => a descida não é suprimida
                                                    na projeção corrente
```

H-0053 não define um estado inicial universal para árvores de produção. A
fixture/demonstração deve preparar deterministicamente, pelo mecanismo de
runtime existente, ao menos o ramo usado na prova em estado aberto. Nenhum
campo novo de schema é criado para isso. Se essa preparação exigir uma
escolha arquitetural material não fechada pelas autoridades ou pelos
mecanismos vigentes, o implementador deve usar a exceção operacional e as
condições de bloqueio de §17.1 e §18, sem inventar default global ou schema.

`estado["ramos_fechados"]` NUNCA é persistido em JSON, nunca sobrevive a
recarregamento de tela/cenário, e é propagado pelo runtime exatamente como
`cursores`/`selecoes` já são (`demo/demo.py`, em torno da linha 843, onde
`novo["cursores"]` e `novo["selecoes"]` já são copiados do `nav_estado`
transitório de volta ao estado persistente da sessão).

### 8.6 `Espaço` — alternância de ramo

Nova função pura em `tela/navegacao.py`, por exemplo
`alternar_ramo(estado, console)`:

- resolve o nó corrente via `sequencia_visivel_arvore` e
  `estado["cursores"][console.id]`;
- se o nó corrente tem `filhos` não vazio: alterna a presença do `id` desse
  nó em `estado["ramos_fechados"][console.id]` (inclui se ausente, remove se
  presente);
- se o nó corrente não tem filhos (folha): retorna o estado inalterado —
  `Espaço` sobre folha não cria seleção nem qualquer outra ação nova
  (D-MULTI-05).

Fechar o ramo mantém o próprio nó como item corrente (o índice do cursor na
sequência recalculada permanece apontando para esse `id`, cuja posição pode
mudar numericamente porque a sequência ficou mais curta — resolver a nova
posição do cursor pelo `id` do nó, não pelo índice numérico anterior).

### 8.7 Dispatch de teclado (`demo/demo.py`)

O bloco de dispatch já existente (linhas ~704-844) trata `\x1b[A`/`\x1b[B`
(setas cima/baixo) chamando `navegacao.mover_cima`/`mover_baixo`
incondicionalmente (essas funções já fazem o próprio guard interno por
`tipo_navegacao_efetivo` — nenhuma mudança de despacho é necessária para as
setas: o novo ramo de comportamento vive dentro de `mover_cima`/`mover_baixo`,
não no chamador).

O ramo `elif comando == " "` (linha ~838, hoje `navegacao.processar_espaco`
para consoles fora de seleção múltipla) precisa reconhecer
`tipo_navegacao_efetivo(console) == "arvore_colapsavel"` e chamar
`alternar_ramo` nesse caso, preservando o `processar_espaco` legado (no-op)
para `nivel_unico` e demais tipos sem seleção múltipla.

Persistir `nav_estado.get("ramos_fechados", {})` de volta a `novo` no mesmo
ponto onde `novo["cursores"]`/`novo["selecoes"]` já são persistidos (~linha
843).

### 8.8 `[✥] Navegar` (`exibir_chip_navegar`)

`exibir_chip_navegar` (`tela/navegacao.py`, linha ~635) hoje calcula
disponibilidade via `itens_navegaveis(console)` (ramo padrão) ou
`paginacao.linhas_logicas_navegaveis_da_pagina` (quando paginado) — nenhum
dos dois enxerga `conteudo_externo`. Precisa de um ramo adicional: quando
`tipo_navegacao_efetivo(console) == "arvore_colapsavel"`, a condição de
existência do chip considera mais de um item navegável na projeção da árvore
e da página atual, não o tamanho da árvore completa nem itens de outras
páginas. `[✥]` continua exclusivamente indicador — nunca aciona movimento
por si (§22.11 do contrato).

### 8.9 Renderer (`tela/renderizacao/conteudo_externo.py`, `console.py`)

`_linhas_apresentacao_hierarquia` hoje percorre `conteudo.nos` e desce
incondicionalmente em `no.filhos` sempre que existem (nenhum conceito de
runtime de expansão/recolhimento). Para `arvore_colapsavel` navegável e
focado, a apresentação precisa:

1. receber o conjunto de ramos fechados do console (mesma fonte de
   `estado["ramos_fechados"][console.id]`) e deixar de descer em `no.filhos`
   quando `no.id` estiver nesse conjunto — espelhando exatamente a mesma
   regra usada por `sequencia_visivel_arvore` (§8.3), para que o que é
   navegável e o que é visível na tela nunca divirjam dentro da página atual;
2. quando o console é o console focado, marcar a linha física do nó
   correspondente ao item corrente (`estado["cursores"][console.id]` já
   resolvido via a projeção de `sequencia_visivel_arvore` da página atual) com
   o indicador de foco
   (`selecionado_simbolo` do estilo global, mesma fonte que `nivel_unico`
   já usa — `contrato_console.md` §22.6), reservando a coluna correspondente
   quando o console é focalizável (mesmo princípio de `_largura_indicador_
   do_elemento` já usado em `tela/renderizacao/console.py`).

`tela/renderizacao/console.py` é o ponto de composição atual entre
`conteudo_externo` e a caixa do console (função que despacha para
`_linhas_conteudo_externo`); é o local esperado para passar o estado de
runtime (ramos fechados, console focado, cursor) para o renderer de
`conteudo_externo.py`. A menor forma de passar esses três dados cabe ao
implementador (por exemplo, parâmetros adicionais opcionais em
`_linhas_conteudo_externo`/`_linhas_apresentacao_hierarquia`, todos com
default preservando o comportamento passivo atual para consoles sem
navegação) — não se prescreve assinatura além do necessário, mas nenhuma das
duas responsabilidades (1) e (2) acima pode ficar incompleta.

### 8.10 Subordinação à paginação vigente

Quando houver paginação, a hierarquia lógica completa continua sendo a fonte
de ordem e a projeção atualmente renderizável/navegável é a parte dessa
hierarquia que pertence à página vigente, já considerada a expansão e o
recolhimento dos ramos. `↑`/`↓` operam somente nesse subconjunto alcançável e
não atravessam implicitamente uma fronteira de página. Nós pertencentes a
outra página só podem ser alcançados depois que essa página for ativada.

```yaml
cursor_implica_troca_de_pagina: false
controles_de_paginacao: [PageUp, PageDown]
```

Somente `PageUp` e `PageDown` alteram a página. Após essa mudança, o cursor é
reconciliado pela infraestrutura vigente da ADR-0041; H-0053 não cria regra
concorrente. O renderer deve representar o mesmo universo de página e árvore
que o cursor considera, e `[✥] Navegar` deve refletir a disponibilidade de
navegação por setas nessa página, não o tamanho total da árvore. Nenhum
algoritmo novo de paginação é definido neste handoff.

`tabela`/`conjuntos_campos` (outras apresentações) e `selecao_multinivel`/
`dois_niveis_por_foco` (inertes) não recebem nenhuma mudança de
comportamento de renderização por este handoff.

### 8.11 Barra de menus e chip contextual (ADR-0043)

A fixture H-0053 deve declarar, pelo mecanismo vigente da
`barra_de_menus`, o chip universal:

```text
[?] Ajuda
```

Aplicam-se as seguintes invariantes:

```yaml
existencia: obrigatoria
posicao: ultimo_chip
ativo: true
permanece_entre_paginas: true
pode_ser_omitido_para_caber: false
```

Ajuda permanece presente após mudança de foco, em todos os estados e páginas
da mesma tela. Se a largura for insuficiente, aplica-se a política vigente de
erro de layout; o chip não é omitido, truncado ou reordenado.

Para `politica_navegacao.tipo = arvore_colapsavel`, a barra deve apresentar um
chip próprio de expansão/recolhimento na faixa canônica de chips
específicos/contextuais, depois de `[⏎]` quando aplicável e antes de `[V]` e
`[?]`. Não se cria segunda ordenação completa. A mesma tecla física não funde
este chip com `[␣] Selecionar`.

O chip contextual é derivado exclusivamente do item corrente da
`arvore_colapsavel` focalizada:

| Item corrente | Estado | Representação | Estado |
|---|---|---|---|
| ramo com filhos | expandido | `[␣] Recolher` | presente, ativo |
| ramo com filhos | recolhido | `[␣] Expandir` | presente, ativo |
| folha | não aplicável | `[␣] Expandir` | presente, inativo |

Pressionar Espaço recolhe ou expande o ramo corrente; na folha, permanece sem
efeito e não cria seleção, expansão fictícia ou ação nova. O texto e o estado
ativo podem mudar imediatamente quando o cursor muda. Não são derivados de
seleção, último ramo alterado, primeiro nó, nome da fixture, página global,
item oculto ou estado global da árvore.

Quando a árvore está focalizada, cursor válido e item corrente navegável são
obrigatórios. Se não houver nó navegável visível, a árvore não é focalizável;
portanto não existe estado válido de chip contextual para árvore focalizada
sem item corrente. Após expansão, recolhimento, troca de página ou
recomputação da projeção, a implementação deve preservar ou reconciliar
cursor válido antes da próxima interação contextual, usando a infraestrutura
vigente e sem inventar algoritmo, regra de borda ou fallback novo.

```yaml
arvore_colapsavel:
  quando_focalizado:
    cursor_valido: obrigatorio
    item_corrente_navegavel: obrigatorio

  sem_nos_navegaveis_visiveis:
    focalizavel: false
```

### 8.12 Limite da integração demonstrativa multilinha/paginada

Esta reconciliação permite que a fixture contenha texto real multilinha, mas
não transforma H-0053 em ciclo dedicado de integração entre árvore,
multiline, paginação, mudança de página, cursor e expansão/recolhimento.
Preservam-se `PageUp`, `PageDown`, `[PgUp][PgDn] Páginas` e a coerência já
exigida entre página, cursor e renderer.

Essa integração será trabalho posterior e deverá ser atribuída, depois da
conclusão de H-0053, ao ITEM/ciclo proprietário já existente em
`docs/backlog.md`, se houver. Se não houver ciclo adequado, a criação do ITEM
pertence a etapa posterior. Não se atribui automaticamente a ITEM-0024 e
este patch não altera o backlog.

## 9. Entradas mínimas de teste

### Caso ATIVACAO_ARVORE

```json
"politica_navegacao": {"navegavel": true, "tipo": "arvore_colapsavel"}
```

com `conteudo_externo` de apresentação `hierarquia` e ao menos dois nós de
topo. Resultado: `console_e_focalizavel` retorna `True`; console entra em
`lista_foco`.

### Caso ARVORE_SEM_CONTEUDO

Mesmo `politica_navegacao`, sem `conteudo_externo` associado (ou
`conteudo_externo.nos` vazio). Resultado: `console_e_focalizavel` retorna
`False` — não focalizável, sem erro de carregamento.

### Caso SEQUENCIA_INICIAL

Árvore com dois nós de topo, o primeiro com dois filhos, o segundo sem
filhos. Resultado: `sequencia_visivel_arvore` retorna
`[topo1, filho1, filho2, topo2]` quando a fixture prepara o ramo usado na
prova em estado aberto (§8.5 e §10.2); o caso não define estado inicial
universal para outras árvores.

### Caso DESCER_E_SUBIR

A partir do caso acima, cursor em `topo1` (índice 0): `↓` move para
`filho1`; `↓` novamente move para `filho2`; `↓` novamente move para `topo2`;
movimentos internos equivalentes por `↑` percorrem a mesma ordem no sentido
inverso. O caso não fixa política para os limites da sequência.

### Caso FECHAR_RAMO

Cursor em `topo1`: `Espaço` fecha `topo1`. `sequencia_visivel_arvore` passa
a ser `[topo1, topo2]`; cursor permanece em `topo1` (mesmo `id`); `↓` move
diretamente para `topo2`.

### Caso REABRIR_RAMO

A partir do caso anterior, `Espaço` novamente sobre `topo1` (ainda corrente):
`filho1`/`filho2` retornam à sequência visível, na mesma posição relativa.

### Caso ESPACO_SOBRE_FOLHA

Cursor em `filho2` (sem filhos): `Espaço` não altera `ramos_fechados`, não
cria seleção, não altera a sequência visível.

### Casos de regressão (não podem quebrar)

```text
nivel_unico: todos os testes de teste_navegacao.py (D2-D15) permanecem verdes
tabela: console_e_focalizavel(tipo=="tabela") continua sempre False
selecao_multinivel / dois_niveis_por_foco: console_e_focalizavel continua sempre False
mover_direita / mover_esquerda: continuam no-op para arvore_colapsavel
paginação ADR-0041: PageUp/PageDown inalterados; setas não trocam de página
projeção paginada: setas usam somente os itens alcançáveis da página atual;
  itens de outra página não são alcançados implicitamente
[✥] Navegar: disponibilidade calculada somente no universo navegável da
  página atual
renderer/cursor: usam a mesma projeção de página e árvore
```

## 10. Fixtures

### 10.1 Testes unitários (`tela/teste_navegacao.py`)

Reutilizar o padrão local de dicts/`ElementoCorpo` já existente
(`_console()`/`_item()`). Para os casos de §9, um `ElementoCorpo` de console
com `conteudo_externo` atribuído diretamente (objetos `ConteudoExterno`/
`NoConteudo` de `tela.modelo`, construídos localmente no teste ou via
`construir_conteudo_externo` sobre um dict mínimo) — sem tocar em arquivo
JSON. Não inventar schema paralelo de teste.

### 10.2 Fixture demonstrativa permanente

```text
config/telas/demo/h0053_arvore_colapsavel.json
config/telas/demo/h0053_arvore_colapsavel_conteudo.json
```

Par estrutural/externo no mesmo padrão de
`config/telas/demo/h0036_console_hierarquia.json` +
`config/telas/demo/h0036_hierarquia_conteudo.json` (lidos integralmente
nesta autoria — ver §5). O JSON estrutural deve declarar, no console:

```json
"politica_navegacao": {"navegavel": true, "tipo": "arvore_colapsavel"}
```

A instância vigente da `barra_de_menus` da fixture também deve declarar
`[?] Ajuda`, sempre presente, ativo e último. Essa exigência não cria campo
ou schema paralelo.

O documento externo deve seguir o mesmo schema de três níveis do H-0036
(`apresentacao: "hierarquia"`, níveis `container`/`container`/`conteudo` ou
equivalente), com a forma conceitual mínima:

```text
1.
├── 1.1
├── 1.2
│   └── 1.2.1
2.
└── 2.1
```

satisfazendo: os rótulos visíveis correspondentes são `1.`, `1.1`, `1.2`,
`1.2.1`, `2.` e `2.1`; há pelo menos dois nós de topo (`1.` e `2.`); a
execução demonstrativa prepara deterministicamente o ramo `1.` aberto pelo
mecanismo de runtime existente, sem definir default universal de produção
(§8.5); `1.` possui descendentes em pelo menos dois níveis de profundidade
(prova de que fechar remove uma subárvore inteira, não apenas um filho
direto); `2.` é item visível posterior a `1.` na sequência de topo (prova de
que `↓` alcança o próximo item visível após o recolhimento de `1.`). O antigo
item `a)` não pertence à fixture e deve estar ausente. Nenhum campo de
seleção, `Todos` ou apresentação de estado selecionado.

Os textos demonstrativos devem ser reais e suficientes para que alguns itens
ocupem mais de uma linha na largura normal da demonstração. Não se exige que
todos sejam multilinha, não se fixa quantidade artificial de caracteres e as
linhas adicionais não alteram a semântica ou os identificadores da árvore.

A associação ao console vive exclusivamente no catálogo interno de
`demo/demo.py` (`_CATALOGO_CONTEUDO_EXTERNO`), no mesmo padrão das entradas
H-0036/H-0037 — nunca no JSON estrutural (ADR-0026 §19.1, já preservado por
`contrato_console.md` §19).

## 11. Comportamentos que a implementação deve provar

1. `tipo_navegacao_efetivo` continua retornando literalmente
   `arvore_colapsavel` quando declarado.
2. `arvore_colapsavel` não cai em `nivel_unico`.
3. Console de árvore navegável entra em `lista_foco`/mecanismo de foco
   segundo as regras vigentes (D2/D3/D4 preservadas).
4. Cursor inicial aponta para o primeiro nó da projeção vigente, realmente
   visível; se houver paginação, não ativa outra página.
5. `↓` percorre a ordem hierárquica visível (pré-ordem, ordem de documento)
   dentro da página atual.
6. `↑` percorre a mesma sequência no sentido inverso dentro da página atual.
7. Itens ocultos por ramo fechado são removidos imediatamente do conjunto
   alcançável.
8. Nenhum descendente oculto pode receber cursor.
9. `Espaço` sobre ramo aberto fecha o ramo.
10. Fechar o ramo mantém esse ramo como item corrente.
11. Após o fechamento, `↓` alcança o próximo item visível fora dos
    descendentes removidos.
12. `Espaço` sobre o mesmo ramo fechado o reabre.
13. Os descendentes voltam imediatamente a ser alcançáveis por `↑`/`↓`.
14. `Espaço` não cria ou modifica seleção.
15. Item sem ramo (folha) não ganha seleção ou ação nova por `Espaço`.
16. Nenhum `Todos` é criado ou exibido por esta política.
17. Nenhuma ação nova de `Enter` é criada.
18. `←`/`→` não ganham semântica nova de árvore e não caem acidentalmente na
    navegação horizontal de `nivel_unico` (garantido por construção, §8.4 —
    regressão obrigatória, não implementação nova).
19. `[✥] Navegar` aparece enquanto houver mais de um item navegável na
    projeção da árvore na página atual e some quando essa disponibilidade não
    existir, ainda que a árvore completa possua outros itens.
20. Foco, cursor e expansão/recolhimento permanecem estados distintos
    (chaves separadas do mesmo dicionário de estado, nunca fundidas).
21. `nivel_unico` permanece semanticamente inalterado (regressão de
    `teste_navegacao.py`).
22. `tabela` permanece passiva (regressão).
23. `selecao_multinivel` e `dois_niveis_por_foco` permanecem tecnicamente
    inertes (regressão).
24. `PageUp`/`PageDown` continuam sendo a única paginação (regressão de
    `teste_demo_paginacao.py`).
25. Movimentar cursor por `↑`/`↓` não cria regra automática concorrente de
    mudança de página; somente `PageUp`/`PageDown` alteram a página.
26. Renderer e cursor usam a mesma projeção da árvore na página atual.
27. Após `PageUp`/`PageDown`, o cursor é reconciliado pela infraestrutura
    vigente da ADR-0041, sem regra concorrente criada por H-0053.
28. A fixture e a barra exibem `[?] Ajuda` sempre presente, ativa e como
    último chip, inclusive após troca de foco e de página; largura
    insuficiente produz erro de layout e não autoriza omissão.
29. Ramo expandido mostra `[␣] Recolher` presente/ativo; ramo recolhido mostra
    `[␣] Expandir` presente/ativo; folha mostra `[␣] Expandir` presente/inativo.
30. Mover o cursor entre ramo e folha altera imediatamente rótulo e estado do
    chip contextual, sem tratá-lo como seleção.
31. Uma árvore focalizada sempre possui cursor/item corrente navegável válido;
    árvore sem nó navegável visível não é focalizável.
32. Expansão, recolhimento, troca de página e recomputação da projeção
    preservam ou reconciliam cursor válido antes da interação contextual.
33. A fixture demonstra exatamente os rótulos `1.`, `1.1`, `1.2`, `1.2.1`,
    `2.` e `2.1`, não contém `a)` e contém texto real multilinha em alguns
    itens, sem tornar esses nomes uma regra universal.
34. A interação dedicada entre árvore, multilinha e paginação permanece
    explicitamente adiada para trabalho posterior, sem atribuição automática
    a ITEM-0024.

Os limites superior e inferior da sequência da árvore não são transformados
em política adicional por este handoff; os testes demonstram a ordem do
percurso em posições internas e a subordinação à página vigente.

## 12. Testes obrigatórios

Cobertura focal mínima, nos proprietários reais identificados:

```text
tela/teste_navegacao.py
  - ativação do dispatch arvore_colapsavel (console_e_focalizavel)
  - focalizabilidade da árvore (com e sem conteudo_externo)
  - sequência visível inicial (pré-ordem, com o ramo da fixture preparado aberto)
  - ↓ sobre a sequência visível em posições internas, sem política de borda
  - ↑ sobre a sequência visível em posições internas, sem política de borda
  - fechamento por Espaço (alternar_ramo)
  - permanência do ramo como corrente após fechamento
  - exclusão de todos os descendentes do ramo fechado da sequência visível
  - impossibilidade de cursor em descendente oculto
  - reabertura e retorno dos descendentes à sequência visível
  - ausência de efeito de Espaço sobre folha
  - preservação de nivel_unico (D2-D15 já existentes, sem alteração de resultado)
  - preservação de tabela (console_e_focalizavel sempre False)
  - preservação de selecao_multinivel/dois_niveis_por_foco inertes
  - mover_direita/mover_esquerda permanecem no-op para arvore_colapsavel
  - exibir_chip_navegar para arvore_colapsavel (presente/ausente conforme o
    universo navegável da página atual)
  - paginação: ↑/↓ não cruzam página; somente PageUp/PageDown mudam a página
  - renderer e cursor usam a mesma projeção de página e árvore

demo/teste_demo_console.py
  - regressão do catálogo H-0036 (10 cenários existentes inalterados)
  - smoke da nova fixture h0053_arvore_colapsavel: carrega, associa
    conteúdo, renderiza sem placeholder "(console)", sem conteúdo de outro
    cenário
```

Como exigências adicionais da reconciliação P02, a implementação posterior
deve ainda cobrir:

```text
chips
  1. ramo expandido: [␣] Recolher presente e ativo
  2. ramo recolhido: [␣] Expandir presente e ativo
  3. folha: [␣] Expandir presente e inativo
  4. mudança de cursor entre ramo e folha altera o chip
  5. [?] Ajuda sempre presente e sempre ativa
  6. [?] Ajuda permanece último chip
  7. chip contextual não se comporta como seleção

cursor
  8. arvore_colapsavel focalizada possui item corrente válido
  9. console sem nó navegável visível não é focalizável
  10. expansão/recolhimento preserva ou reconcilia cursor válido

fixture
  11. nova hierarquia: 1., 1.1, 1.2, 1.2.1, 2., 2.1
  12. a) ausente
  13. pelo menos alguns itens produzem mais de uma linha
  14. o comportamento não depende dos nomes específicos da fixture
```

Comandos focais reproduzíveis (a partir da raiz):

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_navegacao.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_demo_console.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_demo_paginacao.py -q
```

E a suíte canônica completa:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest
```

Não altere teste preexistente apenas para fazê-lo passar, salvo quando este
handoff identificar nominalmente que aquele teste precisa ser estendido
(§9, §12 acima). Arquivo adicional revelado por teste não é expansão
automática de escopo — aplica-se a cláusula de exceção (§17.1).

## 13. Demonstração operacional

```yaml
cwd: "."
comando: |
  PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao \
    --tela config/telas/demo/h0053_arvore_colapsavel.json
entrada_ou_fixture:
  - config/telas/demo/h0053_arvore_colapsavel.json
  - config/telas/demo/h0053_arvore_colapsavel_conteudo.json (via catálogo demo/demo.py)
configuracao: nenhuma além da fixture
saida_esperada: sessão TTY interativa com console focado exibindo a hierarquia
  nova, cursor visível e válido no primeiro item da projeção vigente, `[?] Ajuda`
  visível como último chip e o chip contextual de Espaço derivado do item
  corrente
prova_semantica: |
  1. Ajuda está visível e é o último chip;
  2. o ramo expandido `1.` mostra `[␣] Recolher` presente e ativo;
  3. ↑/↓ percorrem a sequência `1.`, `1.1`, `1.2`, `1.2.1`, `2.`, `2.1`;
  4. Espaço sobre `1.` fecha o ramo e seus descendentes desaparecem;
  5. `1.` permanece como item corrente, com cursor visível e válido;
  6. o chip muda para `[␣] Expandir` presente e ativo;
  7. ↓ a partir de `1.` fechado segue diretamente para `2.`;
  8. Espaço sobre `1.` reabre e o chip volta a `[␣] Recolher`;
  9. uma folha mostra `[␣] Expandir` presente e inativo;
  10. Espaço sobre folha não produz efeito nem seleção;
  11. a nova hierarquia aparece corretamente e alguns textos aparecem em
      mais de uma linha;
  12. quando houver paginação, ↑/↓ permanecem na página atual e somente
      PageUp/PageDown mudam a página; a fixture não precisa declarar
      paginação para provar arvore_colapsavel.
arquivos_persistentes:
  - config/telas/demo/h0053_arvore_colapsavel.json
  - config/telas/demo/h0053_arvore_colapsavel_conteudo.json
temporarios_operacionais: nenhum
limpeza_ou_restauracao: não aplicável
validacao_manual:
  estado: MANUAL_VALIDATION_APPROVED
  executor_exclusivo: USUARIO_EM_TTY_REAL
```

Código de saída zero, isoladamente, não comprova a entrega. O agente de
implementação pode preparar e executar testes automatizados e fumaça
não-TTY, mas **não pode declarar `MANUAL_VALIDATION_APPROVED`** — essa
validação pertence exclusivamente ao usuário em TTY real.

## 14. Relatório da execução

Criar um novo relatório em:

```text
docs/relatorios/IMP-0053-arvore-colapsavel.md
```

Usar obrigatoriamente:

```text
docs/templates/TEMPLATE_RELATORIO_IMPL.md
```

Conteúdo mínimo: arquivos alterados/criados; proprietários usados;
comportamento entregue; forma de armazenamento do estado de expansão/
recolhimento; forma de derivação da sequência visível; testes focais
executados; suíte integral; demonstração preparada; validação TTY aprovada;
desvios; exceções; bloqueios. Teto normal de 600 palavras, até 900 quando
houver conteúdo material que não possa ser reduzido. Não reproduzir a ADR
nem este handoff.

## 15. Resposta terminal

Retorne somente:

```yaml
status: <STATUS_LITERAL>
relatorio: docs/relatorios/IMP-0053-arvore-colapsavel.md
artefatos:
  - <somente arquivos criados ou alterados>
bloqueios:
  - <somente quando houver>
proxima_acao: <somente quando objetivamente determinada>
```

Omitir campos vazios. Não copiar o relatório nem acrescentar conclusão
narrativa.

## 16. Fora de escopo obrigatório

É proibido, nesta e em qualquer etapa deste handoff:

```text
ler a branch defeituosa da tentativa multinível anterior
comparar com a tentativa anterior
reutilizar código da tentativa anterior
implementar selecao_multinivel
implementar dois_niveis_por_foco
criar Pai: filho_ativo
criar nova distribuição geométrica multinível
criar nova linguagem visual de seleção
transformar expandir/recolher em seleção
criar Todos
criar semântica de Enter
criar semântica nova para ←/→ sem autoridade
criar paginação concorrente
implementar execução
implementar confirmação
implementar cancelamento
implementar persistência
implementar preview/prévia
iniciar ITEM-0023
iniciar ITEM-0024
```

## 17. Preservações obrigatórias

```text
ADR-0042 (não alterar)
contratos aplicados pela ADR-0042 (contrato_console.md, contrato_json_console.md)
módulos de nomenclatura (32_CONSOLE.md, 44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md)
ADR-0041 (paginação universal)
docs/backlog.md
tela/navegacao.py::tipo_navegacao_efetivo — resolver de H-0052, reutilizado, não duplicado
tela/navegacao.py — comportamento vigente de nivel_unico (D2-D15)
tela/navegacao.py — passividade de tabela (console_e_focalizavel sempre False)
tela/modelo.py — representação ConteudoExterno/NoConteudo (ADR-0026/0027), não redesenhada
tela/carregamento/envelope_pre_adr_0028.py — validação de tipo já fechada por H-0052
paginação existente (ADR-0038/ADR-0041)
seleção existente (ADR-0034 e seleção única ADR-0031)
H-0054 (selecao_multinivel) e H-0055 (dois_niveis_por_foco) — continuam inertes
H-0053-IMP-A e H-0053-IMP-B — não reabrir
H-0053-MANUAL-A — não reabrir; validação manual aprovada pelo usuário em TTY real
```

Documentação normativa não pertence ao escopo de implementação de H-0053.

## 17.1 Exceção operacional focal (obrigatória)

Arquivo ou diretório fora da lista nominal de §6.1 não pode ser alterado
silenciosamente. Se um item externo for estritamente necessário para cumprir
o handoff, preservar testes obrigatórios ou evitar aborto desproporcional:

```yaml
status: ESCOPO_ADICIONAL_NECESSARIO
caminho: <caminho exato>
motivo: <razão estritamente necessária>
mudanca_esperada: <mudança mínima proposta>
impacto_se_nao_autorizado: <o que fica bloqueado>
```

1. pare antes da alteração;
2. informe caminho, motivo, escopo exato e mudança esperada;
3. peça autorização explícita ao usuário.

A autorização não permite criar semântica, arquitetura, schema, formato ou
política nova. Arquivo adicional revelado por teste não é expansão
automática de escopo.

## 17.2 Estado documental após P02

```yaml
handoff: H-0053
patch_documental: P02
status: CONCLUIDO
proxima_etapa: CONCLUIDO
implementacao_nova_autorizada: false
fixture_nova_autorizada: false
validacao_manual: MANUAL_VALIDATION_APPROVED
ordem_no_plano:
  H-0052: concluido
  H-0053: atual
  H-0054: futuro
  H-0055: futuro
```

O estado acima não cria H-0056, não altera a ordem do plano e não declara o
handoff pronto para implementação antes do QA_HANDOFF.

## 18. Condições de bloqueio

Bloquear quando:

- faltar decisão;
- houver contradição documental;
- for necessário inventar formato ou schema (por exemplo, campo de estado
  inicial de expansão por nó — proibido, ver §8.5);
- diretório novo necessário não estiver autorizado;
- houver risco de sobrescrever entrada real;
- o handoff for inexequível;
- a leitura focal autorizada for insuficiente — use `LEITURA_ADICIONAL_
  NECESSARIA` no formato:

```yaml
status: LEITURA_ADICIONAL_NECESSARIA
caminho: <caminho exato>
alvo: <símbolo ou trecho exato>
finalidade: <por que é indispensável>
impacto_sem_leitura: <o que não pode ser fechado>
```

Se o bloqueio ocorrer antes de qualquer resultado material, não crie
relatório. Se já houver leitura, verificação, alteração ou evidência que
precise sobreviver ao contexto, crie relatório factual do bloqueio.

## 19. Limite de encerramento

O patch documental P02 e a reconciliação deste handoff estão encerrados pelos
relatórios de QA e de validação manual aprovados.

Não reabrir o handoff, preparar ou executar commit, nem iniciar H-0054, H-0055,
ITEM-0023 ou ITEM-0024.
