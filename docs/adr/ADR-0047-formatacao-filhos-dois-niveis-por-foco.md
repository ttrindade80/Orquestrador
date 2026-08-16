---
name: ADR-0047-formatacao-filhos-dois-niveis-por-foco
description: "Fecha a evolução exclusiva de apresentação/formatação dos filhos da política canônica dois_niveis_por_foco (ADR-0042) — tabulação declarativa min/max entre pai e filhos, unidade inteira do filho deslocada a partir de ec, designadores permitidos pelos mecanismos já existentes, apresentação tabular local de filhos em colunas alinhadas globalmente, espaçamento min/max entre colunas, quebra de conteúdo em múltiplas linhas preservando o item lógico, comportamento em resize, especialização da tela de Estilo (h0063) sem alteração de conteúdo, e aplicação futura às demais telas de dois_niveis_por_foco — sem redesenhar a navegação, a seleção exclusiva obrigatória de filho por pai ou qualquer outro comportamento já fechado pela ADR-0042"
metadata:
  type: adr
  status: aceita_e_aplicada
  id: ADR-0047
  data: "2026-08-15"
  substitui: null
rastreabilidade:
  decisao_usuario: "D-DNF-01 a D-DNF-11 — evolução exclusiva de apresentação/formatação dos filhos de dois_niveis_por_foco (ADR-0042), preservando integralmente sua semântica de navegação e seleção: tabulação declarativa min/max entre pai e filhos (5 a 10 espaços para as telas desta atividade), unidade inteira do filho deslocada a partir de ec (cursor, toggle, designador e conteúdo movidos juntos), designadores permitidos pelos mecanismos já existentes do schema (decimal composto, alfabético maiúsculo com sufixo, nenhum), apresentação tabular local de filhos em colunas alinhadas sem cabeçalho/borda/título próprios, largura de coluna determinada pelo conteúdo e nunca persistida como geometria calculada, alinhamento global das colunas entre todos os filhos do console independentemente do pai corrente, espaçamento declarativo min/max entre colunas (3 a 8 espaços para a configuração desta atividade), quebra de conteúdo em múltiplas linhas físicas preservando o item lógico e as regras vigentes de cursor em linha de continuação, comportamento em resize recalculando geometria sem perder o item lógico, especialização da tela de Estilo (h0063) para designador nenhum e apresentação tabular local de 2 colunas (texto/nome existente e exemplo visual existente) sem alterar presets, textos, exemplos, símbolos, ordem, conteúdo, valores de estilo, candidato, baseline, aplicação, persistência ou publicação, e aplicação futura da capacidade a todas as telas existentes de dois_niveis_por_foco na etapa de aplicação/handoff/implementação"
  rfc_origem: null
  issues_relacionadas: []
  contratos_afetados:
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_json_console.md
  handoffs_bloqueados: []
---

# ADR-0047 — Formatação dos filhos de `dois_niveis_por_foco`

## 1. Status

`aceita e aplicada`

Esta ADR foi criada a partir de onze decisões fechadas fornecidas ao autor
documental (D-DNF-01 a D-DNF-11). Nenhuma delas foi escolhida, reaberta ou
alterada por este documento. Não há arquitetura, schema, política,
representação visual ou fluxo de execução introduzido além do que foi
explicitamente decidido.

QA da ADR: `ADR_APPROVED`, após correção de fronteira registrada em §4.13
(QA-ADR-0047-001, resolvido). Aplicação documental concluída e aprovada:
`ADR_APPLICATION_APPROVED`. H-0072 e H-0073 concluíram, respectivamente, a
capacidade genérica e sua aplicação a H-0055/H-0063. QA final da implementação:
`I1_IMPLEMENTATION_APPROVED`. Revalidação manual final:
`MANUAL_REVALIDATION_APPROVED`, com VM-H0073-001 e VM-H0073-002 resolvidos,
tabulação dinâmica aprovada nas duas telas e espaçamento 3..8 preservado.
H-0070 permanece falha histórica não causal e fora deste ciclo.

Patch documental P02 (2026-08-15) corrigiu a especialização de H-0063 em
§4.11/§4.11.1 e o item correspondente de §10: a suposição anterior de que
H-0063 já possuía dois campos semânticos separados para as duas colunas não
correspondia ao estado real do produtor de conteúdo
(`tela/estilo.py::ControladorTelaEstilo._construir_conteudo`); o patch fecha
`preset` e `amostra` como nomes literais das colunas e autoriza
`campos["amostra"]` como extensão compatível da projeção de conteúdo, sem
alterar `campos["titulo"]` nem qualquer conteúdo visível — ver
`docs/relatorios/RELATORIO_PATCH_ADR-0047_P02.md`. O QA posterior aprovou
essa reconciliação.

Patch documental P03 (2026-08-15) corrige a expressividade insuficiente do
schema estrutural de `designador`: §4.4, a especialização futura de H-0055,
§4.13, §6 e os critérios de §10 agora fecham `tipo` obrigatório, `prefixo`
e `sufixo` opcionais como strings, as regras para `tipo: nenhum` e a
rejeição de chaves desconhecidas. A extensão preserva as configurações que
continham somente `tipo`, não cria herança do documento de conteúdo e foi
aprovada no QA posterior.

---

## 2. Contexto

### 2.1 Estado material ao início deste ciclo

A ADR-0042 fechou `dois_niveis_por_foco` como uma das cinco políticas de
navegação multinível do console: exatamente dois níveis (pais e filhos
diretos), toroide único de pais, toroide próprio de filhos por pai, seleção
exclusiva obrigatória de filho por pai e as demais regras de navegação,
foco, cursor e Espaço/Esc já fechadas (`contrato_console.md` §22.16). Essa
ADR não fechou, e explicitamente não fecha, a apresentação física dos
filhos — apenas sua navegabilidade e sua seleção.

O envelope do documento externo multinível (`contrato_json_console.md` §12)
já declara, por nível, um campo `conteudo` (nome de campo único, ou par
`nome`/`valor` para nós `nome_valor`) e um campo `designador` com tipos
fechados (`nenhum`, `simbolo`, `decimal`, `alfabetico_minusculo`,
`alfabetico_maiusculo`, `romano_minusculo`, `romano_maiusculo`,
`decimal_composto`, `personalizado`). O bloco `formato` de cada apresentação
já reserva, vazio, os blocos `espacamento` e `alinhamento` (§12.2), como
pontos de extensão declarativa ainda não preenchidos por nenhuma ADR
anterior. O princípio normativo vigente — "o JSON externo declara a intenção
de apresentação e o conteúdo semântico; o renderizador calcula a
representação física" — já está fixado por `contrato_console.md` §19.4/§19.6
e por `contrato_json_console.md` §11.4/§11.5/§12.6, que proíbem
explicitamente largura efetiva, posição final, quebra física pronta e
geometria calculada dentro do documento externo.

A estrutura do item do `console` — `ec` (espaço do cursor), `tg` (espaço de
toggle) e `tx` (texto do item), sempre nessa ordem — é terminologia
proprietária de `docs/nomenclatura/32_CONSOLE.md` §4.4. Item lógico distinto
de linha física, e a preservação do item lógico em redimensionamento e em
mudança de modo, são regras já vigentes (ADR-0031 D10; `contrato_console.md`
§22.5, §21.8).

A tela `h0063_estilo_estrutura_navegacao_dois_niveis.json` já usa
`politica_navegacao.tipo: "dois_niveis_por_foco"` para apresentar categorias
(pais) e presets (filhos) de estilo, sem qualquer declaração de tabulação,
colunas ou espaçamento entre colunas — os filhos são hoje itens de uma única
linha, sem apresentação tabular local.

### 2.2 Problema

Sem esta ADR, não existe autoridade documental fechada sobre como os filhos
de `dois_niveis_por_foco` são fisicamente formatados: quanto se recua o
filho em relação ao pai, se e como o filho pode apresentar seus dados em
colunas alinhadas, como esse alinhamento se comporta quando o pai corrente
muda, e como a tela de Estilo deve declarar sua apresentação de duas colunas
sem alterar o conteúdo semântico dos presets. A ausência dessa autoridade
impede a evolução da apresentação de `h0063` e de qualquer outra tela que
precise declarar formatação tabular local para filhos de
`dois_niveis_por_foco`, sem redesenhar a navegação, a seleção ou o schema já
fechados. Esta ADR responde a essa lacuna por meio de onze decisões
fechadas (D-DNF-01 a D-DNF-11), restritas ao escopo declarado.

### 2.3 Autoridades consultadas

| Documento | Papel |
|---|---|
| `docs/adr/ADR-0042-navegacao-multinivel-do-console.md` | Autoridade vigente da política `dois_niveis_por_foco` — dois níveis, dois toroides, seleção exclusiva obrigatória de filho por pai, preservada integralmente por esta ADR |
| `docs/contratos/contrato_console.md` | Autoridade comportamental do console — estrutura `ec`/`tg`/`tx` (§4.4 do módulo `32`, aplicada em §22.6), política `dois_niveis_por_foco` (§22.16), fronteira consumidor/renderizador (§19), redimensionamento preservando item lógico (§21.8, §22.5) |
| `docs/contratos/contrato_json_console.md` | Fronteira declarativa do documento externo multinível — schema semântico de níveis, `conteudo` e `designador` (§12.3), blocos `espacamento`/`alinhamento` reservados e vazios (§12.2), proibição de resultados físicos calculados no documento externo (§12.6) |
| `docs/nomenclatura/10_ESTILO.md` | Terminologia de presets, indicadores (`selecionado`, `incluido`) e materialização de estilo — autoridade preservada sobre valores e conteúdo de Estilo |
| `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` | Terminologia de redimensionamento reativo e preservação do item lógico durante recálculo de geometria |
| `docs/nomenclatura/32_CONSOLE.md` | Terminologia canônica de `ec`, `tg`, `tx`, item lógico, item corrente e vocabulário de `dois_niveis_por_foco` (ADR-0042) |
| `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` | Terminologia de apresentação por tela do console e sua fronteira explícita com a navegação multinível, referenciada e não duplicada |
| `config/telas/demo/h0055_dois_niveis_por_foco.json` e `..._conteudo.json` | Fixture vigente de `dois_niveis_por_foco` — demonstra a estrutura atual de pais/filhos sem tabulação nem colunas declaradas |
| `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json` | Tela de Estilo objeto da especialização de D-DNF-09 |

---

## 3. Decisão explícita do usuário

As onze decisões abaixo são fechadas e transportadas integralmente. Nenhuma
alternativa é escolhida por este documento.

### D-DNF-01 — Tabulação declarativa entre pai e filhos

```yaml
tabulacao_pai_filho:
  declaracao: obrigatoria_em_toda_apresentacao_de_dois_niveis_por_foco
  limites:
    minimo_espacos: 5
    maximo_espacos: 10
  escopo_dos_valores_acima: telas_atualmente_abrangidas_por_esta_atividade
  hardcoded_no_renderer: proibido
  escolha_do_valor_efetivo:
    responsavel: renderer
    criterio: maior_valor_dentro_do_intervalo_que_couber_na_largura_disponivel
    regra:
      - se_so_o_minimo_couber: usar_minimo
      - se_um_valor_intermediario_couber: usar_esse_valor
      - se_o_maximo_couber: usar_maximo
    sobra_apos_maximo: permanece_a_direita_da_apresentacao
```

### D-DNF-02 — Unidade inteira do filho deslocada

```yaml
ordem_fisica_do_filho: "tabulacao -> ec -> tg (quando existir) -> designador (quando existir) -> conteudo"
tabulacao_comeca: antes_de_ec
elementos_deslocados_para_a_direita:
  - cursor_do_filho_ec
  - toggle_do_filho_tg
  - designador_do_filho
  - conteudo_do_filho
posicao_do_cursor_do_filho: sempre_para_dentro_do_primeiro_caractere_visual_do_item_pai
proibido: aplicar_recuo_somente_ao_texto_mantendo_cursor_ou_toggle_alinhados_ao_pai
```

### D-DNF-03 — Designadores dos filhos

```yaml
formas_permitidas_para_o_nivel_filho:
  - decimal_composto  # ex.: "1.1"
  - alfabetico_maiusculo_com_sufixo  # ex.: "A)"
  - nenhum
designador_estrutural:
  tipo: obrigatorio
  prefixo: string_opcional
  sufixo: string_opcional
  ausentes_equivalem_a: string_vazia
tipo_nenhum: prefixo_e_sufixo_ausentes
identidade_logica_nova: proibida
identidade_derivada_do_texto_exibido: proibida
ausencia_de_designador: apenas_visual
```

### D-DNF-04 — Conteúdo tabular local do nível filho

```yaml
capacidade: nivel_filho_de_dois_niveis_por_foco_pode_declarar_dados_em_colunas_alinhadas
nao_transforma:
  - politica_navegacao_tipo_em_tabela
  - navegacao_em_nova_politica
  - console_em_passivo
  - dois_niveis_em_tres_niveis
cada_linha_da_apresentacao_tabular: continua_pertencendo_ao_mesmo_item_logico_filho
declaracao_exige:
  - numero_de_colunas
  - dados_que_alimentam_cada_coluna
apresentacao_tabular_local:
  cabecalho: ausente
  linha_separadora: ausente
  borda_propria: ausente
  titulo_proprio: ausente
integracao: bloco_formato_dois_niveis_por_foco_filho_do_elemento_console_no_json_estrutural_da_tela_sem_envelope_concorrente
```

### D-DNF-05 — Largura das colunas

```yaml
largura_natural_de_cada_coluna: determinada_pelo_conteudo_real_daquela_coluna
nao_armazenar_no_json:
  - largura_fisica_final
  - posicao_final
  - quebra_fisica_pronta
  - geometria_calculada
esses_resultados_pertencem_ao: renderer
```

### D-DNF-06 — Alinhamento global das colunas

```yaml
escopo_do_alinhamento: todos_os_filhos_do_console_inclusive_de_pais_diferentes
recalculo_separado_por_pai: proibido
trocar_o_pai_corrente: nao_move_horizontalmente_as_colunas
```

### D-DNF-07 — Espaçamento declarativo entre colunas

```yaml
espacamento_entre_colunas:
  declaracao: limites_minimo_e_maximo_em_formato_dois_niveis_por_foco_filho_tabela_espacamento_do_elemento_console_no_json_estrutural_da_tela
  limites_desta_configuracao:
    minimo_espacos: 3
    maximo_espacos: 8
  escolha_do_valor_efetivo:
    responsavel: renderer
    criterio: maior_espacamento_que_couber_dentro_de_3_a_8
    regra:
      - se_so_3_couber: usar_3
      - se_um_valor_intermediario_couber: usar_esse_valor
      - se_8_couber: usar_8
    sobra_apos_8: permanece_a_direita_de_toda_a_tabela
  ampliacao_artificial_de_colunas_para_consumir_sobra: proibida
```

### D-DNF-08 — Quebra de conteúdo

```yaml
quando: representacao_tabular_nao_couber_horizontalmente_mesmo_apos_compactacao_permitida
comportamento: conteudo_das_celulas_quebra_em_multiplas_linhas
item_logico: permanece_unico
preservar_regras_vigentes_de_cursor_em_linhas_fisicas_de_continuacao: true
proibido_por_linha_quebrada:
  - novo_cursor
  - novo_toggle
  - nova_identidade_logica
resize: recalcula_geometria_fisica_preservando_o_item_logico
```

### D-DNF-09 — Tela de Estilo

```yaml
tela: config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json
filhos:
  designador: nenhum
  apresentacao_local: tabular
  colunas: 2
colunas_representam:
  1: texto_nome_ja_existente
  2: exemplo_visual_ja_existente
natureza_da_alteracao: exclusivamente_de_formatacao
proibido_nesta_atividade:
  - nomes_dos_presets
  - textos
  - exemplos
  - simbolos
  - ordem_dos_itens
  - conteudo
  - valores_de_estilo
  - semantica_de_selecao
  - candidato
  - baseline
  - aplicacao
  - persistencia
  - publicacao_do_estilo
```

### D-DNF-10 — Aplicação a todas as telas existentes

```yaml
capacidade: nao_e_especial_da_tela_de_estilo
telas_existentes_com_dois_niveis_por_foco:
  reconciliacao: posterior_na_aplicacao_handoff_implementacao
  cada_tela_escolhe:
    - sua_forma_valida_de_designador
    - sua_apresentacao_de_dados
imposicao_de_tabela_de_duas_colunas_a_todas_as_telas: proibida
```

### D-DNF-11 — Separação de responsabilidades

```yaml
json_estrutural_da_tela_elemento_console_declara:
  - estrutura_semantica
  - designador
  - limites_min_max_de_tabulacao
  - estrutura_das_colunas
  - limites_min_max_do_espaco_entre_colunas

renderer_calcula:
  - tabulacao_fisica_efetiva
  - larguras_fisicas
  - alinhamento
  - quebras
  - linhas_fisicas
  - posicoes_finais

resultados_calculados_retornam_ao_json_como_configuracao_persistida: false
```

---

## 4. Decisão

Ficam adotadas, para a apresentação/formatação dos filhos de
`dois_niveis_por_foco`, as regras abaixo, fechadas por decisão explícita do
usuário e sem alternativa de desenho em aberto. Esta ADR evolui
exclusivamente a apresentação — nunca a navegação, a seleção ou o schema
semântico já fechados pela ADR-0042.

### 4.1 Separação entre navegação e apresentação

`dois_niveis_por_foco` permanece, integralmente e sem redesenho, a política
já fechada pela ADR-0042 (D-MULTI-07 a D-MULTI-09; `contrato_console.md`
§22.16): exatamente dois níveis (pais e filhos diretos), navegação primeiro
entre pais e, ao entrar em um pai, entre seus filhos, toroide único de pais,
toroide próprio de filhos por pai, cursor e escolha persistente do filho
como mecanismos distintos, e seleção exclusiva obrigatória de filho por pai
inalterada. Esta ADR não redefine `politica_navegacao.tipo`, não cria novo
valor de `tipo`, não altera paginação, foco, Esc ou qualquer comportamento
de navegação. O objeto desta ADR é exclusivamente a representação física e a
configuração declarativa de apresentação dos filhos — como o conteúdo já
navegável é exibido, não como ele é navegado.

### 4.2 Tabulação mínima e máxima entre pai e filhos

Toda apresentação usada com `dois_niveis_por_foco` deve declarar, no bloco
`formato.dois_niveis_por_foco.filho.tabulacao` do elemento `console` no JSON
estrutural da tela (schema fechado em §4.13) — nunca no documento externo de
conteúdo —, os limites mínimo e máximo de tabulação entre pai e filhos. Para
as telas abrangidas por esta atividade, o mínimo é 5 espaços e o máximo é 10
espaços; esses valores não são hardcoded no renderer, e outras telas de
`dois_niveis_por_foco` podem declarar seus próprios limites na aplicação
futura (§4.11, §4.12).

O renderer escolhe dinamicamente, conforme a largura disponível do
terminal, o maior valor possível dentro do intervalo declarado: usa o
mínimo se apenas o mínimo couber, um valor intermediário se este couber, ou
o máximo se o máximo couber. Espaço horizontal excedente depois de atendido
o máximo permanece à direita da apresentação — não é consumido por
ampliação artificial de tabulação, coluna ou espaçamento.

### 4.3 Relação entre tabulação e `ec`/`tg`/designador/conteúdo

A tabulação começa antes de `ec`. A ordem física do filho permanece
`tabulação → ec → tg, quando existir → designador, quando existir →
conteúdo` — a mesma ordem `ec`/`tg`/`tx` já fixada por
`docs/nomenclatura/32_CONSOLE.md` §4.4, com a tabulação como recuo aplicado
antes do início dessa estrutura, e o designador e o conteúdo posicionados
dentro do espaço de `tx`. Cursor do filho, toggle do filho, designador do
filho e conteúdo do filho ficam todos deslocados para a direita como uma
unidade inteira — nunca apenas o texto. O cursor do filho deve estar sempre
para dentro do primeiro caractere visual do item pai. É proibido aplicar
recuo somente ao texto mantendo cursor ou toggle alinhados ao pai: a
distinção `ec`/`tg` como espaços coexistentes e adjacentes, não
sobrepostos, é preservada integralmente pela unidade deslocada.

### 4.4 Designadores permitidos pelos mecanismos existentes

A apresentação do nível filho pode utilizar as formas de designador já
existentes no schema semântico multinível (`contrato_json_console.md`
§12.3): decimal composto (produzindo formas como `1.1`), alfabético
maiúsculo com sufixo (produzindo formas como `A)`), ou nenhum designador.
No bloco estrutural, `designador` é um objeto fechado com `tipo` obrigatório
e somente os campos opcionais `prefixo` e `sufixo`, ambos strings. Os únicos
valores válidos de `tipo` nesta capacidade são `decimal_composto`,
`alfabetico_maiusculo` e `nenhum`; uma chave desconhecida ou outro tipo é
inválido. Quando presentes, `prefixo` e `sufixo` envolvem o designador base
do tipo, nessa ordem; quando ausentes, equivalem a string vazia. Para
`tipo: nenhum`, não existe designador visual e `prefixo`/`sufixo` devem
estar ausentes. Esta extensão não cria tipo novo de designador nem altera a
lógica de cálculo de `decimal_composto`. Nenhuma identidade lógica nova é
criada, e nenhuma identidade é derivada do texto exibido — a ausência de
designador é estritamente visual, sem efeito sobre `id` do nó, ordem
semântica ou qualquer outro campo estrutural. Não há herança automática do
designador do documento de conteúdo, campo `fonte`, campo `herdar` ou
parsing de designador externo; a configuração estrutural continua sendo a
autoridade de como apresentar, e o conteúdo continua sendo dados.

### 4.5 Apresentação tabular local de filhos

Um nível filho de `dois_niveis_por_foco` pode declarar apresentação de seus
dados em colunas alinhadas. Essa capacidade não transforma
`politica_navegacao.tipo` em `tabela`, não cria nova política de navegação,
não torna o console passivo e não cria terceiro nível: cada linha da
apresentação tabular continua pertencendo ao mesmo item lógico filho — a
distinção entre item lógico e linha física, já fixada por
`contrato_console.md` §22.4 e §4.4 do módulo `32`, permanece integralmente
aplicável dentro da própria apresentação tabular local.

A apresentação tabular local declara o número de colunas e quais dados
alimentam cada coluna; não possui cabeçalho, linha separadora, borda
própria ou título próprio — distinguindo-se, por essa ausência de moldura
própria, da apresentação `tabela` do schema multinível (§12.2 de
`contrato_json_console.md`), que é apresentação de nível de console inteiro
com cabeçalho. A declaração da apresentação tabular local pertence
exclusivamente ao elemento `console` do JSON estrutural da tela — bloco
`formato.dois_niveis_por_foco.filho.tabela` (schema fechado em §4.13) —, no
mesmo local estrutural já usado pelo precedente `console.formato.excesso`
(D23; `contrato_console.md` §21.7; `contrato_json_console.md` §13.13.1). Ela
não estende o mecanismo `conteudo` do schema semântico multinível do
documento externo de conteúdo (`contrato_json_console.md` §12.3), não cria
envelope concorrente a esse documento, e o documento de conteúdo não recebe
tabulação, mínimo/máximo, tipo de apresentação tabular, colunas,
espaçamento entre colunas, geometria ou alinhamento físico. Os campos
`campo` das colunas apenas referenciam, por nome semântico, dados que
continuam a existir somente no documento de conteúdo.

### 4.6 Largura das colunas

A largura natural de cada coluna é determinada pelo conteúdo real daquela
coluna. Consistente com a proibição já vigente de resultados físicos
calculados no documento externo (`contrato_console.md` §19.4;
`contrato_json_console.md` §11.4, §12.6), o JSON não armazena largura física
final, posição final, quebra física pronta ou geometria calculada — esses
resultados pertencem exclusivamente ao renderer.

### 4.7 Alinhamento global das colunas

Para uma mesma apresentação, as colunas permanecem alinhadas considerando
todos os filhos do console, inclusive filhos pertencentes a pais
diferentes. O alinhamento não é recalculado separadamente por pai: trocar o
pai corrente não faz as colunas mudarem horizontalmente apenas porque outro
conjunto de filhos passou a estar em foco. Este princípio de medição sobre o
conjunto lógico completo do console — e não sobre o subconjunto
momentaneamente em foco — é consistente com o precedente já fixado por
`contrato_json_console.md` §13.13.11 para o alinhamento da coluna de
segundo nível no cenário verboso de dois níveis, medido sobre o "conteúdo
lógico completo do cenário".

### 4.8 Espaçamento mínimo e máximo entre colunas

O espaço entre colunas possui limites mínimo e máximo declarados no bloco
`formato.dois_niveis_por_foco.filho.tabela.espacamento` do elemento
`console` no JSON estrutural da tela (schema fechado em §4.13) — nunca no
documento externo de conteúdo. Para a configuração desta atividade, o
mínimo é 3 espaços e o máximo é 8 espaços. O renderer usa o maior
espaçamento que couber dentro de 3 a 8: 3 se apenas 3 couberem, um valor
intermediário se este couber, ou 8 se 8 couberem. Se ainda restar largura
horizontal após usar 8, a sobra permanece à direita de toda a tabela — as
colunas não são artificialmente ampliadas para consumir essa sobra.

### 4.9 Quebra de conteúdo em múltiplas linhas

Quando a representação tabular não couber horizontalmente mesmo após a
compactação permitida por §4.2 e §4.8, o conteúdo das células quebra em
múltiplas linhas, como em uma tabela. O item continua sendo um único item
lógico. As regras vigentes de cursor em linhas físicas de continuação são
preservadas: nenhuma linha quebrada recebe cursor, toggle ou identidade
lógica adicional — o mesmo princípio já aplicado a linhas de continuação em
modo verboso (`contrato_console.md` §21.3, §22.6; módulo `44` §8B).

### 4.10 Comportamento em resize

Redimensionamento recalcula a geometria física — tabulação efetiva,
larguras de coluna, espaçamento entre colunas e quebras — preservando o
item lógico, na mesma linha já fixada para o console em geral (ADR-0031
D10; `contrato_console.md` §21.8, §22.5). Nenhuma nova exceção a essa regra
é criada para `dois_niveis_por_foco`.

### 4.11 Especialização da tela de Estilo sem alteração de conteúdo

A tela `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json`
deve declarar, no elemento `console` do seu próprio JSON estrutural (nunca
no documento de conteúdo), o bloco `formato.dois_niveis_por_foco.filho`
(schema fechado em §4.13) com exatamente:

```yaml
formato.dois_niveis_por_foco.filho:
  tabulacao:
    minimo: 5
    maximo: 10
  designador:
    tipo: nenhum
  apresentacao: tabela
  tabela:
    colunas:
      - campo: preset
      - campo: amostra
    espacamento:
      minimo: 3
      maximo: 8
```

As duas entradas de `tabela.colunas` usam os nomes literais fechados por
§4.11.1: `preset` na primeira coluna e `amostra` na segunda. A alteração da
tela de Estilo é exclusivamente de formatação, restrita ao JSON estrutural
da tela: é expressamente proibido, nesta atividade, alterar nomes dos
presets, textos, exemplos, símbolos, ordem dos itens, conteúdo, valores de
estilo, semântica de seleção, candidato, baseline, aplicação, persistência
ou publicação do estilo — todas essas camadas permanecem sob a autoridade
vigente de `docs/nomenclatura/10_ESTILO.md` §4.8, §4.9, sem qualquer
reabertura por esta ADR.
Como a especialização usa `tipo: nenhum`, seu bloco `designador` não
declara `prefixo` nem `sufixo`; nenhum desses campos deve ser adicionado.

### 4.11.1 Correção de fato e fechamento literal dos campos de H-0063 (patch documental P02)

Esta subseção corrige exclusivamente o pressuposto de §4.11 quanto à
existência prévia de dois campos semânticos separados para as duas colunas
de H-0063, e fecha os nomes literais desses campos. Nenhuma outra decisão
desta ADR — inclusive D-DNF-09 (§3) — é reaberta por esta correção; a
substância de D-DNF-09 (duas colunas, designador `nenhum`, apresentação
tabular local, sem alteração de conteúdo) permanece integralmente
preservada.

**Fato corrigido.** O conteúdo dinâmico real de H-0063 é produzido por
`tela/estilo.py::ControladorTelaEstilo._construir_conteudo`, que hoje popula,
para cada filho, exatamente os campos `navegavel`, `selecionavel`, `titulo`,
`categoria` e `preset`. `campos["titulo"]` já é o resultado de
`tela/renderizacao/estilo.py::compor_titulo_com_amostra`, que compõe o nome
do preset e a amostra visual (produzida por `amostra_de_preset`) em uma
única string. Não existe hoje, nesse fluxo, um campo separado contendo
apenas a amostra visual. A afirmação anterior de §4.11 de que H-0063 já
possuía dois campos semânticos separados para alimentar as duas colunas não
corresponde a esse estado real.

**Decisão fechada.** `campos["preset"]` (já existente, preservado
integralmente) alimenta a primeira coluna. `campos["amostra"]` — campo novo
exclusivamente na projeção de conteúdo entregue ao console — alimenta a
segunda coluna. `campos["amostra"]` deve conter exatamente o mesmo valor
semântico já produzido hoje pela composição de `titulo`, isto é, o mesmo
resultado hoje calculado por `amostra_de_preset` dentro de
`compor_titulo_com_amostra`, obtido a partir do valor/componente semântico
real já disponível no fluxo de composição — nunca por parsing posterior de
`titulo`. `campos["titulo"]` permanece integralmente inalterado, com o
mesmo valor e significado atuais, para consumidores preexistentes; nenhum
campo existente é removido, renomeado ou redefinido.

**Natureza da alteração.** A criação de `campos["amostra"]` é uma extensão
compatível da projeção de dados entregue ao console. Não constitui
alteração do conteúdo visível ou do significado dos dados: nomes de
categorias, nomes de presets, textos existentes, amostras visuais
existentes, símbolos, ordem, valores de estilo, seleção, candidato,
baseline, aplicação, persistência e publicação permanecem idênticos. A
existência de `campos["amostra"]` na projeção não transfere configuração
visual para os dados — a decisão de exibi-lo como segunda coluna continua
pertencendo exclusivamente à configuração estrutural da tela (§4.13, §5).

Após esta correção, nenhuma decisão de nomenclatura de campo necessária à
especialização de H-0063 permanece aberta.

### 4.11.2 Especialização de H-0055 com sufixo alfabético

A futura configuração estrutural de H-0055 deve declarar, no bloco fechado
por esta ADR:

```yaml
formato.dois_niveis_por_foco.filho:
  tabulacao:
    minimo: 5
    maximo: 10

  designador:
    tipo: alfabetico_maiusculo
    sufixo: ")"

  apresentacao: texto
```

Essa configuração produz `A)`, `B)`, `C)`, `D)` e assim por diante. O
documento externo `config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json`
permanece integralmente inalterado: não há herança automática, parsing ou
remoção do designador existente no conteúdo. A configuração estrutural da
tela é a autoridade de como apresentar, e o conteúdo permanece dados.

### 4.12 Aplicação futura às telas existentes

A capacidade de apresentação tabular local não é especial da tela de
Estilo. Todas as telas existentes que utilizem `dois_niveis_por_foco` devem
ser reconciliadas posteriormente, na aplicação/handoff/implementação, para
declarar explicitamente a apresentação necessária segundo o novo contrato.
Cada tela pode escolher sua forma válida de designador (§4.4) e sua
apresentação de dados (com ou sem colunas locais); não se impõe tabela de
duas colunas a todas as telas.

### 4.13 Localização e schema literal fechados (correção de fronteira — QA-ADR-0047-001)

Esta seção corrige e fecha, para as três capacidades declarativas desta ADR
(tabulação, designador local e apresentação/tabela), a localização exata, a
forma e os nomes literais de campo. Nenhuma dessas declarações pertence ao
envelope declarativo do documento externo de conteúdo
(`contrato_json_console.md` §11–§14): esse documento continua fornecendo
exclusivamente dados — ele não recebe tabulação, mínimo/máximo de
tabulação, tipo de apresentação tabular, configuração de colunas,
espaçamento entre colunas, geometria ou alinhamento físico. Essa
distribuição vale igualmente para telas cujo conteúdo é produzido
dinamicamente, como a futura H-0063: a origem do conteúdo permanece
inalterada, e a configuração de apresentação continua pertencendo
exclusivamente ao JSON estrutural da tela.

Todas as três capacidades pertencem exclusivamente ao elemento `console` do
JSON estrutural da tela (`tela.json`), no mesmo local estrutural já usado
pelo precedente `console.formato.excesso.politica_modo` (D23;
`contrato_console.md` §21.7; `contrato_json_console.md` §13.13.1). Quando
`politica_navegacao.tipo = "dois_niveis_por_foco"`, o elemento `console`
declara, dentro do bloco `formato` já existente (preservando os campos
preexistentes, como `formato.excesso` quando presente), o bloco literal
`formato.dois_niveis_por_foco`, na forma canônica:

```json
"formato": {
  "...campos preexistentes preservados...": "...",

  "dois_niveis_por_foco": {
    "filho": {
      "tabulacao": {
        "minimo": 5,
        "maximo": 10
      },

      "designador": {
        "tipo": "<decimal_composto|alfabetico_maiusculo|nenhum>",
        "prefixo": "<string opcional>",
        "sufixo": "<string opcional>"
      },

      "apresentacao": "texto"
    }
  }
}
```

**`tabulacao`** — local literal `formato.dois_niveis_por_foco.filho.tabulacao`,
campos literais `minimo` e `maximo`, ambos inteiros positivos, com
`minimo <= maximo`. Para as telas abrangidas nesta atividade: `minimo = 5`,
`maximo = 10`. O renderer usa o maior valor que couber dentro do intervalo
(§4.2), e a tabulação desloca a unidade inteira do filho a partir de `ec`
(§4.3).

**`designador`** — local literal `formato.dois_niveis_por_foco.filho.designador`.
É um objeto fechado com `tipo` obrigatório e somente os campos opcionais
`prefixo` e `sufixo`, ambos strings. Os únicos tipos válidos nesta
capacidade são `decimal_composto`, `alfabetico_maiusculo` e `nenhum`;
qualquer outro tipo ou chave desconhecida é inválido. A ausência de
`prefixo` ou `sufixo` equivale a string vazia. Para os tipos que produzem
designador visual, o resultado é `prefixo + designador_base_do_tipo +
sufixo`; assim, `decimal_composto` continua produzindo, por exemplo, `1.1`,
e `alfabetico_maiusculo` com `sufixo: ")"` produz `A)`. A lógica de cálculo
de `decimal_composto` não é redefinida. Para `tipo: nenhum`, não existe
designador visual e `prefixo` e `sufixo` devem estar ausentes. Não há
herança automática do documento de conteúdo, campo `fonte`, campo `herdar`
ou parsing do designador externo. A ausência de designador é somente
visual; nenhuma identidade lógica nova é criada.

**`apresentacao`** — local literal `formato.dois_niveis_por_foco.filho.apresentacao`,
valor `"texto"` ou `"tabela"`. Quando `"texto"`, não existe bloco `tabela` e
o conteúdo continua exibido pelo mecanismo normal já vigente. Quando
`"tabela"`, é obrigatório o bloco
`formato.dois_niveis_por_foco.filho.tabela`:

```json
"tabela": {
  "colunas": [
    { "campo": "<campo_semantico_do_conteudo>" }
  ],
  "espacamento": {
    "minimo": 3,
    "maximo": 8
  }
}
```

**`tabela.colunas`** — local literal
`formato.dois_niveis_por_foco.filho.tabela.colunas`. Array com mínimo de 1
elemento; cada elemento possui exatamente o campo literal `campo`,
referência semântica ao campo do conteúdo que alimenta aquela coluna; a
ordem no array é a ordem visual; a quantidade de elementos determina a
quantidade de colunas; `numero_colunas` não é criado; a configuração é
declarada uma única vez por tela e não é repetida em cada item filho. Os
valores de `campo` referenciam dados existentes no documento de conteúdo —
não os copiam para o JSON estrutural.

**`tabela.espacamento`** — local literal
`formato.dois_niveis_por_foco.filho.tabela.espacamento`, campos `minimo` e
`maximo`, ambos inteiros positivos, com `minimo <= maximo`. Para esta
atividade: `minimo = 3`, `maximo = 8` (§4.8).

Largura de coluna e quebra de conteúdo (§4.6, §4.9) e alinhamento global
entre todos os filhos do console (§4.7) permanecem exclusivamente
calculados pelo renderer, sem campo JSON adicional além dos fechados nesta
seção — nenhum campo de largura, posição final ou geometria calculada é
armazenado.

Após esta correção, nenhuma decisão de schema necessária a `APLICAR_ADR`
permanece aberta: localização, cardinalidade e nomes literais das três
capacidades estão integralmente fechados por esta seção.

---

## 5. Separação de responsabilidades

O elemento `console` do JSON estrutural da tela declara estrutura semântica
(via `politica_navegacao`), designador local, limites min/max de tabulação,
estrutura das colunas e limites min/max do espaço entre colunas, no bloco
`formato.dois_niveis_por_foco.filho` fechado em §4.13. O documento externo
de conteúdo continua declarando exclusivamente dados. O renderer calcula
tabulação física efetiva, larguras físicas, alinhamento, quebras, linhas
físicas e posições finais. Os resultados calculados não retornam a nenhum
dos dois documentos como configuração persistida — o mesmo princípio
normativo já fixado por `contrato_console.md` §19.6 ("o JSON externo
declara a intenção de apresentação e o conteúdo semântico; o renderizador
calcula a representação física") aplicado especificamente às capacidades
desta ADR, com "JSON externo" abrangendo aqui o JSON estrutural da tela
para as declarações desta ADR, e não o documento de conteúdo.

Esta ADR fixa integralmente a localização, a cardinalidade e a nomenclatura
literal de campo para tabulação min/max, designador local, estrutura de
colunas e espaçamento min/max entre colunas (§4.13). Nenhuma dessas
declarações se integra aos pontos de extensão reservados no schema
semântico multinível do documento externo de conteúdo — os blocos
`formato.espacamento` e `formato.alinhamento` por apresentação
(`contrato_json_console.md` §12.2) e o mecanismo de declaração de
`conteudo` por nível (§12.3) permanecem exclusivos do documento de
conteúdo, sem relação com as capacidades desta ADR. A aplicação documental
que reconciliar os contratos afetados (§8) propaga a localização e os nomes
já fechados por §4.13; ela não decide nomenclatura nova.

---

## 6. Compatibilidade

Configurações existentes de `dois_niveis_por_foco` que não declaram
tabulação, colunas locais ou espaçamento entre colunas permanecem válidas
sem alteração automática: nenhuma migração é feita por esta ADR. A
capacidade aqui fechada é aditiva ao envelope estrutural do elemento
`console` — introduz o bloco `formato.dois_niveis_por_foco` (§4.13) sem
remover, renomear ou redefinir campo existente do envelope nem do schema
semântico multinível do documento de conteúdo. `dois_niveis_por_foco`
permanece a mesma política fechada pela ADR-0042; nenhuma tela deixa de ser
válida por não declarar as novas capacidades até sua reconciliação futura
(§4.12).

O patch documental P03 é uma extensão compatível do schema estrutural
fechado em P01/P02: `designador` continua objeto, `tipo` continua
obrigatório e configurações que declaram somente `tipo` continuam válidas;
`prefixo` e `sufixo` são os únicos campos opcionais novos, ambos strings.
Para os tipos visuais ausentes equivalem a strings vazias; para
`tipo: nenhum`, permanecem ausentes e não têm efeito visual. P03 corrige
somente a expressividade do designador estrutural. Não altera a política
`dois_niveis_por_foco`, tabulação, apresentação texto/tabela, tabela,
colunas, espaçamento, alinhamento, quebra, resize, item lógico, seleção ou
navegação.

---

## 7. Consequências

### Positivas

- Fecha, para `dois_niveis_por_foco`, uma autoridade documental única sobre
  tabulação declarativa entre pai e filhos, deslocamento da unidade inteira
  do filho, designadores permitidos, apresentação tabular local, alinhamento
  global de colunas, espaçamento entre colunas, quebra de conteúdo e
  comportamento em resize.
- Preserva integralmente a navegação, a seleção exclusiva obrigatória de
  filho por pai, a paginação, o foco e o Esc já fechados pela ADR-0042 —
  nenhum desses comportamentos é reaberto.
- Permite que `h0063_estilo_estrutura_navegacao_dois_niveis.json` declare
  apresentação de duas colunas para seus filhos sem alterar presets,
  textos, exemplos, símbolos, ordem, conteúdo, valores de estilo, candidato,
  baseline, aplicação, persistência ou publicação do estilo.
- Mantém a separação já vigente entre o que o JSON estrutural/documento de
  conteúdo declara e o que o renderer calcula, sem introduzir geometria
  física calculada em nenhum dos dois.
- Fecha a fronteira entre configuração estrutural da tela e conteúdo/dados:
  as novas declarações pertencem exclusivamente ao envelope do elemento
  `console` (§4.13), sem duplicar ou concorrer com o schema semântico
  multinível do documento de conteúdo.

### Custos e restrições

- Exigirá, na aplicação documental futura, a propagação da localização, da
  cardinalidade e da nomenclatura literal já fechadas por esta ADR (§4.13)
  para `contrato_console.md` (comportamento) e `contrato_json_console.md`
  (schema do envelope do elemento `console` no JSON estrutural da tela) —
  sem decisão nova de nomenclatura, apenas propagação.
- Exigirá, na aplicação e nos handoffs futuros, a reconciliação de
  `config/telas/demo/h0055_dois_niveis_por_foco.json` e de
  `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json` para
  declarar explicitamente, em seus respectivos JSONs estruturais, o bloco
  `formato.dois_niveis_por_foco.filho` fechado por esta ADR; o documento de
  conteúdo de cada tela permanece inalterado por esta reconciliação.
- Introduz uma dependência documental explícita: nenhuma implementação
  futura pode antecipar geometria física calculada dentro do JSON
  estrutural ou do documento externo de conteúdo, nem tratar a apresentação
  tabular local como nova política de navegação, terceiro nível, ou console
  passivo.

---

## 8. Documentos, contratos e módulos que a aplicação da ADR deverá reconciliar

- `docs/contratos/contrato_console.md` — recebe o comportamento da
  capacidade: propagação da apresentação/formatação de filhos de
  `dois_niveis_por_foco` (§22.16), incluindo a relação entre tabulação,
  `ec`/`tg`/`tx` e a apresentação tabular local.
- `docs/contratos/contrato_json_console.md` — recebe o schema do envelope
  do elemento `console` no JSON estrutural da tela: o bloco
  `formato.dois_niveis_por_foco.filho` com `tabulacao`, `designador`,
  `apresentacao` e `tabela` (colunas e espaçamento), literalmente fechado
  por §4.13 desta ADR, no mesmo local estrutural do precedente
  `formato.excesso` (§13.13.1). Os blocos `formato.espacamento`,
  `formato.alinhamento` e o mecanismo de `conteudo` por nível do documento
  externo de conteúdo (§11–§14, em especial §12.2, §12.3) não são usados
  como justificativa para armazenar essas novas configurações — eles
  permanecem exclusivos do documento de conteúdo, sem relação com as
  capacidades desta ADR. Quando necessário, a aplicação deve apenas
  preservar/clarificar essa fronteira entre configuração estrutural da tela
  e conteúdo/dados separados.
- `docs/nomenclatura/32_CONSOLE.md` — eventual termo proprietário para a
  apresentação tabular local de filhos, se necessário, preservando `ec`,
  `tg`, `tx` e item lógico sem redefinição.
- `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` —
  eventual remissão à apresentação tabular local como apresentação por
  tela, preservando a fronteira já fixada com a navegação multinível (§8B).
- `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` — eventual
  remissão ao comportamento de resize desta capacidade, preservando a
  preservação do item lógico já fixada.
- `config/telas/demo/h0055_dois_niveis_por_foco.json` e
  `..._conteudo.json` — reconciliação declarativa futura, conforme §4.12.
- `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json` —
  especialização declarativa conforme §4.11.

---

## 9. Fora de escopo

- Mudar a navegação de `dois_niveis_por_foco`.
- Alterar a seleção exclusiva obrigatória de filho por pai.
- Criar nova política de navegação.
- Transformar filhos em `politica_navegacao.tipo = tabela`.
- Alterar conteúdo da tela de Estilo — nomes de presets, textos, exemplos,
  símbolos, ordem dos itens, conteúdo, valores de estilo, semântica de
  seleção, candidato, baseline, aplicação, persistência ou publicação.
- Alterar presets ou símbolos de Estilo.
- Alterar paginação.
- Alterar teclas.
- Alterar Barra de Menus.
- Corrigir outros defeitos não necessários a esta decisão.
- Implementar código.
- Escolher handoffs.

---

## 10. Critérios para aplicação

- [ ] `contrato_console.md` e `contrato_json_console.md` propagam a
  apresentação/formatação de filhos de `dois_niveis_por_foco` exatamente
  como fechada nesta ADR, sem introduzir alternativa não decidida aqui.
- [ ] O bloco `formato.dois_niveis_por_foco.filho` (tabulação, designador,
  apresentação e tabela) é declarado exclusivamente no elemento `console`
  do JSON estrutural da tela (§4.13), nunca no documento externo de
  conteúdo; o documento de conteúdo não recebe tabulação, mínimo/máximo,
  tipo de apresentação tabular, colunas, espaçamento entre colunas,
  geometria ou alinhamento físico.
- [ ] `formato.dois_niveis_por_foco.filho.tabulacao.minimo` e `.maximo` são
  inteiros positivos com `minimo <= maximo`; `formato.dois_niveis_por_foco
  .filho.tabela.espacamento.minimo` e `.maximo` idem.
- [ ] `formato.dois_niveis_por_foco.filho.apresentacao` vale exatamente
  `"texto"` ou `"tabela"`; o bloco `tabela` existe se e somente se
  `apresentacao = "tabela"`.
- [ ] `formato.dois_niveis_por_foco.filho.tabela.colunas` é array com no
  mínimo 1 elemento, cada um com exatamente o campo literal `campo`; a
  ordem no array é a ordem visual; a quantidade de elementos determina a
  quantidade de colunas; `numero_colunas` não é criado; a declaração ocorre
  uma única vez por tela, nunca repetida por item filho.
- [ ] `dois_niveis_por_foco` permanece exatamente dois níveis, com toroide
  único de pais, toroide próprio de filhos por pai e seleção exclusiva
  obrigatória de filho por pai, sem alteração.
- [ ] Toda apresentação de `dois_niveis_por_foco` declara limites mínimo e
  máximo de tabulação entre pai e filhos; nenhum valor é hardcoded no
  renderer.
- [ ] O renderer escolhe o maior valor de tabulação que couber dentro do
  intervalo declarado, com a sobra permanecendo à direita da apresentação.
- [ ] A tabulação começa antes de `ec`; cursor, toggle, designador e
  conteúdo do filho são deslocados juntos, como unidade inteira; nenhum
  recuo aplica-se somente ao texto.
- [ ] O cursor do filho permanece sempre para dentro do primeiro caractere
  visual do item pai.
- [ ] Os designadores de filho utilizados pertencem exclusivamente aos
  tipos já existentes no schema (`decimal_composto`,
  `alfabetico_maiusculo` com sufixo, ou `nenhum`); nenhuma identidade
  lógica nova é criada nem derivada do texto exibido.
- [ ] O designador estrutural é objeto fechado com `tipo` obrigatório;
  `prefixo` e `sufixo`, quando presentes, são strings, ausentes equivalem
  a string vazia, tipos fora de `decimal_composto`,
  `alfabetico_maiusculo` e `nenhum` são inválidos e chaves desconhecidas
  não são aceitas silenciosamente.
- [ ] Para tipos visuais, o renderer calcula
  `prefixo + designador_base_do_tipo + sufixo`; para
  `tipo: nenhum`, não há designador visual e `prefixo`/`sufixo` estão
  ausentes. Não há herança automática do documento de conteúdo, campo
  `fonte`, campo `herdar` ou parsing externo, e `decimal_composto` mantém
  sua lógica de cálculo.
- [ ] A apresentação tabular local de filhos, quando declarada, não altera
  `politica_navegacao.tipo`, não cria terceiro nível e não torna o console
  passivo; cada linha continua pertencendo ao mesmo item lógico filho.
- [ ] A apresentação tabular local não possui cabeçalho, linha separadora,
  borda própria nem título próprio.
- [ ] O JSON não armazena largura física final, posição final, quebra
  física pronta ou geometria calculada de colunas.
- [ ] O alinhamento das colunas é calculado sobre todos os filhos do
  console, inclusive de pais diferentes; trocar o pai corrente não desloca
  horizontalmente as colunas.
- [ ] Toda apresentação com colunas locais declara limites mínimo e máximo
  de espaçamento entre colunas; o renderer usa o maior valor que couber,
  com a sobra permanecendo à direita da tabela, sem ampliação artificial de
  coluna.
- [ ] Quando a representação tabular não couber horizontalmente mesmo após
  a compactação permitida, o conteúdo quebra em múltiplas linhas físicas
  sem criar novo cursor, toggle ou identidade lógica para as linhas de
  continuação.
- [ ] Resize recalcula tabulação, larguras, alinhamento e quebras
  preservando o item lógico corrente.
- [ ] `h0063_estilo_estrutura_navegacao_dois_niveis.json` declara, em seu
  próprio JSON estrutural (nunca no documento de conteúdo), o bloco
  `formato.dois_niveis_por_foco.filho` com `tabulacao.minimo = 5`,
  `tabulacao.maximo = 10`, `designador.tipo = nenhum` sem `prefixo` ou
  `sufixo`,
  `apresentacao = tabela` e `tabela` com exatamente 2 entradas em
  `colunas`: `campo: preset` (já existente em `campos`, preservado
  integralmente) e `campo: amostra` (novo somente como campo da projeção de
  conteúdo, conforme §4.11.1, cujo valor semântico já existe hoje no fluxo
  de composição de `titulo` — nunca obtido por parsing posterior de
  `titulo`) — e `tabela.espacamento.minimo = 3`,
  `tabela.espacamento.maximo = 8`. `campos["titulo"]` permanece intacto
  para consumidores preexistentes; nenhum campo existente é removido,
  renomeado ou redefinido; nenhuma alteração de nomes de presets, textos,
  exemplos, símbolos, ordem, conteúdo, valores de estilo, semântica de
  seleção, candidato, baseline, aplicação, persistência ou publicação do
  estilo é permitida.
- [ ] A futura especialização estrutural de H-0055 declara `tipo:
  alfabetico_maiusculo`, `sufixo: ")"`, tabulação 5..10 e
  `apresentacao: texto`, produzindo `A)`, `B)`, `C)`, `D)`; o documento
  externo de conteúdo permanece inalterado.
- [ ] Nenhuma tela de `dois_niveis_por_foco` além das abrangidas por esta
  atividade é alterada por esta ADR; a reconciliação das demais telas
  existentes é etapa posterior, e nenhuma delas é obrigada a usar tabela de
  duas colunas.
- [ ] Nenhuma implementação de código é feita nesta etapa de ADR.
- [ ] Nenhum handoff é criado nesta etapa de ADR.

---

## 11. Alternativas consideradas

Não há alternativas de desenho a registrar nesta ADR. As decisões D-DNF-01
a D-DNF-11 constituem decisão já fechada fornecida ao autor documental;
este documento não escolhe entre opções nem introduz arquitetura, schema,
política, representação visual ou fluxo de execução além do que foi
explicitamente decidido.

---

## 12. Bloqueios

nenhum
\n