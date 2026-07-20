---
name: IMP-0037-apresentacao-multinivel-console-alternancia-verbosa
description: Relatorio factual da implementacao do H-0037 — apresentacao multinivel no console com politica de modo por tela (campos D23, 15 validacoes V-01 a V-15, quatro fixtures, tecla V exclusiva para telas alternaveis)
metadata:
  type: relatorio_implementacao
  id: IMP-0037
  handoff: H-0037
  data: "2026-07-19"
  etapa: IMPLEMENTAR
  status_literal: IMPLEMENTATION_PATCHED
  patch_manual_pos_validacao: H0037-MANUAL-001/002/003
---

# IMP-0037 — Implementacao do H-0037

> Relatorio factual da etapa `IMPLEMENTAR`. Nao aprova a propria implementacao,
> nao declara validacao visual e nao inicia QA, stage, commit ou novo ciclo.

## 1. Identificacao

| Campo | Valor |
|---|---|
| Relatorio | IMP-0037 |
| Handoff | H-0037 (QA final `H1_HANDOFF_APPROVED`, implementacao AUTORIZADA) |
| Etapa executada | IMPLEMENTAR |
| Data | 2026-07-19 |
| Branch | master |
| HEAD inicial | f6982d0 |
| Commit novo | NAO realizado |
| Stage | vazio |

## 2. Autoridades

Lidas integralmente antes de qualquer alteracao (ordem de autoridade: contratos
ativos > ADR-0028 > ADR-0027 > ADR-0026 > H-0037 aprovado > relatorios como evidencia):

- `docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md`
- `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md`
- `docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md`
- `docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md`
- `docs/contratos/contrato_tela_json.md`, `contrato_console.md`,
  `contrato_json_console.md`, `contrato_barra_de_menus.md`,
  `contrato_composicao_corpo.md`
- `docs/NOMENCLATURA.md`
- `docs/relatorios/RELATORIO_QA_H-0037_HANDOFF.md`
- `docs/relatorios/RELATORIO_QA_ADR-0028.md`,
  `RELATORIO_QA_POS_PATCH_ADR-0028.md`,
  `RELATORIO_APLICACAO_ADR-0028.md`,
  `RELATORIO_QA_APLICACAO_ADR-0028.md`,
  `RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0028.md`,
  `RELATORIO_QA_ADR-0028_REVISAO_MODOS_POR_TELA.md`,
  `RELATORIO_QA_POS_PATCH_ADR-0028_REVISAO_MODOS_POR_TELA.md`,
  `RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md`,
  `RELATORIO_QA_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md`,
  `RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md`
- Preservacao dos ciclos anteriores: IMP-0036, H-0036, IMP-0035.

Os campos D23 (`politica_modo`, `modo_inicial`), as 15 validacoes V-01 a V-15,
as quatro politicas de modo e os valores canonicos foram tratados como requisitos
FECHADOS (ADR-0028 D23; `contrato_json_console.md` §12; `contrato_console.md`
§21). Nao foram decididos pela implementacao.

## 3. Estado Git inicial

```
branch: master
head: f6982d0
descricao: docs: corrige whitespace do fechamento H-0036
git diff --check: sem erros
```

O workspace ja continha artefatos documentais acumulados das ADR-0026, ADR-0027,
ADR-0028, H-0036 e H-0037 (arquivos `docs/adr/ADR-002{6,7,8}-*`,
`docs/handoff/H-0037-*`, `docs/relatorios/RELATORIO_*ADR-0028*`,
`docs/relatorios/RELATORIO_*H-0037*` e modificacoes em `docs/NOMENCLATURA.md`,
`docs/adr/INDICE_ADR.md`, `docs/contratos/contrato_*`).
**Esses documentos NAO foram atribuidos a esta implementacao, NAO foram
alterados e NAO foram restaurados.**

## 4. Lista nominal autorizada

**Alterar (12 autorizados):**

1. `tela/loader.py`
2. `tela/modelo.py`
3. `tela/renderizador.py`
4. `tela/teste_loader.py`
5. `tela/teste_modelo.py`
6. `tela/teste_renderizador.py`
7. `demo/demo.py`
8. `demo/teste_demo.py`
9. `demo/teste_diagnostico.py`
10. `demo/teste_demo_console.py`
11. `demo/teste_explorar_barra_de_menus.py`
12. `config/telas/demo/demo.json`

**Criar (9 autorizados):**

1. `config/telas/demo/h0037_console_nao_verboso.json`
2. `config/telas/demo/h0037_console_verboso_dois_niveis.json`
3. `config/telas/demo/h0037_console_alternavel_tres_niveis.json`
4. `config/telas/demo/h0037_console_tabela_alternavel.json`
5. `config/telas/demo/h0037_dois_niveis_conteudo.json`
6. `config/telas/demo/h0037_tres_niveis_conteudo.json`
7. `config/telas/demo/h0037_tabela_conteudo.json`
8. `demo/teste_demo_console_modos.py`
9. `docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md`

## 5. Arquivos realmente alterados (11)

`tela/loader.py`, `tela/modelo.py`, `tela/renderizador.py`,
`tela/teste_loader.py`, `tela/teste_modelo.py`, `tela/teste_renderizador.py`,
`demo/demo.py`, `demo/teste_demo.py`, `demo/teste_demo_console.py`,
`demo/teste_diagnostico.py`, `config/telas/demo/demo.json`.

## 6. Arquivos autorizados NAO alterados e justificativas

- `demo/teste_explorar_barra_de_menus.py` — nao alterado.

  Os testes existentes do explorar_barra_de_menus nao tocam politica de modo
  nem contam itens do launcher; permaneceram validos sem modificacao.

## 7. Arquivos realmente criados (8 + este relatorio)

`config/telas/demo/h0037_console_nao_verboso.json`,
`config/telas/demo/h0037_console_verboso_dois_niveis.json`,
`config/telas/demo/h0037_console_alternavel_tres_niveis.json`,
`config/telas/demo/h0037_console_tabela_alternavel.json`,
`config/telas/demo/h0037_dois_niveis_conteudo.json`,
`config/telas/demo/h0037_tres_niveis_conteudo.json`,
`config/telas/demo/h0037_tabela_conteudo.json`,
`demo/teste_demo_console_modos.py`,
e este relatorio.

## 8. Baseline medido antes das alteracoes (H-0036)

| Script | Verificacoes | Falhas |
|---|---|---|
| `tela/teste_loader.py` | 334 | 0 |
| `tela/teste_modelo.py` | 178 | 0 |
| `tela/teste_renderizador.py` | 1223 | 0 |
| `tela/teste_distribuicao_matricial.py` | 36 | 0 |
| `demo/teste_demo.py` | 344 | 0 |
| `demo/teste_diagnostico.py` | 47 | 0 |
| `demo/teste_demo_distribuicao.py` | 109 | 0 |
| `demo/teste_explorar_barra_de_menus.py` | 38 | 0 |
| `demo/teste_demo_console.py` | 116 | 0 |
| **Total** | **2425** | **0** |

Baseline confirmado por `git stash` / `git stash pop` antes e depois das
alteracoes para isolar regressoes introduzidas pelo H-0037.

## 9. Implementacao por camada

### 9.1 `tela/loader.py`

- Implementada validacao D23: `_validar_d23_console(elemento)` aceita o
  elemento `console` do corpo e valida os campos `politica_modo` e
  `modo_inicial` conforme a matriz de validade de 10 entradas (ADR-0028 D23).
- Integrada ao fluxo de `carregar_tela`: chamada apos a construcao do elemento
  console quando o JSON estrutural contiver `formato.excesso.politica_modo`.
- Integradas 15 validacoes V-01 a V-15 na funcao `validar_conteudo_externo`
  (ja existente, expandida).

### 9.2 `tela/modelo.py`

- `ElementoCorpo` passou a transportar os atributos `politica_modo` e
  `modo_inicial` lidos do JSON estrutural via `formato.excesso`.
- `construir_modelo` propaga esses atributos ao construir o elemento console.

### 9.3 `tela/renderizador.py`

- `renderizar_tela` passou a aceitar `estado` com a chave `modo_verboso`.
- Implementadas funcoes `_verboso_efetivo(estado, modelo)` e
  `_modo_verboso_de_modelo(modelo)` para resolver verbosidade corrente.
- O renderizador usa `modo_verboso` para escolher a quantidade de linhas
  fisicas por dado na renderizacao do console multinivel.

### 9.4 `demo/demo.py`

- Quatro entradas adicionadas ao catalogo `_CATALOGO_CONTEUDO_EXTERNO`:
  ```python
  "h0037_console_nao_verboso":         "h0037_dois_niveis_conteudo",
  "h0037_console_verboso_dois_niveis": "h0037_dois_niveis_conteudo",
  "h0037_console_alternavel_tres_niveis": "h0037_tres_niveis_conteudo",
  "h0037_console_tabela_alternavel":   "h0037_tabela_conteudo",
  ```
- Implementadas `_verboso_efetivo(estado, modelo)` e
  `_modo_verboso_de_modelo(modelo)` com guarda `try/except AttributeError`
  para compatibilidade com mocks de testes.
- Tecla `V` passa a alternar `estado["modo_verboso"]` somente em telas com
  `politica_modo: "alternavel"`. Em telas fixas (`somente_verboso`,
  `somente_nao_verboso`) a tecla `V` nao produz efeito.
- Quatro itens adicionados ao launcher `demo.json` (chips 6 a 9).

## 10. Campos D23 (`politica_modo`, `modo_inicial`)

| Campo | Caminho JSON | Arquivo | Validacao |
|---|---|---|---|
| `politica_modo` | `formato.excesso.politica_modo` | JSON estrutural h0037 | `_validar_d23_console` em `tela/loader.py` |
| `modo_inicial` | `formato.excesso.modo_inicial` | JSON estrutural h0037 | `_validar_d23_console` em `tela/loader.py` |

Conteudo externo (`h0037_*_conteudo.json`) **nao contem** `politica_modo` nem
`modo_inicial`. Ausencia verificada pelos testes de identidade semantica em
`demo/teste_demo_console.py`.

## 11. Matriz de validade implementada (10 entradas, ADR-0028 D23)

| `politica_modo` | `modo_inicial` | Valido | Teste de rejeicao |
|---|---|---|---|
| ausente (tela legada H-0036) | ausente | sim | — (aceito) |
| `somente_verboso` | ausente | sim | — (aceito) |
| `somente_nao_verboso` | ausente | sim | — (aceito) |
| `alternavel` | `"verboso"` | sim | — (aceito) |
| `alternavel` | `"nao_verboso"` | sim | — (aceito) |
| `somente_verboso` | presente (qualquer) | nao | `teste_d23_estrutural` |
| `somente_nao_verboso` | presente (qualquer) | nao | `teste_d23_estrutural` |
| `alternavel` | ausente | nao | `teste_d23_estrutural` |
| `alternavel` | valor invalido | nao | `teste_d23_estrutural` |
| valor invalido | qualquer | nao | `teste_d23_estrutural` |

Testes em `tela/teste_loader.py` (`teste_d23_estrutural`) e
`demo/teste_demo_console_modos.py` (`teste_transporte_politica_modo`).

## 12. Campo antigo `excesso.modo` (legado)

O campo `excesso.modo` (legado, usado nas telas H-0036 como `"nao_verboso"`)
NAO e usado nos quatro cenarios H-0037. As telas H-0037 usam exclusivamente
`politica_modo` e `modo_inicial`. As telas H-0036 existentes nao foram
migradas; o campo antigo e ignorado pelo processamento de verbosidade nas
telas H-0037 (fallback `False` quando `politica_modo` esta ausente).

## 13. Quatro telas com politicas distintas

| Cenario | `politica_modo` | `modo_inicial` | Chip `[V]` |
|---|---|---|---|
| `h0037_console_nao_verboso` | `somente_nao_verboso` | ausente | nao |
| `h0037_console_verboso_dois_niveis` | `somente_verboso` | ausente | nao |
| `h0037_console_alternavel_tres_niveis` | `alternavel` | `nao_verboso` | sim |
| `h0037_console_tabela_alternavel` | `alternavel` | `verboso` | sim |

## 14. Tres documentos externos de conteudo

| Documento | Apresentacao | Usado por |
|---|---|---|
| `h0037_dois_niveis_conteudo.json` | `hierarquia` | cenarios 1 e 2 (compartilhado) |
| `h0037_tres_niveis_conteudo.json` | `hierarquia` | cenario 3 |
| `h0037_tabela_conteudo.json` | `tabela` | cenario 4 |

## 15. Conteudo compartilhado entre cenarios 1 e 2

Os cenarios `h0037_console_nao_verboso` e `h0037_console_verboso_dois_niveis`
compartilham o mesmo documento externo (`h0037_dois_niveis_conteudo.json`).
As politicas distintas (`somente_nao_verboso` vs `somente_verboso`) produzem
renderizacoes diferentes do mesmo conteudo. Verificado em
`demo/teste_demo_console_modos.py` (`teste_conteudo_compartilhado_cenarios_1_e_2`
e `teste_renderizacao_modo_nao_verboso_vs_verboso`).

## 16. Barra de menus — chip `[V] Verboso` apenas nas alternaveis

O chip `[V] Verboso` esta declarado nos JSONs estruturais dos cenarios 3 e 4
(`h0037_console_alternavel_tres_niveis.json`,
`h0037_console_tabela_alternavel.json`) e AUSENTE nos cenarios 1 e 2.
Verificado em `demo/teste_demo_console_modos.py` (`teste_tecla_v_ausente_nas_fixas`).

## 17. Tecla `V` — exclusiva das alternaveis

Em `demo/demo.py`, a captura da tecla `V` esta condicionada a
`politica_modo == "alternavel"`. Em telas fixas, a tecla `V` e ignorada.
Verificado em `demo/teste_demo_console_modos.py` (`teste_alternancia_v_nas_alternaveis`,
`teste_tecla_v_ausente_nas_fixas`).

## 18. Testes de rejeicao D23

Mapeamento de cada caso invalido ao teste correspondente em
`tela/teste_loader.py` (`teste_d23_estrutural`):

| Caso invalido | Teste |
|---|---|
| `politica_modo` com valor desconhecido | `D23: politica_modo invalida rejeitada` |
| `modo_inicial` presente sem `politica_modo` | `D23: modo_inicial sem politica_modo rejeitado` |
| `somente_nao_verboso` com `modo_inicial` | `D23: somente_nao_verboso com modo_inicial rejeitado` |
| `somente_verboso` com `modo_inicial` | `D23: somente_verboso com modo_inicial rejeitado` |
| `alternavel` sem `modo_inicial` | `D23: alternavel sem modo_inicial rejeitado` |
| `alternavel` com `modo_inicial` invalido | `D23: alternavel com modo_inicial invalido rejeitado` |

## 19. Testes de rejeicao V-01 a V-15

Mapeamento normativo (conforme `contrato_json_console.md` §13.9 / ADR-0028 §33)
ao arquivo `tela/teste_loader.py` (funcao `teste_conteudo_externo_h0036`):

| Validacao | Condicao normativa | Testes de rejeicao |
|---|---|---|
| V-01 | `apresentacao == "tabela"` sem `cabecalho` ou com `cabecalho: []` | `V-01: tabela sem cabecalho rejeitada`; `V-01: tabela com cabecalho vazio rejeitada` |
| V-02 | Referencia a filho inexistente (nivel declara `filhos` com id ausente) | `V-02: referencia a filho inexistente rejeitada` |
| V-03 | Documento com multiplas raizes quando `formato` declara `filhos` | `V-03: multiplas raizes no documento rejeitadas` |
| V-04 | Folha (`conteudo` ou `nome_valor`) declara `filhos` (inclusive `[]`) | `V-04: folha com filhos rejeitada`; `V-04: folha com filhos vazio rejeitada` |
| V-05 | Container com `filhos` vazio — comportamento aceito documentado | `V-05: container com filhos vazio aceito` |
| V-06 | Nivel `nome_valor` sem campo `nome` ou `valor` nos dados | `V-06: nome_valor sem campo valor rejeitado` |
| V-07 | Medida negativa em `formato.espacamento` | `V-07: medida negativa rejeitada` |
| V-08 | `largura_maxima < largura_minima` em coluna de tabela | `V-08: largura maxima menor que minima rejeitada` |
| V-09 | `formato.excesso.linhas_nao_verboso > 1` | `V-09: linhas_nao_verboso maior que 1 rejeitada` |
| V-10 | `formato.excesso.verboso` declarado sem `continuacao` | `V-10: verboso sem continuacao rejeitado` |
| V-11 | `formato.alinhamento.tipo == "justificado"` sem `escopo` | `V-11: justificado sem escopo rejeitado` |
| V-12 | No raiz (sem ancestral) com nivel de designador `decimal_composto` | `V-12: raiz com decimal_composto rejeitada` |
| V-13 | Dado refere nivel inexistente no `formato.niveis` | `V-13: nivel inexistente rejeitado` |
| V-14 | Coluna de tabela sem `nivel` nem `campo` | `V-14: coluna tabela sem nivel nem campo rejeitada` |
| V-15 | `politica_modo`, `modo_inicial` ou `modo` em `formato.excesso` do conteudo externo; `politica_modo`/`modo_inicial` na raiz do documento | `V-15: politica_modo em excesso rejeitada`; `V-15: modo legado em excesso rejeitado`; `V-15: politica_modo na raiz rejeitada` |

## 20. Testes comportamentais — telas fixas (cenarios 1 e 2)

Em `demo/teste_demo_console_modos.py`:

- `teste_transporte_politica_modo`: politica carregada corretamente do JSON estrutural.
- `teste_modo_verboso_inicial`: modo determinado pela politica (fixas → False para nao_verboso, True para verboso).
- `teste_tecla_v_ausente_nas_fixas`: chip `[V]` ausente; tecla `V` nao altera a apresentacao.

## 21. Testes comportamentais — telas alternaveis (cenarios 3 e 4)

Em `demo/teste_demo_console_modos.py`:

- `teste_transporte_politica_modo`: ID do JSON estrutural e catalogo verificados.
- `teste_modo_verboso_inicial`: modo inicial lido da politica (`alternavel + nao_verboso` → False; `alternavel + verboso` → True).
- `teste_verboso_efetivo_por_politica`: `_verboso_efetivo` retorna valor do estado para alternavel.
- `teste_alternancia_v_nas_alternaveis`: `V` altera o modo; segunda ativacao restaura o modo anterior.
- `teste_isolamento_verbosidade_entre_telas`: alternancia nao vaza entre cenarios.
- `teste_renderizacao_modo_nao_verboso_vs_verboso`: saida difere entre modos.
- `teste_todos_cenarios_renderizam_sem_excecao`: todos os quatro cenarios rendenizam sem excecao.

## 22. Suite canonica — resultado final

Comandos executados a partir da raiz do projeto:

```bash
PYTHONDONTWRITEBYTECODE=1 python tela/teste_loader.py
PYTHONDONTWRITEBYTECODE=1 python tela/teste_modelo.py
PYTHONDONTWRITEBYTECODE=1 python tela/teste_renderizador.py
PYTHONDONTWRITEBYTECODE=1 python tela/teste_distribuicao_matricial.py
PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo.py
PYTHONDONTWRITEBYTECODE=1 python demo/teste_diagnostico.py
PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo_distribuicao.py
PYTHONDONTWRITEBYTECODE=1 python demo/teste_explorar_barra_de_menus.py
PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo_console.py
PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo_console_modos.py
```

| Script | Verificacoes | Falhas |
|---|---|---|
| `tela/teste_loader.py` | 396 | 0 |
| `tela/teste_modelo.py` | 186 | 0 |
| `tela/teste_renderizador.py` | 1223 | 0 |
| `tela/teste_distribuicao_matricial.py` | 36 | 0 |
| `demo/teste_demo.py` | 363 | 0 |
| `demo/teste_diagnostico.py` | 48 | 0 |
| `demo/teste_demo_distribuicao.py` | 109 | 0 |
| `demo/teste_explorar_barra_de_menus.py` | 38 | 0 |
| `demo/teste_demo_console.py` | 116 | 0 |
| `demo/teste_demo_console_modos.py` | 63 | 0 |
| **Total** | **2578** | **0** |

10 scripts, 2578 verificacoes (acima do minimo de 2423 exigido), 0 falhas.
Resultado pos-patch: +9 verificacoes (4 em `teste_loader.py`, 5 em `teste_demo_console_modos.py`).

## 23. Identidade semantica verificavel

| Cenario | String de identidade |
|---|---|
| `h0037_console_nao_verboso` | `"H-0037 conteudo_dois_niveis"` |
| `h0037_console_verboso_dois_niveis` | `"H-0037 conteudo_dois_niveis"` |
| `h0037_console_alternavel_tres_niveis` | `"H-0037 alternavel_tres_niveis"` |
| `h0037_console_tabela_alternavel` | `"H-0037 tabela_alternavel"` |

Os cenarios 1 e 2 compartilham o mesmo documento externo
(`h0037_dois_niveis_conteudo.json`) com identidade neutra unica
`"H-0037 conteudo_dois_niveis"`. A politica de modo pertence a tela, nao ao
conteudo. Cada string aparece no documento externo e NAO no JSON estrutural.
Verificado em `demo/teste_demo_console.py` (`teste_carregamento_separado_por_cenario`).

## 24. Regressao H-0036

- Todos os 5 cenarios H-0036 e H-0035 passam no smoke test de
  `demo/teste_demo_console.py` (sem placeholder, sem mistura).
- As 20 validacoes ADR-0027 continuam ativas (expandidas pelas 15 validacoes V-01-V-15).
- Nenhuma fixture ou comportamento anterior foi alterado.
- O launcher expandido (7 → 11 itens) nao alterou o comportamento dos cenarios H-0036
  nem H-0035; apenas adicionou chips 6 a 9.

## 25. Redimensionamento automatizavel

- Com 11 itens no launcher a w=80: matriz 4x3 (3 linhas), testada em
  `tela/teste_renderizador.py` (`test_demo_matriz_109_e_80`).
- Com 11 itens a w=110: matriz 6x2 (2 linhas), testada em
  `test_demo_fila_110`.
- Coluna minima: content_w=19 (max item_w=15 "Nao Verboso" / "Tab Altern."),
  area>=22; testado em `test_demo_fronteira_global_suplementar`.
- Fila: fila_content_w_min=170, area>=173; nao testado no demo real (terminal
  demasiado largo para ambientes convencionais).
- PTY: SIGWINCH testado com 40x32 (subiu de 30 para acomodar 11 itens a w=40).

## 26. Pendencia de TTY real

```
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

A validacao manual em TTY real (roteiro em §24 do handoff) nao foi executada
pelo implementador e aguarda o usuario. O resultado sera registrado em
`docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0037.md`.

## 27. Excecoes autorizadas

Nenhuma excecao operacional foi necessaria. Todos os arquivos alterados estavam
nominalmente listados em §18 do handoff.

## 28. Limitacoes conhecidas

- A fila do launcher real exige area>=173 (terminal muito largo); os testes
  do demo real testam apenas a matriz (w=80 e w=110).

As limitacoes anteriores de V-01 (cabecalho vazio) e V-04 (filhos vazio)
foram corrigidas no PATCH_IMPLEMENTACAO (veja §30); a restricao adicional de
V-01 (coluna semanticamente valida) e o fechamento do bypass D23 foram
tratados no segundo patch pos-QA (veja §31).

## 29. Higiene

```
git diff --check: sem erros
```

Sem trailing whitespace, sem conflitos de merge, sem arquivos fora da lista
nominal.

## 30. PATCH_IMPLEMENTACAO — correcoes pos-QA

Aplicado com base em `docs/relatorios/RELATORIO_QA_H-0037_IMPLEMENTACAO.md`
(status `IMPLEMENTATION_PATCH_REQUIRED`). Nenhum commit, stage ou nova etapa
foi iniciada.

### H0037-IMPL-QA-001: modo inicial ausente na abertura por argv

**Problema**: `demo/demo.py` nao aplicava `_modo_verboso_de_modelo(modelo)`
antes da primeira renderizacao quando a tela era aberta por argumento de linha
de comando. O cenario 4 (`h0037_console_tabela_alternavel`, `modo_inicial:
verboso`) abria em modo nao-verboso na primeira frame.

**Correcao**: linha inserida em `demo/demo.py` apos o carregamento do modelo
por argv, antes do bloco TTY:
```python
estado = dict(estado, modo_verboso=_modo_verboso_de_modelo(modelo))
```

**Teste adicionado**: `teste_abertura_por_argv` em
`demo/teste_demo_console_modos.py` (5 verificacoes).

### H0037-IMPL-QA-002: D23 e V-01 a V-15 nao conformes ao normativo

**Problema**: multiplos desvios nos rotulos e nas condicoes V-01 a V-15 versus
a tabela normativa (`contrato_json_console.md` §13.9 / ADR-0028 §33):

1. **D23**: `_validar_d23_console` rejeitava qualquer tile sem `politica_modo`,
   inclusive tiles legados sem bloco `formato.excesso`. A primeira tentativa de
   correcao usou o parametro `excesso_declarado` para isentar tiles sem
   `formato.excesso`. **ESSA ABORDAGEM PERMITIA BYPASS D23** (ver §31): uma tela
   nova podia omitir o bloco inteiro para evitar a obrigacao. A correcao final
   (§31) substitui essa logica por determinacao estrutural de escopo.
2. **V-01**: cabecalho vazio (`[]`) era aceito; passou a ser rejeitado. Porem a
   correcao ainda aceitava cabecalho sem coluna semanticamente valida (ver §31).
3. **V-04**: `filhos: []` em no folha era aceito (`no.get("filhos")` avaliava
   como falsy); passou a ser rejeitado via verificacao `"filhos" in no`.
4. **V-02 a V-15**: rotulos e semanticas alinhados ao normativo (tabela em §19).

**Arquivos alterados no patch**: `tela/loader.py`, `tela/teste_loader.py`,
`demo/demo.py`, `demo/teste_demo_console_modos.py`, `demo/teste_demo_console.py`,
`config/telas/demo/h0037_dois_niveis_conteudo.json`.

---

## 31. Segundo patch pos-QA — correcao do bypass D23 e V-01 (QAPP-001, QAPP-002)

Aplicado com base em `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0037_IMPLEMENTACAO.md`
(status `IMPLEMENTATION_PATCH_REQUIRED`). Nenhum commit, stage ou nova etapa
foi iniciada.

```yaml
qa_de_origem: docs/relatorios/RELATORIO_QA_POS_PATCH_H-0037_IMPLEMENTACAO.md
status_de_origem: IMPLEMENTATION_PATCH_REQUIRED

achados_tratados:
  - H0037-IMPL-QAPP-001
  - H0037-IMPL-QAPP-002
```

### 31.1 H0037-IMPL-QAPP-001 — impedir bypass D23 por ausencia de formato.excesso

**Causa do bypass**: a primeira correcao (§30) tratava a ausencia do bloco
`formato.excesso` como isencao da politica D23 (`excesso_declarado=False` em
`carregar_tela` fazia `_validar_d23_console` retornar sem erro). Isso permitia
que uma tela nova de console consumidora de conteudo multinivel contornasse a
obrigacao de declarar `politica_modo` simplesmente omitindo o bloco inteiro —
contrariando ADR-0028 D23 e `contrato_json_console.md` §13.13.3 (ausencia de
politica em tela nova/revisada e invalida; nao existe default implicito).

**Nova regra de determinacao do escopo D23**: o escopo D23 agora e determinado
estruturalmente por `_console_em_escopo_d23(elemento, id_tela)`,
independentemente da presenca de `formato.excesso`:

- **Console de envelope pre-ADR-0028** (declara `itens`, `origem_dados` ou
  qualquer campo de envelope: `politica_composicao`, `politica_navegacao`,
  `politica_selecao`, `politica_paginacao`, `politica_exibicao`) esta FORA do
  escopo D23. Esses elementos seguem o envelope classico de
  `contrato_json_console.md` §4 (declaracao direta de itens), nao consomem
  conteudo multinivel externo e preservam o comportamento contratual anterior.
  A deteccao e por campos do elemento, nao por id da tela, valendo para
  qualquer tela de envelope futura.
- **Console consumidor de conteudo multinivel** (sem campos de envelope) esta
  DENTRO do escopo D23, salvo tela nominalmente legada reconhecida em
  `_TELAS_LEGADAS_D23`.

`_validar_d23_console` agora recebe `em_escopo` (computado pelo chamador) em
vez de `excesso_declarado`. Fora do escopo, preserva o comportamento anterior
sem exigir politica. Em escopo, telas legadas nominais podem omitir
`politica_modo`; telas novas/revisadas devem declara-la obrigatoriamente,
mesmo se o bloco `formato.excesso` estiver ausente.

**Forma de preservacao nominal do H-0036**: o inventario `_TELAS_LEGADAS_D23`
e estritamente nominal e historico. Inclui os tres cenarios canonicos do
H-0036 (`h0036_console_hierarquia`, `h0036_console_tabela`,
`h0036_console_conjuntos`) e os dois cenarios de console do H-0035 adaptados
em H-0036 (`h0035_console_com`, `h0035_console_sem`) — ambos pre-D23,
consumidores de conteudo multinivel externo, sem politica declarada. Essas
telas permanecem validas por compatibilidade (ADR-0028 §13.13.8; §39; §43
item 3). O inventario nao vira regra generica para telas futuras.

**Prova de que omitir `formato.excesso` nao contorna a politica**: coberto
nominalmente pelos testes D23-01 a D23-07 em `tela/teste_loader.py`. Em
especial:

- D23-01: nova tela consumidora com `formato.excesso` mas sem `politica_modo`
  → REJEITADA.
- D23-02: nova tela consumidora sem todo o bloco `formato.excesso` → REJEITADA
  (o bypass anterior esta fechado).
- D23-03: tela equivalente com ID alternativo fora do inventario, sem bloco
  → REJEITADA (impede correcao baseada apenas nos quatro IDs H-0037).
- D23-04: tela H-0036 legada sem campos D23 → ACEITA (3 cenarios nominais).
- D23-05: tela nova com apenas `formato.excesso.modo` legado, sem
  `politica_modo` → REJEITADA (campo legado nao supre a politica).
- D23-06: console de envelope pre-ADR-0028 (`itens`/`origem_dados`) →
  PRESERVA_COMPORTAMENTO_CONTRATUAL_ANTERIOR.
- D23-07: tela nova consumidora com politica valida e matriz correta → ACEITA.

### 31.2 H0037-IMPL-QAPP-002 — V-01 exige coluna semanticamente valida

**Causa do defeito**: a correcao anterior (§30) rejeitava cabecalho ausente,
nulo e lista vazia, mas ainda aceitava qualquer lista nao vazia
(`len(cabecalho) > 0`). Um cabecalho `[{}]`, `[42]`, `[null]` ou
`[{"desconhecido": "x"}]` — sem nenhuma coluna semanticamente valida — era
aceito indevidamente.

**Definicao aplicada para coluna semanticamente valida**: uma entrada de
`formato.tabela.cabecalho` e estruturalmente reconhecivel como coluna quando
(`_coluna_reconhecivel` em `tela/loader.py`):

- e uma string nao vazia (cabecalho simples, como `["Grupo", "Valor"]`); ou
- e um objeto declarando ao menos um dos campos minimos da forma de coluna:
  `titulo` (rotulo), `nivel` ou `campo` (origem — verificados por V-14).

Entradas nulas, tipos incorretos (numero, booleano), objetos vazios e objetos
sem nenhum dos campos minimos NAO sao colunas reconheciveis. A validacao V-01
agora exige `any(_coluna_reconhecivel(c) for c in cabecalho)` — ao menos uma
coluna reconhecivel.

**Separacao entre V-01 e V-14**:

- **V-01** cobre a ausencia total de coluna reconhecivel no cabecalho (lista
  vazia, entradas nulas, tipos incorretos, objetos sem forma de coluna).
- **V-14** cobre a coluna reconhecivel (tem forma de coluna, ex.
  `{"titulo": "..."}`) que carece de origem (`nivel`/`campo`).

Uma mesma entrada nao representa simultaneamente V-01 e V-14: `{"titulo": "X"}`
e reconhecivel como coluna (satisfaz V-01) e pode ser rejeitada por V-14 se
faltarem `nivel`/`campo`. Ja `{}` nao e reconhecivel (rejeitada por V-01) e
nao chega a ser candidata a V-14.

### 31.3 Testes adicionados

Em `tela/teste_loader.py`:

- **D23-01 a D23-07**: 7 cenarios nominais de bypass/isencao D23 via
  `carregar_tela` em diretorio temporario, mais 3 verificacoes diretas de
  `_console_em_escopo_d23`.
- **V-01 casos 1 a 10**: 13 verificacoes cobrindo propriedade ausente, valor
  nulo, lista vazia, item nulo, tipos incorretos (int/float/bool), objeto
  vazio, objeto sem forma de coluna, lista sem nenhuma coluna reconhecivel,
  separacao V-01 vs V-14, coluna plenamente valida, multiplas colunas validas
  e lista mista com ao menos uma coluna reconhecivel.

### 31.4 Contagem final da suíte

| Script | Verificacoes | Falhas |
|---|---|---|
| `tela/teste_loader.py` | 419 | 0 |
| `tela/teste_modelo.py` | 186 | 0 |
| `tela/teste_renderizador.py` | 1223 | 0 |
| `tela/teste_distribuicao_matricial.py` | 36 | 0 |
| `demo/teste_demo.py` | 363 | 0 |
| `demo/teste_diagnostico.py` | 48 | 0 |
| `demo/teste_demo_distribuicao.py` | 109 | 0 |
| `demo/teste_explorar_barra_de_menus.py` | 38 | 0 |
| `demo/teste_demo_console.py` | 116 | 0 |
| `demo/teste_demo_console_modos.py` | 63 | 0 |
| **Total** | **2601** | **0** |

10 scripts, 2601 verificacoes, 0 falhas. Acumulado do patch: +23 verificacoes
em `tela/teste_loader.py` (396 → 419) relativas ao baseline do primeiro patch.
Os demais scripts permanecem estaveis.

### 31.5 Arquivos alterados neste patch

```text
tela/loader.py
tela/teste_loader.py
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
```

Nenhum arquivo fora da lista autorizada foi alterado. `demo/demo.py` e
`demo/teste_demo_console_modos.py` nao precisaram de mudanca: as correcoes do
primeiro patch (modo inicial por argv, V-04, identidade neutra do conteudo
compartilhado) permanecem funcionais e foram preservadas integralmente.

### 31.6 Higiene e estado Git

```yaml
git_diff_check: sem_erros
stage: vazio
commit_novo: inexistente
```

### 31.7 Validacao manual

Permanece pendente:

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

### 31.8 Conclusao

```text
implementacao corrigida e aguardando novo QA independente
```

O bypass D23 por ausencia de `formato.excesso` esta fechado; a determinacao de
escopo D23 agora e estrutural (envelope pre-ADR-0028 vs consumidor multinivel)
e o inventario legado e estritamente nominal. V-01 exige ao menos uma coluna
semanticamente valida, com separacao clara entre V-01 (ausencia de coluna
reconhecivel) e V-14 (coluna reconhecivel sem origem). As correcoes anteriores
do ciclo permanecem funcionais. Nenhuma aprovacao e declarada.

---

## 32. Terceiro patch pos-QA — eliminacao de bypass D23 por campo isolado e valores semanticamente vazios (QAPP2-001, QAPP2-002)

**Fonte**: `docs/relatorios/RELATORIO_QA_POS_PATCH_2_H-0037_IMPLEMENTACAO.md`

Dois achados remanescentes apos o segundo patch (secao 31):

- **H0037-IMPL-QAPP2-001**: bypass D23 por campo isolado de envelope
- **H0037-IMPL-QAPP2-002**: valores semanticamente vazios aceitos por V-01

### 32.1 H0037-IMPL-QAPP2-001 — eliminar bypass D23 por campo isolado

**Causa do defeito**: `_console_em_escopo_d23` usava `any(campo in elemento for
campo in _CAMPOS_ENVELOPE_PRE_ADR_0028)` — qualquer campo isolado do envelope
(ex. apenas `itens: []`) eximia o elemento do escopo D23 como se fosse um
envelope historico completo. Um consumidor multinivel com `itens: []` adicionado
por descuido escapava de D23 sem ter os demais 6 campos exigidos pelo contrato.

**Correcao aplicada**: a funcao distingue agora tres estados mutuamente
exclusivos com base em `n_presentes = len(_CAMPOS_ENVELOPE_PRE_ADR_0028 & set(elemento))`:

1. `n_presentes == 7` (envelope completo): verificar sub-caso hibrido — se
   `formato.excesso` contiver `politica_modo` ou `modo_inicial`, a estrutura e
   incompativel e levanta `TelaEstruturaInvalida`; caso contrario retorna `False`
   (fora do escopo D23 — preserva comportamento contratual anterior).
2. `n_presentes == 0` (consumidor puro): retorna `id_tela not in
   _TELAS_LEGADAS_D23` — consumidor novo entra em D23; legado nominado sai.
3. `1 <= n_presentes <= 6` (parcial ou hibrido incompleto): levanta
   `TelaEstruturaInvalida` — presenca parcial nao caracteriza envelope valido
   nem consumidor multinivel; qualquer campo isolado e agora um erro estrutural.

Esta logica torna o bypass por campo isolado impossivel:

| Estado | `n_presentes` | Resultado |
|---|---|---|
| Consumidor puro | 0 | D23 (ou legado isento) |
| Campo isolado (qualquer um) | 1..6 | REJEITADO |
| Envelope incompleto (6/7) | 6 | REJEITADO |
| Envelope completo sem D23 | 7 | Fora de D23 |
| Envelope completo + D23 | 7 + hibrido | REJEITADO |

### 32.2 H0037-IMPL-QAPP2-002 — rejeitar valores semanticamente vazios em _coluna_reconhecivel

**Causa do defeito**: `_coluna_reconhecivel` verificava apenas presenca de chave
em dicts (`any(campo in entrada ...)`) sem inspecionar o valor, e para strings
comparava `!= ""` sem remover whitespace. Resultado: `{"titulo": null}`,
`{"nivel": ""}`, `{"campo": "   "}` e `["   "]` eram aceitos como colunas
reconheciveis, permitindo cabecalhos de tabela semanticamente vazios passarem V-01.

**Correcao aplicada**:

- **Strings**: `return entrada.strip() != ""` — strings so de espacos rejeitadas.
- **Dicts**: para cada campo candidato (`titulo`, `nivel`, `campo`) presente na
  entrada, o valor `v` deve satisfazer `v is not None and not (isinstance(v, str)
  and v.strip() == "")`. Se nenhum campo candidato tiver valor semanticamente
  nao-vazio, retorna `False` (coluna nao reconhecivel).

Valores semanticamente vazios agora rejeitados: `null`, `""`, `"   "` (e
qualquer string composta somente de espacos).

### 32.3 Testes adicionados

Em `tela/teste_loader.py`:

- **V-01 P3-01 a P3-10** (10 verificacoes): casos de valores semanticamente
  vazios em `formato.tabela.cabecalho` — `titulo` nulo, `titulo` vazio, `titulo`
  so com espacos, `nivel` nulo, `nivel` vazio, `campo` nulo, `campo` vazio,
  string vazia, string so com espacos, lista mista com todos os valores vazios.
  Todos devem ser rejeitados com `TelaEstruturaInvalida`.

- **"V-01 vs V-14" corrigido**: o teste anterior sobrescrevia `cabecalho = []`
  (disparando V-01 indevidamente). Corrigido para manter o cabecalho valido de
  `_doc_tabela()` (`["Col"]`) e sobrescrever apenas `colunas` com uma entrada
  sem `nivel` ou `campo` — V-14 deve disparar. Verificacao explicita de "V-14"
  na mensagem de excecao.

- **D23-06 atualizado** (envelope completo com todos os 7 campos): o teste
  anterior tinha apenas 3 dos 7 campos, o que com a nova logica seria tratado
  como parcial e rejeitado. Corrigido para usar o envelope minimo completo.

- **D23-P3-05 a D23-P3-06** (7 verificacoes via `_rejeita_carrega_em_tmp`):
  cada campo do `_CAMPOS_ENVELOPE_PRE_ADR_0028` testado isoladamente — todos
  devem ser rejeitados como estrutura incompativel.

- **D23-P3-07** (1 verificacao): estrutura hibrida — envelope completo com 7
  campos mais `politica_modo` em `formato.excesso` — deve ser rejeitada.

- **D23-P3-08** (1 verificacao): envelope historico completo sem campos D23 —
  deve ser aceito (fora do escopo D23).

- **D23-P3-09** (1 verificacao): envelope com 6 de 7 campos (faltando
  `politica_paginacao`) — deve ser rejeitado.

- **D23-P3-10** (2 verificacoes): telas legadas H-0035 (`h0035_console_com`,
  `h0035_console_sem`) como consumidores — devem ser aceitas.

- **D23-P3-11** (1 verificacao): copia renomeada de legado sem politica — deve
  ser rejeitada.

- **D23-P3-12a e D23-P3-12b** (2 verificacoes): prefixos semelhantes aos
  legados (`h0035_console_novo`, `h0036_console_copia`) sem politica — devem ser
  rejeitadas.

- **Verificacoes diretas de `_console_em_escopo_d23`** (4 verificacoes):
  - Envelope completo → retorna False.
  - Consumidor novo → retorna True.
  - Consumidor legado H-0036 → retorna False.
  - Campo isolado `itens` → levanta `TelaEstruturaInvalida` (nao retorna False).

### 32.4 Arquivos alterados neste patch

```text
tela/loader.py
tela/teste_loader.py
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
```

Nenhum arquivo fora da lista autorizada foi alterado. `docs/adr/`, `docs/contratos/`,
`docs/handoff/` e todos os relatorios QA permanecem intocados.

### 32.5 Higiene e estado Git

```yaml
git_diff_check: sem_erros
stage: vazio
commit_novo: inexistente
```

### 32.6 Validacao manual

Permanece pendente:

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

### 32.7 Conclusao

```text
implementacao corrigida e aguardando novo QA independente
```

O bypass D23 por campo isolado de envelope esta eliminado: presenca parcial dos
campos do envelope (1 a 6 dos 7 exigidos) agora levanta `TelaEstruturaInvalida`
em vez de isentar o elemento do escopo D23. O envelope historico completo (todos
os 7 campos, sem campos D23 em `formato.excesso`) continua sendo aceito e
preservado com comportamento contratual anterior. Valores semanticamente vazios
(`null`, string vazia, string so com espacos) em entradas de
`formato.tabela.cabecalho` sao agora corretamente rejeitados por V-01. As
correcoes dos patches anteriores (modo inicial, V-04, alternancia V, regressao
H-0036, bypass por ausencia de `formato.excesso`, V-01 para lista vazia/nula)
permanecem funcionais. Nenhuma aprovacao e declarada.

---

## 33. Quarto patch pos-QA — validacao de valores do envelope, regressao demo.json, modo somente_verboso e V-14 semantica (QAPP3-001, QAPP3-002)

**Fonte**: `docs/relatorios/RELATORIO_QA_POS_PATCH_3_H-0037_IMPLEMENTACAO.md`

Dois achados remanescentes apos o terceiro patch (secao 32):

- **H0037-IMPL-QAPP3-001**: sete campos de envelope aceitos por presenca de chaves,
  sem validar tipos/valores; regressao em `demo.json` (6/7 campos rejeitados).
- **H0037-IMPL-QAPP3-002**: V-14 aceita `campo`/`nivel` nulos ou semanticamente
  vazios; `_modo_verboso_de_modelo` retorna `False` para `somente_verboso`; teste
  focal mascara a semantica incorreta.

```yaml
qa_de_origem: docs/relatorios/RELATORIO_QA_POS_PATCH_3_H-0037_IMPLEMENTACAO.md
status_de_origem: IMPLEMENTATION_PATCH_REQUIRED

achados_tratados:
  - H0037-IMPL-QAPP3-001
  - H0037-IMPL-QAPP3-002
```

### 33.1 H0037-IMPL-QAPP3-001 — validacao de valores do envelope e regressao demo.json

**Causa do defeito (parte 1)**: `_console_em_escopo_d23` verificava apenas
presenca de chaves para os 7 campos do envelope, sem validar os valores.
Resultado: `{"itens": null, "politica_selecao": null, ...}` (todos null) era
aceito como envelope valido e recebia isencao D23.

**Causa do defeito (parte 2)**: a logica "1 a 6 campos → levanta
`TelaEstruturaInvalida` imediatamente" era aplicada a qualquer console com
envelope parcial, independentemente de possuir marcadores D23
(`politica_modo`/`modo_inicial` em `formato.excesso`). `console_principal` em
`demo.json` possui 6 dos 7 campos do envelope (`itens` ausente,
`politica_paginacao` com tipo invalido) e nenhum marcador D23, portanto era
rejeitado indevidamente — regressao.

**Correcao aplicada**:

1. **Nova funcao `_validar_valores_envelope_pre_adr_0028(elemento)`**: chamada
   quando todos os 7 campos de `_CAMPOS_ENVELOPE_PRE_ADR_0028` estao presentes.
   Valida cada campo por tipo e valores validos:
   - `itens`: deve ser lista.
   - `origem_dados`: deve ser dict ou null.
   - `politica_composicao`: deve ser dict.
   - `politica_navegacao`: deve ser dict.
   - `politica_selecao`: deve ser string em `{"nenhuma", "unica", "multipla"}`.
   - `politica_paginacao`: deve ser string em `{"sem", "com"}`.
   - `politica_exibicao`: deve ser dict.
   Levanta `TelaEstruturaInvalida` ao primeiro campo com tipo ou valor invalido.

2. **Nova semantica para 1 a 6 campos**: em vez de rejeitar imediatamente,
   verifica se ha marcadores D23 em `formato.excesso`. Se sim (estrutura
   hibrida), levanta `TelaEstruturaInvalida`. Se nao, retorna `False` (fora do
   escopo D23 — tratado como estrutura pre-ADR-0028 em rascunho ou historico
   parcial). Isso preserva `demo.json` sem exigir alteracao no arquivo.

Nova tabela de estados:

| `n_presentes` | Marcadores D23? | Resultado |
|---|---|---|
| 7, todos validos | nao | Fora do escopo D23 |
| 7, qualquer invalido | nao | `TelaEstruturaInvalida` |
| 7 | sim (hibrido) | `TelaEstruturaInvalida` |
| 0 | — | D23 (ou legado isento) |
| 1–6 | sim (hibrido) | `TelaEstruturaInvalida` |
| 1–6 | nao (parcial sem D23) | Fora do escopo D23 |

### 33.2 H0037-IMPL-QAPP3-002 — modo somente_verboso e V-14 semantica

**Causa do defeito (parte 1)**: `_modo_verboso_de_modelo` em `demo/demo.py`
retornava `True` apenas para `alternavel` com `modo_inicial == "verboso"`. Para
`somente_verboso`, retornava `False`. O estado inicial `modo_verboso` ficava
`False`, embora `_verboso_efetivo` (correto) sobrescrevesse para `True` em tempo
de renderizacao. O efeito observavel era a tela `h0037_console_verboso_dois_niveis`
ser reportada com `primeiro_modo: nao_verboso` no smoke test do QA.

**Correcao**: adicionado `if politica == "somente_verboso": return True` em
`_modo_verboso_de_modelo`, antes da verificacao de `alternavel`.

**Causa do defeito (parte 2)**: V-14 em `validar_conteudo_externo` rejeitava
apenas ausencia total das chaves `nivel` e `campo`. Se a chave estava presente
com valor `None`, string vazia `""` ou string so de espacos `"   "`, a validacao
passava. Resultado: `{"campo": null}` ou `{"nivel": ""}` eram aceitos como
colunas com origem valida.

**Correcao**: substituida a verificacao de presenca de chave por verificacao de
valor semanticamente valido: `"campo" in col and isinstance(col["campo"], str)
and col["campo"].strip() != ""` (idem para `nivel`). Apenas valor string nao
vazio e nao exclusivamente de espacos e considerado origem valida.

**Causa do defeito (parte 3)**: o teste `teste_modo_verboso_inicial` em
`demo/teste_demo_console_modos.py` esperava `_modo_verboso_de_modelo(m2) is
False` para o cenario 2 (`somente_verboso`). Esta expectativa mascarava o defeito
(teste passava exatamente por verificar o valor incorreto).

**Correcao**: alterado para `_modo_verboso_de_modelo(m2) is True`.

### 33.3 Testes adicionados e modificados

Em `tela/teste_loader.py`:

- **D23-P3-05/06** (7 verificacoes): alterados de `_rejeita_carrega_em_tmp` para
  `_carrega_em_tmp` — campo isolado sem marcadores D23 e agora aceito (nao mais
  rejeitado).
- **D23-P3-09** (1 verificacao): alterado de `_rejeita_carrega_em_tmp` para
  `_carrega_em_tmp` — envelope parcial (6/7 campos) sem marcadores D23 e aceito.
- **Verificacao direta de `_console_em_escopo_d23`**: campo isolado agora deve
  retornar `False` (nao levantar excecao); adicionado teste de hibrido
  (campo + `politica_modo`) que deve levantar `TelaEstruturaInvalida`.
- **D23-P4-01**: envelope com todos os 7 campos `null` — rejeitado.
- **D23-P4-02**: envelope com `itens` tipo errado (string) — rejeitado.
- **D23-P4-03**: envelope com `politica_selecao` invalida — rejeitado.
- **D23-P4-04**: envelope com `politica_paginacao` tipo dict — rejeitado.
- **D23-P4-05** (3 verificacoes): hibrido campo isolado + `politica_modo` — rejeitado.
- **D23-P4-06**: hibrido 6 campos de envelope + `politica_modo` — rejeitado.
- **D23-P4-09**: `demo.json` real carrega sem excecao — aceito.
- **V-14 semantica** (8 verificacoes): `nivel`/`campo` nulos, strings vazias,
  whitespace — rejeitados; `campo` valido e `nivel` valido — aceitos.

Em `demo/teste_demo_console_modos.py`:

- **`teste_modo_verboso_inicial` cenario 2**: corrigido de `is False` para
  `is True` para `somente_verboso`.

### 33.4 Contagem final da suite

| Script | Verificacoes | Falhas |
|---|---|---|
| `tela/teste_loader.py` | 463 | 0 |
| `tela/teste_modelo.py` | 186 | 0 |
| `tela/teste_renderizador.py` | 1223 | 0 |
| `tela/teste_distribuicao_matricial.py` | 36 | 0 |
| `demo/teste_demo.py` | 363 | 0 |
| `demo/teste_diagnostico.py` | 48 | 0 |
| `demo/teste_demo_distribuicao.py` | 109 | 0 |
| `demo/teste_explorar_barra_de_menus.py` | 38 | 0 |
| `demo/teste_demo_console.py` | 116 | 0 |
| `demo/teste_demo_console_modos.py` | 63 | 0 |
| **Total** | **2645** | **0** |

10 scripts, 2645 verificacoes (acima do minimo de 2423), 0 falhas. Acumulado do
patch: +44 verificacoes em `tela/teste_loader.py` (419 → 463) relativas ao
baseline do segundo patch.

### 33.5 Smoke tests pos-patch

```yaml
h0037_console_nao_verboso:
  primeiro_modo: nao_verboso
  verboso_efetivo: nao_verboso
h0037_console_verboso_dois_niveis:
  primeiro_modo: verboso
  verboso_efetivo: verboso
h0037_console_alternavel_tres_niveis:
  primeiro_modo: nao_verboso
  verboso_efetivo: nao_verboso
h0037_console_tabela_alternavel:
  primeiro_modo: verboso
  verboso_efetivo: verboso
```

Todos os 4 cenarios corretos. `h0037_console_verboso_dois_niveis` agora reporta
`primeiro_modo: verboso` conforme D23.

### 33.6 Arquivos alterados neste patch

```text
tela/loader.py
tela/teste_loader.py
demo/demo.py
demo/teste_demo_console_modos.py
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
```

Nenhum arquivo fora da lista autorizada foi alterado. `docs/adr/`,
`docs/contratos/`, `docs/handoff/` e todos os relatorios QA permanecem
intocados. `config/telas/demo/demo.json` e
`config/telas/demo/h0037_console_verboso_dois_niveis.json` nao foram alterados.

### 33.7 Higiene e estado Git

```yaml
git_diff_check: sem_erros
stage: vazio
commit_novo: inexistente
```

### 33.8 Validacao manual

Permanece pendente:

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

### 33.9 Conclusao

```text
implementacao corrigida e aguardando novo QA independente
```

O envelope historico agora e validado por forma contratual completa (tipos e
valores obrigatorios) antes de receber isencao D23. Envelopes parciais sem
marcadores D23 sao tratados como estruturas fora do escopo (pre-ADR-0028 em
rascunho), eliminando a regressao de `demo.json`. V-14 agora rejeita
`nivel`/`campo` nulos, vazios ou so de espacos. `somente_verboso` abre
corretamente em modo verboso. As correcoes dos patches anteriores permanecem
funcionais. Nenhuma aprovacao e declarada.

---

## 34. Quinto Patch Focal (H0037-IMPL-QAPP4-001 e H0037-IMPL-QAPP4-002)

Resultado da auditoria QA do quinto patch:
`docs/relatorios/RELATORIO_QA_POS_PATCH_4_H-0037_IMPLEMENTACAO.md`

Achados tratados:

- `H0037-IMPL-QAPP4-001` (ALTA): bypass D23 por campos parciais de envelope
- `H0037-IMPL-QAPP4-002` (MEDIA): origem de coluna incompativel com estrutura aceita

### 34.1 H0037-IMPL-QAPP4-001: Eliminacao do bypass D23 por envelope parcial

**Problema**: `_console_em_escopo_d23` retornava `False` (fora do escopo D23)
para elementos com 1 a 6 campos canonicos de envelope sem marcadores D23. Isso
permitia que consumidores multinivel novos contornassem a obrigacao de declarar
`politica_modo` adicionando qualquer campo de envelope parcial.

**Discriminador estrutural identificado**: `regra_geracao_itens`

O campo `regra_geracao_itens` e a alternativa contratual a `itens` per
`contrato_console.md` §3 ("itens OU regra de geracao de itens"). Sua presenca
indica geracao interna de itens — o elemento NAO e um consumidor de conteudo
multinivel externo (ADR-0028 §21.1). O `console_principal` de `demo.json` possui
`regra_geracao_itens`, discriminando-o estruturalmente dos consumidores multinivel.

**Logica nova de `_console_em_escopo_d23`**:

1. `n_presentes == n_total` (7 campos canonicos): envelope completo → valida
   valores → return False (isencao D23 por envelope completo, inalterado).
2. `"regra_geracao_itens" in elemento`: geracao interna de itens → return False
   (isencao D23 por tipo estrutural; hibrido com D23 ainda rejeitado).
3. `n_presentes == 0` sem `regra_geracao_itens`: consumidor multinivel puro →
   isentar apenas legados nominais (`_TELAS_LEGADAS_D23`), inalterado.
4. `1 ≤ n_presentes ≤ 6` sem `regra_geracao_itens`: envelope parcial → em escopo
   D23 (return True). **Bypass eliminado.**

**Consequencia nos testes existentes**: fixtures de testes macro (distribuicao,
hierarquia, grupos) que usavam `{"itens": [], "origem_dados": None}` como
placeholder de console nao-consumidor agora requerem `regra_geracao_itens` para
ficarem fora do escopo D23. Todas as fixtures afetadas foram atualizadas para
incluir `"regra_geracao_itens": {}`.

### 34.2 H0037-IMPL-QAPP4-002: Rejeicao de nivel de coluna incompativel

**Problema**: V-14 verificava apenas que `nivel`/`campo` eram strings nao-vazias,
mas nao validava se o valor de `nivel` referenciava um nivel declarado em
`formato.niveis`. Uma coluna com `nivel='inexistente'` era aceita.

**Adicao de V-13 em `validar_conteudo_externo`**: apos a verificacao V-14 (que
garante `nivel` como string nao-vazia), verifica se o valor de `nivel` existe em
`niveis_por_id`. Se nao existir, levanta `TelaEstruturaInvalida` com codigo V-13
("dados incompativeis com a estrutura declarada").

O campo `campo` nao e validado contra um schema de campos de nos de dados (o
contrato nao define um schema declarativo de campos para nos individuais; o
validador semantico nao tem acesso a lista de campos validos para cada nivel). A
validacao V-13 se aplica exclusivamente a `nivel`.

### 34.3 Testes adicionados

**D23-P5 (H0037-IMPL-QAPP4-001)**:

| Teste | Comportamento esperado |
|---|---|
| D23-P5-01: regra_geracao_itens sem campos de envelope | aceito (fora D23) |
| D23-P5-02: regra_geracao_itens com 6 campos de envelope | aceito (fora D23) |
| D23-P5-03: hibrido regra_geracao_itens + politica_modo | rejeitado |
| D23-P5-04: campo isolado sem regra_geracao_itens | rejeitado (em D23) |
| D23-P5-05: 3 campos de envelope sem regra_geracao_itens | rejeitado (em D23) |
| D23-P5-06: 6 campos de envelope sem regra_geracao_itens | rejeitado (em D23) |
| D23-P5-07: envelope completo com regra_geracao_itens | aceito (isencao envelope) |
| D23-P5: verificacoes diretas de _console_em_escopo_d23 | 2 verificacoes |

**D23-P3 modificados (comportamento correto)**:

| Teste | Antes | Depois |
|---|---|---|
| D23-P3-05/06: campo isolado sem D23 (7 casos) | aceito | rejeitado |
| D23-P3-09: 6 de 7 campos sem D23 | aceito | rejeitado |
| Direto: campo isolado 'itens' retorna False | is False | is True |

**V-13 (H0037-IMPL-QAPP4-002)**:

| Teste | Comportamento esperado |
|---|---|
| V-13: coluna com nivel inexistente | rejeitado (V-13) |
| V-13: coluna com nivel de outro esquema | rejeitado (V-13) |
| V-13: mensagem identifica V-13 (nao V-14) | V-13 na mensagem |
| V-13: coluna com nivel valido continua aceita | aceito |

### 34.4 Suite completa pos-patch

| Script | Verificacoes | Falhas |
|---|---|---|
| `tela/teste_loader.py` | 476 | 0 |
| `tela/teste_modelo.py` | 186 | 0 |
| `tela/teste_renderizador.py` | 1223 | 0 |
| `tela/teste_distribuicao_matricial.py` | 36 | 0 |
| `demo/teste_demo.py` | 363 | 0 |
| `demo/teste_diagnostico.py` | 48 | 0 |
| `demo/teste_demo_distribuicao.py` | 109 | 0 |
| `demo/teste_explorar_barra_de_menus.py` | 38 | 0 |
| `demo/teste_demo_console.py` | 116 | 0 |
| `demo/teste_demo_console_modos.py` | 63 | 0 |
| **Total** | **2658** | **0** |

10 scripts, 2658 verificacoes, 0 falhas. Acumulado do patch: +13 verificacoes
em `tela/teste_loader.py` (463 → 476).

### 34.5 Smoke tests pos-patch

```yaml
h0037_console_nao_verboso:
  primeiro_modo: nao_verboso
h0037_console_verboso_dois_niveis:
  primeiro_modo: verboso
h0037_console_alternavel_tres_niveis:
  primeiro_modo: nao_verboso
h0037_console_tabela_alternavel:
  primeiro_modo: verboso
```

### 34.6 Arquivos alterados neste patch

```text
tela/loader.py
tela/teste_loader.py
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
```

Nenhum arquivo fora da lista autorizada foi alterado. `docs/adr/`,
`docs/contratos/`, `docs/handoff/` e todos os relatorios QA permanecem
intocados. Nenhum JSON de configuracao foi alterado.

### 34.7 Higiene e estado Git

```yaml
git_diff_check: sem_erros
stage: vazio
commit_novo: inexistente
```

### 34.8 Validacao manual

Permanece pendente:

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

### 34.9 Conclusao

```text
implementacao corrigida e aguardando novo QA independente
```

O bypass D23 por envelope parcial foi eliminado por discriminador estrutural
(`regra_geracao_itens`): consoles com geracao interna de itens ficam fora do
escopo D23 por tipo estrutural, nao por cardinalidade de campos. Consumidores
multinivel novos com 1 a 6 campos parciais de envelope (sem `regra_geracao_itens`)
agora sao corretamente rejeitados por D23. A validacao V-13 agora rejeita
`nivel` de coluna que nao referencia um nivel declarado em `formato.niveis`.
Nenhuma aprovacao e declarada.

---

## 35. Sexto Patch Focal (H0037-IMPL-QAPP5-001 e H0037-IMPL-QAPP5-002)

Resultado da auditoria QA do quinto patch:
`docs/relatorios/RELATORIO_QA_POS_PATCH_5_H-0037_IMPLEMENTACAO.md`
(status `IMPLEMENTATION_PATCH_REQUIRED`).

```yaml
qa_de_origem: docs/relatorios/RELATORIO_QA_POS_PATCH_5_H-0037_IMPLEMENTACAO.md
status_de_origem: IMPLEMENTATION_PATCH_REQUIRED

achados_tratados:
  - H0037-IMPL-QAPP5-001
  - H0037-IMPL-QAPP5-002
```

### 35.0 Correcao de afirmacoes anteriores refutadas pelo QA

A secao 34 (quinto patch) declarou que:

- o discriminador estrutural identificado para eliminar o bypass D23 por envelope
  parcial era `regra_geracao_itens`;
- consoles com `regra_geracao_itens` ficavam fora do escopo D23 por tipo
  estrutural;
- consumidores multinivel novos com 1 a 6 campos parciais de envelope (sem
  `regra_geracao_itens`) eram rejeitados por D23.

O QA do quinto patch refutou essas afirmacoes. A chave `regra_geracao_itens`
nao tem schema interno fechado em nenhum contrato, ADR ou NOMENCLATURA (so
existe a frase "regra de geracao de itens" como alternativa a `itens` em
`contrato_console.md` §3). A isencao por mera presenca da chave aceitava
`{}`, `null`, tipos incorretos, objetos incompletos, combinacoes hibridas e
mascarava a classificacao estrutural (`REGRESSAO_MASCARADA`). A rejeicao de
1 a 6 campos de envelope como bypass estava correta, mas foi anulada pelo
uso concorrente da isencao por `regra_geracao_itens`. A secao 35 substitui
integralmente a regra do quinto patch e descreve a decisao final.

### 35.1 Portao documental para `regra_geracao_itens` — Resultado B

Antes de corrigir, determinou-se se existe autoridade suficiente para fechar a
forma interna de `regra_geracao_itens`. Busca exaustiva em
`docs/contratos/`, `docs/adr/`, `docs/NOMENCLATURA.md` e demais autoridades:

```yaml
regra_geracao_itens:
  string_snake_case_em_contratos_adr_nomenclatura: ausente
  frase_em_contrato_console_secao_3: "itens OU regra de geracao de itens"
  schema_interno_fechado: inexistente
  campos_internos_obrigatorios: nao_definidos
  tipos_e_valores_permitidos: nao_definidos
  funcao_de_validacao_existente: inexistente
  carregamento_historico_comprovado: somente_demo.json
  conclusao: RESULTADO_B_sem_autoridade_suficiente
```

**Decisao (Resultado B):** nao inventar schema novo; nao considerar `{}` valido;
nao usar a propriedade como discriminador suficiente; classificar o elemento
pelo tipo estrutural real e pelo fluxo de carregamento autorizado; rejeitar
combinacoes hibridas.

### 35.2 H0037-IMPL-QAPP5-001 — eliminar `regra_geracao_itens` como chave de isencao

**Causa do defeito:** o quinto patch introduziu em `_console_em_escopo_d23` um
ramo `if "regra_geracao_itens" in elemento: return False` que concedia isencao
D23 por mera presenca da chave, sem validar tipo, valor, campos internos,
coexistencias com `itens`, `origem_dados`, envelope, consumidor multinivel ou
marcadores D23. A matriz adversarial do QA aceitou `{}`, `null`, string, lista,
bool, numero, objetos incompletos, consumidor sem politica mais `regra_geracao_itens`
e varias combinacoes hibridas.

**Discriminador estrutural efetivamente usado:** o tipo estrutural real do
elemento `console`, determinado pela presenca dos campos do envelope
pre-ADR-0028. O envelope classico admite **duas variantes mutuamente exclusivas**
de fonte de itens, ambas combinadas com o mesmo conjunto base de seis campos
(`_CAMPOS_ENVELOPE_BASE_PRE_ADR_0028`: `origem_dados` + as cinco politicas):

```yaml
variante_1:
  fonte_de_itens: itens
  campos_base: 6 (origem_dados + 5 politicas)
variante_2:
  fonte_de_itens: regra_geracao_itens
  campos_base: 6 (os mesmos)
  forma_historica: demo.json (console_principal)
mutuamente_exclusivas: itens_X_regra_geracao_itens
```

A variante 2 e aceita **por compatibilidade restrita com a forma historica
comprovada** — somente telas nominais em `_TELAS_VARIANTE2_LEGADAS`
(atualmente `{"demo"}`). O valor interno de `regra_geracao_itens` nao e
validado (nao ha schema fechado); preserva-se a forma historica de
`demo.json` sem inventar schema novo. Telas novas ou revisadas **nao** podem
usar `regra_geracao_itens` para evitar D23.

**Nova logica de `_console_em_escopo_d23`** (ordem de decisao):

```yaml
1:
  identificar_tipo_estrutural_real: obrigatorio
  (campos_base_presentes, tem_itens, tem_regra, tem_fonte_itens)

2:
  hibrido_envelope_mais_D23:
    condicao: (campos_base >= 1 OU tem_fonte_itens) E tem_marcadores_D23
    resultado: REJEITA_TelaEstruturaInvalida

3:
  duas_fontes_concorrentes:
    condicao: itens E regra_geracao_itens
    resultado: REJEITA_TelaEstruturaInvalida

4:
  consumidor_multinivel_mais_regra:
    condicao: regra_geracao_itens E campos_base == 0
    resultado: REJEITA_TelaEstruturaInvalida (hibrido)
    observacao: "qualquer valor sob a chave e ignorado; nao ha schema fechado"

5:
  envelope_com_fonte_de_itens:
    subcaso_5a_envelope_incompleto:
      condicao: tem_fonte_itens E campos_base != 6
      resultado: REJEITA_TelaEstruturaInvalida
    subcaso_5b_variante2_em_tela_nova:
      condicao: tem_regra E id_tela nao_em__TELAS_VARIANTE2_LEGADAS
      resultado: REJEITA_TelaEstruturaInvalida
    subcaso_5c_envelope_completo:
      acao: _validar_valores_envelope_pre_adr_0028 (conforme variante)
      resultado: return False (fora do escopo D23)

6:
  campos_base_sem_fonte_de_itens:
    condicao: campos_base >= 1 E nao tem_fonte_itens
    resultado: REJEITA_TelaEstruturaInvalida (estrutura incompleta)

7:
  consumidor_multinivel_puro:
    condicao: campos_base == 0 E nao tem_fonte_itens
    resultado: return id_tela not in _TELAS_LEGADAS_D23
```

**Validacao por variante** (`_validar_valores_envelope_pre_adr_0028`):

```yaml
variante_1 (itens):
  validacao: estrita_dos_tipos_canonicos
  itens: lista
  origem_dados: objeto_ou_null
  politica_composicao: objeto
  politica_navegacao: objeto
  politica_selecao: string_em {nenhuma, unica, multipla}
  politica_paginacao: string_em {sem, com}
  politica_exibicao: objeto
variante_2 (regra_geracao_itens, legada comprovada):
  validacao: compatibilidade_restrita_sem_tipos_escalars
  justificativa: "sem schema fechado; preserva forma historica de demo.json"
  regra_geracao_itens: valor_nao_validado
  campos_base: preservados_como_declarados (rascunho historico)
```

**Consequencia em `demo.json`:** `console_principal` (variante 2 legada,
`regra_geracao_itens: {tipo: "pendente"}` + 6 campos base, sem `itens`)
permanece ACEITO pelo tipo estrutural real (variante 2 historica
comprovada em `_TELAS_VARIANTE2_LEGADAS`), fora do escopo D23. A validade
NAO decorre de path de arquivo, ID generico, objeto vazio ou mera presenca
da chave — decorre do reconhecimento nominal da configuracao historica.

**Fixtures mascaradoras corrigidas:** os testes macro de `tela/teste_loader.py`
que recebido `"regra_geracao_itens": {}` artificialmente para escapar de D23
foram corrigidos. Cada fixture foi reclassificada conforme seu objetivo
original (elemento console pre-ADR-0028 para testes de arranjo/distribuicao/
matriz) e passou a usar envelope variante 1 completo (`_ENVELOPE_CONSOLE_COMPLETO`,
constante de modulo) — preservando o objetivo original sem a chave mascaradora.
Nenhuma categoria semantica de teste foi alterada.

**Resultado exigido alcancado:**

```yaml
regra_geracao_itens:
  usada_como_chave_de_isencao: false
  consumidor_sem_politica_com_objeto_vazio_aceito: false
  consumidor_sem_politica_com_null_aceito: false
  consumidor_sem_politica_com_tipo_incorreto_aceito: false
  consumidor_com_politica_hibrido_aceito: false
  coexistencia_invalida_aceita: false
  demo_json_carrega: true
  bypass_remanescente: false
```

### 35.3 H0037-IMPL-QAPP5-002 — V-13 completo por `campo`

**Causa do defeito:** a validacao V-13 (dados incompativeis com a estrutura
declarada) em `validar_conteudo_externo` cobria apenas `nivel` de coluna de
tabela; o `campo` de coluna era aceito sem confronto com a estrutura. Uma
coluna com `campo: "nao_existe"` passava mesmo sendo origem declarada mas
incompativel.

**Autoridade para validar `campo`:** o contrato nao define catalogo literal
fechado de valores de `campo` (V-14 exige apenas presenca de string nao-vazia),
mas define **onde estao os campos validos** — em `formato.niveis[].conteudo`
(`contrato_json_console.md` §12.3):

```yaml
container_ou_conteudo:
  conteudo: string (nome do campo de texto do no)
nome_valor:
  conteudo: objeto {nome: <campo>, valor: <campo>}
```

Esse conjunto e o catalogo estrutural derivado (sem inventar catalogo novo).
A coleta acontece em `validar_conteudo_externo` apos a leitura dos niveis:

```python
_campos_validos_por_no = set()
for _nivel in niveis_por_id.values():
    _cont = _nivel.get("conteudo")
    if isinstance(_cont, str) and _cont.strip() != "":
        _campos_validos_por_no.add(_cont)
    elif isinstance(_cont, dict):
        for _chave_cont in ("nome", "valor"):
            _nome_cont = _cont.get(_chave_cont)
            if isinstance(_nome_cont, str) and _nome_cont.strip() != "":
                _campos_validos_por_no.add(_nome_cont)
```

**Separacao V-13/V-14 por `campo`:**

```yaml
V_14:
  causa: origem_ausente_ou_sem_valor_semantico
  dispara: campo ausente OU nulo OU string vazia OU whitespace
V_13:
  causa: origem_declarada_mas_incompativel
  dispara: campo declarado (string nao vazia) que nao pertence a
           _campos_validos_por_no
```

A validacao V-13 por `campo` e adicionada ao bloco V-13/V-14 em
`validar_conteudo_externo`, apos a validacao V-13 por `nivel`. As fixtures
reais (`h0036_tabela_conteudo.json`, `h0037_tabela_conteudo.json`) usam
`formato.tabela.cabecalho` como lista de strings (sem `colunas[]`), portanto
nao sao afetadas pela validacao de `campo` em `colunas[]`.

### 35.4 Lista mista — observacao nao bloqueante

```yaml
lista_mista:
  estado: observacao_nao_bloqueante
  alterada_neste_patch: false
```

O QA classificou a aceitacao de lista mista em `formato.tabela.cabecalho`
como observacao nao bloqueante. Este patch nao altera esse comportamento e
nao amplia o escopo.

### 35.5 Testes adicionados e modificados

Em `tela/teste_loader.py`:

- **D23-P6 / RGI-P6-01 a RGI-P6-13 + verificacoes diretas** (H0037-IMPL-QAPP5-001):
  - RGI-P6-01: `demo.json` real carrega (variante 2 historica);
  - RGI-P6-02: copia estrutural de `demo.json` com outro ID rejeitada (variante 2
    nao legada);
  - RGI-P6-03/04/05: consumidor multinivel + `regra_geracao_itens` em 9 formas
    (`{}`, `null`, string, lista, bool, numero, objeto sem tipo, objeto sem ids,
    objeto incompleto) — todas rejeitadas como hibrido;
  - RGI-P6-06: consumidor + `regra_geracao_itens` + `politica_modo` rejeitado;
  - RGI-P6-07: `itens` + `regra_geracao_itens` (duas fontes) rejeitado;
  - RGI-P6-08: `regra_geracao_itens` + `origem_dados` (variante 2 incompleta)
    rejeitado;
  - RGI-P6-09: `regra_geracao_itens` + campos parciais (variante 2 incompleta)
    rejeitado;
  - RGI-P6-10: variante 2 completa em tela nova rejeitada; em `demo` retorna
    `False` (legada, fora de D23);
  - RGI-P6-11: consumidor + `regra_geracao_itens` + 0/1/3/6 campos de envelope
    — todos rejeitados;
  - RGI-P6-12: envelope variante 1 incompleto (6/7) rejeitado;
  - RGI-P6-13: cinco legados nominais (3 H-0036 + 2 H-0035) preservados;
  - verificacoes diretas de `_console_em_escopo_d23`: consumidor +
    `regra_geracao_itens` (4 formas) levanta hibrido; consumidor novo sem regra
    retorna `True`; variante 2 em tela nova levanta excecao.

- **V-13 por campo / V13-P6-01 a V13-P6-10 + extras** (H0037-IMPL-QAPP5-002):
  - V13-P6-01: campo inexistente -> V-13;
  - V13-P6-02: campo declarado ausente nos dados -> rejeitado;
  - V13-P6-03: campo incompativel com tabela -> V-13;
  - V13-P6-04: campo de outra apresentacao -> V-13;
  - V13-P6-05: campo valido -> aceito;
  - V13-P6-06: nivel valido -> aceito;
  - V13-P6-07: duas colunas validas -> aceitas;
  - V13-P6-08: titulo valido + campo inexistente -> V-13;
  - V13-P6-09: campo vazio -> V-14 (nao V-13);
  - V13-P6-10: nivel inexistente -> V-13;
  - extras nome_valor: campo `vlr` (declarado em `conteudo.valor`) aceito;
    campo `fantasma` rejeitado por V-13.

- **Modificados para a nova semantica das variantes:**
  - D23-P3-05/06: campo isolado -> agora rejeitado (estrutura incompleta);
  - D23-P3-09: envelope variante 1 incompleto (6/7) -> rejeitado;
  - verificacao direta "campo isolado 'itens' retorna False" -> agora levanta
    `TelaEstruturaInvalida` (envelope incompleto);
  - `_run_tipos_validos`: placeholder de console passou a usar
    `_ENVELOPE_CONSOLE_COMPLETO` (variante 1 completa);
  - `_tela_minima` e 26 fixtures placeholder (`{itens:[], origem_dados:None,
    regra_geracao_itens:{}}`) corrigidas: removida a chave mascaradora
    `regra_geracao_itens:{}` e expandidas para envelope variante 1 completo.

### 35.6 Contagem final da suite

| Script | Verificacoes | Falhas |
|---|---|---|
| `tela/teste_loader.py` | 512 | 0 |
| `tela/teste_modelo.py` | 186 | 0 |
| `tela/teste_renderizador.py` | 1223 | 0 |
| `tela/teste_distribuicao_matricial.py` | 36 | 0 |
| `demo/teste_demo.py` | 363 | 0 |
| `demo/teste_diagnostico.py` | 48 | 0 |
| `demo/teste_demo_distribuicao.py` | 109 | 0 |
| `demo/teste_explorar_barra_de_menus.py` | 38 | 0 |
| `demo/teste_demo_console.py` | 116 | 0 |
| `demo/teste_demo_console_modos.py` | 63 | 0 |
| **Total** | **2694** | **0** |

10 scripts, 2694 verificacoes (acima do baseline de 2658 do quinto patch), 0
falhas. Acumulado deste patch: +36 verificacoes em `tela/teste_loader.py`
(476 -> 512).

### 35.7 Preservacoes confirmadas

```yaml
modos_iniciais:
  h0037_console_nao_verboso: nao_verboso
  h0037_console_verboso_dois_niveis: verboso
  h0037_console_alternavel_tres_niveis: nao_verboso
  h0037_console_tabela_alternavel: verboso

tecla_V:
  telas_fixas: inerte
  telas_alternaveis: reversivel

V_01: conforme
V_04:
  folha_sem_filhos: aceita
  folha_com_filhos_vazio: rejeitada
  folha_com_filho_real: rejeitada

V_14:
  origem_ausente: rejeitada
  origem_nula: rejeitada
  origem_vazia: rejeitada
  origem_whitespace: rejeitada
  tipo_incorreto: rejeitado

conteudo_compartilhado:
  identidade: H-0037 conteudo_dois_niveis
  varia_por_tela: false

demo_json:
  carrega: true
  entradas: 11

inventario_legado:
  total: 5
  h0036_console_hierarquia: preservado
  h0036_console_tabela: preservado
  h0036_console_conjuntos: preservado
  h0035_console_com: preservado
  h0035_console_sem: preservado

regressao_H_0036:
  preservada: true
```

### 35.8 Arquivos alterados neste patch

```text
tela/loader.py
tela/teste_loader.py
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
```

Nenhum arquivo fora da lista autorizada foi alterado. `docs/adr/`,
`docs/contratos/`, `docs/handoff/`, `docs/NOMENCLATURA.md`,
`docs/adr/INDICE_ADR.md`, `config/telas/demo/` (incluindo `demo.json`),
`demo/` e todos os relatorios QA permanecem intocados.

### 35.9 Higiene e estado Git

```yaml
git_diff_check: sem_erros
stage: vazio
commit_novo: inexistente
push: inexistente
arquivos_fora_da_lista_alterados_pelo_patch: nenhum
relatorios_QA_alterados: nenhum
relatorio_manual_criado: false
artefatos_transitorios_restantes: nenhum
```

### 35.10 Validacao manual

Permanece pendente:

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

### 35.11 Conclusao

```text
implementacao corrigida e aguardando novo QA independente
```

A propriedade `regra_geracao_itens` nao concede mais isencao D23 por mera
presenca. O discriminador estrutural efetivo e o tipo estrutural real do
elemento (duas variantes do envelope pre-ADR-0028, mutuamente exclusivas
quanto a fonte de itens). A variante 2 (`regra_geracao_itens`) e aceita
apenas por compatibilidade restrita com a forma historica comprovada de
`demo.json` (inventario nominal `_TELAS_VARIANTE2_LEGADAS`); telas novas nao
podem usa-la para evitar D23. `{}`, `null` e tipos incorretos sob a chave
jamais sao aceitos como bypass. A validacao V-13 agora cobre `campo` de
coluna contra o catalogo estrutural derivado de `formato.niveis[].conteudo`,
com causa distinta de V-14. As correcoes dos patches anteriores (modo
inicial, V-04, alternancia V, bypass por ausencia de `formato.excesso`,
V-01 para coluna reconhecivel, valores do envelope variante 1, V-14
semantico, V-13 por nivel) permanecem funcionais. Nenhuma aprovacao e
declarada.

---

## 36. Setimo Patch Focal — correcoes apos validacao manual do usuario (H0037-MANUAL-001/002/003)

```yaml
origem:
  relatorio: docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0037.md
  status: MANUAL_VALIDATION_FAILED

achados_tratados:
  - H0037-MANUAL-001
  - H0037-MANUAL-002
  - H0037-MANUAL-003
```

Patch focal decorrente da validacao manual executada pelo usuario em terminal
real (TTY) registrada em `RELATORIO_VALIDACAO_MANUAL_H-0037.md`. Os tres
achados sao defeitos de interface reproduzidos pelo usuario. A ausencia de
paginacao nao e defeito deste ciclo.

### 36.1 H0037-MANUAL-001 — Marcador de truncamento `...` ausente

**Causa do marcador ausente**: em modo nao verboso, o renderizador montava as
linhas de conteudo com o texto integral e deixava o envelope da caixa
(``_linha_conteudo``) truncar silenciosamente os caracteres excedentes por
``texto[:content_w]``. O resultado cortava o conteudo sem exibir o marcador
``...`` ao final da linha truncada, contrariando o comportamento obrigatorio
de ``contrato_console.md §21.2`` (cada conteudo aplicavel ocupa exatamente
uma linha fisica com truncamento conforme a politica declarada; os dados
originais permanecem inalterados).

**Ponto central corrigido**: nova funcao ``_truncar_com_marcador(texto,
largura)`` em ``tela/renderizador.py`` aplica o marcador ``...`` ANTES do
envelope de caixa, de modo que o sufixo ``...`` faz parte do trecho visivel
e nao e acrescentado depois de o texto ja ter sido cortado pela borda. O
truncamento com marcador e aplicado nos tres modos de apresentacao do
conteudo externo multinivel quando ``content_w`` esta disponivel e o modo e
nao verboso:

- ``_linhas_apresentacao_hierarquia``: cada item de conteudo aplicavel em
  modo nao verboso e truncado para caber em ``content_w - len(prefixo)``
  com marcador;
- ``_linhas_apresentacao_tabela``: cada linha da tabela (cabecalho, regua e
  dados) em modo nao verboso e truncada para ``content_w`` com marcador;
- ``_linhas_apresentacao_conjuntos``: cada valor e cada texto de conteudo
  em modo nao verboso e truncado com marcador.

**Comportamento com e sem truncamento**:

```yaml
texto_que_cabe:
  marcador: ausente
  texto: integral
texto_que_excede_e_largura_maior_ou_igual_a_3:
  marcador: presente
  sufixo_visivel: "..."
  linha_resultante: "texto[:largura-3] + '...'"
  comprimento_final: exatamente_largura
  largura_respeitada: true
largura_muito_pequena_menor_que_3:
  comportamento: truncamento_silencioso_sem_marcador
  motivo: "marcador nao cabe; segue a regra vigente para areas menores que
           o comprimento do marcador"
  resultado: texto[:largura]
modo_verboso:
  marcador_artificial: ausente
  conteudo: quebrado_em_multiplas_linhas
hierarquia_nao_verbosa:
  linha_fisica: unica
tabela_compacta:
  altura: uma_linha_por_celula_de_dados
alinhamento_e_bordas:
  preservados: true
dados_originais:
  modificados: false
```

O marcador nunca aumenta a linha alem do limite e nunca e acrescentado depois
de o texto ja ter sido cortado pelo terminal.

### 36.2 H0037-MANUAL-002 — ``[Esc]`` sempre primeiro chip

**Causa da ordem incorreta dos chips**: os JSONs estruturais dos cenarios 3
e 4 (``h0037_console_alternavel_tres_niveis.json``,
``h0037_console_tabela_alternavel.json``) declaravam ``[V] Verboso`` antes
de ``[Esc] Voltar`` em ``barra_de_menus.chips[]``. O renderizador
``_linhas_barra`` preservava a ordem declarada sem aplicar a regra
contratual de que ``[Esc]`` e sempre o primeiro chip quando declarado
(``contrato_barra_de_menus.md §8.2``).

**Regra ``[Esc]`` primeiro**: a regra contratual ja vigora em
``contrato_barra_de_menus.md §8.2``: ``[Esc]`` e sempre o primeiro chip
quando declarado. Esta revisao aplica a regra na origem central da
ordenacao da barra — nova funcao ``_garantir_esc_primeiro(chips)`` em
``tela/renderizador.py``, chamada por ``_linhas_barra`` apos a validacao de
ancoras e antes da montagem das linhas.

**Aplicacao centralizada**: a regra e aplicada na origem central da
ordenacao da barra, valendo para qualquer tela. Nao ha condicao especifica
por ID de tela, JSON, cenario ou posicao fixa inserida apenas no teste. A
funcao:

- percorre os chips e identifica o primeiro cuja ``tecla`` seja ``"Esc"``;
- se houver, move-o para a primeira posicao, preservando a ordem relativa
  dos demais chips;
- se nao houver, retorna a lista sem alteracao (nao inventa ``[Esc]``);
- nao duplica (teclas duplicadas ja sao rejeitadas em outro ponto do
  contrato para a mesma instancia);
- nao altera texto, tecla nem funcao dos demais chips.

Resultado observado nas telas alternaveis:

```text
[Esc] Voltar  [V] Verboso
```

### 36.3 H0037-MANUAL-003 — Tecla ``v`` minuscula nao reconhecida

**Causa da falta de ``v`` minusculo**: ``processar_comando`` em
``demo/demo.py`` tratava apenas ``comando == "V"`` (maiusculo) como
alternancia de modo nas telas com ``politica_modo == "alternavel"``. A tecla
``v`` minuscula nao era reconhecida.

**Tratamento de ``V`` e ``v``**: o ramo de alternancia passou a tratar
nominalmente as duas entradas — ``comando in ("V", "v")`` — somente neste
ponto (alternancia de verbosidade). As duas variantes sao tratadas por
nome, sem transformar todas as teclas em maiusculas globalmente. Outros
comandos continuam case-sensitive (``b``, ``s``, chips do lancador etc.).
Nas telas fixas (``somente_verboso`` / ``somente_nao_verboso``) e nas telas
legadas, ambas as variantes permanecem inertes (nao alteram o estado).

```yaml
telas_alternaveis:
  V: alterna_true
  v: alterna_true
telas_fixas:
  V: inerte
  v: inerte
isolamento:
  alternar_v_em_uma_tela: nao_altera_estado_inicial_de_outra
eco:
  entrada: nao_aparece_como_caractere_no_conteudo_renderizado
```

A normalizacao foi mantida estritamente local: nao persiste o modo
globalmente, nao muda de tela, nao muda o documento externo, nao cria chip
em tela fixa e nao altera ``Esc``.

### 36.4 Testes adicionados

Em ``tela/teste_renderizador.py`` (funcoes
``teste_h0037_manual_001_marcador_truncamento`` e
``teste_h0037_manual_002_esc_primeiro``):

- **RET-01**: conteudo que cabe integralmente nao recebe marcador;
- **RET-02**: conteudo hierarquico excede em modo nao verboso recebe
  marcador ``...``, linha unica, largura respeitada;
- **RET-03**: celula de tabela excede recebe marcador, tabela compacta em
  uma linha por celula de dados;
- **RET-04**: alternancia verboso/nao_verboso da tabela — verboso sem
  marcador (conteudo quebrado), expansao vertical, retorno ao verboso
  restaura conteudo multilinha;
- **RET-05**: redimensionamento automatizavel — largura menor produz
  marcador, ampliar reduz/elimina, largura generosa restaura sem marcador;
- casos diretos do helper ``_truncar_com_marcador`` (texto cabe, excede,
  largura muito pequena);
- **ESC-01**: barra com ``Esc`` e ``V`` — ``[Esc]`` aparece antes de
  ``[V]`` nas telas alternaveis 3 e 4;
- **ESC-02**: barra com ``Esc`` e varios chips — ``Esc`` primeiro, ordem
  relativa dos demais preservada;
- **ESC-03**: barra sem ``Esc`` — chips existentes preservados, ``Esc`` nao
  inventado;
- **ESC-04**: ausencia de duplicacao — quantidade de ``Esc`` == 1;
- **ESC-05**: regressao das barras historicas (``demo.json`` e telas
  H-0036) — ``Esc`` permanece primeiro quando presente.

Em ``demo/teste_demo_console_modos.py`` (funcao
``teste_h0037_manual_003_tecla_v_minuscula``):

- **TECLA-01**: cenario 3 com ``V`` alterna e retorna;
- **TECLA-02**: cenario 3 com ``v`` alterna e retorna;
- **TECLA-03**: cenario 4 com ``V`` compacta e retorna;
- **TECLA-04**: cenario 4 com ``v`` compacta e retorna;
- **TECLA-05**: tela fixa nao verbosa — ``V`` e ``v`` inertes;
- **TECLA-06**: tela fixa verbosa — ``V`` e ``v`` inertes;
- **TECLA-07**: isolamento — alternar ``v`` em uma tela nao muda o estado
  inicial de outra;
- **TECLA-08**: sem eco — a entrada nao aparece como caractere no conteudo
  renderizado.

### 36.5 Contagem final da suite

| Script | Verificacoes | Falhas |
|---|---|---|
| ``tela/teste_loader.py`` | 512 | 0 |
| ``tela/teste_modelo.py`` | 186 | 0 |
| ``tela/teste_renderizador.py`` | 1253 | 0 |
| ``tela/teste_distribuicao_matricial.py`` | 36 | 0 |
| ``demo/teste_demo.py`` | 363 | 0 |
| ``demo/teste_diagnostico.py`` | 48 | 0 |
| ``demo/teste_demo_distribuicao.py`` | 109 | 0 |
| ``demo/teste_explorar_barra_de_menus.py`` | 38 | 0 |
| ``demo/teste_demo_console.py`` | 116 | 0 |
| ``demo/teste_demo_console_modos.py`` | 80 | 0 |
| **Total** | **2741** | **0** |

10 scripts, 2741 verificacoes (acima do baseline de 2694 do sexto patch), 0
falhas. Acumulado deste patch: +30 verificacoes em ``tela/teste_renderizador.py``
(1223 -> 1253) relativas a RET-01..05 e ESC-01..05; +17 verificacoes em
``demo/teste_demo_console_modos.py`` (63 -> 80) relativas a TECLA-01..08.

### 36.6 Smoke tecnico pos-patch

Confirmacao tecnica (sem aprovacao visual) das quatro telas:

```yaml
modos_iniciais:
  h0037_console_nao_verboso: nao_verboso
  h0037_console_verboso_dois_niveis: verboso
  h0037_console_alternavel_tres_niveis: nao_verboso
  h0037_console_tabela_alternavel: verboso

chips:
  telas_alternaveis:
    Esc_primeiro: true
    V_presente: true

teclas:
  V: funcional
  v: funcional
  telas_fixas:
    V: inerte
    v: inerte

render_sem_excecao:
  quatro_cenarios_nos_dois_modos: true
```

A confirmacao visual final continua exclusiva do usuario.

### 36.7 Arquivos alterados neste patch

```text
tela/renderizador.py
tela/teste_renderizador.py
demo/demo.py
demo/teste_demo_console_modos.py
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
```

Nenhum arquivo fora da lista autorizada foi alterado. ``docs/adr/``,
``docs/contratos/``, ``docs/handoff/``, ``docs/NOMENCLATURA.md``,
``docs/adr/INDICE_ADR.md``, ``config/telas/demo/`` (incluindo os quatro
JSONs H-0037 e seus conteudos externos), ``demo/teste_demo.py``,
``demo/teste_demo_console.py``, ``demo/teste_diagnostico.py``,
``demo/teste_explorar_barra_de_menus.py``, ``tela/loader.py``,
``tela/teste_loader.py``, ``tela/modelo.py`` e ``tela/teste_modelo.py``
permanecem intocados neste patch.

### 36.8 Paginacao fora do escopo

```yaml
paginacao:
  aplicavel_a_este_patch: false
  motivo: funcionalidade_nao_prevista_para_esta_rodada
```

Nenhum mecanismo historico de paginacao existente em outras telas foi
removido ou alterado.

### 36.9 Preservacoes confirmadas

```yaml
modos_iniciais:
  h0037_console_nao_verboso: nao_verboso
  h0037_console_verboso_dois_niveis: verboso
  h0037_console_alternavel_tres_niveis: nao_verboso
  h0037_console_tabela_alternavel: verboso

conteudo_compartilhado:
  identidade: H-0037 conteudo_dois_niveis
  varia_por_tela: false

alinhamento_dois_niveis:
  preservado: true

tabela:
  cabecalho: preservado
  celulas_multilinha_no_verboso: preservadas

D23: conforme
V_01: preservada
V_04: preservada
V_13: preservada
V_14: preservada

envelopes_historicos:
  variantes: preservadas

demo_json:
  carrega: true
  entradas: 11

regressao_H_0036:
  preservada: true
```

### 36.10 Higiene e estado Git

```yaml
git_diff_check: sem_erros
stage: vazio
commit_novo: inexistente
push: inexistente
arquivos_fora_da_lista_alterados_pelo_patch: nenhum
relatorios_QA_alterados: nenhum
relatorio_manual_alterado: false
artefatos_transitorios_restantes: nenhum
```

O relatorio manual original ``RELATORIO_VALIDACAO_MANUAL_H-0037.md`` permanece
intocado e continua registrando ``MANUAL_VALIDATION_FAILED`` — nao foi
alterado para parecer aprovado.

### 36.11 Validacao manual

Permanece pendente — uma nova rodada de validacao manual em TTY real
executada pelo usuario e necessaria para confirmar a correcao dos tres
achados. O implementador nao declarou aprovacao visual.

```text
REVALIDACAO_MANUAL_PENDENTE_USUARIO
```

### 36.12 Necessidade de novo QA

A implementacao corrigida apos a reprovacao manual aguarda novo QA
independente (``QA_POS_PATCH_IMPLEMENTACAO``) sobre os tres achados tratados,
antes da revalidacao manual pelo usuario.

### 36.13 Conclusao

```text
implementacao corrigida apos reprovação manual e aguardando novo QA independente
```

O marcador de truncamento ``...`` agora aparece no final de conteudo
efetivamente truncado em modo nao verboso (hierarquia, tabela e conjuntos),
sem afetar conteudo que cabe integralmente. O chip ``[Esc]`` agora e sempre
o primeiro chip quando declarado, por aplicacao centralizada na origem da
ordenacao da barra (vale para qualquer tela). A tecla ``v`` minuscula agora
alterna o modo nas telas alternaveis, ao lado de ``V`` maiuscula, tratadas
nominalmente sem normalizacao global de teclas; ambas permanecem inertes
nas telas fixas. As correcoes dos patches anteriores (D23, V-01, V-04,
V-13, V-14, modo inicial, alternancia V, bypass D23, etc.) permanecem
funcionais. A paginacao permanece fora do escopo. Nenhuma aprovacao e
declarada.

> **Correcao registrada pelo QA pos-patch 7**: embora este patch focal
> afirmasse que o modo verboso nao recebia marcador artificial, a afirmacao
> era **incompleta**. Na apresentacao hierarquica em modo verboso sob
> largura reduzida, nos container ainda passavam por ``_truncar_com_marcador``
> e exibiam ``...`` no lugar do final do conteudo (vide secao 37 — oitavo
> patch focal, que trata ``H0037-IMPL-QAPP7-001`` e ``H0037-IMPL-QAPP7-002``).

## 37. Oitavo Patch Focal — hierarquia verbosa sem corte silencioso (H0037-IMPL-QAPP7-001 e H0037-IMPL-QAPP7-002)

```yaml
qa_de_origem:
  arquivo: docs/relatorios/RELATORIO_QA_POS_PATCH_7_H-0037_IMPLEMENTACAO.md
  status: IMPLEMENTATION_PATCH_REQUIRED

achados_tratados:
  - H0037-IMPL-QAPP7-001
  - H0037-IMPL-QAPP7-002
```

Patch focal decorrente do setimo QA pos-patch de implementacao. O QA
aprovou integralmente o marcador ``...`` no modo nao verboso, ``[Esc]``
como primeiro chip, a ordem relativa dos demais chips, ``V`` maiusculo,
``v`` minusculo, a inercia das telas fixas, a tabela nao verbosa e os
conjuntos nao verbosos. Estas correcoes **nao foram reabertas**. O defeito
residual estava na apresentacao hierarquica verbosa quando a largura
disponivel era reduzida.

### 37.1 H0037-IMPL-QAPP7-001 — Hierarquia verbosa em largura reduzida

**Causa do corte silencioso (e do marcador artificial)**: em
``_linhas_apresentacao_hierarquia``, o ramo verboso estava protegido pela
condicao ``eh_folha = nivel is not None and nivel.tipo != "container"``.
Apenas nos folha entravam no ramo de quebra multilinha; os nos container
(``1.``, ``1.1.`` etc.) caiam no ramo ``else`` que aplica
``_truncar_com_marcador``. O resultado, em largura reduzida, era:

- o texto do container era truncado com sufixo ``...`` (marcador artificial
  em modo verboso, proibido pelo ``contrato_console.md §21.3``); e
- a camada generica do envelope da caixa (``_linha_conteudo``) aplicava
  ainda um corte final ``texto[:content_w]`` sobre a linha ja marcada —
  perda silenciosa do final do conteudo.

```yaml
exemplos_do_defeito:
  - tela: h0037_console_verboso_dois_niveis
    largura: 30
    linha_observada: "1. H-0037 conteudo_dois_...|"
  - tela: h0037_console_alternavel_tres_niveis
    largura: 50
    linha_observada: "1.1. Politica alternavel com modo inicial ...|"
causa_raiz:
  ramo_verboso_apenas_para_folha: true
  container_cai_no_ramo_nao_verboso: true
  envelope_da_caixa_aplica_corte_final: true
regra_violada:
  contrato_console_md_secao_21_3: conteudo_multilinha_preservado_no_verboso
  contrato_console_md_secao_21_2: marcador_so_no_nao_verboso
```

**Ponto exato em que a linha excedia a largura**: a linha do container em
modo verboso era montada pelo ramo ``else`` com
``_truncar_com_marcador(texto, content_w - len(prefixo_linha))``. Quando o
texto do container excedia a largura restante, o sufixo ``...`` ocupava a
ultima porcao visivel, descartando o restante do conteudo original.

**Correcao aplicada antes do envelope generico**: em
``tela/renderizador.py``, o ramo verboso deixou de ser condicionado a
``eh_folha``. Em modo verboso, TODO no (container ou folha) pode ocupar
varias linhas fisicas:

- o prefixo (recuo + designador + separador) e montado uma unica vez;
- ``largura_disp = max(10, content_w - len(prefixo))`` e a largura restante
  real para o conteudo;
- ``_quebrar_texto(texto, largura_disp)`` quebra o texto em palavras sem
  perder caracteres e sem introduzir ``...``;
- a primeira linha recebe ``prefixo + fragmentos[0]``;
- as linhas de continuacao recebem apenas ``indent_cont + frag``, onde
  ``indent_cont`` tem a mesma largura do prefixo.

Como o renderizador agora sempre produz linhas que cabem na largura interna
``content_w`` antes do envelope generico, o corte final ``texto[:content_w]``
da camada da caixa jamais atua em modo verboso.

**Regra distinta para verboso e nao verboso**:

```yaml
modo_verboso:
  comportamento_horizontal:
    conteudo_longo: quebrado_em_multiplas_linhas
    corte_silencioso: proibido
    marcador_de_reticencias: ausente
    conteudo_original: preservado
    largura_da_caixa: respeitada
modo_nao_verboso:
  comportamento_horizontal:
    linhas_por_item: uma
    conteudo_truncado: permitido
    marcador: "..."
```

O modo verboso nao foi convertido em nao verboso; nenhum ``...`` foi
acrescentado ao conteudo verboso para esconder o defeito.

**Tratamento das linhas de continuacao**:

```yaml
linhas_de_continuacao:
  permanecem_dentro_da_largura_interna: true
  preservam_hierarquia_visual: true
  usam_indentacao_deterministica: true
  largura_da_indentacao: igual_a_largura_do_prefixo
  nao_repetem_designador: true
  nao_perdem_caracteres: true
  nao_introduzem_reticencias: true
  nao_alteram_os_dados_originais: true
```

**Largura extremamente reduzida**: ``largura_disp = max(10, ...)`` ja e a
regra minima existente do renderizador para a quebra multilinha. Nenhuma
paginacao foi inventada, nenhuma rolagem horizontal foi criada, e o escopo
nao foi ampliado para decisoes de layout nao relacionadas.

**Preservacao do alinhamento hierarquico**: o pre-calculo da largura maxima
dos designadores do nivel raiz (``largura_desig_raiz``) foi preservado, de
modo que o alinhamento de coluna no nivel raiz (ja aprovado manualmente no
dois niveis) permanece estavel. A regressao do dois niveis e do tres niveis
e coberta por ``VERB-06`` e ``VERB-07``.

### 37.2 H0037-IMPL-QAPP7-002 — Teste integrado e relatorio

O teste ``teste_h0037_manual_001_marcador_truncamento`` nao detectava o
corte da hierarquia verbosa porque validava apenas a tabela verbosa. Foi
adicionado o teste integrado ``teste_h0037_qapp7_verb_sem_corte_silencioso``
em ``tela/teste_renderizador.py``, que atravessa a renderizacao real da
apresentacao hierarquica e da caixa (nao apenas ``_truncar_com_marcador``).

Casos cobertos (VERB-01 a VERB-13):

```yaml
VERB-01:
  modo: verboso
  esperado: texto_integral_presente_reticencias_ausentes_em_largura_ampla
VERB-02:
  modo: verboso
  esperado: quebra_de_linha_presente_corte_silencioso_ausente_reticencias_ausentes
VERB-03:
  modo: verboso
  conteudo: tokens_distintos_no_inicio_meio_e_fim
  esperado: tres_tokens_preservados_em_alguma_linha_renderizada
VERB-04:
  modo: verboso
  esperado: prefixo_hierarquico_largo_respeita_a_largura_restantante_real
VERB-05:
  modo: verboso
  esperado: continuacoes_indentacao_deterministica_designador_nao_repetido
VERB-06:
  modo: verboso
  esperado: alinhamento_do_segundo_nivel_aprovado_permanece_correto
VERB-07:
  modo: verboso
  esperado: tres_niveis_sem_eliminar_ou_misturar_niveis
VERB-08:
  modo: verboso
  largura: reduzida_reproduzindo_o_defeito_do_QA
  esperado: nenhuma_linha_interna_excede_o_espaco_disponivel
VERB-09:
  modo: verboso
  esperado: ampliacao_posterior_recalcula_conteudo_a_partir_dos_dados_originais
VERB-10:
  alternancia: verboso_nao_verboso_verboso
  esperado: cada_modo_comportamento_distinto
VERB-11:
  alvo: saida_final_apos_envelope_da_caixa
  esperado: nenhuma_linha_ultrapassa_largura_total_token_final_presente_bordas_alinhadas
VERB-12:
  tabela: preservada
  esperado: multilinha_no_verboso_compacta_com_reticencias_no_nao_verboso
VERB-13:
  conjuntos: preservados
  esperado: comportamento_aprovado_mantido
```

### 37.3 Cobertura da saida final

O teste integrado inspeciona a saida apos o envelope generico da caixa, nao
apenas uma funcao intermediaria:

```yaml
saida_final_coberta:
  nenhuma_linha_ultrapassa_a_largura_total: true   # VERB-08, VERB-11
  token_final_permanece_presente: true             # VERB-03, VERB-09, VERB-11
  corte_silencioso_ausente: true                   # VERB-02, VERB-08
  bordas_alinhadas: true                           # VERB-11
larguras_cobertas:
  - 30_reduzida_dois_niveis
  - 30_reduzida_tres_niveis
  - 50_reduzida_tres_niveis
  - 50_tabela
  - 80_conjuntos
  - 220_ampla
alternancia_coberta:
  verboso_para_nao_verboso: true
  nao_verboso_para_verboso: true
  idempotencia_no_retorno: true
IMP_0037_corrigido: true
```

### 37.4 Preservacao das correcoes aprovadas

Regressao confirmada por suite (sem reimplementacao):

```yaml
H0037_MANUAL_001:
  nao_verboso_com_reticencias: preservado        # VERB-10, VERB-12, VERB-13
  tabela_nao_verbosa_com_reticencias: preservado # VERB-12
  conjuntos_nao_verbosos_com_reticencias: preservado # VERB-13

H0037_MANUAL_002:
  Esc_primeiro: preservado                       # smoke tecnico, ESC-01..05
  ordem_dos_demais: preservada                   # ESC-02
  duplicacao: ausente                            # ESC-04

H0037_MANUAL_003:
  V_maiusculo: funcional                         # TECLA-01, TECLA-03
  v_minusculo: funcional                         # TECLA-02, TECLA-04
  telas_fixas: inertes                           # TECLA-05, TECLA-06
```

``demo/demo.py`` e a ordenacao dos chips nao foram alterados neste patch.

### 37.5 Paginacao fora do escopo

```yaml
paginacao:
  aplicavel: false
  alterada: false
```

Nenhum mecanismo historico de paginacao foi adicionado, removido ou
alterado. Nenhum teste novo exige paginacao.

### 37.6 Testes focais

```yaml
- script: tela/teste_renderizador.py
  verificacoes: 1290
  falhas: 0
  codigo_saida: 0
- script: demo/teste_demo_console_modos.py
  verificacoes: 80
  falhas: 0
  codigo_saida: 0
```

### 37.7 Suite canonica completa

| Script | Verificacoes | Falhas | Codigo de saida |
|---|---|---|---|
| ``tela/teste_loader.py`` | 512 | 0 | 0 |
| ``tela/teste_modelo.py`` | 186 | 0 | 0 |
| ``tela/teste_renderizador.py`` | 1290 | 0 | 0 |
| ``tela/teste_distribuicao_matricial.py`` | 36 | 0 | 0 |
| ``demo/teste_demo.py`` | 363 | 0 | 0 |
| ``demo/teste_diagnostico.py`` | 48 | 0 | 0 |
| ``demo/teste_demo_distribuicao.py`` | 109 | 0 | 0 |
| ``demo/teste_explorar_barra_de_menus.py`` | 38 | 0 | 0 |
| ``demo/teste_demo_console.py`` | 116 | 0 | 0 |
| ``demo/teste_demo_console_modos.py`` | 80 | 0 | 0 |
| **Total** | **2778** | **0** | todos zero |

10 scripts, 2778 verificacoes (acima do baseline de 2741 do setimo patch),
0 falhas. Acumulado deste patch: +37 verificacoes em
``tela/teste_renderizador.py`` (1253 -> 1290) relativas a VERB-01..13.

### 37.8 Smoke tecnico pos-patch

```yaml
hierarquia_verbosa:
  largura_reduzida:
    corte_silencioso: false
    reticencias: false
    quebra_em_linhas: true
  larguras_reduzidas_testadas:
    dois_niveis_em_30: sem_marcador
    tres_niveis_em_30: sem_marcador
    tres_niveis_em_50: sem_marcador

hierarquia_nao_verbosa:
  truncamento:
    marcador: "..."

chips:
  Esc_primeiro: true
  telas_alternaveis_V_presente: true
  telas_fixas_V_ausente: true

teclas:
  V: funcional
  v: funcional
  telas_fixas: inertes

smoke_nao_visual: tecnico
aprovacao_visual: nao_declarada
```

### 37.9 Arquivos alterados neste patch

```text
tela/renderizador.py
tela/teste_renderizador.py
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
```

Nenhum arquivo fora da lista autorizada foi alterado.
``docs/adr/``, ``docs/contratos/``, ``docs/handoff/``, ``docs/NOMENCLATURA.md``,
``docs/adr/INDICE_ADR.md``, ``config/telas/demo/``, ``demo/``,
``tela/loader.py``, ``tela/teste_loader.py``, ``tela/modelo.py`` e
``tela/teste_modelo.py`` permanecem intocados. Os relatorios de QA e o
relatorio manual nao foram alterados.

### 37.10 Higiene e estado Git

```yaml
git:
  branch: master
  head: f6982d08640af1762b8e0e8814b6e90c9421538e
  diff_check: sem_erros
  stage: vazio
  commit_novo: inexistente
  push: inexistente
arquivos_fora_da_lista_alterados_pelo_patch: nenhum
relatorios_QA_alterados: nenhum
relatorio_manual_alterado: false
artefatos_transitorios_restantes: nenhum
```

### 37.11 Validacao manual

```text
REVALIDACAO_MANUAL_PENDENTE_USUARIO
```

Permanece pendente — uma nova rodada de validacao manual em TTY real
executada pelo usuario e necessaria. O implementador nao declarou aprovacao
visual.

### 37.12 Necessidade de novo QA

A implementacao corrigida apos o QA pos-validacao manual aguarda novo QA
independente (``QA_POS_PATCH_IMPLEMENTACAO``) sobre os dois achados
tratados (``H0037-IMPL-QAPP7-001`` e ``H0037-IMPL-QAPP7-002``), antes da
revalidacao manual pelo usuario.

### 37.13 Conclusao

```text
implementacao corrigida apos QA pós-validação manual e aguardando novo QA independente
```

A apresentacao hierarquica em modo verboso nao sofre mais corte horizontal
silencioso: nos container agora sao quebrados em linhas como os nos folha,
preservando o conteudo original e o alinhamento hierarquico, sem marcador
artificial ``...``. O modo nao verboso continua usando ``...`` em
hierarquia, tabela e conjuntos. ``[Esc]`` permanece o primeiro chip e ``V``
/``v`` continuam funcionais nas telas alternaveis e inertes nas telas
fixas. A paginacao permanece fora do escopo. Nenhuma aprovacao e declarada.
