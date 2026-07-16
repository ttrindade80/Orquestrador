# Relatorio de QA da implementacao H-0034

```yaml
etapa: QA_IMPLEMENTACAO
handoff: H-0034
artefato_implementacao: docs/relatorios/IMP-0034-distribuicao-responsiva-lancador-fila-matriz.md
relatorio: docs/relatorios/RELATORIO_QA_H-0034_IMPLEMENTACAO.md
data: 2026-07-15
auditoria: independente
status_literal: I2_IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: PATCH_REQUERIDO
validacao_manual_tty_real: NAO_EXECUTADA
```

## 1. Escopo desta auditoria

Esta auditoria verificou a implementacao do H-0034 contra o handoff aprovado,
a ADR-0023 aplicada, os contratos ativos, o diff real, os testes declarados, as
duas excecoes operacionais autorizadas e o estado Git.

Nenhum codigo, teste, snapshot, contrato, ADR, handoff ou relatorio de
implementacao foi corrigido. O unico arquivo criado por esta etapa e este
relatorio de QA.

## 2. Autoridades lidas

Foram lidos integralmente ou nas secoes diretamente aplicaveis:

- `docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md`
- `docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0034_HANDOFF.md`
- `docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0034_HANDOFF.md`
- `docs/adr/ADR-0023-largura-minima-funcional-lancador.md`
- `docs/adr/ADR-0017-redimensionamento-reativo-tui.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md`
- `docs/relatorios/RELATORIO_APLICACAO_ADR-0023.md`
- `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0023.md`
- `docs/contratos/contrato_lancador.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/NOMENCLATURA.md`
- `config/elementos/lancador.json`
- `config/telas/demo/demo.json`
- `tela/modelo.py`
- `tela/renderizador.py`
- `tela/teste_renderizador.py`
- `demo/demo.py`
- `demo/teste_demo.py`
- `demo/teste_diagnostico.py`

## 3. Estado Git inicial

Comandos executados no inicio, a partir da raiz do projeto:

```bash
git status --short
git diff --name-only
git diff --check
git diff --cached --name-only
```

`git status --short` inicial:

```text
 M demo/teste_demo.py
 M demo/teste_diagnostico.py
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_lancador.md
 M docs/contratos/contrato_tela_json.md
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

`git diff --name-only` listou os nove arquivos rastreados modificados acima.
`git diff --check` nao produziu saida. `git diff --cached --name-only` nao
produziu saida; o stage estava vazio.

## 4. Escopo real do diff

Diff de implementacao inspecionado:

```bash
git diff -- \
  tela/renderizador.py \
  tela/teste_renderizador.py \
  demo/teste_demo.py \
  demo/teste_diagnostico.py
```

Classificacao:

```yaml
arquivos_da_implementacao_h0034:
  - tela/renderizador.py
  - tela/teste_renderizador.py
  - docs/relatorios/IMP-0034-distribuicao-responsiva-lancador-fila-matriz.md

excecoes_operacionais_autorizadas:
  - demo/teste_demo.py
  - demo/teste_diagnostico.py

alteracoes_documentais_preexistentes_da_adr_0023:
  - docs/NOMENCLATURA.md
  - docs/adr/INDICE_ADR.md
  - docs/contratos/contrato_composicao_corpo.md
  - docs/contratos/contrato_lancador.md
  - docs/contratos/contrato_tela_json.md

caches:
  demo/__pycache__/:
    origem: NAO_CONFIRMADA
    produzido_pelo_executor: NAO_CONFIRMADO
    produzido_pelo_usuario: NAO_CONFIRMADO
  tela/__pycache__/:
    origem: NAO_CONFIRMADA
    produzido_pelo_executor: NAO_CONFIRMADO
    produzido_pelo_usuario: NAO_CONFIRMADO
```

Nao ha evidencia para atribuir os documentos preexistentes da ADR-0023 ao
executor da implementacao. O relatorio de implementacao novo e artefato
declarado da propria implementacao.

## 5. Achados

### QA-H0034-IMPL-ALTO-001: alinhamento por instancia nao e implementado

Status: confirmado.

Autoridades:

- `docs/contratos/contrato_lancador.md`, secoes 4.7, 6.4 e R-10: o alinhamento
  horizontal pertence a instancia declarada no `tela.json`.
- `docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md`, secao
  3.5: sobra a direita equivale ao alinhamento `"esquerda"` da instancia
  `demo`, nao a uma regra universal.
- `config/telas/demo/demo.json`: a instancia `lancador_principal` declara
  `layout.alinhamento = "esquerda"`.

Evidencia do codigo:

- `tela/modelo.py` preserva campos adicionais, incluindo `layout`, em
  `_campos_inertes`.
- `tela/renderizador.py` chama `_linhas_lancador(elemento, content_w)`, mas
  `_linhas_lancador` nao le `elemento._campos_inertes["layout"]`.
- Em `tela/renderizador.py`, a fila manda o excesso residual para a direita
  incondicionalmente; a matriz faz o mesmo. Os comentarios citam a demo como
  instancia esquerda, mas o valor declarado nao e consultado.

Prova independente executada:

```text
layout.alinhamento = "esquerda", "centro" e "direita" produziram saidas
identicas para o mesmo lancador sintetico.
```

Conclusao: a implementacao generaliza silenciosamente a politica da instancia
`demo` para qualquer `lancador`. Isso viola requisito material do H-0034 e do
contrato. Os testes adicionados nao cobrem instancias com alinhamento diferente
de `"esquerda"`.

### QA-H0034-IMPL-ALTO-002: parametros do tipo `lancador` estao hardcoded no renderer

Status: confirmado.

Autoridades:

- `docs/contratos/contrato_lancador.md`, R-6: nenhum parametro de layout do
  tipo `lancador` pode estar hardcoded no codigo.
- `docs/contratos/contrato_lancador.md`, R-11, e ADR-0023: parametros de
  `coluna_minima_content_w` vem de `config/elementos/lancador.json` sem
  hardcoding.
- `docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md`, secao
  3.2: o renderer deve ler os parametros de vao de
  `config/elementos/lancador.json`, sem hardcoding.

Evidencia do codigo:

```text
tela/renderizador.py:
  _LANC_VAO_CHIP_TEXTO_MIN = 1
  _LANC_VAO_CHIP_TEXTO_MAX = 3
  _LANC_VAO_ITENS_MIN = 2
  _LANC_VAO_ITENS_MAX = 5
  _LANC_MARGEM_VERTICAL_SUPERIOR = 1
  _LANC_MARGEM_VERTICAL_INFERIOR = 1
```

O proprio comentario da implementacao reconhece que as autoridades exigem
leitura de `config/elementos/lancador.json`, mas justifica o espelhamento por
uma proibicao local de o renderer importar `json`/`os`/`pathlib` ou abrir
arquivos. Essa tensao operacional nao foi resolvida pelo handoff nem por ADR
nova. A implementacao escolheu manter uma proibicao tecnica preexistente e
descumprir a autoridade ativa do `lancador`.

Conclusao: o comportamento atual passa nos testes porque os testes tambem
aceitam o espelhamento, mas nao cumpre R-6/R-11 nem o H-0034. Isto exige patch
de implementacao ou nova decisao documental antes de aprovacao.

### QA-H0034-IMPL-MEDIO-001: relatorio de implementacao afirma conformidade nao comprovada

Status: confirmado.

O relatorio de implementacao declara que:

```text
o alinhamento horizontal segue o declarado pela instancia
```

Essa afirmacao e contradita pelo achado `QA-H0034-IMPL-ALTO-001`: o renderer
nao le o alinhamento da instancia e produz a mesma saida para `"esquerda"`,
`"centro"` e `"direita"`. O relatorio tambem trata o hardcoding de parametros
como limitacao aceitavel, mas as autoridades aplicadas o proibem.

Conclusao: o relatorio de implementacao nao pode ser aceito como descricao
integralmente fiel do estado implementado.

## 6. Pontos conformes verificados

Apesar dos achados, foram confirmados os comportamentos centrais abaixo:

- Para a demo, `sum(item_w_min) = 91`, seis vaos minimos somam `12`, margens
  minimas somam `4`, `fila_content_w_min = 107` e
  `area_lancador_w_min = 110`.
- Em `area_lancador_w=110`, a demo fica em fila, com sete chips na mesma linha.
- Em `area_lancador_w=109`, a fila deixa de caber e a matriz valida e usada.
- Em `area_lancador_w=80`, a matriz esperada e 4x2, com colunas:
  `[Destino, Grupo Min.]`, `[Console, Dashboard]`,
  `[Matriz 2x2, Matriz 3x2]`, `[Matriz 2x4]`.
- As larguras independentes da demo em 80 sao `[14, 13, 14, 14]`.
- A ordem declarativa e preservada por preenchimento coluna-a-coluna.
- Nao foi observada paginacao, perda, duplicacao ou truncamento de itens nas
  larguras validas testadas.
- `max_chip_sub = 3`, `max_texto_sub = 10`,
  `coluna_minima_content_w = 18`, `lancador_caixa_min_w = 21`.
- `area_lancador_w=21` produz coluna valida; `area_lancador_w=20` aciona o
  quadro minimo global.
- O quadro minimo reutiliza o mecanismo global `_quadro_minimo_global` e
  substitui a tela normal quando o sinal `_quadro_minimo_lancador_ativo` fica
  ativo.
- O sinal global e redefinido no inicio de `renderizar_tela`, e a recuperacao
  21 -> 20 -> 21 foi comprovada por teste automatizado.
- As margens verticais de uma linha acima e uma abaixo dos itens foram
  incorporadas nos modos validos.

## 7. Excecoes operacionais autorizadas

### `demo/teste_demo.py`

O diff permaneceu dentro da excecao autorizada:

- snapshots `_EXPECTED_*` foram atualizados para o novo layout do `lancador`;
- comentarios associados foram atualizados;
- o ajuste focal de altura/contagem mudou o cenario de 20 para 19 linhas,
  coerente com `n_minimo=19` e `L_corpo_conteudo=13`;
- nao houve alteracao de logica de producao, configuracao, contratos, ADRs ou
  handoff.

Nao foi identificado relaxamento indevido de assert ou remocao material de
cobertura fora da autorizacao.

### `demo/teste_diagnostico.py`

O diff permaneceu dentro da excecao autorizada:

- somente o snapshot `_EXPECTED_ORQUESTRADOR` foi atualizado para refletir a
  matriz do `lancador`;
- nao houve alteracao de logica do teste, entrada, comando, fixture ou
  identidade da tela.

## 8. Testes executados

Executados com `python -B` quando aplicavel para evitar escrita de bytecode.

```yaml
pytest_focal:
  comando: python -B -m pytest tela/teste_renderizador.py -q --tb=short -o cacheprovider_disabled=true
  resultado: 227 passed
  observacao: a opcao cacheprovider_disabled nao foi reconhecida por esta versao do pytest; nao surgiu .pytest_cache no estado Git

suite_canonica_direta:
  tela/teste_loader.py: 249/249, codigo 0
  tela/teste_modelo.py: 148/148, codigo 0
  tela/teste_renderizador.py: 1018/1018, codigo 0
  demo/teste_demo.py: 358/358, codigo 0
  demo/teste_diagnostico.py: 30/30, codigo 0
  demo/teste_explorar_barra_de_menus.py: 38/38, codigo 0
  total: 1838/1838
  codigos_saida: 6/6

smoke_demo:
  comando: printf 's\n' | python -B demo/demo.py
  codigo_saida: 0
  conteudo_confirmado:
    - ORQUESTRADOR
    - NAVEGAR
    - "[d] Destino"
    - "[g] Grupo Min."
    - "[1] Console"
    - "[2] Dashboard"
    - "[3] Matriz 2x2"
    - "[4] Matriz 3x2"
    - "[5] Matriz 2x4"
```

A aprovacao das suites nao elimina os achados materiais, porque as suites nao
cobrem alinhamento por instancia diferente de `"esquerda"` e aceitam o
espelhamento hardcoded dos parametros do `lancador`.

## 9. Validacao humana

Validacao humana em TTY real nao foi executada, conforme restricao desta etapa.

Estado correto:

```text
VALIDACAO_MANUAL_PENDENTE_USUARIO
```

Contudo, a validacao humana nao e o unico residuo: existem defeitos tecnicos
materiais antes da aprovacao da implementacao.

## 10. Conclusao

```yaml
resultado: REPROVADO_COM_PATCH_REQUERIDO
status_literal: I2_IMPLEMENTATION_PATCH_REQUIRED
motivos:
  - alinhamento por instancia nao implementado
  - parametros do tipo lancador hardcoded apesar de autoridade ativa exigir leitura de config/elementos/lancador.json
  - relatorio de implementacao contem afirmacoes de conformidade contraditas pelo codigo
nao_bloqueia_por_si_so:
  - excecoes operacionais em demo/teste_demo.py e demo/teste_diagnostico.py
  - validacao humana pendente
stage_git: vazio no inicio da auditoria
```

A implementacao nao deve ser aprovada no estado atual.

## 11. Estado Git final

Comandos executados ao final, a partir da raiz do projeto:

```bash
git status --short
git diff --name-only
git diff --check
git diff --cached --name-only
```

`git status --short` final:

```text
 M demo/teste_demo.py
 M demo/teste_diagnostico.py
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_lancador.md
 M docs/contratos/contrato_tela_json.md
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
?? docs/relatorios/RELATORIO_QA_H-0034_IMPLEMENTACAO.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0034_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0034_HANDOFF.md
?? tela/__pycache__/
```

`git diff --name-only` final listou somente os nove arquivos rastreados ja
identificados no inicio:

```text
demo/teste_demo.py
demo/teste_diagnostico.py
docs/NOMENCLATURA.md
docs/adr/INDICE_ADR.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_tela_json.md
tela/renderizador.py
tela/teste_renderizador.py
```

`git diff --check` nao produziu saida. `git diff --cached --name-only` nao
produziu saida; o stage permaneceu vazio.
