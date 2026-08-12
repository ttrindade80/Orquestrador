# Handoff H-0060 — Resize responsivo das formações do pop-up de marcação

## 1. Identificação

| Campo | Valor |
|---|---|
| Item | `ITEM-0028` |
| ADR | `ADR-0045` |
| Handoff | `H-0060` |
| Título | Resize responsivo das formações do pop-up de marcação |
| Etapa | `PATCH_HANDOFF` P01 concluído após `MV-H0060-001`; implementação corretiva futura em uma única etapa |
| Escopo | Conteúdo `tipo: marcacao` do pop-up modal e sua integração física com a área do corpo em `renderizar_tela` |

Este é o único handoff planejado para o `ITEM-0028`. A implementação deve
transportar a ADR-0045 já aprovada e aplicada, sem criar decisão arquitetural,
sem alterar contrato, nomenclatura, backlog ou ADR e sem criar um segundo
fluxo de redimensionamento.

## 2. Objetivo

Implementar a recomposição responsiva das formações físicas dos itens de
marcação enquanto a mesma instância do pop-up permanece aberta e o terminal
recebe novos pares válidos de dimensões físicas.

A prioridade obrigatória é:

```text
coluna → matriz → linha → quadro mínimo de terminal pequeno
```

A mudança é exclusivamente física. Conteúdo recebido, ordem lógica, IDs,
cursor, marcações provisórias, política de marcação, confirmação e aborto
devem permanecer com as semânticas vigentes.

## 3. Estado inicial relevante

A implementação atual já contém as estruturas que devem ser evoluídas:

- `PopupInstancia` mantém declaração, envelope e `_estado` mutável da mesma
  instância; o estado registra `cursor_id`, `marcados`, `formacao`, `grade` e
  `colunas`.
- `_layout_popup_marcacao` calcula as larguras dos itens, limita a largura à
  área do corpo, faz wrapping da instrução, distribui os chips e desconta o
  overhead antes de escolher a formação.
- `_colunas_formacao` particiona os IDs em fatias verticais, preservando a
  ordem lógica.
- `_grade_para_formacao` materializa as linhas físicas a partir das colunas,
  sem inserir células navegáveis artificiais.
- `_navegar_marcacao` navega sobre a grade materializada e preserva as regras
  por formação.
- `renderizar_popup` e `sobrepor_no_corpo` já recebem as dimensões físicas e
  acionam a recomposição da geometria.
- O fluxo geral já é responsável pelo par de dimensões válido, pelo resize
  geral e pelo quadro mínimo de terminal pequeno.

O ponto originalmente alterado foi a política materializada em
`_selecionar_formacao`. A implementação aprovada já avalia as candidatas e
retém a matriz que maximiza as colunas fisicamente ocupadas; esse algoritmo
não é a causa de `MV-H0060-001` e não deve ser reaberto sem nova necessidade
demonstrada.

O código atual também já possui cálculo de largura física de item, cálculo de
altura após overhead, coluna, matriz, linha, grade, preservação de cursor e
marcações, navegação, integração com o corpo e o vão visual de dois espaços.
O trabalho deve ajustar somente o comportamento necessário ao contrato desta
ADR, evitando reescrever esses subsistemas.

### 3.1 Causa de integração descoberta por `MV-H0060-001`

O diagnóstico P02 confirmou que o fluxo TTY obtém e propaga corretamente o
novo par físico de largura e altura. A falha está na fronteira de
`renderizar_tela`:

- `l_corpo_disponivel` registra a altura física reservada ao corpo depois de
  descontar cabeçalho e barra de menus;
- `_renderizar_container` pode materializar o corpo subjacente com altura
  natural superior a essa cota;
- com um pop-up aberto, a sobreposição recebe atualmente a quantidade natural
  de linhas do bloco materializado;
- o pop-up escolhe sua formação usando essa altura natural excedente;
- a verificação final compara o corpo com `l_corpo_disponivel`, detecta o
  excesso e produz `RenderizadorErro`;
- o runtime classifica a insuficiência e apresenta o quadro vigente de
  terminal pequeno.

Assim, a altura natural do corpo materializado e a altura física
`l_corpo_disponivel` são grandezas distintas. A primeira não pode ser usada
como espaço fictício para a geometria do pop-up. Em `80x18`, por exemplo, a
área física do corpo observada foi de 12 linhas, mas o pop-up recebeu 14 e
permaneceu em coluna quando uma matriz era fisicamente válida. Em `77x14`, a
área física foi de 8 linhas, mas o pop-up recebeu 12 e escolheu matriz quando
a formação fisicamente válida era linha. Esses valores são pontos de partida
diagnósticos, não dimensões normativas.

## 4. Arquivos previstos para alteração

### 4.1 Implementação

- `tela/renderizacao/popup.py`
- `tela/renderizacao/tela.py`

As áreas focais são `_colunas_formacao`, `_selecionar_formacao`,
`_grade_para_formacao`, `_layout_popup_marcacao` e a materialização das linhas
em `renderizar_popup`. A navegação em `_navegar_marcacao` só deve ser alterada
se a nova grade exigir a correção necessária para manter as regras já
vigentes; não deve receber uma semântica nova.

Em `tela/renderizacao/tela.py`, a área focal é `renderizar_tela`, estritamente
na fronteira entre o cálculo de `l_corpo_disponivel`, a materialização do
corpo, a chamada a `sobrepor_no_corpo` e a verificação final de ocupação. A
implementação deve assegurar que, quando `popup is not None`, o bloco físico
usado para a sobreposição represente exatamente a área reservada ao corpo e o
layout do pop-up receba essa altura física real.

Não alterar o dispatcher geral de resize nem instalar tratamento paralelo de
`SIGWINCH`. Não redefinir genericamente a altura natural de console,
dashboard, lançador, grupo ou outro elemento. A especialização de
`tela/renderizacao/tela.py` é autorizada somente para a composição com pop-up
aberto. Sem pop-up, a política geral de composição, excesso e terminal
pequeno permanece inalterada.

`tela/renderizacao/popup.py` já contém a implementação aprovada das formações.
Não alterá-lo novamente sem necessidade demonstrada pela integração.

### 4.2 Testes

- `tela/teste_popup.py`: ampliar os helpers e os testes unitários focais de
  geometria, formação, grade, navegação, marcação e recomposição.
- `demo/teste_demo_popup.py`: ampliar a demonstração runtime dos acionamentos
  `popup_lista_exclusiva` e `popup_lista_multipla`, usando dimensões explícitas
  para verificar a recomposição e o retorno reversível da mesma instância.
- `tela/testes_renderizador/integracao.py`: arquivo canônico existente para a
  fronteira de `renderizar_tela`; acrescentar a regressão focal da área física
  do corpo com pop-up e a proteção do comportamento anterior sem pop-up.

### 4.3 Fixture/demonstração

Existe a fixture focal:

- `demo/fixtures/h0058_popup_lista_marcacao.py`

Ela já fornece seis itens determinísticos e as políticas
`marcacao: exclusiva` e `marcacao: multipla`, e é carregada pela demonstração
existente. Ela é suficiente para exercitar coluna, matriz com maximização de
colunas, linha e recuperação por aumento da área, pois as dimensões são
fornecidas pelo renderer/demonstração. Portanto, não criar nova fixture, não
alterar essa fixture e não alterar `config/telas/demo/demo.json`; adicionar a
cobertura dimensional nos testes focais existentes.

## 5. Comportamento normativo

### 5.1 Coluna

Usar `coluna` sempre que todos os itens couberem integralmente em uma única
coluna: cada item deve ocupar uma linha física e a largura do item mais largo
deve caber na largura útil. A coluna é a formação preferencial e deve ser
tentada antes de qualquer matriz, mesmo que uma matriz também caiba.

### 5.2 Matriz

Só avaliar `matriz` depois que a coluna não couber e somente quando a área
disponível aos itens tiver pelo menos duas linhas físicas.

Para cada candidata de matriz que couber integralmente:

1. particionar os IDs em colunas verticais, da ordem lógica para a esquerda
   para a direita;
2. materializar as linhas lendo a primeira posição de cada coluna, depois a
   segunda e assim por diante;
3. rejeitar qualquer candidata com menos de duas linhas físicas;
4. verificar a largura usando a largura máxima dos itens reais de cada coluna
   e o vão horizontal de exatamente dois espaços;
5. comparar candidatas pela quantidade de colunas efetivamente ocupadas por
   itens reais;
6. escolher a candidata com o maior número real de colunas ocupadas.

Não retornar a primeira candidata que passar no encaixe. A quantidade nominal
solicitada ao particionamento não é o critério de escolha.

Uma matriz nunca pode representar apenas uma linha física. Com `n` itens, uma
candidata que resulte em uma linha deve ser descartada como matriz, mesmo que
sua largura caiba.

O preenchimento vertical por colunas e a ordem lógica devem ser preservados.
Não preencher células inexistentes com valores artificiais para uniformizar a
grade.

### 5.3 Linha

`linha` é uma formação distinta de `matriz` e só pode ser escolhida quando a
área disponível aos itens comportar exatamente uma linha física (`linhas
disponíveis == 1`) e todos os itens couberem integralmente nessa linha.

Se houver duas ou mais linhas disponíveis e existir uma matriz válida, a linha
não pode ser escolhida. Mesmo que nenhuma matriz válida caiba e a soma dos
itens caiba em uma linha, a implementação não deve usar linha como fallback
antecipado quando houver mais de uma linha física disponível.

### 5.4 Quadro mínimo de terminal pequeno

Se a coluna não couber, não houver matriz válida nas condições normativas e a
linha não puder ser usada, propagar a insuficiência geométrica para o fluxo
geral já vigente, que materializa o quadro mínimo de terminal pequeno.

Não criar quadro alternativo dentro do pop-up. Não adicionar paginação,
truncamento, reticências, placeholders ou redução silenciosa dos espaçamentos
para impedir esse resultado.

## 6. Algoritmo comportamental esperado

O algoritmo pode preservar as funções e estruturas atuais. A alteração
obrigatória é o comportamento observável:

1. obter uma largura física integral para cada item real, usando a
   representação completa vigente;
2. calcular largura útil, linhas da instrução, linhas dos chips e overhead
   real do pop-up;
3. calcular `linhas_disponiveis` depois de descontar o overhead;
4. tentar coluna;
5. se necessário, avaliar todas as candidatas de matriz permitidas, retendo
   a candidata que maximize as colunas reais ocupadas e que satisfaça largura,
   altura e mínimo de duas linhas;
6. somente se `linhas_disponiveis == 1`, avaliar linha;
7. se nenhuma formação permitida couber, deixar o fluxo geral aplicar o
   quadro mínimo vigente;
8. materializar `colunas` e `grade` a partir da mesma candidata escolhida,
   preservando os IDs reais;
9. reconciliar apenas a validade do cursor e das marcações por ID, sem
   recalcular a seleção a partir de uma posição física;
10. materializar a saída usando as mesmas larguras e o mesmo vão usados no
    encaixe.

O particionamento deve ser verificável sem impor uma solução algorítmica
específica. Depois de formar cada candidata, a implementação deve poder
demonstrar que:

- toda coluna materializada é não vazia;
- a concatenação das colunas, da esquerda para a direita e de cima para
  baixo dentro de cada coluna, é exatamente a sequência de IDs de entrada;
- cada ID aparece uma única vez;
- a grade é a leitura horizontal dessas colunas, omitindo somente posições que
  não existem, sem criar placeholder;
- a contagem usada na maximização é `len(colunas efetivamente não vazias)`,
  nunca a quantidade nominal pedida ao particionador.

Se uma rotina intermediária produzir coluna vazia ou quantidade nominal
artificial, a candidata deve ser normalizada/rejeitada antes da comparação,
sem contabilizar a coluna vazia e sem deixá-la chegar à grade ou à navegação.

## 7. Critérios de encaixe

Cada item permanece em exatamente uma linha física. Não aceitar wrapping,
truncamento ou reticências no item.

A largura integral de cada item deve continuar considerando:

- indicador de cursor;
- indicador de marcação;
- separação interna vigente;
- texto integral do item.

Para uma lista de larguras `W` e vão `G = 2`:

- coluna: cabe quando `max(W)` cabe na largura útil e o número de itens cabe
  nas linhas disponíveis;
- matriz: cabe quando o máximo das alturas das colunas cabe nas linhas
  disponíveis e a soma das larguras máximas das colunas mais `G` entre cada
  par de colunas cabe na largura útil;
- linha: cabe quando a soma das larguras integrais mais `G` entre cada par de
  itens cabe na largura útil e existe exatamente uma linha disponível.

O `G = 2` deve ser uma constante interna compartilhada pela decisão de encaixe
e pela materialização das formações de itens. O mesmo valor deve aparecer:

- entre colunas da matriz no cálculo de largura;
- entre itens da linha no cálculo de largura;
- entre textos de itens na saída da matriz;
- entre textos de itens na saída da linha.

Não introduzir literais divergentes para cálculo e renderização. O vão entre
chips continua sujeito à regra existente dos chips; não confundir o layout de
chips com a formação dos itens.

A altura disponível deve ser obtida após descontar o overhead real do pop-up:

- moldura;
- espaçamento superior;
- todas as linhas da instrução depois de seu wrapping;
- espaçamento entre conteúdo e chips;
- todas as linhas ocupadas pelos chips;
- espaçamento inferior.

O wrapping continua permitido somente à instrução e à distribuição dos chips,
conforme o contrato. Um item maior que a largura útil deve continuar levando à
insuficiência geométrica vigente; não pode ser diminuído, truncado ou dividido.

## 8. Invariantes e preservação de estado

Durante toda recomposição:

- a instância de `PopupInstancia` permanece a mesma, sem fechar e reabrir o
  pop-up;
- o envelope de conteúdo permanece imutável;
- a ordem lógica da lista permanece a ordem de entrada;
- cada ID continua presente exatamente uma vez na representação física válida;
- `cursor_id` é preservado por ID;
- `marcados` é preservado por ID e continua ordenado pela ordem lógica;
- a seleção não é reconstruída a partir da linha/coluna anterior;
- a marcação exclusiva continua exatamente uma marcação válida;
- a marcação múltipla continua aceitando zero a N marcações;
- a confirmação continua produzindo o mesmo contrato `CONFIRMADO`;
- `Esc` continua produzindo exatamente `ABORTADO`, sem payload;
- nenhuma formação materializa célula ou item vazio navegável.

Uma recomposição pode substituir `formacao`, `colunas` e `grade`, mas não pode
substituir a identidade lógica da instância nem os IDs do estado vivo.

## 9. Navegação

Manter exatamente as regras vigentes sobre a grade resultante:

- `coluna`: `↑` e `↓` navegam toroidalmente na única coluna; `←` e `→`
  retornam `SEM_MOVIMENTO`;
- `linha`: `←` e `→` navegam toroidalmente na única linha; `↑` e `↓`
  retornam `SEM_MOVIMENTO`;
- `matriz`: `←` e `→` navegam toroidalmente somente entre itens ocupados da
  mesma linha; `↑` e `↓` navegam toroidalmente somente entre itens ocupados
  da mesma coluna;
- células inexistentes não são destinos;
- não há compensação diagonal ao encontrar uma célula inexistente;
- um eixo sem outro item ocupado retorna `SEM_MOVIMENTO`.

Após uma recomposição, a posição física do cursor deve ser encontrada pelo
`cursor_id` preservado e pela nova topologia; nunca pelo índice físico antigo.
As mesmas regras geométricas valem para `marcacao: exclusiva` e
`marcacao: multipla`, sem converter a primeira em seleção única de console.

## 10. Resize e transições obrigatórias

A formação deve ser recalculada em cada novo par válido de dimensões recebido
pelo fluxo geral já existente. O código não deve instalar mecanismo paralelo
de `SIGWINCH`, nem manter uma política local concorrente de dimensões.

A recomposição deve ser reversível pela aplicação dos mesmos critérios:

```text
linha → matriz
matriz → coluna
linha → matriz → coluna
```

Também deve ser possível permanecer na formação atual quando o novo par ainda
for suficiente para ela. Dimensões inválidas continuam sob a política geral
de últimas dimensões válidas; isso não deve ser reinventado no pop-up.

O crescimento do terminal não cria nova instância, não restaura marcações do
envelope e não move o cursor para o primeiro item. Apenas recalcula a forma
física e redesenha.

### 10.1 Integração obrigatória da altura física do corpo

Quando houver pop-up aberto, `renderizar_tela` deve distinguir explicitamente:

- a altura natural produzida pela materialização do corpo subjacente;
- a altura física `l_corpo_disponivel` reservada pelo renderer.

A área de referência fornecida ao pop-up deve corresponder a
`l_corpo_disponivel`, e o bloco sobre o qual a caixa é sobreposta deve
representar exatamente essa mesma área física. Conteúdo natural excedente do
corpo não pode aumentar as linhas disponíveis usadas por
`_layout_popup_marcacao`. A saída final tampouco pode aceitar um corpo maior
que a cota reservada.

A implementação não deve simplesmente desativar ou contornar a verificação
final de excesso. Deve reconciliar a materialização física usada pela
sobreposição com a cota já calculada, preservando as invariantes de largura e
altura do quadro. Este handoff não impõe uma técnica interna específica de
recorte, recomposição ou projeção do corpo: exige apenas que nenhum conteúdo
do pop-up, instrução, chip ou item seja truncado e que a área física entregue
ao layout seja verdadeira.

Se nenhuma formação completa couber nessa área física, a insuficiência deve
continuar propagando para o quadro vigente de terminal pequeno. Se matriz ou
linha couber, a altura natural excedente do corpo subjacente não pode fazer o
quadro mínimo prevalecer.

## 11. Fronteiras negativas

O trabalho não pode:

- transformar o pop-up em `console`;
- usar a capacidade declarativa `distribuicao_matricial` de elementos
  funcionais;
- alterar pop-up `tipo: texto`;
- alterar contrato de abertura ou envelope de conteúdo;
- alterar os resultados `CONFIRMADO` ou `ABORTADO`;
- alterar confirmação por Enter, aborto por Esc ou ação de negócio;
- alterar chips, área própria de chips ou aparência universal dos chips;
- alterar estilo, centralização universal ou a política geral de composição
  do corpo sem pop-up;
- redefinir genericamente a altura natural de consoles, dashboards,
  lançadores, grupos ou outros elementos;
- ocultar a verificação final de excesso ou aceitar composição fisicamente
  maior que `l_corpo_disponivel`;
- introduzir paginação, truncamento, reticências ou placeholders;
- reduzir silenciosamente espaçamentos declarados;
- mudar a política geral de terminal pequeno;
- mudar a semântica de `marcacao: exclusiva` ou `marcacao: multipla`;
- criar tratamento local ou paralelo para `SIGWINCH`;
- restaurar a regra antiga de escolher a primeira/menor matriz;
- contar colunas vazias, células artificiais ou quantidade nominal não ocupada.

## 12. Testes automatizados obrigatórios

Ampliar os testes focais existentes, preferencialmente mantendo os helpers de
declaração, conteúdo e estilo já presentes em `tela/teste_popup.py`, para
cobrir no mínimo:

1. coluna permanece enquanto todos os itens cabem verticalmente;
2. redução de altura força coluna → matriz;
3. entre várias matrizes possíveis, é escolhida a com maior número de colunas
   fisicamente ocupadas que cabe;
4. matriz nunca possui apenas uma linha;
5. coluna vazia ou quantidade nominal artificial não aumenta a contagem usada
   na escolha;
6. preenchimento da matriz permanece vertical por colunas e preserva a ordem;
7. exatamente uma linha disponível produz linha quando todos os itens cabem;
8. linha não é escolhida quando há mais de uma linha disponível e existe
   matriz válida;
9. quando coluna, matriz e linha não cabem, o resultado segue o fluxo vigente
   de terminal pequeno;
10. crescimento do terminal permite linha → matriz;
11. crescimento adicional permite matriz → coluna;
12. resize preserva cursor por ID;
13. resize preserva marcações em `marcacao: multipla`;
14. resize preserva a marca única em `marcacao: exclusiva`;
15. matriz mantém navegação toroidal horizontal e vertical;
16. linha mantém navegação toroidal horizontal;
17. coluna mantém navegação toroidal vertical;
18. eixo sem outro item retorna `SEM_MOVIMENTO`;
19. vão de dois espaços participa do cálculo de largura;
20. vão de dois espaços é materializado na saída;
21. item mais largo considera indicadores visuais e texto integral;
22. wrapping adicional da instrução ou distribuição dos chips reduz
    corretamente as linhas disponíveis aos itens;
23. o novo comportamento não introduz truncamento, paginação ou placeholder.

Os casos 10–14 devem afirmar a identidade da instância e comparar IDs do
estado vivo antes e depois da recomposição. Os casos 15–18 devem usar grades
com e sem células ocupadas no último trecho para comprovar a ausência de
destino artificial e de compensação diagonal. Os casos 19–22 devem validar o
mesmo layout calculado e materializado, não apenas a largura de uma string
isolada.

Em `demo/teste_demo_popup.py`, incluir a sequência focal usando a fixture
H-0058 para demonstrar coluna, matriz maximizada, linha e recuperação por
área crescente, preservando a mesma instância. Não é necessário criar arquivo
de fixture novo.

### 12.1 Regressão obrigatória de integração de `MV-H0060-001`

Adicionar uma regressão que atravesse `renderizar_tela` ou o caminho público
imediatamente superior que reproduza a mesma decisão física. Chamar somente
`_selecionar_formacao`, `_layout_popup_marcacao` ou `geometria_popup` não é
cobertura suficiente.

O arquivo canônico do compositor é
`tela/testes_renderizador/integracao.py`. Ele deve proteger a concordância
entre `l_corpo_disponivel`, o bloco físico de sobreposição e a verificação
final, incluindo um caso equivalente sem pop-up que confirme a política
anterior. `demo/teste_demo_popup.py` deve atravessar `_resolver_conteudo` ou
`renderizar_estado`, usando a fixture H-0058 e a mesma instância aberta, para
comprovar o resultado observável do runtime.

A regressão deve provar objetivamente os três estados abaixo para
`marcacao: exclusiva` e `marcacao: multipla` quando aplicável:

1. **Matriz:** a coluna não cabe na área física real, uma matriz válida cabe,
   o fluxo completo materializa os seis itens em matriz e não apresenta
   `Terminal pequeno demais`. `80x18` pode ser usado como ponto de partida.
2. **Linha:** coluna e matriz não cabem na área física real, todos os itens
   cabem em uma linha, o fluxo completo materializa a linha e não apresenta
   `Terminal pequeno demais`. `77x14` pode ser usado como ponto de partida.
3. **Terminal pequeno real:** nenhuma das três formações completas cabe; o
   fluxo produz por igualdade o quadro vigente de terminal pequeno, sem
   representação parcial do pop-up.

As dimensões finais do teste podem ser ajustadas para determinismo, desde que
as pré-condições geométricas sejam afirmadas. Os casos devem também confirmar
que o quadro final respeita a largura e a altura físicas e que a identidade da
instância, cursor e marcações por ID são preservados entre recomposições.

## 13. Critérios objetivos de aceite

O handoff de implementação será aceito somente quando:

- a seleção obedecer inequivocamente `coluna → matriz → linha → terminal
  pequeno`;
- coluna continuar preferencial sempre que couber;
- matriz só for considerada com pelo menos duas linhas físicas;
- entre matrizes válidas a comparação usar somente colunas reais ocupadas e
  escolher a maior quantidade;
- o particionamento preservar todos os IDs uma vez, a ordem e o preenchimento
  vertical, sem placeholder ou coluna vazia;
- linha for independente e só ocorrer com exatamente uma linha disponível e
  todos os itens cabendo;
- o vão de dois espaços participar do cálculo e aparecer na saída;
- largura integral dos itens incluir indicadores, separação e texto completo;
- overhead incluir instrução embrulhada, chips distribuídos e todos os
  espaçamentos declarados;
- recomposição ocorrer por dimensões válidas no fluxo geral e for reversível;
- cursor, marcações e identidade da instância forem preservados por ID;
- navegação conservar os toroides por eixo, células inexistentes não forem
  destinos e eixo unitário retornar `SEM_MOVIMENTO`;
- o quadro mínimo geral continuar sendo usado quando nenhuma formação couber;
- `renderizar_tela` usar `l_corpo_disponivel` como autoridade vertical da
  geometria do pop-up, sem entregar a ele altura natural excedente;
- dimensão física que comporte matriz não resultar em terminal pequeno apenas
  porque o corpo natural é mais alto;
- dimensão física que comporte linha não resultar em terminal pequeno apenas
  porque o corpo natural é mais alto;
- o bloco físico de sobreposição representar exatamente a área reservada e a
  verificação final de excesso continuar ativa;
- o caminho sem pop-up manter o comportamento anterior de composição e
  terminal pequeno;
- nenhuma forma de truncamento, recorte de conteúdo do pop-up, paginação,
  remoção de item ou redução silenciosa de espaçamento ser introduzida;
- pop-up textual, chips, contratos de resultado, política de terminal pequeno
  e fronteiras negativas permanecerem inalterados;
- os testes diretos anteriores de `tela/teste_popup.py` continuarem passando;
- a regressão de `tela/testes_renderizador/integracao.py` atravessar
  `renderizar_tela` e a de `demo/teste_demo_popup.py` atravessar o caminho
  runtime responsável por `MV-H0060-001`.

## 14. Comandos focais de validação

Executar, na raiz do repositório, após a implementação:

```bash
python -m pytest tela/teste_popup.py -q
python -m pytest tela/testes_renderizador/integracao.py -q
python -m pytest demo/teste_demo_popup.py -q
python -m pytest -q
git diff --check
```

O primeiro comando preserva as regras algorítmicas, geométricas, de navegação
e de estado já aprovadas. O segundo comprova a fronteira de
`renderizar_tela`, inclusive a não regressão sem pop-up. O terceiro comprova a
demonstração com a fixture existente e o fluxo de resize da mesma instância.
O conjunto completo protege os demais consumidores do compositor.

## 15. Condições de bloqueio

Interromper a implementação e reportar exatamente o bloqueio aplicável, sem
resolver autonomamente, se ocorrer qualquer uma destas condições:

- `BLOCKED_USER_DECISION`: surgir uma escolha normativa não contida na
  ADR-0045 ou no contrato aplicado;
- `BLOCKED_DOCUMENTATION`: a documentação vigente ficar contraditória em
  ponto que impeça determinar uma implementação compatível;
- `BLOCKED_HANDOFF_DECOMPOSITION`: a aplicação exigir mais de um subsistema
  independente ou mais de um handoff material, especialmente fora da
  fronteira do pop-up e do fluxo geral de resize.

Não são bloqueios: a necessidade de trocar a ordem de avaliação das
candidatas, compartilhar a constante de dois espaços, ampliar os testes
focais, reutilizar a fixture H-0058 ou especializar `renderizar_tela` para que
um pop-up aberto receba `l_corpo_disponivel`. Essas ações estão contidas nesta
ADR e neste patch do handoff.

## 16. Definição de conclusão

Considerar o `H-0060` concluído quando a alteração de implementação e os
testes previstos neste documento estiverem materializados em uma única etapa,
os comandos focais passarem, a demonstração H-0058 cobrir as quatro situações
dimensionais e todos os critérios de aceite forem satisfeitos.

Não alterar, como parte desta conclusão, contrato, nomenclatura, backlog,
configuração de popup ou política geral de terminal pequeno. Alterar somente
`tela/renderizacao/popup.py` quando houver necessidade demonstrada,
`tela/renderizacao/tela.py` na especialização de integração aqui autorizada e
os três arquivos de testes focais identificados neste handoff.
