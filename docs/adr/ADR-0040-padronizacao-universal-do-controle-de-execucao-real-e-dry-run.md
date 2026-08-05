---
name: ADR-0040-padronizacao-universal-do-controle-de-execucao-real-e-dry-run
description: "Fecha, para o ITEM-0020, a padronização universal do controle de escolha entre execução real e dry-run: chip específico padronizado e reutilizável [Ins], rótulo dinâmico Real/Simulação (D-DRY-12, substituindo os rótulos Executar/Dry-Run originalmente fixados por D-DRY-02) com destaque por cor_alerta em Simulação, objeto fechado controle_execucao.modo_inicial sem default, autoridade implementacional de categoria e modos aceitos por ação, alcance único por instância de tela, compatibilidade integral das ações de processo, ciclo de vida do modo e transmissão explícita do modo na requisição — preservando o [Ins] Dry-Run focal da ADR-0037 como especialização do Handoff 4 do ITEM-0006, ainda não reconciliada com o padrão universal"
metadata:
  type: adr
  status: aceita
  id: ADR-0040
  data: 2026-08-04
  substitui: null
rastreabilidade:
  decisao_usuario: "D-DRY-01 a D-DRY-11 — controle universal como chip específico padronizado e reutilizável, na faixa de chips específicos, fora da lista de chips canônicos; rótulo dinâmico [Ins] Executar / [Ins] Dry-Run, sempre operável nos dois estados; estado inicial declarado por tela na raiz controle_execucao do tela.json, obrigatoriamente em controle_execucao.modo_inicial, com valores exatamente executar | dry_run e sem default implícito; controle_execucao como objeto fechado, contendo exatamente modo_inicial e rejeitando propriedades internas adicionais; modo único por instância de tela, aplicável a todas as ações de processo compatíveis, não pertencente ao console focado nem ao item corrente, sem variação silenciosa entre ações; compatibilidade autoritativa na implementação registrada da ação, com categoria obrigatória e modos_execucao_aceitos obrigatório para ações de processo; declaração do controle condicionada à compatibilidade integral de todas as ações de processo relevantes da tela com os dois modos, com exceção de ações de navegação/visualização; destaque visual por cor_alerta em dry-run, com o rótulo como indicação primária e a cor como reforço não exclusivo; ciclo de vida iniciado pela configuração declarada, preservado durante a mesma instância de tela inclusive sob suspensão por tela de resultado, e reinicializado a cada nova abertura ou recarga, sem persistência entre instâncias ou sessões; transmissão explícita do modo capturado no acionamento da ação de processo, incluído no lote reconciliado quando aplicável, sem consulta direta do executor ao estado de runtime da interface, sem alteração retroativa de requisições já iniciadas e sem transformar representação interna em protocolo público universal; preserva o [Ins] Dry-Run da ADR-0037 como especialização focal do Handoff 4 do ITEM-0006, ainda não encerrada nem substituída, com reconciliação futura deferida a handoff próprio. D-DRY-10 e D-DRY-11 surgem da auditoria do H-0050."
  rfc_origem: null
  issues_relacionadas:
    - ITEM-0020
    - ITEM-0006
  contratos_afetados:
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_chip.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_registro_acoes.md (artefato futuro preferencial, se necessário)
  handoffs_bloqueados: []
  decisao_posterior:
    id: D-DRY-12
    estado: fechada
    origem: decisao_explicita_do_usuario_apos_validacao_manual_R03_do_H-0050
    resumo: "Reconcilia somente os rótulos visuais do modo corrente do controle universal — [Ins] Executar/[Ins] Dry-Run (D-DRY-02) tornam-se [Ins] Real/[Ins] Simulação — sem alterar valores internos (executar | dry_run), schema, tecla Insert, regra de atividade ou qualquer outra decisão desta ADR."
---

# ADR-0040 — Padronização universal do controle de escolha entre execução real e `dry-run`

## 1. Status

`aceita`

## 2. Contexto

O backlog registra o `ITEM-0020 — Chip de escolha entre execução real e
dry-run`, com a descrição "padronizar genericamente a escolha entre execução
real e dry-run" e o pré-requisito explícito de que "o `[Ins] Dry-Run` da
ADR-0037 é especialização focal do Handoff 4 e não encerra este item". O
próprio item foi originado como um dos quatro itens bloqueados registrados
pela aplicação documental da ADR-0034 (D-SEL-24, item 3: "Chip de escolha
entre execução real e dry-run — permitir escolher na interface o modo da
operação vinculada").

A ADR-0037 (2026-07-29) fechou, como especialização exclusiva do Handoff 4 do
`ITEM-0006`, um toggle focal `[Ins] Dry-Run`: chip de alternância que liga e
desliga `dry-run` na instância de tela criada para esse ciclo, com estado
inicial fixo em execução real, destaque por `cor_alerta` quando ligado, e
regras próprias de origem suspensa e retorno diferenciado. A própria ADR-0037
(D-H4-04) declarou explicitamente que esse toggle "não estabelece o padrão
universal para todas as telas, operações ou ações do sistema" e que o
`ITEM-0020` "permanece ativo, com finalidade a reconciliar futuramente para a
padronização genérica da escolha entre execução real e `dry-run`", exigindo
ADR própria — este documento.

Os contratos ativos de `barra_de_menus`, `chip`, `tela.json` e `console`
registram hoje apenas a instância concreta e focal do `[Ins] Dry-Run` do
Handoff 4 (`contrato_barra_de_menus.md` §23.3; `contrato_chip.md` §9, nota
sobre `[Ins] Dry-Run`), sem fechar: a categoria e a identidade de um controle
reutilizável por qualquer tela que ofereça execução real e `dry-run`; a
obrigação de declaração do estado inicial por tela; a exigência de
compatibilidade integral das ações de processo de uma tela antes que o
controle possa ser declarado; o alcance desse modo dentro de uma instância de
tela; o ciclo de vida do modo entre aberturas, suspensões e recargas; e a
forma de transmissão explícita do modo corrente à execução de uma ação de
processo.

A capacidade universal também exige duas autoridades que não podem ser
deixadas para o handoff ou para a implementação: a configuração de
`controle_execucao` deve ser fechada e deterministicamente validável, e a
implementação registrada de cada ação deve fornecer a autoridade para sua
classificação e para a declaração explícita dos modos aceitos por ações de
processo. Essas lacunas foram identificadas na auditoria do H-0050 e são
fechadas por D-DRY-10 e D-DRY-11.

Este documento registra as decisões já fechadas para essas lacunas, sem
escolher entre alternativas, sem inventar campos, políticas ou autoridades
adicionais, e sem determinar a migração da instância concreta do Handoff 4
para o padrão aqui fechado — essa migração permanece para decisão e handoff
futuros.

---

## 3. Decisão explícita do usuário

### D-DRY-01 — Categoria do controle

O controle universal de escolha entre execução real e `dry-run` é um **chip
específico padronizado e reutilizável**:

- permanece na faixa destinada aos chips específicos da `barra_de_menus`,
  entre `[⏎]` e `[V]`/`[?]` (`contrato_barra_de_menus.md` §7, §16;
  `contrato_chip.md` §7);
- **não integra** a lista de chips canônicos (`contrato_barra_de_menus.md`
  §7, §8; `contrato_chip.md` §7);
- possui identidade, schema e comportamento comuns a todas as telas que
  ofereçam execução real e `dry-run` — não é reinventado por classe de tela;
- substitui, como modelo-alvo, a condição excepcional do `[Ins] Dry-Run`
  focal da ADR-0037 por uma capacidade reutilizável — sem que esta ADR
  execute, por si só, essa substituição na instância concreta já entregue
  (ver seção 6 e seção 10).

O tipo conceitual de chip (`contrato_chip.md` §5) permanece `alternancia`,
como já fixado pela instância focal da ADR-0037; esta ADR não introduz tipo
conceitual novo.

### D-DRY-02 — Rótulo dinâmico

O chip usa a tecla `Insert` e apresenta o modo corrente no próprio rótulo.

Rótulos originalmente fixados por esta decisão, **históricos, substituídos
por D-DRY-12**:

```text
[Ins] Executar   — execução real     (substituído por D-DRY-12)
[Ins] Dry-Run    — simulação          (substituído por D-DRY-12)
```

Rótulos vigentes, fixados por D-DRY-12:

```text
[Ins] Real         — execução real
[Ins] Simulação    — simulação
```

O chip permanece **ativo e operável nos dois estados** — nunca usa
`cor_inativo` e nunca fica ausente enquanto a tela o declarar. A tecla
`Insert`, a alternância entre os dois estados e o caráter dinâmico do
rótulo continuam fixados por esta decisão; apenas o texto apresentado em
cada estado foi substituído por D-DRY-12.

### D-DRY-03 — Estado inicial declarado

Cada tela que ofereça o controle deve **declarar explicitamente** o estado
inicial de abertura, limitado semanticamente a dois valores:

```text
executar
dry_run
```

Não existe default implícito do loader para uma declaração ausente ou
incompleta — configuração sem estado inicial declarado é inválida para
qualquer tela que declare o controle.

Depois da abertura da tela, o modo corrente passa a ser **estado de
runtime** (`docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` §4.5),
não mais configuração concreta.

O estado inicial é declarado na estrutura fechada por D-DRY-09. O objeto
`controle_execucao` na raiz do `tela.json` contém obrigatoriamente
`modo_inicial`; a ausência do objeto significa que a tela não declara o
controle universal. `dry_run_ativo`, pertencente à especialização focal da
ADR-0037, permanece nome de estado de runtime e não é promovido nem
reinterpretado como campo de configuração universal.

### D-DRY-04 — Alcance por tela

Existe **um único modo corrente por instância da tela**. O modo:

- aplica-se a **todas as ações de processo compatíveis** da tela;
- **não pertence** ao console focado — não existe modo independente por
  console (distinto, portanto, do modelo de independência por console já
  fixado para seleção múltipla, ADR-0034 D-SEL-01, e para página,
  ADR-0038 D-PAG-13);
- **não pertence** ao item corrente;
- **não varia silenciosamente** entre ações da mesma tela.

### D-DRY-05 — Compatibilidade integral das ações

Uma tela **somente pode declarar** o controle universal quando **todas** as
suas ações de processo relevantes aceitarem ambos os modos:

- execução real;
- `dry-run`.

Ações de **navegação** ou de **simples visualização** não entram nessa
exigência de compatibilidade integral.

Nenhuma ação de processo compatível pode **ignorar silenciosamente** o modo
global apresentado pelo chip quando acionada.

### D-DRY-06 — Destaque visual

A apresentação do chip é:

| Estado | Rótulo vigente (D-DRY-12) | Aparência |
|---|---|---|
| `executar` | `[Ins] Real` | aparência ativa normal |
| `dry_run` | `[Ins] Simulação` | texto destacado por `cor_alerta` |

Os rótulos `[Ins] Executar`/`[Ins] Dry-Run`, originalmente fixados por
D-DRY-02, são históricos e foram substituídos por `[Ins] Real`/`[Ins]
Simulação` (D-DRY-12); a regra de destaque em si — cor associada ao estado
`dry_run` — não é alterada.

O **rótulo** é a indicação primária do modo corrente. A **cor** é um alerta
adicional — não pode ser a única forma de distinção do modo. Esta regra
reutiliza `cor_alerta` já concretizado no estilo global (ADR-0037 D-H4-03;
`contrato_estilo.md` §3.5) — esta ADR não redefine nem duplica essa
materialização.

### D-DRY-07 — Ciclo de vida

```text
abertura da tela        → aplica o estado inicial declarado na configuração
durante a mesma instância → escolha do usuário permanece, inclusive quando
                             a tela estiver suspensa por uma tela de resultado
nova abertura ou recarga  → reinicializa o modo conforme a configuração
                             declarada
```

O modo **não é persistido** entre instâncias, sessões ou novas aberturas da
mesma tela.

### D-DRY-08 — Transmissão à execução

Quando uma ação de processo compatível é acionada, na ordem:

1. a tela **captura o modo corrente** naquele instante do acionamento;
2. inclui **explicitamente** `executar` ou `dry_run` na requisição da
   operação;
3. em operações baseadas em seleção, **transmite o modo junto ao lote
   reconciliado** (`contrato_console.md` §23.3, §23.6 — lote reconciliado da
   ADR-0034/ADR-0035);
4. o **executor não consulta diretamente** o estado de runtime da interface
   — recebe o modo apenas pela requisição já construída;
5. uma **alteração posterior** do chip não muda o significado de uma
   requisição já iniciada.

### D-DRY-09 — Estrutura declarativa do controle

Uma tela que adote o controle universal declara, na raiz de seu `tela.json`,
o objeto `controle_execucao`. A presença desse objeto identifica que a tela
adota a capacidade universal de escolha entre execução real e `dry-run`.

O objeto contém obrigatoriamente o campo `modo_inicial`, que aceita
exatamente os valores:

- `executar`;
- `dry_run`.

Não existe default implícito para `modo_inicial`. O objeto ausente significa
que a tela não declara o controle universal. O objeto guarda somente a
configuração concreta inicial; o modo corrente após a abertura continua sendo
estado de runtime e não é persistido de volta no `tela.json`.

`dry_run_ativo`, pertencente à especialização focal da ADR-0037, não é
promovido nem reinterpretado como campo da configuração universal. Nenhum
outro campo interno de `controle_execucao` é autorizado por esta ADR.

Forma normativa:

```json
{
  "controle_execucao": {
    "modo_inicial": "executar"
  }
}
```

Exemplo alternativo válido:

```json
{
  "controle_execucao": {
    "modo_inicial": "dry_run"
  }
}
```

### D-DRY-10 — Objeto fechado

`controle_execucao` é um objeto fechado. Quando presente, contém exatamente
o campo obrigatório `modo_inicial`, cujos únicos valores permitidos continuam
sendo `executar` e `dry_run`.

Qualquer propriedade interna adicional torna a configuração inválida. Não
existe default implícito, e a ausência do objeto continua significando não
adoção da capacidade. Extensões futuras exigem nova decisão material e
atualização contratual explícita. O fechamento equivale semanticamente a
propriedades adicionais desautorizadas, independentemente da tecnologia de
validação utilizada; esta decisão não autoriza criar JSON Schema ou
mecanismo novo específico nesta etapa.

### D-DRY-11 — Registro autoritativo das ações

A compatibilidade com os modos universais pertence à implementação registrada
da ação. Cada ação registrada declara obrigatoriamente:

```yaml
categoria: processo | navegacao | visualizacao
```

Toda ação de categoria `processo` declara também:

```yaml
modos_execucao_aceitos:
  - executar
  - dry_run
```

`categoria` é metadado obrigatório e seus únicos valores são `processo`,
`navegacao` e `visualizacao`. `modos_execucao_aceitos` é obrigatório para
ações de `processo` e seus valores pertencem ao conjunto fechado `executar`,
`dry_run`. Uma tela que declara `controle_execucao` somente é válida quando
todas as suas ações relevantes classificadas como `processo` aceitam
explicitamente os dois modos. Ações de `navegacao` e `visualizacao` ficam
fora dessa exigência.

Ação ausente do registro, sem categoria, com categoria desconhecida ou ação
de processo sem declaração suficiente falha de forma fechada. A tela não
declara nem pode falsificar a compatibilidade da implementação, que não pode
ser inferida por identificador, nome, rótulo, texto, caminho de script, flag
de CLI, adaptador ou comportamento observado. A localização física e a
estrutura interna reversível do registro podem ser definidas pela
implementação, mas sua semântica deve obedecer a este contrato. Não é
autorizado criar campo de compatibilidade no `tela.json` nem compatibilidade
específica apenas para a demonstração H-0050 e apresentá-la como solução
universal.

### D-DRY-12 — Reconciliação dos rótulos visuais do modo corrente

Decisão fechada, posterior ao encerramento de D-DRY-01 a D-DRY-11, originada
de decisão explícita do usuário após a validação manual R03 do `H-0050`
(status `MANUAL_VALIDATION_APPROVED`, 7 de 7 critérios conformes, nenhum
achado aberto).

O chip específico do controle universal continua indicando o **modo
corrente** (`executar` | `dry_run`), sem alteração de tecla, de tipo
conceitual, de condição de existência ou de regra de atividade. Alteram-se
somente os **rótulos visuais** apresentados pelo chip:

```yaml
rotulos_visuais:
  executar: Real
  dry_run: Simulação

apresentacao:
  modo_executar: "[Ins] Real"
  modo_dry_run: "[Ins] Simulação"
```

**Justificativa — distinção entre modo e ação.** O rótulo anterior
`[Ins] Executar`, fixado por D-DRY-02, colidia lexicalmente com o chip de
ação `[⏎] Executar`, que inicia o processamento do lote atual. A colisão
textual confundia dois conceitos distintos:

```text
[⏎] Executar
→ ação que inicia o processamento do lote atual

[Ins] Real / [Ins] Simulação
→ modo em que a futura execução ocorrerá
```

D-DRY-12 substitui **somente** os rótulos visuais fixados por D-DRY-02. Não
revoga a existência dos dois modos, não altera os identificadores internos
`executar` e `dry_run`, não altera a tecla `Insert`, não altera a regra de
atividade do chip nos dois estados, e não altera D-DRY-03 a D-DRY-11.

**Aparência:**

```yaml
aparencia:
  Real:
    modo_interno: executar
    tratamento: aparencia_ativa_normal

  Simulação:
    modo_interno: dry_run
    tratamento: cor_alerta
```

`Simulação` nunca usa `cor_inativo`. Os dois estados continuam ativos e
alternáveis por `Insert`.

**Preservações obrigatórias.** D-DRY-12 altera somente a apresentação
visual do controle. Permanecem integralmente preservados: a tecla `Insert`;
o chip específico e não canônico (D-DRY-01); os valores internos `executar`
e `dry_run`; a configuração `controle_execucao.modo_inicial` com esses
mesmos valores (D-DRY-03, D-DRY-09, D-DRY-10); o estado vivo de runtime
(D-DRY-03, D-DRY-07); o registro autoritativo das ações e suas categorias
(D-DRY-11); os modos de execução aceitos; a elegibilidade da tela para
declarar o controle (D-DRY-05); a captura privada da requisição e a
semântica de execução real e de `dry-run` (D-DRY-08); o ciclo de vida por
instância (D-DRY-07); a ausência de persistência (D-DRY-07, D-DRY-09); a
posição do chip na barra (D-DRY-01); o chip ativo nos dois modos (D-DRY-02);
a especialização focal do H-0044 (ADR-0037, seção 6); o chip `[⏎] Todos`; e
o chip `[⏎] Executar`.

**Fronteiras negativas.** D-DRY-12 não autoriza: renomear o valor interno
`executar` para `real`; renomear o valor interno `dry_run` para `simulacao`;
alterar o schema do `tela.json`; criar aliases de configuração; alterar o
contrato do registro de ações; alterar o modo capturado na requisição;
alterar o resultado produzido pelo executor; substituir o termo técnico
`dry-run` em documentação conceitual; alterar `[⏎] Executar`; alterar o
H-0044; criar novo chip; alterar a tecla `Insert`; ou modificar código
nesta decisão.

**Verificação terminológica.** Permanecem distintos: `executar` (valor
interno do modo); `dry_run` (valor interno do modo); `Real` (rótulo visual
do modo `executar`); `Simulação` (rótulo visual do modo `dry_run`);
`Executar` (ação do chip `[⏎]`). `Real` e `Simulação` não se tornam novos
valores de schema.

**Aplicação futura.** A aplicação documental posterior a D-DRY-12 deverá
identificar nominalmente os documentos afetados. A implementação posterior
deverá alterar somente a apresentação e suas provas, incluindo, quando
aplicável: barra de menus; configurações demonstrativas; testes de
renderização; testes da demonstração; roteiro de validação manual; e textos
de documentação que tratem dos rótulos visuais atuais. Essa aplicação e
implementação devem provar: `[Ins] Real` quando o estado interno é
`executar`; `[Ins] Simulação` quando o estado interno é `dry_run`; que
`Insert` alterna entre os dois rótulos; que `Simulação` usa `cor_alerta`;
que `Real` usa aparência ativa normal; que `[⏎] Executar` permanece
inalterado; que os valores internos continuam `executar` e `dry_run`; que
nenhuma configuração ou requisição passa a usar `real` ou `simulacao`; e
que o H-0044 permanece sem alteração.

### Clarificação preservada de D-DRY-08

O modo deve ser transmitido explicitamente na requisição. Esta ADR fixa a
obrigação semântica, mas não transforma uma representação interna específica,
como `{ids, modo}`, em protocolo público universal por si só.

A implementação pode escolher estrutura interna reversível quando o valor
for explícito, sua captura for imutável para a requisição iniciada, o executor
não consultar a interface, o modo não compuser a identidade do lote e nenhum
protocolo público vigente for alterado silenciosamente.

### Separação entre configuração concreta e estado de runtime

Esta ADR mantém, sem exceção, a distinção já fixada por
`docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` §4.5 e por
`contrato_tela_json.md` §6:

| Camada | Conteúdo | Onde vive |
|---|---|---|
| Configuração concreta | estado inicial declarado (`executar` \| `dry_run`) por tela (D-DRY-03) | `tela.json` da instância declarante |
| Estado de runtime | modo corrente durante a sessão, capturado a cada acionamento (D-DRY-07, D-DRY-08) | execução da tela aberta |

O `tela.json` nunca guarda o modo corrente como estado vivo; apenas o estado
inicial declarado é configuração.

---

## 4. Decisão

Fica adotado, para o `ITEM-0020`, o padrão universal de escolha entre
execução real e `dry-run` descrito em D-DRY-01 a D-DRY-12: um chip específico
padronizado e reutilizável, identificado pela tecla `Insert`, com rótulo
dinâmico `[Ins] Real`/`[Ins] Simulação` (D-DRY-12 — substitui os rótulos
`[Ins] Executar`/`[Ins] Dry-Run` originalmente fixados por D-DRY-02) sempre
operável, destacado por `cor_alerta` exclusivamente quando em `dry-run`
(rótulo `Simulação`); uma tela que adote o
controle declara na raiz do `tela.json` o objeto fechado
`controle_execucao`, contendo exatamente o campo obrigatório `modo_inicial`,
que aceita somente `executar` ou `dry_run`, sem default implícito e com
rejeição de propriedades internas adicionais; a implementação registrada de
cada ação fornece metadado obrigatório `categoria`, limitado a `processo`,
`navegacao` e `visualizacao`, e toda ação de `processo` fornece
`modos_execucao_aceitos`, limitado a `executar` e `dry_run`; um único modo por
instância de tela, aplicável a todas as ações de processo compatíveis e
condicionado à compatibilidade integral dessas ações com os dois modos,
excluídas navegação e visualização; ciclo de vida iniciado pela configuração
declarada, preservado durante a mesma instância — inclusive sob suspensão
por tela de resultado — e reinicializado a cada nova abertura ou recarga; e
transmissão explícita do modo capturado no acionamento, incorporada à
requisição e ao lote reconciliado quando aplicável, sem consulta direta do
executor ao estado de runtime da interface e sem transformar uma
representação interna reversível em protocolo público universal. A ausência
de `controle_execucao` significa que a tela não declara o controle, a tela
não declara nem falsifica a compatibilidade e o modo corrente não é
persistido de volta no `tela.json`. Ausência ou insuficiência da autoridade
registrada para qualquer ação de processo relevante produz falha fechada.

D-DRY-12 reconcilia exclusivamente os rótulos visuais desse controle: o modo
`executar` passa a ser apresentado como `[Ins] Real` e o modo `dry_run` como
`[Ins] Simulação`, substituindo os rótulos `[Ins] Executar`/`[Ins] Dry-Run`
originalmente fixados por D-DRY-02 — sem alterar valores internos, schema de
`controle_execucao`, tecla, regra de atividade, registro de ações ou
qualquer outra decisão desta ADR.

Esta decisão fixa o **padrão-alvo** para telas que venham a adotar o
controle universal. Ela não redefine, não substitui e não migra a instância
concreta do `[Ins] Dry-Run` focal já entregue pela ADR-0037 e pelo H-0044
para o Handoff 4 do `ITEM-0006` — essa reconciliação permanece decisão e
handoff futuros, conforme seção 6.

---

## 5. Consequências

### Positivas

- Fecha, para o `ITEM-0020`, a lacuna de padronização genérica que a
  ADR-0037 explicitamente deixou aberta (D-H4-04), permitindo que telas
  futuras adotem um controle único de execução real/`dry-run` sem repetir
  desenho ad hoc por tela.
- Formaliza a exigência de compatibilidade integral das ações de processo
  antes de uma tela declarar o controle, evitando telas em que o chip global
  seja ignorado silenciosamente por alguma ação.
- Fixa a transmissão explícita do modo na requisição como regra universal,
  evitando que executores futuros dependam de consulta direta ao estado de
  runtime da interface.
- Preserva integralmente o `[Ins] Dry-Run` focal da ADR-0037 e a
  responsabilidade dela sobre preservação e restauração da origem no fluxo
  focal, evitando reabertura de decisões já fechadas e testadas pelo H-0044.
- Reduz o risco de divergência estrutural ao fixar uma estrutura declarativa
  nominal e fechada para o schema universal: `controle_execucao` com
  `modo_inicial`.
- Mantém telas sem `controle_execucao` fora da capacidade universal e exige
  que telas com o objeto declarem `modo_inicial` com um dos dois valores
  permitidos.
- Mantém o estado vivo fora da configuração: o modo corrente permanece em
  runtime e não retorna ao `tela.json`.
- Fecha `controle_execucao` como objeto de exatamente um campo e torna
  rejeição de propriedades adicionais uma regra normativa, evitando
  extensões sem semântica ou ignorância silenciosa.
- Coloca a autoridade de compatibilidade no registro da implementação da
  ação, com classificação e modos aceitos verificáveis, sem permitir que a
  tela declare capacidade inexistente.
- Elimina, por D-DRY-12, a colisão lexical entre o rótulo do modo corrente
  (`[Ins] Executar`) e o chip de ação `[⏎] Executar`, substituindo os
  rótulos do modo por `Real`/`Simulação` sem alterar valores internos,
  schema, tecla ou regra de destaque.

### Custos e restrições

- Exige que toda tela candidata ao controle universal seja auditada quanto à
  compatibilidade integral de suas ações de processo antes de declarar o
  chip — telas com qualquer ação incompatível não podem adotar o controle
  sem antes resolver essa incompatibilidade.
- Mantém, até reconciliação futura, duas superfícies distintas de
  `dry-run`/execução real no sistema: o `[Ins] Dry-Run` focal do Handoff 4
  (ADR-0037) e o padrão universal aqui fechado — exigindo cuidado
  documental para não confundir as duas enquanto coexistirem.
- Exige que a transmissão explícita do modo (D-DRY-08) seja replicada em
  todo binding futuro que consuma o controle universal, ampliando a
  superfície de validação de requisições de operação.
- Futuras extensões de `controle_execucao` exigirão nova decisão material e
  atualização contratual explícita.
- A aplicação deverá criar ou atualizar a autoridade contratual do registro
  de ações; ações existentes poderão precisar de classificação documental e
  implementacional antes de serem usadas por telas com o controle.
- A capacidade universal não pode ser comprovada apenas por uma associação
  focal da demonstração H-0050.
- A representação física da requisição permanece detalhe interno reversível,
  salvo quando integrar contrato público vigente.
- Exige que toda documentação, configuração demonstrativa, teste de
  renderização, teste da demonstração e roteiro de validação manual que
  mencionem os rótulos `[Ins] Executar`/`[Ins] Dry-Run` sejam atualizados
  para `[Ins] Real`/`[Ins] Simulação` (D-DRY-12), preservando os valores
  internos `executar` e `dry_run`.

### Artefatos afetados

| Artefato | Aplicação necessária |
|---|---|
| `docs/contratos/contrato_tela_json.md` | Registrar nominalmente o objeto raiz `controle_execucao` e o campo `controle_execucao.modo_inicial`; registrar a obrigatoriedade condicional do campo quando o objeto estiver presente, a enumeração fechada (`executar` \| `dry_run`) e a ausência de default; registrar a exigência de compatibilidade integral das ações de processo (D-DRY-05) como pré-condição de validação. |
| `docs/contratos/contrato_barra_de_menus.md` | Registrar o chip `[Ins] Real`/`[Ins] Simulação` (D-DRY-12) como instância padronizada de chip específico reutilizável, distinta da instância focal do Handoff 4 já registrada em §23.3; propagar rótulo dinâmico e regra de destaque por `cor_alerta` (D-DRY-02, D-DRY-06, D-DRY-12), identificando os rótulos `[Ins] Executar`/`[Ins] Dry-Run` como histórico substituído. |
| `docs/contratos/contrato_chip.md` | Registrar o controle universal como chip específico padronizado de tipo `alternancia`, com regras de existência condicionadas à compatibilidade integral das ações da tela (D-DRY-05) e regra de ativo/inativo que nunca usa `cor_inativo` (D-DRY-02). |
| `docs/contratos/contrato_console.md` | Registrar a transmissão explícita do modo corrente ao lote reconciliado (D-DRY-08) como extensão da entrada da operação consumidora já fechada por §23.6, sem alterar D-SEL-01 a D-SEL-11. |
| Contratos vigentes de ações, execução, console ou runtime que forem semanticamente proprietários | Propagar a autoridade de `categoria` e `modos_execucao_aceitos` conforme o contrato já proprietário; se nenhuma autoridade vigente for suficiente, elaborar contrato focal próprio. |
| `docs/contratos/contrato_registro_acoes.md` (artefato futuro preferencial) | Materializar a autoridade física reutilizável de D-DRY-11, caso nenhum contrato vigente seja suficiente; o nome é organização reversível e a semântica é obrigatória independentemente do arquivo. Não criar ou alterar este contrato durante este patch. |
| `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` | Avaliar necessidade de termo próprio para o controle universal, distinto do termo já registrado para `[Ins] Dry-Run` focal (§4.4.1). |
| `docs/nomenclatura/32_CONSOLE.md` | Avaliar necessidade de termo para o alcance único do modo por instância de tela (D-DRY-04), preservando a distinção já registrada para seleção múltipla e página independentes por console. |
| `docs/adr/INDICE_ADR.md` | Registrar a ADR-0040 após QA favorável. |
| `docs/backlog.md` | Atualizar o estado do `ITEM-0020` quando o fluxo documental determinar mudança material. |
| `docs/handoff/H-0050-controle-universal-execucao-real-dry-run.md` | Aplicar a ADR e corrigir o handoff somente após esta ADR ser aplicada documentalmente e submetida a QA. |

#### Escopo de aplicação de D-DRY-12

A aplicação documental posterior deverá identificar nominalmente os
documentos afetados pela reconciliação de rótulos de D-DRY-12. A
implementação posterior deverá alterar somente a apresentação e suas
provas, restrita às camadas abaixo, quando aplicável, sem tocar valores
internos, schema, tecla ou semântica de execução:

- barra de menus;
- configurações demonstrativas;
- testes de renderização;
- testes da demonstração;
- roteiro de validação manual;
- textos de documentação que tratem dos rótulos visuais atuais do controle
  universal.

---

## 6. Compatibilidade e transição

Esta ADR não executa aplicação documental, alteração de contrato, alteração
de nomenclatura, criação de handoff, implementação ou validação manual —
apenas registra a decisão fechada do padrão universal. Até a aplicação, os
contratos e módulos de nomenclatura listados na seção 5 permanecem no estado
atual.

Esta ADR preserva integralmente:

- o `[Ins] Dry-Run` da ADR-0037 como especialização focal necessária ao
  Handoff 4 do `ITEM-0006` — instância concreta, testada e implementada pelo
  H-0044, que **não é alterada** por este documento;
- a autoridade da ADR-0037 sobre preservação e restauração da origem
  suspensa no fluxo focal (D-H4-07 a D-H4-10) — esta ADR **não a substitui**
  nessas responsabilidades;
- `cor_alerta` já concretizado no estilo global pela ADR-0037 (D-H4-03) —
  reutilizado, não redefinido;
- D-SEL-01 a D-SEL-11 (ADR-0034) e a fronteira do lote reconciliado
  (`contrato_console.md` §23.6) — a transmissão explícita do modo (D-DRY-08)
  é aditiva a essa entrada, não a substitui.

A especialização focal da ADR-0037 **não encerrou** o `ITEM-0020`. A
capacidade existente do `[Ins] Dry-Run` deverá ser **reconciliada
futuramente** com o padrão universal aqui fechado, em decisão e handoff
próprios. Esta ADR não decide o escopo, os arquivos, a estratégia ou os
critérios de aceite dessa reconciliação futura.

Nenhuma migração da instância concreta do Handoff 4 é executada, autorizada
ou implicitamente aprovada por esta ADR.

D-DRY-12 fecha a reconciliação dos rótulos visuais do controle universal,
mas não executa, por si só, a aplicação documental aos contratos, à
nomenclatura, às configurações demonstrativas, aos testes de renderização,
aos testes da demonstração ou ao roteiro de validação manual do `H-0050`
(seção 5, "Escopo de aplicação de D-DRY-12"). Até essa aplicação, os
artefatos afetados permanecem, para fins de leitura literal, com os
rótulos `[Ins] Executar`/`[Ins] Dry-Run` fixados originalmente por D-DRY-02,
que passam a ser considerados histórico substituído a partir desta decisão.

## 7. Alternativas consideradas

| Alternativa | Motivo para rejeitar ou adiar |
|---|---|
| D-DRY-01 a D-DRY-08 recebidas já fechadas | A autoria da ADR recebeu essas decisões já fechadas; não houve escolha de alternativa durante a etapa `CRIAR_ADR`. |
| Objeto aberto | Rejeitado porque permitiria campos sem semântica e ignorância silenciosa; `controle_execucao` é fechado por D-DRY-10. |
| Compatibilidade declarada no `tela.json` | Rejeitada porque a tela poderia afirmar capacidade inexistente; a autoridade pertence ao registro da implementação da ação. |
| Compatibilidade implícita pelo adaptador | Rejeitada por acoplamento e inferência implementacional; a aceitação deve ser metadado autoritativo registrado. |
| Metadados no registro da ação | Escolhida por manter a autoridade junto à implementação consumidora, com classificação e modos aceitos verificáveis. |
| Opções anteriores da especificação | Não são reconstituídas como autoridade normativa neste documento. |

## 8. Itens fora de escopo

- Transformar o controle em chip canônico.
- Permitir tecla ou rótulo escolhidos livremente por cada tela.
- Modo independente por console.
- Modo independente por ação.
- Persistência do modo entre telas, instâncias ou sessões.
- Ação incompatível ignorar o modo corrente.
- Registro e despacho genéricos de ações do `ITEM-0004`.
- Abertura e retorno genéricos entre telas do `ITEM-0005`.
- Binding definitivo com o Pipeline.
- Alteração das regras de seleção, lote, paginação ou foco (ADR-0031,
  ADR-0034, ADR-0038).
- Modos de visualização do `ITEM-0021`.
- Migração ou alteração da instância concreta do `[Ins] Dry-Run` do Handoff 4
  (ADR-0037, H-0044) — permanece decisão e handoff futuros.
- Autorizar extensões internas de `controle_execucao` nesta etapa — o objeto
  é fechado e qualquer extensão futura exige nova decisão material.
- Escolher arquitetura centralizada ou distribuída para o registro de ações.
- Migrar todas as ações existentes ou reconciliar o H-0044.
- Escolher classe, `dataclass`, dicionário ou estrutura interna da requisição.
- Definir protocolo público novo.
- Implementar loader, registry, dispatcher, executor ou demonstração.
- Corrigir o H-0050 antes da aplicação documental desta ADR.
- Criar ou alterar o contrato focal do registro de ações durante este patch.
- Implementação de código nesta etapa.
- QA, aplicação documental, handoff, testes e Git de escrita — fora desta
  execução.

## 9. Critérios para aplicação

- [ ] `docs/contratos/contrato_tela_json.md`, `docs/contratos/contrato_barra_de_menus.md`,
  `docs/contratos/contrato_chip.md` e `docs/contratos/contrato_console.md`
  foram atualizados conforme a tabela de artefatos afetados (seção 5).
- [ ] O contrato da tela materializou nominalmente o objeto raiz
  `controle_execucao` e o campo `controle_execucao.modo_inicial`.
- [ ] O contrato confirma que `modo_inicial` é obrigatório quando
  `controle_execucao` está presente e aceita exatamente `executar` ou
  `dry_run`.
- [ ] O contrato não estabelece default implícito para `modo_inicial`.
- [ ] A ausência de `controle_execucao` é interpretada como não adoção do
  controle universal.
- [ ] O modo corrente permanece como estado de runtime e não é persistido no
  `tela.json`.
- [ ] Somente os módulos proprietários da nomenclatura efetivamente afetados
  (`31`, `32`) foram avaliados e, quando material, atualizados.
- [ ] A instância concreta do `[Ins] Dry-Run` do Handoff 4 (ADR-0037,
  H-0044) permaneceu inalterada por esta aplicação.
- [ ] `docs/adr/INDICE_ADR.md` foi atualizado somente após QA favorável desta
  ADR.
- [ ] `docs/backlog.md` foi atualizado somente quando o fluxo documental
  determinar mudança material do `ITEM-0020`.
- [ ] Nenhuma implementação de código foi feita durante a aplicação
  documental.
- [ ] Nenhum handoff foi criado na mesma etapa da aplicação documental.
- [ ] Caminhos permanecem relativos à raiz do Orquestrador.
- [ ] A execução de aplicação produziu relatório próprio em
  `docs/relatorios/`.
- [ ] O relatório de aplicação não sobrescreveu relatório de execução
  anterior.
- [ ] A aplicação foi submetida a QA independente.
- [ ] `controle_execucao` é fechado e contém exatamente `modo_inicial` quando
  presente.
- [ ] Propriedades internas adicionais de `controle_execucao` são rejeitadas.
- [ ] O contrato do registro de ações define `categoria` como metadado
  obrigatório.
- [ ] O contrato do registro define `modos_execucao_aceitos` para ações de
  `processo`.
- [ ] Categorias e modos de execução formam enumerações fechadas.
- [ ] A tela não declara nem falsifica compatibilidade no `tela.json`.
- [ ] Toda ação de processo de uma tela adotante aceita explicitamente os dois
  modos.
- [ ] Ações de navegação e visualização ficam fora dessa exigência.
- [ ] Ausência ou insuficiência do registro produz falha fechada.
- [ ] Nenhum detalhe interno da requisição é apresentado indevidamente como
  protocolo público.
- [ ] D-DRY-01 a D-DRY-11 permanecem preservadas materialmente.
- [ ] D-DRY-12 está registrada como decisão fechada, distinta de D-DRY-01 a
  D-DRY-11.
- [ ] `[Ins] Real` é apresentado quando o estado interno do modo é
  `executar`.
- [ ] `[Ins] Simulação` é apresentado quando o estado interno do modo é
  `dry_run`.
- [ ] A tecla `Insert` continua alternando entre os dois rótulos vigentes.
- [ ] O rótulo `Simulação` mantém destaque por `cor_alerta`; o rótulo `Real`
  mantém aparência ativa normal.
- [ ] `[⏎] Executar` permanece inalterado.
- [ ] Os valores internos do modo permanecem exatamente `executar` e
  `dry_run`; nenhuma configuração ou requisição passou a usar `real` ou
  `simulacao`.
- [ ] O H-0044 permanece sem alteração em decorrência de D-DRY-12.
- [ ] Os rótulos `[Ins] Executar`/`[Ins] Dry-Run` aparecem, quando
  mencionados, somente como referência histórica explicitamente
  identificada como substituída por D-DRY-12.
- [ ] A aplicação documental de D-DRY-12 identificou nominalmente os
  documentos afetados, restrita a: barra de menus; configurações
  demonstrativas; testes de renderização; testes da demonstração; roteiro
  de validação manual; e textos de documentação sobre os rótulos visuais.

## 10. Relação com a ADR-0037 e com o `ITEM-0006`

Esta ADR fecha, para o `ITEM-0020`, o padrão universal cuja necessidade foi
explicitamente registrada pela ADR-0037 (D-H4-04) e pelo backlog
(pré-requisito do `ITEM-0020`). Ela não reabre D-H4-01 a D-H4-10, não altera
o comportamento entregue pelo H-0044, e não determina, por si só, quando ou
como a instância focal será migrada para o padrão aqui fechado.

Para o `ITEM-0006`, esta ADR não produz nenhum efeito — o item permanece
concluído nos termos já registrados pela ADR-0034, ADR-0035, ADR-0036 e
ADR-0037.

Para o `ITEM-0020`, esta ADR fecha a especificação do padrão universal. A
reconciliação da instância focal do Handoff 4 com esse padrão, quando
decidida, exigirá especificação e handoff próprios. Esta ADR não decide o
escopo, os arquivos, a estratégia ou os critérios de aceite dessa
reconciliação — ela não é antecipada nem autorizada por este documento.

## 11. Bloqueios

nenhum
