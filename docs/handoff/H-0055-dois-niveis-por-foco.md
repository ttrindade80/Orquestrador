# H-0055 — `dois_niveis_por_foco`

## 1. Identificação e estado transportado

```yaml
handoff: H-0055
item: ITEM-0007
capacidade: dois_niveis_por_foco
predecessor_operacional: H-0054
posicao_no_item: ultimo_handoff
etapa: PATCH_HANDOFF
patch: P03
predecessor_documental: H-0055_P02
predecessor_da_etapa: MANUAL_VALIDATION_FAILED
estado: pronto_para_correcao_de_implementacao
adr: ADR-0042
status_da_adr: aceita
qa_da_adr: ADR_APPROVED
aplicacao_documental: concluida
qa_da_aplicacao: ADR_APPLICATION_APPROVED
qa_tecnico_da_implementacao_e_patch_focal: I1_IMPLEMENTATION_APPROVED
achados_corrigidos:
  - MV-H0055-001
  - MV-H0055-002
decisoes_materializadas:
  - D-MULTI-07-P04
  - D-MULTI-08
  - D-MULTI-09
  - demais_decisoes_aplicaveis_da_ADR-0042
paginação: subordinada_a_ADR-0041
```

H-0054 (`selecao_multinivel`) está concluído e aprovado e deve permanecer
preservado como predecessor operacional. Este handoff cobre exclusivamente
`dois_niveis_por_foco`; não reabre H-0054, H-0053, a tentativa multinível
anterior em branch de erro ou qualquer capacidade fora de seu limite.

A decisão explícita do usuário no P02 fecha a materialização inicial sem criar
campo, schema, enum ou política: o JSON de dados da fixture é a fonte do valor
inicial, e o primeiro filho direto listado para cada pai é o filho inicialmente
escolhido na entrada atual da demonstração ou do teste.

O P03 sucede o resultado `MANUAL_VALIDATION_FAILED` da primeira rodada manual e
corrige exclusivamente `MV-H0055-001` e `MV-H0055-002`. A implementação e o
patch focal do carregador já receberam QA técnico `I1_IMPLEMENTATION_APPROVED`;
a correção de implementação preparada por este texto permanece futura. Este
patch é somente documental, não executa implementação, QA ou commit.

## 2. Escopo fechado

### 2.1 Escopo positivo

Aplicar somente a política declarada explicitamente como:

```json
"politica_navegacao": {
  "navegavel": true,
  "tipo": "dois_niveis_por_foco"
}
```

A política tem exatamente dois níveis:

- nível 1: pais;
- nível 2: filhos diretos de cada pai.

Um terceiro nível é inválido e não recebe comportamento funcional nesta
capacidade. A estrutura do conteúdo, a apresentação e o nome da fixture não
podem inferir a política. O campo `tipo` continua sendo o discriminador
canônico de `politica_navegacao`; não criar segunda forma de declaração nem
valor novo.

Todos os pais navegáveis pertencem a um único toroide de pais. Cada pai possui
um toroide próprio de seus filhos diretos. Filhos de pais distintos nunca
compartilham toroide. O toroide de filhos ativo é determinado pelo pai
corrente no nível dos pais.

No nível dos pais, Espaço entra no toroide de filhos do pai corrente. No nível
dos filhos, Esc retorna ao toroide dos pais, preserva a escolha do pai e não
limpa essa escolha. Nesse contexto, Esc não é cancelamento. As setas operam
somente no toroide atualmente ativo: no nível 1, no toroide único de pais; no
nível 2, no toroide próprio do pai corrente.

O despacho contextual de Esc é fechado nos dois níveis: no nível dos filhos,
o chip exibe `[Esc] Voltar` e Esc executa somente o retorno ao toroide dos pais,
preservando todas as escolhas; no nível dos pais, o chip exibe `[Esc] Sair`, não
há retorno de nível e Esc usa a saída vigente, preservando as escolhas. O
rótulo é recalculado a partir do nível ativo e muda junto com a entrada nos
filhos ou o retorno aos pais, sem conservar texto do nível anterior.
O ramo genérico de §23.4 que limpa seleção ativa não se aplica a esta escolha,
porque `politica_selecao: multipla` é apenas compatibilidade declarativa para
`tg`/`[␣]`, enquanto a escolha obrigatória por pai é o mecanismo distinto
fechado por D-MULTI-09. Não se cria cancelamento, Enter ou ação nova.

Cada pai deve possuir exatamente um filho escolhido, de forma exclusiva e
obrigatória. Espaço em outro filho transfere a escolha para esse filho e
remove a escolha do irmão anterior. Espaço no filho já escolhido mantém o
estado e não o remove. Nenhuma interação por Espaço pode deixar o pai sem
filho escolhido. O estado de todos os pais deve continuar independente:
transferir a escolha em um pai não altera a escolha de outro.

Cursor e escolha do filho são mecanismos independentes. Mover o cursor entre
filhos não transfere a escolha; a transferência ocorre somente ao pressionar
Espaço sobre outro filho válido. Pressionar Espaço não move o cursor.

### 2.2 Distinções terminológicas obrigatórias

- **seleção exclusiva obrigatória de filho por pai**: mecanismo deste handoff;
  mantém exatamente uma escolha por pai e só transfere a escolha por Espaço.
- **seleção única**: termo canônico da ADR-0031 para o item sob cursor, que
  muda com o cursor e não representa o mecanismo deste handoff.
- **seleção múltipla**: política existente de conjunto de IDs estáveis,
  independente de cursor e página, usada por H-0054 e por outras capacidades.

O mecanismo deste handoff não será nomeado como `seleção única` nem como
`seleção múltipla`. A apresentação visual de seleção já existente é apenas
reutilizada; não há redefinição de qualquer termo canônico.

### 2.3 Escopo negativo

É proibido neste handoff:

- implementar qualquer parte antes da aprovação posterior deste handoff;
- alterar ADRs, contratos, nomenclaturas, backlog ou H-0054;
- abrir, ler, comparar ou reaproveitar a branch de erro da tentativa anterior;
- admitir terceiro nível, toroide compartilhado entre pais ou toroide global
  de todos os filhos;
- fazer setas atravessarem o toroide ativo, trocarem de nível ou paginarem;
- criar `Pai: filho_ativo`, promoção visual do filho, nova geometria,
  distribuição geométrica de grupos, nova quebra ou nova linguagem visual;
- criar nova semântica de Enter, execução, confirmação, cancelamento,
  persistência, prévia ou qualquer ação posterior à escolha;
- criar política, schema, enum, campo de runtime persistente ou arquitetura
  próprios de H-0055;
- permitir variação de verbosidade, tecla `V` ou chip de mudança de modo;
- criar tecla, chip ou política concorrente de paginação;
- alterar a semântica ou os chips de `arvore_colapsavel` de H-0053;
- transformar a demonstração posterior em aprovação nesta etapa.

## 3. Preservações obrigatórias

### 3.1 Console, foco, cursor e políticas vizinhas

- Tab e Shift+Tab continuam trocando o foco entre consoles focalizáveis;
  somente o console focado recebe as setas e o indicador de item corrente.
- Foco, cursor, escolha do filho e seleção permanecem mecanismos distintos.
- `nivel_unico` preserva quatro setas, toroidalidade por eixo, ignorância de
  células vazias, entrada por foco e demais regras vigentes, sem redesenho.
- `tabela` permanece passiva, sem foco, cursor entre linhas, setas ou `[✥]`;
  declaração incompatível como navegável continua sendo falha focal.
- `arvore_colapsavel` de H-0053 permanece árvore navegável sem seleção:
  ↑/↓ percorrem o visível e Espaço abre/fecha o ramo; seus chips
  `[␣] Expandir`/`[␣] Recolher` não são fundidos com a escolha deste handoff.
- H-0054 permanece com uma topologia multinível única e sua semântica de
  seleção recursiva, incluindo `ec`, `tg`, reconciliação e regressões já
  aprovadas. H-0055 não altera sua fixture, relatório ou implementação.

### 3.2 Apresentação, chips e modo

- A escolha utiliza a apresentação `tg` já existente, com os símbolos e o
  estilo vigentes. `ec` continua sendo o espaço do cursor; `tg` não passa a
  representar cursor.
- Os chips vigentes são preservados: `[✥] Navegar` somente quando aplicável
  ao toroide ativo e à página vigente; `[␣]` e `tg` reutilizam a apresentação
  existente mediante a declaração nominal `politica_selecao: multipla`;
  `[?] Ajuda` sempre presente, ativo e por último; `[Esc] Voltar` aparece no
  toroide de filhos e `[Esc] Sair` no toroide de pais.
- Não criar `[␣] Expandir` ou `[␣] Recolher` para esta política e não usar os
  chips de `arvore_colapsavel` como atalho para escolha.
- D23 permanece obrigatório com a política fixa
  `formato.excesso.politica_modo: somente_nao_verboso`; a tela não oferece
  variação de verbosidade, não declara modo inicial e não apresenta tecla ou
  chip para mudança de modo.
- Preservar a distinção entre `modo normal` e `modo não verboso`, sem
  reconciliá-la, e entre `hierarquia` e o termo concorrente
  `hierarquia_indentada`. Redimensionamento preserva o item lógico corrente e
  recalcula a geometria vigente; não limpa nem reescolhe filhos.
- Se a geometria matricial ou outro modo vigente já for declarado, ele é
  preservado. H-0055 não cria distribuição, colunas, recuos ou alinhamentos.

### 3.3 Paginação

A paginação permanece integralmente subordinada à ADR-0041 e às regras de
paginação limitada já aplicadas:

- `PageUp` é exclusivamente página anterior;
- `PageDown` é exclusivamente próxima página;
- a representação é `[PgUp][PgDn] Páginas`;
- `<`, `>`, `,` e `.` não são aliases, atalhos nem fallback;
- não há wrap entre a primeira e a última página;
- a página é estado independente do console focado;
- setas não trocam de página e o cursor não recebe semântica implícita de
  paginação;
- troca de página e redimensionamento seguem as reconciliações vigentes, sem
  política de página por nível ou por toroide.

## 4. Forma das fixtures e fronteira de dados

Usar a superfície nominal de H-0054 como baseline, ajustada somente para a
política deste handoff. A tela estrutural e o documento externo permanecem
separados e usam apenas os envelopes já contratados:

- `config/telas/demo/h0055_dois_niveis_por_foco.json`: fixture estrutural
  própria, com console focalizável, política declarada explicitamente como
  `dois_niveis_por_foco`, controles vigentes e sem campo novo de filho ativo;
- `config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json`: documento
  externo `tipo: "multinivel"`, apresentação `hierarquia`, dois níveis
  declarados, IDs estáveis, pais e seus filhos diretos, sem resultados físicos
  calculados e sem terceiro nível.

A especificação nominal da fixture estrutural futura deve manter os envelopes
contratados e declarar, no elemento `console`, exatamente os mecanismos já
existentes:

```yaml
politica_navegacao:
  navegavel: true
  tipo: dois_niveis_por_foco
politica_selecao: multipla
politica_paginacao: com
formato:
  excesso:
    politica_modo: somente_nao_verboso
```

`politica_selecao: multipla` é a declaração canônica existente exigida para
reutilizar `tg` e `[␣]`; ela não transforma a escolha obrigatória por pai em
seleção múltipla genérica, não autoriza limpeza por Esc e não cria mecanismo,
enum ou schema novo. `politica_paginacao: com` é a declaração canônica
existente para os controles de paginação.

O documento externo deve permanecer separado e declarar exatamente dois
níveis, preservando `apresentacao: hierarquia` — nunca
`hierarquia_indentada` — e sem resultados físicos:

- nível `pai`, tipo `container`, conteúdo `titulo`, designador existente;
- nível `filho`, tipo `conteudo`, conteúdo `titulo`, sem filhos;
- cinco pais raiz (`pai_01` a `pai_05`), cada um com quatro filhos diretos
  estáveis (`filho_01_01` a `filho_05_04`), sem terceiro nível, IDs duplicados
  ou ausentes.

Os 25 itens lógicos são o mínimo nominal para a fixture demonstrar mais de
uma página sob a paginação vigente. A demonstração deve alcançar pelo menos
duas páginas, acionar `PageDown` e `PageUp` e exibir `[PgUp][PgDn] Páginas`;
não se declara tamanho de página nem paginação por nível, pai ou toroide.

D23 fica fechado pela combinação fixa válida acima: a tela sempre usa modo não
verboso. O campo `formato.excesso.modo_inicial` é proibido em política fixa e
deve estar ausente; a tecla `V` e o chip correspondente não são aplicáveis.
Telas novas ou revisadas continuam obrigadas a declarar `politica_modo`.
`modo normal` e `modo não verboso` permanecem termos coexistentes sem
reconciliação; `hierarquia` não é renomeada.

A decisão inicial obrigatória fica fechada e reproduzível pela ordem semântica
já existente do array de filhos diretos no JSON de dados: para cada pai, o
primeiro filho listado é o valor inicial da escolha. Esse valor vale somente
para a entrada atual da demonstração ou do teste. Durante a execução, a
transferência por Espaço altera apenas o estado de runtime, mantendo exatamente
um filho por pai; o JSON de dados não é reescrito ao sair ou reabrir o sistema.
Persistência futura da escolha runtime no JSON não é implementada nem
antecipada neste ciclo e fica registrada no `ITEM-0026`, que exige
especificação/decisão própria.

## 5. Arquivos autorizados para etapa futura

A lista abaixo é fechada. Nenhuma autorização é dada para um diretório
inteiro, arquivo por proximidade temática ou caminho não listado.

| Caminho exato | Uso autorizado |
|---|---|
| `tela/navegacao.py` | Política explícita, dois níveis, foco, cursor, toroide ativo, setas, Espaço e Esc, preservando as demais políticas. |
| `tela/selecao.py` | Reutilização do estado de escolha e da apresentação `tg`, sem schema ou persistência novos. |
| `tela/renderizador.py` | Integração dos estados existentes de cursor, escolha e chips. |
| `tela/renderizacao/console.py` | Mapa físico e projeção do console, sem nova geometria ou linguagem visual. |
| `tela/renderizacao/conteudo_externo.py` | Renderização da hierarquia existente e distinção entre item lógico e linha física. |
| `tela/carregamento/envelope_pre_adr_0028.py` | Reconciliação focal D23 de H-0055: reconhecer a combinação fixa `somente_nao_verboso` sem `modo_inicial`, mantendo validação estrita e rejeições vigentes. |
| `demo/demo.py` | Associação nominal do cenário H-0055, carregamento separado e despacho das teclas previstas. |
| `tela/teste_navegacao.py` | Testes unitários focais de níveis, toroides, cursor, escolha, Esc, Espaço e regressões. |
| `demo/teste_demo_console.py` | Testes integrados de fixtures separadas, renderização, chips, foco e paginação. |
| `config/telas/demo/h0055_dois_niveis_por_foco.json` | Fixture estrutural nova e exclusiva de H-0055. |
| `config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json` | Documento externo novo e exclusivo de H-0055. |
| `docs/relatorios/IMP-0055-dois-niveis-por-foco.md` | Relatório obrigatório da implementação futura. |

Qualquer necessidade de outro caminho exige parar antes de editar, registrar
o caminho exato, a responsabilidade e o motivo técnico e solicitar
autorização focal. Não criar catálogo genérico nem mover a implementação para
um caminho não autorizado.

## 6. Entrada, fixtures, temporários e saídas

| Categoria | Regra fechada |
|---|---|
| Entrada real | `python demo/demo.py h0055_dois_niveis_por_foco` em TTY real; Tab/Shift+Tab, setas, Espaço, Esc, `?` e, se declarada, PageUp/PageDown. |
| Fixture | Somente os dois arquivos `config/telas/demo/h0055_dois_niveis_por_foco*`; não reutilizar nem alterar fixtures de H-0053/H-0054. |
| Temporário | `NAO_APLICAVEL`; não criar subprocesso, diretório temporário ou arquivo temporário para esta demonstração. Se uma necessidade concreta surgir, ela é bloqueio até autorização. |
| Saída persistente | Somente `docs/relatorios/IMP-0055-dois-niveis-por-foco.md` na implementação futura. O valor inicial é lido do JSON de dados; a escolha em runtime não é persistida, o JSON não é alterado e o estado é descartado ao sair/recarregar. Persistência futura pertence ao `ITEM-0026`. |
| Saída de teste | `NAO_APLICAVEL`; testes não gravam snapshot, relatório, quadro ou fixture persistente. |

## 7. Arquivos preservados

Preservar sem alteração as autoridades documentais:

- `docs/adr/ADR-0042-navegacao-multinivel-do-console.md`;
- `docs/adr/ADR-0041-paginacao-universal-por-pageup-e-pagedown.md`;
- `docs/adr/ADR-0043-ajuda-universal-e-chip-contextual-de-expandir-recolher.md`;
- `docs/contratos/contrato_console.md`;
- `docs/contratos/contrato_json_console.md`;
- `docs/nomenclatura/32_CONSOLE.md`;
- `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md`;
- `docs/backlog.md`.

Preservar também H-0054 e H-0053, incluindo, no mínimo, o handoff de H-0054,
as duas fixtures `config/telas/demo/h0054_selecao_multinivel.json` e
`config/telas/demo/h0054_selecao_multinivel_conteudo.json`, as duas fixtures
`config/telas/demo/h0053_arvore_colapsavel.json` e
`config/telas/demo/h0053_arvore_colapsavel_conteudo.json`, e o relatório de
implementação `docs/relatorios/IMP-0054-selecao-multinivel.md`. Todos os
demais artefatos existentes de H-0053/H-0054 e todo caminho não listado na
seção 5 também permanecem fora de alteração. Não alterar outros relatórios.

## 8. Critérios de aceite para etapa posterior

### 8.1 Comportamentais

- A política é selecionada somente por `politica_navegacao.tipo` explícito;
  o conteúdo não a infere.
- Há exatamente dois níveis; terceiro nível é rejeitado como configuração
  inválida, sem fallback funcional.
- Todos os pais navegáveis percorrem um único toroide com wrap próprio.
- Cada pai possui um toroide independente de filhos com wrap próprio; nenhum
  filho de pais diferentes entra no mesmo toroide.
- O pai corrente determina o toroide de filhos ativo; mudar o pai corrente
  não transfere escolha nem mistura cursores de pais.
- Espaço no nível dos pais entra nos filhos do pai corrente; Esc no nível dos
  filhos retorna aos pais, preservando a escolha e sem cancelamento.
- O rótulo contextual acompanha o nível ativo: `[Esc] Voltar` no toroide de
  filhos e `[Esc] Sair` no toroide de pais; retornar aos pais atualiza o rótulo
  sem limpar escolhas.
- As setas só movimentam o toroide ativo e não paginam, mudam de nível ou
  atravessam para outro pai.
- Cada pai mantém exatamente um filho escolhido em todo estado válido.
- Espaço em outro filho transfere a escolha exclusivamente para ele; Espaço
  no filho escolhido mantém a escolha; nenhuma ação por Espaço deixa o pai
  sem escolha.
- Mover o cursor não transfere a escolha; somente Espaço sobre outro filho
  válido o faz; Espaço não move o cursor.
- `ec`, `tg`, foco, cursor, escolha e página permanecem estados distintos.
- `[✥]`, `[␣]` vigente, `[Esc]`, `[?] Ajuda` e a apresentação `tg` conservam
  suas regras e posições aplicáveis, sem chip novo; a declaração estrutural
  de compatibilidade é nominalmente `politica_selecao: multipla`.
- D23 é válido na fixture: `formato.excesso.politica_modo` é
  `somente_nao_verboso`, não há `formato.excesso.modo_inicial`, tecla `V` nem
  chip correspondente; a distinção `modo normal` × `modo não verboso` e o nome
  `hierarquia` permanecem preservados.
- A exceção focal em `tela/carregamento/envelope_pre_adr_0028.py` reconhece
  essa combinação fixa válida somente para a reconciliação D23 autorizada de
  H-0055, mantendo validação estrita e rejeições vigentes.
- Redimensionamento preserva o item lógico corrente e recalcula somente a
  geometria vigente, sem limpar ou reescolher filhos.
- H-0052, H-0053 e H-0054 continuam comportando-se conforme suas autoridades;
  `nivel_unico` e `tabela` não sofrem regressão.
- Paginação mantém `politica_paginacao: com`, `PageUp`/`PageDown`,
  `[PgUp][PgDn] Páginas`, topologia limitada, independência por console e
  seleção/estado entre páginas conforme as autoridades, sem paginação por
  setas; a fixture tem 25 itens lógicos e deve exercitar ao menos duas
  páginas.

### 8.2 Negativos

- Terceiro nível, pai sem filho válido ou IDs ausentes/duplicados que impeçam
  a escolha são bloqueios; não criar fallback, schema ou decisão nova.
- Filho de um pai não pode aparecer no toroide de outro pai.
- Setas não podem escapar do toroide ativo, transferir escolha, executar ação
  ou trocar página.
- Espaço no filho escolhido não pode removê-lo; nenhum pai pode ficar sem
  filho escolhido por essa interação.
- Movimento de cursor, Tab, Shift+Tab, redimensionamento, PageUp ou PageDown
  não pode transferir a escolha por si só.
- Esc no nível dos filhos não pode limpar escolha, cancelar, executar ou
  abrir outra tela.
- No toroide de filhos, o chip de Esc não pode conservar o rótulo `Sair`; no
  toroide de pais, não pode conservar o rótulo `Voltar`.
- Esc no nível dos pais deve usar somente o retorno/saída já existente do
  §23.4, preservar a escolha obrigatória e não passar pelo ramo genérico de
  limpeza de seleção; isso não cria cancelamento novo.
- A escolha exclusiva obrigatória não pode produzir o rótulo `[Esc] Limpar`.
- A fixture H-0055 não pode declarar `formato.excesso.modo_inicial`, tecla `V`
  ou chip de mudança de modo, nem aceitar política de modo diferente de
  `somente_nao_verboso`.
- Na entrada atual, cada pai deve iniciar com o primeiro filho direto listado
  no JSON de dados; Espaço transfere a escolha somente em runtime, e sair ou
  reabrir não altera o JSON nem persiste a escolha.
- Não pode existir `Pai: filho_ativo`, novo símbolo, estado parcial, política
  concorrente de paginação, nova geometria ou semântica de Enter.
- A tentativa anterior em branch de erro e qualquer caminho não autorizado
  não podem participar da implementação, dos testes ou da demonstração.

## 9. Testes e demonstração reproduzíveis

Adicionar testes somente nos dois arquivos de teste autorizados. Os testes
focais devem cobrir: declaração explícita e terceiro nível inválido; wrap do
toroide de pais; wrap de cada toroide de filhos; isolamento entre pais; entrada
por Espaço e retorno por Esc; transferência e manutenção da escolha; cursor
movido sem transferência; foco entre consoles; preservação em
redimensionamento; chips e `tg`; paginação universal; e regressões de H-0052,
H-0053 e H-0054. Incluir regressões automatizadas do rótulo `[Esc] Sair` nos
pais, `[Esc] Voltar` nos filhos e da atualização nos dois sentidos, sempre sem
`[Esc] Limpar`. Cobrir também a fixture fixa `somente_nao_verboso`, sem campo de
modo inicial e sem tecla ou chip `V`, e a exceção focal do carregador que aceita
essa combinação mantendo as rejeições vigentes. Não converter esses testes em
QA geral.

A demonstração posterior deve executar em TTY real:

```text
python demo/demo.py h0055_dois_niveis_por_foco
```

Ela deve demonstrar, sem declarar aprovação nesta etapa: foco no console,
percurso e wrap dos pais; Espaço sobre um pai e percurso exclusivo de seus
filhos; transferência para outro filho e manutenção ao repetir Espaço;
movimento do cursor sem transferência; Esc de retorno com escolha preservada;
troca para outro pai sem compartilhamento de toroide; `[Esc] Voltar` enquanto
os filhos estiverem ativos e `[Esc] Sair` após o retorno aos pais; ausência de
controle de mudança de modo sob D23 fixo; e, com pelo menos duas páginas,
PageDown e PageUp com `[PgUp][PgDn] Páginas` visível. A nova validação TTY real,
QA, correção de implementação e relatório de implementação pertencem a etapas
posteriores.

## 10. Relatório esperado, exceções e bloqueios

O relatório obrigatório da implementação futura é:

`docs/relatorios/IMP-0055-dois-niveis-por-foco.md`

Bloqueios objetivos são: política ausente, não objeto ou com tipo diferente;
documento externo ausente
ou semanticamente inválido; terceiro nível; falta de IDs estáveis; pai sem
filho elegível; impossibilidade de representar a escolha exclusiva com a
estrutura e a apresentação existentes; impossibilidade de compartilhar a
mesma projeção lógica entre navegação, mapa físico e renderização;
impossibilidade de produzir as duas páginas com a fixture nominal;
necessidade de criar schema, arquitetura, geometria, linguagem visual,
persistência, Enter, execução, confirmação, cancelamento ou paginação nova;
regressão de H-0052/H-0053/H-0054; necessidade de alterar autoridade ou
caminho preservado; ou necessidade de editar arquivo fora da seção 5.

A única exceção focal de caminho acrescentada pelo P03 é
`tela/carregamento/envelope_pre_adr_0028.py`, exclusivamente para reconhecer a
combinação D23 fixa válida de H-0055, sem relaxar a validação ou as rejeições
vigentes. Necessidade de ampliar essa exceção, admitir variação de modo, manter
campo de modo inicial em política fixa ou usar outro caminho é bloqueio.

Nenhum desses bloqueios deve ser resolvido por decisão implícita. Registrar o
caminho e a responsabilidade exatos, interromper a edição fora da lista e
solicitar autorização focal quando aplicável.
