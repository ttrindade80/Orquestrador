# RELATORIO_LEVANTAMENTO_BLOQUEIO_H-0024_JSON_ALTURA_MINIMA_STASH

## 1. Identificacao

Levantamento tecnico e documental neutro sobre o bloqueio do H-0024 apos retorno
`ARCHITECTURE_REVIEW_REQUIRED`, considerando a regra processual explicita do
usuario sobre alteracoes JSON em handoffs.

Data do levantamento: 2026-07-11.

Branch/HEAD de referencia:

```text
branch: master
HEAD: 3332773a3f10e716115a164148af323fa86e608f
mensagem: feat: implementa redimensionamento reativo da TUI
```

Status deste levantamento: `LEVANTAMENTO_CONCLUIDO`.

Proxima categoria unica: `BLOCKED_USER_DECISION`.

## 2. Escopo

Este levantamento:

- verificou o estado Git/stash atual;
- leu os artefatos H-0024/QA/IMP-0025 e as autoridades aplicaveis;
- localizou o JSON real usado pelo cenario de `tela/teste_demo.py`;
- comprovou a cadeia de carregamento;
- analisou a colisao entre ausencia de `corpo.distribuicao`, divisao igual,
  expectativa historica de regressao e necessidade possivel de alterar JSON;
- executou as quatro suites baseline no HEAD restaurado;
- criou somente este relatorio.

Nao foram alterados JSON, codigo, testes, handoff, ADR, contratos,
documentacao normativa, stash, stage ou historico Git.

## 3. Regra explicita do usuario

Autoridade direta para este ciclo:

```text
Qualquer alteracao necessaria em JSON para a implementacao de um handoff
deve fazer parte do proprio handoff.
```

Consequencia aplicada neste levantamento: se uma alteracao no JSON real for
necessaria para entregar a implementacao, o H-0024 precisa listar o JSON como
arquivo alteravel, declarar a mudanca no escopo positivo, especificar criterios
de aceite/testes e possuir autoridade suficiente para modo e valores. A regra
processual nao escolhe modo nem valores.

## 4. Estado Git e stash

Comandos obrigatorios executados antes da analise normativa:

```text
$ git status --short
?? docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md
?? docs/relatorios/IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_VERTICAL_PERCENTUAL_FRACAO.md
?? docs/relatorios/RELATORIO_QA_H-0024_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0024_HANDOFF.md
```

```text
$ git status
On branch master
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md
	docs/relatorios/IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md
	docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_VERTICAL_PERCENTUAL_FRACAO.md
	docs/relatorios/RELATORIO_QA_H-0024_HANDOFF.md
	docs/relatorios/RELATORIO_QA_POS_PATCH_H-0024_HANDOFF.md

nothing added to commit but untracked files present (use "git add" to track)
```

```text
$ git branch --show-current
master
```

```text
$ git rev-parse HEAD
3332773a3f10e716115a164148af323fa86e608f
```

```text
$ git log -1 --oneline
3332773 feat: implementa redimensionamento reativo da TUI
```

```text
$ git diff --check
<sem saida>
```

```text
$ git diff --stat
<sem saida>
```

```text
$ git diff --name-only
<sem saida>
```

```text
$ git diff --cached --stat
<sem saida>
```

```text
$ git diff --cached --name-only
<sem saida>
```

```text
$ git stash list
stash@{0}: pre-H-0022 recuperado apos drop acidental
```

```text
$ git reflog show stash 2>/dev/null || true
21f98d0 stash@{0}: pre-H-0022 recuperado apos drop acidental
```

Confirmacoes:

| Item | Resultado |
|---|---|
| Branch | `master` |
| HEAD | `3332773a3f10e716115a164148af323fa86e608f` |
| Stage | vazio |
| Arquivos rastreados modificados | nenhum |
| Arquivos nao rastreados | 5 artefatos H-0024/QA/IMP ja existentes |
| Marcas de conflito | nenhuma localizada por `rg` |
| Indice com conflitos | `git ls-files -u` sem saida |
| Operacao Git em andamento | nenhum sentinela `MERGE_HEAD`, `CHERRY_PICK_HEAD`, `REVERT_HEAD`, `rebase-*`, `BISECT_LOG` |
| `tela/demo.py` | sem diff contra HEAD |
| `tela/teste_demo.py` | sem diff contra HEAD |
| Stash atual | referencia existe |
| Hash do stash | `21f98d0f4a479d72e6df21b1dca1511c3ad38937` |
| Identidade do stash informado | coincide exatamente com `21f98d0f4a479d72e6df21b1dca1511c3ad38937` |

Conclusao: estado seguro para analise. Nao ha `BLOCKED_REPOSITORY_STATE`.

## 5. Arquivos temporariamente afetados pela intercorrencia

Segundo a intercorrencia informada pelo usuario, os arquivos temporariamente
afetados foram:

```text
tela/demo.py
tela/teste_demo.py
```

Confirmacao local:

- `git diff -- tela/demo.py tela/teste_demo.py`: sem saida;
- `git diff --cached -- tela/demo.py tela/teste_demo.py`: sem saida;
- nao ha marcas `<<<<<<<`, `=======`, `>>>>>>>` em `tela/` ou `docs/`.

Conclusao: os dois arquivos estao restaurados ao HEAD.

Observacao operacional: a execucao das suites gerou `tela/__pycache__/`, que foi
removido em seguida para preservar a regra de criar somente este relatorio. O
estado final nao mantem esse artefato.

## 6. Artefatos analisados

Lidos integralmente:

```text
docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md
docs/relatorios/RELATORIO_QA_H-0024_HANDOFF.md
docs/relatorios/RELATORIO_QA_POS_PATCH_H-0024_HANDOFF.md
docs/relatorios/IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md
```

Lidos nos trechos relevantes:

```text
docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md
docs/adr/ADR-0017-redimensionamento-reativo-tui.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_json_tela_minima.md
docs/NOMENCLATURA.md
```

Lidos nos trechos relevantes:

```text
tela/loader.py
tela/modelo.py
tela/renderizador.py
tela/demo.py
tela/teste_demo.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
```

## 7. JSON efetivamente usado

Caminho real:

```text
/home/tiago/Dropbox/UFRGS/Survey/versao_0_1/scripts/config/telas/orquestrador.json
```

Trecho relevante:

```json
{
  "schema": "tela.v1",
  "id": "orquestrador",
  "corpo": {
    "arranjo": "vertical",
    "elementos": [
      {
        "id": "console_principal",
        "tipo": "console",
        "titulo": "Itens"
      },
      {
        "id": "dashboard_info",
        "tipo": "dashboard",
        "titulo": "Info"
      },
      {
        "id": "lancador_principal",
        "tipo": "lancador",
        "titulo": "Navegar",
        "itens": [
          {"id": "item_destino_minimo", "chip": "d", "texto": "Destino", "tela_destino": "destino_minimo"},
          {"id": "item_grupo_minimo", "chip": "g", "texto": "Grupo Min.", "tela_destino": "grupo_minimo"}
        ]
      }
    ]
  },
  "barra_de_menus": {
    "distribuicao": {
      "modo": "horizontal_responsiva"
    }
  }
}
```

Registro factual:

| Campo | Resultado |
|---|---|
| `corpo.arranjo` | `"vertical"` |
| `corpo.distribuicao` | ausente |
| Filhos diretos | 3 |
| Ordem | `console_principal`, `dashboard_info`, `lancador_principal` |
| Tipos | `console`, `dashboard`, `lancador` |
| Distribuicao existente | somente `barra_de_menus.distribuicao`, nao `corpo.distribuicao` |
| Altura/composicao relevante | lancador tem 2 itens; barra responsiva ocupa 3 linhas em largura 42 |

## 8. Cadeia de carregamento do JSON

Comprovacao por cadeia de chamadas:

1. `tela/teste_demo.py` define `_BASE_PADRAO = Path(__file__).resolve().parent.parent`.
2. `tela/teste_demo.py::_carregar_modelo()` chama:

```python
tela_raw = carregar_tela(_BASE_PADRAO, "orquestrador")
return construir_modelo(tela_raw)
```

3. `tela/loader.py::carregar_tela(caminho_base, id_tela)` resolve:

```python
caminho_relativo = os.path.join("config", "telas", id_tela + ".json")
caminho_arquivo = base / caminho_relativo
texto = caminho_arquivo.read_text(encoding="utf-8")
dados = json.loads(texto)
```

4. Com `id_tela = "orquestrador"` e `_BASE_PADRAO` apontando para
   `/home/tiago/Dropbox/UFRGS/Survey/versao_0_1/scripts`, o arquivo lido e
   `config/telas/orquestrador.json`.
5. `tela/demo.py::renderizar_estado()` apenas repassa `largura` e `altura` ao
   renderer:

```python
return renderizar_tela(
    modelo, tipo_borda=estado["tipo_borda"], largura=largura, altura=altura
)
```

Nao ha presuncao de caminho: o caminho foi derivado da chamada real do teste.

## 9. Cenario que produz `[3,3,3]`

Cenario do teste:

```text
renderizar_estado(estado_curva, modelo, largura=42, altura=15)
```

Calculo atual da area:

```text
altura total = 15
l_cabecalho = 3
l_barra = 3
l_corpo_disponivel = 15 - 3 - 3 = 9
filhos diretos = 3
```

Pela regra de ausencia equivalente a `igual`, os pesos seriam `[1,1,1]`.
Aplicando divisao igual por maiores restos sobre 9 linhas:

```text
9 / 3 = 3
resultado = [3, 3, 3]
```

Essa parte do retorno do executor foi confirmada no reposititorio.

## 10. Necessidade de quatro linhas do lancador

Alturas naturais observaveis no renderer atual para largura 42:

| Elemento | Tipo | Linhas naturais |
|---|---:|---:|
| `console_principal` | `console` | 3 |
| `dashboard_info` | `dashboard` | 2 |
| `lancador_principal` | `lancador` | 4 |

Base tecnica:

- `_linhas_console()` retorna uma linha de conteudo `"(console)"`;
- `_linhas_dashboard()` ignora campos sem `fonte == "literal"`; no JSON real,
  os campos do dashboard estao com fonte pendente, portanto nao geram linhas;
- `_linhas_lancador()` gera uma linha por item; o JSON real tem 2 itens;
- `_caixa()` sempre produz topo + conteudo + base.

Logo:

```text
console:   topo + 1 linha + base = 3
dashboard: topo + 0 linhas + base = 2
lancador: topo + 2 linhas + base = 4
```

O `lancador` exige quatro linhas no comportamento atual porque possui dois
itens renderizados e `_caixa` nao trunca.

## 11. Local exato do `RenderizadorErro`

No HEAD atual, `tela/renderizador.py::renderizar_tela()` calcula:

```python
l_corpo_conteudo = sum(_contar_linhas(p) for p in partes[1:])
l_corpo_disponivel = altura - l_cab - l_barra
if l_corpo_conteudo > l_corpo_disponivel:
    raise RenderizadorErro(...)
```

Na implementacao tentada, segundo `IMP-0025`, a divisao `[3,3,3]` teria atribuido
3 linhas ao `lancador`, mas `_caixa` nao truncaria seu conteudo natural de 4
linhas. A soma renderizada ficaria:

```text
console 3 + dashboard 3 + lancador 4 = 10
area disponivel = 9
10 > 9 => RenderizadorErro
```

O local de erro e a guarda existente de altura insuficiente em
`renderizar_tela`, nao uma excecao nova de schema.

## 12. Expectativa de `tela/teste_demo.py`

`tela/teste_demo.py::teste_renderizar_estado_altura()` codifica:

```python
res_16 = renderizar_estado(estado_curva, modelo, largura=42, altura=15)

res_16.count("\n") == 15
res_16 == renderizar_estado(estado_curva, modelo, largura=42)
```

O comentario do teste identifica esse caso como CA-01/CA-03 de H-0015:
altura minima 15 sem preenchimento e saida identica ao comportamento natural
sem altura.

Classificacao dessa expectativa:

| Item | Classificacao |
|---|---|
| `altura=15` sem fill externo adicional | expectativa de regressao historica |
| Igualdade com `altura=None` | preservacao de implementacao H-0015 no teste |
| Forca normativa ativa contra ADR-0015/H-0024 | nao comprovada |
| Valor como requisito do H-0024 | o H-0024 manda executar `teste_demo.py` como regressao e proibe altera-lo |

A expectativa preserva uma implementacao historica. Nao foi localizada autoridade
normativa ativa igual ou superior dizendo que esse cenario real deve continuar
igual a `altura=None` apos H-0024.

## 13. Hierarquia das autoridades

Para este levantamento:

1. Regra explicita do usuario neste ciclo sobre alteracoes JSON em handoff.
2. Decisoes explicitas do usuario ja registradas em handoffs/ADRs.
3. ADRs e contratos ativos.
4. Handoff H-0024 aprovado.
5. Codigo e testes.
6. Relatorios de levantamento, QA e implementacao como evidencias, nao normas.

Ponto relevante: relatorios e codigo/testes nao criam regra normativa nova.

## 14. Analise da equivalencia ausencia/igual

Autoridades ativas:

- ADR-0015: `igual` divide a area disponivel igualmente entre filhos diretos.
- `contrato_composicao_corpo.md`: mesma regra para `igual`.
- `contrato_json_tela_minima.md`: `distribuicao` ausente e valida e equivale a
  `igual`.
- H-0024 corrigido: ausencia de `corpo.distribuicao` equivale a `modo = "igual"`
  e, com altura definida, substitui o empilhamento sequencial antigo por divisao
  igual.

Conclusao: nao ha contradicao documental ativa entre ADR/contratos sobre
ausencia/igual. A colisao aparece quando essa norma e aplicada ao JSON real e ao
teste historico que o H-0024 proibiu alterar.

Classificacao da colisao:

```text
HANDOFF_INCOMPATIVEL_COM_REGRESSAO
DECISAO_AUSENTE
```

Nao e `CONTRADICAO_DOCUMENTAL`, pois a expectativa do teste nao demonstrou
autoridade normativa igual ou superior a ADR/contratos. Tambem ha limite de
conteudo/cota: sem valores declarativos que garantam cota suficiente ao lancador
no cenario real, a guarda existente de altura insuficiente permanece aplicavel.

## 15. Opcoes declarativas ja normatizadas

### `modo = "igual"`

Autoridade suficiente para o comportamento geral:

- modo reconhecido;
- valores nao exigidos;
- pesos unitarios;
- filhos diretos na ordem declarada;
- maiores restos;
- soma das alturas igual a area disponivel;
- ausencia de `corpo.distribuicao` equivale a esse modo.

No cenario real `altura=15`, `igual` gera `[3,3,3]`, insuficiente para o
`lancador` natural de 4 linhas.

### `modo = "percentual"`

Autoridade suficiente para schema e algoritmo:

- `distribuicao.valores` obrigatorio;
- `len(valores) == len(corpo.elementos)` => 3 valores no JSON real;
- todos positivos;
- soma exatamente 100;
- associacao pela ordem dos filhos diretos:
  `console_principal`, `dashboard_info`, `lancador_principal`;
- arredondamento por maiores restos;
- linhas residuais por maiores restos; empates pela ordem declarada.

Autoridade insuficiente para este cenario:

- nao ha valor percentual exato determinado para o JSON real;
- existem multiplos percentuais validos que poderiam preservar o lancador no
  cenario de altura 15;
- a escolha altera comportamento visual e prioridade relativa entre elementos.

### `modo = "fracao"`

Autoridade suficiente para schema e algoritmo:

- `distribuicao.valores` obrigatorio;
- `len(valores) == len(corpo.elementos)` => 3 valores no JSON real;
- todos positivos;
- pesos relativos com denominador implicito pela soma;
- associacao pela ordem dos filhos diretos;
- arredondamento por maiores restos;
- linhas residuais por maiores restos; empates pela ordem declarada.

Autoridade insuficiente para este cenario:

- nao ha pesos exatos determinados para o JSON real;
- existem multiplas fracoes validas que poderiam preservar o lancador no
  cenario de altura 15;
- a escolha altera comportamento visual e prioridade relativa entre elementos.

## 16. Necessidade de alterar JSON

Respostas separadas:

| Pergunta | Resposta |
|---|---|
| 1. A alteracao do JSON e tecnicamente necessaria? | Para entregar H-0024 mantendo `tela/teste_demo.py` imutavel e sem altura minima nova, sim, e necessaria ou no minimo apropriada alterar o JSON real para deixar de cair em ausencia/igual no cenario real. |
| 2. A alteracao do JSON e apenas uma das possiveis solucoes? | Sim. Outras categorias envolveriam alterar teste/regressao, redefinir ausencia/igual, ou normatizar minimo/overflow. |
| 3. O arquivo exato ja pode ser identificado? | Sim: `config/telas/orquestrador.json`. |
| 4. O modo exato ja e determinado pelas autoridades? | Nao. `percentual` e `fracao` sao permitidos; `igual` e determinado para ausencia, mas falha no cenario real. |
| 5. Os valores exatos ja sao determinados pelas autoridades? | Nao. |
| 6. Os valores podem ser derivados mecanicamente de regra existente, sem escolha de politica? | Nao. A regra de maiores restos calcula cotas a partir de valores; ela nao escolhe os valores. |
| 7. Existem multiplas distribuicoes validas que preservariam o lancador? | Sim, ha multiplos percentuais/pesos capazes de atribuir pelo menos 4 linhas ao lancador em area 9. |
| 8. A escolha altera comportamento visual ou prioridade entre elementos? | Sim. Ela muda como linhas extras sao distribuidas em alturas maiores e como sobras/residuos sao priorizados. |
| 9. Essa escolha exigiria decisao explicita do usuario? | Sim. |
| 10. A alteracao JSON elimina a necessidade de altura minima? | Elimina para o caso conhecido se os valores escolhidos alocarem cotas suficientes; nao elimina a lacuna geral de minimo/overflow para alturas menores ou outras configuracoes. |
| 11. Ela preserva corretamente redimensionamentos menores e maiores? | Nao e determinavel sem modo/valores e testes. Para alturas menores que a soma natural observavel, alguma politica de erro/aviso/minimo continua necessaria. |
| 12. Ela apenas desloca o problema para outras alturas? | Pode deslocar, dependendo dos valores e das alturas testadas. |
| 13. Seria necessario definir minimo, overflow, rejeicao ou degradacao quando uma cota ficar menor que o conteudo? | Sim para a politica geral; H-0024 tenta usar o `RenderizadorErro` existente, mas a escolha JSON para o caso real nao define uma politica universal de cotas insuficientes. |

## 17. Modo e valores: determinados ou dependentes de decisao

Determinado:

- arquivo real: `config/telas/orquestrador.json`;
- filhos diretos e ordem;
- ausencia atual de `corpo.distribuicao`;
- efeito de ausencia como `igual`;
- calculo `[3,3,3]` para area 9;
- necessidade observavel de 4 linhas do `lancador`.

Nao determinado:

- escolher `percentual` ou `fracao`;
- escolher os tres valores;
- decidir se a distribuicao deve reproduzir exatamente alturas naturais em
  `altura=15` ou apenas evitar erro;
- decidir prioridade entre console, dashboard e lancador em alturas maiores;
- decidir comportamento para cotas menores que conteudo em outras alturas.

Conclusao: os valores dependem de decisao do usuario.

## 18. Relacao com altura minima

O executor cogitou altura minima por elemento. Evidencia normativa:

- ADR-0015 registra `minimo`, `preferido`, `maximo`, `restante` e `conteudo`
  como conceitos futuros;
- H-0024 proibe definir altura minima por elemento;
- H-0024 tambem diz que conteudo que excede a area alocada continua usando a
  politica existente: `_caixa` nao trunca e `RenderizadorErro` e levantado se o
  corpo exceder a area disponivel.

Analise:

- para o cenario especifico, uma distribuicao JSON que aloque cota suficiente ao
  lancador pode evitar a necessidade imediata de uma regra nova de altura minima;
- para a politica geral, minimo/overflow/degradacao ainda nao estao plenamente
  normatizados para todos os casos em que uma cota fica menor que o conteudo;
- portanto a alteracao JSON pode resolver o caso concreto, mas nao fecha a lacuna
  arquitetural geral.

## 19. Relacao com redimensionamento

ADR-0017 exige que novo par valido de dimensoes recalcule areas e distribuicoes
dependentes da dimensao real, sem alterar composicao declarativa. H-0024 pretende
que a distribuicao seja funcao pura da `altura` recebida por `renderizar_tela`.

Impacto do JSON:

- o JSON declararia a composicao/distribuicao;
- o renderer recalcularia cotas a cada altura;
- a escolha dos valores alteraria o resultado visual em alturas menores e maiores;
- sem valores definidos, nao e possivel afirmar preservacao correta de todos os
  redimensionamentos relevantes.

## 20. Impacto da regra nova no H-0024

Comparacao com H-0024:

| Pergunta | Resultado |
|---|---|
| H-0024 proibe `config/`? | Sim, proibe alterar `config/`. |
| H-0024 exclui o JSON real? | Sim, `config/telas/*.json` foi excluido; `config/telas/orquestrador.json` aparece apenas como leitura. |
| H-0024 exige comportamento que nao pode ser entregue sem alterar JSON? | No cenario real com `teste_demo.py` imutavel, sim, a entrega coerente exige tratar o JSON real ou mudar outra autoridade/expectativa. |
| H-0024 deveria listar o JSON como arquivo alteravel? | Sim, se a solucao escolhida for declarativa no JSON. |
| H-0024 deveria especificar a alteracao declarativa? | Sim. |
| H-0024 deveria exigir validacao sintatica do JSON? | Sim, se alterar JSON. |
| H-0024 deveria exigir testes do cenario real? | Sim, incluindo `tela/teste_demo.py` e/ou teste especifico do JSON real. |
| H-0024 deveria permitir fixture/config adicional? | Apenas se a decisao formal permitir; para o caso real, o arquivo identificado e o JSON do Orquestrador. |
| H-0024 precisaria alterar listas permitidas/proibidas? | Sim, se a solucao for JSON. |

Classificacao da omissao:

```text
DECISAO_AUSENTE
```

Motivo: o arquivo exato esta identificado e a necessidade processual de inclui-lo
no handoff e clara, mas modo e valores exatos nao estao determinados por
autoridade existente.

## 21. Matriz handoff x JSON x codigo x teste x autoridade

| Eixo | Evidencia | Estado |
|---|---|---|
| Handoff | H-0024 manda ausencia/igual dividir igualmente com altura definida | Normativo no ciclo |
| Handoff | H-0024 proibe `config/` e `tela/teste_demo.py` | Bloqueia solucao declarativa/teste dentro do escopo atual |
| JSON | `orquestrador.json` tem `corpo.arranjo="vertical"` e sem `corpo.distribuicao` | Cai em ausencia/igual |
| Codigo | loader atual nao preserva `corpo.distribuicao` | Lacuna de implementacao prevista pelo H-0024 |
| Codigo | renderer atual empilha vertical e fill externo H-0015 | Baseline historico |
| Codigo | `_caixa` nao trunca se conteudo excede `altura_alvo` | Pode gerar corpo maior que cota |
| Teste | `tela/teste_demo.py` exige `altura=15` identica a sem altura | Expectativa historica |
| Autoridade | ADR-0015/contratos definem `igual`, `percentual`, `fracao`, maiores restos | Suficiente para algoritmo |
| Autoridade | Valores do JSON real nao definidos | Decisao ausente |
| Autoridade | Minimo/overflow geral sao conceitos futuros/parciais | Lacuna geral ainda existe |

## 22. Classificacao do bloqueio

Classificacao tecnica:

```text
DECISAO_AUSENTE
```

Classificacao processual associada:

```text
HANDOFF_INCOMPATIVEL_COM_REGRESSAO
```

Justificativa:

- a norma de ausencia/igual esta clara;
- o teste historico imutavel no H-0024 preserva comportamento anterior para o
  JSON real;
- a regra nova do usuario exige que qualquer alteracao JSON necessaria esteja no
  proprio handoff;
- o H-0024 exclui o JSON real;
- o arquivo real foi identificado;
- alterar JSON e uma solucao apropriada/necessaria para conciliar o caso concreto
  sem mexer em teste nem criar minimo, mas modo e valores nao estao determinados;
- ha multiplas configuracoes validas com efeitos visuais diferentes.

Nao classificado como:

- `BLOCKED_REPOSITORY_STATE`: estado Git/stash seguro;
- `BLOCKED_EVIDENCE`: JSON, cenario, stash e artefatos comprovados;
- `CONTRADICAO_DOCUMENTAL`: nao ha divergencia ativa entre ADR/contratos sobre
  ausencia/igual;
- `PATCH_HANDOFF`: faltam modo e valores exatos determinados;
- `CRIAR_ADR`: o usuario ainda nao decidiu modo/valores.

## 23. Unica proxima categoria

```text
BLOCKED_USER_DECISION
```

Motivo: alterar o JSON real e necessario ou apropriado para resolver o caso
concreto dentro da regra nova, mas ha mais de uma configuracao valida e a escolha
de modo, valores e prioridade entre elementos precisa ser feita pelo usuario.

## 24. Testes baseline

Executados no HEAD restaurado, sem reaplicar a implementacao tentada:

| Suite | Codigo de saida | Verificacoes | Falhas |
|---|---:|---:|---:|
| `python tela/teste_loader.py` | 0 | 89 | 0 |
| `python tela/teste_modelo.py` | 0 | 56 | 0 |
| `python tela/teste_renderizador.py` | 0 | 331 | 0 |
| `python tela/teste_demo.py` | 0 | 303 | 0 |

Confirmacao de baseline: as quatro suites passam no estado restaurado ao HEAD.

## 25. Arquivos criados ou alterados

Criado por este levantamento:

```text
docs/relatorios/RELATORIO_LEVANTAMENTO_BLOQUEIO_H-0024_JSON_ALTURA_MINIMA_STASH.md
```

Nenhum JSON, codigo, teste, handoff, ADR, contrato, stash, stage ou commit foi
alterado.
