# ADR-0044 — Pop-up modal genérico de decisão

**Projeto:** Orquestrador
**Item:** ITEM-0017
**Estado:** aplicada

## Contexto e problema

O `ITEM-0017` registra historicamente a avaliação de `popup_execucao`. A
decisão deste ciclo substitui a necessidade dessa especialização por uma
capacidade genérica de pop-up modal para decisões pequenas e focais do
sistema. É necessário registrar a capacidade sem transformá-la em tela,
elemento funcional do corpo, região permanente, `console`,
`barra_de_menus` ou executor de ações.

## Decisão

O Orquestrador terá um **pop-up** genérico: uma apresentação modal aberta
sobre a tela ativa, usando o corpo dessa tela como referência física. Ele
suspende a interação com a tela inferior enquanto está aberto, mas não
substitui a tela, não altera sua composição ou seu estado declarativo e não
cria novo elemento funcional nem nova região permanente. A tela subjacente
permanece materializada e, ao encerramento, volta exatamente ao estado vivo
anterior.

O pop-up existe somente para decisões pequenas que não justificam uma tela
completa. Ele recebe configuração e conteúdo prontos, valida, apresenta,
mantém o estado provisório da interação e devolve um resultado estruturado.
Nunca executa a decisão de negócio: qualquer efeito posterior é decidido pelo
chamador.

## Arquitetura conceitual da capacidade

### Fronteiras

- **Tela e corpo:** o pop-up é uma apresentação sobre a tela ativa. O corpo
  da tela é apenas sua área física de referência; o pop-up não passa a ser
  filho da composição declarativa, não altera a composição e não substitui a
  tela.
- **`barra_de_menus`:** os chips do pop-up pertencem ao próprio pop-up e não
  são a `barra_de_menus` da tela subjacente. A barra inferior da tela continua
  sendo uma região independente.
- **Estilo:** o pop-up possui moldura, título e aparência compatíveis com o
  padrão visual vigente. A moldura reutiliza o padrão visual vigente e
  posteriormente consome a materialização vigente do estilo universal.
  Símbolos, caracteres e cores de borda não podem ser hardcoded para o
  pop-up. O título reutiliza o padrão de títulos de componentes com moldura,
  ocupa a moldura superior e não cria linha interna adicional nem segundo
  sistema de aparência.
- **Conteúdo externo:** o conteúdo concreto chega pronto em runtime por quem
  chama o pop-up. O pop-up não resolve origem de dados, não chama produtor,
  não executa script e não conhece como os dados foram produzidos.
- **Runtime:** cursor, marcações provisórias, abertura, fechamento e demais
  condições vivas da interação pertencem ao estado de runtime da instância.

### Configuração, conteúdo e estado vivo

| Camada | Responsabilidade |
|---|---|
| Configuração estrutural | JSON geral de configuração; declara apresentação, comportamento permitido, título, alinhamento, espaçamentos, chips, política de marcação e contrato de retorno, conforme aplicável. |
| Conteúdo recebido | Envelope discriminado por tipo, fornecido pronto pelo chamador; contém somente os dados daquela abertura. |
| Estado de runtime | Cursor, marcações provisórias, abertura/fechamento e condições vivas; não altera a configuração nem o envelope. |

O envelope recebido permanece imutável durante a interação. A configuração
declara a política `marcacao: exclusiva` ou `marcacao: multipla`; essa política
não é redefinida pelo envelope.

### D-POP-25 — Declaração estrutural, identidade e abertura de pop-ups

O JSON geral estrutural da tela declara as configurações de pop-up no campo
literal `popups`. Esse campo fica no nível geral do JSON, como configuração
auxiliar, fora de `cabecalho`, `corpo` e `barra_de_menus`. Portanto, `popups`
não cria uma quarta região, não integra a composição do corpo e não altera a
taxonomia funcional da tela.

`popups` é um mapa/objeto, não uma lista, com cardinalidade de `0..N`
declarações. A ausência do campo ou um mapa vazio representa que não há
declaração de pop-up. A forma conceitual é:

```yaml
popups:
  popup_mensagem:
    tipo: texto
    titulo: "Mensagem"
  popup_escolha:
    tipo: marcacao
    titulo: "Escolha"
```

A chave do mapa é o ID estável da declaração estrutural. Esse ID pertence à
declaração, permanece estável dentro daquela configuração e não depende do
conteúdo, da posição ou da ordem física. Não há necessidade de repetir essa
identidade em um campo interno `id` obrigatório.

Cada valor de `popups` contém somente a configuração estrutural e interativa
do pop-up, conforme esta ADR. A declaração não incorpora conteúdo concreto de
uma abertura nem dados persistentes de runtime: não contém mensagem produzida,
lista concreta de itens, marcações runtime, cursor, resultado, produtor,
loader ou origem de dados.

Para abrir um pop-up, o chamador fornece o ID da declaração, o envelope de
conteúdo já pronto daquela abertura e, quando aplicável, o contrato de
resultado esperado previsto nesta ADR. O runtime resolve a configuração em
`popups[ID]`, valida configuração, conteúdo e contrato esperado e só então
materializa a instância modal. O pop-up continua sem conhecer ou acionar o
produtor do conteúdo e sem executar ação de negócio.

Uma mesma declaração pode ser aberta zero, uma ou várias vezes, em momentos
distintos e com envelopes compatíveis diferentes. A reutilização não altera a
configuração declarada.

Declaração em `popups` e instância aberta são entidades distintas. A
declaração é configuração; a instância é runtime e mantém o conteúdo daquela
abertura, o cursor quando aplicável, as marcações provisórias quando
aplicáveis, o estado aberto/fechado e o resultado eventual. A instância não
modifica a declaração estrutural original.

## Tipos de conteúdo

### Texto

O tipo `texto` recebe do exterior uma string semântica. O alinhamento do
conjunto é declarado pela configuração e fica limitado a:

```text
esquerda | centralizado | justificado
```

O renderer quebra preferencialmente entre palavras. Palavra isolada maior que
a largura útil só pode ser quebrada quando indispensável. O conteúdo não é
truncado, não recebe reticências e não é paginado. No modo justificado, linhas
completas são justificadas e a última permanece alinhada à esquerda.

### Marcação navegável

O tipo `marcacao` possui instrução textual obrigatória e não selecionável e
uma lista plana de itens em um único nível. Deve haver pelo menos um item;
todos os itens reais são navegáveis; cada item possui ID estável e único; o
texto de cada item ocupa uma única linha física. A instrução é texto livre do
conteúdo e pode usar as mesmas regras de alinhamento e wrapping do conteúdo
textual. Itens não sofrem wrapping nem truncamento.

## Geometria, moldura e resize

A referência geométrica é exclusivamente a área física do corpo da tela
ativa. Cabeçalho e `barra_de_menus` não entram no retângulo de centralização.
O pop-up é centralizado horizontal e verticalmente nessa área e deve ficar
integralmente contido nela.

Largura e altura não são dimensões fixas declaradas. O tamanho acompanha o
conteúdo:

1. calcular a largura intrínseca necessária;
2. usá-la quando couber;
3. limitar à largura disponível do corpo quando excedê-la;
4. recalcular wrapping, chips e altura;
5. centralizar o resultado final.

A altura é consequência do conteúdo, dos espaçamentos e das linhas de chips.

Os espaçamentos são declarativos no JSON. Os intervalos verticais
independentes são:

- borda superior → conteúdo: `0|1` linha;
- conteúdo → chips: `0|1` linha;
- chips → borda inferior: `0|1` linha;
- para marcação, instrução → itens: `0|1` linha.

O espaçamento horizontal entre bordas laterais e área útil é de no mínimo 1 e
no máximo 5 colunas. Esses valores não podem ser hardcoded nem reduzidos
autonomamente pelo renderer para forçar encaixe.

O pop-up permanece logicamente aberto durante o redimensionamento. Reutiliza
o mecanismo geral de redimensionamento reativo da TUI. Após novas dimensões
válidas, recalcula, nesta ordem, área do corpo, largura, wrapping, distribuição
dos chips, altura e centralização. Resize não fecha nem reabre, não altera a
configuração, não perde cursor nem marcação e muda somente a representação
física. Par de dimensões inválido preserva as últimas dimensões válidas.

Se a representação completa não couber após todos os ajustes permitidos, o
pop-up usa o `quadro mínimo de terminal pequeno` já vigente. Não cria fallback
próprio, não pagina, não trunca, não remove chips, não reduz espaçamentos
declarados e não altera a política de apresentação. Quando houver dimensões
suficientes, restaura automaticamente a mesma instância lógica.

## Chips e retorno de Esc

A área de chips é do pop-up, vem declarada no JSON e aparece depois do
conteúdo. Os chips preservam exatamente a ordem declarada, são centralizados
horizontalmente, tentam ocupar inicialmente uma linha e, quando necessário,
distribuem-se por quantas linhas forem necessárias. Cada linha é centralizada
independentemente. Um chip é indivisível e a quebra nunca muda a ordem lógica.

Tecla física, rótulo visual e semântica de retorno são conceitos distintos.
O rótulo é livre conforme o contexto; são válidos, por exemplo,
`[Esc] Voltar`, `[Esc] Cancelar`, `[Enter] Aplicar`, `[Enter] Executar` e
`[Enter] Confirmar`. O texto do rótulo não determina ação de negócio.

`Esc` é a saída não confirmatória. Produz:

```yaml
status: ABORTADO
```

`ABORTADO` não possui payload, não altera escolha ou valor preexistente do
chamador e é semanticamente distinto de uma seleção vazia. Toda alteração
feita dentro do pop-up permanece provisória até a confirmação.

## Navegação e marcação

O cursor é independente da marcação. A navegação da lista é sempre toroidal
por eixo, reutilizando as regras canônicas vigentes:

- células vazias não recebem cursor nem participam do toroide;
- não há compensação entre eixos, salto diagonal ou busca geométrica pelo
  item mais próximo;
- coluna: `↑/↓` são toroide e `←/→` resultam em `SEM_MOVIMENTO`;
- linha: `←/→` são toroide e `↑/↓` resultam em `SEM_MOVIMENTO`;
- matriz: os eixos horizontal e vertical são toroides independentes;
- eixo sem outro item ocupado resulta em `SEM_MOVIMENTO`.

O cursor inicial é sempre o primeiro item real da ordem declarada.

A apresentação tenta, nesta ordem, uma coluna, uma matriz e uma linha. Na
matriz, usa o menor número de colunas capaz de acomodar todos os itens,
preenche verticalmente por colunas e depois segue da esquerda para a direita.
Não cria placeholders nem itens em branco. A mudança entre coluna, matriz e
linha é somente física: IDs, ordem lógica, cursor e marcações permanecem
independentes da posição geométrica.

Não se usa o termo canônico de console **`seleção única`** para a política
exclusiva do pop-up. No console, esse termo designa o item sob cursor e mover
o cursor muda automaticamente a seleção. No pop-up, as únicas políticas são:

```text
marcacao: exclusiva
marcacao: multipla
```

### `marcacao: exclusiva`

Mantém exatamente um item marcado em todo estado válido. A entrada deve
conter exatamente um ID inicialmente marcado; zero ou mais de um tornam o
conteúdo inválido. Espaço sobre item diferente transfere a marcação; sobre o
próprio item marcado resulta em `SEM_MUDANCA`. Mover o cursor não altera a
marcação. A confirmação sempre devolve exatamente um ID.

### `marcacao: multipla`

Admite de zero a N itens marcados. Espaço alterna individualmente a marcação
do item em foco. O conjunto vazio é válido. A confirmação devolve uma lista
de IDs na ordem lógica declarada, nunca na ordem temporal de marcação.

Marcações iniciais referenciam IDs, nunca índices físicos. São inválidos IDs
duplicados entre itens, referências a IDs inexistentes e cardinalidade inicial
incompatível com a política. Resize e recomposição preservam cursor e
marcações pelos IDs.

## Entrada, saída e compatibilidade

O conteúdo de entrada possui envelope discriminado por tipo. Formas
conceituais:

```yaml
conteudo_popup:
  tipo: texto
  texto: "Mensagem"
```

```yaml
conteudo_popup:
  tipo: marcacao
  instrucao: "Escolha uma opção:"
  itens:
    - id: opcao_1
      texto: "Opção 1"
    - id: opcao_2
      texto: "Opção 2"
  marcados:
    - opcao_2
```

O envelope não redefine título, aparência, alinhamento configurado,
espaçamentos, chips, política de retorno ou dimensões. Campos desconhecidos
geram falha fechada.

O resultado tem a forma conceitual:

```yaml
resultado_popup:
  status: CONFIRMADO | ABORTADO
  valor: <quando aplicável>
```

`ABORTADO` não possui `valor`. Em `CONFIRMADO`, `marcacao: exclusiva`
retorna exatamente um ID e `marcacao: multipla` retorna lista de zero a N IDs.
O resultado nunca contém cursor, coordenadas, linha/coluna física, ordem de
acionamento ou rótulo do chip.

O chamador declara o tipo de resultado que aceita. A abertura só ocorre se
configuração, conteúdo e contrato esperado forem compatíveis. O pop-up não
converte tipos para atender ao chamador; incompatibilidade é falha de
configuração anterior à interação. `ABORTADO` permanece distinto de valor
vazio, inclusive quando o retorno confirmado de marcação múltipla for uma
lista vazia.

## Validação antes da materialização

Antes da abertura, configuração e envelope são validados em conjunto. A
validação confirma pelo menos:

- tipo de conteúdo;
- campos permitidos;
- domínios de alinhamento;
- domínios de espaçamento;
- chips;
- ausência de tecla duplicada;
- IDs;
- cardinalidade;
- tipo de retorno;
- compatibilidade com o chamador.

Configuração ou conteúdo inválido não é corrigido silenciosamente. Não se
escolhe default arbitrário, não se elimina campo desconhecido, não se removem
marcações excedentes, não se converte tipo e não se abre parcialmente.
Somente depois da validação é criado o estado de runtime da instância.

## Consequências

- A mesma capacidade atende decisões textuais e listas focais sem criar uma
  especialização `popup_execucao`.
- A tela ativa continua materializada e preserva seu estado vivo; a interação
  modal fica isolada até o encerramento.
- O chamador permanece dono da decisão de negócio, da interpretação do
  resultado e de qualquer efeito posterior.
- A separação entre configuração, conteúdo pronto e runtime impede que dados
  de uma abertura sejam confundidos com schema, origem de dados ou estado
  vivo.
- Geometria, wrapping, chips e resize são recalculados sem alterar a
  identidade lógica, IDs, cursor ou marcações.
- A validação fechada torna erros de configuração, conteúdo e compatibilidade
  observáveis antes da interação, sem correção implícita.
- A capacidade não introduz paginação, nova aparência independente, nova
  política geral de terminal pequeno ou ação de negócio.

## Compatibilidade

Esta decisão preserva as seguintes compatibilidades terminológicas e
arquiteturais:

- pop-up não é `console`, não é elemento funcional do corpo, não é tela e não
  é região permanente;
- pop-up não é a `barra_de_menus`; seus chips ocupam área própria;
- a aparência depende do padrão vigente e da materialização do estilo
  universal, sem hardcode específico;
- conteúdo chega pronto em runtime e o pop-up não declara produtor, origem ou
  carregamento de dados;
- `seleção única` continua sendo o termo canônico do console, com a semântica
  de seleção que acompanha o cursor; `marcacao: exclusiva` é a política
  própria do pop-up e não é renomeada para esse termo;
- `ABORTADO` não equivale a valor vazio;
- não há paginação de conteúdo nem mudança da política geral de terminal
  pequeno;
- o retorno expõe semântica lógica por IDs, não representação física ou
  histórico de interação.

## Fora de escopo

Não são definidos nem implementados por esta ADR:

- ação de negócio específica;
- produtor concreto de conteúdo;
- integração definitiva com escolha ou persistência de estilo;
- execução de processos pelo pop-up;
- paginação de conteúdo;
- hierarquia multinível dentro do pop-up;
- campo de busca ou filtro;
- edição livre de texto;
- tela completa de gerenciamento de pop-ups;
- nova política geral de terminal pequeno;
- nova aparência independente do estilo universal.

## Critérios de aplicação

A capacidade se aplica quando a decisão é pequena e focal, não justifica uma
tela completa, o chamador dispõe de conteúdo já pronto e existe um contrato
de retorno esperado. A abertura depende da validade conjunta da configuração
e do envelope, da política de marcação quando aplicável e da compatibilidade
entre o tipo de resultado produzido e o tipo aceito pelo chamador.

Uma abertura inválida falha antes da interação. Uma abertura válida apresenta
o conteúdo na instância modal, mantém alterações provisórias e encerra por
confirmação ou por `Esc`, devolvendo somente o envelope de resultado previsto.

## Decomposição incremental prevista

A implementação futura será incremental, sem tratar expansões posteriores
como patches corretivos da fundação:

1. exibição mínima textual + `[Esc] Voltar`;
2. geometria dinâmica, wrapping e resize;
3. lista navegável + marcação exclusiva/múltipla;
4. confirmação, envelopes de retorno e compatibilidade chamador↔pop-up.

Essa decomposição é operacional e não altera o contrato funcional integral
registrado nesta ADR.
