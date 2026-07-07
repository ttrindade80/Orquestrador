---
name: H-0001-loader-validador-tela-json
description: Handoff de implementação do loader e validador mínimo do tela.json para a tela raiz do Orquestrador
metadata:
  type: handoff_implementacao
  status: READY_FOR_IMPLEMENTATION
  id: H-0001
  data_criacao: 2026-07-07
rastreabilidade:
  contrato_alvo: "docs/contratos/contrato_tela_json.md"
  adr_relacionadas:
    - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
    - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
  issues_relacionadas: []
  handoffs_anteriores: []
---

# H-0001 — Loader e validador mínimo de tela JSON

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
10. Este handoff

Se houver conflito entre este handoff e qualquer um dos artefatos acima,
bloquear e registrar a divergência. Este handoff não pode criar regra nova que
contradiga os contratos acima.

---

## Contexto

A Fase 0 documental foi concluída no commit `b7532d5`. O arquivo
`config/telas/orquestrador.json` existe, é sintaticamente válido e segue o
contrato `contrato_tela_json.md` na sua estrutura macro.

Até o momento, **não existe nenhum código Python neste repositório**. Este
handoff é o primeiro passo de implementação: criar o módulo mínimo capaz de
localizar, carregar e validar a estrutura macro do `tela.json` da tela raiz.

O renderer completo, a navegação, a execução de ações e a renderização visual
são escopo futuro, fora deste handoff.

### Estado atual de pendências documentais relevantes

O arquivo `config/telas/orquestrador.json` contém campos marcados como
pendentes:

- **DOC-B008**: tipos internos de item de `console` não definidos; campo
  `origem_dados` e `regra_geracao_itens` do `console_principal` marcados como
  `pendente`.
- **DOC-B009**: registry completo de ações e tipos de chip não fechado; ações
  dos chips são referências declarativas conceituais provisórias.
- **`chip_estilo.tela_destino`**: marcado como `pendente` — tela de destino
  não documentada.
- **`lancador_principal.itens`**: lista vazia — itens e `tela_destino`
  pendentes de definição das telas do sistema.
- **`bindings`**: declarados apenas como nota pendente DOC-B008/DOC-B009.
- **`referencias_de_acoes`**: status `pendente_DOC-B009`.

O loader implementado neste handoff **não deve tratar essas pendências como
erro**. Elas são declaração inerte no JSON — o loader as carrega e preserva
em memória sem executar, resolver, validar funcionalmente ou rejeitar por
incompletude, salvo se o JSON estiver estruturalmente inválido conforme
`contrato_tela_json.md`.

---

## Objetivo

Implementar um loader/validador mínimo capaz de:

1. localizar `config/telas/orquestrador.json` a partir de um caminho base
   configurável;
2. carregar o conteúdo do arquivo;
3. validar que o conteúdo é JSON sintaticamente válido;
4. validar a estrutura macro conforme `contrato_tela_json.md` seção 3:
   presença obrigatória de `schema`, `id`, `cabecalho`, `corpo` e
   `barra_de_menus`;
5. validar que o campo `id` existe e é não vazio;
6. validar que para a tela raiz o `id` é exatamente `"orquestrador"`;
7. validar que o nome base do arquivo (sem extensão) coincide com o `id`
   declarado internamente (ADR-0009 seção 3);
8. validar presença de `cabecalho`;
9. validar presença de `corpo`;
10. validar presença de `barra_de_menus`;
11. validar que `corpo.elementos` existe e é uma lista;
12. validar que cada elemento de `corpo.elementos` possui campo `id`;
13. validar que cada elemento de `corpo.elementos` possui campo `tipo`;
14. validar que o valor de `tipo` em cada elemento pertence à taxonomia
    fechada: `console`, `lancador`, `dashboard` (contrato_composicao_corpo.md
    seção 3; contrato_tela_json.md seção 8);
15. produzir uma representação interna simples e auditável da tela carregada;
16. expor um comando de diagnóstico textual que permita verificar o loader.

---

## Fontes normativas

| Artefato | Seções relevantes para este handoff |
|---|---|
| `docs/contratos/contrato_tela_json.md` | 3 (estrutura macro), 4 (schema), 5 (id), 7 (cabecalho), 8 (corpo), 18 (barra_de_menus), 23 (validação) |
| `docs/contratos/contrato_composicao_corpo.md` | 3 (taxonomia de tipos), 4 (campos declarados), 4.1 (tipos dos elementos) |
| `docs/adr/ADR-0009-caminho-formato-jsons-tela.md` | 3 (nome do arquivo = id), 4 (id canônico orquestrador), 2 (caminho config/telas/) |
| `docs/adr/ADR-0008-modelo-configuracao-por-tela.md` | 2 (estrutura macro fixa), 6 (estilo.json restrito a aparência global) |
| `docs/NOMENCLATURA.md` | 2 (regiões macro da tela), 2.1 (tipos de objeto do corpo) |

---

## Escopo permitido

### Objetivo da implementação

O implementador deve criar um módulo Python mínimo que carregue e valide a
estrutura macro do `tela.json`.

### Arquivos permitidos para criação ou alteração

O repositório não possui código Python. O implementador deve criar:

```
tela/loader.py          — módulo loader/validador
tela/__init__.py        — marcador de pacote (pode ser vazio)
tela/teste_loader.py    — script de diagnóstico verificável
docs/relatorios/IMP-0001-loader-validador-tela-json.md  — relatório de implementação
```

Esses caminhos são relativos à raiz do repositório de scripts
(`/home/tiago/Dropbox/UFRGS/Survey/versao_0_1/scripts`).

Se a estrutura real do repositório durante a implementação mostrar convenção
diferente já estabelecida (ex.: pasta `src/`, `orquestrador/`), o
implementador deve parar e registrar bloqueio antes de criar estrutura nova.
Não inventar estrutura de módulo sem verificar primeiro.

**Somente os arquivos listados acima podem ser criados ou alterados.**

---

## Fora de escopo — proibições explícitas

O implementador **não pode** implementar nem iniciar:

- renderização visual completa de qualquer região da tela;
- navegação real entre telas;
- execução de ações declaradas nos chips;
- registry de ações (`referencias_de_acoes`);
- resolução de `bindings`;
- ativação de filtros funcionais (`filtros[]`);
- paginação funcional;
- seleção funcional;
- alteração de estilo em runtime;
- dashboard dinâmico com dados reais;
- processamento de dados reais;
- validação funcional de `tela_destino` nos chips ou itens de `lancador`;
- validação funcional de chips específicos;
- validação funcional de ações provisórias;
- validação interna completa dos itens de `console` (tipos internos de item
  são pendência DOC-B008);
- qualquer comportamento que dependa de DOC-B008 estar fechado;
- qualquer comportamento que dependa de DOC-B009 estar fechado;
- escrita de estado de runtime no JSON;
- alteração de `config/telas/orquestrador.json`;
- alteração de `config/estilo.json`;
- alteração de qualquer arquivo em `config/`;
- alteração de qualquer arquivo de configuração ou contrato;
- alteração de qualquer arquivo em `docs/` **exceto** o relatório de
  implementação `docs/relatorios/IMP-0001-loader-validador-tela-json.md`;
- em particular, são estritamente proibidos:
  - `docs/contratos/*`
  - `docs/adr/*`
  - `docs/handoff/*`
  - `docs/NOMENCLATURA.md`
  - `docs/INDICE.md`
  - `docs/backlog.md`
  - `docs/issues.md`

### Regra específica para DOC-B008 e DOC-B009

Campos como `bindings`, `referencias_de_acoes`, `chips` individuais,
`tela_destino`, `origem_dados` com valor `"pendente"`, ações provisórias e
itens vazios de `lancador` devem ser **carregados e preservados em memória**
como dados inertes.

O loader **não pode**:
- executar ou resolver esses campos;
- validar funcionalmente esses campos;
- rejeitar o JSON por causa dessas pendências, salvo se a **estrutura macro**
  obrigatória estiver ausente.

Se durante a implementação surgir necessidade de decisão sobre DOC-B008 ou
DOC-B009, o implementador deve **parar imediatamente** e retornar status
`BLOCKED` com descrição do bloqueio. Não tomar decisão local.

---

## Comportamento esperado

### Caminho canônico do arquivo

```
config/telas/orquestrador.json
```

O loader deve aceitar o caminho base como parâmetro (não hardcodar o caminho
absoluto do sistema de arquivos). O caminho base padrão é o diretório raiz do
repositório de scripts.

### Validações obrigatórias (em ordem)

1. **Arquivo existe**: o arquivo `config/telas/orquestrador.json` deve estar
   acessível. Ausência gera `TelaArquivoNaoEncontrado`.

2. **JSON válido**: o conteúdo deve ser JSON sintaticamente válido. Erro de
   sintaxe gera `TelaJsonInvalido`.

3. **Campo `schema` presente**: o campo `schema` deve existir. Ausência gera
   `TelaCampoObrigatorioAusente(campo="schema")`.

4. **Campo `id` presente e não vazio**: o campo `id` deve existir e não pode
   ser string vazia. Ausência ou valor vazio gera
   `TelaCampoObrigatorioAusente(campo="id")`.

5. **`id` coincide com nome base do arquivo**: o valor de `id` deve coincidir
   exatamente com o nome base do arquivo sem extensão (ADR-0009 seção 3). Para
   `orquestrador.json`, o `id` deve ser `"orquestrador"`. Divergência gera
   `TelaIdNaoCoincideComArquivo`.

6. **`id` da tela raiz**: para a tela raiz, o `id` deve ser exatamente
   `"orquestrador"`. Valor diferente gera `TelaIdIncorreto`.

7. **Campo `cabecalho` presente**: o campo `cabecalho` deve existir. Ausência
   gera `TelaCampoObrigatorioAusente(campo="cabecalho")`.

8. **Campo `corpo` presente**: o campo `corpo` deve existir. Ausência gera
   `TelaCampoObrigatorioAusente(campo="corpo")`.

9. **Campo `barra_de_menus` presente**: o campo `barra_de_menus` deve existir.
   Ausência gera `TelaCampoObrigatorioAusente(campo="barra_de_menus")`.

10. **`corpo.elementos` presente e é lista**: o campo `corpo.elementos` deve
    existir e ser uma lista (pode ser lista vazia). Ausência gera
    `TelaCampoObrigatorioAusente(campo="corpo.elementos")`. Tipo incorreto
    gera `TelaEstruturaInvalida`.

11. **Cada elemento tem `id`**: todo objeto em `corpo.elementos` deve ter
    campo `id`. Ausência gera `TelaElementoSemId(indice=N)`.

12. **Cada elemento tem `tipo`**: todo objeto em `corpo.elementos` deve ter
    campo `tipo`. Ausência gera `TelaElementoSemTipo(indice=N, id=X)`.

13. **`tipo` pertence à taxonomia**: o valor de `tipo` em cada elemento deve
    ser um de: `"console"`, `"lancador"`, `"dashboard"`. Valor desconhecido
    gera `TelaTipoDesconhecido(tipo=X, id=Y)`.

### Campos carregados como declaração inerte

Os seguintes campos devem ser carregados e preservados em memória sem
validação funcional:

- `metadados`
- `filtros`
- `bindings`
- `referencias_de_acoes`
- `corpo.elementos[*].origem_dados`
- `corpo.elementos[*].regra_geracao_itens`
- `barra_de_menus.chips` (lista inteira — carregada como lista de dicts)
- `lancador_principal.itens` (pode estar vazio)
- qualquer campo com valor `"pendente"`

### Representação interna mínima

Após validação bem-sucedida, o loader deve retornar (ou construir internamente)
um objeto com, no mínimo:

```python
{
    "id": str,                  # valor do campo id do JSON
    "schema": str,              # valor do campo schema do JSON
    "cabecalho": dict,          # conteúdo completo de cabecalho
    "corpo": {
        "arranjo": str | None,  # valor de corpo.arranjo se existir, None caso contrário
        "elementos": [
            {
                "id": str,
                "tipo": str,    # um de: console, lancador, dashboard
                # demais campos carregados como-está (inertes)
            }
        ]
    },
    "barra_de_menus": dict,     # conteúdo completo carregado como-está
    "_raw": dict,               # conteúdo completo do JSON original (para diagnóstico)
}
```

A estrutura acima é sugestão mínima. O implementador pode usar dataclasses,
TypedDict ou dicionário simples, desde que os campos mínimos estejam
acessíveis e auditáveis. Nenhuma regra arquitetural nova deve ser introduzida.

---

## Erros esperados e mensagens verificáveis

O loader deve usar exceções ou retornar códigos de erro com mensagens
descritivas. As mensagens abaixo são referências — o implementador pode
escolher a forma exata, desde que a mensagem identifique claramente o campo
e o motivo.

| Situação | Identificador sugerido | Mensagem mínima verificável |
|---|---|---|
| Arquivo não encontrado | `TelaArquivoNaoEncontrado` | `"Arquivo não encontrado: config/telas/orquestrador.json"` |
| JSON sintaticamente inválido | `TelaJsonInvalido` | `"JSON inválido em: config/telas/orquestrador.json — <detalhe do erro>"` |
| Campo obrigatório ausente | `TelaCampoObrigatorioAusente` | `"Campo obrigatório ausente: <nome_do_campo>"` |
| `id` não coincide com nome do arquivo | `TelaIdNaoCoincideComArquivo` | `"id interno '<id>' não coincide com nome do arquivo '<basename>'"` |
| `id` incorreto para tela raiz | `TelaIdIncorreto` | `"id esperado para tela raiz: 'orquestrador'; encontrado: '<valor>'"` |
| Elemento sem `id` | `TelaElementoSemId` | `"Elemento na posição <N> não possui campo 'id'"` |
| Elemento sem `tipo` | `TelaElementoSemTipo` | `"Elemento '<id>' não possui campo 'tipo'"` |
| `tipo` desconhecido | `TelaTipoDesconhecido` | `"Tipo desconhecido '<tipo>' em elemento '<id>'; tipos válidos: console, lancador, dashboard"` |
| Corpo sem `elementos` | `TelaEstruturaInvalida` | `"'corpo.elementos' ausente ou não é uma lista"` |

---

## Critérios de aceite

Os critérios abaixo devem ser verificados um a um antes de considerar a
implementação concluída.

### Funcionamento correto

- [ ] `config/telas/orquestrador.json` é carregado sem erro quando o arquivo
      é válido.
- [ ] JSON inválido gera erro identificável com mensagem clara.
- [ ] Campo `id` ausente gera erro com mensagem identificando o campo.
- [ ] `id` diferente de `"orquestrador"` para a tela raiz gera erro com
      mensagem identificando o valor encontrado.
- [ ] Nome base do arquivo diferente do `id` interno gera erro com mensagem
      comparando os dois valores.
- [ ] Ausência de `cabecalho` gera erro com mensagem identificando o campo.
- [ ] Ausência de `corpo` gera erro com mensagem identificando o campo.
- [ ] Ausência de `barra_de_menus` gera erro com mensagem identificando o
      campo.
- [ ] Ausência de `corpo.elementos` gera erro com mensagem identificando o
      campo.
- [ ] Elemento de corpo sem `id` gera erro com índice do elemento.
- [ ] Elemento de corpo sem `tipo` gera erro com identificação do elemento.
- [ ] Tipo de corpo desconhecido gera erro identificando o valor inválido.
- [ ] Tipos `console`, `dashboard` e `lancador` são aceitos como válidos.
- [ ] `chips`, `bindings`, `referencias_de_acoes` e `filtros` são carregados
      como declaração inerte, sem validação funcional.
- [ ] `lancador_principal.itens` vazio não gera erro.
- [ ] `tela_destino` com valor `"pendente"` não gera erro.
- [ ] `origem_dados` com valor `"pendente"` não gera erro.

### Garantias de não alteração

- [ ] Nenhuma ação real é executada pelo loader.
- [ ] Nenhum binding é ativado.
- [ ] Nenhum `tela_destino` pendente é resolvido.
- [ ] Nenhum estado de runtime é gravado no JSON.
- [ ] `config/telas/orquestrador.json` não é alterado.
- [ ] `config/estilo.json` não é alterado.
- [ ] Nenhum arquivo em `config/` é alterado.
- [ ] Nenhum arquivo em `docs/contratos/`, `docs/adr/`, `docs/handoff/`,
      `docs/NOMENCLATURA.md`, `docs/INDICE.md`, `docs/backlog.md` ou
      `docs/issues.md` é alterado.
- [ ] Nenhum arquivo fora de `tela/loader.py`, `tela/__init__.py`,
      `tela/teste_loader.py` e
      `docs/relatorios/IMP-0001-loader-validador-tela-json.md`
      é criado ou alterado.

### Diagnóstico verificável

- [ ] `tela/teste_loader.py` pode ser executado via `python tela/teste_loader.py`
      (ou equivalente) e produz saída textual indicando sucesso ou falha para
      cada critério de aceite testável.
- [ ] A saída do diagnóstico mostra o `id`, o `schema`, os `tipos` dos
      elementos de corpo e o status de carregamento.

---

## Comandos de verificação

Executar a partir do diretório raiz do repositório de scripts
(`/home/tiago/Dropbox/UFRGS/Survey/versao_0_1/scripts`):

```bash
# Verificar integridade dos JSONs de configuração
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
python -m json.tool config/estilo.json >/dev/null && echo "estilo.json OK"

# Verificar que nenhum arquivo fora do escopo foi alterado
git status --short
git diff --stat

# Executar diagnóstico do loader (a ser criado pelo implementador)
python tela/teste_loader.py
```

O implementador deve criar `tela/teste_loader.py` de modo que sua execução
cubra todos os critérios de aceite verificáveis via código.

O relatório de implementação deve incluir a saída real dos comandos acima
executados pelo implementador.

---

## Estrutura de módulo proposta

Como não existe código Python no repositório, o implementador deve criar os
seguintes arquivos, todos dentro de `tela/`:

```
tela/
  __init__.py        — pode ser vazio
  loader.py          — loader e validador
  teste_loader.py    — diagnóstico
```

### Responsabilidades de cada arquivo

**`tela/loader.py`**:

- função ou classe `carregar_tela(caminho_base, id_tela)` que:
  - constrói o caminho `config/telas/<id_tela>.json`;
  - abre e lê o arquivo;
  - analisa o JSON;
  - executa as validações obrigatórias na ordem definida neste handoff;
  - retorna a representação interna mínima se válido;
  - lança exceção ou retorna erro estruturado se inválido;
- definição das exceções ou classes de erro enumeradas na seção de erros;
- constante `TIPOS_CORPO_VALIDOS = {"console", "lancador", "dashboard"}`.

**`tela/teste_loader.py`**:

- executa `carregar_tela` com o arquivo `config/telas/orquestrador.json`;
- imprime resultado de cada verificação (PASSOU / FALHOU);
- cria arquivos JSON temporários mínimos para testar os casos de erro
  (arquivo ausente, JSON inválido, campo faltando, tipo inválido, id
  divergente, etc.);
- remove os arquivos temporários ao fim;
- retorna código de saída 0 se todos os critérios passaram, 1 se algum falhou.

O implementador não deve usar bibliotecas externas além da biblioteca padrão
do Python. `json`, `os`, `pathlib` e `sys` são suficientes e permitidos.

---

## Riscos e bloqueios

| Risco | Condição de bloqueio |
|---|---|
| Decisão sobre DOC-B008 | Se a implementação exigir validar tipos internos de item de `console`, parar e registrar bloqueio |
| Decisão sobre DOC-B009 | Se a implementação exigir validar ações ou chips específicos, parar e registrar bloqueio |
| Estrutura de módulo diferente da proposta | Se o repositório mostrar convenção estabelecida diferente, parar e registrar bloqueio antes de criar arquivos |
| Campo de contrato ausente ou contradição | Se contrato e JSON contradisserem este handoff, parar e registrar bloqueio |
| Necessidade de estado global ou singleton | Este handoff não autoriza. Parar e registrar bloqueio |

---

## Instrução explícita ao implementador (GLM/OpenCode)

**Você deve parar imediatamente e retornar status `BLOCKED` se:**

1. A implementação exigir decisão sobre qualquer campo pendente de DOC-B008
   ou DOC-B009 além do que está descrito neste handoff.
2. Você precisar criar arquivo fora de `tela/loader.py`, `tela/__init__.py`,
   `tela/teste_loader.py` ou
   `docs/relatorios/IMP-0001-loader-validador-tela-json.md`.
3. Você encontrar convenção de módulo diferente da proposta já estabelecida
   no repositório.
4. Você precisar introduzir dependência externa (além da stdlib Python).
5. Você encontrar contradição entre este handoff e um dos contratos listados
   na seção "Ordem de autoridade".
6. Você precisar tomar qualquer decisão arquitetural que não esteja coberta
   por este handoff.

**Você não deve:**

- preencher lacunas de especificação com decisão local;
- usar inferência sobre o sistema para além do que os contratos permitem;
- fazer commit do resultado;
- alterar qualquer arquivo fora do escopo aprovado.

---

## Formato do relatório de implementação esperado

O implementador deve produzir o arquivo:

```
docs/relatorios/IMP-0001-loader-validador-tela-json.md
```

usando o template `docs/templates/TEMPLATE_RELATORIO_IMPL.md`.

O relatório deve conter:

- lista de arquivos criados (com caminho completo relativo à raiz do
  repositório);
- saída real dos comandos de verificação executados;
- status de cada critério de aceite (PASSOU / FALHOU / NÃO VERIFICADO);
- descrição de qualquer desvio do handoff, com justificativa;
- status final: IMPLEMENTADO ou BLOCKED;
- se BLOCKED: descrição completa do bloqueio e do que falta para desbloquear.

**O implementador não deve fazer commit.**

---

## Instrução sobre commit

**Nenhum commit deve ser feito pelo implementador.** O commit é responsabilidade
do Engenheiro após revisão e aprovação do relatório de implementação e do
handoff de QA.
