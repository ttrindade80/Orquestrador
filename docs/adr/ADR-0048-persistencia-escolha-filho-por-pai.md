# ADR-0048 — Persistência da escolha de filho por pai

```yaml
id: ADR-0048
titulo: Persistência da escolha de filho por pai
status: ADR_APPLIED
item: ITEM-0026
item_titulo: Persistência da escolha de filho por pai
data: 2026-08-16
baseline: master / 3a8425a
```

Esta ADR foi criada a partir de onze decisões fechadas fornecidas ao autor
documental (D-0026-01 a D-0026-11). Nenhuma delas foi escolhida, reaberta ou
alterada por este documento. Não há arquitetura, schema executivo, política,
representação visual ou fluxo de execução introduzido além do que foi
explicitamente decidido, exceto a decisão adicional D-0026-12, incorporada
pelo patch `P02` descrito abaixo. QA desta ADR: `ADR_APPROVED`, após patch
`P01` (achado `QA-ADR0048-001`, resolvido). Aplicação documental realizada,
reconciliando `contrato_console.md`, `contrato_json_console.md` e os módulos
de nomenclatura `32`, `42` e `43`; o QA dessa aplicação (`QA-APP-0048`)
resultou em `BLOCKED_DOCUMENTATION`, motivado pelo achado `QA-APP-0048-001`
— o nome/representação pública da escolha persistida ainda não estava
fechado. O patch `P02` fecha essa decisão de schema (D-0026-12),
materializando o literal público `filho_default`. A correção dos documentos
já aplicados, o QA pós-patch, o handoff, a implementação e a validação
foram concluídas. O `ITEM-0026` é encerrado pelo fechamento deste ciclo.

---

## 1. Contexto e problema

### 1.1 Estado predecessor

A política de navegação `dois_niveis_por_foco`, fechada pela ADR-0042
(D-MULTI-07 a D-MULTI-09) e propagada em `contrato_console.md` §22.16, já
possui: pais e filhos estruturais; exatamente uma escolha runtime de filho por
pai (a **seleção exclusiva obrigatória de filho por pai**); transferência da
escolha por Espaço dentro do pai; independência entre cursor e escolha; e
independência das escolhas entre pais.

Hoje essa escolha é mantida **somente em runtime**: é estado vivo da sessão,
descartado ao encerrar a execução. O comportamento histórico de inicializar a
escolha pelo primeiro filho de cada pai é **predecessor** desta capacidade —
ele não constitui autoridade persistida da escolha e não define a persistência
nova (D-0026-02).

### 1.2 Problema

Não existe autoridade documental que defina onde a escolha ativa de filho por
pai vive de forma persistida, quem a fornece, como ela é restaurada em nova
execução e como uma alteração feita na tela se torna persistente. Sem esse
fechamento, a escolha do usuário não sobrevive à sessão e nenhuma camada é
formalmente responsável por sua gravação.

### 1.3 Objeto

O `ITEM-0026` não redesenha a navegação de `dois_niveis_por_foco`. Seu objeto
é transformar a escolha de filho por pai em **estado semanticamente fornecido
e persistido pelo produtor dos dados**, com ciclo explícito de baseline,
candidato, aplicação confirmada e restauração.

### 1.4 Autoridades consultadas

| Documento | Papel |
|---|---|
| `docs/backlog.md` | Registra o `ITEM-0026` e seu escopo |
| `docs/adr/ADR-0042-navegacao-multinivel-do-console.md` | Autoridade da política `dois_niveis_por_foco` e da seleção exclusiva obrigatória de filho por pai |
| `docs/adr/ADR-0046-alteracao-aplicacao-estilo-global-runtime.md` | Filosofia de baseline persistida × candidato, Aplicar por divergência, confirmação por pop-up e persistência fail-closed |
| `docs/contratos/contrato_console.md` | Comportamento vigente do console, §22.16 e fronteiras das seções 19–25 |
| `docs/contratos/contrato_json_console.md` | Envelope do console e schema semântico do documento externo de conteúdo (§11–§15) |
| `docs/contratos/contrato_estilo.md` | Ciclo normativo de baseline, candidato, persistência e publicação (§3.8) como referência de filosofia |
| `docs/contratos/contrato_popup.md` | Sistema genérico de pop-up modal, resultados `CONFIRMADO`/`ABORTADO` e fronteira com o chamador |
| `docs/contratos/contrato_barra_de_menus.md` | Semântica contextual vigente de ações e estados de chip |
| `docs/nomenclatura/01_NUCLEO_COMUM.md`, `02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md`, `10_ESTILO.md`, `31_BARRA_DE_MENUS_E_CHIPS.md`, `32_CONSOLE.md`, `35_POPUP.md`, `42_DADOS_EXTERNOS_MULTINIVEL.md`, `43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md` | Terminologia canônica: produtor, consumidor, loader, configuração × runtime, JSON estrutural × JSON externo de conteúdo, cursor × escolha, pop-up genérico |

---

## 2. Decisão

### 2.1 D-0026-01 — Autoridade persistida pertence aos dados externos

O produtor responsável por gerar o documento externo de dados deve fornecer,
para cada pai sujeito à política `dois_niveis_por_foco`, qual de seus filhos
está ativo.

A informação persistida pertence ao **JSON externo de conteúdo**. Ela não
pertence:

- ao JSON estrutural da tela;
- à configuração global de estilo;
- ao estado de cursor;
- ao renderer.

A escolha ativa persistida é **conteúdo semântico** fornecido pelo produtor —
não é resultado físico calculado, não é geometria e não é configuração de
apresentação da tela. A fronteira vigente do documento externo
(`contrato_json_console.md` §11.4 e §12.6) permanece preservada.

### 2.2 D-0026-02 — Exclusividade persistida

A estrutura persistida representa **escolha ativa exclusiva de filho por
pai**: para cada pai há exatamente um filho ativo. O produtor deve entregar
essa informação **explicitamente**.

A solução alvo não deve tratar a posição do primeiro filho como autoridade
persistida da escolha. O comportamento histórico de inicializar pelo primeiro
filho é predecessor da capacidade e não define a persistência nova.

### 2.3 D-0026-03 — Baseline e candidato

Ao carregar os dados, a escolha ativa persistida fornecida pelo produtor
constitui a **baseline persistida** da tela.

Durante a interação, mudanças feitas pelo usuário constituem um **candidato de
runtime**, separado da baseline persistida. Alterar a escolha na tela:

- modifica o candidato;
- não grava imediatamente o JSON externo;
- não altera a estrutura pai-filho;
- não altera o cursor como efeito colateral.

Cursor e escolha continuam mecanismos independentes, conforme a ADR-0042.

### 2.4 D-0026-04 — Aplicar somente quando houver divergência

A ação `Aplicar` representa a tentativa explícita de persistir o candidato.

- Quando candidato e baseline forem equivalentes, não há alteração a aplicar e
  `Aplicar` não está ativo.
- Quando houver divergência, `Aplicar` inicia o fluxo de confirmação.

A filosofia é a mesma já empregada no fluxo de aplicação de Estilo
(ADR-0046; `contrato_estilo.md` §3.8): baseline persistida e candidato de
runtime permanecem distintos até uma aplicação confirmada e bem-sucedida.

### 2.5 D-0026-05 — Reuso do pop-up genérico

A confirmação reutiliza o **sistema genérico de pop-up** já existente
(`contrato_popup.md`). Não se cria um novo sistema de pop-up para esta
capacidade.

O pop-up:

- apresenta a confirmação;
- devolve a decisão ao chamador;
- não persiste dados;
- não conhece o JSON externo;
- não executa o script produtor/atualizador;
- não contém lógica de negócio específica do `ITEM-0026`.

Os resultados relevantes permanecem os estados canônicos vigentes
`CONFIRMADO` e `ABORTADO`.

### 2.6 D-0026-06 — Persistência delegada ao responsável pelos dados

Após `CONFIRMADO`, o chamador encaminha a alteração ao script responsável pela
atualização do JSON externo dos dados. A responsabilidade pela gravação
persistente fica na **camada responsável pelos dados** — não no renderer e não
no pop-up.

Esta ADR fecha a responsabilidade e o fluxo, mas deliberadamente **não
escolhe**:

- nome de função;
- nome concreto do script;
- caminho físico definitivo do script;
- assinatura interna;
- algoritmo físico de escrita;
- mecanismo específico de escrita atômica.

Esses detalhes executivos são posteriores, desde que preservem as decisões
desta ADR e os contratos vigentes.

### 2.7 D-0026-07 — Sucesso

Somente depois de persistência completa e válida:

- a alteração conta como aplicada;
- o estado gravado passa a ser a nova baseline persistida;
- o candidato é sincronizado/equalizado com essa nova baseline;
- o fluxo retorna à tela de seleção;
- `Aplicar` deixa de estar ativo enquanto não surgir nova divergência.

Uma aplicação confirmada anteriormente não é desfeita por uma edição candidata
posterior que seja abandonada.

### 2.8 D-0026-08 — ABORTADO

`ABORTADO` cancela somente a tentativa de aplicação:

- nenhum JSON é alterado;
- nenhum script de atualização é executado para persistir a mudança;
- a baseline permanece inalterada;
- o candidato de runtime é preservado;
- o usuário retorna à seleção e pode continuar editando ou tentar aplicar
  novamente.

### 2.9 D-0026-09 — Falha de persistência

A persistência é **fail-closed**. Se o script ou a gravação não concluir com
sucesso:

- a aplicação não é considerada confirmada;
- a baseline persistida permanece a anterior;
- não se assume persistência parcial como sucesso;
- o candidato permanece disponível para nova tentativa ou edição.

Esta ADR não determina o algoritmo físico usado para garantir a gravação.

### 2.10 D-0026-10 — Restauração em nova execução

Em nova carga da tela, o estado ativo deve ser obtido novamente do documento
externo produzido/persistido. A tela não deve depender do estado runtime da
sessão anterior para reconstruir qual filho está ativo.

### 2.11 D-0026-11 — Fronteiras

Não alterar neste delta:

- semântica estrutural de pai e filhos;
- toróides de navegação;
- comportamento de cursor;
- geometria ou formatação dos filhos;
- apresentação `Pai: filho_ativo`;
- promoção visual do filho ativo;
- distribuição geométrica de grupos;
- paginação de grupos;
- `ITEM-0023`;
- `ITEM-0024`;
- sistema genérico de registro/dispatcher de ações do `ITEM-0004`;
- política global de estilo.

### 2.12 D-0026-12 — Literal público fechado: `filho_default` (patch P02)

Após `QA-APP-0048-001` (achado do QA da aplicação: o nome/representação
pública da escolha persistida não estava fechado), o usuário forneceu decisão
material nova, incorporada por este patch. Nenhuma das decisões D-0026-01 a
D-0026-11 é reaberta ou alterada por D-0026-12; esta decisão fecha
especificamente a forma literal do campo público que a ADR, até este patch,
deixava deliberadamente aberta.

**Literal fechado.** O nome público do campo que registra, para cada pai, o
ID do filho direto que constitui sua escolha persistida é exatamente
`filho_default`. Esse literal é parte do schema público do documento externo
de conteúdo. Não é substituído por `filho_ativo`, `filho_ativo_id`,
`selecionado`, `selected`, `active` ou qualquer outro alias.

**Forma estrutural.** Para cada pai sujeito a `dois_niveis_por_foco`:

- o pai possui sua própria coleção `filhos`;
- o pai possui o campo público obrigatório `filho_default`;
- `filho_default` contém o ID estável de exatamente um filho direto daquele
  pai;
- o valor de `filho_default` constitui a escolha persistida/baseline daquele
  pai (D-0026-01, D-0026-03);
- cada pai possui seu próprio `filho_default` — não existe um único
  `filho_default` global compartilhado entre todos os pais;
- a ordem física dos filhos na coleção não determina nem substitui o valor de
  `filho_default` — reafirma D-0026-02: a posição do primeiro filho não é
  autoridade persistida da escolha;
- não se cria mapa paralelo global pai → filho para essa finalidade, porque o
  próprio pai já é a unidade proprietária da sua escolha persistida.

**Semântica normativa.** Para cada pai aplicável:

1. `filho_default` é obrigatório;
2. seu valor é um ID;
3. esse ID deve identificar exatamente um filho direto existente na coleção
   `filhos` daquele pai;
4. o filho referenciado pertence ao próprio pai;
5. dois pais podem possuir valores de `filho_default` independentes entre si;
6. a ordem física dos filhos não determina o valor de `filho_default`;
7. o primeiro filho não é fallback para `filho_default` ausente;
8. ausência de `filho_default` em um pai aplicável é documento inválido
   segundo esta política;
9. referência a ID inexistente é documento inválido;
10. referência a um filho pertencente a outro pai é documento inválido;
11. referência ambígua por ID duplicado é inválida, conforme as regras
    vigentes de identidade;
12. o loader/consumidor usa `filho_default` para formar a baseline inicial
    daquele pai (D-0026-03);
13. a edição de runtime feita pelo usuário na tela altera somente o
    candidato (D-0026-03), nunca `filho_default` diretamente;
14. `CONFIRMADO` seguido de persistência bem-sucedida substitui, no documento
    externo, o `filho_default` daquele pai pelo ID do novo filho escolhido
    (D-0026-07);
15. `ABORTADO` não altera `filho_default` de nenhum pai (D-0026-08);
16. falha de persistência não altera autoritativamente `filho_default` de
    nenhum pai (D-0026-09);
17. em nova execução, a escolha ativa de cada pai é restaurada a partir do
    `filho_default` persistido daquele pai (D-0026-10).

**Relação com o padrão estrutural do Estilo.** Para materializar a decisão
acima sem inventar desenho novo, o usuário determinou que a forma estrutural
replique, para `dois_niveis_por_foco`, o mesmo padrão de persistência já
usado pelo sistema de Estilo para registrar o preset persistido de cada
categoria (`contrato_estilo.md` §3.1–§3.3; ADR-0030 D2): cada categoria de
Estilo possui sua própria coleção `presets`; a categoria possui
`preset_default`; `preset_default` identifica qual preset daquela categoria é
a escolha persistida; a escolha de runtime/candidata pode divergir
temporariamente; somente aplicação confirmada substitui o valor persistido.

A equivalência é estrutural: `preset_default` está para um item de `presets`
de uma categoria de Estilo assim como `filho_default` está para um item de
`filhos` de um pai em `dois_niveis_por_foco`. A analogia cobre exclusivamente
o padrão de persistência — coleção local, referência persistida local,
baseline carregada, candidato de runtime, aplicação confirmada substituindo a
referência persistida — e não transforma o Estilo em autoridade sobre o
documento externo de conteúdo. Nenhum campo de aparência, preset ou regra
específica do Estilo (borda, chip, indicadores, `cor_inativo`, `cor_alerta`,
`tiling`) é copiado ou introduzido no schema de `dois_niveis_por_foco`. A
autoridade persistida da escolha de filho por pai continua sendo,
exclusivamente, o JSON externo de conteúdo (D-0026-01); `config/estilo.json`
e a política global de estilo permanecem inalterados e fora deste delta,
como já registrado em §6.

**Representação conceitual.** Apenas como exemplo ilustrativo não expansivo,
sem introduzir campos não decididos:

```yaml
pai:
  id: <id_do_pai>
  filho_default: <id_de_um_filho_direto>
  filhos:
    - id: <id_do_filho_1>
    - id: <id_do_filho_2>
```

**O que esta decisão não altera.** D-0026-12 não reabre nem modifica
autoridade no documento externo, baseline × candidato, cursor × escolha,
confirmação, pop-up, responsabilidade de persistência, sucesso, `ABORTADO`,
fail-closed, restauração, ou as fronteiras de `ITEM-0023`/`ITEM-0024`
(D-0026-11). Continuam fora desta decisão: nome de função, nome e caminho do
script, assinatura interna, algoritmo físico de escrita e mecanismo concreto
de escrita atômica (D-0026-06, D-0026-09) — esses detalhes executivos devem
apenas preservar o contrato público `filho_default` e o fail-closed já
fechado.

---

## 3. Camadas de estado

| Camada | Conteúdo e responsabilidade | Persiste? |
|---|---|---|
| Escolha ativa persistida | Dado semântico do JSON externo de conteúdo, fornecido explicitamente pelo produtor: exatamente um filho ativo por pai sujeito à política | Sim — autoridade persistida |
| Baseline persistida da tela | A escolha ativa persistida tal como carregada; referência de comparação do fluxo | Deriva da carga; substituída somente por aplicação confirmada e bem-sucedida |
| Candidato de runtime | Estado vivo separado, acumulando as escolhas feitas pelo usuário na tela | Não — estado de runtime |
| Cursor | Mecanismo de navegação, independente da escolha | Não — estado de runtime |

A partir do patch `P02`, essa escolha ativa persistida é representada, no
documento externo, pelo campo público `filho_default` de cada pai
(D-0026-12).

O loader/consumidor continua responsável por carregar e validar o documento
externo e entregar o conteúdo semântico ao fluxo; a **persistência** da
alteração confirmada é responsabilidade distinta, delegada à camada
responsável pelos dados (D-0026-06). Loader e persistência não se confundem.

---

## 4. Transições do fluxo

| Estado | Evento | Próximo estado | Efeito obrigatório |
|---|---|---|---|
| Carga da tela | documento externo carregado | Seleção | Escolha ativa persistida vira baseline; candidato inicia equivalente à baseline |
| Seleção | mudança de escolha (Espaço) | Seleção | Atualiza somente o candidato; sem gravação, sem efeito em estrutura ou cursor |
| Seleção | `Aplicar` sem divergência | Seleção | Nenhum efeito — não há alteração a aplicar |
| Seleção | `Aplicar` com divergência | Confirmação | Abre o pop-up genérico de confirmação |
| Confirmação | `ABORTADO` | Seleção | Nenhum JSON alterado; nenhum script executado para persistir; baseline inalterada; candidato preservado |
| Confirmação | `CONFIRMADO` e persistência bem-sucedida | Seleção | Estado gravado vira a nova baseline; candidato equalizado; `Aplicar` inativo até nova divergência |
| Confirmação | `CONFIRMADO` e falha de persistência | Seleção não confirmada | Aplicação não confirmada; baseline anterior mantida; candidato disponível para nova tentativa ou edição |
| Nova execução | nova carga da tela | Carga da tela | Estado ativo obtido novamente do documento externo persistido; sem dependência do runtime anterior |

---

## 5. Compatibilidade

- A navegação de `dois_niveis_por_foco` (ADR-0042; `contrato_console.md`
  §22.16) permanece integralmente vigente: toroides, Espaço, Esc contextual,
  exclusividade da escolha e independência entre cursor e escolha não são
  redesenhados.
- Cursor, foco, seleção múltipla, página e modo verboso continuam estados de
  runtime não persistidos. Esta ADR persiste exclusivamente a escolha ativa de
  filho por pai, como conteúdo semântico do JSON externo, fornecido pelo
  produtor.
- A regra vigente de que o JSON estrutural da tela não guarda estado vivo
  permanece intacta: a autoridade persistida desta capacidade está no JSON
  externo de conteúdo, não no `tela.json`.
- O comportamento histórico de inicializar pelo primeiro filho permanece o
  predecessor da capacidade. Esta ADR não define fallback para documento
  externo que não forneça a escolha ativa; o tratamento concreto de
  compatibilidade dos documentos existentes foi materializada pela
  implementação, preservando D-0026-01 e D-0026-02.

---

## 6. Relação com ADR-0042 e ADR-0046

**ADR-0042.** Esta ADR consome a seleção exclusiva obrigatória de filho por
pai como mecanismo já fechado e acrescenta somente seu ciclo de persistência:
autoridade persistida, baseline, candidato, aplicação e restauração. Nenhuma
decisão D-MULTI é reaberta.

**ADR-0046.** Esta ADR adota a mesma filosofia de aplicação do fluxo de
Estilo — baseline persistida distinta do candidato de runtime, `Aplicar` ativo
somente sob divergência, confirmação pelo pop-up genérico, persistência
fail-closed antes de qualquer efeito durável, equalização do candidato após
sucesso e preservação de aplicação já confirmada. A analogia é **de
filosofia, não de autoridade**: o Estilo não se torna autoridade dos dados. A
autoridade persistida do `ITEM-0026` é o JSON externo de conteúdo produzido
pelo produtor dos dados; `config/estilo.json` e a política global de estilo
permanecem inalterados e fora deste delta.

O patch `P02` (D-0026-12) estende essa analogia ao nível estrutural do nome
do campo — `preset_default` está para `presets` de uma categoria de Estilo
assim como `filho_default` está para `filhos` de um pai — sem alterar essa
fronteira: a analogia permanece de padrão de persistência, não de autoridade
sobre o documento externo.

---

## 7. Distinções terminológicas preservadas

| Par | Distinção |
|---|---|
| JSON estrutural da tela × JSON externo de conteúdo | A configuração da interface permanece no `tela.json`; a escolha ativa persistida é dado semântico do documento externo |
| configuração persistida × estado vivo de runtime | A escolha ativa persistida e a baseline derivam do documento externo; candidato e cursor são estado vivo |
| produtor × consumidor | O produtor fornece explicitamente o filho ativo por pai; o consumidor carrega e usa, sem inferir nem reconstruir |
| loader × persistência | O loader lê, valida e converte; a gravação persistente pertence à camada responsável pelos dados |
| cursor × escolha | Mover o cursor não altera a escolha; alterar a escolha não move o cursor |
| baseline persistida × candidato | A baseline é a última escolha persistida conhecida; o candidato acumula edições ainda não aplicadas |
| pop-up genérico × lógica de negócio do chamador | O pop-up devolve `CONFIRMADO`/`ABORTADO`; interpretação, encaminhamento e persistência pertencem ao chamador |
| conteúdo semântico × representação física | O filho ativo é dado semântico; geometria, promoção visual e apresentação permanecem do renderer e fora deste delta |
| `preset_default` (Estilo) × `filho_default` (`dois_niveis_por_foco`) | Mesmo padrão estrutural de persistência local por unidade proprietária; o Estilo não se torna autoridade do documento externo (D-0026-12) |

---

## 8. Consequências

### Positivas

- A escolha de filho por pai sobrevive às sessões, com autoridade persistida
  única e explícita no JSON externo de conteúdo.
- O produtor passa a ser formalmente responsável por declarar o filho ativo,
  eliminando a ambiguidade do predecessor "primeiro filho".
- O ciclo baseline × candidato × aplicação confirmada reutiliza uma filosofia
  já validada pela ADR-0046, sem criar segundo modelo de aplicação.
- O pop-up genérico é reutilizado sem novo sistema modal e sem lógica de
  negócio embutida.
- A persistência fail-closed impede estado durável parcial ou inconsistente.
- O literal público `filho_default` elimina a ambiguidade de nome que
  bloqueou o QA da aplicação (`QA-APP-0048-001`), replicando um padrão de
  persistência já validado pelo Estilo sem transformá-lo em autoridade dos
  dados externos (D-0026-12).

### Custos e restrições

- A aplicação documental reconciliou os contratos e módulos de nomenclatura
  afetados (§9) sem alterar as decisões desta ADR.
- O runtime precisará distinguir baseline persistida e candidato para esta
  capacidade, além dos estados já existentes.
- O fluxo de dados ganha uma dependência explícita de um responsável pela
  atualização do JSON externo, cujos detalhes executivos permanecem abertos
  (D-0026-06) e deverão ser fechados em etapa própria.

---

## 9. Documentos afetados pela aplicação

A aplicação documental desta ADR foi executada e aprovada após o patch `P02`,
sem reabrir decisões. Foram reconciliados:

- `docs/contratos/contrato_console.md` — ciclo de persistência da escolha em
  `dois_niveis_por_foco` (§22.16 e seção 26);
- `docs/contratos/contrato_json_console.md` — dado semântico do filho ativo no
  documento externo de conteúdo (§16 e §16.7);
- `docs/nomenclatura/32_CONSOLE.md` — terminologia de baseline e candidato da
  escolha de filho por pai;
- `docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md` — filho ativo como dado
  semântico fornecido pelo produtor;
- `docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md` — fronteira
  entre carregamento/restauração e persistência;
- `docs/adr/INDICE_ADR.md` — registro da ADR aplicada e do ciclo encerrado;
- `docs/backlog.md` — remoção do `ITEM-0026` encerrado, conforme a convenção
  vigente do backlog.

A forma literal do campo público (`filho_default`) já está fechada por
D-0026-12; a aplicação documental deve usá-la tal como decidida, sem reabrir
alternativas de nome.

Esses documentos pertencem à aplicação documental, não à criação desta ADR.

---

## 10. Itens fora de escopo

- `ITEM-0023` — apresentação de filho ativo em grupos multinível
  (`Pai: filho_ativo`, promoção visual). Delta próprio; não incorporado,
  resolvido nem antecipado por esta ADR.
- `ITEM-0024` — distribuição geométrica de grupos multinível. Delta próprio;
  não incorporado, resolvido nem antecipado por esta ADR.
- Semântica estrutural de pai e filhos, toróides, cursor, geometria e
  formatação dos filhos, paginação de grupos (D-0026-11).
- Sistema genérico de registro/dispatcher de ações do `ITEM-0004`.
- Política global de estilo e qualquer alteração em `config/estilo.json`.
- Nome de função, nome e caminho do script, assinatura interna, algoritmo
  físico de escrita e mecanismo de escrita atômica (D-0026-06, D-0026-09).
- Redação concreta do literal `filho_default` nos contratos e módulos de
  nomenclatura afetados (§9) — a decisão de schema está fechada nesta ADR
  (D-0026-12) e foi materializada pela aplicação documental, preservando
  D-0026-01, D-0026-02 e D-0026-12.
- Handoff, implementação, testes e demonstração são artefatos executivos
  subsequentes; seus resultados pertencem aos respectivos registros do ciclo.

---

## 11. Critérios para aplicação

- [x] A escolha ativa por pai é registrada como dado semântico do JSON externo
  de conteúdo, fornecido explicitamente pelo produtor — nunca no JSON
  estrutural da tela, na configuração global de estilo, no estado de cursor ou
  no renderer.
- [x] Para cada pai sujeito à política há exatamente um filho ativo persistido.
- [x] O campo público que registra essa escolha persistida chama-se
  exatamente `filho_default` em todo documento aplicado — sem uso de
  `filho_ativo`, `filho_ativo_id`, `selecionado`, `selected`, `active` ou
  outro alias (D-0026-12).
- [x] Cada pai possui seu próprio `filho_default`, referenciando um ID de
  filho direto pertencente a esse mesmo pai, sem mapa paralelo global
  pai → filho e sem uso de posição ordinal como identidade persistida
  (D-0026-12).
- [x] A posição do primeiro filho não é tratada como autoridade persistida da
  escolha em nenhum documento aplicado.
- [x] A escolha carregada constitui a baseline; as edições do usuário formam
  candidato separado, sem gravação imediata, sem alteração estrutural e sem
  efeito colateral sobre o cursor.
- [x] `Aplicar` permanece sem efeito quando candidato e baseline são
  equivalentes e inicia a confirmação somente sob divergência.
- [x] A confirmação reutiliza o sistema genérico de pop-up vigente, com os
  resultados canônicos `CONFIRMADO` e `ABORTADO`; nenhum novo sistema de
  pop-up é criado.
- [x] O pop-up não persiste dados, não conhece o JSON externo, não executa o
  script atualizador e não contém lógica de negócio do `ITEM-0026`.
- [x] Após `CONFIRMADO`, a persistência é encaminhada pelo chamador à camada
  responsável pelos dados — não ao renderer nem ao pop-up.
- [x] Após persistência completa e válida: estado gravado vira a nova
  baseline, candidato equalizado, retorno à seleção e `Aplicar` inativo até
  nova divergência.
- [x] Aplicação confirmada anteriormente não é desfeita por edição candidata
  posterior abandonada.
- [x] `ABORTADO` não altera JSON, não executa script para persistir, preserva
  a baseline e o candidato e retorna à seleção.
- [x] Falha de persistência é fail-closed: aplicação não confirmada, baseline
  anterior mantida, persistência parcial nunca tratada como sucesso, candidato
  preservado.
- [x] Em nova carga, o estado ativo é obtido do documento externo persistido,
  sem dependência do runtime da sessão anterior.
- [x] Nenhuma fronteira de D-0026-11 é alterada; `ITEM-0023` e `ITEM-0024` não
  são antecipados.
- [x] Nomes de função, script, caminho, assinatura e algoritmo físico de
  escrita não são fixados pela aplicação documental como decisão desta ADR.
- [x] Nenhuma implementação de código é feita na etapa de ADR.
- [x] Nenhum handoff é criado na etapa de ADR.

---

## 12. Alternativas consideradas

Não há alternativas de desenho a registrar. As decisões D-0026-01 a D-0026-12
constituem decisão já fechada fornecida ao autor documental — D-0026-12
incorporada pelo patch `P02`, em resposta a `QA-APP-0048-001`; este documento
não escolhe entre opções.

---

## 13. Bloqueios

nenhum
