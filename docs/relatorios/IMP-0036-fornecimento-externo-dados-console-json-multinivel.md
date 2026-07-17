---
name: IMP-0036-fornecimento-externo-dados-console-json-multinivel
description: Relatorio factual da implementacao do H-0036 — fornecimento externo de dados ao console por JSON multinivel (carregamento separado pelo demo.py, 20 validacoes, modelo, tres apresentacoes, revisao dos JSONs do H-0035)
metadata:
  type: relatorio_implementacao
  id: IMP-0036
  handoff: H-0036
  data: "2026-07-17"
  etapa: IMPLEMENTAR
  status_literal: IMPLEMENTATION_COMPLETED
---

# IMP-0036 — Implementacao do H-0036

> Relatorio factual da etapa `IMPLEMENTAR`. Nao aprova a propria implementacao,
> nao declara validacao visual e nao inicia QA, stage, commit ou novo ciclo.

## 1. Identificacao

| Campo | Valor |
|---|---|
| Relatorio | IMP-0036 |
| Handoff | H-0036 (QA final `H1_HANDOFF_APPROVED`, implementacao AUTORIZADA) |
| Etapa executada | IMPLEMENTAR |
| Data | 2026-07-17 |
| Branch | master |
| HEAD inicial | fb9e5be |
| Commit novo | NAO realizado |
| Stage | vazio |

## 2. Autoridades

Lidas integralmente antes de qualquer alteracao (ordem de autoridade: contratos
ativos > ADR-0027 > ADR-0026 > H-0036 aprovado > relatorios como evidencia):

- `docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md`
- `docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md`
- `docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md`
- `docs/contratos/contrato_tela_json.md`, `contrato_console.md`, `contrato_json_console.md`
- `docs/NOMENCLATURA.md`
- `docs/relatorios/RELATORIO_QA_H-0036_HANDOFF.md`,
  `RELATORIO_QA_POS_PATCH_H-0036_HANDOFF.md`,
  `RELATORIO_QA_POS_SEGUNDO_PATCH_H-0036_HANDOFF.md`
- Preservacao do ciclo anterior: `ADR-0025`, `H-0035`, `IMP-0035`.

O schema semantico multinivel, as 20 validacoes, as tres apresentacoes, os tres
tipos de nivel, os designadores e os resultados fisicos proibidos foram tratados
como requisitos FECHADOS (ADR-0027 D11/D13; `contrato_json_console.md` §12). Nao
foram decididos pela implementacao.

## 3. Estado Git inicial

```
branch: master
head: fb9e5be
git diff --check: sem erros
```

O workspace ja continha artefatos documentais acumulados das ADR-0026, ADR-0027
e H-0036 (arquivos `docs/adr/ADR-002{6,7}-*`, `docs/handoff/H-0036-*`,
`docs/relatorios/RELATORIO_*ADR-002{6,7}*`, `docs/relatorios/RELATORIO_QA_*H-0036*`
e modificacoes em `docs/NOMENCLATURA.md`, `docs/adr/INDICE_ADR.md`,
`docs/contratos/contrato_*`). **Esses documentos NAO foram atribuidos a esta
implementacao, NAO foram alterados e NAO foram restaurados.**

## 4. Lista nominal autorizada (13 alterar + 10 criar = 23; duplicatas 0)

**Alterar (13):**

1. `tela/loader.py`
2. `tela/modelo.py`
3. `tela/renderizador.py`
4. `tela/teste_loader.py`
5. `tela/teste_modelo.py`
6. `tela/teste_renderizador.py`
7. `demo/demo.py`
8. `demo/teste_demo.py`
9. `demo/teste_diagnostico.py`
10. `demo/teste_demo_distribuicao.py`
11. `config/telas/demo/h0035_console_com.json`
12. `config/telas/demo/h0035_console_sem.json`
13. `config/telas/demo/demo.json`

**Criar (10):**

1. `config/telas/demo/h0036_console_hierarquia.json`
2. `config/telas/demo/h0036_console_tabela.json`
3. `config/telas/demo/h0036_console_conjuntos.json`
4. `config/telas/demo/h0036_hierarquia_conteudo.json`
5. `config/telas/demo/h0036_tabela_conteudo.json`
6. `config/telas/demo/h0036_conjuntos_conteudo.json`
7. `config/telas/demo/h0035_console_com_conteudo.json`
8. `config/telas/demo/h0035_console_sem_conteudo.json`
9. `demo/teste_demo_console.py`
10. `docs/relatorios/IMP-0036-fornecimento-externo-dados-console-json-multinivel.md`

Conferencia: `quantidade_ALTERAR: 13`, `quantidade_CRIAR: 10`,
`caminhos_unicos: 23`, `duplicatas: 0`, `conflitos_com_preservados: 0`.

## 5. Arquivos realmente alterados (12)

`tela/loader.py`, `tela/modelo.py`, `tela/renderizador.py`,
`tela/teste_loader.py`, `tela/teste_modelo.py`, `tela/teste_renderizador.py`,
`demo/demo.py`, `demo/teste_demo.py`, `demo/teste_diagnostico.py`,
`demo/teste_demo_distribuicao.py`,
`config/telas/demo/h0035_console_com.json`,
`config/telas/demo/h0035_console_sem.json`.

## 6. Arquivos realmente criados (9 + este relatorio)

`config/telas/demo/h0036_console_hierarquia.json`,
`config/telas/demo/h0036_console_tabela.json`,
`config/telas/demo/h0036_console_conjuntos.json`,
`config/telas/demo/h0036_hierarquia_conteudo.json`,
`config/telas/demo/h0036_tabela_conteudo.json`,
`config/telas/demo/h0036_conjuntos_conteudo.json`,
`config/telas/demo/h0035_console_com_conteudo.json`,
`config/telas/demo/h0035_console_sem_conteudo.json`,
`demo/teste_demo_console.py`,
e este relatorio `docs/relatorios/IMP-0036-...md`.

## 7. Arquivo autorizado NAO alterado e justificativa

- `config/telas/demo/demo.json` — **nao alterado.**

  A autorizacao (§15.1 do handoff) era CONDICIONAL: "Adicionar entradas de
  launcher para os cenarios H-0036 **se o mecanismo de catalogo do demo.py
  exigir entradas no JSON estrutural**". O mecanismo de catalogo adotado nao
  exige entradas no JSON estrutural: a associacao vive no dicionario interno
  `_CATALOGO_CONTEUDO_EXTERNO` do `demo.py`, e o acesso pelo ponto de entrada
  ocorre por argumento de tela inicial (`python demo/demo.py <cenario>`),
  seguindo o precedente ja existente de `demo/demo_distribuicao.py <id_tela>`.
  Assim, a identidade e a finalidade historica do launcher da demonstracao
  foram integralmente preservadas (nenhum item de launcher novo, nenhum literal
  de layout do `demo.json` alterado). Nenhuma exceção operacional foi
  necessaria; nenhum arquivo fora da lista nominal foi tocado.

## 8. Mecanismo interno de associacao no `demo.py`

- **Catalogo:** `demo/demo.py` define
  `_CATALOGO_CONTEUDO_EXTERNO: dict[str, str]` (id da tela estrutural ->
  id/nome-base do documento externo de conteudo, na raiz `config/telas/demo`).
  A AUSENCIA de conteudo externo e representada explicitamente pela AUSENCIA da
  chave (nao herdada, nao implicita).

  ```yaml
  h0036_console_hierarquia: h0036_hierarquia_conteudo
  h0036_console_tabela:      h0036_tabela_conteudo
  h0036_console_conjuntos:   h0036_conjuntos_conteudo
  h0035_console_com:         h0035_console_com_conteudo
  h0035_console_sem:         h0035_console_sem_conteudo
  ```

- **API interna efetiva:**
  - `id_conteudo_externo_de(id_tela) -> str | None`: consulta o catalogo;
    ausencia -> `None`.
  - `_carregar_modelo_por_id(id_tela)`: carrega o JSON estrutural com
    `carregar_tela(None, id_tela, _RAIZ_TELAS_DEMO)`; quando o catalogo associa
    um documento externo, carrega-o SEPARADAMENTE com
    `carregar_conteudo_externo(None, id_conteudo, _RAIZ_TELAS_DEMO)`; entrega os
    dois documentos como entradas distintas a
    `construir_modelo(tela_raw, conteudo_externo=conteudo_externo)`. Cada
    chamada reconstroi o modelo do zero — sem estado residual entre trocas de
    cenario (sem heranca, sem vazamento).
  - `_tela_inicial_de_argv(argv) -> str`: resolve a tela inicial do ponto de
    entrada (primeiro argumento posicional; default `"demo"`).
  - `main(argv=None)`: aceita opcionalmente o cenario inicial via argv.

- **Cenarios acessiveis e metodo:** todos os 5 cenarios com conteudo externo
  (`h0036_console_hierarquia|tabela|conjuntos`, `h0035_console_com|sem`) e
  qualquer tela sem conteudo sao acessiveis por
  `python demo/demo.py <id_tela>`. Sem argumento, abre a tela raiz `demo`
  (cenario sem conteudo -> placeholder). A associacao NAO foi criada como campo
  no JSON estrutural.

## 9. API interna efetiva do loader e do modelo

**Loader (`tela/loader.py`):**

- `carregar_conteudo_externo(caminho_base, id_conteudo, raiz_telas=None) -> dict`:
  abre, decodifica (`json.loads`) e valida o documento externo; devolve o
  documento validado (representacao semantica no nivel do loader). Nao abre o
  JSON estrutural, nao vincula tela e conteudo, nao calcula geometria, nao
  infere hierarquia.
- `validar_conteudo_externo(documento, origem=...) -> dict`: executa as 20
  validacoes; exposto para testes em memoria.
- Auxiliares: `_validar_no_conteudo`, `_validar_designador_conteudo`,
  `_rejeitar_resultados_fisicos_conteudo`.
- Constantes: `APRESENTACOES_CONTEUDO_VALIDAS`, `TIPOS_NIVEL_CONTEUDO_VALIDOS`,
  `TIPOS_DESIGNADOR_VALIDOS`, `CAMPOS_RESULTADO_FISICO_PROIBIDOS`.
- **Classes de erro:** reutiliza as existentes (nenhuma classe nova):
  `TelaEstruturaInvalida`, `TelaCampoObrigatorioAusente`, `TelaJsonInvalido`,
  `TelaArquivoNaoEncontrado` (todas subclasses de `TelaErro`).

**Modelo (`tela/modelo.py`):**

- `construir_modelo(tela_raw, conteudo_externo=None) -> ModeloTela`: recebe
  estrutura e conteudo como entradas SEPARADAS; aceita o dict validado do loader
  ou um `ConteudoExterno` ja tipado. Nao abre arquivos, nao escolhe fonte, nao
  calcula geometria.
- `construir_conteudo_externo(conteudo_raw) -> ConteudoExterno | None`.
- `_propagar_conteudo_externo(...)`: associa o conteudo a cada `ElementoCorpo`
  do tipo console (recursivo em grupos).

## 10. Representacao semantica adotada

Dataclasses em `tela/modelo.py` (origem SEPARADA do JSON estrutural; nunca
reinserida em `_raw` nem em `_campos_inertes`):

- `NivelConteudo(id, tipo, conteudo, designador, _campos_inertes)`
- `NoConteudo(id, nivel, campos, filhos)` — `filhos` preserva a hierarquia
  declarada e a ordem original.
- `ConteudoExterno(tipo, apresentacao, niveis, nos, formato, _raw)` com
  `nivel_por_id`.
- `ModeloTela.conteudo_externo` e `ElementoCorpo.conteudo_externo` transportam a
  mesma referencia tipada; ausencia -> `None`.

A ordem dos arrays e preservada por construcao (listas, sem reordenacao). A
hierarquia usa exclusivamente `filhos` (nunca inferida por nome, posicao,
prefixo, ID ou convencao externa).

## 11. Implementacao das tres apresentacoes (renderizador)

`tela/renderizador.py`, `_linhas_console(elemento, content_w)` despacha para
`_linhas_conteudo_externo(conteudo, content_w)`:

- **`hierarquia`** (`_linhas_apresentacao_hierarquia`): lista recuada por
  profundidade, com designador por nivel.
- **`tabela`** (`_linhas_apresentacao_tabela`): cabecalho + regua + linhas com
  colunas alinhadas por largura calculada pelo renderizador; `ancestrais:
  "repetir"` repete os textos ancestrais como colunas iniciais.
- **`conjuntos_campos`** (`_linhas_apresentacao_conjuntos`): conjuntos
  (container + designador + titulo) com pares nome-valor justificados por
  conjunto e separador de `formato.campos`.

Sem conteudo externo, `_linhas_console` retorna o placeholder historico
`["(console)"]` (compatibilidade retroativa). O renderizador nao abre arquivos
(nao importa `json`/`os`/`pathlib`; nao chama `carregar_conteudo_externo` —
verificado por inspecao de fonte no teste).

## 12. Implementacao dos tres tipos de nivel

- `container`: campo textual (`conteudo`) + `filhos` (array), recursivo.
- `conteudo`: campo textual diretamente exibivel.
- `nome_valor`: par declarado por `conteudo.{nome,valor}`, exibido como
  `"nome: valor"` (hierarquia/conjuntos) ou em colunas (tabela).

`_texto_no_conteudo(no, nivel)` resolve o texto exibivel conforme o tipo.

## 13. Designadores

`_texto_designador(designador, ordinal, ancestrais)` calcula o texto concreto a
partir da POLITICA declarativa (o documento nunca armazena numeracao pronta).
Tipos suportados: `nenhum`, `simbolo`, `decimal`, `alfabetico_minusculo`,
`alfabetico_maiusculo`, `romano_minusculo`, `romano_maiusculo`,
`decimal_composto`, `personalizado`. Campos condicionais aplicados: `prefixo`,
`sufixo`, `valor`, `separador`. Auxiliares `_romano` e `_alfabetico`
(bijetivo). Exemplos observados na demonstracao: `1.`, `1.1.`, `a)`, `IV`, `AA`.

## 14. Vinte validacoes (loader) — casos e classes de erro

Implementadas nominalmente em `validar_conteudo_externo` e testadas em
`tela/teste_loader.py::teste_conteudo_externo_h0036` (aceitacao e rejeicao com
verificacao da CLASSE de erro de dominio):

| # | Validacao | Classe de erro |
|---|---|---|
| 1 | raiz e objeto | TelaEstruturaInvalida |
| 2 | `tipo` presente e string | TelaCampoObrigatorioAusente / TelaEstruturaInvalida |
| 3 | `tipo == "multinivel"` | TelaEstruturaInvalida |
| 4 | `formato` presente e objeto | TelaCampoObrigatorioAusente / TelaEstruturaInvalida |
| 5 | `dados` presente e array | TelaCampoObrigatorioAusente / TelaEstruturaInvalida |
| 6 | `formato.apresentacao` presente | TelaCampoObrigatorioAusente |
| 7 | apresentacao valida | TelaEstruturaInvalida |
| 8 | `formato.niveis` presente e array | TelaCampoObrigatorioAusente / TelaEstruturaInvalida |
| 9 | nivel com id/tipo/conteudo/designador | TelaCampoObrigatorioAusente |
| 10 | ids de nivel nao vazios e unicos | TelaEstruturaInvalida |
| 11 | tipo de nivel valido | TelaEstruturaInvalida |
| 12 | no com id e nivel | TelaCampoObrigatorioAusente |
| 13 | `nivel` referencia nivel declarado | TelaEstruturaInvalida |
| 14 | container com campo semantico + filhos array | TelaCampoObrigatorioAusente / TelaEstruturaInvalida |
| 15 | conteudo com campo semantico | TelaCampoObrigatorioAusente |
| 16 | nome_valor com nome e valor | TelaCampoObrigatorioAusente |
| 17 | filhos validados recursivamente | (mesma regra, recursivo) |
| 18 | ordem dos arrays preservada | verificado materialmente (nao reordena) |
| 19 | blocos especificos compativeis (`tabela`/`campos`) | TelaEstruturaInvalida |
| 20 | ausencia de resultados fisicos calculados | TelaEstruturaInvalida |

Alem disso: `designador.tipo` invalido, JSON sintaticamente invalido
(`TelaJsonInvalido`) e documento ausente (`TelaArquivoNaoEncontrado`). Os testes
verificam resultados materiais (classe e efeito), nao apenas ausencia de
excecao.

## 15. Resultados fisicos rejeitados

`_rejeitar_resultados_fisicos_conteudo` percorre o documento recursivamente e
rejeita, em qualquer profundidade, os nomes de campo mapeados a partir das
formas fisicas proibidas normativas (`contrato_json_console.md` §12.6; H-0036
§13.8):

```
largura_efetiva, altura_efetiva, linhas_calculadas, colunas_calculadas,
posicao_final, coordenada_final, pagina_calculada, quebra_pronta,
truncamento_aplicado, distribuicao_concreta, celulas_vazias, geometria_final,
numeracao_concreta
```

A deteccao rejeita apenas esses nomes exatos; nao amplia silenciosamente a
proibicao para campos semanticos validos. Testado na raiz e aninhado.

## 16. Inventario dos 26 JSONs do H-0035

Confirmada a classificacao do §11 do handoff: total 26; `ALTERAR_E_SEPARAR` 2
(`h0035_console_com.json`, `h0035_console_sem.json`);
`PRESERVAR_SEM_ALTERACAO` 24. Os 24 preservados nao foram tocados (nenhum
aparece em `git status`). Nenhuma reclassificacao foi feita durante a
implementacao.

## 17. Adaptacao dos dois JSONs afetados

- `h0035_console_com.json`: removido o campo `itens` (12 itens de runtime);
  preservados `titulo`, `overflow_normal` e a `distribuicao_matricial`
  (`preferencia_colunas`, 2 colunas) integral. Conteudo movido para
  `h0035_console_com_conteudo.json`.
- `h0035_console_sem.json`: removido o campo `itens` (2 itens); preservada a
  configuracao estrutural restante. Conteudo movido para
  `h0035_console_sem_conteudo.json`.

Nao ha duplicacao: os textos (`P01 linha`..`P12 linha`, `Linha alfa`,
`Linha bravo`) estao SOMENTE nos documentos externos, ausentes do estrutural
(provado em `demo/teste_demo_distribuicao.py::teste_separacao_h0036_console`).

## 18. Preservacao dos outros 24

Os 24 JSONs `h0035_*` classificados como `PRESERVAR_SEM_ALTERACAO` permanecem
byte-a-byte inalterados (nao aparecem no `git status`). A suite de regressao
(`teste_demo_distribuicao.py`, `teste_diagnostico.py`, `teste_renderizador.py`)
permanece verde.

## 19. Fixtures criadas

| Fixture | Apresentacao | Niveis / tipos | Designadores | Identidade |
|---|---|---|---|---|
| `h0036_hierarquia_conteudo.json` | hierarquia | 3 (container, container, conteudo) | decimal, decimal_composto, alfabetico_minusculo | `Fluxo H-0036 hierarquia`, `Documento H-0036 carregado pelo demo.py` |
| `h0036_tabela_conteudo.json` | tabela | 2 (container, nome_valor) | nenhum, decimal | `tabela H-0036`, `Entradas`/`Saidas` |
| `h0036_conjuntos_conteudo.json` | conjuntos_campos | 2 (container, nome_valor) | decimal, nenhum | `Parametros`/`Origens`, valor `H-0036` |
| `h0035_console_com_conteudo.json` | hierarquia | 1 (conteudo) | nenhum | `P01 linha`..`P12 linha` |
| `h0035_console_sem_conteudo.json` | hierarquia | 1 (conteudo) | nenhum | `Linha alfa`, `Linha bravo` |

Cobertura em conjunto: 3 apresentacoes; 3 niveis hierarquicos (hierarquia);
multiplos nos em >= 2 niveis; `container`, `conteudo`, `nome_valor`; `filhos`;
preservacao de ordem; designadores declarativos; texto direto; par nome-valor;
blocos especificos (`tabela` so em tabela, `campos` so em conjuntos_campos);
ausencia de geometria. A fixture principal contem a string exclusiva `"H-0036"`,
visivel no console e ausente do JSON estrutural correspondente.

## 20. Identidades semanticas

Cada cenario possui identidade semantica exclusiva e verificavel (usada por
smoke tests e demo tecnico):

```yaml
h0036_console_hierarquia:  "H-0036" / "Fluxo H-0036 hierarquia"
h0036_console_tabela:      "tabela H-0036" / "Entradas"
h0036_console_conjuntos:   "Parametros" / valor "H-0036"
h0035_console_com:         "P01 linha" .. "P12 linha"
h0035_console_sem:         "Linha alfa" / "Linha bravo"
```

## 21. Testes do loader

`tela/teste_loader.py::teste_conteudo_externo_h0036`: envelope minimo aceito; as
20 validacoes (aceitacao + rejeicao com classe de erro); designador invalido;
ordem preservada materialmente; JSON invalido e documento ausente; carga com
sucesso das 5 fixtures permanentes (fontes validas em arquivo). Contagem do
script: 303 -> 348 (+45).

## 22. Testes do modelo

`tela/teste_modelo.py::teste_conteudo_externo_h0036_modelo`: entradas separadas;
origens distintas (conteudo nao reinserido em `_raw`); ordem de `dados` e de
`filhos`; niveis acessiveis; pais e filhos; `container`/`conteudo`/`nome_valor`
acessiveis; ausencia de campos de geometria no modelo; aceitacao de
`ConteudoExterno` ja tipado; cenario sem conteudo -> `None`. Contagem: 169 ->
186 (+17).

## 23. Testes do renderizador

`tela/teste_renderizador.py::teste_conteudo_externo_h0036_render`: designadores
concretos (unitarios: decimal, alfabetico, romano, decimal_composto, simbolo;
`_romano`, `_alfabetico`); tres apresentacoes sem placeholder; conteudo direto;
pares nome-valor; recuo hierarquico recursivo; identidade `H-0036` na saida;
placeholder ausente com conteudo e preservado sem conteudo; render integrado;
truncamento como calculo (largura 24 respeitada); `h0035_console_com` com DM +
externo (grade `P01..P12`); inspecao de fonte (renderizador nao abre arquivos).
Contagem: 1191 -> 1223 (+32).

## 24. Testes do catalogo e `demo.py`

- `demo/teste_demo_console.py` (NOVO, 72 verificacoes): catalogo e ausencia
  explicita; carregamento separado por cenario; tres apresentacoes acessiveis;
  ausencia de mistura entre cenarios e ausencia de residuo na troca; smoke tests
  semanticos por cenario; ponto de entrada real (`python demo/demo.py <cenario>`
  e sem argumento). Responsabilidade distinta dos testes focais.
- `demo/teste_demo.py` (+5): `teste_catalogo_conteudo_externo_h0036` —
  compatibilidade retroativa (cenario `demo` sem conteudo -> `None`,
  `conteudo_externo` None), presenca do catalogo e resolucao de argv. 358 ->
  363.
- `demo/teste_diagnostico.py` (+7): `teste_pipeline_h0036` — pipeline integrado
  `carregar tela + carregar externo + construir + renderizar` para os 5 cenarios
  e cenario sem conteudo (placeholder). 41 -> 48.

## 25. Testes de regressao (H-0035 / ADR-0025)

`demo/teste_demo_distribuicao.py` (+10): `_n_campos_fixture` passou a contar os
nos do documento externo para os consoles adaptados (carregamento separado dos
dois arquivos); novo `teste_separacao_h0036_console` prova: `itens` ausente do
estrutural; associacao no catalogo; contagem do externo (12 / 2); nao-duplicacao
(textos so no externo); `distribuicao_matricial` de `h0035_console_com`
preservada; `h0035_console_sem` permanece sem DM. A distribuicao matricial
configuravel do H-0035 permanece funcional. 99 -> 109.

## 26. Smoke tests (por cenario)

Provados em `teste_demo_console.py` (nao usam codigo de saida zero, ausencia de
excecao, nome de arquivo, esperado derivado da saida nem snapshot da propria
saida; o esperado e definido independentemente na matriz `_SMOKE`):

```yaml
h0036_console_hierarquia: {estrutural: h0036_console_hierarquia, externo: h0036_hierarquia_conteudo, identidade: "H-0036", incorreto_ausente: "Parametros", placeholder: AUSENTE}
h0036_console_tabela:     {estrutural: h0036_console_tabela,     externo: h0036_tabela_conteudo,     identidade: "tabela H-0036", incorreto_ausente: "Fluxo H-0036 hierarquia", placeholder: AUSENTE}
h0036_console_conjuntos:  {estrutural: h0036_console_conjuntos,  externo: h0036_conjuntos_conteudo,  identidade: "Parametros" + "H-0036", incorreto_ausente: "Entradas", placeholder: AUSENTE}
h0035_console_com:        {estrutural: h0035_console_com,        externo: h0035_console_com_conteudo, identidade: "P01 linha".."P12 linha", incorreto_ausente: "Linha alfa", placeholder: AUSENTE}
h0035_console_sem:        {estrutural: h0035_console_sem,        externo: h0035_console_sem_conteudo, identidade: "Linha alfa"/"Linha bravo", incorreto_ausente: "P01 linha", placeholder: AUSENTE}
cenario_sem_conteudo (demo / h0030_console_unico): {externo: NENHUM, placeholder: PRESENTE, sem vazamento de "H-0036"}
```

## 27. Baseline inicial (8 scripts, antes das alteracoes)

```yaml
comandos: PYTHONDONTWRITEBYTECODE=1 python <script>
contagens_por_script:
  tela/teste_loader.py: 303
  tela/teste_modelo.py: 169
  tela/teste_renderizador.py: 1191
  tela/teste_distribuicao_matricial.py: 36
  demo/teste_demo.py: 358
  demo/teste_diagnostico.py: 41
  demo/teste_demo_distribuicao.py: 99
  demo/teste_explorar_barra_de_menus.py: 38
total_scripts: 8
falhas: 0
```

## 28. Suite final (9 scripts, apos a implementacao)

```yaml
comandos: PYTHONDONTWRITEBYTECODE=1 python <script>
contagem_por_script:
  tela/teste_loader.py: 348
  tela/teste_modelo.py: 186
  tela/teste_renderizador.py: 1223
  tela/teste_distribuicao_matricial.py: 36
  demo/teste_demo.py: 363
  demo/teste_diagnostico.py: 48
  demo/teste_demo_distribuicao.py: 109
  demo/teste_explorar_barra_de_menus.py: 38
  demo/teste_demo_console.py: 72   # novo script canonico
total_verificacoes: 2423
total_scripts: 9
falhas: 0
baseline_inicial: 8 scripts, 0 falhas
baseline_final: 9 scripts, 0 falhas
git_diff_check: sem erros
```

Alteracao do conjunto canonico: adicao do novo script
`demo/teste_demo_console.py` (previsto pelo handoff §20.2). Os 8 scripts
anteriores permanecem verdes.

## 29. Demonstracao tecnica

Ponto de entrada real `python demo/demo.py <cenario>` (fora de TTY, entrada
`s`), confirmado tecnicamente:

| Cenario | Tela | Identidade | Apresentacao | Placeholder |
|---|---|---|---|---|
| h0036_console_hierarquia | H0036 HIERARQUIA | `H-0036` presente | hierarquia | ausente |
| h0036_console_tabela | H0036 TABELA | `tabela H-0036` presente | tabela | ausente |
| h0036_console_conjuntos | H0036 CONJUNTOS | `Parametros`/`H-0036` presente | conjuntos_campos | ausente |
| h0035_console_com | H0035 CONSOLE COM | `P01 linha`..`P12 linha` (grade DM) | hierarquia (DM) | ausente |
| h0035_console_sem | H0035 CONSOLE SEM | `Linha alfa`/`Linha bravo` | hierarquia | ausente |
| (sem arg) demo | ORQUESTRADOR | sem `H-0036` | — | `(console)` presente |

Troca para cenario sem conteudo (apos abrir um com conteudo) nao vaza a
identidade `H-0036`. Esta execucao tecnica NAO substitui a observacao visual do
usuario em TTY real.

## 30. Validacao manual

```
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

Roteiro em linguagem comum (o executor preparou o ambiente; a validacao visual e
exclusiva do usuario — nao ha declaracao de aprovacao visual, legibilidade,
redimensionamento ou quadro minimo):

1. No terminal, rode `python demo/demo.py h0036_console_hierarquia`.
   Esperado: a janela abre e o console mostra a hierarquia numerada; a linha com
   o texto `H-0036` aparece no console.
2. Confirme que o texto com `H-0036` esta visivel na area do console.
3. (Fora do TTY) abra `config/telas/demo/h0036_console_hierarquia.json` e
   confirme que ele NAO contem o texto `H-0036` (o conteudo esta so no externo).
4. Maximize a janela do terminal. Esperado: a interface se reorganiza e o
   conteudo continua legivel.
5. Restaure o tamanho normal. Esperado: reorganiza; conteudo visivel.
6. Reduza a largura. Esperado: conteudo visivel com truncamento/ajuste.
7. Reduza a altura. Esperado: conteudo visivel com ajuste.
8. Redimensione livremente. Esperado: conteudo visivel em tamanhos razoaveis.
9. Reduza abaixo do quadro minimo (largura < 10 ou altura < 6). Esperado:
   aparece o quadro minimo canonico; a sessao nao quebra.
10. Aumente de volta ao tamanho normal. Esperado: o conteudo da fixture retorna
    sem residuos do quadro minimo.
11. Feche (tecla `Esc`) e rode `python demo/demo.py` (sem argumento). Abra a tela
    raiz. Esperado: o console mostra o placeholder `(console)`.
12. Confirme que o texto `H-0036` NAO aparece nessa tela sem conteudo.
    Esperado: nenhum vazamento do cenario anterior.

Para as tres apresentacoes, use tambem
`python demo/demo.py h0036_console_tabela` e
`python demo/demo.py h0036_console_conjuntos`.

## 31. Excecoes operacionais solicitadas e autorizadas

Nenhuma. Nenhum arquivo fora da lista nominal foi necessario; nenhum pedido de
autorizacao foi feito.

## 32. Estado Git final

```
branch: master
head: fb9e5be   (inalterado; nenhum commit)
stage: vazio    (nenhum git add)
alterados (12) + criados (9 + este relatorio) = exatamente a lista autorizada
demo.json: nao alterado (ver §7)
```

Verificacao de escopo: `git status --short`, `git diff --name-only` e
`git ls-files --others --exclude-standard` mostram apenas arquivos autorizados;
os artefatos documentais anteriores (ADR-0026/0027, H-0036, RELATORIO_*,
NOMENCLATURA, INDICE_ADR, contratos) permaneceram intactos; nenhum arquivo
inesperado foi modificado.

## 33. `git diff --check`

Sem erros de whitespace. Nenhum `__pycache__`/`*.pyc` gerado (comandos com
`PYTHONDONTWRITEBYTECODE=1`; nenhum cache produzido por esta etapa).

## 34. Limitacoes e itens futuros

- Script produtor ligado ao Pipeline: NAO implementado (fora de escopo).
- Protocolo definitivo com o Pipeline, transporte, argumentos, codigos de saida,
  timeout, autenticacao, cache, atualizacao automatica, persistencia,
  versionamento: NAO implementados (deferidos).
- `tipo: "matriz"` no fornecimento externo: NAO incluido.
- Navegacao interativa, expansao/recolhimento, paginacao interativa do conteudo
  multinivel: NAO implementados.
- Diretorio global definitivo de runtime: NAO criado (fixtures permanecem em
  `config/telas/demo/` com sufixo `_conteudo.json`).
- Acesso aos cenarios H-0036 pelo `demo.py` e por argumento de tela inicial
  (precedente `demo_distribuicao.py`); o launcher de `demo.json` nao foi alterado
  (ver §7). A validacao visual em TTY permanece pendente do usuario (§30).

## 35. Conclusao factual

O escopo nominal do H-0036 foi implementado: loader com carregamento e 20
validacoes do documento externo; modelo com representacao semantica de origens
separadas; renderizador com as tres apresentacoes, tres tipos de nivel e
designadores concretos; catalogo de associacao no `demo.py` com carregamento
separado dos dois documentos; separacao dos dois JSONs do H-0035 e criacao das
fixtures e telas estruturais nominais; testes focais, de integracao, do catalogo
e de regressao. A suite canonica de 9 scripts esta verde (2423 verificacoes, 0
falhas), `git diff --check` sem erros, sem caches e sem commit/stage. A
validacao visual em TTY permanece pendente do usuario.

Este relatorio nao aprova a propria implementacao.

Resultado: `IMPLEMENTATION_COMPLETED`. Proxima categoria: `QA_IMPLEMENTACAO`.
