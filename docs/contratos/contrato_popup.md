---
name: contrato-popup
description: Contrato especializado do pop-up modal genérico de decisão
metadata:
  type: contrato
  scope: orquestrador
  versao: "0.1"
  status: ativo
  rastreabilidade:
    origem_especificacao:
      - docs/adr/ADR-0044-popup-modal-generico-de-decisao.md
    adrs_aplicadas:
      - docs/adr/ADR-0044-popup-modal-generico-de-decisao.md
    reaproveitado_de_legado: false
  dependencias_nomenclatura:
    dependencias_obrigatorias:
      - docs/nomenclatura/01_NUCLEO_COMUM.md
      - docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md
      - docs/nomenclatura/10_ESTILO.md
      - docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md
      - docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md
      - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
      - docs/nomenclatura/32_CONSOLE.md
      - docs/nomenclatura/35_POPUP.md
    dependencias_condicionais:
      - modulo: docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md
        quando: verificar a fronteira com o envelope multinível do console
      - modulo: docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md
        quando: verificar a fronteira com carregamento e produtor de conteúdo
---

# Contrato — `pop-up`

## 1. Objetivo

Este contrato define a capacidade genérica de pop-up modal para decisões
pequenas e focais. O pop-up apresenta conteúdo recebido, mantém uma interação
provisória e devolve um resultado ao chamador. Não implementa ação de negócio,
não define produtor de dados e não transforma o pop-up em uma tela ou em um
elemento funcional do corpo.

## 2. Natureza e fronteiras

`pop-up` é uma apresentação modal sobreposta à tela ativa. O corpo da tela
ativa é a área física de referência para sua geometria; ele não passa a
conter o pop-up como filho. A tela subjacente permanece materializada e seu
estado vivo é preservado, mas fica suspensa para interação enquanto a
instância de pop-up está aberta. Ao encerramento, a tela subjacente volta a
receber interação.

O pop-up não é `console`, não é elemento funcional do corpo, não é região
permanente e não é uma quarta região da tela. Não executa a ação de negócio
sugerida por um rótulo. O chamador consome o resultado, interpreta-o e decide
qualquer efeito posterior.

## 3. Configuração, conteúdo e runtime

As camadas permanecem separadas:

| Camada | Responsabilidade |
|---|---|
| Configuração do pop-up | Declara apresentação, título, alinhamento, espaçamentos, chips, política de marcação e contrato esperado de retorno, conforme aplicável. Pertence à configuração estrutural geral. |
| Conteúdo recebido | Envelope pronto da abertura, discriminado por `tipo`. Contém somente o conteúdo daquela interação e permanece imutável durante a abertura. |
| Estado vivo da instância | Abertura, fechamento, cursor e marcações provisórias. Não altera a configuração nem o envelope recebido. |

O conteúdo concreto chega pronto do chamador. A instância não resolve
produtor, origem de dados, loader ou associação externa de conteúdo.

### 3.1 Declaração estrutural e resolução

Uma definição estrutural de pop-up reside no mapa geral `popups` do JSON
estrutural da tela, sob a chave `popups[ID]`. Uma abertura referencia o ID da
declaração e fornece o envelope de conteúdo já pronto e, quando aplicável, o
contrato de resultado esperado pelo chamador.

Antes de materializar a instância, o runtime recebe o ID, resolve
`popups[ID]`, combina a declaração com o envelope pronto e valida a
compatibilidade. ID inexistente é erro de validação e impede a abertura; não
há fallback para outra declaração.

Uma mesma declaração pode ser reutilizada várias vezes com envelopes
diferentes e compatíveis. A abertura não consome nem modifica a declaração.
Declaração de pop-up e instância de pop-up são entidades distintas: a
declaração é configuração estável do JSON estrutural, e a instância é o objeto
de runtime criado para uma abertura concreta, com conteúdo e estado vivo
próprios. A instância nunca altera a declaração.

## 4. Estrutura visual e geometria

Uma instância válida possui:

- moldura compatível com o estilo universal;
- título na moldura superior, sem linha interna adicional;
- área de conteúdo;
- área própria de chips, posterior ao conteúdo;
- centralização horizontal e vertical na área física do corpo;
- tamanho intrínseco derivado do conteúdo, dos espaçamentos e dos chips;
- limites integralmente contidos na área do corpo.

Cabeçalho e `barra_de_menus` não entram no retângulo de referência da
centralização; somente a área física do corpo é considerada.

Largura e altura não são dimensões fixas. A largura intrínseca é usada quando
couber; quando exceder a área do corpo, o conteúdo é recalculado com wrapping,
os chips são redistribuídos e a altura é recalculada antes da centralização.

Os espaçamentos verticais independentes aceitam somente `0|1` linha:

| Intervalo | Campo semântico |
|---|---|
| borda superior → conteúdo | superior ao conteúdo |
| conteúdo → chips | inferior ao conteúdo |
| chips → borda inferior | inferior aos chips |
| instrução → itens | aplicável ao tipo `marcacao` |

O espaçamento horizontal entre cada borda lateral e a área útil aceita somente
`1..5` colunas. O renderer não reduz silenciosamente um valor declarado para
forçar encaixe.

## 5. Conteúdo textual

O envelope de tipo `texto` fornece uma string semântica. O alinhamento é
declarado na configuração e aceita somente:

```text
esquerda | centralizado | justificado
```

O texto usa wrapping, preferencialmente entre palavras. Palavra isolada maior
que a largura útil só é quebrada quando indispensável. O conteúdo não é
truncado, não recebe reticências e não é paginado. Em texto justificado, linhas
completas são justificadas e a última permanece alinhada à esquerda.

## 6. Conteúdo de marcação

O envelope de tipo `marcacao` contém instrução textual obrigatória e uma lista
plana de itens de um único nível. A instrução não é selecionável. Deve existir
pelo menos um item; cada item real tem ID estável e único, e seu texto ocupa
uma única linha física. Itens não sofrem wrapping nem truncamento.

As formações físicas são tentadas nesta ordem:

```text
coluna → matriz → linha
```

Na matriz, usa-se o menor número de colunas capaz de acomodar todos os itens,
com preenchimento vertical por colunas e avanço das colunas da esquerda para a
direita. Não há placeholders navegáveis, itens em branco ou células vazias
introduzidas para completar a grade. A mudança de formação é somente física:
IDs, ordem lógica, cursor e marcações permanecem os mesmos.

O cursor é independente da marcação. A navegação é toroidal por eixo:

- coluna: `↑/↓` percorrem o toroide; `←/→` resultam em `SEM_MOVIMENTO`;
- linha: `←/→` percorrem o toroide; `↑/↓` resultam em `SEM_MOVIMENTO`;
- matriz: os eixos horizontal e vertical são toroides independentes;
- eixo sem outro item ocupado resulta em `SEM_MOVIMENTO`;
- células vazias não recebem cursor nem participam do toroide.

O cursor inicial é o primeiro item real da ordem declarada.

## 7. Políticas de marcação

As políticas próprias do pop-up são, literalmente:

```text
marcacao: exclusiva
marcacao: multipla
```

Não se reutiliza `seleção única` do console para `marcacao: exclusiva`.

### 7.1 `marcacao: exclusiva`

- mantém exatamente uma marcação válida;
- exige exatamente uma marcação inicial válida;
- Espaço sobre item diferente transfere a marcação;
- Espaço no item já marcado resulta em `SEM_MUDANCA`;
- mover o cursor não muda a marcação;
- a confirmação devolve exatamente um ID.

### 7.2 `marcacao: multipla`

- admite zero a N marcações;
- Espaço alterna a marcação do item corrente;
- a confirmação devolve uma lista de IDs na ordem lógica declarada, inclusive
  quando a lista é vazia.

Marcações iniciais referenciam IDs, nunca índices físicos. IDs duplicados,
referências inexistentes e cardinalidade incompatível com a política são
inválidos. Resize e recomposição preservam cursor e marcações por ID.

## 8. Envelope de entrada

O envelope de conteúdo é discriminado por `tipo` e recebe somente conteúdo
pronto:

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

Para `tipo: texto`, os campos permitidos são `tipo` e `texto`. Para
`tipo: marcacao`, os campos permitidos são `tipo`, `instrucao`, `itens` e
`marcados`; `itens` é a lista plana de itens e `marcados` identifica as
marcações iniciais. Campos desconhecidos são inválidos. O envelope não redefine
título, aparência, alinhamento, espaçamentos, chips, política de marcação,
contrato de retorno ou dimensões.

A política de marcação pertence à configuração, não ao envelope.

## 9. Chips e resultado

Tecla física, rótulo visual e semântica de retorno são propriedades distintas.
A área de chips pertence ao próprio pop-up; sua ordem é a ordem declarada no
pop-up, não a ordem canônica da `barra_de_menus`. A aparência dos chips deriva
do estilo universal. Os chips tentam ocupar inicialmente uma linha, distribuem-
se por quantas linhas forem necessárias quando não couberem, mantêm a ordem
declarada, são indivisíveis e têm cada linha centralizada independentemente.
O rótulo não define ação de negócio.

`Esc` é a saída não confirmatória e produz exatamente:

```yaml
status: ABORTADO
```

`ABORTADO` não possui payload. É distinto de uma seleção ou lista vazia. Toda
alteração feita na instância permanece provisória até a confirmação.

Quando declarada e compatível, a confirmação produz:

```yaml
status: CONFIRMADO
valor: <conforme tipo>
```

O chamador é o consumidor do resultado. O pop-up não executa a ação sugerida
por `[Enter]`, pelo rótulo ou pelo valor confirmado.

O chamador declara o contrato de resultado que aceita. A confirmação só é
compatível quando o valor produzido corresponde ao tipo de conteúdo e à forma
de retorno prevista para a instância.

## 10. Validação fechada

Configuração, envelope de conteúdo e contrato esperado pelo chamador são
validados conjuntamente antes da materialização da instância. A abertura só
ocorre se forem compatíveis.

Falha fechada é obrigatória para, no mínimo:

- campos desconhecidos;
- tipo de conteúdo ou de retorno incompatível;
- alinhamento ou espaçamento fora do domínio;
- chip inválido ou tecla duplicada;
- lista vazia de itens;
- ID ausente, duplicado ou inexistente nas marcações;
- cardinalidade inicial incompatível;
- marcações excedentes;
- contrato esperado incompatível.

Não se escolhe default arbitrário, não se elimina campo desconhecido, não se
converte tipo, não se removem marcações excedentes e não se abre parcialmente.

## 11. Resize e terminal pequeno

O pop-up reutiliza a autoridade geral vigente de redimensionamento: `SIGWINCH`,
par de dimensões válido, últimas dimensões válidas, redesenho integral e
`quadro mínimo de terminal pequeno`. A instância permanece logicamente aberta;
resize altera somente a representação física e preserva envelope, cursor,
marcações e configuração.

Quando a representação completa não couber após os ajustes permitidos, aplica-se
o quadro mínimo geral. O pop-up não cria fallback concorrente, não pagina, não
trunca, não remove chips, não reduz espaçamentos declarados e não redefine a
política geral de terminal pequeno. Com dimensões suficientes, a mesma
instância lógica é restaurada.

## 12. Relações normativas

- `contrato_tela_json.md`: configuração estrutural geral e fronteira com o
  conteúdo runtime; não incorpora o envelope como estado persistido da tela.
- `contrato_chip.md`: entidade visual/semântica de chip consumível pelo
  pop-up; a área própria não é `barra_de_menus`.
- `docs/nomenclatura/35_POPUP.md`: termos proprietários e fronteiras do domínio.
- `docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md` e
  `docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md`: o envelope
  do pop-up não é envelope multinível do console e não declara origem,
  produtor ou loader.
