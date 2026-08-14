# H-0063 — Tela de Estilo: estrutura e navegação em dois níveis

## 1. Metadata e rastreabilidade

```yaml
projeto: Orquestrador
item: ITEM-0010
adr: ADR-0046
handoff: H-0063
data_criacao: 2026-08-12
status: READY_FOR_IMPLEMENTATION
predecessor_status: substituido
rastreabilidade:
  handoff_historico:
    id: H-0062
    caminho: docs/handoff/H-0062-tela-selecao-interativa-presets-estilo.md
    relacao: substituicao_operacional
    campo_substituido_por: NAO_EXISTE
    preservacao_predecessor: obrigatoria
```

H-0063 substitui operacionalmente H-0062. H-0062 permanece preservado como
histórico e não é reescrito por este documento. H-0063 não é continuação por
patch de H-0062: a reprovação da validação manual e a decisão gerencial de
reparticionar o trabalho exigem uma nova fundação estrutural.

O estado de predecessor acima registra a substituição operacional no sucessor;
nenhum campo `substituido_por` deve ser criado.

## 2. Contexto causal

A validação manual de H-0062 foi reprovada com três achados materiais,
registrados em `docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0062.md`:

- `VM-H0062-001`: a seleção de Estilo apareceu/comportou-se como popup, embora
  o esperado fosse uma tela normal com Cabeçalho, Console e Barra de Menus;
  popup pertence somente à futura confirmação de aplicação.
- `VM-H0062-002`: a navegação em dois níveis não funcionou adequadamente.
- `VM-H0062-003`: o redimensionamento do terminal quebrou a exibição.

Não há diagnóstico técnico adicional neste handoff. Esses fatos justificam a
decomposição e a prioridade da fundação estrutural.

## 3. Objetivo exclusivo

Entregar a tela real, normal e navegável de Estilo, aberta por `F4`, contendo:

```text
TELA DE ESTILO
├── CABEÇALHO
├── CONSOLE
│   └── navegação em dois níveis
└── BARRA DE MENUS
```

O objetivo é somente estrutural: quatro categorias no primeiro nível, presets
reais no segundo nível, foco/cursor válidos, navegação funcional e resize com
redesenho correto. H-0063 pode ser aprovado sem alterar qualquer estilo.

A tela não é popup, modal, overlay ou painel flutuante sobre outra tela.

## 4. Escopo funcional

### 4.1 Tela normal

- Usar o pipeline normal de tela declarativa.
- Declarar um Cabeçalho normal, um Console normal e uma Barra de Menus normal.
- O Cabeçalho deve ser produzido pelo renderer normal a partir da configuração
  declarativa, sem título artesanal no renderer de Estilo.
- O Console deve receber uma projeção de conteúdo em memória, derivada dos
  dados reais de Estilo, mas continuar sendo um Console normal do modelo e do
  renderer.
- A Barra de Menus pertence à tela completa, fora do corpo, e deve obedecer à
  declaração da tela e às regras canônicas.

### 4.2 Primeiro nível

O primeiro nível contém exatamente estes quatro pais, nesta ordem estrutural:

1. `borda`
2. `chip`
3. `indicadores.selecionado`
4. `indicadores.incluido`

O item corrente e a seleção vigente podem ser indicados passivamente, mas não
criam categorias adicionais. Não mostrar `tiling`, `cor_inativo`, `cor_alerta`
ou `indicadores.concluido`.

### 4.3 Segundo nível e fonte dos dados

Cada pai deve construir seus filhos dinamicamente a partir do mapa `presets`
do próprio caminho em `config/estilo.json`:

```text
borda                         → borda.presets
chip                          → chip.presets
indicadores.selecionado       → indicadores.selecionado.presets
indicadores.incluido          → indicadores.incluido.presets
```

Não hardcodar nomes, símbolos, quantidade ou lista paralela de filhos. Um
preset sintético acrescentado em uma cópia de teste de `config/estilo.json`
deve aparecer como novo filho sem alteração enumerativa no código.

`indicadores.concluido` não entra na projeção porque não é um dos quatro pais
e não fornece o catálogo de presets desta tela.

### 4.4 Estado navegacional e fronteira com mutação de estilo

H-0063 distingue dois planos de estado, que nunca se confundem:

**A. Estado navegacional canônico** (reutilizado da política
`dois_niveis_por_foco`, conforme H-0055 e `contrato_console.md`
§§22.11–22.18):

- pai corrente: posição do cursor no toroide de pais;
- filho corrente: posição do cursor no toroide de filhos do pai corrente;
- filho escolhido por pai: escolha exclusiva mantida pela política canônica,
  independente do cursor, transferida somente por `Espaço` sobre um filho.

**B. Mutação de estilo**:

- candidato;
- `preset_default` persistido em `config/estilo.json`;
- estilo global materializado;
- publicação.

A escolha de filho descrita em A pertence integralmente à política
navegacional canônica. Ela **não** significa executar nenhuma ação de B.

Ao construir os pais a partir do catálogo, cada pai possui exatamente um
filho escolhido; esse filho inicial corresponde à projeção observacional do
`preset_default` daquele pai — leitura, não mutação. `Espaço` sobre um filho
transfere a escolha exclusiva interna daquele pai, conforme a política
canônica; essa transferência é estado de runtime navegacional e não altera
candidato, `config/estilo.json`, `preset_default` persistido, materialização
global nem publicação. `Esc` retornando ao toroide de pais preserva o filho
escolhido de cada pai, sem limpar ou cancelar. Mover o cursor entre filhos sem
acionar `Espaço` não transfere a escolha — cursor (filho corrente) e escolha
(filho escolhido) são mecanismos independentes, já fechados por H-0055 e por
`contrato_console.md`/`contrato_barra_de_menus.md` §9.

H-0063 não implementa `Espaço` escolhendo preset, candidato ou qualquer
mutação de estilo. A transferência da escolha exclusiva de filho é
inteiramente observacional/navegacional neste ciclo e não chama mutação de
candidato.

## 5. Navegação em dois níveis

Declarar e reutilizar literalmente a política canônica
`politica_navegacao.tipo: dois_niveis_por_foco`, conforme H-0055 e
`docs/contratos/contrato_console.md` §22.16. Não criar política nova, terceiro
nivel, geometria ou decoder paralelo.

Vocabulário: **filho corrente** é o item em foco/cursor dentro do toroide de
filhos do pai corrente; **filho escolhido** é a opção exclusiva daquele pai
mantida pela política canônica (§4.4). Navegação por setas muda somente o
filho corrente; `Espaço` sobre filho transfere o filho escolhido. Testes,
demonstração e critérios de aceite usam os dois termos de forma consistente,
nunca como sinônimos.

Com um único Console focalizável:

- foco inicial: o Console de Estilo, com primeiro pai válido sob o cursor;
- item corrente: sempre um pai ou filho existente na projeção atual;
- ↑/↓/←/→: usar os movimentos já fornecidos pela navegação vigente; no nível
  dos pais, percorrer o toroide único de pais; no nível dos filhos, percorrer
  somente o toroide dos filhos do pai corrente;
- bordas: obedecer ao wrap/borda do mecanismo canônico, sem cruzar do toroide
  de um pai para o de outro;
- `Espaço` sobre pai: entrar/expor o toroide dos filhos pelo mecanismo vigente,
  reconciliando o filho corrente para um filho válido — inicialmente o filho
  escolhido daquele pai — sem alterar preset, candidato ou estilo global;
- no nível dos filhos, setas movem somente o filho corrente (cursor); não
  transferem a escolha exclusiva e não escolhem preset;
- `Espaço` sobre filho: transfere a escolha exclusiva do pai corrente para o
  filho corrente, conforme a política canônica de `dois_niveis_por_foco`
  (H-0055); o filho anteriormente escolhido deixa de estar escolhido; essa
  transferência é estado de runtime navegacional e não altera preset,
  candidato, `preset_default` persistido, estilo global ou publicação;
- `Esc` no nível dos filhos: retornar ao toroide de pais, preservando o filho
  corrente e o filho escolhido de cada pai, sem limpar ou cancelar estado de
  Estilo — rótulo contextual `[Esc] Retornar aos pais`;
- `Esc` no nível dos pais: voltar à tela anterior pela pilha normal,
  preservando as escolhas de todos os pais — rótulo contextual dinâmico
  conforme `docs/contratos/contrato_barra_de_menus.md` §9;
- foco, cursor, filho escolhido e representação dos níveis devem ser
  reconciliados antes de qualquer render ou interação após mudança de dados
  ou resize.

O chip contextual `[✥] Navegar` só aparece/atua segundo a regra canônica do
Console focalizado. A tecla física usada para entrada deve ser a já prevista
pela política vigente; nenhuma tecla nova é criada.

## 6. Cabeçalho, Console e Barra de Menus

### 6.1 Cabeçalho

Arquivo declarativo autorizado:
`config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json`.

Ele deve declarar `cabecalho.titulo` como `Estilo`, uma descrição da tela e o
bloco `apresentacao` completo. O renderer normal de tela deve produzir a região
superior. Não duplicar o Cabeçalho em `tela/estilo.py` ou em um renderer
específico.

### 6.2 Console

O shell declarativo deve conter um único elemento `tipo: console`, navegável,
com `politica_navegacao` declarada como `dois_niveis_por_foco`. O shell pode
permanecer sem itens concretos; o controlador deve associar, em memória e no
limite correto do modelo, a projeção de pais/filhos derivada dos `presets`.

O elemento deve também declarar `politica_selecao: multipla` como
compatibilidade declarativa exigida pelo mecanismo vigente de
`dois_niveis_por_foco` (H-0055) para reutilizar a apresentação e o chip de
Espaço. Isso não é reabertura de seleção múltipla genérica, não autoriza
escolher mais de um filho do mesmo pai e não muda o escopo funcional do
ITEM-0010: cada pai continua mantendo uma única escolha exclusiva de filho.

Usar a infraestrutura normal de conteúdo externo/modelo/renderização. O
renderer deve consumir a representação estrutural dos dois níveis, preservar
a ordem declarada, mostrar o cursor válido e não abrir renderer modal.

### 6.3 Barra de Menus

Declarar somente ações necessárias à navegação estrutural, preservando a ordem
canônica aplicável:

```text
[Esc] contextual (Retornar aos pais no nível dos filhos; Sair/Voltar no nível
dos pais, conforme dynamic Esc de contrato_barra_de_menus.md §9)
→ [✥] Navegar (contextual) → [␣] Selecionar (contextual) → [?] Ajuda
```

`[␣] Selecionar` reutiliza a identidade canônica já usada pelo mecanismo
`dois_niveis_por_foco` (H-0055 e `config/telas/demo/h0055_dois_niveis_por_foco.json`,
chip `selecionar`/texto `Selecionar`); não criar rótulo ou chip próprio como
`entrada no nível`. O mesmo `Espaço` cobre, conforme o estado do cursor: a
exposição/entrada no toroide de filhos quando o foco está em pai, e a
transferência da escolha exclusiva quando o foco está em filho — sem dois
chips concorrentes de Espaço.

`[?] Ajuda` é obrigatório, sempre ativo e último. A Barra deve usar a
infraestrutura normal de `barra_de_menus`; o renderer não pode inventar chips,
textos, teclas ou regras.

Não incluir `Aplicar`, confirmação, escolha de preset, F1, F2, F3, F5 ou F11.
Não incluir `Enter` como ação de aplicação. F4 é entrada global, não chip da
Barra.

## 7. Entrada F4 e saída

`F4` deve ser normalizado pelo decoder global vigente e tratado pelo dispatcher
central vigente, sem novo decoder ou dispatcher. A ação deve empilhar a tela
atual e abrir a tela normal de Estilo pelo identificador declarativo H-0063.

A saída é puramente navegacional: `Esc` no nível dos pais retorna pela pilha
normal. Não há confirmação, rollback, descarte de candidato, persistência,
publicação, promoção de baseline ou mudança de preset.

## 8. Resize e redesenho

Reutilizar a infraestrutura normal já vigente em `demo/demo.py`, baseada em
`SIGWINCH`, par coerente de largura/altura, últimas dimensões válidas, limpeza
e redesenho completo. Não criar geometria fixa de popup nem limiares
específicos de Estilo.

Para cada par válido de dimensões:

- recalcular áreas e linhas físicas da tela normal;
- manter Cabeçalho, Console e Barra de Menus em toda dimensão suportada;
- manter cada linha dentro da largura e o quadro dentro da altura;
- recompor os dois níveis e conservar/reconciliar pai corrente, filho
  corrente e filho escolhido válidos — a escolha exclusiva de cada pai não
  pode desaparecer por redraw;
- eliminar resíduos do frame anterior;
- preservar a composição declarativa, sem inventar ou remover regiões.

Quando a dimensão válida for insuficiente para a tela normal, usar o quadro
mínimo canônico de terminal pequeno, sem encerrar a sessão; ao crescer para
dimensão suficiente, restaurar automaticamente a tela normal completa.

## 9. Fora de escopo

### Alteração

- `Espaço` escolhendo preset;
- candidato, baseline, divergência, `Aplicar` ou qualquer mutação de estilo;
- amostras finais sofisticadas, preview completo ou tela demonstrativa do
  estilo.

A transferência da escolha exclusiva de filho pela política canônica
`dois_niveis_por_foco` (§4.4 e §5) não é `Espaço` escolhendo preset — é
estado navegacional obrigatório de H-0063 e não está listada como fora de
escopo.

### Confirmação e aplicação

- popup, modal, `CONFIRMADO`, `ABORTADO`;
- persistência, publicação global, promoção de baseline, runtime de aplicação;
- rollback, descarte de candidato ou E2E de aplicação.

### Trabalhos futuros

- F1, F11, F2, F3, F5;
- tiling por tela;
- restante do ITEM-0010 além desta fundação.

## 10. Relação com a implementação anterior

A implementação futura pode reaproveitar trechos corretos de H-0062, mas deve
remover qualquer shell popup-like, reconectar o conteúdo a uma tela normal,
simplificar antecipações e substituir trechos incompatíveis com este contrato.
Não há obrigação de preservar o desenho técnico reprovado. Infraestrutura
compartilhada só deve ser alterada quando necessária à integração normal.

## 11. Autoridades

Usar somente as seguintes autoridades documentais e referências focalizadas:

- `docs/contratos/contrato_tela_json.md` §§3, 7, 8, 18, 24 e 31–33 — estrutura
  macro, regiões, declaração, conteúdo externo e resize;
- `docs/contratos/contrato_json_cabecalho.md` — schema e renderer do Cabeçalho;
- `docs/contratos/contrato_console.md` §§20–22.11, 22.16–22.18 — fluxo de
  conteúdo, foco, cursor, dois níveis e demonstração;
- `docs/contratos/contrato_json_console.md` §7.1 — declaração da política;
- `docs/contratos/contrato_barra_de_menus.md` §§2, 4, 5, 8.2, 8.2.1 e 9 —
  região, declaração, ordem, Ajuda e Esc;
- `docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md` — composição da tela;
- `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` §§4.1–4.6 —
  dimensões, resize e preservação do item lógico;
- `docs/nomenclatura/30_CABECALHO.md` — Cabeçalho como região fixa;
- `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` — chips e integração de
  Estilo;
- `docs/nomenclatura/32_CONSOLE.md` e
  `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` —
  Console, foco/cursor e vocabulário multinível;
- `config/telas/demo/h0055_dois_niveis_por_foco.json` e
  `config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json` — referência
  concreta da política, sem copiar seus nomes ou dados para Estilo.

## 12. Arquivos autorizados para futura implementação

Somente os caminhos nominais abaixo ficam autorizados para a implementação e
seu registro:

### Tela/controlador

- `tela/estilo.py` — projetar os quatro pais e filhos dinâmicos, estado
  navegacional, foco/cursor e saída sem mutação de Estilo.

### Configuração declarativa

- `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json` — shell
  normal com Cabeçalho, um Console e Barra de Menus; não listar presets.

### Renderização e integração normal

- `tela/renderizacao/estilo.py` — somente adaptação/projeção de conteúdo, se
  necessária; não compor popup, moldura ou Cabeçalho próprio.
- `tela/renderizador.py` — somente integração focal para que a tela passe pelo
  renderer normal, se necessária; não duplicar geometria.
- `tela/renderizacao/contexto_execucao.py` — somente remoção ou ajuste mínimo
  de contexto transitório específico de aplicação legado, preservando a
  infraestrutura normal de foco, seleção e dimensões.
- `demo/demo.py` — reutilizar decoder/dispatcher global F4, pilha de telas,
  carregamento normal e resize vigente; não criar caminho paralelo.

Não autorizar alterações em `config/estilo.json`, `tela/loader.py`,
`tela/navegacao.py`, `tela/selecao.py`, `tela/renderizacao/tela.py`,
`tela/renderizacao/console.py` ou nos contratos: são fontes/infraestrutura
canônicas a consumir.

### Fixture/demo e testes

- `tela/teste_estilo_h0063.py` — controlador, projeção dinâmica, navegação e
  ausência de mutação de Estilo.
- `demo/teste_demo_estilo_h0063.py` — F4, ciclo da tela, render normal e
  resize simulável.
- `docs/relatorios/IMP-0063-tela-estilo-estrutura-navegacao-dois-niveis.md` —
  relatório futuro da implementação, com arquivos efetivamente alterados,
  testes e validação TTY.

Não criar fixture persistente paralela de presets: testes devem copiar
`config/estilo.json` para diretório temporário quando precisarem adicionar um
preset sintético.

## 13. Testes automatizados mínimos

### Estrutura

- F4 abre uma tela normal pelo caminho declarativo H-0063.
- O resultado contém Cabeçalho, Console e Barra de Menus normais.
- `[?] Ajuda` existe, está ativo e é o último chip.
- Não existe popup, modal, overlay ou renderer modal no fluxo.

### Dados e projeção

- O primeiro nível contém exatamente os quatro pais exigidos.
- O segundo nível deriva exclusivamente de `presets`.
- Um preset sintético em fixture aparece sem enumeração no código.
- A primeira projeção não mostra `tiling`, `cor_inativo`, `cor_alerta` ou
  `indicadores.concluido`.

### Navegação e fronteira de estado

- Foco inicial e item corrente são válidos.
- Pais movimentam-se no toroide dos pais; entrada, filhos, bordas e retorno
  obedecem à política `dois_niveis_por_foco`.
- Cada pai inicia com exatamente um filho escolhido, correspondente à
  projeção observacional de `preset_default` daquele pai.
- Mover o cursor entre filhos altera o filho corrente e não altera o filho
  escolhido.
- `Espaço` sobre um filho transfere a escolha exclusiva dentro do pai; o
  filho anteriormente escolhido deixa de estar escolhido; outros pais
  preservam suas próprias escolhas; `config/estilo.json` permanece intacto;
  candidato e estilo global não são alterados.
- `Esc` no nível dos filhos retorna ao toroide de pais e preserva o filho
  escolhido; o rótulo contextual corresponde à política vigente
  (`[Esc] Retornar aos pais`).
- O chip de Espaço da Barra de Menus usa a identidade canônica
  `[␣] Selecionar`; não existe rótulo `entrada no nível` como semântica nova;
  `[?] Ajuda` permanece o último chip.
- Nenhuma seta, entrada, retorno, transferência de escolha ou resize produz
  persistência, publicação, `Aplicar` ou alteração real de `preset_default`,
  candidato, baseline ou estilo global.

### Resize

Renderizar em dimensões larga, média, estreita suportada, baixa e após
crescimento. Verificar sem exceção, sem resíduos, conteúdo dentro da largura e
altura, Cabeçalho/Console/Barra preservados quando a dimensão é suportada,
foco/cursor reconciliados e ausência de geometria fixa de popup. Para dimensão
abaixo do mínimo canônico, verificar o quadro mínimo e sua recuperação após
crescimento.

## 14. Demonstração reproduzível

Definir no fluxo real da demonstração uma entrada reproduzível que:

1. inicia a demo normal;
2. aciona F4 físico ou o comando normalizado `F4` fora de TTY;
3. mostra a tela completa e os quatro pais;
4. entra no segundo nível, percorre filhos (filho corrente), aciona `Espaço`
   para transferir o filho escolhido, retorna ao pai por `Esc` preservando a
   escolha e sai pela pilha;
5. observa pai corrente, filho corrente e filho escolhido como estados
   distintos, sem qualquer mutação de estilo;
6. permite simular resize quando o mecanismo de teste suportar isso.

A demonstração deve usar o shell declarativo H-0063 e a projeção dinâmica de
`config/estilo.json`. Ela não substitui validação visual humana.

## 15. Validação manual futura

Executar somente validação TTY material: F4 físico; aparência inequívoca de
tela completa; Cabeçalho, Console e Barra de Menus; quatro pais e presets reais
em dois níveis; navegação real; resize para redução e crescimento; ausência de
resíduos; foco/cursor válido; legibilidade estrutural. A validação não inclui
escolha, aplicação ou confirmação de preset.

## 16. Critérios de aceite

H-0063 está concluído quando:

- F4 abre uma tela normal de Estilo, não popup;
- Cabeçalho, Console e Barra de Menus aparecem pelo renderer normal;
- exatamente quatro categorias e seus presets reais aparecem em dois níveis;
- a política canônica `dois_niveis_por_foco` permite foco, cursor, movimento,
  entrada e retorno válidos, distinguindo pai corrente, filho corrente e
  filho escolhido;
- `Espaço` sobre filho transfere a escolha exclusiva daquele pai; `Esc` no
  nível dos filhos retorna aos pais preservando essa escolha
  (`[Esc] Retornar aos pais`);
- resize não quebra a composição nem deixa resíduos, e reconcilia pai
  corrente, filho corrente e filho escolhido;
- navegar, transferir a escolha de filho ou redimensionar não altera preset
  persistido, candidato, baseline ou estilo global;
- não há Aplicar, confirmação, persistência, publicação ou aplicação
  antecipada.

## 17. Fronteira posterior

Após a aprovação de H-0063, o restante do ITEM-0010 será reparticionado
incrementalmente. A próxima partição será decidida pelo gerente depois de
observar o resultado real desta fundação. Este documento não numera nem
especifica integralmente handoffs posteriores.
