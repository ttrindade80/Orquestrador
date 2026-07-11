---
name: ADR-0017-redimensionamento-reativo-tui
description: Política de redimensionamento reativo da janela do terminal durante sessão TUI — detecção por SIGWINCH, cadeia de obtenção de dimensões por ioctl/TIOCGWINSZ, validação de par largura/altura, conservação das últimas dimensões válidas, redesenho após redução e ampliação, e quadro mínimo de aviso para terminal pequeno demais
metadata:
  type: adr
  status: aceita
  data: 2026-07-11
  substitui: null
rastreabilidade:
  rfc_origem: null
  issues_relacionadas: []
  contratos_afetados:
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/NOMENCLATURA.md
    - docs/adr/INDICE_ADR.md
  handoffs_bloqueados: []
---

# ADR-0017 — Redimensionamento reativo da TUI

## Status

`aceita`

## Data

2026-07-11

## Contexto

A ADR-0016 estabeleceu a política completa de sessão TUI em tela cheia: alternate
screen, modo `cbreak`, posicionamento absoluto linha a linha, escrita atômica por
quadro, synchronized output e restauração de terminal em `finally`. Ela excluiu
expressamente o redimensionamento reativo da janela de seu escopo e registrou o
tratamento por `SIGWINCH` como pendência de ciclo futuro — sem reservar número de
handoff.

A ADR-0013 normatizou que o renderer deve tratar `altura_disponivel` como dimensão
explícita do render, complementando a largura já dinâmica. Essa ADR deixou a
propagação da altura para handoff futuro, mas fixou a obrigação de ocupar a área
vertical disponível.

Durante a sessão TUI, qualquer alteração de tamanho da janela do terminal produz um
estado incorreto: as dimensões usadas pela TUI permanecem as do momento de
inicialização. O quadro anterior, calculado para outras dimensões, fica visível ou
incompleto. O sistema precisa de um mecanismo para detectar a mudança, obter as
novas dimensões de forma confiável e redesenhar o quadro usando os valores atualizados.

Esta ADR fecha esse gap normativo. Ela não implementa código, não altera contratos
nem cria handoff — define exclusivamente a política que o ciclo de implementação
subsequente deve seguir.

## Problema

Sem política de redimensionamento reativo:

1. **Dimensões obsoletas:** o renderer continua usando largura e altura da
   inicialização após redimensionamento; linhas calculadas para o tamanho antigo
   podem ultrapassar ou não preencher o terminal atual.
2. **Resíduos visuais:** partes do quadro anterior ficam visíveis quando a janela
   encolhe (conteúdo fora da área nova) ou quando a janela cresce (espaço não
   preenchido).
3. **Scroll acidental:** escrita além da última linha da janela menor produz scroll
   indesejado, violando a política de alternate screen da ADR-0016.
4. **Dimensões inválidas como fonte única:** chamar apenas `shutil.get_terminal_size()`
   em tempo de render não constitui mecanismo normativo suficiente para o ciclo
   reativo, pois não fornece garantias de atomicidade do par largura/altura nem
   cadeia de fallback normativa.

## Decisão

As declarações abaixo constituem a política normativa desta ADR.

### 1. Gerenciamento próprio; sem biblioteca de TUI

O redimensionamento reativo será gerenciado pelo próprio sistema, sem uso de
`ncurses`, `curses`, `textual` ou `rich`. Nenhuma dependência de biblioteca de TUI
pode ser introduzida para prover essa capacidade.

### 2. Gatilho de redimensionamento

Em sessão TTY ativa, a alteração do tamanho da janela será detectada por `SIGWINCH`.
O recebimento do sinal deve provocar a atualização das dimensões usadas pela TUI e o
redesenho correspondente.

O detalhe de onde o trabalho é executado — se diretamente dentro do manipulador de
sinal ou diferido para o loop principal — não é normativo por esta ADR, desde que o
resultado obrigatório descrito nos itens seguintes seja respeitado. O handoff de
implementação é responsável por essa decisão técnica.

### 3. Fonte primária das dimensões

A fonte primária de largura e altura durante a sessão TTY é:

```text
ioctl(fd, TIOCGWINSZ, ...)
```

O resultado do `ioctl` prevalece quando largura e altura forem válidas e maiores
que zero (conforme a definição de validade do item 4).

As duas dimensões devem ser tratadas como um único estado coerente de janela. É
proibido usar largura de uma fonte e altura de outra na mesma atualização.

### 4. Validade das dimensões

Um par de dimensões somente é válido quando todas as condições abaixo forem
satisfeitas simultaneamente:

- largura e altura estão presentes;
- ambas podem ser interpretadas como inteiros;
- largura é maior que zero;
- altura é maior que zero.

Dimensões ausentes, inválidas ou zeradas não podem ser aplicadas ao renderer.

### 5. Cadeia de obtenção na inicialização

Na inicialização da aplicação TTY, usar a seguinte precedência:

```text
ioctl(TIOCGWINSZ)
→ LINES e COLUMNS
→ fallback fixo (80, 24)
```

`LINES` e `COLUMNS` somente são aceitas quando ambas formarem um par válido
conforme o item 4.

Variáveis de ambiente nunca prevalecem sobre um resultado válido do `ioctl`.

O fallback fixo normativo é:

```text
largura = 80
altura = 24
```

### 6. Cadeia de obtenção após SIGWINCH

Durante a sessão TTY, após o recebimento de `SIGWINCH`, usar a seguinte
precedência:

```text
ioctl(TIOCGWINSZ)
→ LINES e COLUMNS
→ últimas dimensões válidas
```

Se `ioctl` falhar ou retornar dimensões inválidas, consultar `LINES` e `COLUMNS`.
`LINES` e `COLUMNS` somente são aceitas quando ambas formarem um par válido.

Se também as variáveis não formarem um par válido:

- conservar as últimas dimensões válidas;
- não aplicar dimensões inválidas;
- não redesenhar como se o tamanho tivesse mudado;
- aguardar uma futura atualização válida.

O fallback fixo `(80, 24)` é usado exclusivamente para estabelecer o estado inicial
quando nenhuma fonte fornece dimensões válidas. Ele não substitui automaticamente as
últimas dimensões válidas durante uma sessão já iniciada.

### 7. Redesenho após atualização válida

Quando for obtido um novo par válido de dimensões:

- atualizar largura e altura da sessão;
- recalcular integralmente a tela;
- recalcular as áreas de cabeçalho, corpo, dashboard, console, lancador e
  barra_de_menus que forem aplicáveis;
- recalcular paginação e distribuição dependentes do espaço disponível;
- redesenhar o quadro usando as novas dimensões.

O redimensionamento não altera decisões declarativas de composição. Em especial:

- não modificar `corpo.arranjo`;
- não modificar o `tiling` escolhido pelo usuário;
- não inventar ou remover chips;
- não transformar automaticamente uma composição declarada em outra.

Somente os cálculos visuais já autorizados e dependentes da dimensão real podem
ser refeitos.

### 8. Comportamento em redução e ampliação

A política se aplica tanto quando a janela for reduzida quanto quando for ampliada.

Depois de cada atualização válida:

- nenhuma parte residual do quadro anterior pode permanecer visível;
- não pode haver scroll acidental;
- o redesenho não pode acrescentar linhas fora da área atual;
- o quadro não pode continuar usando largura ou altura antigas;
- o conteúdo deve ser novamente calculado, não apenas recortado superficialmente.

### 9. Terminal pequeno demais

Quando as dimensões atuais forem válidas, mas insuficientes para representar a
tela normal, a aplicação não deve:

- encerrar a sessão TUI;
- propagar `RenderizadorErro` como encerramento normal;
- conservar na tela um quadro antigo incompatível com o novo tamanho;
- tentar desenhar além da área disponível.

Deve exibir um quadro mínimo de aviso equivalente a:

```text
terminal pequeno demais
```

A formulação textual final pode ser adequada à largura disponível, mas deve
preservar inequivocamente esse significado.

O quadro mínimo:

- deve caber estritamente nas dimensões atuais;
- não pode gerar scroll;
- não pode escrever linha adicional;
- não pode deixar resíduos do quadro anterior;
- deve continuar respeitando alternate screen, autowrap desativado e a política de
  escrita da sessão estabelecida pela ADR-0016;
- deve ser substituído automaticamente pela tela normal assim que uma atualização
  posterior fornecer dimensões suficientes.

Não é exigida ação do usuário para sair do modo de aviso.

### 10. Preservações da ADR-0016

Esta ADR complementa a ADR-0016. As seguintes políticas da ADR-0016 permanecem
integralmente vigentes e não podem ser revertidas sob pretexto de redesenho
reativo:

- ativação da sessão somente quando stdin e stdout forem TTY;
- modo `cbreak`, nunca `raw`; `ISIG` e `OPOST` preservados;
- alternate screen (`\x1b[?1049h/l`);
- cursor oculto durante a sessão (`\x1b[?25l/h`);
- autowrap desativado durante a sessão (`\x1b[?7l/h`);
- posicionamento absoluto linha a linha com `CSI <linha>;1H`;
- preenchimento de cada linha escrita até a largura atual;
- uma escrita e um flush por quadro (escrita atômica);
- synchronized output (`\x1b[?2026h/l`) em toda atualização de quadro;
- limpeza integral de tela (`\x1b[2J`) apenas na entrada da sessão — o
  redimensionamento não autoriza repetir `\x1b[2J` a cada quadro nem a cada
  redimensionamento;
- restauração do terminal em `finally`;
- escopo de Ctrl+C definido pela ADR-0016;
- comportamento não-TTY preservado.

### 11. Comportamento não-TTY

O comportamento não-TTY permanece inalterado. Não devem ser adicionados ao fluxo
não-TTY:

- manipulador de `SIGWINCH`;
- sequências ANSI de sessão;
- alternate screen;
- redesenho reativo;
- qualquer alteração do protocolo de leitura por pipe.

### 12. Plataforma

Manter o escopo já estabelecido pelas ADRs anteriores:

- sistema compatível com `termios`, sinais POSIX e `ioctl`;
- terminal ANSI/VT/xterm;
- suporte Windows fora do escopo;
- detecção de capacidades por `terminfo` fora do escopo.

## Relação com a ADR-0013

A ADR-0013 normatizou que `altura_disponivel` é dimensão explícita do render e que
o renderer deve preencher a área vertical disponível entre `cabecalho` e
`barra_de_menus`. Esta ADR provê o mecanismo normativo para obter e manter a
dimensão de altura válida durante toda a sessão, inclusive após redimensionamento. As
duas ADRs são complementares: a ADR-0013 fixa a obrigação de usar a altura; a
ADR-0017 fixa como obter e atualizar esse valor de forma confiável durante a sessão
TTY.

## Consequências

### Obrigatórias

- A cadeia de obtenção por `ioctl(TIOCGWINSZ)` prevalece sobre qualquer outra
  fonte quando retorna dimensões válidas; `shutil.get_terminal_size()` não é
  mecanismo normativo suficiente como fonte primária do ciclo reativo.
- O par largura/altura deve ser sempre tratado como estado coerente; misturar fontes
  no mesmo redimensionamento é comportamento proibido.
- O redesenho por redimensionamento deve seguir o mesmo protocolo de escrita atômica
  e synchronized output já definido pela ADR-0016; não introduz exceção.
- O quadro mínimo de aviso para terminal pequeno demais é obrigatório e deve ser
  substituído automaticamente, sem intervenção do usuário, quando as dimensões
  ficarem suficientes novamente.
- O fallback fixo `(80, 24)` é exclusivo da inicialização sem fontes válidas; não
  se aplica como substituto das últimas dimensões válidas durante sessão ativa.
- A composição declarada (`corpo.arranjo`, `tiling`, chips, elementos) não pode ser
  alterada pelo redimensionamento.

### Artefatos a atualizar na futura etapa `APLICAR_ADR`

| Arquivo | Atualização mínima |
|---|---|
| `docs/adr/INDICE_ADR.md` | Registrar ADR-0017 |
| `docs/contratos/contrato_tela_json.md` | Registrar seção normativa de redimensionamento reativo: SIGWINCH, cadeia ioctl → LINES/COLUMNS → últimas dimensões válidas, redesenho, quadro mínimo de aviso e preservações da ADR-0016; distinguir da cadeia de inicialização |
| `docs/contratos/contrato_composicao_corpo.md` | Registrar que paginação e distribuição dependentes de dimensão devem ser recalculadas após atualização válida de dimensões; confirmar que `corpo.arranjo` e `tiling` não são alterados pelo redimensionamento |
| `docs/NOMENCLATURA.md` | Registrar `SIGWINCH`, `ioctl(TIOCGWINSZ)`, `últimas_dimensoes_validas` e `quadro_minimo_aviso` como termos específicos desta política; complementar a seção 6 (Layout e largura) com a política normativa de redimensionamento reativo |

`docs/contratos/contrato_processo_desenvolvimento.md` não requer atualização por
esta ADR: não há consequência processual nova — a ADR-0017 segue o ciclo padrão.

### Arquivos que NÃO devem ser alterados por esta ADR

| Arquivo ou grupo | Motivo |
|---|---|
| `tela/demo.py`, `tela/renderizador.py` e demais módulos | Implementação pertence ao handoff, não a esta ADR |
| `tela/teste_demo.py`, `tela/teste_renderizador.py` | Testes pertencem ao handoff |
| `docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md` | ADR aceita não é reescrita; a ADR-0017 a complementa sem substituí-la |
| `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md` | ADR aceita não é reescrita; a ADR-0017 a complementa sem substituí-la |
| `config/` | JSONs de configuração não são afetados por decisão de sessão TTY |
| `docs/handoff/` | Artefatos históricos permanecem; handoff novo será criado no tempo próprio |
| `docs/relatorios/` | Artefatos históricos de rastreabilidade; não reescrever |

### Riscos

- **`SIGWINCH` durante escrita:** se o sinal chegar enquanto um quadro está sendo
  construído, a implementação deve garantir que o quadro em curso não seja
  corrompido. A política não especifica o mecanismo (flag, fila, deferred) — esse
  detalhe pertence ao handoff, desde que o resultado obedeça à escrita atômica da
  ADR-0016.
- **Dimensões transientemente inválidas:** o terminal pode emitir `SIGWINCH` antes
  de atualizar `TIOCGWINSZ`. A cadeia de fallback (últimas dimensões válidas) protege
  contra isso, mas o redesenho pode ocorrer com as dimensões do estado anterior até
  que `ioctl` retorne valores consistentes em sinal subsequente.
- **Terminal muito pequeno sem recuperação:** se o usuário mantiver a janela abaixo
  do tamanho mínimo por período prolongado, o quadro de aviso permanece. Não é
  comportamento de erro — é o resultado esperado pela política do item 9. Não exige
  ação adicional.
- **Ausência de saída alternativa de emergência:** herdado da ADR-0016, que aceita
  esse risco explicitamente. Redimensionamento não altera o escopo de Ctrl+C.

### Pendências derivadas

- Handoff de implementação de redimensionamento reativo: registrar `SIGWINCH`,
  implementar a cadeia `ioctl → LINES/COLUMNS → últimas dimensões válidas`, integrar
  ao loop de sessão TUI, implementar o quadro mínimo de aviso e os critérios de
  recuperação automática. O handoff citará esta ADR como autoridade superior e
  aplicará a numeração sequencial vigente no momento da criação.
- A aplicação da ADR aos contratos (`APLICAR_ADR`) deve preceder a criação do
  handoff de implementação, conforme o ciclo padrão do
  `contrato_processo_desenvolvimento.md`.

## Fora do escopo

- Implementação de qualquer código ou teste — pendências de handoff.
- Estrutura interna do manipulador de `SIGWINCH` (flag, fila, deferred) — decisão
  de implementação do handoff, desde que respeite a política desta ADR.
- Nome exato de função, classe, módulo ou flag interna — pertence ao handoff.
- Texto visual exato do aviso de terminal pequeno demais além do significado
  obrigatório — margem de adequação à largura disponível é do handoff.
- Algoritmo interno do loop de sessão — decisão de implementação.
- Suporte Windows.
- Detecção de capacidades por `terminfo`.
- Uso de `curses`, `textual` ou `rich`.
- Alteração do comportamento não-TTY.
- Redimensionamento de `barra_de_menus` com comportamento específico de
  `distribuicao.modo = "horizontal_responsiva"` além do recálculo visual já previsto
  pelo item 7 — detalhes permanecem no contrato da barra_de_menus.

## Alternativas consideradas

| Alternativa | Motivo para rejeitar |
|---|---|
| `shutil.get_terminal_size()` como fonte primária do ciclo reativo | Não é mecanismo normativo suficiente para o ciclo reativo: não fornece garantias de atomicidade do par, e a ADR não pode deixar a cadeia de fallback implícita em uma única chamada de conveniência |
| `ncurses` / `curses` para gerenciar resize | Dependência de biblioteca de TUI rejeitada explicitamente — viola a restrição já estabelecida desde H-0009 e confirmada na ADR-0016 |
| `textual` / `rich` | Mesma razão: dependência de biblioteca de TUI |
| Reiniciar a sessão TUI ao receber SIGWINCH | Produziria flash de tela ao sair e reentrar no alternate screen, violando o objetivo de ausência de cintilação da ADR-0016 |
| Ignorar SIGWINCH e não redesenhar | Deixa o quadro incoerente com as dimensões reais do terminal até reinicialização manual — comportamento rejeitado pelo escopo desta ADR |
| Usar somente `LINES` e `COLUMNS` | Variáveis de ambiente podem não refletir o estado atual após redimensionamento; `ioctl(TIOCGWINSZ)` é mais confiável e deve prevalecer |
| Encerrar a sessão TUI quando o terminal for pequeno demais | Interrompe a sessão desnecessariamente; a recuperação automática é preferível e não exige ação do usuário |
| Exibir quadro antigo comprimido quando o terminal for pequeno demais | Risco de escrever além da área disponível e gerar scroll; não garante que o conteúdo seja legível |

## Critérios objetivos para futura aplicação da ADR

Os critérios abaixo são verificáveis na etapa `APLICAR_ADR` e no handoff de
implementação subsequente:

- [ ] `docs/adr/INDICE_ADR.md` registra ADR-0017 com status `aceita` e data
      2026-07-11.
- [ ] `docs/contratos/contrato_tela_json.md` contém seção normativa sobre
      redimensionamento reativo que referencia SIGWINCH, cadeia
      `ioctl → LINES/COLUMNS → últimas dimensões válidas`,
      `ioctl → LINES/COLUMNS → (80,24)` na inicialização, quadro mínimo de aviso
      e preservações da ADR-0016.
- [ ] `docs/contratos/contrato_composicao_corpo.md` registra que paginação e
      distribuição são recalculadas após atualização válida de dimensões, sem alterar
      `corpo.arranjo` nem `tiling`.
- [ ] `docs/NOMENCLATURA.md` registra `SIGWINCH`, `ioctl(TIOCGWINSZ)`,
      `últimas_dimensoes_validas` e `quadro_minimo_aviso` como termos específicos.
- [ ] Nenhum arquivo em `tela/`, `config/` ou `docs/handoff/` foi alterado na etapa
      `APLICAR_ADR`.
- [ ] `docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md` não foi
      modificado.

Critérios verificáveis na implementação (handoff):

- [ ] Recebimento de SIGWINCH desencadeia atualização de dimensões e redesenho.
- [ ] `ioctl(TIOCGWINSZ)` é a primeira fonte consultada; outras fontes só são
      consultadas quando `ioctl` falha ou retorna par inválido.
- [ ] Largura e altura são atualizadas como par coerente — nunca de fontes distintas
      na mesma atualização.
- [ ] Par inválido não é aplicado ao renderer; últimas dimensões válidas são mantidas.
- [ ] Fallback fixo `(80, 24)` aparece apenas na inicialização sem fontes válidas,
      nunca como substituto de últimas dimensões válidas durante sessão ativa.
- [ ] Quadro redesenhado não deixa resíduos do quadro anterior, não gera scroll e não
      escreve além da área disponível.
- [ ] Composição declarada (`corpo.arranjo`, `tiling`, chips, elementos) permanece
      inalterada após redimensionamento.
- [ ] Terminal abaixo do tamanho mínimo exibe quadro mínimo de aviso que cabe nas
      dimensões atuais, sem scroll, sem resíduo e sem escrita além da área.
- [ ] Quadro mínimo é substituído automaticamente pela tela normal quando dimensões
      suficientes são restauradas, sem ação do usuário.
- [ ] `\x1b[2J` não é emitido a cada redesenho por redimensionamento.
- [ ] Escrita de quadro continua atômica (uma chamada `write()` + um `flush()`) e usa
      synchronized output (`\x1b[?2026h/l`).
- [ ] Nenhum manipulador de SIGWINCH é instalado no fluxo não-TTY.

## Relação com o handoff de implementação

Esta ADR define a política. O handoff de implementação subsequente — a ser criado em
ciclo futuro, com numeração sequencial atribuída no momento da criação — é responsável
por detalhar:

- estrutura técnica do manipulador de `SIGWINCH` e integração ao loop de sessão;
- representação interna das últimas dimensões válidas;
- mecanismo concreto de deferimento ou execução direta dentro do handler;
- texto visual exato do aviso de terminal pequeno demais;
- limiares mínimos de dimensão para determinar "suficiente" vs "pequeno demais";
- casos de teste e critérios de aceite verificáveis item a item.

O handoff deve citar esta ADR como autoridade superior. Nenhum detalhe do handoff
pode contradizer a política registrada aqui.

Código, testes e handoff serão tratados apenas depois da aplicação documental
(`APLICAR_ADR`) ter sido aprovada.
