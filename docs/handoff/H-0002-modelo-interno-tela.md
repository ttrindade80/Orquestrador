---
name: H-0002-modelo-interno-tela
description: Handoff de implementação do modelo interno normalizado de tela — camada estruturada sobre o dict retornado pelo loader H-0001
metadata:
  type: handoff_implementacao
  status: READY_FOR_IMPLEMENTATION
  id: H-0002
  data_criacao: 2026-07-07
rastreabilidade:
  contrato_alvo: "docs/contratos/contrato_tela_json.md"
  adr_relacionadas:
    - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
    - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
  issues_relacionadas: []
  handoffs_anteriores:
    - docs/handoff/H-0001-loader-validador-tela-json.md
---

# H-0002 — Modelo interno normalizado de tela

## Ordem de autoridade

1. `docs/contratos/contrato_processo_desenvolvimento.md`
2. `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`
3. `docs/adr/ADR-0009-caminho-formato-jsons-tela.md`
4. `docs/contratos/contrato_tela_json.md`
5. `docs/contratos/contrato_composicao_corpo.md`
6. `docs/contratos/contrato_lancador.md`
7. `docs/contratos/contrato_console.md`
8. `docs/contratos/contrato_chip.md`
9. `docs/contratos/contrato_barra_de_menus.md`
10. `docs/handoff/H-0001-loader-validador-tela-json.md`
11. Este handoff

Se houver conflito entre este handoff e qualquer artefato acima, bloquear e
registrar a divergência. Este handoff não pode criar regra nova que contradiga
nenhum dos artefatos acima.

---

## Contexto

O H-0001 foi implementado e aprovado (ver `docs/relatorios/IMP-0001-loader-validador-tela-json.md`,
status `IMPLEMENTED_POS_QA`). O pacote `tela/` contém:

```
tela/__init__.py       — marcador de pacote (vazio)
tela/loader.py         — loader/validador macro de tela.json
tela/teste_loader.py   — diagnóstico verificável (37 verificações, todas passando)
```

O `loader.py` implementa `carregar_tela(caminho_base, id_tela) -> dict`, que
valida a estrutura macro e retorna um dicionário plano com os campos mínimos
da tela carregada.

O dicionário retornado pelo H-0001 tem a forma:

```python
{
    "id": str,
    "schema": str,
    "cabecalho": dict,
    "corpo": {
        "arranjo": str | None,
        "elementos": [{"id": str, "tipo": str, ...campos_inertes}],
    },
    "barra_de_menus": dict,
    "_raw": dict,
}
```

Essa representação é funcional, mas não estruturada: todos os campos são
dicts genéricos. Etapas futuras de renderização precisarão de acesso tipado
e separado a cada região, a cada elemento do corpo e a cada campo relevante
— sem operar sobre o JSON bruto diretamente.

O H-0002 especifica a implementação de uma camada de **modelo interno
normalizado** que envolve o resultado do loader em uma estrutura Python
explícita, acessível e auditável.

### Estado atual de pendências documentais relevantes

As mesmas pendências declaradas no H-0001 continuam ativas e inertes:

- **DOC-B008**: tipos internos de item de `console` não definidos; campos
  `origem_dados` e `regra_geracao_itens` do `console_principal` marcados
  como `pendente`.
- **DOC-B009**: registry completo de ações e tipos de chip não fechado;
  ações dos chips são referências declarativas conceituais provisórias.
- **`lancador_principal.itens`**: lista vazia; itens e `tela_destino`
  pendentes de definição das telas do sistema.
- **`bindings`**: declarados apenas como nota pendente DOC-B008/DOC-B009.
- **`referencias_de_acoes`**: status `pendente_DOC-B009`.

O modelo interno implementado neste handoff **não deve tratar essas
pendências como erro**. Elas são declaração inerte — o modelo as carrega e
preserva sem executar, resolver, validar funcionalmente ou rejeitar.

---

## Objetivo

Implementar uma camada de modelo interno normalizado da tela, capaz de:

1. receber o dicionário produzido por `carregar_tela` (H-0001) e construir
   uma estrutura Python explícita com campos acessíveis por nome;
2. identificar a tela carregada por `id` e `schema`;
3. expor o `cabecalho` como campo estruturado;
4. expor o `corpo` com seu `arranjo` e sua lista de `elementos`;
5. expor cada elemento do corpo com `id`, `tipo` e demais campos preservados
   como dados inertes;
6. identificar cada elemento do corpo por `id` e `tipo`, sem executar nenhuma
   semântica adicional;
7. rejeitar tipos desconhecidos, preservando a regra do H-0001 (a rejeição
   ocorre no loader, antes do modelo ser construído — o modelo nunca recebe
   elemento com tipo inválido);
8. expor a `barra_de_menus` como campo estruturado;
9. preservar chips, bindings, filtros, referencias_de_acoes e demais
   declarações ainda inertes, sem executá-las;
10. preservar campos pendentes sem criar semântica nova;
11. produzir diagnóstico textual ou serializável para teste e auditoria.

---

## Escolha arquitetural — estrutura do modelo

O executor deve implementar o modelo usando **`dataclass` da biblioteca
padrão do Python** (`dataclasses.dataclass`). Esta é a escolha definida por
este handoff — não cabe ao executor escolher outra estrutura sem
`ARCHITECTURE_REVIEW_REQUIRED`.

Justificativa da escolha:
- `dataclass` é stdlib Python (sem dependência externa);
- declara campos explicitamente com tipo, tornando a estrutura auditável;
- `__repr__` automático serve como diagnóstico imediato;
- não impõe overhead nem acoplamento desnecessário.

### Estrutura de dataclasses esperada

```python
from dataclasses import dataclass, field
from typing import Any

@dataclass
class ElementoCorpo:
    id: str
    tipo: str           # um de: "console", "lancador", "dashboard"
    _campos_inertes: dict = field(default_factory=dict, repr=False)
    # Contém todos os demais campos do elemento tal como vieram do JSON,
    # preservados sem interpretação, sem execução, sem semântica nova.

@dataclass
class Corpo:
    arranjo: str | None
    elementos: list  # lista de ElementoCorpo

@dataclass
class ModeloTela:
    id: str
    schema: str
    cabecalho: dict                  # conteúdo completo do cabecalho (inerte)
    corpo: Corpo
    barra_de_menus: dict             # conteúdo completo carregado como-está
    _raw: dict = field(repr=False)   # JSON original completo para auditoria
```

O executor pode adicionar métodos auxiliares (`diagnostico()`, `elementos_por_tipo()`,
`elemento_por_id()`) desde que esses métodos sejam somente leitura e não
criem semântica nova, não ativem bindings, não executem ações e não
resolvam campos pendentes.

O executor **não pode**:
- criar campos de estado de runtime no modelo (cursor, página, filtro
  ativo, seleção, foco);
- criar método que altere o JSON ou o `_raw`;
- criar método que resolva `tela_destino`, `origem_dados` ou ações;
- criar subclasses diferentes de `ElementoCorpo` por tipo (`ConsoleElemento`,
  `LancadorElemento`, etc.) — não existe taxonomia de subclasses neste handoff;
- introduzir herança, metaclasses ou protocolo Python não previsto aqui.

### Função pública de construção

```python
def construir_modelo(tela_raw: dict) -> ModeloTela:
    """Constrói ModeloTela a partir do dict retornado por carregar_tela.

    Não valida novamente a estrutura macro — essa responsabilidade pertence
    ao loader (H-0001). Constrói a estrutura tipada a partir dos campos
    já validados.

    Parâmetros:
        tela_raw: dict retornado por carregar_tela(caminho_base, id_tela).

    Retorna:
        ModeloTela com campos acessíveis por nome.

    Lança:
        ModeloTelaErro se o dict de entrada não tiver o formato mínimo
        esperado (ausência de chave que o loader deveria ter produzido).
    """
```

A função `construir_modelo` **não chama** `carregar_tela` internamente.
Ela recebe o dict já produzido pelo loader e constrói o modelo a partir dele.
O pipeline completo é responsabilidade do chamador:

```python
tela_raw = carregar_tela(caminho_base, "orquestrador")
modelo = construir_modelo(tela_raw)
```

---

## Arquivos permitidos

O executor pode criar ou alterar **somente** os arquivos abaixo, todos
relativos à raiz do repositório de scripts
(`/home/tiago/Dropbox/UFRGS/Survey/versao_0_1/scripts`):

```
tela/modelo.py               — módulo do modelo interno (CRIAR)
tela/teste_modelo.py         — diagnóstico verificável do modelo (CRIAR)
tela/__init__.py             — pode ser atualizado para reexportar ModeloTela
                               e construir_modelo se desejado (OPCIONAL)
tela/loader.py               — SOMENTE para adicionar importação ou reexportação
                               conveniente de ModeloTela/construir_modelo;
                               a função carregar_tela e as exceções existentes
                               NÃO PODEM ser alteradas em comportamento
tela/teste_loader.py         — SOMENTE para manter ou ampliar — NUNCA reduzir
                               verificações; todos os 37 critérios do H-0001
                               devem continuar passando
docs/relatorios/IMP-0002-modelo-interno-tela.md   — relatório (CRIAR)
```

**Regra para `loader.py`**: o executor pode adicionar código ao final do
arquivo (imports, reexportações), mas não pode modificar nenhuma linha
existente. A função `carregar_tela` deve permanecer byte-a-byte idêntica
ao que foi entregue no H-0001, salvo adição de importação no topo ou
reexportação no final que não altere o comportamento observável.

---

## Arquivos proibidos

O executor **não pode** criar, alterar, renomear, mover ou remover nenhum
arquivo além dos listados na seção anterior. São especificamente proibidos:

```
docs/NOMENCLATURA.md
docs/INDICE.md
docs/backlog.md
docs/issues.md
docs/contratos/
docs/adr/
docs/handoff/
docs/templates/
config/
```

Se a implementação do H-0002 exigir alterar contrato, ADR, nomenclatura,
índice, configuração, backlog ou qualquer decisão documental, o executor
deve parar imediatamente com:

```
ARCHITECTURE_REVIEW_REQUIRED
```

e explicar objetivamente o que falta para desbloquear.

---

## Fora de escopo obrigatório

O H-0002 **não implementa** nenhum dos itens abaixo. O executor que
tentar implementar qualquer um deles viola este handoff:

- renderer de qualquer região da tela;
- navegação real entre telas;
- execução de ações declaradas em chips;
- registry de ações (`referencias_de_acoes`);
- resolução de `bindings`;
- ativação de filtros funcionais;
- paginação funcional;
- seleção funcional;
- alteração de estilo em runtime;
- dashboard dinâmico com dados reais;
- validação funcional de `tela_destino`;
- resolução funcional de `origem_dados`;
- subclasses específicas por tipo de elemento do corpo (`ConsoleElemento`,
  `LancadorElemento`, `DashboardElemento`);
- registry de tipos de elemento;
- tipos internos completos de item do `console` (DOC-B008);
- mudança de estilo em runtime;
- execução de chips;
- alteração de JSON em runtime.

---

## Tarefas do executor

Executar na seguinte ordem, verificando cada tarefa antes de passar à próxima:

**Tarefa 1 — Criar `tela/modelo.py`**

Criar o arquivo com:
- classes `ModeloTelaErro` (exceção base), `ElementoCorpo`, `Corpo` e
  `ModeloTela` conforme a estrutura definida na seção "Escolha arquitetural";
- função pública `construir_modelo(tela_raw: dict) -> ModeloTela`;
- método `diagnostico(self) -> str` em `ModeloTela` que retorne representação
  textual auditável contendo ao menos: `id`, `schema`, `corpo.arranjo`,
  lista de elementos com `id` e `tipo` de cada um;
- constante `TIPOS_CORPO_VALIDOS` (pode importar de `tela.loader` ou
  redeclará-la — preferir importar para evitar divergência);
- apenas biblioteca padrão do Python (`dataclasses`, `typing`).

**Tarefa 2 — Criar `tela/teste_modelo.py`**

Criar script de diagnóstico executável via `python tela/teste_modelo.py` que:
- define `sys.dont_write_bytecode = True` antes de qualquer import;
- carrega `config/telas/orquestrador.json` via `carregar_tela` (H-0001) e
  depois chama `construir_modelo`;
- verifica que o modelo resultante tem `id == "orquestrador"`;
- verifica que `modelo.schema == "tela.v1"`;
- verifica que `modelo.cabecalho` é um dict com `titulo` e `descricao`;
- verifica que `modelo.corpo.arranjo == "sobreposto"`;
- verifica que `modelo.corpo.elementos` é uma lista com 3 itens;
- verifica que cada elemento tem `id` e `tipo` acessíveis por atributo;
- verifica que os tipos presentes são `{console, dashboard, lancador}`;
- verifica que `elemento._campos_inertes` preserva os campos adicionais
  sem executá-los (ex.: `origem_dados` com `referencia == "pendente"`
  está presente e inerte);
- verifica que `modelo.barra_de_menus` é um dict não vazio;
- verifica que `modelo._raw` preserva o JSON original completo;
- verifica que `modelo.diagnostico()` retorna string não vazia contendo `id`;
- cobre ao menos um caso de erro: `construir_modelo({})` levanta `ModeloTelaErro`;
- imprime resultado de cada verificação (PASSOU / FALHOU);
- retorna código de saída 0 se todos passaram, 1 se algum falhou;
- remove quaisquer arquivos temporários criados durante os testes.

**Tarefa 3 — Executar e confirmar `tela/teste_loader.py`**

Executar `python tela/teste_loader.py` e confirmar que todas as 37 verificações
do H-0001 continuam passando. Se alguma falhar, é bloqueio imediato:
registrar `BLOCKED` com descrição antes de continuar.

**Tarefa 4 — Verificar ausência de bytecode**

Confirmar que nenhum `__pycache__` nem `.pyc` foi gerado:

```bash
find tela -type d -name '__pycache__'
find tela -type f -name '*.pyc'
```

Ambos devem retornar vazio.

**Tarefa 5 — Verificar JSONs de configuração**

```bash
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
python -m json.tool config/estilo.json >/dev/null && echo "estilo.json OK"
```

**Tarefa 6 — Verificar Git**

```bash
git status --short
git diff --stat
```

Confirmar que nenhum arquivo fora do escopo foi criado ou alterado.

**Tarefa 7 — Criar relatório `docs/relatorios/IMP-0002-modelo-interno-tela.md`**

Produzir o relatório conforme a seção "Relatório obrigatório" deste handoff,
usando como referência o template `docs/templates/TEMPLATE_RELATORIO_IMPL.md`
e o relatório anterior `docs/relatorios/IMP-0001-loader-validador-tela-json.md`
como modelo de nível de detalhe esperado.

---

## Invariantes herdados do H-0001

O H-0002 não pode enfraquecer nenhum invariante do H-0001. Devem continuar
válidos após a implementação do H-0002:

- JSON inválido gera `TelaJsonInvalido` antes de qualquer construção de modelo;
- ausência de `schema` gera `TelaCampoObrigatorioAusente(campo="schema")`;
- ausência de `id` gera `TelaCampoObrigatorioAusente(campo="id")`;
- ausência de `cabecalho` gera `TelaCampoObrigatorioAusente(campo="cabecalho")`;
- ausência de `corpo` gera `TelaCampoObrigatorioAusente(campo="corpo")`;
- ausência de `barra_de_menus` gera `TelaCampoObrigatorioAusente(campo="barra_de_menus")`;
- `corpo` sem `elementos` válidos gera `TelaCampoObrigatorioAusente` ou
  `TelaEstruturaInvalida`;
- elemento de corpo sem `id` gera `TelaElementoSemId`;
- elemento de corpo sem `tipo` gera `TelaElementoSemTipo`;
- tipo fora de `console`, `lancador`, `dashboard` gera `TelaTipoDesconhecido`;
- nenhuma ação real é executada;
- nenhum binding é ativado;
- nenhum estado de runtime é gravado no JSON;
- `config/telas/orquestrador.json` não é alterado;
- `config/estilo.json` não é alterado;
- nenhum `__pycache__` nem `.pyc` permanece após os testes.

Os 37 critérios de `tela/teste_loader.py` devem todos continuar passando.

---

## Campos pendentes e inertes

O executor deve garantir que os seguintes campos sejam preservados em
`_campos_inertes` de `ElementoCorpo` e em `_raw` de `ModeloTela`, como
declaração inerte — nunca executados, nunca resolvidos, nunca validados
funcionalmente, nunca rejeitados por incompletude:

```
bindings
referencias_de_acoes
filtros
chips (lista completa da barra_de_menus)
tela_destino (qualquer valor, incluindo "pendente")
origem_dados (qualquer valor, incluindo {"referencia": "pendente"})
regra_geracao_itens
itens vazios de lancador
campos com valor "pendente" (string ou dict)
```

O executor não pode:
- atribuir semântica nova a esses campos;
- ativar comportamento a partir deles;
- resolver `tela_destino`;
- executar ação, aplicar filtro, navegar, paginar ou selecionar com base
  nesses campos.

---

## Critérios de aceite

Os critérios abaixo devem ser verificados um a um antes de considerar a
implementação concluída.

### Modelo construído corretamente

- [ ] `construir_modelo(carregar_tela(base, "orquestrador"))` retorna
      `ModeloTela` sem erro.
- [ ] `modelo.id == "orquestrador"`.
- [ ] `modelo.schema == "tela.v1"`.
- [ ] `modelo.cabecalho` é acessível como atributo e é um dict com ao
      menos os campos `titulo` e `descricao`.
- [ ] `modelo.corpo` é um objeto `Corpo` com atributos `arranjo` e
      `elementos`.
- [ ] `modelo.corpo.arranjo == "sobreposto"`.
- [ ] `modelo.corpo.elementos` é uma lista com exatamente 3 itens.
- [ ] Cada elemento de `modelo.corpo.elementos` é um `ElementoCorpo` com
      atributos `id` e `tipo` acessíveis por nome.
- [ ] Os valores de `tipo` presentes são `{console, dashboard, lancador}`.
- [ ] `modelo.barra_de_menus` é acessível como atributo e é um dict não vazio.
- [ ] `modelo._raw` preserva o conteúdo JSON original completo.

### Elementos do corpo separados e acessíveis

- [ ] O elemento com `id == "console_principal"` e
      `tipo == "console"` é acessível em `modelo.corpo.elementos`.
- [ ] O elemento com `id == "dashboard_info"` e
      `tipo == "dashboard"` é acessível em `modelo.corpo.elementos`.
- [ ] O elemento com `id == "lancador_principal"` e
      `tipo == "lancador"` é acessível em `modelo.corpo.elementos`.

### Campos pendentes preservados inertes

- [ ] `console_principal._campos_inertes["origem_dados"]["referencia"] == "pendente"`
      (ou equivalente, dependendo da estrutura): campo preservado sem erro.
- [ ] `lancador_principal._campos_inertes["itens"] == []`: lista vazia
      preservada sem erro.
- [ ] `modelo.barra_de_menus` contém `chips` com `chip_estilo` cujo
      `acao.tela_destino == "pendente"`: preservado sem erro.
- [ ] `modelo._raw["bindings"]` é preservado como dict inerte.
- [ ] `modelo._raw["referencias_de_acoes"]` é preservado como dict inerte.
- [ ] `modelo._raw["filtros"]` é preservado como lista inerte.

### Diagnóstico

- [ ] `modelo.diagnostico()` retorna string não vazia.
- [ ] A string de diagnóstico contém `id`, `schema` e ao menos a lista de
      elementos com `id` e `tipo` de cada um.

### Erros esperados

- [ ] `construir_modelo({})` levanta `ModeloTelaErro` (ou subclasse).
- [ ] `construir_modelo(carregar_tela(base, "orquestrador"))` não levanta
      exceção quando o JSON é válido e o loader já validou.

### Invariantes do H-0001 preservados

- [ ] `python tela/teste_loader.py` retorna código de saída 0 com todas as
      37 verificações passando.
- [ ] Nenhuma exceção do loader (`TelaArquivoNaoEncontrado`,
      `TelaJsonInvalido`, `TelaCampoObrigatorioAusente`,
      `TelaIdNaoCoincideComArquivo`, `TelaIdIncorreto`,
      `TelaEstruturaInvalida`, `TelaElementoSemId`, `TelaElementoSemTipo`,
      `TelaTipoDesconhecido`) foi removida ou alterada em comportamento.

### Integridade dos arquivos

- [ ] `config/telas/orquestrador.json` é JSON válido:
      `python -m json.tool config/telas/orquestrador.json` retorna OK.
- [ ] `config/estilo.json` é JSON válido:
      `python -m json.tool config/estilo.json` retorna OK.
- [ ] Nenhum `__pycache__` nem `.pyc` presente em `tela/` após execução
      dos testes.
- [ ] Nenhum arquivo fora dos listados em "Arquivos permitidos" foi criado
      ou alterado (`git status --short` confirma).
- [ ] Relatório `docs/relatorios/IMP-0002-modelo-interno-tela.md` criado
      e classifica o resultado como `APROVADO`, `APROVADO_COM_RESSALVAS`
      ou `BLOQUEADO`.

---

## Comandos de verificação esperados

Executar a partir do diretório raiz do repositório de scripts
(`/home/tiago/Dropbox/UFRGS/Survey/versao_0_1/scripts`):

```bash
# Verificar integridade dos JSONs de configuração
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
python -m json.tool config/estilo.json >/dev/null && echo "estilo.json OK"

# Verificar que testes do H-0001 continuam passando
python tela/teste_loader.py

# Verificar o novo módulo de modelo (a ser criado)
python tela/teste_modelo.py

# Verificar ausência de bytecode
find tela -type d -name '__pycache__' -o -type f -name '*.pyc'

# Verificar Git
git status --short
git diff --stat
```

Todos os comandos acima devem produzir saída limpa (sem erro, sem bytecode,
sem arquivo fora do escopo). O relatório deve incluir a saída real de cada
um desses comandos.

---

## Relatório obrigatório

O executor deve criar:

```
docs/relatorios/IMP-0002-modelo-interno-tela.md
```

usando o template `docs/templates/TEMPLATE_RELATORIO_IMPL.md` como
referência de estrutura.

O relatório deve conter obrigatoriamente:

1. **Objetivo do H-0002**: resumo do que foi especificado.
2. **Arquivos criados ou alterados**: lista completa com caminho relativo
   à raiz do repositório.
3. **Modelo interno criado**: descrição das classes implementadas,
   com os campos de cada uma.
4. **Validações do H-0001 preservadas**: evidência de que os 37 critérios
   do H-0001 continuam passando (saída de `python tela/teste_loader.py`).
5. **Comportamento deliberadamente não implementado**: lista dos itens
   fora de escopo que foram preservados como declaração inerte.
6. **Pendências preservadas**: lista dos campos pendentes (DOC-B008,
   DOC-B009) que foram carregados como declaração inerte sem execução.
7. **Comandos de verificação executados**: saída real de todos os comandos
   listados na seção anterior.
8. **Resultado final**:
   - `APROVADO`: todos os critérios de aceite foram verificados;
   - `APROVADO_COM_RESSALVAS`: critérios atendidos, com ressalvas menores
     documentadas;
   - `BLOQUEADO`: impedimento que impede conclusão — descrever o bloqueio
     completo.

**O executor não deve fazer commit.**

---

## Condições de bloqueio

O executor deve parar imediatamente e retornar status `BLOCKED` ou
`ARCHITECTURE_REVIEW_REQUIRED` se:

1. A implementação exigir decisão sobre qualquer campo pendente de
   DOC-B008 ou DOC-B009 além do que está descrito neste handoff.
2. A implementação exigir criar arquivo fora dos listados em "Arquivos
   permitidos".
3. A implementação exigir alterar o comportamento observável de
   `carregar_tela` ou de qualquer exceção do H-0001.
4. A implementação exigir criar subclasse específica por tipo de elemento
   do corpo (`ConsoleElemento`, `LancadorElemento`, `DashboardElemento`)
   ou qualquer hierarquia de tipos não prevista aqui.
5. A implementação exigir alterar contrato, ADR, nomenclatura, índice,
   configuração, backlog ou qualquer arquivo normativo.
6. Qualquer verificação do H-0001 (`python tela/teste_loader.py`) falhar
   após qualquer mudança feita neste ciclo.
7. For necessário introduzir dependência externa (além da stdlib Python).
8. For necessário criar lógica de estado de runtime (cursor, página,
   filtro ativo, seleção, foco) no modelo.
9. For necessário resolver `tela_destino`, `origem_dados` ou qualquer
   ação declarativa como parte da construção do modelo.

---

## Instrução explícita ao executor

**Você deve parar imediatamente e retornar `BLOCKED` ou
`ARCHITECTURE_REVIEW_REQUIRED` se** qualquer das condições de bloqueio
acima for atingida.

**Você não deve:**
- preencher lacunas de especificação com decisão local;
- usar inferência sobre o sistema para além do que os contratos permitem;
- fazer commit do resultado;
- alterar qualquer arquivo fora do escopo aprovado;
- modificar o comportamento de `carregar_tela` ou das exceções do H-0001;
- criar lógica de runtime, navegação, execução ou resolução de pendências.
