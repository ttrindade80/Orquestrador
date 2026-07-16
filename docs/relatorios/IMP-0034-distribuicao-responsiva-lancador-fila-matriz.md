# Relatório de Implementação — H-0034

```yaml
etapa: IMPLEMENTAR
handoff: H-0034
titulo: "Distribuição responsiva do lançador entre fila e matriz"
data: 2026-07-15
executor: implementacao
status_neutral: implementado (NAO autoaprovado)
patch_implementacao:
  data: 2026-07-15
  qa_reprovador: docs/relatorios/RELATORIO_QA_H-0034_IMPLEMENTACAO.md
  achados_corrigidos:
    - QA-H0034-IMPL-ALTO-001  # alinhamento horizontal lido da instancia
    - QA-H0034-IMPL-MEDIO-001  # correcoes neste relatorio
  achados_bloqueados: {}  # ALTO-002 corrigido no PATCH_IMPLEMENTACAO (secao 39)
```

---

## 1. Identificação da etapa

Etapa `IMPLEMENTAR`. Implementa estritamente o handoff H-0034 aprovado
(`docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md`) e a
ADR-0023 aplicada. Não decide arquitetura, não altera autoridades documentais,
não faz QA formal, não aprova a própria implementação, não executa validação
humana em TTY real, não prepara nem executa commit.

## 2. Handoff aprovado

```yaml
arquivo: docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
```

## 3. QA final do handoff

```yaml
relatorio_qa_final: docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0034_HANDOFF.md
status_literal: H1_HANDOFF_APPROVED
status_normalizado: APROVADO
achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 0
regressoes: 0
validacao_manual: NAO_EXECUTADA
observacao_nao_bloqueante: QA-H0034-POS2-HANDOFF-OBS-001
```

Observação `QA-H0034-POS2-HANDOFF-OBS-001` (tratada na seção 21/22 deste
relatório): os vetores `[20,60]` e `[21,59]` são **pesos relativos**, não
larguras absolutas; as cotas reais produzidas pelo algoritmo de maiores restos
foram calculadas e registradas abaixo, não apenas repetidas.

## 4. Autoridades documentais

Lidas integralmente:

- `docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md`
- `docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0034_HANDOFF.md`
- `docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0034_HANDOFF.md`
- `docs/adr/ADR-0023-largura-minima-funcional-lancador.md`
- `docs/adr/ADR-0017-redimensionamento-reativo-tui.md` (seção 9 — mecanismo
  canônico do quadro mínimo reutilizado)
- `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md`
- `docs/relatorios/RELATORIO_APLICACAO_ADR-0023.md`
- `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0023.md`
- `docs/contratos/contrato_lancador.md` (seções 6.1–6.7, R-11 a R-14)
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/NOMENCLATURA.md` (seções 6.2, 6.3, 8.1–8.3)
- `config/elementos/lancador.json`
- `config/telas/demo/demo.json`
- `tela/modelo.py`, `tela/renderizador.py`, `tela/teste_renderizador.py`,
  `demo/demo.py`

## 5. Estado Git inicial

Capturado antes de qualquer alteração, a partir da raiz do projeto:

```bash
git status --short
git diff --name-only
git diff --check
git diff --cached --name-only
```

`git status --short` inicial:

```text
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_lancador.md
 M docs/contratos/contrato_tela_json.md
?? demo/__pycache__/
?? docs/adr/ADR-0023-largura-minima-funcional-lancador.md
?? docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
?? docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0034_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0034_HANDOFF.md
?? tela/__pycache__/
```

`git diff --name-only`: os 5 documentos normativos acima (todos da etapa
`APLICAR_ADR` da ADR-0023, anteriores a esta implementação).

`git diff --check`: sem saída (código 0).

`git diff --cached --name-only`: sem saída (código 0); stage vazio.

## 6. Itens não rastreados iniciais

```yaml
demo/__pycache__/:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
tela/__pycache__/:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
docs/adr/ADR-0023-largura-minima-funcional-lancador.md:
  origem: NAO_CONFIRMADA  # etapa ADR anterior
docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md:
  origem: NAO_CONFIRMADA  # etapa PATCH_HANDOFF anterior
docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md:
  origem: NAO_CONFIRMADA
docs/relatorios/RELATORIO_APLICACAO_ADR-0023.md:
  origem: CONFIRMADA  # etapa APLICAR_ADR ADR-0023 anterior
docs/relatorios/RELATORIO_QA_ADR-0023.md:
  origem: NAO_CONFIRMADA
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0023.md:
  origem: CONFIRMADA  # etapa QA_APLICACAO_ADR anterior
docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md:
  origem: NAO_CONFIRMADA  # etapa QA_HANDOFF anterior
docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md:
  origem: NAO_CONFIRMADA
docs/relatorios/RELATORIO_QA_POS_PATCH_H-0034_HANDOFF.md:
  origem: CONFIRMADA  # etapa QA_POS_PATCH anterior
docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0034_HANDOFF.md:
  origem: CONFIRMADA  # etapa QA_POS_SEGUNDO_PATCH anterior
```

Nenhum item não rastreado foi removido, movido ou atribuído sem evidência.

## 7. Arquivos alterados

```yaml
arquivos_alterados:
  - tela/renderizador.py        # implementacao (autorizado H-0034 secao 6.1)
  - tela/teste_renderizador.py  # testes focais + atualizacao de snapshots/contagens
  - demo/teste_demo.py          # excecao operacional autorizada (secao 35)
  - demo/teste_diagnostico.py   # excecao operacional autorizada (secao 35)
arquivos_criados:
  - docs/relatorios/IMP-0034-distribuicao-responsiva-lancador-fila-matriz.md  # este relatorio
```

Os 5 documentos normativos em `git diff` (`docs/NOMENCLATURA.md`,
`docs/adr/INDICE_ADR.md`, `docs/contratos/contrato_*.md`) NÃO foram tocados por
esta etapa — são modificações preexistentes da etapa `APLICAR_ADR` da ADR-0023.

## 8. Algoritmo implementado

`_linhas_lancador(elemento, content_w)` (em `tela/renderizador.py`) implementa a
sequência normativa de decisão do handoff H-0034 seção 3.4 e da ADR-0023 seção
3.3 / `contrato_lancador.md` 6.7:

```text
obter content_w (largura interna da caixa do lancador)
→ calcular coluna_minima_content_w
→ se content_w < coluna_minima_content_w:
    sinalizar _quadro_minimo_lancador_ativo = True; retornar []
→ testar fila (content_w >= fila_content_w_min?)
    sim → 1 linha com todos os itens; distribuir excesso (vaos → margens → direita)
→ testar matrizes validas (n_rows = 2 .. n_itens, crescente em linhas)
    primeiro (n_rows, n_col=ceil(n/n_rows)) que couber → matriz
→ coluna minima (n_col=1, n_rows=n_itens) — já garantido por content_w >= min
```

O sinal `_quadro_minimo_lancador_ativo` (atributo de módulo) é redefinido para
`False` no início de cada `renderizar_tela` (renderer puro, R-14) e, quando
`True` ao final do assembly, `renderizar_tela` retorna
`_quadro_minimo_global(total_w, altura)` em vez da tela normal — substituindo
integralmente cabeçalho, corpo, `lancador`, dashboards e `barra_de_menus`
(ADR-0017 seção 9 / ADR-0023 seção 3.2 / R-12, R-13).

Margens verticais canônicas (1 linha em branco acima do primeiro item e 1
abaixo do último, `contrato_lancador.md` 6.6) são incluídas nas linhas de
conteúdo retornadas em todos os modos válidos (fila, matriz, coluna mínima).

Distribuição de excesso (após o modo escolhido, `contrato_lancador.md` 6.5 /
`config/elementos/lancador.json` distribuicao_de_sobra):

1. expandir vãos entre itens/colunas até o máximo (5), cada vão
   independentemente, maiores-restos nos primeiros vãos;
2. expandir margens (esquerda depois direita) até o máximo (5);
3. excesso restante à direita (alinhamento `"esquerda"` da instância demo —
   propriedade da instância, não regra universal).

## 9. Distinção entre obrigação e caminho técnico

- **Obrigação normativa**: fila/matriz/coluna-mínima, ordem
  coluna-a-coluna, largura por maior item da própria coluna, sub-colunas
  independentes, margens verticais, alinhamento por instância, gatilho do
  quadro mínimo global quando `content_w < coluna_minima_content_w`,
  recuperação automática. Derivam do handoff H-0034 e da ADR-0023.
- **Caminho técnico**: `_linhas_lancador(elemento, content_w)`,
  `_quadro_minimo_lancador_ativo` (sinal de módulo), `_quadro_minimo_global()`,
  `_caixa_de_elemento` repassando `content_w`. Estes são nomes privados e
  estruturas compatíveis com a implementação atual — não normas
  arquiteturais permanentes. A obrigação é comportamental.

## 10. Cinco grandezas de largura

```text
terminal_w            : largura total do terminal/viewport
area_lancador_w       : largura total da caixa alocada ao lancador (bordas+padding)
lancador_caixa_min_w  : largura mínima total da caixa do lancador
content_w             : largura interna após descontar bordas e padding
coluna_minima_content_w: largura mínima do conteúdo para uma coluna válida
```

Relação factual da estrutura atual (`_caixa`/`_linha_conteudo`):
`content_w = area_lancador_w - 3` (1 borda vertical esquerda + 1 padding
esquerdo + 1 borda vertical direita). Não é regra eterna — se a estrutura da
caixa mudar, recalcular.

Comparações normativas usadas (mesmo domínio):

```text
content_w < coluna_minima_content_w      (domínio do conteúdo)
area_lancador_w < lancador_caixa_min_w   (domínio da caixa completa)
```

Nenhuma comparação mistura `terminal_w` com `coluna_minima_content_w`.

## 11. Cálculo de fila

`fila_content_w_min = margem_min + Σ(item_w_min) + (n-1)·vao_itens_min + margem_min`

Para a demo (7 itens):

```text
Σ item_w_min = 11+14+11+13+14+14+14 = 91
vaos internos = 6 × 2 = 12
margens = 2 + 2 = 4
fila_content_w_min = 91 + 12 + 4 = 107  → area_lancador_w min = 110
```

## 12. Cálculo de matrizes

Matrizes válidas avaliadas em ordem crescente de `n_rows` (decrescente em
colunas); o primeiro que cabe é escolhido:

```text
matriz 4×2 (n_rows=2, n_col=4): col_w=[14,13,14,14], min = 65 → area min 68
matriz 3×3 (n_rows=3, n_col=3): col_w=[14,14,14],   min = 50 → area min 53
matriz 2×4 (n_rows=4, n_col=2): col_w=[14,14],       min = 34 → area min 37
```

## 13. Colunas independentes

Cada coluna tem largura calculada pelo maior item da própria coluna (chip-sub
+ vao_chip_texto + texto-sub), não pelo maior item global. Provado em T-07
(col_w_0=17 ≠ col_w_1=6) e em T-11 (demo 80: col0=14, col1=13, col2=14,
col3=14). Ver seções 18 e 27.

## 14. Alinhamento por instância

**Corrigido por PATCH_IMPLEMENTACAO (QA-H0034-IMPL-ALTO-001).**

O renderer lê `elemento._campos_inertes.get("layout") or {}` e obtém
`alinhamento = layout_inst.get("alinhamento")`, aplicando a semântica
correspondente (R-10 / `contrato_lancador.md` 6.4):

- `"esquerda"` ou `None`: excesso residual à direita do bloco (`exc_esq=0`).
- `"direita"`: excesso residual à esquerda do bloco (`exc_dir=0`).
- `"centro"`: excesso dividido; maiores-restos para a esquerda
  (`esq = (excesso+1)//2`).
- valor desconhecido: `RenderizadorErro` imediato (R-10).

A lógica está em `_split_excesso_lancador(excesso, alinhamento)` (função de
módulo) e é aplicada na fila (Passo 3), na matriz (Passo 3 de `_tentar_matriz`)
e na coluna mínima (com `excesso_min = content_w - coluna_minima_content_w`).

Para a demo (`config/telas/demo/demo.json` declara `layout.alinhamento =
"esquerda"`), o excesso vai à direita — comportamento idêntico ao que a
implementação inicial produzia por hardcoding. A implementação inicial não lia o
campo e divergia para `"centro"` e `"direita"`, o que foi refutado por
QA-H0034-IMPL-ALTO-001.

Testes genéricos não generalizam o valor da demo; a propriedade pertence à
instância declarante.

## 15. Coluna mínima

```text
max_chip_sub = 3   (todos os chips da demo têm 1 caractere)
max_texto_sub = 10 (Grupo Min., Matriz 2x2, Matriz 3x2, Matriz 2x4)
coluna_minima_content_w = 2 + 3 + 1 + 10 + 2 = 18
lancador_caixa_min_w = 18 + 3 = 21
```

`content_w >= 18` (area >= 21) permite coluna única completa. Abixo disso:
quadro mínimo global.

## 16. Quadro mínimo global

Quando `content_w < coluna_minima_content_w`, `_linhas_lancador` atribui
`_quadro_minimo_lancador_ativo = True` e retorna `[]`. Ao final,
`renderizar_tela` retorna `_quadro_minimo_global(total_w, altura)`, que:

- substitui integralmente toda a tela normal;
- não preserva cabeçalho, corpo, `lancador`, dashboards nem `barra_de_menus`;
- não cria mensagem local do `lancador`;
- não trunca, não pagina, não omite itens;
- adequa o aviso textual à largura ("terminal pequeno demais" ≥ 23 chars;
  "tela peq." entre 9 e 22; vazio abaixo de 9);
- cabe estritamente nas dimensões atuais (sem overflow/scroll).

## 17. Recuperação

O renderer é puro: o sinal de quadro mínimo é redefinido no início de cada
`renderizar_tela`. A recuperação é determinística — mesma entrada produz
mesma saída, independentemente de chamadas anteriores. Provado em T-ISOL-03
(sequência 21→20→21: `s_passo1 == s_passo3`).

## 18. Provas em 80, 109 e 110 (demo)

```yaml
prova_demo_110:
  area_lancador_w: 110
  content_w: 107
  modo: fila
  resultado: "[d] e [g] na mesma linha (row 20); 7 chips presentes;
    [d] inicia na posicao absoluta 4 (conteudo 2); [g] na posicao 17 (conteudo 15);
    1 linha de conteudo de itens; 6 vaos internos = 2; margens = 2; sem segunda linha;
    sem quadro minimo."
prova_demo_109:
  area_lancador_w: 109
  content_w: 106
  modo: matriz 4x2
  resultado: "[d] e [g] em linhas diferentes; matriz valida escolhida; quadro
    minimo NAO acionado; nenhum item perdido."
prova_demo_80:
  area_lancador_w: 80
  content_w: 77
  modo: matriz 4x2
  preenchimento: coluna_a_coluna
  colunas:
    col0: [d, g]        col_w: 14
    col1: [1, 2]        col_w: 13
    col2: [3, 4]        col_w: 14
    col3: [5]           col_w: 14
  distribuicao_excesso_12:
    vaos_internos_3: "cada um expande 3 (min 2 -> 5); absorvido 9"
    margens: "esquerda absorve 3 (2 -> 5); direita absorve 0; restante 0"
    sobra_direita: 0
  posicoes_iniciais_colunas:
    col0: 5   # borda(1)+pad(1)+margem_esq(3)... [d] na posicao absoluta 5+2... ver T-11
  alinhamento: esquerda  # propriedade da instancia demo
  resultado: "row0=[d][1][3][5]; row1=[g][2][4]; 7 chips presentes; sem
    paginacao; sem quadro minimo; cabecalho/barra/NAVEGAR preservados."
```

Distâncias verificadas em T-11 (linha 0 da matriz em area=80):

```text
[d] -> [1] : 19  (col_w_0=14 + vao=5)
[1] -> [3] : 18  (col_w_1=13 + vao=5)
[3] -> [5] : 19  (col_w_2=14 + vao=5)
```

`col_w_1 (13) ≠ col_w_0 (14)` comprovado pelas distâncias 18 ≠ 19.

## 19. Provas suplementares globais 20/21

```yaml
largura_total_20:
  isola_gatilho_interno_do_lancador: false
  finalidade: fronteira suplementar (demo em arranjo vertical; terminal_w ==
    area_lancador_w; o quadro minimo pode ser acionado pelo minimo global
    preexistente da tela, ADR-0017)
  resultado: "area=20 -> content_w=17 < 18 -> nenhum chip presente (quadro
    minimo). NAO prova causalmente o gatilho interno do lancador."
largura_total_21:
  isola_gatilho_interno_do_lancador: false
  finalidade: fronteira suplementar
  resultado: "area=21 -> content_w=18 = coluna_minima -> coluna unica valida,
    7 chips presentes. NAO prova causalmente o gatilho interno do lancador."
```

Elas não substituem a prova causal isolada (seção 20).

## 20. Prova isolada do gatilho interno

Modelo em memória `teste_isolamento_lancador` (arranjo `horizontal`,
distribuicao `fracao`), `terminal_w=80` constante; o `lancador` recebe
`area_lancador_w` via pesos fracao, independente do viewport global. Segundo
elemento `console_resto` (tipo funcional fechado, válido, incapaz de acionar
falha própria; cotas 60/59 ≥ mínimo operacional de 10 do particionamento
horizontal). Ver seção 25 para validade do `console_resto`.

```yaml
prova_isolada:
  terminal_w: 80
  largura_distribuivel: 80
  modo_distribuicao: fracao
  pesos_insuficiente: [20, 60]
  pesos_valido: [21, 59]
  denominadores: 80   # soma dos pesos em ambos os casos
  cotas_ideais:
    insuficiente: [20.0, 60.0]
    valido: [21.0, 59.0]
  arredondamentos: floor (parte inteira)
  maiores_restos: "nao aplicavel — faltam=0 em ambos os casos"
  area_lancador_w_insuficiente: 20
  area_lancador_w_valida: 21
  area_resto:
    insuficiente: 60
    valido: 59
  lancador_caixa_min_w: 21
  coluna_minima_content_w: 18
  minimo_global_tela_satisfeito: true   # controle T-ISOL-02 produziu tela normal
  demais_componentes_validos: true
  causa_do_quadro_minimo: area_lancador_w (20) < lancador_caixa_min_w (21)
  evidencias:
    - "controle T-ISOL-02: terminal_w=80 + area_lancador_w=21 -> tela normal (7 chips)"
    - "caso T-ISOL-01: terminal_w=80 + area_lancador_w=20 -> quadro minimo global (0 chips)"
```

## 21. Cálculo real dos pesos `[20,60]`

`fracao` representa **pesos relativos**, não larguras absolutas. Neste cenário
a largura distribuível é 80 e a soma dos pesos também é 80, então o algoritmo
de maiores restos produz cotas inteiras exatas:

```text
largura_distribuivel = 80
pesos = [20, 60]
soma_pesos = 80
ideal_lancador = 80 × 20 / 80 = 20.0
ideal_console  = 80 × 60 / 80 = 60.0
partes_inteiras (floor) = [20, 60]
faltam = 80 - (20 + 60) = 0
maiores_restos = não aplicável
cotas_finais = [20, 60]
area_lancador_w_real = 20
content_w_lancador = 20 - 3 = 17  <  coluna_minima_content_w (18)
resultado = quadro mínimo global
```

## 22. Cálculo real dos pesos `[21,59]`

```text
largura_distribuivel = 80
pesos = [21, 59]
soma_pesos = 80
ideal_lancador = 80 × 21 / 80 = 21.0
ideal_console  = 80 × 59 / 80 = 59.0
partes_inteiras (floor) = [21, 59]
faltam = 80 - (21 + 59) = 0
maiores_restos = não aplicável
cotas_finais = [21, 59]
area_lancador_w_real = 21
content_w_lancador = 21 - 3 = 18  =  coluna_minima_content_w (18)
resultado = tela normal (coluna mínima válida completa)
```

A observação `QA-H0034-POS2-HANDOFF-OBS-001` foi tratada: as cotas reais foram
demonstradas, não apenas repetidas. Confirmadas computacionalmente via
`_distribuir_larguras(80, [20,60]) == [20,60]` e
`_distribuir_larguras(80, [21,59]) == [21,59]` (cobertura em
`test_isolamento_gatilho_interno`).

## 23. `area_lancador_w` final em cada cenário

```yaml
fila_110:        area_lancador_w=110, content_w=107, modo=fila
matriz_109:      area_lancador_w=109, content_w=106, modo=matriz 4x2
matriz_80:       area_lancador_w=80,  content_w=77,  modo=matriz 4x2
supl_21:         area_lancador_w=21,  content_w=18,  modo=coluna minima
supl_20:         area_lancador_w=20,  content_w=17,  modo=quadro minimo global
isol_T-ISOL-01:  area_lancador_w=20,  content_w=17,  modo=quadro minimo global
isol_T-ISOL-02:  area_lancador_w=21,  content_w=18,  modo=coluna minima (tela normal)
```

## 24. Comprovação de que o mínimo global da tela estava satisfeito

O controle T-ISOL-02 usa `terminal_w=80`, `area_lancador_w=21`, o mesmo
cabeçalho, a mesma barra, os mesmos 7 itens e o mesmo segundo elemento
(`console_resto`) do caso insuficiente T-ISOL-01. T-ISOL-02 produziu **tela
normal** com os 7 chips presentes. Portanto os requisitos globais da tela
estavam satisfeitos em ambos os casos. A única diferença material entre
T-ISOL-01 e T-ISOL-02 é `area_lancador_w` (20 vs 21), provando que o quadro
mínimo em T-ISOL-01 foi causado exclusivamente por
`area_lancador_w (20) < lancador_caixa_min_w (21)`.

## 25. Validade do `console_resto`

`console_resto` é `ElementoCorpo(id="console_resto", tipo="console",
_campos_inertes={"titulo": "Console"})`:

- `console` é tipo funcional fechado já suportado (`_linhas_console` retorna o
  placeholder estável `"(console)"`);
- não exige JSON novo nem campo contratual novo;
- as cotas reais alocadas (60 em T-ISOL-01, 59 em T-ISOL-02) são maiores que o
  mínimo operacional de 10 caracteres imposto ao particionamento horizontal
  (`_renderizar_container_horizontal` / `_montar_corpo_horizontal`);
- não aciona quadro mínimo por causa própria;
- resolvido exclusivamente com semântica existente.

## 26. Resultados de T-ISOL-01, T-ISOL-02 e T-ISOL-03

```yaml
T-ISOL-01:
  cenario: "modelo em memoria, terminal_w=80, fracao [20,60]"
  grandezas_esperadas: "area_lancador_w=20, content_w=17, lancador_caixa_min_w=21"
  resultado: "quadro minimo global — nenhum dos 7 chips do lancador presente;
    nenhum elemento da tela normal visivel"
  causa: "area_lancador_w < lancador_caixa_min_w (requisitos globais satisfeitos)"
T-ISOL-02:
  cenario: "mesmo modelo, terminal_w=80, fracao [21,59]"
  grandezas_esperadas: "area_lancador_w=21, content_w=18"
  resultado: "tela normal com uma coluna valida completa — 7 chips presentes,
    sem quadro minimo"
T-ISOL-03:
  cenario: "sequencia 21 -> 20 -> 21, terminal_w=80 constante"
  resultado: "s_passo1 == s_passo3 (determinismo); passo 3 contem os 7 chips
    (tela normal reconstruida)"
  nao_alegado: "este teste automatizado NAO valida sinais/SIGWINCH/redraw real/
    cursor/flicker/sessao TTY real — esses pontos permanecem para validacao humana"
```

## 27. Suíte focal

```bash
python -m pytest tela/teste_renderizador.py -q --tb=short
```

Resultado (pós-PATCH_IMPLEMENTACAO):

```text
228 passed, 3 warnings in 0.21s
```

Execução direta (contagem real de verificações `_registrar`):

```bash
python tela/teste_renderizador.py
```

```text
Total de verificacoes: 1042
Passaram: 1042
Falharam: 0
codigo de saida: 0
```

Contagem antes do patch: `227 passed`, `1018/1018`. O PATCH_IMPLEMENTACAO
adicionou 1 função de teste pytest (`test_alinhamento_horizontal_por_instancia`)
e 24 verificações internas `_registrar` cobrindo os três alinhamentos em fila e
matriz, alinhamento `None`, alinhamento inválido e regressão da demo. O pytest
conta funções, não verificações `_registrar`; a contagem autoritativa é a direta
acima.

## 28. Suíte canônica completa

Executados individualmente:

```yaml
tela/teste_loader.py:
  codigo_de_saida: 0
  verificacoes: 249/249
tela/teste_modelo.py:
  codigo_de_saida: 0
  verificacoes: 148/148
tela/teste_renderizador.py:
  codigo_de_saida: 0
  verificacoes: 1018/1018
demo/teste_demo.py:
  codigo_de_saida: 0
  verificacoes: 358/358
demo/teste_diagnostico.py:
  codigo_de_saida: 0
  verificacoes: 30/30
demo/teste_explorar_barra_de_menus.py:
  codigo_de_saida: 0
  verificacoes: 38/38
```

Total consolidado: **1838/1838 verificações, 6/6 códigos de saída zero**.

Diferença para a linha de base anterior (`1803/1803`): +35 verificações,
decorrentes dos novos testes H-0034 (+38 em `teste_renderizador.py`,
parcialmente compensado por ajustes de contagem em `demo/teste_demo.py` cujos
snapshots e contagens de altura foram atualizados para refletir o novo
comportamento). Nenhuma regressão.

## 29. Smoke do ponto de entrada

```bash
echo "s" | python demo/demo.py
```

Resultado: **código de saída 0**. Confirmado:

- ponto de entrada real demonstrativo funciona;
- identidade `demo` presente (`ORQUESTRADOR` na saída);
- presença dos 7 itens (`[d]`,`[g]`,`[1]`,`[2]`,`[3]`,`[4]`,`[5]`);
- `NAVEGAR` presente;
- ausência de erro de integração (sem `Traceback`).

O comando isolado **não comprova** os limiares exatos 80/109/110 (depende da
largura do terminal); código de saída zero isolado não comprova a identidade
da tela — esta foi confirmada pela inspeção de conteúdo acima.

## 30. Pseudo-TTY

Executado:

```bash
echo "s" | timeout 8 script -q /dev/null -c "python demo/demo.py"
```

Resultado: o `script` foi envolvido por `timeout` e terminou por timeout
(código 124 do `timeout`, não erro da demo). O conteúdo capturado (2173 bytes)
contém `ORQUESTRADOR` e `NAVEGAR`, sem `Traceback`. Isto confirma apenas a
**inicialização em ambiente TTY sem erro**; o travamento decorre da
incompatibilidade entre alimentação de texto por pipe e o modo TTY interativo
da demo, não de defeito do renderer. Pseudo-TTY **não substitui** observação
humana de layout, redraw ou transição visual (handoff seção 5.3).

## 31. Validação manual pendente

```text
VALIDACAO_MANUAL_PENDENTE_USUARIO
```

Comando e critérios previstos no handoff (seção 5.4) para execução posterior
pelo usuário:

```bash
python demo/demo.py
# Redimensionar progressivamente a janela do terminal:
# - largura inicial ampla (area_lancador_w >= 110): fila
# - reduzir < 110: matriz 4x2
# - reduzir progressivamente: matriz 3x3, 2x4, 1x7 (coluna unica)
# - reduzir para area_lancador_w < 21: quadro minimo global
# - ampliar para >= 21: restauracao automatica da tela normal
# Criterios: ausencia de cintilacao, residuos ou tela parcialmente preservada.
```

## 32. Estado Git final

```text
git status --short:
 M demo/teste_demo.py
 M demo/teste_diagnostico.py
 M docs/NOMENCLATURA.md            (preexistente APLICAR_ADR ADR-0023)
 M docs/adr/INDICE_ADR.md          (preexistente APLICAR_ADR ADR-0023)
 M docs/contratos/contrato_composicao_corpo.md  (preexistente APLICAR_ADR ADR-0023)
 M docs/contratos/contrato_lancador.md          (preexistente APLICAR_ADR ADR-0023)
 M docs/contratos/contrato_tela_json.md         (preexistente APLICAR_ADR ADR-0023)
 M tela/renderizador.py
 M tela/teste_renderizador.py
?? demo/__pycache__/
?? docs/adr/ADR-0023-largura-minima-funcional-lancador.md
?? docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
?? docs/relatorios/IMP-0034-distribuicao-responsiva-lancador-fila-matriz.md
?? docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0034_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0034_HANDOFF.md
?? tela/__pycache__/
```

`git diff --check`: sem saída (código 0). `git diff --cached --name-only`: sem
saída; **stage vazio**.

Arquivos alterados por esta etapa (fora os 5 preexistentes ADR-0023):
`tela/renderizador.py`, `tela/teste_renderizador.py`,
`demo/teste_demo.py`, `demo/teste_diagnostico.py` (estes dois últimos por
exceção operacional autorizada — seção 35).

## 33. Todos os itens não rastreados

```yaml
demo/__pycache__/: cache Python preexistente; nao removido
tela/__pycache__/: cache Python preexistente; nao removido
docs/adr/ADR-0023-largura-minima-funcional-lancador.md: etapa ADR anterior
docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md: etapa PATCH_HANDOFF anterior
docs/relatorios/IMP-0034-distribuicao-responsiva-lancador-fila-matriz.md: criado por esta etapa
docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md: etapa anterior
docs/relatorios/RELATORIO_APLICACAO_ADR-0023.md: etapa APLICAR_ADR anterior
docs/relatorios/RELATORIO_QA_ADR-0023.md: etapa anterior
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0023.md: etapa QA anterior
docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md: etapa QA anterior
docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md: etapa anterior
docs/relatorios/RELATORIO_QA_POS_PATCH_H-0034_HANDOFF.md: etapa QA anterior
docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0034_HANDOFF.md: etapa QA anterior
```

## 34. Caches criados ou observados

- `demo/__pycache__/`, `tela/__pycache__/`: preexistentes ao início da etapa
  (origem `NAO_CONFIRMADA`). Não removidos.
- Esta etapa pode ter atualizado bytecode nesses diretórios ao executar os
  scripts de teste e a demo. Esses caches não fazem parte da entrega e não
  foram incluídos no escopo.

## 35. Exceções operacionais autorizadas

```yaml
excecao_1:
  arquivo: demo/teste_demo.py
  motivo: >-
    Snapshots _EXPECTED_CURVA, _EXPECTED_RETA (largura 80 natural) e
    _EXPECTED_DIAGNOSTICO_CURVA_42, alem de contagem
    L_corpo_conteudo=14 / n_minimo=20, asserted o layout antigo do lancador
    (1 item por linha, sem margens verticais). A implementacao correta do
    H-0034 (fila/matriz + margens verticais) invalidou esses snapshots.
    6 verificacoes falhavam.
  escopo_exato: >-
    Atualizacao SOMENTE das constantes de snapshot (_EXPECTED_*) para refletir
    o novo layout, e ajuste de n_minimo 20->19 / L_corpo_conteudo 14->13 em
    comentario+assert. Sem alterar logica de producao, contratos, ADRs,
    handoff, config JSON nem demo.py.
  mudanca_esperada: codigo de saida 0 restaurado; 358/358.
  autorizacao: "Usuario autorizou atualizacao focal desta excecao operacional."
excecao_2:
  arquivo: demo/teste_diagnostico.py
  motivo: >-
    Snapshot _EXPECTED_ORQUESTRADOR (largura 42) asserted o layout antigo do
    lancador. 1 verificacao falhava.
  escopo_exato: >-
    Atualizacao SOMENTE da constante de snapshot para refletir o novo layout.
    Sem alterar logica.
  mudanca_esperada: codigo de saida 0 restaurado; 30/30.
  autorizacao: "Usuario autorizou atualizacao focal desta excecao operacional."
```

As exceções não criaram semântica, arquitetura, política, configuração nem
decisão documental. Foram estritamente atualização de snapshots/contagens de
teste para refletir o comportamento normativo novo.

## 36. Limitações

- Validação humana em TTY real não executada (seção 31).
- Pseudo-TTY só confirmou inicialização sem erro; não validou transições
  visuais (seção 30).
- **QA-H0034-IMPL-ALTO-002 (CORRIGIDO no PATCH_IMPLEMENTACAO — ver seção 39)**:
  Os parâmetros de tipo do `lancador` foram removidos do renderer e propagados
  via pipeline `loader → modelo → renderer`. Não há mais bloqueio.
- As margens verticais (1 branco topo + 1 branco base dentro da caixa do
  lancador) mudaram a altura natural das caixas NAVEGAR (9→8 linhas em largura
  42; 9→7 em largura 60), exigindo atualização de snapshots e contagens em
  `tela/teste_renderizador.py`, `demo/teste_demo.py` e
  `demo/teste_diagnostico.py`.

## 37. Fatos `NAO_CONFIRMADO`

```yaml
- item: demo/__pycache__/
  fato_nao_confirmado: origem do cache Python
- item: tela/__pycache__/
  fato_nao_confirmado: origem do cache Python
- item: arquivos nao rastreados preexistentes (ADR-0023, handoff H-0034, relatorios)
  fato_nao_confirmado: executor especifico que criou cada um em etapas anteriores
```

## 38. Bloqueios

**Atualizado por PATCH_IMPLEMENTACAO e por segundo PATCH_IMPLEMENTACAO.**

Nenhum bloqueio ativo. ALTO-002 foi corrigido no PATCH_IMPLEMENTACAO (seção 39)
com autorização para `tela/loader.py`, `tela/modelo.py`, `tela/teste_loader.py`
e `tela/teste_modelo.py`.

```yaml
QA-H0034-IMPL-ALTO-002:
  status: CORRIGIDO
  corrigido_em: secao_39_PATCH_IMPLEMENTACAO
```

Condições sem bloqueio (mantidas):

- todas as regras comportamentais derivam das autoridades ativas (H-0034,
  ADR-0023, contratos, nomenclatura);
- nenhuma decisão nova foi inventada;
- o quadro mínimo global reutiliza mecanismo canônico existente (ADR-0017);
- **o alinhamento horizontal agora segue o declarado pela instância** (corrigido
  por ALTO-001 — leitura de `_campos_inertes["layout"]["alinhamento"]`);
- o modelo isolado foi construído com semânticas existentes (`horizontal`,
  `fracao`, tipos `console`/`lancador`).

## 39. PATCH_IMPLEMENTACAO — sumário

```yaml
qa_reprovador: docs/relatorios/RELATORIO_QA_H-0034_IMPLEMENTACAO.md
data_patch: 2026-07-15
```

**QA-H0034-IMPL-ALTO-001 (CORRIGIDO):**

- Causa: `_linhas_lancador` não lia `elemento._campos_inertes["layout"]["alinhamento"]`;
  hardcodava excesso à direita, produzindo saída idêntica para os três alinhamentos.
- Correção em `tela/renderizador.py`:
  - Adicionada `_split_excesso_lancador(excesso, alinhamento)` (função de módulo).
  - `_linhas_lancador` lê e valida `alinhamento` logo após a verificação de
    `content_w is None`; valor inválido levanta `RenderizadorErro` (R-10).
  - Passo 3 da fila: substitui `partes_linha.append(" " * excesso)` por
    `exc_esq, exc_dir = _split_excesso_lancador(excesso, alinhamento)` com
    `exc_esq` antes da margem_esq e `exc_dir` após a margem_dir.
  - Passo 3 de `_tentar_matriz`: mesmo padrão aplicado à construção da `linha`.
  - Coluna mínima: `excesso_min = content_w - coluna_minima_content_w` distribuído
    conforme alinhamento; texto paddado a `max_texto_sub` para comprimento fixo.
- Cobertura adicionada em `tela/teste_renderizador.py`:
  - Helper `_h0034_modelo_alinhamento(itens, alinhamento, largura)`.
  - `test_alinhamento_horizontal_por_instancia` na classe
    `TestDistribuicaoResponsivaH0034` (adicionado a `run_all()`).
  - 24 verificações novas: posições literais para fila e matriz em
    esquerda/centro/direita; `None` idêntico a "esquerda"; valor inválido →
    `RenderizadorErro`; regressão demo ([d] na posição 4).
- Suíte pós-patch: `228 passed`, `1042/1042 verificações`, código 0.

**QA-H0034-IMPL-ALTO-002 (CORRIGIDO — continuação do PATCH_IMPLEMENTACAO):**

Autorização adicional recebida em 2026-07-15 para `tela/loader.py`,
`tela/modelo.py`, `tela/teste_loader.py`, `tela/teste_modelo.py`.

- Causa: 6 constantes `_LANC_*` hardcoded em `tela/renderizador.py` violavam
  R-6 (fonte única de verdade) e R-11 (parâmetros de tipo em `config/`).
  O renderer não pode fazer I/O nem importar `json`/`os`/`pathlib`.

- Solução: pipeline `loader → modelo → renderer` via `parametros_tipo` em
  `ElementoCorpo`. O loader, já autorizado a I/O, carrega e valida
  `config/elementos/lancador.json` quando há lancador na tela; propaga ao modelo;
  o renderer consome `elemento.parametros_tipo`.

- **`tela/loader.py`** — duas funções adicionadas antes de `_para_base`:
  - `_tem_lancador_em_elementos(elementos)`: varredura recursiva para decidir
    se a carga é necessária.
  - `_carregar_e_validar_config_lancador(base)`: lê e valida os 6 campos
    normativos; levanta `TelaArquivoNaoEncontrado`, `TelaJsonInvalido`,
    `TelaCampoObrigatorioAusente`, `TelaEstruturaInvalida` conforme o caso.
  - `carregar_tela` chama condicionalmente e retorna `_config_lancador` no dict.

- **`tela/modelo.py`** — `ElementoCorpo` recebe campo `parametros_tipo: dict | None`.
  `construir_modelo` extrai `tela_raw.get("_config_lancador")` e propaga
  para cada lancador (direto e recursivo dentro de grupos).

- **`tela/renderizador.py`** — bloco das 6 constantes `_LANC_*` removido;
  `_linhas_lancador` lê `params = elemento.parametros_tipo`, levanta
  `RenderizadorErro` se `None`, extrai os 6 valores locais e substitui todos
  os usos de `_LANC_*`. Margens verticais passam de literais `[""]` para
  `[""] * margem_v_sup` / `[""] * margem_v_inf` (retrocompatíveis, pois
  valores do JSON coincidem com as antigas constantes).

- **`tela/teste_loader.py`**:
  - Adicionado `_LANCADOR_JSON_VALIDO` e `_criar_config_lancador(tmp_base)`.
  - `main()` chama `_criar_config_lancador(tmp_base)` antes dos testes existentes
    (os que criam telas com lancador em tmp_base sem o arquivo falhavam).
  - `TestValidacaoMatrizH0028._com_tmp()` também chama `_criar_config_lancador`.
  - Nova função `teste_config_lancador_h0034(tmp_base)` com 24 verificações
    cobrindo os 12 pontos especificados.

- **`tela/teste_modelo.py`** — nova função `teste_parametros_tipo_h0034()` com
  13 verificações cobrindo os 10 pontos especificados.

- **`tela/teste_renderizador.py`**:
  - `_PARAMS_LANCADOR_DEMO` adicionado como constante de módulo.
  - `modelo_item_limite`, `_h0034_modelo_lancador`, `_h0034_modelo_isolado`,
    `_h0034_modelo_alinhamento` atualizados com `parametros_tipo=_PARAMS_LANCADOR_DEMO`.
  - Novo método `test_parametros_tipo_ausente_levanta_erro` na classe
    `TestDistribuicaoResponsivaH0034` (adicionado a `run_all()`): 2 verificações.
  - Comentário de `test_renderer_preserva_proibicoes_import` corrigido.

- **Contagens pós-patch (verificadas):**
  - `tela/teste_renderizador.py`: 1044/1044 (+2 sobre 1042)
  - `tela/teste_loader.py`: 273/273 (+24 sobre 249)
  - `tela/teste_modelo.py`: 161/161 (+13 sobre 148)
  - Smoke (`printf 's\n' | python -B demo/demo.py`): OK, matriz de 4×2 visível.

**QA-H0034-IMPL-MEDIO-001 (CORRIGIDO):**

Seções 14, 36 e 38 deste relatório corrigidas para refletir o achado do QA,
o patch executado e o bloqueio de ALTO-002.

---

## 40. PATCH_IMPLEMENTACAO — continuação ALTO-002 — inspeção final

```yaml
data: 2026-07-15
arquivos_alterados:
  - tela/renderizador.py   # remoção _LANC_*, reescrita _linhas_lancador
  - tela/loader.py         # _tem_lancador_em_elementos, _carregar_e_validar_config_lancador
  - tela/modelo.py         # ElementoCorpo.parametros_tipo, construir_modelo propagação
  - tela/teste_loader.py   # _criar_config_lancador, teste_config_lancador_h0034
  - tela/teste_modelo.py   # teste_parametros_tipo_h0034
  - tela/teste_renderizador.py  # _PARAMS_LANCADOR_DEMO, helpers, novo teste
  - docs/relatorios/IMP-0034-distribuicao-responsiva-lancador-fila-matriz.md
arquivos_inalterados:
  - config/elementos/lancador.json  # fonte canônica, sem modificação
  - docs/contratos/contrato_lancador.md
  - docs/adr/ADR-0023-*.md
```

---

## 41. Segundo PATCH_IMPLEMENTACAO — correção QA-H0034-POS-IMPL-ALTO-001 e QA-H0034-POS-IMPL-MEDIO-001

```yaml
qa_reprovador: docs/relatorios/RELATORIO_QA_POS_PATCH_H-0034_IMPLEMENTACAO.md
data_patch: 2026-07-15
arquivos_alterados:
  - tela/loader.py
  - tela/renderizador.py
  - tela/teste_loader.py
  - tela/teste_modelo.py
  - tela/teste_renderizador.py
  - docs/relatorios/IMP-0034-distribuicao-responsiva-lancador-fila-matriz.md
arquivos_inalterados:
  - tela/modelo.py          # nenhuma alteração necessária
  - config/elementos/lancador.json   # fonte canônica, sem modificação
```

**QA-H0034-POS-IMPL-ALTO-001 (CORRIGIDO):**

- Causa: `_TEXTO_ITEM_MAX = 15` estava hardcoded em `tela/renderizador.py`
  (linha 79 à época). `_carregar_e_validar_config_lancador` em `tela/loader.py`
  não carregava nem retornava `verificacao.texto.max_caracteres`; logo o campo
  nunca chegava a `parametros_tipo` e o renderer usava a constante interna.
  Teste com `max_caracteres=3` não mudava o comportamento porque o JSON não era
  a autoridade real.

- Correção em `tela/loader.py`:
  - `_carregar_e_validar_config_lancador` passou a carregar e validar
    `verificacao.texto.max_caracteres` (int não-booleano, > 0).
  - Validações: `verificacao` deve ser dict; `verificacao.texto` deve ser dict;
    `max_caracteres` deve existir, ser `int` não-bool, ser > 0.
  - Valor incluído na dict de retorno: `"verificacao": {"texto": {"max_caracteres": mc}}`.

- Correção em `tela/renderizador.py`:
  - `_TEXTO_ITEM_MAX = 15` removido.
  - `_itens_lancador_normalizados(elemento)` → `_itens_lancador_normalizados(elemento, max_caracteres)`.
  - `_linhas_lancador` reestruturado: (1) checagem de itens brutos sem validação
    de texto; (2) caminho legado sem validação de texto; (3) alinhamento;
    (4) verificação de `parametros_tipo`; (5) extração de `max_caracteres` via
    `params["verificacao"]["texto"]["max_caracteres"]`; (6) chamada a
    `_itens_lancador_normalizados(elemento, max_caracteres)`.
  - Docstring do módulo atualizado: referência a "15 caracteres" substituída
    por "max_caracteres (lido de config/elementos/lancador.json via pipeline)".

- Cobertura adicionada:
  - `tela/teste_loader.py`: 10 novos pontos em `_run_config_lancador_h0034`
    (Mc-1 a Mc-10): ausência de `verificacao`, `verificacao.texto`,
    `max_caracteres`; string/bool/zero/negativo como tipo inválido; campo extra
    ignorado; valor canônico 15; valor alternativo 3 propagado.
  - `tela/teste_modelo.py`: 2 novos pontos em `teste_parametros_tipo_h0034`:
    pipeline real `max_caracteres == 15`; valor alternativo 3 propagado.
  - `tela/teste_renderizador.py`: novo método `test_max_caracteres_configuravel`
    em `TestDistribuicaoResponsivaH0034` (adicionado a `run_all()`): 10 pontos
    incluindo `_TEXTO_ITEM_MAX` ausente, `mc=3` aceita/rejeita, `mc=15` aceita,
    `_PARAMS_LANCADOR_DEMO` correto.

**QA-H0034-POS-IMPL-MEDIO-001 (CORRIGIDO):**

- Causa: 7 funções em `tela/teste_loader.py` tinham parâmetro `tmp_base` mas
  não eram pytest fixtures. O pytest as coletava (prefixo `teste_`) e falhava
  com `fixture 'tmp_base' not found` (7 errors, exit code 1).

- Correção em `tela/teste_loader.py`:
  - As 7 funções renomeadas com prefixo `_run_` (saem da coleção pytest):
    `_run_erros`, `_run_tipos_validos`, `_run_grupo_estrutural`,
    `_run_arranjo_corpo_h0019`, `_run_distribuicao_corpo_h0025`,
    `_run_hierarquia_grupos_adr0019`, `_run_config_lancador_h0034`.
  - 7 wrappers pytest adicionados com `tmp_path` (fixture nativa do pytest):
    cada wrapper chama `_criar_config_lancador(tmp_path)` + `_run_*(tmp_path)`.
  - `main()` atualizado para chamar `_run_*` em vez de `teste_*`.
  - `_LANCADOR_JSON_VALIDO` atualizado com `verificacao.texto.max_caracteres: 15`.

- Contagens pós-patch (verificadas):
  - `tela/teste_loader.py` runner direto: 283/283 (+10 sobre 273)
  - `tela/teste_modelo.py` runner direto: 163/163 (+2 sobre 161)
  - `tela/teste_renderizador.py` runner direto: 1052/1052 (+10 sobre 1042 contados
    no patch anterior; inclui `test_max_caracteres_configuravel` com 10 pontos)
  - Suite pytest focal (3 arquivos): 260 passed, 5 warnings, 0 errors (antes: 252 passed, 7 errors)
  - Smoke `demo/teste_demo.py`: 358/358

---

## 42. Terceiro PATCH_IMPLEMENTACAO — correção QA-H0034-POS-SEGUNDO-IMPL-MEDIO-001

```yaml
qa_reprovador: docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0034_IMPLEMENTACAO.md
status_anterior: I2_IMPLEMENTATION_PATCH_REQUIRED
data_patch: 2026-07-15
arquivos_alterados:
  - tela/renderizador.py
  - tela/teste_renderizador.py
  - docs/relatorios/IMP-0034-distribuicao-responsiva-lancador-fila-matriz.md
arquivos_inalterados:
  - tela/loader.py
  - tela/modelo.py
  - tela/teste_loader.py
  - tela/teste_modelo.py
  - config/elementos/lancador.json
```

**QA-H0034-POS-SEGUNDO-IMPL-MEDIO-001 (CORRIGIDO):**

- Achado: `_linhas_lancador(elemento, content_w=None)` formava itens a partir de
  `_itens_brutos` antes de consultar `elemento.parametros_tipo` e antes de
  chamar `_itens_lancador_normalizados`. O caminho legado aceitava texto acima
  do limite configurável, ignorando `verificacao.texto.max_caracteres`.

- Causa técnica: a checagem de `content_w is None` ocorria imediatamente após a
  verificação de cardinalidade zero, antes da extração de `parametros_tipo` e da
  normalização. Assim, o caminho legado formatava `_itens_brutos` diretamente,
  contornando toda a validação de texto.

- Correção em `tela/renderizador.py` — reordenação da sequência em
  `_linhas_lancador`:
  1. Obter `_itens_brutos`; cardinalidade zero → `return []` (sem consultar parâmetros).
  2. Obter `params = elemento.parametros_tipo`; ausência → `RenderizadorErro`.
  3. Extrair `max_caracteres = params["verificacao"]["texto"]["max_caracteres"]`.
  4. Chamar `itens = _itens_lancador_normalizados(elemento, max_caracteres)`.
  5. **Somente então**: ramificar entre caminho legado (`content_w is None`) e
     caminho responsivo (`content_w` fornecido).
  6. Caminho legado consome `itens` (tuplas `(chip, texto)`) já normalizados,
     preservando formato `"[{chip}] {texto}"`.
  7. Caminho responsivo: alinhamento → demais parâmetros normativos (inalterado).

- Sequência final comum de normalização (aplicada a ambos os caminhos):
  `_itens_brutos` → cardinalidade zero → `parametros_tipo` → `max_caracteres`
  → `_itens_lancador_normalizados` → ramificação legado/responsivo.

- Parâmetros ausentes ou estrutura incompleta produzem o mesmo comportamento de
  erro já usado pela rota normal: `RenderizadorErro` para `params is None`;
  `KeyError` para estrutura incompleta. Sem fallback numérico, sem `.get(..., 15)`.

- Testes adicionados em `tela/teste_renderizador.py` — novo método
  `test_caminho_legado_valida_texto` na classe `TestDistribuicaoResponsivaH0034`
  (adicionado a `run_all()`), com 13 verificações:
  - cardinalidade zero retorna `[]` sem consultar `parametros_tipo`;
  - `parametros_tipo=None` levanta `RenderizadorErro` (+ mensagem menciona campo);
  - estrutura incompleta (`verificacao` ausente) levanta erro;
  - `mc=3`: texto de 3 chars aceito;
  - `mc=3`: texto de 4 chars rejeitado (`Quat`), mensagem menciona limite e texto;
  - `mc=3`: `"Quatro"` (6 chars) rejeitado, mensagem menciona texto;
  - `mc=15`: texto válido aceito; saída preserva formato `"[chip] texto"`;
  - equivalência: `content_w=None` e `content_w` válido rejeitam o mesmo texto
    acima do máximo com `RenderizadorErro`.

- Contagens pós-patch (verificadas):
  - `tela/teste_renderizador.py` runner direto: 1065/1065 (+13 sobre 1052)
  - `tela/teste_loader.py` runner direto: 283/283 (inalterado)
  - `tela/teste_modelo.py` runner direto: 163/163 (inalterado)
  - Suite pytest focal (3 arquivos): 261 passed, 5 warnings, 0 errors (era 260)
  - Código de saída pytest focal: 0

- Suíte canônica completa:
  ```yaml
  tela/teste_loader.py:       283/283  codigo 0
  tela/teste_modelo.py:       163/163  codigo 0
  tela/teste_renderizador.py: 1065/1065 codigo 0
  demo/teste_demo.py:         358/358  codigo 0
  demo/teste_diagnostico.py:   30/30   codigo 0
  demo/teste_explorar_barra_de_menus.py: 38/38 codigo 0
  total: 1937/1937  (era 1924/1924; diferenca: +13)
  ```

- Smoke (`printf 's\n' | python -B demo/demo.py`): código 0; `ORQUESTRADOR`
  presente; `NAVEGAR` presente; sete itens `[d] [g] [1] [2] [3] [4] [5]`
  presentes; sem `Traceback`.

- Ausência de hardcoding residual confirmada:
  - `_TEXTO_ITEM_MAX`: ausente (removido no segundo patch);
  - literal `15` como limite normativo: ausente no renderer;
  - fallback numérico de `max_caracteres`: ausente;
  - ramificação legado com validação própria: corrigida neste patch;
  - formatação de `_itens_brutos` contornando `_itens_lancador_normalizados`:
    corrigida neste patch.

- Narrativa das onze falhas anteriores do loader: o total histórico de falhas
  do loader foi registrado nas contagens de implementações e patches anteriores,
  mas a decomposição individual das onze falhas não estava preservada com
  granularidade suficiente nos artefatos disponíveis para enumeração literal.
  Não foi criada enumeração retrospectiva sem evidência.

- Regressões H-0034: nenhuma observada. Preservados: fila em 110, matriz em 109,
  matriz 4×2 em 80, alinhamento esquerda/centro/direita, coluna válida em área 21,
  quadro mínimo em área 20, T-ISOL-01/02/03, cardinalidades zero/um/dois, margens
  verticais, ausência de paginação/perda/duplicação/truncamento, parâmetros
  alternativos em memória, renderer sem I/O, proibições de importação.

- Validação humana em TTY real: não executada.

```text
VALIDACAO_MANUAL_PENDENTE_USUARIO
```

- Aprovação formal: ausente. Nenhum QA independente executado nesta etapa.

---

Este relatório **não aprova formalmente** a implementação. A aprovação formal
depende de QA independente e da validação humana em TTY real, ambas fora do
escopo desta etapa.
