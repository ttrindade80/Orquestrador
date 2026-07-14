---
name: H-0031-migracao-repositorio-orquestrador-raiz-independente
description: Formalizar migração estrutural do Orquestrador para repositório independente, concluir correções terminológicas e documentais ativas, e produzir evidência auditável da preservação funcional
metadata:
  type: handoff_implementacao
  status: READY_FOR_IMPLEMENTATION
  id: H-0031
  data_criacao: 2026-07-14
rastreabilidade:
  contrato_alvo: "docs/contratos/contrato_processo_desenvolvimento.md"
  adr_relacionadas: []
  issues_relacionadas: []
  handoffs_anteriores:
    - H-0030-catalogo-telas-utilizaveis
---

# H-0031 — Formalizar migração e corrigir referências ativas do Orquestrador

## Ordem de autoridade

1. `docs/contratos/contrato_processo_desenvolvimento.md`
2. Este handoff

Se houver conflito, bloquear e registrar a divergência.

## Contexto

### Base de caminhos

Raiz Git e diretório operacional coincidem em:

```
/home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador
```

Todos os caminhos deste handoff são relativos a essa raiz.

A origem histórica está em `/home/tiago/Dropbox/UFRGS/Survey/versao_0_1`
e **não deve ser alterada** em nenhuma circunstância.

### Estado comprovado antes deste handoff

- Branch: `master`; HEAD: `62fd501b82fe005d3d6782a4064bbcf6bb3530e5`
- Último commit: `feat: adiciona catalogo de telas utilizaveis`
- Repositório sem remoto configurado
- Reorganização física já executada e comprovada manualmente:
  - `config/` na raiz ✔
  - `docs/` na raiz ✔
  - `tela/` na raiz ✔
  - `scripts/` não existe fisicamente ✔
  - `referencias/` não existe fisicamente ✔
  - `texto/` não existe fisicamente ✔
  - `tree.txt` removido ✔
- Os 331 arquivos provenientes de `scripts/` comparados com a origem:
  zero divergências
- Suíte canônica executada na nova raiz: 1796/1796 testes passando ✔
- Stage vazio ✔

### O que já foi feito e não deve ser repetido

- Clonagem do repositório independente
- Movimentação física dos diretórios `config/`, `docs/` e `tela/`
- Remoção dos projetos externos (`referencias/`, `texto/` e arquivos isolados
  pertencentes a outros projetos)
- Remoção de `tree.txt`

## Escopo

**Objetivo:** Verificar a integridade do diff estrutural, executar as
correções terminológicas autorizadas em código e em documentação ativa, e
produzir evidência auditável da preservação funcional.

Esta migração não altera semântica, arquitetura funcional, comportamento de
tela nem contratos de domínio.

Não é necessária ADR para esta migração estrutural (decisão fechada).

### Arquivos permitidos — verificação estrutural (leitura e auditoria)

O implementador deve verificar — sem repetir — que o diff do repositório
contém exatamente:

- Remoção de todos os caminhos `scripts/config/**` com inclusão equivalente
  em `config/**`
- Remoção de todos os caminhos `scripts/docs/**` com inclusão equivalente
  em `docs/**`
- Remoção de todos os caminhos `scripts/tela/**` com inclusão equivalente
  em `tela/**`
- Remoção de `scripts/tree.txt` sem arquivo substituto
- Remoção dos arquivos pertencentes a projetos externos conforme levantamento
  manual já executado

### Arquivos permitidos — correções terminológicas de código

- `tela/diagnostico.py`
- `tela/loader.py`

Apenas comentários, docstrings e descrições de parâmetros que chamem a raiz
de "repositório de scripts". Nenhuma alteração em lógica, imports, funções,
nomes de variáveis ou cálculo de caminhos.

### Arquivos permitidos — atualizações documentais ativas

- `docs/INDICE.md`
- `docs/NOMENCLATURA.md`
- `docs/backlog.md`
- `docs/issues.md`
- `docs/build_docs/prompts.md`
- `docs/build_docs/instruction.md`
- `docs/build_docs/to_do.md`
- `docs/templates/TEMPLATE_HANDOFF_IMPLEMENTACAO.md`
- `docs/templates/TEMPLATE_RELATORIO_IMPL.md`
- `docs/adr/INDICE_ADR.md`
- `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_cabecalho.md`
- `docs/contratos/contrato_chip.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_console.md`
- `docs/contratos/contrato_estilo.md`
- `docs/contratos/contrato_json_barra_de_menus.md`
- `docs/contratos/contrato_json_cabecalho.md`
- `docs/contratos/contrato_json_console.md`
- `docs/contratos/contrato_json_dashboard.md`
- `docs/contratos/contrato_json_lancador.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/contratos/contrato_lancador.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/contratos/contrato_tela_json.md`

### Arquivo de saída autorizado

- `docs/relatorios/IMP-0031-migracao-repositorio-orquestrador-raiz-independente.md`

### Arquivos proibidos (leitura autorizada, alteração proibida)

- `config/**`
- Lógica executável em `tela/**` (exceto comentários/docstrings listados nas
  tarefas 5.1–5.3)
- `tela/teste_*.py`
- `tela/demo.py`
- `tela/explorar_barra_de_menus.py`
- ADRs fora da lista nominal acima
- Handoffs históricos (`docs/handoff/H-0001` … `H-0030`)
- Relatórios históricos (`docs/relatorios/IMP-0001` … `IMP-0030` e todos os
  `RELATORIO_*`)
- `/home/tiago/Dropbox/UFRGS/Survey/versao_0_1/**`
- `/home/tiago/Dropbox/UFRGS/Survey/versao_0_2/pipeline/**`
- `/home/tiago/Dropbox/UFRGS/Survey/versao_0_2/revisao/**`
- JSON de caminhos de integração — não criar neste ciclo

## Tarefas

### Tarefa 1 — Verificar estrutura física da raiz

Confirmar que a raiz contém somente `config/`, `docs/`, `tela/` e `.git`:

```zsh
ls -la /home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador/
```

Resultado esperado: exatamente `.git`, `config`, `docs`, `tela` — nada mais.

### Tarefa 2 — Verificar estado Git

```zsh
git log --oneline -1
git remote -v
```

Resultados esperados:

- `62fd501 feat: adiciona catalogo de telas utilizaveis`
- Saída vazia para `remote -v` (sem remoto)

### Tarefa 3 — Confirmar ausência de diretórios externos

Verificar que não existem fisicamente:

- `scripts/`
- `referencias/`
- `texto/`
- `tree.txt`

### Tarefa 4 — Verificar integridade das 8 expressões `parent.parent`

As oito ocorrências abaixo devem permanecer intactas e inalteradas:

```zsh
grep -rn "parent\.parent" tela/ --include="*.py"
```

Resultado esperado — exatamente 8 linhas:

| Arquivo | Linha | Expressão |
|---|---|---|
| `tela/loader.py` | 142 | `return Path(__file__).resolve().parent.parent` |
| `tela/teste_modelo.py` | 26 | `_BASE_PADRAO = Path(__file__).resolve().parent.parent` |
| `tela/teste_diagnostico.py` | 36 | `_BASE_PADRAO = Path(__file__).resolve().parent.parent` |
| `tela/teste_explorar_barra_de_menus.py` | 18 | `_BASE = Path(__file__).resolve().parent.parent` |
| `tela/explorar_barra_de_menus.py` | 25 | `_BASE = Path(__file__).resolve().parent.parent` |
| `tela/teste_loader.py` | 29 | `_BASE_PADRAO = Path(__file__).resolve().parent.parent` |
| `tela/teste_demo.py` | 94 | `_BASE_PADRAO = Path(__file__).resolve().parent.parent` |
| `tela/teste_renderizador.py` | 44 | `_BASE_PADRAO = Path(__file__).resolve().parent.parent` |

Se a contagem ou as localizações diferirem, bloquear e registrar.

### Tarefa 5 — Executar correções terminológicas de código

Corrigir somente os três trechos abaixo. Nenhuma outra linha dos dois
arquivos deve ser alterada.

#### 5.1 `tela/diagnostico.py` — linha 28

Trecho atual (dentro da docstring do módulo):

```
  repositorio de scripts ao sys.path antes de importar tela.*.
```

Substituir por:

```
  repositorio do Orquestrador ao sys.path antes de importar tela.*.
```

**Preservar sem alteração:**

- Variável `_raiz_scripts` nas linhas 44–46 — é nome de variável, não
  docstring, e está fora do escopo de correção
- Qualquer expressão `parent.parent`

#### 5.2 `tela/loader.py` — linha 141 (docstring de `_caminho_padrao_base`)

Trecho atual:

```python
    """Diretorio raiz do repositorio de scripts (pai de tela/)."""
```

Substituir por:

```python
    """Diretorio raiz do repositorio do Orquestrador (pai de tela/)."""
```

#### 5.3 `tela/loader.py` — linha 570 (descrição do parâmetro `caminho_base`)

Trecho atual:

```
        caminho_base: diretorio raiz do repositorio de scripts. Se None,
```

Substituir por:

```
        caminho_base: diretorio raiz do repositorio do Orquestrador. Se None,
```

### Tarefa 6 — Executar atualizações documentais ativas

Para cada arquivo da lista autorizada, aplicar as correções da seção 6.1
quando encontradas, e preservar tudo da seção 6.2.

A correção deve ser **seletiva por ocorrência**, nunca por substituição global
de substring.

#### 6.1 O que atualizar

| Padrão a corrigir | Substituição |
|---|---|
| Caminho operacional `scripts/docs/...` | `docs/...` |
| Caminho operacional `scripts/config/...` | `config/...` |
| Caminho operacional `scripts/tela/...` | `tela/...` |
| `scripts/modulo_exemplo/...` como exemplo de caminho operacional | `tela/modulo_exemplo/` ou equivalente relativo à nova raiz |
| Afirmação de que `scripts/` é o diretório operacional atual | remover ou substituir pela nova raiz |
| Afirmação de que a raiz Git fica acima do diretório operacional | corrigir para raiz Git = raiz operacional |
| Metadado `scope: scripts` | `scope: orquestrador` |
| Metadado `name: indice-scripts` | `name: indice-orquestrador` |
| Metadado `name: backlog-scripts` | `name: backlog-orquestrador` |
| Metadado `name: issues-scripts` | `name: issues-orquestrador` |
| Diagrama de árvore que mostra `scripts/` como raiz operacional ativa | atualizar para mostrar `config/`, `docs/`, `tela/` diretamente na raiz |
| Descrição que trata o projeto como "coleção de scripts" quando o contexto indica identidade do projeto | substituir por "Orquestrador" ou equivalente |

#### 6.2 O que preservar

- A palavra "scripts" com sentido genérico de programas ou processos
  executáveis
- Referências históricas presentes em: handoffs antigos, relatórios antigos,
  registros de implementação, tabelas de evidência histórica e planos
  executados dentro de ADRs
- Em especial, **não reescrever referências históricas de caminhos no corpo
  da ADR-0020** para refletir a nova estrutura
- Decisões funcionais e normativas dos contratos
- JSONs, testes e lógica do produto
- Ocorrências de "scripts/processos internos" em sentido genérico em
  `tela/demo.py` (fora do escopo de correção de código; ausência de evidência
  textual objetiva de que afirmam a existência da antiga pasta)

#### 6.3 Critério de ambiguidade

Quando uma ocorrência de "scripts" não puder ser classificada objetivamente
como uso genérico legítimo, referência histórica legítima ou caminho
operacional a corrigir, registrar como "bloqueio não resolvido" no relatório
e **não alterar**.

### Tarefa 7 — Executar suíte canônica

A partir da raiz `/home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador`:

```zsh
PYTHONDONTWRITEBYTECODE=1 python3 tela/teste_loader.py
PYTHONDONTWRITEBYTECODE=1 python3 tela/teste_modelo.py
PYTHONDONTWRITEBYTECODE=1 python3 tela/teste_renderizador.py
PYTHONDONTWRITEBYTECODE=1 python3 tela/teste_demo.py
PYTHONDONTWRITEBYTECODE=1 python3 tela/teste_diagnostico.py
PYTHONDONTWRITEBYTECODE=1 python3 tela/teste_explorar_barra_de_menus.py
```

Todos os seis scripts devem retornar código de saída zero.

Contagem de referência: 1796/1796.

### Tarefa 8 — Verificar `git diff --check`

```zsh
git diff --check
```

Resultado esperado: saída vazia.

### Tarefa 9 — Verificar origem histórica intacta

```zsh
git -C /home/tiago/Dropbox/UFRGS/Survey/versao_0_1 status
git -C /home/tiago/Dropbox/UFRGS/Survey/versao_0_1 log --oneline -1
```

Resultado esperado:

- `nothing to commit, working tree clean`
- `62fd501 feat: adiciona catalogo de telas utilizaveis`

### Tarefa 10 — Manter stage vazio

O stage deve permanecer vazio durante toda a implementação e o QA.

O fechamento manual (stage + commit) será feito pelo gerente após o QA.

**Não executar `git add` nem `git commit` neste handoff.**

### Tarefa 11 — Produzir relatório

Criar:

```
docs/relatorios/IMP-0031-migracao-repositorio-orquestrador-raiz-independente.md
```

Usar `docs/templates/TEMPLATE_RELATORIO_IMPL.md` como base.

O relatório deve obrigatoriamente:

1. Listar todos os arquivos alterados neste handoff
2. Apresentar evidência por critério de aceite
3. Listar **todas** as ocorrências de `scripts/` nos documentos ativos
   auditados e classificar cada uma como:
   - ocorrência corrigida
   - uso genérico legítimo
   - referência histórica legítima
   - bloqueio não resolvido
4. Confirmar que nenhuma referência operacional ativa permanece como caminho
   antigo válido após a implementação
5. Confirmar que as 8 expressões `parent.parent` estão intactas nos arquivos
   e linhas listados na Tarefa 4
6. Registrar resultado dos 6 scripts de teste com contagem de casos e código
   de saída de cada um

## Critérios de aceite

| # | Critério | Evidência esperada |
|---|---|---|
| 1 | Raiz Git = `/home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador` | `git rev-parse --show-toplevel` |
| 2 | Raiz contém somente `config/`, `docs/`, `tela/` além de `.git` | `ls -la` na raiz |
| 3 | `scripts/`, `referencias/`, `texto/` e `tree.txt` não existem fisicamente | `ls` confirma ausência |
| 4 | Sem remoto configurado | `git remote -v` produz saída vazia |
| 5 | Origem histórica limpa em `62fd501` | `git -C versao_0_1 log` e `status` limpo |
| 6 | Stage vazio durante implementação e QA | `git status --short` |
| 7 | As 8 expressões `parent.parent` permanecem inalteradas | `grep -rn "parent\.parent" tela/ --include="*.py"` retorna exatamente 8 linhas nos arquivos e linhas listados na Tarefa 4 |
| 8 | Nenhuma alteração funcional em código | Diff de `tela/` contém somente os três trechos de comentários/docstrings listados nas tarefas 5.1–5.3 |
| 9 | Referências operacionais ativas usam caminhos relativos à nova raiz | Relatório confirma por arquivo |
| 10 | Referências históricas preservadas e justificadas no relatório | Relatório com classificação completa |
| 11 | Relatório classifica todas as ocorrências de `scripts/` nos documentos ativos | Nenhum arquivo autorizado omitido |
| 12 | Nenhuma referência operacional ativa classificada como caminho antigo válido | Relatório |
| 13 | `git diff --check` sem saída | Saída do comando |
| 14 | Suíte canônica completa aprovada | 1796/1796 — seis scripts com código de saída zero |
| 15 | Relatório criado no caminho nominal | `docs/relatorios/IMP-0031-migracao-repositorio-orquestrador-raiz-independente.md` existe |

## Testes obrigatórios

Executar a partir da raiz `/home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador`:

```zsh
PYTHONDONTWRITEBYTECODE=1 python3 tela/teste_loader.py
PYTHONDONTWRITEBYTECODE=1 python3 tela/teste_modelo.py
PYTHONDONTWRITEBYTECODE=1 python3 tela/teste_renderizador.py
PYTHONDONTWRITEBYTECODE=1 python3 tela/teste_demo.py
PYTHONDONTWRITEBYTECODE=1 python3 tela/teste_diagnostico.py
PYTHONDONTWRITEBYTECODE=1 python3 tela/teste_explorar_barra_de_menus.py
```

Contagem de referência: 1796/1796 — seis scripts com código de saída zero.

## Saída esperada

Produzir relatório:

```
docs/relatorios/IMP-0031-migracao-repositorio-orquestrador-raiz-independente.md
```

Usando `docs/templates/TEMPLATE_RELATORIO_IMPL.md`.
