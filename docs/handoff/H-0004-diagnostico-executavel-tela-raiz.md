---
name: H-0004-diagnostico-executavel-tela-raiz
description: Handoff de implementação do ponto de entrada diagnóstico executável — prova integração H-0001 → H-0002 → H-0003 sobre a tela raiz do Orquestrador
metadata:
  type: handoff_implementacao
  status: READY_FOR_REAUDIT
  id: H-0004
  data_criacao: 2026-07-07
rastreabilidade:
  contrato_alvo: "docs/contratos/contrato_processo_desenvolvimento.md"
  adr_relacionadas:
    - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
    - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
  handoffs_anteriores:
    - docs/handoff/H-0001-loader-validador-tela-json.md
    - docs/handoff/H-0002-modelo-interno-tela.md
    - docs/handoff/H-0003-renderizador-textual-estatico.md
  issues_relacionadas: []
---

# H-0004 — Diagnóstico executável da tela raiz

## Ordem de autoridade

1. `docs/contratos/contrato_processo_desenvolvimento.md`
2. `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`
3. `docs/adr/ADR-0009-caminho-formato-jsons-tela.md`
4. `docs/handoff/H-0001-loader-validador-tela-json.md`
5. `docs/handoff/H-0002-modelo-interno-tela.md`
6. `docs/handoff/H-0003-renderizador-textual-estatico.md`
7. Este handoff

Se houver conflito entre este handoff e qualquer artefato acima, o executor
deve parar com `ARCHITECTURE_REVIEW_REQUIRED` e registrar a divergência. Este
handoff não pode criar regra nova que contradiga nenhum dos artefatos acima.

---

## Contexto

Os handoffs H-0001, H-0002 e H-0003 foram implementados e aprovados por QA.
O pacote `tela/` contém atualmente:

```
tela/__init__.py           — marcador de pacote (vazio)
tela/loader.py             — loader/validador macro (H-0001)
tela/teste_loader.py       — diagnóstico H-0001 (37 verificações, todas passando)
tela/modelo.py             — modelo interno normalizado (H-0002)
tela/teste_modelo.py       — diagnóstico H-0002 (30 verificações, todas passando)
tela/renderizador.py       — renderer textual estático (H-0003)
tela/teste_renderizador.py — diagnóstico H-0003 (39 verificações, todas passando)
```

O pipeline completo já funciona mas não tem ponto de entrada único e auditável
que o exercite de ponta a ponta. O H-0004 cria esse ponto de entrada mínimo:
uma função `gerar_diagnostico_tela` e um script executável `tela/diagnostico.py`
que percorrem a cadeia inteira e produzem saída textual determinística no stdout.

### Pipeline já estabelecido pelos handoffs anteriores

```
config/telas/orquestrador.json
    → carregar_tela(None, "orquestrador")   [tela/loader.py  — H-0001]
    → dict (tela_raw)
    → construir_modelo(tela_raw)            [tela/modelo.py  — H-0002]
    → ModeloTela
    → renderizar_tela(modelo)               [tela/renderizador.py — H-0003]
    → str
```

O H-0004 **não reimplementa** nenhuma dessas etapas. Apenas as encadeia em
um ponto de entrada verificável.

### Pendências documentais que permanecem ativas e inertes no H-0004

As mesmas pendências dos ciclos anteriores continuam inertes:

- **DOC-B008**: tipos internos de item de `console` não definidos.
- **DOC-B009**: registry completo de ações e tipos de chip não fechado.
- **`lancador_principal.itens`**: lista vazia; `tela_destino` pendente.
- **`bindings`** e **`referencias_de_acoes`**: declarados como pendentes.

O diagnóstico não deve tratar essas pendências como erro. O pipeline existente
já as preserva como declaração inerte — o H-0004 apenas chama esse pipeline.

---

## Objetivo

Criar um ponto de entrada mínimo e auditável que:

1. Execute a cadeia completa:
   `carregar_tela` → `construir_modelo` → `renderizar_tela`
   para a tela `"orquestrador"`.
2. Exponha uma função pública `gerar_diagnostico_tela(id_tela: str = "orquestrador") -> str`
   que retorne a string produzida pelo pipeline.
3. Em modo executável (`python tela/diagnostico.py`), imprima a string no
   stdout e encerre com código de saída 0.
4. Prove, por meio de teste integrado (`tela/teste_diagnostico.py`), que a
   cadeia H-0001 → H-0002 → H-0003 funciona corretamente de ponta a ponta.
5. Não implementar nenhuma lógica nova além do encadeamento descrito.

---

## Arquivos permitidos

O executor pode criar ou alterar **somente** os três arquivos abaixo, todos
relativos à raiz do repositório de scripts
(`/home/tiago/Dropbox/UFRGS/Survey/versao_0_1/scripts`):

```
tela/diagnostico.py                                   — ponto de entrada (CRIAR)
tela/teste_diagnostico.py                             — teste integrado (CRIAR)
docs/relatorios/IMP-0004-diagnostico-executavel-tela-raiz.md  — relatório (CRIAR)
```

A lista acima é exaustiva e sem exceção. Nenhum outro arquivo pode ser
criado ou alterado — incluindo os módulos herdados listados na seção
"Proibição absoluta de alteração de módulos herdados" abaixo.

O executor pode **ler** qualquer arquivo do pacote `tela/` e de `config/`
para entender o contexto, mas não pode alterá-los.

### Proibição absoluta de alteração de módulos herdados

Os arquivos abaixo são **estritamente proibidos de alteração**, sem exceção
e sem possibilidade de justificativa local:

```
tela/loader.py             — proibido de alterar (H-0001)
tela/modelo.py             — proibido de alterar (H-0002)
tela/renderizador.py       — proibido de alterar (H-0003)
tela/__init__.py           — proibido de alterar
tela/teste_loader.py       — proibido de alterar (H-0001)
tela/teste_modelo.py       — proibido de alterar (H-0002)
tela/teste_renderizador.py — proibido de alterar (H-0003)
```

Se a implementação exigir alterar qualquer um desses arquivos, o executor
deve parar imediatamente com `BLOCKED` e descrever o que exige a alteração.
Não há escape por justificativa: esses arquivos são somente leitura no H-0004.

---

## Arquivos proibidos

O executor **não pode** criar, alterar, renomear, mover ou remover nenhum
arquivo fora dos listados em "Arquivos permitidos". São especificamente
proibidos:

```
docs/NOMENCLATURA.md
docs/INDICE.md
docs/backlog.md
docs/issues.md
docs/contratos/          (qualquer arquivo)
docs/adr/                (qualquer arquivo)
docs/handoff/            (qualquer arquivo, incluindo este)
docs/templates/          (qualquer arquivo)
config/                  (qualquer arquivo)
```

Se a implementação exigir alterar qualquer contrato, ADR, nomenclatura,
índice, configuração, handoff anterior ou relatório anterior, o executor
deve parar com:

```
ARCHITECTURE_REVIEW_REQUIRED
```

e descrever objetivamente o que falta para desbloquear.

---

## Fora de escopo — proibições explícitas

O H-0004 **não implementa** nenhum dos itens abaixo. Implementar qualquer
um viola este handoff:

- loop de aplicação;
- navegação real entre telas;
- execução de ações declaradas em chips ou itens de lancador;
- registry de ações (`referencias_de_acoes`);
- resolução de `bindings`;
- ativação de filtros funcionais (`filtros[]`);
- paginação funcional;
- seleção funcional;
- registry de tipos de elemento;
- execução de chips;
- navegação por `tela_destino`;
- dashboard dinâmico com dados reais;
- mudança de estilo em runtime;
- layout final responsivo completo;
- interface interativa;
- curses, textual, rich ou qualquer biblioteca de UI;
- renderização com escape codes ANSI ou cores de terminal;
- alteração de JSON em runtime;
- qualquer estado de runtime (cursor, página, filtro ativo, seleção, foco);
- validação funcional de campos pendentes (DOC-B008 / DOC-B009).

---

## Comportamento esperado

### Função pública

```python
def gerar_diagnostico_tela(id_tela: str = "orquestrador") -> str:
```

**Módulo**: `tela/diagnostico.py`

**Contrato da função**:

| Aspecto | Regra |
|---|---|
| Entrada | `id_tela: str` — identificador da tela (padrão: `"orquestrador"`) |
| Saída | `str` — string produzida por `renderizar_tela(construir_modelo(carregar_tela(None, id_tela)))` |
| Efeitos colaterais | Nenhum — não altera JSON, não executa ação, não ativa binding, não grava arquivo |
| Determinismo | Dado o mesmo `id_tela` e o mesmo JSON em disco, sempre retorna a mesma string |
| Caminho base | Usa `None` como `caminho_base` em `carregar_tela`, o que aciona o padrão do loader (raiz do repositório de scripts) |

**Importações obrigatórias no módulo**:

```python
from tela.loader import carregar_tela
from tela.modelo import construir_modelo
from tela.renderizador import renderizar_tela
```

**Importações proibidas no módulo `tela/diagnostico.py`**:

- `import json` (não precisa ler JSON diretamente)
- `import os` (não precisa construir caminhos diretamente)
- `import pathlib` (não precisa construir caminhos diretamente)
- `subprocess`, `exec`, `eval` ou qualquer mecanismo de execução de processo

O executor pode importar `sys` exclusivamente para `sys.dont_write_bytecode`
e `sys.exit` no bloco `__main__`.

### Encadeamento do pipeline

A implementação deve seguir exatamente:

```python
def gerar_diagnostico_tela(id_tela: str = "orquestrador") -> str:
    tela_raw = carregar_tela(None, id_tela)
    modelo = construir_modelo(tela_raw)
    return renderizar_tela(modelo)
```

O executor não deve implementar lógica de encadeamento diferente, não deve
adicionar cache, não deve adicionar tratamento de exceção que engula erros,
não deve adicionar parâmetro `caminho_base` sem justificativa objetiva registrada
no relatório.

### Propagação de exceções

A função `gerar_diagnostico_tela` deve deixar as exceções dos módulos
subjacentes propagarem naturalmente para o chamador:

- `TelaArquivoNaoEncontrado`, `TelaJsonInvalido`, `TelaCampoObrigatorioAusente`,
  `TelaIdNaoCoincideComArquivo`, `TelaIdIncorreto`, `TelaEstruturaInvalida`,
  `TelaElementoSemId`, `TelaElementoSemTipo`, `TelaTipoDesconhecido`
  (do `tela.loader`, H-0001)
- `ModeloTelaErro` (do `tela.modelo`, H-0002)
- `RenderizadorErro` (do `tela.renderizador`, H-0003)

O módulo `tela/diagnostico.py` **não deve** capturar, relançar nem
transformar essas exceções.

### Modo executável

Quando executado diretamente (`python tela/diagnostico.py`), o módulo deve:

1. Importar `sys` como **primeiro import do módulo** e definir
   `sys.dont_write_bytecode = True` imediatamente a seguir — antes dos imports
   de `tela.*` — para prevenir a geração de `__pycache__`/`.pyc`.
2. Chamar `gerar_diagnostico_tela()` (sem argumento — usa padrão `"orquestrador"`).
3. Imprimir a string retornada no stdout (sem `\n` extra — a string já termina
   com `\n`, conforme o H-0003).
4. Encerrar com código de saída `0` em caso de sucesso.
5. Em caso de exceção do pipeline, deixar o traceback aparecer no stderr
   (comportamento padrão do Python) e encerrar com código de saída `1`.

Exemplo de implementação do bloco `__main__`:

```python
if __name__ == "__main__":
    resultado = gerar_diagnostico_tela()
    print(resultado, end="")
    sys.exit(0)
```

### Saída esperada para o estado atual de `config/telas/orquestrador.json`

A string abaixo é a saída **exata** esperada quando `gerar_diagnostico_tela()`
é chamada (igualdade estrita, incluindo o `\n` final). Ela é idêntica à
saída validada no H-0003:

```
TELA: orquestrador
SCHEMA: tela.v1

CABECALHO
  titulo: Orquestrador
  descricao: Tela raiz do sistema — ponto de entrada e visao consolidada do pipeline de survey

CORPO
  arranjo: sobreposto
  elementos:
    - id: console_principal | tipo: console
    - id: dashboard_info | tipo: dashboard
    - id: lancador_principal | tipo: lancador

BARRA_DE_MENUS
  chips:
    - id: chip_esc | texto: Sair
    - id: chip_paginas | texto: Páginas
    - id: chip_colunas | texto: Colunas
    - id: chip_grupos | texto: Grupos
    - id: chip_alternar | texto: Alternar
    - id: chip_navegar | texto: Navegar
    - id: chip_selecionar | texto: Selecionar
    - id: chip_enter | texto: Todos
    - id: chip_estilo | texto: Estilo
    - id: chip_verboso | texto: Verboso
    - id: chip_ajuda | texto: Ajuda
```

A string acima termina com `\n` após `    - id: chip_ajuda | texto: Ajuda`.

O executor deve usar essa string como valor de referência no teste integrado
(`_EXPECTED_ORQUESTRADOR`) e verificar igualdade estrita.

---

## Invariantes obrigatórios

O H-0004 deve preservar todos os invariantes dos handoffs anteriores:

- `config/telas/orquestrador.json` não é alterado em runtime;
- nenhuma ação é executada;
- nenhum binding é ativado;
- nenhum chip é executado;
- nenhum estado é gravado;
- nenhuma navegação ou interação é implementada;
- nenhum `__pycache__` nem `.pyc` permanece em `tela/` após os testes;
- nenhum arquivo fora do escopo aprovado é criado ou alterado;
- os testes H-0001 (37 verificações), H-0002 (30 verificações) e H-0003
  (39 verificações) continuam passando integralmente.

---

## Estrutura esperada de `tela/diagnostico.py`

```
tela/diagnostico.py
  import sys                          ← primeiro import
  sys.dont_write_bytecode = True      ← imediatamente após import sys, antes de tela.*

  from tela.loader import carregar_tela
  from tela.modelo import construir_modelo
  from tela.renderizador import renderizar_tela

  def gerar_diagnostico_tela(id_tela: str = "orquestrador") -> str:
      tela_raw = carregar_tela(None, id_tela)
      modelo = construir_modelo(tela_raw)
      return renderizar_tela(modelo)

  if __name__ == "__main__":
      resultado = gerar_diagnostico_tela()
      print(resultado, end="")
      sys.exit(0)
```

A ordem obrigatória no topo do módulo é:
1. `import sys` — único import da stdlib permitido no topo do módulo
2. `sys.dont_write_bytecode = True` — imediatamente após `import sys`
3. imports de `tela.*` — após a atribuição acima

Essa é a mesma convenção adotada por `tela/teste_loader.py`,
`tela/teste_modelo.py` e `tela/teste_renderizador.py` nos ciclos anteriores.

O executor pode ajustar a estrutura interna (ex.: adicionar docstrings), desde
que o comportamento externo seja exatamente o especificado. Nenhuma lógica
adicional é autorizada.

---

## Estrutura esperada de `tela/teste_diagnostico.py`

O script de teste deve:

- Definir `sys.dont_write_bytecode = True` **antes** de qualquer import.
- Importar apenas da biblioteca padrão, de `tela.loader`, `tela.modelo`,
  `tela.renderizador` e `tela.diagnostico`.
- Imprimir `[PASSOU] <nome>` ou `[FALHOU] <nome>` para cada verificação.
- Imprimir ao final: `Total de verificacoes`, `Passaram`, `Falharam`.
- Retornar código de saída 0 se todos passaram, 1 se algum falhou.
- Não usar `unittest`, `pytest` nem nenhum framework externo.

### Verificações obrigatórias

| Verificação | Critério |
|---|---|
| `gerar_diagnostico_tela()` não lança exceção | Chamada com padrão `"orquestrador"` retorna sem exceção |
| Retorno é `str` | `isinstance(resultado, str) is True` |
| Resultado começa com `"TELA: orquestrador"` | `resultado.startswith("TELA: orquestrador")` |
| Resultado contém `"SCHEMA: tela.v1"` | String presente no resultado |
| Resultado contém `"CABECALHO"` | String presente no resultado |
| Resultado contém `"titulo: Orquestrador"` | String presente no resultado |
| Resultado contém `"CORPO"` | String presente no resultado |
| Resultado contém `"arranjo: sobreposto"` | String presente no resultado |
| Resultado contém `"id: console_principal \| tipo: console"` | String presente no resultado |
| Resultado contém `"id: dashboard_info \| tipo: dashboard"` | String presente no resultado |
| Resultado contém `"id: lancador_principal \| tipo: lancador"` | String presente no resultado |
| Resultado contém `"BARRA_DE_MENUS"` | String presente no resultado |
| Resultado contém `"id: chip_esc"` | String presente no resultado |
| Resultado contém `"id: chip_ajuda"` | String presente no resultado |
| Resultado é determinístico | Duas chamadas produzem strings idênticas |
| Resultado bate com saída esperada do H-0003 | Igualdade estrita com `_EXPECTED_ORQUESTRADOR` |
| `python tela/diagnostico.py` imprime a mesma string | Anti-regressão do modo executável — verificar via `subprocess.run(["python", "tela/diagnostico.py"], capture_output=True)` que a saída stdout é idêntica à string retornada por `gerar_diagnostico_tela()` |
| Campos inertes não vazam na saída | `"origem_dados"`, `"bindings"`, `"filtros"`, `"tela_destino"`, `"regra_existencia"` não aparecem no resultado |
| `gerar_diagnostico_tela("orquestrador")` retorna o mesmo que `gerar_diagnostico_tela()` | Argumento explícito vs. padrão |
| Invariantes H-0001 preservados | `python tela/teste_loader.py` retorna código de saída 0 (verificar antes de importar `diagnostico`) |
| Invariantes H-0002 preservados | `python tela/teste_modelo.py` retorna código de saída 0 |
| Invariantes H-0003 preservados | `python tela/teste_renderizador.py` retorna código de saída 0 |

As três últimas verificações (invariantes H-0001, H-0002, H-0003) devem ser
executadas como subprocessos via `subprocess.run` **antes** dos demais testes,
para confirmar que o estado de partida está limpo. Esse é o único uso
autorizado de `subprocess` em `tela/teste_diagnostico.py`.

---

## Pré-condição obrigatória

Antes de criar qualquer arquivo, o executor deve confirmar que os invariantes
dos três handoffs anteriores estão todos passando:

```bash
python tela/teste_loader.py    # todas as 37 verificações passando
python tela/teste_modelo.py    # todas as 30 verificações passando
python tela/teste_renderizador.py  # todas as 39 verificações passando
```

Se qualquer verificação falhar, o executor deve parar imediatamente com
`BLOCKED` e registrar qual verificação falhou e em qual módulo.

---

## Critérios de aceite

Os critérios abaixo devem ser verificados um a um antes de considerar a
implementação concluída.

### Ponto de entrada e encadeamento

- [ ] `tela/diagnostico.py` define `gerar_diagnostico_tela(id_tela: str = "orquestrador") -> str`.
- [ ] `gerar_diagnostico_tela()` usa exatamente o encadeamento:
      `carregar_tela(None, id_tela)` → `construir_modelo(tela_raw)` → `renderizar_tela(modelo)`.
- [ ] `gerar_diagnostico_tela()` retorna `str` sem exceção para `id_tela="orquestrador"`.
- [ ] `gerar_diagnostico_tela()` não importa `json`, `os` nem `pathlib`.
- [ ] `gerar_diagnostico_tela()` não importa `subprocess`, não usa `exec` nem `eval`.
- [ ] `gerar_diagnostico_tela()` não executa ação, não ativa binding, não altera estado.
- [ ] `gerar_diagnostico_tela()` não altera `config/telas/orquestrador.json`.
- [ ] `sys.dont_write_bytecode = True` está definido antes dos imports de `tela.*`.

### Saída determinística

- [ ] O resultado é idêntico à saída esperada do H-0003 (igualdade estrita).
- [ ] Duas chamadas consecutivas a `gerar_diagnostico_tela()` retornam a mesma string.
- [ ] Campos inertes (`origem_dados`, `bindings`, `filtros`, `tela_destino`,
      `regra_existencia`) não aparecem no resultado.

### Modo executável

- [ ] `python tela/diagnostico.py` imprime a string no stdout e encerra com código 0.
- [ ] A saída de `python tela/diagnostico.py` é idêntica à string retornada por
      `gerar_diagnostico_tela()`.

### Teste integrado

- [ ] `tela/teste_diagnostico.py` existe e é executável via `python tela/teste_diagnostico.py`.
- [ ] `python tela/teste_diagnostico.py` retorna código de saída 0 com todas as verificações passando.
- [ ] O teste cobre o fluxo integrado (`carregar_tela` → `construir_modelo` → `renderizar_tela`)
      via `gerar_diagnostico_tela()`.
- [ ] O teste verifica igualdade estrita da saída com o expected output literal.
- [ ] O teste verifica que campos inertes não vazam na saída.

### Invariantes preservados

- [ ] `python tela/teste_loader.py` retorna código de saída 0 (37 verificações).
- [ ] `python tela/teste_modelo.py` retorna código de saída 0 (30 verificações).
- [ ] `python tela/teste_renderizador.py` retorna código de saída 0 (39 verificações).
- [ ] Nenhum `__pycache__` nem `.pyc` presente em `tela/` após execução dos testes.
- [ ] `config/telas/orquestrador.json` é JSON válido e não foi alterado.
- [ ] `config/estilo.json` é JSON válido e não foi alterado. (`config/estilo.json`
      **não faz parte** da cadeia de diagnóstico do H-0004 — o módulo
      `tela/diagnostico.py` não o consulta. A verificação é herdada como
      regressão documental dos ciclos anteriores e deve ser incluída no
      relatório IMP-0004 por completude.)

### Integridade documental e de escopo

- [ ] Nenhum contrato, ADR, nomenclatura, índice, handoff anterior, relatório anterior,
      `config/*.json`, `docs/INDICE.md`, `docs/backlog.md` ou `docs/issues.md`
      foi alterado.
- [ ] Somente `tela/diagnostico.py`, `tela/teste_diagnostico.py` e
      `docs/relatorios/IMP-0004-diagnostico-executavel-tela-raiz.md` foram criados.
- [ ] Nenhum arquivo fora do escopo autorizado foi criado ou alterado
      (`git status --short` confirma).

### Relatório

- [ ] `docs/relatorios/IMP-0004-diagnostico-executavel-tela-raiz.md` criado com
      resultado `APROVADO`, `APROVADO_COM_RESSALVAS` ou `BLOQUEADO`.

### QA final

- [ ] QA aprova o ciclo H-0004 ou registra bloqueio/ressalva com descrição objetiva.

---

## Comandos de verificação esperados

Executar a partir do diretório raiz do repositório de scripts
(`/home/tiago/Dropbox/UFRGS/Survey/versao_0_1/scripts`):

```bash
# 1. Integridade dos JSONs de configuração
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"

# 2. Invariantes de H-0001 preservados
python tela/teste_loader.py

# 3. Invariantes de H-0002 preservados
python tela/teste_modelo.py

# 4. Invariantes de H-0003 preservados
python tela/teste_renderizador.py

# 5. Teste integrado H-0004
python tela/teste_diagnostico.py

# 6. Ponto de entrada executável
python tela/diagnostico.py

# 7. Verificação de bytecode
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print

# 8. Estado do repositório
git status --short
git diff --stat
```

Todos os comandos devem produzir saída limpa. O relatório deve incluir a
saída real de cada um.

---

## Relatório de implementação obrigatório

O executor deve criar:

```
docs/relatorios/IMP-0004-diagnostico-executavel-tela-raiz.md
```

O relatório deve conter obrigatoriamente:

1. **Objetivo do H-0004**: o que foi especificado e o que foi implementado.
2. **Arquivos criados ou alterados**: lista completa com caminho relativo à raiz
   do repositório.
3. **Assinatura da função e módulos importados**: assinatura exata de
   `gerar_diagnostico_tela` e quais módulos são importados em
   `tela/diagnostico.py`.
4. **Saída real do pipeline** para `orquestrador.json`: reprodução literal da
   string retornada por `gerar_diagnostico_tela()`.
5. **Invariantes de H-0001, H-0002 e H-0003**: evidência de que as 37, 30 e 39
   verificações respectivas continuam passando (saída dos comandos).
6. **Comportamento fora de escopo preservado como inerte**: lista dos itens não
   implementados e por quê cada um foi mantido inerte.
7. **Pendências preservadas**: confirmação de que DOC-B008, DOC-B009 e campos
   `pendente` continuam sem execução.
8. **Saída real de todos os comandos de verificação**: cópia integral.
9. **Resultado final**: `APROVADO`, `APROVADO_COM_RESSALVAS` ou `BLOQUEADO`.

**O executor não deve fazer commit.**

---

## Condições de bloqueio

O executor deve parar imediatamente com `BLOCKED` ou
`ARCHITECTURE_REVIEW_REQUIRED` se:

1. Qualquer verificação de H-0001 (`python tela/teste_loader.py`) falhar.
2. Qualquer verificação de H-0002 (`python tela/teste_modelo.py`) falhar.
3. Qualquer verificação de H-0003 (`python tela/teste_renderizador.py`) falhar.
4. A implementação exigir criar arquivo fora dos listados em "Arquivos
   permitidos".
5. A implementação exigir alterar contrato, ADR, nomenclatura, índice,
   configuração, backlog, issues, handoff anterior ou relatório anterior.
6. A implementação exigir dependência externa além da stdlib Python.
7. A implementação exigir lógica além do encadeamento
   `carregar_tela` → `construir_modelo` → `renderizar_tela`.
8. A implementação exigir tomar decisão arquitetural não coberta por este
   handoff.
9. A saída de `gerar_diagnostico_tela()` divergir da saída esperada do H-0003
   por razão não prevista neste handoff.

---

## Instrução explícita ao executor

**Parar imediatamente com `BLOCKED` ou `ARCHITECTURE_REVIEW_REQUIRED`** se
qualquer condição de bloqueio for atingida.

**Não preencher lacunas** de especificação com decisão local.

**Não fazer commit** do resultado — o commit é responsabilidade do engenheiro.

**Não alterar** nenhum arquivo fora do escopo aprovado.

**Não implementar** nenhum item listado em "Fora de escopo".

**Não reimplementar** a lógica de loader, modelo ou renderizador — apenas
encadeá-los.
