# RELATORIO_QA_POS_SEGUNDO_PATCH_H-0034_IMPLEMENTACAO

status_literal: I2_IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: patch_requerido
data_execucao: 2026-07-15
papel: auditor independente pos-segundo-patch
escopo: QA_IMPLEMENTACAO

## 1. Identificacao

Auditoria do segundo patch da implementacao H-0034, com foco nos achados
`QA-H0034-POS-IMPL-ALTO-001` e `QA-H0034-POS-IMPL-MEDIO-001`, preservacao dos
achados anteriores e fidelidade do relatorio IMP atualizado.

Nao foram corrigidos codigo, testes ou relatorios anteriores. Nao foi executada
validacao humana em TTY real. Nao foi preparado commit.

## 2. Relatorios anteriores

Lidos e confrontados:

- `docs/relatorios/RELATORIO_QA_H-0034_IMPLEMENTACAO.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0034_IMPLEMENTACAO.md`
- `docs/relatorios/IMP-0034-distribuicao-responsiva-lancador-fila-matriz.md`

O primeiro QA havia reprovado alinhamento por instancia, parametros normativos do
`lancador` e fidelidade do IMP. O QA pos-patch registrou dois novos achados:
`max_caracteres` hardcoded no renderer e sete erros pytest por coleta de funcoes
com fixture inexistente `tmp_base`.

## 3. Autoridades

Autoridades consultadas:

- `docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md`
- `docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0034_HANDOFF.md`
- `docs/adr/ADR-0023-largura-minima-funcional-lancador.md`
- `docs/contratos/contrato_lancador.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/NOMENCLATURA.md`
- `config/elementos/lancador.json`
- `config/telas/demo/demo.json`
- arquivos de implementacao e teste listados no prompt.

## 4. Estado Git inicial e final

Comandos iniciais executados:

```text
git status --short
git diff --name-only
git diff --check
git diff --cached --name-only
```

`git diff --check`: sem saida, codigo 0.

`git diff --cached --name-only`: sem saida; stage vazio.

Arquivos modificados no estado inicial:

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
```

Itens nao rastreados no inicio:

```yaml
- caminho: demo/__pycache__/
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
- caminho: docs/adr/ADR-0023-largura-minima-funcional-lancador.md
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
- caminho: docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
- caminho: docs/relatorios/IMP-0034-distribuicao-responsiva-lancador-fila-matriz.md
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
- caminho: docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
- caminho: docs/relatorios/RELATORIO_APLICACAO_ADR-0023.md
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
- caminho: docs/relatorios/RELATORIO_QA_ADR-0023.md
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
- caminho: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0023.md
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
- caminho: docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
- caminho: docs/relatorios/RELATORIO_QA_H-0034_IMPLEMENTACAO.md
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
- caminho: docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
- caminho: docs/relatorios/RELATORIO_QA_POS_PATCH_H-0034_HANDOFF.md
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
- caminho: docs/relatorios/RELATORIO_QA_POS_PATCH_H-0034_IMPLEMENTACAO.md
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
- caminho: docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0034_HANDOFF.md
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
- caminho: tela/__pycache__/
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
```

Estado final esperado apos este relatorio: mesmos itens acima, mais
`docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0034_IMPLEMENTACAO.md` como
unico arquivo criado por esta auditoria. Stage deve permanecer vazio.

## 5. Escopo real

O diff real contem alteracoes em `tela/loader.py`, `tela/modelo.py`,
`tela/renderizador.py`, `tela/teste_loader.py`, `tela/teste_modelo.py`,
`tela/teste_renderizador.py`, alem de `demo/teste_demo.py` e
`demo/teste_diagnostico.py`.

O segundo patch declarado ficou funcionalmente concentrado nos arquivos de tela
e no IMP. As alteracoes em `demo/teste_demo.py` e `demo/teste_diagnostico.py`
correspondem as excecoes operacionais anteriores descritas no IMP, nao ao
segundo patch. O estado Git tambem mostra documentos normativos modificados
(`docs/NOMENCLATURA.md`, contratos e indice ADR); esta auditoria nao atribui
proveniencia a esses itens sem evidencia adicional.

## 6. Resultado dos dois achados

```yaml
achado: QA-H0034-POS-IMPL-ALTO-001
estado: PARCIALMENTE_CORRIGIDO
evidencia: >
  A rota normal do renderer removeu _TEXTO_ITEM_MAX e consome
  params["verificacao"]["texto"]["max_caracteres"] em tela/renderizador.py:452-454.
  O loader valida e transporta o campo em tela/loader.py:403-441; o modelo
  propaga em tela/modelo.py:55, 194-200, 306-312.
testes: >
  loader 283/283; modelo 163/163; renderer 1052/1052; pytest focal 260 passed.
  test_max_caracteres_configuravel prova mc=3 aceito/rejeitado e mc=15 aceito.
residuos: >
  O caminho legado _linhas_lancador(elemento, content_w=None) retorna antes de
  consultar parametros_tipo e sem validar texto, em tela/renderizador.py:423-429.
regressoes: nenhuma regressao observada nas suites executadas.
conclusao: >
  Corrigido para renderizar_tela e caminhos responsivos, mas nao integralmente
  corrigido para o caminho legado explicitamente auditado.
```

```yaml
achado: QA-H0034-POS-IMPL-MEDIO-001
estado: CORRIGIDO
evidencia: >
  As sete funcoes internas de tela/teste_loader.py usam prefixo _run_ e os
  wrappers pytest usam tmp_path em tela/teste_loader.py:2392-2424.
testes: >
  PYTHONDONTWRITEBYTECODE=1 python -B -m pytest tela/teste_loader.py
  tela/teste_modelo.py tela/teste_renderizador.py -q --tb=short
  -p no:cacheprovider => 260 passed, 5 warnings, 0 errors, codigo 0.
residuos: >
  Persistem 5 PytestReturnNotNoneWarning preexistentes por funcoes que retornam
  objetos, mas nao ha fixture inexistente nem erro de coleta.
regressoes: nenhuma.
conclusao: corrigido.
```

## 7. Preservacao dos achados anteriores

```yaml
QA-H0034-IMPL-ALTO-001:
  estado: CORRIGIDO
  evidencia: >
    Alinhamento por instancia preservado em fila e matriz; posicoes literais
    verificadas no renderer: esquerda pos 7, centro pos 9, direita pos 10 nos
    testes H-0034 ALTO-001.
QA-H0034-IMPL-ALTO-002:
  estado: PARCIALMENTE_CORRIGIDO
  evidencia: >
    Vaos, margens verticais e max_caracteres vem de parametros_tipo na rota
    normal. Residuo: caminho legado sem content_w nao usa parametros_tipo.
QA-H0034-IMPL-MEDIO-001:
  estado: CORRIGIDO_COM_RESSALVAS
  evidencia: >
    IMP registra primeiro QA, patches, achados, contagens novas, smoke e
    validacao humana pendente. Ressalva: o proprio IMP documenta que o caminho
    legado ficou sem validacao de texto, mas classifica o achado como corrigido.
```

## 8. Fluxo de max_caracteres

Fluxo auditado:

```text
config/elementos/lancador.json
-> tela/loader.py:_carregar_e_validar_config_lancador
-> chave interna _config_lancador
-> tela/modelo.py:ElementoCorpo.parametros_tipo
-> tela/renderizador.py:_linhas_lancador
```

Confirmado:

- valor real em `config/elementos/lancador.json`: `15`;
- arquivo real nao foi alterado;
- leitura ocorre no loader por `base / config/elementos/lancador.json`;
- renderer nao importa `json`, `os` ou `pathlib`, e nao usa `open`/`read_text`;
- modelo separa `parametros_tipo` de `_campos_inertes`;
- lancadores diretos e recursivos recebem `parametros_tipo`;
- console e dashboard ficam com `parametros_tipo=None`;
- configuracao de instancia (`layout.alinhamento`) permanece em `_campos_inertes`.

Residuo: a chamada legada direta `_linhas_lancador(elemento, content_w=None)` nao
entra nesse fluxo.

## 9. Validacao do loader

Confirmado em codigo e testes:

- presenca de `verificacao`, `verificacao.texto`, `max_caracteres`;
- tipo inteiro, rejeitando booleano explicitamente;
- valor maior que zero; zero e negativo rejeitados;
- string rejeitada;
- JSON invalido e arquivo ausente rejeitados;
- independencia do diretorio atual;
- base temporaria criada em `tmp_path`/`tempfile`, sem escrita na arvore real;
- assinatura publica de `carregar_tela(caminho_base, id_tela, raiz_telas=None)` preservada.

Politica ativa para estrutura desconhecida em `verificacao.texto`: campo extra e
aceito/ignorado, conforme teste Mc-8.

## 10. Propagacao do modelo

`ElementoCorpo` agora tem `parametros_tipo` em `tela/modelo.py:55`. A construcao
recursiva passa `parametros_lancador` aos lancadores em `tela/modelo.py:194-200`;
o corpo raiz faz o mesmo em `tela/modelo.py:306-312`. Outros tipos nao recebem
parametros indevidos.

## 11. Consumo no renderer

Confirmado:

- `_TEXTO_ITEM_MAX` removido;
- nao ha literal `15` como substituto normativo no caminho normal;
- `_itens_lancador_normalizados(elemento, max_caracteres)` recebe limite
  propagado;
- fila, matriz, coluna minima e cardinalidade 1 usam o valor recebido;
- item acima do limite e rejeitado; item no limite e aceito;
- nao ha truncamento nem reticencias;
- renderer nao le JSON diretamente.

Residuo: o caminho legado `content_w is None` ignora validacao de texto e
`parametros_tipo`.

## 12. Busca completa de hardcoding normativo

```yaml
- nome_ou_literal: max_caracteres / 15
  uso: valor real no JSON e em fixture de teste; renderer normal usa params
  autoridade: config/elementos/lancador.json
  configuravel: sim
  duplicacao_normativa: nao no caminho normal; sim como fixture de teste
  conclusao: corrigido no caminho normal
- nome_ou_literal: chip_texto minimo/maximo
  uso: renderer consome params["vaos"]["chip_texto"]["minimo"]
  autoridade: config/elementos/lancador.json
  configuravel: sim
  duplicacao_normativa: nao no caminho normal
  conclusao: preservado
- nome_ou_literal: entre_itens_colunas_margem minimo/maximo
  uso: renderer consome params["vaos"]["entre_itens_colunas_margem"]
  autoridade: config/elementos/lancador.json
  configuravel: sim
  duplicacao_normativa: nao no caminho normal
  conclusao: preservado
- nome_ou_literal: margem_borda_superior / margem_borda_inferior
  uso: renderer consome params["vertical"]
  autoridade: config/elementos/lancador.json
  configuravel: sim
  duplicacao_normativa: nao no caminho normal
  conclusao: preservado
- nome_ou_literal: politicas de fila/matriz/ordem/alinhamento
  uso: algoritmo implementado no renderer
  autoridade: config/elementos/lancador.json, contrato_lancador e ADR-0023
  configuravel: parcialmente descritivo/normativo
  duplicacao_normativa: algoritmo codificado, nao fallback numerico silencioso
  conclusao: sem regressao observada, mas o caminho legado ainda contorna parametros
```

## 13. Parametros alternativos

Prova independente com `max_caracteres: 3`:

- `"Uno"` com 3 caracteres aceito;
- `"Quat"` com 4 caracteres rejeitado;
- `"Quatro"` com 6 caracteres rejeitado;
- `max_caracteres: 15` aceita `"Quatro"`;
- alteracao decorre de `ElementoCorpo.parametros_tipo` em memoria;
- nenhuma constante produtiva foi monkeypatched;
- arquivo real nao foi alterado.

## 14. Alinhamento

Revalidado por testes diretos do renderer:

- fila: esquerda, centro, direita;
- matriz: esquerda, centro, direita;
- ausencia de alinhamento equivalente a esquerda;
- valor invalido levanta `RenderizadorErro`;
- demo em largura 110 preserva esquerda com `[d]` na posicao 4;
- patch de `max_caracteres` nao alterou alinhamento.

## 15. Harness pytest

Confirmado:

- helpers `_run_*` nao sao coletados pelo pytest;
- sete wrappers `teste_*` recebem `tmp_path`;
- cada wrapper cria `config/elementos/lancador.json` temporario;
- runner direto chama helpers;
- nao ha `skip` ou `xfail` nos arquivos focais;
- nenhuma fixture `tmp_base` permanece coletada como teste;
- nao ha caminho fixo `/tmp` nos wrappers pytest; o runner direto usa
  `tempfile.mkdtemp`, como ja fazia.

## 16. Testes novos

Loader:

- Mc-1 a Mc-3 cobrem ausencia de `verificacao`, `verificacao.texto` e
  `max_caracteres`;
- Mc-4 a Mc-7 cobrem string, booleano, zero e negativo;
- Mc-8 cobre campo extra desconhecido aceito/ignorado;
- Mc-9 cobre valor canonico 15;
- Mc-10 cobre valor alternativo 3 propagado.

Modelo:

- pipeline real propaga `max_caracteres == 15`;
- valor alternativo 3 em memoria e propagado.

Renderer:

- `test_max_caracteres_configuravel` cobre ausencia de `_TEXTO_ITEM_MAX`, aceite
  no limite 3, rejeicao acima do limite, aceite com 15 e fixture demo com 15.

Ressalva: os testes novos nao cobrem o caminho legado `content_w is None`.

## 17. Onze falhas anteriores do loader

O IMP diferencia os sete erros pytest de fixture do segundo patch. Sobre as
falhas anteriores do loader, a narrativa atual nao enumera literalmente "onze"
falhas em um bloco proprio; ela distribui a explicacao por historico, excecoes
operacionais e contagens. Nao encontrei evidencia de assert relaxado nem de
cobertura removida; a contagem direta subiu para 283/283.

## 18. Regressoes H-0034

Revalidado por `python -B tela/teste_renderizador.py`:

- largura 110: fila;
- largura 109: matriz;
- largura 80: matriz 4x2;
- larguras independentes `[14, 13, 14, 14]`;
- preenchimento coluna a coluna;
- T-07;
- area 21: coluna valida;
- area 20: quadro minimo global;
- T-ISOL-01, T-ISOL-02, T-ISOL-03;
- cardinalidades zero, um e dois;
- alinhamento esquerda, centro e direita;
- margens verticais;
- ausencia de paginacao, perda, duplicacao e truncamento.

Nao foram observadas regressoes nas suites executadas.

## 19. Suite focal

Comando executado:

```text
PYTHONDONTWRITEBYTECODE=1 python -B -m pytest tela/teste_loader.py tela/teste_modelo.py tela/teste_renderizador.py -q --tb=short -p no:cacheprovider
```

Resultado:

```yaml
codigo_de_saida: 0
resultado: 260 passed
errors: 0
warnings: 5
duracao: 0.29s
```

Warnings: cinco `PytestReturnNotNoneWarning` em testes que retornam objetos; nao
relacionados aos sete erros de fixture anteriores.

## 20. Suite canonica

```yaml
tela/teste_loader.py:
  codigo_de_saida: 0
  verificacoes: 283/283
tela/teste_modelo.py:
  codigo_de_saida: 0
  verificacoes: 163/163
tela/teste_renderizador.py:
  codigo_de_saida: 0
  verificacoes: 1052/1052
demo/teste_demo.py:
  codigo_de_saida: 0
  verificacoes: 358/358
demo/teste_diagnostico.py:
  codigo_de_saida: 0
  verificacoes: 30/30
demo/teste_explorar_barra_de_menus.py:
  codigo_de_saida: 0
  verificacoes: 38/38
total_calculado: 1924/1924
```

## 21. Smoke

Comando:

```text
printf 's\n' | python -B demo/demo.py
```

Resultado:

- codigo de saida 0;
- contem `ORQUESTRADOR`;
- contem `NAVEGAR`;
- contem sete itens `[d]`, `[g]`, `[1]`, `[2]`, `[3]`, `[4]`, `[5]`;
- sem `Traceback`.

Este smoke e distinto das 358 verificacoes de `demo/teste_demo.py`.

## 22. Fidelidade do IMP

O IMP atualizado registra primeiro QA, primeiro patch, QA pos-patch, segundo
patch, `max_caracteres`, falha pytest, contagens novas, fluxo
configuracao-loader-modelo-renderer, alinhamento por instancia, excecoes
operacionais, smoke, validacao humana pendente e ausencia de autoaprovacao.

Ressalvas:

- classifica `QA-H0034-POS-IMPL-ALTO-001` como corrigido, embora descreva que o
  caminho legado ficou "sem validacao de texto";
- nao encontrei bloco literal que enumere "onze falhas preexistentes" do loader;
- o relatorio contem secoes historicas com contagens antigas, mas a secao do
  segundo patch registra as contagens atuais.

## 23. Validacao humana pendente

Nao executada por instrucao. Como ha achado tecnico residual, o status nao e
`I5_MANUAL_VALIDATION_REQUIRED`; e `I2_IMPLEMENTATION_PATCH_REQUIRED`.

## 24. Novos achados

```yaml
- id: QA-H0034-POS-SEGUNDO-IMPL-MEDIO-001
  severidade: medio
  arquivo: tela/renderizador.py
  trecho: linhas 423-429
  evidencia: >
    _linhas_lancador(elemento, content_w=None) retorna linhas formatadas a
    partir de _itens_brutos antes de consultar elemento.parametros_tipo e antes
    de chamar _itens_lancador_normalizados(elemento, max_caracteres).
  regra_violada: >
    O prompt exige auditar o caminho legado e determina que todos os caminhos
    relevantes usem o valor recebido, sem fallback numerico silencioso nem
    reintroducao de limite proprio incompatavel.
  impacto: >
    Chamadas diretas legadas a _linhas_lancador podem aceitar texto acima de
    verificacao.texto.max_caracteres. A rota normal renderizar_tela nao e
    afetada porque sempre passa content_w.
  correcao_necessaria: >
    Fazer o caminho legado consultar parametros_tipo e aplicar
    _itens_lancador_normalizados com max_caracteres, ou remover/fechar
    explicitamente esse caminho se ele nao for parte da API suportada.
```

## 25. Status literal e normalizado

```yaml
status_literal: I2_IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: patch_requerido
motivo: >
  As suites estao verdes e os dois achados principais foram corrigidos na rota
  normal, mas ha residuo tecnico no caminho legado do renderer explicitamente
  solicitado para auditoria.
```

## 26. Proxima categoria

proxima_categoria: PATCH_IMPLEMENTACAO
