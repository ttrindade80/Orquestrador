# Relatorio de QA pos-patch da implementacao H-0034

```yaml
etapa: QA_IMPLEMENTACAO_POS_PATCH
handoff: H-0034
artefato_implementacao: docs/relatorios/IMP-0034-distribuicao-responsiva-lancador-fila-matriz.md
relatorio_qa_anterior: docs/relatorios/RELATORIO_QA_H-0034_IMPLEMENTACAO.md
relatorio: docs/relatorios/RELATORIO_QA_POS_PATCH_H-0034_IMPLEMENTACAO.md
data: 2026-07-15
auditoria: independente
status_literal: I2_IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: PATCH_REQUERIDO
validacao_manual_tty_real: NAO_EXECUTADA
```

## 1. Identificacao

Auditoria independente pos-patch da implementacao H-0034. Foram reavaliados os
tres achados anteriores, a autorizacao adicional para `loader`/`modelo`, o
fluxo completo de configuracao, o diff real, as suites, o IMP atualizado e a
preservacao dos comportamentos ja aprovados.

Nenhum codigo, teste, contrato, ADR, nomenclatura, handoff ou relatorio anterior
foi corrigido. O unico arquivo criado por esta etapa foi este relatorio.

## 2. QA anterior

Relatorio lido integralmente:

```yaml
arquivo: docs/relatorios/RELATORIO_QA_H-0034_IMPLEMENTACAO.md
status_anterior: I2_IMPLEMENTATION_PATCH_REQUIRED
achados_reauditados:
  - QA-H0034-IMPL-ALTO-001
  - QA-H0034-IMPL-ALTO-002
  - QA-H0034-IMPL-MEDIO-001
```

## 3. Autorizacao adicional

Foi tratada como autorizacao focal valida a alteracao em:

```yaml
arquivos_autorizados_adicionalmente:
  - tela/loader.py
  - tela/modelo.py
  - tela/teste_loader.py
  - tela/teste_modelo.py
finalidade_exclusiva: "config/elementos/lancador.json -> loader -> modelo -> ElementoCorpo.parametros_tipo -> renderer"
classificacao: NAO_DESVIO_DE_HANDOFF_QUANDO_LIMITADO_A_ESSE_FLUXO
```

As alteracoes nesses quatro arquivos permaneceram concentradas em carregar,
validar parcialmente, transportar e testar parametros do tipo `lancador`.

## 4. Artefatos auditados

Lidos integralmente ou nas secoes aplicaveis:

- `docs/relatorios/RELATORIO_QA_H-0034_IMPLEMENTACAO.md`
- `docs/relatorios/IMP-0034-distribuicao-responsiva-lancador-fila-matriz.md`
- `docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md`
- `docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0034_HANDOFF.md`
- `docs/adr/ADR-0023-largura-minima-funcional-lancador.md`
- `config/elementos/lancador.json`
- `tela/loader.py`
- `tela/modelo.py`
- `tela/renderizador.py`
- `tela/teste_loader.py`
- `tela/teste_modelo.py`
- `tela/teste_renderizador.py`
- `demo/teste_demo.py`
- `demo/teste_diagnostico.py`
- `docs/contratos/contrato_lancador.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/NOMENCLATURA.md`
- demais scripts da suite canonica citados neste relatorio.

## 5. Estado Git inicial

Comandos executados no inicio:

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
 M tela/loader.py
 M tela/modelo.py
 M tela/renderizador.py
 M tela/teste_loader.py
 M tela/teste_modelo.py
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

`git diff --name-only` inicial listou os 13 arquivos rastreados acima.
`git diff --check` nao produziu saida. `git diff --cached --name-only` nao
produziu saida; o stage estava vazio.

## 6. Escopo real do diff

Inspecionado:

```bash
git diff -- \
  tela/loader.py \
  tela/modelo.py \
  tela/renderizador.py \
  tela/teste_loader.py \
  tela/teste_modelo.py \
  tela/teste_renderizador.py \
  demo/teste_demo.py \
  demo/teste_diagnostico.py
```

Classificacao:

```yaml
patch_informou_alterar:
  - tela/loader.py
  - tela/modelo.py
  - tela/renderizador.py
  - tela/teste_loader.py
  - tela/teste_modelo.py
  - tela/teste_renderizador.py
  - docs/relatorios/IMP-0034-distribuicao-responsiva-lancador-fila-matriz.md

preservados_sem_diff_rastreado:
  - config/elementos/lancador.json
  - demo/demo.py
  - docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
  - relatorios_de_QA_anteriores

diffs_rastreados_preexistentes_ou_fora_do_patch_pos_qa:
  - demo/teste_demo.py
  - demo/teste_diagnostico.py
  - docs/NOMENCLATURA.md
  - docs/adr/INDICE_ADR.md
  - docs/contratos/contrato_composicao_corpo.md
  - docs/contratos/contrato_lancador.md
  - docs/contratos/contrato_tela_json.md
```

As modificacoes em `demo/teste_demo.py` e `demo/teste_diagnostico.py` continuam
compatíveis com as excecoes autorizadas da primeira implementacao. Os contratos,
nomenclatura e indice ADR ja apareciam modificados no QA anterior; esta auditoria
nao os atribui ao patch pos-QA, mas registra que o worktree permanece com esses
diffs rastreados.

## 7. Proveniencia

```yaml
itens_nao_rastreados_iniciais:
  demo/__pycache__/:
    origem: NAO_CONFIRMADA
    produzido_pelo_executor: NAO_CONFIRMADO
    produzido_pelo_usuario: NAO_CONFIRMADO
  tela/__pycache__/:
    origem: NAO_CONFIRMADA
    produzido_pelo_executor: NAO_CONFIRMADO
    produzido_pelo_usuario: NAO_CONFIRMADO
  docs/adr/ADR-0023-largura-minima-funcional-lancador.md:
    origem: NAO_CONFIRMADA
    produzido_pelo_executor: NAO_CONFIRMADO
    produzido_pelo_usuario: NAO_CONFIRMADO
  docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md:
    origem: NAO_CONFIRMADA
    produzido_pelo_executor: NAO_CONFIRMADO
    produzido_pelo_usuario: NAO_CONFIRMADO
  docs/relatorios/IMP-0034-distribuicao-responsiva-lancador-fila-matriz.md:
    origem: IMPLEMENTACAO_H0034
    produzido_pelo_executor: CONFIRMADO
    produzido_pelo_usuario: NAO_CONFIRMADO
  docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md:
    origem: NAO_CONFIRMADA
    produzido_pelo_executor: NAO_CONFIRMADO
    produzido_pelo_usuario: NAO_CONFIRMADO
  docs/relatorios/RELATORIO_APLICACAO_ADR-0023.md:
    origem: NAO_CONFIRMADA
    produzido_pelo_executor: NAO_CONFIRMADO
    produzido_pelo_usuario: NAO_CONFIRMADO
  docs/relatorios/RELATORIO_QA_ADR-0023.md:
    origem: NAO_CONFIRMADA
    produzido_pelo_executor: NAO_CONFIRMADO
    produzido_pelo_usuario: NAO_CONFIRMADO
  docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0023.md:
    origem: NAO_CONFIRMADA
    produzido_pelo_executor: NAO_CONFIRMADO
    produzido_pelo_usuario: NAO_CONFIRMADO
  docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md:
    origem: NAO_CONFIRMADA
    produzido_pelo_executor: NAO_CONFIRMADO
    produzido_pelo_usuario: NAO_CONFIRMADO
  docs/relatorios/RELATORIO_QA_H-0034_IMPLEMENTACAO.md:
    origem: QA_IMPLEMENTACAO_ANTERIOR
    produzido_pelo_executor: NAO_CONFIRMADO
    produzido_pelo_usuario: NAO_CONFIRMADO
  docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md:
    origem: NAO_CONFIRMADA
    produzido_pelo_executor: NAO_CONFIRMADO
    produzido_pelo_usuario: NAO_CONFIRMADO
  docs/relatorios/RELATORIO_QA_POS_PATCH_H-0034_HANDOFF.md:
    origem: NAO_CONFIRMADA
    produzido_pelo_executor: NAO_CONFIRMADO
    produzido_pelo_usuario: NAO_CONFIRMADO
  docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0034_HANDOFF.md:
    origem: QA_HANDOFF_POS_SEGUNDO_PATCH
    produzido_pelo_executor: NAO_CONFIRMADO
    produzido_pelo_usuario: NAO_CONFIRMADO
```

Caches observados nao foram removidos. Scripts foram executados com `python -B`
e `PYTHONDONTWRITEBYTECODE=1` quando aplicavel.

## 8. Resultado individual dos achados anteriores

```yaml
achado: QA-H0034-IMPL-ALTO-001
estado: CORRIGIDO
evidencia: >
  tela/renderizador.py agora le elemento._campos_inertes["layout"]["alinhamento"]
  por caminho seguro, valida esquerda/centro/direita e distribui o excesso via
  _split_excesso_lancador em fila, matriz e coluna unica.
testes: >
  tela/teste_renderizador.py confirmou fila e matriz nos tres alinhamentos,
  posicoes literais [A] em 7/9/10, default None identico a esquerda,
  valor invalido com RenderizadorErro e regressao da demo.
residuos: nenhum residuo tecnico identificado neste achado.
regressoes: nenhuma regressao observada nas suites e no smoke.
conclusao: CORRIGIDO
```

```yaml
achado: QA-H0034-IMPL-ALTO-002
estado: PARCIALMENTE_CORRIGIDO
evidencia: >
  O fluxo para os seis parametros de layout antes hardcoded foi implementado:
  config/elementos/lancador.json -> tela/loader.py -> _config_lancador ->
  tela/modelo.py -> ElementoCorpo.parametros_tipo -> tela/renderizador.py.
  Entretanto, a autoridade real e unica do JSON nao foi completada para todos
  os campos normativos efetivamente usados. O renderer ainda hardcoda
  _TEXTO_ITEM_MAX = 15 enquanto config/elementos/lancador.json declara
  verificacao.texto.max_caracteres = 15.
testes: >
  Scripts diretos passaram; prova independente em /tmp alterou
  verificacao.texto.max_caracteres para 3 e o pipeline ainda renderizou texto
  com 6 caracteres, demonstrando que esse campo do JSON nao e autoridade real.
residuos: >
  Validacao do loader cobre apenas subset de layout.vaos e layout.vertical;
  nao propaga verificacao.texto.max_caracteres nem valida esse campo.
regressoes: >
  Nao houve regressao observada para os seis parametros de layout; ha defeito
  remanescente de configurabilidade/hardcoding normativo.
conclusao: PARCIALMENTE_CORRIGIDO
```

```yaml
achado: QA-H0034-IMPL-MEDIO-001
estado: PARCIALMENTE_CORRIGIDO
evidencia: >
  O IMP registra o patch de alinhamento, a autorizacao adicional, o fluxo
  loader -> modelo -> renderer, contagens e smoke. Porem mantem contradicoes:
  no cabecalho e nas secoes 36/38 ainda classifica ALTO-002 como bloqueado por
  falta de autorizacao, enquanto a secao 39 declara ALTO-002 corrigido; a
  secao 912-915 tambem diz que secoes 36 e 38 foram corrigidas, mas elas
  continuam com texto antigo.
testes: leitura direta do IMP atualizado.
residuos: afirmacoes antigas contraditorias permanecem no relatorio IMP.
regressoes: nao aplicavel a runtime.
conclusao: PARCIALMENTE_CORRIGIDO
```

## 9. Fluxo de configuracao

Confirmado para os seis parametros de layout:

```yaml
parametros_de_tipo:
  origem: config/elementos/lancador.json
  loader: tela/loader.py::_carregar_e_validar_config_lancador
  chave_interna: _config_lancador
  modelo: tela/modelo.py::ElementoCorpo.parametros_tipo
  renderer: elemento.parametros_tipo

campos_de_instancia:
  origem: config/telas/<id>.json
  destino: ElementoCorpo._campos_inertes
  exemplo_preservado: layout.alinhamento
```

Provas independentes:

```yaml
leituras_por_operacao:
  demo_json: 1
  lancador_json: 1
tela_sem_lancador:
  _config_lancador: null
tipo_semelhante_lancador_fake:
  resultado: TelaTipoDesconhecido
layout_instancia:
  preservado_em: _campos_inertes
chave_interna:
  vaza_em_raw_da_tela: false
```

## 10. Validacao do loader

Conforme:

- caminho resolvido por `base / config/elementos/lancador.json`, independente de
  CWD;
- usa `Path.read_text`/`json.loads`, fronteira de I/O do loader;
- nao altera o arquivo real;
- carrega apenas quando ha `tipo == "lancador"` direto ou recursivo em `grupo`;
- uma leitura do `lancador.json` por operacao observada;
- assinatura publica de `carregar_tela` preservada;
- chave interna `_config_lancador` nao e campo declarativo da tela.

Parcial:

- valida obrigatoriedade/tipo/bool/negativo/minimo-maior-que-maximo para
  `layout.vaos.chip_texto`, `layout.vaos.entre_itens_colunas_margem` e
  `layout.vertical.margem_borda_superior/inferior`;
- nao valida nem propaga `verificacao.texto.max_caracteres`, embora o renderer
  use esse limite;
- nao valida o restante de `layout.distribuicao_de_sobra`, `layout.alinhamento`,
  `layout.colunas`, `layout.matriz`, `layout.vertical.entre_elementos` e
  `navegacao`, exceto quando essas regras aparecem hardcoded ou estruturais no
  renderer;
- campos desconhecidos nao foram rejeitados.

## 11. Propagacao pelo modelo

Confirmado:

- `ElementoCorpo` possui `parametros_tipo`;
- `_campos_inertes` continua reservado aos campos da instancia;
- `layout.alinhamento` permanece em `_campos_inertes`;
- parametros sao propagados para `lancador` direto e recursivo;
- `console` e `dashboard` nao recebem parametros indevidos;
- `_config_lancador` nao entra como campo normal da tela;
- APIs publicas antigas continuam utilizaveis;
- testes em memoria conseguem fornecer parametros alternativos;
- o desenho atual compartilha o mesmo dict entre `_config_lancador` e
  `parametros_tipo`, intencionalmente registrado pelos testes.

## 12. Consumo no renderer

Confirmado:

- `tela/renderizador.py` nao importa `json`, `os` ou `pathlib`;
- nao abre arquivos nem resolve caminhos;
- consome `elemento.parametros_tipo` para os seis parametros de layout;
- rejeita `parametros_tipo is None` com `RenderizadorErro`;
- nao manteve fallback numerico silencioso para os seis parametros `_LANC_*`.

Nao conforme:

- `_TEXTO_ITEM_MAX = 15` permanece em `tela/renderizador.py:79` e e usado em
  `tela/renderizador.py:353-357`;
- esse valor duplica `config/elementos/lancador.json:10-13`;
- parametros em memoria alternativos nao conseguem alterar o limite de texto.

## 13. Busca completa de hardcoding

```yaml
- nome_ou_literal: _TEXTO_ITEM_MAX = 15
  uso: limite de caracteres de item do lancador
  autoridade: config/elementos/lancador.json.verificacao.texto.max_caracteres
  configuravel: true
  duplicacao_normativa: true
  conclusao: NAO_CONFORME

- nome_ou_literal: len(chip) + 2
  uso: largura da subcoluna do chip com colchetes
  autoridade: sintaxe visual do chip "[x]"
  configuravel: false
  duplicacao_normativa: false
  conclusao: constante estrutural aceitavel

- nome_ou_literal: content_w = total_w - 3 / inner_w = total_w - 2 / label_max = total_w - 4
  uso: estrutura da caixa com bordas e padding
  autoridade: primitiva local de caixa
  configuravel: false
  duplicacao_normativa: false
  conclusao: constante estrutural preexistente

- nome_ou_literal: "esquerda", "centro", "direita"
  uso: enumeracao de alinhamento de instancia
  autoridade: contrato_lancador.md R-10
  configuravel: false
  duplicacao_normativa: false
  conclusao: enumeracao normativa aceitavel

- nome_ou_literal: range(2, n + 1)
  uso: tentativa de matrizes validas por numero de linhas
  autoridade: algoritmo H-0034/ADR-0023
  configuravel: false
  duplicacao_normativa: false
  conclusao: controle estrutural do algoritmo

- nome_ou_literal: 0/1 em loops, indices e maiores restos
  uso: controle de listas, pisos e indices
  autoridade: algoritmo generico
  configuravel: false
  duplicacao_normativa: false
  conclusao: estrutural
```

Os seis parametros originalmente hardcoded em `_LANC_*` foram removidos como
constantes do renderer e passaram a vir de `parametros_tipo`.

## 14. Alinhamento por instancia

Confirmado:

- origem em `elemento._campos_inertes`;
- caminho seguro para `layout.alinhamento`;
- esquerda, centro, direita, ausencia e valor invalido cobertos;
- comportamento em fila e matriz coberto com posicoes literais;
- coluna unica usa `_split_excesso_lancador` no excesso minimo;
- demo preserva esquerda declarada;
- `_split_excesso_lancador` divide impar de centro com maior resto a esquerda;
- a sobra residual muda posicao sem alterar vãos internos, margens expandidas
  ou escolha do modo.

Provas literais registradas nos testes:

```yaml
fila:
  esquerda: "[A] pos 7"
  centro: "[A] pos 9"
  direita: "[A] pos 10"
matriz:
  esquerda: "[A] pos 7"
  centro: "[A] pos 9"
  direita: "[A] pos 10"
```

## 15. Parametros alternativos em memoria

Prova independente:

```yaml
params_base:
  chip_texto.minimo: 1
  entre_itens_colunas_margem.minimo: 2
  entre_itens_colunas_margem.maximo: 5
  margens_verticais: [1, 1]
params_alt:
  chip_texto.minimo: 2
  entre_itens_colunas_margem.minimo: 3
  entre_itens_colunas_margem.maximo: 6
  margens_verticais: [2, 2]
resultado:
  saida_mudou: true
  linha_base: "│      [A] Uno     [B] Dos        │"
  linha_alt:  "│       [A]  Uno      [B]  Dos    │"
  linhas_base: 10
  linhas_alt: 12
```

Os testes provam configurabilidade real para vãos, margens, largura minima e
fronteiras de fila/matriz/quadro minimo. Nao provam configurabilidade de
`verificacao.texto.max_caracteres`, que permanece hardcoded.

## 16. Regressões H-0034

Confirmado por suites e inspecao:

- demo 110: fila;
- demo 109: matriz;
- demo 80: matriz 4x2;
- larguras independentes `[14, 13, 14, 14]`;
- T-07;
- area 21: coluna completa;
- area 20: quadro minimo global;
- cenario isolado com `terminal_w = 80`;
- T-ISOL-01, T-ISOL-02 e T-ISOL-03;
- cardinalidades zero, um e dois;
- ausencia de paginacao, perda, duplicacao e truncamento;
- margens verticais;
- sinal global redefinido no inicio de cada renderizacao;
- sequencia 21 -> 20 -> 21 sem vazamento;
- mais de um `lancador` e ordem de validos/invalidos cobertos pelo mecanismo
  global quando suportado pelos modelos de teste.

## 17. Analise dos testes

### Loader

Cobertura nova real:

- JSON real e valores esperados;
- base temporaria;
- independencia de CWD por desenho;
- arquivo ausente;
- JSON invalido;
- campos ausentes de parte do layout;
- tipo invalido/bool;
- relacao minimo/maximo;
- tela sem `lancador`;
- assinatura publica preservada.

Limites:

- no modo `pytest`, funcoes com parametro `tmp_base` sao coletadas como testes e
  falham por fixture inexistente;
- validacao nao cobre todos os campos normativos do JSON;
- a correcao de falhas preexistentes nos temporarios decorre de criar
  `config/elementos/lancador.json` em `tmp_base`, nao de relaxar asserts.

### Modelo

Cobertura adequada para:

- campo `parametros_tipo`;
- separacao de `_campos_inertes`;
- alinhamento preservado;
- propagacao direta e recursiva;
- ausencia em outros tipos;
- valores reais e alternativos em memoria;
- identidade/compartilhamento do objeto conforme desenho;
- APIs publicas preservadas.

### Renderer

Cobertura adequada para:

- ausencia de I/O/importacoes proibidas;
- seis parametros de layout reais;
- parametros alternativos em memoria;
- alinhamento por instancia;
- fila e matriz nos tres alinhamentos;
- valor invalido;
- default autorizado;
- regressões 80/109/110, 20/21, T-ISOL;
- margens verticais, coluna minima e distribuicao de excesso.

Limite:

- teste de hardcoding nao cobre `verificacao.texto.max_caracteres`;
- `_PARAMS_LANCADOR_DEMO` em teste espelha apenas o subset de layout.

## 18. Suite focal

Comando solicitado:

```bash
PYTHONDONTWRITEBYTECODE=1 python -B -m pytest \
  tela/teste_loader.py \
  tela/teste_modelo.py \
  tela/teste_renderizador.py \
  -q --tb=short -p no:cacheprovider
```

Resultado:

```yaml
codigo_saida: 1
resultado: "252 passed, 7 errors, 5 warnings"
erros:
  causa: "fixture 'tmp_base' not found"
  locais:
    - tela/teste_loader.py::teste_erros
    - tela/teste_loader.py::teste_tipos_validos
    - tela/teste_loader.py::teste_grupo_estrutural
    - tela/teste_loader.py::teste_arranjo_corpo_h0019
    - tela/teste_loader.py::teste_distribuicao_corpo_h0025
    - tela/teste_loader.py::teste_hierarquia_grupos_adr0019
    - tela/teste_loader.py::teste_config_lancador_h0034
warnings: 5 PytestReturnNotNoneWarning
```

Execucoes diretas solicitadas:

```yaml
tela/teste_loader.py:
  verificacoes: 273/273
  codigo_saida: 0
tela/teste_modelo.py:
  verificacoes: 161/161
  codigo_saida: 0
tela/teste_renderizador.py:
  verificacoes: 1044/1044
  codigo_saida: 0
```

## 19. Suite canonica

Executada individualmente:

```yaml
tela/teste_loader.py:
  verificacoes: 273/273
  codigo_saida: 0
tela/teste_modelo.py:
  verificacoes: 161/161
  codigo_saida: 0
tela/teste_renderizador.py:
  verificacoes: 1044/1044
  codigo_saida: 0
demo/teste_demo.py:
  verificacoes: 358/358
  codigo_saida: 0
demo/teste_diagnostico.py:
  verificacoes: 30/30
  codigo_saida: 0
demo/teste_explorar_barra_de_menus.py:
  verificacoes: 38/38
  codigo_saida: 0
total_real: 1904/1904
codigos_saida_zero: 6/6
```

## 20. Smoke

Comando:

```bash
printf 's\n' | python -B demo/demo.py
```

Resultado:

```yaml
codigo_saida: 0
ORQUESTRADOR: presente
NAVEGAR: presente
sete_itens:
  - "[d] Destino"
  - "[g] Grupo Min."
  - "[1] Console"
  - "[2] Dashboard"
  - "[3] Matriz 2x2"
  - "[4] Matriz 3x2"
  - "[5] Matriz 2x4"
Traceback: ausente
```

## 21. Fidelidade do IMP

Conforme:

- registra QA reprovador;
- registra os tres achados;
- registra patch de alinhamento;
- registra bloqueio inicial de arquivo adicional;
- registra autorizacao adicional;
- registra arquivos autorizados;
- descreve fluxo loader -> modelo -> renderer;
- registra contagens finais 273/161/1044 e smoke;
- registra excecoes anteriores;
- nao autoaprova formalmente.

Nao conforme:

- cabecalho ainda lista `QA-H0034-IMPL-ALTO-002` como bloqueado;
- secoes 36 e 38 mantem texto antigo de bloqueio por falta de autorizacao;
- secao 39 declara `QA-H0034-IMPL-ALTO-002` corrigido;
- secao 912-915 afirma que secoes 36 e 38 foram corrigidas, mas elas ainda
  preservam a contradicao;
- as contagens antigas de pytest no IMP (`228 passed`, `1042/1042`) nao refletem
  a suite focal ampliada solicitada neste QA.

## 22. Validacao humana pendente

Nao foi executada validacao humana em TTY real, conforme restricao do prompt.
Mesmo sem os defeitos tecnicos acima, o status nao poderia ser
`I1_IMPLEMENTATION_APPROVED`; a categoria correta nesse caso seria
`I5_MANUAL_VALIDATION_REQUIRED`.

Como ha defeitos tecnicos remanescentes, o status desta auditoria e
`I2_IMPLEMENTATION_PATCH_REQUIRED`.

## 23. Novos achados

### QA-H0034-POS-IMPL-ALTO-001

```yaml
ID: QA-H0034-POS-IMPL-ALTO-001
severidade: alto
evidencia: >
  config/elementos/lancador.json declara verificacao.texto.max_caracteres = 15,
  mas tela/renderizador.py mantem _TEXTO_ITEM_MAX = 15 e usa esse valor
  diretamente. Prova independente com config temporaria max_caracteres = 3
  ainda renderizou texto "Quatro" (6 caracteres).
regra_violada: >
  Nenhum parametro configuravel de config/elementos/lancador.json pode continuar
  duplicado no renderer; JSON deve ser autoridade real e unica.
impacto: >
  Alterar o arquivo canonico nao altera o limite efetivo de texto; o renderer
  aceita/rejeita por constante propria, mantendo hardcoding normativo.
correcao_necessaria: >
  Validar e propagar verificacao.texto.max_caracteres pelo mesmo fluxo
  config -> loader -> modelo -> parametros_tipo -> renderer, removendo
  _TEXTO_ITEM_MAX hardcoded ou classificando documentalmente o campo como nao
  configuravel, se essa for a decisao autorizada.
arquivo_e_trecho:
  - config/elementos/lancador.json:10
  - tela/renderizador.py:79
  - tela/renderizador.py:340
```

### QA-H0034-POS-IMPL-MEDIO-001

```yaml
ID: QA-H0034-POS-IMPL-MEDIO-001
severidade: medio
evidencia: >
  A suite focal ampliada via pytest falha com 7 erros por fixture tmp_base
  inexistente, embora os scripts diretos passem.
regra_violada: >
  O prompt exige execucao e registro da suite focal ampliada; a suite nao deve
  falhar por incompatibilidade de harness quando coletada pelo pytest.
impacto: >
  A validacao independente por pytest nao confirma o patch; exige execucao por
  mecanismo alternativo para obter as contagens.
correcao_necessaria: >
  Tornar os testes de loader compativeis com pytest (fixture adequada ou nao
  coleta das funcoes diagnosticas com parametro interno), preservando os scripts
  diretos.
arquivo_e_trecho:
  - tela/teste_loader.py:406
  - tela/teste_loader.py:2064
```

## 24. Status literal e normalizado

```yaml
status_literal: I2_IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: PATCH_REQUERIDO
motivos:
  - QA-H0034-IMPL-ALTO-002 parcialmente corrigido, com hardcoding remanescente de texto.max_caracteres
  - QA-H0034-IMPL-MEDIO-001 parcialmente corrigido, com IMP contraditorio
  - QA-H0034-POS-IMPL-MEDIO-001: suite focal pytest falha
validacao_manual: pendente, mas nao e o unico residuo
```

## 25. Proxima categoria

```yaml
proxima_categoria: IMPLEMENTAR
objetivo: patch de implementacao e relatorio IMP para corrigir achados remanescentes
nao_gerar_prompt: true
```

## 26. Estado Git final

Comandos executados apos a criacao deste relatorio:

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
 M tela/loader.py
 M tela/modelo.py
 M tela/renderizador.py
 M tela/teste_loader.py
 M tela/teste_modelo.py
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
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0034_IMPLEMENTACAO.md
?? docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0034_HANDOFF.md
?? tela/__pycache__/
```

`git diff --name-only` final:

```text
demo/teste_demo.py
demo/teste_diagnostico.py
docs/NOMENCLATURA.md
docs/adr/INDICE_ADR.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_tela_json.md
tela/loader.py
tela/modelo.py
tela/renderizador.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
```

`git diff --check` final nao produziu saida. `git diff --cached --name-only`
final nao produziu saida; o stage permaneceu vazio.

```yaml
relatorio_criado_por_esta_auditoria:
  - docs/relatorios/RELATORIO_QA_POS_PATCH_H-0034_IMPLEMENTACAO.md
stage: vazio
```
